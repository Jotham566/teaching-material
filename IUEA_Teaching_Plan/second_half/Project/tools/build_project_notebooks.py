"""Build the project notebooks. python3 tools/build_project_notebooks.py [--require-forms]

Writes, for each cohort (CML3112, CML3113, CML3111):
  Notebooks/<cohort>/ML_PROJECT_student.ipynb             the marked notebook (guided TODO cells, self-checks, memo form, Test 1 submit cell); the data is inside it
  Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb            the unmarked rehearsal (same structure and file, another target, no submit cell)
  grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb the model solutions used to prove the grader (NEVER give to students)
  grader_spec/supplied_cell_hashes.json                    hashes of the three supplied cells and of every issued TODO cell (stubs), so an edited supplied
                                                           cell is noticed and an unedited stub never overwrites the student's own cell
The last two cells are supplied (tools/pipeline_cells.py): Check my notebook (optional self-help) and an information cell. There is no
Submit cell: the collection design of 14 November 2026 collects the issued Drive file at the deadline, or the newest on-time backup.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402
import pipeline_cells as PL  # noqa: E402

PLAN = PC.PLAN
ROOT = PLAN.parent
RULES = '''**Rules (the same rules as Practical Test 1).** Individual work, online, from anywhere. **Permitted resources:** your lecture slides, your lab notebooks from Classes 1 to 3, the revision guide, the cheatsheet and your own course notes. Write the code yourself.
**No AI or outside help:** do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not get answers from another person, collaborate or copy someone else's work.
**Understanding check:** after the window, any student may be asked, in an online call, to explain their submitted code or make a small change to it, without AI or another person's help. The copy checks and the identity checks run on every notebook.
**Declaration:** by submitting, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and change the code I submitted.'''


def cell(text, code=False, tags=None, form=False):
    d = dict(cell_type='code' if code else 'markdown', metadata={}, source=text.splitlines(True))
    if code:
        d.update(execution_count=None, outputs=[])
    if tags:
        d['metadata']['tags'] = tags
    if form:
        d['metadata']['cellView'] = 'form'
    return d


def load_forms(code, require):
    """The project no longer uses a Google Form. The notebook is ready to hand out when the lecturer has set up the collector and the
    gateway routes (deploy/SETUP_GITHUB_ACTIONS.md) and written tools/pipeline_ready.json. Returns (unused, unused, ready)."""
    ready = (HERE / 'pipeline_ready.json').exists()
    if require and not ready:
        raise SystemExit('The submission pipeline is not marked ready. Finish deploy/SETUP_GITHUB_ACTIONS.md, then create tools/pipeline_ready.json '
                         '(for example {"collector_deployed": "2026-11-20"}).')
    return '', {}, ready


def marks_text():
    """The Part A mark table in one sentence, read from the spec (project_contracts.PARTS), so a new blueprint needs only a rebuild."""
    words = {'clean': 'cleaning the real data', 'charts': 'two labelled charts', 'split': 'the split by month', 'regression': 'the baseline, linear regression and decision tree',
             'errors': 'MAE and RMSE', 'leakage': 'no leakage (imputation and the baseline mean fitted on the training rows only)',
             'warning': 'the warning question (probabilities, then the confusion matrix counts, precision and recall at 0.5)',
             'test': 'opening the test set once, after your choice, and its result',
             'results': 'your results on the file, the same answer every time (keep `random_state=17`) and every required function and the MEMO form being there'}
    parts = [f'{m} for {words.get(t, K.TITLES[t])}' for t, m in K.PARTS]
    return f'Of the {K.PART_A_MAX} Part A marks: ' + '; '.join(parts) + '.'


def intro_cell(code, mode, configured):
    MARKS_TEXT = marks_text()
    cfg = PC.CFGS['rehearsal' if mode == 'rehearsal' else 'exam']
    plan = '\n'.join(f'| {name} | {m} min |' for name, m in PC.TIME_PLAN)
    if mode == 'rehearsal':
        head = f'''# {code} Machine Learning: Engineering ML project, REHEARSAL (unmarked)
**This is a rehearsal. Nothing here is marked or submitted.** It has the same structure, the same task wording and the same kinds of check as the marked project, on the same steel plant file, but with a different target: here you predict **{cfg['what']}** ({cfg['unit']}), with its own warning limit. The marked project predicts the energy used (kWh). Your numbers here will not be the numbers you get in the project. Released {PC.REHEARSAL_TEXT[code]}. The project window {PC.WINDOW_TEXT}.

**How to use it.** Open it from the rehearsal entry link, exactly as you will open the project: type your registration number, confirm your name, press Start and click Open my project in Colab. It is your own copy in Drive and it saves itself. Work through it as if it were the real project, with a 3-hour timer if you can. Use the self-check cells, the Check my work button on the entry page, and I have finished when you are done. In the rehearsal nothing is locked and nothing is marked. A solved walk-through is not given: the point is that you can do it yourself.'''
    else:
        draft = '' if configured or mode == 'solution' else '> **DRAFT. The submission collector for this project is not set up yet. Do not hand this notebook out.**\n\n'
        head = f'''{draft}# {code} Machine Learning: Engineering ML project
**Part A: coded notebook (30 marks) and Part B: decision memo form (15 marks). Together 45 marks, scaled to 40 percent of the course. Online, 3 hours, individual work, marked automatically.**
**Window:** {PC.WINDOW_TEXT}. Your own 3 hours start when you press Start on the entry page and cannot be paused; the window's close is the last cutoff, so start by {PC.WINDOW['last_full_start']} to get the full 3 hours.'''
    return f'''{head}

This project uses only what you learned in Weeks 1 to 10 (up to Class 3). You work on real readings from a steel plant, `Steel_industry_data.csv` ({PC.SOURCE['plant']}, 2018, one reading every 15 minutes), and answer two questions: **Question 1** how much is {cfg['what']} ({cfg['unit']}) in months the model has never seen, and **Question 2** which readings should raise a warning. November and December are the test set and are opened **once**.

Data: {PC.CITATION}

## How to work
1. Fill in the identity cell below (in the issued notebook it is filled in for you; check it) and run it. Then run the supplied cell **Prepare the data and the libraries**. The data file is stored inside it, so you need no upload and no download.
2. Work from top to bottom. Replace each `TODO` and each `None`. Keep the function names, the argument order and the variable names exactly as printed. Run each cell and read what it prints. {PC.OWN_CELLS}
3. Run the **self-check** cells to see which functions still need work. They are not marked.
4. Part B is a form (the `MEMO` cell). Nothing is written as an essay.
5. Choose **Runtime, then Restart session and run all**. Fix any error. Press **Ctrl+S** (File, then Save) now and then; the countdown reminds you 30 and 10 minutes before your deadline.
6. There is **no Submit button**. Your notebook saves itself to your Drive and a backup goes to your lecturer every 5 minutes. At your deadline your editing stops and your work is collected automatically. Use **Check my work** on the entry page to see whether your notebook runs from the top; press **I have finished** there if you finish early.

## Time plan (180 minutes)
| Step | Time |
|---|---|
{plan}

## How it is marked
Everything is marked by the lecturer's computer. No person reads your notebook for marks. Your functions are run on **other rows that you cannot see** (hidden checks), and a few of your results on the file are compared with the correct values. {MARKS_TEXT} Part B gives {K.PART_B_MAX} marks for the memo form. A list of notebooks that look unusual is checked by the lecturer afterwards.

## Help during the window
Ask wording and technical questions on the class channel, {PC.SUPPORT_HOURS}. If something fails (Colab, the entry page, the form), report it at once on the class channel with a screenshot. The lecturer can authorise one fresh attempt, still ending at the window's close.

{RULES}
'''


def build_notebook(code, mode, require_forms=False):
    """mode: 'student' (the marked notebook), 'solution' or 'rehearsal'. Returns (notebook, supplied sources, stub sources)."""
    cfg = PC.CFGS['rehearsal' if mode == 'rehearsal' else 'exam']
    email, forms, configured = load_forms(code, require_forms and mode == 'student')
    cells = [cell(intro_cell(code, mode, configured))]
    test_id = 'ML_PROJECT_REHEARSAL' if mode == 'rehearsal' else 'ML_PROJECT'
    cells.append(cell(f'''FULL_NAME = ""
EMAIL = ""
STUDENT_ID = ""   # your Student Registration Number exactly as on your university record
COHORT = "{code}"  # Do not edit: identifies your course for marking.
TEST_ID = "{test_id}"  # Do not edit: identifies this assessment.
''', True))
    cells.append(cell(f'''## Your data
Real readings from the electricity meters of a steel plant ({PC.SOURCE['plant']}), one row every 15 minutes for the whole of 2018: 35,040 rows. Source: {PC.CITATION} The same file is used by every student.

| Column | Meaning |
|---|---|
| date | Day and time of the reading, written DD/MM/YYYY HH:MM. Each day's last reading is written with that day's date and 00:00 (see Task 1). |
| Usage_kWh | Energy used in the 15 minutes, kWh. |
| Lagging_Current_Reactive.Power_kVarh, Leading_Current_Reactive_Power_kVarh | Reactive power in the 15 minutes, kVarh. |
| CO2(tCO2) | Carbon dioxide, calculated from the energy used (it leaks the answer; Task 1 removes it). |
| Lagging_Current_Power_Factor, Leading_Current_Power_Factor | Power factors in percent, 0 to 100. Calculated from the energy and the reactive power, so they are not used as features. |
| NSM | Seconds since midnight (0 to 85500). |
| WeekStatus, Day_of_week | Weekday or Weekend, and the day's name. |
| Load_Type | Light_Load, Medium_Load or Maximum_Load: a time-of-day band. Not used. |

The target is `{cfg['target']}` ({cfg['unit']}). The features are `FEATURES` = {', '.join('`' + f + '`' for f in cfg['features'])} (`weekend` is made in Task 1). A **record** is one row as a dictionary. A **list of records** is several rows. Your functions take and return these. Missing values are `None`. Calculate from the lists you are given. Do not use the global tables inside a function, because the marked checks give your functions other rows. The constants `TARGET`, `FEATURES`, `LIMIT` and the others from the setup cell may be used.'''))
    setup = PC.setup_cell(cfg)
    cells.append(cell(setup, True, ['iuea-support'], True))
    test_src, choose_src = PC.test_cell(), PC.choose_cell()
    stub_sources = []
    for i, task in enumerate(PC.tasks(cfg), 1):
        marks = sum(task['marks'].values())
        head = f'## Task {i}: {task["title"]}' + (f' ({marks} automatic marks, {task["week"]})' if marks else ' (supplied rule; no marks of its own)')
        if mode == 'rehearsal' and task['key'] in PC.REHEARSAL_NOTES:
            cells.append(cell(PC.REHEARSAL_NOTES[task['key']]))
        cells.append(cell(head + '\n\n' + task['intro']))
        for starter, model in task['cells']:
            if starter == '__TEST__':
                cells.append(cell(test_src, True, ['iuea-support'], True))
                continue
            if starter == '__CHOOSE__':
                cells.append(cell(choose_src, True, ['iuea-support'], True))
                continue
            stub_sources.append(starter)
            cells.append(cell(model if mode == 'solution' else starter, True, ['iuea-answer-' + task['key']]))
    cells.append(cell('## Self-check (not marked)\nRun this supplied cell to see which functions still need work. It uses tiny examples with known answers. The marked checks use other rows.'))
    cells.append(cell(PC.SELF_CHECK, True, ['iuea-selfcheck', 'autograde-skip']))
    cells.append(cell(PC.memo_markdown(code, cfg, len(PC.tasks(cfg)) + 1)))
    cells.append(cell((PC.memo_solution(code, cfg) if mode == 'solution' else PC.MEMO_STARTER.replace('in UNIT', 'in ' + cfg['unit'])), True, ['iuea-memo']))
    cells.append(cell('## Memo self-check (not marked)\nRun this supplied cell after you fill in the form. It tells you which fields are empty and whether your numbers agree with your own notebook.'))
    cells.append(cell(PC.MEMO_SELF_CHECK, True, ['iuea-selfcheck', 'autograde-skip']))
    cells.append(cell('''## Before your deadline
1. Choose **Runtime, then Restart session and run all**. Every cell must run without an error. Fix the first error first.
2. Optional: run the **Check my notebook** cell below and click its button. It runs a copy of your code again from the top, the way the marking computer does, and tells you which cell fails, whether every required function and the `MEMO` form are there, and what the self-checks say. It never shows a mark. The same check is on the entry page (**Check my work**), run on your saved notebook.
3. Press **Ctrl+S**. There is no Submit button and no form. At your deadline your editing stops and the lecturer's server collects your work: the last version saved before the deadline, or the newest automatic backup if that is newer.
4. Finished early? Press **I have finished** on the entry page. Your editing stops at once and your work is collected.

Work only in the notebook the entry page opened for you. If you open a copy ("Save a copy in Drive"), the backup still reaches your lecturer and the setup cell shows a warning; go back to the entry page and click Resume.

**Declaration:** by working in this notebook until your deadline, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and change the code I submitted.''' if mode != 'rehearsal' else '''## End of the rehearsal
Nothing here is marked. Practise the end of the project: run **Check my notebook** below (optional), press **Ctrl+S**, then on the entry page click **Check my work** and, when you are done, **I have finished**. In the rehearsal your editing is never stopped.

Before the window, check that you can: finish every function and see PASS in the self-check; run **Runtime, Restart session and run all** with no error; fill in every `MEMO` field and see every memo self-check pass; and explain, in your own words, what each function does and why the test set is opened only once.'''))
    cells.append(cell(PL.check_cell(), True, ['iuea-check', 'autograde-skip'], True))
    cells.append(cell(PL.attempt_cell(), True, ['iuea-attempt', 'autograde-skip'], True))
    nb = dict(cells=cells, metadata=dict(iuea_exam_version=PC.VERSION, kernelspec=dict(display_name='Python 3', language='python', name='python3')), nbformat=4, nbformat_minor=4)
    return nb, dict(setup=setup, test=test_src, choose=choose_src), stub_sources


def write_nb(path, nb):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-forms', action='store_true', help='Refuse to build a release notebook before the submission pipeline is marked ready (tools/pipeline_ready.json)')
    a = ap.parse_args()
    hashes = {}
    stubs = set()
    for code in PC.CODES:
        nb, supplied, stub_sources = build_notebook(code, 'student', a.require_forms)
        write_nb(PC.PROJECT / 'Notebooks' / code / 'ML_PROJECT_student.ipynb', nb)
        sol, _, _ = build_notebook(code, 'solution')
        write_nb(PC.PROJECT / 'grader_spec/solutions' / code / 'ML_PROJECT_solution.ipynb', sol)
        reh, _, reh_stubs = build_notebook(code, 'rehearsal')
        write_nb(PC.PROJECT / 'Rehearsal' / code / 'ML_PROJECT_rehearsal.ipynb', reh)
        hashes[code] = {k: K.source_hash(v) for k, v in supplied.items()}
        stubs |= {K.source_hash(s) for s in stub_sources}
        print('built', code)
    hashes['stubs'] = sorted(stubs)
    (PC.PROJECT / 'grader_spec/supplied_cell_hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')


if __name__ == '__main__':
    main()
