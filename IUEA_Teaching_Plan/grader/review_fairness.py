"""Review of every coded assessment (lecturer's instruction, 13 Nov 2026).

  "Ensure no unfair penalizing for such issues like creating new cells for code
   instead of answering within our created code cells. Review all."

Runs in the trusted evaluator only. Student code still runs only in the Docker
sandbox. Switch: IUEA_REVIEW_FAIRNESS=1 (default off, so every earlier result is
reproduced exactly). Every rule here only ADDS credit: the ordinary check decides
correctness, and each question keeps the higher of the earlier and the new award.

Patterns found by the review that lose marks without the method or answer being
wrong, and the rule for each:

R4 One broken line. A cell with a syntax error does not run at all, so every
   correct line in it is lost with the broken one (e.g. a stray `x =` line after a
   correct function). The cell is run again without the broken top-level
   statement(s) (at most MAX_REMOVED). The broken line itself earns nothing.
R5 Colab's Python 3.12. Colab runs Python 3.12; the sandbox runs 3.11. A cell that
   compiles only under 3.12 (PEP 701 f-strings such as f"{d["k"]}") is run as the
   equivalent 3.11 code produced by the trusted side (ast.unparse).
R6 Function keys one by one (Test 1 Q7). One key whose calculation raises (e.g. a
   typo in `.median()`) made the function raise, so the correct keys scored 0 too.
   Each returned value is evaluated on its own; a failing key still earns nothing.
R7 Dictionary keys ignoring case and spaces (Test 1 Q7 'mean ', Q8 'Low'): the
   values decide, when normalising the keys gives exactly the required keys.
R8 Grouped columns (Test 1 Q6): agg({'target': ['mean', 'count']}) gives two-level
   column names; the last level is used when it is exactly mean and count.
R9 Same points drawn twice (Test 1 Q2/Q4): identical scatter layers on one axes
   count once.
"""
import ast
import copy
import os
import re
import textwrap

REVIEW_VERSION = '2026.11-review-1'
FIX = {
    'salvage': 'review: cell run without its broken line',
    'py312': "review: Colab's Python 3.12 syntax",
    'keys_each': 'review: function keys checked one by one',
    'dict_keys': 'review: dictionary keys ignoring case and spaces',
    'columns': 'review: grouped column names flattened',
    'scatter': 'review: same points drawn twice counted once',
}
MAX_REMOVED = 3
Q7_FUNCTION = 'calculate_column_statistics'
SAFE_HELPER = ('def _iuea_safe(_iuea_f):\n'
               '    try:\n'
               '        return _iuea_f()\n'
               '    except Exception:\n'
               '        return None\n')


def enabled():
    return os.environ.get('IUEA_REVIEW_FAIRNESS', '0') == '1'


def _text(cell):
    s = cell.get('source', '')
    return ''.join(s) if isinstance(s, list) else str(s)


def _worker_source(cell):
    """The cell as the worker runs it (notebook magics become comments)."""
    return '\n'.join('# notebook magic omitted' if line.lstrip().startswith(('%', '!', '?')) else line
                     for line in _text(cell).splitlines())


def _parses(source):
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


# --------------------------------------------------------------------------- #
# R4: one broken line
# --------------------------------------------------------------------------- #
def salvage(source, max_removed=MAX_REMOVED):
    """`source` without the top-level statement(s) that stop it compiling, or None.
    Pure text processing on the trusted side."""
    if _parses(source) or _parses(textwrap.dedent(source)):
        return None
    lines = source.split('\n')
    removed = 0
    while removed < max_removed:
        try:
            ast.parse('\n'.join(lines))
            break
        except SyntaxError as exc:
            at = min(max((exc.lineno or 1) - 1, 0), len(lines) - 1)
        # The top-level statement holding the error: back to its unindented first line,
        # forward over indented / continuation lines.
        start = at
        while start > 0 and (not lines[start].strip() or lines[start][:1] in (' ', '\t')):
            start -= 1
        end = at + 1
        while end < len(lines) and (not lines[end].strip() or lines[end][:1] in (' ', '\t')
                                    or lines[end].lstrip()[:1] in (')', ']', '}')):
            end += 1
        if all(not l.strip() or l.lstrip().startswith('#') for l in lines[start:end]):
            return None
        lines = lines[:start] + [''] * (end - start) + lines[end:]
        removed += 1
    text = '\n'.join(lines)
    return text if removed and _parses(text) else None


# --------------------------------------------------------------------------- #
# R5: Python 3.12 syntax
# --------------------------------------------------------------------------- #
def py311_equivalent(source):
    """ast.unparse of a cell that parses here (Python 3.12) and uses f-strings: the
    worker uses it only if the original does not compile under the sandbox's 3.11."""
    if not re.search(r'''(?<![A-Za-z0-9_])[fF][rR]?["']|(?<![A-Za-z0-9_])[rR][fF]["']''', source):
        return None
    try:
        out = ast.unparse(ast.parse(source))
    except (SyntaxError, ValueError, RecursionError):
        return None
    return out if out.strip() != source.strip() else None


# --------------------------------------------------------------------------- #
# R6: function keys one by one (Test 1 Q7)
# --------------------------------------------------------------------------- #
class _WrapReturnDict(ast.NodeTransformer):
    def __init__(self):
        self.changed = False

    def visit_Return(self, node):
        if isinstance(node.value, ast.Dict) and node.value.keys and all(k is not None for k in node.value.keys):
            node.value.values = [ast.Call(func=ast.Name(id='_iuea_safe', ctx=ast.Load()),
                                          args=[ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[],
                                                                              kw_defaults=[], defaults=[]), body=v)],
                                          keywords=[]) for v in node.value.values]
            self.changed = True
        return node


def keys_each(source, function=Q7_FUNCTION):
    """The cell with each value of `function`'s returned dict evaluated on its own
    (a value that raises becomes None), or None when there is nothing to change."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    t = _WrapReturnDict()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function:
            t.visit(node)
    if not t.changed:
        return None
    ast.fix_missing_locations(tree)
    return SAFE_HELPER + ast.unparse(tree)


def repairs(notebook, assignment, q7=False):
    """{str(cell index): {'alts': [...], 'replace': src}, '__kinds__': {...}} for the worker."""
    out, kinds = {}, set()
    for index, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') != 'code':
            continue
        source = _worker_source(cell)
        if not source.strip():
            continue
        fix = {}
        if q7 and assignment == 'TEST1' and re.search(r'\bdef\s+%s\b' % Q7_FUNCTION, source):
            rep = keys_each(source)
            if rep:
                fix['replace'] = rep
                fix['kind'] = 'keys_each'
                kinds.add('keys_each')
                source = rep
        if _parses(source):
            alt = py311_equivalent(source)
            if alt:
                fix['alts'] = [alt]
                fix.setdefault('kind', 'py312')
                kinds.add('py312')
        else:
            alt = salvage(source)
            if alt:
                fix['alts'] = [alt]
                fix.setdefault('kind', 'salvage')
                kinds.add('salvage')
        if fix:
            out[str(index)] = fix
    return out, kinds


def needs_run(repair, kinds, cell_errors):
    """A repair run is needed for the Q7 rewrite, or when a cell failed to compile in the
    sandbox (the worker uses an alternative only for such a cell)."""
    if not repair:
        return False
    if 'keys_each' in kinds:
        return True
    syntax = any(str(e.get('etype', '')) in ('SyntaxError', 'IndentationError', 'TabError')
                 for e in cell_errors or [] if isinstance(e, dict))
    return syntax and bool(kinds & {'salvage', 'py312'})


def used_kinds(repair, second):
    """The repair kinds that actually ran: every 'replace', and each alternative the
    worker reports it used ('review repair used')."""
    notes = list((second or {}).get('worker_notes') or [])
    notes += list(((second or {}).get('fairness') or {}).get('worker_notes') or [])
    cells = {int(n['cell']) - 1 for n in notes if isinstance(n, dict) and n.get('note') == 'review repair used'}
    used = set()
    for index, fix in (repair or {}).items():
        if 'replace' in fix:
            used.add('keys_each')
        if int(index) in cells:
            used.add(fix.get('kind', 'salvage') if fix.get('kind') != 'keys_each' else 'py312')
    return used


def merge(first, second, kinds, label='review_repair', repair=None):
    """Per question the higher award; `first` is never lowered. Returns {qid: note}."""
    notes = {}
    if repair is not None:
        kinds = used_kinds(repair, second) or set(kinds)
    fix = ' + '.join(FIX[k] for k in sorted(kinds))
    for qid, q in first.get('questions', {}).items():
        s = (second or {}).get('questions', {}).get(qid)
        if not s or s['awarded'] <= q['awarded'] + 1e-9:
            continue
        notes[qid] = dict(original=q['awarded'], awarded=s['awarded'], fix=fix, detail='repaired cells re-run')
        q.update(awarded=s['awarded'], ok=s.get('ok', False),
                 msg='Credited by %s. %s' % (fix, q.get('msg') or ''))
    first.setdefault('fairness', {})
    if isinstance(first['fairness'], dict):
        first['fairness'][label] = dict(version=REVIEW_VERSION, kinds=sorted(kinds), notes=notes,
                                        error=(second or {}).get('error', ''))
    return notes


def review_ca(evaluate, first, work, spec_path, hidden_path, assignment, cohort, per_cell, total_timeout, fairness):
    """A2-A5: a second run with the repaired cells when a cell cannot run as written."""
    import json
    from pathlib import Path
    try:
        notebook = json.loads((Path(work) / 'submission.ipynb').read_text())
        repair, kinds = repairs(notebook, assignment)
    except Exception as exc:  # noqa: BLE001
        first.setdefault('fairness', {})['review_repair'] = dict(version=REVIEW_VERSION, error=str(exc)[:200], notes={})
        return first
    if not any(q['awarded'] < q['marks'] - 1e-9 for q in first.get('questions', {}).values()) or \
            not needs_run(repair, kinds, first.get('cell_errors')):
        first.setdefault('fairness', {})['review_repair'] = dict(version=REVIEW_VERSION, kinds=[], notes={})
        return first
    try:
        second = evaluate(work, spec_path, hidden_path, assignment, cohort, per_cell, total_timeout,
                          fairness=fairness, repair=repair)
    except Exception as exc:  # noqa: BLE001
        second = dict(questions={}, error='%s: %s' % (type(exc).__name__, str(exc)[:200]))
    merge(first, second, kinds, repair=repair)
    return first


# --------------------------------------------------------------------------- #
# R7-R9: answers read through a normalising view (Test 1)
# --------------------------------------------------------------------------- #
def norm_keys(value, required):
    """dict with keys stripped and lower-cased, when that gives exactly `required`."""
    if not isinstance(value, dict):
        return None
    new = {}
    for k, v in value.items():
        key = str(k).strip().lower() if isinstance(k, str) else k
        if key in new:
            return None
        new[key] = v
    if set(new) != set(required) or set(value) == set(required):
        return None
    return new


def flatten_columns(frame, wanted=('mean', 'count')):
    import pandas as pd
    if not isinstance(frame, pd.DataFrame):
        return None
    cols = list(frame.columns)
    if not cols or not all(isinstance(c, tuple) for c in cols):
        return None
    for option in (cols, [tuple(x) for x in zip(*cols)]):
        if len(option) != len(cols):
            continue
        last = [c[-1] if isinstance(c, tuple) and c else None for c in option]
        if sorted(map(str, last)) == sorted(wanted):
            out = frame.copy()
            out.columns = [str(x) for x in last]
            return out
    return None


def dedupe_scatter(figure):
    from isolated_grading import PlotEvidence
    if not isinstance(figure, PlotEvidence) or len(figure.get('plot_axes', [])) != 1:
        return None
    ax = figure['plot_axes'][0]
    import math

    def finite(c):
        return sorted(tuple(p) for p in c if all(v is not None and math.isfinite(v) for v in p))
    layers = [finite(c) for c in ax.get('scatter', [])]
    if len(layers) < 2 or any(layer != layers[0] for layer in layers[1:]) or not layers[0]:
        return None
    new = copy.deepcopy(dict(ax))
    new['scatter'] = [ax['scatter'][0]]
    return PlotEvidence(plot_axes=[new])


class ReviewView:
    """Namespace view applying R7-R9 to the named answers; everything else as the base."""
    DICTS = {'load_band_counts': ('low', 'medium', 'high')}

    def __init__(self, base):
        self.base = base
        self.cache = {}
        self.used = set()

    def __getattr__(self, attr):
        return getattr(self.base, attr)

    def get(self, name, default=None):
        value = self.base.get(name, default)
        if name in self.DICTS:
            fixed = norm_keys(value, self.DICTS[name])
            if fixed is not None:
                self.used.add('dict_keys')
                return fixed
        if name == 'equipment_summary':
            fixed = flatten_columns(value)
            if fixed is not None:
                self.used.add('columns')
                return fixed
        if name in ('before_figure', 'after_figure'):
            fixed = dedupe_scatter(value)
            if fixed is not None:
                self.used.add('scatter')
                return fixed
        return value


def view_pass_t1(ig, worker, per_cell, cohort, lenient, results, scopes):
    """Test 1 questions below full marks, re-checked through ReviewView in every scope
    (whole notebook, own-cell snapshots, reference re-runs), and Q7 with its returned
    keys normalised. Only raises. Returns {qid: note}."""
    notes = {}
    for qid, question in lenient:
        res = results[qid]
        if res['awarded'] >= res['marks'] - 1e-9:
            continue
        best = None
        if qid == 'q7':
            import test1_fairness as tf
            for label, scope in scopes['q7']:
                credit = tf._q7_fraction(worker, per_cell, scope, cohort, tf.FUNCTION, keyfix=True) * res['marks']
                if credit > res['awarded'] + 1e-9 and (best is None or credit > best[0] + 1e-9):
                    best = (round(credit, 4), {'dict_keys'}, label)
        else:
            extra = [scopes['rerun'][qid]] if qid in scopes.get('rerun', {}) else []
            for label, ns in list(scopes['ns']) + extra:
                view = ReviewView(ns)
                try:
                    r = ig.run_check(qid, question, view)
                except Exception:  # noqa: BLE001
                    continue
                if view.used and r.awarded > res['awarded'] + 1e-9 and (best is None or r.awarded > best[0] + 1e-9):
                    best = (r.awarded, set(view.used), label)
        if best:
            fix = ' + '.join(FIX[k] for k in sorted(best[1]))
            notes[qid] = dict(original=res['awarded'], awarded=best[0], fix=fix, detail=best[2])
            res.update(awarded=best[0], ok=best[0] >= res['marks'] - 1e-9, fix=fix, detail=best[2])
    return notes
