"""Trusted synthetic answers verify grading without student-side grader files.

This does not execute student submissions or replace Docker isolation tests.
"""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'IUEA_Teaching_Plan'
sys.path.insert(0, str(BASE / 'grader'))
import iuea_grader as ig


class NoStudentGraders(unittest.TestCase):
    def test_packaged_notebooks_run_and_grade_without_helpers(self):
        for cohort in ('CML3111', 'CML3112', 'CML3113'):
            for aid in ('W03', 'W05'):
                with self.subTest(cohort=cohort, assignment=aid):
                    with zipfile.ZipFile(BASE / 'student_packages' / f'{cohort}_{aid}_student.zip') as z:
                        nb = json.loads(z.read(f'{aid}_student.ipynb'))
                        csv = z.read('campus_energy.csv') if aid == 'W05' else None
                    variant = {
                        'CML3111': 'def power_loss(current,resistance): return current**2*resistance',
                        'CML3112': 'def slab_mass(area_m2,thickness_m): return area_m2*thickness_m*2400',
                        'CML3113': 'def mud_pressure(depth_m,density): return density*9.81*depth_m/1000',
                    }[cohort]
                    answers = [
                        'weight_n=40*9.81',
                        'def percent_error(measured,expected): return 100*(measured-expected)/expected',
                        variant,
                        'def efficiency(out_w,in_w): return None if in_w<=0 else 100*out_w/in_w',
                        'worst_reading=max(READINGS,key=lambda r:abs(percent_error(r,100)))\nworst_error=percent_error(worst_reading,100)',
                    ] if aid == 'W03' else [
                        'import pandas as pd\ndf=pd.read_csv("campus_energy.csv")',
                        'n_meters=df.meter_id.nunique()',
                        'df["cost_per_kwh"]=df.cost_ugx/df.kwh',
                        'high_use=df[df.kwh>5000]',
                        'mean_cost_per_kwh=df.cost_per_kwh.mean()',
                        'peak_building=df.groupby("building").kwh.sum().idxmax()',
                    ]
                    answer_iter = iter(answers)
                    old_cwd = Path.cwd()
                    with tempfile.TemporaryDirectory() as tmp:
                        try:
                            os.chdir(tmp)
                            if csv is not None: Path('campus_energy.csv').write_bytes(csv)
                            ns = {}
                            for cell in nb['cells']:
                                if cell['cell_type'] != 'code': continue
                                source = ''.join(cell['source'])
                                if source.strip() == '# Your answer here': source = next(answer_iter)
                                self.assertNotRegex(source, r'iuea_grader|spec_W\d+|g\.check\(')
                                exec(compile(source, '<trusted fixture>', 'exec'), ns)
                            self.assertIsNone(next(answer_iter, None))
                            spec = ig.load_spec(aid, str(BASE / 'grader/specs' / f'spec_{aid}.py'),
                                include_hidden=True, hidden_path=str(BASE / 'grader/specs/hidden' / f'spec_{aid}_hidden.py'))
                            results = [ig.run_check(qid, q, ns) for qid, q in ig.resolve_questions(spec, cohort)]
                            self.assertEqual(sum(r.awarded for r in results), 20, [r.message for r in results])
                        finally:
                            os.chdir(old_cwd)


if __name__ == '__main__': unittest.main()
