"""Word and PDF documents for AI and Data Science Professional (KLAi edition), generated from the session files.
python3 kit/make_docs.py [guide|script|sheets|learner|checklist|all]
Writes under the course folder (BUILD.parent.parent), each as .docx and .pdf:
  04 Facilitator Materials: Facilitator Guide, Presenter Script, Sheets Lab Answers, Playback and Rehearsal Checklist
  03 Learner Materials: Start Here, Glossary, Sheets Lab Sheets
Never edit the generated files; edit this script or the session files."""
import re
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent.parent          # the course folder: AI and Data Science Professional/
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
import deck  # noqa: E402
import docx_kit  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

COURSE = 'AI and Data Science Professional'
FAC = ROOT / '04 Facilitator Materials'
LEARN = ROOT / '03 Learner Materials'
DATA_DIR = LEARN / 'Practice Files' / 'data'
docx_kit.FOOT = f'KLAi | {COURSE} | '
SESS = [deck.load(n) for n in range(1, 25)]
SPECS = {s['num']: deck.build_spec(s) for s in SESS}
WPM = 130

MILESTONES = {8: 'Project milestone 1: a cleaned file reconciled to a control total',
               13: 'Project milestone 2: a one page analysis report and the project question',
               19: 'Project milestone 3: a tested model beside its baseline',
               24: 'Course project: the presentation'}


# ------------------------------------------------------------------ helpers
def new_doc2(name):
    d = new_doc(name, COURSE)
    for t in d.sections[0].header.tables:
        for c in t._cells:
            for p in c.paragraphs:
                for r in p.runs:
                    if 'Mathematics' in r.text:
                        r.text = f'{COURSE}  |  KLAi'
    return d


def to_pdf(path):
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_docsA', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True, timeout=300)


def finish(d, path):
    save(d, path)
    to_pdf(path)


def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def clock_rows(s):
    t, rows = 0, []
    for m, lab in s['clock']:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), lab])
        t += m
    return rows


def stitle(sl):
    return sl['title']['text'].replace('\n', ' ') if sl.get('title') else (sl.get('title_raw') or '')


def slide_rows(s):
    return [(i, stitle(sl), sl.get('section') or '', sl['notes']) for i, sl in enumerate(SPECS[s['num']]['slides'], 1)]


def part2_index(s):
    for i, t, _sec, _n in slide_rows(s):
        if t.startswith('Part 2'):
            return i
    return None


def notes_minutes(s, upto=None):
    w = sum(len(n.split()) for i, _t, _s, n in slide_rows(s) if upto is None or i < upto)
    return w, w / WPM


def modules():
    out = {}
    for s in SESS:
        out.setdefault(s['block'], []).append(s)
    return out


def mod_name(blk):
    return blk.replace('Module ', '').replace(':', '')


def lab_tool(s):
    n = s['num']
    if n == 1:
        return 'Google Sheets, then Google Colab'
    if n == 24:
        return 'Google Sheets (planning) and your own course project'
    if s.get('sheet_tasks'):
        return 'Google Sheets'
    if n == 10:
        return 'Google Colab with SQLite'
    return 'Google Colab'


# per-session honest status (used in the guide boxes and the checklist)
SESSION_OPEN = {
    1: 'Sheets formulas were computed in pandas and not run in real Google Sheets. The first Colab cell was not run in real Colab.',
    2: 'Sheets formulas (UNIQUE, SUMPRODUCT with MATCH, SUMIF) were not run in real Google Sheets. Check them on your own copy.',
    3: 'Sheets formulas and the chart settings (histogram, pivot tables) were not run in real Google Sheets. The numbers come from pandas.',
    4: 'The simulation tab (INDEX with RAND, freezing values, AVERAGEIF with an empty criterion) was not run in real Google Sheets. The answer ranges come from numpy.',
    10: 'Check the SQLite version in Colab. Before version 3.39 there is no RIGHT JOIN or FULL OUTER JOIN.',
    11: 'Check the seaborn version in Colab. Older versions do not accept err_kws or linecolor.',
    12: 'The notebook uses SciPy and statsmodels, which were not available where it was built. It was only syntax-checked. The numbers on the slides come from numpy.',
    13: 'The notebook uses statsmodels, which was not available where it was built. It was only syntax-checked. The numbers come from numpy.',
    14: 'The notebook was only syntax-checked here. The loans numbers come from a numpy replica of the scikit-learn split and tree. Run the index check in LOANS_RECIPE.md on real scikit-learn first.',
    15: 'The notebook was only syntax-checked here. Every number comes from a numpy replica. Run the index check in LOANS_RECIPE.md on real scikit-learn first. Counts at a threshold may move by a few loans.',
    16: 'The notebook was only syntax-checked here. Every number comes from a numpy replica. Run the index check in LOANS_RECIPE.md on real scikit-learn first.',
    17: 'The notebook was only syntax-checked here. Slide numbers come from numpy replicas of the algorithms. Compare every number on real scikit-learn.',
    18: 'The notebook was only syntax-checked here. Slide numbers come from numpy. Run it once in Colab and compare every check.',
    19: 'The Pipeline cells ran here only against a numpy stand-in. Confirm in Colab that the Pipeline MAE equals the numpy MAE and that the notebook ends with All 19 checks pass.',
    20: 'The notebook was only syntax-checked here. The MLPClassifier, RandomForestClassifier and LogisticRegression numbers come from numpy replicas. Widen a tolerance if a check fails. The optional pretrained model cell needs a licence check.',
    21: 'The scikit-learn recipe, the step 8 check (about 0.79) and the sentence-transformers results were not run on the real libraries. Confirm the model licence and size on the model card.',
    22: 'No language model was run when this deck was written. Every score comes from TF-IDF retrieval in numpy. Confirm the name, size and licence of the small model before class.',
    23: 'The notebook was only syntax-checked here and its model cells were proved with a stand-in. Re-check the Streamlit and GitHub steps and limits. The Data Protection and Privacy Act slides are a plain-language summary and not legal advice.',
    24: 'Sheets formulas were not run in real Google Sheets.',
}

OPEN_ITEMS = [
    ('Notebooks of Sessions 12 to 18, 20 and 23',
     'Only syntax-checked here (every cell compiles). The expected numbers come from numpy replicas of the algorithms. Sessions 12 and 13 need SciPy and statsmodels, and Sessions 14 to 18, 20 and 23 need scikit-learn (Session 23 also joblib). None of these were available where the course was built.',
     'Run every solution notebook top to bottom in real Colab. Each must end with All N checks pass. Where a check fails, compare with the number on the slide. Then decide whether the slide or the tolerance changes, and rebuild.'),
    ('Loans canonical numbers (Sessions 14 to 17, 20, 23, 24)',
     'Every loans number comes from the numpy replica in content/loans_canon.py and not from real scikit-learn.',
     'On real scikit-learn, check that X_test.index[:10] is [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150] and X_test.index.sum() is 8,081,998 (index check in LOANS_RECIPE.md). If either differs, the split differs and every loans number must be recomputed. If both match, expect small differences only: a count at a threshold may move by a few loans and an AUC by about 0.001.'),
    ('Session 19 Pipeline cells',
     'They ran here only against a numpy stand-in.',
     'In Colab confirm that the Pipeline MAE equals the numpy MAE and that the notebook ends with All 19 checks pass.'),
    ('Sessions 21 and 22: model and sentence-transformers cells',
     'The scikit-learn recipe slide, the Session 21 step 8 check (about 0.79) and every embedding result come from a numpy replica. The small language model cell in Session 22 (step 9) was never run, and no language model was used to write the examples. Every Session 22 score on the slides comes from TF-IDF retrieval in numpy.',
     'Re-run both notebooks in Colab with real scikit-learn and sentence-transformers. Replace any slide number that differs by more than the range in the checks. If a learner asks, say that no language model produced the Session 22 examples.'),
    ('Model licences',
     'The licence and download size of all-MiniLM-L6-v2 (384 dimensions, from its public model card), of the small language model named by MODEL_NAME in Session 22 (a suggestion that was not run) and of the optional pretrained model in Session 20 have not been confirmed.',
     'Read each model card before class and confirm the licence and the size. Swap the model name if it has changed. The course still works with embeddings and retrieval alone.'),
    ('Sheets formulas (Sessions 1 to 4 and 24)',
     'No formula or chart setting was run in real Google Sheets or Excel. The answers come from pandas and numpy on lakeside_for_sheets.xlsx. Risky spots: UNIQUE, SUMPRODUCT with MATCH, INDEX with RAND, AVERAGEIF with an empty criterion, and the histogram and pivot table settings.',
     'Work every Sheets task once in Google Sheets and compare with Sheets Lab Answers. The Session 4 answers are ranges because RAND changes on every recalculation.'),
    ('Platform limits and sign-in steps',
     'Limits and menus for Google Colab, Streamlit Community Cloud and GitHub change. The slides say at the time of writing. Google does not publish the idle and maximum session lengths of Colab. Colab had SQLite 3.37 at the time of writing, which has no RIGHT JOIN or FULL OUTER JOIN.',
     'Re-check Colab, Streamlit Community Cloud and GitHub terms and limits in the week before Session 1 and again before Session 23. Check the SQLite and seaborn versions in Colab.'),
    ('Uganda Data Protection and Privacy Act, 2019',
     'The Session 23 slides give a plain-language summary for teaching. It is not legal advice and nobody qualified has reviewed it.',
     'Say so in class and do not answer legal questions beyond the slide. If you want to teach more than the summary, have it reviewed by a qualified person first.'),
    ('Notebooks of Sessions 5 to 11',
     'They ran end to end here with pandas and numpy only. They have not been run in real Colab.',
     'Run each solution notebook once in Colab before its session.'),
    ('The data file for learners (data.zip on Google Drive)',
     'The course data are fictional and generated. Each notebook starts with a setup cell that downloads data.zip from the Google Drive link in DATA_LINK. The link is read from KLAi Build/data_zip_url.txt when the notebooks are built, and that file is empty at the moment. With no link the cell asks every learner to upload data.zip.',
     'data.zip is on Google Drive (Anyone with the link, Viewer) and the link is already built into every notebook through KLAi Build/data_zip_url.txt. Test one notebook in a fresh Colab session to confirm the download works. If you ever replace the file or the link, edit data_zip_url.txt and regenerate the notebooks (python3 kit/make_notebooks.py N, once for each coding session).'),
]


# ------------------------------------------------------------------ TERMS.md parser
def parse_terms(path):
    area, out = None, []
    for line in path.read_text().split('\n'):
        if line.startswith('## '):
            area = re.sub(r'\s*\(.*$', '', line[3:]).strip()
            if area.startswith('Added after Session 2'):
                area = 'Data, tables and statistics'
            continue
        if not line.startswith('|') or set(line.replace('|', '').strip()) <= set('-: '):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells[0] in ('Do not use as a name', 'Term'):
            continue
        if len(cells) >= 3:
            out.append((area, cells[0], cells[1], cells[2]))
        elif len(cells) == 2 and area == 'Data, tables and statistics':
            out.append((area, '', f'**{cells[0]}**', cells[1]))
    return out


def clean_alias(par):
    par = re.sub(r'^(also called|also known as|also)\s+', '', par.strip())
    if re.search(r'["=:]', par):
        return par
    parts = [x.strip() for x in re.split(r',\s*|\s+or\s+', par) if x.strip()]
    if len(parts) >= 2 and all(len(x.split()) <= 4 for x in parts):
        parts = [re.sub(r'^(an|a|the)\s+', '', x) for x in parts]
        return ', '.join(parts)
    return par


def cap(t):
    if t.startswith(('groupby', 'GROUP', 'ddof')) or '_' in t:
        return t
    return t[0].upper() + t[1:]


def industry_terms():
    out = []
    for area, col1, col2, col3 in parse_terms(BUILD / 'TERMS.md'):
        segs = list(re.finditer(r'\*\*(.+?)\*\*', col2))
        names = []
        for m in segs:
            raw = m.group(1)
            pm = re.match(r'^(.*?)\s*\((.*)\)$', raw)
            if pm:
                name, par = pm.group(1).strip(), pm.group(2)
            else:
                name, par = raw.strip(), None
                pm2 = re.match(r'^\s*\(([^()]*(?:\([^()]*\))?[^()]*)\)', col2[m.end():])
                if pm2 and pm2.group(1).strip().lower() != 'keep':
                    par = pm2.group(1)
            label = cap(name)
            par = par.replace('*', '') if par else par
            if par:
                label = 'Granularity (data warehouse alias: grain)' if name == 'granularity' else f'{label} ({clean_alias(par)})'
            names.append((name, label))
        meaning = re.sub(r'\s*Write it as one sentence:.*$', '', col3).replace('*', '')
        sib = [n for n, _l in names]
        for name, label in names:
            out.append(dict(area=area, name=name, label=label, col1=col1, meaning=meaning, sibs=[x for x in sib if x != name]))
    # terms listed in prose at the end of TERMS.md
    extra = [('Data, tables and statistics', 'instalment-to-income ratio', 'Instalment-to-income ratio (payment-to-income ratio)', 'The loan instalment divided by the monthly income. It shows how heavy the repayment is for the borrower.'),
             ('Data, tables and statistics', 'join log', 'Join log', 'An audit trail of the row counts before and after a join, so that a fan-out cannot go unseen.'),
             ('Data, tables and statistics', 'statistical power', 'Statistical power', 'The chance that a test detects a real effect of a stated size.'),
             ('Data, tables and statistics', 'sampling variability', 'Sampling variability', 'How much a sample figure, such as a mean, changes from one random sample to the next.'),
             ('Data, tables and statistics', 'reconciliation difference', 'Reconciliation difference (control total gap)', 'The gap between a cleaned total and the control total. Do not call it a residual: residual is a model word.'),
             ('Machine learning workflow, models and evaluation', 'true positive rate', 'True positive rate (recall, sensitivity)', 'The share of the real positives that the model flags. It is the vertical axis of the ROC curve.'),
             ('Machine learning workflow, models and evaluation', 'false positive rate', 'False positive rate', 'The share of the real negatives that the model wrongly flags. It is the horizontal axis of the ROC curve.')]
    have = {o['name'].lower() for o in out}
    for area, name, label, meaning in extra:
        if name not in have:
            out.append(dict(area=area, name=name, label=label, col1='', meaning=meaning, sibs=[]))
    return out


def base(t):
    return re.sub(r'\s*\(.*$', '', t).strip().lower()


OV = {
'unit of observation': 'What one record stands for, such as one till order or one loan.',
'composite key': 'A key made of two or more variables that are unique only together, such as branch and week.',
'relational model': 'Data kept in several tables that link through keys, as the tabs of the Lakeside workbook do.',
'many-to-many relationship': 'Each record on one side can match many on the other side and the reverse. A junction table links them.',
'entity relationship diagram': 'A drawing of the tables and the keys that link them. Crow\'s foot ends mark the many side.',
'informative missingness': 'A blank that carries meaning, such as a walk-in shopper with no customer id. Add a missing-indicator flag.',
'variance': 'The average squared distance from the mean. Its square root is the standard deviation.',
'interquartile range': 'Q3 minus Q1: the spread of the middle half of the sorted values.',
'sampling error': 'The gap between a sample figure and the true value for the whole population.',
'sampling distribution': 'The spread of a statistic, such as the mean, over many repeated samples. Its standard deviation is the standard error.',
'sampling variability': 'How much a sample figure changes from one random sample to the next.',
'random sample': 'Records drawn by chance so that each has a known chance of being chosen.',
'sampling with replacement': 'Each record drawn goes back before the next draw, so it can be drawn again.',
'without replacement': 'Each record drawn stays out, so no record is drawn twice.',
'causation': 'One thing makes another happen. A correlation alone does not show it.',
'selection bias': 'The records you see were chosen by something other than chance, so they misrepresent the whole.',
'survivorship bias': 'You only see the records that survived a filter, such as the shops still open.',
'a/b test': 'A controlled experiment that compares a treatment group with a control group.',
'treatment': 'The group that gets the change being tested.',
'control': 'The group that does not get the change. It is the comparison.',
'lift': 'The treatment mean minus the control mean.',
'uplift': 'Another name for lift: the gain caused by the treatment.',
'confidence level': 'The 95 percent in a 95 percent confidence interval: how often such intervals catch the true value over many samples.',
'bootstrap': 'Redraw samples with replacement from your own data many times to see how a statistic varies.',
'alternative hypothesis': 'H1: there is a real difference. It is what you decide for if the data reject H0.',
'p-value': 'How often chance alone would give a gap at least this big if H0 were true.',
'significance level': 'Alpha: the p-value below which you reject H0, chosen before the test, often 0.05.',
'statistical significance': 'The p-value is below the significance level, so chance alone is an unlikely explanation.',
'practical significance': 'The effect is big enough to matter for the decision. Judge it with the effect size.',
'false negative': 'Missing a real difference or a real case (Type II error).',
'multiple comparisons problem': 'The more tests you run, the more likely one gives a false positive by chance.',
'optional stopping': 'Peeking at results and stopping when they look good. It raises false positives.',
'p-hacking': 'Trying tests or stopping points until a p-value falls under the line.',
'line items': 'The lines of an order, one record per product on the order (the order_lines table).',
'many-to-one merge': 'A merge where many left records match one lookup record. pandas checks it with validate="m:1".',
'inner join, left join, right join, full outer join': 'Merge types. Inner keeps matches only, left keeps every left record, right keeps every right record, full outer keeps all.',
'ratio': 'One quantity divided by another, such as returns per order.',
'percentage': 'A part divided by the whole, times 100.',
'decomposition': 'Splitting a time series into trend, seasonality and noise.',
'fitted line': 'The line a linear regression model draws through the points on a scatter plot.',
'scatter plot': 'A chart with one dot per record, one variable on each axis.',
'residuals': 'Actual value minus predicted value for each record.',
'error': 'The gap between a prediction and the actual value for one record.',
'ordinary least squares': 'The way of fitting a line that makes the sum of squared residuals as small as possible.',
'adjusted r squared': 'R squared corrected for the number of predictors, so extra useless predictors do not raise it.',
'dummy variable trap': 'Keeping every level of an indicator variable makes the columns add to one. Drop one level to avoid it.',
'homoscedasticity': 'The residuals have about the same spread at every predicted value.',
'residual plot': 'A chart of residuals against predicted values. A fair model shows an even cloud with no pattern.',
'parameters': 'The numbers a model learns from the data, such as coefficients.',
'hyperparameters': 'Settings you choose before training, such as max_depth.',
'validation set': 'Records held out to compare models and settings before the final test.',
'true positive, false positive, true negative, false negative': 'The four cells of a confusion matrix: right yes, wrong yes, right no, wrong no.',
'f1 score': 'One number that combines precision and recall.',
'accuracy': 'The share of all predictions that are right. It misleads when one class is rare.',
'precision-recall curve': 'Precision against recall as the decision threshold moves. Useful when the positive class is rare.',
'sigmoid (logistic) function': 'The S-shaped curve that turns any score into a probability between 0 and 1.',
'root node, internal node, leaf node, split': 'The parts of a decision tree: the first question, later questions, the final answers, and the rule that sends records left or right.',
'bagging': 'Bootstrap aggregation: train many models on bootstrap samples and combine their votes.',
'bias-variance trade-off': 'A model that is too simple misses the pattern (bias). One that is too flexible follows noise (variance).',
'generalisation': 'How well a model works on records it has not seen.',
'k-fold cross-validation': 'Split the training records into k folds, train on k minus 1, score on the held-out fold, and repeat k times.',
'stratified k-fold': 'K-fold in which every fold keeps the same share of each class.',
'hyperparameter tuning': 'Trying settings and choosing the best by cross-validation.',
'grid search': 'Tuning that tries every combination from a list of settings (GridSearchCV).',
'clusters': 'Groups of similar records found by k-means or another clustering method.',
'customer segments': 'Clusters of customers described in business words.',
'elbow method': 'Plot inertia for several k and choose the k where the drop flattens.',
'inertia': 'The sum of squared distances from each record to its cluster centre. Lower means tighter clusters.',
'dimensionality reduction': 'Mixing many variables into a few that keep most of the information.',
'principal components': 'The new variables that PCA builds, ordered by how much variance they keep.',
'standardisation': 'Rescaling a variable to mean 0 and standard deviation 1 (z-score).',
'min-max scaling': 'Rescaling a variable to run from 0 to 1.',
'perceptron / artificial neuron': 'A weighted sum of inputs plus a bias, passed through an activation function.',
'bias': 'The constant a neuron adds to its weighted sum. It is the neuron\'s intercept.',
'input layer, hidden layers, output layer': 'The layers of a neural network: where the data enter, the middle layers, and where the prediction leaves.',
'training by gradient descent': 'Repeated small corrections to the weights that lower the loss function, using backpropagation to find each correction.',
'loss function': 'A number that says how wrong the model is. Training tries to lower it.',
'learning rate': 'How big each correction step is in gradient descent.',
'epoch': 'One full pass through the training records.',
'batch': 'A group of training records used for one correction step.',
'inference': 'Using a trained model to predict for new records.',
'walk-forward validation': 'Train on the past, test on the next period, then move the window forward and repeat.',
'naive baseline': 'The simplest forecast, such as repeating last year. A model must beat it.',
'forecast horizon': 'How far ahead the forecast looks, such as one month.',
'regular expression': 'A pattern that finds text, such as every phone number in a message.',
'chunk': 'A piece of a document, small enough to search and to fit in a prompt.',
'chunking': 'Cutting documents into chunks before they are searched.',
'audit log': 'A record of what the assistant was asked and what it answered, kept so people can check.',
'deploy': 'Put the app on the internet so other people can use it.',
'deployment': 'The act of putting a model or app where users can reach it.',
'seed': 'The starting number of a random generator. Fixing it gives the same result every run.',
'versions': 'The numbers of the libraries you used. Record them so others can rebuild your work.',
'requirements file': 'A text file (requirements.txt) listing the libraries and versions the project needs.',
'git repository': 'A project folder with its full history of changes.',
'commit': 'A saved snapshot of the project with a short message.',
'branch': 'A separate line of work in a repository.',
'push': 'Send your commits to the copy on GitHub.',
'github': 'A website that hosts Git repositories.',
'model card': 'A one-page note that says what a model is for, what data it used, how well it works and where it fails.',
'concept drift': 'The relationship between the inputs and the outcome changes over time.',
}


def meaning_for(o, wmap):
    n = o['name'].lower()
    if n.startswith('record'):
        return 'One row of a table: one thing the table describes, such as one till order.'
    if n == 'granularity':
        return 'The level of detail of the table: one row per order, per order line or per branch per week.'
    if o['meaning'] and not o['sibs']:
        return o['meaning']
    if n in OV:
        return OV[n]
    w = wmap.get(n)
    if w:
        return w[0]
    if o['meaning']:
        return o['meaning'] + ' (Taught together with: ' + ', '.join(o['sibs']) + '.)'
    c = re.sub(r'\s*\((as the main word|when you mean .*?|as the only names|drawing)\)', '', o['col1'])
    return f'The proper name for the everyday phrase: {c}.' if c else ''


# ------------------------------------------------------------------ Facilitator Guide
def guide():
    d = new_doc2('Facilitator Guide')
    title(d, 'Facilitator Guide', f'{COURSE} (KLAi edition)  |  24 sessions of 2 hours  |  Keep it private')
    h2(d, 'What is in this guide', 0)
    grid(d, [['1', 'The course plan: modules, project milestones, the 24-session map and the session clock'],
             ['2', 'How to run a concepts-then-lab session'],
             ['3', 'The free tools, the datasets and the setup you need as tutor (Colab, Sheets, GitHub, Streamlit)'],
             ['4', 'Open items before teaching: what has not been verified yet'],
             ['5', 'Session pages 1 to 24: question, outcomes, slide map, facilitator notes, lab answer key and the deliverable']],
         [1.2, 16.2], size=9.5)

    h2(d, '1  The course plan')
    para(d, 'Working professionals in Uganda and East Africa, confident in Excel, with no code and no statistics, take 24 sessions of two hours (48 hours). They start in Google Sheets, move to Python, SQL and machine learning in Google Colab, and finish by shipping a small model and presenting a course project. You are the tutor. You teach live and read the slide notes aloud in your own voice. Every tool is free for you and for the learners.', 10, after=4)
    h2(d, 'The six modules', 4)
    desc = {'A': 'Sheets and reasoning. No code.', 'B': 'Python, pandas and the first cleaning.', 'C': 'SQL, charts, inference and regression.', 'D': 'Build, test and judge machine learning models.',
            'E': 'Neural networks, text, embeddings and language models.', 'F': 'Save a model, publish a small app, govern it and present.'}
    rows = [[mod_name(blk), f'{ss[0]["num"]} to {ss[-1]["num"]}', desc[blk.split()[1].rstrip(':')]] for blk, ss in modules().items()]
    grid(d, rows, [5.6, 2.2, 9.6], header=['Module', 'Sessions', 'What happens'], size=9.5, label_cols=(0,))
    h2(d, 'Project milestones and the course project')
    grid(d, [[str(k), v] for k, v in MILESTONES.items()], [1.6, 15.8], header=['Session', 'Practical work'], size=9.5)
    para(d, 'Nothing in this course is marked: no exams, marks, grades, pass marks, weights or scored rubrics (lecturer decision, 4 November 2026). Learners build practical projects and keep them. You review each project milestone with the learner for feedback and never score it. The check cells (OK or NOT YET), the recall questions and the exit-check questions are self-checks that nobody marks. A learner who completes the course project receives a certificate of completion from KLAi Professional Learning, with no other criteria.', 10, before=3, after=4)

    h2(d, 'The 24-session map')
    para(d, 'Each row gives the session, the question it answers and what the learner keeps from the lab.', 10, after=3)
    for blk, ss in modules().items():
        h2(d, blk, 4, 2)
        rows = []
        for s in ss:
            n = s['num']
            first = f'{s["short_title"]}\n~{s["question"]}'
            if n in MILESTONES:
                first += f'\n{MILESTONES[n]}'
            rows.append([str(n), first, s['keep']])
        grid(d, rows, [1.0, 8.6, 7.8], header=['No', 'Session and question', 'What the learner keeps'], size=8.5, label_cols=(0,))
    h2(d, 'The session clock')
    para(d, 'Every session has the same 120 minutes. The name of the lab block changes by session (see each session page).', 10, after=3)
    grid(d, clock_rows(SESS[4]), [2.0, 2.0, 13.4], header=['Starts', 'Minutes', 'What happens'], size=9.5)

    h2(d, '2  How to run a concepts-then-lab session')
    para(d, 'Each deck has two halves. The concepts half has no laptops open: pictures, plain words and one example by hand. A black slide titled Part 2 marks the switch. After it come a few lab slides, and then the learners work for 45 minutes in the notebook or the Google Sheet. You switch from slides to the notebook once.', 10, after=4)
    grid(d, [['Opening slides\n(10 min)', 'Cover, outcomes, the plan, three recall questions and then their answers, and the five words of the day. Ask the three questions aloud and let learners answer before you show the answers.'],
             ['Concepts\n(45 min)', 'Laptops closed. Read each slide note aloud in your own voice. Say the industry term first and then the plain words beside it. Where code appears it is a recipe that you read aloud. Use the probes on the session page to check understanding, and stop for questions on every figure.'],
             ['Break\n(10 min)', 'Tell learners to open the notebook or the sheet after the break and to leave it alone until you say go.'],
             ['The switch', 'Show the Part 2 slide. It says: Close the slides. Open the notebook (or the sheet). Walk through the lab map, the check-your-numbers table and the error cards, then stop sharing the slides.'],
             ['Lab\n(45 min)', 'Learners work alone or in pairs. Each step has four moves: PREDICT (write a guess before you run), RUN, READ (say what the output means) and CHANGE (alter one thing and see what happens). Walk the room using the Walking the lab table of the session page. The checks print OK or NOT YET and the notebook ends with how many checks pass.'],
             ['Exit check, keep and next\n(10 min)', 'Three exit questions with short answers, then what the learner keeps and what comes next. Ask learners to save the notebook to their own Google Drive before they leave.']],
         [3.6, 13.8], header=['Phase', 'What you do'], size=9)
    h2(d, 'Rules the whole course follows')
    bullets(d, [('Industry term first.', 'Name the real term (record, observation, residual, confounder) and explain it in plain words next to it. See TERMS.md. Excel stays the anchor: say the Excel word first and the industry term right after it.'),
                ('Numbers.', 'Every number on a slide was computed from the data. Made-up teaching numbers are labelled illustrative or hypothetical.'),
                ('Fictional data.', 'Lakeside Mart, Nile Microfinance, District Clinics and the Lakeside feedback messages are fictional and generated. Never ask learners to put real customer or patient data into a notebook or an assistant.'),
                ('Closed AI products.', 'ChatGPT, Gemini, Claude and similar products are built on large language models whose internals are not published. Say what published research describes (transformers, next-token prediction, retrieval) and what open models publish. If a learner asks about a closed product, say: my understanding is that the maker has not published that.'),
                ('Reading aloud.', 'The notes are written to be read as they stand. Change any wording that does not sound like you, then keep the slide and the note in agreement.')], 10)

    h2(d, '3  Tools, datasets and setup')
    para(d, 'Everything is free. No learner needs a paid account, a paid service, an API key, a GPU or an installation. Limits and menus change, so check the current terms before each module that depends on them.', 10, after=4)
    tools = [['Google Colab', 'Run Python notebooks in the browser. Needs a free Google account.', 'Free tier. Google does not publish exact limits. At the time of writing reports give an idle disconnect of about 90 minutes and a longest session of about 12 hours. Check current limits. Save to Drive.'],
             ['Google Sheets (or Excel, or LibreOffice Calc)', 'Sessions 1 to 4, 24 and every Excel comparison.', 'Free. Any spreadsheet works. Session 2 uses UNIQUE. My understanding is that older Excel versions lack it, so use Google Sheets or a current Excel.'],
             ['Python with pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib, seaborn', 'The data science stack.', 'Free and open source. Preinstalled in Colab at the time of writing. Check versions.'],
             ['SQLite (inside Python)', 'SQL practice with no server (Session 10).', 'Free, public domain. Colab had SQLite 3.37 at the time of writing, which has no RIGHT JOIN or FULL OUTER JOIN.'],
             ['Git and GitHub', 'Save work, share a portfolio, host the app (Sessions 23 and 24).', 'Free account. Public repositories for the course. Check current terms.'],
             ['Streamlit Community Cloud', 'Publish a small model app (Session 23).', 'Free for public apps at the time of writing. Apps may sleep when nobody visits. Check current limits.'],
             ['TensorFlow Playground', 'See a neural network learn (Session 20).', 'Free web page. No login.'],
             ['sentence-transformers all-MiniLM-L6-v2', 'Turn text into vectors (Sessions 21 and 22).', 'Runs inside Colab. A download at the first run. No API key. Check the model card for the licence and size.'],
             ['A small open language model run in Colab', 'Show how a language model answers (Session 22).', 'Optional. Confirm the licence on the model card before class. The session works with retrieval alone.']]
    grid(d, tools, [4.3, 5.0, 8.1], header=['Tool', 'Use', 'Cost and terms'], size=8.5, label_cols=(0,))
    h2(d, 'The datasets')
    ds = [['Lakeside Mart', 'Eight mini-markets in Uganda: 8 branches, 150 products, 2,500 loyalty customers, 30,229 till orders and 98,066 order lines (a 5 percent sample), returns, weekly branch summaries, an offer test, 800 feedback messages, eight policy documents and a raw export with seeded defects.', 'Sessions 1 to 13, 18, 21, 22'],
          ['lakeside_for_sheets.xlsx', 'A 2,000-order sample with 6,590 order lines for Google Sheets. Tabs: orders, order_lines, branches, products, customers, branch_weeks, READ ME.', 'Sessions 1 to 4'],
          ['Nile Microfinance', '8,000 loans with a default outcome (1,004 defaults), missing values and impossible ages.', 'Sessions 14 to 17, 20, 23, 24'],
          ['District Clinics', 'Twelve districts by 60 months of visits, malaria cases and rainfall (720 rows).', 'Session 19']]
    grid(d, ds, [3.3, 10.3, 3.8], header=['Dataset', 'Contents', 'Used in'], size=8.5, label_cols=(0,))
    para(d, 'The files are in 03 Learner Materials/Practice Files/data. DATA DICTIONARY.txt defines every column. Learner notebooks are in Practice Files/notebooks and your solution notebooks are in 04 Facilitator Materials/Lab Solutions. Keep the solutions and this guide private.', 9.5, before=3, after=4)
    h2(d, 'Setup you do as tutor')
    bullets(d, [('Google Colab.', 'Sign in at colab.research.google.com with a Google account. Choose File, Upload notebook, upload a solution notebook and choose Runtime, Run all. The first cell downloads data.zip from the Google Drive link in DATA_LINK, or asks you to upload data.zip when DATA_LINK is empty. Choose File, Save a copy in Drive when it works.'),
                ('Google Sheets.', 'Upload lakeside_for_sheets.xlsx to Google Drive, open it, and choose File, Save as Google Sheets. Share it so that every learner can make a copy. Work every Sheets task once yourself.'),
                ('GitHub.', 'Create a free account. For Session 23 make one public repository and practise uploading files with Add file, Upload files. Ask learners to create their own free account before Session 23 if they want to publish.'),
                ('Streamlit Community Cloud.', 'Sign in with GitHub, choose New app, then the repository, the branch and the main file (app.py). The repository needs a requirements.txt. Deployment is not part of the 45-minute lab. Learners do it afterwards.'),
                ('Your teaching laptop.', 'Install the Lato fonts from brand/fonts so the slides look right. Open each deck in Presenter View: the spoken script is in the notes. Export a PDF of each deck to share with learners, who revise from the PDF without notes.'),
                ('Learners.', 'Send Start Here before Session 1. Give out Sheets Lab Sheets and the Glossary. Ask in Session 1 who has no Google account.')], 10)

    h2(d, '4  Open items before teaching')
    para(d, 'This section lists what has not been verified. Treat every item as work to do before the session it names. Each one is a number or a menu that was never checked in the real tool.', 10, after=4)
    grid(d, [[f'{i}. {a}', f'{b}\n\n{c}'] for i, (a, b, c) in enumerate(OPEN_ITEMS, 1)], [4.6, 12.8], header=['Item', 'What is unverified, and what to do'], size=8.5, label_cols=(0,))
    para(d, 'Each session page below repeats the open item that applies to it.', 9.5, before=3, after=0)

    for s in SESS:
        n = s['num']
        page_break(d)
        title(d, f'Session {n}: {s["short_title"]}', f'{s["block"]}  |  {s["title"]}')
        para(d, 'The question of the day: ' + s['question'], 10.5, italic=True, after=3)
        if s.get('use_at_work'):
            para(d, 'At work on Monday: ' + s['use_at_work'], 10, after=3)
        if n in MILESTONES:
            para(d, MILESTONES[n] + '.', 10, True, after=3)
        para(d, 'Lab: ' + s['clock'][3][1].replace('Lab: ', '') + '  |  Tool: ' + lab_tool(s), 10, after=3)
        if n in SESSION_OPEN:
            box(d, 'Open item for this session', [SESSION_OPEN[n]])
        h2(d, 'Outcomes', 3)
        bullets(d, s['outcomes'], 10)
        h2(d, 'Slide map')
        grid(d, [[str(i), t, sec] for i, t, sec, _n in slide_rows(s)], [1.1, 13.6, 2.7], header=['Slide', 'Title', 'Section'], size=8, label_cols=(0,))
        f = s['facilitator']
        if f.get('prep'):
            h2(d, 'Before the session')
            bullets(d, f['prep'], 9.5)
        if f.get('misconceptions'):
            h2(d, 'Ideas learners often get wrong')
            grid(d, [[a, b] for a, b in f['misconceptions']], [6.6, 10.8], header=['What a learner may say', 'What to say back'], size=8.5, label_cols=())
        if f.get('probes'):
            h2(d, 'Questions to ask, and a good answer')
            grid(d, [[q, a] for q, a in f['probes']], [6.6, 10.8], header=['Ask', 'A good answer'], size=8.5, label_cols=())
        if f.get('lab_steps'):
            h2(d, 'Walking the lab: what to look for')
            grid(d, [[a, b] for a, b in f['lab_steps']], [4.6, 12.8], header=['Step', 'What to look for'], size=8.5)
        if f.get('rescue'):
            h2(d, 'If things go wrong')
            bullets(d, f['rescue'], 9.5)
        if f.get('after'):
            h2(d, 'After the session')
            bullets(d, f['after'], 9.5)
        if f.get('lab_answer_key'):
            h2(d, 'Lab answer key (the PREDICT, READ and CHANGE prompts)')
            grid(d, [[a, b] for a, b in f['lab_answer_key']], [7.4, 10.0], header=['Prompt', 'Answer'], size=8.5, label_cols=())
        if s.get('sheet_tasks'):
            para(d, f'The {len(s["sheet_tasks"])} Sheets tasks and their answers are in Sheets Lab Answers.', 9.5, before=4, after=2, italic=True)
        h2(d, 'Lab deliverable')
        para(d, s['keep'], 10, after=2)
        para(d, 'Next: ' + s['next'], 9.5, color='404040', before=3, after=0)
    finish(d, FAC / 'Facilitator Guide.docx')


# ------------------------------------------------------------------ Presenter Script
def script():
    d = new_doc2('Presenter Script')
    title(d, 'Presenter Script', 'The spoken script of every slide, in order. The same words are in the notes of each deck. Read them aloud at about 130 words a minute.')
    rows = []
    for s in SESS:
        w, m = notes_minutes(s)
        rows.append([str(s['num']), s['short_title'], str(len(SPECS[s['num']]['slides'])), f'{w:,}', f'{m:.0f}'])
    grid(d, rows, [1.6, 9.0, 2.2, 2.3, 2.3], header=['Session', 'Title', 'Slides', 'Words', 'Minutes'], size=8.5, label_cols=(0,))
    for s in SESS:
        page_break(d)
        h2(d, f'Session {s["num"]}: {s["short_title"]}', 0)
        w, m = notes_minutes(s)
        para(d, f'{len(SPECS[s["num"]]["slides"])} slides, {w:,} words, about {m:.0f} minutes aloud.', 9, color='595959', after=2)
        for i, t, _sec, notes in slide_rows(s):
            para(d, f'Slide {i}. {t}', 9.5, True, before=5, after=1, keep=True)
            for ptxt in notes.split('\n\n'):
                para(d, ptxt, 9.5, after=2)
    finish(d, FAC / 'Presenter Script.docx')


# ------------------------------------------------------------------ Sheets labs
TABS = ['orders', 'order_lines', 'branches', 'products', 'customers', 'branch_weeks']


def tabs_used(s):
    txt = ' '.join(t['task'] for t in s['sheet_tasks'])
    return [t for t in TABS if re.search(r'\b' + t + r'\b', txt)]


def workbook_table():
    import openpyxl
    wb = openpyxl.load_workbook(DATA_DIR / 'lakeside_for_sheets.xlsx', read_only=True)
    rows = []
    for ws in wb:
        head = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        rows.append([ws.title, f'{ws.max_row - 1:,}' if ws.title != 'READ ME' else 'a note', ', '.join(str(h) for h in head)])
    return rows


def sheets(answers):
    name = 'Sheets Lab Answers' if answers else 'Sheets Lab Sheets'
    d = new_doc2(name)
    if answers:
        title(d, 'Sheets Lab Answers', 'For the tutor only. Sessions 1 to 4 and 24: every task with its answer. Keep it private.')
        para(d, 'The answers come from pandas and numpy on lakeside_for_sheets.xlsx. The formulas have not been run in real Google Sheets, so work each task once before you teach it. The Session 4 answers are ranges because RAND changes on every recalculation.', 10, after=4)
    else:
        title(d, 'Sheets Lab Sheets', 'Sessions 1 to 4 and 24. Work through the tasks in the lab half of the session. Write each answer in the space beside the task.')
        para(d, 'Sessions 1 to 4 use the workbook lakeside_for_sheets.xlsx. Upload it to Google Drive, open it, and choose File, Save as Google Sheets (in Excel just open it). Session 24 uses a new Google Sheet that you make yourself. Write formulas exactly as the task shows them, with the tab name, an exclamation mark and the range.', 10, after=4)
    h2(d, 'The workbook: lakeside_for_sheets.xlsx', 4)
    grid(d, workbook_table(), [3.0, 2.4, 12.0], header=['Tab', 'Records', 'Variables'], size=8.5, label_cols=(0,))
    for s in (x for x in SESS if x.get('sheet_tasks')):
        n = s['num']
        page_break(d)
        h2(d, f'Session {n}: {s["short_title"]}', 0)
        if n == 24:
            para(d, 'Data file: none. Work in a new Google Sheet named Presentation plan. The tab names are in the tasks.', 9.5, color='404040', after=3)
        else:
            para(d, 'Data file: lakeside_for_sheets.xlsx. Tabs used: ' + ', '.join(tabs_used(s)) + '. New tabs you create are named in the tasks.', 9.5, color='404040', after=3)
        if n == 1:
            para(d, 'Part one is in Google Sheets. Part two is the Session 1 notebook in Google Colab.', 9.5, color='404040', after=3)
        if answers:
            grid(d, [[str(i), t['task'], t['answer']] for i, t in enumerate(s['sheet_tasks'], 1)], [0.9, 7.6, 8.9], header=['No', 'Task', 'Answer'], size=8.5, label_cols=(0,))
        else:
            grid(d, [[str(i), t['task'], ''] for i, t in enumerate(s['sheet_tasks'], 1)], [0.9, 8.5, 8.0], header=['No', 'Task', 'Your answer'], size=9, label_cols=(0,), min_h=2.6)
    finish(d, (FAC if answers else LEARN) / (name + '.docx'))


# ------------------------------------------------------------------ Learner documents
def start_here():
    d = new_doc2('Start Here')
    title(d, 'Start here', f'{COURSE}  |  KLAi Professional Learning')
    para(d, 'Welcome. This course takes you from the spreadsheet you already know to a tested model that a colleague can open. You do not need to code or to know statistics. You need to be comfortable with Excel or Google Sheets. There are 24 sessions of 2 hours, 48 hours in all, and every tool is free.', 10, after=4)
    h2(d, 'How a session runs')
    grid(d, [['10', 'Recall three questions from last time, and meet the question of the day'], ['45', 'Ideas first: pictures, plain words and one example by hand. Laptops closed.'], ['10', 'Break'],
             ['45', 'Lab: you predict, run, read and change, in a Google Sheet or a Colab notebook'], ['10', 'Exit check, what you keep and what comes next']], [2.0, 15.4], header=['Minutes', 'What happens'], size=9.5)
    para(d, 'The ideas come before the code. After the break a black slide says Close the slides. Open the notebook. From then on you work on your own laptop and your tutor walks round.', 10, before=3, after=4)
    h2(d, 'What to bring')
    bullets(d, ['A laptop (Windows or Mac) with a browser and a charger. A phone is too small for the lab.', 'A free Google account.', 'A notebook and a pen.', 'One question from your own work that you would like data to answer. You use it in Session 1 and again for your course project.'], 10)
    h2(d, 'The free tools')
    bullets(d, [('Google Colab.', 'Runs Python in your browser. Nothing to install.'), ('Google Sheets', '(or Excel). Sessions 1 to 4, Session 24 and every comparison with Python.'),
                ('Python libraries:', 'pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib and seaborn. They are already in Colab.'), ('SQLite', 'for SQL, inside Colab.'),
                ('GitHub and Streamlit Community Cloud', 'to save your work and publish a small app (Sessions 23 and 24).'), ('TensorFlow Playground', 'in your browser, for neural networks (Session 20).')], 10)
    para(d, 'Free plans and their limits change. Your tutor tells you if something has moved. The course data are fictional and generated. Never put real customer or patient data into a notebook, a chat assistant or an app.', 10, before=2, after=4)
    h2(d, 'Set up before Session 1 (about 20 minutes)')
    bullets(d, [('1. A Google account.', 'If you have Gmail you have one. Otherwise make one at accounts.google.com.'),
                ('2. Open Colab once.', 'Go to colab.research.google.com and sign in. Choose New notebook, type print("Hello from Colab") in the first cell and press the play button. Then choose File, Save a copy in Drive.'),
                ('3. The workbook.', 'Your tutor gives you lakeside_for_sheets.xlsx. Upload it to Google Drive, open it and choose File, Save as Google Sheets.'),
                ('4. The data file.', 'Your tutor gives you a Google Drive link to data.zip, or the file itself. Each notebook starts with a setup cell that downloads it from the link (the line DATA_LINK) or asks you to upload it, and unpacks it.')], 10)
    h2(d, 'How the checks work')
    para(d, 'Every notebook has check cells. A check compares your answer with the right one and prints OK or NOT YET. NOT YET means your answer differs. Read the step above it, change your code and run it again. You may try as often as you like. At the end a line tells you how many checks pass. The checks show you that the lab worked. They are not marks, and nobody marks them. There are no exams in this course. You build projects and keep them. In Sessions 1 to 4 and 24 you work in Google Sheets and compare your answers with the check table on the lab slide. Session 1 also has a short notebook with checks.', 10, after=3)
    para(d, 'Each step has the rhythm PREDICT, RUN, READ, CHANGE. Write a guess before you run a cell. Run it. Say what the output means. Then change one thing and see what happens. Before you finish, choose Runtime, Restart session and run all, so that the notebook works from the top.', 10, after=4)
    h2(d, 'How to revise')
    bullets(d, ['Your tutor shares the slides as a PDF. Read it again after class. Every term is defined where it first appears and every picture has a caption, so the slides make sense without the speaker.', 'The Glossary lists every term of the course, with its plain meaning and the session where you meet it.',
                'Words you will meet at work come with the proper industry name first and the plain explanation beside it. Learn the industry name.', 'Your saved notebooks are your own reference. Add a comment wherever you learn something.'], 10)
    h2(d, 'What you keep from each module')
    mod_keep = {'A': 'A Google Sheet with your data dictionary, pivot tables, a simulation and your own business question.',
                'B': 'Notebooks that load, clean and reshape a file, a cleaning log, and a cleaned file you can reuse.',
                'C': 'A SQL query book, an exploration notebook, an inference notebook and a one page regression report.',
                'D': 'A baseline and models for loan default, a customer segment table, and a tested forecast.',
                'E': 'A network result table, a scored feedback file and a small search over documents with a test sheet.',
                'F': 'A folder with your model, requirements and app, a model card, and your course project presentation.'}
    rows = [[mod_name(blk), f'{ss[0]["num"]} to {ss[-1]["num"]}', mod_keep[blk.split()[1].rstrip(':')]] for blk, ss in modules().items()]
    grid(d, rows, [5.4, 2.0, 10.0], header=['Module', 'Sessions', 'You keep'], size=9, label_cols=(0,))
    h2(d, 'How to ask for help')
    bullets(d, ['Colab will not open: try Chrome or Edge and turn off any extension that blocks pages.', 'A cell shows red text: read the last line first. It says what went wrong. Session 5 practises this.',
                'You have no Google account and do not want one: tell your tutor before Session 1.', 'You are stuck in the lab: ask your neighbour for two minutes, then ask your tutor. Write down any question you could not ask and bring it to the next session.', 'You missed a session: read the PDF slides and run the notebook before the next one.'], 10)
    finish(d, LEARN / 'Start Here.docx')


def glossary():
    wmap = {}
    for s in SESS:
        for term, meaning in s['words']:
            keys = {base(term)}
            keys.update(x.strip() for x in re.split(r',| and ', base(term)) if x.strip())
            m = re.search(r'\((.*)\)', term)
            if m:
                keys.update(x.strip().lower() for x in re.split(r',| or ', m.group(1)) if x.strip())
            for k in keys:
                wmap.setdefault(k, (meaning, s['num']))
    d = new_doc2('Glossary')
    title(d, 'Glossary of terms', 'Part 1 lists the words of each session. Part 2 lists the industry terms by area. Learn the industry term. The plain words explain it.')
    h2(d, 'Part 1  The words of the sessions', 4)
    rows = [[term, meaning, str(s['num'])] for s in SESS for term, meaning in s['words']]
    rows.sort(key=lambda r: re.sub(r'[^a-z0-9 ]', '', r[0].lower()))
    grid(d, rows, [4.6, 11.0, 1.8], header=['Term', 'Plain meaning', 'Session'], size=8.5, label_cols=(0,))
    page_break(d)
    h2(d, 'Part 2  Industry terms by area', 0)
    para(d, 'The proper name comes first. Other names for the same thing are in brackets. Where a term is also one of the words of a session, the session number is shown.', 9.5, after=3)
    terms = industry_terms()
    areas = []
    for o in terms:
        if o['area'] not in areas:
            areas.append(o['area'])
    for area in areas:
        h2(d, area, 6, 2)
        rows, seen = [], set()
        for o in sorted((x for x in terms if x['area'] == area), key=lambda x: re.sub(r'[^a-z0-9 ]', '', x['name'].lower())):
            if o['name'].lower() in seen:
                continue
            seen.add(o['name'].lower())
            w = wmap.get(o['name'].lower())
            rows.append([o['label'], meaning_for(o, wmap), str(w[1]) if w else ''])
        grid(d, rows, [5.4, 10.2, 1.8], header=['Term', 'Plain meaning', 'Session'], size=8.5, label_cols=(0,))
    finish(d, LEARN / 'Glossary.docx')


# ------------------------------------------------------------------ Checklist
def checklist():
    d = new_doc2('Playback and Rehearsal Checklist')
    title(d, 'Playback and Rehearsal Checklist', 'A tick list for the tutor, one block per session. Do it once before each session.')
    para(d, 'Part 1: open the deck in Slide Show on the machine you teach from and step through every slide. Check that every picture loads and nothing overlaps. Part 2: read the notes aloud once and time yourself. The estimate is the speaking time of the notes alone at 130 words a minute, before pauses. Part 3: run the lab. Open the solution notebook in Colab and choose Runtime, Run all, or work the Sheets tasks once in Google Sheets.', 10, after=4)
    for s in SESS:
        n = s['num']
        p2 = part2_index(s)
        w, m = notes_minutes(s)
        wc, mc = notes_minutes(s, p2) if p2 else (w, m)
        rows = [['', f'Deck opens in Slide Show and plays from slide 1 to slide {len(SPECS[n]["slides"])}. The Part 2 divider is slide {p2}.'],
                ['', f'Notes read aloud once: about {m:.0f} minutes for the whole deck, of which about {mc:.0f} minutes come before Part 2 (the concepts half has 45 minutes on the clock). Wording changed where it does not sound like you.'],
                ['', 'Slide notes and slide text agree, including the industry term.']]
        if s.get('sheet_tasks'):
            rows.append(['', f'The {len(s["sheet_tasks"])} Sheets tasks done once in ' + ('a new Google Sheet' if n == 24 else 'Google Sheets with lakeside_for_sheets.xlsx') + ' and compared with Sheets Lab Answers.'])
        if n == 1:
            rows.append(['', 'The Session 1 notebook runs top to bottom in Colab.'])
        elif not s.get('sheet_tasks'):
            rows.append(['', 'The solution notebook runs top to bottom in Colab (Runtime, Run all) and the last cell prints All N checks pass. The learner version does not.'])
        if n in SESSION_OPEN:
            rows.append(['', 'Open item: ' + SESSION_OPEN[n]])
        h2(d, f'Session {n}: {s["short_title"]}', 7)
        grid(d, rows, [1.3, 16.1], size=9, label_cols=(), min_h=0.9)
    finish(d, FAC / 'Playback and Rehearsal Checklist.docx')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    LEARN.mkdir(exist_ok=True)
    FAC.mkdir(exist_ok=True)
    if which in ('learner', 'all'):
        start_here()
        glossary()
    if which in ('sheets', 'all'):
        sheets(True)
        sheets(False)
    if which in ('guide', 'all'):
        guide()
    if which in ('script', 'all'):
        script()
    if which in ('checklist', 'all'):
        checklist()
