"""Course-level checks across all 12 sessions.  python3 check_course.py"""
import json, re, collections, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; CONTENT = HERE.parent / 'Content'
import curriculum as cur
cat = json.loads((HERE / 'figs_cache/catalog.json').read_text(encoding='utf-8'))
terms = collections.defaultdict(list); probs = []; tot = dict(slides=0, clicks=0, anim=0, words=0)
rows = []
for n in range(1, 13):
    c = json.loads((CONTENT / f's{n:02d}.json').read_text(encoding='utf-8'))
    for t, d, x in c['vocab']: terms[t.strip().lower()].append(n)
    figs = [s.get('fig') for s in c['slides'] if s.get('fig')]
    for f in figs:
        f = f['name'] if isinstance(f, dict) else f
        if f not in cat: probs.append(f'S{n}: unknown figure {f}')
    words = sum(len(s.get('notes', '').split()) for s in c['slides']) + sum(len(c.get(k, '').split()) for k in ('notes_title', 'notes_outcomes', 'notes_words'))
    titles = [s['title'] for s in c['slides'] if 'title' in s]
    if len(titles) != len(set(titles)): probs.append(f'S{n}: duplicate slide titles')
    for s in c['slides']:
        if 'title' in s and s['title'].rstrip().endswith('.'): probs.append(f'S{n}: title ends with a full stop: {s["title"]}')
    rows.append((n, len(c['slides']) + 3, words, round(words / 130)))
# repeated sentences in the read-aloud notes: ritual lines must differ from session to session
PAUSES = {"Take your time.", "Have a think.", "No rush.", "Think it over.", "Give that a moment.", "Sit with it for a second.", "Give that a little thought.", "See what you come up with.", "Say it out loud if it helps.", "Let's hear your answer first.", "Work it through before I answer."}
sent = collections.defaultdict(set)
for n in range(1, 13):
    c = json.loads((CONTENT / f's{n:02d}.json').read_text(encoding='utf-8'))
    for tx in [c.get(k, '') for k in ('notes_title', 'notes_outcomes', 'notes_words')] + [s.get('notes', '') for s in c['slides']]:
        for s_ in re.split(r'(?<=[.?!])\s+', tx.replace('\n\n', ' ')):
            if len(s_.split()) >= 4 and s_ not in PAUSES: sent[s_.strip()].add(n)
REPEAT_LIMIT = 2
for s_, ns in sorted(sent.items(), key=lambda x: -len(x[1])):
    if len(ns) > REPEAT_LIMIT: probs.append(f'sentence used in {len(ns)} sessions {sorted(ns)}: {s_[:90]!r}')
for t, ns in terms.items():
    if len(ns) > 1: probs.append(f'vocabulary term {t!r} defined in sessions {ns}')
print('Session  slides  note-words  minutes-spoken'); [print(f'{n:7} {s:7} {w:11} {m:14}') for n, s, w, m in rows]
print('total slides', sum(r[1] for r in rows), 'note words', sum(r[2] for r in rows), 'hours spoken', round(sum(r[3] for r in rows) / 60, 1))
print('vocabulary terms', len(terms)); print('\n'.join(probs) or 'No course-level problems.')
sys.exit(1 if probs else 0)
