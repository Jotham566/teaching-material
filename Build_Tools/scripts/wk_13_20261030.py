"""Week 13: regularisation and nearest neighbours, followed by the existing reproducibility slides."""
import numpy as np
import week_reference_numpy as R
import week_figs_20261030 as F
from deckkit_20261030 import *
from wk_8b_9_20261030 import num


def w13(prs, ctx):
    code, c, O, fd, lab = ctx["code"], ctx["c"], ctx["O"], ctx["figdir"], ctx["lab"]
    short, unit = c["short"], c["unit"]; N = {}; B = R.bundle13(code); rr = B["ridge_rows"]; kn = B["knn"]; reg = O["reg"]
    N["vocabA"] = table_slide(prs, "WORDS WE USE", "Words for today: holding a model back",
        ["Word", "Plain meaning", "Example from today"],
        [["Regularisation", "Holding a model back so that it cannot chase noise.", "Ridge regression"],
         ["Penalty", "An extra cost added to the loss for large coefficients.", "alpha × sum of squared coefficients"],
         ["Ridge regression", "A line or curve fitted with a penalty on its coefficients.", "Ridge(alpha=1)"],
         ["alpha", "How strong the penalty is. A larger alpha shrinks the coefficients toward zero. A hyperparameter.", "0, 1 or 100"],
         ["Polynomial feature", "A power of an input, such as load squared.", "load, load², load³ and so on"],
         ["Lasso", "A cousin of ridge that can set some coefficients to exactly zero.", "Named only"]],
        [220, 420, 228],
        spoken("Six words for the first half of today. Regularisation means holding a model back, so that it cannot chase every wobble in the training rows. The usual way is a penalty, an extra cost added to the loss whenever the coefficients get large. Ridge regression is a line or a curve fitted with exactly that kind of penalty. The setting alpha says how strong the penalty is, and, like the depth of a tree, it is a hyperparameter that we choose before training.",
               "A polynomial feature is a power of an input, such as load squared or load cubed. Adding powers gives a straight-line method room to bend, and a flexible curve often needs holding back. Lasso is a cousin of ridge that can push some coefficients all the way to zero. We only name it today."), lab(), size=17)
    prep = ("import pandas as pd\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.metrics import mean_absolute_error\nraw = pd.read_csv(\"engineering_data.csv\")\ndata = raw.drop_duplicates(\"record_id\")\n"
            "data = data[data[\"target\"].notna()\n            & data[\"load_pct\"].between(0, 100)].copy()\ngroups = [\"E1\", \"E2\", \"E3\", \"E4\"]\ntrain = data[data[\"equipment_id\"].isin(groups)]\nvalid = data[data[\"equipment_id\"] == \"E5\"]\n"
            "features = [\"load_pct\", \"ambient_c\"]\nX_train, y_train = train[features], train[\"target\"]\nX_valid, y_valid = valid[features], valid[\"target\"]\nprint(len(train), len(valid))")
    N["prep"] = code_slide(prs, "WORKED EXAMPLE", "Preparing the rows once more", prep, f"{O['n_tr']} {O['n_va']}",
        ["The same cleaning as Weeks 8 to 12: drop copies, keep valid rows.", "E1 to E4 train, E5 validates, E6 stays sealed.", "X holds the two inputs. y holds the target."],
        "Every experiment today uses these four tables.",
        spoken("Before the experiments, we set up the same tables as in the last weeks. We read the file, drop repeated record IDs, and keep the rows that have a target and a valid load. Then we pick out the training rows, the equipment groups E1 to E4, and the validation rows, which are E5. The last group, E6, stays sealed.",
               f"X holds the two inputs, load and ambient temperature. Y holds the target, which here is {short}. The last line prints the sizes: {O['n_tr']} training rows and {O['n_va']} validation rows. Every experiment today uses these four tables."), lab(), code_size=13, out_size=15)
    F.fig_poly_ridge(fd / "poly_ridge.png", code)
    N["polyfig"] = figure_slide(prs, "A flexible curve can chase the training rows, and a penalty calms it", fd / "poly_ridge.png",
        f"Same degree-{B['degree']} curve on load alone. Left: no penalty. Right: penalty alpha = 1.",
        spoken(f"Here is a curve built from the powers of load, up to load to the power of {B['degree']}. That gives a straight-line method a lot of room to bend. On the left there is no penalty, so the curve is free to chase the training rows, the dark dots. On the right we add a penalty with alpha equal to one, and the curve calms down.",
               "The orange diamonds are the validation rows. They are the honest test of each curve, because neither curve has seen them. Notice that the penalised curve is smoother, and that its error on the training rows is slightly larger than the free curve's error. We accept a slightly worse fit to the training rows in exchange for a more stable model."), lab())
    N["penalty"] = statement_slide(prs, "ONE IDEA AT A TIME", "Ridge adds a price for large coefficients",
        ["loss = sum of squared misses", "+ alpha × (sum of squared coefficients)"],
        [("alpha = 0 means no penalty. The method is ordinary least squares.", False),
         ("A larger alpha shrinks the coefficients toward zero and calms the curve.", False),
         ("We choose alpha with the validation rows, in the way that we chose tree depth.", False),
         ("The penalty treats all coefficients alike, so the inputs are scaled first. That is why StandardScaler sits in the pipeline.", False)],
        spoken("Here is the whole idea in one line. Training lowers a loss, and the loss we know is built from the squared misses. In scikit-learn's Ridge we add up the squared misses over all the training rows. Ridge then adds a second part: alpha times the sum of the squared coefficients. A model can now lower its loss in two ways, by fitting the data better, or by making its coefficients smaller. The starting level of the line, the intercept, is left out of the penalty.",
               "When alpha is zero there is no penalty, and we are back to ordinary least squares. A larger alpha pushes the coefficients toward zero and calms the curve. We choose alpha the same way we chose the depth of a tree, by looking at the validation rows.",
               "One practical detail. The penalty adds up the squares of all coefficients and treats them alike, so the inputs must be on a common ruler first. That is the reason StandardScaler appears in the pipeline on the next slide."), lab())
    curve_code = ("from sklearn.preprocessing import (\n    PolynomialFeatures, StandardScaler)\nfrom sklearn.linear_model import LinearRegression, Ridge\ndef curve_model(estimator):\n    return make_pipeline(\n        PolynomialFeatures(6, include_bias=False),\n        StandardScaler(), estimator)\n"
                  "models = {\n    \"none\": curve_model(LinearRegression()),\n    \"alpha 1\": curve_model(Ridge(alpha=1)),\n    \"alpha 100\": curve_model(Ridge(alpha=100)),\n}")
    N["curvecode"] = code_slide(prs, "WORKED EXAMPLE", "Three curve models that differ only in the penalty", curve_code, "(nothing printed)",
        ["PolynomialFeatures(6) adds load squared up to load to the power of 6.", "StandardScaler puts those columns on a common ruler.", "The last step is the estimator: no penalty, alpha 1 or alpha 100."],
        "A dictionary keeps the three models side by side. Nothing is fitted yet.",
        spoken("Now the code. The function curve model builds one pipeline from three steps. The first step, PolynomialFeatures with six, adds the powers of the input: load, load squared, up to load to the power of six. The second step, StandardScaler, puts those columns on a common ruler. The third step is the estimator we pass in.",
               "The dictionary below keeps three versions side by side. The first uses LinearRegression, which has no penalty. The second uses Ridge with alpha equal to one. The third uses Ridge with alpha equal to one hundred. Nothing is fitted yet. The pipelines are recipes."), lab(), code_size=14, out_size=15)
    loop = ("load_train = X_train[[\"load_pct\"]]\nload_valid = X_valid[[\"load_pct\"]]\nprint(\"model train valid\")\nfor name, model in models.items():\n    model.fit(load_train, y_train)\n    train_pred = model.predict(load_train)\n    valid_pred = model.predict(load_valid)\n"
            "    train_mae = mean_absolute_error(y_train, train_pred)\n    valid_mae = mean_absolute_error(y_valid, valid_pred)\n    print(name, round(train_mae, 2), round(valid_mae, 2))")
    N["loop"] = code_slide(prs, "WORKED EXAMPLE", "Fitting the three curves and scoring them", loop,
        "model train valid\n" + "\n".join(f"{r['name']} {round(r['train'], 2)} {round(r['valid'], 2)}" for r in rr),
        ["X_train[[\"load_pct\"]] keeps the load column only, as a table.", "Each model is fitted on the training rows and scored on both sets.", f"Errors are in {unit}."],
        "A stronger penalty lowers the fit to the training rows. The validation rows say whether that helps.",
        spoken("Now we fit the three models and score each one twice, on the training rows it learned from and on the validation rows it has never seen. We keep only the load column, because the curve is built from powers of load alone.",
               f"Read the three printed lines. With no penalty the training error is {rr[0]['train']:.2f} and the validation error is {rr[0]['valid']:.2f}. With alpha equal to one they are {rr[1]['train']:.2f} and {rr[1]['valid']:.2f}. With alpha equal to one hundred they are {rr[2]['train']:.2f} and {rr[2]['valid']:.2f}.",
               ("The penalty of one improved the validation error, which suggests that holding the curve back helped. A penalty of one hundred is too strong, and both errors rise, because the curve is held so tightly that it can no longer follow the pattern." if rr[1]["valid"] < rr[0]["valid"] - 0.05 else "In this cohort the validation error barely moves with a penalty of one, so the penalty does little for the errors. It still changes the coefficients, as the next slide shows. A penalty of one hundred is too strong, and both errors rise.")), lab(), code_size=13, out_size=15)
    big = lambda v: (f"over {10 ** int(np.log10(v)):,}" if v >= 100 else f"{v:.1f}")
    N["coef"] = table_slide(prs, "ONE IDEA AT A TIME", "What the penalty does to the coefficients and the errors",
        ["Model", "Largest coefficient (scaled columns)", f"Train MAE ({unit})", f"Valid MAE ({unit})"],
        [[r["name"], big(r["coef"]), f"{r['train']:.2f}", f"{r['valid']:.2f}"] for r in rr],
        [150, 346, 186, 186],
        spoken(f"Look at the second column. Without a penalty, the largest coefficient on the scaled columns is {big(rr[0]['coef'])}. These huge coefficients cancel each other out to draw a wiggly curve. With alpha equal to one the largest coefficient shrinks to {big(rr[1]['coef'])}, and with alpha equal to one hundred to {big(rr[2]['coef'])}.",
               f"That is shrinkage. The penalty keeps all coefficients small, and a model with small coefficients is much less able to swing between training rows. For comparison, a plain straight line on load alone scores {B['line_load']['valid']:.2f} {unit} on the validation rows. The best curve here scores {rr[1]['valid']:.2f}, so with only fifteen validation rows the two are too close to separate. The big gain comes from a better input: the Week 8 line with both load and ambient temperature scores {reg['linear']['mae']:.2f}."), lab(), size=20, row_h=54,
        below=[f"A plain straight line on load alone: validation MAE {B['line_load']['valid']:.2f} {unit}.", f"The Week 8 line on load and ambient temperature: {reg['linear']['mae']:.2f} {unit}.", "In scikit-learn the coefficients are in model[-1].coef_, the last step of the pipeline."], below_size=18)
    N["vocabB"] = table_slide(prs, "WORDS WE USE", "Words for today: predicting from neighbours",
        ["Word", "Plain meaning", "Example from today"],
        [["Neighbour", "A training row whose inputs are close to the new row's inputs.", "The 3 closest rows"],
         ["Distance", "How far apart two rows are, measured over all inputs.", "Straight-line distance, after scaling"],
         ["k", "How many neighbours vote. A hyperparameter.", "k = 3"],
         ["k-nearest neighbours (KNN)", "Predict by averaging the targets of the k closest training rows.", "KNeighborsRegressor"],
         ["Lazy learner", "A model that stores the training rows and does its work at prediction time.", "KNN has no training step to speak of"]],
        [230, 400, 238],
        spoken("Five words for the second half. A neighbour is a training row whose inputs are close to the inputs of a new row. Distance says how close, measured over all the inputs, and for this to be fair the inputs must be scaled first. The number k says how many neighbours we use. K nearest neighbours, written KNN, predicts by averaging the targets of the k closest training rows. People call it a lazy learner, because it stores the training rows and does its work only when a prediction is asked for."), lab(), size=17)
    ex = F.fig_knn(fd / "knn.png", code)
    N["knnfig"] = figure_slide(prs, "A prediction from the three nearest training rows", fd / "knn.png",
        f"The star is the validation row with record_id {ex['query_row']}. Its 3 nearest training rows (scaled inputs) have targets {ex['neighbour_targets'][0]:g}, {ex['neighbour_targets'][1]:g} and {ex['neighbour_targets'][2]:g}.",
        spoken(f"Here is KNN at work. The star is one validation row, the one with record_id {ex['query_row']}. The grey dots are the training rows. To predict, we find the three training rows closest to the star, which are the green dots. Their targets are {ex['neighbour_targets'][0]:g}, {ex['neighbour_targets'][1]:g} and {ex['neighbour_targets'][2]:g}, all in {unit}.",
               f"The prediction is their average, {ex['prediction']:.1f} {unit}. The true value for this row is {ex['actual']:g}, so the miss is {abs(ex['prediction'] - ex['actual']):.1f}. Distances are measured after scaling both inputs, so a step of one typical swing in load counts the same as a step of one typical swing in ambient temperature. The picture uses the scaled columns, so the nearest rows really are the nearest on the page."), lab())
    knn_code = ("from sklearn.neighbors import KNeighborsRegressor\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\nprint(\"k valid\")\nfor k in [1, 3, 20]:\n    model = make_pipeline(\n        SimpleImputer(strategy=\"median\"),\n        StandardScaler(),\n"
                "        KNeighborsRegressor(n_neighbors=k))\n    model.fit(X_train, y_train)\n    valid_pred = model.predict(X_valid)\n    valid_mae = mean_absolute_error(y_valid, valid_pred)\n    print(k, round(valid_mae, 2))")
    best = min(kn, key=lambda r: r["valid"])
    N["knncode"] = code_slide(prs, "WORKED EXAMPLE", "Trying three values of k", knn_code, "k valid\n" + "\n".join(f"{r['k']} {round(r['valid'], 2)}" for r in kn),
        ["n_neighbors is k, the number of neighbours that vote.", "The imputer fills blanks and the scaler puts inputs on a common ruler before distances are measured.", f"Errors are in {unit}, on the validation rows."],
        "fit stores the training rows. predict does the neighbour search.",
        spoken("The pipeline has three steps. The imputer fills the one blank ambient temperature in the training rows, using the median, which is the middle value. The scaler puts load and ambient temperature on a common ruler, because KNN measures distance and an unscaled input with big numbers would dominate. The last step is the KNN regressor, and n neighbors is the number we called k.",
               f"The loop tries three values of k and prints the validation error for each. Read the three lines. With k equal to {best['k']} the error is {best['valid']:.2f} {unit}, the lowest of the three. With k equal to one the model copies a single neighbour, noise included. With k equal to twenty it averages so many rows that the prediction becomes blurry. As with tree depth, a small value chases noise and a very large value misses the pattern."), lab(), code_size=13, out_size=13)
    N["choosek"] = idea_slide(prs, "ONE IDEA AT A TIME", "Choosing k, and the price of waiting until prediction time",
        [("CHOOSING k", True), "Try several values and compare the validation error. Very small k chases noise. Very large k averages too much.", f"Here k = {best['k']} gives the lowest error of the three we tried."],
        [("THE PRICE", True), "KNN keeps every training row. Each prediction measures the distance to all of them, so it slows down as the training table grows.", "A line or a tree answers in an instant once it is trained."],
        spoken(f"How do we choose k? We do what we did for tree depth and for alpha: try several values and compare the validation error. A very small k chases noise. A very large k averages too much and blurs the pattern. In our rows k equal to {best['k']} gave the lowest error of the three values we tried.",
               "There is a price to remember. KNN keeps every training row. For each prediction it measures the distance to all of them, so it gets slower as the training table grows. A line or a tree is quick to answer once trained. For a small engineering table the difference is invisible, and for a million rows it matters."), lab())
    cands = B["candidates"]
    N["cands"] = table_slide(prs, "ONE IDEA AT A TIME", "Five candidates on the same validation rows",
        ["Candidate", f"Validation MAE ({unit})"], [[n, f"{v:.2f}"] for n, v in cands], [560, 308],
        spoken(f"Here are five candidates scored on the same validation rows, with the baseline at the top. The average guess is the reference. The straight line using both inputs scores {cands[1][1]:.2f}. The depth four tree scores {cands[2][1]:.2f}. The ridge curve on load alone scores {cands[3][1]:.2f}. KNN with k equal to three scores {cands[4][1]:.2f}.",
               "The straight line on both inputs fits these rows best, and KNN on the same two inputs comes second. The ridge curve sees only the load, so its row is not a like-for-like comparison. A flexible model earns its place only when the pattern needs it. When two models score about the same, we choose the simpler one, because it is easier to explain and to maintain. One caution: we picked alpha and k by looking at these same validation rows, so these scores are slightly optimistic. The sealed test group gives the final check later. We will use this reasoning in the project write-up."), lab(), size=20, row_h=52,
        below=["All five were scored on the same validation rows.", "The ridge row sees load only, so it is not a like-for-like comparison.", "alpha and k were chosen on these rows, so the scores are slightly optimistic."], below_size=18)
    N["which"] = table_slide(prs, "ONE IDEA AT A TIME", "Which model for which job",
        ["Model", "Works well when", "Watch out for"],
        [["Straight line", "The pattern is close to a straight path", "A curved pattern"],
         ["Ridge", "Many or flexible inputs, and overfitting is a risk", "Choosing alpha, and scaling first"],
         ["Decision tree", "Inputs interact and steps are natural", "Jumpy answers, overfitting with depth"],
         ["Random forest", "A tree is too jumpy", "Harder to explain, slower"],
         ["KNN", "Nearby rows really are similar", "Scaling, slow prediction on big tables"]],
        [200, 360, 308],
        spoken("To close the modelling block, here is a quick guide to which model for which job. A straight line works well when the pattern is close to a straight path, and it fails on curves. Ridge suits flexible or crowded inputs where overfitting is a risk, and it needs scaling and a sensible alpha. A decision tree handles inputs that interact, and its answers can be jumpy. A random forest smooths a jumpy tree and gives up some clarity. KNN works when nearby rows really are similar, and it needs scaling and gets slow on big tables.",
               "No row in this table is the best everywhere. We choose with evidence from validation rows, and we explain the choice."), lab(), size=17)
    N["colab"] = idea_slide(prs, "ONE IDEA AT A TIME", "A fresh start in Colab",
        [("BEFORE THE CHECK", True), "Upload your data file to the Colab Files panel, or mount Drive.", "Put the file where the README says, for example data/raw/engineering_data.csv."],
        [("THE CHECK", True), "Choose Runtime, then Restart session, then Run all.", "Disconnect and delete runtime wipes uploaded files, so you upload them again before the check."],
        spoken("In Colab, a fresh start has a few specific steps. Uploaded files live only as long as the runtime. So before the check, upload your data file to the Files panel, or mount Drive, and put it exactly where your README says it goes.",
               "Then choose Runtime, Restart session, and Run all. A restart clears every variable from memory but keeps uploaded files. The other choice, Disconnect and delete runtime, wipes the uploaded files as well, so after that we upload them again before we run. If every cell runs from top to bottom with no error and the results match what we saved, the notebook passes our fresh-start check."), lab())
    ver_code = ("import sys, pandas, numpy, sklearn\nprint(sys.version.split()[0])\nprint(\"pandas\", pandas.__version__)\nprint(\"numpy\", numpy.__version__)\nprint(\"scikit-learn\", sklearn.__version__)")
    N["versions"] = code_slide(prs, "WORKED EXAMPLE", "Recording the versions you used", ver_code, "(your versions print here)",
        ["Each line prints the version of one tool.", "Copy the four results into requirements.txt and the README.", "Write them as pandas==X.Y.Z, one tool on each line, with the numbers your own run printed."],
        "Install later with: pip install -r requirements.txt",
        spoken("A reader needs to know which versions of the tools you used, because a newer version can behave differently. This short cell asks Python for them. The first line imports the tools and the system module. The next lines print the Python version and the version of pandas, NumPy and scikit-learn.",
               "Your own run prints the numbers. We copy them into a small text file called requirements dot txt, one tool on each line, written as the tool name, two equals signs and the version. Someone else can then install the same versions with one command, pip install dash r requirements dot txt, and mention the Python version in the README."), lab(), code_size=15, out_size=15)
    N["words13"] = table_slide(prs, "WORDS WE USED", "Words from today",
        ["Word", "Plain meaning", "Where we met it"],
        [["Regularisation", "Holding a model back with a penalty.", "Ridge with alpha 1"],
         ["alpha", "The strength of the penalty. A hyperparameter.", "0, 1 and 100"],
         ["Shrinkage", "Coefficients pulled toward zero by the penalty.", "A huge coefficient became a small one"],
         ["Neighbour and k", "The closest training rows, and how many we use.", f"k = {best['k']}"],
         ["KNN", "Average the targets of the k closest rows.", f"Validation MAE {best['valid']:.2f} {unit}"],
         ["Hyperparameter", "A setting chosen before training.", "alpha and k"]],
        [230, 400, 238],
        spoken("Six words to keep from the modelling half. Regularisation holds a model back with a penalty. Alpha is the strength of that penalty. Shrinkage is what the penalty does to the coefficients. A neighbour is a close training row and k is how many we use. KNN averages the targets of the k closest rows. Alpha and k are both hyperparameters, settings we choose before training. Shrinkage and neighbours lead into the second half of today, where we make the project runnable by someone else."), lab(), size=17)
    return N
