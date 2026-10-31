"""Lint the authored slide content (concepts_*.py) and the built specs for house style.

    python Schools_ML_Track/camp_2026/build/slides/lint_slides.py [concepts_da_1 ...]

Checks: no em dashes, no antithesis emphasis, no filler words, titles state a claim (no 'Introduction to', 'Understanding',
'Overview of', no trailing period, at most 75 characters), at most 3 short points (14 words) per concept slide, notes between
35 and 190 words with no stage directions, no leftover placeholders, every figure name registered.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import figkit  # noqa: E402

STYLE = [
    (re.compile(r'—'), 'em dash'),
    (re.compile(r'\bnot (only|just|merely|simply)\b', re.I), 'not only/just'),
    (re.compile(r'\bnot [^.;:\n]{1,50}, but\b', re.I), 'not X, but Y'),
    (re.compile(r',\s+not\s+(a|an|the|to|about|because|for)\b', re.I), 'X, not Y'),
    (re.compile(r'\b(genuinely|honestly|straightforward|it is worth noting|let us dive|dive into|unlock|journey)\b', re.I), 'filler word'),
    (re.compile(r'\b(lorem|ipsum|TODO|TBD|XXX)\b', re.I), 'placeholder'),
]
TITLE_BAD = re.compile(r'^(introduction to|understanding|overview of|an overview|a look at|about)\b', re.I)
STAGE = re.compile(r'^(\[|\(|point to|click|pause|slide|note:|show |next slide|advance)', re.I)


def lint(mods):
    problems = []
    figs = None
    for name in mods:
        try:
            m = __import__(name)
        except ImportError as e:
            problems.append((name, f'cannot import: {e}'))
            continue
        figs = figkit.fig_registry()
        for key, spec in m.CONCEPTS.items():
            where = f'{name}:{key}'
            texts = []
            q = spec.get('question')
            if q:
                texts.append(('question say', q.get('say', '')))
                fn = q['fig'][0] if isinstance(q['fig'], (list, tuple)) else q['fig']
                if fn not in figs:
                    problems.append((where, f'question figure {fn!r} not registered'))
            else:
                problems.append((where, 'no question figure'))
            for i, c in enumerate(spec.get('slides', [])):
                t = c.get('title', '')
                w = f'{where} slide {i + 1}'
                if not t:
                    problems.append((w, 'no title'))
                if len(t) > 75:
                    problems.append((w, f'title too long ({len(t)})'))
                if TITLE_BAD.match(t) or t.rstrip().endswith('.'):
                    problems.append((w, f'title style: {t!r}'))
                pts = c.get('points', [])
                if len(pts) > 3:
                    problems.append((w, 'more than 3 points'))
                for p in pts:
                    if len(p.split()) > 14:
                        problems.append((w, f'point too long: {p[:50]!r}'))
                    texts.append((w + ' point', p))
                say = c.get('say', '')
                nw = len(say.split())
                if not 35 <= nw <= 190:
                    problems.append((w, f'notes {nw} words'))
                if STAGE.match(say.strip()):
                    problems.append((w, 'notes start like a stage direction'))
                texts += [(w + ' title', t), (w + ' say', say)]
                figs_used = [c['fig']] if 'fig' in c else c.get('figs', [])
                for f in figs_used:
                    fn = f[0] if isinstance(f, (list, tuple)) else f
                    if fn not in figs:
                        problems.append((w, f'figure {fn!r} not registered'))
            for label, t in texts:
                for rx, what in STYLE:
                    mm = rx.search(t or '')
                    if mm:
                        problems.append((where + ' ' + label, f'{what}: ...{t[max(0, mm.start() - 25):mm.end() + 25]}...'))
    return problems


if __name__ == '__main__':
    mods = sys.argv[1:] or ['concepts_da_1', 'concepts_da_2', 'concepts_da_3', 'concepts_ml_1', 'concepts_ml_2', 'concepts_ml_3']
    for pre in ('figs_common', 'figs_da', 'figs_da_r1', 'figs_da_r2', 'figs_ml', 'figs_ml_r3', 'figs_ml_r4'):
        try:
            __import__(pre)
        except ImportError:
            pass
    probs = lint(mods)
    for w, p in probs:
        print('LINT', w, p)
    print(f'{len(probs)} problems')
    sys.exit(1 if probs else 0)
