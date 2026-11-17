"""Write docs_data.json for the document builders (reads curriculum.py, Content/sNN.json, the built decks' counts and the template folder).
   python3 export_docs_data.py"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
import curriculum as cur
import openpyxl
import build_course as bc

TEMPLATES = sorted(p.name for p in (bc.ROOT / '03 Learner Materials/Workpiece Templates').iterdir() if not p.name.startswith('.'))
STEMS = sorted({(t.rsplit('.', 1)[0], t) for t in TEMPLATES}, key=lambda x: -len(x[0]))
HEAVY = {'sentence_transformers': 'sentence-transformers', 'SentenceTransformer': 'sentence-transformers', 'chromadb': 'chromadb', 'psycopg2': 'pgvector and psycopg2', 'pgvector': 'pgvector and psycopg2',
         'pandera': 'pandera', 'great_expectations': 'great_expectations', 'presidio': 'presidio', 'dagster': 'dagster', 'duckdb': 'duckdb', 'pyarrow': 'pyarrow', 'docling': 'docling', 'ragas': 'ragas'}
HEAVY_RE = re.compile('|'.join(sorted(HEAVY, key=len, reverse=True)))
def levels_guide():
    ws = openpyxl.load_workbook(bc.ROOT / '03 Learner Materials/Workpiece Templates/Readiness Scorecard.xlsx')['Levels guide']
    rows = [[str(x) for x in r if x is not None] for r in ws.iter_rows(values_only=True)]
    return [r for r in rows if len(r) == 4 and r[0].isdigit()]
PAGES = {7: ['Search pilot report outline'], 8: ['Pipeline map'], 9: ['Data protection map'], 12: ['Board presentation outline']}   # pages of the Participant Workbook that the slides name or the workpiece needs

def libs_in(text): return sorted({HEAVY[m] for m in HEAVY_RE.findall(text)})

def workbooks_used(lab):
    text = ' '.join([lab.get('intro', '')] + [t['task'] for t in lab.get('workshop', [])])
    found = []
    for stem, fname in STEMS:
        if re.search(re.escape(stem), text):
            found.append(fname); text = text.replace(stem, ' ')
    return [t for t in TEMPLATES if t in found]

rows = []; tot = dict(slides=0, clicks=0, animated=0, words=0, vocab=0, workshop_tasks=0, notebook_tasks=0, code_slides=0)
vocab_full = []
for n in range(1, cur.COURSE['sessions'] + 1):
    c = json.loads((bc.CONTENT / f's{n:02d}.json').read_text(encoding='utf-8')); s = cur.SESSIONS[n]
    probs = []; deck = bc.build_deck(n, json.loads((bc.CONTENT / f's{n:02d}.json').read_text(encoding='utf-8')), probs)
    words = sum(len(x.get('notes', '').split()) for x in c['slides']) + sum(len(c.get(k, '').split()) for k in ('notes_title', 'notes_outcomes', 'notes_words'))   # same count as check_course.py
    lab = c.get('lab', {}); cells = lab.get('cells', [])
    nb_tasks = [x['md'].lstrip().split('\n')[0].lstrip('# ').strip() for x in cells if 'md' in x and x['md'].lstrip().startswith('## Task')]
    heavy_cells = []; last = None
    for x in cells:
        if 'md' in x:
            m = re.match(r'\s*##\s*(Task \d+)', x['md'])
            if m: last = m.group(1)
        elif 'code' in x and libs_in(x['code']): heavy_cells.append(dict(where=last or 'notebook', libs=libs_in(x['code'])))
    slides = []; demo = []
    for i, sl in enumerate(c['slides'], 1):
        if 'title' not in sl: continue
        slides.append(dict(no=i + 3, type=sl['type'], title=sl['title']))
        if sl['type'] == 'code':
            demo.append(dict(no=i + 3, title=sl['title'], libs=libs_in(json.dumps(sl)), syntax_only='syntax only' in sl['title'].lower()))
    chk = [x for x in c['slides'] if x['type'] == 'check' and x['title'] == 'Questions to finish'][0]['questions']
    for term, d, x in c['vocab']: vocab_full.append(dict(term=term, meaning=d, example=x or '', session=n))
    wk = lab.get('workshop', [])
    rows.append(dict(no=n, module=s['module'], notebook=f"{bc.title_file(n)} (student).ipynb", solution_notebook=f"{bc.title_file(n)} (solution).ipynb", deck_file=f"{bc.title_file(n)}.pptx", title=s['title'], question=s['question'], result=s['result'], outcomes=s['outcomes'], lab=s['lab'], intro=lab.get('intro', ''),
                     workpiece=cur.WORKPIECES.get(n), slides=deck.n, clicks=deck.clicks, animated=deck.animated, minutes_spoken=round(words / 130), words=words,
                     vocab=[dict(term=v[0], meaning=v[1], example=v[2] if len(v) > 2 else '') for v in c['vocab']],
                     workshop=wk, notebook_tasks=nb_tasks, workbooks=workbooks_used(lab), pages=PAGES.get(n, []),
                     slide_list=slides, demo=demo, heavy_cells=heavy_cells, exit_questions=chk, decision=chk[-1]))
    tot['slides'] += deck.n; tot['clicks'] += deck.clicks; tot['animated'] += deck.animated; tot['words'] += words; tot['vocab'] += len(c['vocab'])
    tot['workshop_tasks'] += len(wk); tot['notebook_tasks'] += len(nb_tasks); tot['code_slides'] += len(demo)
out = dict(course=cur.COURSE, shape=cur.SESSION_SHAPE, dimensions=cur.DIMENSIONS, levels=cur.LEVELS, workpieces={str(k): v for k, v in cur.WORKPIECES.items()},
           modules=[(a, b, list(r), d) for a, b, r, d in cur.MODULES], tools=cur.TOOLS, avoided=cur.AVOIDED, templates=TEMPLATES, vocab=vocab_full, levels_guide=levels_guide(), sessions=rows, totals=tot)
(HERE / 'docs_data.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8'); print(tot)
