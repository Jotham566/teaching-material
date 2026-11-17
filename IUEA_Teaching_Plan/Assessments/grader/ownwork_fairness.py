"""Own-work credit for coded answers (lecturer's rule, 13 Nov 2026).

  "We shouldn't penalize students if they wrote their own code cells, as long as
   they wrote the correct code and answered the question."

Runs in the trusted evaluator only. Student code still runs only in the Docker
sandbox; the worker (isolated_worker.py, init(ownwork=True)) records what each cell
printed, displayed or showed as its last expression, and every figure still open
when the cell finished, encoded at that moment. Nothing here executes student code.

Switch: IUEA_OWNWORK_FAIRNESS=1 turns it on (default off, so the ordinary and the
10 Nov fairness results are unchanged). It is used by test1_fairness.py (Test 1)
and by isolated_grading._fairness_pass (A2-A5, W02-W05).

For each question below full marks, after the 10 Nov passes, and applied the same
way to every student:

1. Different names, FULL credit. A student variable or function holding the answer
   under another name counts in full when it is unambiguous: it is the only
   candidate of that kind (DataFrame, number, dict, function ...) among the names
   the student assigned in that question's own cells or names sharing a word with
   the required one, or the only such candidate that shares a word with it.
   Otherwise it is flagged AMBIGUOUS_NAME for the lecturer and earns nothing new.
2. Printed answers count. A value the student's own cells printed, displayed or
   left as the cell's last expression, in that question's cells, counts when the
   ordinary check accepts it (same type, value within the usual tolerance).
3. Charts on the student's own figure count. A figure drawn in that question's
   cells (or kept under another name) is checked by the ordinary chart check:
   the right data, a title, and axis labels with units.
4. The ordinary check decides correctness every time, so wrong is still wrong;
   the caller keeps the higher of the stored and the new award.

The same evidence is read in the whole-notebook namespace, the best own-cell
snapshot and, for Test 1, the question's reference-input re-run (10 Nov rule).
"""
import ast
import os
import re

OWNWORK_VERSION = '2026.11-ownwork-1'
FIX_NAME = 'own work: answer under a different name (full credit)'
FIX_PRINT = 'own work: printed or displayed answer'
FIX_CHART = 'own work: chart on the student\'s own figure'
MAX_NAME_CANDIDATES = 24
MAX_OUTPUT_CANDIDATES = 80


def enabled():
    return os.environ.get('IUEA_OWNWORK_FAIRNESS', '0') == '1'


# --------------------------------------------------------------------------- #
# Notebook structure (pure text processing)
# --------------------------------------------------------------------------- #
def _text(cell):
    s = cell.get('source', '')
    return ''.join(s) if isinstance(s, list) else str(s)


_Q_HEADING = re.compile(r'^\s*#{1,6}\s*(q\d+)\b', re.I | re.M)
_ANY_HEADING = re.compile(r'^\s*#{1,6}\s*(\S+)', re.M)


def question_cells(notebook, assignment, required_fn, qids):
    """{qid: [cell index]} - the code cells that belong to each question.

    Test 1: test1_fairness.task_cells (answer tags, else 'Task N' headings; student
    cells after an answer cell belong to that task). A2-A5: a markdown heading
    '## q3: ...' or '## mean_reading (5 marks)' starts that question; a heading
    that is neither ends it. W02 has no question headings: a question's cells are
    the cells whose code mentions its required name."""
    cells = notebook.get('cells', [])
    if assignment == 'TEST1':
        import test1_fairness as tf
        by_task = tf.task_cells(notebook)
        return {qid: list(by_task.get(task, [])) for qid, task in zip(qids, tf.TASKS)}
    by_name = {}
    for qid in qids:
        for n in required_fn(qid):
            by_name.setdefault(n.lower(), qid)
    out = {qid: [] for qid in qids}
    current, headed = None, False
    for index, cell in enumerate(cells):
        text = _text(cell)
        if cell.get('cell_type') == 'markdown':
            m = _Q_HEADING.search(text)
            if m and m.group(1).lower() in out:
                current, headed = m.group(1).lower(), True
                continue
            h = _ANY_HEADING.search(text) if text.lstrip().startswith('#') else None
            if h:
                word = re.sub(r'[^\w]', '', h.group(1)).lower()
                if word in by_name:
                    current, headed = by_name[word], True
                else:
                    current = None
            continue
        if cell.get('cell_type') == 'code' and current:
            out[current].append(index)
    if not headed:
        for index, cell in enumerate(cells):
            if cell.get('cell_type') != 'code':
                continue
            words = set(re.findall(r'[A-Za-z_]\w*', _text(cell)))
            for qid in qids:
                if words & set(required_fn(qid)):
                    out[qid].append(index)
    return out


def assigned_names(notebook, indices):
    """Names the given cells bind at top level: assignments (also tuple targets),
    augmented/annotated assignments, def and class names."""
    found = []
    cells = notebook.get('cells', [])
    for i in indices:
        if i >= len(cells):
            continue
        source = '\n'.join('# magic' if l.lstrip().startswith(('%', '!', '?')) else l
                           for l in _text(cells[i]).splitlines())
        try:
            tree = ast.parse(source)
        except SyntaxError:
            try:
                import textwrap
                tree = ast.parse(textwrap.dedent(source))
            except SyntaxError:
                continue
        for node in tree.body:
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
                targets = [node.target]
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name not in found:
                    found.append(node.name)
                continue
            for t in targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name) and n.id not in found:
                        found.append(n.id)
    return found


# --------------------------------------------------------------------------- #
# Checking
# --------------------------------------------------------------------------- #
def family(value):
    """Kind of value, used to decide whether a renamed answer is unambiguous."""
    import numbers
    if value is None or (isinstance(value, str) and value == '__MISSING__'):
        return None
    try:
        from isolated_grading import PlotEvidence
        if isinstance(value, PlotEvidence):
            return 'figure'
    except Exception:  # noqa: BLE001
        pass
    if callable(value):
        return 'callable'
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, numbers.Number):
        return 'number'
    if isinstance(value, str):
        return 'text'
    if isinstance(value, (list, tuple)):
        return 'list'
    if isinstance(value, dict):
        return 'dict'
    t = type(value).__name__
    return {'DataFrame': 'table', 'Series': 'series', 'ndarray': 'array'}.get(t, t)


class View:
    """Namespace view: each required name reads another name or a recorded output.
    For a renamed variable the source scans (loop structure, info() call) see the
    required name too, so the answer is checked exactly as if it had that name."""

    def __init__(self, base, names, renamed=()):
        self.base, self.names = base, dict(names)
        self.cache = {}
        sources = getattr(base, 'notebook_sources', [])
        for req, cand in self.names.items():
            if cand in renamed:
                sources = [re.sub(r'\b%s\b' % re.escape(cand), req, s) for s in sources]
        self.notebook_sources = sources

    def __getattr__(self, attr):
        return getattr(self.base, attr)

    def get(self, name, default=None):
        return self.base.get(self.names.get(name, name), default)


def _score(ig, qid, question, ns):
    try:
        return ig.run_check(qid, question, ns)
    except Exception:  # noqa: BLE001
        return None


def _safe_get(ns, name):
    try:
        return ns.get(name)
    except Exception:  # noqa: BLE001
        return None


def rescore(ig, gf, qid, question, res, scopes, required, watch, local_names, student_names, outputs,
            figure_names=(), foreign=(), moved=()):
    """Own-work pass for one question. `scopes` = [(label, ns, rerun_key)]; `outputs` =
    the worker's record list; `local_names` = names bound in this question's cells;
    `foreign` = names bound in OTHER questions' cells and not in this one's (those
    answer the other question and are never candidates here); `moved` = names whose
    last binding is in another question's cells (their final value is not this
    question's work, so they are only read in this question's re-run); `required` =
    the names the question reads. A printed value that is the stored value of another
    required name (e.g. the modes printed as the 'standard deviation') is that other
    answer and is not used. Updates `res` upwards only.
    Returns (note or None, flags)."""
    flags = []
    marks = res['marks']
    if res['awarded'] >= marks - 1e-9 or not required:
        return None, flags
    best = dict(awarded=res['awarded'])
    watch = set(watch)
    foreign = set(foreign) - set(local_names)
    moved = set(moved)
    for label, ns, key in scopes:
        excluded = foreign if key is not None else foreign | moved
        base = _score(ig, qid, question, ns)
        if base is None:
            continue
        base_award = base.awarded
        mapping, kinds, renamed, evidence = {}, {}, set(), []
        for req in required:
            cands = []
            # Rule 1: a different name (and rule 3 for a figure kept under another name).
            pool = [c for c in student_names if c != req and c not in watch and not c.startswith('_')
                    and c not in gf.NOT_ALIASES and c not in excluded and gf.alias_tier(req, c)]
            pool += [c for c in local_names if c != req and c not in watch and not c.startswith('_')
                     and c not in gf.NOT_ALIASES and c not in pool and c not in excluded]
            pool = pool[:MAX_NAME_CANDIDATES]
            fams = {c: family(_safe_get(ns, c)) for c in pool}
            for c in pool:
                f = fams[c]
                if f is None:
                    continue
                same = [d for d in pool if fams[d] == f]
                shared = [d for d in same if gf.alias_tier(req, d)]
                if f == 'figure' and req in figure_names:
                    cands.append((c, 'chart', c))
                elif len(same) == 1 or (gf.alias_tier(req, c) and len(shared) == 1):
                    cands.append((c, 'name', c))
                else:
                    cands.append((c, 'ambiguous', c))
            # Rules 2 and 3: what this question's own cells printed, displayed or drew.
            outs = [o for o in outputs if o.get('rerun') == key and o.get('cell') in local_cells_of(question)]
            for o in outs[:MAX_OUTPUT_CANDIDATES]:
                kind = 'chart' if o.get('kind') == 'figure' else 'print'
                if kind == 'chart' and req not in figure_names:
                    continue
                cands.append((o['key'], kind, 'cell %s %s: %s' % (o.get('cell'), o.get('kind'), o.get('text', '')[:80])))
            top = None
            for cand, kind, what in cands:
                r = _score(ig, qid, question, View(ns, {req: cand}, renamed={cand} if kind == 'name' else ()))
                if r is None or r.awarded <= base_award + 1e-9:
                    continue
                if kind == 'print' and _is_other_answer(ns, cand, req, watch):
                    flags.append('PRINTED_OTHER_ANSWER %s: %s matches %s but is the stored value of another answer (%s)' % (
                        qid, what[:60], req, label))
                    continue
                if kind == 'ambiguous':
                    flags.append('AMBIGUOUS_NAME %s: %s for %s would add %.4g (%s) - more than one %s candidate' % (
                        qid, cand, req, r.awarded - base_award, label, family(_safe_get(ns, cand))))
                    continue
                if top is None or r.awarded > top[0] + 1e-9:
                    top = (r.awarded, cand, kind, what)
            if top:
                mapping[req] = top[1]
                kinds[req] = top[2]
                if top[2] == 'name':
                    renamed.add(top[1])
                evidence.append('%s <- %s' % (req, top[3]))
        if not mapping:
            continue
        r = _score(ig, qid, question, View(ns, mapping, renamed=renamed))
        if r is None or r.awarded <= best['awarded'] + 1e-9:
            continue
        used = sorted(set(kinds.values()))
        fix = ' + '.join({'name': FIX_NAME, 'print': FIX_PRINT, 'chart': FIX_CHART}[k] for k in used)
        if key is not None:
            fix += ' (on the reference inputs)'
        best = dict(awarded=r.awarded, ok=r.ok, msg=r.message, fix=fix,
                    detail='%s; %s' % (label, '; '.join(evidence)))
    if 'fix' not in best:
        return None, sorted(set(flags))
    note = dict(original=res['awarded'], awarded=min(marks, best['awarded']), fix=best['fix'], detail=best['detail'])
    res['awarded'] = note['awarded']
    res['ok'] = bool(best.get('ok')) and res['awarded'] >= marks - 1e-9
    res['msg'] = 'Credited by %s: %s. %s' % (best['fix'], best['detail'], res.get('msg') or '')
    res['fix'], res['detail'] = best['fix'], best['detail']
    return note, sorted(set(flags))


def _same(a, b):
    from test1_coding_v3 import equal
    if b is None or (isinstance(b, str) and b == '__MISSING__') or callable(b):
        return False
    try:
        return bool(equal(a, b))
    except Exception:  # noqa: BLE001
        return False


def _is_other_answer(ns, key, req, watch):
    value = _safe_get(ns, key)
    for other in watch:
        if other != req and _same(value, _safe_get(ns, other)):
            return True
    return False


def local_cells_of(question):
    return question.get('_ownwork_cells', ())


def with_cells(question, cells):
    """The question dict with its own cell labels (1-based, as the worker reports them)."""
    q = dict(question)
    q['_ownwork_cells'] = frozenset(int(i) + 1 for i in cells)
    return q


def pick_scopes(ig, qid, question, namespaces, extra=()):
    """The whole-notebook namespace, the best own-cell snapshot for this question, and
    any extra (re-run) scopes: [(label, ns, rerun_key)]."""
    scopes = [(namespaces[0][0], namespaces[0][1], None)]
    best = None
    for label, ns in namespaces[1:]:
        r = _score(ig, qid, question, ns)
        if r is not None and (best is None or r.awarded > best[0] + 1e-9):
            best = (r.awarded, label, ns)
    if best is not None:
        scopes.append((best[1], best[2], None))
    scopes.extend(extra)
    return scopes


def foreign_names(notebook, cells, qid):
    """Names bound in the cells of the other questions."""
    out = set()
    for other, idx in cells.items():
        if other != qid:
            out.update(assigned_names(notebook, idx))
    return out


def moved_names(notebook, cells, qid):
    """Names whose last top-level binding (in notebook order) is in another question's cells."""
    owner = {}
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'code':
            for n in assigned_names(notebook, [i]):
                owner[n] = i
    others = {i for other, idx in cells.items() if other != qid for i in idx}
    return {n for n, i in owner.items() if i in others}


def run_ca(ig, gf, worker, assignment, cohort, questions, results, namespaces, notebook, names):
    """A2-A5 (W02-W05): the own-work pass after grader_fairness.rescore."""
    outputs = worker.request(op='outputs')
    outputs = outputs if isinstance(outputs, list) else []
    qids = [q for q, _ in questions]
    required_fn = lambda q: gf.required_names(assignment, q, cohort)
    cells = question_cells(notebook, assignment, required_fn, qids)
    watch = gf.watch_names(assignment, cohort)
    notes, flags = {}, []
    for qid, question in questions:
        res = results[qid]
        if res['awarded'] >= res['marks'] - 1e-9:
            continue
        required = [n for n in required_fn(qid) if n not in ('STUDENT_ID',)]
        if not required:
            continue
        q = with_cells(question, cells.get(qid, []))
        scopes = pick_scopes(ig, qid, q, namespaces)
        note, f = rescore(ig, gf, qid, q, res, scopes, required, watch,
                          assigned_names(notebook, cells.get(qid, [])), names, outputs,
                          foreign=foreign_names(notebook, cells, qid), moved=moved_names(notebook, cells, qid))
        flags.extend(f)
        if note:
            notes[qid] = note
    return dict(version=OWNWORK_VERSION, notes=notes, flags=flags, outputs=len(outputs))
