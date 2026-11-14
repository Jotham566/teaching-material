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
WEEKS = dict(clean='Weeks 3 to 7', charts='Weeks 3 to 8', split='Week 10', regression='Weeks 8 and 9', errors='Week 8', leakage='Weeks 8 to 10',
             warning='Week 9', test='Week 10', results='Weeks 8 to 10')
CHECKED = dict(
    clean='Your function on rows built from the real file with problems added: midnight readings moved to the next day, the all-zero reading dropped, CO2(tCO2) removed, the first copy of a timestamp kept, impossible values and a missing target dropped, month and weekend added, your input unchanged. Each rule earns its own share.',
    charts='Chart 1 and Chart 2 (under any name, or only shown) each have a title, named axes and the unit, and plot the right data. One mark each.',
    split='Your function on other rows, also in a different order: months 1 to 8 training set, 9 and 10 validation set, 11 and 12 test set.',
    regression='Baseline model, linear regression and decision tree (max_depth 4, random_state 17) predictions on other rows with missing values, each in a pipeline with median imputation learned from the training rows.',
    errors='MAE and RMSE on other numbers, including a case with no error.',
    leakage='Two probes: adding extreme feature rows does not change the other predictions (imputation from training rows only), and the baseline predicts the mean of the training targets it is given.',
    warning='Warning probabilities (logistic regression) on other rows (1 mark); the confusion matrix counts, precision and recall at the fixed threshold 0.5 on other cases, one with no predicted warning (2 marks).',
    test='The test set opened once with the supplied cell, after you chose the model, with that model; the supplied cells unedited; no November or December row among your development rows; the test result is the correct one for your model.',
    results='Your validation errors and chosen model on the file, wherever they are (a variable of any name, or printed; typed-in numbers earn nothing) (1); the same answer every time with random_state=17 (1); every required function and the MEMO form exist (1).')
SMALL = 'Written 14 November 2026'


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
        'Online, from anywhere: your own laptop, your own Google account and an internet connection. There is no room and nobody watching. There is no Submit button: your notebook is your own file in Drive, it saves itself, and it is collected automatically at your deadline.',
        f'The rehearsal (unmarked): released {PC.REHEARSAL_TEXT[code]}. Same structure and the same kinds of task, on the same file with a different target. A solved walk-through is not given.',
        'One notebook, one person. Everything is marked automatically. Part A is the coded notebook (30 marks). Part B is the decision memo (15 marks), written as a form inside the notebook.',
        'It covers what we taught in Weeks 1 to 8, with a light warning question from Week 9 and the month split and the sealed test set from Week 10. There is nothing new to learn. No cross-validation, no cost table and no threshold choice.',
        'Every student works on the same real file, so your numbers will match a classmate\'s. Most marks come from checks of your functions on rows you cannot see, and a short online understanding check may follow for anyone.'])
    h2(d, '1. The situation and the two questions', 4)
    para(d, f'You work for the energy manager of a steel plant ({PC.SOURCE["plant"]}). They give you one year of electricity readings: {n["file"]:,} rows, one every 15 minutes for 2018. Each row has the energy used (Usage_kWh, the target variable), the lagging and leading reactive power, two power factors, the seconds since midnight (NSM), the day and a CO2 column. You answer two questions.', 10, after=4)
    grid(d, [['Question 1\nHow much?', f'How much energy will the plant use in a 15-minute reading, in {u}, in months the model has never seen?\nCompare a baseline model, a multiple linear regression model and a decision tree of depth 4, on the same rows, with MAE and RMSE in {u}. The features are the lagging and leading reactive power, NSM and a weekend flag.'],
             ['Question 2\nWarn or not?', f'A reading is a warning (1, the positive class) when its Usage_kWh is at or above {cfg["limit"]:g} {u}, and no warning (0) below it. A quarter hour at or above 60 kWh means at least 240 kW on average, which is when peak-demand charges build up.\nGive each reading a probability with logistic regression, raise a warning when the probability is 0.5 or more (one fixed decision threshold), and report the confusion matrix counts, precision and recall.'],
             ['The client\'s limits', f'A typical prediction error of at most {cfg["max_mae"]:g} {u} (MAE) and a prediction time of at most {P.MAX_MS} ms. A supplied rule in your notebook picks one model with these limits. Both numbers, and the 60 kWh limit, are invented for teaching.']],
         [3.6, W - 3.6], header=['', 'What you must answer'], size=9.5)
    h2(d, '2. The data and the test set')
    bullets(d, [('Where the data comes from.', f'{PC.CITATION} The file is stored inside the supplied setup cell of your notebook and written out with a check, so nothing is uploaded or downloaded.'),
                ('What is really in it.', 'We checked the file before the project. It has no missing cells and no repeated rows. It does have three things you must handle in Task 1: each day\'s last reading is written with that day\'s date and the time 00:00 (it really belongs to midnight at the end of the day); one reading on 7 November has every measurement 0 (the meter recorded nothing); and CO2(tCO2) is calculated from Usage_kWh, so it would leak the answer. The two power factors are calculated from the energy and the reactive power, so they are not used as features either.'),
                ('Split by month.', f'Train on January to August ({n["train"]:,} rows, the training set), validate on September and October ({n["validation"]:,} rows, the validation set). November and December ({n["test"]:,} rows after cleaning) are the test set.'),
                ('Why not a random split?', 'Readings 15 minutes apart are almost the same. A random split would put near-copies of the same hour in the training and validation sets, and let the model learn from days after the ones it is tested on. The score would look better than it will be next month. Splitting by month keeps the future in the future.'),
                ('Fit on the training rows only.', 'The median used to fill a missing value and the mean of the baseline model are learned from the training rows, then applied to the other rows. A pipeline does this for you.')], 10)
    box(d, 'How the test set is opened once', [
        'The supplied cell "Open the test set" is in your notebook. Do not edit it. It defines open_test_set(model_name).',
        'Near the end you call it ONE time: test_result = open_test_set(chosen_model), after the supplied rule has chosen the model on the validation set. It cleans the whole file with your clean_rows, refits your functions on January to October, evaluates on November and December (warnings at 0.5) and prints the result.',
        'The notebook counts how often you call it. A second call loses part of the test set marks, even with the same model, and prints a warning that stays in your notebook. A second call with a different model loses more.',
        'Never use November or December to choose a model or a hyperparameter. Once you have looked at them and then changed your mind, they can no longer tell you how the model behaves on new months.'])
    h2(d, '3. How the window works')
    numbered(d, [('Before you start.', 'Use a charged laptop, your own Google account and a working internet connection, somewhere quiet. Do the rehearsal first. Open the entry link or scan the QR code your lecturer shared. Check the course and the title "Engineering ML project".'),
                 ('Start.', 'Type your registration number. The page checks it against your course list as you type and shows your name: tick This is me. Enter the Google email you will use in Colab, then press Start. Your three hours begin at that moment. Opening the page alone does not start the clock. A registration number from another course is refused: use your own course link.'),
                 ('Your notebook.', 'Press Open my project in Colab. It is your own notebook in Drive and it saves itself; do not use Save a copy. Run the first code cell (your details and the countdown), then the supplied setup cell. Work from the top. Save often with File, then Save.'),
                 ('The deadline.', f'Your deadline is the earlier of three hours after you started and the window\'s close ({w["closes"]}). The clock cannot be paused. Refreshing, a new device or an internet interruption does not restart it. If you start after {w["last_full_start"]}, you only have the time left until the close.'),
                 ('The end.', 'At your deadline your notebook becomes read only and your work is collected automatically. The deadline is kept on the server, so nothing typed in the notebook changes it. Work done in a copy after the deadline is not marked.'),
                 ('Help.', f'The lecturer answers questions about wording and technical problems on the class channel, {PC.SUPPORT_HOURS}. The lecturer does not write or debug your answers.'),
                 ('If something fails.', 'Report it at once on the class channel with a screenshot. The lecturer can give one fresh attempt (also after a wrong Google account); it still ends at the window\'s close. Do not make a second identity and do not use another student\'s file. If Colab disconnects or your laptop dies, open the entry page again and click Resume: your work up to the last save or the last automatic backup is safe, and the timer continues.')], 10)
    rows = [[name, f'{m} min'] for name, m in PC.TIME_PLAN] + [['Total', f'{PC.MINUTES} min']]
    grid(d, rows, [W - 3.0, 3.0], header=['Suggested time plan', 'Time'], size=9)
    h2(d, '4. What you hand in, exactly')
    grid(d, [['One notebook', 'Your issued notebook, with Tasks 1 to 6 done and the Part B memo form (Task 7) filled in. Restarted and run from the top, then checked with Check my notebook.'],
             ['How', 'Nothing to press. Your notebook is a file in Drive shared with your Google account; Colab saves it as you work (press Ctrl+S now and then; the countdown reminds you at 30 and 10 minutes). The setup cell also sends a backup to the lecturer every 5 minutes. At your deadline your editing stops and your work is collected: the last version saved before the deadline, or the newest backup if that is newer. Finished early? Press I have finished on the entry page.'],
             ['Check my work', 'On the entry page. It runs your saved notebook from the top on the lecturer\'s computer and tells you whether it runs, whether every required function and the MEMO form are there, and whether it is the notebook issued to you. It never shows a mark. Nothing else is handed in: no form, ZIP, CSV, PDF or screenshot.']],
         [3.2, W - 3.2], header=['Item', 'Detail'], size=9.5)
    h2(d, '5. Allowed tools and the AI rule')
    para(d, 'These are the same rules as Practical Test 1.', 10, after=3)
    bullets(d, [('Permitted:', 'Google Colab, your notebook, Python with pandas, NumPy, matplotlib and scikit-learn as used in class, and your lecture slides, your lab notebooks from Classes 1 to 3, the revision guide, the cheatsheet and your own course notes.'),
                ('No AI or outside help:', 'do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not get answers from another person, collaborate, message or copy someone else\'s work.'),
                ('Understanding check:', 'after the window, any student may be asked, in an online call, to explain their submitted code or make a small change to it, without AI or another person\'s help.'),
                ('Declaration:', 'by working in your issued notebook until your deadline, you confirm that you completed this project yourself without AI assistance or another person\'s help, using only the permitted resources, and that you can explain and change the code you hand in.')], 10)
    para(d, 'The copy checks and the identity checks run on every notebook. The lecturer\'s computer compares notebooks for copying and lists unusual cases for a person to look at. A flag never changes a mark by itself.', 9.5, italic=True, before=2, after=3)
    h2(d, '6. Rules that make your notebook run every time')
    numbered(d, [('Restart and run all.', 'Choose Runtime, then Restart session and run all, before your deadline. Every cell must run from the top without an error, in under five minutes in total and under 30 seconds per cell. With 35,040 rows, look timestamps up in a set: a list is far too slow.'),
                 ('Your own cells are fine.', PC.OWN_CELLS),
                 ('Keep the supplied cells and names.', 'Do not edit the supplied cells (the ones that say Do not edit this cell). Keep each function name, argument order, returned keys and variable name exactly as printed. The test-set cell calls your functions by these names.'),
                 ('Use only the arguments.', 'A function uses the lists it is given (and the constants such as TARGET and FEATURES), never a global table. It is marked on other rows you cannot see.'),
                 ('Train on the training set only.', 'The imputation, the StandardScaler and the baseline model\'s mean are learned from the training rows. Using validation or test rows in them is data leakage and loses marks.'),
                 ('Seeds.', 'Keep random_state=17 for the decision tree. Do not add random choices without a seed, and never use a random split.'),
                 ('Calculate, do not type.', 'Your results come from your code. A number typed in by hand earns nothing in Part A.'),
                 ('No extras.', 'No pip installs, no downloads, no extra files.')], 10)
    h2(d, '7. How Part A is marked (30 marks)')
    para(d, 'The lecturer\'s computer runs your notebook from the top in a locked box that has the same Python and libraries as Colab. The self-check cells and Check my notebook are not marked: they use tiny examples with known answers and show PASS or TODO. The hidden checks run your functions on other rows built from the same plant file and compare the numbers. You cannot see them, so test your functions with your own small examples too. Each item earns the share of its checks that pass, so one wrong task does not cost the others. Because everyone has the same file, your results on the file are worth only 1 mark (inside A9).', 10, after=4)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], WEEKS[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Total', '', '', str(K.PART_A_MAX)])
    grid(d, rows, [4.2, 8.4, 2.8, 2.0], header=['Part A item', 'What is checked', 'Taught in', 'Marks'], size=8.5, label_cols=(0,))
    h2(d, '8. Part B: the decision memo form (15 marks)')
    para(d, f'The memo is for {PC.PAYER}, who is not a data scientist. You write it as a form: a Python dictionary called MEMO in Task 7. Every field is checked automatically, so type your numbers carefully (two decimals are enough, in {u}). The lists of limits and next steps are printed in your notebook; each course has its own lettering.', 10, after=3)
    grid(d, [['recommended_model', 'A model you trained ("baseline", "linear" or "tree"). It must be the model the supplied rule chose and the model you opened the test set with.', '3'],
             ['validation_mae', 'The validation MAE of the three models. Compared with the values your own notebook computed.', '3'],
             ['test_mae, test_recall', 'The MAE and the warning recall on the test set from your one opening. Compared with the value the marking computer calculates from the same predictions.', '2'],
             ['improvement_over_baseline', f'The validation MAE of the baseline minus the validation MAE of your recommended model, in {u}. Compared with your own values.', '1'],
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
                'Practise the whole path in the rehearsal: restart and run all, fill in the MEMO form until every memo self-check passes, and read the self-check output. The rehearsal has short self-study notes before the tasks that need them.'], 10)
    h2(d, 'Before your deadline')
    grid(d, [['☐', 'Identity cell correct (name, email, registration number). COHORT and TEST_ID unchanged.'], ['☐', 'Restart session and run all: no error, every cell ran.'],
             ['☐', 'The test set was opened one time, after the choice. Chart 1 and Chart 2 have a title, named axes and the unit.'], ['☐', 'The MEMO form is complete and the memo self-check passes.'],
             ['☐', 'Worked only in the notebook the entry page opened; Ctrl+S pressed; Check my work on the entry page shows no failing cell.']],
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
    para(d, f'One online window for all three courses: it opens {w["opens"]} and closes {w["closes"]} Kampala time (confirmed 13 November 2026). Each student has 3 hours from pressing Start, capped at the window\'s close, with the same entry page and personal deadline as Practical Test 1. There is no Submit step: the issued notebook is a Drive file the student edits; at the deadline the collector makes it read only and collects the newer of the last save before the deadline and the last on-time automatic backup. Students work from anywhere; there is no room and no invigilation. It is marked entirely by computer. Your manual work is a short spot-check list of flagged cases and, if you choose, online understanding checks. The project follows your blueprint "Weeks 1-8 core" of 14 November 2026: no cross-validation, no cost table, no threshold choice, a light warning question at the fixed threshold 0.5. Marks are final by {PC.RESULTS_BY}.', 10, after=4)
    rows = [[c, f'{w["opens"]} to {w["closes"]}', PC.REHEARSAL_TEXT[c]] for c in PC.CODES]
    grid(d, rows, [2.4, 8.4, 6.6], header=['Course', 'Window (the same for all)', 'Rehearsal released'], size=9, label_cols=(0,))
    h2(d, 'The data')
    para(d, f'Every student has the same real file: {PC.CITATION} {p["n"]["file"]:,} rows, one every 15 minutes for 2018. Checked on 13 November 2026 (SHA-256 {P.DATA_SHA256[:16]}...): no missing cells, no repeated rows. Real problems the students handle: each day\'s last reading is written with that day\'s date at 00:00 (365 rows; their real time is midnight at the end of the day); one reading on 7 November has every measurement 0; CO2(tCO2) and the two power factors are calculated from Usage_kWh, so they would leak the target. No error was invented in the file. The function checks use rows sampled from the file with a small seeded change and with problems added, which the brief says plainly. Split: training January to August ({p["n"]["train"]:,} rows), validation September and October ({p["n"]["validation"]:,}), test November and December ({p["n"]["test"]:,} after cleaning). The file is stored inside the setup cell (bzip2 and base64, about 380 KB) and written out with a SHA-256 check.', 10, after=3)
    vm = p['validation_mae']
    para(d, f'Reference results (the model solution, real scikit-learn): validation MAE baseline {vm["baseline"]:.2f}, linear {vm["linear"]:.2f}, tree {vm["tree"]:.2f} kWh; chosen model {nums["chosen"]} (MAX_MAE {P.EXAM["max_mae"]:g} kWh); improvement over the baseline {p["improvement"]:.2f} kWh; validation warnings at 0.5: precision {p["warning_scores"]["precision"]:.3f}, recall {p["warning_scores"]["recall"]:.3f}; test MAE {nums["test"]["mae"]:.2f} kWh and test recall {nums["test"]["warning"]["recall"]:.3f}. Everyone should reach these same numbers, so the results share is worth 1 mark.', 10, after=4)
    h2(d, '1. How the time limit works (the Test 1 mechanism, reused)')
    bullets(d, [('Server timer.', 'The portal stores the start time when the student presses Start test. The personal deadline is the earlier of start plus the duration_minutes of the Test windows row (180) and the closes_at of that row. It is stored in the Test allocations sheet (columns started_at and personal_deadline), not in the notebook.'),
                ('In the notebook.', 'A countdown cell shows the deadline (a reminder only). The deadline that counts is kept on the server; a deadline typed into the notebook is ignored.'),
                ('At the end.', f'The every-minute trigger makes the file read only at the personal deadline (or at {w["closes"]}) and collects it. A backup that arrives later is kept and never used (LATE_BACKUP_IGNORED). A student who worked in a copy is collected from the newest on-time backup (COLLECTED_FROM_BACKUP, WORKED_IN_OTHER_FILE). These lines are information only.'),
                ('Late start.', f'A student who starts after {w["last_full_start"]} has only the time left until the close. Time lost is not added back. Say this in every reminder.'),
                ('Technical failure.', 'The student reports it at once on the class channel with a screenshot. authoriseFreshTestAttemptForRegistration(registration, reason) in the collector gives one fresh attempt. The new attempt is still capped at the window\'s close.'),
                ('Outage for everyone (portal, Google).', 'Editing closes_at alone does not lengthen a timer that has already started, because personal_deadline is stored. Edit closes_at and then column personal_deadline of each affected allocation row, and tell the class on the channel.')], 9.5)
    h2(d, '2. Timeline')
    grid(d, [['17 and 20 November', 'Send the rehearsal right after Class 3 (CML3112 Tuesday 17; CML3113 and CML3111 Friday 20). Share the entry links and QR codes with it (the page releases nothing before the window opens).'],
             ['By 20 November', 'Run deploy/setup_pipeline.sh (it sets up the repository, the collector, the portal and the gateway; you paste one token and approve one Google screen), load the Class list with loadClassListFromCsv, then one Colab dry run with the rehearsal link: Start, a few saves, Check my work, I have finished.'],
             ['22 November', 'Start Docker Desktop and run the one-notebook grade (grade_project.py --folder ... --cohort ...) to prove Docker works. Run setMlProjectWindow for each course with CONFIRMED (or type the rows from Test_windows_rows.csv with enabled YES), then syncColabExams. Post the window, the support hours and the failure rule on the class channel.'],
             ['23 to 25 November', f'Answer the class channel {PC.SUPPORT_HOURS}. Read the Test Monitor morning and evening. Authorise fresh attempts only for reported failures with a screenshot. On 25 November at 20:00, remind the class that the window closes at 23:59.'],
             ['26 November', 'In the collector project run exportMlProjectBatch() and download the ZIP unchanged. Run final_regrade.py (section 3). Read the spot-check list and actions_vs_final.csv.'],
             ['27 November to 1 December', 'Settle each spot-check line. Hold online understanding checks (section 9) for flagged students and a few chosen at random. Apply overrides with --overrides, rerun, export.'],
             [f'By {PC.RESULTS_BY}', 'Marks are final. Import the two files and run recomputeAll(). Publish.']],
         [3.4, W - 3.4], header=['When', 'What'], size=9, label_cols=(0,))
    h2(d, '3. How to run the grading')
    box(d, 'Exact commands (from the repository root; Docker Desktop running)', [
        '1. In the collector project (IUEA ML Project Submissions): run exportMlProjectBatch(). Download IUEA-ml-project-batch-<date>.zip.',
        '2. python3 IUEA_Teaching_Plan/second_half/Project/actions/final_regrade.py --zip ~/Downloads/IUEA-ml-project-batch-<date>.zip --roster ~/Downloads/Grades.csv',
        '   It runs grade_project.py --zip (all fairness rules), export_for_gradebook.py, and compares every student\'s marks with the instant marks from GitHub Actions (actions_vs_final.csv). The final run\'s marks count.',
        '3. Open grading_output/ML_PROJECT_results.xlsx. Read the Spot-check list sheet first.',
        '4. In the gradebook sheet: importMarkedResults("<Drive id of ML_Project_Part_A_import.csv>", "ML Project Part A"), then the same for Part B and "ML Project Part B", then recomputeAll(). Then releaseMlProjectMarks("RELEASE") in the collector project shows the marks on the entry page.',
        'The fallback without GitHub: grade_project.py --zip <batch> alone gives the same marks. Notebooks collected another way: grade_project.py --folder <folder> --cohort CML3112 (files named <registration>_ML_PROJECT.ipynb).',
        'The command grades a prepared copy of each notebook (own cells count, see section 6) in the Colab-matching sandbox (iuea-notebooks:colab-2026.11) with 30 seconds per cell and 300 seconds per notebook. It stops with a clear message if Docker is not running or the image is missing, and then marks nothing.'])
    para(d, 'Outputs in grading_output/ (keep it private): ML_PROJECT_results.xlsx (Results, Spot-check list, Not graded, Read me), ML_PROJECT_results.csv, ML_PROJECT_spot_check.csv, feedback/<registration>.txt for each student, memos/<registration>.txt (the memo form as typed, with the verdict on each written answer) and similarity_report.csv.', 10, before=3, after=3)
    h2(d, 'Column mapping: grading output to gradebook')
    grid(d, [['ML_PROJECT_results.csv: registration', 'student_id', 'Both import files. Trimmed, upper case: the roster key.', ''],
             ['ML_PROJECT_results.csv: part_a', 'ML Project Part A', f'ML_Project_Part_A_import.csv, column score; maximum {K.PART_A_MAX}', f'/{K.PART_A_MAX}'],
             ['ML_PROJECT_results.csv: part_b', 'ML Project Part B', f'ML_Project_Part_B_import.csv, column score; maximum {K.PART_B_MAX}', f'/{K.PART_B_MAX}'],
             ['status OK or ERRORS', 'status', 'Accepted by importMarkedResults. Anything else (held back) is not exported.', ''],
             ['project_total', '(not imported)', 'The sheet adds Part A and Part B itself and sets Project: marked only when both are filled.', '/45']],
         [4.8, 3.2, 7.4, 2.0], header=['Grading output', 'Gradebook column', 'Import file and rule', 'Out of'], size=8.5, label_cols=(0,))
    para(d, 'The import file is exactly: student_id,status,score,maximum, one row per student, maximum 30 or 15. export_for_gradebook.py checks every rule that importMarkedResults checks (duplicates, roster membership, status, maximum, range, commas) before it writes a file, so an import cannot stop half way. Held-back students (IDENTITY_MISMATCH, grader could not run the notebook) go to ML_Project_held_back.csv instead; release them with --release <registration> after you have looked. Students not on the roster go to ML_Project_not_on_roster.csv. --zeros-for-no-submission gives roster students with no submission 0 and 0 (AUTO_SCORED) once the window is over.', 9.5, before=3, after=3)
    h2(d, '4. During the window')
    numbered(d, [('The channel.', f'Answer wording and technical questions {PC.SUPPORT_HOURS}. Do not debug code or say whether an answer is right. When the same question comes twice, answer it once for everyone.'),
                 ('Failures.', 'Ask for a screenshot. A genuine failure, or a student who typed the wrong Google account: freshMlProjectAttempt(registration, reason, email) in the collector. An outage for a course or everyone: extendMlProject(\'CML3113\' or \'ALL\', minutes, reason); one student: extendMlProject(registration, minutes, reason). A check that did not run: redispatchMlProject().'),
                 ('Monitor.', 'The Attempt state sheet shows each attempt, its last backup and whether it was collected. Contact students with no backup for a long time on the channel.'),
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
        'b1': 'recommended_model is a model the student trained (1), equals the student\'s own rule choice (1), and is the model the test set was opened with (1).',
        'b2': 'validation_mae for baseline, linear and tree each within 0.011 of the student\'s own computed value (1 each).',
        'b3': 'test_mae (1) and test_recall (1) within 0.011 of the value the grader computes by calling the student\'s own functions for the model that was opened (warnings at 0.5).',
        'b4': 'improvement_over_baseline within 0.011 of the student\'s own validation MAE of the baseline minus that of the recommended model.',
        'b5': 'Three different letters; one mark for each of the four true limits chosen (four true and six false statements, lettered differently for each course).',
        'b6': 'The one correct next step of five (collect readings from more years or another plant and check the chosen model again on months it has never seen).',
        'b7': '8 to 80 words and the keyword groups: answer_choice needs a measure word (error, MAE, lowest, better...), an evidence word (validation, baseline, compared, September...) and a number; answer_test_set needs a test-set word (test, November, December...) and a reason word (honest, leak, optimistic, unbiased, tune, choose, unseen...).'}
    grid(d, [[f'{k.upper()} {M_t} ({m})', ex[k]] for (k, M_t, m) in M.PARTB], [4.6, W - 4.6], header=['Part B field', 'Automatic check'], size=8.5, label_cols=(0,))
    para(d, 'Keyword rules cannot judge quality. They accept several correct wordings on purpose (the lists are in grader_spec/memo_spec.py and are tested in run_proofs.py with a differently worded pair). A written answer that is a list of keywords earns the mark and appears on the spot-check list as KEYWORD_STUFFING for you to read.', 9.5, italic=True, before=3, after=3)
    h2(d, '7. A worked example')
    marks = proof_example()
    a = sum(marks[t] for t, _ in K.PARTS)
    b = sum(marks[t] for t, _ in K.PARTB)
    para(d, 'A CML3112 student has written every function correctly except RMSE, which they left without the square root, and filled in the memo form from their own notebook. This is one of the wrong solutions the grader was tested on, so the numbers below are what the grader gives.', 10, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', fmt(marks[t]), str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Part A total', fmt(a), str(K.PART_A_MAX)])
    rows += [[f'Part B {M_t}', fmt(marks[k]), str(m)] for (k, M_t, m) in M.PARTB]
    rows.append(['Part B total', fmt(b), str(K.PART_B_MAX)])
    grid(d, rows, [11.0, 3.2, 3.2], header=['Item', 'Awarded', 'Out of'], size=8.5, label_cols=(0,))
    para(d, f'Why: regression_errors fails the RMSE checks, so item A5 loses marks; the test set result is compared on RMSE too, so item A8 loses some. Part B is full because the memo agrees with the student\'s own notebook (the grader compares with the student\'s own values, so a Part A error does not also cost Part B marks). Project total {fmt(a + b)} of {K.PART_A_MAX + K.PART_B_MAX}, which is {100 * (a + b) / (K.PART_A_MAX + K.PART_B_MAX):.0f} percent of the project.', 10, before=3, after=3)
    h2(d, '8. Common errors and what they cost')
    grid(d, [['The midnight readings left at the start of the day', 'Item A1 loses the date-fix share and the whole-result share: the timestamps are wrong and a later reading can look like a repeat.'],
             ['CO2(tCO2) kept, or a power factor used as a feature', 'Item A1 loses the CO2 share. A power factor added to the features changes every prediction, so items A4, A7 and A8 lose marks.'],
             ['Imputation fitted on all rows', 'Item A4 fails on the linear and tree lists, and item A6 (no leakage) drops.'],
             ['Baseline model built from other targets', 'The baseline list is wrong and item A6 drops. Often a global table used inside the function.'],
             ['Wrong months in the split, or a random split', 'Item A3 scores 0 and the results share of A9 fails, because the validation set is different. A random split also loses the reproducibility share.'],
             ['Looking timestamps up in a list', 'The split cell runs for minutes and stops at 30 seconds; everything after it fails. The brief and the task text warn about this.'],
             ['RMSE without the square root', 'Part of item A5 and of item A8.'],
             ['> instead of >= at the threshold 0.5', 'Part of the counts share of item A7. A probability of exactly 0.5 is a warning.'],
             ['Opening the test set twice', 'Part of item A8 (even with the same model), more with another model; it appears on the spot-check list.'],
             ['No random_state=17 on the tree', 'The reproducibility share of item A9 is lost.'],
             ['Chart without an axis name or unit', 'Part of item A2 is lost.'],
             ['Editing a supplied cell', 'Detected by a hash; item A8 drops and the case is flagged.'],
             ['Results typed in', 'The results share of item A9 earns 0 for those numbers; flagged RESULTS_NOT_CALCULATED.'],
             ['A required function missing or misnamed beyond recognition', 'That function\'s own item, and the "functions and MEMO present" share of item A9.'],
             ['Memo numbers copied wrongly', 'The Part B field loses its mark; flagged MEMO_NUMBERS_DISAGREE. Look for a missing decimal point before overriding.'],
             ['STUDENT_ID blank or someone else\'s', 'IDENTITY_MISMATCH. The allocation and its Drive file say who it was issued to; speak to the student.']],
         [5.4, W - 5.4], header=['Mistake', 'What happens and what to do'], size=9, label_cols=(0,))
    h2(d, '9. Integrity checks')
    bullets(d, ['Everyone has the same file, so the numbers, the chosen model and (within a course) the memo letters are the same for honest students. Numbers alone prove nothing. Look for shared code, shared sentences and shared unusual choices.',
                'grade_project.py compares only what each student wrote, after removing the issued template, and compares the written answers. The tasks are short and guided, so honest notebooks can look alike: talk to a pair only when you can also see the same sentences or the same unusual choices.',
                'Understanding check: the brief says that any student may be asked, after the window, in an online call, to explain their code or make a small change. Suggested questions: why is the midnight reading moved to the next day, why is CO2 removed, why split by month and not at random, why is the median learned from the training rows, why is the test set opened once, what does recall mean for a missed warning.',
                'The hidden checks run on rows built from the file that no student has, so a function copied without understanding still has to work on them.'], 10)
    h2(d, '10. What was proved and what was not')
    n, ok = counts()
    para(d, f'Proved on this Mac in the Colab-matching Docker sandbox (iuea-notebooks:colab-2026.11: Python 3.13.18, numpy 2.4.6, pandas 2.2.3, scikit-learn 1.6.1, matplotlib 3.10.0, IPython 7.34.0, the versions Colab lists on 13 November 2026), through grader_spec/run_proofs.py --docker, the real batch_grade.py and the hidden spec: {ok} of {n} proof cases behave as required, for all three courses. They cover the model solution, a differently written correct solution, the own-cells cases, the Colab habits that broke Test 1 (display and IPython imports, a re-uploaded "(1)" copy, an unnamed chart and a later plt call), leaks, a wrong split, each cleaning rule, a wrong metric, the warning counts at 0.5, edited supplied cells, the test set opened twice or early, a missing function, memo values that disagree with the notebook, copied notebooks, the untouched template, grade_project.py end to end, the gradebook import under the real gradebook.gs, and the patched portal under node, including the notebook exactly as the portal issues it.', 10, after=3)
    para(d, 'The collection and instant marking were proved end to end with no network (actions/test_actions_e2e.py): the real Portal.gs, Gateway.gs, the collector ml_project_pipeline.gs and the Cloudflare worker run on in-memory fakes of Sheets and Drive (permissions and revisions with their modifiedTime). The cases: an ordinary student, one who saved a copy, a laptop that died at minute 170, a student who never pressed anything and one who pressed only Start, a backup after the deadline, a stopped backup thread, the wrong Google account (and its fresh attempt), a wrong-course registration, a whole-course and a one-student extension, I have finished, Check my work and the rehearsal. The marks stay hidden until the release switch and the window close, and final_regrade.py agrees with the instant marks.', 10, after=3)
    para(d, 'Not proved (needs you): a real Colab session (that the background backup can read the notebook on screen from a thread, and that a shared editor file opens without the Copy to Drive banner), the Apps Script deployments, the GitHub repository and its minutes, and the Cloudflare gateway. deploy/setup_pipeline.sh does the set-up; deploy/SETUP_GITHUB_ACTIONS.md says what is left.', 10, after=3)
    h2(d, '11. Open points for you')
    bullets(d, [f'Confirm the support hours on the class channel ({PC.SUPPORT_HOURS.split(" (")[0]}).',
                'A student who starts late loses time (the Test 1 rule). Say so in every reminder.',
                'Two copies of the notebook cannot be told apart by the portal: one registration number gets one attempt.',
                'The secrecy of grader_spec/ (hidden checks, model solutions) is the same as for Tests 1 and 2. If the repository is public, students can read it. Publish without Project/grader_spec/ if you want to avoid that, and grade from a private copy.',
                'The written answers are marked by keyword and length rules, so a vague but keyword-rich answer earns the mark. The spot-check list shows the extreme cases.',
                'Within a course every student sees the same lettering of the limits and next-step lists. Only the lettering between courses differs.',
                'The split inside Part A follows your blueprint: 21 marks for functions on hidden rows (A1, A3, A4, A5, A7), 2 for no leakage, 2 for the charts, 2 for the test set, 3 for results, reproducibility and the required parts.'], 10)
    save_pdf(d, OUT / 'Lecturer_Marking_Guide.docx')


if __name__ == '__main__':
    for code in PC.CODES:
        student_brief(code)
    marking_guide()
