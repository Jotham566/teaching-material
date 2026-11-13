"""Build the student briefs and the lecturer marking guide (Word and PDF, KLAi house style). python3 tools/build_project_docs.py

Uses the Word kit in second_half/Build/templates_gen/docx_kit.py (the pattern of kit/make_plan.py). Every number comes from project_content.py
and from proof_results.json (the worked example), so the documents and the grader can never disagree. Run run_proofs.py first.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402
import memo_spec as M  # noqa: E402
import project_numpy_reference as P  # noqa: E402
sys.path.insert(0, str(PC.PROJECT / 'grader_spec'))
import grade_project as GP  # noqa: E402

sys.path.insert(0, str(PC.PLAN / 'second_half/Build/templates_gen'))
from docx_kit import *  # noqa: E402,F401,F403

OUT = PC.PROJECT
W = CONTENT_CM
FONTS = PC.PLAN / 'second_half/Build/brand/fonts'
WEEKS = dict(clean='Weeks 3 to 7', split='Week 10', regression='Weeks 8 and 9', errors='Week 8', warning='Week 9', scores='Week 9', monthcv='Week 10',
             results='Weeks 8 to 10', test='Week 10', sealed='Week 10', leakage='Weeks 8 to 10', repro='Weeks 8 to 10', charts='Weeks 3 to 8')
CHECKED = dict(
    clean='Your function on rows built from the real file with problems added: midnight readings moved to the next day, first copy of a timestamp kept, an empty reading, impossible values and a missing target dropped, CO2(tCO2) removed, a missing feature left as None, your input unchanged.',
    split='Your function on other rows, also in a different order: months 1 to 8 training set, 9 and 10 validation set, 11 and 12 test set.',
    regression='Baseline model, linear regression and decision tree predictions on other rows with missing values, fitted on training rows only, with the median imputation learned from training rows.',
    errors='MAE and RMSE on other numbers, including a case with no error.',
    warning='Warning probabilities (logistic regression) on other rows, for the limit you are given and for another limit.',
    scores='Confusion matrix counts, precision, recall, F1, cost and AUC at four decision thresholds, including one where nothing is flagged.',
    monthcv='Ten month folds, their mean and their spread, on other rows (November and December must be left out).',
    results='Your validation errors, cross-validation, AUC and chosen model on the file, wherever they are in your notebook (a variable of any name, or printed). Numbers typed in by hand earn nothing.',
    test='The test set opened with your chosen model and threshold; the supplied cells unedited; the test result is the correct one for your choice.',
    sealed='The test set opened exactly once, after you chose the model and the threshold, with that choice; no November or December row among your development rows.',
    leakage='Four probes: the imputation, the baseline model, the StandardScaler and the cross-validation by month use only the rows they are given for training (no data leakage).',
    repro='Calling your regression function twice gives the same answer; the decision tree keeps random_state=17; no unseeded randomness; your saved predictions equal a fresh run.',
    charts='Chart 1 and Chart 2 (under any name) each have a title, named axes and the unit, and plot the right data; the required functions and the MEMO form exist.')
SMALL = 'Written 13 November 2026'


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


def numbered(d, items, size=10, after=2):
    for i, it in enumerate(items, 1):
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        add_run(p, f'{i}.  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def new(name, header):
    d = new_doc(name, 'IUEA Machine Learning for Engineers')
    cell = d.sections[0].header.tables[0].rows[0].cells[1]
    for r in cell.paragraphs[0].runs:
        r.text = header
    return d


def soffice():
    for c in (shutil.which('soffice'), '/Applications/LibreOffice.app/Contents/MacOS/soffice', '/opt/homebrew/bin/soffice'):
        if c and Path(c).exists():
            return c
    raise SystemExit('LibreOffice (soffice) is needed to write the PDFs.')


_PROFILE = []


def lato_profile():
    """A private LibreOffice profile with the Lato brand fonts in <profile>/user/fonts, so the PDFs embed Lato (not a substitute)."""
    if not _PROFILE:
        prof = Path(tempfile.mkdtemp(prefix='lo_lato_'))
        fonts = prof / 'user' / 'fonts'
        fonts.mkdir(parents=True)
        for f in FONTS.glob('Lato-*.ttf'):
            shutil.copyfile(f, fonts / f.name)
        _PROFILE.append(prof)
    return _PROFILE[0]


def save_pdf(d, path):
    save(d, path)
    r = subprocess.run([soffice(), f'-env:UserInstallation=file://{lato_profile()}', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)],
                       capture_output=True, text=True, timeout=300)
    pdf = path.with_suffix('.pdf')
    if r.returncode or not pdf.exists():
        raise SystemExit(f'PDF conversion failed for {path.name}: {r.stderr[-400:]}')
    names = pdf_fonts(pdf)
    if not any('Lato' in n for n in names):
        raise SystemExit(f'{pdf.name} does not embed Lato: {sorted(names)}')


def pdf_fonts(pdf):
    """The base font names used in a PDF (pypdf when present, else a byte search)."""
    try:
        from pypdf import PdfReader
        names = set()
        for page in PdfReader(str(pdf)).pages:
            for f in (page.get('/Resources') or {}).get('/Font', {}).values():
                names.add(str(f.get_object().get('/BaseFont')))
        return names
    except ImportError:
        import re
        return set(re.findall(r'/BaseFont\s*/([A-Za-z0-9+_-]+)', pdf.read_bytes().decode('latin-1')))


# ------------------------------------------------------------------------------------------------ the student brief
def student_brief(code):
    c = PC.COHORT[code]
    cfg = P.EXAM
    u = cfg['unit']
    n = PC.numbers()['p']['n']
    w = PC.WINDOW
    d = new(f'{code} Engineering ML project: student brief', 'IUEA Machine Learning for Engineers  |  Student Brief')
    title(d, 'Engineering ML project: energy use at a steel plant', f'{code}  |  {c["name"]}  |  Part A 30 marks + Part B 15 marks = 45 marks, scaled to 40 percent of the course  |  Online, 3 hours, individual work, marked by computer')
    box(d, 'At a glance', [
        f'The window: opens {w["opens"]} and closes {w["closes"]} Kampala time, the same for all three courses. You have 3 hours from the moment you press Start test. Start by {w["last_full_start"]} to get the full 3 hours.',
        'Online, from anywhere: your own laptop, your own Google account and an internet connection. There is no room and nobody watching. You use the same entry page, countdown and Submit test steps as Practical Test 1.',
        f'The rehearsal (unmarked): released {PC.REHEARSAL_TEXT[code]}. Same structure and the same kinds of task, on the same file with a different target. A solved walk-through is not given.',
        'One notebook, one person. Everything is marked automatically. Part A is the coded notebook (30 marks). Part B is the decision memo (15 marks), written as a form inside the notebook.',
        'It covers only what we taught in Weeks 1 to 10 (up to Class 3). There is nothing new to learn.',
        'Every student works on the same real file, so your numbers will match a classmate\'s. Most marks come from checks of your functions on rows you cannot see, and a short online understanding check may follow for anyone.'])
    h2(d, '1. The situation and the two questions', 4)
    para(d, f'You work for the energy manager of a steel plant ({PC.SOURCE["plant"]}). They give you one year of electricity readings: {n["file"]:,} rows, one every 15 minutes for 2018. Each row has the energy used (Usage_kWh, the target variable), the lagging and leading reactive power, two power factors, the seconds since midnight (NSM), the day and a CO2 column. You answer two questions.', 10, after=4)
    grid(d, [['Question 1\nHow much?', f'How much energy will the plant use in a 15-minute reading, in {u}, in months the model has never seen?\nCompare a baseline model, a multiple linear regression model and a decision tree of depth 4, on the same rows, with MAE and RMSE in {u}. The features are the lagging and leading reactive power, NSM and a weekend flag.'],
             ['Question 2\nWarn or not?', f'A reading is a warning (1, the positive class) when its Usage_kWh is at or above {cfg["limit"]:g} {u}, and no warning (0) below it. A quarter hour at or above 60 kWh means at least 240 kW on average, which is when peak-demand charges build up.\nGive each reading a probability with logistic regression, choose a decision threshold, and report the confusion matrix counts, precision, recall, F1, the cost and the ROC AUC. A false negative (a missed warning) costs 5 and a false positive (a false alarm) costs 1 (invented teaching costs).'],
             ['The client\'s limits', f'A typical prediction error of at most {cfg["max_mae"]:g} {u} (MAE) and a prediction time of at most {P.MAX_MS} ms. A supplied rule in your notebook picks one model with these limits. Both numbers, and the 60 kWh limit, are invented for teaching.']],
         [3.6, W - 3.6], header=['', 'What you must answer'], size=9.5)
    h2(d, '2. The data and the test set')
    bullets(d, [('Where the data comes from.', f'{PC.CITATION} The file is stored inside the supplied setup cell of your notebook and written out with a check, so nothing is uploaded or downloaded.'),
                ('What is really in it.', 'We checked the file before the project. It has no missing cells and no repeated rows. It does have three things you must handle in Task 1: each day\'s last reading is written with that day\'s date and the time 00:00 (it really belongs to midnight at the end of the day); one reading on 7 November has every measurement 0 (the meter recorded nothing); and CO2(tCO2) is calculated from Usage_kWh, so it would leak the answer. The two power factors are calculated from the energy and the reactive power, so they are not used as features either.'),
                ('Split by month.', f'Train on January to August ({n["train"]:,} rows, the training set), validate on September and October ({n["validation"]:,} rows, the validation set). November and December ({n["test"]:,} rows after cleaning) are the test set.'),
                ('Why not a random split?', 'Readings 15 minutes apart are almost the same. A random split would put near-copies of the same hour in the training and validation sets, and let the model learn from days after the ones it is tested on. The score would look better than it will be next month. Splitting by month keeps the future in the future.'),
                ('Cross-validation by month.', 'Each month from January to October takes a turn as the unseen month (the idea of GroupKFold, with the month as the group).')], 10)
    box(d, 'How the test set is opened once', [
        'The supplied cell "Open the test set" is in your notebook. Do not edit it. It defines open_test_set(model_name, threshold).',
        'Near the end you call it ONE time: test_result = open_test_set(chosen_model, chosen_threshold), after you have chosen the model and the threshold on the validation set. It cleans the whole file with your clean_rows, trains your functions on January to October, evaluates on November and December and prints the result.',
        'The notebook counts how often you call it. A second call loses the "opened once" mark, even with the same choice. A second call with a different model or threshold also prints a warning that is saved in your notebook and loses the test set marks.',
        'Never use November or December to choose a model, a threshold or a hyperparameter. Once you have looked at them and then changed your mind, they can no longer tell you how the model behaves on new months.'])
    h2(d, '3. How the window works')
    numbered(d, [('Before you start.', 'Use a charged laptop, your own Google account and a working internet connection, somewhere quiet. Do the rehearsal first. Open the entry link or scan the QR code your lecturer shared. Check the course and the title "Engineering ML project".'),
                 ('Start.', 'Enter your full name, your Google email and your Student Registration Number, then press Start test. Your three hours begin at that moment. Opening the page alone does not start the clock. Use the same Google account in Colab and in the form.'),
                 ('Your notebook.', 'Press Open my test in Colab. It is your own private notebook; no copy is needed. Run the first code cell (your details and the countdown), then the supplied setup cell. Work from the top. Save often with File, then Save.'),
                 ('The deadline.', f'Your deadline is the earlier of three hours after you started and the window\'s close ({w["closes"]}). The clock cannot be paused. Refreshing, a new device or an internet interruption does not restart it. If you start after {w["last_full_start"]}, you only have the time left until the close.'),
                 ('The end.', 'At your deadline the Submit test button switches itself off, the lecturer\'s server refuses new snapshots, and a form response after the deadline is kept for review and is not marked. Colab may still let you type; nothing you type after the deadline is marked.'),
                 ('Help.', f'The lecturer answers questions about wording and technical problems on the class channel, {PC.SUPPORT_HOURS}. The lecturer does not write or debug your answers.'),
                 ('If something fails.', 'Report it at once on the class channel with a screenshot (Colab, the entry page or the form). The lecturer can authorise one fresh attempt; it still ends at the window\'s close. Do not make a second identity and do not use another student\'s file. If Colab disconnects, reconnect and run the countdown cell and the setup cell again; your saved notebook is still in Drive and the timer continues.')], 10)
    rows = [[name, f'{m} min'] for name, m in PC.TIME_PLAN] + [['Total', f'{PC.MINUTES} min']]
    grid(d, rows, [W - 3.0, 3.0], header=['Suggested time plan', 'Time'], size=9)
    h2(d, '4. What you hand in, exactly')
    grid(d, [['One notebook', 'Your issued notebook, with Tasks 1 to 7 done and the Part B memo form (Task 8) filled in. Restarted, run from the top, then saved.'],
             ['How', 'The last cell of the notebook. Run it, click Submit test, open the form link, check your name and registration number, and press Submit. Wait for the message that your response was recorded. Allow at least 20 minutes for this step.'],
             ['Nothing else', 'No ZIP, CSV, PDF, Word file, screenshot or separate memo. One submission per person. A new submission before your deadline must be the complete notebook; the latest one on time is marked.']],
         [3.2, W - 3.2], header=['Item', 'Detail'], size=9.5)
    h2(d, '5. Allowed tools and the AI rule')
    para(d, 'These are the same rules as Practical Test 1.', 10, after=3)
    bullets(d, [('Permitted:', 'Google Colab, your notebook, Python with pandas, NumPy, matplotlib and scikit-learn as used in class, the submission form, and your lecture slides, your lab notebooks from Classes 1 to 3, the revision guide, the cheatsheet and your own course notes.'),
                ('No AI or outside help:', 'do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not get answers from another person, collaborate, message or copy someone else\'s work.'),
                ('Understanding check:', 'after the window, any student may be asked, in an online call, to explain their submitted code or make a small change to it, without AI or another person\'s help.'),
                ('Declaration:', 'by submitting, you confirm that you completed this project yourself without AI assistance or another person\'s help, using only the permitted resources, and that you can explain and change the code you submitted.')], 10)
    para(d, 'The copy checks and the identity checks run on every notebook. The lecturer\'s computer compares notebooks for copying and lists unusual cases for a person to look at. A flag never changes a mark by itself.', 9.5, italic=True, before=2, after=3)
    h2(d, '6. Rules that make your notebook run every time')
    numbered(d, [('Restart and run all.', 'Choose Runtime, then Restart session and run all, before you submit. Every cell must run from the top without an error, in under five minutes in total and under 30 seconds per cell. With 35,040 rows, look timestamps up in a set: a list is far too slow.'),
                 ('Your own cells are fine.', PC.OWN_CELLS),
                 ('Keep the supplied cells and names.', 'Do not edit the supplied cells (the ones that say Do not edit this cell). Keep each function name, argument order, returned keys and variable name exactly as printed. The test-set cell calls your functions by these names.'),
                 ('Use only the arguments.', 'A function uses the lists it is given (and the constants such as TARGET and FEATURES), never a global table. It is marked on other rows you cannot see.'),
                 ('Train on the training set only.', 'The imputation, the StandardScaler and the baseline model\'s mean are learned from the training rows. Using validation or test rows in them is data leakage and loses marks.'),
                 ('Seeds.', 'Keep random_state=17 for the decision tree. Do not add random choices without a seed, and never use a random split.'),
                 ('Calculate, do not type.', 'Your results come from your code. A number typed in by hand earns nothing in Part A.'),
                 ('No extras.', 'No pip installs, no downloads, no extra files.')], 10)
    h2(d, '7. How Part A is marked (30 marks)')
    para(d, 'The lecturer\'s computer runs your notebook from the top in a locked box. The self-check cells in your notebook are not marked: they use tiny examples with known answers and show PASS or TODO. The hidden checks run your functions on other rows built from the same plant file and compare the numbers. You cannot see them, so test your functions with your own small examples too. Each item earns the share of its checks that pass, so one wrong task does not cost the others. Because everyone has the same file, your results on the file are worth only 1 mark (A8); the functions are worth 21; six marks are for how you worked (items A10 to A13).', 10, after=4)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], WEEKS[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Total', '', '', '30'])
    grid(d, rows, [4.2, 8.4, 2.8, 2.0], header=['Part A item', 'What is checked', 'Taught in', 'Marks'], size=8.5, label_cols=(0,))
    h2(d, '8. Part B: the decision memo form (15 marks)')
    para(d, f'The memo is for {PC.PAYER}, who is not a data scientist. You write it as a form: a Python dictionary called MEMO in Task 8. Every field is checked automatically, so type your numbers carefully (two decimals are enough, in {u}). The lists of limits and next steps are printed in your notebook; each course has its own lettering.', 10, after=3)
    grid(d, [['recommended_model, recommended_threshold', 'A model you trained ("baseline", "linear" or "tree") and a decision threshold (0.3, 0.5 or 0.7). They must be the choice your rule and cost table made.', '3'],
             ['validation_mae', 'The validation MAE of the three models. Compared with the values your own notebook computed.', '3'],
             ['test_mae, test_recall', 'The MAE and the warning recall on the test set from your one opening. Compared with the value the marking computer calculates from the same predictions.', '2'],
             ['cv_mean_mae', 'The mean MAE of your cross-validation by month. Compared with your own cv_summary.', '1'],
             ['limits', 'Three different letters: the statements that are true limits of this study. Ten statements are listed and six are false. One mark for each true one.', '3'],
             ['next_step', 'One letter: the best next step, from five.', '1'],
             ['answer_choice, answer_test_set', 'Two short written answers of 8 to 80 words each: why you recommend your model (use a validation number and say what you compared it with) and why the test set is opened only once. One mark each. Several correct wordings are accepted; write sentences in your own words.', '2'],
             ['Total', '', '15']],
         [4.6, W - 6.4, 1.8], header=['Field', 'What you enter and how it is checked', 'Marks'], size=9, label_cols=(0,))
    h2(d, '9. Rehearsal, help and results')
    bullets(d, [f'Rehearsal: {PC.REHEARSAL_TEXT[code]}. It predicts the lagging reactive power (kVarh) from the same file, with its own warning. Do it with a timer. It is unmarked.',
                f'Window: {PC.WINDOW_TEXT}.',
                f'Questions about task wording and technical problems: the class channel, {PC.SUPPORT_HOURS}.',
                f'Results: marks are final about a week after the window closes, by {PC.RESULTS_BY}.',
                'Practise the whole path in the rehearsal: restart and run all, fill in the MEMO form until the memo self-check shows 10 of 10, and read the self-check output.'], 10)
    h2(d, 'Before you submit')
    grid(d, [['☐', 'Identity cell correct (name, email, registration number). COHORT and TEST_ID unchanged.'], ['☐', 'Restart session and run all: no error, every cell ran.'],
             ['☐', 'The test set was opened one time, after the choice. Chart 1 and Chart 2 have a title, named axes and the unit.'], ['☐', 'The MEMO form is complete and the memo self-check passes.'],
             ['☐', 'File saved, Submit test clicked, form submitted, confirmation seen before your deadline.']],
         [1.0, W - 1.0], size=9.5, label_cols=())
    para(d, f'Data credit: {PC.CITATION} Introductory paper: {PC.SOURCE["paper"]}.', 8.5, italic=True, before=4, after=2)
    save_pdf(d, OUT / f'Student_Brief_{code}.docx')


# ------------------------------------------------------------------------------------------------ the marking guide
def proof_example():
    data = json.loads((PC.PROJECT / 'grader_spec/proof_results.json').read_text())
    case = [x for x in data['cases'] if x['cohort'] == 'CML3112' and x['case'] == 'wrong_metric_rmse_without_root'][0]
    return case['marks']


def counts():
    data = json.loads((PC.PROJECT / 'grader_spec/proof_results.json').read_text())
    return len(data['cases']), sum(1 for c in data['cases'] if c['ok'])


def fmt(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.')


def marking_guide():
    w = PC.WINDOW
    nums = PC.numbers()
    p = nums['p']
    d = new('Engineering ML project: marking guide', 'IUEA Machine Learning for Engineers  |  Lecturer Marking Guide')
    title(d, 'Engineering ML project: marking guide', f'CML3111, CML3112 and CML3113  |  {SMALL}  |  Part A 30 + Part B 15 = 45 marks, scaled to 40 percent of the course  |  Individual, online, timed, automatic')
    h2(d, 'What this is', 0)
    para(d, f'One online window for all three courses: it opens {w["opens"]} and closes {w["closes"]} Kampala time (confirmed 13 November 2026). Each student has 3 hours from pressing Start test, capped at the window\'s close, with the same entry page, personal deadline and Submit test flow as Practical Test 1. Students work from anywhere; there is no room and no invigilation. It is marked entirely by computer. Your manual work is a short spot-check list of flagged cases and, if you choose, online understanding checks. The project covers Weeks 1 to 10 (up to Class 3). The Week 11 tasks (feature ablation, writing the model-choice rule) are not in it: the rule is a supplied cell. Marks are final by {PC.RESULTS_BY}.', 10, after=4)
    rows = [[c, f'{w["opens"]} to {w["closes"]}', PC.REHEARSAL_TEXT[c]] for c in PC.CODES]
    grid(d, rows, [2.4, 8.4, 6.6], header=['Course', 'Window (the same for all)', 'Rehearsal released'], size=9, label_cols=(0,))
    h2(d, 'The data')
    para(d, f'Every student has the same real file: {PC.CITATION} {p["n"]["file"]:,} rows, one every 15 minutes for 2018. Checked on 13 November 2026 (SHA-256 {P.DATA_SHA256[:16]}...): no missing cells, no repeated rows. Real problems the students handle: each day\'s last reading is written with that day\'s date at 00:00 (365 rows; their real time is midnight at the end of the day); one reading on 7 November has every measurement 0; CO2(tCO2) and the two power factors are calculated from Usage_kWh, so they would leak the target. No error was invented in the file. The function checks use rows sampled from the file with a small seeded change and with problems added, which the brief says plainly. Split: training January to August ({p["n"]["train"]:,} rows), validation September and October ({p["n"]["validation"]:,}), test November and December ({p["n"]["test"]:,} after cleaning). The file is stored inside the setup cell (bzip2 and base64, about 380 KB) and written out with a SHA-256 check.', 10, after=3)
    vm = p['validation_mae']
    para(d, f'Reference results (the model solution, real scikit-learn): validation MAE baseline {vm["baseline"]:.2f}, linear {vm["linear"]:.2f}, tree {vm["tree"]:.2f} kWh; cross-validated MAE {p["cv"]["mean"]:.2f} kWh (spread {p["cv"]["spread"]:.2f}); AUC {p["warning_auc"]:.3f}; chosen threshold {nums["threshold"]} and chosen model {nums["chosen"]} (MAX_MAE {P.EXAM["max_mae"]:g} kWh); test MAE {nums["test"]["mae"]:.2f} kWh and test recall {nums["test"]["warning"]["recall"]:.3f}. Everyone should reach these same numbers, so the results item is worth 1 mark and the function checks 21.', 10, after=4)
    h2(d, '1. How the time limit works (the Test 1 mechanism, reused)')
    bullets(d, [('Server timer.', 'The portal stores the start time when the student presses Start test. The personal deadline is the earlier of start plus the duration_minutes of the Test windows row (180) and the closes_at of that row. It is stored in the Test allocations sheet (columns started_at and personal_deadline), not in the notebook.'),
                ('In the notebook.', 'A countdown cell shows the deadline (a reminder only). The Submit test cell refuses to run after the deadline and switches its button off. The deadline is also written into the last cell.'),
                ('At the end.', f'A form response whose timestamp is after the personal deadline is stored as OUTSIDE_PERSONAL_WINDOW and is never exported for grading. A response after {w["closes"]} is OUTSIDE_WINDOW. The form closes at the window\'s close when syncColabExams runs (every five minutes). Colab cannot be locked remotely, so a student can still type; nothing typed after the deadline reaches the grader.'),
                ('Late start.', f'A student who starts after {w["last_full_start"]} has only the time left until the close. Time lost is not added back. Say this in every reminder.'),
                ('Technical failure.', 'The student reports it at once on the class channel with a screenshot. authoriseFreshTestAttemptForRegistration(registration, reason) in the collector gives one fresh attempt. The new attempt is still capped at the window\'s close.'),
                ('Outage for everyone (portal, Google).', 'Editing closes_at alone does not lengthen a timer that has already started, because personal_deadline is stored. Edit closes_at and then column personal_deadline of each affected allocation row, and tell the class on the channel.')], 9.5)
    h2(d, '2. Timeline')
    grid(d, [['17 and 20 November', 'Send the rehearsal right after Class 3 (CML3112 Tuesday 17; CML3113 and CML3111 Friday 20). Share the entry links and QR codes with it (the page releases nothing before the window opens).'],
             ['By 20 November', 'One full dry run with the rehearsal account: portal, Colab, Submit test, export, grade_project.py, export_for_gradebook.py. Mark that row REHEARSAL afterwards. Check the three Test windows rows and the three forms exist.'],
             ['22 November', 'Start Docker Desktop and run the one-notebook grade (grade_project.py --folder ... --cohort ...) to prove Docker works. Run setMlProjectWindow for each course with CONFIRMED (or type the rows from Test_windows_rows.csv with enabled YES), then syncColabExams. Post the window, the support hours and the failure rule on the class channel.'],
             ['23 to 25 November', f'Answer the class channel {PC.SUPPORT_HOURS}. Read the Test Monitor morning and evening. Authorise fresh attempts only for reported failures with a screenshot. On 25 November at 20:00, remind the class that the window closes at 23:59.'],
             ['26 November', 'Run syncColabExams. Then in the workbook: Export Test ZIP, Export latest submissions. Download the ZIP unchanged. Run grade_project.py (section 3). Read the spot-check list.'],
             ['27 November to 1 December', 'Settle each spot-check line. Hold online understanding checks (section 9) for flagged students and a few chosen at random. Apply overrides with --overrides, rerun, export.'],
             [f'By {PC.RESULTS_BY}', 'Marks are final. Import the two files and run recomputeAll(). Publish.']],
         [3.4, W - 3.4], header=['When', 'What'], size=9, label_cols=(0,))
    h2(d, '3. How to run the grading')
    box(d, 'Exact commands (from the repository root; Docker Desktop running)', [
        '1. In the test collection workbook: Export Test ZIP, Export latest submissions. Wait for COMPLETE. Download IUEA-test-batch-<date>.zip.',
        '2. python3 IUEA_Teaching_Plan/second_half/Project/grader_spec/grade_project.py --zip ~/Downloads/IUEA-test-batch-<date>.zip',
        '3. Open grading_output/ML_PROJECT_results.xlsx. Read the Spot-check list sheet first.',
        '4. python3 IUEA_Teaching_Plan/second_half/Project/tools/export_for_gradebook.py --roster ~/Downloads/Grades.csv',
        '5. In the gradebook sheet: importMarkedResults("<Drive id of ML_Project_Part_A_import.csv>", "ML Project Part A"), then the same for Part B and "ML Project Part B", then recomputeAll().',
        'Do not use Grade_Tests.command: it only knows Tests 1 and 2. Notebooks collected another way: grade_project.py --folder <folder> --cohort CML3112 (files named <registration>_ML_PROJECT.ipynb).',
        'The command grades a prepared copy of each notebook (own cells count, see section 6) with 30 seconds per cell and 300 seconds per notebook. It stops with a clear message if Docker is not running, and then marks nothing.'])
    para(d, 'Outputs in grading_output/ (keep it private): ML_PROJECT_results.xlsx (Results, Spot-check list, Not graded, Read me), ML_PROJECT_results.csv, ML_PROJECT_spot_check.csv, feedback/<registration>.txt for each student, memos/<registration>.txt (the memo form as typed, with the verdict on each written answer) and similarity_report.csv.', 10, before=3, after=3)
    h2(d, 'Column mapping: grading output to gradebook')
    grid(d, [['ML_PROJECT_results.csv: registration', 'student_id', 'Both import files. Trimmed, upper case: the roster key.', ''],
             ['ML_PROJECT_results.csv: part_a', 'ML Project Part A', 'ML_Project_Part_A_import.csv, column score; maximum 30', '/30'],
             ['ML_PROJECT_results.csv: part_b', 'ML Project Part B', 'ML_Project_Part_B_import.csv, column score; maximum 15', '/15'],
             ['status OK or ERRORS', 'status', 'Accepted by importMarkedResults. Anything else (held back) is not exported.', ''],
             ['project_total', '(not imported)', 'The sheet adds Part A and Part B itself and sets Project: marked only when both are filled.', '/45']],
         [4.8, 3.2, 7.4, 2.0], header=['Grading output', 'Gradebook column', 'Import file and rule', 'Out of'], size=8.5, label_cols=(0,))
    para(d, 'The import file is exactly: student_id,status,score,maximum, one row per student, maximum 30 or 15. export_for_gradebook.py checks every rule that importMarkedResults checks (duplicates, roster membership, status, maximum, range, commas) before it writes a file, so an import cannot stop half way. Held-back students (IDENTITY_MISMATCH, grader could not run the notebook) go to ML_Project_held_back.csv instead; release them with --release <registration> after you have looked. Students not on the roster go to ML_Project_not_on_roster.csv. --zeros-for-no-submission gives roster students with no submission 0 and 0 (AUTO_SCORED) once the window is over.', 9.5, before=3, after=3)
    h2(d, '4. During the window')
    numbered(d, [('The channel.', f'Answer wording and technical questions {PC.SUPPORT_HOURS}. Do not debug code or say whether an answer is right. When the same question comes twice, answer it once for everyone.'),
                 ('Failures.', 'Ask for a screenshot. A genuine failure (Colab, the portal, the form): authoriseFreshTestAttemptForRegistration, with the reason written down. A wrong account or a late start: do not extend.'),
                 ('Monitor.', 'Read the Test Monitor morning and evening: In progress, Submitted, Needs attention. Contact students listed under Needs attention on the channel.'),
                 ('The last evening.', 'Remind the class at 20:00 on 25 November that the window closes at 23:59 and that a submission takes up to 20 minutes.')], 9.5)
    h2(d, '5. How to read the spot-check list')
    para(d, 'A flag is a reason to look. It never reduces a mark. The list is sorted by priority (1 first). Settle each line by writing your decision in the last column; if a mark should change, use an overrides file: registration,part,mark,reason (part A or B) and run grade_project.py again with --overrides.', 10, after=3)
    rows = [[f, str(v[0]), v[1], v[2]] for f, v in GP.FLAGS.items()]
    grid(d, rows, [4.8, 1.0, 5.6, 6.0], header=['Flag', 'Pri.', 'What it means', 'What to do'], size=8, label_cols=(0,))
    h2(d, '6. How the marks are earned')
    para(d, 'Own cells count (your rule of 13 November 2026). Before a notebook runs, the grader works on a copy: an issued TODO cell that the student left unedited is left out when the student defined the same function or variable in a cell of their own; a required function found under a near name with the same arguments is marked in full and flagged RENAMED_FUNCTION; results count wherever their values are (a variable of any name, a print, or a cell\'s last value), except numbers typed in and numbers in the memo form; Chart 1 and Chart 2 count under any name. The brief tells students: ' + PC.OWN_CELLS, 9.5, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    grid(d, rows, [4.6, 11.0, 1.8], header=['Part A item', 'Automatic check', 'Marks'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    ex = {
        'b1': 'recommended_model is a model the student trained (1), equals the student\'s own rule choice (1); recommended_threshold equals the student\'s own choice (1).',
        'b2': 'validation_mae for baseline, linear and tree each within 0.011 of the student\'s own computed value (1 each).',
        'b3': 'test_mae (1) and test_recall (1) within 0.011 of the value the grader computes by calling the student\'s own functions for the model and threshold that were opened.',
        'b4': 'cv_mean_mae within 0.011 of the student\'s own cv_summary["mean"].',
        'b5': 'Three different letters; one mark for each of the four true limits chosen (four true and six false statements, lettered differently for each course).',
        'b6': 'The one correct next step of five (collect readings from more years or another plant and check the model again with cross-validation by month).',
        'b7': '8 to 80 words and the keyword groups: answer_choice needs a measure word (error, MAE, lowest, better...), an evidence word (validation, baseline, compared, September...) and a number; answer_test_set needs a test-set word (test, November, December...) and a reason word (honest, leak, optimistic, unbiased, tune, choose, unseen...).'}
    grid(d, [[f'{k.upper()} {M_t} ({m})', ex[k]] for (k, M_t, m) in M.PARTB], [4.6, W - 4.6], header=['Part B field', 'Automatic check'], size=8.5, label_cols=(0,))
    para(d, 'Keyword rules cannot judge quality. They accept several correct wordings on purpose (the lists are in grader_spec/memo_spec.py and are tested in run_proofs.py with a differently worded pair). A written answer that is a list of keywords earns the mark and appears on the spot-check list as KEYWORD_STUFFING for you to read.', 9.5, italic=True, before=3, after=3)
    h2(d, '7. A worked example')
    marks = proof_example()
    a = sum(marks[t] for t, _ in K.PARTS)
    b = sum(marks[t] for t, _ in K.PARTB)
    para(d, 'A CML3112 student has written every function correctly except RMSE, which they left without the square root, and filled in the memo form from their own notebook. This is one of the wrong solutions the grader was tested on, so the numbers below are what the grader gives.', 10, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', fmt(marks[t]), str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Part A total', fmt(a), '30'])
    rows += [[f'Part B {M_t}', fmt(marks[k]), str(m)] for (k, M_t, m) in M.PARTB]
    rows.append(['Part B total', fmt(b), '15'])
    grid(d, rows, [11.0, 3.2, 3.2], header=['Item', 'Awarded', 'Out of'], size=8.5, label_cols=(0,))
    para(d, f'Why: regression_errors fails the RMSE checks, so item A4 loses marks; the test set result is compared on RMSE too, so item A9 loses some. Part B is full because the memo agrees with the student\'s own notebook (the grader compares with the student\'s own values, so a Part A error does not also cost Part B marks). Project total {fmt(a + b)} of 45, which is {100 * (a + b) / 45:.0f} percent of the project.', 10, before=3, after=3)
    h2(d, '8. Common errors and what they cost')
    grid(d, [['The midnight readings left at the start of the day', 'Item A1 loses marks: the timestamps are wrong and a later reading can look like a repeat.'],
             ['CO2(tCO2) kept, or a power factor used as a feature', 'Item A1 loses marks for CO2. A power factor added to the features changes every prediction, so items A3, A5 and A7 lose marks.'],
             ['Imputation or StandardScaler fitted on all rows', 'Items A3 and A5 fail on the linear and tree lists, and the leakage mark drops (probes 1 and 3).'],
             ['Baseline model built from other targets', 'The baseline list is wrong and the leakage mark drops (probe 2). Often a global table used inside the function.'],
             ['Cross-validation that trains on November or December', 'The leakage mark drops (probe 4).'],
             ['Wrong months in the split, or a random split', 'Item A2 scores 0 and the results check fails, because the validation set is different. A random split also loses the reproducibility mark.'],
             ['Looking timestamps up in a list', 'The split cell runs for minutes and stops at 30 seconds; everything after it fails. The brief and the task text warn about this.'],
             ['RMSE without the square root', 'Part of item A4 and of item A9.'],
             ['> instead of >= at the decision threshold', 'Item A6 loses marks at ties. The confusion matrix counts differ.'],
             ['Opening the test set twice', 'The "opened once" mark is lost (even with the same choice). A second call with another choice also loses test set marks and appears on the spot-check list.'],
             ['No random_state=17 on the tree', 'The reproducibility mark is lost.'],
             ['Chart without an axis name or unit', 'Part of the charts mark is lost.'],
             ['Editing a supplied cell', 'Detected by a hash; the test set marks drop and the case is flagged.'],
             ['Results typed in', 'Item A8 earns 0 for those numbers; flagged RESULTS_NOT_CALCULATED.'],
             ['Memo numbers copied wrongly', 'The Part B field loses its mark; flagged MEMO_NUMBERS_DISAGREE. Look for a missing decimal point before overriding.'],
             ['STUDENT_ID blank or someone else\'s', 'IDENTITY_MISMATCH. Use the verified receipt, then speak to the student.']],
         [5.4, W - 5.4], header=['Mistake', 'What happens and what to do'], size=9, label_cols=(0,))
    h2(d, '9. Integrity checks')
    bullets(d, ['Everyone has the same file, so the numbers, the chosen model and (within a course) the memo letters are the same for honest students. Numbers alone prove nothing. Look for shared code, shared sentences and shared unusual choices.',
                'grade_project.py compares only what each student wrote, after removing the issued template, and compares the written answers. The tasks are short and guided, so honest notebooks can look alike: talk to a pair only when you can also see the same sentences or the same unusual choices.',
                'Understanding check: the brief says that any student may be asked, after the window, in an online call, to explain their code or make a small change. Suggested questions: why is the midnight reading moved to the next day, why is CO2 removed, why split by month and not at random, why is the median learned from the training rows, why is the test set opened once, what does recall mean for a missed warning.',
                'The hidden checks run on rows built from the file that no student has, so a function copied without understanding still has to work on them.'], 10)
    h2(d, '10. What was proved and what was not')
    n, ok = counts()
    para(d, f'Proved on this Mac, offline, with real scikit-learn (grader_spec/run_proofs.py, the real batch_grade.py and hidden spec, the Docker container replaced by a local worker): {ok} of {n} proof cases behave as required, for all three courses. They cover the model solution, a differently written correct solution, the four own-cells cases (own cell then an unedited stub, a renamed function, a printed-only result, a chart under its own name), leaks, a wrong split, cleaning mistakes, a wrong metric, edited supplied cells, the test set opened twice or early, memo values that disagree with the notebook, copied notebooks, the untouched template, the grade_project.py command end to end, the gradebook import under the real gradebook.gs, and the patched portal and collector under node, including the notebook exactly as the portal issues it.', 10, after=3)
    para(d, 'Also proved through the real Docker image (iuea-notebooks:2026.09, scikit-learn 1.7.2) with grade_project.py --folder on 13 November 2026: the model solution, the alternative solution and the four own-cells cases earned 45 of 45, and the untouched template 0, at about 5 seconds per notebook. The offline proofs used scikit-learn 1.9.1; both agree with the NumPy reference (the warning-function check allows 0.005 for the solver\'s stopping point).', 10, after=3)
    para(d, 'Not proved (needs you): a real Colab session (open the rehearsal and the model solution, Restart session and run all), the real Google Forms, the Apps Script deployment (PacketsMLProject.gs is about 0.6 MB) and the Cloudflare gateway. The step list is in deploy/DEPLOYMENT_STEPS.md.', 10, after=3)
    h2(d, '11. Open points for you')
    bullets(d, [f'Confirm the support hours on the class channel ({PC.SUPPORT_HOURS.split(" (")[0]}).',
                'A student who starts late loses time (the Test 1 rule). Say so in every reminder.',
                'Two copies of the notebook cannot be told apart by the portal: one registration number gets one attempt.',
                'The secrecy of grader_spec/ (hidden checks, model solutions) is the same as for Tests 1 and 2. If the repository is public, students can read it. Publish without Project/grader_spec/ if you want to avoid that, and grade from a private copy.',
                'The written answers are marked by keyword and length rules, so a vague but keyword-rich answer earns the mark. The spot-check list shows the extreme cases.',
                'Within a course every student sees the same lettering of the limits and next-step lists. Only the lettering between courses differs.',
                'The split inside Part A is 21 marks for functions on hidden rows, 3 for results on the file (results 1, test result 2) and 6 for process.'], 10)
    save_pdf(d, OUT / 'Lecturer_Marking_Guide.docx')


if __name__ == '__main__':
    for code in PC.CODES:
        student_brief(code)
    marking_guide()
