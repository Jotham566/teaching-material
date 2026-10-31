"""Verify the Holiday Data and AI Camp pack (revision 2).

What it proves
  * structure: 24 lessons per track, schema fields, words <= 6, two error cards, clocks sum to 180
  * every python block runs against the real data and its `check` expression is True,
    every Modify answer and Make reference runs and its check is True
  * the four ML labs run and their checks hold
  * only the approved libraries are imported; no SQL or statistics module in teen material
  * house style: no antithesis emphasis, no em dashes, no filler words
  * generated sheets, notebooks, guides, glossaries exist and the notebooks are valid
Sessions that need scikit-learn are SKIPPED, and reported as skipped, when scikit-learn is
not installed. Run this on a machine with the camp environment to execute them.

    python Schools_ML_Track/camp_2026/build/verify_camp.py
"""
import ast
import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import traceback

os.environ['MPLBACKEND'] = 'Agg'
import warnings
warnings.filterwarnings('ignore', message='FigureCanvasAgg is non-interactive')
from common import ROOT, CURRICULUM, ALLOWED_IMPORTS, BANNED_TERMS, DEFAULT_CLOCK, DATA_DA, DATA_ML
from content import ML, DA, LABS, EXTENSION

try:
    import sklearn  # noqa: F401
    HAVE_SK = True
except Exception:
    HAVE_SK = False

failures = []
skipped = []
passed = 0
STUDENT = {'DA': ROOT / 'student_materials' / 'DA', 'ML': ROOT / 'student_materials' / 'ML'}


def fail(msg):
    failures.append(msg)
    print('FAIL', msg)


def ok():
    global passed
    passed += 1


def all_text(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from all_text(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from all_text(v)


def needs_sk(l):
    if l.get('needs_sklearn'):
        return True
    for b in l['blocks']:
        if b.get('needs_sklearn') or (b.get('code') and 'sklearn' in b['code']):
            return True
    mk = l['make']
    return bool(mk.get('needs_sklearn') or (mk.get('reference_is_code') and 'sklearn' in mk['reference']))


def execute(track, ident, steps):
    """steps: list of ('exec'|'eval', text, label). Returns None or an error string."""
    import matplotlib.pyplot as plt
    files = DATA_DA if track == 'DA' else DATA_ML
    tmp = tempfile.mkdtemp()
    for f in files:
        shutil.copy2(STUDENT[track] / f, tmp)
    prev = os.getcwd()
    os.chdir(tmp)
    ns = {'__name__': '__main__'}
    try:
        for kind, text, label in steps:
            with contextlib.redirect_stdout(io.StringIO()):
                if kind == 'exec':
                    exec(compile(text, f'{ident}:{label}', 'exec'), ns)
                    plt.close('all')
                else:
                    if not eval(text, ns):
                        return f'{label}: check evaluated False: {text}'
        return None
    except Exception:
        return f'{label}: {traceback.format_exc(limit=3).strip().splitlines()[-1]}'
    finally:
        os.chdir(prev)
        shutil.rmtree(tmp, ignore_errors=True)


STYLE = [
    (re.compile(r'\bnot (only|just|merely|simply)\b', re.I), 'not only/just contrast'),
    (re.compile(r'\bnot [^.;:\n]{1,50}, but\b', re.I), '"not X, but Y" contrast'),
    (re.compile(r',\s+not\s+(a|an|the|to|about|because|for)\b', re.I), '"X, not Y" contrast'),
    (re.compile(r'—'), 'em dash'),
    (re.compile(r'\b(genuinely|honestly|straightforward|it is worth noting)\b', re.I), 'filler word'),
]


def check_lesson(track, i, l):
    ident = f'{track}{i:02}'
    for k in ('title', 'objective', 'question', 'words', 'blocks', 'make', 'errors', 'exit_ticket', 'mode', 'libs', 'data', 'misconceptions', 'questions'):
        if k not in l:
            fail(f'{ident}: missing {k}')
            return
    if not l['objective'].startswith('By the end:'):
        fail(f'{ident}: objective must start "By the end:"')
    if len(l['words']) > 6:
        fail(f'{ident}: {len(l["words"])} words, limit 6')
    if any(len(w) != 3 for w in l['words']):
        fail(f'{ident}: each word needs (term, definition, comparison)')
    if len(l['errors']) != 2 or any(len(e) != 3 for e in l['errors']):
        fail(f'{ident}: exactly two (see, means, fix) error cards required')
    if len(l['blocks']) > 2:
        fail(f'{ident}: more than two blocks')
    if l['mode'] not in ('python', 'guide'):
        fail(f'{ident}: bad mode')
    if not l['misconceptions'] or not l['questions']:
        fail(f'{ident}: instructor misconceptions and questions required')
    if l.get('pacing'):
        mins = [int(m) for m in re.findall(r'(\d+)\s*minutes?', l['pacing'])]
        if sum(mins) != 180:
            fail(f'{ident}: pacing sums to {sum(mins)}')
    for b in l['blocks']:
        if not 2 <= len(b['investigate']) <= 3:
            fail(f'{ident}: block "{b["idea"]}" needs 2 or 3 investigate questions')
        if l['mode'] == 'python' and b.get('code') and not b.get('check') and not b.get('nocheck'):
            fail(f'{ident}: block "{b["idea"]}" has code but no check')
    # style and banned terms
    for t in all_text(l):
        for rx, label in STYLE:
            m = rx.search(t)
            if m:
                fail(f'{ident}: style ({label}): "...{t[max(0, m.start() - 30):m.end() + 30]}..."')
        for term in BANNED_TERMS:
            if term.lower() in t.lower():
                fail(f'{ident}: banned term "{term}"')
    # imports
    codes = [b.get('code') for b in l['blocks'] if b.get('code')]
    codes += [b['modify'].get('code') for b in l['blocks'] if b['modify'].get('code')]
    if l['make'].get('reference_is_code'):
        codes.append(l['make']['reference'])
    for src in codes:
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            fail(f'{ident}: syntax error {e}')
            continue
        for n in ast.walk(tree):
            mods = [a.name.split('.')[0] for a in n.names] if isinstance(n, ast.Import) else ([n.module.split('.')[0]] if isinstance(n, ast.ImportFrom) and n.module else [])
            for m in mods:
                if m not in ALLOWED_IMPORTS:
                    fail(f'{ident}: import {m} is outside the approved stack')
    ok()


def exec_lesson(track, i, l):
    ident = f'{track}{i:02}'
    if needs_sk(l) and not HAVE_SK:
        skipped.append(ident)
        return
    blocks = l['blocks'] if l['mode'] == 'python' else []
    for bi, b in enumerate(blocks):
        if not b.get('code'):
            continue
        base = [('exec', x['code'], f'block {bi + 1} code') for x in blocks[:bi + 1] if x.get('code')]
        steps = base + ([('eval', b['check'], f'block {bi + 1} check')] if b.get('check') else [])
        err = execute(track, ident, steps)
        err and fail(f'{ident}: {err}')
        mod = b['modify']
        if mod.get('code'):
            steps = base + [('exec', mod['code'], f'block {bi + 1} modify')] + ([('eval', mod['check'], f'block {bi + 1} modify check')] if mod.get('check') else [])
            err = execute(track, ident, steps)
            err and fail(f'{ident}: {err}')
        elif mod.get('check'):
            fail(f'{ident}: modify check without modify code')
    mk = l['make']
    if mk.get('reference_is_code'):
        steps = [('exec', mk['reference'], 'make reference')] + ([('eval', mk['check'], 'make check')] if mk.get('check') else [])
        err = execute(track, ident, steps)
        err and fail(f'{ident}: {err}')
        if not mk.get('check'):
            fail(f'{ident}: make reference is code but has no check')
    ok()


def main():
    try:
        import nbformat
    except ImportError:
        nbformat = None
    for track, lessons in (('ML', ML), ('DA', DA)):
        assert len(lessons) == 24, track
        titles = [l['title'] for l in lessons]
        if len(set(titles)) != 24:
            fail(f'{track}: duplicate titles')
        seen = {}
        for i, l in enumerate(lessons, 1):
            check_lesson(track, i, l)
            for w in l['words']:
                k = w[0].lower()
                if k in seen:
                    fail(f'{track}{i:02}: word "{w[0]}" already defined in session {seen[k]}')
                seen[k] = i
            exec_lesson(track, i, l)
            ident = f'{track}{i:02}'
            for p in (STUDENT[track] / f'{ident}.md', STUDENT[track] / f'{ident}.ipynb', ROOT / 'instructor_materials' / track / f'{ident}_guide.md'):
                if not p.exists():
                    fail(f'missing generated file {p.name}')
            nb = STUDENT[track] / f'{ident}.ipynb'
            if nb.exists():
                try:
                    if nbformat:
                        nbformat.validate(nbformat.read(nb, as_version=4))
                    else:  # minimal structural check when nbformat is not installed
                        d = json.loads(nb.read_text())
                        assert d['nbformat'] == 4 and all('id' in c and 'source' in c for c in d['cells'])
                except Exception as e:
                    fail(f'{ident}.ipynb invalid: {e}')
        for g in (CURRICULUM / f'GLOSSARY_{track}.md', CURRICULUM / f'CURRICULUM_{track}.md', CURRICULUM / f'CLASS_PLAN_{track}.md'):
            if not g.exists():
                fail(f'missing {g.name}')
        for f in (DATA_DA if track == 'DA' else DATA_ML):
            if not (STUDENT[track] / f).exists():
                fail(f'{track}: data file {f} missing from student folder')
    # labs
    for n, lab in enumerate(LABS, 1):
        name = f'F{n:02}'
        if len(lab['words']) > 6:
            fail(f'{name}: more than six words')
        for t in all_text(lab):
            for rx, label in STYLE:
                m = rx.search(t)
                if m:
                    fail(f'{name}: style ({label}): "...{t[max(0, m.start() - 30):m.end() + 30]}..."')
            for term in BANNED_TERMS:
                if term.lower() in t.lower():
                    fail(f'{name}: banned term "{term}"')
        if 'sklearn' in lab['code'] and not HAVE_SK:
            skipped.append(name)
            continue
        err = execute('ML', name, [('exec', lab['code'], 'lab code'), ('eval', lab['check'], 'lab check')])
        err and fail(f'{name}: {err}')
        ok()
    if EXTENSION.get('needs_sklearn') and not HAVE_SK:
        skipped.append('ML25')
    else:
        err = execute('ML', 'ML25', [('exec', EXTENSION['code'], 'extension'), ('eval', EXTENSION['check'], 'extension check')])
        err and fail(f'ML25: {err}')
    # reference numbers
    ref = json.loads((ROOT / 'instructor_materials' / 'reference_values.json').read_text())
    cs = ref['camp_shop']
    if (cs['row_count'], cs['total_units'], cs['revenue_ugx']) != (60, 277, 550000):
        fail(f'camp_shop reference changed: {cs}')
    report = {'passed': passed, 'failed': len(failures), 'skipped_need_scikit_learn': skipped, 'scikit_learn_installed': HAVE_SK,
              'failures': failures}
    out = ROOT.parents[1] / 'review' / '2026-10-31' / 'schools-camp' / 'verification.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(f'\n{passed} items passed, {len(failures)} failed, {len(skipped)} skipped (need scikit-learn: {", ".join(skipped) or "none"})')
    if not HAVE_SK:
        print('scikit-learn is not installed here. Run this script in the camp environment to execute the skipped sessions.')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
