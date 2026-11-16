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
WEEKS = dict(clean_h='Weeks 3 to 7', split_h='Week 10', regression='Weeks 8 and 9', errors='Week 8', leakage='Weeks 8 to 10', charts='Weeks 3 to 8',
             encoded='Revision class (recipe given)', test_h='Week 10', clean_m='Weeks 3 to 7', split_m='Week 10', classify='Week 9', scores='Week 9',
             test_m='Week 10', results='Weeks 8 to 10')
CHECKED = dict(       # the marking guide's wording: the same checks as the rubric descriptions (build_grader_spec.py)
    clean_h='Task 1 cells re-run on two hidden raw house tables with added duplicates, missing prices and impossible values. Shares: the whole result, no duplicates, no missing price, no impossible value (valid rows kept), other gaps kept, raw table unchanged.',
    split_h='Task 2 cells re-run on hidden clean houses, also reversed: the three sets of the stated rule.',
    regression='Task 3 cells re-run on hidden train and valid houses: linear regression and decision tree predictions (median imputation, max_depth 4, random_state 17).',
    errors='MAE and RMSE of the student\'s own Task 3 predictions (a model mistake is not counted twice); printed values count.',
    leakage='Task 3 re-run with extreme rows added to valid: the other predictions must not change (imputation learned from the training rows only).',
    charts='Chart 1 and Chart 2 from the run from the top (under any name, or only shown): title, named axes, unit, right data.',
    encoded='Task 3b cells (under Task 3) re-run on the Task 3 hidden sets, each with a real neighbourhood or kitchen_quality value the training rows never show: encoded_pred equals the one-hot reference (needs handle_unknown="ignore"), encoded_mae from the own predictions, and extra validation rows leave the other predictions unchanged.',
    test_h='Task 4 re-run on hidden train, valid and test houses, with validation numbers that make the rule pick each model once: the choice and the test MAE; houses_test read only after chosen_house_model; no test house in train or valid.',
    clean_m='Task 5 cells re-run on two hidden raw machine tables with added problems. Shares: the whole result, no duplicates, no impossible value, product_type mapped, raw table unchanged.',
    split_m='Task 6 cells re-run on hidden clean machines, also reversed: the three sets of the stated rule.',
    classify='Task 7 re-run on hidden train and valid machines: logistic probabilities (solver tolerance), logistic warnings at 0.5 from the own probabilities, tree warnings equal to DecisionTreeClassifier(max_depth=3, random_state=17).',
    scores='Task 7: for each model, the counts (tn, fp, fn, tp), precision, recall and F1 from the student\'s own warnings.',
    test_m='Task 8 re-run on hidden train, valid and test machines, with F1 values that make the rule pick each model once: the choice and the test F1; machines_test read only after chosen_warning_model; no test run in train or valid.',
    results='A third each: validation MAE (houses) and F1 (machines) of both models on the real tables, calculated, and both rule choices; the same predictions twice, random_state=17 on both trees, no unseeded randomness; every result and MEMO present (Task 3b excluded).')
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
CHECKED_BRIEF = dict(
    clean_h='Your Task 1 cells re-run on hidden raw houses with the same kinds of problems. Each rule earns a share.',
    split_h='Your Task 2 cells re-run on hidden clean houses, also in another order.',
    regression='Your Task 3 cells re-run on hidden train and valid houses: both models\' predictions.',
    errors='The MAE and RMSE of your own predictions on hidden valid rows.',
    leakage='Extra extreme rows in valid leave the other predictions unchanged.',
    charts='Chart 1 and Chart 2: title, both axis labels, unit, right data. 1 mark each.',
    encoded='Your Task 3b cells re-run on hidden train and valid, which include a category train never shows: the predictions and their MAE; the encoder learns from train only.',
    test_h='Your Task 4 cells re-run: the rule\'s choice and the test MAE; the test houses used only after the choice; no test house in train or valid.',
    clean_m='Your Task 5 cells re-run on hidden raw machines with the same kinds of problems. Each rule earns a share.',
    split_m='Your Task 6 cells re-run on hidden clean machines, also in another order.',
    classify='Your Task 7 cells re-run: logistic probabilities and warnings, and the tree\'s warnings.',
    scores='For each model: counts, precision, recall and F1 from your own warnings.',
    test_m='Your Task 8 cells re-run: the rule\'s choice and the test F1; the test runs used only after the choice; no test run in train or valid.',
    results='A third each: results on the real tables calculated, not typed, and both choices; the same answer every time with random_state=17; every result and MEMO present.')

def student_brief(code):
    c = PC.COHORT[code]
    cfg = P.EXAM
    u = cfg['h_unit']
    n = PC.numbers()['p']['n']
    w = PC.WINDOW
    d = new(f'{code} Engineering ML project: student brief', 'IUEA Machine Learning for Engineers  |  Student Brief')
    title(d, 'Engineering ML project: house prices and machine failures', f'{code}  |  {c["name"]}  |  Part A 30 + Part B 15 = 45 marks, scaled to 40 percent  |  Online, 3 hours, individual, marked by computer')
    box(d, 'At a glance', [
        f'Window: opens {w["opens"]}, closes {w["closes"]} Kampala time. You have 3 hours from Start. Start by {w["last_full_start"]} for the full 3 hours.',
        'Online, from anywhere: your own laptop, Google account and internet.',
        'No Submit button. Your notebook saves itself and is collected automatically at your deadline.',
        f'Rehearsal (unmarked): {PC.REHEARSAL_TEXT[code]}. Exactly the project\'s tasks, files and result names; only the split\'s random_state is 29, so the numbers differ.',
        'Part A: the coded notebook (30). Part B: the MEMO form in the notebook (15). All marked automatically.'])
    h2(d, '1. The two questions', 4)
    grid(d, [['Question 1', f'Houses only (Tasks 1 to 4). What will a house sell for (sale_price_usd, {u})? Clean, split 60/20/20, then compare a linear regression and a decision tree (depth 4), each with median imputation, by MAE and RMSE in {u}. '
                            f'Features: the {len(cfg["h_features"])} number columns (H_FEATURES). Task 3b (2 marks) adds the {len(cfg["h_text"])} text columns with one-hot encoding, using a recipe given in the task. '
                            f'A supplied rule picks the model (validation MAE at most {cfg["max_mae"]:,} {u}, prediction time at most {P.MAX_MS} ms, both invented teaching numbers); then the test set once.'],
             ['Question 2', 'Machines only (Tasks 5 to 8). Will a machine run fail (failure is 1, about 3 percent of runs)? Clean, split 60/20/20, then compare logistic regression (with StandardScaler; warn at 0.5 or more) '
                            'and a decision tree classifier (depth 3). For each: the confusion matrix counts, precision, recall and F1. A supplied rule picks the higher validation F1; then the test set once.']],
         [3.2, W - 3.2], size=9.5)
    h2(d, '2. The data')
    bullets(d, [('Houses:', f'{n["houses_raw"]:,} rows of house sales in Ames, Iowa, 2006 to 2010, recorded by the city assessor (De Cock 2011, Journal of Statistics Education 19(3)), organised into 18 plain columns in metric units, the target sale_price_usd.'),
                ('Machines:', f'{n["machines_raw"]:,} runs of a metal-cutting machine from the AI4I 2020 data (Matzka 2020, UCI, CC BY 4.0). These data are SYNTHETIC: generated to behave like real machine records, not measured on real machines. The target is failure.'),
                ('Added problems:', 'a few duplicate rows, rows with no target value and impossible values were added to both tables on purpose, for you to clean. The notebook says so.'),
                ('Task 1:', f'remove the duplicate rows, the rows with no target and the rows with an impossible value (a living area of 0 or less or a house built after {P.LAST_YEAR}; a torque or speed of 0 or less); change product_type to a number (L 0, M 1, H 2). Leave the other gaps for the imputer.'),
                ('Split:', f'you split each cleaned table with the given lines: test = 20 percent, validation = 25 percent of the rest, training the remainder (random_state=17). That gives {n["houses_train"]:,}, {n["houses_valid"]:,} and {n["houses_test"]:,} houses, and {n["machines_train"]:,}, {n["machines_valid"]:,} and {n["machines_test"]:,} machines.'),
                ('Test set:', 'use it once, in Task 6, after the rule has chosen. Reading the test rows earlier loses marks.')], 10)
    h2(d, '3. On the day')
    numbered(d, [('Start.', 'Open the entry link. Choose your course and type your registration number (for example 26/BCE/001/PS). Tick This is me; if your name is not shown, type your full name. Type the Google email you use in Colab twice and press Start. A typo in the email can be corrected once on the page in the first 15 minutes. Your 3 hours begin. A number on another course\'s list is refused.'),
                 ('Work.', 'Press Open my project in Colab. Your deadline is at the top. Run Setup: run me first (do not edit it), then each task from the top. Do not use Save a copy. Press Ctrl+S now and then; the time left shows after every cell.'),
                 ('Deadline.', f'3 hours after Start, or the window\'s close ({w["closes"]}) if earlier. It cannot be paused or restarted.'),
                 ('Check.', 'Check my work on the entry page runs your saved notebook from the top: does it run, are all results and MEMO there, is it your issued notebook. No mark is shown.'),
                 ('End.', 'At your deadline editing stops and your work is collected: the last save before the deadline, or the newest 5-minute backup if newer. Finished early? Press I have finished.'),
                 ('Help.', f'The class channel, {PC.SUPPORT_HOURS}. The lecturer does not write or debug answers.'),
                 ('Failure.', 'Post a screenshot on the class channel at once. The lecturer can give one fresh attempt, also for a wrong Google account; it still ends at the window\'s close. After a disconnect, open the entry page and click Resume: the timer continues.')], 10)
    rows = [[name, f'{m} min'] for name, m in PC.TIME_PLAN] + [['Total', f'{PC.MINUTES} min']]
    grid(d, rows, [W - 3.0, 3.0], header=['Suggested time plan', 'Time'], size=9)
    h2(d, '4. Rules')
    bullets(d, [('Allowed:', 'Colab, your slides, your lab notebooks from Classes 1 to 3, the revision guide, the cheatsheet, your own notes.'),
                ('No AI:', 'no Gemini, ChatGPT, Copilot or any other AI tool to write, complete, explain or debug your answers.'),
                ('No outside help:', 'no help from another person, no copying. Identity checks run on every notebook and identical written answers are flagged.'),
                ('Understanding check:', 'any student may be asked afterwards, in an online call, to explain or change their code.'),
                ('Declaration:', 'by working in your issued notebook until your deadline, you declare the work is your own.')], 10)
    h2(d, '5. How to write your answers')
    numbered(d, [('Plain code.', 'Each task names its inputs (for example train and valid) and the results to store (for example linear_mae). Write ordinary code in as many cells as you like; functions, loops and if statements are optional.'),
                 ('Keep the result names', 'exactly as printed. A near name or a printed value still counts, but the exact name is safest.'),
                 ('Each task is checked on its own', 'with hidden versions of its inputs, so a mistake in one task does not cost the next. Use only the task\'s inputs and the setup constants (TARGET, FEATURES, LIMIT...).'),
                 ('Restart and run all', 'before your deadline. No errors; under 30 seconds a cell. Never split at random; keep random_state=17.'),
                 ('Calculate, do not type', 'numbers: a typed number fails on the hidden inputs. The setup cell is always restored to its original before marking, so editing it changes nothing.')], 10)
    h2(d, '6. Part A (30 marks)')
    para(d, 'Your notebook runs from the top in a box with Colab\'s Python. Then the cells of each task run again on hidden rows from the same file; each item earns the share of its checks that pass.', 10, after=4)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED_BRIEF[t], WEEKS[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Total', '', '', str(K.PART_A_MAX)])
    grid(d, rows, [4.2, 8.4, 2.8, 2.0], header=['Item', 'What is checked', 'Taught in', 'Marks'], size=8.5, label_cols=(0,))
    h2(d, '7. Part B: the MEMO form (15 marks)')
    para(d, f'For {PC.PAYER}. Numbers with at least two decimals (MAE in {u}, F1 from 0 to 1). The lists of limits and next steps are in the notebook.', 10, after=3)
    grid(d, [['house_model', '"linear" or "tree": the house model the rule chose in Task 4.', '2'],
             ['house_validation_mae', 'The validation MAE of both house models, from your notebook.', '2'],
             ['warning_model', '"logistic" or "tree": the warning model the rule chose in Task 8.', '2'],
             ['warning_validation_f1', 'The validation F1 of both warning models, from your notebook.', '1'],
             ['test_mae, test_f1', 'From Tasks 4 and 8.', '2'],
             ['limits', 'Three different letters: the true limits of this study. One mark each.', '3'],
             ['next_step', 'One letter: the best next step.', '1'],
             ['answer_choice, answer_test_set', 'Why you recommend your model (give a validation number and what you compared it with), and why the test set is used once. 8 to 80 words each, your own words. One mark each.', '2'],
             ['Total', '', '15']],
         [4.6, W - 6.4, 1.8], header=['Field', 'Enter', 'Marks'], size=9, label_cols=(0,))
    para(d, f'Results: final by {PC.RESULTS_BY}.', 10, before=4, after=3)
    h2(d, 'Before your deadline')
    grid(d, [['☐', 'Restart session and run all: no error. Every result named in the tasks is stored.'],
             ['☐', 'Test set used once, after the choice. Both charts have a title, axis labels and the unit.'], ['☐', 'MEMO complete, with your own numbers.'],
             ['☐', 'Worked only in the issued notebook; Ctrl+S pressed; Check my work shows no failing cell.']],
         [1.0, W - 1.0], size=9.5, label_cols=())
    para(d, f'Data credit: {PC.CITATION}.', 8.5, italic=True, before=4, after=2)
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
    para(d, f'Every student has the same two tables, built from two published files. {PC.CITATION} Houses: the Ames sales (SHA-256 {P.HOUSES_SHA256[:16]}...) organised into 18 plain columns in metric units, the 5 sales above 4000 sq ft left out as De Cock advises; lot_frontage_m has {sum(r["lot_frontage_m"] is None for r in P.houses_given())} real gaps. Machines: AI4I 2020 (SHA-256 {P.MACHINES_SHA256[:16]}...), SYNTHETIC (the brief says so), 3.4 percent failures; the failure-type columns that leak the target are left out. Added on purpose and said so in the notebook (fixed, the same for everyone): houses {P.H_PROBLEMS["duplicates"]} duplicates, {P.H_PROBLEMS["missing_target"]} missing prices, {P.H_PROBLEMS["invalid"]} impossible values; machines {P.M_PROBLEMS["duplicates"]} duplicates, {P.M_PROBLEMS["missing_target"]} missing failures, {P.M_PROBLEMS["invalid"]} impossible values and {P.M_PROBLEMS["missing_feature"]} missing tool wear values. Given {p["n"]["houses_raw"]:,} houses and {p["n"]["machines_raw"]:,} machines; cleaned {p["n"]["houses"]:,} and {p["n"]["machines"]:,}. Students split 60/20/20 with the given lines (random_state=17): {p["n"]["houses_train"]:,}, {p["n"]["houses_valid"]:,} and {p["n"]["houses_test"]:,} houses; {p["n"]["machines_train"]:,}, {p["n"]["machines_valid"]:,} and {p["n"]["machines_test"]:,} machines.', 10, after=3)
    vm = p['validation_mae']
    pr = P.pipeline(P.REHEARSAL)
    para(d, f'Reference results (the model solution, real scikit-learn). Question 1: validation MAE linear {vm["linear"]:,.0f}, tree {vm["tree"]:,.0f} USD; chosen {nums["chosen"]} (MAX_MAE {P.EXAM["max_mae"]:,} USD); test MAE {nums["test"]["mae"]:,.0f} USD; Task 3b about 17,500 USD (a comparison only). '
            f'Question 2: logistic regression F1 {p["warning_scores"]["f1"]:.3f} (TP {p["warning_scores"]["tp"]}, FP {p["warning_scores"]["fp"]}, FN {p["warning_scores"]["fn"]}), tree F1 {p["tree_warning_scores"]["f1"]:.3f} (TP {p["tree_warning_scores"]["tp"]}, FP {p["tree_warning_scores"]["fp"]}, FN {p["tree_warning_scores"]["fn"]}); chosen {p["chosen_warning"]}; test F1 {nums["test"]["warning"]["f1"]:.3f}. '
            f'The rehearsal (random_state=29): MAE linear {pr["validation_mae"]["linear"]:,.0f}, tree {pr["validation_mae"]["tree"]:,.0f} USD; F1 logistic {pr["warning_scores"]["f1"]:.3f}, tree {pr["tree_warning_scores"]["f1"]:.3f}.', 10, after=4)
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
    para(d, 'Plain code (your redesign of 14 November 2026). Students write ordinary code under each task heading and store the named results. Before a notebook runs, the grader works on a copy: the supplied setup cell is put back to its original (whatever was done to it, even deleted; flagged SUPPLIED_CELL_EDITED); then, after the run from the top, the cells of each task (every code cell between its heading and the next task heading, the student\'s own cells included) run again in a fresh namespace with hidden versions of the task\'s inputs. Typed or copied numbers fail, an earlier mistake never costs a later task, a result under a near name counts (flagged RENAMED_RESULT), and a printed number counts. ' + PC.OWN_CELLS, 9.5, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    grid(d, rows, [4.6, 11.0, 1.8], header=['Part A item', 'Automatic check', 'Marks'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    ex = {
        'b1': 'house_model is a model the student trained (1) and equals the student\'s own rule choice (1).',
        'b2': 'house_validation_mae for linear and tree each within 0.011 of the student\'s own computed value (1 each).',
        'b3': 'warning_model is a model the student trained (1) and equals the student\'s own rule choice, the higher validation F1 (1).',
        'b4': 'warning_validation_f1 for logistic and tree both within 0.011 of the student\'s own values (1).',
        'b5': 'test_mae (1) and test_f1 (1) within 0.011 of the student\'s own Task 4 and Task 8 values.',
        'b6': 'Three different letters; one mark for each of the four true limits chosen (four true and six false statements, lettered differently for each course).',
        'b7': 'The one correct next step of five (collect sales from more towns and years, and real machine records, and check the chosen models again on unseen rows).',
        'b8': '8 to 80 words and the keyword groups: answer_choice needs a measure word (error, MAE, F1, lower, better...), an evidence word (validation, compared, than, tree, linear...) and a number; answer_test_set needs "test" and a reason (honest, leak, choose, tune, unseen...).'}
    grid(d, [[f'{k.upper()} {M_t} ({m})', ex[k]] for (k, M_t, m) in M.PARTB], [4.6, W - 4.6], header=['Part B field', 'Automatic check'], size=8.5, label_cols=(0,))
    para(d, 'Keyword rules cannot judge quality. They accept several correct wordings on purpose (the lists are in grader_spec/memo_spec.py and are tested in run_proofs.py with a differently worded pair). A written answer that is a list of keywords earns the mark and appears on the spot-check list as KEYWORD_STUFFING for you to read.', 9.5, italic=True, before=3, after=3)
    h2(d, '7. A worked example')
    marks = proof_example()
    a = sum(marks[t] for t, _ in K.PARTS)
    b = sum(marks[t] for t, _ in K.PARTB)
    para(d, 'A CML3112 student has done every task correctly except RMSE, which they left without the square root, and filled in the memo form from their own notebook. This is one of the wrong solutions the grader was tested on, so the numbers below are what the grader gives.', 10, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', fmt(marks[t]), str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    rows.append(['Part A total', fmt(a), str(K.PART_A_MAX)])
    rows += [[f'Part B {M_t}', fmt(marks[k]), str(m)] for (k, M_t, m) in M.PARTB]
    rows.append(['Part B total', fmt(b), str(K.PART_B_MAX)])
    grid(d, rows, [11.0, 3.2, 3.2], header=['Item', 'Awarded', 'Out of'], size=8.5, label_cols=(0,))
    para(d, f'Why: the RMSE checks fail, so item A4 (MAE and RMSE) loses a quarter of its marks; nothing else changes, because every other task is checked on its own hidden inputs. Part B is full because the memo agrees with the student\'s own notebook (the grader compares with the student\'s own values, so a Part A error does not also cost Part B marks). Project total {fmt(a + b)} of {K.PART_A_MAX + K.PART_B_MAX}, which is {100 * (a + b) / (K.PART_A_MAX + K.PART_B_MAX):.0f} percent of the project.', 10, before=3, after=3)
    h2(d, '8. Common errors and what they cost')
    grid(d, [['Duplicate rows kept', 'Item A1 (houses) or A9 (machines) loses the duplicates share and the whole-result share.'],
             ['Impossible values or rows with no target kept', 'Item A1 or A9 loses those shares; the models also learn from wrong rows.'],
             ['Imputation fitted on all rows', 'Item A3 fails on the linear and tree lists, and item A5 (no leakage) drops.'],
             ['A choice typed in instead of the rule', 'The hidden run that needs the other model fails, so item A8 or A13 drops.'],
             ['F1 as the plain mean of precision and recall', 'Item A12 (scores) drops: F1 is 2 x P x R / (P + R).'],
             ['Another split rule (other frac or seed)', 'Item A2 or A10 scores 0 and the results share of A14 fails, because the validation rows are different.'],
             ['Gaps filled in Task 1 (fillna on all rows)', 'Item A1 loses the gaps share: the imputer must learn the medians from the training rows only.'],
             ['RMSE without the square root', 'Part of item A4.'],
             ['Task 3b without handle_unknown="ignore"', 'predict stops on a category the training rows never show, so item A7 earns 0. Nothing else is lost.'],
             ['Task 3b skipped', 'Item A7 (2 marks) only: its results are not part of "results and MEMO present".'],
             ['Test rows added to the training or validation rows', 'Part of item A8 or A13 is lost.'],
             ['Test rows read before the choice', 'Part of item A8 or A13; flagged TEST_USED_EARLY on the spot-check list.'],
             ['No random_state=17 on a tree', 'The reproducibility share of item A14 is lost.'],
             ['Chart without an axis name or unit', 'Part of item A6 is lost.'],
             ['Editing the setup cell', 'The original is put back before marking, so it costs nothing; the case is flagged SUPPLIED_CELL_EDITED.'],
             ['Results typed in', 'The results share of item A14 earns 0 for those numbers; flagged RESULTS_NOT_CALCULATED.'],
             ['A required result missing or named beyond recognition', 'That result\'s share, and the "results and MEMO present" share of item A14.'],
             ['Memo numbers copied wrongly', 'The Part B field loses its mark; flagged MEMO_NUMBERS_DISAGREE. Look for a missing decimal point before overriding.'],
             ['STUDENT_ID blank or someone else\'s', 'IDENTITY_MISMATCH. The allocation and its Drive file say who it was issued to; speak to the student.']],
         [5.4, W - 5.4], header=['Mistake', 'What happens and what to do'], size=9, label_cols=(0,))
    h2(d, '9. Integrity checks')
    bullets(d, ['Everyone has the same file, so the numbers, the chosen model and (within a course) the memo letters are the same for honest students. Numbers alone prove nothing. Look for shared code, shared sentences and shared unusual choices.',
                'grade_project.py compares only what each student wrote, after removing the issued template, and compares the written answers. The rehearsal has exactly the project\'s tasks, so honest task code is near-identical: code similarity is recorded as SIMILAR_CODE, information only (your decision of 14 November). Identical written answers still raise SAME_WRITTEN_ANSWERS; talk to a pair only when you see the same sentences or the same unusual choices.',
                'Understanding check: the brief says that any student may be asked, after the window, in an online call, to explain their code or make a small change. Suggested questions: why remove duplicate rows, why remove a row with no price, how did you find the impossible values, why is the split rule fixed with a seed, why is the median learned from the training rows, why is the test set used once and last, what does recall mean for a missed warning.',
                'Each task\'s cells are re-run on rows built from the file that no student has, so copied code or copied numbers still have to work on them.'], 10)
    h2(d, '10. What was proved and what was not')
    n, ok = counts()
    para(d, f'Proved on this Mac in the Colab-matching Docker sandbox (iuea-notebooks:colab-2026.11: Python 3.13.18, numpy 2.4.6, pandas 2.2.3, scikit-learn 1.6.1, matplotlib 3.10.0, IPython 7.34.0, the versions Colab lists on 13 November 2026), through grader_spec/run_proofs.py --docker, the real batch_grade.py and the hidden spec: {ok} of {n} proof cases behave as required, for all three courses. They cover the model solution, a differently written correct solution, the own-cells cases (several cells, a near name, a printed result), the tampered, deleted and edited setup cell, the Colab habits that broke Test 1 (display and IPython imports, a re-uploaded "(1)" copy, an unnamed chart and a later plt call), leaks, a wrong split, each cleaning rule, a wrong metric, the warning counts at 0.5, edited supplied cells, the test set opened twice or early, a missing result, memo values that disagree with the notebook, copied notebooks, the untouched template, grade_project.py end to end, the gradebook import under the real gradebook.gs, and the patched portal under node, including the notebook exactly as the portal issues it.', 10, after=3)
    para(d, 'The collection and instant marking were proved end to end with no network (actions/test_actions_e2e.py): the real Portal.gs, Gateway.gs, the collector ml_project_pipeline.gs and the Cloudflare worker run on in-memory fakes of Sheets and Drive (permissions and revisions with their modifiedTime). The cases: an ordinary student, one who saved a copy, a laptop that died at minute 170, a student who never pressed anything and one who pressed only Start, a backup after the deadline, a stopped backup thread, the wrong Google account (and its fresh attempt), a wrong-course registration, a whole-course and a one-student extension, I have finished, Check my work and the rehearsal. The marks stay hidden until the release switch and the window close, and final_regrade.py agrees with the instant marks.', 10, after=3)
    para(d, 'Not proved (needs you): a real Colab session (that the background backup can read the notebook on screen from a thread, and that a shared editor file opens without the Copy to Drive banner), the Apps Script deployments, the GitHub repository and its minutes, and the Cloudflare gateway. deploy/setup_pipeline.sh does the set-up; deploy/SETUP_GITHUB_ACTIONS.md says what is left.', 10, after=3)
    h2(d, '11. Open points for you')
    bullets(d, [f'Confirm the support hours on the class channel ({PC.SUPPORT_HOURS.split(" (")[0]}).',
                'A student who starts late loses time (the Test 1 rule). Say so in every reminder.',
                'Two copies of the notebook cannot be told apart by the portal: one registration number gets one attempt.',
                'The secrecy of grader_spec/ (hidden checks, model solutions) is the same as for Tests 1 and 2. If the repository is public, students can read it. Publish without Project/grader_spec/ if you want to avoid that, and grade from a private copy.',
                'The written answers are marked by keyword and length rules, so a vague but keyword-rich answer earns the mark. The spot-check list shows the extreme cases.',
                'Within a course every student sees the same lettering of the limits and next-step lists. Only the lettering between courses differs.',
                'The split inside Part A follows your blueprint and the change of 14 November: 20 marks for task code re-run on hidden rows (A1, A3, A4, A5, A7), 2 for no leakage, 2 for the charts, 2 for the test set, 2 for results, reproducibility and the required parts, and 2 for Task 3b (one-hot encoding, recipe given).',
                'Task 3b on the real file: scikit-learn switches to a sparse matrix there and solves with an iterative method, so its validation MAE (about 15,440 USD, against 20,538 for the linear model) is not compared with a reference; Task 3b is marked only on the hidden rows, where the matrix stays dense and the answer is exact. Fitting the encoder alone on train and valid together cannot be detected: a category seen only in valid gets a weight of zero, so the predictions are the same.'], 10)
    save_pdf(d, OUT / 'Lecturer_Marking_Guide.docx')


if __name__ == '__main__':
    for code in PC.CODES:
        student_brief(code)
    marking_guide()
