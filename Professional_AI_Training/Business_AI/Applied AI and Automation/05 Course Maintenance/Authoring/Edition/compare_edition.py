"""Compare a staging build with the live teaching edition.

  python3 compare_edition.py STAGING_FOLDER [LIVE_FOLDER]

Decks are compared part by part (canonical XML, media bytes, no tolerance), Word documents by
document.xml, every other file by SHA-256. Folders 05 Course Maintenance and cache
files are ignored. Exit code 0 means identical, 1 means differences (listed).
"""
import sys, hashlib, zipfile
from pathlib import Path
from lxml import etree

LIVE = Path(__file__).resolve().parents[3]
SKIP_DIRS = {'05 Course Maintenance', '__pycache__'}
SKIP_FILES = {'.DS_Store', '.gitignore'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def c14n(z, n):
    try: return hashlib.sha256(etree.tostring(etree.fromstring(z.read(n)), method='c14n')).hexdigest()
    except Exception: return hashlib.sha256(z.read(n)).hexdigest()

def zip_sig(p):
    with zipfile.ZipFile(p) as z:
        return {n: (c14n(z, n) if n.endswith(('.xml', '.rels')) else hashlib.sha256(z.read(n)).hexdigest()) for n in z.namelist() if not n.startswith('docProps/')}

def decks_equal(pa, pb):
    """Exact: every part, picture bytes included. Illustrations are the approved PNGs, embedded unchanged, so no
    picture needs a tolerance. A one-pixel change to any image (illustration, scan or screenshot) is a difference."""
    return zip_sig(pa) == zip_sig(pb)

def listing(root):
    out = {}
    for p in Path(root).rglob('*'):
        rel = p.relative_to(root)
        if p.is_dir() or rel.parts[0] in SKIP_DIRS or set(rel.parts) & SKIP_DIRS or p.name in SKIP_FILES or p.name.startswith(('~$', '.~lock.')): continue
        if 'Rehearsal Audio' in rel.parts and p.suffix.lower() in ('.m4a', '.aiff'): continue
        out[str(rel)] = p
    return out

def main(staging, live=LIVE):
    a, b = listing(staging), listing(live)
    diffs = []
    for k in sorted(set(a) | set(b)):
        if k not in a: diffs.append(('only in live', k)); continue
        if k not in b: diffs.append(('only in staging', k)); continue
        if k.endswith(('.pptx', '.docx')):
            if not decks_equal(a[k], b[k]): diffs.append(('content differs', k))
        elif sha(a[k]) != sha(b[k]): diffs.append(('content differs', k))
    print(f'{len(a)} staged files, {len(b)} live files, {len(diffs)} differences')
    for d in diffs: print('  ', *d)
    return 1 if diffs else 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))
