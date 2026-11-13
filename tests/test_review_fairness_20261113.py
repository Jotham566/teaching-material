"""Review of every coded assessment (lecturer's instruction, 13 Nov 2026).

"Ensure no unfair penalizing for such issues like creating new cells for code instead
of answering within our created code cells. Review all." Behind IUEA_REVIEW_FAIRNESS=1:
R4 a cell with one broken line still runs its correct lines, R5 Colab's Python 3.12
syntax runs, R6 Q7 keys are checked one by one, R7 dictionary keys ignore case and
spaces, R8 two-level grouped column names are flattened, R9 identical scatter layers
count once. Marks never go down, wrong is still wrong, and switched off nothing changes.
Fixtures are synthetic; notebook code only runs in the Docker sandbox.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'IUEA_Teaching_Plan/grader'
sys.path.insert(0, str(G))
import review_fairness as rf  # noqa: E402
from test1_coding_reference import NOTEBOOK_ANSWERS, complete_notebook  # noqa: E402

BANK = G.parent / 'assessment_banks/TEST1/CML3111/A'
W04_DATA = G.parent / 'practicals/W04/CML3111'
ON = {'IUEA_OWNWORK_FAIRNESS': '1', 'IUEA_REVIEW_FAIRNESS': '1'}
OWN_ONLY = {'IUEA_OWNWORK_FAIRNESS': '1', 'IUEA_REVIEW_FAIRNESS': '0'}
OFF = {'IUEA_OWNWORK_FAIRNESS': '0', 'IUEA_REVIEW_FAIRNESS': '0'}


def _docker_ready():
    import shutil
    import subprocess
    if not shutil.which('docker'):
        return False
    try:
        return subprocess.run(['docker', 'image', 'inspect', 'iuea-notebooks:2026.09'],
                              capture_output=True, timeout=20).returncode == 0
    except Exception:  # noqa: BLE001
        return False


class HostHelpers(unittest.TestCase):
    """No Docker."""

    def test_switch_is_off_by_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('IUEA_REVIEW_FAIRNESS', None)
            self.assertFalse(rf.enabled())
        with patch.dict(os.environ, {'IUEA_REVIEW_FAIRNESS': '1'}):
            self.assertTrue(rf.enabled())

    def test_salvage_drops_only_the_broken_statements(self):
        src = 'a = 1\nraw = pd.read_csv(file_ path)\nb = 2\nc =\n'
        out = rf.salvage(src)
        self.assertIn('a = 1', out)
        self.assertIn('b = 2', out)
        self.assertNotIn('read_csv', out)
        self.assertNotIn('c =', out)

    def test_salvage_keeps_a_correct_function_before_a_broken_call(self):
        src = 'def f(t, c):\n    return {"mean": t[c].mean()}\nresult =\nf(1, 2)\n'
        out = rf.salvage(src)
        self.assertIn('def f(t, c):', out)
        self.assertIn('f(1, 2)', out)

    def test_salvage_leaves_valid_or_dedentable_cells_alone(self):
        self.assertIsNone(rf.salvage('x = 1\n'))
        self.assertIsNone(rf.salvage('    x = 1\n    y = 2\n'))

    def test_salvage_limit(self):
        self.assertIsNone(rf.salvage('a =\nb =\nc =\nd =\ne =\n'))

    def test_py311_equivalent_rewrites_nested_quotes(self):
        out = rf.py311_equivalent('d = {"k": 1}\nprint(f"{d["k"]}")\n')
        self.assertIn("f\"{d['k']}\"", out)
        self.assertIsNone(rf.py311_equivalent('x = 1\n'))

    def test_keys_each_wraps_each_value(self):
        out = rf.keys_each('def calculate_column_statistics(table, column_name):\n'
                           '    return {"mean": table[column_name].mean(), "median": table[column_name].meadian()}\n')
        ns = {}
        exec(out, ns)  # trusted test fixture, not student code
        import pandas as pd
        r = ns['calculate_column_statistics'](pd.DataFrame({'x': [1.0, 3.0]}), 'x')
        self.assertEqual(r, {'mean': 2.0, 'median': None})
        self.assertIsNone(rf.keys_each('def other():\n    return {"a": 1}\n'))

    def test_norm_keys(self):
        req = ('low', 'medium', 'high')
        self.assertEqual(rf.norm_keys({'Low': 1, 'Medium': 2, 'High ': 3}, req), {'low': 1, 'medium': 2, 'high': 3})
        self.assertIsNone(rf.norm_keys({'low': 1, 'medium': 2, 'high': 3}, req))      # already right
        self.assertIsNone(rf.norm_keys({'Low': 1, 'low': 2, 'high': 3}, req))         # collision
        self.assertIsNone(rf.norm_keys({'small': 1, 'medium': 2, 'high': 3}, req))    # different key

    def test_flatten_columns(self):
        import pandas as pd
        f = pd.DataFrame([[1.0, 2]], columns=pd.MultiIndex.from_tuples([('target', 'mean'), ('target', 'count')]))
        self.assertEqual(list(rf.flatten_columns(f).columns), ['mean', 'count'])
        garbled = pd.DataFrame([[1.0, 2]], columns=[('target', 'target'), ('mean', 'count')])  # as decoded
        self.assertEqual(list(rf.flatten_columns(garbled).columns), ['mean', 'count'])
        self.assertIsNone(rf.flatten_columns(pd.DataFrame({'mean': [1.0], 'count': [2]})))

    def test_dedupe_scatter(self):
        from isolated_grading import PlotEvidence
        ax = dict(title='t', xlabel='%', ylabel='kW', lines=[], bars=[], xticklabels=[],
                  scatter=[[[1.0, 2.0], [3.0, 4.0]], [[3.0, 4.0], [1.0, 2.0]]])
        out = rf.dedupe_scatter(PlotEvidence(plot_axes=[ax]))
        self.assertEqual(len(out['plot_axes'][0]['scatter']), 1)
        ax2 = dict(ax, scatter=[[[1.0, 2.0]], [[5.0, 6.0]]])
        self.assertIsNone(rf.dedupe_scatter(PlotEvidence(plot_axes=[ax2])))

    def test_merge_only_raises(self):
        first = {'questions': {'q1': dict(awarded=2.0, marks=5.0), 'q2': dict(awarded=5.0, marks=5.0)}}
        second = {'questions': {'q1': dict(awarded=1.0, marks=5.0), 'q2': dict(awarded=0.0, marks=5.0)}}
        self.assertEqual(rf.merge(first, second, {'salvage'}), {})
        self.assertEqual(first['questions']['q1']['awarded'], 2.0)
        second['questions']['q1']['awarded'] = 4.0
        notes = rf.merge(first, second, {'salvage'})
        self.assertEqual(notes['q1']['awarded'], 4.0)
        self.assertEqual(first['questions']['q2']['awarded'], 5.0)

    def test_needs_run(self):
        self.assertFalse(rf.needs_run({}, set(), []))
        self.assertFalse(rf.needs_run({'1': {}}, {'py312'}, [{'etype': 'NameError'}]))
        self.assertTrue(rf.needs_run({'1': {}}, {'py312'}, [{'etype': 'SyntaxError'}]))
        self.assertTrue(rf.needs_run({'1': {}}, {'keys_each'}, []))


@unittest.skipUnless(_docker_ready(), 'Docker sandbox image not available')
class Test1Sandbox(unittest.TestCase):
    """Real Test 1 runs in the iuea-notebooks sandbox."""

    def notebook(self):
        return complete_notebook(json.loads((BANK / 'TEST1_student.ipynb').read_text()))

    def replace(self, nb, task, source):
        for c in nb['cells']:
            if 'iuea-answer-' + task in c.get('metadata', {}).get('tags', []):
                c['source'] = source

    def grade(self, nb, env=ON):
        from batch_grade import grade_one
        with patch.dict(os.environ, env), tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'test.ipynb'
            path.write_text(json.dumps(nb))
            return grade_one(str(path), str(G / 'specs/spec_TEST1.py'), str(G / 'specs/hidden/spec_TEST1_hidden.py'),
                             'TEST1', 'CML3111', str(BANK), 20, 180, None)

    def awards(self, r):
        return {q: v['awarded'] for q, v in r['questions'].items()}

    def test_complete_notebook_unchanged(self):
        r = self.grade(self.notebook())
        self.assertEqual(sum(self.awards(r).values()), 100, r)
        self.assertEqual(r['fairness']['review']['notes'], {})

    def test_R4_broken_line_and_R6_keys_and_R7_names(self):
        nb = self.notebook()
        # Q7: a correct function followed by a broken line (the whole cell fails to compile).
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'] + 'target_stats =\n')
        # Q8: correct counts under capitalised keys.
        self.replace(nb, 'loops', NOTEBOOK_ANSWERS['loops'].replace("'low'", "'Low'").replace("'medium'", "'Medium'")
                     .replace("'high'", "'High'"))
        # Q6: two-level column names from agg({'target': [...]}).
        self.replace(nb, 'grouping', "equipment_summary = cleaned_data.groupby('equipment_id').agg({'target': ['mean', 'count']})\n")
        off = self.awards(self.grade(nb, OWN_ONLY))
        self.assertEqual((off['q6'], off['q7'], off['q8']), (0, 0, 4))
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual((a['q6'], a['q7'], a['q8']), (10, 5, 10), r['fairness'])
        self.assertEqual(r['fairness']['review_repair']['notes']['q7']['fix'], rf.FIX['salvage'])
        self.assertEqual(r['fairness']['review']['notes']['q8']['fix'], rf.FIX['dict_keys'])
        self.assertEqual(r['fairness']['review']['notes']['q6']['fix'], rf.FIX['columns'])

    def test_R6_one_failing_key_and_R9_doubled_points(self):
        nb = self.notebook()
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'].replace("].median()", "].meadian()"))
        self.replace(nb, 'before', NOTEBOOK_ANSWERS['before'].replace(
            "raw_data.plot.scatter(x='load_pct', y='target', ax=axes)",
            "raw_data.plot.scatter(x='load_pct', y='target', ax=axes)\naxes.scatter(raw_data['load_pct'], raw_data['target'])"))
        off = self.awards(self.grade(nb, OWN_ONLY))
        self.assertEqual((off['q2'], off['q7']), (6, 0))
        r = self.grade(nb)
        a = self.awards(r)
        self.assertAlmostEqual(a['q7'], 5 * 8 / 12, places=3)     # mean and sum right, median still lost
        self.assertEqual(a['q2'], 10, r['fairness'])

    def test_wrong_is_still_wrong(self):
        nb = self.notebook()
        self.replace(nb, 'loops', NOTEBOOK_ANSWERS['loops'].replace("'low'] += 1", "'low'] += 2").replace("'low'", "'Low'"))
        self.replace(nb, 'function', "def calculate_column_statistics(table, column_name):\n"
                     "    return {'mean': table[column_name].max(), 'sum': table[column_name].sum() + 1, 'median': table[column_name].meadian()}\n")
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q7'], 0, r['fairness'])
        self.assertLess(a['q8'], 10)
        self.assertNotIn('q8', r['fairness']['review']['notes'])

    def test_switch_off_is_the_own_work_result(self):
        nb = self.notebook()
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'] + 'target_stats =\n')
        own = self.grade(nb, OWN_ONLY)
        self.assertNotIn('review', own['fairness'])
        self.assertNotIn('review_repair', own['fairness'])
        on = self.grade(nb)
        for q, v in self.awards(own).items():
            self.assertGreaterEqual(self.awards(on)[q], v)


@unittest.skipUnless(_docker_ready(), 'Docker sandbox image not available')
class AssignmentSandbox(unittest.TestCase):
    """A2-A5 path (isolated_grading.evaluate)."""

    def grade(self, nb, env=ON):
        from batch_grade import grade_one
        with patch.dict(os.environ, env), tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'S99997_W04.ipynb'
            p.write_text(json.dumps(nb))
            return grade_one(str(p), str(G / 'specs/spec_W04.py'), str(G / 'specs/hidden/spec_W04_hidden.py'),
                             'W04', 'CML3111', str(W04_DATA), 5, 60, None)

    def notebook(self):
        nb = json.loads((W04_DATA / 'W04_student.ipynb').read_text())
        nb['cells'][4]['source'] = ('valid = [float(r["winding_temp_c"]) for r in rows if r["winding_temp_c"].strip()]\n'
                                    'valid_count = len(valid)\n')
        nb['cells'][6]['source'] = 'mean_reading = sum(valid) / len(valid)\nprint(f"mean {mean_reading:.2f}"\n'
        nb['cells'][8]['source'] = 'above_limit = len([v for v in valid if v > 130.0])\n'
        nb['cells'][10]['source'] = ('groups = {}\nfor r in rows:\n    if r["winding_temp_c"].strip():\n'
                                     '        groups.setdefault(r["motor_id"], []).append(float(r["winding_temp_c"]))\n'
                                     'group_means = {k: sum(v) / len(v) for k, v in groups.items()}\n'
                                     'print(f"{group_means["M1"]:.1f}")\n')
        return nb

    def test_broken_line_and_python312_syntax(self):
        off = self.grade(self.notebook(), OWN_ONLY)
        on = self.grade(self.notebook())
        a_off = {q: v['awarded'] for q, v in off['questions'].items()}
        a_on = {q: v['awarded'] for q, v in on['questions'].items()}
        self.assertEqual(a_off, {'q1': 5, 'q2': 0, 'q3': 5, 'q4': 0})
        self.assertEqual(a_on, {'q1': 5, 'q2': 5, 'q3': 5, 'q4': 5}, on['fairness'])
        self.assertEqual(sorted(on['fairness']['review_repair']['kinds']), ['py312', 'salvage'])
        self.assertNotIn('review_repair', off['fairness'])


if __name__ == '__main__':
    unittest.main()
