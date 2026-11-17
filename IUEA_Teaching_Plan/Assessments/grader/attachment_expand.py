"""Find the student's notebook/README inside ZIPs and GitHub links in HTML uploads.

Nothing here executes student content. ZIP members are size-capped and path-checked.
Only public github.com repositories are read (JSON tree listing plus raw file
downloads, text/notebook files only). Downloads are cached by URL so reruns are
repeatable and work offline. The original upload's hash stays the receipt evidence.
"""
import hashlib
import html as htmllib
import json
import re
import urllib.request
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
CACHE_DIR=HERE.parent/'assessment_operations'/'private'/'expanded_attachments'
MAX_MEMBER=5*1024*1024
MAX_FILES=6
KEEP=('.ipynb','.md','.txt')
SKIP_PART=re.compile(r'^(\.|__MACOSX)|checkpoint',re.I)
GITHUB=re.compile(r'https?://(?:www\.)?github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(?:/(?:tree|blob)/([\w.\-/%]+))?(?=[\s"\'<>)#?]|$)',re.I)
COLAB=re.compile(r'https?://colab\.research\.google\.com/github/([\w.-]+)/([\w.-]+)/blob/([\w.\-/%]+)',re.I)
OWNER_SKIP={'features','about','pricing','login','orgs','settings','sponsors','marketplace','topics'}


def _sha(data):return hashlib.sha256(data).hexdigest()


def _info(path,name,origin):
    data=Path(path).read_bytes()
    return dict(path=Path(path),sha256=_sha(data),original_name=name,origin=origin,export_name=Path(path).name)


def zip_members(archive,cache=CACHE_DIR):
    """Notebook/README members of a ZIP, written to the cache. Returns info dicts."""
    archive=Path(archive);out=[]
    try:z=zipfile.ZipFile(archive)
    except zipfile.BadZipFile:return out
    base=Path(cache)/('zip_'+_sha(archive.read_bytes())[:24]);base.mkdir(parents=True,exist_ok=True)
    with z:
        infos=[i for i in z.infolist() if not i.is_dir()]
        if len(infos)>500:return out
        for i,m in enumerate(infos):
            name=Path(m.filename)
            if name.is_absolute() or '..' in name.parts or any(SKIP_PART.search(p) for p in name.parts):continue
            if name.suffix.lower() not in KEEP or m.file_size>MAX_MEMBER:continue
            if len(out)>=MAX_FILES:break
            target=base/f'{i:03d}_{re.sub(r"[^A-Za-z0-9._-]","_",name.name)}'
            target.write_bytes(z.read(m))
            out.append(_info(target,name.name,'ZIP '+archive.name))
    return out


def github_links(path):
    """(owner, repo, ref_or_path) for GitHub links found in an HTML/URL file."""
    try:text=Path(path).read_bytes().decode('utf-8',errors='replace')
    except OSError:return []
    text=htmllib.unescape(text)
    found=[];seen=set()
    for m in COLAB.finditer(text):
        k=(m.group(1),m.group(2),m.group(3))
        if k not in seen:seen.add(k);found.append(k)
    for m in GITHUB.finditer(text):
        if m.group(1).lower() in OWNER_SKIP:continue
        k=(m.group(1),m.group(2),m.group(3) or '')
        if k not in seen:seen.add(k);found.append(k)
    return found[:2]


def _get(url,limit=MAX_MEMBER):
    req=urllib.request.Request(url,headers={'User-Agent':'iuea-grader','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read(limit+1)
    if len(data)>limit:raise ValueError('File too large')
    return data


def _cached(url,cache,limit=MAX_MEMBER):
    f=Path(cache)/'gh'/(_sha(url.encode())[:32]+'.bin')
    if f.exists():return f.read_bytes()
    f.parent.mkdir(parents=True,exist_ok=True)
    data=_get(url,limit);f.write_bytes(data);return data


def github_files(owner,repo,ref_path,cache=CACHE_DIR):
    """Notebook/README files of a public repo (or the single file/folder a link names)."""
    out=[];base=Path(cache)/('gh_'+_sha(f'{owner}/{repo}/{ref_path}'.encode())[:24]);base.mkdir(parents=True,exist_ok=True)
    ref='HEAD';sub=''
    if ref_path:
        ref,_,sub=ref_path.partition('/')
        sub=sub.strip('/')
    tree=json.loads(_cached(f'https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}?recursive=1',cache,limit=4*MAX_MEMBER))
    cands=[]
    for e in tree.get('tree',[]):
        p=Path(e['path'])
        if e.get('type')!='blob' or p.suffix.lower() not in KEEP or any(SKIP_PART.search(x) for x in p.parts):continue
        if (e.get('size') or 0)>MAX_MEMBER:continue
        if sub and not (e['path']==sub or e['path'].startswith(sub+'/')):continue
        cands.append(e['path'])
    # Notebooks first, then READMEs.
    cands.sort(key=lambda p:(Path(p).suffix.lower()!='.ipynb',len(p)))
    for i,path in enumerate(cands[:MAX_FILES]):
        quoted=urllib.request.quote(path)
        data=_cached(f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quoted}',cache)
        target=base/f'{i:03d}_{re.sub(r"[^A-Za-z0-9._-]","_",Path(path).name)}'
        target.write_bytes(data)
        out.append(_info(target,Path(path).name,f'GitHub {owner}/{repo}'))
    return out


def html_members(path,cache=CACHE_DIR):
    out=[]
    for owner,repo,rest in github_links(path):
        try:out+=github_files(owner,repo,rest,cache)
        except Exception:continue
    return out


def expanded(path,cache=CACHE_DIR):
    """Info dicts for the notebooks/READMEs behind one uploaded ZIP or HTML file."""
    suffix=Path(path).suffix.lower()
    if suffix=='.zip':return zip_members(path,cache)
    if suffix in ('.html','.htm','.url','.webloc'):return html_members(path,cache)
    return []
