"""Build the project notebooks. python3 tools/build_project_notebooks.py [--require-forms]

Writes, for each cohort (CML3112, CML3113, CML3111):
  Notebooks/<cohort>/ML_PROJECT_student.ipynb             the marked notebook (guided TODO cells, self-checks, memo form, Test 1 submit cell); the data is inside it
  Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb            the unmarked rehearsal (same structure and file, another target, no submit cell)
  grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb the model solutions used to prove the grader (NEVER give to students)
  grader_spec/supplied_cell_hashes.json                    hashes of the three supplied cells and of every issued TODO cell (stubs), so an edited supplied
                                                           cell is noticed and an unedited stub never overwrites the student's own cell
The submit cell is the Test 1 helper (test_operations/colab_submit_cell.py) with ONE change: the missing-deadline guard also applies to ML_PROJECT.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402

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


def submit_helper():
    helper = (PLAN / 'test_operations/colab_submit_cell.py').read_text()
    old = "if globals().get('_IUEA_ALLOCATION') and TEST_ID == 'TEST1':"
    assert helper.count(old) == 1, 'colab_submit_cell.py changed: re-check the deadline guard before building'
    return helper.replace(old, "if globals().get('_IUEA_ALLOCATION') and TEST_ID in ('TEST1', 'ML_PROJECT'):")


def load_forms(code, require):
    for source in (ROOT / 'data/colab_test_submission_config.json', HERE / 'project_forms.json'):
        if source.exists():
            config = json.loads(source.read_text())
            if code + '|ML_PROJECT' in config.get('forms', {}):
                return config['lecturer_email'], {code + '|ML_PROJECT': config['forms'][code + '|ML_PROJECT']}, True
    if require:
        raise SystemExit(f'No form is configured for {code}|ML_PROJECT. Create the form (see Project/deploy/DEPLOYMENT_STEPS.md), then add it to tools/project_forms.json.')
    config = json.loads((ROOT / 'data/colab_test_submission_config.json').read_text())
    return config['lecturer_email'], {}, False


def intro_cell(code, mode, configured):
    cfg = PC.CFGS['rehearsal' if mode == 'rehearsal' else 'exam']
    plan = '\n'.join(f'| {name} | {m} min |' for name, m in PC.TIME_PLAN)
    if mode == 'rehearsal':
        head = f'''# {code} Machine Learning: Engineering ML project, REHEARSAL (unmarked)
**This is a rehearsal. Nothing here is marked or submitted.** It has the same structure, the same task wording and the same kinds of check as the marked project, on the same steel plant file, but with a different target: here you predict **{cfg['what']}** ({cfg['unit']}), with its own warning limit. The marked project predicts the energy used (kWh). Your numbers here will not be the numbers you get in the project. Released {PC.REHEARSAL_TEXT[code]}. The project window {PC.WINDOW_TEXT}.

**How to use it.** Open it in Colab (File, then Save a copy in Drive). Work through it as if it were the real project: set a timer for 3 hours if you want to practise the timing. Use the self-check cells. Ask about anything unclear on the class channel before the window. A solved walk-through is not given: the point is that you can do it yourself.'''
    else:
        draft = '' if configured or mode == 'solution' else '> **DRAFT. The submission form for this project is not set up yet. Do not hand this notebook out.**\n\n'
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
5. Choose **Runtime, then Restart session and run all**. Fix any error, then save with **File, then Save**.
6. Run the last cell, click **Submit test**, open the form link, check your details and press **Submit** there. Submission is finished only when the form says your response has been recorded.

## Time plan (180 minutes)
| Step | Time |
|---|---|
{plan}

## How it is marked
Everything is marked by the lecturer's computer. No person reads your notebook for marks. Your functions are run on **other rows that you cannot see** (hidden checks), and a few of your results on the file are compared with the correct values. Of the 30 Part A marks, 21 are for the functions, 3 for your results, and 6 for how you worked: the test set opened once and only after you chose, no data leakage (fit preprocessing on the training set only), the same answer every time (keep `random_state=17`), and readable charts. Part B gives 15 marks for the memo form. A list of notebooks that look unusual is checked by the lecturer afterwards.

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
    if mode == 'rehearsal':
        cells.append(cell('''## End of the rehearsal
Nothing is submitted from this notebook. In the project, the notebook has a last cell that saves a snapshot and opens the submission form, and a countdown at the top.

Before the window, check that you can: finish every function and see PASS in the self-check; run **Runtime, Restart session and run all** with no error; fill in every `MEMO` field and see 10 of 10 memo self-checks pass; and explain, in your own words, what each function does and why the test set is opened only once.'''))
    else:
        cells.append(cell('''## Save and submit (allow at least 20 minutes)
1. Choose **Runtime, then Restart session and run all**. Every cell must run without an error. Fix the first error first.
2. Check your identity cell, your two charts and your `MEMO` form. Choose **File, then Save**.
3. **Run, do not edit:** the **Submit your test** cell below. Choose the same Google account when asked. Click **Submit test** and wait for the form link.
4. In the form, check the account email, your name and registration number. Leave the prefilled snapshot fields unchanged. Press **Submit** before your personal deadline.
5. Wait for **Your response has been recorded**. Keep the saved snapshot in Drive until marks are released.

A saved notebook, a snapshot or an open form is not a submission: **you must submit the form**. Submit your work even if some tasks are unfinished. A new submission before the deadline must be a complete notebook; the latest one on time is marked. When the time ends the form no longer counts. Colab may still let you type, but nothing after the deadline is marked.

**Declaration:** by submitting, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and change the code I submitted.'''))
        submit = cell('#@title Submit your test — Do not edit this cell\n# Do not edit this cell: saves your answers and prepares the submission form.\n' +
                      submit_helper().replace('__EXAM_CONFIG__', repr(dict(lecturer_email=email, forms=forms))), True, ['iuea-submission', 'autograde-skip'], True)
        cells.append(submit)
    nb = dict(cells=cells, metadata=dict(iuea_exam_version=PC.VERSION, kernelspec=dict(display_name='Python 3', language='python', name='python3')), nbformat=4, nbformat_minor=4)
    return nb, dict(setup=setup, test=test_src, choose=choose_src), stub_sources


def write_nb(path, nb):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-forms', action='store_true', help='Refuse to build a release notebook without a configured submission form')
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
