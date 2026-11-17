"""Week 8b (explain-before-use additions) and Week 9 (classification) slides."""
import numpy as np
import week_reference_numpy as R
import week_figs_20261030 as F
from deckkit_20261030 import *


def num(x, n=2): return f"{x:.{n}f}"


# ================================================================== WEEK 8b
def w8b(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit = c["short"], c["unit"]
    N = {}
    b1, m1 = O["line_load_only"]["intercept"], O["line_load_only"]["slope"]
    lin = O["lin"]; p70 = b1 + m1 * 70
    N["line_eq"] = statement_slide(prs, "ONE IDEA AT A TIME", "The fitted line is an equation",
        f"predicted {short} = {b1:.1f} + {m1:.3f} × load_pct",
        [("A fit on load alone, to show the idea.", False), ("Intercept " + num(b1, 1) + ": the prediction when load is 0 percent.", False),
         (f"Slope {m1:.3f}: each extra 1 percent of load adds {m1:.3f} {unit} to the prediction.", False),
         (f"At 70 percent load the line predicts {p70:.1f} {unit}.", False),
         (f"With both inputs the model learns one slope for each: {lin['intercept']:.2f} + {lin['w_load']:.3f} × load_pct + {lin['w_amb']:.3f} × ambient_c. scikit-learn keeps these in intercept_ and coef_.", False)],
        spoken(f"We keep saying a line, so let us write it down. A straight line is an equation with two numbers. The first is the intercept, where the line starts. It is the prediction when the load is zero. The second is the slope. It says how much the prediction rises for every extra one percent of load.",
               f"For our training rows the computer found an intercept of {b1:.1f} and a slope of {m1:.3f}. So each extra percent of load adds about {m1:.2f} {unit} to the {short}. At seventy percent load the line predicts {p70:.1f} {unit}. You can check that on a calculator.",
               f"Our real model has two inputs, load and ambient temperature, so it learns one slope for each. Those numbers are on the right. scikit-learn keeps them in two places, intercept underscore and coef underscore. Remember this slide. When we say the model learned something, we mean it found numbers like these."), lab())
    rec = fig_info = F.fig_blanks(fd / "blanks.png", code)
    N["blanks"] = figure_slide(prs, "A model cannot learn from a blank, so we fill it first", fd / "blanks.png",
        "An imputer fills each blank with the median of the training rows. Median means the middle value.",
        spoken(f"Before a model can learn, every input needs a number. In our training rows one ambient temperature is blank. That is row {rec['record_id']} in the picture. A model cannot add up a blank, so we fill it.",
               f"The usual fill is the median, the middle value you met in Week 6. The tool that does the filling is called an imputer. That word just means a filler.",
               f"The important detail is where the median comes from. We work it out from the training rows only. Here it is {rec['med']:.2f}. We keep that number and reuse it for any blank in later rows. If we worked it out from the validation rows as well, the validation rows would leak a little information into the model, and the score would no longer be fair."), lab())
    F.fig_pipeline(fd / "pipeline.png")
    N["pipeline"] = figure_slide(prs, "A pipeline runs its steps in order", fd / "pipeline.png",
        "A pipeline is a short to-do list. Write it once, then call fit and predict on the whole list.",
        spoken("Now every row needs two jobs. First fill the blanks, then predict. A pipeline is a short to-do list that runs those jobs in order.",
               "We write the list once with make underscore pipeline. When we call fit, the pipeline learns the median and then learns the model, both from the training rows. When we call predict, it fills the blanks in the new rows using the median it already learned, and then makes the prediction.",
               "The benefit is safety. You cannot forget a step, and you cannot run the steps in the wrong order. In the next slides you will see the imputer and the model written as one pipeline."), lab())
    F.fig_tree(fd / "tree.png", code)
    N["tree"] = figure_slide(prs, "A decision tree asks yes or no questions", fd / "tree.png",
        "max_depth is a hyperparameter, a setting you choose before training. It limits how many questions in a row.",
        spoken(f"A decision tree is the second model we compare. It is a list of yes or no questions about the inputs. Read it from the top. Is the load at most {O['tree2_rules'][0].split('<=')[1].strip(' :')} percent? If yes, go left. Otherwise go right.",
               f"The boxes at the bottom are called leaves. Each leaf predicts the average {short} of the training rows that ended up there. This tree asks two questions in a row, so we say its depth is two.",
               "The depth is a setting we choose before training. A setting like that is called a hyperparameter. In the assignment the tree may ask four questions in a row, so max depth is four. The other setting you will see, random state, fixes the starting point for any random choice inside the algorithm. With the same random state, everyone in the room gets the same tree."), lab())
    r = O["reg"]
    sc_code = ("from sklearn.metrics import mean_absolute_error\nmodels = {\n    \"baseline\": baseline_model,\n    \"line\": linear_model,\n    \"tree\": tree_model,\n}\n"
               "for name, model in models.items():\n    predicted = model.predict(X_valid)\n    error = mean_absolute_error(y_valid, predicted)\n    print(name, round(error, 2))")
    N["scores"] = code_slide(prs, "WORKED EXAMPLE", "One MAE for each model on the validation rows", sc_code,
        f"baseline {r['baseline']['mae']:.2f}\nline {r['linear']['mae']:.2f}\ntree {r['tree']['mae']:.2f}",
        ["A dictionary pairs each name with a model we fitted earlier.", "items() gives one name and one model per turn of the loop.", "mean_absolute_error(actual, predicted) is the MAE from earlier slides."],
        f"The numbers are in {unit}. Each model predicts the same validation rows.",
        spoken("We now have three fitted models, so let us score them all in the same way. The dictionary pairs a short name with each model we fitted earlier. The loop takes one name and one model at a time. For each model we predict the validation rows, and then we score the predictions with mean absolute error, the MAE we calculated by hand.",
               f"Look at the three printed lines. Each one is the average miss of one model, in {unit}. They all use the same validation rows, so the comparison is fair."), lab(), code_size=14, out_size=15)
    N["results"] = table_slide(prs, "ONE IDEA AT A TIME", "Three models on the validation rows",
        ["Model", f"MAE ({unit})", f"RMSE ({unit})"],
        [["Average (baseline)", num(r["baseline"]["mae"]), num(r["baseline"]["rmse"])],
         ["Straight line", num(r["linear"]["mae"]), num(r["linear"]["rmse"])],
         ["Decision tree, depth 4", num(r["tree"]["mae"]), num(r["tree"]["rmse"])]],
        [420, 224, 224],
        spoken(f"Here is what everything we built today produces, on the validation rows that none of the models saw. The average guess misses by {r['baseline']['mae']:.2f} {unit} on average. The tree misses by {r['tree']['mae']:.2f}. The line misses by {r['linear']['mae']:.2f}.",
               "Look at the pattern. The line beats the tree by a wide margin. Remember the scatter plot: the dots follow a straight path, so a straight line is the right shape. A tree can only predict in steps, so it has to cut that path into rough pieces.",
               "A more complicated model earns its place only when the error falls. Always put the baseline beside the number, and let the simplest model that does the job win."), lab(), size=22, row_h=58,
        below=[(f"The line misses by about {r['linear']['mae']:.2f} {unit} on average. The average guess misses by {r['baseline']['mae']:.2f} {unit}.", True),
               "All three models used the same training rows and the same validation rows."], below_size=20)
    N["words8"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Baseline", "A simple guess every model must beat.", "The training average"],
         ["Error", "Actual value minus predicted value.", "Four misses, measured three ways"],
         ["MAE and RMSE", "Average size of the misses. RMSE punishes big misses more.", f"Both in {unit}"],
         ["Loss", "One number for how wrong a model is. Training lowers it.", "The bowl and the downhill walk"],
         ["Imputer and pipeline", "A filler for blanks, and a to-do list of steps.", "make_pipeline(imputer, model)"],
         ["Hyperparameter", "A setting chosen before training.", "max_depth = 4"]],
        [200, 420, 248],
        spoken("Let us gather today's new words in one place. A baseline is the simple guess every model must beat. An error is the actual value minus the predicted value. MAE is the average size of the misses, and RMSE is a similar score that punishes large misses more. Loss is the single number that training tries to lower. An imputer fills blanks, and a pipeline runs steps in order. A hyperparameter is a setting you choose before training, such as the depth of a tree.",
               "Keep this slide. Every one of these words returns in the next weeks."), lab(), size=17)
    return N


def w8b_exit(slide, c, O):
    n = replace_text(slide, "Explain each cleaning or modelling decision using your pandas table and its outputs.",
                     f"Explain to a classmate what a feature and a target are in today's data, why some rows stay hidden while a model learns, and what an error of {O['reg']['linear']['mae']:.2f} {c['unit']} tells you.")
    assert n >= 1


# ================================================================== WEEK 9
def w9(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit, limit = c["short"], c["unit"], c["limit"]
    k = O["cls_counts"]; N = {}
    all_no = 1 - k["tr_pos"] / k["tr_n"]
    lm, tm = O["logit_metrics"], O["tree_metrics"]; lc = O["logit_conf"]; tcn = O["tree_conf"]
    N["vocab1"] = table_slide(prs, "WORDS WE USE", "Words for today: the question",
        ["Word", "Plain meaning", "Example from today"],
        [["Class", "One of the possible answers.", "alert or no alert"],
         ["Label", "The correct class recorded for a row.", "The alert column we build"],
         ["Binary classification", "A classification with exactly two classes.", "alert (1) or no alert (0)"],
         ["Probability", "A number from 0 to 1 for how likely a class is.", "0.47 means 47 percent"],
         ["Threshold", "The probability at or above which the model says yes.", "0.5"]],
        [210, 420, 238],
        spoken("Five words for the question we ask today. A class is one of the possible answers, such as alert or no alert. A label is the correct class that has been recorded for a row. When there are exactly two classes we call the job binary classification. A probability is a number from zero to one that says how likely a class is. Zero point four seven means forty-seven percent. A threshold is the probability at or above which the model says yes. We will start with zero point five and then move it."), lab(), size=17)
    F.fig_cls_vs_reg(fd / "cls_vs_reg.png", code)
    N["cvr"] = figure_slide(prs, "Classification turns a number into a yes or no", fd / "cls_vs_reg.png",
        "Same dots. On the left we predict the number. On the right we predict which side of the limit it falls on.",
        spoken(f"In Week 8 we predicted a number, the {short}. Today the question changes. Engineers often care about a decision. Do we raise an alert or not?",
               f"So we draw a limit line. Here it is {limit:g} {unit}. A row at or above the line gets the label alert, written as one. A row below the line gets no alert, written as zero. The dots are the same dots. Only the question changed.",
               f"When the answer is one of a few classes, the job is called classification. With exactly two classes it is binary classification. The limit of {limit:g} {unit} is a teaching assumption for this course. It is a convenient line to practise on and is not a real safe operating limit."), lab())
    code_lab = ("import pandas as pd\nraw = pd.read_csv(\"engineering_data.csv\")\ndata = raw.drop_duplicates(\"record_id\")\n"
                "has_target = data[\"target\"].notna()\nvalid_load = data[\"load_pct\"].between(0, 100)\ndata = data[has_target & valid_load].copy()\n"
                f"data[\"alert\"] = (data[\"target\"] >= {limit}).astype(int)\ngroups = [\"E1\", \"E2\", \"E3\", \"E4\"]\ntrain = data[data[\"equipment_id\"].isin(groups)]\n"
                "print(len(train), train[\"alert\"].sum())\nprint(train[\"alert\"].value_counts().to_dict())")
    no = k["tr_n"] - k["tr_pos"]
    vc = {0: no, 1: k["tr_pos"]}; vc = dict(sorted(vc.items(), key=lambda kv: -kv[1]))
    N["label_code"] = code_slide(prs, "WORKED EXAMPLE", "Building the alert label", code_lab, f"{k['tr_n']} {k['tr_pos']}\n{vc}",
        ["The first six lines repeat Week 8: read, drop copies, keep valid rows.", f">= compares each target with the limit, {limit} {unit}. The answer is True or False.",
         ".astype(int) turns True and False into 1 and 0. The training rows are E1 to E4.", "sum() adds the ones, so it counts the alerts in the training rows."],
        f"The limit is {limit} {unit}, a teaching assumption. The counts use the training rows only.",
        spoken("Here is the label in code. The first six lines repeat what we did in Week 8: read the file, drop repeated record IDs, and keep the rows that have a recorded target and a valid load.",
               f"The next line builds the column. It compares each target with the limit and gets True or False for every row. As type int turns True into one and False into zero. That new column is the label. Then we pick out the training rows, the equipment groups E1 to E4, and we count only those. The last test group stays sealed.",
               f"The last two lines count. We have {k['tr_n']} training rows and {k['tr_pos']} of them are alerts. Value counts shows the same thing as a dictionary: {no} rows with no alert and {k['tr_pos']} with an alert."), lab(), code_size=14, out_size=15)
    ac = F.fig_counts(fd / "counts.png", code)
    N["counts"] = figure_slide(prs, f"A model that always says no scores {ac['acc'] * 100:.0f} percent", fd / "counts.png",
        "Most rows are no alert, so a model that never raises an alert still looks accurate.",
        spoken("Look at the two bars. Most rows are no alert. Now picture a model that does nothing except say no alert for every row.",
               f"Its accuracy is the share of rows it answers correctly. On our {ac['n']} training rows it would be right on {ac['no']} of them. That is {ac['acc'] * 100:.0f} percent. It has found zero alerts, and the alerts were the whole point of building the model.",
               "This is the accuracy trap. When one class is much more common than the other, accuracy looks good for a model that has learned nothing. The rest of today gives us better scores: precision, recall and F1. First we need a model that produces probabilities."), lab())
    sg = F.fig_sigmoid(fd / "sigmoid.png", code)
    N["sigmoid"] = figure_slide(prs, "Logistic regression turns a line into a probability", fd / "sigmoid.png",
        "The curve gives a probability between 0 and 1 for every load. Higher load, higher probability of an alert.",
        spoken("To answer yes or no, a model first produces a probability. Logistic regression does this. It starts from the same kind of straight line you already know, then bends it into an S shape so the answer always stays between zero and one.",
               f"Read the picture. At twenty percent load the curve sits near zero, so an alert is very unlikely. The curve crosses one half at a load of about {sg['cross']:.0f} percent. At ninety percent load the probability of an alert is about {sg['p90']:.1f}. The dots are the {sg['n']} training rows.",
               "The name has regression in it for historical reasons. The job is classification, because the answer is a class. This curve uses load alone so that we can draw it. The model on the next slides uses load and ambient temperature together."), lab())
    sc = O["scaler"]; rows = O["scaling_rows"]
    N["scaling"] = table_slide(prs, "ONE IDEA AT A TIME", "Features on different scales need a common ruler",
        ["Row", "load_pct", "ambient_c", "load_pct scaled", "ambient_c scaled"],
        [[i + 1, f"{a:g}", f"{b:g}", f"{x:.2f}", f"{y:.2f}"] for i, (a, b, x, y) in enumerate(rows)],
        [90, 160, 160, 230, 228],
        spoken(f"In our training rows, load runs from about {O['ranges']['load'][0]:.0f} to {O['ranges']['load'][1]:.0f}, and ambient temperature runs from about {O['ranges']['amb'][0]:.0f} to {O['ranges']['amb'][1]:.0f}. Some models, logistic regression among them, work better when the inputs share a common scale.",
               f"Scaling gives every feature the same ruler. For each value we subtract the training mean and divide by the training standard deviation. The standard deviation is the typical distance from the mean. After scaling, zero means average and one means one standard deviation above average.",
               f"Look at the first row. Its load is {rows[0][0]:g}. The training mean is {sc['mu'][0]:.1f}, so the scaled load is {rows[0][2]:.2f}, almost exactly average. Its ambient temperature of {rows[0][1]:g} is above the mean of {sc['mu'][1]:.1f}, so it scales to {rows[0][3]:.2f}.",
               "The tool is called StandardScaler. It learns the mean and the spread from the training rows during fit, the same way the imputer learned the median. Decision trees do not need scaling, because they only ask whether a value is above or below a cut."), lab(), size=20, row_h=52,
        below=[(f"scaled value = (value − mean) ÷ standard deviation", True),
               f"Training mean and standard deviation: load_pct {sc['mu'][0]:.1f} and {sc['sd'][0]:.1f}; ambient_c {sc['mu'][1]:.1f} and {sc['sd'][1]:.1f}.",
               "StandardScaler learns these from the training rows only."], below_size=19)
    N["split"] = code_slide(prs, "WORKED EXAMPLE", "Splitting the rows and choosing features",
        "valid = data[data[\"equipment_id\"] == \"E5\"]\nfeatures = [\"load_pct\", \"ambient_c\"]\nX_train, y_train = train[features], train[\"alert\"]\nX_valid, y_valid = valid[features], valid[\"alert\"]\nprint(len(train), len(valid))",
        f"{O['n_tr']} {O['n_va']}",
        ["train was built on the last slide from groups E1 to E4. E5 validates. E6 stays sealed.", "X holds the input columns. y holds the answers.", "This time the answer column is alert."],
        "X is a table of features. y is the column of answers.",
        spoken(f"The split is the one from Week 8. Equipment E1 to E4 are the training rows, which we picked out on the last slide. Here we add E5, the validation group. E6 stays sealed for the final test.",
               "X holds the input columns, load and ambient temperature. y holds the answers. The difference from Week 8 is that the answer column is now alert, zero or one, instead of a temperature.",
               f"The print shows {O['n_tr']} training rows and {O['n_va']} validation rows."), lab(), code_size=15, out_size=15)
    fit_code = ("from sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\n"
                "model = make_pipeline(\n    SimpleImputer(strategy=\"median\"),\n    StandardScaler(),\n    LogisticRegression(),\n)\nmodel.fit(X_train, y_train)\n"
                "probability = model.predict_proba(X_valid)[:, 1]\nprint(probability[:5].round(3))\nprint(y_valid.to_list()[:5])")
    p5 = np.round(np.array(O["logit"]["proba_first5"]), 3)
    out_fit = f"{p5}\n{O['logit']['actual_first5']}"
    a5 = O["logit"]["actual_first5"]; idx = a5.index(1) if 1 in a5 else None
    N["fit"] = code_slide(prs, "WORKED EXAMPLE", "Fitting a classifier and reading its probabilities", fit_code, out_fit,
        ["make_pipeline lists the steps in order: fill blanks, scale, classify.", "predict_proba returns two columns: the chance of class 0 and of class 1.",
         "[:, 1] keeps the second column, the probability of an alert.", "[:5] shows the first five validation rows."],
        "fit learns from the training rows. predict_proba answers for rows the model has not seen.",
        spoken("Now the model itself. We list three steps in a pipeline: fill blanks with the median, scale the features, then fit logistic regression. The pipeline learns everything it needs from the training rows when we call fit.",
               "Then we call predict underscore proba. It returns two columns for every row. The first is the chance of class zero. The second is the chance of class one, an alert. The square brackets with a colon and a one keep the second column.",
               f"We print the probabilities for the first five validation rows, and below them the true labels. " + (f"Look at row {idx + 1}. It really was an alert, and the model gave it a probability of {p5[idx]:.2f}. That is the model's honest uncertainty." if idx is not None else "") ), lab(), code_size=13, out_size=14)
    pr = np.array(O["logit"]["proba_first5"]); dec = (pr >= 0.5).astype(int)
    N["thr"] = table_slide(prs, "ONE IDEA AT A TIME", "A threshold turns a probability into a decision",
        ["Validation row", "Probability of alert", "Decision at 0.5", "Actual alert", "Correct?"],
        [[i + 1, f"{pr[i]:.3f}", "alert" if dec[i] else "no alert", "alert" if a5[i] else "no alert", "yes" if dec[i] == a5[i] else "no"] for i in range(5)],
        [140, 210, 200, 170, 148],
        spoken("A probability is not yet a decision. To decide we pick a threshold. If the probability is at or above the threshold, the model says alert. Otherwise it says no alert. We start with a threshold of zero point five.",
               "Read the table row by row. The first column is the probability. The second is the decision that follows from the threshold. The third is what really happened. The last column checks the decision.",
               "A threshold is a choice, and we are free to move it. We will do that in a few minutes and watch what changes."), lab(), size=19, row_h=50,
        below=[("decision = alert when probability ≥ 0.5, otherwise no alert", True), "Lowering the threshold raises more alerts. Raising it raises fewer."], below_size=19)
    N["vocab2"] = table_slide(prs, "WORDS WE USE", "Words for scoring the answers",
        ["Word", "Plain meaning", "Example from today"],
        [["Positive and negative", "Positive is the class we look for. Negative is the other class.", "Positive = alert"],
         ["True positive (TP)", "The model said alert, and it was an alert.", "Alert raised, limit really passed"],
         ["False positive (FP)", "The model said alert, but it was not. A false alarm.", "Alert raised, nothing wrong"],
         ["False negative (FN)", "The model said no alert, but it was one. A missed alert.", "Limit passed, no alert raised"],
         ["True negative (TN)", "The model said no alert, and it was no alert.", "Quiet and correct"],
         ["Confusion matrix", "A 2 by 2 table of the four counts.", "Next slides"]],
        [220, 420, 228],
        spoken("Before we score anything, six words. In a yes or no problem, positive means the class we are looking for. Here, positive is an alert. Negative is the other class.",
               "Now the four outcomes. A true positive means the model said alert and it was an alert. A false positive means the model said alert but nothing was wrong. That is a false alarm. A false negative means the model said no alert but the limit really was passed. That is a missed alert, and in engineering it is often the costly one. A true negative means the model said no alert and all was well.",
               "Put the four counts in a two by two table and you have a confusion matrix. We will build one by hand from a small file first, and then read the matrix for our own model."), lab(), size=17)
    F.fig_confusion(fd / "confusion.png", code, lc)
    N["modelconf"] = figure_slide(prs, "The confusion matrix of our model on the validation rows", fd / "confusion.png",
        f"{O['n_va']} validation rows. Accuracy {lm['accuracy'] * 100:.0f} percent, precision {lm['precision']:.2f}, recall {lm['recall']:.2f}.",
        spoken(f"Here is the confusion matrix for our model. The rows are what really happened. The columns are what the model said.",
               f"Of the {k['va_pos']} real alerts in the validation rows, the model caught {lc['tp']} and missed {lc['fn']}. Of the {k['va_n'] - k['va_pos']} quiet rows, it raised {lc['fp']} false alarms and answered {lc['tn']} correctly.",
               f"That gives an accuracy of {lm['accuracy'] * 100:.0f} percent, a precision of {lm['precision']:.2f} and a recall of {lm['recall']:.2f}. One caution. There are only {k['va_pos']} real alerts in the validation rows, so a single missed alert moves recall a long way. Treat these numbers as an illustration and judge the model on more data in later weeks."), lab())
    N["f1"] = statement_slide(prs, "ONE IDEA AT A TIME", "F1 combines precision and recall in one number",
        "F1 = 2 × precision × recall ÷ (precision + recall)",
        [(f"F1 is high only when precision and recall are both high.", False),
         (f"Our model: precision {lm['precision']:.2f}, recall {lm['recall']:.2f}, F1 {lm['f1']:.2f}.", False),
         ("A model that never raises an alert has recall 0, so its F1 is 0, even though its accuracy looked high.", False)],
        spoken("Precision and recall pull in different directions, so people often want one number that reflects both. That number is F1. It is a kind of average that is high only when precision and recall are both high.",
               f"For our model, precision is {lm['precision']:.2f} and recall is {lm['recall']:.2f}. The formula gives an F1 of {lm['f1']:.2f}.",
               "Remember the model that always says no alert. Its recall is zero because it finds none of the real alerts. So its F1 is zero, even though its accuracy was high. F1 exposes what accuracy hid."), lab())
    th = O["thresholds"]
    N["thresholds"] = table_slide(prs, "ONE IDEA AT A TIME", "Moving the threshold trades false alarms for missed alerts",
        ["Threshold", "TP", "FP", "FN", "Precision", "Recall"],
        [[f"{t['th']}", t["tp"], t["fp"], t["fn"], f"{t['precision']:.2f}", f"{t['recall']:.2f}"] for t in th],
        [180, 120, 120, 120, 164, 164],
        spoken("Now we move the threshold and watch the counts. A low threshold makes the model say alert more often, so we can catch more of the real alerts, and in most data we also pay with more false alarms. A high threshold does the opposite.",
               f"Here is what our small sample shows. At a threshold of {th[0]['th']} the model catches {th[0]['tp']} of the {k['va_pos']} real alerts and raises {th[0]['fp']} {'false alarm' if th[0]['fp'] == 1 else 'false alarms'}. At {th[1]['th']} it catches {th[1]['tp']} and raises {th[1]['fp']}. At {th[2]['th']} it catches {th[2]['tp']} and raises {th[2]['fp']}. The trade is easy to see in the TP and FP columns, and in the precision and recall columns built from them.",
               f"There is no threshold that is best for everybody. The right setting depends on the cost of each mistake. In this week's assignment a missed alert costs five units and a false alarm costs one, so a low threshold is attractive. For a different machine the costs could reverse. Only {k['va_pos']} real alerts sit in the validation rows, so the exact numbers will move with more data."), lab(), size=20, row_h=52,
        below=["Lower threshold: more alerts, more false alarms, fewer misses.", "Higher threshold: fewer alerts, fewer false alarms, more misses.", "Choose the threshold from the cost of each mistake."], below_size=19)
    F.fig_roc(fd / "roc.png", code)
    N["roc"] = figure_slide(prs, "The ROC curve shows every threshold at once", fd / "roc.png",
        f"Each point is one threshold. AUC is {O['auc']:.2f} here. 1.00 is a perfect ranking and 0.50 is guessing.",
        spoken("What if we want to judge the model without choosing one threshold? The ROC curve does that. Every point on the curve is one threshold. The horizontal axis is the false alarm rate, which is the share of quiet rows that raised an alert: false positives divided by false positives plus true negatives. The vertical axis is the detection rate, which is recall.",
               "A model that is only guessing follows the dashed diagonal. A good model climbs quickly toward the top left corner. The area under the curve is called AUC. It has a friendly meaning: pick one real alert and one quiet row at random, and AUC is the chance that the model gives the alert the higher probability.",
               f"Our AUC is {O['auc']:.2f}. With only {k['va_pos']} real alerts in the validation rows, a very high AUC is easy to reach, so treat it lightly. We introduce the curve now because you will meet it in every machine learning report."), lab())
    N["treeclf"] = idea_slide(prs, "ONE IDEA AT A TIME", "A decision tree can answer yes or no too",
        [("SAME IDEA AS WEEK 8", True), "A tree asks yes or no questions about the inputs. For a classifier, each leaf holds the share of alerts among the training rows that end there, and the tree answers with the majority.", "In scikit-learn: DecisionTreeClassifier(max_depth=3, random_state=17)."],
        [("ON THE VALIDATION ROWS", True), f"Tree: TP {tcn['tp']}, FP {tcn['fp']}, FN {tcn['fn']}, TN {tcn['tn']}. Precision {tm['precision']:.2f}, recall {tm['recall']:.2f}, F1 {tm['f1']:.2f}.", f"Logistic regression: TP {lc['tp']}, FP {lc['fp']}, FN {lc['fn']}, TN {lc['tn']}. Precision {lm['precision']:.2f}, recall {lm['recall']:.2f}, F1 {lm['f1']:.2f}."],
        spoken("The tree you met in Week 8 can answer yes or no questions as well. It asks the same kind of questions about the inputs. In a classifier each leaf holds the share of alerts among the training rows that end there, and the tree answers with the majority.",
               f"On the right are the scores for a tree of depth three on the same rows, beside the scores for logistic regression. The tree has {tcn['tp']} true positives, {tcn['fp']} {'false positive' if tcn['fp'] == 1 else 'false positives'} and {tcn['fn']} {'false negative' if tcn['fn'] == 1 else 'false negatives'}. The two blocks have the same four counts in the same order, so we read the counts first and then the three scores.",
               "With fifteen validation rows the two models are hard to separate. In Week 10 we learn how to compare models more fairly, using several splits."), lab())
    N["words9"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Accuracy", "Share of rows answered correctly.", f"{all_no * 100:.0f} percent for a model that never alerts"],
         ["Precision", "Of the alerts raised, the share that were real.", "TP ÷ (TP + FP)"],
         ["Recall", "Of the real alerts, the share that were found.", "TP ÷ (TP + FN)"],
         ["F1", "One number that is high only when both are high.", f"{lm['f1']:.2f} for our model"],
         ["ROC curve and AUC", "Performance at every threshold, and the area under it.", f"AUC {O['auc']:.2f}"],
         ["Class imbalance", "One class is much more common than the other.", f"{no} no alert, {k['tr_pos']} alert (training rows)"]],
        [230, 400, 238],
        spoken("Six words to take away. Accuracy is the share of rows answered correctly, and it can mislead when one class dominates. Precision asks, of the alerts we raised, how many were real. Recall asks, of the real alerts, how many did we find. F1 combines the two. The ROC curve shows performance at every threshold, and AUC is the area under it. Class imbalance means one class is much more common than the other.",
               "In the assignment you will compute the four counts, precision, recall and the cost. You now know what each of those words means."), lab(), size=17)
    return N


def w9_exit(slide, c, O):
    k = O["cls_counts"]; all_no = 1 - k["tr_pos"] / k["tr_n"]
    n = replace_text(slide, "Explain each cleaning or modelling decision using your pandas table and its outputs.",
                     f"Explain to a classmate why a model that never raises an alert can score {all_no * 100:.0f} percent, and what a missed alert costs in your engineering field.")
    assert n >= 1
