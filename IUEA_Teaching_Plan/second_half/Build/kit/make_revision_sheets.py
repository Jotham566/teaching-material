"""Revision class run sheets (Week 10, 17 and 20 November 2026): one Word file and PDF per cohort. python3 kit/make_revision_sheets.py

Class 3 is not taught as a lecture. The revision class works through the project rehearsal
(Project/Rehearsal/<code>/ML_PROJECT_rehearsal.ipynb, opened through the rehearsal entry link) live and teaches the Class 3 ideas, and for CML3112 the Class 2 ideas,
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
ENTRY = (20,
         'The rehearsal entry link and its QR code on the projector. Class 3 deck, slides 37 to 39 (the project). My own rehearsal attempt with the demo registration.',
         'Type your registration number and check the name is yours, then tick This is me. Type your Google email twice. It must be the account you are signed into in Colab, top right of colab.research.google.com: the notebook is shared with that account only. '
         'Press Start. The big countdown on the page is your 3 hours. A typo in the email can be fixed once, on the page, in the first 15 minutes. Then Open my project in Colab. Never use Save a copy. '
         'In the project the window is Monday 00:00 to Wednesday 23:59, Kampala time. Start by Wednesday 20:59 or you lose time.',
         'Everyone: rehearsal entry link, registration number, This is me, email twice, Start, Open my project in Colab. I walk the room and check that each Colab shows the right account.')
SETUP = (10,
         'The collapsed cell "Setup: run me first". The line it prints, then the countdown line under it.',
         'Run Setup first, and again after any restart. You do not open it or edit it: the marking always uses the original. The data is inside it, so nothing is uploaded or downloaded. '
         'After every cell a line shows the time left and your deadline, for example "2:47 left (deadline 14:05 Kampala)". Under 30 minutes it says Press Ctrl+S. A grey line says when the last automatic backup was sent. '
         'Every row is 15 minutes of one steel plant meter in 2018. Today we predict the lagging reactive power in kVarh; in the project you predict the energy used in kWh.',
         'Setup: run me first, then read the countdown line')
PLAIN = (5,
         'The Task 1 heading: the Input and Store line, then the empty cell "# Your code here. Store: clean".',
         'Each task names its inputs and the results to store. Write plain code under it, in as many cells as you like. No functions needed. Store the result under the exact name, then print it and read it. '
         'Each task is re-run on its own with hidden versions of its inputs, so use only those inputs and the setup names (TARGET, FEATURES, LIMIT). Calculate, never type a number.',
         'How to write an answer')
BREAK = (10, 'Nothing.', 'Ten minutes. Leave Colab open; your variables stay as long as the session stays connected.', 'Break')


def finish(m):
    return (m,
            'Runtime, then Restart session and run all, on my copy. Ctrl+S. Then the entry page: Check my work, and I have finished.',
            'There is no Submit button. Nothing is submitted. At your deadline editing stops and your work is collected: the last save, or the newest 5-minute backup if it is newer. '
            'Restart and run all, fix the first failing cell first, press Ctrl+S. Then Check my work on the entry page. It runs your saved notebook from the top and says whether it runs, whether every result and MEMO are there, and whether it is your issued notebook. No mark. '
            'I have finished stops editing in the project. Today nothing is locked, so you can keep working after you press it.',
            'Everyone: restart and run all, Ctrl+S, Check my work and read the result (one to three minutes), then I have finished. I look at each screen.')


def friday_blocks():
    return [ENTRY, SETUP, PLAIN,
            (25, 'Task 1. Print the dates around midnight: 01/01/2018 23:45 is followed by 01/01/2018 00:00. Then the 7 November reading that is all zeros.',
             'Start with clean = raw.copy(), so raw never changes. The 00:00 reading belongs to the end of the day, so add one day to its timestamp. CO2 goes: it is calculated from the energy, so it gives the answer away (target leakage). '
             'Write every rule, even the ones this file does not need: the hidden raw table has problems added. Chart 1: title, both axis names, the unit in the y label.',
             'Task 1: store clean, Chart 1 (7 + 1 marks in the project)'),
            (10, 'The note "Split by month". Class 3 slide 23 (train-test contamination) and slide 14 (the test set stays sealed).',
             'Readings 15 minutes apart are near copies. A random split puts copies in both sets, so the score looks better than next month will be. '
             'Train January to August, validate September and October, keep November and December closed.',
             'Task 2: store train and valid (2 marks)'),
            (30, 'The note "Fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 21 (MAE, MSE, RMSE).',
             'Every number learned from data comes from train only: the medians and the baseline mean. make_pipeline does it inside fit. The marking checks for leakage with extreme rows in valid. '
             'RMSE needs the square root. The tree keeps random_state=17 so everyone gets the same numbers.',
             'Task 3: the three _pred, _mae and _rmse results, Chart 2 (6 + 3 + 2 + 1 marks)'),
            BREAK,
            (15, 'The note on logistic regression. Class 2 slides 19 to 21 (confusion matrix, precision, recall).',
             'You had this in Class 2. The threshold is fixed at 0.5 and 0.5 itself is a warning, so use >=. confusion_matrix(..., labels=[0, 1]).ravel() gives tn, fp, fn, tp in that order. '
             'Precision: of the warnings raised, how many were right. Recall: of the real high readings, how many we caught. A zero count gives 0.',
             'Task 4: store warning_proba, tp, fp, fn, tn, precision, recall (3 marks)'),
            (5, 'The Task 5 line.',
             'One line: chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae}). The rule is in Setup. The test set never helps to choose.',
             'Task 5: store chosen_model'),
            (10, 'The note "Open the test set once, then refit". Class 3 slide 14 again, and slide 27 (the checklist).',
             'Choose first, then test_rows = open_test_set(chosen_model), once. Refit the chosen model and the warning model on train and valid together, then score test_rows. '
             'A second call prints a warning and costs marks. Whatever comes out, you report it.',
             'Task 6: store test_rows, test_mae, test_recall (2 marks)'),
            (10, 'The MEMO cell and its table of fields.',
             'Every field is checked by computer. Copy your own numbers with at least two decimals. For limits, pick the three statements that are true limits of this study. Write the two answers in your own words, 8 to 80 words each.',
             'Task 7: fill in MEMO (15 marks)'),
            finish(30)]


def tuesday_blocks():
    return [ENTRY, SETUP, PLAIN,
            (20, 'Task 1. Print the dates around midnight: 01/01/2018 23:45 is followed by 01/01/2018 00:00. Then the 7 November reading that is all zeros.',
             'Start with clean = raw.copy(). The 00:00 reading belongs to the end of the day, so add one day to its timestamp. CO2 goes: it gives the answer away. '
             'We write it together up to the date fix and the repeats. You finish the impossible-value rules and Chart 1 at home.',
             'Task 1: store clean (in class up to the date fix and repeats)'),
            (10, 'The note "Split by month". Class 3 slide 23 (train-test contamination) and slide 14 (the test set stays sealed).',
             'Readings 15 minutes apart are near copies. A random split puts copies in both sets, so the score looks better than next month will be. '
             'Train January to August, validate September and October, keep November and December closed.',
             'Task 2: store train and valid (2 marks)'),
            (25, 'The note "Fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 33 (the pipeline).',
             'Every number learned from data comes from train only: the medians and the baseline mean. make_pipeline does it inside fit. The marking checks for leakage. '
             'RMSE needs the square root. The tree keeps random_state=17.',
             'Task 3: the three _pred, _mae and _rmse results (Chart 2 at home)'),
            BREAK,
            (30, 'The note on logistic regression in the rehearsal. Class 2 slides 12 and 13 (sigmoid, score, probability), slide 10 (standard deviation, for StandardScaler), slide 19 (confusion matrix), slides 20 and 21 (precision, recall). The board for the 2 by 2 table.',
             'You have not had Class 2, so this is the new part. About 8 minutes: logistic regression adds up the weighted features into a score, and the sigmoid turns the score into a probability between 0 and 1; StandardScaler puts the features on one scale first. '
             'About 10 minutes: the confusion matrix on the board. A warning that was right is TP, a false alarm is FP, a missed high reading is FN, a quiet reading left quiet is TN. '
             'About 7 minutes: precision is TP / (TP + FP), recall is TP / (TP + FN). Illustrative counts, invented: TP 8, FP 2, FN 4 give precision 8 / 10 = 0.80 and recall 8 / 12 = 0.67. '
             'About 5 minutes: we write Task 4 together, with >= 0.5 and the ravel order tn, fp, fn, tp.',
             'Task 4: store warning_proba, tp, fp, fn, tn, precision, recall (3 marks)'),
            (15, 'The Task 5 line, then the note "Open the test set once, then refit" and Class 3 slide 14.',
             'chosen_model = choose_model({...}) with your three validation MAEs: the rule is in Setup. Then test_rows = open_test_set(chosen_model), once. '
             'Refit on train and valid together and score test_rows. A second call prints a warning and costs marks. The test set never helps to choose.',
             'Tasks 5 and 6: store chosen_model, then test_rows, test_mae, test_recall'),
            (10, 'The MEMO cell and its table of fields. I do not fill it in.',
             'Every field is checked by computer. Copy your own numbers with at least two decimals. For limits, pick the three statements that are true limits of this study. You fill it in at home.',
             'Task 7: how MEMO is marked (filled in at home)'),
            finish(25)]


HOME_3112 = [
    ['Task 1: the impossible-value rules (negative values, power factors outside 0 to 100, NSM outside 0 to 85500) and Chart 1', 'Class 1 slide 11 (removing rows we cannot trust). Your Week 7 chart notes: title, both axis names, the unit.'],
    ['Task 3: Chart 2, and RMSE', 'Class 1 slides 21 and 23 (MAE, MSE, RMSE).'],
    ['Task 4: read the rehearsal note again and redo the task on your own', 'Class 2 slides 12, 13, 19, 20 and 21. Slides 22 to 31 (the cost table, choosing a threshold, ROC) are not in the project: skip them.'],
    ['Task 7: fill in MEMO', 'Class 3 slides 14 and 27 (the sealed test set, the checklist).'],
    ['The whole notebook: Restart session and run all, Ctrl+S, then Check my work on the entry page, until no cell fails', 'Class 3 slide 38 (enter, work, finish).'],
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
     'Title, both axis names, the unit in the y label.'],
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
    if tue:
        para(d, 'Class 3 is not taught as a lecture. Today we work through the project rehearsal (same steel file, different target: lagging reactive power, kVarh, warning at 40 kVarh) and I teach the Class 3 ideas as they come up: why we split by month, why a random split leaks, fitting on the training rows only, and opening the test set once and refitting. '
                'This cohort has had Class 1 but not Class 2, so logistic regression, the confusion matrix, precision and recall are taught inside Task 4, about 30 minutes. Some parts are left for home (list below).', 10, after=4)
    else:
        para(d, 'Class 3 is not taught as a lecture. Today we work through the project rehearsal (same steel file, different target: lagging reactive power, kVarh, warning at 40 kVarh) and I teach the Class 3 ideas as they come up: why we split by month, why a random split leaks, fitting on the training rows only, and opening the test set once and refitting. '
                'This cohort had Class 2, so Task 4 is a short recap.', 10, after=4)
    para(d, 'The project: online, Monday 23 November 00:00 to Wednesday 25 November 23:59, Kampala time, 3 hours from Start. Part A 30 (clean 7, charts 2, split 2, three models 6, MAE and RMSE 3, no leakage 2, warning question 3, test set once 2, results, seed and MEMO present 3) and Part B memo 15. Plain code under each task, one supplied cell (Setup: run me first), no Submit: work is collected at the deadline. No cross-validation, no cost table, no threshold choice.', 10, after=4)

    h2(d, 'Before class')
    bullets(d, [f'Rehearsal window opened in the collector for {code} (DEPLOYMENT_STEPS.md, the ML_REHEARSAL line), so the rehearsal entry link works in the room.',
                'Rehearsal entry link (Project/deploy/ML_PROJECT_ENTRY_LINKS.md, Rehearsal links) posted on the class channel the day before. Ask them to bring a laptop signed into the Google account they will use in Colab.',
                'Class list loaded in the collector. Type one registration number from this class on the entry page and check that the name shows.',
                'My own rehearsal attempt done with the demo registration: Start, Open my project in Colab, Setup prints the countdown line and "Automatic backup sent", Check my work answers in one to three minutes. Screenshots kept in case the network fails.',
                'Support hours (08:00 to 20:00 each day of the window) confirmed before I say them.',
                'Decks open: Class 3 at slide 37, ' + ('Class 2 at slide 10, Class 1 at slide 21.' if tue else 'Class 2 at slide 19, Class 1 at slide 21.'),
                'My worked copy of the rehearsal ready, for the projector only. I do not post it.'], mark='[  ]')

    h2(d, 'The run sheet (180 minutes)')
    rows = clock(tuesday_blocks() if tue else friday_blocks())
    grid(d, rows, [1.2, 1.0, 4.4, 6.8, 4.0], header=['Starts', 'Min', 'What to show', 'What to say', 'Rehearsal task'], size=8.5, label_cols=(0,))
    para(d, 'Nothing is submitted, today or in the project. The rehearsal runs the same entry page as the project, but nothing is locked or marked, so students can practise Check my work and I have finished and keep working afterwards.', 9.5, italic=True, before=4, after=4)

    if tue:
        h2(d, 'Left for home, with the slides to read')
        grid(d, HOME_3112, [8.4, 9.0], header=['Rehearsal task', 'Slides to read'], size=9, label_cols=())

    h2(d, 'Six things that went wrong in Practical Test 1, and what protects them now')
    para(d, 'Say them once at the start and once in the last 25 minutes.', 10, after=3)
    grid(d, TEST1, [5.6, 6.2, 5.6], header=['What went wrong in Test 1', 'What the project does now', 'What I tell them'], size=9, label_cols=())

    h2(d, 'Also in this project')
    bullets(d, ['0.5 itself is a warning: use >=.', 'random_state=17 on the tree.', 'Never split at random. A cell must finish in under 30 seconds.', 'open_test_set once, after choose_model.', 'Editing Setup changes nothing: the marking puts the original back.'])

    h2(d, 'After class')
    bullets(d, ['Post on the class channel: the project entry link, the window, the support hours and ' + ('the list of home tasks with the slides to read.' if tue else 'the Class 3 slides to read again (14, 23, 24, 25, 27).'),
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
