"""Session 19: Forecasting and a first end-to-end model. Facts module (all numbers computed here with pandas and numpy from clinic_visits.csv)."""
import contextlib
import io
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
FEATS = ['cases_lag1', 'cases_lag12', 'rain_lag1']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def mae(y, p):
    return float(np.mean(np.abs(np.asarray(y, float) - np.asarray(p, float))))


def rmse(y, p):
    return float(np.sqrt(np.mean((np.asarray(y, float) - np.asarray(p, float)) ** 2)))


def mape(y, p):
    y = np.asarray(y, float)
    return float(np.mean(np.abs(y - np.asarray(p, float)) / y) * 100)


def ols_fit_predict(train, test, feats):
    X = np.c_[np.ones(len(train)), train[feats]]
    coef = np.linalg.lstsq(X, train.malaria_cases, rcond=None)[0]
    return np.c_[np.ones(len(test)), test[feats]] @ coef, coef


@lru_cache(maxsize=None)
def facts():
    F = {}
    clinic = pd.read_csv(DATA / 'clinic_visits.csv', parse_dates=['month']).sort_values(['district', 'month']).reset_index(drop=True)
    F['clinic'] = clinic
    F['rows'], F['districts'], F['months'] = len(clinic), clinic.district.nunique(), clinic.month.nunique()
    F['first_month'], F['last_month'] = clinic.month.min(), clinic.month.max()
    F['blank_visits'] = int(clinic.total_visits.isna().sum())
    F['blank_cases'] = int(clinic.malaria_cases.isna().sum())
    # decomposition of the total across districts: straight-line trend, season = mean of what is left by calendar month, noise = the rest
    tot = clinic.groupby('month').malaria_cases.sum()
    F['total'] = tot
    t = np.arange(len(tot))
    slope, icpt = np.polyfit(t, tot.values, 1)
    trend = icpt + slope * t
    detr = tot.values - trend
    cm = tot.index.month
    season_by_m = np.array([detr[cm == m].mean() for m in range(1, 13)])
    season = season_by_m[cm - 1]
    noise = tot.values - trend - season
    F.update(dec_observed=tot.values, dec_trend=trend, dec_season=season, dec_noise=noise, dec_slope=float(slope), dec_icpt=float(icpt),
             season_by_m=season_by_m, noise_sd=float(noise.std(ddof=1)), season_range=float(season_by_m.max() - season_by_m.min()))
    F['year_totals'] = clinic.groupby(clinic.month.dt.year).malaria_cases.sum()
    F['by_cal_month'] = clinic.groupby(clinic.month.dt.month).malaria_cases.sum()
    F['peak_m'], F['trough_m'] = int(F['by_cal_month'].idxmax()), int(F['by_cal_month'].idxmin())
    F['peak_v'], F['trough_v'] = int(F['by_cal_month'].max()), int(F['by_cal_month'].min())
    # lags, inside each district
    g = clinic.groupby('district')
    c = clinic.copy()
    for k in (1, 3, 6, 12):
        c[f'cases_lag{k}'] = g.malaria_cases.shift(k)
        c[f'rain_lag{k}'] = g.rainfall_mm.shift(k)
    F['c'] = c
    ready = c.dropna(subset=FEATS)
    F['ready'] = ready
    F['n_ready'] = len(ready)
    train, test = ready[ready.month < '2025-01-01'], ready[ready.month >= '2025-01-01']
    F['train'], F['test'] = train, test
    F['n_train'], F['n_test'] = len(train), len(test)
    F['n_lost'] = len(c) - len(ready)
    F['train_first'], F['train_last'] = train.month.min(), train.month.max()
    y = test.malaria_cases.values
    F['y_mean'] = float(y.mean())
    pred, coef = ols_fit_predict(train, test, FEATS)
    F['coef'] = coef
    F['pred'] = pred
    naive = test.cases_lag12.values
    F['naive_mae'], F['naive_rmse'], F['naive_mape'] = mae(y, naive), rmse(y, naive), mape(y, naive)
    F['model_mae'], F['model_rmse'], F['model_mape'] = mae(y, pred), rmse(y, pred), mape(y, pred)
    F['naive_rel'], F['model_rel'] = F['naive_mae'] / F['y_mean'] * 100, F['model_mae'] / F['y_mean'] * 100
    F['gain_pct'] = (F['naive_mae'] - F['model_mae']) / F['naive_mae'] * 100
    # one-feature baselines for context
    F['mae_lag1_only'] = mae(y, ols_fit_predict(train, test, ['cases_lag1'])[0])
    F['mae_lag12_fit'] = mae(y, ols_fit_predict(train, test, ['cases_lag12'])[0])
    # correlations on the rows that have every lag feature
    F['r_rain_now'] = float(ready.rainfall_mm.corr(ready.malaria_cases))
    F['r_rain_lag1'] = float(ready.rain_lag1.corr(ready.malaria_cases))
    F['scatter_now'] = list(zip(ready.rainfall_mm.round(1), ready.malaria_cases))
    F['scatter_lag'] = list(zip(ready.rain_lag1.round(1), ready.malaria_cases))
    for key, xs in (('now', ready.rainfall_mm), ('lag', ready.rain_lag1)):
        b1, b0 = np.polyfit(xs, ready.malaria_cases, 1)
        F[f'line_{key}'] = (float(b0), float(b1))
    # by district and by month
    te = test.assign(pred=pred, naive=naive)
    te['e_naive'] = (te.malaria_cases - te.naive).abs()
    te['e_model'] = (te.malaria_cases - te.pred).abs()
    F['te'] = te
    F['by_district'] = te.groupby('district').agg(naive=('e_naive', 'mean'), model=('e_model', 'mean'), mean_cases=('malaria_cases', 'mean'))
    F['model_wins'] = int((te.e_model < te.e_naive).sum())
    F['districts_naive_wins'] = sorted(F['by_district'].index[F['by_district'].naive < F['by_district'].model])
    F['districts_model_wins'] = int((F['by_district'].model < F['by_district'].naive).sum())
    # worked example: one district, 2025
    m = te[te.district == 'Mbarara'].sort_values('month')
    F['mb_actual'] = m.malaria_cases.values
    F['mb_naive'] = m.naive.values
    F['mb_pred'] = m.pred.values
    F['mb_months'] = [x.strftime('%b') for x in m.month]
    F['mb_abs_sum'] = float(np.abs(F['mb_actual'] - F['mb_naive']).sum())
    F['mb_mae'], F['mb_rmse'], F['mb_mape'] = mae(F['mb_actual'], F['mb_naive']), rmse(F['mb_actual'], F['mb_naive']), mape(F['mb_actual'], F['mb_naive'])
    mb24 = c[(c.district == 'Mbarara') & (c.month.dt.year == 2024)].sort_values('month')
    F['mb_2024'] = mb24.malaria_cases.values
    assert (F['mb_2024'] == F['mb_naive']).all()
    F['mb_err_first3'] = [int(abs(a - b)) for a, b in zip(F['mb_actual'][:3], F['mb_naive'][:3])]
    # random split against the time split
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(ready))
    k = int(round(0.25 * len(ready)))
    rte, rtr = ready.iloc[idx[:k]], ready.iloc[idx[k:]]
    F['random_mae'] = mae(rte.malaria_cases, ols_fit_predict(rtr, rte, FEATS)[0])
    F['random_test_n'] = k
    # leakage from the future: a feature that looks one month ahead (shift(-1)), same random split on the rows that have it
    c['cases_lead1'] = g.malaria_cases.shift(-1)
    rl = c.dropna(subset=FEATS + ['cases_lead1'])
    idx = np.random.default_rng(42).permutation(len(rl))
    k = int(round(0.25 * len(rl)))
    lte, ltr = rl.iloc[idx[:k]], rl.iloc[idx[k:]]
    F['leak_honest_mae'] = mae(lte.malaria_cases, ols_fit_predict(ltr, lte, FEATS)[0])
    F['leak_mae'] = mae(lte.malaria_cases, ols_fit_predict(ltr, lte, FEATS + ['cases_lead1'])[0])
    F['leak_drop_pct'] = (F['leak_honest_mae'] - F['leak_mae']) / F['leak_honest_mae'] * 100
    # the lag that borrows from another district
    b = clinic[['district', 'month', 'malaria_cases', 'rainfall_mm']].copy()
    b['cases_lag1'] = b.malaria_cases.shift(1)
    b['cases_lag12'] = b.malaria_cases.shift(12)
    b['rain_lag1'] = b.rainfall_mm.shift(1)
    okb = b.dropna()
    F['bad_ready'] = len(okb)
    F['bad_extra'] = len(okb) - len(ready)
    trb, teb = okb[okb.month < '2025-01-01'], okb[okb.month >= '2025-01-01']
    F['bad_mae'] = mae(teb.malaria_cases, ols_fit_predict(trb, teb, FEATS)[0])
    F['bad_n_test'] = len(teb)
    first = clinic.groupby('district').head(1).index
    F['bad_first_rows'] = int(b.loc[first, 'cases_lag1'].notna().sum())
    F['bad_lag12_rows'] = int(sum(b.loc[i:i + 11, 'cases_lag12'].notna().sum() for i in first))
    gi = clinic.index[(clinic.district == 'Gulu')][0]
    F['gulu_first'] = clinic.loc[gi]
    F['gulu_bad_lag1'] = int(b.loc[gi, 'cases_lag1'])
    F['prev_row'] = clinic.loc[gi - 1]
    # horizon: direct models, lag h of cases and rain, plus the 12-month lag
    ok12 = c.dropna(subset=['cases_lag12', 'rain_lag12', 'cases_lag1', 'rain_lag1', 'cases_lag3', 'rain_lag3', 'cases_lag6', 'rain_lag6'])
    assert len(ok12) == len(ready)
    htr, hte = ok12[ok12.month < '2025-01-01'], ok12[ok12.month >= '2025-01-01']
    F['horizon'] = []
    for h in (1, 3, 6, 12):
        f = [f'cases_lag{h}', f'rain_lag{h}'] + (['cases_lag12'] if h < 12 else [])
        F['horizon'].append((h, mae(hte.malaria_cases, ols_fit_predict(htr, hte, f)[0])))
    # walk-forward validation: expanding window, three cut dates
    F['walk'] = []
    for yr in (2023, 2024, 2025):
        wtr, wte = ready[ready.month < f'{yr}-01-01'], ready[(ready.month >= f'{yr}-01-01') & (ready.month < f'{yr + 1}-01-01')]
        pw, _ = ols_fit_predict(wtr, wte, FEATS)
        F['walk'].append((yr, len(wtr), len(wte), mae(wte.malaria_cases, wte.cases_lag12), mae(wte.malaria_cases, pw)))
    # pipeline with district indicator variables (pandas get_dummies outside; the scikit-learn Pipeline holds impute, scale, fit)
    dm = pd.get_dummies(ready.district, dtype=float).iloc[:, 1:]
    r2 = pd.concat([ready, dm], axis=1)
    f2 = FEATS + list(dm.columns)
    ptr, pte = r2[r2.month < '2025-01-01'], r2[r2.month >= '2025-01-01']
    F['pipe_feats'] = f2
    F['pipe_mae'] = mae(pte.malaria_cases, ols_fit_predict(ptr, pte, f2)[0])
    dm_all = pd.get_dummies(ready.district, dtype=float)
    r3 = pd.concat([ready, dm_all], axis=1)
    f3 = FEATS + list(dm_all.columns)
    F['pipe_mae_all_dummies'] = mae(r3[r3.month >= '2025-01-01'].malaria_cases, ols_fit_predict(r3[r3.month < '2025-01-01'], r3[r3.month >= '2025-01-01'], f3)[0])
    F['n_pipe_feats'] = len(f2)
    return F


def run_snippet(code, ns=None):
    """Execute a code string shown on a slide and return (what it prints, namespace), so a slide never carries an output that was not produced.
    scikit-learn is not installed in the authoring sandbox: `import sklearn` finds the NumPy stand-in in ref/ (same least-squares maths)."""
    import sys
    ref = str(BUILD / 'ref')
    if ref not in sys.path:
        sys.path.insert(0, ref)
    F = facts()
    if ns is None:
        ns = {'np': np, 'pd': pd, 'clinic': F['clinic'].copy()}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, ns)
    return buf.getvalue().strip(), ns


def n(x):
    return f'{int(round(x)):,}'


def f1(x):
    return f'{x:.1f}'


def build():
    F = facts()
    c, ready, train, test = F['c'], F['ready'], F['train'], F['test']
    yt = [(0, '2021'), (12, '2022'), (24, '2023'), (36, '2024'), (48, '2025')]
    nm, mm = F['naive_mae'], F['model_mae']
    by = F['by_district']
    assert F['rows'] == 720 and F['n_ready'] == 576 and F['n_train'] == 432 and F['n_test'] == 144
    assert F['peak_m'] == 12 and F['trough_m'] == 9 and F['model_mae'] < F['naive_mae']
    pct_rel = F['model_rel']
    # ---- code snippets that are shown on slides are executed here, and their real printed output is shown
    code_lag = ("clinic = clinic.sort_values(['district', 'month'])\n"
                "g = clinic.groupby('district')\n"
                "clinic['cases_lag1'] = g.malaria_cases.shift(1)\n"
                "clinic['cases_lag12'] = g.malaria_cases.shift(12)\n"
                "clinic['rain_lag1'] = g.rainfall_mm.shift(1)\n"
                "features = ['cases_lag1', 'cases_lag12', 'rain_lag1']\n"
                "ready = clinic.dropna(subset=features)\n"
                "train = ready[ready.month < '2025-01-01']\n"
                "test = ready[ready.month >= '2025-01-01']\n"
                "print(len(clinic), len(ready), len(train), len(test))")
    out_lag, ns = run_snippet(code_lag)
    assert out_lag == '720 576 432 144'
    code_fit = ("X_train = np.c_[np.ones(len(train)), train[features]]\n"
                "y_train = train.malaria_cases\n"
                "coef = np.linalg.lstsq(X_train, y_train,\n"
                "                       rcond=None)[0]\n"
                "X_test = np.c_[np.ones(len(test)), test[features]]\n"
                "y_pred = X_test @ coef\n"
                "y_test = test.malaria_cases\n"
                "baseline_mae = abs(y_test - test.cases_lag12).mean()\n"
                "model_mae = abs(y_test - y_pred).mean()\n"
                "print('baseline', round(baseline_mae, 1))\n"
                "print('model   ', round(model_mae, 1))")
    out_fit, ns = run_snippet(code_fit, ns)
    assert out_fit == f'baseline {f1(nm)}\nmodel    {f1(mm)}', out_fit
    code_pipe = ("from sklearn.pipeline import make_pipeline\n"
                 "from sklearn.impute import SimpleImputer\n"
                 "from sklearn.preprocessing import StandardScaler\n"
                 "from sklearn.linear_model import LinearRegression\n"
                 "pipe = make_pipeline(SimpleImputer(strategy='median'),\n"
                 "                     StandardScaler(),\n"
                 "                     LinearRegression())\n"
                 "pipe.fit(train[features], train.malaria_cases)\n"
                 "y_pipe = pipe.predict(test[features])\n"
                 "print(round(abs(y_test - y_pipe).mean(), 1))")
    out_pipe, ns = run_snippet(code_pipe, ns)
    assert out_pipe == f1(mm), out_pipe
    gl = c[c.district == 'Gulu'].reset_index(drop=True)

    def lagrow(i):
        r = gl.iloc[i]
        l1 = '' if pd.isna(r.cases_lag1) else str(int(r.cases_lag1))
        l12 = '' if pd.isna(r.cases_lag12) else str(int(r.cases_lag12))
        return [r.month.strftime('%Y-%m'), str(int(r.malaria_cases)), l1, l12]
    lag_rows = [lagrow(0), lagrow(11), lagrow(12), lagrow(13)]
    assert lag_rows[2][3] == lag_rows[0][1] and lag_rows[3][2] == lag_rows[2][1]
    first4 = [[r.month.strftime('%Y-%m'), str(r.rainfall_mm), str(int(r.malaria_cases))] for r in gl.head(4).itertuples()]
    bw = F['by_district']
    pick = ['Gulu', 'Mbarara', 'Mukono', 'Jinja', 'Kabale', 'Kampala']
    hz = dict(F['horizon'])
    walk = F['walk']
    gulu_first, prev = F['gulu_first'], F['prev_row']
    peak, trough = F['peak_v'], F['trough_v']

    sess = dict(
        num=19, block='Module D: Machine learning', short_title='Forecasting and a first end-to-end model',
        title='Forecasting and a first end-to-end model: baseline, time-based split and Pipeline',
        question='How do we predict next month, and how do we pack a whole modelling job into one object we can trust?',
        outcomes=['Split a time series by date and explain why a random split leaks the future',
                  'Beat a seasonal naive baseline with lag features and report the error in cases (MAE, RMSE, MAPE)',
                  'Build a scikit-learn Pipeline and write your Project milestone 3 result in three sentences'],
        outcome_icons=['calendar', 'chart', 'gear'],
        outcome_note=('Here is what you can do by the end of today. You can split a time series by date, and you can explain why a random split lets the model peek at the future. '
                      'You can beat a seasonal naive baseline using lag features, and report the error in cases with three measures: MAE, RMSE and MAPE. '
                      'And you can pack the whole job into a scikit-learn Pipeline and write your Project milestone 3 result in three sentences. We use the District Clinics file, twelve districts and five years of malaria cases.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: time series, baseline, split, lags, error, Pipeline'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: forecasting ideas first, then the Project milestone 3 lab',
        plan_caption='Ideas with pictures first. Then you open the notebook, forecast 2025 and write your result.',
        plan_note=('We have two hours, and today produces Project milestone 3. The first ten minutes bring back Session 18 and set the question. Then forty-five minutes of concepts with laptops closed: what a time series is, the baseline you must beat, '
                   'the split by date, lag features, the three error measures, and the Pipeline. After a ten minute break you open the notebook for a forty-five minute lab. You forecast 2025 for twelve districts and write your result. '
                   'The last ten minutes are the exit check and what you keep.'),
        recall_from='Session 18',
        recall=[('What is learning without a target variable called, and how did we judge the customer segments?', 'Unsupervised learning. With no right answer to check, we judged each cluster by whether it could be described in business words and acted on.'),
                ('Why did we standardise the variables before running k-means?', 'k-means works with distances. A variable in large units, such as spend in UGX, would swamp a variable in small units, such as visits.'),
                ('What does the elbow method plot, and what do you look for?', 'The inertia (within-cluster sum of squares) for each k. You look for the bend where another cluster stops reducing it much.')],
        words=[('Time series (trend, seasonality, noise)', 'One variable recorded at regular times, such as cases each month. It splits into a slow trend, a yearly seasonality and leftover noise.'),
               ('Baseline model (seasonal naive forecast)', 'The simplest forecast: copy the same month from last year. A model must beat it to be worth using.'),
               ('Time-based split (temporal split)', 'Train on the months before a cut date and test on the months after it. Never split a time series at random.'),
               ('Lag feature', 'An earlier value placed in the same row, such as last month\'s cases. It is built inside each district.'),
               ('Pipeline (scikit-learn)', 'Preprocessing steps and a model packed into one object, so training and test records go through the same steps.')],
        word_icons=['calendar', 'flag', 'clock', 'grid', 'gear'],
        words_note=('Five words for today. A time series is one variable recorded at regular times, and it has a trend, a seasonality and noise. A baseline model is the simplest forecast, and ours copies the same month from last year. '
                    'A time-based split trains on the past and tests on the future. A lag feature puts an earlier value into the same row. And a Pipeline packs the preprocessing and the model into one object. We use every one of them today.'),
        keep='Keep your Project milestone 3 notebook: a baseline, a model tested on 2025, the error in cases with MAE, RMSE and MAPE, a Pipeline, and three sentences for a district manager.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A forecast notebook'), dict(label='The key test', value='Model beats the baseline'), dict(label='Next session', value='Neural networks')]),
        keep_title='Save your notebook: it is your Project milestone 3',
        next='Session 20: Neural networks and deep learning. One neuron and a training loop in numpy, then a network against a forest.', next_label='Next session',
        keep_note=('Before you go, save the notebook and the results file it wrote. Together they are your Project milestone 3, which you show me for feedback and nobody scores: a baseline, a model tested on months it never saw, the error in cases, and your three sentences. '
                   'If a district manager could read those three sentences and decide how much stock to hold, they are good. Next session we meet neural networks, and the test you learned today still applies: a network must beat the baseline too.'),
        cover_note=('Welcome back. For five sessions you have built models that predict a label or a number from a table. Today the table has a calendar in it, and one rule changes completely: the future is hidden, and a fair test must hide it too. '
                    'We forecast malaria cases for twelve districts, we meet the baseline that every model must beat, and we pack the whole job into one object called a Pipeline. Today is Project milestone 3, and the result you build goes into your course project.'),
        use_at_work='Forecast next month with a baseline and a lag model, test it by date, and report the error in the units of the business.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 18', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['pin', 'chart', 'magnifier'],
                  notes=('Here are the answers to the three warm-up questions. Learning without a target variable is unsupervised learning. Because there was no right answer to check against, we judged each cluster by whether we could describe it in business words and act on it. '
                         'We standardised before k-means because it works with distances, and a variable in large units would swamp one in small units. And the elbow method plots the inertia for each k, and we look for the bend. '
                         'Today the answers come back in a new form: we will predict a number that we can check against what really happened. Which of the three did you find hardest?')))

    # 2 time series data
    S.append(dict(kind='idea', title='A time series is one variable recorded at regular times: here 60 months for 12 districts',
                  visual=dict(kind='sheet', headers=['month', 'rainfall_mm', 'malaria_cases'], rows=first4, hl=[0, 2], size=17),
                  lead='A time series is a variable recorded at regular times, in time order.',
                  points=[f'Each record is one district in one month: {n(F["rows"])} records from clinic_visits.csv.', f'The picture shows the first months of Gulu, from {first4[0][0]}.', 'Forecasting means predicting the next values of the series.'],
                  notes=(f'Our data for today is the District Clinics file. Each record is one district in one month, and there are {F["districts"]} districts and {F["months"]} months, January 2021 to December 2025, so {n(F["rows"])} records. '
                         'The picture shows the first four months of Gulu. The variable we want to predict is malaria cases, the gold cell. A variable recorded at regular times and kept in time order is called a time series. '
                         'In Excel it is a column of monthly figures with the dates beside it. Forecasting means predicting the next values of that column. What would you want to forecast in your own work?')))

    # 3 decomposition
    S.append(dict(kind='wide', title='A time series splits into trend, seasonality and noise (decomposition)',
                  visual=dict(kind='dsj_decomp', observed=[float(v) for v in F['dec_observed']], trend=[float(v) for v in F['dec_trend']], season=[float(v) for v in F['dec_season']], noise=[float(v) for v in F['dec_noise']], year_ticks=yt),
                  caption=f'All 12 districts added up. Trend: about {n(F["dec_slope"])} more cases a month. Noise: the rest.',
                  notes=(f'Here is the total of all twelve districts, pulled apart into three pieces. This is called a decomposition. The trend is the slow drift. I fitted a straight line to it, and it rises by about {n(F["dec_slope"])} cases each month. '
                         f'The seasonality is the shape that repeats every year, and it moves the total by about {n(F["season_range"])} cases from its lowest month to its highest. The noise is what is left over, and no model can predict it. '
                         'A forecast can use the trend and the seasonality. It can never use the noise. Which of the three would a manager find most useful?')))

    # 4 seasonality
    S.append(dict(kind='wide', title='Seasonality repeats every year: December is the peak and September is the trough',
                  visual=dict(kind='dsj_columns', labels=MONTHS, values=[int(v) for v in F['by_cal_month']], hl=[F['peak_m'] - 1]),
                  caption='Cases of all 12 districts over five years, added for each calendar month. Gold: the peak.',
                  notes=(f'This picture adds every January of the five years into one column, every February into the next, and so on. December is the tallest at {n(peak)} cases, the gold column. September is the lowest at {n(trough)}. '
                         'The columns are far from equal: April to June and October to December are higher than the months around them. That repeating shape is seasonality, and it is what makes forecasting possible. '
                         'If every month looked the same, last month would tell us everything. Because the year has a shape, the same month a year ago is already a decent guess. What seasonal pattern do you see in your own work?')))

    # 5 horizon
    S.append(dict(kind='wide', title='The forecast horizon is how far ahead you predict',
                  visual=dict(kind='dsj_horizon'),
                  caption='Horizon: months between the last month you know and the month you predict. Today: horizon 1.',
                  notes=('Every forecast has a forecast horizon, the number of months between the last month you know and the month you want to predict. The black squares are the months you know. The red line is today. '
                         'Horizon 1 means next month. Horizon 3 means three months ahead, and horizon 12 means a whole year ahead. The horizon matters because a forecast gets harder the further ahead you look, and later we measure by how much. '
                         'Today we forecast with horizon 1, and the lab makes you say so in your report. What horizon would a pharmacy stock planner need?')))

    # 6 seasonal naive
    mbser = [float(v) for v in c[c.district == 'Mbarara'].sort_values('month').malaria_cases]
    S.append(dict(kind='wide', title='The baseline model is a seasonal naive forecast: copy the same month from last year',
                  visual=dict(kind='dsj_lines', series=[dict(name='Actual cases in Mbarara', values=mbser, color='ink'), dict(name='Seasonal naive forecast for 2025', values=[None] * 48 + [float(v) for v in F['mb_naive']], color='red', dash=True)],
                              ticks=[(0, 'Jan 2021'), (12, 'Jan 2022'), (24, 'Jan 2023'), (36, 'Jan 2024'), (48, 'Jan 2025')], cut=48, cut_label='history|forecast', ylabel='cases per month', yticks=[2000, 3000, 4000, 5000], ymin=1500),
                  caption=f'Forecast for January 2025 = January 2024. Mbarara 2025: average miss {n(F["mb_mae"])} cases.',
                  notes=('Before any clever model, we build the baseline model, the simplest forecast that could work. The seasonal naive forecast copies the same month from last year. So January 2025 is predicted by January 2024. '
                         'In Excel it is a formula that points twelve rows up. The picture shows Mbarara. The black line is what happened, and the dashed red line is the copy of the year before. '
                         f'It follows the shape, but it misses the peaks. The average miss for Mbarara in 2025 is {n(F["mb_mae"])} cases a month. Every model we build today must beat this baseline, or it is not worth using.')))

    # 7 MAE formula
    S.append(dict(kind='formula', title='Mean absolute error (MAE) is the average size of the errors, in cases',
                  formulas=[('Definition', r'$\mathrm{MAE} = \frac{1}{n}\sum_{i=1}^{n}\left|\,y_i-\hat{y}_i\,\right|$'), ('Mbarara 2025, n = 12', r'$\mathrm{MAE} = \frac{' + f'{int(F["mb_abs_sum"]):,}'.replace(',', '{,}') + r'}{12} = ' + f'{F["mb_mae"]:.2f}' + r'$')],
                  symbols=[['n', 'How many forecasts are scored.', '12 months of 2025'], ['y_i', 'The actual value for month i.', f'Mbarara, January 2025: {n(F["mb_actual"][0])} cases'], ['ŷ_i (y-hat)', 'The forecast for month i.', f'Mbarara, January 2025: {n(F["mb_naive"][0])} cases'],
                           ['| |', 'Absolute value: drop the sign.', f'January miss: {F["mb_err_first3"][0]}']],
                  size=20, note=f'MAE is in the unit of the target: cases. The sum of the 12 absolute errors is {int(F["mb_abs_sum"]):,}.',
                  notes=(f'Now we need a number for how wrong a forecast is. The mean absolute error, MAE, takes each miss, which is actual minus forecast, drops the sign, and averages. The symbol y is the actual value and y-hat is the forecast. '
                         f'The bars mean absolute value, so a miss of plus five hundred and a miss of minus five hundred both count as five hundred. For Mbarara the twelve absolute misses add up to {int(F["mb_abs_sum"]):,}. Divide by twelve and the MAE is {F["mb_mae"]:.2f} cases. '
                         'The great advantage is the unit. A manager hears cases and understands. Why would we drop the sign before averaging?')))

    # 8 three measures
    S.append(dict(kind='table', title='MAE, RMSE and MAPE are three ways to score the same forecast',
                  headers=['Measure', 'How it is computed', 'Unit', 'Baseline', 'Lag model'],
                  rows=[['MAE', 'Average of |actual minus forecast|', 'cases', f1(nm), f1(mm)], ['RMSE (root mean squared error)', 'Square each miss, average, take the square root. Big misses count more.', 'cases', f1(F['naive_rmse']), f1(F['model_rmse'])],
                        ['MAPE (mean absolute percentage error)', 'Average of |miss| divided by actual, times 100', 'percent', f1(F['naive_mape']), f1(F['model_mape'])]],
                  widths=[3.0, 4.0, 1.6, 1.5, 1.6], icons=['calculator', 'chart', 'coin'], note=f'Scores on the {F["n_test"]} district-months of 2025. MAPE cannot be used when an actual value can be 0.',
                  notes=(f'Three scores for one forecast. MAE is the average miss in cases. RMSE squares each miss, averages, and takes the square root, so one large miss hurts it far more than many small ones. '
                         f'MAPE divides each miss by the actual value, so it gives a percentage, and it fails when an actual value can be zero. On the 2025 test the baseline scores {f1(nm)} on MAE, {f1(F["naive_rmse"])} on RMSE and {f1(F["naive_mape"])} percent on MAPE. '
                         f'The lag model, which we build in a moment, scores {f1(mm)}, {f1(F["model_rmse"])} and {f1(F["model_mape"])}. Which would you report to a manager, and which to a data team?')))

    # 9 time split
    rng = np.random.default_rng(1)
    test_idx = sorted(int(i) for i in rng.choice(60, 12, replace=False))
    S.append(dict(kind='wide', title='A time-based split trains on the past and tests on the future',
                  visual=dict(kind='dsj_timesplit', test_idx=test_idx, year_ticks=yt, left_title='Random split: wrong for a time series', right_title='Time-based split (temporal split): cut at 1 January 2025',
                              note_left='Some training months come after the test months, so the model has seen the future.', note_right=f'Train on the {F["n_train"]} records of 2022 to 2024. Test on the {F["n_test"]} records of 2025.'),
                  caption='Next month always lies after everything you know, so the test must too.',
                  notes=('In Session 14 you split the loans at random. A time series changes the rule. The split must follow the calendar. In the top strip the test months, in gold, are scattered, so some training months come after the test months. '
                         f'The model has seen the future. In the bottom strip we cut at the first of January 2025. We train on the earlier months and test on the {F["n_test"]} records of 2025. '
                         'That is a time-based split, also called a temporal split. It copies real life, because next month always lies after everything you know. Why does a scattered test set look unfair to you?')))

    # 10 leakage compare
    S.append(dict(kind='compare', title='Data leakage from the future flatters a score',
                  left=dict(head='Looks ahead (leaks)', points=[f'A random split moved MAE only a little here ({f1(F["random_mae"])} against {f1(mm)}), but trend raises the risk.', f'A shift(-1) feature holds next month: MAE falls from {f1(F["leak_honest_mae"])} to {f1(F["leak_mae"])}.']),
                  right=dict(head='Safe', points=['Cut at a date: train before, test after.', 'Use the past only: shift(1) or more.']),
                  verdict='A feature absent on forecast day must go.',
                  notes=('Data leakage means information from outside the training period slips into the model. Two forms matter for a time series. A random split puts later months in the training set. And a feature built with shift minus one holds next month, which you will never know on the day you forecast. '
                         f'Look at the number. On one random split, adding that next-month feature cuts the MAE from {f1(F["leak_honest_mae"])} to {f1(F["leak_mae"])}. That looks like progress, but it is borrowed from the future. '
                         f'Notice also that our simple linear model scores {f1(F["random_mae"])} on a random split and {f1(mm)} on the date split, almost the same. Nothing warns you, which is why we follow the rule. These numbers come from one seeded split and are not in the lab. Which feature in your own data might look ahead?')))

    # 11 scatter lag
    S.append(dict(kind='wide', title=f'Last month\'s rain relates to malaria cases (r={F["r_rain_lag1"]:.2f}) but this month\'s rain does not (r={F["r_rain_now"]:.2f})',
                  visual=dict(kind='dsj_scatter2', panels=[dict(title='Rain in the same month', points=F['scatter_now'], xlabel='rainfall (mm)', r_label=f'r = {F["r_rain_now"]:.2f}', line=F['line_now']),
                                                           dict(title='Rain in the month before', points=F['scatter_lag'], xlabel='rainfall one month earlier (mm)', r_label=f'r = {F["r_rain_lag1"]:.2f}', line=F['line_lag'])]),
                  caption=f'Each dot is one district-month ({F["n_ready"]} in all). r is the Pearson correlation.',
                  notes=(f'Why would we bring earlier values into a row? Look at rain. On the left, each dot is one district in one month, {F["n_ready"]} dots, with rainfall in the same month. The correlation is {F["r_rain_now"]:.2f}, almost nothing. '
                         f'On the right, the same cases against the rainfall of the month before. The correlation is {F["r_rain_lag1"]:.2f}, and the red line clearly climbs. The effect of rain comes with a delay, and a plausible reason is that standing water needs time to produce mosquitoes. '
                         'A model that sees only this month\'s rain would miss it. A model that is given last month\'s rain finds it. What delayed effect exists in your own work?')))

    # 12 lag feature
    S.append(dict(kind='idea', title='A lag feature puts an earlier value into the same row',
                  visual=dict(kind='sheet', headers=['month', 'malaria_cases', 'cases_lag1', 'cases_lag12'], rows=lag_rows, hl=[2, 3], size=16),
                  lead='A lag feature is the value of a variable some months earlier, in the same record.',
                  points=['cases_lag1 is last month. cases_lag12 is the same month last year.', f'Gulu, {lag_rows[2][0]}: the lag 12 value {lag_rows[2][3]} is the cases of {lag_rows[0][0]}.', 'The first rows have no lag, so they are blank.'],
                  notes=('A lag feature is the value of a variable some months earlier, placed in the same record. In the picture, cases lag one is last month and cases lag twelve is the same month last year. '
                         f'Look at the gold cell. For Gulu in {lag_rows[2][0]}, the lag twelve value is {lag_rows[2][3]}, which is the cases of {lag_rows[0][0]}, a year earlier. In Excel you would type equals B2 one row down. In pandas it is the shift function. '
                         'The first rows of each district have no earlier value, so they are blank. Why would we need to throw those rows away before fitting?')))

    # 13 lag trap
    S.append(dict(kind='wide', title='A lag built without groupby borrows values from the district above it',
                  visual=dict(kind='ds_flagged_sheet', headers=['district', 'month', 'malaria_cases', 'cases_lag1'],
                              rows=[[prev.district, prev.month.strftime('%Y-%m'), str(int(prev.malaria_cases)), ''], [gulu_first.district, gulu_first.month.strftime('%Y-%m'), str(int(gulu_first.malaria_cases)), str(F['gulu_bad_lag1'])],
                                    ['Gulu', gl.iloc[1].month.strftime('%Y-%m'), str(int(gl.iloc[1].malaria_cases)), str(int(gulu_first.malaria_cases))]],
                              flags=[[1, 3, f'Shifting the whole column gives Gulu a lag of {F["gulu_bad_lag1"]}: the December 2025 cases of Fort Portal. Gulu has no earlier month, so it should be blank.']]),
                  caption=f'Without groupby: {F["bad_first_rows"]} wrong lag 1 and {F["bad_lag12_rows"]} wrong lag 12 values. Test MAE {f1(F["bad_mae"])}.',
                  notes=(f'This trap raises no error. The file is stacked, one district after another, sorted by district and month. If you shift the whole column, the first month of Gulu receives the last month of the district above it. '
                         f'Here that is {F["gulu_bad_lag1"]}, the December 2025 cases of Fort Portal. Across the file, {F["bad_first_rows"]} districts get a wrong lag one and {F["bad_lag12_rows"]} records get a wrong lag twelve. '
                         f'On our data the test MAE becomes {f1(F["bad_mae"])} instead of {f1(mm)}. The cure is to group by district before you shift, and to check one first row by hand. Why does Python give no warning?')))

    # 14 row counts
    S.append(dict(kind='table', title=f'Lag features cost records: {F["rows"]} become {F["n_ready"]}, then {F["n_train"]} to train and {F["n_test"]} to test',
                  headers=['Step', 'Records', 'Why'],
                  rows=[['All records in clinic_visits.csv', str(F['rows']), '12 districts times 60 months'], ['Records with every lag feature', str(F['n_ready']), f'The first 12 months of each district have no lag 12: {F["n_lost"]} lost'],
                        ['Training set: January 2022 to December 2024', str(F['n_train']), '12 districts times 36 months'], ['Test set: January 2025 to December 2025', str(F['n_test']), '12 districts times 12 months']],
                  widths=[5.0, 1.6, 5.4], icons=['grid', 'cross', 'calendar', 'flag'], note='Lost rows are an expected cost. A lag needs history.',
                  notes=(f'Lag features cost records. We start with {F["rows"]}, twelve districts times sixty months. A lag of twelve months needs a year of history, so the first twelve months of each district have no value, and {F["n_lost"]} records drop out. '
                         f'That leaves {F["n_ready"]}. We cut at the first of January 2025. The training set is twenty twenty-two to twenty twenty-four, {F["n_train"]} records, and the test set is the twelve months of 2025, {F["n_test"]} records. '
                         'Dropping the early rows is a normal cost of the method. A lag simply needs history. Check these counts in the lab, because every later number depends on them. How many records would you keep if the lag were 24 months?')))

    # 15 code lag and split
    S.append(dict(kind='code', title='Read the recipe: lag features inside each district, then a split at the cut date',
                  code=code_lag, output=out_lag.split('\n'),
                  reads=['Line 1 sorts by district and month. Line 2 groups by district, so every shift stays inside one district.', 'Lines 3 to 5 build the three lag features.', 'Line 7 drops the records that have no lag.', 'Lines 8 and 9 cut at 1 January 2025.', f'The four counts: {F["rows"]}, {F["n_ready"]}, {F["n_train"]} and {F["n_test"]}.'],
                  notes=('Read this recipe before the lab. Line one sorts the records by district and month, and line two groups them by district, so every shift stays inside one district. Lines three to five build the three lag features: last month\'s cases, the cases of the same month last year, and last month\'s rainfall. '
                         'Line seven drops the records that have no lag. Lines eight and nine cut the calendar at the first of January 2025. The last line prints four counts, and the output is real, from the clinic file. '
                         f'{F["rows"]}, then {F["n_ready"]}, then {F["n_train"]} and {F["n_test"]}. These match the table you just saw. Which line would you change for a lag of two months?')))

    # 16 code fit
    S.append(dict(kind='code', title='Fit on the past, test on 2025: the lag model beats the baseline',
                  code=code_fit, output=out_fit.split('\n'),
                  reads=['Lines 1 to 3 fit a linear regression with numpy, using only the training set.', 'The coefficients are the intercept and one weight for each lag feature.', 'y_pred holds the forecast for each test record.', f'The baseline misses by {f1(nm)} cases on average. The model misses by {f1(mm)}.'],
                  notes=('Now we fit. The first three lines fit a linear regression with numpy, using only the training set, and then predict the test set. The model is the intercept plus a weight for each lag feature. '
                         f'The last two lines score the baseline and the model on the 2025 test, as the average absolute miss in cases. The baseline misses by {f1(nm)} cases a month on average. The lag model misses by {f1(mm)}. '
                         f'That is {F["gain_pct"]:.0f} percent smaller. The printed numbers are real output from the clinic file. Does a smaller number alone tell you the model is good enough? I will answer that in a moment.')))

    # 17 stat
    S.append(dict(kind='stat', title=f'Judge the error in cases: an average miss of {n(mm)} is {pct_rel:.0f} percent of a typical month', big=f'{pct_rel:.0f}%',
                  text=f'The lag model misses by {f1(mm)} cases on average. The mean district-month in 2025 had {n(F["y_mean"])} cases. The baseline misses by {F["naive_rel"]:.0f} percent of that.',
                  waffle_label='percent of a typical month is the average miss',
                  notes=(f'A score only matters in the unit of the decision. The lag model misses by {f1(mm)} cases on average, and the mean district month in 2025 had {n(F["y_mean"])} cases. So the average miss is about {pct_rel:.0f} percent of that. This differs from the MAPE of 16.3 percent, because MAPE averages the percentage miss of each month and small months weigh more. '
                         f'The baseline misses by about {F["naive_rel"]:.0f} percent. A district manager can plan stock around that: keep enough medicine for about {n(mm)} more cases than you expect. '
                         'One caution. It is an average, so some months and districts miss by much more, and we say that when we report. How would you phrase this for a manager in one sentence?')))

    # 18 district table
    rows = [[d, n(bw.loc[d, 'mean_cases']), n(bw.loc[d, 'naive']), n(bw.loc[d, 'model']), 'Model' if bw.loc[d, 'model'] < bw.loc[d, 'naive'] else 'Baseline'] for d in pick]
    S.append(dict(kind='table', title='The model beats the baseline on average but not in every district',
                  headers=['District', 'Typical month (cases)', 'Baseline MAE', 'Model MAE', 'Lower error'], rows=rows, widths=[2.6, 2.9, 2.2, 2.0, 2.2], icons=['clinic'] * 6,
                  note=f'The model has the lower error in {F["districts_model_wins"]} of 12 districts and in {F["model_wins"]} of {F["n_test"]} district-months. Always look below the average.',
                  notes=(f'An average hides differences. Here are six districts, with the typical monthly cases and the MAE of the baseline and of the model. In Gulu, Mbarara and Mukono the model is clearly better. '
                         f'In Jinja, Kabale and Kampala the baseline wins. Those are the districts with fewer cases, where the baseline already misses by little. Over all twelve districts the model has the lower error in {F["districts_model_wins"]}, and in {F["model_wins"]} of the {F["n_test"]} district months. '
                         'So the honest report says the model is better on average, and it names where it is not. Why might a simple copy work well for a small district?')))

    # 19 horizon table
    S.append(dict(kind='table', title='The longer the horizon, the weaker the model: at 12 months it loses to the baseline',
                  headers=['Horizon', 'Features used', 'Model MAE', 'Baseline MAE', 'Result'],
                  rows=[[f'{h} month' + ('s' if h > 1 else ''), ('cases and rain h months back, and cases 12 months back' if h < 12 else 'cases and rain 12 months back'), f1(hz[h]), f1(nm), 'Model better' if hz[h] < nm else 'Baseline better'] for h in (1, 3, 6, 12)],
                  widths=[1.6, 4.4, 1.6, 1.8, 2.0], icons=['clock'] * 4, note='Each row refits the model with lags that are known h months ahead. Same train and test split.',
                  notes=(f'The forecast horizon changes the answer. For horizon one, we know last month, so the model uses it, and the MAE is {f1(hz[1])}. For horizon three, the most recent month we know is three months back, so the model has to use older lags, and the MAE rises to {f1(hz[3])}. '
                         f'At six months it is {f1(hz[6])}, lower than at three months, so the loss of skill is not a straight line. At twelve months the model has only the year-old values, and the MAE is {f1(hz[12])}, which is worse than the baseline of {f1(nm)}. '
                         'The lesson is to state the horizon with every forecast. Which horizon does your own decision need?')))

    # 20 walk-forward
    S.append(dict(kind='table', title='Walk-forward validation repeats the cut date, so one lucky year cannot fool you',
                  headers=['Cut date', 'Train records', 'Test year', 'Baseline MAE', 'Model MAE'],
                  rows=[[f'1 January {y}', str(a), str(y), f1(nb), f1(mo)] for (y, a, b_, nb, mo) in walk], widths=[2.6, 2.2, 1.8, 2.6, 2.4], icons=['calendar'] * 3,
                  note='Walk-forward validation (expanding window). In scikit-learn the same idea is TimeSeriesSplit.',
                  notes=(f'One test year is a single test. Walk-forward validation repeats it. We cut at the first of January 2023, train on the {walk[0][1]} records of 2022, and test on 2023. Then we move the cut to 2024, train on {walk[1][1]} records, and test on 2024. '
                         f'Then the cut for 2025, the one we used, trains on {walk[2][1]}. The model wins in all three years: {f1(walk[0][4])}, {f1(walk[1][4])} and {f1(walk[2][4])} against baselines of {f1(walk[0][3])}, {f1(walk[1][3])} and {f1(walk[2][3])}. '
                         'That makes the result far more believable than one year alone. Would you trust a model that won in only one of three years?')))

    # 21 pipeline concept
    S.append(dict(kind='wide', title='A Pipeline packs preprocessing and the model into one object',
                  visual=dict(kind='dsj_pipeline', steps=[dict(name='SimpleImputer', text='fills a blank with the training median'), dict(name='StandardScaler', text='rescales each variable with the training mean'), dict(name='LinearRegression', text='fits the model')],
                              fit_text='fit(X_train, y_train): every step learns only from the training records.', predict_text='predict(X_test): the same steps run on the test records. Nothing is re-learned.'),
                  caption='One object to fit, one to predict, one to save. It also stops test records leaking into the preprocessing.',
                  notes=('So far we did each step by hand. That works, but it is easy to forget a step on the test data, or to run the steps in another order next month. A Pipeline fixes that. It is a list of steps that always run in the same order. '
                         'Here the steps are an imputer that fills blanks with the median, a scaler that standardises each variable, and the linear regression. When you call fit, each step learns only from the training records. When you call predict, the same steps run on the test records. '
                         'In Excel it is a recorded macro you can run again on next month\'s file. Which steps would your own pipeline need?')))

    # 22 pipeline code
    S.append(dict(kind='code', title='Read the recipe: a scikit-learn Pipeline gives the same forecast in a few lines',
                  code=code_pipe, output=out_pipe.split('\n'),
                  reads=['make_pipeline chains the three steps in order.', 'fit learns the median, the mean and the weights from the training records only.', 'predict runs the same steps on the test records.', f'The MAE is {f1(mm)}, the same as the numpy fit: standardising does not change a linear regression forecast.'],
                  notes=('Here is the recipe. Make pipeline chains the three steps in order. The fit line learns the median, the mean and the weights from the training records only. The predict line runs the same steps on the test records. '
                         f'The printed MAE is {f1(mm)}, exactly the number we got with numpy. That is a useful check: scaling the variables does not change what a linear regression forecasts, so the two methods must agree, and they do. '
                         'The real work of a Pipeline shows when you add steps, as you will see shortly. Why is it good news that two different methods agree?')))

    # 23 district indicators
    S.append(dict(kind='table', title=f'Adding the district as indicator variables lowers the MAE from {n(mm)} to {n(F["pipe_mae"])}',
                  headers=['Model', 'Variables', 'MAE (cases)'],
                  rows=[['Pipeline on three lag features', '3', f1(mm)], ['Same Pipeline with 11 district indicator variables', str(F['n_pipe_feats']), f1(F['pipe_mae'])]],
                  widths=[6.0, 2.6, 3.0], icons=['gear', 'clinic'],
                  note='One-hot encoding: district becomes 0/1 indicator (dummy) variables. Drop one district to avoid the dummy variable trap. In scikit-learn: ColumnTransformer and OneHotEncoder.',
                  notes=(f'Districts differ a lot in size. Kampala has about {n(by.loc["Kampala", "mean_cases"])} cases in a typical month and Mukono about {n(by.loc["Mukono", "mean_cases"])}. If the model also knows which district it is forecasting, it can correct for that. '
                         f'We add the district as indicator variables, columns of zero and one, which is called one-hot encoding. Eleven columns plus the three lags make {F["n_pipe_feats"]} variables, and the MAE falls from {f1(mm)} to {f1(F["pipe_mae"])}. '
                         'In scikit-learn the encoding goes inside the Pipeline with a ColumnTransformer and a OneHotEncoder. In the lab we create the columns with pandas, which gives the same forecast. Which variable would you add for your own district?')))

    # 24 use at work
    S.append(dict(kind='table', title='Where you will use this at work: forecast next month, then say how wrong you may be',
                  headers=['Your job', 'The series you meet', 'What today lets you do'],
                  rows=[['Records officer at a district health office, using Excel and pandas', 'Malaria or clinic cases per district per month', 'Forecast next month and tell the pharmacy how many extra cases to stock for.'],
                        ['Sales analyst at a retail chain', 'Weekly orders per branch (Lakeside Mart style)', 'Forecast next week with a baseline and a lag model, tested by date.'],
                        ['Credit analyst at a microfinance institution', 'Monthly collections or repayments', 'Check that no feature looks ahead before you report a score.'],
                        ['Analyst at a mobile money agent network', 'Daily or weekly transactions (illustrative)', 'Package preparation and model in a Pipeline you can rerun every month.']],
                  widths=[3.8, 3.6, 4.6], icons=['clinic', 'chart', 'coin', 'phone'],
                  notes=('Where will you use this on Monday? Four examples. A records officer at a district health office who uses Excel or pandas can forecast next month\'s cases and tell the pharmacy how many extra cases to stock for. '
                         'A sales analyst at a retail chain can forecast next week\'s orders for each branch and test the forecast by date. A credit analyst at a microfinance institution can check that no feature looks ahead before reporting a score. '
                         'And an analyst at a mobile money agent network can wrap the work in a Pipeline and rerun it every month. Which of these is closest to your job?')))

    # 25 course project timeline
    S.append(dict(kind='wide', title='Course project timeline: today is the baseline and tested model',
                  visual=dict(kind='timeline', items=[dict(when='Session 13', what='Write and scope the question'), dict(when='Session 14', what='Choose the dataset'), dict(when='Session 19', what='Baseline and tested model', hl=True),
                                                      dict(when='Session 23', what='Learn to publish an app and a model card'), dict(when='Session 24', what='Present for ten minutes')]),
                  caption='Milestone 3: baseline, unseen-record score, error in business units.',
                  notes=('This is the course project timeline, and today is the third step. In Session 13 you scoped your question and in Session 14 you chose your dataset. Today, in Session 19, you build a baseline and a tested model, and that is Project milestone 3. '
                         'In Session 23 you learn to publish an app and write a model card on the loans, and you apply it to your own course project at home before Session 24, where you present for ten minutes. A tested model means three things: a baseline, a score on records the model never saw, split by date if your data has a calendar, and an error in the units of your business. '
                         'Today\'s lab shows the pattern on the clinic file. Your course project needs the same three moves on your own dataset. Which of the three will take you longest?')))

    # 26 divider
    S.append(dict(kind='divider', title='Part 2: the forecasting lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. Open the Session 19 notebook in Google Colab and run the setup cell first. '
                         'In every task, predict the answer first and write your guess in the notebook. Then run the cell, read the output, and change one thing. The checks tell you whether a number is right. '
                         'This lab produces Project milestone 3, so please do not skip the final cell with your three sentences. I will walk around.')))

    # 27 lab map
    S.append(dict(kind='steps', title='The lab has five parts and ends with your Project milestone 3 results file',
                  steps=[dict(head='1 Load', text='Sort by district and month', icon='folder'), dict(head='2 Baseline', text='Seasonal naive for Gulu and Kampala', icon='flag'), dict(head='3 Lags and split', text='Inside each district, cut at 2025', icon='calendar'),
                         dict(head='4 Model', text='Score with MAE, RMSE, MAPE', icon='chart'), dict(head='5 Pipeline', text='Then write three sentences', icon='gear')], highlight=None,
                  caption='Predict, run, read, change one thing. Automatic checks tell you when a number is right. Keep the results file the notebook writes.',
                  notes=('Here is the map of the lab. Step one, load the clinic file and sort it by district and month. Step two, build the seasonal naive baseline for Gulu and for Kampala and compare the two misses. '
                         'Step three, build the lag features inside each district and cut at the first of January 2025. Step four, fit the model and score it with MAE, RMSE and MAPE. '
                         'Step five, build the Pipeline, add the district indicator variables, and write your three sentences. The notebook saves a results file, and that file is what you keep. Please do not skip the predictions.')))

    # 28 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Records in the file, and blank total_visits', f'{F["rows"]} and {F["blank_visits"]}'], ['Gulu baseline MAE, and Kampala baseline MAE in 2025', f'{f1(by.loc["Gulu", "naive"])} and {f1(by.loc["Kampala", "naive"])}'],
                        ['Correlation of cases with this month\'s rain and with last month\'s rain', f'{F["r_rain_now"]:.2f} and {F["r_rain_lag1"]:.2f}'], ['Records with every lag, training records and test records', f'{F["n_ready"]}, {F["n_train"]} and {F["n_test"]}'],
                        ['Baseline MAE, model MAE', f'{f1(nm)} and {f1(mm)}'], ['Model RMSE and model MAPE', f'{f1(F["model_rmse"])} and {f1(F["model_mape"])} percent'], ['MAE with the district indicator variables', f1(F['pipe_mae'])],
                        ['MAE when the lag is built without groupby', f1(F['bad_mae'])]],
                  widths=[7.4, 4.6], icons=['folder', 'flag', 'magnifier', 'calendar', 'chart', 'calculator', 'clinic', 'cross'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The most common cause is a shift without groupby, which gives the wrong lag values, or a sort that is not by district and month. Another is a cut date that puts a month in both sets. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your baseline MAE is smaller than the table says?')))

    # 29 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['Test records are not 144', 'The cut date or the dropna step differs.', 'Use month >= \'2025-01-01\' and drop records missing a lag first.'],
                        ['The model scores worse than the baseline', 'The features or the lag direction are wrong.', 'Check that you used shift(1). A shift(-1) looks ahead. Check the sort order.'],
                        ['NaN in the predictions', 'A lag feature is blank in a test record.', 'Drop the blank records with dropna(subset=features) before you split.'],
                        ['KeyError: \'cases_lag12\'', 'The lag column was not created, or it has another name.', 'Run the lag cell again, and check the spelling.'],
                        ['Your MAE differs from the table by a little', 'A different cut date, features or dropped row.', 'Below 0.1 case is rounding. Larger means other features.']],
                  widths=[3.7, 4.1, 4.2], icons=['cross'] * 5,
                  notes=('Five messages you may meet. A test set that is not 144 records means the cut date or the dropna step is different, so cut at the first of January 2025 and drop the records with a missing lag first. '
                         'If the model is worse than the baseline, check that you used shift one, because shift minus one looks ahead, and that the table is sorted. NaN in the predictions means a blank lag feature reached the test set. '
                         'A KeyError means the lag column was never created. And a tiny difference in the MAE is fine. Read the message first. It usually tells you the answer.')))

    # 30 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A seasonal naive forecast for March 2026 uses which number?', 'The March 2025 value: the same month last year.'],
                        ['Why must a forecast be tested on later months?', 'Next month always lies after the data you have. A random split lets the model see the future, which is data leakage.'],
                        [f'Your model misses by {n(mm)} cases and the baseline by {n(nm)}. What do you tell the manager?', f'It beats the baseline by about {F["gain_pct"]:.0f} percent, with an average miss near {n(mm)} cases at horizon 1, but some districts and months miss by more.']],
                  widths=[5.6, 6.4], icons=['calendar', 'clock', 'people'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, a seasonal naive forecast for March 2026: which number does it use? '
                         'Two, why must a forecast be tested on later months? Three, your model misses by three hundred and thirty eight cases and the baseline by four hundred and sixty one: what do you tell the manager? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 20. If one surprised you, look at that step in your notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 19 notebook in Colab before anyone arrives. Check that clinic_visits.csv is in the notebook folder.',
              'Run the solution notebook once in Colab. It should end with All 19 checks pass. The Pipeline cells use scikit-learn; the authoring sandbox ran them with a NumPy stand-in, so confirm in Colab that the Pipeline MAE equals the numpy MAE.',
              'Write the check table (slide 28) on the board before the lab.', 'Concepts run with laptops closed. Learners open the notebook only after the Part 2 divider.',
              'Remind learners that today produces Project milestone 3 and that the results file the notebook writes is something they keep. Nothing is scored. All data is fictional and generated.'],
        misconceptions=[('A random split is always fine, as I did with the loans', 'For a time series the test must lie after the training period. A random split lets the model see the future.'),
                        ('A bigger model is always better than the seasonal naive baseline', f'The baseline is hard to beat for small districts: it wins in {len(F["districts_naive_wins"])} of 12 districts on this test ({", ".join(F["districts_naive_wins"])}).'),
                        ('shift(1) on the whole column is enough', 'Without groupby the first month of each district borrows from the previous district. Always group by the entity first.'),
                        ('MAPE is better because it is a percentage', 'MAPE breaks when an actual value can be 0 and it punishes forecasts that are too high more than too low. Report MAE with the unit, and say why.'),
                        ('A lower MAE on the test set proves the model is good', 'It is one test year. Walk-forward validation, a look by district and a statement of the horizon make the claim believable.')],
        probes=[('What is the forecast horizon of today\'s model?', 'One month: it uses last month\'s cases and rain, which are known when we forecast.'),
                ('Why are 144 records lost before we fit?', 'A lag of 12 months needs a year of history, so the first 12 months of each of the 12 districts have no lag 12.'),
                ('What is a baseline model for a time series?', 'A seasonal naive forecast: the same month last year.'),
                ('Why did last month\'s rain correlate with cases when this month\'s did not?', f'The effect of rain has a delay (r = {F["r_rain_lag1"]:.2f} against {F["r_rain_now"]:.2f}). A plausible reason is that standing water needs time to produce mosquitoes. This is generated data, so say plausible and avoid saying proven.'),
                ('What does a Pipeline protect you from?', 'Forgetting a preprocessing step on the test records, and learning the median or the mean from the test records.')],
        lab_steps=[('Step 1: load and sort', f'{F["rows"]} records, {F["blank_visits"]} blank total_visits. Sorted by district and month.'), ('Step 2: baseline', f'Gulu {f1(by.loc["Gulu", "naive"])}, Kampala {f1(by.loc["Kampala", "naive"])}. Gulu is far larger, so the miss is larger.'),
                   ('Step 3: season and lags', f'Peak month 12. Correlations {F["r_rain_now"]:.2f} and {F["r_rain_lag1"]:.2f}.'), ('Step 4: split', f'{F["n_ready"]}, {F["n_train"]}, {F["n_test"]}.'),
                   ('Step 5: model', f'Baseline {f1(nm)}, model {f1(mm)}, RMSE {f1(F["model_rmse"])}, MAPE {f1(F["model_mape"])}.'), ('Step 6: Pipeline', f'Same MAE {f1(mm)}; with district indicator variables {f1(F["pipe_mae"])}.'),
                   ('Step 7: the trap and the report', f'Wrong lag MAE {f1(F["bad_mae"])}. Three sentences with the horizon, both scores in cases, and one limit.')],
        rescue=['If the concepts run over, shorten the districts table (slide 18) and the horizon table (slide 19), and keep the leakage slide.', 'If only 30 minutes of lab remain, do steps 1, 3, 4, 5 and the report; skip the Pipeline district indicators.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.', 'If Colab cannot import scikit-learn, the numpy cells still work: the Pipeline cells are the only ones that need it.'],
        after=['Review the three sentences and the results file with each learner for feedback (Project milestone 3). Nothing is scored.', 'Ask each learner to name the baseline for their own course project data.', 'Note any question you could not answer and open Session 20 with it.'],
        lab_answer_key=[['Step 2 PREDICT: will the baseline miss more in Gulu or in Kampala?', f'Gulu: {f1(by.loc["Gulu", "naive"])} against {f1(by.loc["Kampala", "naive"])}. Gulu has about {n(by.loc["Gulu", "mean_cases"] / by.loc["Kampala", "mean_cases"])} times the cases.'],
                        ['Step 3 READ: which calendar month has the most cases?', f'December (month 12) with {n(peak)} cases.'],
                        ['Step 3 READ: what do the two correlations say?', f'This month\'s rain: {F["r_rain_now"]:.2f}. Last month\'s rain: {F["r_rain_lag1"]:.2f}. The effect has a delay.'],
                        ['Step 5 READ: does the model beat the baseline?', f'Yes: {f1(mm)} against {f1(nm)} in MAE, {f1(F["model_rmse"])} against {f1(F["naive_rmse"])} in RMSE.'],
                        ['Step 5 CHANGE: use only cases_lag1.', f'The MAE becomes {f1(F["mae_lag1_only"])}, worse than the baseline. Last month alone is not enough.'],
                        ['Step 6 READ: why does the Pipeline give the same MAE as numpy?', 'Standardising does not change the forecast of a linear regression. Two methods agreeing is a check.'],
                        ['Step 6 CHANGE: add the district indicator variables.', f'MAE {f1(F["pipe_mae"])}.'],
                        ['Step 7 READ: what happens when the lag is built without groupby?', f'MAE {f1(F["bad_mae"])}, worse than {f1(mm)}, and {F["bad_extra"]} extra records are wrongly kept.']])
    return sess
