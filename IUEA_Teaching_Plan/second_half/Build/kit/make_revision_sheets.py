"""Revision class run sheets (Week 10, 17 and 20 November 2026): one Word file and PDF per cohort. python3 kit/make_revision_sheets.py

Class 3 is not taught as a lecture. The revision class works through the project rehearsal
(Project/Rehearsal/<code>/ML_PROJECT_rehearsal.ipynb: the project's exact tasks on the Ames houses and AI4I machines, split random_state=29, opened through the rehearsal entry link) live and teaches the Class 3 ideas, and for CML3112 the Class 2 ideas,
as they come up. Slide numbers are those of the current decks (the same numbers in all three cohorts).
The PDF is written by LibreOffice with a private profile that holds the Lato fonts (kit/lo_fonts.py)."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
sys.path.insert(0, str(BUILD / 'content'))
import common as C  # noqa: E402
import lo_fonts  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

OUT = BUILD.parent / 'Lecturer Guides'
FILES = {'CML3112': 'Revision_Class_CML3112_Tuesday17', 'CML3113': 'Revision_Class_CML3113_Friday20', 'CML3111': 'Revision_Class_CML3111_Friday20'}
DAY = {'CML3112': 'Tuesday 17 November 2026', 'CML3113': 'Friday 20 November 2026', 'CML3111': 'Friday 20 November 2026'}


def bullets(d, items, size=10, after=2, mark='•'):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.55)
        p.paragraph_format.first_line_indent = Cm(-0.45)
        add_run(p, mark + '  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def clock(blocks):
    t, rows = 0, []
    for m, show, say, task in blocks:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), show, say, task])
        t += m
    assert t == 180, t
    return rows


# ------------------------------------------------------------------ the blocks
# Rehearsal reference results (tidy tables of 16 November 2026, split random_state=29, real scikit-learn): cleaned 2,913 houses and 9,984 machines;
# split 1,748 / 582 / 583 houses and 5,990 / 1,997 / 1,997 machines; validation MAE baseline 58,789, linear 22,005, tree 27,785 USD; Task 3b about
# 17,800 USD; warnings at 0.5: TP 10, FP 6, FN 58, TN 1,923, precision 0.63, recall 0.15; chosen model linear; test MAE 20,135 USD, test recall 0.19.
ENTRY = (20,
         'The rehearsal entry page on the projector. I enter the demo number 26/DEMO/001/LECTURER. Class 3 deck, slides 37 to 39 (the project).',
         'I show every step slowly; you will do these yourself on Monday. Choose your course first: the page refuses a number from another course. Type your registration number and check the name is yours, then tick This is me. Type your Google email twice. It must be the account you are signed into in Colab, top right of colab.research.google.com: the notebook is shared with that account only. '
         'Press Start. The big countdown on the page is your 3 hours. A typo in the email can be fixed once, on the page, in the first 15 minutes. Then Open my project in Colab. Never use Save a copy. '
         'In the project the window is Monday 00:00 to Wednesday 23:59, Kampala time. Start by Wednesday 20:59 or you lose time.',
         'Watch and write down the steps: course, registration number, This is me, email twice, Start, Open my project in Colab. Students do not open the rehearsal: only the demo numbers do.')
SETUP = (10,
         'The collapsed cell "Setup: run me first. DO NOT EDIT THIS CELL". The line it prints (the size of houses_raw and machines_raw), the big clock under it, the deadline at the top, then the cell "The data" with its two column tables.',
         'Run Setup first, and again after any restart. You do not open it or edit it: the marking always uses the original. The data is inside it, so nothing is uploaded or downloaded. '
         'Two tables, read with me through "The data": houses_raw, real house sales in Ames, Iowa, 2006 to 2010, one row per sale, the target sale_price_usd; and machines_raw, runs of a metal-cutting machine (synthetic), the target failure. Each column is explained there. A few problems were added on purpose for Task 1. '
         'Your deadline is written at the top of the notebook. Setup shows a big clock, and after every cell a line shows the time left. Under 30 minutes it says Press Ctrl+S. These are the project\'s exact tasks and files; only the split seed is 29 today, so your numbers will not be the project\'s.',
         'Setup: run me first, then read the clock')
PLAIN = (5,
         'The Task 1 heading: the Input and Store line, then the empty cell "# Your code here. Store: houses, machines".',
         'Each task names its inputs and the results to store. Write plain code under it, in as many cells as you like. No functions needed. Store the result under the exact name, then print it and read it. '
         'Each task is re-run on its own with hidden versions of its inputs, so use only those inputs and the setup names (H_TARGET, H_FEATURES, M_TARGET, M_FEATURES, THRESHOLD). Calculate, never type a number.',
         'How to write an answer')
BREAK = (10, 'Nothing.', 'Ten minutes. Leave Colab open; your variables stay as long as the session stays connected.', 'Break')

TASK1_SHOW = ('Task 1 and the note "Cleaning". houses_raw.duplicated().sum(), houses_raw[H_TARGET].isna().sum(), houses_raw[houses_raw["living_area_m2"] <= 0], houses_raw[houses_raw["year_built"] > 2010]; the same questions for machines_raw. Class 1 slide 11 (removing rows we cannot trust).')
TASK1_SAY = ('Start from a copy, so the raw tables never change. Look first: count the duplicates, the missing prices and the impossible values, then remove them in three lines: drop_duplicates(), dropna(subset=[H_TARGET]), then keep the rows that pass the rule (living_area_m2 above 0, year_built 2010 or earlier). '
             'Machines: the same three steps (torque_nm and rotation_speed_rpm above 0), then product_type as a number, L 0, M 1, H 2. Leave the other gaps, such as lot_frontage_m: the imputer fills them from the training rows only. '
             'These problems were added on purpose, and the notebook says so. Today: 2,935 houses become 2,913, and 10,012 machines become 9,984. ')
SPLIT = (10, 'The note "Training, validation and test sets". Class 3 slide 23 (train-test contamination) and slide 14 (the test set stays sealed).',
         'Four given lines per table: houses_test = houses.sample(frac=0.2, random_state=29), houses_rest = houses.drop(houses_test.index), houses_valid = houses_rest.sample(frac=0.25, random_state=29), houses_train = houses_rest.drop(houses_valid.index); the same for machines. '
         'That is 60, 20 and 20 percent. The seed makes the random choice repeat, so everyone gets the same rows; the project uses 17. The test set is used once, at the end: if we chose or tuned on it, its score would look better than the truth. Check: 1,748, 582 and 583 houses; 5,990, 1,997 and 1,997 machines.',
         'Task 2: store the six sets (2 marks)')
TASK3_SAY = ('Every number learned from data comes from houses_train only: the imputation medians and the baseline mean. make_pipeline(SimpleImputer(strategy="median"), model) learns them in fit and reuses them in predict. '
             'The marking checks for leakage with extreme rows in valid. RMSE needs the square root. The tree keeps random_state=17. Today: baseline about 58,789, linear 22,005, tree 27,785 USD. ')
ONEHOT = ('Task 3b is a comparison only, never part of choose_model. A model needs numbers, so one-hot encoding turns a text column into one 0 or 1 column per category: neighbourhood NAmes becomes a 1 in neighbourhood_NAmes. '
          'The categories are learned from houses_train only, like the medians. handle_unknown="ignore" gives a category train never saw all zeros instead of an error. Copy the recipe from the task. Today about 17,800 USD against 22,005 for linear: the text columns help.')
TASK5 = ('chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae}). The rule is in Setup: MAE at most 25,000 USD and time at most 50 ms, then the smallest MAE. Today it picks linear. The test set never helps to choose.')
TASK6 = ('Only now, after the choice, use the test rows, once. Refit the chosen model on houses_train and houses_valid together and score houses_test (test_mae); refit the warning model on machines_train and machines_valid together and score machines_test at 0.5 (test_recall). '
         'Reading the test rows before the choice costs marks. Whatever comes out, you report it. Today: test MAE about 20,135 USD, test recall 0.19.')


def finish(m):
    return (m,
            'Runtime, then Restart session and run all, on the projector. Ctrl+S. Then the entry page: Check my work, and I have finished.',
            'There is no Submit button. Nothing is submitted. At your deadline editing stops and your work is collected: the last save, or the newest 5-minute backup if it is newer. '
            'Restart and run all, fix the first failing cell first, press Ctrl+S. Then Check my work on the entry page. It runs your saved notebook from the top and says whether it runs, whether every result and MEMO are there, and whether it is your issued notebook. No mark. '
            'I have finished stops editing in the project, so press it only when you are done.',
            'Watch: restart and run all, Ctrl+S, Check my work and its result (one to three minutes), then I have finished.')


def friday_blocks():
    return [ENTRY, SETUP, PLAIN,
            (25, TASK1_SHOW,
             TASK1_SAY + 'Write every rule, even if this file would pass without it: the hidden raw tables have problems added. Chart 1: living_area_m2 across, sale price up, a title, both axis names, USD in the y label.',
             'Task 1: store houses, machines, Chart 1 (6 + 1 marks)'),
            SPLIT,
            (25, 'The note "Fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 21 (MAE, MSE, RMSE).',
             TASK3_SAY + 'Chart 2: the three MAE values as bars, with the unit.',
             'Task 3: the three _pred, _mae and _rmse results, Chart 2 (three models 6, MAE and RMSE 3, no leakage 2, chart 1)'),
            BREAK,
            (10, 'The note "One-hot encoding" and the recipe in Task 3b.', ONEHOT, 'Task 3b: store encoded_pred, encoded_mae (2 marks)'),
            (15, 'The note on logistic regression. Class 2 slides 13, 19, 20 and 21 (logistic regression, confusion matrix, precision, recall).',
             'You had this in Class 2. A warning is failure 1, about 3 rows in 100. The probability is predict_proba(X)[:, 1]; warn when it is >= 0.5. confusion_matrix(..., labels=[0, 1]).ravel() gives tn, fp, fn, tp in that order. '
             'Precision: of the warnings raised, how many were right. Recall: of the real failures, how many we caught. A zero count gives 0. Today: TP 10, FP 6, FN 58, precision 0.63, recall 0.15. Most failures are missed at 0.5. The project keeps 0.5; say it in the memo.',
             'Task 4: store warning_proba, tp, fp, fn, tn, precision, recall (3 marks)'),
            (5, 'The Task 5 line.', TASK5, 'Task 5: store chosen_model'),
            (10, 'The note "Use the test set once, then stop". Class 3 slide 14 again, and slide 27 (the checklist).', TASK6,
             'Task 6: store test_mae, test_recall (2 marks)'),
            (10, 'The MEMO cell and its table of fields.',
             'Every field is checked by computer. Copy your own numbers with at least two decimals. For limits, pick the three statements that are true limits of this study. Write the two answers in your own words, 8 to 80 words each.',
             'Task 7: fill in MEMO (15 marks)'),
            finish(25)]


def tuesday_blocks():
    return [ENTRY, SETUP, PLAIN,
            (20, TASK1_SHOW,
             TASK1_SAY + 'I write all of it on the projector. Chart 1 if time allows.',
             'Task 1: houses, machines (Chart 1 if time allows)'),
            SPLIT,
            (20, 'The note "Fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 33 (the pipeline).',
             TASK3_SAY + 'Chart 2 if time allows.',
             'Task 3: the three _pred, _mae and _rmse results (Chart 2 if time allows)'),
            BREAK,
            (5, 'The note "One-hot encoding" and the recipe in Task 3b.', ONEHOT, 'Task 3b: store encoded_pred, encoded_mae (2 marks)'),
            (30, 'The note on logistic regression in the rehearsal. Class 2 slides 12 and 13 (sigmoid, score, probability), slide 10 (standard deviation, for StandardScaler), slide 19 (confusion matrix), slides 20 and 21 (precision, recall). The board for the 2 by 2 table.',
             'You have not had Class 2, so this is the new part. About 8 minutes: logistic regression adds up the weighted features into a score, and the sigmoid turns the score into a probability between 0 and 1; StandardScaler puts the features on one scale first. '
             'About 10 minutes: the confusion matrix on the board. A warning before a real failure is TP, a false alarm is FP, a missed failure is FN, a quiet machine left quiet is TN. '
             'About 7 minutes: precision is TP / (TP + FP), recall is TP / (TP + FN). Today: TP 10, FP 6, FN 58 give precision 10 / 16 = 0.63 and recall 10 / 68 = 0.15. Failures are rare (3 in 100), so most are missed at 0.5. '
             'About 5 minutes: I write Task 4 on the projector, with >= 0.5 and the ravel order tn, fp, fn, tp.',
             'Task 4: store warning_proba, tp, fp, fn, tn, precision, recall (3 marks)'),
            (15, 'The Task 5 line, then the note "Use the test set once, then stop" and Class 3 slide 14.', TASK5 + ' ' + TASK6,
             'Tasks 5 and 6: store chosen_model, then test_mae, test_recall'),
            (10, 'The MEMO cell and its table of fields. I do not fill it in.',
             'Every field is checked by computer. Copy your own numbers with at least two decimals. For limits, pick the three statements that are true limits of this study. I fill in the first fields to show the format.',
             'Task 7: how MEMO is marked'),
            finish(25)]


HOME_3112 = [
    ['Task 1: the cleaning rules and what a good chart needs', 'Class 1 slide 11 (removing rows we cannot trust), Class 3 slide 26 (target leakage). Your Week 7 chart notes: title, both axis names, the unit.'],
    ['Task 3: MAE and RMSE, and why RMSE punishes big errors', 'Class 1 slides 21 and 23 (MAE, MSE, RMSE).'],
    ['Task 3b: one-hot encoding', 'Your notes from the Task 3b demonstration.'],
    ['Task 4: logistic regression, the confusion matrix, precision and recall', 'Class 2 slides 12, 13, 19, 20 and 21. Slides 22 to 31 (the cost table, choosing a threshold, ROC) are not in the project: skip them.'],
    ['Task 7: why the test set is opened once; the MEMO fields', 'Class 3 slides 14 and 27 (the sealed test set, the checklist).'],
    ['The entry steps and finishing', 'Class 3 slide 38 (enter, work, finish), and your notes from today.'],
]

TEST1 = [
    ['The notebook did not run from the top: cells out of order, a name defined in a deleted cell, one early error.',
     'Check my work runs the saved notebook from the top and names the first cell that stopped. Each task is also re-run on its own, so one broken task no longer costs the next.',
     'Restart session and run all, Ctrl+S, then Check my work. Fix the first error first.'],
    ['The data file uploaded again, so Colab read "engineering_data (1).csv".',
     'The data is inside Setup: run me first. Nothing to upload or download.',
     'After a restart, run Setup again.'],
    ['A required name changed or retyped.',
     'Results are found by the names in each Store line. A near name still counts.',
     'Use the exact names. Your own extra names and cells are fine.'],
    ['A chart with no axis name or unit.',
     'Charts, 2 marks.',
     'Title, both axis names, the unit (USD) in the y label.'],
    ['A method without brackets, or a typed number instead of a calculated one.',
     'Each task is re-run on hidden inputs, so a typed number fails.',
     'Calculate every result from the task inputs. Print it and read it.'],
    ['Started late, or no time left to submit; work lost before submitting.',
     'No Submit step. Work is collected at the deadline: the last save or the newest 5-minute backup. The email is typed twice and can be fixed once in 15 minutes.',
     'Start by Wednesday 20:59. Work only in the issued notebook, never Save a copy. Ctrl+S now and then.'],
]


def build(code):
    co = C.COHORTS[code]
    tue = code == 'CML3112'
    d = new_doc(f'Revision class, {code}', 'IUEA Machine Learning for Engineers')
    title(d, f'Revision class, {code}, {DAY[code]}',
          f'My working notes. {co["slot"]}, {co["room"]}. The rehearsal, worked live. Keep private.')
    h2(d, 'What today is for', 0)
    intro = ('Class 3 is not taught as a lecture. Today we work through the project rehearsal: the project\'s exact tasks, files and result names, with one change, the split uses random_state=29, so the numbers differ from the project\'s. '
             'Two files: Ames house sales (real, De Cock 2011) for the price question, and AI4I 2020 machine records (synthetic, UCI, CC BY 4.0) for the warning question. '
             'I teach the ideas as they come up: a random split with a seed and why the test set is opened once (Task 2), imputation fitted on the training rows only (Task 3), one-hot encoding (Task 3b, briefly), and target leakage, why the failure-type columns are dropped (Task 1). ')
    if tue:
        para(d, intro + 'This cohort has had Class 1 but not Class 2, so logistic regression, the confusion matrix, precision and recall are taught inside Task 4, about 30 minutes. Some parts are left for home (list below).', 10, after=4)
    else:
        para(d, intro + 'This cohort had Class 2, so Task 4 is a short recap.', 10, after=4)
    para(d, 'The project: online, Monday 23 November 00:00 to Wednesday 25 November 23:59, Kampala time, 3 hours from Start. Part A 30 (clean 6, charts 2, split 2, three models 6, MAE and RMSE 3, no leakage 2, warning at 0.5 3, test set once 2, results, seed and MEMO present 2, Task 3b text columns 2) and Part B memo 15. Plain code under each task, one supplied cell (Setup: run me first), no Submit: work is collected at the deadline. No cross-validation, no cost table, no threshold choice.', 10, after=4)

    h2(d, 'Before class')
    bullets(d, ['The rehearsal is open until Sunday 22 November 23:59, for the demo numbers only (26/DEMO/001/LECTURER in class, 26/SMOKE/001/TEST for my own checks). Students cannot open it, so I do not post the rehearsal link.',
                'Class list loaded in the collector. Type one registration number from this class on the entry page and check that the name shows.',
                'My own check with 26/SMOKE/001/TEST, not the class demo number (each number keeps its own 3-hour clock): Start, Open my project in Colab, the deadline at the top, Setup shows the clock and "Automatic backup sent", Check my work answers in one to three minutes. Screenshots kept in case the network fails.',
                'Support hours (08:00 to 20:00 each day of the window) confirmed before I say them.',
                'Decks open: Class 3 at slide 37, ' + ('Class 2 at slide 10, Class 1 at slide 21.' if tue else 'Class 2 at slide 13, Class 1 at slide 21.'),
                'My worked copy of the rehearsal ready, for the projector only. I do not post it.'], mark='[  ]')

    h2(d, 'The run sheet (180 minutes)')
    rows = clock(tuesday_blocks() if tue else friday_blocks())
    grid(d, rows, [1.2, 1.0, 4.4, 6.8, 4.0], header=['Starts', 'Min', 'What to show', 'What to say', 'Rehearsal task'], size=8.5, label_cols=(0,))
    para(d, 'Students watch; only I open the rehearsal. It uses the same entry page and notebook as the project, so every step they see is the one they will do on Monday. Nothing is locked or marked.', 9.5, italic=True, before=4, after=4)

    if tue:
        h2(d, 'Left for home, with the slides to read')
        grid(d, HOME_3112, [8.4, 9.0], header=['Rehearsal task', 'Slides to read'], size=9, label_cols=())

    h2(d, 'Six things that went wrong in Practical Test 1, and what protects them now')
    para(d, 'Say them once at the start and once in the last 25 minutes.', 10, after=3)
    grid(d, TEST1, [5.6, 6.2, 5.6], header=['What went wrong in Test 1', 'What the project does now', 'What I tell them'], size=9, label_cols=())

    h2(d, 'Also in this project')
    bullets(d, ['0.5 itself is a warning: use >=.', 'random_state=17 on the tree.', 'Split only with the four given lines: random_state=29 today, 17 in the project. A cell must finish in under 30 seconds.', 'The failure-type columns never go into the warning model.', 'open_test_set once, after choose_model.', 'Task 3b is a comparison only: it never goes into choose_model.', 'Editing Setup changes nothing: the marking puts the original back.'])

    h2(d, 'After class')
    bullets(d, ['Post on the class channel: the project entry link, the window, the support hours and ' + ('the list of home tasks with the slides to read.' if tue else 'the Class 3 slides to read again (14, 23, 24, 25, 26, 27).'),
                'Do not post my worked copy.',
                'Note any question I could not answer and answer it on the channel the same day.'])
    path = OUT / f'{FILES[code]}.docx'
    save(d, path)
    return path


def main():
    lo = '-env:UserInstallation=file://' + str(Path(tempfile.gettempdir()) / 'iuea_second_half_lo')
    lo_fonts.seed(lo)
    for code in ('CML3112', 'CML3113', 'CML3111'):
        path = build(code)
        subprocess.run(['soffice', lo, '--headless', '--convert-to', 'pdf', '--outdir', str(OUT), str(path)], capture_output=True)


if __name__ == '__main__':
    main()
