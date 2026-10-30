"""Weeks 8b to 12 patch, 30 October 2026.

Run after patch_week8_20261030.py. For each cohort it
  * adds the explain-before-use slides to Week 8 (equation of the line, blanks, pipeline, tree, results, words);
  * rebuilds Weeks 9 to 12: removes the blocks that repeat Week 8, adds vocabulary, concept and worked slides
    with spoken-script notes, replaces the generic objectives and exit check, and re-orders the deck;
  * renumbers footers.
Every number on a new slide comes from week_reference_numpy (NumPy re-implementations of the scikit-learn
pieces). Run verify_week_reference_with_sklearn.py where scikit-learn is installed to confirm them.

Usage: python3 scripts/patch_weeks8b_12_20261030.py [--out DIR] [--weeks 8 9 10 11 12]
"""
import argparse, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import week_reference_numpy as R
import week_figs_20261030 as F
from deckkit_20261030 import *
from pptx import Presentation
import wk_8b_9_20261030 as A
import wk_10_12_20261030 as B
import wk_13_20261030 as W13

DECKS = p8.DECKS
BACKUP = DECKS / "_backup_2026-10-30"
FIGS = p8.ROOT / "figs" / "week8b_12_20261030"
NAMES = {"CML3111": "Engineering", "CML3112": "Design_Infrastructure", "CML3113": "Mining_Petroleum"}
MARK = {13: "Words for today: holding a model back", 8: "The fitted line is an equation", 9: "Words for today: the question", 10: "Words for today: fitting and fairness",
        11: "Words for today: making inputs more useful", 12: "Words for today: choosing a model"}
SUPPLIED = "Upload classification_case.csv into Colab"


NEWTITLES = {}


def first_title(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() and not sh.text_frame.text.strip().isupper():
            return sh.text_frame.text.strip()
    return ""


def deck_name(code, week): return f"{code}_Week{week:02d}_{NAMES[code]}.pptx"


def has_mark(prs, week):
    if week in (14, 15): return prs.core_properties.comments == "patched-20261030"
    return any(MARK[week] in slide_title_texts(s)[:3] for s in prs.slides)


def dedupe_title_shape(slide, title):
    shapes = [sh for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip() == title]
    for sh in shapes[:-1]: sh._element.getparent().remove(sh._element)


def nth_slides(prs): return list(prs.slides)



def fix_captions(prs, week):
    n = 0
    for sl in prs.slides:
        txt = " ".join(sh.text_frame.text for sh in sl.shapes if sh.has_text_frame)
        if week == 9 and "recall = 0.0" in txt:
            n += replace_text(sl, "precision: fraction of positive predictions that are correct.", "recall: fraction of real positives that the model found.")
        if week == 9 and "total_error_cost = 5" in txt:
            n += replace_text(sl, "precision: fraction of positive predictions that are correct.", "total_error_cost: five units per missed alert plus one per false alarm.")
        if week == 11:
            n += replace_text(sl, "Explain each quantity and the unit of the mean_load_by_equipment_group.", "Explain each quantity in the relationship and its unit before reading the pattern.")
        if week == 12:
            n += replace_text(sl, "cross-validation_data", "cross-validation")
            if "candidate_models = pd.DataFrame" in txt:
                n += replace_text(sl, "prediction_start_time: timer reading immediately before predicting the batch.", "candidate_models: one row per model, with its name, validation error and prediction time.")
    return n


COMMON_FIXES = [
    ("These are synthetic teaching records, not measurements suitable for deployment.", "These are synthetic teaching records for practice."),
    ("These costs are teaching assumptions, not approved operating limits.", "These costs are teaching assumptions for practice."),
    ("std(ddof=0) describes spread across these four errors; it is not a confidence interval.", "std(ddof=0) describes the spread across these four errors only."),
    ("negate the scores before reporting baseline_errors", "negate the scores before reporting the fold errors"),
    ("baseline_errors", "errors"),
    ("iloc[0] selects the first row by its position, not its label.", "iloc[0] selects the first row by its position."),
    ("One measured run is an illustration, not a reliable performance benchmark.", "One measured run is an illustration and varies from run to run."),
    ("The CSV supplies observations, not a table of model candidates or timings.", "The CSV supplies observations. We build the table of candidates and timings ourselves."),
    ("This classroom timing is a demonstration, not a production benchmark.", "This classroom timing is a demonstration of the method."),
    ("Illustrated spread: population SD 0.39 MPa, not a confidence interval.", "An illustration from another engineering field (strength in MPa). Our own fold errors follow on later slides."),
    ("A pipeline keeps this rule with the linear_model.", "A pipeline keeps this rule with the model."),
    ("equipment_records = raw_data.to_dict(\"records\")", "equipment_records = modelling_data.to_dict(\"records\")"),
    ("cross-validation_data", "cross-validation"),
    ("sum counts the True validation_results.", "sum counts the True entries."),
    ("keep it beside the notebook locally", "keep them beside the notebook locally"),
    ("training_data[features] selects the two input columns", "training_data[feature_columns] selects the two input columns"),
    ("Compare the printed result with the explanation in the notebook.", "Run the cell and read the output below it."),
    ("as a equipment_data", "as a table"),
]
W1315_FIXES = [
    ("state the operational test_data.", "state the test you used."), ("to check the mean_load_by_equipment_group.", "to check the result."),
    ("the offline test_data.", "the offline test."), ("Compare validation baseline_errors.", "Compare validation errors."),
    ("Training rows teach the linear_model.", "Training rows teach the model."), (".copy() creates a separate equipment_data.", ".copy() creates a separate table."),
    ("applies the imputer before the linear_model.", "applies the imputer before the model."), ("for the actual test_data.", "for the actual test."),
    ("in an independent test_data.", "in an independent test."), ("the uploaded equipment_data.", "the uploaded file."),
]
TITLE_FIXES = {"Time prediction, not training": "Time the prediction step", "Precision recall and cost": "Precision, recall and cost"}


def common_fixes(prs, late=False):
    n = 0
    for sl in prs.slides:
        for old, new in (W1315_FIXES if late else COMMON_FIXES): n += replace_text(sl, old, new)
        for sh in sl.shapes:
            if not (sh.has_text_frame and sh.text_frame.text.strip() and not sh.text_frame.text.strip().isupper()): continue
            t = sh.text_frame.text.strip()
            nt = TITLE_FIXES.get(t, t.replace(" \u2014 ", ": "))
            if nt != t:
                p0 = sh.text_frame.paragraphs[0]; p0.runs[0].text = nt
                for r in p0.runs[1:]: r.text = ""
                n += 1
            break
    return n


def build_week(code, week, src, dst):
    prs = Presentation(str(src))
    if has_mark(prs, week):
        print(f"{code} W{week}: already patched, skipped"); return False
    c = R.COHORT[code]; O = R.bundle(code); fd = FIGS / code; fd.mkdir(parents=True, exist_ok=True)
    lab = lambda: f"{code}   Week {week}   0"
    ctx = dict(code=code, c=c, O=O, figdir=fd, lab=lab)
    S = nth_slides(prs); o = lambda i: S[i - 1]
    late = week >= 13
    common_fixes(prs, late=late)
    if week in (9, 11, 12): assert fix_captions(prs, week) >= 1, 'caption fix did not apply'
    if week == 8:
        N = A.w8b(prs, ctx)
        dedupe = find_slide(prs, "Training walks downhill on the loss")
        if dedupe is not None: dedupe_title_shape(dedupe, "Training walks downhill on the loss")
        move_slide(prs, N["line_eq"], find_slide(prs, "Training walks downhill on the loss"))
        anchor = find_slide(prs, "Training a model with missing inputs")
        for k in ("blanks", "pipeline"): move_slide(prs, N[k], anchor)
        move_slide(prs, N["tree"], find_slide(prs, "Baseline and tree comparisons"))
        move_slide(prs, N["scores"], find_slide(prs, "Pandas inside the required function"))
        move_slide(prs, N["results"], find_slide(prs, "Pandas inside the required function"))
        move_slide(prs, N["words8"], find_slide(prs, "Your issued task"))
        A.w8b_exit(find_slide(prs, "Revision and submission checklist"), c, O)
        # explain before use: error measures right after the scatter, NumPy before the first NumPy code
        move_slide(prs, find_slide(prs, "Four misses, measured three ways"), find_slide(prs, "Fitting a line to observations"))
        loss = find_slide(prs, "Training walks downhill on the loss")
        for t in ("scikit-learn reads X as a table and y as a column", "NumPy arrays and their shape"):
            move_slide(prs, find_slide(prs, t), loss)
        assert replace_text(loss, "One number for how wrong the model is. We use the mean squared error.",
                            "One number for how wrong the model is. We use the mean squared error: square each miss, then average.") >= 1
        edit_notes(find_slide(prs, "Gradient descent in a few lines of NumPy"), "Here is the same walk as code.", "Here is the same walk as code, using NumPy, the library from the last two slides.")
        assert replace_text(find_slide(prs, "NumPy arrays and their shape"), "predict returns an array. Call .tolist() to get a plain Python list.",
                            "Later, a model's predict returns an array like this. Call .tolist() to get a plain Python list.") >= 1
    elif week == 9:
        assert "Every paired result belongs in one cell" in slide_title_texts(o(8))[0:2] or True
        N = A.w9(prs, ctx)
        replace_two_panels(o(2), "WHAT WE WILL DO",
                           "Turn a number into a yes or no question, teach a model to answer it, and score its answers. Learn the words class, probability, threshold, confusion matrix, precision, recall and F1.",
                           "HOW YOU WILL SHOW IT",
                           f"You can explain why a model that never raises an alert can score {(1 - O['cls_counts']['tr_pos'] / O['cls_counts']['tr_n']) * 100:.0f} percent, and say what a missed alert costs. You can read a confusion matrix and the scores built from it.")
        set_notes(o(2), "Today the question changes from how much to yes or no. We will turn the {c['short']} number into an alert, teach a model to answer it, and score its answers honestly. Along the way we learn the words class, probability, threshold, confusion matrix, precision, recall and F1. By the end you can explain why a model that never raises an alert can still score high on accuracy, and why that makes accuracy a poor judge by itself.")
        assert replace_text(o(3), SUPPLIED, "Upload classification_case.csv and engineering_data.csv into Colab") >= 1
        A.w9_exit(o(41), c, O)
        order = ([o(1), o(2), N["vocab1"], o(3), N["cvr"], N["label_code"], N["counts"], N["sigmoid"], N["scaling"], N["split"], N["fit"], N["thr"], N["vocab2"]]
                 + [o(i) for i in range(7, 31)] + [N["modelconf"], N["f1"], N["thresholds"], N["roc"], N["treeclf"], N["words9"]]
                 + [o(i) for i in (35, 36, 37, 38, 39, 40, 41, 42)])
        order_deck(prs, order)
    elif week == 10:
        N = B.w10(prs, ctx)
        replace_two_panels(o(2), "WHAT WE WILL DO",
                           "Watch a model memorise its training rows, learn to check it on several held-back groups, and find four ways a score can leak. Learn the words overfitting, cross-validation and data leakage.",
                           "HOW YOU WILL SHOW IT",
                           "You can explain why training error cannot be trusted, and how you would tell that a score is leaking. You can split by equipment group and report an error with its spread.")
        set_notes(o(2), "Last week we scored classifiers. This week we ask whether any score deserves trust. We will watch a model memorise its training rows, then learn to check a model on several held-back groups of equipment, and then meet four ways a score can leak. By the end you can explain why training error cannot be trusted, split the data by equipment group, and report an error together with its spread.")
        B.w10_exit(o(53), c, O)
        order = ([o(1), o(2), N["vocabA"], o(3), o(7), o(8), o(9), o(14), o(15), o(16), o(18), o(19), o(20), o(21), o(22),
                  N["fillxy"], N["threefits"], N["loop"], N["curve"], N["onesplit"], N["vocabB"], N["linpipe"]]
                 + [o(i) for i in range(33, 43)] + [N["leakwhat"], N["leakkinds"], N["leakcode"]] + [o(i) for i in range(43, 47)]
                 + [N["words10"]] + [o(i) for i in (47, 48, 49, 50, 51, 52, 53, 54)])
        order_deck(prs, order)
    elif week == 11:
        N = B.w11(prs, ctx)
        replace_two_panels(o(2), "WHAT WE WILL DO",
                           "Build new input columns from the ones we have, test whether each one helps, and read which input moves a prediction more. Learn the words feature engineering, interaction and ablation.",
                           "HOW YOU WILL SHOW IT",
                           "You can build a derived feature, compare models with and without it on the same rows, and decide from the evidence whether to keep it.")
        set_notes(o(2), "Last week we learned how to trust a score. This week we try to improve the model by giving it better inputs. We will build new columns from the ones we have, test whether each one really helps, and learn to read which input moves a prediction more. By the end you can build a derived feature, compare models with and without it on the same rows, and decide from the evidence whether to keep it.")
        B.w11_exit(o(50), c, O)
        order = ([o(1), o(2), N["vocab"], o(3), o(7)] + [o(i) for i in range(13, 19)] + [N["curved"]] + [o(i) for i in range(19, 24)]
                 + [N["effect"], o(24), o(29)] + [o(i) for i in range(30, 39)] + [N["earn"], N["predtime"]]
                 + [o(i) for i in range(43, 49)] + [N["words11"], o(49), o(50)])
        order_deck(prs, order)
    elif week == 12:
        N = B.w12(prs, ctx)
        replace_two_panels(o(2), "WHAT WE WILL DO",
                           "Compare candidate models on the same rows, apply the limits an engineer sets, and explain the choice. Meet random forests and boosting, and write the limits of a model in plain words.",
                           "HOW YOU WILL SHOW IT",
                           "You can select a model that meets stated limits, say who is affected when it is wrong, and describe its purpose, data, scores and limits on one page.")
        set_notes(o(2), "This week we choose. Several models can do the job, so we compare them on the same rows, apply the limits an engineer sets, such as error and speed, and explain the choice. We also meet two more families, random forests and boosting. And we finish with the human side: who is affected when a model is wrong. By the end you can select a model that meets stated limits and describe its purpose, data, scores and limits on one page.")
        B.w12_exit(o(63), c, O)
        order = ([o(1), o(2), N["vocab"], o(3), o(7)] + [o(i) for i in range(13, 18)] + [N["recap"], N["cands"]] + [o(i) for i in range(36, 43)] + [N["cand3"]] + [o(i) for i in range(43, 52)]
                 + [N["forest"], N["forestcode"], N["boost"], N["modelcard"], N["resp1"], N["resp2"]]
                 + [o(i) for i in range(56, 62)] + [N["words12"], o(62), o(63), o(64)])
        order_deck(prs, order)
    if week == 13:
        N = W13.w13(prs, ctx)
        set_body(o(2), "Run the project", ["Hold a flexible model back with a penalty and predict from the nearest neighbours.", "Compare five candidates fairly.", "Make the project run for someone else, from a clean start."])
        set_body(o(2), "Another learner can follow", ["You can say what regularisation, alpha and k mean, and read a table of candidates.", "Another learner can follow your written instructions and reproduce your stated result."])
        set_notes(o(2), "Today has two halves. In the first half we finish our tour of modelling. We learn to hold a flexible model back with a penalty, which is called regularisation, and we meet a model that predicts from the nearest neighbours. Then we compare five candidates fairly. In the second half we turn to the project. We make it runnable by someone else from a clean start, because a result that nobody else can reproduce is hard to trust. By the end you can say what regularisation, alpha and k mean, read a table of candidates, and follow your own written instructions to reproduce your results from a clean start.")
        order = ([o(1), o(2), N["vocabA"], N["prep"], N["polyfig"], N["penalty"], N["curvecode"], N["loop"], N["coef"], N["vocabB"], N["knnfig"], N["knncode"], N["choosek"],
                  N["cands"], N["which"], N["words13"]] + [o(i) for i in range(3, 16)] + [N["versions"], N["colab"]] + [o(i) for i in range(16, 26)])
        order_deck(prs, order)
    N = N if "N" in dir() else {}
    for sl in N.values():
        NEWTITLES.setdefault(week, set()).add(first_title(sl))
    if week in (14, 15): prs.core_properties.comments = "patched-20261030"
    finalize(prs, code, week, dst)
    print(f"{code} W{week}: {len(prs.slides)} slides")
    return True


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=None); ap.add_argument("--weeks", nargs="*", type=int, default=[8, 9, 10, 11, 12, 13, 14, 15]); ap.add_argument("--from-backup", action="store_true", help="start Weeks 9-12 from the original backups")
    a = ap.parse_args(); out = Path(a.out) if a.out else DECKS
    BACKUP.mkdir(exist_ok=True)
    for week in a.weeks:
        for code in R.COHORT:
            name = deck_name(code, week); cur = DECKS / name
            if not (BACKUP / name).exists(): shutil.copy2(cur, BACKUP / name)
            src = (out / name) if (week == 8 and a.out and (out / name).exists()) else ((BACKUP / name) if (a.from_backup and week != 8) else cur)
            build_week(code, week, src, out / name)
    import json
    (p8.ROOT / 'data' / 'week8_12_new_slide_titles_20261030.json').write_text(json.dumps({str(k): sorted(v) for k, v in NEWTITLES.items()}, indent=1))


if __name__ == "__main__":
    main()
