"""Session 14: Machine learning, the workflow (supervised learning on the Nile Microfinance loans). Python lab: content/labs/s14_nb.py.

Every number comes from s14_facts.facts(), which is built on content/loans_canon.py (the one recipe shared by Sessions 14 to 17, 20, 23 and 24): pandas on loans.csv, the canonical
stratified split and the port of the scikit-learn tree. They are NumPy replica numbers: re-run on real scikit-learn in Colab before the course starts.
Numbers that depend on the random split are shown for the canonical split and as a range over ten other splits.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name):
    sp = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


FX = _load('s14_facts')
FX13 = _load('s13_facts')


def n0(x):
    return f'{int(round(x)):,}'


def build():
    F = FX.facts()
    G = FX13.facts()
    L = F['L']
    ex = F['ex']
    q = F['q_rates']
    e = F['q_edges']
    pc = lambda v: f'{v * 100:.1f}'
    assert F['n'] == 8000 and F['dflt'] == 1004 and F['bad_n'] == 2 and F['miss_n'] == 379 and F['n_te'] == 2000 and F['d_te'] == 251
    sess = dict(
        num=14, block='Module D: Machine learning', short_title='Machine learning workflow',
        title='Machine learning: the workflow, from loans data to a first model',
        question='What does it mean for a computer to learn from examples, and how do we know it did?',
        outcomes=['Name the parts of a supervised learning problem: records, features, target, training set and test set',
                  'Prepare data for a model: impossible values, imputation with a missing-indicator and a new feature, and see why a baseline model comes first',
                  'Split the data, fit a first model with scikit-learn, and explain the accuracy paradox on an imbalanced target'],
        outcome_icons=['notebook', 'gear', 'chart'],
        outcome_note=('Here is what you can do by the end of today. You can name the parts of a supervised learning problem: the records, the features, the target, the training set and the test set. '
                      'You can prepare data for a model, which means fixing impossible values, imputing missing values with a missing indicator, and building a new feature. You can say why a baseline model comes first. '
                      'And you can split the data, fit a first model with scikit-learn, and explain the accuracy paradox that appears when one answer is rare. We use eight thousand fictional loans from Nile Microfinance.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python machine learning lab',
        plan_caption='Ideas with pictures first. Then you open the notebook, prepare the loans and fit a first model.',
        plan_note=('We have two hours. The first ten minutes bring back Session 13 and set the question for today. Then forty-five minutes of concepts with no laptops open. '
                   'After a ten minute break we open a Colab notebook for the forty-five minute lab, where you prepare the loan file, split it, fit a baseline model and a first model. '
                   'In every step you predict first, run the cell, read the output and change one thing. The last ten minutes are an exit check and what you keep.'),
        recall_from='Session 13',
        recall=[('In the regression on weekly orders, what did a footfall coefficient of 0.0188 mean?', f'About {G["m3"]["b"][1] * 1000:.1f} more orders for each 1,000 more people at the door, holding promotion and rainfall fixed.'),
                ('What is a residual?', 'The actual value minus the predicted value for one record. A residual plot checks whether the errors have an even spread.'),
                (f'The promotion coefficient was {G["m3"]["b"][2]:.1f}. Does that prove the promotion caused the extra orders?', 'No. It shows an association. A cause needs an experiment or strong outside evidence.')],
        words=[('Supervised learning', 'A model learns the link between features (inputs) and a known target (the answer) from past records, then predicts the target for new records.'),
               ('Features and target', 'Features are the input variables. The target is the variable we predict. Statistics says independent and dependent variable.'),
               ('Training set and test set', 'The training set is what the model learns from. The test set is held back and used once at the end to score the model.'),
               ('Baseline model', 'The simplest possible model, such as always predicting the majority class (DummyClassifier). Every real model has to beat it.'),
               ('Class imbalance (accuracy paradox)', 'One class is far more common than the other, so a model that ignores the rare class can still have high accuracy.')],
        word_icons=['gear', 'flag', 'folder', 'check', 'question'],
        words_note=('Five words for today. Supervised learning means the model learns from past records where the answer is known. The features are the inputs and the target is the answer. '
                    'The training set is what the model learns from, and the test set is held back to score it once. A baseline model is the simplest possible prediction, and every real model has to beat it. '
                    'And class imbalance means one answer is far more common than the other, which leads to the accuracy paradox.'),
        keep='Keep your notebook and loans_prepared.csv, a clean file of 12 features and the target, with a three-sentence note: did the first model beat the baseline model, by how much, and what does accuracy hide?',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab files', value='Notebook and prepared file'), dict(label='Your note', value='Model against baseline'), dict(label='Next session', value='Classification')]),
        keep_title='Save your notebook, your prepared file and your three-sentence note',
        next='Session 15: Classification, yes or no questions. We predict default with logistic regression and a decision tree.', next_label='Next session',
        keep_note=('Before you go, save the notebook and the file loans prepared dot csv. That file is a clean table of twelve features and the target, so you can reload it with read csv instead of repeating the preparation. '
                   'Then write three sentences: did the first model beat the baseline model, by how much, and what does accuracy hide? Next session we take the same loans and fit two classification models properly, '
                   'including how to turn a probability into a decision.'),
        cover_note=('Welcome back. Until now we described data, explained it, and fitted a regression to explain a number. Today we start to predict. '
                    'We take eight thousand loans from Nile Microfinance, a fictional lender in Uganda, and ask which loans are likely to default. You will prepare the loan file, split it, fit a first model, '
                    'and compare it with a baseline model, the simplest predictor we can build. That comparison will change how you read every accuracy figure you meet.'),
        use_at_work='Frame a prediction problem, prepare the data, and judge a first model against a baseline.',
        slides=[])
    S = sess['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 13', headers=['Question', 'Short answer'], rows=[[q_, a_] for q_, a_ in sess['recall']], widths=[5.2, 6.8], icons=['chart', 'magnifier', 'shield'],
                  notes=(f'Here are the answers. A footfall coefficient of 0.0188 means about {G["m3"]["b"][1] * 1000:.1f} more orders for each thousand more people at the door, holding promotion and rainfall fixed. '
                         'A residual is the actual value minus the predicted value, and a residual plot checks that the errors have an even spread. '
                         f'And the promotion coefficient of {G["m3"]["b"][2]:.1f} shows an association only. A cause needs an experiment or strong outside evidence. '
                         'Today we move from explaining a number to predicting a yes or no. Which answer did you find hardest?')))

    S.append(dict(kind='compare', title='A rule you write in Excel and a rule a model learns from examples',
                  left=dict(head='Excel IF rule', points=['=IF(instalment_to_income>0.6,"Risky","OK")', 'The 0.6 is an illustrative hunch.', f'Flags {n0(F["hand_flag"])} of {n0(F["n"])} loans.']),
                  right=dict(head='Supervised learning', points=[f'Show {n0(F["n"])} past loans and what happened.', 'The computer finds the rule.', 'Test it on unseen loans.']),
                  verdict='Excel: you give the rule. Machine learning: you give examples.',
                  notes=(f'Machine learning rests on one idea, and you already know half of it. On the left is a rule you write in Excel: flag the loan as risky when the instalment-to-income ratio, the monthly instalment divided by monthly income, is above zero point six. Lenders also call it the payment-to-income ratio. '
                         f'The zero point six is a hunch, so it is illustrative. On all {n0(F["n"])} loans it flags {n0(F["hand_flag"])}. On the right is supervised learning. We show the computer {n0(F["n"])} past loans and what happened to each, '
                         'and it finds a rule itself. Then we test the rule on loans it has not seen, because a rule that only works on the past is no use to a lender. What would you want to know before trusting a learned rule?')))

    pic = F['pic']
    rows = [[str(r.age), f'{r.monthly_income_ugx:,.0f}', f'{r.loan_amount_ugx:,}', str(r.previous_late_payments), str(r.default)] for r in pic.itertuples()]
    S.append(dict(kind='wide', title='Supervised learning: features go in, the target comes out',
                  visual=dict(kind='ds_ft_table', headers=['age', 'monthly_income_ugx', 'loan_amount_ugx', 'previous_late_payments', 'default'], rows=rows, roles=['feature'] * 4 + ['target'], record_label='one loan'),
                  caption='Four real records of loans.csv. default is 1 for a borrower who stopped repaying.',
                  notes=('Here are four records of the loans file. Each record is one loan. The variables on the left are features, the inputs we know when the loan is approved: age, income, loan amount and earlier late payments. '
                         'The gold column is the target, the variable we want to predict. Here it is default, one when the borrower stopped repaying and zero when the loan was repaid. '
                         'During learning the model sees the features and the known target for thousands of records and works out how they are linked. Later it sees only the features of a new loan and must predict the target. '
                         'Which of these features would you expect to matter most?')))

    S.append(dict(kind='table', title='The Excel word, the statistics word and the machine learning word for each part',
                  headers=['In Excel', 'In statistics', 'In machine learning'],
                  rows=[['A row', 'Observation', 'Instance (record)'], ['The input columns', 'Independent variables (predictors)', 'Features'], ['The column you want to fill in', 'Dependent variable (response)', 'Target (label, for a class)'],
                        ['A yes or no column', 'Binary variable', 'Binary classification target'], ['Rows kept out of the analysis', 'Hold-out data', 'Test set']],
                  widths=[3.8, 4.2, 4.0], icons=['notebook', 'tag', 'flag', 'check', 'folder'], note='This course says feature and target from here on, and statistics words when the topic is explanation.',
                  notes=('Here is the translation table again, this time for machine learning. A row is an observation to a statistician and an instance or record to a machine learning engineer. '
                         'The input columns are independent variables or predictors in statistics, and features in machine learning. The column you want to fill in is the dependent variable, or the target. '
                         'When the target is a class it is also called a label. A yes or no column is a binary variable, and the rows you keep hidden are the test set. '
                         'From here on I say feature and target. Which of these words have you already met at work?')))

    S.append(dict(kind='table', title='Two kinds of supervised problem: regression predicts a number, classification predicts a category',
                  headers=['Problem type', 'The target is', 'Example from our data', 'Where'],
                  rows=[['Regression', 'A number', 'Weekly orders of a Lakeside branch', 'Session 13'], ['Binary classification', 'One of two classes (positive class and negative class)', 'Default: 1 (positive) or 0 (negative)', 'Today and Session 15'],
                        ['Multiclass classification', 'One of three or more classes', 'The theme of a customer message (queue, price, staff and more)', 'Session 21']],
                  widths=[2.9, 3.6, 3.9, 1.9], icons=['chart', 'flag', 'speech'],
                  notes=('Supervised problems come in two kinds, depending on the target. If the target is a number, such as weekly orders, the problem is regression, which we did last session. '
                         'If the target is a category, the problem is classification. Binary classification has two classes, and we call the one we want to find the positive class. For us the positive class is a loan that defaulted, and the negative class is a repaid loan. '
                         'Multiclass classification has three or more classes, such as the theme of a customer message, and we meet it in Session 21. Which kind of problem is your project question?')))

    S.append(dict(kind='stat', title='About 1 loan in 8 defaults: this is class imbalance', big=f'{F["rate"] * 100:.2f}%',
                  text=f'{n0(F["dflt"])} of the {n0(F["n"])} loans defaulted (the positive class). {n0(F["repaid"])} were repaid (the negative class). One class is far more common: class imbalance.',
                  visual=dict(kind='waffle', filled=round(F['rate'] * 100), label=f'About {round(F["rate"] * 100)} in every 100 loans default', size=16),
                  notes=(f'Let us meet the target. In the loans file, {n0(F["dflt"])} of the {n0(F["n"])} loans defaulted, which is {F["rate"] * 100:.2f} percent, about thirteen in every hundred. '
                         f'The defaulted loans are the positive class, because they are the ones we want to find. The other {n0(F["repaid"])} loans were repaid, the negative class. '
                         'When one class is much more common than the other, we say the data has class imbalance. Lenders live with this all the time, because the loans that hurt are the rare ones. '
                         'Hold that number, because a model that ignores the rare class can exploit it. How would you build the simplest possible predictor?')))

    S.append(dict(kind='formula', title=f'A baseline model that predicts repaid for every loan is {F["base_acc"] * 100:.2f} percent accurate',
                  formulas=[('Accuracy', r'$\mathrm{accuracy} = \frac{\mathrm{correct\ predictions}}{\mathrm{all\ predictions}}$'), ('Baseline on our test set', r'$\frac{' + f'{n0(F["n_te"] - F["d_te"])}'.replace(',', '{,}') + r'}{' + f'{n0(F["n_te"])}'.replace(',', '{,}') + r'} = ' + f'{F["base_acc"]:.4f}' + r'$')],
                  symbols=[['correct predictions', 'Predictions that equal the true answer.', f'{n0(F["n_te"] - F["d_te"])} repaid loans'], ['all predictions', 'Loans in the test set.', n0(F['n_te'])],
                           ['baseline model', 'Predicts the majority class every time (DummyClassifier, strategy most_frequent).', 'always repaid']],
                  size=20, note=f'Every other model has to beat {F["base_acc"]:.4f}. Accuracy is the share of correct predictions.',
                  notes=(f'The simplest possible model is a baseline model. It looks at the training set, finds the majority class, repaid, and predicts it for every loan. In scikit-learn it is the DummyClassifier with the strategy most frequent. '
                         f'Accuracy is the number of correct predictions divided by all predictions. On our test set of {n0(F["n_te"])} loans, {n0(F["n_te"] - F["d_te"])} were repaid, so the baseline is right {n0(F["n_te"] - F["d_te"])} times, an accuracy of {F["base_acc"]:.4f}. '
                         'That is the score a real model must beat. A model that scores less than the baseline has learned nothing useful. Does eighty-seven percent sound good to you?')))

    S.append(dict(kind='idea', title='The accuracy paradox: 87.45 percent accurate and not one default caught',
                  visual=dict(kind='ds_confusion_pos', tp=0, fp=0, fn=F['d_te'], tn=F['n_te'] - F['d_te'], pos='defaulted', neg='repaid'),
                  lead='Accuracy hides the rare class.',
                  points=[f'Recall (sensitivity): the share of real defaults caught. Here 0 of {F["d_te"]}.', 'A bank needs the defaults.', 'This is the accuracy paradox.'],
                  notes=(f'Here is the baseline model drawn as a confusion matrix, a two by two count of what the model said against what was true. It said repaid for all {n0(F["n_te"])} loans. '
                         f'So {n0(F["n_te"] - F["d_te"])} true negatives are correct and all {F["d_te"]} defaults are false negatives: missed. Accuracy is {F["base_acc"] * 100:.2f} percent, yet the share of real defaults that the model catches, called recall or sensitivity, is zero. '
                         'This is the accuracy paradox. When one class is rare, a model can be highly accurate and still useless for the job. Session 16 studies the full set of measures. Which number would a credit manager care about here?')))

    S.append(dict(kind='table', title='Look at the data before you model it: three problems in the loans file',
                  headers=['Problem', 'What we found', 'What we do'],
                  rows=[['Impossible values', f'{F["bad_n"]} ages that cannot be right: {F["bad_ages"][0]} and {F["bad_ages"][1]}', f'Replace with the median of the valid ages, {F["age_med"]}'],
                        ['Missing values', f'{F["miss_n"]} blank incomes ({F["miss_pct"]:.1f} percent)', 'Median imputation, plus a missing-indicator flag'],
                        ['A column that leaks the answer', f'collection_calls is above 0 for {F["calls_default"] * 100:.0f} percent of defaulted loans', 'Leave it out of the features']],
                  widths=[3.4, 4.8, 3.8], icons=['cross', 'question', 'lock'], note='Every change goes in a data cleaning log with its counts, as in Session 8.',
                  notes=(f'Before any model, check the data. The loans file has three problems. First, impossible values: {F["bad_n"]} borrowers have ages of {F["bad_ages"][0]} and {F["bad_ages"][1]}, which cannot be right. We replace them with the median of the valid ages, {F["age_med"]}. '
                         f'Second, {F["miss_n"]} loans have a blank monthly income, {F["miss_pct"]:.1f} percent. We fill them with the median and add a flag. Third, the column collection calls is above zero for every defaulted loan, because it is recorded after the loan goes bad. '
                         'It leaks the answer, so we leave it out. We record every change with its count in a data cleaning log. Which of these would you have noticed on your own?')))

    imp = F['imp_rows']
    raw = F['raw']
    rowsi = []
    for i in imp:
        v = raw.monthly_income_ugx[i]
        rowsi.append([str(raw.loan_id[i]), 'blank' if v != v else f'{v:,.0f}', '1' if v != v else '0', f'{L.monthly_income_ugx[i]:,.0f}'])
    S.append(dict(kind='wide', title='Imputation with a missing-indicator: flag the blank first, then fill it with the median',
                  visual=dict(kind='ds_impute', headers=['loan_id', 'monthly_income_ugx (raw)', 'income_missing', 'monthly_income_ugx (imputed)'], rows=rowsi,
                              note=f'Median of the {n0(F["known_n"])} known incomes: {n0(F["inc_med"])} UGX. Make the flag first: after filling, the blanks are gone.'),
                  caption=f'Blank incomes default at {pc(F["miss_rate"])} percent, the others at {pc(F["known_rate"])}. The flag keeps that information.',
                  notes=(f'Imputation means filling a missing value. The simplest kind is median imputation. In the picture, the gold rows have a blank income. We first make a missing indicator, a flag column that is one where the income was blank and zero elsewhere. '
                         f'Then we fill the blank with the median of the {n0(F["known_n"])} known incomes, {n0(F["inc_med"])} shillings. The order matters: after filling, the blanks are gone and the flag would be all zeros. '
                         f'In this file the loans with blank incomes default at {pc(F["miss_rate"])} percent against {pc(F["known_rate"])} for the others, so the blank carries little information here, but the flag costs nothing. Why use the median? What would the mean do with a few very high incomes?')))

    S.append(dict(kind='formula', title='Feature engineering: build a new feature, the instalment-to-income ratio, from three existing variables',
                  formulas=[('Ratio', r'$\mathrm{instalment\_to\_income} = \frac{1.15 \times \mathrm{loan\_amount}}{\mathrm{term\_months} \times \mathrm{monthly\_income}}$'),
                            (f'Loan {ex["id"]}', r'$\frac{1.15 \times ' + f'{ex["loan"]:,}'.replace(',', '{,}') + r'}{' + f'{ex["term"]} \\times ' + f'{ex["inc"]:,.0f}'.replace(',', '{,}') + r'} = ' + f'{ex["ratio"]:.2f}' + r'$')],
                  symbols=[['loan_amount, term_months', 'Loan size in UGX and the number of months to repay it.', f'{ex["loan"]:,} UGX, {ex["term"]} months'], ['monthly_income', 'Income per month in UGX, after imputation.', f'{ex["inc"]:,.0f} UGX'],
                           ['1.15', 'Illustrative assumption: the borrower repays the loan plus 15 percent in charges.', 'not in the file']],
                  size=20, note=f'Share of monthly income for one instalment (1.15 is assumed). Median {F["ratio_med"]:.2f}, highest {F["ratio_max"]:.1f}.',
                  notes=(f'Feature engineering means building a new variable from existing ones, often the step that helps a model most. A lender thinks in terms of the instalment compared with income. We compute the monthly instalment as the loan amount times one point one five, divided by the term in months. '
                         f'The one point one five is an illustrative assumption for charges, because the file has no interest rate. Dividing by monthly income gives the instalment-to-income ratio, which lenders also call the payment-to-income ratio. In our file the column is called instalment to income. For loan {ex["id"]} it is {ex["ratio"]:.2f}: about sixty percent of the borrower income each month. '
                         f'The median ratio is {F["ratio_med"]:.2f}. Which other feature could you build from these columns?')))

    labels = [f'Lowest quarter (up to {e[0]:.2f})', f'Second quarter ({e[0]:.2f} to {e[1]:.2f})', f'Third quarter ({e[1]:.2f} to {e[2]:.2f})', f'Highest quarter (above {e[2]:.2f})']
    S.append(dict(kind='idea', title=f'Default rate climbs with the instalment-to-income ratio: {pc(q[3])} percent in the highest quarter',
                  visual=dict(kind='bars', items=[dict(label=l, value=float(pc(v)), hl=(i == 3)) for i, (l, v) in enumerate(zip(labels, q))], unit=' %', size=17),
                  lead='Each bar is the percentage of loans in that group that defaulted.',
                  points=['Four equal groups of 2,000 loans, cut by the ratio.', f'The highest group defaults at {q[3] / q[0]:.1f} times the rate of the lowest.'],
                  notes=(f'Does the new feature help? We cut the loans into four groups of two thousand by the ratio and looked at the default rate in each. In the lowest quarter, {pc(q[0])} percent default. In the second, {pc(q[1])}. In the third, {pc(q[2])}. '
                         f'In the highest quarter, where the instalment takes more than {e[2]:.2f} of income, {pc(q[3])} percent default. That is more than five times the lowest group. '
                         'A feature that separates the classes like this gives a model something to learn from. It does not prove cause, only that the groups differ. What does this say about the rule of thumb in the Excel formula?')))

    S.append(dict(kind='compare', title='Use only what is known when the decision is made: data leakage',
                  left=dict(head='Known at approval', points=['age, income, loan amount, term', 'savings, previous late payments', 'instalment-to-income ratio']),
                  right=dict(head='Recorded after the loan goes bad', points=[f'collection_calls is above 0 for {F["calls_default"] * 100:.0f} percent of defaulted loans and {F["calls_repaid"] * 100:.0f} percent of repaid ones.', 'It looks brilliant and is useless at approval.']),
                  verdict='Leave it out. Session 16 studies data leakage.',
                  notes=(f'One more preparation decision. Some columns are only known after the outcome. Collection calls are recorded when a lender chases a loan that has gone bad, so the column is above zero for {F["calls_default"] * 100:.0f} percent of defaulted loans '
                         f'and {F["calls_repaid"] * 100:.0f} percent of repaid ones. A model that uses it looks brilliant on the data and is useless at approval time, when no calls exist yet. '
                         'This is data leakage: information about the target sneaks into the features. The rule is to use only what is known at the moment of the decision. We leave collection calls out, and Session 16 studies leakage properly. Which other column might leak?')))

    S.append(dict(kind='wide', title='Hold back a test set before the model sees anything: the train and test split',
                  visual=dict(kind='rowsplit', parts=[dict(label='Training set', sub='75 percent', n=F['n_tr'], role='The model learns from these loans.', fill='ink'), dict(label='Test set', sub='25 percent', n=F['n_te'], role='Held back. Scored once, at the end.', fill='gold')]),
                  caption='The function train_test_split shuffles the 8,000 loans and cuts them in two.',
                  notes=(f'Now the most important habit in machine learning. A model can memorise the records it learned from, so a score on those records proves nothing. We split the loans first. The training set, {n0(F["n_tr"])} loans, is what the model learns from. '
                         f'The test set, {n0(F["n_te"])} loans, is held back and scored once at the end, like covering the last rows of a sheet with paper. In scikit-learn the function is train test split. '
                         'It shuffles the rows and cuts them. Two arguments matter: stratify, and random state. What would happen if you peeked at the test set and adjusted the model?')))

    S.append(dict(kind='table', title='Stratifying keeps the default rate the same in both parts',
                  headers=['Part', 'Loans', 'Defaults', 'Default rate'],
                  rows=[['All loans', n0(F['n']), n0(F['dflt']), f'{F["rate"] * 100:.2f} %'], ['Training set', n0(F['n_tr']), n0(F['d_tr']), f'{F["rate_tr"] * 100:.2f} %'], ['Test set', n0(F['n_te']), n0(F['d_te']), f'{F["rate_te"] * 100:.2f} %']],
                  widths=[3.4, 2.4, 2.4, 3.0], icons=['folder', 'notebook', 'check'],
                  note='stratify=y keeps the class proportions in both parts. random_state=42 fixes the shuffle, so you and I get the same split.',
                  notes=(f'A random cut could by bad luck put too few defaults in the test set. Stratifying prevents that. With stratify set to y, both parts keep the default rate of {F["rate"] * 100:.2f} percent. '
                         f'The training set has {F["d_tr"]} defaults in {n0(F["n_tr"])} loans, and the test set has {F["d_te"]} in {n0(F["n_te"])}. The random state fixes the shuffle, so a colleague who runs your code gets the same split. '
                         'With the same seed, every computer running the same scikit-learn version gets the same split, so the counts in this table will match yours. Why do the test counts have to be known before we score anything?')))

    S.append(dict(kind='wide', title='The train, validate, test discipline: tune on the validation set, use the test set once',
                  visual=dict(kind='rowsplit', parts=[dict(label='Training set', sub='fit', n=4500, role='Learn parameters.', fill='ink'), dict(label='Validation set', sub='compare', n=1500, role='Compare and tune.', fill='paper'),
                                                      dict(label='Test set', sub='final', n=F['n_te'], role='One final score.', fill='gold')]),
                  caption='Illustrative sizes. Today: two parts. Session 17: cross-validation plays the validation set.',
                  notes=('Real projects use three parts, called the train, validate, test discipline. The model learns its parameters on the training set. You compare models and choose settings, called hyperparameters, on the validation set. '
                         'Only when you have chosen the final model do you score it once on the test set. If you tuned on the test set, the final score would be optimistic, because the test set would have influenced your choices. '
                         'The sizes on the slide are illustrative. Today we keep it simple with two parts. In Session 17 you meet cross-validation, which repeats the validation step five times on the training set and plays the role of the validation set. Credit teams also often split by date, training on earlier loans and testing on later ones, which is called a time-based split. Why is a validation set needed at all?')))

    S.append(dict(kind='wide', title='CRISP-DM is the standard six-phase cycle for a data and machine learning project',
                  visual=dict(kind='ds_crispdm', items=['1 Business understanding', '2 Data understanding', '3 Data preparation', '4 Modelling', '5 Evaluation', '6 Deployment'], highlight=[1, 2, 3, 4], center='Data'),
                  caption='CRISP-DM stands for Cross-Industry Standard Process for Data Mining. The arrows loop.',
                  notes=('Our workflow follows a standard that employers recognise, CRISP-DM, which stands for Cross-Industry Standard Process for Data Mining. It has six phases. Business understanding: what is the question and the decision? '
                         'Data understanding: what do we have and what is wrong with it? Data preparation: clean, impute, build features and split. Modelling: fit a baseline model and a first model. Evaluation: score on data the model never saw. '
                         'Deployment: put it to work and monitor it, which we do in Sessions 23 and 24. The arrows form a loop, because a poor result sends you back to an earlier phase. The gold phases are today. Where do you think most of the time goes?')))

    S.append(dict(kind='steps', title='Our workflow in five steps, from the raw loans to a score on the test set',
                  steps=[dict(head='1 Prepare', text='Ages, incomes, ratio', icon='gear'), dict(head='2 Split', text='Train and test', icon='folder'), dict(head='3 Baseline', text='Always repaid', icon='flag'),
                         dict(head='4 Fit', text='First model', icon='calculator'), dict(head='5 Evaluate', text='Test set, once', icon='check')], highlight=None,
                  caption='Preparation comes first and the baseline comes before the model. The test set is used only in step 5.',
                  notes=('Here is the workflow in the order you follow it. Step one, prepare the data: fix impossible ages, impute incomes with a flag, and build the instalment-to-income ratio. Step two, split into a training set and a test set. '
                         'Step three, fit the baseline model, the always repaid predictor, so you know the score to beat. Step four, fit the first model on the training set. Step five, predict the test set and evaluate. '
                         'The order matters. In this course we prepare before we split, on purpose. The medians then come from all eight thousand loans, which lets the test loans influence the training data a little. That is a small data leakage risk, called train-test contamination, and the safe order follows this slide. Which step would you check twice?')))

    S.append(dict(kind='code', title='The safe order: split first, then let a pipeline learn the median from the training rows only',
                  code="X_train, X_test, y_train, y_test = train_test_split(\n    X_raw, y, test_size=0.25, stratify=y,\n    random_state=42)\nimputer = SimpleImputer(strategy='median')\ntree = DecisionTreeClassifier(\n    max_depth=3, random_state=42)\npipe = make_pipeline(imputer, tree)\npipe.fit(X_train, y_train)\ny_pred = pipe.predict(X_test)",
                  reads=['Lines 1 to 3: split first. X_raw still has its blanks.', 'Lines 4 to 7: an imputer, a tree, and a pipeline that chains them.',
                         f'Line 8: fit learns the median from the training rows only: UGX {n0(F["inc_med_train"])}, against {n0(F["inc_med"])} on all loans.', 'Line 9: test loans get the training median.'],
                  notes=(f'Here is the safe order, and it is the one you will use at work. In this course we filled the blank incomes with the median of all {n0(F["n"])} loans before the split, on purpose, to keep the lab short. '
                         f'That is a small leakage risk: the test loans helped to decide the median. How small? The median income is {n0(F["inc_med"])} shillings on all loans and {n0(F["inc_med_train"])} on the {n0(F["n_tr"])} training loans. '
                         'The safe version splits first. A pipeline, which chains steps into one model, then learns the median from the training rows only. '
                         'The flag income missing is a fixed rule, so it can come before the split. The ratio is built from income, so in a full pipeline it follows the imputer, and Session 20 builds that. Session 16 names the problem, train-test contamination. Why does the pipeline protect the test set?')))

    S.append(dict(kind='idea', title=f'Fit and predict: the first model beats the baseline model by only {(F["acc"] - F["base_acc"]) * 100:.1f} points of accuracy',
                  visual=dict(kind='bars', items=[dict(label='Baseline model: always repaid', value=round(F['base_acc'], 4)), dict(label='Decision tree, max_depth=3', value=round(F['acc'], 4), hl=True)], unit='', size=17, max_value=1.0),
                  lead='model.fit learns from the training set. model.predict returns a prediction for each test loan.',
                  points=[f'Test accuracy {F["acc"]:.4f} against {F["base_acc"]:.4f}.', f'Over ten different splits: {F["acc_lo"]:.3f} to {F["acc_hi"]:.3f}.', f'The tree asks about {F["root_feat"]} first.'],
                  notes=(f'Now the first model. We use a decision tree with a maximum depth of three, a model that learns a few yes or no questions about the features. You meet trees properly in Session 15. We fit it on the training set with model dot fit, '
                         f'and predict the test set with model dot predict. The accuracy is {F["acc"]:.4f}, against {F["base_acc"]:.4f} for the baseline. Over ten different random splits it ranges from {F["acc_lo"]:.3f} to {F["acc_hi"]:.3f}, '
                         f'so a different split gives a slightly different number. The first question the tree asks is about the {F["root_feat"]}, the feature we built, at about {F["root_thr"]:.2f}. Is a gain of about one point worth celebrating?')))

    S.append(dict(kind='idea', title=f'The confusion matrix shows what accuracy hides: {F["fn"]} defaults missed',
                  visual=dict(kind='ds_confusion_pos', tp=F['tp'], fp=F['fp'], fn=F['fn'], tn=F['tn'], pos='defaulted', neg='repaid'),
                  lead=f'The tree catches {F["tp"]} of the {F["d_te"]} defaults.',
                  points=[f'Recall {F["recall"]:.2f}: about 1 default in 6 is caught.', f'Precision {F["precision"]:.2f}: of the {F["tp"] + F["fp"]} loans flagged, {F["tp"]} really defaulted.', f'Over ten splits, {F["tp_lo"]} to {F["tp_hi"]} defaults caught.'],
                  notes=(f'Here is the first model as a confusion matrix. Of the {F["d_te"]} real defaults in the test set, the tree caught {F["tp"]} and missed {F["fn"]}. It raised {F["fp"]} false alarms. '
                         f'Recall, the share of real defaults caught, is {F["recall"]:.2f}, so about one default in six. Precision, the share of flagged loans that really defaulted, is {F["precision"]:.2f}. '
                         f'Across ten splits the number caught ranges from {F["tp_lo"]} to {F["tp_hi"]}. The model is better than the baseline, which caught none, but most defaults still slip through. '
                         'We improve this with other models and thresholds in Sessions 15 and 16. Would you lend using this model alone?')))

    S.append(dict(kind='table', title='Accuracy alone ranks the models wrongly: the Excel rule has lower accuracy and finds far more defaults',
                  headers=['Predictor on the test set', 'Accuracy', 'Defaults caught', 'Recall'],
                  rows=[['Baseline model: always repaid', f'{F["base_acc"]:.4f}', f'0 of {F["d_te"]}', '0.00'], [f'Excel rule: instalment_to_income above 0.6', f'{F["h_acc"]:.4f}', f'{F["h_tp"]} of {F["d_te"]}', f'{F["h_recall"]:.2f}'],
                        ['Decision tree, max_depth=3', f'{F["acc"]:.4f}', f'{F["tp"]} of {F["d_te"]}', f'{F["recall"]:.2f}']],
                  widths=[5.2, 2.1, 2.7, 2.0], icons=['flag', 'calculator', 'gear'],
                  note=f'The Excel rule also raises {F["h_fp"]} false alarms; the tree raises {F["fp"]}. Which error costs more is a business question. Session 15 turns it into a decision threshold (rule: 0.0909 with illustrative costs).',
                  notes=(f'Put the three predictors side by side on the same test set. The baseline has the best looking accuracy of the first two, {F["base_acc"]:.4f}, and catches no defaults. '
                         f'The Excel rule, instalment-to-income ratio above zero point six, has a lower accuracy, {F["h_acc"]:.4f}, but catches {F["h_tp"]} of the {F["d_te"]} defaults, a recall of {F["h_recall"]:.2f}. The tree has the highest accuracy, {F["acc"]:.4f}, but catches only {F["tp"]}. '
                         f'The Excel rule also raises {F["h_fp"]} false alarms, against {F["fp"]} for the tree. So which model is best depends on the cost of a missed default against the cost of a false alarm. That is a business question. Session 15 turns it into a decision threshold: with illustrative costs of one million for a missed default and one hundred thousand for a false alarm, flag a loan at probability 0.0909 or more. '
                         'Which error would cost your organisation more?')))

    S.append(dict(kind='table', title='Where you will use this at work: predict which cases need attention first',
                  headers=['Your job', 'The question you can answer', 'The tools you would use'],
                  rows=[['Credit analyst at a bank or microfinance lender in Kampala', 'Which loan applications are likely to default, using only what is known at approval?', 'pandas and scikit-learn, with a baseline model first'],
                        ['Revenue officer at a district local government', 'Illustrative: which taxpayers are likely to file late?', 'pandas and scikit-learn, results shared in Excel'],
                        ['Customer care lead at a mobile money network', 'Illustrative: which customers are likely to leave next month?', 'scikit-learn, Power BI for the dashboard'],
                        ['Data officer at a health programme', 'Illustrative: which clients are likely to miss a follow-up visit?', 'scikit-learn, with the test set held back']],
                  widths=[3.8, 4.8, 3.4], icons=['coin', 'doc', 'phone', 'clinic'],
                  notes=('Where will you use this on Monday? A credit analyst at a bank or microfinance lender in Kampala can predict which applications are likely to default, using only what is known at approval, and always starts with a baseline model. '
                         'A revenue officer at a district local government could predict which taxpayers file late. A customer care lead at a mobile money network could predict which customers leave next month. '
                         'A data officer at a health programme could predict which clients miss a follow-up visit. Those three are illustrative examples. In every case the workflow is the same: prepare, split, baseline, fit, evaluate. '
                         'Which of these is closest to your job?')))

    S.append(dict(kind='table', title='Three habits that make a model result trustworthy',
                  headers=['Habit', 'In practice', 'Why'],
                  rows=[['Fix the random seed', 'random_state=42 in train_test_split and in the model', 'A colleague repeats your result exactly (reproducibility).'], ['Keep the test set untouched', 'Score it once, at the end', 'Otherwise the final score is too optimistic.'],
                        ['Write a data cleaning log', f'{F["bad_n"]} ages replaced, {F["miss_n"]} incomes imputed, 1 feature built, 1 column left out', 'Anyone can audit what you changed.']],
                  widths=[3.3, 4.7, 4.0], icons=['key', 'lock', 'notebook'],
                  notes=('Three habits make a result trustworthy. First, fix the random seed. Setting random state to forty-two in the split and in the model means a colleague who runs your code gets exactly your result, which is called reproducibility. '
                         'Second, keep the test set untouched until the end, and score it once. Otherwise the final score is too optimistic. Third, write a data cleaning log: how many ages you replaced, how many incomes you imputed, which feature you built and which column you left out. '
                         'Anyone can then audit what you changed. Which of these habits do you already have in Excel?')))

    S.append(dict(kind='code', title='Read the recipe before the lab: split, baseline, fit, predict',
                  code="X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.25, stratify=y, random_state=42)\nbaseline_model = DummyClassifier(\n    strategy='most_frequent').fit(X_train, y_train)\nmodel = DecisionTreeClassifier(\n    max_depth=3, random_state=42)\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)",
                  reads=['Lines 1 and 2: split into training and test sets.', 'Lines 3 and 4: the baseline model learns the majority class.', 'Lines 5 to 7: make the first model and fit it on the training set.', 'Line 8: predict the test set. y_pred holds one 0 or 1 per test loan.'],
                  notes=('Before the lab, read the recipe. The first call is train test split. It takes the features X and the target y and returns four things: the training features and test features, then the training target and test target. '
                         'Next we fit the baseline model with the strategy most frequent. Then we create the decision tree with a maximum depth of three and a random state, and call fit on the training set only. '
                         'Finally predict on the test features gives y pred, one zero or one for each test loan. Notice that the test target is never passed to fit. Which line would you change to make the split twenty percent?')))

    S.append(dict(kind='divider', title='Part 2: the machine learning lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the notebook for Session 14 in Google Colab and run the first cell, which puts the data files next to it. '
                         'In every step you predict first, then run, then read the output, then change one thing. Write your prediction before you run the cell.')))

    S.append(dict(kind='steps', title='The lab has five steps and ends with a prepared file and a three-sentence note',
                  steps=[dict(head='1 Look', text='Shape, default rate', icon='magnifier'), dict(head='2 Prepare', text='Ages, incomes, ratio', icon='gear'), dict(head='3 Split', text='Features, target, train, test', icon='folder'),
                         dict(head='4 Baseline', text='Always repaid', icon='flag'), dict(head='5 First model', text='Fit, predict, read', icon='calculator')], highlight=None,
                  caption='Predict, run, read, change in each step. Checks tell you when your numbers match.',
                  notes=('Here is the map of the lab. Step one, look at the loans and the default rate. Step two, prepare the data: the impossible ages, the missing incomes with a flag, and the instalment-to-income ratio. '
                         'Step three, choose the twelve features and the target, leaving out the leaking column, and split. Step four, fit the baseline model and score it. '
                         'Step five, fit the decision tree, predict, and read the confusion matrix. You finish by saving the prepared file and writing three sentences. Each step has a predict prompt and a check. Please do not skip the predictions.')))

    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Shape of the loans, and the default rate', f'{n0(F["n"])} rows, {F["cols"]} columns, {F["rate"]:.4f}'], ['Impossible ages, and the median of the valid ages', f'{F["bad_n"]} and {F["age_med"]}'],
                        ['Blank incomes, and the median income', f'{F["miss_n"]} and {n0(F["inc_med"])}'], ['Median instalment-to-income ratio, and default rate in its top quarter', f'{F["ratio_med"]:.2f} and {pc(q[3])} percent'],
                        ['Shape of X', f'{n0(F["n"])} rows, 12 columns'], ['Test loans, and defaults in the test set', f'{n0(F["n_te"])} and {F["d_te"]}'], ['Baseline accuracy on the test set', f'{F["base_acc"]:.4f}'],
                        ['Tree accuracy and recall on the test set', f'About {F["acc"]:.4f} and {F["recall"]:.2f}']],
                  widths=[7.2, 4.8], icons=['grid', 'cross', 'question', 'chart', 'notebook', 'folder', 'flag', 'check'], note=f'Tree numbers can differ a little between library versions. Ten other splits give accuracy {F["acc_lo"]:.3f} to {F["acc_hi"]:.3f} and recall {F["rec_lo"]:.2f} to {F["rec_hi"]:.2f}.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The numbers about the data must match exactly. The numbers about the tree can differ a little with the library version, so yours may differ in the last digit, and the table gives the range over ten other splits. '
                         'The baseline accuracy should match exactly, because the stratified test set always holds the same number of defaults. If your tree accuracy is below the baseline accuracy, what could be wrong?')))

    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['KeyError or AttributeError on a column name', 'A column name is misspelt, for example monthly_income instead of monthly_income_ugx.', 'Print loans.columns and copy the name.'],
                        ['income_missing is all zeros', 'You filled the blanks before making the flag.', 'Make the flag first. Reload the file and rerun.'], ['ValueError: Input contains NaN', 'A blank is still in X.', 'Check X.isna().sum() and fill the incomes.'],
                        ['Very high accuracy of 0.99 or more', 'collection_calls is in the features, so the answer leaks.', 'Remove collection_calls and rerun.'], ['Tree accuracy is below the baseline', 'You scored the training set, or the split used the wrong y.', 'Score X_test and y_test only.']],
                  widths=[3.8, 4.4, 3.8], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. A key error on a column name usually means a misspelt name, so print the columns and copy. If income missing is all zeros, you filled the blanks before making the flag, so reload and rerun in the right order. '
                         'A value error about NaN means a blank is still in X. An accuracy of ninety-nine percent or more is a warning, because collection calls has leaked the answer into the features. '
                         'And a tree accuracy below the baseline means you scored the wrong rows. Read the message first. It usually tells you the answer.')))

    S.append(dict(kind='table', title='Your keepsake: a prepared file and a three-sentence note on the first model',
                  headers=['What you keep', 'What it holds', 'Where it comes from'],
                  rows=[['loans_prepared.csv', '8,000 rows: 12 features and the target default, with no blanks', 'Notebook step 5'], ['Note, sentence 1', 'Did the first model beat the baseline model, and by how many points?', 'Notebook step 5'],
                        ['Note, sentence 2', 'How many of the real defaults did it catch?', 'Confusion matrix'], ['Note, sentence 3', 'What does accuracy hide, and what would you try next?', 'Slides on the accuracy paradox']],
                  widths=[3.3, 5.6, 3.1], icons=['folder', 'check', 'magnifier', 'question'],
                  notes=('This is what you keep. First, the file loans prepared dot csv, eight thousand rows with twelve features and the target, no blanks. You can reload it with read csv instead of repeating the preparation. '
                         'Second, a three sentence note. Sentence one: did the first model beat the baseline model, and by how many points of accuracy? Sentence two: how many of the real defaults did it catch? '
                         'Sentence three: what does accuracy hide, and what would you try next? Write them in the last cell of your notebook. Which of the three will be hardest to write?')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'A model predicts repaid for every loan and scores {F["base_acc"]:.4f} on the test set. What is it called, and why is the score not impressive?', 'A baseline model. The score is just the share of the majority class, and the model catches no defaults.'],
                        ['Why do we make the missing-indicator flag before we fill the blanks?', 'After filling, the blanks are gone, so the flag could not mark them.'],
                        ['Why is collection_calls left out of the features?', 'It is recorded after the loan goes bad, so it leaks the answer. This is data leakage.']],
                  widths=[5.8, 6.2], icons=['flag', 'question', 'lock'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, a model predicts repaid for every loan and scores about eighty-seven percent: what is it called and why is the score not impressive? '
                         'Two, why do we make the missing indicator flag before we fill the blanks? Three, why is collection calls left out of the features? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 15. If one surprised you, look at that step of your notebook again tonight.')))

    sess['facilitator'] = dict(
        prep=['Open the Session 14 notebook in Colab before anyone arrives and run it once. Scikit-learn is preinstalled in Colab at the time of writing.',
              'Every number on the slides and in the notebook checks comes from a NumPy replica of the scikit-learn split and tree (content/loans_canon.py), because scikit-learn was not available when the deck was built. Before the course starts, run the solution notebook on real scikit-learn in Colab. First confirm that X_test.index[:10] is [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150] and that X_test.index.sum() is 8,081,998. If it is not, the split differs and every number must be recomputed. Then compare accuracy 0.8875, 41 defaults caught, 15 false alarms and 210 missed.',
              'Write the check table (slide 32 of the deck) on the board before the lab.', 'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.',
              'The 1.15 charge factor in the instalment-to-income ratio is an illustrative assumption, not a Nile Microfinance rate. Say so. The medians are computed before the split on purpose (a small leakage risk); the safe-order slide shows the pipeline version.'],
        misconceptions=[('Accuracy of 87 percent is a good model', 'It equals the share of repaid loans, so a model that predicts repaid every time scores it. Compare with the baseline and look at recall.'),
                        ('Split the data after you have tuned the model on all of it', 'Split first. The test set must not influence any choice.'),
                        ('Fill the blank incomes first, then flag them', 'After filling there is nothing to flag. Make the flag first.'),
                        ('Preparing all the data before the split is always safe', 'Medians computed on all rows let the test rows influence training, a small data leakage risk. We accept it for teaching. The safe order is split first, then a pipeline learns the median from the training rows.'),
                        ('A feature that predicts perfectly is a great feature', 'It may leak the answer, as collection_calls does. Ask whether it is known at the time of the decision.'),
                        ('Features and target are new words for variables', 'A variable is any column. Features are the inputs and the target is the one we predict.')],
        probes=[('What is the positive class here?', 'A defaulted loan.'), ('What does a baseline model predict?', 'The majority class for every record.'), ('Why stratify the split?', 'To keep the default rate the same in training and test sets.'),
                ('What does random_state do?', 'Fixes the shuffle so the split can be repeated.'), ('What is recall?', 'The share of real positives that the model catches.'),
                ('What is imputation?', 'Filling a missing value, here with the median.'), ('What is feature engineering?', 'Building a new variable from existing ones, such as the instalment-to-income ratio.'), ('Which CRISP-DM phase is the split in?', 'Data preparation.')],
        lab_steps=[('Step 1: look', f'{n0(F["n"])} rows, {F["cols"]} columns, default rate {F["rate"]:.4f}.'), ('Step 2: prepare', f'{F["bad_n"]} ages, {F["miss_n"]} incomes, median income {n0(F["inc_med"])}, median instalment-to-income ratio {F["ratio_med"]:.2f}.'),
                   ('Step 3: features and split', f'X is {n0(F["n"])} by 12. Test set {n0(F["n_te"])} loans with {F["d_te"]} defaults.'), ('Step 4: baseline', f'Accuracy {F["base_acc"]:.4f}, recall 0.'),
                   ('Step 5: first model', f'Accuracy {F["acc"]:.4f}, {F["tp"]} defaults caught, {F["fp"]} false alarms, {F["fn"]} missed, recall {F["recall"]:.2f}. Ten other splits give accuracy {F["acc_lo"]:.3f} to {F["acc_hi"]:.3f}. Save the file and write the note.')],
        rescue=['If the concepts run over, shorten the habits table (slide 28) and the validation set slide; the lab covers the split.', 'If only 30 minutes of lab remain, do steps 1 to 4 together on the screen and set step 5 as homework.',
                'If a learner has a different accuracy, check the split settings: stratify=y and random_state=42, and test_size=0.25.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to keep loans_prepared.csv.', 'Note any question you could not answer and open Session 15 with it.'],
        lab_answer_key=[['Step 1 PREDICT: what share of loans default?', f'About {F["rate"] * 100:.1f} percent: {n0(F["dflt"])} of {n0(F["n"])}.'], ['Step 2 READ: why flag the missing incomes before filling them?', 'After filling, the blanks cannot be found.'],
                        ['Step 2 CHANGE: use the mean income instead of the median.', 'The imputed value changes a little. The median is safer when incomes are skewed.'], ['Step 3 READ: why is collection_calls left out?', f'It is above 0 for {F["calls_default"] * 100:.0f} percent of defaulted loans because it is recorded after the loan goes bad.'],
                        ['Step 4 PREDICT: what accuracy will the baseline model get?', f'{F["base_acc"]:.4f}, the share of repaid loans in the test set.'], ['Step 5 READ: did the tree beat the baseline, and what did it catch?', f'Accuracy about {F["acc"]:.3f}, a gain of about one point, with recall about {F["recall"]:.2f}.'],
                        ['Step 5 CHANGE: set max_depth to 1, then 6.', f'On our split depth 1 gives accuracy {F["depth"][1][0]:.3f} and recall {F["depth"][1][1]:.2f}; depth 6 gives {F["depth"][6][0]:.3f} and {F["depth"][6][1]:.2f}. A deeper tree is not better, and accuracy and recall move differently. Do not choose a depth by the test score; Session 17 shows how cross-validation on the training rows chooses it.'],
                        ['Step 9 CHANGE: compute the median income on the training rows only. Does it differ from the median on all loans?', f'Training median UGX {n0(F["inc_med_train"])} against {n0(F["inc_med"])} on all loans: a tiny difference, which is why the leak is small. The safe order still splits first.']])
    return sess
