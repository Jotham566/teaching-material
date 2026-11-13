"""Trusted fairness pass for the Test 1 notebook grader (lecturer's order, 10 Nov 2026).

Reuses the A2-A5 machinery (colab_shim.py, the per-cell snapshots in isolated_worker.py
and grader_fairness.rescore). Runs on the trusted side only; student code still runs
only in the Docker sandbox. Marks can only go UP: the original run is always done
first, unchanged, and each question keeps the HIGHER of its original award and the
best fairness result.

For a v4 notebook the fairness run adds, per question that is not already full:

1. Colab shim: display/IPython/drive stubs, plt.close('all') after each cell, and
   the CSV alias resolver ('/content/engineering_data (1).csv' -> the supplied file).
2. Lenient variants the question text did not fix: unit spellings in the vertical
   label ('temperature c', 'kilowatts', 'kWh per tonne', 'target_kw'), 'pct' for
   percent in the horizontal label, describe() limited to the measurement columns.
3. Own-cell check: each graded name is also checked as it was right after its own
   cell, so a later cell cannot overwrite a correct answer.
4. Name aliases (grader_fairness): a spelling variant counts in full, a different
   name sharing a word with the required one gets half of what it adds.
5. Reference inputs for dependent questions: Q2-Q6 and Q8 are re-run (their own
   answer cells only) in a fresh namespace where raw_data / cleaned_data are the
   lecturer's reference tables. One earlier error is then penalised once.
6. Q7 keeps its reference-input design; one broken key (e.g. `.median` without
   brackets) no longer zeroes the other keys, and a renamed function is tried.
"""
import ast
import copy
import re

V3 = '2026.10-test1-coding-v3'
FAIRNESS_VERSION = '2026.11-test1-fairness-1'
TASKS = ['eda', 'before', 'cleaning', 'after', 'statistics', 'grouping', 'function', 'loops']
EDA_NAMES = ['raw_data', 'first_rows', 'last_rows', 'data_shape', 'row_count', 'target_dtype',
             'numeric_summary', 'missing_counts', 'duplicate_count', 'invalid_records']
REQUIRED = {
    'q1': EDA_NAMES, 'q2': ['before_figure'], 'q3': ['cleaned_data'], 'q4': ['after_figure'],
    'q5': ['target_mean', 'target_sum', 'target_median', 'target_count', 'target_std', 'equipment_modes'],
    'q6': ['equipment_summary'], 'q7': [], 'q8': ['load_band_counts'],
}
FUNCTION = 'calculate_column_statistics'
WATCH = [n for q in REQUIRED.values() for n in q] + [FUNCTION]
# Dependent questions re-run on reference inputs, and what they read.
# Weight of the raw_data check in Q1 (2 of 20 marks), never given by a reference re-run.
RAW_DATA_MARKS = 2.0
RERUN = {'q2': 'raw', 'q3': 'raw', 'q4': 'clean', 'q5': 'clean', 'q6': 'clean', 'q8': 'clean'}
REFERENCE_RAW = (
    "import pandas as _iuea_pd\n"
    "raw_data = _iuea_pd.read_csv('/inputs/engineering_data.csv')\n")
REFERENCE_CLEAN = REFERENCE_RAW + (
    "_iuea_c = raw_data.copy().drop_duplicates('record_id')\n"
    "_iuea_c = _iuea_c[_iuea_c['target'].notna() & (_iuea_c['load_pct'] >= 0) & (_iuea_c['load_pct'] <= 100)].copy()\n"
    "_iuea_c['ambient_c'] = _iuea_c['ambient_c'].fillna(_iuea_c['ambient_c'].median())\n"
    "cleaned_data = _iuea_c\n"
    "del _iuea_c\n")

# Lenient unit spellings for the vertical label, per cohort unit. Matched as a whole
# token; underscores count as separators ('target_kw').
_LENIENT_UNITS = {
    'deg C': r'(?:°|º|deg(?:ree)?s?|celsius|centigrade|c)',
    'kW': r'(?:kw|kilo\s*-?\s*watts?)',
    'kWh/t': r'(?:kwh|kw\s*h|kilowatt\s*-?\s*hours?)\s*(?:/|per|_per_|\bper\b)?\s*(?:t|ton|tons|tonne|tonnes|mt)',
}


def lenient_unit(label, unit):
    import unicodedata
    from engineering_contracts import unit_matches
    if unit_matches(label, unit, label=True):
        return True
    if not isinstance(label, str):
        return False
    text = unicodedata.normalize('NFKC', label).lower().replace('_', ' ')
    pattern = _LENIENT_UNITS.get(unit)
    return bool(pattern) and re.search(r'(?<![a-z0-9])' + pattern + r'(?![a-z0-9])', text) is not None


def lenient_percent(label):
    if not isinstance(label, str) or not label.strip():
        return False
    text = label.lower()
    return '%' in text or 'percent' in text or 'per cent' in text or re.search(r'(?<![a-z])pct(?![a-z])', text.replace('_', ' ')) is not None


def _plot_fraction(output, table, unit):
    import math
    from isolated_grading import PlotEvidence
    from test1_coding_v3 import equal
    if not isinstance(output, PlotEvidence) or len(output.get('plot_axes', [])) != 1:
        return 0.0
    ax = output['plot_axes'][0]
    points = []
    for collection in ax['scatter']:
        points.extend(p for p in collection if all(v is not None and math.isfinite(v) for v in p))
    expected = table[['load_pct', 'target']].dropna().values.tolist()
    correct = equal(sorted(points), sorted(expected))
    checks = [correct, correct, bool(str(ax['title']).strip()), lenient_percent(ax['xlabel']),
              lenient_unit(ax['ylabel'], unit)]
    return sum(map(bool, checks)) / 5


def _describe_ok(summary, raw):
    """describe() of the measurement columns (or with include=...) holds the same numbers."""
    import pandas as pd
    from test1_coding_v3 import equal
    if not isinstance(summary, pd.DataFrame):
        return False
    expected = raw.describe()
    need = [c for c in ('load_pct', 'ambient_c', 'target') if c in expected.columns]
    if not all(c in summary.columns for c in need):
        return False
    rows = [r for r in expected.index if r in summary.index]
    if len(rows) != len(expected.index):
        return False
    cols = [c for c in expected.columns if c in summary.columns]
    try:
        got = summary.loc[expected.index, cols].astype(float)
    except (KeyError, ValueError, TypeError):
        return False
    return equal(got, expected[cols])


def lenient_assess(ns, task):
    """The ordinary v4 check, plus the lenient variants. Never lower than assess()."""
    import pandas as pd
    from engineering_contracts import DOMAINS, clean
    from test1_coding_contracts import assess
    strict = assess(ns, task)
    if ns.get('_IUEA_NOTEBOOK_VERSION') == V3:
        return strict
    raw = ns.get('_IUEA_ASSIGNED_DATA')
    course = ns.get('COHORT')
    if not isinstance(raw, pd.DataFrame) or course not in DOMAINS:
        return strict
    fraction = strict[2]
    try:
        if task in ('before', 'after'):
            def get(name):
                try:
                    return ns.get(name)
                except Exception:  # noqa: BLE001
                    return None
            table = raw if task == 'before' else pd.DataFrame(clean(raw.astype(object).where(raw.notna(), None).to_dict('records')))
            fraction = max(fraction, _plot_fraction(get(task + '_figure'), table, DOMAINS[course][1]))
        elif task == 'eda':
            from test1_coding_v3 import equal
            summary = ns.get('numeric_summary')
            if not equal(summary, raw.describe()) and _describe_ok(summary, raw):
                fraction = min(1.0, fraction + 2 / 20)
    except Exception:  # noqa: BLE001
        return strict
    if fraction > strict[2] + 1e-12:
        return fraction >= 1 - 1e-12, strict[1] + ' Lenient unit/label/describe variant accepted.', fraction
    return strict


# --------------------------------------------------------------------------- #
# Which notebook cells belong to which task
# --------------------------------------------------------------------------- #
_TASK_HEADING = re.compile(r'^\s*#{1,6}\s*Task\s*([1-8])\b', re.I | re.M)
_END_HEADING = re.compile(r'^\s*#{1,6}\s*(Need help|Save and submit|Submit)', re.I | re.M)


def _text(cell):
    s = cell.get('source', '')
    return ''.join(s) if isinstance(s, list) else str(s)


def task_cells(notebook):
    """{task: [cell index]} using the iuea-answer-* tags, else the 'Task N' headings.
    Student-added code cells after an answer cell belong to that task until the next task."""
    out = {t: [] for t in TASKS}
    current = None
    for index, cell in enumerate(notebook.get('cells', [])):
        text = _text(cell)
        tags = cell.get('metadata', {}).get('tags', []) or []
        if cell.get('cell_type') == 'markdown':
            m = _TASK_HEADING.search(text)
            if m:
                current = TASKS[int(m.group(1)) - 1]
            elif _END_HEADING.search(text):
                current = None
            continue
        if cell.get('cell_type') != 'code':
            continue
        answer = [t[len('iuea-answer-'):] for t in tags if t.startswith('iuea-answer-')]
        if answer and answer[0] in out:
            current = answer[0]
            out[current].append(index)
            continue
        if any(t in tags for t in ('iuea-support', 'iuea-timer', 'iuea-submission', 'autograde-skip')) or \
                text.lstrip().startswith('#@title'):
            continue
        if current:
            out[current].append(index)
    return out


# --------------------------------------------------------------------------- #
# The fairness run
# --------------------------------------------------------------------------- #
def _tolerant_decode(value):
    """decode(), but a callable value (e.g. `.median` without brackets) becomes None
    instead of making the whole answer undecodable."""
    from isolated_grading import decode
    def strip(v):
        if isinstance(v, dict):
            if v.get('type') == 'callable':
                return None
            return {k: strip(x) for k, x in v.items()}
        if isinstance(v, list):
            return [strip(x) for x in v]
        return v
    return decode(strip(value))


def _q7_fraction(worker, per_call, scope, course, name, keyfix=False):
    import pandas as pd
    from engineering_contracts import clean, dataset
    from test1_coding_v3 import equal
    checks = []
    for seed in (71, 113):
        rows = clean(dataset(course, seed, 36, dirty=True))
        table = pd.DataFrame(rows)
        for column in ('target', 'load_pct'):
            try:
                result = _tolerant_decode(worker.request(op='call_dataframe', name=name, rows=rows, column=column,
                                                         timeout=per_call, **scope))
            except Exception:  # noqa: BLE001
                result = None
            if keyfix:
                # Review (13 Nov 2026, R7): keys compared ignoring case and spaces.
                import review_fairness
                result = review_fairness.norm_keys(result, ('mean', 'sum', 'median')) or result
            for key in ('mean', 'sum', 'median'):
                try:
                    checks.append(isinstance(result, dict) and equal(result.get(key), getattr(table[column], key)()))
                except Exception:  # noqa: BLE001
                    checks.append(False)
    return sum(map(bool, checks)) / len(checks)


class _RerunNamespace:
    """Reads graded names from one reference-input re-run inside the worker."""

    def __init__(self, base, key):
        from isolated_grading import Namespace
        self.inner = Namespace(base.worker, base.per_call)
        self.inner._scope = lambda: {'rerun': key}
        self.inner.cache.update({k: v for k, v in base.cache.items()
                                 if k in ('COHORT', '_IUEA_ASSIGNED_DATA', '_IUEA_NOTEBOOK_VERSION')})
        self.inner.notebook_sources = base.notebook_sources

    def __getattr__(self, attr):
        return getattr(self.inner, attr)

    def get(self, name, default=None):
        return self.inner.get(name, default)


def _new_ns(worker, per_cell, cohort, assigned, version, sources, state=None):
    from isolated_grading import Namespace
    ns = Namespace(worker, per_cell, state=state)
    ns.cache['COHORT'] = cohort
    ns.cache['_IUEA_ASSIGNED_DATA'] = assigned
    ns.cache['_IUEA_NOTEBOOK_VERSION'] = version
    ns.notebook_sources = sources
    return ns


def evaluate(evaluate_plain, work, spec_path, hidden_path, cohort, per_cell, total_timeout):
    """Original result first (unchanged), then the fairness run; per question the higher."""
    import json
    from pathlib import Path
    plain = evaluate_plain(work, spec_path, hidden_path, 'TEST1', cohort, per_cell, total_timeout, fairness=False)
    notebook = json.loads((Path(work) / 'submission.ipynb').read_text())
    version = notebook.get('metadata', {}).get('iuea_exam_version', '')
    if version == V3:
        return plain
    try:
        fair = fairness_run(work, spec_path, hidden_path, cohort or plain.get('cohort', ''), per_cell,
                            total_timeout, notebook, version)
    except Exception as exc:  # noqa: BLE001
        plain['fairness'] = dict(version=FAIRNESS_VERSION, error='%s: %s' % (type(exc).__name__, str(exc)[:200]))
        return plain
    out = combine(plain, fair)
    import review_fairness
    if review_fairness.enabled():
        # Review (13 Nov 2026): when a cell cannot run as written (one broken line, Colab's
        # Python 3.12) or Q7 lost keys to one failing calculation, a further fairness run
        # with the repaired cells; each question keeps the higher award.
        try:
            q7 = out['questions'].get('q7', {})
            repair, kinds = review_fairness.repairs(notebook, 'TEST1',
                                                    q7=q7.get('awarded', 0) < q7.get('marks', 0) - 1e-9)
            errors = list(plain.get('cell_errors') or []) + list(fair.get('cell_errors') or [])
            if any(q['awarded'] < q['marks'] - 1e-9 for q in out['questions'].values()) and \
                    review_fairness.needs_run(repair, kinds, errors):
                second = fairness_run(work, spec_path, hidden_path, cohort or plain.get('cohort', ''), per_cell,
                                      total_timeout, notebook, version, repair=repair)
                review_fairness.merge(out, second, kinds, repair=repair)
            else:
                out['fairness']['review_repair'] = dict(version=review_fairness.REVIEW_VERSION, kinds=[], notes={})
        except Exception as exc:  # noqa: BLE001
            out['fairness']['review_repair'] = dict(version=review_fairness.REVIEW_VERSION, notes={},
                                                    error='%s: %s' % (type(exc).__name__, str(exc)[:200]))
    return out


def combine(plain, fair):
    """Per question: the higher of the original award and the fairness award."""
    out = copy.deepcopy(plain)
    changes = {}
    for qid, q in out['questions'].items():
        f = fair['questions'].get(qid)
        if not f or f['awarded'] <= q['awarded'] + 1e-9:
            continue
        changes[qid] = dict(original=q['awarded'], awarded=f['awarded'], fix=f.get('fix') or 'fairness run',
                            detail=f.get('detail', ''))
        q.update(awarded=f['awarded'], ok=f['ok'], msg='Credited by %s: %s. %s' % (
            changes[qid]['fix'], changes[qid]['detail'], q.get('msg') or ''))
    out['fairness'] = dict(version=FAIRNESS_VERSION, changes=changes,
                           original_questions={k: v['awarded'] for k, v in plain['questions'].items()},
                           fair_cell_errors=fair.get('cell_errors', []), worker_notes=fair.get('worker_notes', []),
                           error=fair.get('error', ''))
    if 'ownwork' in fair:
        out['fairness']['ownwork'] = fair['ownwork']
        out['fairness']['before_ownwork'] = fair.get('before_ownwork', {})
    if 'review' in fair:
        out['fairness']['review'] = fair['review']
    return out


def fairness_run(work, spec_path, hidden_path, cohort, per_cell, total_timeout, notebook, version, repair=None):
    import iuea_grader as ig
    import grader_fairness as gf
    import pandas as pd
    from pathlib import Path
    from isolated_grading import Worker
    import ownwork_fairness
    spec = ig.load_spec('TEST1', spec_path, include_hidden=True, hidden_path=hidden_path)
    worker = Worker(work, total_timeout + 180)
    own = ownwork_fairness.enabled()
    try:
        meta = worker.request(op='init', timeout=total_timeout, cell_timeout=per_cell, colab_shims=True, watch=WATCH,
                              **({'ownwork': True} if own else {}), **({'repair': repair} if repair else {}))
        use_cohort = cohort or str(meta.get('cohort', ''))
        questions = ig.resolve_questions(spec, use_cohort)
        tasks = dict(zip([q for q, _ in questions], TASKS))
        lenient = [(qid, dict(q, check=(lambda ns, t=tasks[qid]: lenient_assess(ns, t)))) for qid, q in questions]
        strict = dict(questions)
        assigned = pd.read_csv(Path(work) / 'engineering_data.csv')
        sources = [''.join(c.get('source', '')) for c in notebook['cells']
                   if c.get('cell_type') == 'code' and 'autograde-skip' not in c.get('metadata', {}).get('tags', [])]
        final = _new_ns(worker, per_cell, use_cohort, assigned, version, sources)
        results = {}
        for qid, q in lenient:
            s = ig.run_check(qid, strict[qid], final)
            r = ig.run_check(qid, q, final)
            best = r if r.awarded > s.awarded + 1e-9 else s
            results[qid] = dict(ok=best.ok, awarded=best.awarded, marks=best.marks, msg=best.message,
                                strict=s.awarded, fix='Colab shim run' if best is s else 'lenient unit/label/describe variant',
                                detail='')
        snaps = meta.get('snapshots') or []
        namespaces = [('the whole notebook', final)] + [
            ('cell %s' % cell, _new_ns(worker, per_cell, use_cohort, assigned, version, sources, state=i))
            for i, cell in enumerate(snaps)]
        names = worker.request(op='names')
        # Own-cell snapshots and name aliases: the A2-A5 rescore with the Test 1 names.
        gf.REQUIRED.setdefault('TEST1', REQUIRED)
        before = {k: v['awarded'] for k, v in results.items()}
        notes = gf.rescore(ig, 'TEST1', use_cohort, lenient, results, namespaces, names if isinstance(names, list) else [])
        for qid, n in notes.items():
            if results[qid]['awarded'] > before[qid] + 1e-9:
                results[qid].update(fix=n['fix'], detail=n['detail'])
        # Reference inputs for the dependent questions.
        cells = task_cells(notebook)
        reference_ok = None
        reran = {}
        for qid, kind in RERUN.items():
            res = results.get(qid)
            if not res or res['awarded'] >= res['marks'] - 1e-9 or not cells.get(tasks[qid]):
                continue
            if reference_ok is None:
                # Safety: the preset must reproduce the reference tables exactly.
                worker.request(op='rerun', key='reference', preset=[REFERENCE_CLEAN], cells=[], cell_timeout=per_cell)
                ref_ns = _RerunNamespace(final, 'reference')
                reference_ok = (ig.run_check('q3', strict['q3'], ref_ns).ok and
                                isinstance(ref_ns.get('raw_data'), pd.DataFrame))
            if not reference_ok:
                break
            ran = worker.request(op='rerun', key=qid, cells=cells[tasks[qid]], cell_timeout=per_cell,
                                 preset=[REFERENCE_RAW if kind == 'raw' else REFERENCE_CLEAN])
            reran[qid] = kind
            r = ig.run_check(qid, dict(lenient)[qid], _RerunNamespace(final, qid))
            if r.awarded > res['awarded'] + 1e-9:
                res.update(ok=r.ok, awarded=r.awarded, msg=r.message,
                           fix='reference inputs (error carried forward)',
                           detail='own Task %d cells re-run on the reference %s (%d cell errors)' % (
                               TASKS.index(tasks[qid]) + 1, 'raw_data' if kind == 'raw' else 'cleaned_data',
                               len(ran.get('errors', []))))
        # Q1: when raw_data itself is wrong (e.g. `pd.read_csv` without brackets) the other
        # inspection lines are re-run on the reference raw_data; the reading marks stay lost.
        res = results.get('q1')
        from test1_coding_v3 import equal
        if res and res['awarded'] < res['marks'] - 1e-9 and cells.get('eda') and reference_ok is not False \
                and not equal(final.get('raw_data'), assigned):
            ran = worker.request(op='rerun', key='q1', cells=cells['eda'], cell_timeout=per_cell,
                                 preset=[REFERENCE_RAW], drop_assign=['raw_data'])
            reran['q1'] = 'raw'
            r = ig.run_check('q1', dict(lenient)['q1'], _RerunNamespace(final, 'q1'))
            credit = max(0.0, r.awarded - RAW_DATA_MARKS)
            if credit > res['awarded'] + 1e-9:
                res.update(ok=False, awarded=credit, msg=r.message,
                           fix='reference inputs (error carried forward)',
                           detail='Task 1 lines re-run on the reference raw_data; the %g marks for reading raw_data stay lost (%d cell errors)' % (
                               RAW_DATA_MARKS, len(ran.get('errors', []))))
        # Q7: per-key credit and a renamed function (reference-input design kept).
        res = results.get('q7')
        if res and res['awarded'] < res['marks'] - 1e-9:
            present = names if isinstance(names, list) else []
            candidates = [(FUNCTION, 'same')] + [(c, gf.alias_tier(FUNCTION, c)) for c in present if c != FUNCTION]
            candidates = [(c, t) for c, t in candidates if t][:8]
            scopes = [('the whole notebook', {})] + [('cell %s' % cell, {'state': i}) for i, cell in enumerate(snaps)]
            base = res['awarded']
            for name, tier in candidates:
                for label, scope in scopes:
                    frac = _q7_fraction(worker, per_cell, scope, use_cohort, name)
                    credit = frac * res['marks']
                    if tier == 'renamed':
                        credit = base + 0.5 * max(0.0, credit - base)
                    if credit > res['awarded'] + 1e-9:
                        res.update(awarded=round(credit, 4), ok=credit >= res['marks'] - 1e-9,
                                   fix='Q7 per-key check' if tier in ('same', 'spelling') else 'name alias (half marks, different name)',
                                   detail='%s called with the reference tables, each key checked on its own (%s)' % (name, label))
        out = dict(questions=results, cell_errors=meta.get('cell_errors', []), worker_notes=meta.get('notes') or [])
        if own:
            before = copy.deepcopy(results)
            out['before_ownwork'] = {k: v['awarded'] for k, v in before.items()}
            try:
                out['ownwork'] = ownwork_pass(ig, gf, worker, per_cell, use_cohort, lenient, results, namespaces,
                                              final, notebook, cells, tasks, reran,
                                              names if isinstance(names, list) else [], snaps)
            except Exception as exc:  # noqa: BLE001
                out['questions'] = before
                out['ownwork'] = dict(version=ownwork_fairness.OWNWORK_VERSION, notes={}, flags=[],
                                      error='%s: %s' % (type(exc).__name__, str(exc)[:200]))
        import review_fairness
        if review_fairness.enabled():
            # Review (13 Nov 2026, R7-R9): dictionary keys, grouped columns, doubled points.
            kept = copy.deepcopy(out['questions'])
            try:
                scopes = dict(ns=list(namespaces),
                              rerun={q: ('the reference-input re-run of %s' % q, _RerunNamespace(final, q)) for q in reran},
                              q7=[('the whole notebook', {})] + [('cell %s' % cell, {'state': i}) for i, cell in enumerate(snaps)])
                out['review'] = dict(version=review_fairness.REVIEW_VERSION,
                                     notes=review_fairness.view_pass_t1(ig, worker, per_cell, use_cohort, lenient,
                                                                        out['questions'], scopes))
            except Exception as exc:  # noqa: BLE001
                out['questions'] = kept
                out['review'] = dict(version=review_fairness.REVIEW_VERSION, notes={},
                                     error='%s: %s' % (type(exc).__name__, str(exc)[:200]))
        return out
    finally:
        worker.close()


FIGURES = {'q2': 'before_figure', 'q4': 'after_figure'}


def ownwork_pass(ig, gf, worker, per_cell, cohort, lenient, results, namespaces, final, notebook, cells, tasks,
                 reran, names, snaps):
    """Own-work credit (13 Nov 2026, ownwork_fairness): different names in full when
    unambiguous, printed/displayed answers, charts on the student's own figure. Read in
    the whole notebook, the best own-cell snapshot and the question's reference-input
    re-run. Only raises a question."""
    import ownwork_fairness as ow
    outputs = worker.request(op='outputs')
    outputs = outputs if isinstance(outputs, list) else []
    notes, flags = {}, []
    for qid, question in lenient:
        res = results[qid]
        if res['awarded'] >= res['marks'] - 1e-9:
            continue
        own_cells = cells.get(tasks[qid], [])
        local = ow.assigned_names(notebook, own_cells)
        foreign = ow.foreign_names(notebook, cells, tasks[qid])
        moved = ow.moved_names(notebook, cells, tasks[qid])
        if qid == 'q7':
            note, f = _ownwork_q7(gf, worker, per_cell, cohort, res, names, local, snaps, foreign | moved)
        else:
            q = ow.with_cells(question, own_cells)
            extra = [('the reference-input re-run of Task %d' % (TASKS.index(tasks[qid]) + 1),
                      _RerunNamespace(final, qid), qid)] if qid in reran and qid != 'q1' else []
            scopes = ow.pick_scopes(ig, qid, q, namespaces, extra)
            fig = (FIGURES[qid],) if qid in FIGURES else ()
            note, f = ow.rescore(ig, gf, qid, q, res, scopes, REQUIRED[qid], WATCH, local, names, outputs, fig, foreign, moved)
            if qid == 'q1' and 'q1' in reran:
                # raw_data itself was wrong: the other Task 1 lines on the reference raw_data,
                # with the printed/renamed evidence; the reading marks stay lost.
                trial = dict(res)
                n2, f2 = ow.rescore(ig, gf, qid, q, trial, [('the reference-input re-run of Task 1',
                                                             _RerunNamespace(final, 'q1'), 'q1')],
                                    REQUIRED[qid], WATCH, local, names, outputs, fig, foreign, moved)
                f.extend(f2)
                if n2:
                    credit = max(0.0, trial['awarded'] - RAW_DATA_MARKS)
                    if credit > res['awarded'] + 1e-9:
                        n2.update(original=res['awarded'], awarded=credit,
                                  detail=n2['detail'] + '; the %g marks for reading raw_data stay lost' % RAW_DATA_MARKS)
                        res.update(awarded=credit, ok=False, fix=n2['fix'], detail=n2['detail'])
                        note = n2
        flags.extend(f)
        if note:
            notes[qid] = note
    return dict(version=ow.OWNWORK_VERSION, notes=notes, flags=flags, outputs=len(outputs))


def _ownwork_q7(gf, worker, per_cell, cohort, res, names, local, snaps, foreign=()):
    """Q7 under another function name: full credit when it is the only function the
    student defined in Task 7 (or the only one sharing a word with the required name)."""
    import ownwork_fairness as ow
    from isolated_grading import Namespace
    final = Namespace(worker, per_cell)
    moved_or_foreign = foreign = set(foreign)
    pool = [c for c in names if c != FUNCTION and not c.startswith('_') and c not in gf.NOT_ALIASES
            and c not in foreign and gf.alias_tier(FUNCTION, c)]
    pool += [c for c in local if c != FUNCTION and c not in pool and not c.startswith('_') and c not in moved_or_foreign]
    funcs = [c for c in pool if ow.family(ow._safe_get(final, c)) == 'callable']
    shared = [c for c in funcs if gf.alias_tier(FUNCTION, c)]
    clear = funcs if len(funcs) == 1 else shared if len(shared) == 1 else []
    flags = []
    if not clear and len(funcs) > 1:
        flags.append('AMBIGUOUS_NAME q7: several functions (%s) and none is the only clear candidate' % ', '.join(funcs[:6]))
        return None, flags
    if not clear:
        return None, flags
    name = clear[0]
    scopes = [('the whole notebook', {})] + [('cell %s' % cell, {'state': i}) for i, cell in enumerate(snaps)]
    best = None
    for label, scope in scopes:
        credit = _q7_fraction(worker, per_cell, scope, cohort, name) * res['marks']
        if credit > res['awarded'] + 1e-9 and (best is None or credit > best[0] + 1e-9):
            best = (credit, label)
    if not best:
        return None, flags
    note = dict(original=res['awarded'], awarded=round(best[0], 4), fix=ow.FIX_NAME,
                detail='%s called with the reference tables, each key checked on its own (%s)' % (name, best[1]))
    res.update(awarded=note['awarded'], ok=note['awarded'] >= res['marks'] - 1e-9, fix=note['fix'], detail=note['detail'])
    return note, flags
