"""Session 13 lab notebook: regression on the Lakeside Mart weekly data. Expected values come from content/s13_facts.py (numpy least squares).

NEEDS statsmodels (not installed in the build sandbox). The runner therefore proves only that every cell compiles. The notebook was also executed end to end against a small statsmodels
stand-in written for the purpose (ref/verify_g.py), which checks the NumPy cells and the use of the statsmodels calls, not the real library output.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import nb as NB  # noqa: E402

_s = importlib.util.spec_from_file_location('s13_facts', HERE.parent / 's13_facts.py')
FX = importlib.util.module_from_spec(_s)
_s.loader.exec_module(FX)

TITLE = 'Regression: explaining and predicting a number'
NEEDS = ['statsmodels']


def r(v, k=4):
    return repr(round(float(v), k))


def build(solution):
    F = FX.facts()
    m1, m3, mb = F['m1'], F['m3'], F['mb']
    c = m3['b']
    ci = F['ci']
    th = F['res_sd_thirds']
    nb = NB.Notebook()

    def ans(sol, hint):
        return sol if solution else hint

    G = '' if solution else 'if model is not None: '   # learner version: wait until the model exists

    nb.md('# Session 13 lab: regression, explaining and predicting a number\n\n'
          'You will fit a simple and a multiple linear regression on the Lakeside Mart weekly data, read every coefficient as a sentence, check the residuals, '
          'meet the dummy variable trap, test the model on weeks it never saw, and save a summary file for your Project milestone 2 report.\n\n'
          'In every step: **PREDICT**, run, **READ**, **CHANGE** one thing. Cells with `# your code here` are yours to fill in. Until you fill them in, the checks say NOT YET and the notebook keeps running. Cells with a `check(...)` line tell you whether your number matches.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nplt.rcParams["figure.figsize"] = (7, 4)\n\n# Helper: run a check on a value that may not exist yet. You do not need to read it.\ndef safe(f):\n    try:\n        return f()\n    except Exception:\n        return np.nan')

    # step 1
    nb.step(1, 'Look at the data', 'Each record of branch_weeks.csv is one branch in one week. Footfall is the door count, promo_on is 1 in a promotion week, orders is the target.')
    nb.predict('Will the correlation of orders with footfall be strongly positive, weakly positive, or near zero? Roughly what number?')
    nb.code('bw = pd.read_csv("branch_weeks.csv")\n'
            'print(bw.shape)\n'
            'print(bw.head(3))\n\n'
            'r = ' + ans('bw.orders.corr(bw.footfall)', 'np.nan  # your code here: the correlation of orders with footfall, using .corr()') + '\n'
            'print("correlation:", r)\n\n'
            'plt.scatter(bw.footfall, bw.orders, s=6)\nplt.xlabel("footfall"); plt.ylabel("orders"); plt.show()\n\n'
            'check("832 records", len(bw), 832, 0)\n'
            f'check("correlation of orders with footfall", r, {r(F["r"])}, 0.01)')
    nb.read('Describe the cloud in one sentence. Is a straight line a fair summary?')

    # step 2
    nb.step(2, 'Simple linear regression by ordinary least squares', 'Solve for the intercept b0 and the coefficient b1 of footfall. X holds a column of ones (for the intercept) and the predictor.')
    nb.predict('The slope will be small because footfall is in people and orders are counts. Will b1 be nearer 0.002, 0.02 or 0.2?')
    nb.code('X1 = np.column_stack([np.ones(len(bw)), bw.footfall])\n'
            'y = bw.orders.values\n'
            'simple = ' + ans('np.linalg.lstsq(X1, y, rcond=None)[0]', 'np.array([np.nan, np.nan])  # your code here: np.linalg.lstsq(X1, y, rcond=None)[0] gives b0 and b1') + '\n'
            'print(simple)\n\n'
            f'check("intercept b0", simple[0], {r(m1["b"][0])}, 0.01)\n'
            f'check("coefficient b1", simple[1], {r(m1["b"][1])}, 0.0005)')
    nb.read('Say b1 as a sentence for a manager: how many more orders go with 1,000 more people at the door?')
    nb.change('Fit orders on rainfall_mm alone (replace bw.footfall in X1). Is the coefficient positive or negative? How does its size compare with footfall?')
    nb.code('Xr = np.column_stack([np.ones(len(bw)), bw.rainfall_mm])\n'
            'rain_only = ' + ans('np.linalg.lstsq(Xr, y, rcond=None)[0]', 'np.array([np.nan, np.nan])  # your code here: the same lstsq call with Xr') + '\n'
            'print(rain_only)\n\n'
            f'check("rain-only coefficient", rain_only[1], {r(F["rain_only_b"])}, 0.005)')

    # step 3
    nb.step(3, 'Multiple linear regression, residuals and R squared', 'Add promo_on and rainfall_mm. Then measure the fit: residuals are actual minus predicted, R squared is 1 minus the unexplained share of the variation.')
    nb.predict('Will R squared rise above the 0.706 of footfall alone? By a lot or a little?')
    nb.code('cols = ["footfall", "promo_on", "rainfall_mm"]\n'
            'X = np.column_stack([np.ones(len(bw)), bw[cols]])\n'
            'coef = ' + ans('np.linalg.lstsq(X, y, rcond=None)[0]', 'np.full(4, np.nan)  # your code here: lstsq on X and y, keep the first result') + '\n'
            'print(dict(zip(["intercept"] + cols, np.round(coef, 4))))\n\n'
            'fitted = ' + ans('X @ coef', 'np.full(len(y), np.nan)  # your code here: X @ coef') + '\n'
            'residuals = ' + ans('y - fitted', 'np.full(len(y), np.nan)  # your code here: actual minus fitted') + '\n'
            'ss_res = ' + ans('(residuals ** 2).sum()', 'np.nan  # your code here: sum of squared residuals') + '\n'
            'ss_tot = ' + ans('((y - y.mean()) ** 2).sum()', 'np.nan  # your code here: total variation of y around its mean') + '\n'
            'r2 = ' + ans('1 - ss_res / ss_tot', 'np.nan  # your code here: 1 minus ss_res over ss_tot') + '\n'
            'rmse = ' + ans('np.sqrt((residuals ** 2).mean())', 'np.nan  # your code here: root of the mean squared residual') + '\n'
            'print("R squared:", round(r2, 3), " RMSE:", round(rmse, 2))\n\n'
            f'check("intercept", coef[0], {r(c[0])}, 0.01)\n'
            f'check("footfall coefficient", coef[1], {r(c[1])}, 0.0005)\n'
            f'check("promo_on coefficient", coef[2], {r(c[2])}, 0.01)\n'
            f'check("rainfall_mm coefficient", coef[3], {r(c[3])}, 0.001)\n'
            f'check("R squared", r2, {r(m3["r2"])}, 0.001)\n'
            f'check("RMSE", rmse, {r(m3["rmse"])}, 0.01)')
    nb.read('Write one sentence for each of the three coefficients, starting "Holding the other predictors fixed ...".')
    nb.change('Drop rainfall_mm from cols and refit. Does R squared fall a lot? What does that say about rainfall as a predictor?')

    # step 4
    nb.step(4, 'Check the residuals, then add indicator variables', 'A residual plot should be an even cloud (homoscedasticity). Then turn the branch into indicator (dummy) variables with one level dropped.')
    nb.predict('Will the residuals have the same spread for quiet and busy weeks, or will busy weeks spread more?')
    nb.code('plt.scatter(fitted, residuals, s=6)\nplt.axhline(0, color="red")\nplt.xlabel("predicted orders"); plt.ylabel("residual"); plt.show()\n\n'
            'thirds = pd.qcut(pd.Series(fitted).rank(method="first"), 3, labels=False) if not np.isnan(fitted).any() else np.zeros(len(y), dtype=int)\n'
            'sd_by_third = ' + ans('pd.Series(residuals).groupby(thirds).std()', 'pd.Series([np.nan, np.nan, np.nan])  # your code here: pd.Series(residuals).groupby(thirds).std()') + '\n'
            'print(sd_by_third)\n\n'
            f'check("residual sd, lowest third", sd_by_third[0], {r(th[0])}, 0.05)\n'
            f'check("residual sd, highest third", sd_by_third[2], {r(th[2])}, 0.05)')
    nb.read('Which pattern from the slide do you see: even cloud, curve, fan or outliers? What does it mean for forecasts of busy weeks?')
    nb.code('dummies = ' + ans('pd.get_dummies(bw.branch_id, drop_first=True, dtype=float)', 'pd.DataFrame(np.nan, index=bw.index, columns=["B02", "B03", "B04", "B05", "B06", "B07", "B08"])  # your code here: pd.get_dummies(bw.branch_id, drop_first=True, dtype=float)') + '\n'
            'Xb = ' + ans('np.column_stack([X, dummies])', 'np.full((len(bw), 11), np.nan)  # your code here: add the dummy columns to X with np.column_stack') + '\n'
            'cb = ' + ans('np.linalg.lstsq(Xb, y, rcond=None)[0]', 'np.full(11, np.nan)  # your code here: lstsq on Xb and y') + '\n'
            'n, k = Xb.shape\n'
            'r2b = ' + ans('1 - ((y - Xb @ cb) ** 2).sum() / ss_tot', 'np.nan  # your code here: R squared as before, using Xb and cb') + '\n'
            'adj_r2b = ' + ans('1 - (1 - r2b) * (n - 1) / (n - k)', 'np.nan  # your code here: 1 - (1 - r2b) * (n - 1) / (n - k)') + '\n'
            'print(list(dummies.columns))\nprint("R squared", round(r2b, 3), "adjusted", round(adj_r2b, 3))\n\n'
            f'check("R squared with branch indicators", r2b, {r(mb["r2"])}, 0.001)\n'
            f'check("adjusted R squared with branch indicators", adj_r2b, {r(mb["adj"])}, 0.001)')
    nb.read('Adjusted R squared was 0.794 without the branch indicators. Did it rise or fall? Would you keep them?')
    nb.change('Now keep all 8 indicators together with the intercept (drop_first=False) and print the matrix rank with np.linalg.matrix_rank. This is the dummy variable trap.')
    nb.code('full = np.column_stack([np.ones(len(bw)), pd.get_dummies(bw.branch_id, dtype=float)])\n'
            'rank = ' + ans('np.linalg.matrix_rank(full)', 'np.nan  # your code here: np.linalg.matrix_rank(full)') + '\n'
            'print(full.shape, "columns, rank", rank)\n\n'
            f'check("matrix rank", rank, {F["trap_rank"]}, 0)')

    # step 5
    nb.step(5, 'Cross-check with the libraries', 'statsmodels and scikit-learn solve the same least squares problem. Their numbers should match your NumPy numbers.')
    nb.predict('Will statsmodels give the same coefficients as NumPy, or slightly different ones?')
    nb.code('import statsmodels.formula.api as smf\n'
            'from sklearn.linear_model import LinearRegression\n\n'
            'model = ' + ans('smf.ols("orders ~ footfall + promo_on + rainfall_mm", data=bw).fit()', 'None  # your code here: smf.ols("orders ~ footfall + promo_on + rainfall_mm", data=bw).fit()   (the lines below wait until this is filled in)') + '\n'
            + G + 'print(model.params.round(4))\n'
            + G + 'print("R squared:", round(model.rsquared, 3), " adjusted:", round(model.rsquared_adj, 3))\n'
            + G + 'print(model.conf_int().round(3))\n\n'
            'linear_model = ' + ans('LinearRegression().fit(bw[cols], bw.orders)', 'None  # your code here: LinearRegression().fit(bw[cols], bw.orders)   (the line below waits until this is filled in)') + '\n'
            + G.replace('model', 'linear_model') + 'print(linear_model.intercept_, linear_model.coef_)\n\n'
            'check("statsmodels matches NumPy", safe(lambda: model.params.values), coef, 0.0001)\n'
            f'check("statsmodels R squared", safe(lambda: model.rsquared), {r(m3["r2"])}, 0.001)\n'
            f'check("promo_on interval, lower end", safe(lambda: model.conf_int().loc["promo_on", 0]), {r(ci[2][0])}, 0.01)\n'
            'check("scikit-learn matches NumPy", safe(lambda: np.r_[linear_model.intercept_, linear_model.coef_]), coef, 0.0001)')
    nb.read('statsmodels adds the intercept for you in a formula. What other things does model.summary() report that NumPy did not?')

    # step 6
    nb.step(6, 'Predict, and test on weeks the model never saw', 'To predict, fit on the first 78 weeks (the training set) and score on the last 26 weeks (the test set). The baseline model predicts the training mean.')
    nb.predict('A branch expects 2,000 people, a promotion week and 20 mm of rain. About how many orders?')
    nb.code('week = np.array([1, 2000, 1, 20])      # the 1 is for the intercept\n'
            'pred = ' + ans('week @ coef', 'np.nan  # your code here: week @ coef') + '\n'
            'print("predicted orders:", round(pred, 2))\n\n'
            f'check("predicted orders for the week", pred, {r(F["pred"])}, 0.05)')
    nb.code('is_train = (bw.week_start < "' + F['cut'] + '").values\n'
            'coef_tr = ' + ans('np.linalg.lstsq(X[is_train], y[is_train], rcond=None)[0]', 'np.full(4, np.nan)  # your code here: lstsq on the training rows only') + '\n'
            'pred_te = X[~is_train] @ coef_tr\n'
            'rmse_model = ' + ans('np.sqrt(((y[~is_train] - pred_te) ** 2).mean())', 'np.nan  # your code here: RMSE of the model on the test rows') + '\n'
            'rmse_baseline = ' + ans('np.sqrt(((y[~is_train] - y[is_train].mean()) ** 2).mean())', 'np.nan  # your code here: RMSE if every test week gets the training mean') + '\n'
            'print(is_train.sum(), "training records,", (~is_train).sum(), "test records")\n'
            'print("test RMSE: model", round(rmse_model, 2), " baseline", round(rmse_baseline, 2))\n\n'
            f'check("training records", is_train.sum(), {F["n_tr"]}, 0)\n'
            f'check("test RMSE of the model", rmse_model, {r(F["te_rmse"])}, 0.05)\n'
            f'check("test RMSE of the baseline model", rmse_baseline, {r(F["te_base_rmse"])}, 0.05)')
    nb.read('Did the regression beat the baseline model on weeks it never saw? By how many orders?')
    nb.change('Change the week to 2,000 people with no promotion (the third number 0). How many orders fewer?')

    # step 7
    nb.step(7, 'Keep a summary file for your report', 'A coefficient table with 95 percent intervals is the heart of your one page report. The interval is the coefficient plus or minus 1.963 standard errors (Student t, 828 degrees of freedom).')
    nb.code('s2 = (residuals ** 2).sum() / (len(y) - X.shape[1])\n'
            'se = ' + ans('np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))', 'np.full(4, np.nan)  # your code here: np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))') + '\n'
            'ci_low = ' + ans('coef - 1.963 * se', 'np.full(4, np.nan)  # your code here: coef - 1.963 * se') + '\n'
            'ci_high = ' + ans('coef + 1.963 * se', 'np.full(4, np.nan)  # your code here: coef + 1.963 * se') + '\n'
            'summary = pd.DataFrame({"term": ["intercept"] + cols, "coefficient": coef, "ci_low": ci_low, "ci_high": ci_high})\n'
            'summary.to_csv("regression_summary.csv", index=False)\n'
            'summary.to_excel("regression_summary.xlsx", index=False)   # opens in Excel or Power BI\n'
            'print(summary.round(4))\n\n'
            f'check("promo_on interval, lower", summary.ci_low[2], {r(ci[2][0])}, 0.01)\n'
            f'check("promo_on interval, upper", summary.ci_high[2], {r(ci[2][1])}, 0.01)\n'
            f'check("rainfall interval, upper", summary.ci_high[3], {r(ci[3][1])}, 0.003)')
    nb.md('## Your one page report (Project milestone 2)\n\nDouble-click this cell and write, in plain sentences:\n\n'
          '1. **Question:** the target, the predictors and the decision.\n'
          '2. **Model:** multiple linear regression, with the unit of every predictor.\n'
          '3. **Findings:** three coefficients as sentences with their intervals, and R squared.\n'
          '4. **Check:** what the residual plot showed and what you would do about it.\n'
          '5. **Limits:** what the model cannot prove, and the test RMSE against the baseline model.\n'
          '6. **Project question:** one sentence.\n\n> My report: ')
    nb.code('show_checks()')
    return nb
