"""Session 23 lab notebook: repeat it, audit it, save it, document it (Nile Microfinance loans).

The model cells need scikit-learn and joblib, which the authoring sandbox lacks, so NEEDS marks the notebook UNVERIFIED there. All expected numbers come from content/s23.py facts(),
computed with pandas and an independent numpy fit of the same logistic objective. The solution was also run here against the NumPy scikit-learn stand-in in ref/ and a pickle-based joblib shim.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('s23_content', BUILD / 'content' / 's23.py')
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

TITLE = 'Ship it'
NEEDS = ['sklearn', 'joblib']


def build(solution):
    F = S.facts()
    A, B, M = F['ruleA'], F['ruleB'], F['model']
    CARD = F['card']
    di_a, di_b, di_m = S.di(A), S.di(B), S.di(M)
    TH = S.THRESHOLD

    def ans(var, code, hint):
        return f'{var} = {code}' if solution else f'{var} = None  # your code here: {hint}'

    def line(code, hint):
        return code if solution else f'# your code here: {hint}'

    nb = NB.Notebook()
    nb.md('# Session 23: Ship it\n\nYou will repeat a draw with a seed, audit two rules and a model for fairness by group, save the model with joblib, write the app file and complete a model card. '
          'The data is the fictional Nile Microfinance file `loans.csv`. Where a cell says `None  # your code here`, replace it with your answer. The checks at the end of each step say OK or NOT YET.')
    nb.data_setup()
    nb.check_setup()
    nb.code('# Imports and a small helper so that a check never crashes while your answer is still None.\n'
            'import os\nimport numpy as np\nimport pandas as pd\n\n'
            'def safe(f):\n    try:\n        return f()\n    except Exception:\n        return float("nan")\n')

    # ---- step 1
    nb.step(1, 'Repeat it: a seed and the library versions', 'A random seed makes a random draw repeatable. A colleague who uses the same seed gets the same loans.')
    nb.predict('You draw 5 loans twice with `random_state=42`, and once with `random_state=43`. Which draws will match?')
    nb.code('loans = pd.read_csv("loans.csv")\n'
            + ans('s1', 'loans.sample(5, random_state=42).index.tolist()', 'draw 5 loans with random_state=42 and keep their row numbers (.index.tolist())') + '\n'
            + ans('s2', 'loans.sample(5, random_state=42).index.tolist()', 'the same draw again') + '\n'
            + ans('s3', 'loans.sample(5, random_state=43).index.tolist()', 'the draw with random_state=43') + '\n'
            'print(s1, s2, s3)\nprint("numpy", np.__version__, "pandas", pd.__version__)\n'
            f'check("seed 42, first draw", safe(lambda: s1), {F["seed42"]}, 0)\n'
            f'check("seed 42, second draw", safe(lambda: s2), {F["seed42"]}, 0)\n'
            f'check("seed 43 draw", safe(lambda: s3), {F["seed43"]}, 0)\n')
    nb.read('Which two lists are identical? Which library versions did your session print? Write them next to your results.')
    nb.change('Change the seed in the first draw to 7. Do the two seed-42 draws still match each other?')

    # ---- step 2
    nb.step(2, 'Default rates by group', 'Before any rule, look at the default rate for each gender and district. First tidy the district spellings.')
    nb.predict('Women and men: will the default rates differ by more than 5 percentage points?')
    nb.code('loans["district"] = loans.district.str.strip().str.title()   # given: the cleaning from Session 8\n'
            + ans('by_gender', 'loans.groupby("gender").default.mean()', 'the mean of default for each gender (groupby)') + '\n'
            + ans('by_district', 'loans.groupby("district").default.mean()', 'the mean of default for each district') + '\n'
            'print(by_gender)\nprint(by_district)\n'
            f'check("default rate, women", safe(lambda: by_gender["F"]), {F["by_gender"]["F"]:.4f}, 0.002)\n'
            f'check("default rate, {F["top_district"]}", safe(lambda: by_district["{F["top_district"]}"]), {F["by_district"][F["top_district"]]:.4f}, 0.002)\n')
    nb.read('Which district has the highest default rate? How many districts are there after tidying?')
    nb.change('Skip the tidy line and run again. How many districts do you get, and why is that wrong?')
    nb.md('**Split the loans once.** From here on, everything that is learned from the data (the occupation default rates, the model) is learned from the 6,000 training loans, and every audit is run on the 2,000 held-out (test) loans. '
          'This is the same stratified split as Sessions 14 to 17, so you get the same 2,000 loans. A blank income stays blank for now: the model Pipeline fills it later, using the training loans only.')
    nb.code('from sklearn.model_selection import train_test_split\n\n'
            'loans["instalment_to_income"] = loans.loan_amount_ugx * 1.15 / loans.term_months / loans.monthly_income_ugx   # the 1.15 is an ILLUSTRATIVE charge factor, not in the data\n'
            'features = ["monthly_income_ugx", "loan_amount_ugx", "term_months", "previous_late_payments"]   # a deliberately simplified four-variable model\n'
            'X = loans[features]\ny = loans.default\n'
            'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n'
            'train = loans.loc[X_train.index]   # the 6,000 training loans\ntest = loans.loc[X_test.index]   # the 2,000 held-out loans\n'
            'print(len(train), len(test), "defaults in the test loans:", y_test.sum())\n'
            f'check("training loans", len(train), {F["n_train"]}, 0)\ncheck("held-out loans", len(test), {F["n_test"]}, 0)\ncheck("defaults in the held-out loans", y_test.sum(), {F["test_defaults"]}, 0)\n'
            f'check("same held-out loans as Sessions 14 to 17 (sum of the row numbers)", sum(X_test.index), {F["test_index_sum"]}, 0)\n')

    # ---- step 3
    nb.step(3, 'Audit rule A: the instalment rule', 'Rule A flags a loan as high risk when instalment_to_income is above 0.40 (about 35 percent of income, before the illustrative 15 percent charge). We audit it on the held-out loans that have an income. Approval rate is the share of loans not flagged. Disparate impact is the lower approval rate divided by the higher.')
    nb.predict('The rule never uses gender. Will women and men have similar approval rates?')
    nb.code('known = test.dropna(subset=["monthly_income_ugx"]).copy()   # held-out loans with an income\n'
            'known["flag"] = (known.instalment_to_income > 0.40).astype(int)\n'
            + ans('approval_a', '1 - known.groupby("gender").flag.mean()', 'one minus the mean flag for each gender') + '\n'
            + ans('di_a', 'approval_a.min() / approval_a.max()', 'the lower approval rate divided by the higher') + '\n'
            'print(approval_a)\nprint(di_a)\n'
            f'check("rule A approval, women", safe(lambda: approval_a["F"]), {A["F"]["approval"]:.4f}, 0.002)\n'
            f'check("rule A disparate impact", safe(lambda: di_a), {di_a:.4f}, 0.003)\n')
    nb.read('Is the disparate impact close to 1? What does that tell you about the two groups?')
    nb.change('Change 0.40 to 0.30. What happens to the two approval rates and to the disparate impact?')

    # ---- step 4
    nb.step(4, 'Audit rule B: the occupation rule', 'Rule B gives each loan the default rate of its occupation, learned from the training loans, and flags it above 12 percent. It never sees gender either.')
    nb.predict('Women are 77 percent of tailors and 73 percent of salon owners. Will rule B approve women and men equally?')
    nb.code('occ_rate = train.groupby("occupation").default.mean()   # learned from the training loans only\n'
            'known["flag2"] = (known.occupation.map(occ_rate) > 0.12).astype(int)\n'
            + ans('approval_b', '1 - known.groupby("gender").flag2.mean()', 'one minus the mean of flag2 for each gender') + '\n'
            + ans('di_b', 'approval_b.min() / approval_b.max()', 'the lower approval rate divided by the higher') + '\n'
            'print(approval_b)\nprint(di_b)\n'
            f'check("rule B approval, women", safe(lambda: approval_b["F"]), {B["F"]["approval"]:.4f}, 0.002)\n'
            f'check("rule B disparate impact", safe(lambda: di_b), {di_b:.4f}, 0.003)\n')
    nb.read('Is the disparate impact below the 0.8 rule of thumb (a screening flag, not a legal test)? Which column acts as the proxy variable?')
    nb.change('Print `known.groupby("occupation").flag2.mean()`. Which occupations does the rule flag?')

    # ---- step 5
    nb.step(5, 'Error rates: who does the rule miss?', 'A false negative is a loan that defaulted but was not flagged. The false negative rate is the share of defaults the rule missed.')
    nb.predict('Under rule B, will the share of missed defaults be the same for women and men?')
    nb.code('defaults = known[known.default == 1]   # only the loans that really defaulted\n'
            + ans('fnr', '1 - defaults.groupby("gender").flag2.mean()', 'one minus the mean of flag2 among the defaults, for each gender') + '\n'
            'print(fnr)\n'
            f'check("missed defaults, women", safe(lambda: fnr["F"]), {B["F"]["fnr"]:.4f}, 0.002)\n'
            f'check("missed defaults, men", safe(lambda: fnr["M"]), {B["M"]["fnr"]:.4f}, 0.002)\n')
    nb.read('Which group has more defaults that the rule misses? Who is harmed: the lender, the borrower, or both?')
    nb.change('Repeat the calculation for rule A (use `flag`). Are the two groups treated more alike?')

    # ---- step 6
    nb.step(6, 'Fit, save and load the model', 'A scikit-learn pipeline chains an imputer, a scaler and a logistic regression (default C = 1.0, L2 penalty). Fit it on the 6,000 training loans only, so the median and the scaling come from the training loans. joblib writes the trained pipeline to a file, saved in your Colab folder. Load files only from sources you trust: joblib uses pickle underneath.')
    nb.predict('After you save and load the model, will its predictions differ from the original in any decimal place?')
    nb.code('from sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nimport joblib\n\n'
            'from sklearn.metrics import roc_auc_score\n\n'
            + ans('model', 'make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))', 'a pipeline of an imputer (median), a scaler and a logistic regression') + '\n'
            + line('model.fit(X_train, y_train)', 'fit the model on the TRAINING loans, X_train and y_train') + '\n'
            + line('joblib.dump(model, "loan_model.joblib")', 'save the model to loan_model.joblib with joblib.dump') + '\n'
            + ans('loaded', 'joblib.load("loan_model.joblib")', 'load the file back with joblib.load') + '\n'
            + ans('p_first', 'loaded.predict_proba(X.head(1))[0, 1]', 'the probability of default (column 1 of predict_proba) for the first loan') + '\n'
            + ans('auc_test', 'roc_auc_score(y_test, loaded.predict_proba(X_test)[:, 1])', 'roc_auc_score of y_test and the predicted probability of default (column 1) for X_test: the held-out AUC') + '\n'
            'print(p_first)\nprint("held-out AUC:", auc_test)\n'
            'diff = safe(lambda: np.abs(loaded.predict_proba(X_test) - model.predict_proba(X_test)).max())\nprint("largest difference after reload:", diff)\n'
            f'check("default probability, first loan", safe(lambda: p_first), {F["p_first"]:.4f}, 0.01)\n'
            f'check("held-out AUC (simplified four-variable model)", safe(lambda: auc_test), {F["auc_test"]:.4f}, 0.01)\n'
            'check("reloaded model gives identical predictions", diff, 0, 1e-9)\n')
    nb.read('What is the probability for the first loan, and what is the held-out AUC? Why do we compare the loaded model with the original? Your model card in Step 9 will quote the held-out AUC.')
    nb.change('Change `strategy="median"` to `"mean"` in a copy of the pipeline. Does the first-loan probability move a lot?')

    # ---- step 7
    nb.step(7, 'Audit the model by group', f'Flag a loan as high risk when the model gives a default probability of {TH} or more, then compute the approval rate for each gender on the 2,000 held-out loans.')
    nb.predict('The model never sees gender and does not use occupation. Will its disparate impact be closer to rule A or rule B?')
    nb.code(ans('flag_model', f'loaded.predict_proba(X_test)[:, 1] >= {TH}', f'True where the default probability for a held-out loan is {TH} or more') + '\n'
            + ans('approval_m', '1 - pd.Series(flag_model).groupby(test.gender.values).mean()', 'one minus the mean flag for each gender') + '\n'
            + ans('di_m', 'approval_m.min() / approval_m.max()', 'the lower approval rate divided by the higher') + '\n'
            'print(approval_m)\nprint(di_m)\n'
            f'check("model flag rate on the held-out loans", safe(lambda: np.mean(flag_model)), {CARD["flag_rate"]:.4f}, 0.02)\n'
            f'check("model approval, women", safe(lambda: approval_m["F"]), {M["F"]["approval"]:.4f}, 0.01)\n'
            f'check("model disparate impact", safe(lambda: di_m), {di_m:.4f}, 0.02)\n')
    nb.read('Is the disparate impact near 1? Would you release this model on this evidence alone? What else would you check?')
    nb.change('Change the threshold to 0.20. What happens to the approval rates?')

    # ---- step 8
    nb.step(8, 'Write app.py and requirements.txt', 'These two files, plus loan_model.joblib, are saved in your Colab folder and are what Streamlit Community Cloud needs. You do not run the app here. You deploy it later from your own GitHub repository.')
    nb.predict('How many lines does the app file have? Which line loads the model?')
    nb.code("app_code = '''" + S.APP_CODE + "'''\n"
            + line("open('app.py', 'w').write(app_code)", 'write app_code to a file called app.py') + '\n'
            + (('from importlib import metadata\nreq = []\nfor name in ["numpy", "pandas", "scikit-learn", "joblib", "streamlit"]:\n    try:\n        req.append(f"{name}=={metadata.version(name)}")\n'
                '    except metadata.PackageNotFoundError:\n        req.append(name)   # not installed in this session: list the name only\n') if solution else
               'req = None  # your code here: a list with one line per library: numpy, pandas, scikit-learn, joblib, streamlit, as name==version (name only if not installed)\n')
            + 'open("requirements.txt", "w").write("\\n".join(req or []) + "\\n")\n'
            'app_text = open("app.py").read() if os.path.exists("app.py") else ""\n'
            'try:\n    compile(app_text, "app.py", "exec")\n    compiles = 1 if app_text else 0\nexcept SyntaxError:\n    compiles = 0\n'
            'print(len(app_text.splitlines()), "lines in app.py;", len(open("requirements.txt").read().split()), "libraries in requirements.txt")\n'
            f'check("app.py has {len(S.APP_LINES)} lines", len(app_text.splitlines()), {len(S.APP_LINES)}, 0)\n'
            'check("app.py is valid Python", compiles, 1, 0)\n'
            'check("app.py calls predict_proba", int("predict_proba" in app_text), 1, 0)\n'
            'check("requirements.txt lists 5 libraries", len(open("requirements.txt").read().split()), 5, 0)\n')
    nb.read('Which line of app.py loads the model and which shows the result? Why must requirements.txt list streamlit?')
    nb.change('Change the caption in app_code to your own sentence, write the file again and read it back. If an app host cannot install a pinned version, remove the version number of that library from requirements.txt and test again.')

    # ---- step 9
    nb.step(9, 'The model card and the data protection checklist', 'Write what the model is for, what it learned from, how well it works, where it fails and who reviews it. Then say what you do for each of the seven principles in the Data Protection and Privacy Act, 2019 (a teaching summary, not legal advice).')
    nb.predict('Which section of the card would a manager read first? Which principle is hardest for your own project?')
    if solution:
        card = ('model_card = {\n'
                '    "purpose": "Ranks loan applications so an officer knows which to review first. It does not approve or refuse.",\n'
                '    "data": "8,000 fictional Nile Microfinance loans, 2023 to 2025; 6,000 for training, 2,000 held out. collection_calls was removed because it leaks the answer.",\n'
                '    "metrics": f"Simplified four-variable model. Held-out AUC {auc_test:.3f}. At decision threshold 0.15 it flags {np.mean(flag_model):.0%} of the held-out loans.",\n'
                '    "limits": "Fictional data. 379 loans lack income and are filled with the training median. Four variables only. Not tested after the data changes.",\n'
                '    "fairness_and_review": f"On the held-out loans, approval women {approval_m[\'F\']:.1%}, men {approval_m[\'M\']:.1%}, disparate impact {di_m:.3f}. Reviewed by the credit manager and the data protection officer before each release.",\n'
                '}\n'
                'dp_checklist = {\n'
                '    "Accountability": "The credit manager owns the model and the model card.",\n'
                '    "Fair and lawful processing": "Loans are scored only for the purpose stated on the card.",\n'
                '    "Adequate and relevant data": "Four input columns only. collection_calls and personal identifiers are left out.",\n'
                '    "Kept only as long as needed": "Delete training extracts when the review ends. Date to be set.",\n'
                '    "Quality of information": "Missing incomes are filled with the training median inside the Pipeline. Age is not used, so the two impossible ages cannot affect the model.",\n'
                '    "Openness and participation": "Borrowers are told that a model ranks applications and that a person decides.",\n'
                '    "Safety and security": "No personal data in the public repository. Passwords and keys stay out of the code.",\n'
                '}\n')
    else:
        card = ('model_card = {\n    "purpose": None,   # your code here: one sentence\n    "data": None,   # your code here: source, years, what you removed and why\n    "metrics": None,   # your code here: the held-out AUC from Step 6 and the share of held-out loans flagged\n'
                '    "limits": None,   # your code here: at least one limit\n    "fairness_and_review": None,   # your code here: the approval rates and disparate impact from step 7 (held-out loans), and who reviews\n}\n'
                'dp_checklist = {\n    "Accountability": None,   # your code here: what you do, or still need to do\n    "Fair and lawful processing": None,\n    "Adequate and relevant data": None,\n'
                '    "Kept only as long as needed": None,\n    "Quality of information": None,\n    "Openness and participation": None,\n    "Safety and security": None,\n}\n')
    nb.code(card + 'for k, v in model_card.items():\n    print(k, ":", v)\n'
            'check("model card has 5 sections", sum(bool(v) for v in model_card.values()), 5, 0)\n'
            'check("checklist has 7 principles", sum(bool(v) for v in dp_checklist.values()), 7, 0)\n'
            'show_checks()')
    nb.read('Does your card state a limit? A limit stated openly builds trust. A hidden one costs it.')
    nb.change('Add a sixth key to model_card called "next_review" with a date, and print the card again.')
    nb.md('## What you keep\n\n`loan_model.joblib`, `app.py` and `requirements.txt` are saved in your Colab folder (the Files panel on the left). Download them and this notebook into one folder. Create a free GitHub account, make a new public repository, and upload the folder after checking that it holds no personal data. '
          'Then, if you wish, deploy the app from Streamlit Community Cloud. At the time of writing it is free for public repositories. Check the current limits.')
    return nb
