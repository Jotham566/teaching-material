"""Write docs_data.json for the document builders (reads curriculum.py and Content/sNN.json)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
import curriculum as cur
import build_course as bc
rows = []; tot = dict(slides=0, clicks=0, animated=0, words=0, vocab=0)
for n in range(1, 25):
    c = json.loads((bc.CONTENT / f's{n:02d}.json').read_text(encoding='utf-8')); s = cur.SESSIONS[n]
    probs = []; deck = bc.build_deck(n, json.loads((bc.CONTENT / f's{n:02d}.json').read_text(encoding='utf-8')), probs)
    words = sum(len(x.get('notes', '').split()) for x in c['slides']) + sum(len(c.get(k, '').split()) for k in ('notes_title', 'notes_outcomes', 'notes_words'))   # same count as check_course.py
    lab_tasks = len([x for x in c.get('lab', {}).get('cells', []) if 'md' in x and x['md'].lstrip().startswith('## Task')]) or len(c.get('lab', {}).get('sheet_tasks', []))
    rows.append(dict(no=n, module=s['module'], title=s['title'], question=s['question'], result=s['result'], dataset=s['dataset'], tools=s['tools'], code=s['code'], outcomes=s['outcomes'],
                     slides=deck.n, clicks=deck.clicks, animated=deck.animated, vocab=[v[0] for v in c['vocab']], lab=s['lab'], lab_tasks=lab_tasks, minutes_spoken=round(words / 130), maps=s['maps'], checkpoint=cur.CHECKPOINTS.get(n)))
    tot['slides'] += deck.n; tot['clicks'] += deck.clicks; tot['animated'] += deck.animated; tot['words'] += words; tot['vocab'] += len(c['vocab'])
vocab_full = []; sheets = {}; rubric = None; capbrief = None
for n in range(1, 25):
    c = json.loads((bc.CONTENT / f's{n:02d}.json').read_text(encoding='utf-8'))
    for term, d, x in c['vocab']: vocab_full.append(dict(term=term, meaning=d, sheet=x or '', session=n))
    if c['lab'].get('sheet_tasks'): sheets[n] = dict(intro=c['lab'].get('intro', ''), tasks=c['lab']['sheet_tasks'])
    for s in c['slides']:
        if n == 24 and s['type'] == 'table' and s['title'].startswith('How your presentation'): rubric = dict(header=s['header'], rows=s['rows'])
        if n == 19 and s['type'] == 'table' and 'capstone' in s['title'].lower(): capbrief = dict(header=s['header'], rows=s['rows'])
out = dict(vocab=vocab_full, sheets=sheets, rubric=rubric, capstone=capbrief, course=cur.COURSE, shape=cur.SESSION_SHAPE, modules=[(a, b, list(r), d) for a, b, r, d in cur.MODULES], tools=cur.TOOLS, avoided=cur.AVOIDED, coverage=cur.ROADMAP_COVERAGE, assessment=cur.ASSESSMENT, sessions=rows, totals=tot)
(HERE / 'docs_data.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8'); print(tot)
