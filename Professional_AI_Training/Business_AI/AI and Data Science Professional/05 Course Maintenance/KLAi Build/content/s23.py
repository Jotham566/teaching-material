"""Session 23: Ship it (reproducible work, a small app and responsible use). Python lab (content/labs/s23_nb.py).

Every number on a slide, in a note, in the notebook checks or in the facilitator answer key is computed in facts() with pandas and numpy from the real
Nile Microfinance file (loans.csv). scikit-learn, joblib and Streamlit are not installed where this was built, so the model numbers come from an independent
numpy Newton fit of the same L2 logistic objective that scikit-learn minimises (the notebook checks use a tolerance for the solver difference).
"""
import importlib.metadata as md
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import loans_canon as LC  # noqa: E402  (the shared split: stratified 6,000 / 2,000, the same rows as Sessions 14 to 17)
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
FEATURES = ['monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_late_payments']
THRESHOLD = 0.15
RULE_A_CUT = 0.40      # instalment_to_income above 0.40 (about 35 percent of income before the illustrative 15 percent charge)
RULE_B_CUT = 0.12      # occupation default rate (from the training loans) above 12 percent

APP_LINES = ["import joblib", "import pandas as pd", "import streamlit as st", "", "model = joblib.load('loan_model.joblib')", "",
             "st.title('Loan risk checker')", "st.caption('A person decides.')", "",
             "income = st.number_input('Income (UGX)',", "                         value=600000)", "amount = st.number_input('Loan (UGX)',",
             "                         value=1500000)", "months = st.slider('Months', 3, 12, 6)", "late = st.slider('Late payments', 0, 6, 0)", "",
             "row = pd.DataFrame({", "  'monthly_income_ugx': [income],", "  'loan_amount_ugx': [amount],", "  'term_months': [months],",
             "  'previous_late_payments': [late]})", "", "if st.button('Show probability'):", "  p = model.predict_proba(row)[0, 1]",
             "  st.metric('Default chance', f'{p:.0%}')"]
APP_CODE = '\n'.join(APP_LINES) + '\n'


def n(x):
    return f'{int(x):,}'


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def logreg_fit(Z, y, C=1.0, iters=100):
    """Newton's method on scikit-learn's L2 logistic objective: 0.5*||w||^2 + C*sum(log loss); the intercept is not penalised."""
    A = np.column_stack([np.ones(len(Z)), Z])
    th = np.zeros(A.shape[1])
    pen = np.eye(A.shape[1])
    pen[0, 0] = 0
    for _ in range(iters):
        p = sigmoid(A @ th)
        g = pen @ th + C * A.T @ (p - y)
        H = pen + C * (A.T * (p * (1 - p))) @ A
        step = np.linalg.solve(H, g)
        th -= step
        if np.max(np.abs(step)) < 1e-12:
            break
    return th


def auc(y, s):
    r = pd.Series(s).rank().values
    n1 = int(y.sum())
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def ver(name):
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return None


def group_rates(df, flag, col='gender'):
    """Approval rate (share not flagged), false negative rate (defaults not flagged) and false positive rate (repaid loans flagged), by group."""
    out = {}
    for g, d in df.groupby(col):
        f = d[flag] if isinstance(flag, str) else flag[d.index]
        dflt = d.default == 1
        out[g] = dict(n=len(d), default_rate=float(dflt.mean()), flag_rate=float(f.mean()), approval=float(1 - f.mean()),
                      fnr=float(((f == 0) & dflt).sum() / dflt.sum()), fpr=float(((f == 1) & ~dflt).sum() / (~dflt).sum()))
    return out


@lru_cache(maxsize=None)
def facts():
    raw = pd.read_csv(DATA / 'loans.csv')
    loans = raw.copy()
    loans['district'] = loans.district.str.strip().str.title()
    F = dict(rows=len(loans), defaults=int(loans.default.sum()), default_rate=float(loans.default.mean()), missing_income=int(loans.monthly_income_ugx.isna().sum()),
             date_min=str(pd.to_datetime(loans.disbursed_date).min().date()), date_max=str(pd.to_datetime(loans.disbursed_date).max().date()))
    # ---- reproducibility: seeds and versions
    F['seed42'] = loans.sample(5, random_state=42).index.tolist()
    F['seed42b'] = loans.sample(5, random_state=42).index.tolist()
    F['seed43'] = loans.sample(5, random_state=43).index.tolist()
    assert F['seed42'] == F['seed42b'] and F['seed42'] != F['seed43']
    F['versions'] = {k: ver(k) for k in ('numpy', 'pandas', 'matplotlib')}
    # ---- default rates by group (after tidying district)
    F['by_gender'] = {k: float(v) for k, v in loans.groupby('gender').default.mean().items()}
    F['by_district'] = {k: float(v) for k, v in loans.groupby('district').default.mean().items()}
    F['n_districts'] = int(loans.district.nunique())
    F['n_district_spellings'] = int(raw.district.nunique())
    F['top_district'] = max(F['by_district'], key=F['by_district'].get)
    F['low_district'] = min(F['by_district'], key=F['by_district'].get)
    # ---- the canonical split (stratified, seed 42): rules and model are judged on the 2,000 TEST loans; anything learned (occupation default rates, the model) comes from the 6,000 training loans
    loans['income_missing'] = loans.monthly_income_ugx.isna().astype(int)
    loans['instalment_to_income'] = loans.loan_amount_ugx * LC.TOTAL_REPAYMENT_FACTOR / loans.term_months / loans.monthly_income_ugx   # blank income stays blank
    y = loans.default.values.astype(float)
    tr, te = LC.split_indices(y)
    F['n_train'], F['n_test'] = len(tr), len(te)
    F['train_defaults'], F['test_defaults'] = int(y[tr].sum()), int(y[te].sum())
    F['test_index_sum'] = int(te.sum())
    trn, tst = loans.iloc[tr], loans.iloc[te]
    # ---- rule A: instalment_to_income above 0.40, test loans that have an income
    known = tst.dropna(subset=['monthly_income_ugx']).copy()
    F['known'] = len(known)
    known['flag'] = (known.instalment_to_income > RULE_A_CUT).astype(int)
    F['ruleA'] = group_rates(known, 'flag')
    # ---- rule B: occupation default rate over 12 percent, rates learned on the training loans
    occ_tr = trn.groupby('occupation').default.mean()
    known['flag2'] = (known.occupation.map(occ_tr) > RULE_B_CUT).astype(int)
    F['ruleB'] = group_rates(known, 'flag2')
    F['occ_rate'] = {k: float(v) for k, v in occ_tr.items()}
    F['occ_flagged'] = sorted(k for k, v in F['occ_rate'].items() if v > RULE_B_CUT)
    ka = loans.dropna(subset=['monthly_income_ugx'])   # all loans with an income (descriptive, not a test)
    F['known_all'] = len(ka)
    fem = (ka.gender == 'F').groupby(ka.occupation).mean().sort_values(ascending=False)
    F['female_share'] = {k: float(v) for k, v in fem.items()}
    F['occ_n'] = {k: int(v) for k, v in ka.occupation.value_counts().items()}
    # ---- the model (simplified, four variables): median imputation and scaling learned on the TRAINING loans, L2 logistic regression (numpy, same objective as scikit-learn)
    Xall = loans[FEATURES].astype(float).values
    med = np.nanmedian(Xall[tr], axis=0)
    Xall = np.where(np.isnan(Xall), med, Xall)
    mu, sd = Xall[tr].mean(0), Xall[tr].std(0)
    Z = (Xall - mu) / sd
    th = logreg_fit(Z[tr], y[tr])
    pall = sigmoid(th[0] + Z @ th[1:])
    F['p_first'] = float(pall[0])
    F['auc_train'] = auc(y[tr], pall[tr])
    ptest = pall[te]
    F['auc_test'] = auc(y[te], ptest)
    flag_te = ptest >= THRESHOLD
    tst = tst.assign(flag_m=flag_te.astype(int))
    F['model'] = group_rates(tst, 'flag_m')
    F['model_flag_rate'] = float(flag_te.mean())
    F['card'] = dict(n_test=len(te), defaults_test=F['test_defaults'], auc=F['auc_test'], flag_rate=float(flag_te.mean()), recall=float((flag_te & (y[te] == 1)).sum() / y[te].sum()),
                     flagged=int(flag_te.sum()), caught=int((flag_te & (y[te] == 1)).sum()))
    F['coef'] = dict(zip(FEATURES, (float(c) for c in th[1:])))
    x_app = (np.array([600000, 1500000, 6, 0], float) - mu) / sd
    F['p_app'] = float(sigmoid(th[0] + x_app @ th[1:]))
    # ---- drift: monthly mean income of new loans (UGX thousand)
    kn_all = loans.dropna(subset=['monthly_income_ugx'])
    d = kn_all.assign(month=pd.to_datetime(kn_all.disbursed_date).dt.to_period('M'))
    m = d.groupby('month').monthly_income_ugx.mean() / 1000
    F['months'] = [str(k) for k in m.index]
    F['month_labels'] = [pd.Period(k).strftime('%b %Y') for k in F['months']]
    F['month_mean'] = [float(v) for v in m.values]
    F['train_n'] = 24
    F['train_mean'] = float(np.mean(F['month_mean'][:24]))
    F['later_mean'] = float(np.mean(F['month_mean'][24:]))
    F['shifted'] = [v if i < 24 else v * 0.85 for i, v in enumerate(F['month_mean'])]
    F['shifted_mean'] = float(np.mean(F['shifted'][24:]))
    F['month_min'], F['month_max'] = float(min(F['month_mean'])), float(max(F['month_mean']))
    # ---- bridge slide output, run here
    ap = 1 - known.groupby('gender').flag.mean()
    F['bridge_out'] = f"{ {k: round(float(v), 3) for k, v in ap.items()} }\n{round(float(ap.min() / ap.max()), 3)}"
    return F


def di(rates):
    a = [v['approval'] for v in rates.values()]
    return min(a) / max(a)


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


def build():
    F = facts()
    A, Bq, M = F['ruleA'], F['ruleB'], F['model']
    dA, dB, dM = di(A), di(Bq), di(M)
    C = F['card']
    fs = F['female_share']
    V = F['versions']
    ver_lines = [f'numpy=={V["numpy"]}', f'pandas=={V["pandas"]}', f'matplotlib=={V["matplotlib"]}', 'scikit-learn==...', 'joblib==...', 'streamlit==...']
    assert A['F']['approval'] > A['M']['approval'] and Bq['F']['approval'] > Bq['M']['approval'] and Bq['F']['fnr'] > Bq['M']['fnr']
    assert F['occ_flagged'] == ['Boda rider', 'Farmer', 'Mechanic'] and dB < 0.8 < dA and 0.8 < dM
    sess = dict(
        num=23, block='Module F: Ship it and present', short_title='Ship it',
        title='Ship it: reproducible work, a small app and responsible use',
        question='How do we turn a notebook into something a colleague can repeat, use and trust?',
        outcomes=['Make a notebook reproducible, save a model to a file and publish code and a small app for free',
                  'Write a model card and watch for data drift and concept drift',
                  'Run a fairness audit by group, spot a proxy variable, and name the main duties in the Uganda Data Protection and Privacy Act, 2019'],
        outcome_icons=['folder', 'shield', 'key'],
        outcome_note=('Here is what you can do by the end of today. You can make a notebook reproducible, which means a colleague gets your result, and you can save a trained model to a file and publish code and a small app for free. '
                      'You can write a model card, and you can watch for data drift and concept drift. And you can run a fairness audit by group, spot a proxy variable, and name the main duties in the Uganda Data Protection and Privacy Act of 2019. '
                      'The lab uses the Nile Microfinance loans, and it ends with a folder you can keep and show.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a notebook lab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 22 and set the question for today. Then forty-five minutes of concepts with no laptops open: how to make work repeatable, how to save and share it, and how to check it is fair and lawful. '
                   'After a ten minute break we open one Colab notebook for a forty-five minute lab on the Nile Microfinance loans. The last ten minutes are an exit check and what you keep. Please protect the lab time, because the fairness checks only make sense when you run them.'),
        recall_from='Session 22',
        recall=[('A language model states a fact that is in none of your documents. What is that called, and what did we add to reduce it?', 'A hallucination: fluent text that is invented. Retrieval-augmented generation (RAG) finds passages in your own documents first and answers from them.'),
                ('Why do we keep an evaluation set of test questions for a document assistant?', 'So we can run the same questions after every change and see whether the answers got better or worse.'),
                ('What is a chunk?', 'A piece of a document, such as one paragraph of a policy, that is stored and searched on its own.')],
        words=[('Reproducibility', 'A colleague who runs your notebook gets your result. It needs a fixed random seed, recorded library versions and a run from the top.'),
               ('Model serialisation (persistence)', 'Saving a trained model to a file, for example with joblib or pickle, so it can be loaded later without training again.'),
               ('Data drift (and concept drift)', 'Data drift: the inputs change after training. Concept drift: the link between the inputs and the outcome changes.'),
               ('Fairness audit (proxy variable, disparate impact)', 'Compare approval and error rates across groups. A proxy variable stands in for a column you left out. Disparate impact is the ratio of two approval rates.'),
               ('Personal data (data subject, data controller)', 'Information that identifies a person. The person is the data subject. The organisation that decides how it is used is the data controller.')],
        word_icons=['check', 'folder', 'chart', 'people', 'lock'],
        words_note=('Five words for today. Reproducibility means a colleague gets your result from your notebook. Model serialisation means saving a trained model to a file. '
                    'Data drift is a change in the inputs after training, and concept drift is a change in the relationship between inputs and outcome. A fairness audit compares approval and error rates across groups, and a proxy variable is a column that stands in for one you removed. '
                    'And personal data is information that identifies a person, the data subject, held by a data controller. We use every one of them today.'),
        keep='Keep your shipping folder: the notebook, requirements.txt, loan_model.joblib, app.py and a completed model card with a fairness audit and a data protection checklist.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab folder', value='Ready to push'), dict(label='The audit', value='Rates by group'), dict(label='Next session', value='Present it')]),
        keep_title='Save your shipping folder and push it to your own GitHub',
        next='Session 24: Present your course project and plan your path from here. You tell a result as an answer, evidence and limits, and plan what to learn next.', next_label='Next session',
        keep_note=('Before you go, save the folder you built today. It holds the notebook, the requirements file, the saved model, the app file and a model card with the fairness audit. '
                   'If you can hand it to a colleague and they can repeat your result without asking you anything, it is good. Create a free GitHub account if you do not have one, and push the folder to a public repository after checking that no personal data is inside. '
                   'Next session you present your course project, so bring your question and your result.'),
        cover_note=('Welcome back. For twenty-two sessions your work has lived in a notebook that only you could run. Today it leaves the notebook. '
                    'You will make it repeatable, save the model, put the code on GitHub, and see how a small app is built. Then comes the part that decides whether anyone should use it: a model card, a watch for drift, a fairness audit by group and the duties under Uganda law.'),
        use_at_work='Make a model repeatable, shareable and checkable for fairness and data protection before anyone relies on it.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 22', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['cloud', 'check', 'doc'],
                  notes=('Here are the answers to the three warm-up questions. A fact that appears in none of your documents is a hallucination: fluent text that is invented. Retrieval-augmented generation, or RAG, reduces it by finding passages in your own documents first. '
                         'An evaluation set is a list of test questions with checked answers, so you can run it again after every change. And a chunk is a piece of a document that is stored and searched on its own. '
                         'Today is about the same habit of repeating and checking, applied to everything you ship. Which of the three was hardest?')))

    # 2 five jobs
    S.append(dict(kind='steps', title='Shipping a model means five jobs after the notebook works',
                  steps=[dict(head='1 Repeat', text='Seed, versions, run from the top', icon='check'), dict(head='2 Save', text='The model as a file', icon='folder'), dict(head='3 Share', text='Git and GitHub', icon='cloud'),
                         dict(head='4 Serve', text='A small Streamlit app', icon='laptop'), dict(head='5 Govern', text='Model card, drift, fairness, the law', icon='shield')], highlight=None,
                  caption='Today covers all five. The lab does 1 and 2, writes the files for 4, and does 5. You do 3 and the deployment with your own free accounts.',
                  notes=('A notebook that works for you is only the start. Five jobs follow. First, make it repeatable with a seed, recorded library versions and a clean run from the top. Second, save the trained model as a file. '
                         'Third, share the code with Git and GitHub. Fourth, serve the model through a small web app built with Streamlit. And fifth, govern it: write a model card, watch for drift, audit it for fairness by group and check your duties under the law. '
                         'The first four are craft. The fifth decides whether anyone should trust the other four. Which job do you skip most often today?')))

    # 3 seed
    S.append(dict(kind='idea', title='A random seed makes a random draw repeatable',
                  visual=dict(kind='dl_runs', head='Five loans drawn at random from 8,000', foot='Each box is the row number of one loan in loans.csv.',
                              rows=[dict(label='seed 42, run 1', values=F['seed42'], tone='gold'), dict(label='seed 42, run 2', values=F['seed42b'], tone='gold', tag='identical', gap_after=0.2),
                                    dict(label='seed 43, run 1', values=F['seed43'], tag='different'), dict(label='seed 43, run 2', values=F['seed43'])]),
                  lead='Seed (random_state): a starting number for the random generator. The same seed gives the same draw.',
                  points=['In pandas: random_state=42.', 'In Sheets, paste RAND as values.', 'Use one seed for every random split.'],
                  notes=('Many steps in data science use chance: drawing a sample, splitting training and test sets, starting a model. If chance changes every run, nobody can repeat your result. '
                         'A random seed fixes it. It is a starting number for the random generator. Look at the picture. Drawing five loans with seed forty-two gives the same five row numbers twice. Seed forty-three gives a different draw, but again the same twice. '
                         'In a spreadsheet the same problem exists with RAND, which changes every time the sheet recalculates, and you freeze it by pasting the values. Which random steps have you used so far in this course?')))

    # 4 requirements
    S.append(dict(kind='idea', title='A requirements file records which library versions your notebook used',
                  visual=dict(kind='dl_file', name='requirements.txt', lines=ver_lines, gold=[0], notes=[(0, 'One library and its version per line'), (3, 'Fill in the versions your notebook printed')]),
                  lead='Requirements file (requirements.txt): a text file that lists each library and its version.',
                  points=['The versions shown come from one machine. Print your own: numpy.__version__, or pip freeze.', 'Keep only libraries you import.', 'Install with pip install -r requirements.txt.'],
                  notes=(f'Libraries change over time, and a notebook that works with one version can fail or give different numbers with another. So you record the versions. In Python every library prints its version, for example numpy is {V["numpy"]} and pandas is {V["pandas"]} on the machine that built this slide. '
                         'Your own versions will differ, and that is fine. You list the libraries you import in a plain text file called requirements dot txt, one per line, with the version after two equals signs. '
                         'A colleague, or a deployment service, installs exactly those. Which libraries would your course project notebook need?')))

    # 5 run all
    S.append(dict(kind='compare', title='Restart and run all is the test of a notebook',
                  left=dict(head='Works only for you', points=['You ran cells in a different order.', 'Your open session remembers a deleted cell.', 'A colleague meets a NameError.']),
                  right=dict(head='Works for anyone', points=['Runtime, then Restart session and run all.', 'Fix the first error and run again.', 'Share when it runs top to bottom.']),
                  verdict='Run it from the top before you share it.',
                  notes=('The third habit is the order. While you work you run cells in any order, and your open session remembers every name you ever created, even from a cell you deleted. '
                         'Your colleague opens the notebook with an empty session and runs it from the top. If a cell depends on something that is no longer there, they meet an error that says a name is not defined. '
                         'The test is simple. In Colab choose Runtime, then Restart session and run all. Fix the first error, then run again. Only share a notebook that runs from top to bottom by itself. Has this ever happened to you?')))

    # 6 serialisation
    S.append(dict(kind='idea', title='Model serialisation saves a trained model to a file you can load later',
                  visual=dict(kind='flow', steps=[dict(head='Train', text='model.fit(X, y)', icon='gear'), dict(head='Save', text='joblib.dump writes the file', icon='folder'), dict(head='Load', text='joblib.load reads it, then predict', icon='laptop')]),
                  lead='Model serialisation (persistence): saving a trained model to a file.',
                  points=['Tools: joblib or pickle. joblib uses pickle underneath.', 'Load only files you trust: loading can run hidden code.', 'Use the same library versions.'],
                  notes=('Training a model takes effort, so you save the result. Model serialisation, also called persistence, writes the trained model to a file. In Python the common tool for scikit-learn models is joblib, and the standard Python tool is pickle. Joblib uses pickle underneath, so it carries the same risk. '
                         'The picture shows three steps: train, save with dump, and load with load, then predict. Two warnings. My understanding from the library documentation is that loading a file can run code that is inside it, so never load a model file from a stranger. '
                         'And save and load with the same library versions, or you may get warnings or wrong results. Where would you store a model file at work?')))

    # 7 git picture
    S.append(dict(kind='wide', title='Git keeps a history of your project, and GitHub keeps a copy online',
                  visual=dict(kind='dl_git', places=[('Working folder', 'Your notebook, app.py and data files as you edit them'), ('Staging area', 'The files you chose for the next saved version'), ('Local repository', 'The history: every commit with its message'),
                                                      ('GitHub', 'A copy online: the remote repository')], commands=['git add', 'git commit', 'git push']),
                  caption='Git is the tool on your laptop. GitHub hosts a copy online.',
                  notes=('Git is a tool that keeps the history of a project folder. The folder you edit is the working folder. With git add you choose which changed files go into the next saved version. '
                         'With git commit you save that version in your local repository, together with a short message saying what changed. And with git push you upload your commits to GitHub, a website that hosts a copy so colleagues can see it. '
                         'In Google Drive you have version history. Git is the same idea, but you choose when to save a version and you name it. What would your commit messages say?')))

    # 8 git words
    S.append(dict(kind='table', title='Six words you will hear about Git and GitHub', headers=['Word', 'Plain meaning', 'You will see'],
                  rows=[['Repository (repo)', 'The project folder together with its full history.', 'github.com/you/loan-model'], ['Commit', 'One saved version, with a message saying what changed.', 'git commit -m "first version"'],
                        ['Branch', 'A separate line of work. The main line is called main.', 'main'], ['Push', 'Upload your commits to GitHub.', 'git push -u origin main'],
                        ['README', 'The front page of a repository: what the project is and how to run it.', 'README.md'], ['.gitignore', 'A list of files Git must never track, such as data with personal details or passwords.', '.gitignore']],
                  widths=[2.4, 6.0, 3.6], icons=['folder', 'check', 'pin', 'cloud', 'doc', 'lock'],
                  notes=('Six words you will meet the first day you use GitHub. A repository, or repo, is the project folder together with its history. A commit is one saved version with a message. A branch is a separate line of work, and the main line is called main. '
                         'Push means uploading your commits to GitHub. A README is the front page of the repository: what the project is and how to run it. And a dot gitignore file lists files Git must never track, such as data with personal details or passwords. '
                         'Which of these would you create first?')))

    # 9 public repo
    S.append(dict(kind='compare', title='A public repository is public: personal data, passwords and keys never go in',
                  left=dict(head='Put in', points=['The notebook, run from the top.', 'app.py and requirements.txt.', 'A README and the model card.', 'Generated or public data.']),
                  right=dict(head='Never put in', points=['Names, phones or loan records of real people.', 'Passwords, keys and tokens.', 'Data your employer has not cleared.']),
                  verdict='Deleting a file later does not erase its history. Check before you push.',
                  notes=('Anyone on the internet can read a public repository and copy it. So decide what goes in before the first push. The notebook, the app file, the requirements file, a README and the model card all belong. '
                         'Data should be generated or public. Never put in personal data such as names, phone numbers or the loan records of real people, and never passwords, keys or tokens, and never data your employer has not agreed to share. '
                         'Remember that Git keeps history, so deleting a file in a later commit does not remove it from the earlier ones. A private repository exists, but check the current terms. What would you check in your own folder?')))

    # 10 app picture
    S.append(dict(kind='idea', title='A Streamlit app turns a saved model into a web page',
                  visual=dict(kind='dl_app', url='your-app-name.streamlit.app', title='Loan risk checker', caption='A person decides.',
                              inputs=[('Income (UGX)', '600,000', 'number'), ('Loan (UGX)', '1,500,000', 'number'), ('Months', '6', 'slider', 0.33), ('Late payments', '0', 'slider', 0.0)], button='Show probability',
                              result_label='Default chance', result_value=f'{F["p_app"] * 100:.0f}%'),
                  lead='Streamlit: a free Python library that builds a web page from a script.',
                  points=['You write inputs and output. Streamlit draws the page.', f'These inputs give {F["p_app"] * 100:.0f}% chance of default.', 'A person makes the decision.'],
                  notes=(f'Here is what a small app looks like. A person types an income and a loan amount, moves two sliders, and presses a button. The page shows the predicted chance of default, which is {F["p_app"] * 100:.0f} percent for these inputs, computed from the same model you will save in the lab. '
                         'Streamlit is a free Python library that builds this page from a script. You describe the inputs and the output, and it does the web work. Notice the caption: this is a teaching model on fictional data, and a person decides. '
                         'Who at your workplace would use an app like this?')))

    # 11 app code
    S.append(dict(kind='wide', title=f'The whole app is about {len(APP_LINES)} lines: load the model, ask for four inputs, predict',
                  visual=dict(kind='dl_code2', lines=APP_LINES, per_col=13, gold=[5, 24]),
                  caption='Gold lines: load the model (line 5) and predict (line 24).',
                  notes=('This is the whole app. Lines one to three import the libraries. Line five loads the saved model. Lines seven and eight give the page a title and a caption. '
                         'Lines ten to fifteen create four inputs: two number boxes and two sliders. Lines seventeen to twenty-one put the four values into a one-row table with the same column names the model was trained on. '
                         'Then lines twenty-three to twenty-five add a button which, when pressed, calls predict probability and shows the result. Streamlit runs the script again from the top whenever someone changes an input. '
                         'Which line would you change first to show a different title?')))

    # 12 deploy
    S.append(dict(kind='steps', title='Streamlit Community Cloud can deploy your app from a GitHub repository',
                  steps=[dict(head='Repository', text='app.py, the model file, requirements.txt', icon='folder'), dict(head='Sign in', text='With your GitHub account', icon='key'), dict(head='New app', text='Pick repository, branch main, file app.py', icon='pin'),
                         dict(head='Deploy', text='It installs the libraries and gives a web address', icon='cloud'), dict(head='Maintain', text='Free apps may sleep when unused', icon='clock')], highlight=3,
                  caption='Deploy: put the app on a server. Free at the time of writing, with limits on resources and sleeping apps. Check current terms, including private repositories.',
                  notes=('To deploy means to put the app on a server so that other people can open it with a web address. Streamlit Community Cloud can do this for free from a GitHub repository. '
                         'You need a repository with app dot py, the model file and requirements dot txt. You sign in with your GitHub account, create a new app, choose the repository, the branch main and the file, and press deploy. It installs the libraries and gives you an address. '
                         'At the time of writing it is free for public repositories and apps may go to sleep when nobody uses them, with reports of about twelve hours. Limits change, so check the current terms. It suits learning and demonstrations. A business-critical service needs something stronger. What would you use it for?')))

    # 13 model card
    S.append(dict(kind='table', title='A model card is a one-page note on what a model is for and where it can fail',
                  headers=['Section', 'The loan model (an illustrative card)'],
                  rows=[['Purpose', 'Ranks loan applications so an officer knows which to review first. It does not approve or refuse.'],
                        ['Data', f'{n(F["rows"])} fictional loans, {F["date_min"][:7]} to {F["date_max"][:7]}. collection_calls was removed because it leaks the answer.'],
                        ['Metrics', f'Simplified four-variable model. AUC {C["auc"]:.3f} on {n(C["n_test"])} held-out loans. At decision threshold {THRESHOLD} it flags {C["flag_rate"] * 100:.0f}% of loans and finds {C["recall"] * 100:.0f}% of defaults.'],
                        ['Limits', f'Fictional data. {F["missing_income"]} loans lack income and are filled with the median. Four variables only. Not tested after the data changes.'],
                        ['Fairness and review', f'On the held-out loans, approval women {pct(M["F"]["approval"])}%, men {pct(M["M"]["approval"])}%. Reviewed by the credit manager and the data protection officer.']],
                  widths=[2.6, 9.4], icons=['doc', 'folder', 'chart', 'cross', 'shield'], note='Update the card every time the model changes.',
                  notes=(f'A model card is a short note, usually one page, that travels with a model. It says what the model is for, what data it learned from, how well it works, where it can fail, and who reviews it. '
                         f'This card is for the loan model you will build. The purpose is to rank applications for an officer. It makes no decision. The data is {n(F["rows"])} fictional loans, with the leaking column removed. '
                         f'This is a simplified model with four variables, fitted on the six thousand training loans. On the {n(C["n_test"])} held-out loans it has never seen, the area under the curve is {C["auc"]:.3f}, and at a decision threshold of {THRESHOLD} it flags {C["flag_rate"] * 100:.0f} percent of loans and finds {C["recall"] * 100:.0f} percent of defaults. '
                         'The limits and the fairness check complete it. Which section would your manager read first?')))

    # 14 drift picture
    S.append(dict(kind='wide', title='Data drift: when new data stops looking like the training data, the model gets worse',
                  visual=dict(kind='dl_drift', labels=F['month_labels'], real=F['month_mean'], shifted=F['shifted'], train_n=24, ymin=500, ymax=800, ytick=100,
                              ylabel='Mean monthly income of new loans (UGX thousand)', real_label='Real: Nile Microfinance loans', shift_label='Hypothetical: incomes 15 percent lower', train_label='Training period', alert='Check here'),
                  caption='Solid: real. Dashed: a hypothetical 15 percent fall from month 25.',
                  notes=(f'Data drift means the inputs change after the model was trained. The solid line is real: the mean monthly income of new loans in each month. For the first twenty-four months, the training period, it averages {F["train_mean"]:.0f} thousand shillings, '
                         f'and in the next nine months {F["later_mean"]:.0f}. So our real data shows no drift. The dashed line is hypothetical: the same months, but with incomes fifteen percent lower, which would average {F["shifted_mean"]:.0f}. '
                         'A model trained on the old picture would now see borrowers it has never met. You catch it by comparing each month of new inputs with the training period. What other input could drift in your data?')))

    # 15 concept drift
    S.append(dict(kind='compare', title='Data drift and concept drift are different problems',
                  left=dict(head='Data drift', points=['The inputs change: incomes or loan sizes move.', 'Check: compare each month of inputs with the training period.']),
                  right=dict(head='Concept drift', points=['The link between inputs and outcome changes. Illustration: a new repayment option changes the risk.', 'Check: compare predicted with actual defaults.']),
                  verdict='Plan monitoring, set a review date, retrain when needed.',
                  notes=('There are two kinds of drift. In data drift the inputs change, so new borrowers look different from the ones the model learned from. You catch it by comparing summaries of each month of inputs with the training period. '
                         'In concept drift the relationship between inputs and outcome changes. As an illustration, suppose a new repayment option changes how borrowers with a given income behave. The inputs look the same but the risk has moved. '
                         'You catch that only when real outcomes arrive, by comparing predicted with actual defaults. In both cases the answer is a monitoring plan, a review date and retraining on newer data. When would your outcomes arrive?')))

    # 16 proxy
    S.append(dict(kind='idea', title='A proxy variable carries the information of a column you removed',
                  visual=dict(kind='dl_groupbars', groups=[(k, [v * 100]) for k, v in fs.items()], series=['Women'], ref=50, ref_label='50%'),
                  lead='Proxy variable: a variable that stands in for another. Occupation stands in for gender.',
                  points=[f'Women are {fs["Tailor"] * 100:.0f}% of tailors and {fs["Salon owner"] * 100:.0f}% of salon owners.', 'Dropping the gender column keeps the information.', 'Occupation rules can treat men and women differently.'],
                  notes=(f'Suppose you remove the gender column so the model cannot use it. Fairness is not solved, because other columns can stand in for it. A variable that stands in for another is a proxy variable. '
                         f'The bars show the share of women among {n(F["known_all"])} loans with a known income, by occupation. Women are {fs["Tailor"] * 100:.0f} percent of tailors and {fs["Salon owner"] * 100:.0f} percent of salon owners, and under half of farmers. '
                         'So a rule that treats occupations differently will treat men and women differently, even though it never sees gender. Which column in your own data might be a proxy?')))

    # 17 formula
    S.append(dict(kind='formula', title='Disparate impact: divide the lower approval rate by the higher one',
                  formulas=[('Approval rate', r'$\mathrm{approval\ rate} = \mathrm{loans\ not\ flagged} \div \mathrm{loans\ in\ the\ group}$'), ('Disparate impact ratio', r'$\mathrm{DI} = \frac{\mathrm{lower\ approval\ rate}}{\mathrm{higher\ approval\ rate}}$'),
                            ('Occupation rule, women and men', rf'$\mathrm{{DI}} = {Bq["M"]["approval"]:.3f} \div {Bq["F"]["approval"]:.3f} = {dB:.3f}$')],
                  symbols=[['Approval rate', 'Share of a group not flagged as high risk.', f'women {pct(Bq["F"]["approval"])}%, men {pct(Bq["M"]["approval"])}%'],
                           ['DI', 'Disparate impact ratio. 1.00 means equal rates.', f'{dB:.3f} for the occupation rule'],
                           ['0.8 rule of thumb', 'Below 0.8 is a warning. It comes from US employment practice and is no Ugandan legal test.', f'{dB:.3f} is below 0.8']],
                  size=22, note='A screening number: it starts a question.', widths=[2.2, 6.0, 3.7],
                  notes=(f'Here is how to measure unequal treatment. The approval rate of a group is the share of its loans that are not flagged as high risk. Disparate impact compares two groups: divide the lower approval rate by the higher one. A ratio of one means equal rates. '
                         f'For the occupation rule, men are approved {pct(Bq["M"]["approval"])} percent of the time and women {pct(Bq["F"]["approval"])} percent, so the ratio is {dB:.3f}. '
                         'A common rule of thumb, used in United States employment practice, treats a ratio below zero point eight as a warning. It is not a Ugandan legal test and it is only a prompt to investigate. What would you ask next?')))

    # 18 three rules chart
    S.append(dict(kind='idea', title='A fairness audit compares approval rates by group, and one rule raises a flag',
                  visual=dict(kind='dl_groupbars', groups=[(f'Instalment rule (DI {dA:.3f})', [A['F']['approval'] * 100, A['M']['approval'] * 100]), (f'Occupation rule (DI {dB:.3f})', [Bq['F']['approval'] * 100, Bq['M']['approval'] * 100]),
                                                          (f'Model at {THRESHOLD} (DI {dM:.3f})', [M['F']['approval'] * 100, M['M']['approval'] * 100])], series=['Women', 'Men'], lab_w=2.6),
                  lead='Fairness audit: compare approval and error rates across groups.',
                  points=['Approval rate: share of loans not flagged.', 'The occupation rule favours women.', 'The other two treat groups alike.'],
                  notes=(f'Now the fairness audit. We take three ways to flag a loan as high risk and compute the approval rate for women and men. These are the 2,000 held-out loans that have an income. Rule one flags an instalment-to-income ratio above zero point four, which is about thirty-five percent of income before the illustrative fifteen percent charge: women {pct(A["F"]["approval"])} percent, men {pct(A["M"]["approval"])}. '
                         f'Rule two flags occupations whose default rate on the training loans is above twelve percent: women {pct(Bq["F"]["approval"])}, men {pct(Bq["M"]["approval"])}, a ratio of {dB:.3f}. '
                         f'The model at a threshold of {THRESHOLD} gives {pct(M["F"]["approval"])} and {pct(M["M"]["approval"])}. None of them uses gender, yet one raises a flag. That is the point of auditing the output rather than trusting the inputs. Which group would you check first at work?')))

    # 19 error rates
    S.append(dict(kind='table', title='Error rates differ too: the occupation rule misses more defaults among women',
                  headers=['Rule and group', 'Approval rate', 'Defaults missed (false negative rate)', 'Repaid loans flagged (false positive rate)'],
                  rows=[['Instalment rule, women', f'{pct(A["F"]["approval"])}%', f'{pct(A["F"]["fnr"])}%', f'{pct(A["F"]["fpr"])}%'], ['Instalment rule, men', f'{pct(A["M"]["approval"])}%', f'{pct(A["M"]["fnr"])}%', f'{pct(A["M"]["fpr"])}%'],
                        ['Occupation rule, women', f'{pct(Bq["F"]["approval"])}%', f'{pct(Bq["F"]["fnr"])}%', f'{pct(Bq["F"]["fpr"])}%'], ['Occupation rule, men', f'{pct(Bq["M"]["approval"])}%', f'{pct(Bq["M"]["fnr"])}%', f'{pct(Bq["M"]["fpr"])}%']],
                  widths=[3.4, 2.0, 3.5, 3.5], icons=['person', 'person', 'person', 'person'], hl_col=2,
                  note='False negative rate: share of actual defaults the rule did not flag. False positive rate: share of repaid loans it flagged.',
                  notes=(f'Approval rates are one side. Error rates are the other. A false negative is a default the rule did not flag. A false positive is a repaid loan the rule flagged. The instalment rule makes errors of a similar size for women and men. '
                         f'The occupation rule does not. It misses {pct(Bq["F"]["fnr"])} percent of defaults among women and {pct(Bq["M"]["fnr"])} percent among men, and it flags {pct(Bq["M"]["fpr"])} percent of repaid loans among men against {pct(Bq["F"]["fpr"])} percent among women. '
                         'So women who will default are missed more often, and men who will repay are flagged more often. Both are harms, to the lender and to the borrower. Which error costs more at your workplace?')))

    # 20 DPPA who
    S.append(dict(kind='table', title="Uganda's Data Protection and Privacy Act, 2019: the key roles (a teaching summary)", headers=['Term', 'Plain meaning', 'In a loan file'],
                  rows=[['Personal data', 'Information from which a person can be identified.', 'Name, phone number, loan record'], ['Data subject', 'The person the data is about.', 'The borrower'],
                        ['Data controller', 'The organisation that decides why and how personal data is used.', 'The lender'], ['Data processor', 'Someone who handles data for the controller.', 'A cloud or software provider'],
                        ['Regulator', 'My understanding: the Personal Data Protection Office, under NITA-U.', 'Where complaints go']],
                  widths=[2.6, 5.6, 3.8], icons=['doc', 'person', 'shop', 'gear', 'flag'], note='Hedged summary from public descriptions. Not legal advice. Read the Act, or ask your data protection officer or a lawyer.',
                  notes=('Now the law. This is a teaching summary in plain words from public descriptions of the Act, and it is not legal advice. Personal data is information from which a person can be identified, such as a name, a phone number or a loan record. '
                         'The person it describes is the data subject, here the borrower. The organisation that decides why and how the data is used is the data controller, here the lender. A data processor handles data on the controller behalf, for example a cloud provider. '
                         'My understanding is that the regulator is the Personal Data Protection Office under NITA-U. For your own case, ask your data protection officer or a lawyer. Who is the data controller where you work?')))

    # 21 principles
    S.append(dict(kind='table', title='Public summaries of the Act describe seven principles: collect less, say why, keep it safe', headers=['Principle', 'In plain words'],
                  rows=[['Accountability', 'Someone is responsible and can show what was done.'], ['Fair and lawful processing', 'Use data fairly and within the law.'], ['Adequate and relevant data', 'Collect only what the purpose needs.'],
                        ['Kept only as long as needed', 'Delete data when the purpose ends.'], ['Quality of information', 'Keep data accurate and up to date.'], ['Openness and participation', 'Tell people what you hold and why.'],
                        ['Safety and security', 'Protect data from loss, leaks and misuse.']],
                  widths=[4.4, 7.6], icons=['flag', 'check', 'tag', 'clock', 'doc', 'people', 'lock'], note='Teaching summary of public descriptions. Not legal advice. Read the Act for the exact wording.',
                  notes=('Public summaries of the Act describe seven principles. Accountability: someone is responsible and can show what was done. Fair and lawful processing. Collect only adequate and relevant data, which means only what the purpose needs. '
                         'Keep data only as long as needed. Keep it accurate. Be open: tell people what you hold and why. And protect it from loss, leaks and misuse. For a model team, that translates into jobs: write down the purpose on the model card, drop columns you do not need, '
                         'and never publish personal data. This is a summary, so read the Act itself for the exact words. Which principle does your current project test most?')))

    # 22 rights
    S.append(dict(kind='table', title='Data subjects have rights, and a model team has matching jobs', headers=['Right', 'In plain words', 'A model team keeps'],
                  rows=[['Access', 'Ask what data an organisation holds about you.', 'A record of which data feeds the model'], ['Correction', 'Ask for wrong data to be fixed.', 'A way to correct a record and retrain'],
                        ['Erasure', 'Ask for data to be deleted, in the cases the law allows.', 'A deletion process that covers copies'], ['Automated decisions', 'Ask not to be subject to a decision taken only by a computer.', 'A person who reviews the model output'],
                        ['Consent and cloud tools', 'My understanding: the Act expects a lawful basis such as consent. Personal data sent outside Uganda may need safeguards.', 'No real personal data in Colab, GitHub or an app host until checked']],
                  widths=[2.4, 5.4, 4.2], icons=['magnifier', 'notebook', 'cross', 'person', 'lock'], note='My understanding from public summaries. Check the Act and take advice for your own case.',
                  notes=('Public summaries list rights for data subjects. Access: asking what data an organisation holds about you. Correction: asking for wrong data to be fixed. Erasure: asking for data to be deleted, in the cases the law allows. '
                         'And a right related to automated decisions: asking not to be subject to a decision taken only by a computer. For a model team each right becomes a job: record what data feeds the model, correct and retrain, delete copies, and keep a person who reviews the output. One more row: my understanding is that the Act expects a lawful basis such as consent, and that sending personal data to a server outside Uganda may need extra safeguards, so check before you put real personal data into Colab, GitHub or an app host. Ask your data protection officer. Which of these would be hardest in your organisation?')))

    # 23 use at work
    S.append(dict(kind='table', title='Where you will use this at work: make it repeatable, then make it checkable', headers=['Your job', 'What you ship', 'What today lets you do'],
                  rows=[['Credit analyst at a bank or SACCO, using Python and scikit-learn', 'A default-risk model', 'Save it with joblib, write a model card, and audit approval and error rates by gender and district before release.'],
                        ['Officer in a ministry, using pandas and Excel', 'A monthly report notebook', 'Fix the seed, record the versions, and rerun it each month from the top so the numbers reproduce.'],
                        ['Sales analyst at a retailer, using Streamlit', 'A forecast tool for branch managers', 'Wrap the model in a small app, with a README, in a repository that holds no customer data.'],
                        ['Data officer at an NGO, using GitHub', 'A survey analysis', 'Keep the code in Git, keep personal data out, and check the duties of the data controller.']],
                  widths=[3.9, 2.9, 5.2], icons=['coin', 'doc', 'chart', 'people'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank or a SACCO who builds a default model should save it with joblib, write a model card and audit approval and error rates by gender and district before release. '
                         'An officer in a ministry whose monthly report must reproduce should fix the seed, record the versions and rerun it from the top each month. A sales analyst can wrap a forecast in a small Streamlit app for branch managers, in a repository with no customer data. '
                         'A data officer at an NGO can keep the analysis in Git, keep personal data out, and check the duties of a data controller. Which of these is closest to your job?')))

    # 24 bridge code
    S.append(dict(kind='code', title='Read the recipe before the lab: a seed and an approval rate by group',
                  code="known = test.dropna(subset=['monthly_income_ugx'])\npay = known.loan_amount_ugx * 1.15 / known.term_months\nratio = pay / known.monthly_income_ugx\nknown = known.assign(flag=(ratio > 0.40).astype(int))\napproval = 1 - known.groupby('gender').flag.mean()\nprint(approval.round(3).to_dict())\nprint(round(approval.min() / approval.max(), 3))",
                  output=F['bridge_out'].split('\n'),
                  reads=['Line 1 keeps the held-out (test) loans that have an income.', 'Lines 2 to 4 flag a loan when the ratio (instalment_to_income) is above 0.40. The 1.15 is an illustrative charge factor.', 'Line 5 is the approval rate: one minus the flag rate, for each gender.', f'Line 7 is the disparate impact ratio: {dA:.3f}.'],
                  notes=(f'Before the lab, read this recipe. The variable test holds the two thousand held-out loans. Line one keeps those that have a monthly income. Lines two to four work out the instalment-to-income ratio, using the illustrative one point one five charge factor, and flag the loan when it is above zero point four. '
                         f'Line five groups by gender and takes one minus the mean flag, which is the approval rate. The output says women {pct(A["F"]["approval"])} percent and men {pct(A["M"]["approval"])}. '
                         f'Line seven divides the lower rate by the higher one, giving {dA:.3f}, close to one. In the lab you do the same with the occupation rule and with the model. What would you expect for the occupation rule?')))

    # 25 divider
    S.append(dict(kind='divider', title='Part 2: the notebook lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Open the Colab notebook called Session 23, Ship it. Run the first cell, which puts the data files next to the notebook, and then the check cell. '
                         'In every step predict first, then run, then read the output, then change one thing and see what moves. The checks tell you whether your answer matches. '
                         'You do not need Streamlit installed, because the lab writes the app file and you deploy it later with your own account.')))

    # 26 lab map
    S.append(dict(kind='steps', title='The lab has five parts, and you keep a folder ready to push', steps=[dict(head='1 Repeat', text='Seed, versions', icon='check'), dict(head='2 Audit rules', text='Instalment and occupation', icon='magnifier'),
                                                                                                         dict(head='3 Save', text='Fit, dump, load', icon='folder'), dict(head='4 Audit model', text='Then write app.py', icon='shield'), dict(head='5 Document', text='Model card, checklist', icon='doc')], highlight=None,
                  caption='Twenty-seven checks in 45 minutes. In each step: predict, run, read, change one thing.',
                  notes=('Here is the map of the lab. Step one, draw loans with a seed twice and check you get the same loans, and print your versions. Step two, split the loans once, then audit two rules on the held-out loans by gender: the instalment rule and the occupation rule, with approval rates, disparate impact and error rates. '
                         'Step three, fit a pipeline on the training loans only, save it with joblib, load it back and check it gives identical predictions. Step four, audit the model on the held-out loans the same way, then write the app file and the requirements file. Step five, complete a model card and a data protection checklist. '
                         'Please do not skip the predictions. They are where you learn.')))

    # 27 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Row numbers drawn with random_state=42', ', '.join(str(i) for i in F['seed42'])], ['Default rate: women, and Masaka', f'{pct(F["by_gender"]["F"])}% and {pct(F["by_district"]["Masaka"])}%'],
                        ['Instalment rule (held-out loans): approval women, men, and DI', f'{pct(A["F"]["approval"])}%, {pct(A["M"]["approval"])}%, {dA:.3f}'], ['Occupation rule (held-out loans): approval women, men, and DI', f'{pct(Bq["F"]["approval"])}%, {pct(Bq["M"]["approval"])}%, {dB:.3f}'],
                        ['Occupation rule: defaults missed, women and men', f'{pct(Bq["F"]["fnr"])}% and {pct(Bq["M"]["fnr"])}%'], ['Model: held-out AUC, and first-loan probability', f'{F["auc_test"]:.3f} and {F["p_first"]:.2f}'],
                        [f'Model at {THRESHOLD}: approval women, men', f'{pct(M["F"]["approval"])}% and {pct(M["M"]["approval"])}%'], ['Lines in app.py, and libraries in requirements.txt', f'{len(APP_LINES)} and 5']],
                  widths=[7.0, 5.0], icons=['grid', 'chart', 'people', 'people', 'cross', 'coin', 'shield', 'doc'], note='The model numbers may differ in the third decimal because the solver differs.',
                  notes=('Use this table as your own self-check. Nobody marks it. If one number does not match, stop and call me, because later steps use earlier ones. '
                         'The most common causes are forgetting to tidy the district spellings, including loans with no income in the rule steps, and dividing the higher approval rate by the lower one. '
                         'The model numbers can differ slightly in the third decimal, because scikit-learn and my check use different solvers. Find out why it differs. What does it mean if your disparate impact is above one?')))

    # 28 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError: name is not defined', 'A cell above did not run, or you ran cells out of order.', 'Runtime, Restart session and run all. Fix the first error.'],
                        ['Different row numbers from the table', 'The seed was not set, or you used a different seed.', 'Use random_state=42 in both draws.'],
                        ['Disparate impact above 1', 'You divided the higher rate by the lower one.', 'Divide the lower approval rate by the higher one.'],
                        ['ModuleNotFoundError for joblib', 'The library is not installed in this session.', 'Run pip install joblib in a cell, then rerun.'],
                        ['Model probabilities all about the same', 'You skipped the imputer or scaler in the pipeline.', 'Use make_pipeline with the imputer, scaler and model.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. A NameError means a cell above did not run or you ran cells out of order, so restart the session and run all, and fix the first error. '
                         'Different row numbers from the table mean the seed was missing or different. A disparate impact above one means you divided the higher rate by the lower one. A module not found for joblib means you can install it with pip in a cell. '
                         'And probabilities that are all similar usually mean the imputer or scaler is missing from the pipeline. Read the message first. It usually tells you the answer.')))

    # 29 exit
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Name three habits that let a colleague repeat your notebook.', 'Set the random seed, record the library versions, and restart and run all from the top.'],
                        [f'A rule never sees gender, yet approves {pct(Bq["F"]["approval"])}% of women and {pct(Bq["M"]["approval"])}% of men. What is going on, and what next?', 'A proxy variable (occupation) carries the information. Report the disparate impact and error rates by group, and justify or change the rule.'],
                        ['In a loan file, who is the data subject and who is the data controller?', 'The borrower is the data subject. The lender, which decides how the data is used, is the data controller.']],
                  widths=[5.6, 6.4], icons=['check', 'people', 'lock'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, name three habits that let a colleague repeat your notebook. '
                         'Two, a rule never sees gender, yet it approves seventy-one percent of women and fifty-four percent of men. What is going on and what do you do next? Three, in a loan file, who is the data subject and who is the data controller? '
                         'The short answers are on the slide. If you got all three, you are ready to present next session.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Run the solution notebook once in Colab before class (it needs scikit-learn and joblib, which Colab has). It was built here without them, so the model cells were proved with a stand-in only, and every model number comes from numpy replicas: before the course starts, compare the notebook output with the slides and fix any difference.',
              'Share the data.zip link or the file so learners can run the first notebook cell. Check that every learner has a Google account.',
              'Ask learners to create a free GitHub account before the session if they want to deploy the app afterwards. Deployment is not part of the 45-minute lab.',
              'Write the check table (slide 27 of the deck) on the board before the lab.',
              'Remind learners that the Data Protection and Privacy Act slides are a teaching summary and not legal advice. Do not answer legal questions beyond the slide.'],
        misconceptions=[('If I remove the gender column the model cannot be unfair', f'A proxy variable such as occupation carries the information. The occupation rule approves {pct(Bq["F"]["approval"])}% of women and {pct(Bq["M"]["approval"])}% of men, a ratio of {dB:.2f}.'),
                        ('A high accuracy number means the model is ready to ship', 'Shipping needs repeatability, a model card, a drift watch, a fairness audit and a data protection check as well.'),
                        ('A pickle or joblib file is just data', 'Loading a file can run code that is inside it. Load only files you trust and read the library warning.'),
                        ('Deleting a file from GitHub removes it', 'Git keeps history. A password or personal data that was ever pushed must be treated as exposed.'),
                        ('Disparate impact of 0.8 is a legal line in Uganda', 'It is a screening rule of thumb from US employment practice. It starts a question and does not give a verdict.')],
        probes=[('Why does the same seed give the same draw?', 'The generator starts from the same number, so it makes the same sequence.'),
                ('What goes in a requirements.txt?', 'One library per line with its version, for example pandas==2.3.3.'),
                ('What does Restart and run all test?', 'That the notebook does not depend on cells you deleted or ran out of order.'),
                ('Why save with joblib?', 'To reuse a trained model without training again, in an app or a report.'),
                ('Which command uploads commits to GitHub?', 'git push.'),
                ('What is the difference between data drift and concept drift?', 'Data drift: the inputs change. Concept drift: the link between inputs and outcome changes.'),
                ('What is a proxy variable?', 'A variable that stands in for another one, such as occupation for gender.'),
                ('Who is the data controller in a loan file?', 'The lender, the organisation that decides how the data is used.')],
        lab_steps=[('Step 1: seeds, versions', f'Row numbers {", ".join(str(i) for i in F["seed42"])} for seed 42, both times. Seed 43 differs.'),
                   ('Step 2: default rates', f'Women {pct(F["by_gender"]["F"])}%, men {pct(F["by_gender"]["M"])}%, highest district {F["top_district"]} {pct(F["by_district"][F["top_district"]])}%. Learners who skip the district tidy get {F["n_district_spellings"]} districts instead of {F["n_districts"]}.'),
                   ('Step 3: instalment rule', f'On the held-out loans: approval {pct(A["F"]["approval"])}% and {pct(A["M"]["approval"])}%, DI {dA:.3f}. Test loans with no income are dropped first ({F["known"]} of {n(F["n_test"])} remain).'),
                   ('Step 4: occupation rule', f'Occupation default rates come from the training loans. Approval {pct(Bq["F"]["approval"])}% and {pct(Bq["M"]["approval"])}%, DI {dB:.3f}. Occupations flagged: {", ".join(F["occ_flagged"])}.'),
                   ('Step 5: error rates', f'Defaults missed: women {pct(Bq["F"]["fnr"])}%, men {pct(Bq["M"]["fnr"])}%.'),
                   ('Step 6: split, fit, save and load', f'The pipeline is fitted on the {n(F["n_train"])} training loans. Held-out AUC {F["auc_test"]:.3f}, first loan default probability about {F["p_first"]:.2f}. The loaded model gives identical predictions to the original.'),
                   ('Step 7: model audit', f'At threshold {THRESHOLD}, approval {pct(M["F"]["approval"])}% and {pct(M["M"]["approval"])}%, DI {dM:.3f}. The audit is on the {n(F["n_test"])} held-out loans.'),
                   ('Step 8: app and requirements', f'app.py has {len(APP_LINES)} lines and compiles. requirements.txt has 5 lines.'),
                   ('Step 9: model card and checklist', 'Five card sections and seven checklist lines filled. Praise cards that state a limit.')],
        rescue=['If the concepts run over, shorten the six Git words (slide 8) and the principles table (slide 21). The lab repeats the ideas.',
                'If only 30 minutes of lab remain, do steps 1, 2, 4, 6 and 9 and set the rest as homework.',
                'If joblib is missing in the Colab session, run pip install joblib in a cell. If a learner has no GitHub account, they can still finish the lab and push later.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the deck again for learners who were absent.', 'Ask each learner to create a public GitHub repository for the folder, check it contains no personal data, and bring the link to Session 24.',
               'Ask each learner to bring their project question and result to Session 24.'],
        lab_answer_key=[['Step 1 PREDICT: will two draws with the same seed be identical, and a draw with another seed?', f'Same seed, identical rows ({", ".join(str(i) for i in F["seed42"])}). Another seed gives a different draw.'],
                        ['Step 3 READ: what does a disparate impact near 1 mean?', f'The two groups have nearly equal approval rates ({dA:.3f}).'],
                        ['Step 4 PREDICT: will the occupation rule treat men and women alike?', f'No. Women are approved {pct(Bq["F"]["approval"])}% and men {pct(Bq["M"]["approval"])}%, DI {dB:.3f}, because occupation is a proxy for gender.'],
                        ['Step 4 CHANGE: use 0.13 instead of 0.12. What happens?', 'Mechanic (default rate about 0.125 on the training loans) drops out of the flagged list, so the disparate impact rises to about 0.79. Any change must be explained from the occupation default rates.'],
                        ['Step 5 READ: who is harmed by the missed defaults?', f'The lender, which loses money, and the women whose defaults the rule misses ({pct(Bq["F"]["fnr"])}% against {pct(Bq["M"]["fnr"])}% for men) in the sense that the rule is less accurate for them.'],
                        ['Step 6 READ: why compare the loaded model with the original?', 'To prove that saving and loading changed nothing: the maximum difference is 0.'],
                        ['Step 7 CHANGE: set the threshold to 0.2. What changes?', 'Fewer loans are flagged, so approval rates rise for both groups, and the disparate impact stays near 1.'],
                        ['Step 8 READ: which line loads the model, and which shows the probability?', 'Line 5 loads the model. Line 25 shows the metric (line 24 computes it).']])
    return sess
