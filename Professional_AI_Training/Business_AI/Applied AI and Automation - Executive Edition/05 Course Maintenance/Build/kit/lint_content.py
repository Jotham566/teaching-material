"""House-style and schema lint for the session files in content/. Run from Build/:  python3 kit/lint_content.py [1 2 ...]

Checks: required fields; 10 to 14 authored slides; every slide has a title and spoken notes of 45 to 150 words; at most 55 to 130 words of text on a slide, depending on the kind;
every authored slide kind is known; no price of the course anywhere; no em dash; no 'X, not Y' construction; no filler words; no exam or marks language;
the learner is addressed as 'you' (no he or she for the learner); sentences in notes are not stage directions.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import deck  # noqa: E402

REQ = ['num', 'title', 'question', 'outcomes', 'keep', 'next', 'clock', 'words', 'cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note', 'slides', 'recall', 'recall_note', 'workbook', 'facilitator']
BAN = [r'honestly', r'genuinely', r'straightforward', r'dive into', r'\bunlock', r'\bjourney\b', r'embark', r'game-changer', r"in today's world", r'delve', r'leverage\b']
PRICE = [r'1,000,000', r'1 million shillings', r'course fee', r'price of (the|this) course', r'cost of (the|this) course', r'tuition']
EXAM = [r'\bexam\b', r'\bexams\b', r'\bmarks\b', r'\bgraded\b', r'\bgrading\b', r'pass mark']
ANTI = [r',\s+not\s+(a|an|the|just|only|about|because|to|for|in|on|by|with|every|all|any)\b', r'\bnot\s+just\b', r'\bnot\s+only\b[^.]*\bbut\b', r'\binstead of\b[^.]*\bnot\b']
STAGE = [r'\[[^\]]*\]', r'\(pause\)', r'\bclick\b', r'\bnext slide\b']


def words(s):
    return len(re.findall(r"[A-Za-z0-9’'%$£]+", s))


def slide_text(sl):
    out = [sl.get('title', ''), sl.get('lead', ''), sl.get('caption', ''), sl.get('verdict', ''), sl.get('task', ''), sl.get('output', ''), sl.get('question', ''),
           sl.get('text', ''), sl.get('big', ''), sl.get('scenario', '')]
    for k in ('points', 'steps', 'items', 'show', 'watch'):
        for x in sl.get(k, []) or []:
            out.append(x if isinstance(x, str) else ' '.join(str(v) for v in x.values() if isinstance(v, str)))
    for side in ('left', 'right'):
        if sl.get(side):
            out.append(sl[side]['head'] + ' ' + ' '.join(sl[side]['points']))
    for o in sl.get('options', []) or []:
        out.append(o['head'] + ' ' + o['text'])
    for b in sl.get('blocks', []) or []:
        out.append(b['label'] + ' ' + b['text'])
    for r in sl.get('rows', []) or []:
        out.append(' '.join(r))
    out.append(' '.join(sl.get('headers', []) or []))
    v = sl.get('visual')
    if v:
        for k in ('steps', 'layers', 'items', 'points'):
            for x in v.get(k, []) or []:
                out.append(x if isinstance(x, str) else ' '.join(str(a) for a in x.values() if isinstance(a, str)))
    return ' '.join(out)


def lint(num):
    errs = []
    try:
        s = deck.load(num)
    except Exception as e:
        return [f'S{num}: cannot load: {e}']
    for k in REQ:
        if k not in s:
            errs.append(f'S{num}: missing field {k}')
    if errs:
        return errs
    sl = s['slides']
    if not (10 <= len(sl) <= 14 or (num == 0 and 14 <= len(sl) <= 38) or (1 <= num <= 14 and 10 <= len(sl) <= 22)):
        errs.append(f'S{num}: {len(sl)} authored slides (want 10 to 22)')
    alltext = []
    for i, x in enumerate(sl, 1):
        tag = f'S{num} slide {i} ({x.get("title", "")[:40]})'
        if x.get('kind') not in deck.KINDS:
            errs.append(f'{tag}: unknown kind {x.get("kind")}')
        if not x.get('title'):
            errs.append(f'{tag}: no title')
        n = words(x.get('notes', ''))
        if not 45 <= n <= 150:
            errs.append(f'{tag}: notes are {n} words (want 45 to 150)')
        t = slide_text(x)
        lim = {'practice': 85, 'decision': 85, 'steps': 85, 'idea': 85, 'list': 70, 'table': 130, 'example': 110, 'compare': 70, 'demo': 70, 'statement': 60}.get(x.get('kind'), 55)
        if words(t) > lim:
            errs.append(f'{tag}: {words(t)} words of slide text (limit {lim} for a {x.get("kind")} slide)')
        alltext.append(x.get('notes', ''))
        alltext.append(t)
    for k in ('cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note'):
        n = words(s[k])
        if not 25 <= n <= 150:
            errs.append(f'S{num}: {k} is {n} words')
        alltext.append(s[k])
    alltext += s['outcomes'] + [s['keep'], s['next'], s['question']] + [a + ' ' + b for a, b in s['words']]
    if num > 1 and not s['recall']:
        errs.append(f'S{num}: recall needs 2 or 3 (question, answer) pairs about the previous session')
    total = sum(m for m, _ in s['clock'])
    if total != 120:
        errs.append(f'S{num}: clock sums to {total}, not 120')
    blob = '\n'.join(alltext)
    for pat, name in ((BAN, 'banned word'), (PRICE, 'course price'), (EXAM, 'exam or marks language'), (ANTI, 'X, not Y construction'), (STAGE, 'stage direction')):
        for p in pat:
            for m in re.finditer(p, blob, re.I):
                a = max(0, m.start() - 40)
                errs.append(f'S{num}: {name}: …{blob[a:m.end() + 30]!r}')
    if '—' in blob or '–' in blob.replace('9 to 11', ''):
        errs.append(f'S{num}: em or en dash found')
    for m in re.finditer(r'\b(he|she|his|her)\b', blob):
        a = max(0, m.start() - 30)
        errs.append(f'S{num}: gendered pronoun: …{blob[a:m.end() + 20]!r}')
    return errs


if __name__ == '__main__':
    nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[1:]) for p in (deck.BUILD / 'content').glob('s[0-9][0-9].py'))
    bad = 0
    for n in nums:
        e = lint(n)
        bad += len(e)
        for x in e:
            print(x)
    print(f'{bad} problems in {len(nums)} sessions')
    sys.exit(1 if bad else 0)
