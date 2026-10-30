"""Weeks 10, 11 and 12: validation and leakage, feature engineering, choosing a model."""
import numpy as np
import week_reference_numpy as R
import week_figs_20261030 as F
from deckkit_20261030 import *
from wk_8b_9_20261030 import num


def curve_rows(O, depths):
    cv = {d: (a, b) for d, a, b in O["overfit_curve"]}
    return [(d, cv[d][0], cv[d][1]) for d in depths]


# ================================================================== WEEK 10
def w10(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit = c["short"], c["unit"]; N = {}
    N["vocabA"] = table_slide(prs, "WORDS WE USE", "Words for today: fitting and fairness",
        ["Word", "Plain meaning", "Example from today"],
        [["Generalisation", "How well a model does on rows it has never seen.", "The validation error"],
         ["Underfitting", "The model is too simple and misses the pattern.", "A tree with one question"],
         ["Overfitting", "The model memorises the training rows, noise included.", "A tree with ten questions in a row"],
         ["Validation set", "Rows kept back to compare models and settings.", "Equipment E5"],
         ["Test set", "Rows opened once, at the very end.", "Equipment E6"],
         ["Hyperparameter", "A setting chosen before training.", "max_depth"]],
        [220, 420, 228],
        spoken("Six words that describe the central problem of machine learning. Generalisation is how well a model does on rows it has never seen. That is what matters most in practice, because nobody needs a prediction for a row whose answer they already have.",
               "Underfitting means the model is too simple and misses the pattern. Overfitting means the model has memorised the training rows, noise included, and does worse on new rows. The validation set is the group of rows we keep back to compare models and settings. The test set stays sealed until the very end. A hyperparameter is a setting we choose before training, such as the depth of a tree.",
               "Today we watch these words happen in our own data."), lab(), size=17)
    fills = ("X_train = training_data[feature_columns]\ny_train = training_data[\"target\"]\nX_valid = validation_data[feature_columns]\ny_valid = validation_data[\"target\"]\n"
             "fill_values = X_train.median()\nX_train_filled = X_train.fillna(fill_values)\nX_valid_filled = X_valid.fillna(fill_values)\nprint(X_train.shape, X_valid.shape)")
    N["fillxy"] = code_slide(prs, "WORKED EXAMPLE", "Preparing X and y, with a filled copy for tree experiments", fills, f"({O['n_tr']}, 2) ({O['n_va']}, 2)",
        ["X holds the input columns. y holds the answers. The raw X keeps its blanks for pipelines.", "median() is worked out from the training rows only.", "The filled copies put that same median into any blank, in both tables."],
        "The validation rows borrow the training median and never contribute to it.",
        spoken("We need two tables and two columns of answers for the experiments that follow. X train holds the inputs for the training rows. Y train holds their targets. X valid and y valid do the same for the validation rows. These raw tables keep their blanks, because a pipeline fills blanks by itself.",
               "Some of today's experiments use a tree on its own, and we want the blank filled before it sees the data. So we also make filled copies. Look at the line with median. The medians come from the training rows only. Then fill na puts those medians into any blank, in the training copy and in the validation copy. The validation rows borrow a number from the training rows and add nothing back.",
               f"The shape printout confirms the sizes: {O['n_tr']} training rows and {O['n_va']} validation rows, two feature columns each."), lab(), code_size=14, out_size=15)
    lp = ("from sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.linear_model import LinearRegression\nlinear_model = make_pipeline(\n    SimpleImputer(strategy=\"median\"),\n    LinearRegression(),\n)")
    N["linpipe"] = code_slide(prs, "WORKED EXAMPLE", "The Week 8 pipeline, ready to be scored on several folds", lp, "(nothing printed)",
        ["This is the Week 8 pipeline: fill blanks with the median, then fit a line.", "Nothing is fitted yet. The pipeline is a recipe.", "Each fold will fit a fresh copy of this recipe on its own training groups."],
        "A fresh median is learned inside every fold, so no fold borrows from its held-back group.",
        spoken("Cross-validation needs a model to score, so we bring back the pipeline from Week 8. It lists two steps: fill blanks with the median, then fit a straight line. Writing it does not train anything. It is a recipe.",
               "That detail matters for fairness. In each fold, scikit-learn fits a fresh copy of the recipe on that fold's training groups. The median is learned again inside every fold, so a held-back group never lends a number to its own score."), lab(), code_size=15, out_size=15)
    F.fig_three_fits(fd / "three_fits.png", code)
    N["threefits"] = figure_slide(prs, "A flexible model can memorise the training rows", fd / "three_fits.png",
        "Same dots, three trees. Depth 1 is too simple. Depth 12 chases every dot, noise included.",
        spoken(f"Here are the same training rows with three different trees. On the left the tree may ask only one question, so it draws a single step. It misses the rising pattern. We call that underfitting.",
               "On the right the tree may ask twelve questions in a row. Look how it jumps up and down to touch every dot. It has memorised the training rows, including their random wobble. That is overfitting. In the middle the tree is flexible enough to follow the trend and calm enough to ignore the wobble.",
               "Some books call the left problem bias, meaning too simple, and the right problem variance, meaning too jumpy. You will see those two words in other courses. In Semester 2 we add tools that hold a flexible model back."), lab())
    cr = curve_rows(O, [1, 4, 8])
    loop = ("from sklearn.tree import DecisionTreeRegressor\nfrom sklearn.metrics import mean_absolute_error\nprint(\"depth train valid\")\nfor depth in [1, 4, 8]:\n    tree = DecisionTreeRegressor(\n        max_depth=depth, random_state=17)\n    tree.fit(X_train_filled, y_train)\n"
            "    train_pred = tree.predict(X_train_filled)\n    valid_pred = tree.predict(X_valid_filled)\n    train_mae = mean_absolute_error(y_train, train_pred)\n    valid_mae = mean_absolute_error(y_valid, valid_pred)\n    print(depth, round(train_mae, 2), round(valid_mae, 2))")
    N["loop"] = code_slide(prs, "WORKED EXAMPLE", "Training error falls to almost zero, validation error stays far above it", loop,
        "depth train valid\n" + "\n".join(f"{d} {round(a, 2)} {round(b, 2)}" for d, a, b in cr),
        ["The loop tries three tree depths.", "mean_absolute_error(actual, predicted) is the MAE you computed by hand.", "We score the same tree twice: on rows it learned from, and on rows it never saw."],
        f"Errors are in {unit}. The deeper tree fits its training rows almost perfectly.",
        spoken("Now the numbers behind the picture. The loop trains three trees, with one, four and eight questions in a row allowed. For each tree we print two errors. The first is the error on the training rows the tree learned from. The second is the error on the validation rows it has never seen.",
               f"Read the output. The training error falls steadily, from {cr[0][1]:.2f} down to {cr[-1][1]:.2f}. The validation error falls much less, and it stays far above the training error; at depth eight it is {cr[-1][2]:.2f}. The gap between the two columns is the sign of overfitting.",
               "This is why we never report the training error as the result of a model. A model always looks good on rows it has already seen."), lab(), code_size=13, out_size=14)
    F.fig_overfit_curve(fd / "overfit_curve.png", code)
    N["curve"] = figure_slide(prs, "The gap between training and validation error is the warning sign", fd / "overfit_curve.png",
        "Depth 1 to 10, computed from this cohort's rows. The orange line is the honest score.",
        spoken("Here is the same experiment for every depth from one to ten. The dark line is the error on the training rows. It falls all the way to zero, because a deep tree can memorise every row. The orange line is the error on the validation rows. It falls, flattens, and then wobbles around the same level.",
               f"The orange line is the honest score. We choose the depth where it stops improving. The dark line reaching zero tells us nothing about new rows. Deeper trees past that point cost more to run and explain, and they deliver no gain. Fifteen rows from one machine give a rough warning, so we look at the overall shape of the two lines.",
               f"One more fact to notice. Even the best tree here is worse than the straight line from Week 8, which scored {O['reg']['linear']['mae']:.2f} {unit} on these same rows. A tree predicts the average of the training rows that land in each leaf, so it cannot continue a rising trend, and these rows rise in a nearly straight path."), lab())
    N["onesplit"] = idea_slide(prs, "ONE IDEA AT A TIME", "One validation group can mislead",
        [("THE PROBLEM", True), f"Our validation group, E5, has only {O['n_va']} rows. One odd machine or one lucky stretch of data can make a model look better or worse than it is."],
        [("THE REMEDY", True), "Score the model several times, each time holding back a different group. Report the average error and how far the scores spread. That is cross-validation."],
        spoken(f"Our validation group has only {O['n_va']} rows. That is a small sample. One odd machine, or one lucky stretch of data, can make a model look better or worse than it really is.",
               "The remedy is to score the model several times, each time holding back a different group of equipment. We then report the average error and how far the scores spread. That is cross-validation. The next slides show how scikit-learn does it, and why we keep whole equipment groups together."), lab())
    N["vocabB"] = table_slide(prs, "WORDS WE USE", "Words for today: repeated checks and leaks",
        ["Word", "Plain meaning", "Example from today"],
        [["Fold", "One turn of the repeated check: one group held back.", "Fold 1 holds back E1"],
         ["Cross-validation", "Scoring a model on several folds in turn.", "GroupKFold with 4 folds"],
         ["Spread", "How far the fold scores differ from each other.", "Standard deviation of fold errors"],
         ["Group split", "Whole equipment groups stay on one side.", "E1 to E4 train, E5 validate"],
         ["Data leakage", "Information from outside the training rows reaches the model.", "A copy of a validation row in training"]],
        [220, 420, 228],
        spoken("Five words for the second half of today. A fold is one turn of a repeated check, with one group of equipment held back. Cross-validation means scoring the model on several folds in turn. The spread tells us how far the fold scores differ from each other. A group split keeps whole equipment groups on one side, so one machine never sits on both sides of the line. Data leakage means information from outside the training rows reaches the model. We will meet leakage in detail after the cross-validation slides."), lab(), size=17)
    N["leakwhat"] = statement_slide(prs, "ONE IDEA AT A TIME", "Leakage makes a score look better than it is",
        "Data leakage: information the model should not have reaches the model during training.",
        [("Think of an exam. If the exam paper is on your desk the night before, a high mark proves nothing about what you learned.", False),
         ("A leaky score is a mark earned with the paper in hand. It looks wonderful and it fails in real use.", False),
         ("Leakage is common and quiet: the code runs, the score is high, and nothing warns you.", False)],
        spoken("Leakage is one of the most common serious mistakes in machine learning. Think of an exam. If the exam paper is on your desk the night before, a high mark proves nothing about what you learned. A leaky score is a mark earned with the paper in hand.",
               "What makes leakage dangerous is that it is quiet. The code runs. The score is high. Nothing warns you. Only a careful look at how the data was prepared reveals it. So we learn the four usual ways it happens, and a guard for each."), lab())
    F.fig_leak_kinds(fd / "leak_kinds.png")
    N["leakkinds"] = figure_slide(prs, "Four ways leakage happens, and a guard for each", fd / "leak_kinds.png",
        "Each guard is a habit you can apply while preparing the data.",
        spoken("Here are four ways leakage usually happens. One, copies across the split. The same observation sits in the training rows and again in the validation rows, for example a repeated record ID. Two, preparing before splitting. If you work out a median or a scale from all the rows, the validation rows have already influenced the model. Three, the same group on both sides. If rows from one machine sit in training and in the test, the model recognises the machine and the score is inflated. Four, a column that holds the answer. An input that is only known after the outcome, such as a repair record written after a fault.",
               "Each box has a guard. Remove repeated IDs. Fit imputers and scalers on the training rows only. Keep whole equipment groups together. Use only inputs that you will really have at the moment of prediction."), lab())
    leak = ("import pandas as pd\nleaky_X = pd.concat([X_train_filled, X_valid_filled])\nleaky_y = pd.concat([y_train, y_valid])\ntree = DecisionTreeRegressor(\n    max_depth=10, random_state=17)\ntree.fit(X_train_filled, y_train)\npred = tree.predict(X_valid_filled)\n"
            "print(\"honest\", round(mean_absolute_error(y_valid, pred), 2))\ntree.fit(leaky_X, leaky_y)\npred = tree.predict(X_valid_filled)\nprint(\"leaky \", round(mean_absolute_error(y_valid, pred), 2))")
    ld = O["leak_demo"]
    N["leakcode"] = code_slide(prs, "WORKED EXAMPLE", "A leaky score looks wonderful", leak, f"honest {round(ld['honest'], 2)}\nleaky  {round(ld['leaky'], 2)}",
        ["concat stacks two tables on top of each other.", "The first score is honest: the tree never saw the validation rows.", "The second score is leaky: we put the validation rows into training first."],
        f"Both scores are validation errors in {unit}. Only the second one is invalid.",
        spoken("Let us leak on purpose and watch what it does. First we score a deep tree honestly: it trains on the training rows and is scored on the validation rows.",
               f"Then we cheat. We stack the validation rows into the training table with concat, train again, and score on the same validation rows. The honest error is {ld['honest']:.2f} {unit}. The leaky error is {ld['leaky']:.2f}. A model that has the answers in front of it looks perfect.",
               "No warning appeared. That is why leakage is so dangerous, and why the habits on the previous slide matter."), lab(), code_size=14, out_size=16)
    N["words10"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Overfitting", "Memorising the training rows, noise included.", "Training error falls to near zero, validation error stays far above"],
         ["Underfitting", "A model too simple for the pattern.", "A tree with one question"],
         ["Generalisation", "Doing well on rows never seen.", "The validation error"],
         ["Cross-validation", "Scoring on several held-back groups in turn.", "GroupKFold, four folds"],
         ["Spread", "How far the fold scores differ.", "Standard deviation of fold errors"],
         ["Data leakage", "Information reaching the model that should not.", f"honest {ld['honest']:.2f}, leaky {ld['leaky']:.2f}"]],
        [220, 400, 248],
        spoken("Six words to keep. Overfitting is memorising the training rows, noise included. Underfitting is a model too simple for the pattern. Generalisation is doing well on rows never seen. Cross-validation scores the model on several held-back groups in turn, and the spread tells us how stable the result is. Data leakage is information reaching the model that should not. Notice that every one of these words is about trust. In the assignment you will build the group split and report errors that an engineer could rely on."), lab(), size=17)
    return N


def w10_exit(slide, c, O):
    n = replace_text(slide, "Explain each cleaning or modelling decision using your pandas table and its outputs.",
                     "Explain to a classmate how you would tell that a model is overfitting, and give one way leakage could creep into your own data preparation.")
    assert n >= 1


# ================================================================== WEEK 11
def w11(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit = c["short"], c["unit"]; N = {}
    N["vocab"] = table_slide(prs, "WORDS WE USE", "Words for today: making inputs more useful",
        ["Word", "Plain meaning", "Example from today"],
        [["Feature engineering", "Building new input columns from the columns you have.", "load_pct / 100"],
         ["Derived feature", "A column calculated from other columns.", "load_fraction"],
         ["Interaction", "A feature that multiplies two inputs.", "load_pct × ambient_c"],
         ["Scaling", "Putting inputs on a common ruler.", "StandardScaler (Week 9)"],
         ["Ablation", "Removing or adding one piece and comparing the scores.", "With and without load × ambient"],
         ["Available at prediction time", "An input you will really have when the model is used.", "Load now, not next month's repair log"]],
        [250, 380, 238],
        spoken("Six words for today. Feature engineering means building new input columns from the columns you already have. A derived feature is one column calculated from others, such as load divided by one hundred. An interaction multiplies two inputs together, for example load times ambient temperature. Scaling puts inputs on a common ruler, and you used it in Week 9. Ablation means adding or removing one piece and comparing the scores. Available at prediction time is the rule that every input must be something you will really have when the model is used.",
               "Today is where your engineering knowledge beats a better programmer. You know which combinations of measurements mean something physically."), lab(), size=17)
    ci = F.fig_curved_toy(fd / "curved_toy.png")
    N["curved"] = figure_slide(prs, "A straight line misses a curve, and a new feature repairs it", fd / "curved_toy.png",
        "Invented data. Adding x squared as a feature lets the same linear model follow the curve.",
        spoken(f"Why build new features at all? Here is an invented example. The dots follow a curve. On the left, a straight line through x misses the curve at both ends, and its MAE on these points is {ci['mae_line']:.2f}. On the right we gave the same linear model one extra input, x squared. That column is a derived feature. Now the fitted line bends with the dots and the MAE on the same points drops to {ci['mae_curve']:.2f}.",
               "The model type did not change. We changed what the model could see. That is feature engineering. In engineering data the useful new columns are often physical: a ratio, a product, a difference, a rate."), lab())
    lin = O["lin"]; sd = O["scaler"]["sd"]
    N["effect"] = table_slide(prs, "ONE IDEA AT A TIME", "Which input moves the prediction more?",
        ["Input", f"Slope ({unit} per unit)", "Typical spread (standard deviation)", f"Effect of one spread ({unit})"],
        [["load_pct", f"{lin['w_load']:.3f}", f"{sd[0]:.1f}", f"{lin['w_load'] * sd[0]:.1f}"],
         ["ambient_c", f"{lin['w_amb']:.3f}", f"{sd[1]:.1f}", f"{lin['w_amb'] * sd[1]:.1f}"]],
        [150, 220, 290, 208],
        spoken(f"The two slopes in our model are in different units, so comparing them directly is unfair. A slope of {lin['w_amb']:.2f} for ambient temperature looks bigger than {lin['w_load']:.2f} for load, yet the load swings over a far wider range.",
               "A fair comparison multiplies each slope by the typical spread of its input, the standard deviation. The result says how much the prediction changes when the input moves by one typical amount.",
               f"Here, one typical swing of load changes the prediction by {lin['w_load'] * sd[0]:.1f} {unit}, and one typical swing of ambient temperature changes it by {lin['w_amb'] * sd[1]:.1f} {unit}. Load matters more. This is how scaling helps us read a model, as well as train it."), lab(), size=19, row_h=58,
        below=["effect of one spread = slope × standard deviation", "Slopes come from the linear model fitted on the training rows. Spreads are the population standard deviation of the same rows, as StandardScaler calculates it."], below_size=19)
    ab = O["ablation"]
    chg = ab["extended"] - ab["base"]
    N["earn"] = statement_slide(prs, "ONE IDEA AT A TIME", "A feature earns its place only if it helps",
        f"Base error {ab['base']:.4f} {unit}. With load × ambient {ab['extended']:.4f} {unit}.",
        [(f"The extra feature changed the validation error by {chg:+.4f} {unit}." + (" The error went up." if chg > 0 else " The error went down."), False),
         ("A derived feature inherits the blanks of the columns it is built from. One training row has a blank ambient temperature, so its product is blank and the imputer fills it with a typical value.", False),
         ("With only 15 validation rows the comparison is rough. A feature that adds a column and gives no clear gain should be dropped. Keep the simpler model.", False)],
        spoken(f"Here is the honest result of the ablation on our own data. The base model, using load and ambient temperature, has a validation error of {ab['base']:.4f} {unit}. Adding the interaction, load times ambient, gives {ab['extended']:.4f}. The change is {chg:+.4f}." + (" The error went up, so the extra feature did not help." if chg > 0 else " The error went down, but only by a tiny amount."),
               "Why might the new column struggle? A derived feature inherits the blanks of the columns it comes from. One training row has a blank ambient temperature, so its product is blank as well, and the imputer fills it with a typical product that has nothing to do with that row. We built the product before filling the blank, and the order matters.",
               "We have only fifteen validation rows, so the comparison is rough, and a new feature also adds a column to maintain and one more thing that can go wrong. Our rule is that a feature earns its place only when the improvement is clear. Here it is not, so we keep the simpler model. That is a real engineering judgement, and it is the kind of reasoning that earns marks in your written evidence."), lab())
    N["predtime"] = idea_slide(prs, "ONE IDEA AT A TIME", "Use only inputs you will have at prediction time",
        [("ALLOWED", True), "Load now. Ambient temperature now. A value calculated from those two, such as load divided by 100.", "Anything the sensor could report at the moment the prediction is requested."],
        [("LEAKS THE ANSWER", True), "The measured target itself. A repair note written after the fault. A monthly average that includes next week.", "A feature like these makes training look wonderful and fails in service."],
        spoken("One rule applies to every feature you build. You must have it at the moment the prediction is requested. Load now and ambient temperature now are fine. A value calculated from those two, such as load divided by one hundred, is fine too.",
               "Be suspicious of anything that is known only afterwards: the measured target itself, a repair note written after a fault, or a monthly average that includes next week. These leak the answer. The model looks wonderful in training and fails in service. Last week's leakage guard number four is this rule."), lab())
    N["words11"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Feature engineering", "Building new inputs from existing columns.", "load_fraction, load × ambient"],
         ["Derived feature", "A column calculated from other columns.", "x squared in the curved example"],
         ["Interaction", "Two inputs multiplied together.", "load_pct × ambient_c"],
         ["Effect of one spread", "Slope times standard deviation, for a fair comparison.", f"load {lin['w_load'] * sd[0]:.1f}, ambient {lin['w_amb'] * sd[1]:.1f} {unit}"],
         ["Ablation", "Compare scores with and without one piece.", f"Error change {chg:+.4f} {unit}"],
         ["Prediction-time rule", "Use only inputs you will have when predicting.", "No repair notes written afterwards"]],
        [250, 380, 238],
        spoken("Six words to keep. Feature engineering builds new inputs from existing columns. A derived feature is one column calculated from others. An interaction multiplies two inputs. The effect of one spread, which is the slope times the standard deviation, lets us compare inputs fairly. Ablation compares scores with and without one piece. And the prediction time rule says to use only inputs you will have when you predict. In the assignment you build the features and run the ablation yourself."), lab(), size=17)
    return N


def w11_exit(slide, c, O):
    n = replace_text(slide, "Explain each cleaning or modelling decision using your pandas table and its outputs.",
                     "Explain to a classmate why load divided by 100 is a derived feature, how you would decide whether to keep a new feature, and why a repair note written after a fault cannot be an input.")
    assert n >= 1


# ================================================================== WEEK 12
def w12(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit, thing = c["short"], c["unit"], c["thing"]; N = {}
    r = O["reg"]
    N["vocab"] = table_slide(prs, "WORDS WE USE", "Words for today: choosing a model",
        ["Word", "Plain meaning", "Example from today"],
        [["Candidate", "A model being considered for the job.", "Baseline, line, tree"],
         ["Constraint", "A limit a model must meet to be allowed.", "MAE at most 10, latency at most 10 ms"],
         ["Latency", "The time one prediction takes.", "Milliseconds per row"],
         ["Ensemble", "Many models whose answers are combined.", "A forest of trees"],
         ["Random forest", "Many trees that vote or average, each seeing different rows.", "RandomForestRegressor"],
         ["Boosting", "Small models added one after another, each fixing the last one's mistakes.", "Named today, taught in Semester 2"]],
        [220, 440, 208],
        spoken("Six words for choosing a model. A candidate is a model being considered for the job. A constraint is a limit a candidate must meet before it is allowed, for example an error limit or a speed limit. Latency is the time one prediction takes. An ensemble is many models whose answers are combined. A random forest is an ensemble of many trees that each see different rows, and their answers are averaged. Boosting adds small models one after another, each one fixing the mistakes of the last. We only name boosting today, and we study it in Semester 2."), lab(), size=17)
    ok = lambda v: "yes" if v <= 10 else "no"
    rc = ("from sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_absolute_error\n"
          "X_train = training_data[feature_columns]\ny_train = training_data[\"target\"]\nX_valid = validation_data[feature_columns]\nlinear_model = make_pipeline(\n    SimpleImputer(strategy=\"median\"), LinearRegression())\n"
          "linear_model.fit(X_train, y_train)\nvalidation_predictions = linear_model.predict(X_valid)\nmae = mean_absolute_error(\n    validation_data[\"target\"], validation_predictions)\nprint(round(mae, 4))")
    N["recap"] = code_slide(prs, "WORKED EXAMPLE", "The Week 8 line, rebuilt in a few lines", rc, f"{round(r['linear']['mae'], 4)}",
        ["Every line repeats Week 8: split into X and y, fit the pipeline, predict, score.", "The names X_valid, linear_model and mae are used again in the next cells.", "The printed number is the validation MAE of the line."],
        "The same rows, the same pipeline, the same MAE as Week 8.",
        spoken("Choosing a model starts with having the candidates ready, so we rebuild the line from Week 8 in a few lines. We split the rows into X and y, fit the pipeline of an imputer and a line on the training rows, predict on the validation rows, and score the predictions with mean absolute error.",
               "Nothing here is new. We repeat it because the next cells reuse three names from it: X valid, linear model and mae. The number printed at the end is the validation MAE of the line. It is the same number that appears in the three-candidates table on the next slide."), lab(), code_size=13, out_size=16)
    N["cands"] = table_slide(prs, "ONE IDEA AT A TIME", "Three candidates on the same validation rows",
        ["Candidate", f"Validation MAE ({unit})", "Within the limit of 10?"],
        [["Baseline: training average", num(r["baseline"]["mae"]), ok(r["baseline"]["mae"])],
         ["Straight line", num(r["linear"]["mae"]), ok(r["linear"]["mae"])],
         ["Decision tree, depth 4", num(r["tree"]["mae"]), ok(r["tree"]["mae"])]],
        [420, 250, 198],
        spoken(f"Choosing a model means comparing candidates fairly. We score three of them on the same validation rows, so the comparison is fair. The average guess has an error of {r['baseline']['mae']:.2f} {unit}. The straight line has {r['linear']['mae']:.2f}. The tree has {r['tree']['mae']:.2f}.",
               "The right column applies one constraint from this week's classroom decision: error at most ten. Notice that error is only one of the things an engineer checks. The next slides add speed, and then the full selection rule."), lab(), size=21, row_h=56,
        below=["All three were scored on the same rows, in the same unit.", "Speed comes next: a candidate must also be fast enough."], below_size=19)
    N["cand3"] = table_slide(prs, "ONE IDEA AT A TIME", "The same recipe gives one row per candidate",
        ["name", "validation_mae", "latency_ms"],
        [["baseline", f"{r['baseline']['mae']:.2f}", "measure on your computer"], ["linear", f"{r['linear']['mae']:.2f}", "measure on your computer"], ["tree", f"{r['tree']['mae']:.2f}", "measure on your computer"]],
        [260, 280, 328],
        spoken("The table on the previous slide has one row, because we measured only the line. The recipe does not change for other candidates. Fit the candidate on the training rows, predict on the validation rows, score its mean absolute error, and time its predict call. Then add one row to the table.",
               f"Here is the table we aim for, with three rows. The error column comes from the same validation rows we used all term. The latency column depends on your computer and on the moment you run it, so we fill it in by measuring in the notebook. In the assignment, the candidate table is handed to you, and your job is to apply the limits and choose."), lab(), size=20, row_h=56,
        below=["Same recipe for every row: fit, predict, score the MAE, time the prediction.", "Latency depends on your computer, so each student measures it."], below_size=19)
    mean_forest = F.fig_forest(fd / "forest.png")
    N["forest"] = figure_slide(prs, "A random forest averages many trees", fd / "forest.png",
        "Illustrative numbers. Each tree sees different rows, and the forest averages their answers.",
        spoken("One tree can be jumpy. A random forest builds many trees, each trained on a different random sample of the rows, and averages their answers. In the picture, five trees give five different predictions. The forest reports their average. Averaging smooths out the jumpiness of any single tree.",
               "The numbers in this picture are invented to show the idea. In scikit-learn the class is called RandomForestRegressor, and it follows the same create, fit, predict pattern you already know. The setting n estimators is the number of trees. You will try it in the notebook, and you may find that on a clean straight pattern like ours the plain line is hard to beat. A forest earns its place when the pattern is curved or the inputs interact."), lab())
    N["forestcode"] = statement_slide(prs, "ONE IDEA AT A TIME", "A forest uses the same create, fit, predict pattern",
        ["RandomForestRegressor(", "    n_estimators=100,", "    random_state=17)"],
        [("n_estimators is the number of trees. random_state fixes the random choices so everyone gets the same forest.", False),
         ("Use it exactly like the other models: forest.fit(X_train, y_train), then forest.predict(X_valid).", False),
         ("Score it with the same MAE on the same validation rows, and compare it with the baseline and the line.", False)],
        spoken("Here is the whole forest in one line. N estimators is the number of trees, and random state fixes the random choices so everyone gets the same forest. After that it behaves like every model you have used. Fit on the training rows, predict on the validation rows, and score it with the same MAE.",
               "In the notebook, run it and put its error beside the baseline, the line and the tree. Fair comparison, same rows."), lab())
    F.fig_boosting(fd / "boosting.png")
    N["boost"] = figure_slide(prs, "Boosting adds small trees that fix what is still wrong", fd / "boosting.png",
        "Illustrative numbers. Named here and taught in Semester 2.",
        spoken("Gradient boosting is another way to combine trees. Instead of many trees averaging at once, it adds small trees one after another. Each new tree is trained to fix what the earlier ones still get wrong. In the picture, the first stage predicts seventy when the truth is eighty, so ten is still missing. The second stage moves the prediction to seventy-seven. The third moves it to seventy-nine point one.",
               "Boosting is behind many winning entries in data competitions, which is why we name it today. These numbers are invented. We study the real thing in Semester 2, after gradient descent, which you previewed in Week 8."), lab())
    N["modelcard"] = table_slide(prs, "ONE IDEA AT A TIME", "A model card puts the evidence on one page",
        ["Section", "The question it answers", "Example for our model"],
        [["Purpose", "What decision does the model support?", f"Warn when {short} may pass its limit"],
         ["Data", "What rows trained and tested it?", f"{O['n_clean']} clean synthetic rows, groups E1 to E6"],
         ["Scores", "How well does it do, beside a baseline?", f"Line MAE {r['linear']['mae']:.2f} {unit}; baseline {r['baseline']['mae']:.2f}"],
         ["Limits", "Where should it not be trusted?", "Other equipment, loads outside the data range"],
         ["Review", "Who checks it, and when?", "A named engineer, every term"]],
        [160, 340, 368],
        spoken("A model card is a one page note that travels with a model. It answers five questions. What decision does the model support? What rows trained and tested it? How well does it do, beside a baseline? Where should it not be trusted? Who checks it, and when?",
               "The example on the right is for the model we have built. Writing this card is excellent practice for the written evidence in your project, because it forces you to state the limits next to the score."), lab(), size=17)
    N["resp1"] = idea_slide(prs, "ONE IDEA AT A TIME", "Who is affected when a model is wrong",
        [("A MISSED ALERT (FALSE NEGATIVE)", True), f"Suppose an alert fires when the predicted {short} passes a limit we choose. If a real problem goes unwarned, equipment can be damaged and people nearby can be put at risk.", "Check that the training data looks like where the model will run. A new machine may behave differently from E1 to E4."],
        [("A FALSE ALARM (FALSE POSITIVE)", True), "Inspections are wasted, and operators learn to ignore the alerts. A model nobody trusts protects nobody.", "Choose the threshold with the people who live with the consequences."],
        spoken("Every model makes mistakes, and the mistakes land on someone. Suppose an alert fires when the predicted value passes a limit we choose. A missed alert means a real problem goes unwarned. Equipment can be damaged and people nearby can be put at risk. A false alarm wastes inspections, and operators who hear too many false alarms learn to ignore the alerts. A model nobody trusts protects nobody.",
               "Two habits follow. Choose the threshold together with the people who live with the consequences. And check that the training data looks like the place where the model will run. A new machine may behave differently from the ones we trained on, and a model trained on one fleet can fail on another."), lab())
    N["resp2"] = idea_slide(prs, "ONE IDEA AT A TIME", "Take care with data about people",
        [("MACHINE DATA", True), "Sensor readings from a motor, a building plant or a crusher carry little personal risk.", "Data about workers, drivers or customers is different. It can identify a person."],
        [("WHAT TO DO", True), "Uganda's Data Protection and Privacy Act, 2019 protects personal data. Collect only what you need, keep it safe, and say what it is used for.", "This is a summary for learning and is not legal advice."],
        spoken("Most of our data comes from machines, and machine data carries little personal risk. Data about workers, drivers or customers is different, because it can identify a person.",
               "Uganda's Data Protection and Privacy Act of 2019 protects personal data. The habits that follow are simple. Collect only what you need. Keep it safe. And say what it will be used for. This is a learning summary and is not legal advice, so for a real project, ask for qualified advice."), lab())
    N["words12"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Candidate", "A model being considered.", "Baseline, line, tree, forest"],
         ["Constraint", "A limit a model must meet.", "MAE and latency limits"],
         ["Random forest", "Many trees, answers averaged.", "RandomForestRegressor"],
         ["Boosting", "Small trees added to fix earlier mistakes.", "Semester 2"],
         ["Model card", "A one page record of purpose, data, scores and limits.", "Five sections"],
         ["False negative", "A missed alert.", "The costly mistake"]],
        [220, 400, 248],
        spoken("Six words to keep. A candidate is a model being considered. A constraint is a limit it must meet. A random forest averages many trees. Boosting adds small trees that fix earlier mistakes, and we study it in Semester 2. A model card records purpose, data, scores and limits on one page. A false negative is a missed alert, usually the costly mistake. In the assignment you apply the constraints and choose a model, and you explain the choice in your own words."), lab(), size=17)
    return N


def w12_exit(slide, c, O):
    n = replace_text(slide, "Explain each cleaning or modelling decision using your pandas table and its outputs.",
                     "Explain to a classmate how you would choose between two models, and name one limit you would write on a model card.")
    assert n >= 1
