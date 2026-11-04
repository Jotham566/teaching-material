"""House-style lint for the class files. python3 kit/lint_content.py [1 2 3 4]   (all three cohorts are checked for each class)

Checks: required fields; 18 to 34 authored slides; every slide has a title that states the point and spoken notes of 45 to 150 words; limits on words per slide;
known slide kinds; no 'X, not Y' construction; no em or en dash; no banned filler words; the learner is 'you' (no he or she); no stage directions in notes;
a concepts half and a lab half (a divider slide named 'Part 2'); at most one text-only slide in five; clock sums to 180."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import deck  # noqa: E402

REQ = ['code', 'cohort_name', 'num', 'week', 'when', 'short_title', 'title', 'question', 'outcomes', 'clock', 'words', 'cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note',
       'keep', 'next', 'slides', 'recall', 'facilitator']
BAN = [r'honestly', r'genuinely', r'straightforward', r'dive into', r'\bunlock', r'\bjourney\b', r'embark', r'game-changer', r"in today's world", r'delve', r'leverage\b']
ANTI = [r',\s+not\s+(a|an|the|just|only|about|because|to|for|in|on|by|with|every|all|any)\b', r'\bnot\s+just\b', r'\bnot\s+only\b[^.]*\bbut\b', r'\binstead of\b[^.]*\bnot\b']
STAGE = [r'\[[^\]]*\]', r'\(pause\)', r'\bclick\b', r'\bnext slide\b']
LIMITS = {'practice': 85, 'decision': 85, 'steps': 100, 'idea': 100, 'list': 90, 'table': 150, 'example': 110, 'compare': 70, 'demo': 70, 'statement': 60, 'code': 85, 'divider': 30, 'formula': 120}


def words(s):
    return len(re.findall(r"[A-Za-z0-9’'%$£]+", s))


def slide_text(sl):
    out = [sl.get('title', ''), sl.get('lead', ''), sl.get('caption', ''), sl.get('verdict', ''), sl.get('task', ''), sl.get('output', '') if isinstance(sl.get('output'), str) else ' '.join(sl.get('output', []) or []),
           sl.get('question', ''), sl.get('text', ''), sl.get('big', ''), sl.get('scenario', ''), sl.get('note', '')]
    for k in ('points', 'steps', 'items', 'show', 'watch', 'reads', 'symbols'):
        for x in sl.get(k, []) or []:
            out.append(x if isinstance(x, str) else ' '.join(str(v) for v in (x.values() if isinstance(x, dict) else x) if isinstance(v, str)))
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
        for k in ('steps', 'layers', 'items', 'points', 'parts'):
            for x in v.get(k, []) or []:
                out.append(x if isinstance(x, str) else ' '.join(str(a) for a in (x.values() if isinstance(x, dict) else x) if isinstance(a, str)))
    return ' '.join(out)


def lint(num, code):
    errs = []
    try:
        s = deck.load(num, code)
    except Exception as e:
        return [f'C{num} {code}: cannot load: {type(e).__name__}: {e}']
    tagc = f'C{num} {code}'
    for k in REQ:
        if k not in s:
            errs.append(f'{tagc}: missing field {k}')
    if errs:
        return errs
    sl = s['slides']
    if not 18 <= len(sl) <= 34:
        errs.append(f'{tagc}: {len(sl)} authored slides (want 18 to 34)')
    if not any(x.get('kind') == 'divider' and x['title'].startswith('Part 2') for x in sl):
        errs.append(f'{tagc}: no "Part 2" divider between concepts and lab')
    alltext = []
    textonly = 0
    for i, x in enumerate(sl, 1):
        tag = f'{tagc} slide {i} ({x.get("title", "")[:40]})'
        if x.get('kind') not in deck.KINDS:
            errs.append(f'{tag}: unknown kind {x.get("kind")}')
        n = words(x.get('notes', ''))
        if not 45 <= n <= 150:
            errs.append(f'{tag}: notes are {n} words (want 45 to 150)')
        t = slide_text(x)
        if words(t) > LIMITS.get(x.get('kind'), 55):
            errs.append(f'{tag}: {words(t)} words of slide text (limit {LIMITS.get(x.get("kind"), 55)} for a {x.get("kind")} slide)')
        if x.get('kind') in ('statement',) and not x.get('icon') and not x.get('points'):
            textonly += 1
        alltext += [x.get('notes', ''), t]
    if textonly > len(sl) // 5:
        errs.append(f'{tagc}: too many text-only slides')
    for k in ('cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note'):
        n = words(s[k])
        if not 25 <= n <= 150:
            errs.append(f'{tagc}: {k} is {n} words')
        alltext.append(s[k])
    alltext += s['outcomes'] + [s['keep'], s['next'], s['question']] + [a + ' ' + b for a, b in s['words']]
    for lab, rows in (('recall', s['recall']),):
        for q, a in rows:
            alltext.append(q + ' ' + a)
    if sum(m for m, _ in s['clock']) != 180:
        errs.append(f'{tagc}: clock sums to {sum(m for m, _ in s["clock"])}, not 180')
    blob = '\n'.join(alltext)
    for pat, name in ((BAN, 'banned word'), (ANTI, 'X, not Y construction'), (STAGE, 'stage direction')):
        for p in pat:
            for m in re.finditer(p, blob, re.I):
                a = max(0, m.start() - 40)
                errs.append(f'{tagc}: {name}: …{blob[a:m.end() + 30]!r}')
    if '—' in blob or '–' in blob:
        errs.append(f'{tagc}: em or en dash found')
    for m in re.finditer(r'\b(he|she|his|her)\b', blob):
        a = max(0, m.start() - 30)
        errs.append(f'{tagc}: gendered pronoun: …{blob[a:m.end() + 20]!r}')
    return errs


if __name__ == '__main__':
    nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[1:]) for p in (deck.BUILD / 'content').glob('c[0-9].py'))
    bad = 0
    for n in nums:
        for code in ('CML3112', 'CML3113', 'CML3111'):
            for e in lint(n, code):
                print(e)
                bad += 1
    print(f'{bad} problems in {len(nums)} classes')
    sys.exit(1 if bad else 0)
