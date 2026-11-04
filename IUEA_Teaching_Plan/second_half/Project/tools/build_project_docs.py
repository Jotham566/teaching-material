"""Build the student briefs and the lecturer marking guide (Word and PDF, KLAi house style). python3 tools/build_project_docs.py

Uses the Word kit in second_half/Build/templates_gen/docx_kit.py (the pattern of kit/make_plan.py). Every number comes from project_content.py
and from proof_results.json (the worked example), so the documents and the grader can never disagree. Run run_proofs.py first.
"""
import json
import subprocess
import sys
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
WEEKS = dict(clean='Weeks 3 to 7', split='Week 10', regression='Weeks 8 and 9', errors='Week 8', warning='Week 9', scores='Week 9', groupcv='Week 10', ablation='Week 11',
             choose='Week 11', results='Weeks 8 to 11', test='Week 11', sealed='Weeks 10 and 11', leakage='Weeks 8 to 10', repro='Weeks 8 to 11', charts='Weeks 3 to 8')
CHECKED = dict(
    clean='Your function on messy data it has not seen: first copy kept, missing target and loads outside 0 to 100 dropped, ambient_c left as a missing value, your input unchanged.',
    split='Your function on other rows, also in a different order: E1 to E4 training set, E5 validation set, E6 test set, no use of the target.',
    regression='Baseline model, linear regression and decision tree predictions on other data with missing values, fitted on training rows only, with the median imputation learned from training rows.',
    errors='MAE and RMSE on other numbers, including a case with no error.',
    warning='Warning probabilities (logistic regression) on other data, for the limit you are given and for another limit.',
    scores='Confusion matrix counts, precision, recall, F1, cost and AUC at four decision thresholds, including one where nothing is flagged.',
    groupcv='Five group folds, their mean and their spread, on other data.',
    ablation='Base error, error with the extra feature, and the improvement, on other data.',
    choose='The selection rule, including ties and the case where nobody qualifies.',
    results='The numbers in your notebook for your data file (validation errors, cross-validation, AUC, ablation, your chosen model) against the correct values. Numbers typed in by hand earn nothing.',
    test='The test set opened with your chosen model and threshold; the supplied cells unedited; the test result is the correct one for your choice.',
    sealed='The test set opened exactly once, after you chose the model and the threshold, with that choice; no test-set row among your development rows.',
    leakage='Four probes: the imputation, the baseline model, the StandardScaler and the group cross-validation use only the rows they are given for training (no data leakage).',
    repro='Calling your regression function twice gives the same answer; the decision tree keeps random_state=17; no unseeded randomness; your saved predictions equal a fresh run.',
    charts='Chart 1 and Chart 2 each have a title, named axes and the unit, and plot the right data; every required variable exists.')
SMALL = 'Written 4 November 2026'


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


def save_pdf(d, path):
    save(d, path)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True)


# ------------------------------------------------------------------------------------------------ the student brief
def student_brief(code):
    c = PC.COHORT[code]
    u = c['unit']
    limit = P.LIMITS[code]
    d = new(f'{code} Engineering ML project: student brief', 'IUEA Machine Learning for Engineers  |  Student Brief')
    title(d, f'Engineering ML project: {c["domain"]}', f'{code}  |  {c["name"]}  |  Part A 30 marks + Part B 15 marks = 45 percent of the course  |  One 3-hour sitting, individual work, marked by computer')
    box(d, 'At a glance', [
        f'The sitting: {PC.SITTING_TEXT[code]}. In Google Colab, with the same entry page, countdown and Submit test steps as Practical Test 1.',
        f'The rehearsal (unmarked): released {PC.REHEARSAL_TEXT[code]}. Same structure and the same kinds of task, on a practice data file. A solved walk-through is not given.',
        'One notebook, one person. Everything is marked automatically, so nobody reads your notebook for marks. Part A is the coded notebook (30 marks). Part B is the decision memo (15 marks), written as a form inside the notebook.',
        'It covers only what we taught in Weeks 1 to 11. There is nothing new to learn.',
        'You get one of three data files (variants A, B and C), chosen for you at random when you start. Your numbers will differ from a classmate\'s.'])
    h2(d, '1. The situation and the two questions', 4)
    para(d, f'You work for {c["payer"]}. They give you one file, engineering_data.csv: 91 rows of invented (synthetic) readings from six pieces of equipment, E1 to E6. Each row has the load in percent, the ambient temperature in degrees Celsius and the {c["domain"]} in {u} (the target variable). Some cells are missing and some rows are repeated or impossible, as in Practical Test 1. You answer two questions.', 10, after=4)
    grid(d, [['Question 1\nHow big?', f'How many {u} of {c["domain"]} will a {c["thing"]} show at a given load and ambient temperature, for a {c["thing"]} that the model has never met?\nCompare a baseline model, a multiple linear regression model and a decision tree of depth 4, on the same rows, with MAE and RMSE in {u}.'],
            ['Question 2\nWarn or not?', f'A row is a warning (1, the positive class) when its {c["domain"]} is at or above {limit:g} {u}, and no warning (0) below it. Which rows should raise a warning?\nGive each row a probability with logistic regression, choose a decision threshold, and report the confusion matrix counts, precision, recall, F1, the cost and the ROC AUC. A false negative (a missed warning) costs 5 and a false positive (a false alarm) costs 1 (invented teaching costs).'],
            ['The client\'s limits', f'A typical prediction error of at most {c["max_mae"]:g} {u} (MAE) and a prediction time of at most {P.MAX_MS} ms. Your notebook turns this into a rule that picks one model. Both numbers are invented for teaching.']],
         [3.6, W - 3.6], header=['', 'What you must answer'], size=9.5)
    h2(d, '2. The data and the test set')
    bullets(d, ['The supplied setup cell in your notebook creates your engineering_data.csv, so you need no upload.',
                ('Develop on E1 to E5.', 'Train on E1 to E4 (the training set), validate on E5 (the validation set), and use group cross-validation. The notebook gives you the E1 to E5 rows as development_records.'),
                ('E6 is the test set.', 'It is a different piece of equipment that no part of your work may use until the very end. It gives one honest estimate for the model you chose.')], 10)
    box(d, 'How the test set is opened once', [
        'The supplied cell "Open the test set" is in your notebook. Do not edit it. It defines open_test_set(model_name, threshold).',
        'Near the end you call it ONE time: test_result = open_test_set(chosen_model, chosen_threshold), after you have chosen the model and the threshold on the validation set. It trains your own functions on all of E1 to E5, evaluates on E6 and prints the result.',
        'The notebook counts how often you call it. A second call loses the "opened once" mark, even with the same choice. A second call with a different model or threshold also prints a warning that is saved in your notebook and loses the test set marks.',
        'Never use E6 to choose a model, a threshold or a hyperparameter. Once you have looked at it and then changed your mind, it can no longer tell you how the model behaves on new equipment.'])
    h2(d, '3. How the sitting works')
    numbered(d, [('Before you start.', 'Bring a charged laptop and your own Google account. Open the entry link or scan the QR code your lecturer shows. Check the course and the title "Engineering ML project". Do not start until your lecturer says so.'),
                 ('Start.', 'Enter your full name, your Google email and your Student Registration Number, then press Start test. Your three hours begin at that moment. Opening the page alone does not start the clock. Use the same Google account in Colab and in the form.'),
                 ('Your notebook.', 'Press Open my test in Colab. It is your own private notebook; no copy is needed. Run the first code cell (your details and the countdown), then the supplied setup cell. Work from the top. Save often with File, then Save.'),
                 ('The deadline.', 'Your deadline is the earlier of three hours after you started and the class closing time. The clock cannot be paused. Refreshing, a new device or an internet interruption does not restart it. A student who starts late has only the time left until the class closing time.'),
                 ('The end.', 'At your deadline the Submit test button switches itself off, the lecturer\'s server refuses new snapshots, and a form response after the deadline is kept for review and is not marked. Colab may still let you type; nothing you type after the deadline is marked.'),
                 ('If something fails.', 'Put your hand up and tell your lecturer at once. Do not make a second identity and do not use another student\'s file. If Colab disconnects, reconnect and run the countdown cell and the setup cell again; your saved notebook is still in Drive and the timer continues.')], 10)
    rows = [[name, f'{m} min'] for name, m in PC.TIME_PLAN] + [['Total', f'{PC.MINUTES} min']]
    grid(d, rows, [W - 3.0, 3.0], header=['Suggested time plan', 'Time'], size=9)
    h2(d, '4. What you hand in, exactly')
    grid(d, [['One notebook', 'Your issued notebook, with Tasks 1 to 9 done (the Part B memo form is Task 9). Restarted, run from the top, then saved.'],
             ['How', 'The last cell of the notebook. Run it, click Submit test, open the form link, check your name and registration number, and press Submit. Wait for the message that your response was recorded. Allow at least 20 minutes for this step.'],
             ['Nothing else', 'No ZIP, CSV, PDF, Word file, screenshot or separate memo. One submission per person. A new submission before your deadline must be the complete notebook; the latest one on time is marked.']],
         [3.2, W - 3.2], header=['Item', 'Detail'], size=9.5)
    h2(d, '5. Allowed tools and the AI rule')
    para(d, 'These are the same rules as Practical Test 1.', 10, after=3)
    bullets(d, [('Permitted:', 'Google Colab, your notebook and its CSV, Python with pandas, NumPy, matplotlib and scikit-learn as used in class, the submission form, and your lecture slides, your lab notebooks from Classes 1 to 4, the revision guide, the cheatsheet and your own course notes.'),
                ('No AI or outside help:', 'do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not get answers from another person, collaborate, message or copy someone else\'s work.'),
                ('Understanding check:', 'you may be asked to explain your submitted code or make a small change to it, without AI or another person\'s help.'),
                ('Declaration:', 'by submitting, you confirm that you completed this project yourself without AI assistance or another person\'s help, using only the permitted resources, and that you can explain and change the code you submitted.')], 10)
    para(d, 'The lecturer\'s computer compares notebooks for copying and lists unusual cases for a person to look at. A flag never changes a mark by itself.', 9.5, italic=True, before=2, after=3)
    h2(d, '6. Rules that make your notebook run every time')
    numbered(d, [('Restart and run all.', 'Choose Runtime, then Restart session and run all, before you submit. Every cell must run from the top without an error, in under three minutes in total and under 30 seconds per cell.'),
                 ('Keep the supplied cells and names.', 'Do not edit the supplied cells (the ones that say Do not edit this cell). Keep each function name, argument order, returned keys and variable name exactly as printed.'),
                 ('Use only the arguments.', 'A function uses the lists it is given, never a global table. It is marked on other data you cannot see.'),
                 ('Train on the training set only.', 'The imputation, the StandardScaler and the baseline model\'s mean are learned from the training rows. Using validation or test rows in them is data leakage and loses marks.'),
                 ('Seeds.', 'Keep random_state=17 for the decision tree. Do not add random choices without a seed.'),
                 ('Calculate, do not type.', 'Your results come from your code. A number typed in by hand earns nothing in Part A.'),
                 ('No extras.', 'No pip installs, no downloads, no extra files.')], 10)
    h2(d, '7. How Part A is marked (30 marks)')
    para(d, 'The lecturer\'s computer runs your notebook from the top in a locked box. The self-check cells in your notebook are not marked: they use tiny examples with known answers and show PASS or TODO. The hidden checks run your functions on other data generated for your course and compare the numbers; they also read your named variables for your own data file. You cannot see them, so test your functions with your own small examples too. Each task earns the share of its checks that pass, so one wrong task does not cost the others. Six of the 30 marks are for how you worked (items A12 to A15).', 10, after=4)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], WEEKS[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Total', '', '', '30'])
    grid(d, rows, [4.2, 8.4, 2.8, 2.0], header=['Part A item', 'What is checked', 'Taught in', 'Marks'], size=8.5, label_cols=(0,))
    h2(d, '8. Part B: the decision memo form (15 marks)')
    para(d, f'The memo is for {c["payer"]}, who is not a data scientist. You write it as a form: a Python dictionary called MEMO in Task 9. Every field is checked automatically, so type your numbers carefully (two decimals are enough, in {u}). The lists of limits and next steps are printed in your notebook; each student sees their own lettering.', 10, after=3)
    grid(d, [['recommended_model, recommended_threshold', 'A model you trained ("baseline", "linear" or "tree") and a decision threshold (0.3, 0.5 or 0.7). They must be the choice your own rule and cost table made.', '3'],
             ['validation_mae', 'The validation MAE of the three models. Compared with the values your own notebook computed.', '3'],
             ['test_mae, test_recall', 'The MAE and the warning recall on the test set from your one opening. Compared with the value the marking computer calculates from the same predictions.', '2'],
             ['cv_mean_mae', 'The mean MAE of your group cross-validation. Compared with your own cv_summary.', '1'],
             ['limits', 'Three different letters: the statements that are true limits of this study. Ten statements are listed and six are false. One mark for each true one.', '3'],
             ['next_step', 'One letter: the best next step, from five.', '1'],
             ['answer_choice, answer_test_set', 'Two short written answers of 8 to 80 words each: why you recommend your model (use a validation number and say what you compared it with) and why the test set is opened only once. One mark each. Several correct wordings are accepted; write sentences in your own words.', '2'],
             ['Total', '', '15']],
         [4.6, W - 6.4, 1.8], header=['Field', 'What you enter and how it is checked', 'Marks'], size=9, label_cols=(0,))
    h2(d, '9. Rehearsal, help and the day')
    bullets(d, [f'Rehearsal: {PC.REHEARSAL_TEXT[code]}. Do it with a timer. It is unmarked. Ask about anything unclear before the sitting.',
                f'Sitting: {PC.SITTING_TEXT[code]}.',
                'Your lecturer answers questions about task wording and about ideas from Classes 1 to 4. Your lecturer does not write or debug your answers.',
                'Practise the whole path in the rehearsal: restart and run all, fill in the MEMO form until the memo self-check shows 10 of 10, and read the self-check output.'], 10)
    h2(d, 'Before you submit')
    grid(d, [['☐', 'Identity cell correct (name, email, registration number). COHORT, TEST_ID and VARIANT unchanged.'], ['☐', 'Restart session and run all: no error, every cell ran.'],
             ['☐', 'The test set was opened one time, after the choice. Chart 1 and Chart 2 have a title, named axes and the unit.'], ['☐', 'The MEMO form is complete and the memo self-check passes.'],
             ['☐', 'File saved, Submit test clicked, form submitted, confirmation seen before your deadline.']],
         [1.0, W - 1.0], size=9.5, label_cols=())
    save_pdf(d, OUT / f'Student_Brief_{code}.docx')


# ------------------------------------------------------------------------------------------------ the marking guide
def proof_example():
    data = json.loads((PC.PROJECT / 'grader_spec/proof_results.json').read_text())
    case = [x for x in data['cases'] if x['cohort'] == 'CML3112' and x['case'] == 'wrong_metric_rmse_without_root'][0]
    return case['marks']


def counts():
    data = json.loads((PC.PROJECT / 'grader_spec/proof_results.json').read_text())
    return len(data['cases']), sum(1 for c in data['cases'] if c['ok'])


def marking_guide():
    d = new('Engineering ML project: marking guide', 'IUEA Machine Learning for Engineers  |  Lecturer Marking Guide')
    title(d, 'Engineering ML project: marking guide', f'CML3111, CML3112 and CML3113  |  {SMALL}  |  Part A 30 + Part B 15 = 45 percent of the course  |  Individual, timed, automatic')
    h2(d, 'What this is', 0)
    para(d, 'One supervised 3-hour sitting in the Week 12 class slot, in Colab, with the same timed entry, personal deadline and Submit test flow as Practical Test 1. It is marked entirely by computer. You mark nothing by hand. Your only manual work is a short spot-check list of flagged cases. The project covers Weeks 1 to 11 only. An unmarked rehearsal is released after Class 4.', 10, after=4)
    rows = [[c, PC.SITTING_TEXT[c], PC.REHEARSAL_TEXT[c]] for c in PC.CODES]
    grid(d, rows, [2.4, 8.4, 6.6], header=['Cohort', 'Sitting (all proposed, lecturer to confirm)', 'Rehearsal released'], size=9, label_cols=(0,))
    h2(d, '1. How the time limit works (the Test 1 mechanism, reused)')
    bullets(d, [('Server timer.', 'The portal stores the start time when the student presses Start test. The personal deadline is the earlier of start plus the duration_minutes of the Test windows row (180) and the closes_at of that row. It is stored in the Test allocations sheet (columns started_at and personal_deadline), not in the notebook.'),
                ('In the notebook.', 'A countdown cell shows the deadline (a reminder only). The Submit test cell refuses to run after the deadline and switches its button off. The deadline is also written into the last cell.'),
                ('At the end.', 'A form response whose timestamp is after the personal deadline is stored as OUTSIDE_PERSONAL_WINDOW and is never exported for grading. A response after the class closing time is OUTSIDE_WINDOW. The form itself closes at the class closing time when syncColabExams runs (every five minutes). Colab cannot be locked remotely, so a student can still type; nothing typed after the deadline reaches the grader.'),
                ('Late start.', 'Someone who starts at 11:20 in an 11:00 to 14:00 slot has until 14:00. Time lost is not added back.'),
                ('Technical failure.', 'authoriseFreshTestAttemptForRegistration(registration, reason) in the collector gives one fresh attempt. The new attempt is still capped at the class closing time.'),
                ('Whole-class delay (power cut).', 'Editing closes_at alone does not lengthen a timer that has already started, because personal_deadline is stored. Edit closes_at and then column personal_deadline of each affected allocation row.')], 9.5)
    h2(d, '2. Timeline: the week before and the week after the sitting')
    grid(d, [['D minus 7 days', 'Rehearsal has been out for a week. Ask who has run it. Check the three Test windows rows exist (enabled NO) and the form for each cohort exists. Share the entry link and QR with the class (the page releases nothing before the window opens).'],
             ['D minus 3 days', 'One full dry run with the rehearsal account: portal, Colab with real scikit-learn, Submit test, export, grade_project.py, export_for_gradebook.py. Mark that row REHEARSAL afterwards. Confirm the times with the class.'],
             ['D minus 1 day', 'Start Docker Desktop and run the one-notebook rehearsal grade (grade_project.py --folder ... --cohort ...) to prove Docker works. Run setMlProjectWindow for each cohort with CONFIRMED (or type the row), then syncColabExams. Charge the laptop. Print this page.'],
             ['D, 30 minutes before', 'Check the room, the Wi-Fi and a spare laptop. Open the Test Monitor tab. Confirm the form for the cohort says it is open.'],
             ['D, the sitting', 'See section 4. Read the Test Monitor every 30 minutes.'],
             ['D, 10 minutes after the end', 'Run syncColabExams. Then in the workbook: Export Test ZIP, Export latest submissions. Download the ZIP unchanged.'],
             ['D plus 0 to 1', 'Run grade_project.py (section 3). Read the spot-check list. Settle each item. Run export_for_gradebook.py. Import the two files and run recomputeAll().'],
             ['D plus 2 to 3', 'Answer student questions. Use the understanding check (section 6) on a few students. Apply overrides with --overrides, rerun, export again.'],
             ['D plus 7 days', 'Marks are final. Publish. Put the semester 1 result through the gradebook (Band stays "Awaiting Faculty bands" until you enter the real bands).']],
         [3.4, W - 3.4], header=['When', 'What'], size=9, label_cols=(0,))
    h2(d, '3. How to run the grading')
    box(d, 'Exact commands (from the repository root; Docker Desktop running)', [
        '1. In the test collection workbook: Export Test ZIP, Export latest submissions. Wait for COMPLETE. Download IUEA-test-batch-<date>.zip.',
        '2. python3 IUEA_Teaching_Plan/second_half/Project/grader_spec/grade_project.py --zip ~/Downloads/IUEA-test-batch-<date>.zip',
        '3. Open grading_output/ML_PROJECT_results.xlsx. Read the Spot-check list sheet first.',
        '4. python3 IUEA_Teaching_Plan/second_half/Project/tools/export_for_gradebook.py --roster ~/Downloads/Grades.csv',
        '5. In the gradebook sheet: importMarkedResults("<Drive id of ML_Project_Part_A_import.csv>", "ML Project Part A"), then the same for Part B and "ML Project Part B", then recomputeAll().',
        'Do not use Grade_Tests.command: it only knows Tests 1 and 2. Notebooks collected another way: grade_project.py --folder <folder> --cohort CML3112 (files named <registration>_ML_PROJECT.ipynb).',
        'The command stops with a clear message if Docker is not running, and then marks nothing.'])
    para(d, 'Outputs in grading_output/ (keep it private): ML_PROJECT_results.xlsx (Results, Spot-check list, Not graded, Read me), ML_PROJECT_results.csv, ML_PROJECT_spot_check.csv, feedback/<registration>.txt for each student, memos/<registration>.txt (the memo form as typed, with the verdict on each written answer) and similarity_report.csv.', 10, before=3, after=3)
    h3 = 'Column mapping: grading output to gradebook'
    h2(d, h3)
    grid(d, [['ML_PROJECT_results.csv: registration', 'student_id', 'Both import files. Trimmed, upper case: the roster key.', ''],
             ['ML_PROJECT_results.csv: part_a', 'ML Project Part A', 'ML_Project_Part_A_import.csv, column score; maximum 30', '/30'],
             ['ML_PROJECT_results.csv: part_b', 'ML Project Part B', 'ML_Project_Part_B_import.csv, column score; maximum 15', '/15'],
             ['status OK or ERRORS', 'status', 'Accepted by importMarkedResults. Anything else (held back) is not exported.', ''],
             ['project_total', '(not imported)', 'The sheet adds Part A and Part B itself and sets Project: marked only when both are filled.', '/45']],
         [4.8, 3.2, 7.4, 2.0], header=['Grading output', 'Gradebook column', 'Import file and rule', 'Out of'], size=8.5, label_cols=(0,))
    para(d, 'The import file is exactly: student_id,status,score,maximum, one row per student, maximum 30 or 15. export_for_gradebook.py checks every rule that importMarkedResults checks (duplicates, roster membership, status, maximum, range, commas) before it writes a file, so an import cannot stop half way. Held-back students (IDENTITY_MISMATCH, VARIANT_MISMATCH, grader could not run the notebook) go to ML_Project_held_back.csv instead; release them with --release <registration> after you have looked. Students not on the roster go to ML_Project_not_on_roster.csv. --zeros-for-no-submission gives roster students with no submission 0 and 0 (AUTO_SCORED) once the sitting is over.', 9.5, before=3, after=3)
    h2(d, '4. What to do on the day')
    numbered(d, [('Before.', 'Arrive 30 minutes early. Check that the window is open (Test Monitor shows Scheduled or Open). Ask for phones away and laptops charged. Remind: own Google account, same account throughout.'),
                 ('Start.', 'Say Start. Students open the entry link, type name, Google email and registration number, press Start test, open Colab. Everyone should start within five minutes. Each gets a notebook with their data variant (A, B or C).'),
                 ('First 15 minutes.', 'Walk the room. The usual problems: a different Google account in Colab (the notebook says so), a wrong registration number (fix in the Test allocations sheet, keep the allocation code), no Connect click.'),
                 ('During.', 'Answer only wording questions and technical problems. Do not debug code. Read the Test Monitor every 30 minutes: In progress, Submitted, Needs attention.'),
                 ('Last 30 minutes.', 'Announce the time. Remind about Restart session and run all, saving, and the form. Submissions take up to 20 minutes.'),
                 ('End.', 'Say Stop at the class closing time. Do not allow a re-run after the deadline. Collect names of students who had a technical failure and write what happened.'),
                 ('Failures.', 'Wrong account or form closed: do not extend. A genuine failure: authoriseFreshTestAttemptForRegistration, with the reason. A failure that affected the room: edit personal_deadline in the allocation rows and closes_at, and write why.')], 9.5)
    h2(d, '5. How to read the spot-check list')
    para(d, 'A flag is a reason to look. It never reduces a mark. The list is sorted by priority (1 first). Settle each line by writing your decision in the last column; if a mark should change, use an overrides file: registration,part,mark,reason (part A or B) and run grade_project.py again with --overrides.', 10, after=3)
    rows = [[f, str(v[0]), v[1], v[2]] for f, v in GP.FLAGS.items()]
    grid(d, rows, [4.8, 1.0, 5.6, 6.0], header=['Flag', 'Pri.', 'What it means', 'What to do'], size=8, label_cols=(0,))
    h2(d, '6. How the marks are earned')
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    grid(d, rows, [4.6, 11.0, 1.8], header=['Part A item', 'Automatic check', 'Marks'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    ex = {
        'b1': 'recommended_model is a model the student trained (1), equals the student\'s own rule choice (1); recommended_threshold equals the student\'s own choice (1).',
        'b2': 'validation_mae for baseline, linear and tree each within 0.011 of the student\'s own computed value (1 each).',
        'b3': 'test_mae (1) and test_recall (1) within 0.011 of the value the grader computes by calling the student\'s own functions for the model and threshold that were opened.',
        'b4': 'cv_mean_mae within 0.011 of the student\'s own cv_summary["mean"].',
        'b5': 'Three different letters; one mark for each of the four true limits chosen (four true and six false statements, lettered differently for each cohort and variant).',
        'b6': 'The one correct next step of five (collect real data from more equipment and validate again).',
        'b7': '8 to 80 words and the keyword groups: answer_choice needs a measure word (error, MAE, lowest, better...), an evidence word (validation, baseline, compared...) and a number; answer_test_set needs a test-set word and a reason word (honest, leak, optimistic, unbiased, tune, choose, unseen...).'}
    grid(d, [[f'{k.upper()} {M_t} ({m})', ex[k]] for (k, M_t, m) in M.PARTB], [4.6, W - 4.6], header=['Part B field', 'Automatic check'], size=8.5, label_cols=(0,))
    para(d, 'Keyword rules cannot judge quality. They accept several correct wordings on purpose (the lists are in grader_spec/memo_spec.py and are tested in run_proofs.py with a differently worded pair). A written answer that is a list of keywords earns the mark and appears on the spot-check list as KEYWORD_STUFFING for you to read.', 9.5, italic=True, before=3, after=3)
    h2(d, '7. A worked example')
    marks = proof_example()
    a = sum(marks[t] for t, _ in K.PARTS)
    b = sum(marks[t] for t, _ in K.PARTB)
    para(d, 'A CML3112 student (variant A) has written every function correctly except RMSE, which they left without the square root, and filled in the memo form from their own notebook. This is one of the wrong solutions the grader was tested on, so the numbers below are what the grader gives.', 10, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', f'{marks[t]:.2f}'.rstrip('0').rstrip('.'), str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Part A total', f'{a:.2f}'.rstrip('0').rstrip('.'), '30'])
    rows += [[f'Part B {M_t}', f'{marks[k]:.2f}'.rstrip('0').rstrip('.'), str(m)] for (k, M_t, m) in M.PARTB]
    rows.append(['Part B total', f'{b:.2f}'.rstrip('0').rstrip('.'), '15'])
    grid(d, rows, [11.0, 3.2, 3.2], header=['Item', 'Awarded', 'Out of'], size=8.5, label_cols=(0,))
    para(d, f'Why: regression_errors fails the RMSE checks, so item A4 loses marks; the test set result is compared on RMSE too, so item A11 loses some. Part B is full because the memo agrees with the student\'s own notebook (the grader compares with the student\'s own values, so a Part A error does not also cost Part B marks). Project total {a + b:.2f} of 45, which is {100 * (a + b) / 45:.0f} percent of the project.', 10, before=3, after=3)
    h2(d, '8. Common errors and what they cost')
    grid(d, [['clean_rows fills ambient_c', 'Item A1 loses marks on every hidden dataset. The brief says missing values stay None and are imputed later from the training rows.'],
             ['Imputation or StandardScaler fitted on all rows', 'Items A3 and A5 fail on the linear and tree lists, and the leakage mark drops (probes 1 and 3).'],
             ['Baseline model built from other targets', 'The baseline list is wrong and the leakage mark drops (probe 2). Often a global table used inside the function.'],
             ['Group cross-validation touches E6', 'The leakage mark drops (probe 4).'],
             ['Wrong groups in the split', 'Item A2 scores 0 and the results check fails, because the validation set is different.'],
             ['RMSE without the square root', 'Part of item A4 and of item A11.'],
             ['> instead of >= at the decision threshold', 'Item A6 loses marks at ties. The confusion matrix counts differ.'],
             ['Opening the test set twice', 'The "opened once" mark is lost (even with the same choice). A second call with another choice also loses test set marks and appears on the spot-check list.'],
             ['Choosing after looking at the test set', 'The order check fails (the call comes before the choice).'],
             ['No random_state=17 on the tree', 'The reproducibility mark is lost.'],
             ['Chart without an axis name or unit', 'Part of the charts mark is lost.'],
             ['Editing a supplied cell', 'Detected by a hash; the test set marks drop and the case is flagged.'],
             ['Results typed in', 'Item A10 earns 0 for those numbers; flagged RESULTS_NOT_CALCULATED.'],
             ['Memo numbers copied wrongly', 'The Part B field loses its mark; flagged MEMO_NUMBERS_DISAGREE. Look for a missing decimal point before overriding.'],
             ['A neighbour\'s list of limit letters', 'Each variant letters the statements differently, so copied letters point at other statements and earn little.'],
             ['STUDENT_ID blank or someone else\'s', 'IDENTITY_MISMATCH. Use the verified receipt, then speak to the student.']],
         [5.4, W - 5.4], header=['Mistake', 'What happens and what to do'], size=9, label_cols=(0,))
    h2(d, '9. Integrity checks')
    bullets(d, ['grade_project.py compares only what each student wrote, after removing the issued template, and compares the written answers. The tasks are short and guided, so honest notebooks can look alike: talk to a pair only when you can also see the same sentences or the same unusual choices.',
                'Understanding check: ask a few students to explain a function or change a decision threshold live, without help. Suggested questions: why is the median learned from the training rows, why is the test set opened once, what does recall mean for a missed warning, why does the baseline model use training targets only.',
                'Three data variants and different lettering of the lists mean a classmate\'s numbers and letters do not fit your data. The hidden checks run on data no student has.'], 10)
    h2(d, '10. What was proved and what was not')
    n, ok = counts()
    para(d, f'Proved offline with the NumPy stand-in for scikit-learn (grader_spec/run_proofs.py): {ok} of {n} proof cases behave as required. They cover a model solution for each variant, a differently written correct solution, leaks, a wrong split, a wrong metric, the test set opened twice, memo values that disagree with the notebook, copied notebooks, the untouched template, the grade_project.py command end to end, the gradebook import under the real gradebook.gs, and the patched portal and collector under node.', 10, after=3)
    para(d, 'Not proved (needs you): real scikit-learn (a tree or logistic number can differ in a late digit; run run_proofs.py on your Mac after pip install scikit-learn with the stand-in removed), a real Colab session, the Docker image, the real Google Forms, Apps Script deployment and Cloudflare gateway. The step list is in deploy/DEPLOYMENT_STEPS.md.', 10, after=3)
    h2(d, '11. Open decisions for you')
    bullets(d, ['Confirm the sitting dates and times. They are proposals. Each place that states them says so.',
                'Late arrivals lose time (the Test 1 rule). If you prefer a fixed 3 hours for everyone, set closes_at 15 to 20 minutes after the class end and tell the class.',
                'Two copies of the notebook cannot be told apart by the portal: one registration number gets one attempt.',
                'The secrecy of grader_spec/ (hidden checks, model solutions) is the same as for Tests 1 and 2. If the repository is public, students can read it. Publish without Project/grader_spec/ and Project/Notebooks/ if you want to avoid that, and grade from a private copy.',
                'The written answers are marked by keyword and length rules, so a vague but keyword-rich answer earns the mark. This is what you asked for. The spot-check list shows the extreme cases.',
                'The 24 and 6 split inside Part A is my choice: 24 marks for functions and results, 6 for process (test set once, no leakage, seed, charts).'], 10)
    save_pdf(d, OUT / 'Lecturer_Marking_Guide.docx')


if __name__ == '__main__':
    for code in PC.CODES:
        student_brief(code)
    marking_guide()
