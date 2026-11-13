"""Own-work credit for coded answers (lecturer's rule, 13 Nov 2026).

"We shouldn't penalize students if they wrote their own code cells, as long as they
wrote the correct code and answered the question." Behind IUEA_OWNWORK_FAIRNESS=1:
1 a correct answer under a different name earns FULL credit when unambiguous,
2 a correct printed/displayed answer counts, 3 a correct chart on the student's own
figure counts, 4 marks never go down, 5 wrong is still wrong. Switched off, the
10 Nov results are unchanged. Fixtures are synthetic; notebook code only runs in
the Docker sandbox.
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
import grader_fairness as gf  # noqa: E402
import ownwork_fairness as ow  # noqa: E402
from test1_coding_reference import NOTEBOOK_ANSWERS, complete_notebook  # noqa: E402

BANK = G.parent / 'assessment_banks/TEST1/CML3111/A'
W04_DATA = G.parent / 'practicals/W04/CML3111'
ON = {'IUEA_OWNWORK_FAIRNESS': '1'}
OFF = {'IUEA_OWNWORK_FAIRNESS': '0'}


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


def code(*cells):
    return {'cells': [{'cell_type': 'code', 'metadata': {}, 'source': c} for c in cells]}


class _Result:
    def __init__(self, awarded, marks=4.0):
        self.awarded, self.ok, self.message, self.marks = awarded, awarded >= marks, '', marks


class _FakeIG:
    """run_check stand-in: full marks when the view reads the right value for 'answer'."""
    def run_check(self, qid, question, ns):
        return _Result(4.0 if ns.get('answer') == 42 else 0.0)


class _FakeNS:
    def __init__(self, values):
        self.values = values
        self.notebook_sources = []

    def get(self, name, default=None):
        return self.values.get(name, default)


class HostHelpers(unittest.TestCase):
    """No Docker."""

    def test_switch_is_off_by_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('IUEA_OWNWORK_FAIRNESS', None)
            self.assertFalse(ow.enabled())
        with patch.dict(os.environ, ON):
            self.assertTrue(ow.enabled())

    def test_question_cells_from_headings_and_names(self):
        nb = json.loads((W04_DATA / 'W04_student.ipynb').read_text())
        cells = ow.question_cells(nb, 'W04', lambda q: gf.required_names('W04', q, 'CML3111'), ['q1', 'q2', 'q3', 'q4'])
        self.assertEqual(cells, {'q1': [4], 'q2': [6], 'q3': [8], 'q4': [10]})
        # No headings (W02 style): a question's cells are those that mention its name.
        nb = code('proof_sum = 2 + 2', 'readings = 12', 'print(readings + 5)', 'x = 1')
        cells = ow.question_cells(nb, 'W02', lambda q: gf.required_names('W02', q, 'CML3111'), ['q2', 'q3'])
        self.assertEqual(cells, {'q2': [0], 'q3': [1, 2]})

    def test_assigned_names(self):
        nb = code('a = 1\nb, c = 2, 3\nd += 1\ndef f(x):\n    inner = 2\n    return x', 'for i in range(3):\n    e = i', '%matplotlib inline\ng = 5')
        self.assertEqual(ow.assigned_names(nb, [0, 1, 2]), ['a', 'b', 'c', 'd', 'f', 'g'])

    def test_family(self):
        import pandas as pd
        self.assertEqual(ow.family(3), 'number')
        self.assertEqual(ow.family(True), 'bool')
        self.assertEqual(ow.family(pd.DataFrame({'a': [1]})), 'table')
        self.assertEqual(ow.family(len), 'callable')
        self.assertIsNone(ow.family('__MISSING__'))

    def test_view_renames_source_scans(self):
        base = _FakeNS({'counts': {'low': 1}})
        base.notebook_sources = ['for v in x:\n    counts["low"] += 1']
        view = ow.View(base, {'load_band_counts': 'counts'}, renamed={'counts'})
        self.assertEqual(view.get('load_band_counts'), {'low': 1})
        self.assertIn('load_band_counts["low"] += 1', view.notebook_sources[0])

    def test_rule1_unambiguous_name_gets_full_credit(self):
        ns = _FakeNS({'my_value': 42})
        res = dict(awarded=0.0, marks=4.0, ok=False, msg='')
        q = ow.with_cells({'marks': 4}, [0])
        note, flags = ow.rescore(_FakeIG(), gf, 'q1', q, res, [('the whole notebook', ns, None)], ['answer'],
                                 ['answer'], ['my_value'], ['my_value'], [])
        self.assertEqual(res['awarded'], 4.0)
        self.assertEqual(note['fix'], ow.FIX_NAME)
        self.assertEqual(flags, [])

    def test_rule1_ambiguous_names_are_flagged_not_credited(self):
        ns = _FakeNS({'first': 42, 'second': 7})
        res = dict(awarded=0.0, marks=4.0, ok=False, msg='')
        q = ow.with_cells({'marks': 4}, [0])
        note, flags = ow.rescore(_FakeIG(), gf, 'q1', q, res, [('the whole notebook', ns, None)], ['answer'],
                                 ['answer'], ['first', 'second'], ['first', 'second'], [])
        self.assertIsNone(note)
        self.assertEqual(res['awarded'], 0.0)
        self.assertTrue(flags and flags[0].startswith('AMBIGUOUS_NAME q1: first'), flags)

    def test_names_of_other_questions_are_not_candidates(self):
        ns = _FakeNS({'answer_q2': 42})
        res = dict(awarded=0.0, marks=4.0, ok=False, msg='')
        q = ow.with_cells({'marks': 4}, [0])
        note, _ = ow.rescore(_FakeIG(), gf, 'q1', q, res, [('the whole notebook', ns, None)], ['answer'],
                             ['answer'], [], ['answer_q2'], [], foreign=['answer_q2'])
        self.assertIsNone(note)

    def test_rule2_printed_value_counts_only_in_its_own_cells(self):
        res = dict(awarded=0.0, marks=4.0, ok=False, msg='')
        outputs = [{'key': '__iuea_out_0', 'cell': 1, 'rerun': None, 'kind': 'print', 'text': '42'}]
        ns = _FakeNS({'__iuea_out_0': 42})
        note, _ = ow.rescore(_FakeIG(), gf, 'q1', ow.with_cells({'marks': 4}, [5]), dict(res),
                             [('the whole notebook', ns, None)], ['answer'], ['answer'], [], [], outputs)
        self.assertIsNone(note)  # printed in another question's cell
        note, _ = ow.rescore(_FakeIG(), gf, 'q1', ow.with_cells({'marks': 4}, [0]), res,
                             [('the whole notebook', ns, None)], ['answer'], ['answer'], [], [], outputs)
        self.assertEqual(note['fix'], ow.FIX_PRINT)
        self.assertEqual(res['awarded'], 4.0)

    def test_rule5_wrong_printed_value_earns_nothing(self):
        res = dict(awarded=0.0, marks=4.0, ok=False, msg='')
        outputs = [{'key': '__iuea_out_0', 'cell': 1, 'rerun': None, 'kind': 'print', 'text': '41'}]
        note, _ = ow.rescore(_FakeIG(), gf, 'q1', ow.with_cells({'marks': 4}, [0]), res,
                             [('the whole notebook', _FakeNS({'__iuea_out_0': 41}), None)],
                             ['answer'], ['answer'], [], [], outputs)
        self.assertIsNone(note)
        self.assertEqual(res['awarded'], 0.0)

    def test_full_marks_untouched(self):
        res = dict(awarded=4.0, marks=4.0, ok=True, msg='')
        note, _ = ow.rescore(_FakeIG(), gf, 'q1', ow.with_cells({'marks': 4}, [0]), res,
                             [('x', _FakeNS({}), None)], ['answer'], ['answer'], [], [], [])
        self.assertIsNone(note)


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
        self.assertEqual(r['fairness']['ownwork']['notes'], {})

    def test_rule1_different_names_full_credit(self):
        nb = self.notebook()
        self.replace(nb, 'cleaning', NOTEBOOK_ANSWERS['cleaning'].replace('cleaned_data', 'tidy_data'))
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'].replace('calculate_column_statistics', 'calculate_stats'))
        off = self.grade(nb, OFF)
        self.assertEqual(self.awards(off)['q3'], 10)      # 10 Nov: half for a different name
        self.assertAlmostEqual(self.awards(off)['q7'], 2.5, places=4)
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q3'], 20, r['fairness'])
        self.assertEqual(a['q7'], 5, r['fairness'])
        self.assertEqual(r['fairness']['ownwork']['notes']['q3']['fix'], ow.FIX_NAME)

    def test_rule2_printed_answers_count(self):
        nb = self.notebook()
        self.replace(nb, 'statistics', "target_mean = None\nprint(cleaned_data['target'].mean())\n"
                     "print('Sum:', cleaned_data['target'].sum())\nprint(f\"median {cleaned_data['target'].median()}\")\n"
                     "cleaned_data['target'].count()\n")
        self.replace(nb, 'eda', NOTEBOOK_ANSWERS['eda'].replace('data_shape = raw_data.shape', 'print(raw_data.shape)')
                     .replace('first_rows = raw_data.head()', 'display(raw_data.head())'))
        off = self.grade(nb, OFF)
        self.assertEqual(self.awards(off)['q1'], 18)
        self.assertEqual(self.awards(off)['q5'], 0)
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q1'], 20, r['fairness'])
        # mean, sum, median (number inside printed text) and count (last expression); std and modes missing.
        self.assertEqual(a['q5'], 10, r['fairness'])
        self.assertIn(ow.FIX_PRINT, r['fairness']['ownwork']['notes']['q5']['fix'])

    def test_rule3_chart_on_own_figure_counts(self):
        nb = self.notebook()
        self.replace(nb, 'before', "fig2, ax2 = plt.subplots()\nax2.scatter(raw_data['load_pct'], raw_data['target'])\n"
                     "ax2.set_title('Raw')\nax2.set_xlabel('Load (%)')\nax2.set_ylabel('Target (' + TARGET_UNIT + ')')\n"
                     "figure, axes = plt.subplots()\nbefore_figure = figure\nplt.show()\n")
        self.replace(nb, 'after', "plt.figure()\nplt.scatter(cleaned_data['load_pct'], cleaned_data['target'])\n"
                     "plt.title('Clean')\nplt.xlabel('Load (%)')\nplt.ylabel('Target (' + TARGET_UNIT + ')')\nplt.show()\n")
        off = self.grade(nb, OFF)
        self.assertEqual(self.awards(off)['q2'], 0)
        self.assertEqual(self.awards(off)['q4'], 0)
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q2'], 10, r['fairness'])
        self.assertEqual(a['q4'], 10, r['fairness'])   # unnamed pyplot figure, recorded when the cell ended
        self.assertIn(ow.FIX_CHART, r['fairness']['ownwork']['notes']['q4']['fix'])

    def test_rule5_wrong_is_still_wrong(self):
        nb = self.notebook()
        self.replace(nb, 'statistics', "target_mean = None\nprint(cleaned_data['target'].mean() + 1)\nprint(cleaned_data['target'].sum() / 2)\n")
        self.replace(nb, 'after', "plt.figure()\nplt.scatter(raw_data['load_pct'], raw_data['target'])\nplt.show()\n")
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q5'], 0, r['fairness'])
        # Wrong rows, no title, no labels: the own-work pass adds nothing to Q4.
        self.assertNotIn('q4', r['fairness']['ownwork']['notes'])
        self.assertEqual(a['q4'], r['fairness']['before_ownwork']['q4'])

    def test_switch_off_reproduces_10_nov(self):
        nb = self.notebook()
        self.replace(nb, 'statistics', "print(cleaned_data['target'].mean())\n")
        r = self.grade(nb, OFF)
        self.assertNotIn('ownwork', r['fairness'])
        on = self.grade(nb)
        self.assertEqual({k: v for k, v in on['fairness']['original_questions'].items()},
                         r['fairness']['original_questions'])
        before = on['fairness']['before_ownwork']
        for q, v in self.awards(r).items():
            self.assertAlmostEqual(max(v, r['fairness']['original_questions'][q]), max(before[q], on['fairness']['original_questions'][q]))
            self.assertGreaterEqual(self.awards(on)[q], v)

    def test_ambiguous_dataframes_flagged(self):
        nb = self.notebook()
        self.replace(nb, 'cleaning', NOTEBOOK_ANSWERS['cleaning'].replace('cleaned_data', 'tbl')
                     + "other_tbl = raw_data.copy()\ncleaned_data = None\n")
        r = self.grade(nb)
        self.assertEqual(self.awards(r)['q3'], 0, r['fairness'])
        self.assertTrue(any(f.startswith('AMBIGUOUS_NAME q3') for f in r['fairness']['ownwork']['flags']), r['fairness'])


@unittest.skipUnless(_docker_ready(), 'Docker sandbox image not available')
class AssignmentSandbox(unittest.TestCase):
    """A2-A5 path (isolated_grading._fairness_pass)."""

    def grade(self, cells, assignment, data=None, env=ON):
        from batch_grade import grade_one
        with patch.dict(os.environ, env), tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ('S99997_%s.ipynb' % assignment)
            p.write_text(json.dumps(cells))
            return grade_one(str(p), str(G / ('specs/spec_%s.py' % assignment)),
                             str(G / ('specs/hidden/spec_%s_hidden.py' % assignment)),
                             assignment, 'CML3111', str(data) if data else None, 5, 60, None)

    def notebook(self):
        nb = json.loads((W04_DATA / 'W04_student.ipynb').read_text())
        answers = {
            4: 'valid = [float(r["winding_temp_c"]) for r in rows if r["winding_temp_c"].strip()]\nprint(len(valid))',
            6: 'avg_temp = sum(valid) / len(valid)',
            8: 'above_limit = len([v for v in valid if v > 130.0])',
            10: 'groups = {}\nfor r in rows:\n    if r["winding_temp_c"].strip():\n        groups.setdefault(r["motor_id"], []).append(float(r["winding_temp_c"]))\n'
                '{k: sum(v) / len(v) for k, v in groups.items()}',
        }
        for i, src in answers.items():
            nb['cells'][i]['source'] = src
        return nb

    def test_printed_renamed_and_shown_answers(self):
        off = self.grade(self.notebook(), 'W04', W04_DATA, OFF)
        on = self.grade(self.notebook(), 'W04', W04_DATA)
        a_off = {q: v['awarded'] for q, v in off['questions'].items()}
        a_on = {q: v['awarded'] for q, v in on['questions'].items()}
        self.assertEqual(a_off, {'q1': 0, 'q2': 0, 'q3': 5, 'q4': 0})
        self.assertEqual(a_on, {'q1': 5, 'q2': 5, 'q3': 5, 'q4': 5}, on['fairness'])
        notes = on['fairness']['ownwork']['notes']
        self.assertEqual(notes['q1']['fix'], ow.FIX_PRINT)       # print(len(valid))
        self.assertEqual(notes['q2']['fix'], ow.FIX_NAME)        # avg_temp: the only number in its cell
        self.assertEqual(notes['q4']['fix'], ow.FIX_PRINT)       # dict shown as the last expression
        self.assertNotIn('ownwork', off['fairness'])


if __name__ == '__main__':
    unittest.main()
