"""Check that each key term is explained before a slide uses it (Weeks 8 to 12, one cohort).
A term is 'explained' on the first slide whose title starts with one of its definition titles.
A term is 'used' on the first slide whose on-slide text matches its pattern (the objectives slide and the
definition slides' own tables are skipped). Usage: python3 scripts/audit_term_order_20261030.py [--dir DIR]"""
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx import Presentation
from patch_weeks8b_12_20261030 import deck_name, first_title, DECKS

T = {8: {
 r"\bfeatures?\b": ["Words for the data and the task"], r"\balgorithm\b": ["Words for the whole field"],
 r"\bvalidation\b": ["Some rows stay hidden"], r"mean squared error|\bMSE\b|\bRMSE\b|\bMAE\b": ["Four misses"],
 r"gradient descent|learning rate": ["Training walks downhill"], r"\bNumPy\b|\bnp\.": ["scikit-learn reads X as a table"],
 r"imputer|SimpleImputer": ["A model cannot learn from a blank"], r"pipeline": ["A pipeline runs its steps"],
 r"hyperparameter|max_depth": ["A decision tree asks yes or no"], r"random_state": ["A decision tree asks yes or no"],
 r"\bbaseline\b": ["Start with a simple reference", "A training-mean baseline"], r"\bleaf\b|\bleaves\b": ["A decision tree asks yes or no"]},
 9: {r"\bprobabilit": ["Words for today: the question"], r"\bthreshold": ["Words for today: the question"],
 r"\baccuracy": ["A model that always says no"], r"StandardScaler|scaled": ["Features on different scales"],
 r"predict_proba": ["Fitting a classifier"], r"confusion matrix": ["Words for scoring the answers"],
 r"\bprecision": ["Words for scoring the answers", "Precision recall and cost"], r"\brecall": ["Words for scoring the answers", "Precision recall and cost"],
 r"\bF1\b": ["F1 combines"], r"\bAUC\b|\bROC\b": ["The ROC curve"]},
 10: {r"overfit": ["Words for today: fitting"], r"underfit": ["Words for today: fitting"], r"generalis": ["Words for today: fitting"],
 r"cross-validation|GroupKFold": ["Words for today: repeated"], r"\bfold": ["Words for today: repeated"], r"leak": ["Words for today: repeated", "Leakage makes"]},
 11: {r"feature engineering|derived feature": ["Words for today: making"], r"interaction": ["Words for today: making"], r"ablation": ["Words for today: making"]},
 13: {r"regularisation|penalty": ["Words for today: holding a model back"], r"\bRidge\b|ridge": ["Words for today: holding a model back"], r"\balpha\b": ["Words for today: holding a model back"],
 r"polynomial": ["Words for today: holding a model back"], r"neighbour": ["Words for today: predicting from neighbours"], r"\bKNN\b": ["Words for today: predicting from neighbours"]},
 12: {r"\blatency": ["Words for today: choosing"], r"\bconstraint": ["Words for today: choosing"], r"random forest|RandomForest": ["Words for today: choosing"],
 r"\bboosting": ["Words for today: choosing"], r"model card": ["A model card puts the evidence"]}}
SKIP = ("Today’s learning",)
# Reviewed by hand: the first use is itself the definition, or the word is used in its ordinary sense.
ALLOW = {(8, r"\bbaseline\b"): "slide introduces and defines baseline in its own text", (8, r"\bleaf\b|\bleaves\b"): "ordinary verb 'leaves the table unchanged'",
         (10, r"cross-validation|GroupKFold"): "defined inline on the slide that introduces it", (10, r"leak"): "word appears in the week title only"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=None); ap.add_argument("--cohort", default="CML3111"); a = ap.parse_args()
    d = Path(a.dir) if a.dir else DECKS; flagged = 0
    for week, terms in T.items():
        prs = Presentation(str(d / deck_name(a.cohort, week))); slides = []
        for i, s in enumerate(prs.slides, 1):
            txt = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame); slides.append((i, first_title(s), txt))
        for pat, defs in terms.items():
            di = next((i for i, t, _ in slides if any(t.startswith(x) for x in defs)), None)
            ui = next((i for i, t, x in slides if t not in SKIP and re.search(pat, x, re.I) and not any(t.startswith(k) for k in defs)), None)
            ok = di is not None and (ui is None or ui >= di)
            if not ok and (week, pat) in ALLOW:
                print(f"W{week}: {pat!r} allowed ({ALLOW[(week, pat)]})"); continue
            if not ok:
                flagged += 1
                print(f"W{week}: {pat!r} used on slide {ui} ({slides[ui-1][1][:45] if ui else ''}) before its definition on slide {di}")
    print("flagged:", flagged); return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
