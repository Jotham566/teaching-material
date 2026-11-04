"""Session 19 lab notebook: forecast malaria cases for 2025, beat the seasonal naive baseline, build a Pipeline (Project milestone 3).

Every expected value comes from s19.facts() (pandas and numpy on clinic_visits.csv). The Pipeline cells use scikit-learn classes that the sandbox stand-in also has
(Pipeline, SimpleImputer, StandardScaler, LinearRegression), so this notebook is run end to end here. Confirm once in Colab that the Pipeline MAE equals the numpy MAE."""
import re
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s19  # noqa: E402

TITLE = 'Forecasting clinic cases'


def _guard(code):
    """Learner version: an unfinished answer must not stop the notebook. Plain lines run in one try block, each check line has its own, and a failed check reports NOT YET."""
    out, block = [], []

    def flush():
        if block:
            out.append('try:\n' + '\n'.join('    ' + l if l else l for l in block) + '\nexcept Exception as e:\n    print("Finish the cells above first. (" + type(e).__name__ + ")")')
            block.clear()
    for line in code.split('\n'):
        m = re.match(r'check\((["\'])(.*?)\1', line)
        if m:
            flush()
            out.append('try:\n    ' + line + '\nexcept Exception:\n    check(' + repr(m.group(2)) + ', float("nan"), 0, 0)')
        elif line.strip() == 'show_checks()':
            flush()
            out.append(line)
        else:
            block.append(line)
    flush()
    return '\n'.join(out)


def _finish(n, solution):
    if solution:
        return n
    seen_check = False
    for c in n.cells:
        if c['cell_type'] != 'code':
            continue
        src = ''.join(c['source'])
        if 'def check(' in src:
            seen_check = True
            continue
        if not seen_check or 'zipfile' in src or src.startswith('import numpy as np'):
            continue
        c['source'] = NB._src(_guard(src))
    return n


def build(solution):
    F = s19.facts()
    by = F['by_district']
    n = NB.Notebook()

    def todo(code, hint):
        n.code(code if solution else f'answer = None  # your code here: {hint}')

    n.md('# Session 19 lab: forecast 2025, beat the baseline, build a Pipeline\n\n**AI and Data Science Professional** | KLAi Professional Learning | Project milestone 3\n\n'
         'You forecast malaria cases for 12 districts in 2025 using only what was known before 2025. You build the seasonal naive baseline, add lag features, score with MAE, RMSE and MAPE, '
         'pack the work in a scikit-learn Pipeline, and write the three sentences that go to a district manager.\n\n'
         '**How to use this notebook**\n\n1. Run the cells in order from the top (Shift and Enter).\n2. Every step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE** one thing.\n'
         '3. Cells that say `answer = None` are yours to fill in. Replace `None` with your code. Then run the check cell under it.\n4. The data is fictional and generated. Cases are counts of malaria cases per district per month.\n5. If you get an error, read the last line first.')
    n.data_setup()
    n.check_setup()

    # ---------------------------------------------------------------- step 1
    n.step(1, 'Load the clinic file and sort it', 'A time series must be in time order inside each district. Each record is one district in one month.')
    n.code('import os\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\n'
           'from sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LinearRegression\n\nos.makedirs("keep", exist_ok=True)   # the folder where you save what you keep')
    n.predict('How many records will the file have? (12 districts, 60 months.) And how many blank values will total_visits have?')
    todo("answer = pd.read_csv('clinic_visits.csv', parse_dates=['month']).sort_values(['district', 'month']).reset_index(drop=True)",
         'read clinic_visits.csv with month as a date, then sort by district and month')
    n.code(f'clinic = answer\nn_rows = len(clinic)\nn_blank = int(clinic.total_visits.isna().sum())\nprint(n_rows, n_blank)\n'
           f'check("Step 1a: records in the file", n_rows, {F["rows"]})\ncheck("Step 1b: blank total_visits", n_blank, {F["blank_visits"]})')
    n.read('Which variable are we going to forecast, and what is the unit of one record?')

    # ---------------------------------------------------------------- step 2
    n.step(2, 'The baseline model: seasonal naive', 'Forecast every month of 2025 with the same month of 2024. Any model you build later must beat this.')
    n.predict('Will the baseline miss by more in Gulu (about 3,700 cases a month) or in Kampala (about 650)? Guess the size of each miss.')
    n.code("gulu = clinic[clinic.district == 'Gulu'].set_index('month').malaria_cases\nactual = gulu.loc['2025'].values       # what happened in 2025\nlast_year = gulu.loc['2024'].values    # the forecast: the same month last year\nprint(len(actual), len(last_year))")
    todo('answer = abs(actual - last_year).mean()', 'the average of the absolute gaps between actual and last_year (this is MAE)')
    n.code(f'gulu_mae = answer\nprint("Gulu baseline MAE:", round(float(gulu_mae), 1), "cases")\ncheck("Step 2a: Gulu baseline MAE", gulu_mae, {by.loc["Gulu", "naive"]:.4f}, 0.1)')
    n.change('Run the same steps for Kampala: change the district name in the first cell of this step and run the cells again. Write down the Kampala MAE, then compare it with the mean cases of each district.')
    n.code("kampala = clinic[clinic.district == 'Kampala'].set_index('month').malaria_cases\nkampala_mae = abs(kampala.loc['2025'].values - kampala.loc['2024'].values).mean()\nprint('Kampala baseline MAE:', round(float(kampala_mae), 1))\n"
           f'check("Step 2b: Kampala baseline MAE", kampala_mae, {by.loc["Kampala", "naive"]:.4f}, 0.1)')

    # ---------------------------------------------------------------- step 3
    n.step(3, 'Seasonality and the delayed effect of rain', 'Add every district together, look at the calendar month with the most cases, then test whether rain works with a delay.')
    n.predict('Which calendar month (1 to 12) has the most cases over the five years? Which month do you guess is the trough?')
    todo('answer = clinic.groupby(clinic.month.dt.month).malaria_cases.sum().idxmax()', 'group by the calendar month number, add the cases, and take the month with the largest total (idxmax)')
    n.code(f'peak_month = answer\nprint("Peak month:", peak_month)\ncheck("Step 3a: peak calendar month", peak_month, {F["peak_m"]})')
    n.predict('Last month\'s rain: will its correlation with this month\'s cases be near 0 or clearly above 0? And this month\'s rain?')
    n.code("g = clinic.groupby('district')      # every shift stays inside one district\nclinic['cases_lag1'] = g.malaria_cases.shift(1)\nclinic['rain_lag1'] = g.rainfall_mm.shift(1)")
    todo('answer = g.malaria_cases.shift(12)', 'the cases of the same month last year, shifted inside each district: shift(12)')
    n.code("clinic['cases_lag12'] = answer\nfeatures = ['cases_lag1', 'cases_lag12', 'rain_lag1']\nclinic[clinic.district == 'Gulu'][['month', 'malaria_cases'] + features].iloc[0:15]")
    n.read('Look at January 2022 for Gulu. Where does its cases_lag12 value come from? Why are the first rows blank?')
    todo('answer = clinic.dropna(subset=features)', 'keep only the records that have all three lag features')
    n.code(f'ready = answer\nr_now = ready.rainfall_mm.corr(ready.malaria_cases)\nr_lag = ready.rain_lag1.corr(ready.malaria_cases)\nprint(len(ready), round(r_now, 2), round(r_lag, 2))\n'
           f'check("Step 3b: records with every lag feature", len(ready), {F["n_ready"]})\ncheck("Step 3c: correlation with this month\'s rain", r_now, {F["r_rain_now"]:.4f}, 0.01)\n'
           f'check("Step 3d: correlation with last month\'s rain", r_lag, {F["r_rain_lag1"]:.4f}, 0.01)')
    n.read('What do the two correlations say about the effect of rain? Why would a model that sees only this month\'s rain miss it?')

    # ---------------------------------------------------------------- step 4
    n.step(4, 'Split by time', 'Train on 2022 to 2024. Test on 2025. Never split a time series at random.')
    n.predict('How many records will the training set have, and how many the test set? (Remember 12 districts.)')
    todo("answer = ready[ready.month < '2025-01-01']", 'the records with month before 1 January 2025')
    n.code(f'train = answer\ncheck("Step 4a: training records", len(train), {F["n_train"]})')
    todo("answer = ready[ready.month >= '2025-01-01']", 'the records with month from 1 January 2025')
    n.code(f'test = answer\nprint(len(train), len(test))\ncheck("Step 4b: test records", len(test), {F["n_test"]})\ncheck("Step 4c: training ends before the test starts", float(train.month.max() < test.month.min()), 1)')
    n.change('Change the cut date to 1 January 2024 in both cells and look at the new counts. Then put it back to 2025 and run the cells again.')

    # ---------------------------------------------------------------- step 5
    n.step(5, 'Fit the lag model and score it three ways', 'A linear regression fitted with numpy on the training set, then scored on the test set against the baseline. MAE, RMSE and MAPE all use the actual and forecast values.')
    n.code("X_train = np.c_[np.ones(len(train)), train[features]]   # a column of ones for the intercept\ny_train = train.malaria_cases\nX_test = np.c_[np.ones(len(test)), test[features]]\ny_test = test.malaria_cases\nbaseline_pred = test.cases_lag12   # seasonal naive forecast")
    todo('answer = np.linalg.lstsq(X_train, y_train, rcond=None)[0]', 'least squares: np.linalg.lstsq(X_train, y_train, rcond=None)[0] gives the intercept and one weight per feature')
    n.code('coef = answer\ny_pred = X_test @ coef\nprint(coef.round(2))')
    n.predict('Will the model\'s MAE be smaller than the baseline\'s? By how many cases, roughly?')
    todo('answer = abs(y_test - baseline_pred).mean()', 'the mean absolute error of the baseline on the test set')
    n.code(f'naive_mae = answer\nprint("baseline MAE:", round(float(naive_mae), 1))\ncheck("Step 5a: baseline MAE", naive_mae, {F["naive_mae"]:.4f}, 0.1)')
    todo('answer = abs(y_test - y_pred).mean()', 'the mean absolute error of the model on the test set')
    n.code(f'model_mae = answer\nprint("model MAE:", round(float(model_mae), 1))\ncheck("Step 5b: model MAE", model_mae, {F["model_mae"]:.4f}, 0.1)')
    todo('answer = np.sqrt(((y_test - y_pred) ** 2).mean())', 'RMSE: square each miss, take the mean, then the square root')
    n.code(f'model_rmse = answer\nprint("model RMSE:", round(float(model_rmse), 1))\ncheck("Step 5c: model RMSE", model_rmse, {F["model_rmse"]:.4f}, 0.1)')
    todo('answer = (abs(y_test - y_pred) / y_test).mean() * 100', 'MAPE: each absolute miss divided by the actual value, then the mean, times 100')
    n.code(f'model_mape = answer\nprint("model MAPE:", round(float(model_mape), 1), "percent")\ncheck("Step 5d: model MAPE", model_mape, {F["model_mape"]:.4f}, 0.05)')
    n.read('The RMSE is larger than the MAE. What does that tell you about the size of the biggest misses? In which unit is each of the three scores?')
    n.change(f'Refit the model with only features = ["cases_lag1"] (rebuild X_train and X_test first). Is it still better than the baseline? The slides give the answer, but check it yourself.')

    # ---------------------------------------------------------------- step 6
    n.step(6, 'Pack the job into a Pipeline', 'A Pipeline chains preprocessing and the model, so the training and the test records go through the same steps, learned from the training records only.')
    n.predict('The Pipeline fills blanks, standardises and fits the same linear regression. Will its MAE be the same as your numpy model, a little different, or very different?')
    todo("answer = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), LinearRegression())", 'make_pipeline with SimpleImputer(strategy="median"), StandardScaler() and LinearRegression()')
    n.code(f'pipe = answer\npipe.fit(train[features], train.malaria_cases)\ny_pipe = pipe.predict(test[features])\npipe_mae = abs(y_test - y_pipe).mean()\nprint("Pipeline MAE:", round(float(pipe_mae), 1))\n'
           f'check("Step 6a: Pipeline MAE equals the numpy MAE", pipe_mae, {F["model_mae"]:.4f}, 0.1)')
    n.read('Why does standardising the variables not change the forecast of a linear regression?')
    n.code("# Districts differ a lot in size. Add the district as indicator variables (one-hot encoding with pandas; drop the first district).\n"
           "dummies = pd.get_dummies(ready.district, dtype=float).iloc[:, 1:]\nready_d = pd.concat([ready, dummies], axis=1)\nfeatures_d = features + list(dummies.columns)\n"
           "train_d = ready_d[ready_d.month < '2025-01-01']\ntest_d = ready_d[ready_d.month >= '2025-01-01']\nprint(len(features_d), 'variables')")
    todo("answer = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), LinearRegression()).fit(train_d[features_d], train_d.malaria_cases).predict(test_d[features_d])",
         'fit the same kind of Pipeline on train_d[features_d] and predict test_d[features_d]')
    n.code(f'y_pipe_d = answer\npipe_d_mae = abs(test_d.malaria_cases - y_pipe_d).mean()\nprint("Pipeline with district indicator variables, MAE:", round(float(pipe_d_mae), 1))\n'
           f'check("Step 6b: Pipeline MAE with district indicator variables", pipe_d_mae, {F["pipe_mae"]:.4f}, 0.1)')
    n.change('In scikit-learn the encoding goes inside the Pipeline with a ColumnTransformer and a OneHotEncoder. Read the documentation page of OneHotEncoder (drop="first") and write in a text cell how you would build it. You do not need to run it today.')

    # ---------------------------------------------------------------- step 7
    n.step(7, 'See the lag trap with your own eyes', 'Build the same lags without groupby. Python gives no error. Read what it does to the score.')
    n.predict('Without groupby, will the test MAE go up, go down, or stay the same? Why?')
    n.code("bad = clinic[['district', 'month', 'malaria_cases', 'rainfall_mm']].copy()\nbad['cases_lag1'] = bad.malaria_cases.shift(1)     # the mistake: no groupby\n"
           "bad['cases_lag12'] = bad.malaria_cases.shift(12)\nbad['rain_lag1'] = bad.rainfall_mm.shift(1)\nbad = bad.dropna()\n"
           "train_bad = bad[bad.month < '2025-01-01']\ntest_bad = bad[bad.month >= '2025-01-01']\n"
           "coef_bad = np.linalg.lstsq(np.c_[np.ones(len(train_bad)), train_bad[features]], train_bad.malaria_cases, rcond=None)[0]\n"
           "y_pred_bad = np.c_[np.ones(len(test_bad)), test_bad[features]] @ coef_bad\nprint(len(train_bad), 'training records instead of', len(train))")
    todo('answer = abs(test_bad.malaria_cases - y_pred_bad).mean()', 'the mean absolute error of the model built on the wrong lags')
    n.code(f'bad_mae = answer\nprint("MAE with the wrong lags:", round(float(bad_mae), 1), "against", round(float(model_mae), 1))\ncheck("Step 7: MAE with the wrong lags", bad_mae, {F["bad_mae"]:.4f}, 0.1)')
    n.read(f'The wrong version keeps {F["bad_extra"]} extra training records. Where do their lag values come from?')

    # ---------------------------------------------------------------- step 8
    n.step(8, 'Your Project milestone 3 results file', 'Collect the three models in one table and save it. This file and the three sentences below are the evidence you keep.')
    n.code('def scores(y, p):\n    mae = abs(y - p).mean()\n    rmse = np.sqrt(((y - p) ** 2).mean())\n    mape = (abs(y - p) / y).mean() * 100\n    return round(float(mae), 1), round(float(rmse), 1), round(float(mape), 1)\n\n'
           'rows = {"Seasonal naive baseline": scores(y_test, baseline_pred),\n        "Lag model (numpy)": scores(y_test, y_pred),\n        "Pipeline with district indicator variables": scores(test_d.malaria_cases, y_pipe_d)}\n'
           'results = pd.DataFrame(rows, index=["MAE (cases)", "RMSE (cases)", "MAPE (percent)"]).T\nresults.to_csv("keep/session19_forecast_results.csv")\nresults')
    n.code('check("Step 8: the results table has three models", len(results), 3)')
    n.code('show_checks()')
    n.md('## Your three sentences (Project milestone 3)\n\nDouble-click this cell and write three sentences for a district manager. Use your own numbers.\n\n'
         '1. The forecast horizon and the average miss of the model, in cases (and as a share of a typical month).\n'
         '2. Whether it beats the seasonal naive baseline, and by how much.\n'
         '3. One limit: for example one test year only, districts where the baseline wins, or a horizon longer than one month.\n\n> My three sentences: ')
    return _finish(n, solution)
