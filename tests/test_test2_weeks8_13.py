"""Practical Test 2 covers Weeks 8 to 13: grader contracts, notebooks, rubric and the Week 14 revision slides.
Uses real scikit-learn when it is installed, otherwise the NumPy stand-in from verify_week_slides_20261030."""
import contextlib, io, json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; G = ROOT / 'IUEA_Teaching_Plan/grader'
sys.path.insert(0, str(G)); sys.path.insert(0, str(ROOT / 'scripts'))
try:
    import sklearn  # noqa: F401
except ImportError:
    import verify_week_slides_20261030 as V; V.install_shim()
import colab_exam_contracts as C
from engineering_contracts import DOMAINS
REFERENCE = (G / 'engineering_pandas_reference.py').read_text()


class NS:
    def __init__(self, ns): self.ns = ns
    def get(self, k, d=None): return self.ns.get(k, d)


def score(source, cohort, extra=None):
    ns = {'COHORT': cohort}; exec(compile(source, 'solution', 'exec'), ns); ns['DECISIONS'] = C.decision_keys()['TEST2']; ns.update(extra or {})
    return {t: C.assess(NS(ns), 'TEST2', t)[2] for t, _ in C.PARTS['TEST2']}


class Test2Weeks8To13(unittest.TestCase):
    def test_marks_and_rubric(self):
        parts = C.PARTS['TEST2']; self.assertEqual(sum(m for _, m in parts), 100)
        self.assertEqual([t for t, _ in parts], ['split', 'regression', 'errors', 'classification', 'groupcv', 'ablation', 'selection', 'ridgeknn', 'decisions'])
        rubric = json.loads((G / 'rubrics/TEST2.json').read_text())
        self.assertEqual([c['maximum'] for c in rubric['criteria']], [m for _, m in parts])
        self.assertEqual(rubric['id'], 'TEST2-' + C.VERSION)

    def test_reference_solution_scores_full_marks(self):
        for cohort in DOMAINS: self.assertEqual(set(score(REFERENCE, cohort).values()), {1.0}, cohort)

    def test_blank_scores_zero_except_nothing(self):
        for cohort in DOMAINS:
            ns = {'COHORT': cohort, 'DECISIONS': {}}
            self.assertEqual({C.assess(NS(ns), 'TEST2', t)[2] for t, _ in C.PARTS['TEST2']}, {0})

    def test_common_mistakes_lose_marks(self):
        wrong_alpha = REFERENCE.replace('Ridge(alpha=1.0)', 'Ridge(alpha=10.0)')
        unscaled = REFERENCE.replace("make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=3))", "make_pipeline(KNeighborsRegressor(n_neighbors=3))")
        uses_e6 = REFERENCE.replace("for group in ['E1', 'E2', 'E3', 'E4', 'E5']:", "for group in ['E1', 'E2', 'E3', 'E4', 'E5', 'E6']:")
        weak_cost = REFERENCE.replace('cost=5*fn+fp', 'cost=fn+fp')
        for name, src, task in [('alpha', wrong_alpha, 'ridgeknn'), ('unscaled', unscaled, 'ridgeknn'), ('E6', uses_e6, 'groupcv'), ('cost', weak_cost, 'classification')]:
            self.assertLess(score(src, 'CML3111')[task], 1.0, name)

    def test_notebooks_list_eight_tasks_and_six_choices(self):
        for cohort in DOMAINS:
            for variant in 'ABC':
                nb = json.loads((G.parent / 'assessment_banks/TEST2' / cohort / variant / 'TEST2_student.ipynb').read_text())
                text = '\n'.join(''.join(c['source']) for c in nb['cells'])
                self.assertEqual(text.count('## Task '), 8); self.assertIn('Structured interpretation — 15 marks', text)
                for fn in ('group_split', 'predict_regression', 'regression_errors', 'classification_metrics', 'group_cv_mae', 'ablation_metrics', 'select_model', 'ridge_and_knn'):
                    self.assertIn('def ' + fn + '(', text)
                self.assertNotIn('offline', text.lower())

    def test_week14_slide_examples_print_what_the_slides_show(self):
        from pptx import Presentation
        import test2_deck_examples_20261030 as X
        want = {'classify': X.EXAMPLES['classify'], 'groupcv': X.EXAMPLES['groupcv'], 'ablation': X.EXAMPLES['ablation'], 'select': X.EXAMPLES['select'],
                'ridgeknn': X.EXAMPLES['ridgeknn_build'] + '\n' + X.EXAMPLES['ridgeknn_score']}
        printed = {}
        for k, code in want.items():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf): exec(compile(code, k, 'exec'), {})
            printed[k] = buf.getvalue().strip()
        deck = Presentation(str(next((G.parent / 'decks').glob('CML3111_Week14_*.pptx'))))
        slide_text = '\n'.join(sh.text_frame.text for s in deck.slides for sh in s.shapes if sh.has_text_frame)
        for k, out in printed.items():
            for line in out.splitlines(): self.assertIn(line, slide_text, (k, line))


if __name__ == '__main__': unittest.main()
