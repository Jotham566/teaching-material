"""Class 1 (Week 8): your first model. Baseline, line, error, hidden rows, tree, then the lab. Built once, re-skinned for three cohorts."""
import sys
from pathlib import Path
import common as C
from common import fmt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_ml_c1  # noqa: E402,F401  (registers bars_c1, tree_c1, descent_c1, sheet_c1)


def build(code):
    f = C.facts(code)
    b, unit, short, thing = f['b'], f['unit'], f['short'], f['thing']
    reg = b['reg']
    L = b['line_load_only']
    fri = f['friday']
    n_raw, n_clean, n_tr, n_va, n_te = len(f['raw']), b['n_clean'], b['n_tr'], b['n_va'], b['n_te']
    mean_tr = b['baseline']
    pts = [(float(x), float(y)) for x, y in zip(f['trf'].load_pct, f['tr'].target)]
    raw = f['raw']
    dup = raw[raw.record_id.duplicated(keep='last')].iloc[0]
    nt = raw[raw.target.isna()].iloc[0]
    bl = raw[~raw.load_pct.between(0, 100)].iloc[0]

    def cell(v, nd=2):
        return 'NaN' if v != v else (str(v) if isinstance(v, str) else (f'{v:g}' if nd is None else f'{v:.{nd}f}'.rstrip('0').rstrip('.')))

    heads = ['record_id', 'equipment_id', 'load_pct', 'ambient_c', 'target']
    ok_rows = [[str(int(r.record_id)), r.equipment_id, cell(r.load_pct), cell(r.ambient_c), f'{r.target:.2f}'] for r in f['clean'].head(4).itertuples()]
    shown_ids = [int(r[0]) for r in ok_rows]
    ok_labels = [int(f['raw'].index[f['raw'].record_id == i][0]) + 1 for i in shown_ids]   # the row of the file each record sits in
    skipped = [str(i) for i in range(1, shown_ids[-1]) if i not in shown_ids]
    last = raw.iloc[-1]
    n_last = len(raw)
    def rrow(r):
        return [str(int(r.record_id)), r.equipment_id, cell(r.load_pct), cell(r.ambient_c), 'NaN' if r.target != r.target else f'{r.target:.2f}']
    first_row_no = int(raw.index.get_loc(dup.name)) + 1
    bad_rows = [rrow(dup), rrow(nt), rrow(bl), rrow(last)]
    bad_labels = [first_row_no, int(raw.index.get_loc(nt.name)) + 1, int(raw.index.get_loc(bl.name)) + 1, n_last]
    gd = C.gd_steps()
    uses = {'CML3112': ['Size the cooling plant before a hot week arrives', 'Spot a building that uses more energy than it should', 'Plan next month’s energy budget'],
            'CML3113': ['Plan crusher power for next week', 'Spot a crusher that uses more energy per tonne than it should', 'Estimate the energy bill for a month of ore'],
            'CML3111': ['Warn before a motor winding overheats', 'Plan maintenance before a failure, not after it', 'Choose the right cooling fan for a motor drive (the unit that powers the motor)']}[code]
    use_icons = {'CML3112': ['gear', 'magnifier', 'calendar'], 'CML3113': ['calendar', 'magnifier', 'receipt'], 'CML3111': ['bell', 'calendar', 'gear']}[code]
    # cohort wording: the question of the day, what load_pct measures, and an example of a costly large error
    question = {'CML3112': 'How can a computer predict cooling load from plant load and air temperature, and how do we know it is any good?',
                'CML3113': 'How can a computer predict crusher energy from crusher load and air temperature, and how do we know it is any good?',
                'CML3111': 'How can a computer predict winding temperature from motor load and air temperature, and how do we know it is any good?'}[code]
    working = {'CML3112': 'how hard the cooling plant was working', 'CML3113': 'how hard the crusher was working', 'CML3111': 'how hard the motor was working'}[code]
    big_err = {'CML3112': 'an undersized chiller on a hot day', 'CML3113': 'tripping the crusher motor', 'CML3111': 'a motor overheating'}[code]
    c2_label = {'CML3112': 'high cooling load', 'CML3113': 'high energy demand', 'CML3111': 'overheating'}[code]
    c2_example = f'will the {short} reach {b["limit"]:g} {unit} ({c2_label}) or not?'
    rules_tree = C.R.tree_reg_fit(f['trf'].to_numpy(), f['tr'].target.to_numpy(), 2)
    tree = C.tree_node(rules_tree, ['load_pct', 'ambient_c'], unit)
    ex = ['The data come from the file engineering_data.csv: ' + f'{n_raw} rows of {thing} readings.']

    if fri:
        clock = [(10, 'Recall from Weeks 1 to 7'), (35, 'Concepts: your first model, with pictures'), (55, 'Lab, part 1: prepare the rows'), (15, 'Break'),
                 (55, 'Lab, part 2: three models and the model comparison table'), (10, 'Close and what is assessed')]
        plan_note = ('You already met the words and the ideas in the theory session. Today we look at them again with pictures, for thirty-five minutes, and then we spend almost all of the time on the lab. '
                     'The concepts come first, then the break comes in the middle of the lab, and you will have the notebook open from the second half of the first hour. Ask your question when it comes to you.')
    else:
        clock = [(10, 'Recall from Weeks 1 to 7'), (35, 'Concepts, part 1: data, baseline model and prediction error'), (30, 'Concepts, part 2: learning, held-out data and models'), (15, 'Break'),
                 (80, 'Lab: your first model, in the notebook'), (10, 'Close and what is assessed')]
        plan_note = ('We have three hours. The first hour and a quarter is concepts only, with no laptop, so you can listen and ask. Then a break. Then the lab, about an hour and twenty minutes, '
                     'where you run everything we just talked about on your own data. You will not need to switch between slides and the notebook while you learn, because the ideas come first and the code comes second.')

    # ---- numbers used by the formula slides (all from the reference, never typed)
    lin = b['lin']
    b0, b1, b2 = lin['intercept'], lin['w_load'], lin['w_amb']
    L0, L1 = L['intercept'], L['slope']
    ut = unit.replace(' ', r'\ ')                      # unit as it is written inside a maths line
    va_raw, va_fill = f['va'], f['vaf']
    y_all = va_raw.target.to_numpy()

    def lp(x1, x2):
        return b0 + b1 * x1 + b2 * x2

    r2 = lambda v: round(float(v), 2)                  # worked errors use the two-decimal values shown on the slide
    ex_rows = []
    for k in range(4):
        r = va_raw.iloc[k]
        lg = L0 + L1 * float(va_fill.load_pct.iloc[k])
        ex_rows.append([str(int(r.record_id)), cell(r.load_pct), cell(r.ambient_c), f'{r.target:.2f}', f'{mean_tr:.2f}', f'{r2(r.target) - r2(mean_tr):+.2f}', f'{lg:.2f}', f'{r2(r.target) - r2(lg):+.2f}'])
    # the worked row: the first validation row whose baseline error is clearly visible (at least a fifth of the baseline MAE)
    k0 = next(k for k in range(n_va) if abs(float(va_raw.target.iloc[k]) - mean_tr) >= 0.2 * reg['baseline']['mae'])
    r0 = va_raw.iloc[k0]
    y0 = r2(r0.target)
    e0 = round(y0 - r2(mean_tr), 2)
    e0_word = 'too high' if e0 < 0 else 'too low'
    sum_abs_base = reg['baseline']['mae'] * n_va
    p0, p1, p2, p3 = lp(60, 25), lp(61, 25), lp(60, 26), lp(61, 26)
    L0r, L1r = round(L0, 2), round(L1, 3)
    pl60 = L0r + L1r * 60                                # worked from the rounded numbers shown on the slide
    miss_tr = f['tr'][f['tr'].ambient_c.isna()]
    miss_rec = ', '.join(f'record {int(r.record_id)} (group {r.equipment_id})' for r in miss_tr.itertuples())
    tree_mae_s = f'{reg["tree"]["mae"]:.2f} {unit}'
    if code == 'CML3113':                                # two splits tie at depth 4: another random_state gives 1.18 (checked with scikit-learn 1.9.1)
        tree_mae_s += ' (1.18 if random_state differs)'
    lo_pred = [L0 + L1 * float(v) for v in va_fill.load_pct]
    lo_abs = [abs(float(a) - p_) for a, p_ in zip(y_all, lo_pred)]
    sum_abs_lo = sum(lo_abs)
    lo_mae = sum_abs_lo / n_va
    n_dedup = len(raw.drop_duplicates('record_id'))
    rules_tree1 = C.R.tree_reg_fit(f['trf'].to_numpy(), f['tr'].target.to_numpy(), 1)
    tree1 = C.tree_node(rules_tree1, ['load_pct', 'ambient_c'], unit)
    first_q = ['load_pct', 'ambient_c'][rules_tree[1]]
    first_cut = rules_tree[2]
    g1 = -2 * sum(x * y for x, y in zip((1, 2, 3), (2, 4, 6))) / 3          # slope of the loss at w = 0

    s = dict(
        code=code, cohort_name=f['name'], num=1, week=8, when=f['dates'][1] + ', ' + f['slot'], short_title='Your first model',
        title='Your first model: baseline model, linear regression and prediction error',
        question=question,
        outcome_head='By the end of today you can',
        outcomes=[f'Explain features, target variable, baseline model and prediction error using the {thing} data', 'Say why some rows must be held out (validation set and test set) while a model trains',
                  'Train a linear regression model and a decision tree in Python and compare them with a baseline model'],
        outcome_icons=['book', 'lock', 'chart'],
        outcome_note=('Here is what you can do by the end of today. You can explain the words feature, target variable, baseline model and prediction error using the data in front of you. You can say why some rows must be held out, in a validation set and a test set, while a model trains. '
                      'And you can train a linear regression model and a decision tree in Python and compare both with a baseline model. Nothing is submitted today. The lab prepares you for part A of the first assignment, and I explain how at the end.'),
        clock=clock, plan_title='Your three hours: ideas first, then the lab', plan_note=plan_note,
        plan_caption=('A short concepts section with pictures first. Then most of the time is the lab, with the notebook open.' if fri else 'Concepts first, with no laptops. Then a break, then the lab with the notebook open.'),
        recall_from='the first seven weeks',
        recall=[('What does data.shape tell you about a table?', 'It gives the number of rows and then the number of columns.'),
                ('Why do we clean a copy of the file and keep the original unchanged?', 'So we can always go back to the raw data and check what we changed.'),
                ('What is a missing value, and how does pandas show it?', 'It is an empty cell with no reading. pandas shows it as NaN.')],
        words=[('Feature', 'An input column (also called an input variable or predictor) that the model reads to make a prediction. Here: load_pct and ambient_c.'),
               ('Target variable', f'The column we want to predict. Here: {short} in {unit}. When the target is a class such as yes or no, it is called a label. In Class 2 we make a yes or no label from the target.'),
               ('Baseline model', 'The simplest possible model, which every other model must beat. Here it predicts the mean of the training targets for every row.'),
               ('Prediction error (residual)', 'For one row: actual value minus predicted value. Later slides combine many errors into one score, the MAE or the RMSE.'),
               ('Training set and validation set', 'The training set is the rows the model learns from. The validation set is held-out data: rows kept back while the model trains, used to compare models fairly.')],
        word_icons=['grid', 'flag', 'check', 'cross', 'lock'],
        words_note=(f'Five terms for today, and these are the real industry names, so you will hear them again in textbooks and documentation. Think of one reading from our file. Its load_pct and ambient_c are the features, and its {short} is the target variable. '
                    f'If we always guessed the mean, about {mean_tr:.0f} {unit}, that guess would be the baseline model. If the real reading were two above our guess, the prediction error would be plus two. '
                    'The model learns from the training set, and we judge it on the validation set, rows it never saw. Which of the five words was new to you?'),
        keep='Keep your lab notebook, saved after you restart the session and run all cells in order. Keep your three MAE numbers from the model comparison table: the baseline model, the multiple linear regression model and the decision tree.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved notebook', value='Restart, run all, save'), dict(label='Model comparison', value='MAE of the three models'),
                                                              dict(label='Next class', value='Classification'), dict(label='Bring', value='Laptop with the saved lab file')]),
        keep_title='Save the notebook and keep your three MAE scores',
        next='Class 2: classification, where the model answers yes or no.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the three MAE scores from the model comparison table: the baseline model, the multiple linear regression model and the decision tree. '
                   f'Next class we predict a yes or no answer, for example: {c2_example} We learn how to measure a model that answers that way. If anything today was unclear, write the question down and bring it.'),
        cover_note=(f'Welcome to the second half of the semester. Today is your first full machine learning model. We use the {thing} data and we predict {short}. '
                    'You have spent seven weeks learning to read, clean and chart data. Now that work pays off, because a model is only as good as the rows we give it. '
                    'The ideas come first, then the lab.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions at the start of the class',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='Check each answer against your own. If one surprised you, look back at Weeks 1 to 7 before the lab.',
                  notes=('Here are the short answers to the three questions. Data dot shape gives the number of rows and then the number of columns, so ninety-one rows and five columns for our file. '
                         'We clean a copy and keep the original unchanged, so we can always go back and check what we changed. '
                         'And a missing value is an empty cell with no reading. pandas shows it as NaN. If you answered all three correctly, you are ready for today. If one surprised you, look it up before the lab.')))

    S.append(dict(kind='list', title='A prediction turns past readings into a number you can act on', items=uses, icons=use_icons,
                  notes=(f'Let us start with why anyone predicts a number. With {thing} readings you can do things like these. {uses[0]}. {uses[1]}. {uses[2]}. '
                         'Every one of those is a decision that costs money or safety if it is wrong, and every one starts with a number we do not yet know. '
                         'That is what a model does for us: it takes readings we already have and gives a good guess for the number we want. Which of these three sounds closest to something you would do in your own field?')))

    S.append(dict(kind='table', title='A glossary you will meet again in textbooks and documentation',
                  headers=['Term', 'What it means in plain words'],
                  rows=[['Linear regression', 'Predicts the target as an intercept plus weighted features. Simple (also called univariate): one feature. Multiple: two or more features. Multivariate regression means several targets, a different thing.'],
                        ['MAE, MSE and RMSE', 'Three scores that sum up many prediction errors, in the unit of the target (MSE: unit squared).'],
                        ['Missing value and imputation', 'A missing value is an empty cell (NaN). Imputation fills it, for example with the median.'],
                        ['Parameters and hyperparameter', 'Parameters (intercept, coefficients) are learned. A hyperparameter, such as max_depth, is chosen before training.'],
                        ['Pipeline', 'Chains preprocessing and a model, and runs them in order.']],
                  widths=[3.6, 8.4], icons=False,
                  note='Each term is explained again where it first matters.',
                  notes=('Before the ideas, here is a short glossary. These are the real industry names, and you will meet them again in textbooks, documentation and interviews, so we use them from the start. '
                         'Linear regression is a model that predicts the target as an intercept plus weighted features. MAE, MSE and RMSE are three ways to sum up prediction errors. '
                         'A missing value is an empty cell, and imputation fills it. Parameters are learned, and a hyperparameter is chosen before training. A pipeline runs the steps in order. '
                         'Each term comes back later with a picture, and gradient descent and the loss function have their own slides. Which of these have you already heard somewhere?')))

    S.append(dict(kind='idea', title='Machine learning finds the rule from examples, so nobody writes it by hand',
                  visual=dict(kind='flow', steps=[dict(head='Examples', text='Past rows, each with its answer', icon='folder'), dict(head='Learning', text='The computer finds the pattern', icon='gear'),
                                                  dict(head='Model', text='The rule it keeps', icon='robot'), dict(head='Prediction', text='An answer for a new row', icon='chart')], highlight=2),
                  lead='A model is the rule the computer found.',
                  points=['We do not write the rule ourselves. The computer finds it from the examples.', 'Every example row must include its answer, which we call the target variable.'],
                  notes=('Here is the whole idea of machine learning in one picture. We give the computer examples, which are past rows that include the answer. '
                         'It looks for a pattern that links the inputs to the answer. What it keeps is called the model. Then, when a new row arrives without an answer, the model produces a prediction. '
                         'Compare that with what you did in Weeks 3 and 4, where you wrote every rule yourself with if and else. Today the computer finds the rule. Our job is to give it good rows and to check its work.')))

    S.append(dict(kind='idea', title='Every row is one reading: the inputs are features and the answer is the target variable',
                  visual=dict(kind='sheet_c1', headers=heads, rows=ok_rows, rowlabels=ok_labels, hl=[0, 4]),
                  lead=f'The model reads the features and predicts the target variable (yellow): {short} in {unit}.',
                  points=['Features (input variables): load_pct (percent of full load) and ambient_c (deg C).', 'record_id and equipment_id only label the row.'] + ([f'Record {skipped[0]} is left out: its target is a missing value (NaN).'] if len(skipped) == 1 else []),
                  notes=(f'Look at the table. The grey numbers on the left are the rows of the file. Each row is one reading of one {thing}. The columns load_pct and ambient_c tell us {working} and how warm the air was. '
                         f'Those are the features, also called input variables or predictors: the things the model is allowed to see. The last column is the target variable, {short} in {unit}. It is the answer we want the model to learn to guess. '
                         'The record number and the equipment label help us keep track, but they are not features today. Which column is the target?')))

    S.append(dict(kind='idea', title='Before we model, we remove the rows we cannot trust',
                  visual=dict(kind='sheet_c1', headers=heads, rows=bad_rows, rowlabels=bad_labels, hl=[3, 0]),
                  lead=f'Our file has {n_raw} rows. Three kinds of row cannot be used.',
                  points=[f'record_id {int(dup.record_id)} is in row {first_row_no} and again in the last row, row {n_last} (yellow). Keep the first.', f'record_id {int(nt.record_id)} has a missing target (NaN): nothing to learn from.', f'record_id {int(bl.record_id)} has load_pct {cell(bl.load_pct)}: impossible.'],
                  notes=(f'This is the Week 6 data cleaning you already know, now with a purpose. Our file has {n_raw} rows, and three kinds of trouble. One record number appears twice, once near the top and once in the very last row of the file, so we keep the first copy. '
                         'One row has no target, so there is no answer to learn from. And one row has a load below zero percent, which cannot happen, so it is a recording error. '
                         f'After removing them we keep {n_clean} rows. One more missing value remains, in a feature column, and we deal with it later by imputation. Notice that we clean a copy and keep the raw file safe.')))

    S.append(dict(kind='idea', title='Hold out rows while the model trains, so the evaluation is fair',
                  visual=dict(kind='rowsplit', parts=[dict(label='Training', sub='E1 to E4', n=n_tr, role='Training set: the model learns from these rows.', fill='ink'),
                                                      dict(label='Validation', sub='E5', n=n_va, role='Validation set: we compare models here.', fill='paper'),
                                                      dict(label='Test', sub='E6', n=n_te, role='Test set: held out until the end.', fill='gold')]),
                  lead=f'After cleaning, {n_clean} rows remain. We cut them into three sets by equipment group.',
                  points=['Held-out data are rows not used to fit the model: the validation and test sets.', 'Each equipment group goes into one set only.'],
                  notes=(f'Suppose you learned ten answers by heart and I tested you on the same ten. You would look brilliant and I would learn nothing. A model is the same. So we cut the {n_clean} clean rows into three groups. '
                         f'The training set, {n_tr} rows, is what the model learns from. The validation set, {n_va} rows, is held-out data that the model never trains on, and we use it to compare models. The test set, {n_te} rows, is also held out and stays untouched until the end of the block. '
                         f'We cut by equipment group, E1 to E4, then E5, then E6, so the model is judged on whole {thing} groups it has never met. Why would mixing the groups give us a rosier score?')))

    S.append(dict(kind='steps', title='Imputation fills a missing value with the training median of its column',
                  steps=[dict(head='Learn the value', text='Find the median (middle value) of each feature column in the training set', icon='calculator'),
                         dict(head='Fill training rows', text='Put that median into each missing value in the training set', icon='notebook'),
                         dict(head='Fill validation rows', text='Use the same training medians in the validation set', icon='lock')],
                  caption=(f'Training medians: {f["med"]["load_pct"]:.1f} percent (load_pct) and {f["med"]["ambient_c"]:.1f} deg C (ambient_c). '
                           f'{miss_rec[0].upper() + miss_rec[1:]} has no ambient_c, so it gets {f["med"]["ambient_c"]:.1f}. This is imputation (SimpleImputer).'),
                  notes=('One feature value is missing, and a model cannot use a missing value. So we fill it by imputation, with the median, the middle value of that column. The important rule is where the median comes from. '
                         f'We find it from the training rows only, here {f["med"]["load_pct"]:.1f} for load and {f["med"]["ambient_c"]:.1f} for ambient temperature. We use that same number to fill missing values in the validation set too. '
                         'If the validation set helped decide the fill, information would leak from the held-out data into the model, which is called data leakage, and our score would be a little too kind. '
                         'The scikit-learn tool that does this is called SimpleImputer, and we meet it in the lab.')))

    S.append(dict(kind='idea', title='The baseline model comes first: predict the mean of the training targets every time',
                  visual=dict(kind='scatter_c1', points=pts, xlabel='load_pct (percent)', ylabel=f'{short} ({unit})', hline=mean_tr, hline_label=f'Baseline model: mean of\ntraining targets, {mean_tr:.2f} {unit}'),
                  lead=f'Each dot is one training row. The dashed line is the baseline model: it predicts {mean_tr:.2f} {unit} for every row.',
                  points=['A baseline model is the simplest possible model: it predicts the mean of the training targets and ignores the features.', 'Every other model must beat it. If it cannot, it has learned nothing useful.'],
                  notes=(f'Each dot is one training row. Before building anything clever, we build the simplest possible model, called the baseline model. It predicts the mean of the training targets, {mean_tr:.2f} {unit}, for every row, whatever the load. '
                         'That dashed line is the baseline model. Look at the dots: it is fine for rows near the middle and very wrong at both ends. '
                         'This matters because any model has to do better than the baseline model, or it is not worth the trouble. How large do you think its prediction error will be, on average?')))

    S.append(dict(kind='formula', title=f'The baseline model adds the {n_tr} training targets and divides by {n_tr}: {mean_tr:.2f} {unit}',
                  formulas=[('Baseline model', r'$\hat{y} = \bar{y} = \frac{1}{n}\sum_{i=1}^{n} y_i$'),
                            ('Our data', r'$\hat{y} = ' + f'{mean_tr:.2f}' + r'\ \mathrm{' + ut + r'}$')],
                  symbols=[['y-hat and y-bar', 'The prediction, which is the mean of the y_i.', f'{mean_tr:.2f} {unit}'],
                           ['y_i', 'The actual target of training row i.', f'column target, in {unit}'],
                           ['n', 'How many training rows there are.', f'{n_tr} rows (E1 to E4)'],
                           ['sum, i = 1 to n', 'Add up the values from row 1 to row n.', 'all training rows'],
                           ],
                  size=20, note=f'We add the {n_tr} training targets and divide by {n_tr}. The validation set plays no part.',
                  notes=(f'Here is the baseline model written as a formula. The symbol y with a little hat on top means a prediction. The symbol y with a bar on top means the mean. '
                         f'To get it we add up the targets of all {n_tr} training rows and divide by {n_tr}. For our data that gives {mean_tr:.2f} {unit}. '
                         'Every row gets that same prediction. Notice that the validation set never takes part, because it is held out. '
                         'Read the table row by row and check that you can say what each symbol means in our data.')))

    S.append(dict(kind='idea', title='Simple linear regression fits a line through the dots and beats the baseline model',
                  visual=dict(kind='scatter_c1', points=pts, xlabel='load_pct (percent)', ylabel=f'{short} ({unit})', line=(L0, L1), line_label='Simple linear regression (load_pct only)'),
                  lead=f'Simple (univariate) linear regression: one feature, load_pct. Each extra 1 percent of load adds {L1:.2f} {unit}.',
                  points=[f'At zero load it starts at {L0:.1f} {unit} (the intercept).', 'It predicts the target as an intercept plus a weighted feature.', f'On the validation set its MAE is {lo_mae:.2f} {unit}.'],
                  notes=(f'This model is called simple linear regression, or univariate linear regression, because it has one feature. The line has two numbers. The intercept, {L0:.1f} {unit}, is where it starts at zero load. '
                         f'The slope, {L1:.2f}, says that each extra one percent of load adds that much to the prediction. This is the model: a rule that stands in for the table. '
                         'Give it any load and it reads off a prediction. We drew it with load alone to keep the picture simple. On the validation set its mean absolute error is about '
                         f'{lo_mae:.2f} {unit}. In the lab the model also uses ambient_c, so it learns one weight for each feature. With two or more features the model is called multiple linear regression. Multivariate strictly means several targets, so we say multiple.')))

    S.append(dict(kind='formula', title=f'Simple linear regression has two learned numbers: at 60 percent load it predicts {pl60:.2f} {unit}',
                  formulas=[('Simple linear regression', r'$\hat{y} = b_0 + b_1\,x$'), ('Our fitted model', r'$\hat{y} = ' + f'{L0:.2f} + {L1:.3f}' + r'\,x$')],
                  symbols=[['y-hat', 'The predicted target.', f'{short}, in {unit}'],
                           ['x', 'The feature of the row. Here the load alone.', 'column load_pct, in percent'],
                           ['b0', 'The intercept (bias): the prediction when x is 0.', f'{L0:.2f} {unit}'],
                           ['b1', 'The slope, or coefficient (weight): how much the prediction grows when x grows by 1.', f'{L1:.3f} {unit} per percent of load']],
                  note=f'Example: at load_pct = 60 the prediction is {L0:.2f} + {L1:.3f} × 60 = {pl60:.2f} {unit}.',
                  notes=(f'The fitted red line is a formula. The prediction equals b zero plus b one times x. B zero is the intercept, the value where the line starts at zero load. '
                         f'B one is the slope, how much the prediction grows when the load grows by one percent. For our data b zero is {L0:.2f} and b one is {L1:.3f}. '
                         f'Try it at a load of sixty percent: {L0:.2f} plus {L1:.3f} times sixty gives {pl60:.2f} {unit}. The computer finds b zero and b one by itself. Which load gives the largest prediction?')))

    S.append(dict(kind='idea', title='The prediction error (residual) is the actual value minus the predicted value',
                  visual=dict(kind='scatter_c1', points=pts, xlabel='load_pct (percent)', ylabel=f'{short} ({unit})', line=(L0, L1), residuals=True),
                  lead='Prediction error (residual) = actual value minus predicted value, for one row. The line is simple linear regression.',
                  points=['Each red segment joins a dot (actual) to the line (predicted). Its length is the error size.', 'Positive error: the model predicted too low.', 'A good model leaves short segments.'],
                  notes=('How do we know if a model is good? We look at its prediction errors, also called residuals. Each red segment is the distance between an actual value and what the model predicted. '
                         'That distance is the error, actual minus predicted. If the model predicted too low, the error is positive. If it predicted too high, the error is negative. '
                         'A good model leaves small errors. A poor one leaves large errors. To compare models we need one number that sums up all the errors, and two ways to do that come next.')))

    S.append(dict(kind='formula', title=f'e = y minus y-hat: for record {int(r0.record_id)} the baseline model is off by {e0:+.2f} {unit}',
                  formulas=[('Prediction error of row i', r'$e_i = y_i - \hat{y}_i$'),
                            ('One row of ours', r'$e = ' + f'{y0:.2f} - {mean_tr:.2f} = {e0:.2f}' + r'\ \mathrm{' + ut + r'}$')],
                  symbols=[['e_i', f'The prediction error (residual) of row i. Negative means the prediction was too high.', f'in {unit}'],
                           ['y_i', 'The actual target of row i.', f'column target, in {unit}'],
                           ['y-hat_i', 'The prediction for row i.', f'baseline model: {mean_tr:.2f} {unit}'],
                           ['i and n', 'The row number i runs from 1 up to n, the number of rows.', 'one row at a time']],
                  note=f'Our row: record_id {int(r0.record_id)}, load_pct {cell(r0.load_pct)}, ambient_c {cell(r0.ambient_c)}. Predicted {e0_word} by {abs(e0):.2f} {unit}, from the values shown.',
                  notes=(f'Here is the prediction error as a formula. For row i, the error e i equals the actual value y i minus the prediction y hat i. The small i just says which row we mean. '
                         f'Our example is a validation row with a clear error, record {int(r0.record_id)}. Its actual target is {y0:.2f} {unit}. The baseline model predicts {mean_tr:.2f}. '
                         f'So the error is {e0:.2f}, and the sign tells us the prediction was {e0_word}. Work out the same error yourself with a calculator before you move on.')))

    S.append(dict(kind='table', title='Worked example with hypothetical numbers: four prediction errors give MAE 2.75 and RMSE 3.5',
                  headers=['Reading', 'Actual', 'Predicted', 'Error e', 'Absolute error |e|', 'Squared error e × e'],
                  rows=[['1', '70', '72', '-2', '2', '4'], ['2', '80', '77', '+3', '3', '9'], ['3', '90', '90', '0', '0', '0'], ['4', '60', '66', '-6', '6', '36']],
                  widths=[1.4, 1.4, 1.6, 1.4, 2.7, 2.7], icons=False,
                  note='MAE = (2 + 3 + 0 + 6) / 4 = 2.75.  MSE = (4 + 9 + 0 + 36) / 4 = 12.25.  RMSE = square root of 12.25 = 3.5.  These four readings are hypothetical (made up, with no unit) to show the arithmetic.',
                  notes=('Here are four hypothetical readings, made up so that you can follow the arithmetic by hand. Reading four has a prediction error of minus six. If we simply averaged the errors, the plus and minus would cancel, which hides the problem. '
                         'So we remove the sign. Take the absolute value of each error: two, three, zero, six. Their mean is 2.75. That is the mean absolute error, MAE. '
                         'Or square each error first: four, nine, zero, thirty-six, mean 12.25, and take the square root to get back to the original unit: 3.5. That is the root mean squared error, RMSE. Check the first one on your own page.')))

    S.append(dict(kind='formula', title='Three ways to turn many errors into one number: MAE, MSE and RMSE',
                  formulas=[('MAE', r'$\mathrm{MAE} = \frac{1}{n}\sum_{i=1}^{n} |e_i|$'), ('MSE and RMSE', r'$\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n} e_i^{2}\qquad \mathrm{RMSE} = \sqrt{\mathrm{MSE}}$')],
                  symbols=[['n', 'How many rows we score.', f'{n_va} validation rows'],
                           ['|e_i| and e_i squared', 'The error with its sign removed, and the error multiplied by itself.', f'{unit} and {unit} squared'],
                           ['sum', 'Add the values for rows 1 to n.', 'all validation rows']],
                  size=21,
                  note='MAE and RMSE are in the unit of the target. MSE is in the unit squared. Lower is better.',
                  notes=('Here are the three measures as formulas. For MAE we take the absolute value of every error, add them up and divide by n, the number of rows. '
                         'For MSE we square every error, add them up and divide by n. RMSE is the square root of the MSE, which brings us back to the unit of the target. '
                         f'In our lab we score on the {n_va} validation rows, so n is {n_va}. MAE and RMSE are the two you will quote. Which one punishes a large error more?')))

    S.append(dict(kind='table', title='Our own validation rows: the baseline model and simple linear regression',
                  headers=['record_id', 'load_pct', 'ambient_c', 'Actual', 'Baseline', 'Error', 'Linear', 'Error'],
                  rows=ex_rows, widths=[1.6, 1.5, 1.6, 1.4, 1.5, 1.4, 1.4, 1.4], icons=False,
                  note=(f'Values in {unit}. Linear = simple linear regression (load_pct only). Errors use the rounded values shown. Absolute errors over {n_va} rows add up to {sum_abs_base:.1f} (baseline, MAE = {sum_abs_base:.1f} / {n_va} = {reg["baseline"]["mae"]:.2f}) '
                        f'and {sum_abs_lo:.1f} (linear, MAE = {lo_mae:.2f}).'),
                  notes=(f'Now the same arithmetic on real rows. These are the first four validation rows. The baseline model predicts {mean_tr:.2f} for every row, so its error is the actual value minus {mean_tr:.2f}. '
                         'The simple linear regression prediction changes from row to row, because it uses the load, and its errors are much smaller. '
                         f'Over all {n_va} validation rows, the baseline model has absolute errors that add up to {sum_abs_base:.1f}. Divide by {n_va} and you get an MAE of {reg["baseline"]["mae"]:.2f} {unit}. '
                         f'Simple linear regression gets {lo_mae:.2f}. Multiple linear regression, which uses both features, does better still, and it comes in a few slides.')))

    S.append(dict(kind='compare', title='MAE and RMSE both measure prediction error in the target’s own unit',
                  left=dict(head='MAE', points=['The mean of the absolute errors', 'Every error counts by its size', 'Easy to explain to a client']),
                  right=dict(head='RMSE', points=['Squares the errors, takes the mean, then the root', 'One large error counts for much more', 'Use it when large errors are costly']),
                  verdict=f'Both are in {unit}: "the model is off by about this many {unit}".',
                  notes=('Both measures answer the question: how far off are we, on average? MAE treats every error the same way. If one reading was off by six and another by two, they count as six and two. '
                         f'RMSE squares first, so the error of six counts for nine times the error of two. That makes it the stricter measure, and the right one when a large error is dangerous, such as {big_err}. '
                         f'Both are in {unit}, the same unit as the target, so we can say in plain words how far off we are. RMSE is always at least as big as MAE. Which would you quote to a client?')))

    S.append(dict(kind='idea', title='Gradient descent trains a model by walking downhill on the loss, one small step at a time',
                  visual=dict(kind='descent_c1', labels=['Start: a big loss', 'Each step: update the parameter a little', 'Bottom: the smallest\nloss we can find']),
                  lead='Training starts with a poor model and improves its parameters (here the slope) by repeating small steps.',
                  points=['Loss function: how wrong the model is, as one number (here the MSE).', 'Gradient: the slope of the loss. It shows which way is downhill.', 'Learning rate: the size of each step.'],
                  notes=('How does the computer train a model? Most models learn by trial and improvement. The model starts poor, measures the loss, given by the loss function, a single number for how wrong it is, and works out which direction lowers the loss. '
                         'That direction is the gradient. Then it takes a small step in that direction, and the size of the step is the learning rate. Too big and it overshoots. Too small and it takes forever. '
                         'It repeats until the loss stops falling. Picture walking down a hill in fog, feeling the slope with your feet. That method is called gradient descent. Logistic regression next week and neural networks learn this way.')))

    S.append(dict(kind='formula', title='Gradient descent, part 1: the loss L is the MSE, and dL/dw is its slope',
                  formulas=[('Loss (MSE)', r'$L = \frac{1}{n}\sum_{i=1}^{n} (w\,x_i - y_i)^{2} = \frac{1}{n}\sum_{i=1}^{n} e_i^{2}$'),
                            ('Slope of the loss', r'$\frac{dL}{dw} = \frac{2}{n}\sum_{i=1}^{n} x_i\,(w\,x_i - y_i)$')],
                  symbols=[['L', 'The loss: the MSE of the model y-hat = w x over n rows (x_i, y_i).', 'illustrative: x = 1, 2, 3; y = 2, 4, 6; n = 3'],
                           ['w', 'The slope parameter (no intercept, to keep it small).', 'stands in for b1'],
                           ['e_i', 'Residual y_i minus w x_i. Squaring removes the sign, so both forms of L match.', 'as before'],
                           ['dL/dw', 'How fast L changes when w changes.', f'at w = 0 it is {g1:.2f}']],
                  size=19, widths=[1.4, 6.3, 4.2], note='A negative slope: a bigger w lowers the loss.',
                  notes=('Here is gradient descent as formulas. The first line is the loss itself, the mean squared error you met a few slides ago. Inside the bracket I wrote predicted minus actual, which is minus the residual, and squaring removes the sign, so it is the same loss. '
                         'The second line is the slope of the loss. The tiny example uses illustrative data, x equal one, two, three and y equal two, four, six. The model is y hat equals w times x, with no intercept. '
                         'At w equal zero the slope is minus 18.67, which says that a bigger w lowers the loss.')))

    S.append(dict(kind='formula', title='Gradient descent, part 2: change w a little, downhill',
                  formulas=[('Update rule', r'$w \leftarrow w - \eta \cdot \frac{dL}{dw}$')],
                  symbols=[['w', 'The parameter (slope) we are improving. It starts at 0.', 'the tiny example'],
                           ['arrow', 'Replace the old w by the new value on the right.', 'one update per step'],
                           ['dL/dw', 'The slope of the loss from the last slide.', f'at w = 0 it is {g1:.2f}'],
                           ['eta', 'The learning rate: the size of each step.', '0.05'],
                           ['LinearRegression', 'Skips these steps: it finds b0, b1 and b2 at once with a direct formula (least squares). Logistic regression (Class 2) and neural networks learn by gradient descent.', 'the lab model']],
                  size=24, note='Repeat: new w = old w minus the learning rate times the slope of the loss.',
                  notes=('This is the second formula, the update rule. The new w equals the old w minus the learning rate times the slope of the loss. '
                         'If the slope of the loss is negative, we are on the downhill side, so minus a negative number makes w bigger. The learning rate eta is 0.05. '
                         'One fact to keep straight: LinearRegression in scikit-learn solves for its parameters directly with the least-squares formula, so it never walks downhill. Gradient descent reaches the same answer step by step, and it is how logistic regression and neural networks learn. Next we calculate the first step by hand.')))

    S.append(dict(kind='table', title='On a tiny illustrative example, five steps almost reach the best slope',
                  headers=['Step', 'w after the step', 'Loss after the step'], rows=[['0 (start)', '0', f'{(4 + 16 + 36) / 3:.3f}']] + [[str(a), f'{w:.3f}', f'{l:.3f}'] for a, w, l in gd],
                  widths=[2.6, 3.4, 3.4], icons=False,
                  note=(f'Illustrative (hypothetical) data: x = 1, 2, 3 and y = 2, 4, 6, so the best w is 2. Step 1 by hand: dL/dw = (2/3) × (1 × (0 − 2) + 2 × (0 − 4) + 3 × (0 − 6)) = {g1:.2f}. '
                        f'New w = 0 − 0.05 × ({g1:.2f}) = {gd[0][1]:.3f}.'),
                  notes=('Here is the tiny illustrative example with one step worked by hand. The inputs are one, two, three and the answers are two, four, six, so the best slope is exactly two. We start the slope at zero. '
                         f'The slope of the loss at zero is minus {abs(g1):.2f}. The new w is zero minus 0.05 times minus {abs(g1):.2f}, which is {gd[0][1]:.3f}. '
                         f'After step two it is {gd[1][1]:.3f}. After five steps it is {gd[4][1]:.3f}, very close to two, and the loss has fallen to {gd[4][2]:.3f}. '
                         'Nobody told the computer the answer was two. In the lab, LinearRegression gets its answer with the direct formula instead.')))

    S.append(dict(kind='formula', title='Multiple linear regression has three learned parameters: b0, b1 and b2',
                  formulas=[('Regression function', r'$\hat{y} = b_0 + b_1 x_1 + b_2 x_2$'), ('Our learned parameters', r'$\hat{y} = ' + f'{b0:.2f} + {b1:.3f}' + r'\,x_1 + ' + f'{b2:.3f}' + r'\,x_2$')],
                  symbols=[['y-hat', 'The predicted target.', f'{short}, in {unit}'],
                           ['x1, x2', 'The two features (input variables) of a row.', 'x1 = load_pct (percent), x2 = ambient_c (deg C)'],
                           ['b0', 'The intercept (bias): the prediction if both features were 0. Nothing runs at 0 percent load in 0 deg C air, so it is only an anchor.', f'{b0:.2f} {unit}'],
                           ['b1, b2', 'The coefficients (weights) of x1 and x2.', f'b1 = {b1:.3f} {unit} per percent; b2 = {b2:.3f} {unit} per deg C']],
                  widths=[1.6, 5.4, 4.9],
                  size=18, note='LinearRegression finds b0, b1 and b2 with the direct least-squares formula (no gradient descent).',
                  notes=('This is the model you will train in the lab, multiple linear regression. It is the same idea as simple linear regression, but with two features. The prediction equals b zero plus b one times x one plus b two times x two. '
                         f'X one is the load in percent and x two is the ambient temperature. After training on our rows, b zero is {b0:.2f}, b one is {b1:.3f} and b two is {b2:.3f}. '
                         'B zero is only an anchor, because nothing runs at zero load in air at zero degrees. '
                         'These three numbers are the parameters the model has learned. In the lab you print them. Each coefficient tells you how much the prediction moves for one more unit of its feature.')))

    S.append(dict(kind='table', title='What one more unit of a feature does to the prediction',
                  headers=['Case', 'load_pct (percent)', 'ambient_c (deg C)', f'Prediction ({unit})', 'Change'],
                  rows=[['Start', '60', '25', f'{p0:.2f}', ''], ['load_pct up by 1', '61', '25', f'{p1:.2f}', f'+{b1:.3f}'], ['ambient_c up by 1', '60', '26', f'{p2:.2f}', f'+{b2:.3f}'],
                        ['Both up by 1', '61', '26', f'{p3:.2f}', f'+{b1 + b2:.3f}']],
                  widths=[3.2, 2.3, 2.3, 2.4, 1.8], icons=False,
                  note=f'This is multiple linear regression. Its coefficient for load_pct is not the same as the {L1:.3f} of simple linear regression, because now the two features share the work. The start values 60 and 25 are chosen for the example.',
                  notes=(f'Let us use the formula. Take a reading with a load of sixty percent and an ambient temperature of twenty-five degrees. The prediction is {p0:.2f} {unit}. '
                         f'Now raise the load by one percent and keep the ambient temperature fixed. The prediction rises by {b1:.3f}, which is b one. '
                         f'Raise the ambient temperature by one degree instead and it rises by {b2:.3f}, which is b two. Raise both and the changes add up to {b1 + b2:.3f}. '
                         'That is how you read a coefficient: the change in the prediction for one more unit of that feature, with the other feature held fixed.')))

    S.append(dict(kind='idea', title='A decision tree learns a short list of yes or no questions about the features',
                  visual=dict(kind='tree_c1', node=tree),
                  lead='A row follows yes or no answers down to one yellow box, a leaf node. That leaf gives the prediction.',
                  points=[f'Each question is an internal node: a split on a feature and a threshold. The top one asks: is {first_q} at most {first_cut:.1f}?', 'The prediction is the mean target of the training rows in that leaf node.'],
                  notes=('A second kind of model. A decision tree asks yes or no questions about the features and sends each row down one branch until it reaches a leaf node, the yellow box at the bottom. Each question is an internal node. '
                         f'The first box asks whether {first_q} is at most {first_cut:.1f}. If yes, the row goes left. If no, it goes right. '
                         'Each yellow box is a leaf node. It predicts the mean target of the training rows that ended up there during training. This small tree has only two questions on any path, so you can read it like a rule. '
                         'Which question does the tree ask first, and why do you think it picked that one?')))

    S.append(dict(kind='idea', title='max_depth is the largest number of questions a row can be asked',
                  visual=dict(kind='tree_c1', node=tree1),
                  lead='max_depth is a hyperparameter: a setting we choose before training. It limits how many questions a row meets.',
                  points=['This tree has max_depth 1. The tree on the previous slide had max_depth 2.', 'Deeper trees can overfit (fit noise): Class 3. The lab uses max_depth 4 and random_state=17, so ties break the same way for all.'],
                  notes=('The setting called max_depth is the largest number of questions a row can be asked on the way down. It is a hyperparameter, which means a setting that we choose before training. The computer does not learn it, unlike the parameters. '
                         'This tree has depth one, so one question and two answers. The earlier tree had depth two. A deeper tree asks more questions and can fit the training rows more closely, even to the point of overfitting, which means fitting noise in the training set. '
                         'In the lab you use depth four, with random_state set to seventeen so that everyone gets the same tree when two questions tie. Class 3 shows when deeper trees stop being helpful. Why would a tree that is perfect on its training set still disappoint us?')))

    S.append(dict(kind='idea', title='Model comparison: three models evaluated on the same validation set',
                  visual=dict(kind='bars_c1', items=[dict(label='Baseline model (mean of training targets)', value=round(reg['baseline']['mae'], 2)), dict(label='Multiple linear regression (both features)', value=round(reg['linear']['mae'], 2), hl=True),
                                                  dict(label='Decision tree, max_depth 4', value=round(reg['tree']['mae'], 2))], unit=f' {unit}',
                              caption=f'Bar length = error in {unit} (the MAE). Shorter is better. Gold = best.'),
                  lead=f'Multiple linear regression has a validation MAE of {reg["linear"]["mae"]:.2f} {unit}. The baseline model has {reg["baseline"]["mae"]:.2f} {unit}.',
                  points=[f'Simple linear regression (load_pct only, not shown) scored {lo_mae:.2f} {unit}.', 'The lab also plots actual against predicted: a point on the dashed diagonal is a perfect prediction.'],
                  notes=(f'This is where we are heading. Three models, all trained on the same training set and all evaluated on the same validation set. The baseline model has a mean absolute error of {reg["baseline"]["mae"]:.2f} {unit}. '
                         f'The decision tree has {reg["tree"]["mae"]:.2f}. Multiple linear regression has only {reg["linear"]["mae"]:.2f}, the best of the three. That is a different model from simple linear regression, which scored {lo_mae:.2f}. '
                         f'The RMSE tells the same story: {reg["baseline"]["rmse"]:.2f}, {reg["tree"]["rmse"]:.2f} and {reg["linear"]["rmse"]:.2f}. '
                         'Do not memorise these numbers. The point is that you will produce them yourself in the lab, and that a fair comparison always includes the baseline model.')))

    S.append(dict(kind='wide', title='A pipeline is one container that holds the imputer and the model, and runs them in order',
                  visual=dict(kind='pipe_c1', fit_text='fit: learn the median, then train the model', predict_text='predict: fill, then predict'),
                  caption='The gold frame is the pipeline: fit learns the medians, then the model; predict fills, then predicts.',
                  notes=('Before the code, two terms. An imputer is a tool that fills missing values, here with the median of the training set. A pipeline is the container around the steps: it chains preprocessing and a model, and runs them in order. '
                         'Our pipeline holds two steps: first the imputer, then the model. When we fit the pipeline, it learns the medians and then learns the model. When we predict with it, it fills any missing value first and then predicts. '
                         'Why do we put the imputer inside the pipeline instead of filling the cells by hand?')))

    S.append(dict(kind='code', title='Read the workflow before you write it: create, fit, predict, score',
                  code='imputer = SimpleImputer(strategy="median")\nlinear_model = make_pipeline(\n    imputer, LinearRegression())\nlinear_model.fit(X_train, y_train)\ny_pred = linear_model.predict(X_valid)\nmae = mean_absolute_error(y_valid, y_pred)',
                  reads=['Line 1: an imputer fills missing values.', 'Lines 2 and 3: a pipeline: imputer, then linear regression.', 'Line 4, fit (training) on X (features) and y (target): learns the median, then b0, b1, b2.',
                         'Lines 5 and 6: predict (inference), then score by the MAE.', 'Baseline and tree: swap in DummyRegressor or DecisionTreeRegressor.'],
                  notes=('Before we leave the concepts, look at the code you will use. Create an imputer, which fills missing values. Join it with an untrained linear regression model in a pipeline. Fit the pipeline, which means train it on the training set. '
                         'Predict, which is also called inference, means produce predicted targets for the validation set. Then score the predictions by comparing them with the actual targets. The imputer is there because one training value is missing, and a model alone would stop with an error. '
                         'A capital X is the table of features, and a lowercase y is the target variable. The baseline model and the tree use the same steps, with DummyRegressor or DecisionTreeRegressor as the second piece in the pipeline. You do not need to memorise it, because the notebook explains every line.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides and open the lab notebook. Use the slides "Check your numbers" and "Four errors you will meet" at the end of this deck.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Remember to run the cells in order from the top.')))

    S.append(dict(kind='steps', title='The lab has five stages, and the notebook numbers its steps 0 to 8',
                  steps=[dict(head='1 Load and look', text='Steps 0 and 1: read the file, count rows and missing values', icon='folder'), dict(head='2 Clean', text='Step 2: remove the three bad rows from a copy', icon='check'),
                         dict(head='3 Split', text='Step 3: training, validation and test sets by equipment group', icon='lock'), dict(head='4 Models', text='Steps 4 to 6: baseline model, linear regression, decision tree', icon='gear'),
                         dict(head='5 Compare', text='Steps 7 and 8: model comparison table, then save', icon='chart')], highlight=3,
                  caption='In every step: predict first, run the cell, read the output, then change one thing.',
                  notes=('Here are the five stages of the lab. One, load the file and look at it. Two, clean it by removing the three bad rows. Three, split by equipment group into a training set, a validation set and a test set. '
                         'Four, train the baseline model, the linear regression model and the decision tree. Five, put the scores side by side in a model comparison table and save. The notebook numbers its steps from zero to eight, so a stage can contain several steps. '
                         'Each step asks you to predict first, then run, then read the output. Predicting before you run is how you find out what you really understand. Do not skip the predict cells.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What the notebook prints', 'You should see'],
                  rows=[['Rows: raw file (5 columns), after removing the repeated record_id, after removing the 3 bad rows', f'{n_raw}, {n_dedup}, {n_clean}'], ['Training, validation and test rows', f'{n_tr}, {n_va}, {n_te}'],
                        [f'Baseline model: MAE on the validation set', f'{reg["baseline"]["mae"]:.2f} {unit}'], ['Simple linear regression (load_pct only): MAE (Step 5 CHANGE)', f'{lo_mae:.2f} {unit}'], ['Multiple linear regression: MAE', f'{reg["linear"]["mae"]:.2f} {unit}'],
                        ['Multiple linear regression: b0, b1 (load_pct), b2 (ambient_c)', f'{b0:.3f}, {b1:.3f}, {b2:.3f}'], ['Decision tree, max_depth 4: MAE', tree_mae_s],
                        ['RMSE: baseline, multiple linear regression, tree', f'{reg["baseline"]["rmse"]:.2f}, {reg["linear"]["rmse"]:.2f}, {reg["tree"]["rmse"]:.2f} {unit}']],
                  widths=[7.0, 4.9], icons=False,
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, you can carry on. If they do not, stop and call me over, because every later step builds on the earlier ones. '
                         'The most common reason is a cell that was run out of order, or a row removed twice. Do not edit a number to make it match. The aim is to understand why it is different, and that is a skill you will need in every project.')))

    S.append(dict(kind='table', title='Four errors you will meet, what they mean and what to do',
                  headers=['Error message', 'What it says', 'What to do'],
                  rows=[['FileNotFoundError', 'The CSV is not beside the notebook', 'Upload engineering_data.csv in the Files panel'],
                        ['KeyError: target', 'The code uses a column name that is not in the table, often a spelling difference', 'Print data.columns and copy the name exactly'],
                        ['NameError', 'The code uses a name from a cell that has not been run yet', 'Run all cells from the top, in order'],
                        ['ValueError: contains NaN', 'A missing value (an empty feature cell) reached the model', 'Fit the model inside the imputer pipeline, as in Step 5']],
                  widths=[3.4, 4.4, 4.2], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Errors are normal, and reading them is a skill. Here are the four you will most likely meet. File not found means the data file is not next to the notebook, so upload it. '
                         'Key error means you spelled a column name differently from the file, so print the columns and copy the name. Name error means you skipped a cell above, so run all cells from the top. '
                         'And a value error about NaN means a missing value reached the model, so use the imputer pipeline. Read the last line of the error first. It usually tells you the answer.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['Nothing is submitted today. Block 1 is Classes 1 and 2. Its assignment has two parts: A7 (regression) and A8 (classification).',
                         'Block work is practice: it is collected and you get feedback, but it does not count toward your final mark.',
                         f'The Block 1 assignment closes on {C.COHORTS[code]["b1_close"]} (Kampala time).', 'The Block 1 quiz opens in the last 20 minutes of Class 2 and stays open for 24 hours.', 'Keep your saved notebook: Class 2 reuses its cleaning steps.'],
                  icons=['doc', 'check', 'calendar', 'clock', 'folder'],
                  notes=('A word on how this counts. The block work is practice: it is collected and you get feedback, but it does not count toward your final mark. Your final mark comes from A1 to A5, Q1 to Q5, Practical Test 1 and the Engineering ML project, which is worth 40 percent. Nothing is submitted today. Block 1 is this class and the next one. Its assignment has two parts: part A on regression, which repeats the steps of today\'s lab with the assignment notebook, and part B on classification, which follows next class. '
                         f'The Block 1 assignment closes on {C.COHORTS[code]["b1_close"]}, Kampala time. The Block 1 quiz opens in the last 20 minutes of Class 2, stays open for 24 hours, and covers both classes. Keep your saved Class 1 notebook for the assignment. Next class reuses the cleaning steps.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once so you know it works on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Every learner needs both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (numbers for your cohort are in the table below).',
              'The Block 1 assignment notebook (W08_student.ipynb, practice: collected, feedback, not counted) is not used in class. Do not open it.'],
        recap_path=['Answers to the three', 'A glossary', 'Machine learning finds', 'Every row is one reading', 'Before we model', 'The baseline model comes', 'Simple linear regression fits', 'The prediction error (residual)', 'Worked example', 'Our own validation rows',
                    'Hold out rows', 'Imputation fills', 'A decision tree', 'Model comparison', 'Read the workflow'],
        misconceptions=[('A model that is perfect on its training set is excellent', 'It may be overfitting: fitting noise in the training set. We always evaluate a model on held-out data.'),
                        ('Machine learning means the computer understands the problem', 'It finds a numerical rule from examples. It has no understanding, which is why we check its work.'),
                        ('More input columns always help', 'They can add noise. The lab step "only load_pct" tests this.'),
                        ('The test set is for choosing the best model', 'The validation set chooses. The test set stays held out until the end.')],
        probes=[('Why is the baseline model the first model we build?', 'It sets the score to beat. A model that cannot beat the mean of the training targets has learned nothing useful.'),
                ('Which is bigger, the MAE or the RMSE?', 'The RMSE is always at least as big, because squaring makes large errors count for more.'),
                ('Why do we split by equipment group and not at random?', 'So the model is judged on equipment it has never met, which is the situation we face in real use.'),
                ('Why must the imputer learn its median from the training set only?', 'If the validation set decided the fill, information from held-out data would reach the model (data leakage) and the score would be too kind.'),
                ('Is the tree better because it is more complicated?', 'No. On these data multiple linear regression scores better on the validation set. The model comparison table decides, and when scores are close we prefer the simpler model (parsimony).'),
                ('What does a positive error mean?', 'The actual value was higher than the prediction, so the model predicted too low.'),
                ('What is the difference between a parameter and a hyperparameter?', 'A parameter is learned from data, such as the slope. A hyperparameter is a setting we choose before training, such as max_depth.'),
                ('Is gradient descent what LinearRegression does inside?', 'No. LinearRegression finds b0, b1 and b2 with a direct formula (least squares). Gradient descent reaches the same answer step by step and is how logistic regression (Class 2) and neural networks learn.')],
        lab_steps=[('Step 0 and 1: open and look', 'Shape (91, 5). Missing values: one in target and one in ambient_c. Anyone who sees an error here has the CSV in the wrong place.'),
                   ('Step 2: clean a copy', 'After removing repeats: 90. Rows left to model with: 88. If someone has a different count, they left between(0, 90) from the CHANGE task in place.'),
                   ('Step 3: split', 'Rows 58, 15, 15. One missing value remains in the training features (ambient_c).'),
                   ('Step 4: baseline model', 'The same number for every row. The five-row table shows the arithmetic of error. Ask one learner to read a row aloud.'),
                   ('Step 5: linear regression', 'Intercept and two coefficients (b0, b1, b2 on the slides), both coefficients positive. The CHANGE task (simple linear regression, one feature) gives a larger MAE: the second feature helps.'),
                   ('Step 6: tree', 'Depth 4 gives the number on the board. CML3113: 1.18 is also correct if random_state differs (two splits tie; 1.20 with random_state=17). The depth experiment shows the tree changing: park the explanation for Class 3.'),
                   ('Step 7 and 8: model comparison table and save', 'Three rows, multiple linear regression best. Insist on restart and run all before saving.')],
        rescue=['If the concepts run over, skip gradient descent and the tiny example. Say: the computer improves the parameters of a model by small steps, and you will see it in a later class.',
                'If only thirty minutes of lab remain, do steps 0 to 5 and 7. Set step 6 (the tree) as practice for next time.',
                'If wifi fails in the room, use the offline set-up from Week 2: the notebook runs unchanged in VS Code.',
                'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Tell the class that nothing is submitted today. Part A of the Block 1 assignment (practice: collected, feedback, not counted) follows the same steps with the assignment notebook.',
               'Note any question you could not answer and start the next class with it.'])
    s['numbers_fn'] = 'numbers'
    return s


def numbers(F):
    """Rows of cohort numbers for the guide: F maps cohort code to facts."""
    codes = list(F)
    def row(label, g):
        return [label] + [g(F[c]) for c in codes]
    return [row('Rows in the file', lambda f: str(len(f['raw']))), row('After removing the repeated record_id', lambda f: str(len(f['raw'].drop_duplicates('record_id')))),
            row('After the three bad rows are removed', lambda f: str(f['b']['n_clean'])),
            row('Training, validation, test rows', lambda f: f'{f["b"]["n_tr"]}, {f["b"]["n_va"]}, {f["b"]["n_te"]}'),
            row('Baseline model, MAE', lambda f: f'{f["b"]["reg"]["baseline"]["mae"]:.2f} {f["unit"]}'), row('Multiple linear regression, MAE', lambda f: f'{f["b"]["reg"]["linear"]["mae"]:.2f} {f["unit"]}'),
            row('Decision tree max_depth 4, MAE', lambda f: f'{f["b"]["reg"]["tree"]["mae"]:.2f} {f["unit"]}'), row('Multiple linear regression, intercept, coefficient of load_pct, coefficient of ambient_c', lambda f: ', '.join(f'{f["b"]["lin"][k]:.3f}' for k in ('intercept', 'w_load', 'w_amb'))), row('RMSE: baseline model, multiple linear regression, decision tree', lambda f: ', '.join(f'{f["b"]["reg"][k]["rmse"]:.2f}' for k in ('baseline', 'linear', 'tree')) + f' {f["unit"]}')]
