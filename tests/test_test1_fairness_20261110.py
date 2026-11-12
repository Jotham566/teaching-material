"""Test 1 grader fairness fixes ordered on 10 Nov 2026.

Colab shim (CSV copies, IPython/display, plt.close after each cell), own-cell snapshots,
lenient unit/label variants, reference inputs for dependent questions (Q2-Q6, Q8),
Q7 per-key credit. Marks can only go up. Fixtures are synthetic; notebook code only
runs in the Docker sandbox.
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
import test1_fairness as tf  # noqa: E402
from test1_coding_reference import NOTEBOOK_ANSWERS, complete_notebook  # noqa: E402

BANK = G.parent / 'assessment_banks/TEST1/CML3111/A'


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

    def test_lenient_units(self):
        for label in ('Temperature (deg C)', 'Motor winding temperature c', 'Temperature (C)', 'temp °', 'Temp_degrees'):
            self.assertTrue(tf.lenient_unit(label, 'deg C'), label)
        for label in ('target_kw', 'Target_KW', 'Cooling load (kilowatts)', 'kW'):
            self.assertTrue(tf.lenient_unit(label, 'kW'), label)
        for label in ('kWh per tonne', 'Energy kwh/ton', 'kWh/t', 'kwh_per_t'):
            self.assertTrue(tf.lenient_unit(label, 'kWh/t'), label)
        # Still no unit, or the wrong unit, earns nothing.
        for label, unit in (('Target', 'deg C'), ('Cooling load', 'kW'), ('Energy kWh', 'kW'),
                            ('Energy (kWh)', 'kWh/t'), ('', 'kW'), (None, 'kW'), ('Crusher energy', 'kWh/t')):
            self.assertFalse(tf.lenient_unit(label, unit), label)

    def test_lenient_percent(self):
        for label in ('Load (%)', 'Load percent', 'load_pct', 'Load pct'):
            self.assertTrue(tf.lenient_percent(label), label)
        for label in ('Load', '', None, 'capacity'):
            self.assertFalse(tf.lenient_percent(label), label)

    def test_task_cells_tags_headings_and_added_cells(self):
        nb = json.loads((BANK / 'TEST1_student.ipynb').read_text())
        cells = tf.task_cells(nb)
        self.assertEqual(cells['cleaning'], [9])
        self.assertEqual(cells['loops'], [19])
        # A student-added cell after Task 3 belongs to Task 3; tags lost: headings decide.
        nb['cells'].insert(10, {'cell_type': 'code', 'metadata': {}, 'source': 'cleaned_data = cleaned_data.copy()'})
        for c in nb['cells']:
            c.get('metadata', {}).pop('tags', None)
        cells = tf.task_cells(nb)
        self.assertEqual(cells['cleaning'], [9, 10])
        self.assertEqual(cells['after'], [12])
        self.assertNotIn(3, sum(cells.values(), []))  # support cell never re-run
        self.assertNotIn(22, sum(cells.values(), []))  # submission cell never re-run

    def test_describe_of_measurement_columns(self):
        import pandas as pd
        raw = pd.read_csv(BANK / 'engineering_data.csv')
        self.assertTrue(tf._describe_ok(raw[['load_pct', 'ambient_c', 'target']].describe(), raw))
        self.assertTrue(tf._describe_ok(raw.describe(include='all'), raw))
        self.assertFalse(tf._describe_ok(raw[['target']].describe(), raw))
        self.assertFalse(tf._describe_ok(raw.head(), raw))

    def test_combine_only_raises(self):
        plain = {'questions': {'q1': dict(ok=False, awarded=10.0, marks=20.0, msg=''),
                               'q2': dict(ok=True, awarded=10.0, marks=10.0, msg='')}}
        fair = {'questions': {'q1': dict(ok=True, awarded=20.0, marks=20.0, fix='Colab shim run', detail=''),
                              'q2': dict(ok=False, awarded=2.0, marks=10.0, fix='x', detail='')}}
        out = tf.combine(plain, fair)
        self.assertEqual(out['questions']['q1']['awarded'], 20.0)
        self.assertEqual(out['questions']['q2']['awarded'], 10.0)
        self.assertEqual(set(out['fairness']['changes']), {'q1'})


@unittest.skipUnless(_docker_ready(), 'Docker sandbox image not available')
class SandboxRuns(unittest.TestCase):
    """Real runs in the iuea-notebooks sandbox."""

    def notebook(self):
        return complete_notebook(json.loads((BANK / 'TEST1_student.ipynb').read_text()))

    def replace(self, nb, task, source):
        for c in nb['cells']:
            if 'iuea-answer-' + task in c.get('metadata', {}).get('tags', []):
                c['source'] = source

    def grade(self, nb):
        from batch_grade import grade_one
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'test.ipynb'
            path.write_text(json.dumps(nb))
            return grade_one(str(path), str(G / 'specs/spec_TEST1.py'), str(G / 'specs/hidden/spec_TEST1_hidden.py'),
                             'TEST1', 'CML3111', str(BANK), 20, 180, None)

    def awards(self, r):
        return {q: v['awarded'] for q, v in r['questions'].items()}

    def test_complete_notebook_unchanged(self):
        r = self.grade(self.notebook())
        self.assertEqual(sum(self.awards(r).values()), 100, r)
        self.assertEqual(r['fairness']['changes'], {})

    def test_switch_off_gives_original(self):
        nb = self.notebook()
        self.replace(nb, 'eda', NOTEBOOK_ANSWERS['eda'].replace('pd.read_csv(file_path)', 'pd.read_csv("/content/engineering_data (1).csv")'))
        with patch.dict(os.environ, {'IUEA_TEST1_FAIRNESS': '0'}):
            r = self.grade(nb)
        self.assertNotIn('fairness', r)
        self.assertLess(sum(self.awards(r).values()), 50)

    def test_colab_copy_path_ipython_and_display(self):
        nb = self.notebook()
        self.replace(nb, 'eda', NOTEBOOK_ANSWERS['eda'].replace('pd.read_csv(file_path)', 'pd.read_csv("/content/engineering_data (1).csv")') + 'display(first_rows)\n')
        self.replace(nb, 'cleaning', 'from IPython.core.display import clear_output\n' + NOTEBOOK_ANSWERS['cleaning'])
        r = self.grade(nb)
        self.assertEqual(sum(self.awards(r).values()), 100, r)
        self.assertEqual(r['fairness']['changes']['q1']['fix'], 'Colab shim run')
        self.assertEqual(r['fairness']['original_questions']['q3'], 0)

    def test_agg_backend_figure_overwrite(self):
        nb = self.notebook()
        # In Colab plt.show() closes the figure; this later pyplot call must not change before_figure.
        self.replace(nb, 'cleaning', NOTEBOOK_ANSWERS['cleaning'] + "plt.scatter([1, 2], [3, 4])\nplt.ylabel('y')\n")
        r = self.grade(nb)
        self.assertEqual(self.awards(r)['q2'], 10, r)

    def test_cascade_uses_reference_inputs_and_keeps_own_q3(self):
        nb = self.notebook()
        broken = NOTEBOOK_ANSWERS['cleaning'].replace("cleaned_data = cleaned_data.drop_duplicates('record_id')", "cleaned_data.drop_duplicates('record_id')")
        self.replace(nb, 'cleaning', broken)
        r = self.grade(nb)
        a = self.awards(r)
        self.assertLess(a['q3'], 20)  # the student's own error still costs marks once
        for q, full in (('q4', 10), ('q5', 15), ('q6', 10), ('q8', 10)):
            self.assertEqual(a[q], full, (q, r['fairness']))
            self.assertIn('reference inputs', r['fairness']['changes'][q]['fix'])

    def test_own_cell_snapshot_beats_later_overwrite_and_rerun_on_reference_raw(self):
        nb = self.notebook()
        self.replace(nb, 'grouping', NOTEBOOK_ANSWERS['grouping'] + "cleaned_data = cleaned_data['load_pct'].between(0, 100)\n")
        self.replace(nb, 'eda', NOTEBOOK_ANSWERS['eda'].replace('raw_data = pd.read_csv(file_path)', 'raw_data = pd.read_csv'))
        r = self.grade(nb)
        a = self.awards(r)
        self.assertEqual(a['q3'], 20, r['fairness'])
        self.assertEqual(a['q2'], 10, r['fairness'])
        # The other Task 1 lines are re-run on the reference raw_data; the reading marks stay lost.
        self.assertEqual(a['q1'], 18, r['fairness'])

    def test_renamed_function_gets_half(self):
        nb = self.notebook()
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'].replace('calculate_column_statistics', 'calculate_stats'))
        r = self.grade(nb)
        self.assertAlmostEqual(self.awards(r)['q7'], 2.5, places=4)

    def test_q7_one_bad_key_and_unit_variant(self):
        nb = self.notebook()
        self.replace(nb, 'function', NOTEBOOK_ANSWERS['function'].replace("table[column_name].median()", "table[column_name].median"))
        self.replace(nb, 'before', NOTEBOOK_ANSWERS['before'].replace("'Target (' + TARGET_UNIT + ')'", "'Motor winding temperature c'"))
        r = self.grade(nb)
        a = self.awards(r)
        self.assertAlmostEqual(a['q7'], 5 * 8 / 12, places=3)
        self.assertEqual(r['fairness']['original_questions']['q7'], 0)
        self.assertEqual(a['q2'], 10)
        self.assertEqual(r['fairness']['original_questions']['q2'], 8)


if __name__ == '__main__':
    unittest.main()
