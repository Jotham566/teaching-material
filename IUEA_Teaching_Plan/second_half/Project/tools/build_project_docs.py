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
CHECKED = dict(       # the marking guide's wording: the same checks as the rubric descriptions (build_grader_spec.py)
    clean='Task 1 cells re-run on a hidden raw table with problems added. Nine shares per table: the whole result, rows in order, the date fix, the all-zero reading, CO2 removed, repeats, impossible values, month and weekend, raw unchanged.',
    charts='Chart 1 and Chart 2 from the run from the top (under any name, or only shown): title, named axes, unit, right data.',
    split='Task 2 cells re-run on hidden clean tables, also reversed: train months 1 to 8, valid 9 and 10, rows in order.',
    regression='Task 3 cells re-run on hidden train and valid: baseline, linear regression and decision tree predictions (median imputation, max_depth 4, random_state 17).',
    errors='MAE and RMSE of the student\'s own Task 3 predictions (a model mistake is not counted twice); printed values count.',
    leakage='Task 3 re-run twice more: extreme rows added to valid leave the other predictions unchanged; the baseline is the mean of the (shifted) train targets.',
    warning='Task 4 re-run: probabilities (1 mark); counts, precision and recall at 0.5 from the student\'s own probabilities (2 marks).',
    test='Task 6 re-run on hidden train, valid and test rows (MAE and recall after refitting); opened once, after the choice, with it; no November or December row in train or valid.',
    results='Validation MAE of the three models and the chosen model on the real file (1); the same predictions twice, random_state=17, no unseeded randomness (1); every result and MEMO present (1).')
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
    clean='Your Task 1 cells re-run on a hidden raw table with problems added: midnight fix, all-zero row dropped, CO2(tCO2) removed, first copy kept, impossible values and missing target dropped, month and weekend added, raw unchanged. Each rule earns a share.',
    charts='Chart 1 and Chart 2: title, both axis labels, unit, right data. 1 mark each.',
    split='Your Task 2 cells re-run on hidden clean tables, also in another order.',
    regression='Your Task 3 cells re-run on hidden train and valid: the three models\' predictions.',
    errors='The MAE and RMSE of your own predictions on hidden valid rows.',
    leakage='Extra extreme rows in valid leave the other predictions unchanged; the baseline follows the train targets.',
    warning='Your Task 4 cells re-run: probabilities (1); counts, precision and recall at 0.5 (2).',
    test='Your Task 6 cells re-run (test MAE and recall after refitting); opened once, after the choice, with that model; no November or December row in train or valid.',
    results='Results on the real file calculated, not typed (1); the same answer every time with random_state=17 (1); every result and MEMO present (1).')


def student_brief(code):
    c = PC.COHORT[code]
    cfg = P.EXAM
    u = cfg['unit']
    n = PC.numbers()['p']['n']
    w = PC.WINDOW
    d = new(f'{code} Engineering ML project: student brief', 'IUEA Machine Learning for Engineers  |  Student Brief')
    title(d, 'Engineering ML project: energy use at a steel plant', f'{code}  |  {c["name"]}  |  Part A 30 + Part B 15 = 45 marks, scaled to 40 percent  |  Online, 3 hours, individual, marked by computer')
    box(d, 'At a glance', [
        f'Window: opens {w["opens"]}, closes {w["closes"]} Kampala time. You have 3 hours from Start. Start by {w["last_full_start"]} for the full 3 hours.',
        'Online, from anywhere: your own laptop, Google account and internet.',
        'No Submit button. Your notebook saves itself and is collected automatically at your deadline.',
        f'Rehearsal (unmarked): {PC.REHEARSAL_TEXT[code]}. Same tasks, same file, another target.',
        'Part A: the coded notebook (30). Part B: the MEMO form in the notebook (15). All marked automatically.'])
    h2(d, '1. The two questions', 4)
    grid(d, [['Question 1', f'How much energy (Usage_kWh) does a 15-minute reading use, in months the model has not seen? Compare a baseline, a linear regression and a decision tree (depth 4) with MAE and RMSE in {u}. Features: lagging and leading reactive power, NSM, a weekend flag.'],
             ['Question 2', f'A reading is a warning (1) when Usage_kWh is at or above {cfg["limit"]:g} {u}. Logistic regression gives each reading a probability; a warning when it is 0.5 or more. Report the confusion matrix counts, precision and recall.'],
             ['Model choice', f'A supplied rule picks one model: validation MAE at most {cfg["max_mae"]:g} {u} and prediction time at most {P.MAX_MS} ms.']],
         [3.2, W - 3.2], size=9.5)
    h2(d, '2. The data')
    bullets(d, [('File:', f'{n["file"]:,} readings, one every 15 minutes in 2018, {PC.SOURCE["plant"]}. Stored inside the setup cell: no upload or download.'),
                ('Handle in Task 1:', 'each day\'s last reading is written as that day\'s date at 00:00 (it belongs to the next midnight); one reading on 7 November is all 0; CO2(tCO2) leaks the target and is removed.'),
                ('Not features:', 'the two power factors (calculated from the target) and Load_Type.'),
                ('Split by month:', f'training January to August ({n["train"]:,} rows), validation September and October ({n["validation"]:,}), test November and December ({n["test"]:,} after cleaning).'),
                ('Test set:', 'open it once with the supplied open_test_set(chosen_model), after the rule has chosen. A second call loses marks.')], 10)
    h2(d, '3. On the day')
    numbered(d, [('Start.', 'Open the entry link. Type your registration number, tick This is me, type the Google email you use in Colab twice, press Start. A typo can be corrected once on the page in the first 15 minutes. Your 3 hours begin. A number from another course is refused.'),
                 ('Work.', 'Press Open my project in Colab. Run Setup: run me first, then each task from the top. Do not use Save a copy. Press Ctrl+S now and then; the line after every cell shows the time left.'),
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
                ('No outside help:', 'no help from another person, no copying. Copy and identity checks run on every notebook.'),
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
    para(d, f'For {PC.PAYER}. Numbers with at least two decimals, in {u}. The lists of limits and next steps are in the notebook.', 10, after=3)
    grid(d, [['recommended_model', '"baseline", "linear" or "tree": the model the rule chose and you opened the test set with.', '3'],
             ['validation_mae', 'The validation MAE of the three models, from your notebook.', '3'],
             ['test_mae, test_recall', 'From your one test opening.', '2'],
             ['improvement_over_baseline', f'Baseline validation MAE minus your model\'s, in {u}.', '1'],
             ['limits', 'Three different letters: the true limits of this study. One mark each.', '3'],
             ['next_step', 'One letter: the best next step.', '1'],
             ['answer_choice, answer_test_set', 'Why you recommend your model (give a validation number and what you compared it with), and why the test set is opened once. 8 to 80 words each, your own words. One mark each.', '2'],
             ['Total', '', '15']],
         [4.6, W - 6.4, 1.8], header=['Field', 'Enter', 'Marks'], size=9, label_cols=(0,))
    para(d, f'Results: final by {PC.RESULTS_BY}.', 10, before=4, after=3)
    h2(d, 'Before your deadline')
    grid(d, [['☐', 'Restart session and run all: no error. Every result named in the tasks is stored.'],
             ['☐', 'Test set opened once, after the choice. Both charts have a title, axis labels and the unit.'], ['☐', 'MEMO complete, with your own numbers.'],
             ['☐', 'Worked only in the issued notebook; Ctrl+S pressed; Check my work shows no failing cell.']],
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
    para(d, f'Every student has the same real file: {PC.CITATION} {p["n"]["file"]:,} rows, one every 15 minutes for 2018. Checked on 13 November 2026 (SHA-256 {P.DATA_SHA256[:16]}...): no missing cells, no repeated rows. Real problems the students handle: each day\'s last reading is written with that day\'s date at 00:00 (365 rows; their real time is midnight at the end of the day); one reading on 7 November has every measurement 0; CO2(tCO2) and the two power factors are calculated from Usage_kWh, so they would leak the target. No error was invented in the file. The hidden re-runs use rows sampled from the file with a small seeded change and with problems added, which the brief says plainly. Split: training January to August ({p["n"]["train"]:,} rows), validation September and October ({p["n"]["validation"]:,}), test November and December ({p["n"]["test"]:,} after cleaning). The file is stored inside the setup cell (bzip2 and base64, about 380 KB) and written out with a SHA-256 check.', 10, after=3)
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
    para(d, 'Plain code (your redesign of 14 November 2026). Students write ordinary code under each task heading and store the named results. Before a notebook runs, the grader works on a copy: the supplied setup cell is put back to its original (whatever was done to it, even deleted; flagged SUPPLIED_CELL_EDITED); then, after the run from the top, the cells of each task (every code cell between its heading and the next task heading, the student\'s own cells included) run again in a fresh namespace with hidden versions of the task\'s inputs. Typed or copied numbers fail, an earlier mistake never costs a later task, a result under a near name counts (flagged RENAMED_RESULT), and a printed number counts. ' + PC.OWN_CELLS, 9.5, after=3)
    rows = [[f'A{i}. {K.TITLES[t]}', CHECKED[t], str(m)] for i, (t, m) in enumerate(K.PARTS, 1)]
    grid(d, rows, [4.6, 11.0, 1.8], header=['Part A item', 'Automatic check', 'Marks'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    ex = {
        'b1': 'recommended_model is a model the student trained (1), equals the student\'s own rule choice (1), and is the model the test set was opened with (1).',
        'b2': 'validation_mae for baseline, linear and tree each within 0.011 of the student\'s own computed value (1 each).',
        'b3': 'test_mae (1) and test_recall (1) within 0.011 of the student\'s own Task 6 values (or the reference for the model that was opened, when they are missing).',
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
    para(d, 'A CML3112 student has done every task correctly except RMSE, which they left without the square root, and filled in the memo form from their own notebook. This is one of the wrong solutions the grader was tested on, so the numbers below are what the grader gives.', 10, after=3)
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
             ['Baseline model built from other targets', 'The baseline predictions are wrong and item A6 drops. Often pd.concat of train and valid.'],
             ['Wrong months in the split, or a random split', 'Item A3 scores 0 and the results share of A9 fails, because the validation set is different. A random split also loses the reproducibility share.'],
             ['Looking timestamps up in a list', 'The split cell runs for minutes and stops at 30 seconds; everything after it fails. The brief and the task text warn about this.'],
             ['RMSE without the square root', 'Part of item A5 and of item A8.'],
             ['> instead of >= at the threshold 0.5', 'Part of the counts share of item A7. A probability of exactly 0.5 is a warning.'],
             ['Opening the test set twice', 'Part of item A8 (even with the same model), more with another model; it appears on the spot-check list.'],
             ['No random_state=17 on the tree', 'The reproducibility share of item A9 is lost.'],
             ['Chart without an axis name or unit', 'Part of item A2 is lost.'],
             ['Editing a supplied cell', 'Detected by a hash; item A8 drops and the case is flagged.'],
             ['Results typed in', 'The results share of item A9 earns 0 for those numbers; flagged RESULTS_NOT_CALCULATED.'],
             ['A required result missing or named beyond recognition', 'That result\'s share, and the "results and MEMO present" share of item A9.'],
             ['Memo numbers copied wrongly', 'The Part B field loses its mark; flagged MEMO_NUMBERS_DISAGREE. Look for a missing decimal point before overriding.'],
             ['STUDENT_ID blank or someone else\'s', 'IDENTITY_MISMATCH. The allocation and its Drive file say who it was issued to; speak to the student.']],
         [5.4, W - 5.4], header=['Mistake', 'What happens and what to do'], size=9, label_cols=(0,))
    h2(d, '9. Integrity checks')
    bullets(d, ['Everyone has the same file, so the numbers, the chosen model and (within a course) the memo letters are the same for honest students. Numbers alone prove nothing. Look for shared code, shared sentences and shared unusual choices.',
                'grade_project.py compares only what each student wrote, after removing the issued template, and compares the written answers. The tasks are short and guided, so honest notebooks can look alike: talk to a pair only when you can also see the same sentences or the same unusual choices.',
                'Understanding check: the brief says that any student may be asked, after the window, in an online call, to explain their code or make a small change. Suggested questions: why is the midnight reading moved to the next day, why is CO2 removed, why split by month and not at random, why is the median learned from the training rows, why is the test set opened once, what does recall mean for a missed warning.',
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
                'The split inside Part A follows your blueprint: 21 marks for task code re-run on hidden rows (A1, A3, A4, A5, A7), 2 for no leakage, 2 for the charts, 2 for the test set, 3 for results, reproducibility and the required parts.'], 10)
    save_pdf(d, OUT / 'Lecturer_Marking_Guide.docx')


if __name__ == '__main__':
    for code in PC.CODES:
        student_brief(code)
    marking_guide()
