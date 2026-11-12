"""Build the project notebooks. python3 tools/build_project_notebooks.py [--require-forms]

Writes, for each cohort (CML3112, CML3113, CML3111):
  Notebooks/<cohort>/<A|B|C>/ML_PROJECT_student.ipynb      the three marked variants a student can be allocated (guided TODO cells, self-checks, memo form, Test 1 submit cell)
  Notebooks/<cohort>/<A|B|C>/engineering_data.csv          that variant's data file
  Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb            the unmarked rehearsal (same structure, practice data variant P, no submit cell)
  Rehearsal/<cohort>/engineering_data_practice.csv         the practice data
  grader_spec/solutions/<cohort>/<A|B|C>/ML_PROJECT_solution.ipynb   the model solutions used to prove the grader (NEVER give to students)
  grader_spec/supplied_cell_hashes.json                    hashes of the two supplied cells for every variant, so an edited supplied cell is noticed
The submit cell is the Test 1 helper (test_operations/colab_submit_cell.py) with ONE change: the missing-deadline guard also applies to ML_PROJECT.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402

PLAN = PC.PLAN
ROOT = PLAN.parent
RULES = '''**Rules (the same rules as Practical Test 1).** Individual work. **Permitted resources:** your lecture slides, your lab notebooks from Classes 1 to 4, the revision guide, the cheatsheet and your own course notes. Write the code yourself.
**No AI or outside help:** do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not get answers from another person, collaborate or copy someone else's work.
**Understanding check:** you may be asked to explain your submitted code, or make a small change to it, without AI or another person's help.
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


def intro_cell(code, v, mode, configured):
    c = PC.COHORT[code]
    s = PC.SITTING[code]
    plan = '\n'.join(f'| {name} | {m} min |' for name, m in PC.TIME_PLAN)
    if mode == 'rehearsal':
        head = f'''# {code} Machine Learning: Engineering ML project, REHEARSAL (unmarked)
**This is a rehearsal. Nothing here is marked or submitted.** It has the same structure, the same task wording and the same kinds of check as the real project sitting, but a different practice data file (variant P), so your numbers will not be the numbers you get on the day. Released {PC.REHEARSAL_TEXT[code]}. The real sitting is {PC.SITTING_TEXT[code]}.

**How to use it.** Open it in Colab (File, then Save a copy in Drive). Work through it as if it were the real sitting: set a timer for 3 hours if you want to practise the timing. Use the self-check cells. Ask your lecturer about anything unclear before the sitting. A solved walk-through is not given: the point is that you can do it yourself.'''
    else:
        draft = '' if configured or mode == 'solution' else '> **DRAFT. The submission form for this project is not set up yet. Do not hand this notebook out.**\n\n'
        head = f'''{draft}# {code} Machine Learning: Engineering ML project
**Part A: coded notebook (30 marks) and Part B: decision memo form (15 marks). Together 45 marks, scaled to 40 percent of the course. One sitting of 3 hours, individual work, marked automatically.**
**Sitting:** {PC.SITTING_TEXT[code]}. Your own 3 hours start when you press Start on the entry page and cannot be paused; the class closing time is the last cutoff.'''
    return f'''{head}

This project uses only what you learned in Weeks 1 to 11. You work on `engineering_data.csv` ({c['domain']}, in **{c['unit']}**), and answer two questions: **Question 1** how large will the {c['domain']} be on equipment the model has never met, and **Question 2** which rows should raise a warning. Group E6 is the test set and is opened **once**.

## How to work
1. Fill in the identity cell below (in the issued notebook it is filled in for you; check it) and run it. Then run the supplied cell **Prepare the data and the libraries**. It creates your CSV, so you need no upload.
2. Work from top to bottom. Replace each `TODO` and each `None`. Keep the function names, the argument order and the variable names exactly as printed. Run each cell and read what it prints.
3. Run the **self-check** cells to see which functions still need work. They are not marked.
4. Part B is a form (the `MEMO` cell). Nothing is written as an essay.
5. Choose **Runtime, then Restart session and run all**. Fix any error, then save with **File, then Save**.
6. Run the last cell, click **Submit test**, open the form link, check your details and press **Submit** there. Submission is finished only when the form says your response has been recorded.

## Time plan (180 minutes)
| Step | Time |
|---|---|
{plan}

## How it is marked
Everything is marked by the lecturer's computer. No person reads your notebook. Your functions are run on **other data that you cannot see** (hidden checks) and your results on your own data file are compared with the correct values. Of the 30 Part A marks, 24 are for the functions and your results, and 6 are for how you worked: the test set opened once and only after you chose, no data leakage (fit preprocessing on the training set only), the same answer every time (keep `random_state=17`), and readable charts. Part B gives 15 marks for the memo form. A list of notebooks that look unusual is checked by the lecturer afterwards.

{RULES}
'''


def build_notebook(code, v, mode, require_forms=False):
    """mode: 'student' (marked variant A/B/C), 'solution' or 'rehearsal'."""
    c = PC.COHORT[code]
    email, forms, configured = load_forms(code, require_forms and mode == 'student')
    cells = [cell(intro_cell(code, v, mode, configured))]
    test_id = 'ML_PROJECT_REHEARSAL' if mode == 'rehearsal' else 'ML_PROJECT'
    cells.append(cell(f'''FULL_NAME = ""
EMAIL = ""
STUDENT_ID = ""   # your Student Registration Number exactly as on your university record
COHORT = "{code}"  # Do not edit: identifies your course for marking.
TEST_ID = "{test_id}"  # Do not edit: identifies this assessment.
VARIANT = "{v}"  # Do not edit.
''', True))
    cells.append(cell(f'''## Your data
Each row is one synthetic (invented for teaching) observation of **{c['domain']}**.

| Column | Meaning |
|---|---|
| record_id | Row ID. A repeated ID means a duplicate row. record_id is never a time. |
| equipment_id | Which equipment: E1 to E6. Repeats across rows. E6 is the test set. |
| load_pct | Load in percent (a feature). Valid range 0 to 100, both included. |
| ambient_c | Ambient temperature in degrees Celsius (a feature). May be a missing value. |
| target | The target variable: {c['domain']}, in **{c['unit']}**. May be a missing value. |

A **record** is one row as a dictionary. A **list of records** is several rows. Your functions take and return these. Missing values are `None`. Calculate from the lists you are given. Do not use the global tables inside a function, because the marked checks give your functions other data.'''))
    setup = PC.setup_cell(code, v)
    cells.append(cell(setup, True, ['iuea-support'], True))
    test_src = PC.test_cell(code)
    for i, task in enumerate(PC.tasks(code, v), 1):
        marks = sum(task['marks'].values())
        head = f'## Task {i}: {task["title"]}' + (f' ({marks} automatic marks, {task["week"]})' if marks else f' ({task["week"]})')
        cells.append(cell(head + '\n\n' + task['intro']))
        for starter, model in task['cells']:
            if starter == '__TEST__':
                cells.append(cell(test_src, True, ['iuea-support'], True))
                continue
            cells.append(cell(model if mode == 'solution' else starter, True, ['iuea-answer-' + task['key']]))
    cells.append(cell('## Self-check (not marked)\nRun this supplied cell to see which functions still need work. It uses tiny examples with known answers. The marked checks use other data.'))
    cells.append(cell(PC.SELF_CHECK, True, ['iuea-selfcheck', 'autograde-skip']))
    cells.append(cell(PC.memo_markdown(code, v)))
    cells.append(cell((PC.memo_solution(code, v) if mode == 'solution' else PC.MEMO_STARTER.replace('in UNIT', 'in ' + c['unit'])), True, ['iuea-memo']))
    cells.append(cell('## Memo self-check (not marked)\nRun this supplied cell after you fill in the form. It tells you which fields are empty and whether your numbers agree with your own notebook.'))
    cells.append(cell(PC.MEMO_SELF_CHECK, True, ['iuea-selfcheck', 'autograde-skip']))
    if mode == 'rehearsal':
        cells.append(cell('''## End of the rehearsal
Nothing is submitted from this notebook. On the day, the real notebook has a last cell that saves a snapshot and opens the submission form, and a countdown at the top.

Before the sitting, check that you can: finish every function and see PASS in the self-check; run **Runtime, Restart session and run all** with no error; fill in every `MEMO` field and see 10 of 10 memo self-checks pass; and explain, in your own words, what each function does and why the test set is opened only once.'''))
    else:
        cells.append(cell('''## Save and submit (allow at least 20 minutes)
1. Choose **Runtime, then Restart session and run all**. Every cell must run without an error. Fix the first error first.
2. Check your identity cell, your two charts and your `MEMO` form. Choose **File, then Save**.
3. **Run, do not edit:** the **Submit your test** cell below. Choose the same Google account when asked. Click **Submit test** and wait for the form link.
4. In the form, check the account email, your name and registration number. Leave the prefilled snapshot fields unchanged. Press **Submit** before your personal deadline.
5. Wait for **Your response has been recorded**. Keep the saved snapshot in Drive until marks are released.

A saved notebook, a snapshot or an open form is not a submission: **you must submit the form**. Submit your work even if some tasks are unfinished. A new submission before the deadline must be a complete notebook; the latest one on time is marked. When the time ends the form no longer counts, Colab may still let you type but nothing after the deadline is marked.

**Declaration:** by submitting, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and change the code I submitted.'''))
        submit = cell('#@title Submit your test — Do not edit this cell\n# Do not edit this cell: saves your answers and prepares the submission form.\n' +
                      submit_helper().replace('__EXAM_CONFIG__', repr(dict(lecturer_email=email, forms=forms))), True, ['iuea-submission', 'autograde-skip'], True)
        cells.append(submit)
    nb = dict(cells=cells, metadata=dict(iuea_exam_version=PC.VERSION, kernelspec=dict(display_name='Python 3', language='python', name='python3')), nbformat=4, nbformat_minor=4)
    return nb, setup, test_src


def write_nb(path, nb):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-forms', action='store_true', help='Refuse to build a release notebook without a configured submission form')
    a = ap.parse_args()
    hashes = {}
    for code in PC.CODES:
        hashes[code] = {}
        for v in K.VARIANT_SEEDS:
            if v in K.MARKED_VARIANTS:
                nb, setup, test_src = build_notebook(code, v, 'student', a.require_forms)
                folder = PC.PROJECT / 'Notebooks' / code / v
                write_nb(folder / 'ML_PROJECT_student.ipynb', nb)
                shutil.copyfile(K.csv_path(code, v), folder / 'engineering_data.csv')
                sol, _, _ = build_notebook(code, v, 'solution')
                write_nb(PC.PROJECT / 'grader_spec/solutions' / code / v / 'ML_PROJECT_solution.ipynb', sol)
            else:
                nb, setup, test_src = build_notebook(code, v, 'rehearsal')
                folder = PC.PROJECT / 'Rehearsal' / code
                write_nb(folder / 'ML_PROJECT_rehearsal.ipynb', nb)
                shutil.copyfile(K.csv_path(code, v), folder / 'engineering_data_practice.csv')
            hashes[code][v] = dict(setup=K.source_hash(setup), test=K.source_hash(test_src))
        print('built', code)
    (PC.PROJECT / 'grader_spec/supplied_cell_hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')


if __name__ == '__main__':
    main()
