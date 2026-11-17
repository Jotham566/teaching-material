"""The run-all revision notebooks (16 and 17 November 2026). python3 tools/build_worked_answers.py [--proof-dir DIR]

Writes Lecturer Guides/Rehearsal_Answers_<course>.ipynb: the rehearsal notebook (random_state=29) with every task answered by the code of
tools/worked_answers.py and the MEMO filled in, so Runtime > Run all gives every result. In this copy the clock and the automatic backup are
switched off (it is not an attempt from the entry page). FOR THE LECTURER ONLY: never post it.
tools/worked_answers.py holds the answer code and stays on this computer only (git-ignored, 17 November 2026).
Also writes Lecturer Guides/Rehearsal_Answers_<course>_for_students.ipynb: the same worked code, commented for self-study, to share with
students after the revision class. Its MEMO fills in only the numbers (from the variables); the Limits and Next step letters and the two
written answers are left for the student, because the project uses the same lists and identical sentences would trip the copy check.
With --proof-dir, also writes the same answers on the project's split (random_state=17) as a submission to grade, to prove full marks.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import build_project_notebooks as BN  # noqa: E402
import worked_answers as W  # noqa: E402
import project_numpy_reference as P  # noqa: E402

OUT = PC.PLAN / 'Weeks_08-12/Lecturer Guides'
TITLE = '''# {code} Engineering ML project: REHEARSAL ANSWERS (lecturer only, do not post)
Every task is answered, one step per cell. Choose **Runtime > Run all**, then talk through one cell at a time. The split uses random_state=29, as in the rehearsal; the project uses 17.
The clock and the automatic backup are off in this copy.'''
STUDENT_TITLE = '''# {code} Engineering ML project: worked revision notebook (practice)
Every task of the rehearsal is worked, one step per cell, with comments. Choose **Runtime > Run all**, then read each cell and its output.
The split uses random_state=29; the project uses 17, so your project numbers will differ. Nothing here is marked.
Part B is yours: choose the Limits and Next step letters and write the two answers in the MEMO cell yourself.'''
PRACTICE_MEMO = '''# The numbers come from your variables (never type them). The letters and the two answers are yours to fill in.
MEMO = {
    "house_model": chosen_house_model,
    "house_validation_mae": {"linear": round(float(linear_mae), 3), "tree": round(float(tree_mae), 3)},
    "warning_model": chosen_warning_model,
    "warning_validation_f1": {"logistic": round(float(logistic_f1), 3), "tree": round(float(tree_f1), 3)},
    "test_mae": round(float(test_mae), 3),
    "test_f1": round(float(test_f1), 3),
    "limits": ["", "", ""],      # three different letters from the Limits list above
    "next_step": "",             # one letter from the Next step list above
    "answer_choice": "",         # one or two sentences: which house model, and why (use your numbers)
    "answer_test_set": "",       # one or two sentences: why the test set is used only once, at the end
}
print(MEMO)
'''


def src(cell):
    return ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']


def answered(code, mode):
    """mode 'rehearsal' (the lecturer copy), 'students' (the practice copy to share) or 'project' (the proof submission)."""
    practice = mode in ('rehearsal', 'students')
    nb, _, _ = BN.build_notebook(code, 'rehearsal' if practice else 'student')
    cfg = P.REHEARSAL if practice else P.EXAM
    labels = {t['label']: t['key'] for t in PC.tasks(cfg)}
    current = None
    cells = []
    for cell in nb['cells']:
        text = src(cell)
        m = re.match(r'^## Task (\w+):', text)
        if cell['cell_type'] == 'markdown' and m:
            current = labels.get(m.group(1))
        step = re.match(r'^# Your code here \(step (\d+)\)', text) if cell['cell_type'] == 'code' else None
        if step:                                                            # the answer cells for this step, one logical step per cell
            k = int(step.group(1))
            for part in W.step_cells(current, k, cfg['split_seed']):
                one = copy.deepcopy(cell)
                one['source'] = part.splitlines(True)
                cells.append(one)
            if practice and current == 'encoded' and k == len(PC.task_steps(PC.tasks(cfg)[[t['key'] for t in PC.tasks(cfg)].index('encoded')])[1]):
                cells.append(BN.cell(W.DEMO_TEXT_INTRO))                    # revision-only demo: both models with the text columns
                for part in W.demo_cells():
                    one = copy.deepcopy(cell)
                    one['source'] = part.splitlines(True)
                    cells.append(one)
                cells.append(BN.cell(W.DEMO_TEXT_READ))
            continue
        if practice and cell['cell_type'] == 'markdown' and text.startswith('**How to read the weights table**'):
            cells.append(cell)                                              # the supplied note, then the revision-only sentence
            cells.append(BN.cell(W.GD_SENTENCE))
            continue
        if cell['cell_type'] == 'code' and text.startswith('# Fill in every field'):
            cell['source'] = (PRACTICE_MEMO if mode == 'students' else PC.memo_solution(code, cfg)).splitlines(True)
        cells.append(cell)
    nb['cells'] = cells
    if practice:
        nb['cells'][0]['source'] = (STUDENT_TITLE if mode == 'students' else TITLE).format(code=code).splitlines(True)
        setup = nb['cells'][1]
        s = src(setup)
        for call in ('_iuea_backup_start()\n', '_iuea_countdown_start()\n'):
            assert s.count('\n' + call) == 1, call
            s = s.replace('\n' + call, '\n# ' + call.strip() + '  (switched off in this copy)\n')
        setup['source'] = s.splitlines(True)
    return nb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proof-dir', default='')
    a = ap.parse_args()
    for code in PC.CODES:
        path = OUT / f'Rehearsal_Answers_{code}.ipynb'
        BN.write_nb(path, answered(code, 'rehearsal'))
        print('wrote', path.name)
        path = OUT / f'Rehearsal_Answers_{code}_for_students.ipynb'
        BN.write_nb(path, answered(code, 'students'))
        print('wrote', path.name)
        if a.proof_dir:
            nb = answered(code, 'project')
            sid = f'26/PROOF/7{PC.CODES.index(code)}1/ANS'
            for c in nb['cells']:
                if '# IUEA-SETUP-CELL' in src(c):
                    ident = dict(name='Answer Key', registration=sid, course=code, test='ML_PROJECT', email='answers@example.org')
                    c['source'] = re.sub(r'^_IUEA_IDENTITY = .*$', lambda _: '_IUEA_IDENTITY = ' + json.dumps(ident), src(c), count=1, flags=re.M).splitlines(True)
            folder = Path(a.proof_dir) / code
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f'{sid.replace("/", "_")}_ML_PROJECT.ipynb').write_text(json.dumps(nb))


if __name__ == '__main__':
    main()
