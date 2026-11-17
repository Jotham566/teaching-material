"""Trusted fairness re-checks for the A2-A5 notebook checker (lecturer's order, 10 Nov 2026).

Runs in the trusted evaluator only (never inside the sandbox). The ordinary check
on the final namespace always runs first and is never lowered; these passes can
only ADD credit to a question that did not get full marks:

1. Own-cell check (fix 4). The worker snapshots the graded names right after the
   cell that set them. Each snapshot is checked like the final namespace and the
   best result counts, so a later cell that rebinds a name does not remove credit.
2. Output-name aliases (fix 3). When a required name is missing, a student variable
   with a near name is tried in its place:
     * a spelling variant (same letters ignoring case/underscores, or at most two
       typing slips, e.g. n_meter, cosr_per_kwh) is ACCEPTED: full credit;
     * a different name sharing a word with the required one (weight for weight_n,
       worst for worst_reading, mean_width for mean_reading) gets HALF of the
       credit that the rename would add.
   The same applies to a required DataFrame column (A5 cost_per_kwh).

Also: `cannot_judge_reason` decides when a zero is really a wrong upload (fix 5).
"""
import ast
import re

# Assessments that use the Colab shims, per-cell snapshots and aliases.
FAIRNESS_ASSESSMENTS = {'W02', 'W03', 'W04', 'W05'}

ALIAS_HALF = 0.5

# Required output names per question; q3 of W03 depends on the cohort.
REQUIRED = {
    'W02': {'q1': ['STUDENT_ID'], 'q2': ['proof_sum'], 'q3': ['readings'], 'q4': ['rows']},
    'W03': {'q1': ['weight_n'], 'q2': ['percent_error'],
            'q3': {'CML3111': ['power_loss'], 'CML3112': ['slab_mass'], 'CML3113': ['mud_pressure']},
            'q4': ['efficiency'], 'q5': ['worst_reading', 'worst_error']},
    'W04': {'q1': ['valid_count'], 'q2': ['mean_reading'], 'q3': ['above_limit'], 'q4': ['group_means']},
    'W05': {'q1': ['df'], 'q2': ['n_meters'], 'q3': ['df'], 'q4': ['high_use'],
            'q5': ['mean_cost_per_kwh'], 'q6': ['peak_building']},
}
# Required DataFrame columns: (frame names, column, columns of the supplied file).
REQUIRED_COLUMNS = {
    'W05': {'q3': (['df'], 'cost_per_kwh'), 'q4': (['high_use'], 'cost_per_kwh')},
}
BASE_COLUMNS = {'W05': ['meter_id', 'building', 'block', 'month', 'kwh', 'cost_ugx']}
# Never used as an alias for something else (identity, cohort, data).
NOT_ALIASES = {'STUDENT_ID', 'COHORT', 'READINGS', 'NOMINAL', 'G', 'pd', 'np', 'plt', 'csv'}
# Generic loop/temporary names are never treated as a renamed answer.
TOO_GENERIC = {'i', 'j', 'k', 'x', 'y', 'n', 'r', 'f', 'v', 'row', 'rows_', 'value', 'val', 'data', 'result', 'temp', 'tmp'}


def required_names(assignment, qid, cohort):
    spec = REQUIRED.get(assignment, {}).get(qid, [])
    if isinstance(spec, dict):
        spec = spec.get(cohort, [])
    return list(spec)


def watch_names(assignment, cohort):
    names = []
    for qid in REQUIRED.get(assignment, {}):
        for n in required_names(assignment, qid, cohort):
            if n not in names:
                names.append(n)
    return names


def _levenshtein(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _squash(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())


def _tokens(name):
    return {t for t in re.split(r'[^a-z0-9]+', re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()) if len(t) >= 3}


def alias_tier(required, candidate):
    """'spelling' (accept), 'renamed' (half credit) or None."""
    if candidate == required or candidate in NOT_ALIASES or candidate.lower() in TOO_GENERIC:
        return None
    a, b = _squash(required), _squash(candidate)
    if not b:
        return None
    # Same letters ignoring case/underscores, or one typing slip (n_meter, cosr_per_kwh).
    if a == b or (len(a) >= 5 and _levenshtein(required.lower(), candidate.lower()) <= 1):
        return 'spelling'
    if _tokens(required) & _tokens(candidate):
        return 'renamed'
    return None


class AliasView:
    """A namespace view that reads `required` from another name, and optionally renames
    a DataFrame column (decoded in the trusted evaluator; the copy is renamed)."""

    def __init__(self, base, names=None, column=None):
        self.base, self.names, self.column = base, dict(names or {}), column
        self.cache = {}

    def __getattr__(self, attr):
        return getattr(self.base, attr)

    def get(self, name, default=None):
        value = self.base.get(self.names.get(name, name), default)
        if self.column and name in self.column[0] and hasattr(value, 'rename') and hasattr(value, 'columns'):
            wrong, right = self.column[1], self.column[2]
            if wrong in list(value.columns) and right not in list(value.columns):
                value = value.rename(columns={wrong: right})
        return value


def _awarded(ig, qid, question, ns):
    r = ig.run_check(qid, question, ns)
    return r


def rescore(ig, assignment, cohort, questions, results, namespaces, student_names):
    """Re-check questions without full marks. `namespaces` = [(label, ns)] with the
    final namespace first, then one per snapshot. Returns {qid: note} for changes and
    updates `results` in place (only ever upwards)."""
    notes = {}
    for qid, question in questions:
        res = results[qid]
        if res['awarded'] >= res['marks'] - 1e-9:
            continue
        best = dict(awarded=res['awarded'], fix=None, detail='')
        # 1. own-cell snapshots
        for label, ns in namespaces[1:]:
            r = _awarded(ig, qid, question, ns)
            if r.awarded > best['awarded'] + 1e-9:
                best = dict(awarded=r.awarded, fix='own-cell check', detail='value as it was right after ' + label,
                            ok=r.ok, msg=r.message)
        # 2. aliases for names that never existed
        present = set(student_names)
        for req in required_names(assignment, qid, cohort):
            if req in present:
                continue
            cands = [(c, alias_tier(req, c)) for c in sorted(present)]
            cands = [(c, t) for c, t in cands if t and c not in watch_names(assignment, cohort)]
            for cand, tier in sorted(cands, key=lambda ct: ct[1] != 'spelling')[:6]:
                for label, ns in namespaces:
                    r = _awarded(ig, qid, question, AliasView(ns, {req: cand}))
                    gain = r.awarded - res['awarded']
                    credit = res['awarded'] + (gain if tier == 'spelling' else ALIAS_HALF * gain)
                    if credit > best['awarded'] + 1e-9:
                        best = dict(awarded=round(credit, 4), fix='name alias (%s)' % ('accepted spelling variant' if tier == 'spelling' else 'half marks, different name'),
                                    detail='%s used for %s (%s)' % (cand, req, label), ok=tier == 'spelling' and r.ok, msg=r.message)
        # 3. column alias
        col = REQUIRED_COLUMNS.get(assignment, {}).get(qid)
        if col:
            frames, right = col
            for label, ns in namespaces:
                frame = ns.get(frames[0])
                cols = [str(c) for c in getattr(frame, 'columns', [])]
                if not cols or right in cols:
                    continue
                for c in cols:
                    if c in BASE_COLUMNS.get(assignment, []):
                        continue
                    tier = alias_tier(right, c)
                    if not tier:
                        continue
                    view = AliasView(ns, column=(frames + ['df', 'high_use'], c, right))
                    r = _awarded(ig, qid, question, view)
                    gain = r.awarded - res['awarded']
                    credit = res['awarded'] + (gain if tier == 'spelling' else ALIAS_HALF * gain)
                    if credit > best['awarded'] + 1e-9:
                        best = dict(awarded=round(credit, 4), fix='column alias (%s)' % ('accepted spelling variant' if tier == 'spelling' else 'half marks, different name'),
                                    detail='column %s used for %s (%s)' % (c, right, label), ok=tier == 'spelling' and r.ok, msg=r.message)
        if best['fix']:
            notes[qid] = dict(original=res['awarded'], awarded=best['awarded'], fix=best['fix'], detail=best['detail'])
            res['awarded'] = min(res['marks'], best['awarded'])
            res['ok'] = bool(best.get('ok')) and res['awarded'] >= res['marks'] - 1e-9
            res['msg'] = ('Credited by %s: %s. ' % (best['fix'], best['detail'])) + (res.get('msg') or '')
    return notes


def mentioned_names(sources):
    found = set()
    for s in sources:
        try:
            tree = ast.parse(s)
        except SyntaxError:
            found |= set(re.findall(r'[A-Za-z_]\w*', s))
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Name):
                found.add(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.add(n.name)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and re.fullmatch(r'\w+', n.value):
                found.add(n.value)
    return found


def cannot_judge_reason(assignment, cohort, sources, total):
    """A zero from a notebook that contains none of the assignment's required names is
    a different notebook (wrong upload): 'cannot judge', not 0."""
    if assignment not in FAIRNESS_ASSESSMENTS or total > 0:
        return ''
    # Raw text (comments included): code left inside a comment still shows the right notebook.
    names = mentioned_names(sources) | {w for s in sources for w in re.findall(r'[A-Za-z_]\w*', s)}
    wanted = set(watch_names(assignment, cohort)) - {'STUDENT_ID', 'df'}
    if assignment == 'W05':
        wanted |= {'cost_per_kwh'}
    if not (names & wanted):
        return ('The uploaded notebook contains none of the required names (%s), so it is a different '
                'notebook; cannot judge (no mark) - ask for the right file.' % ', '.join(sorted(wanted)))
    return ''
