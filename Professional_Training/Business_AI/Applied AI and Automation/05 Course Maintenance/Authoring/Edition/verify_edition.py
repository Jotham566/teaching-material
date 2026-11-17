"""Verify the live teaching edition. Exit code 0 only if every check passes.

  python3 verify_edition.py [--write-records] [--rebuild]

Checks the files that teachers and learners use, not the builder's private folders:
  decks         12 decks, 285 slides, essential and optional counts, titles, notes against
                lesson_notes.json, Sources and Playback lines, click stages against the
                native animation, animation targets, pictures with alt text and inside the slide
  documents     the four Word files open; the Guide's twelve time tables each sum to 120 minutes;
                every file named in an "Open before class" line exists
  agreement     hashes of the unmodified source, the specimen and the library copy; the specimen's
                Standard Terms body matches the source; the Key Terms wording is present
  practice      Practice Guide lists every practice file; scripts compile; the scripted host tests pass;
                the lexical retrieval tests give the recorded result
  evidence      the observed run files exist; each agent trace is model-selected and within its budget
  stale text    no old clause names, long-agreement names, rotated lines or the unverified K-Files citation
                in any edition file
  --rebuild     also builds a staging copy from the authoring sources and requires it to match the edition
--write-records refreshes 05 Course Maintenance/File Integrity.json and Validation/Edition Verification.json.
"""
import sys, re, json, hashlib, subprocess, tempfile, zipfile, datetime, importlib.util
from pathlib import Path
from lxml import etree
from pptx import Presentation
from docx import Document

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUTH = HERE.parent
P = ROOT / '03 Learner Materials/Practice Files'
TR = ROOT / '04 Facilitator Materials/Teaching Resources'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
PN = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
RESULTS = []

def check(name, ok, detail=''):
    RESULTS.append(dict(check=name, passed=bool(ok), detail=detail))
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))
    return ok

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6: yield from walk(sh.shapes)

def click_stages(slide):
    """Number of click steps in the main animation sequence."""
    t = slide._element.find(PN + 'timing')
    if t is None: return 0
    for n in t.iter(PN + 'cTn'):
        if n.get('nodeType') == 'mainSeq':
            lst = n.find(PN + 'childTnLst')
            return len(list(lst)) if lst is not None else 0
    return 0

# ------------------------------------------------------------------ notes
SCRIPT_HARD = [(r'\bclicks?\b', 'mentions a click'), (r'\bthis slide\b|\bnext slide\b|\bprevious slide\b|\bon the screen\b', 'talks about the slide'),
    (r'\bI ask\b|\bsatisfactory answer\b|\bgood answer\b|\bfollow-up if needed\b', 'guide phrasing'), (r'https?://|www\.|Sources?:|Playback:', 'link, Sources or Playback line'),
    (r'[\[\]{}<>]', 'brackets'), (r'—|–', 'dash aside'), (r'\b(genuinely|honestly|straightforward|delve|pivotal|robust|leverage)\b', 'banned word'),
    (r'\b(she|her|hers|he|his)\b', 'gendered learner'), (r'(?m)^[A-Z][A-Za-z ]{1,28}:\s', 'label at paragraph start'), (r'\bthe learner\b|\bfacilitator\b', 'third-person guide wording')]
PAUSE = re.compile(r"(Give that a little thought|Have a think|Take your time|No rush|Sit with it for a second|See what you come up with|Say it out loud if it helps|Work it through before I answer|Think it over|Let's hear your answer first|Take a moment with (?:that|all three)(?: as well)?|Give that a moment|Think about it for a moment|Sit with that for a moment|Think it through out loud if it helps)\.")
def script_problems(note, clicks):
    out = []
    if any(PAUSE.search(p) and p[PAUSE.search(p).end():].strip() for p in note.split('\n\n')): out.append('text follows a pause line in the same paragraph')
    paras = [p for p in note.split('\n\n') if p.strip()]; w = len(note.split())
    if clicks and len(paras) < clicks + 1: out.append(f'only {len(paras)} paragraphs for {clicks} clicks')
    if not 40 <= w <= 300: out.append(f'{w} words')
    for pat, why in SCRIPT_HARD:
        if re.search(pat, note, re.I): out.append(why)
    return out

# ------------------------------------------------------------------ decks
def decks():
    course = json.loads((AUTH / 'Documents/course.json').read_text(encoding='utf-8'))
    notes = json.loads((AUTH / 'Documents/lesson_notes.json').read_text(encoding='utf-8'))
    extra = json.loads((AUTH / 'Documents/lesson_notes_sources.json').read_text(encoding='utf-8'))
    overrides = json.loads((HERE / 'expected_changes.json').read_text(encoding='utf-8'))['title_overrides']
    bt = (TR / 'Presenter Notes Backup.txt').read_text(encoding='utf-8')
    backup_sections = {int(m.group(1)): m.group(0) for m in re.finditer(r'^SESSION (\d+):.*?(?=^SESSION |\Z)', bt, re.M | re.S)}
    files = sorted((ROOT / '02 Class Slides').glob('[0-1][0-9] - *.pptx'))
    check('twelve decks', len(files) == 12, len(files))
    total = optional = clicks = pics = animated = 0; bad = []
    for f, sess in zip(files, course):
        n = sess['session']; prs = Presentation(str(f)); slides = list(prs.slides)
        with zipfile.ZipFile(f) as z:
            if z.testzip() is not None: bad.append((n, 'zip'))
        if len(slides) != len(sess['slides']): bad.append((n, 'slide count', len(slides)))
        W, H = prs.slide_width, prs.slide_height
        for i, s in enumerate(slides, 1):
            vis = ' '.join(sh.text_frame.text for sh in walk(s.shapes) if sh.has_text_frame)
            for sh in walk(s.shapes):
                if getattr(sh, 'has_table', False) and sh.has_table:
                    vis += ' ' + ' '.join(c.text for r in sh.table.rows for c in r.cells)
            title = overrides.get(f'{n}/{i}', sess['slides'][i - 1]['title'])
            if title not in vis: bad.append((n, i, 'title', title))
            if (('OPTIONAL EXPLORATION' in vis) != ((i in sess['optional_slides']))): bad.append((n, i, 'optional flag'))
            optional += i in sess['optional_slides']
            note = s.notes_slide.notes_text_frame.text
            exp = notes[f'{n:02d}'][str(i)].strip()
            if note != exp: bad.append((n, i, 'note text differs from lesson_notes.json'))
            k = click_stages(s)
            bad += [(n, i, p) for p in script_problems(note, k)]
            bk = re.search(rf'^Slide {i}: .*?\[(\d+) clicks\]', backup_sections.get(n, ''), re.M)
            if (int(bk.group(1)) if bk else 0) != k: bad.append((n, i, 'click count in Presenter Notes Backup', k))
            sources = extra[f'{n}/{i}']['sources']
            if sources and sources not in backup_sections.get(n, ''): bad.append((n, i, 'sources missing from backup'))
            clicks += k; animated += bool(k)
            ids = {el.get('id') for el in s._element.iter(PN + 'cNvPr')}
            t = s._element.find(PN + 'timing')
            if t is not None and any(el.get('spid') not in ids for el in t.iter(PN + 'spTgt')): bad.append((n, i, 'animation target'))
            for sh in walk(s.shapes):
                if sh.shape_type == 13:
                    pics += sh.name.startswith('illustration-')
                    if sh.name.startswith('illustration-'):
                        d = sh._element.nvPicPr.cNvPr.get('descr')
                        if not d: bad.append((n, i, 'alt text'))
                        if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W or sh.top + sh.height > H: bad.append((n, i, 'picture off slide'))
        total += len(slides)
    import collections
    allnotes = [v for s in notes.values() for v in s.values()]
    sent = collections.Counter(x for v in allnotes for x in re.split(r'(?<=[.?!])\s+', v.replace('\n\n', ' ')) if len(x.split()) >= 4)
    check('no spoken stock sentence repeated more than 40 times', max(sent.values()) <= 40, sent.most_common(2))
    check('285 slides, 52 optional, 233 essential', (total, optional, total - optional) == (285, 52, 233), (total, optional))
    check('126 click stages on 34 animated slides', (clicks, animated) == (126, 34), (clicks, animated))
    check('deck titles, notes, sources, playback, animation targets, pictures', not bad, bad[:6])
    check('illustrations placed with alt text', pics >= 150, pics)
    return pics

# ------------------------------------------------------------------ documents
def documents():
    names = {'Course Overview.docx': ROOT / '01 Course Overview', 'Learner Workbook.docx': ROOT / '03 Learner Materials',
             'Facilitator Guide.docx': ROOT / '04 Facilitator Materials', 'Law Firm Implementation Playbook.docx': ROOT / '04 Facilitator Materials'}
    docs = {}
    for n, d in names.items():
        try: docs[n] = Document(str(d / n))
        except Exception as e: check('open ' + n, False, e); continue
    check('four Word documents open', len(docs) == 4)
    g = docs['Facilitator Guide.docx']
    sums = []
    for t in g.tables:
        rows = [[c.text.strip() for c in r.cells] for r in t.rows]
        if rows and rows[0][:2] == ['Block', 'Min']: sums.append(sum(int(r[1]) for r in rows[1:]))
    check('Guide time tables: twelve sessions of 120 minutes', len(sums) == 12 and all(s == 120 for s in sums), sums)
    paras = [p.text for p in g.paragraphs]; missing = []
    for i, p in enumerate(paras):
        if p.strip() == 'Open before class':
            for item in paras[i + 1].split(';'):
                item = re.sub(r'\s*\(.*?\)\s*$', '', item.strip())
                if not item: continue
                cands = [ROOT / '03 Learner Materials/Practice Files' / item, TR / item, ROOT / item, ROOT / '04 Facilitator Materials/Teaching Resources' / Path(item).name]
                if not any(c.exists() for c in cands): missing.append(item)
    check('every file named in "Open before class" exists', not missing, missing[:5])

# ------------------------------------------------------------------ agreement
def agreement():
    M = P / '01 Matter and Sources'
    src, docx_, txt = M / 'Common Paper CSA v3.0 with SLA - Original unmodified.docx', M / 'Agreement - Executed v2.docx', M / 'Agreement - Executed v2.txt'
    prov = (M / 'Agreement Provenance and Adaptations.txt').read_text(encoding='utf-8')
    check('source and specimen hashes match the provenance record', all(sha(x) in prov for x in (src, docx_, txt)))
    lib = P / '02 Data and Retrieval/Knowledge Library/agreement-current.txt'
    check('library copy of the agreement equals the specimen text', sha(lib) == sha(txt))
    body = lambda d: [p.text.strip() for p in Document(str(d)).paragraphs if p.text.strip()]
    a, b = body(src), body(docx_)
    check('every body paragraph of the unmodified source appears unchanged, in order, at the end of the specimen (Standard Terms untouched)', b[-len(a):] == a, f'{len(a)} v {len(b)}')
    check('the specimen adds only a short notice before the source text', len(b) - len(a) <= 6, len(b) - len(a))
    t = txt.read_text(encoding='utf-8')
    check('Key Terms replacement of Section 12.6 and supplement to Section 1.5 present',
          'Provider must obtain Customer’s prior written consent before a change of control of Provider takes effect.' in t and 'only if each person is named in a written request' in t)
    check('original Section 12.6 still present in the Standard Terms', 'either party may assign this Agreement upon notice if the assigning party undergoes a merger' in t)

# ------------------------------------------------------------------ practice
def practice():
    guide = (P / 'Practice Guide.txt').read_text(encoding='utf-8')
    files = [p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store' and p.name != 'Practice Guide.txt']
    lib = P / '02 Data and Retrieval/Knowledge Library'; ocr = P / '02 Data and Retrieval/OCR Experiment/images'
    ocrd = P / '02 Data and Retrieval/OCR Experiment'
    miss = [f.name for f in files if lib not in f.parents and ocrd not in f.parents and f.name not in guide]
    check('Practice Guide lists every practice file', not miss, miss[:5])
    bad = []
    for py in P.rglob('*.py'):
        try: compile(py.read_text(encoding='utf-8'), str(py), 'exec')
        except SyntaxError as e: bad.append((py.name, e))
    check('practice scripts compile', not bad, bad)
    r = subprocess.run([sys.executable, '-I', str(P / '04 Automation and Tax/host_control_tests.py'), str(P / '02 Data and Retrieval')], capture_output=True, text=True)
    check('scripted host tests T1 to T7 pass', r.returncode == 0 and r.stdout.count('ok') >= 7 and 'FAIL' not in r.stdout, r.stdout[-200:] + r.stderr[-200:])
    r = subprocess.run([sys.executable, '-I', str(P / '02 Data and Retrieval/run_retrieval_tests.py'), '--method', 'lexical'], capture_output=True, text=True, cwd=str(P / '02 Data and Retrieval'))
    res = re.findall(r'(K\d) (PASS|FAIL)', r.stdout)
    check('lexical retrieval tests give the recorded result (6 of 8; K3 and K8 fail)', [x for x in res if x[1] == 'FAIL'] == [('K3', 'FAIL'), ('K8', 'FAIL')] and len(res) == 8, res)
    cr = json.loads((P / '02 Data and Retrieval/Clause Record.json').read_text(encoding='utf-8'))
    check('Clause Record holds the four host identifiers', [x.get('clause') for x in cr] == ['12.6', 'KT-1', '1.5', 'KT-2'], [x.get('clause') for x in cr])

# ------------------------------------------------------------------ evidence
def evidence():
    O = TR / 'Observed Runs'
    need = ['Observed Consent Run 1.txt', 'Observed Consent Run 2.txt', 'Observed Consent Run 3.txt', 'Observed Standard Terms Only.txt', 'Observed Extracts Only.txt',
            'Observed Missing Fee.txt', 'Observed Share Sale Advice.txt', 'Observed Assignment Advice.txt', 'Observed Share Sale Consequence.txt', 'Observed OCR Output.txt',
            'Observed Retrieval Test Output.txt', 'Observed Reconciliation.txt', 'Observed Labelled Reconciliation.txt']
    check('observed model runs and outputs preserved', all((O / n).exists() for n in need), [n for n in need if not (O / n).exists()])
    traces = sorted(O.glob('Agent Trace - *.json')); ok = len(traces) == 4
    for t in traces:
        d = json.loads(t.read_text(encoding='utf-8'))
        ok &= d.get('model_selected') is True and d['lookup_calls'] <= d['max_lookup_calls'] and d['external_actions'] == 0
    check('four model-selected agent traces, within budget, no external action', ok)
    check('scripted host test output kept apart from model traces', (TR / 'Scripted Host Tests/Host Control Test Output.json').exists())

# ------------------------------------------------------------------ stale text
STALE = [r'clause 3', r'long agreement', r'contract - executed', r'likely confusion', r'k-files', r'teaching status:', r'\bshe\b']
def texts():
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT)
        if p.is_dir() or rel.parts[0] == '05 Course Maintenance' or 'Superseded - earlier fictional agreement' in rel.parts or p.name.startswith(('.', '~$')): continue
        if p.suffix in ('.txt', '.csv', '.json', '.py', '.md', '.html', '.js', '.xml'): yield rel, p.read_text(encoding='utf-8', errors='ignore')
        elif p.suffix == '.docx':
            z = zipfile.ZipFile(p); yield rel, re.sub(r'<[^>]+>', '', z.read('word/document.xml').decode('utf8', 'ignore'))
        elif p.suffix == '.pptx':
            z = zipfile.ZipFile(p)
            for n in z.namelist():
                if n.endswith('.xml') and ('slides/slide' in n or 'notesSlide' in n): yield rel / n, re.sub(r'<[^>]+>', '', z.read(n).decode('utf8', 'ignore'))

def stale():
    hits = []
    for rel, t in texts():
        low = t.lower()
        for pat in STALE:
            if pat == r'\bshe\b' and (rel.suffix in ('.py', '.json', '.html', '.js', '.csv') or 'Knowledge Library' in rel.parts or rel.name in ('Observed Reconciliation.txt',) or 'Observed Runs' in rel.parts): continue
            if re.search(pat, low): hits.append((str(rel)[-60:], pat))
    check('no stale agreement names, rotated lines, K-Files reliance or gendered learner', not hits, hits[:8])

# ------------------------------------------------------------------ records
INVENTORY = ROOT / '05 Course Maintenance/File Integrity.json'
RECORD = ROOT / '05 Course Maintenance/Validation/Edition Verification.json'

def inventory():
    """SHA-256 of every file in the course folder except the inventory itself, hidden files, caches and
    the private .build folder. The verification record IS included, so it must be written first."""
    inv = {}
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_dir() or p == INVENTORY or p.name.startswith(('.', '~$')) or '__pycache__' in rel.parts or '.build' in rel.parts or any(x.startswith('.chart-data') for x in rel.parts): continue
        if 'Rehearsal Audio' in rel.parts and p.suffix.lower() in ('.m4a', '.aiff'): continue
        inv[str(rel)] = sha(p)
    return inv

def inventory_matches():
    if not INVENTORY.exists(): return False, 'no inventory'
    old, new = json.loads(INVENTORY.read_text(encoding='utf-8')), inventory()
    diff = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    return not diff, diff[:6]

def records(pics):
    """Order matters: 1 the verification record, 2 the inventory (which hashes the record and omits itself),
    3 a read-back that the inventory matches the folder."""
    rec = dict(date=datetime.date.today().isoformat(), checks=RESULTS, all_passed=all(r['passed'] for r in RESULTS), illustrations=pics,
               note='File Integrity.json hashes this record. It does not hash itself.')
    RECORD.write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
    inv = inventory()
    INVENTORY.write_text(json.dumps(inv, indent=1, ensure_ascii=False), encoding='utf-8')
    ok, d = inventory_matches()
    print('records written:', len(inv), 'files inventoried; read-back', 'matches' if ok else f'FAILS {d}')
    return ok

def comparison_tests():
    r = subprocess.run([sys.executable, str(HERE / 'test_compare_edition.py')], capture_output=True, text=True)
    check('picture comparison is exact for every image, with the Session 12 title illustration regression', r.returncode == 0, r.stdout[-300:] + r.stderr[-200:])

def illustration_assets():
    """Approved PNGs match their manifest, cover the plan, and are the exact bytes inside every deck."""
    I = AUTH / 'Illustrations'; man = json.loads((I / 'Approved Assets.json').read_text(encoding='utf-8'))['files']
    plan = json.loads((I / 'illustration_plan.json').read_text(encoding='utf-8'))
    need = {f"hero_{e['session']:02d}.png" if e['kind'] == 'hero' else f"{e['motif']}.png" for e in plan if e['kind'] in ('hero', 'side')}
    bad = [k for k, v in man.items() if not (I / 'approved' / k).exists() or sha(I / 'approved' / k) != v['sha256']]
    check('approved illustration PNGs match their manifest and cover the plan', not bad and need == set(man), (bad[:3], sorted(need ^ set(man))[:3]))
    pm = {(e['session'], e['slide']): e for e in plan}; wrong = []
    for f in sorted((ROOT / '02 Class Slides').glob('[0-1][0-9] - *.pptx')):
        n = int(f.name[:2])
        for i, s in enumerate(Presentation(str(f)).slides, 1):
            for sh in walk(s.shapes):
                if sh.shape_type == 13 and sh.name.startswith('illustration-') and not sh.name.startswith('illustration-shot'):
                    e = pm.get((n, i)); name = f"hero_{n:02d}.png" if e and e['kind'] == 'hero' else (f"{e['motif']}.png" if e else None)
                    if not name or sh.image.blob != (I / 'approved' / name).read_bytes(): wrong.append((n, i, name))
    check('every illustration in the decks is the approved PNG, byte for byte', not wrong, wrong[:4])

def baseline():
    B = AUTH / 'Baseline'; man = json.loads((B / 'Baseline Manifest.json').read_text(encoding='utf-8'))['files']
    bad = [k for k, h in man.items() if not (B / k).exists() or sha(B / k) != h]
    check('versioned rebuild baseline matches its manifest', not bad and len(man) == 16, bad[:4])

def rebuild():
    with tempfile.TemporaryDirectory() as t:
        st = Path(t) / 'staging'
        r = subprocess.run([sys.executable, str(HERE / 'build_edition.py'), str(st)], capture_output=True, text=True)
        if r.returncode: check('staging build runs', False, r.stderr[-300:]); return
        r = subprocess.run([sys.executable, str(HERE / 'compare_edition.py'), str(st)], capture_output=True, text=True)
        check('staging build from the authoring sources equals the live edition', r.returncode == 0, r.stdout[-300:])

def correction_evidence():
    """Verify the saved repair experiment is tied to the current sources; no model quality is inferred."""
    import csv
    E = TR / 'Observed Runs/Corrections 2026-10-28'
    manifest = json.loads((E / 'Tested Sources.json').read_text())
    bad = [rel for rel, value in manifest.items() if not (ROOT / rel).is_file() or sha(ROOT / rel) != value]
    r = json.loads((E / 'Retrieval Retest.json').read_text())
    check('repaired retrieval evidence passes 19 checks and matches the tested sources', not bad and r['passed'] == r['total'] == 19 and all(x['passed'] for x in r['checks']), bad)
    rows = list(csv.DictReader((TR / 'Goal Relief Assessment Check.csv').open()))
    amounts = [int(row['amount_UGX']) for row in rows if row['included_in_page_1_total'] == 'yes']
    check('historical case arithmetic uses exactly the four original assessment rows', len(amounts) == 4 and sum(amounts) == 650508770, amounts)
    plans = json.loads((AUTH / 'Documents/session_delivery.json').read_text())
    tables = [t for t in Document(str(ROOT / '04 Facilitator Materials/Facilitator Guide.docx')).tables if t.cell(0,0).text == 'Block']
    aligned = len(plans) == len(tables) == 12
    for plan, table in zip(plans, tables):
        aligned = aligned and plan['minutes'] == 120 and len(plan['blocks']) == 7
        for block, row in zip(plan['blocks'], table.rows[1:]):
            aligned = aligned and block['end_minute'] - block['start_minute'] == int(row.cells[1].text) and block['action'] == row.cells[3].text
    check('twelve concrete in-class plans match the Guide and each total 120 minutes', aligned)

def demonstration_instructions():
    data = json.loads((AUTH / 'Documents/demonstrations.json').read_text())
    guide = Document(str(ROOT / '04 Facilitator Materials/Facilitator Guide.docx'))
    text = '\n'.join(p.text for p in guide.paragraphs)
    # python-docx includes ordinary paragraph text; hyperlink labels are inspected in XML.
    with zipfile.ZipFile(ROOT / '04 Facilitator Materials/Facilitator Guide.docx') as z:
        xml = etree.fromstring(z.read('word/document.xml'))
    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    anchors = {b.get('{'+ns['w']+'}name') for b in xml.findall('.//w:bookmarkStart',ns)}
    required = ['purpose','tool','files','prepare','steps','check','discuss','rescue','record','transition','executive_task','executive_check']
    bad=[];prompt_count=0
    for item in data:
        n=item['session']
        if any(not item.get(k) for k in required) or len(item['steps'])<6:bad.append((n,'incomplete procedure'))
        if f'demo{n:02d}' not in anchors:bad.append((n,'missing navigation'))
        for path in item['files']:
            if not (ROOT/path).exists():bad.append((n,'missing source',path))
        for key in ('executive_task','executive_check'):
            if item[key] not in text:bad.append((n,'executive decision missing from Guide',key))
        for step in item['steps']:
            if step not in text:bad.append((n,'step missing from Guide'))
        for prompt in item['prompts']:
            prompt_count+=1;f=TR/'Demo Materials'/(prompt['id']+'.txt')
            if not f.exists() or f.read_text().strip()!=prompt['text'] or prompt['text'] not in text:bad.append((n,'prompt mismatch',prompt['id']))
    check('all twelve demonstrations have linked complete procedures, existing sources and matching prompts',len(data)==12 and prompt_count==17 and not bad,bad[:4])
    e=json.loads((ROOT/'05 Course Maintenance/Validation/Demonstration Delivery.json').read_text())
    changed=[rel for rel,value in e['tested_source_hashes'].items() if not (ROOT/rel).exists() or sha(ROOT/rel)!=value]
    changed += [rel for rel,value in e.get('instruction_source_hashes',{}).items() if not (ROOT/rel).exists() or sha(ROOT/rel)!=value]
    check('seventeen documented launch routes passed with the current tested sources',e['passed']==e['total']==17 and not changed,changed[:4])

if __name__ == '__main__':
    write = '--write-records' in sys.argv
    pics = decks(); documents(); agreement(); practice(); evidence(); stale(); baseline(); illustration_assets(); comparison_tests(); correction_evidence(); demonstration_instructions()
    if '--rebuild' in sys.argv: rebuild()
    if not write:
        ok_inv, d = inventory_matches(); check('File Integrity.json matches every file in the folder', ok_inv, d)
    ok = all(r['passed'] for r in RESULTS)
    print('\nRESULT:', 'ALL CHECKS PASSED' if ok else 'FAILURES', f'({sum(r["passed"] for r in RESULTS)}/{len(RESULTS)})')
    if write and not records(pics): ok = False
    sys.exit(0 if ok else 1)
