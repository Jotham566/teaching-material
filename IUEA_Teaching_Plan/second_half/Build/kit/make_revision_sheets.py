"""Revision class run sheets (Week 10, 17 and 20 November 2026): one Word file and PDF per cohort. python3 kit/make_revision_sheets.py

Class 3 is not taught as a lecture. The revision class works through the project rehearsal
(Project/Rehearsal/<code>/ML_PROJECT_rehearsal.ipynb) live and teaches the Class 3 ideas, and for CML3112 the Class 2 ideas,
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
ONLINE = (20,
          'Class 3 deck, slides 37 to 39 (the project). The course entry link on the projector. The Check my notebook cell at the end of the rehearsal. My dry-run notebook with the demo registration.',
          'The window is Monday 00:00 to Wednesday 23:59, Kampala time, and your 3 hours start when you press Start. Start by Wednesday 20:59 or you lose time. '
          'You type your registration number, check that the name is yours, press Start, work, run Check my notebook, then Submit test and keep the receipt code. You see your mark after the window closes.',
          'Everyone opens the rehearsal in Colab (File, Save a copy in Drive) and runs the identity cell and the setup cell. '
          'Practice check: I run Check my notebook on the empty rehearsal so you see what TODO lines look like. Practice submit: I press Submit test on my demo notebook and we read the receipt and the checks together.')
SETUP = (10,
         'The "Your data" table in the rehearsal, and the first rows printed by the setup cell.',
         'Every row is 15 minutes of one steel plant meter in 2018. Today we predict the lagging reactive power in kVarh; in the project you predict the energy used in kWh. '
         'CO2 is calculated from the energy used, so it gives the answer away. That is target leakage, and Task 1 removes it.',
         'Setup cells, "Your data"')
BREAK = (10, 'Nothing.', 'Ten minutes. Leave Colab open; your variables stay as long as the session stays connected.', 'Break')
CHECK = (25,
         'Runtime, then Restart session and run all, on my copy. Then Check my notebook. Then the entry link again.',
         'Unfinished is fine today. The point is that the check runs and you can read what it says. Fix the first failing cell first, because one early error stops every cell after it. '
         'Then open the entry link, type your registration number and check your name. If the page says it is not open yet, that is expected until Monday.',
         'Everyone: restart and run all, File then Save, run Check my notebook and read its output. Practice submit: entry link, registration number, name check. I walk the room and look at each screen.')


def friday_blocks():
    return [ONLINE, SETUP,
            (25, 'Task 1. Print the dates around midnight: 01/01/2018 23:45 is followed by 01/01/2018 00:00. Then the 7 November reading that is all zeros.',
             'The 00:00 reading belongs to the end of the day, so add one day to its timestamp. Return a copy and never change the list you were given. '
             'Write every rule, even the ones this file does not need, because the marking runs your function on other rows. For Chart 1: a title, both axis names, the unit in the y label, and chart_1 = figure before plt.show().',
             'Task 1: clean_rows and Chart 1 (7 + 1 marks in the project)'),
            (15, 'The self-study note "why split by month". Class 3 slide 23 (train-test contamination) and slide 14 (the test set stays sealed).',
             'Readings 15 minutes apart are near copies. A random split puts copies in both sets and lets the model learn from later days, so the score looks better than next month will be. '
             'So we split by month: train January to August, check September and October, keep November and December closed. Look the timestamps up in a set: a list takes minutes, and the marking stops a cell after 30 seconds.',
             'Task 2: time_split (2 marks)'),
            (30, 'The note "fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 21 (MAE, MSE, RMSE).',
             'Every number learned from data comes from the training rows only: the medians and the baseline mean. make_pipeline does it inside fit. A median taken from all the rows first is leakage, and the marking checks for it with extreme rows. '
             'RMSE needs the square root. The tree keeps random_state=17 so everyone gets the same numbers.',
             'Task 3: fit_predict_regression, regression_errors, the validation results, Chart 2 (6 + 3 + 2 + 1 marks)'),
            BREAK,
            (15, 'The note on logistic regression. Class 2 slides 19 to 21 (confusion matrix, precision, recall).',
             'You had this in Class 2. Here the threshold is fixed at 0.5 and nobody chooses it, and 0.5 itself is a warning, so use >=. confusion_matrix(...).ravel() gives tn, fp, fn, tp in that order. '
             'Precision: of the warnings raised, how many were right. Recall: of the real high readings, how many we caught.',
             'Task 4: warning_probabilities and classification_scores (3 marks)'),
            (10, 'The supplied model-choice cell (Do not edit).',
             'The rule is given. You build candidate_table from your own validation MAE and LATENCY_MS, then call choose_model. The test set never helps to choose.',
             'Task 5: candidate_table and choose_model (no marks of its own)'),
            (10, 'The note "open the test set once, then refit". Class 3 slide 14 again, and slide 27 (the checklist).',
             'Choose first, then open the test set once. The supplied cell refits your functions on January to October and scores November and December. A second call costs marks, more with a different model. Whatever comes out, you report it.',
             'Task 6: open_test_set, one call (2 marks)'),
            (10, 'The MEMO form and the memo self-check.',
             'Every field is checked by computer. Copy your numbers from the notebook with at least two decimals. For limits, pick the three statements that are true limits of this study. Write the two answers in your own words, 8 to 80 words each.',
             'Task 7: Part B memo form (15 marks)'),
            CHECK]


def tuesday_blocks():
    return [ONLINE, SETUP,
            (20, 'Task 1. Print the dates around midnight: 01/01/2018 23:45 is followed by 01/01/2018 00:00. Then the 7 November reading that is all zeros.',
             'The 00:00 reading belongs to the end of the day, so add one day to its timestamp. CO2 goes. Return a copy and never change the list you were given. '
             'We write the loop together up to the date fix and the repeat check. You finish the impossible-value rules and Chart 1 at home.',
             'Task 1: clean_rows (in class up to the date fix and repeats)'),
            (15, 'The self-study note "why split by month". Class 3 slide 23 (train-test contamination) and slide 14 (the test set stays sealed).',
             'Readings 15 minutes apart are near copies. A random split puts copies in both sets and lets the model learn from later days, so the score looks better than next month will be. '
             'So we split by month: train January to August, check September and October, keep November and December closed. Look the timestamps up in a set: a list takes minutes, and the marking stops a cell after 30 seconds.',
             'Task 2: time_split (2 marks)'),
            (25, 'The note "fit on the training rows only". Class 3 slides 24 and 25 (the pipeline rule). Class 1 slide 33 (the pipeline).',
             'Every number learned from data comes from the training rows only: the medians and the baseline mean. make_pipeline does it inside fit. A median taken from all the rows first is leakage, and the marking checks for it. '
             'RMSE needs the square root. The tree keeps random_state=17.',
             'Task 3: fit_predict_regression, regression_errors, validation results (Chart 2 at home)'),
            BREAK,
            (30, 'Class 2 slides 12 and 13 (sigmoid, score, probability), slide 10 (standard deviation, for StandardScaler), slide 19 (confusion matrix), slides 20 and 21 (precision, recall). The board for the 2 by 2 table.',
             'You have not had Class 2, so this is the new part. About 8 minutes: logistic regression adds up the weighted features into a score, and the sigmoid turns the score into a probability between 0 and 1; StandardScaler puts the features on one scale first. '
             'About 10 minutes: the confusion matrix on the board. A warning that was right is TP, a false alarm is FP, a missed high reading is FN, a quiet reading left quiet is TN. '
             'About 7 minutes: precision is TP / (TP + FP), recall is TP / (TP + FN). Illustrative counts, invented: TP 8, FP 2, FN 4 give precision 8 / 10 = 0.80 and recall 8 / 12 = 0.67. '
             'About 5 minutes: we write classification_scores together, with >= 0.5 and the ravel order tn, fp, fn, tp.',
             'Task 4: warning_probabilities and classification_scores (3 marks)'),
            (15, 'The supplied model-choice cell, then the note "open the test set once, then refit" and Class 3 slide 14.',
             'The rule is given: build candidate_table from your own validation MAE and LATENCY_MS and call choose_model. Then open the test set once. '
             'The supplied cell refits on January to October and scores November and December. A second call costs marks. The test set never helps to choose.',
             'Tasks 5 and 6: choose_model, then open_test_set once'),
            (10, 'The MEMO form and the memo self-check. I do not fill it in.',
             'Every field is checked by computer. Copy your own numbers with at least two decimals. For limits, pick the three statements that are true limits of this study. You fill it in at home and run the memo self-check.',
             'Task 7: how the form is marked (filled in at home)'),
            CHECK]


HOME_3112 = [
    ['Task 1: the impossible-value rules (negative values, power factors outside 0 to 100, NSM outside 0 to 85500) and Chart 1', 'Class 1 slide 11 (removing rows we cannot trust). Your Week 7 chart notes: title, both axis names, the unit.'],
    ['Task 3: Chart 2, and RMSE until the self-check passes', 'Class 1 slides 21 and 23 (MAE, MSE, RMSE).'],
    ['Task 4: read the self-study note again and do both functions until the self-check passes', 'Class 2 slides 12, 13, 19, 20 and 21. Slides 22 to 31 (the cost table, choosing a threshold, ROC) are not in the project: skip them.'],
    ['Task 7: fill in the MEMO form, run the memo self-check', 'Class 3 slides 14 and 27 (the sealed test set, the checklist).'],
    ['The whole notebook: Restart session and run all, then Check my notebook, until no cell fails', 'Class 3 slide 38 (enter, check, submit).'],
]

TEST1 = [
    ['The notebook did not run from the top: cells run out of order, a name defined in a deleted cell, or one early error that stopped every cell after it.',
     'Every item. The marking runs the notebook from the top in a fresh Python.',
     'Restart session and run all, then Check my notebook. Fix the first error first.'],
    ['The data file uploaded again, so Colab read a copy called "engineering_data (1).csv".',
     'Setup. The steel file is inside the setup cell.',
     'Never upload anything. After a reset, run the setup cell again.'],
    ['A required name changed: a function or variable renamed or retyped.',
     'The functions are called by name on hidden rows.',
     'Keep every name exactly as printed. Your own extra cells are fine.'],
    ['A chart with no axis name or unit, or a later plt call that replaced the chart.',
     'Charts, 2 marks.',
     'Title, both axis names, the unit in the y label, and chart_1 = figure before plt.show().'],
    ['A method without brackets (.median instead of .median()), or a later cell that overwrote a right answer.',
     'Results and functions.',
     'Print each result and read it. Do not reuse a required name for something else.'],
    ['Started late, or left no time to submit.',
     'The 3 hours run from Start and end at Wednesday 23:59 at the latest.',
     'Start by Wednesday 20:59. Leave 25 minutes for the check and the submit. Submit early and again later: up to five times, the latest on time counts.'],
]


def build(code):
    co = C.COHORTS[code]
    tue = code == 'CML3112'
    d = new_doc(f'Revision class, {code}', 'IUEA Machine Learning for Engineers')
    title(d, f'Revision class, {code}, {DAY[code]}',
          f'My working notes. {co["slot"]}, {co["room"]}. The rehearsal notebook, worked live. Keep private.')
    h2(d, 'What today is for', 0)
    if tue:
        para(d, 'Class 3 is not taught as a lecture. Today we work through the project rehearsal (same steel file, different target: lagging reactive power, kVarh, warning at 40 kVarh) and I teach the Class 3 ideas as they come up: why we split by month, why a random split leaks, fitting on the training rows only, and opening the test set once and refitting. '
                'This cohort has had Class 1 but not Class 2, so logistic regression, the confusion matrix, precision and recall are taught inside Task 4, about 30 minutes. Some parts are left for home (list below).', 10, after=4)
    else:
        para(d, 'Class 3 is not taught as a lecture. Today we work through the project rehearsal (same steel file, different target: lagging reactive power, kVarh, warning at 40 kVarh) and I teach the Class 3 ideas as they come up: why we split by month, why a random split leaks, fitting on the training rows only, and opening the test set once and refitting. '
                'This cohort had Class 2, so Task 4 is a short recap.', 10, after=4)
    para(d, 'The project: online, Monday 23 November 00:00 to Wednesday 25 November 23:59, Kampala time, 3 hours from Start. Part A 30 (clean 7, charts 2, split 2, three models 6, MAE and RMSE 3, no leakage 2, warning question 3, test set once 2, results, seed and functions 3) and Part B memo 15. No cross-validation, no cost table, no threshold choice.', 10, after=4)

    h2(d, 'Before class')
    bullets(d, [f'Rehearsal released: Project/Rehearsal/{code}/ML_PROJECT_rehearsal.ipynb sent to the class the same way as the class packs, before the class, so everyone can open it in Colab in the room. Ask them to download it before they come in.',
                'Links shared: the course entry link and its QR code (Project/deploy/ML_PROJECT_ENTRY_LINKS.md and deploy/qr/) posted on the class channel. The page should say the project is not open yet.',
                'Class list loaded in the collector workbook. Type one registration number from this class on the entry page and check that the name shows.',
                'Check cell tested in real Colab: open the rehearsal from Drive, Restart session and run all, run Check my notebook. It should finish in one to three minutes. Do the same on my own worked copy.',
                'Dry run done (DEPLOYMENT_STEPS.md step 6) so I can show a real Submit test with the demo registration. Keep a screenshot of the receipt and the instant checks in case the network fails.',
                'Support hours (08:00 to 20:00 each day of the window) confirmed before I say them.',
                'Decks open: Class 3 at slide 37, ' + ('Class 2 at slide 10, Class 1 at slide 21.' if tue else 'Class 2 at slide 19, Class 1 at slide 21.'),
                'My worked copy of the rehearsal ready, for the projector only. I do not post it: the rehearsal says no solved walk-through is given.'], mark='[  ]')

    h2(d, 'The run sheet (180 minutes)')
    rows = clock(tuesday_blocks() if tue else friday_blocks())
    grid(d, rows, [1.2, 1.0, 4.4, 6.8, 4.0], header=['Starts', 'Min', 'What to show', 'What to say', 'Rehearsal task'], size=8.5, label_cols=(0,))
    para(d, 'About the practice submit. The rehearsal has no Submit cell, and the entry page opens nothing before Monday. So the practice submit is: everyone runs Check my notebook and does the entry page up to the name check, and I show one real Submit test from my dry-run notebook on the projector.', 9.5, italic=True, before=4, after=4)

    if tue:
        h2(d, 'Left for home, with the slides to read')
        grid(d, HOME_3112, [8.4, 9.0], header=['Rehearsal task', 'Slides to read'], size=9, label_cols=())

    h2(d, 'Six things students got wrong in Practical Test 1')
    para(d, 'The Test 1 marking had to be re-run fairly for each of these. Say them once at the start and once in the last 25 minutes.', 10, after=3)
    grid(d, TEST1, [6.6, 4.6, 6.2], header=['What went wrong in Test 1', 'Where it bites in the project', 'What I tell them'], size=9, label_cols=())

    h2(d, 'Also in this project')
    bullets(d, ['0.5 itself is a warning: use >=.', 'random_state=17 on the tree, or the reproducibility mark goes.', 'Look timestamps up in a set, never a list.', 'The test set is opened once, with the supplied cell, after the choice.', 'Never type a result in: compute it.'])

    h2(d, 'After class')
    bullets(d, ['Post on the class channel: the entry link again, the window, the support hours and ' + ('the list of home tasks with the slides to read.' if tue else 'the Class 3 slides to read again (14, 23, 24, 25, 27).'),
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
