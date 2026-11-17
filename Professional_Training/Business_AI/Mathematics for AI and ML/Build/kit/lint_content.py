"""House-style lint for the session files in content/. python3 kit/lint_content.py [1 2 ...]

Checks: required fields; 20 to 40 authored slides; a 'Part 2' divider between concepts and lab; a slide titled 'Where ... appears' about ChatGPT, Gemini, Claude or other AI after the divider; every slide has a title and
spoken notes of 45 to 150 words; words per slide; no 'X, not Y'; no em or en dash; no banned filler; no he or she for the learner; no stage directions; clock sums to 120."""
import re
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import deck  # noqa: E402

REQ = ['num', 'block', 'short_title', 'title', 'question', 'outcomes', 'clock', 'words', 'cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note', 'keep', 'next', 'slides', 'recall', 'facilitator']
BAN = [r'honestly', r'genuinely', r'straightforward', r'dive into', r'\bunlock', r'\bjourney\b', r'embark', r'game-changer', r"in today's world", r'delve', r'leverage\b']
ANTI = [r',\s+not\s+(a|an|the|just|only|about|because|to|for|in|on|by|with|every|all|any)\b', r'\bnot\s+just\b', r'\bnot\s+only\b[^.]*\bbut\b', r'\binstead of\b[^.]*\bnot\b']
SLOP_NOTES = [(r'\b(simply|just|really|actually|clearly|obviously)\b', 5), (r'\b(Think of|Imagine|Picture)\b', 3), (r'\bthe key\b', 2), (r'\bin plain words\b', 2), (r'\bThat is (why|the point)\b', 2), (r'\bNotice\b', 3)]
STAGE = [r'\[[^\]]*\]', r'\(pause\)', r'\bclick\b', r'\bnext slide\b']
LIMITS = {'practice': 85, 'decision': 85, 'steps': 100, 'idea': 100, 'list': 90, 'table': 150, 'example': 110, 'compare': 70, 'demo': 70, 'statement': 60, 'code': 90, 'divider': 30, 'formula': 120}


def words(s):
    return len(re.findall(r"[A-Za-z0-9’'%$£]+", s))


def slide_text(sl):
    out = [sl.get('title', ''), sl.get('lead', ''), sl.get('caption', ''), sl.get('verdict', ''), sl.get('task', ''), sl.get('question', ''), sl.get('text', ''), sl.get('big', ''), sl.get('scenario', ''), sl.get('note', '')]
    o = sl.get('output', '')
    out.append(o if isinstance(o, str) else ' '.join(o or []))
    for k in ('points', 'steps', 'items', 'show', 'watch', 'reads', 'symbols'):
        for x in sl.get(k, []) or []:
            out.append(x if isinstance(x, str) else ' '.join(str(v) for v in (x.values() if isinstance(x, dict) else x) if isinstance(v, str)))
    for side in ('left', 'right'):
        if sl.get(side):
            out.append(sl[side]['head'] + ' ' + ' '.join(sl[side]['points']))
    for o2 in sl.get('options', []) or []:
        out.append(o2['head'] + ' ' + o2['text'])
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


def lint(num):
    errs = []
    try:
        s = deck.load(num)
    except Exception as e:
        return [f'S{num}: cannot load: {type(e).__name__}: {e}']
    tagc = f'S{num}'
    for k in REQ:
        if k not in s:
            errs.append(f'{tagc}: missing field {k}')
    if errs:
        return errs
    sl = s['slides']
    if not 20 <= len(sl) <= 40:
        errs.append(f'{tagc}: {len(sl)} authored slides (want 20 to 40)')
    di = [i for i, x in enumerate(sl) if x.get('kind') == 'divider' and x['title'].startswith('Part 2')]
    if not di:
        errs.append(f'{tagc}: no "Part 2" divider')
    elif not any(re.search(r'ChatGPT|Gemini|Claude|language model|AI', x.get('title', '')) and 'appear' in x.get('title', '').lower() or 'where' in x.get('title', '').lower() and re.search(r'ChatGPT|Gemini|Claude|AI', x.get('title', '')) for x in sl[di[0]:]):
        errs.append(f'{tagc}: no "where this appears in AI" slide after the divider')
    alltext = []
    for i, x in enumerate(sl, 1):
        tag = f'{tagc} slide {i} ({x.get("title", "")[:40]})'
        if x.get('kind') not in deck.KINDS:
            errs.append(f'{tag}: unknown kind {x.get("kind")}')
        n = words(x.get('notes', ''))
        if not 45 <= n <= 150:
            errs.append(f'{tag}: notes are {n} words (want 45 to 150)')
        t = slide_text(x)
        lim = LIMITS.get(x.get('kind'), 55)
        if words(t) > lim:
            errs.append(f'{tag}: {words(t)} words of slide text (limit {lim} for a {x.get("kind")} slide)')
        alltext += [x.get('notes', ''), t]
    for k in ('cover_note', 'outcome_note', 'plan_note', 'words_note', 'keep_note'):
        n = words(s[k])
        if not 25 <= n <= 150:
            errs.append(f'{tagc}: {k} is {n} words')
        alltext.append(s[k])
    alltext += s['outcomes'] + [s['keep'], s['next'], s['question']] + [a + ' ' + b for a, b in s['words']]
    for q, a in s['recall']:
        alltext.append(q + ' ' + a)
    if sum(m for m, _ in s['clock']) != 120:
        errs.append(f'{tagc}: clock sums to {sum(m for m, _ in s["clock"])}, not 120')
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
    # ---- house style against formulaic, machine-sounding writing (12 November 2026)
    sl_ = s['slides']
    titles = [x.get('title', '') for x in sl_]
    notes = [x.get('notes', '').strip() for x in sl_]
    here = sum(1 for n in notes if re.match(r'(Here (is|are)|Let me|Let us|Let’s|Now,? let)', n))
    if here > 3:
        errs.append(f'S{num}: {here} notes open with "Here is", "Let me", "Let us" or "Now let" (at most 3)')
    q_end = sum(1 for n in notes if n.endswith('?'))
    if q_end > max(4, len(notes) * 0.35):
        errs.append(f'S{num}: {q_end} of {len(notes)} notes end on a question (at most 35%)')
    allnotes = ' '.join(notes)
    for pat, lim in SLOP_NOTES:
        k = len(re.findall(pat, allnotes))
        if k > lim:
            errs.append(f'S{num}: {k} uses of {pat!r} in the notes (at most {lim})')
    return errs


if __name__ == '__main__':
    nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[1:]) for p in (deck.BUILD / 'content').glob('s[0-9][0-9].py'))
    bad = 0
    for n in nums:
        for e in lint(n):
            print(e)
            bad += 1
    print(f'{bad} problems in {len(nums)} sessions')
    sys.exit(1 if bad else 0)
