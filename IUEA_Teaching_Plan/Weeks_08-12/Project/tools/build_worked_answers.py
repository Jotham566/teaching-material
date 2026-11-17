"""The lecturer's run-all answer notebooks (16 November 2026). python3 tools/build_worked_answers.py [--proof-dir DIR]

Writes Lecturer Guides/Rehearsal_Answers_<course>.ipynb: the rehearsal notebook (random_state=29) with every task answered by the code of
tools/worked_answers.py and the MEMO filled in, so Runtime > Run all gives every result. In this copy the clock and the automatic backup are
switched off (it is not an attempt from the entry page). FOR THE LECTURER ONLY: never post it.
With --proof-dir, also writes the same answers on the project's split (random_state=17) as a submission to grade, to prove full marks.
"""
import argparse
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
Every task is answered. Choose **Runtime > Run all**. The split uses random_state=29, as in the rehearsal; the project uses 17.
The clock and the automatic backup are off in this copy.'''


def src(cell):
    return ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']


def answered(code, mode):
    """mode 'rehearsal' (the lecturer copy) or 'project' (the proof submission)."""
    nb, _, _ = BN.build_notebook(code, 'rehearsal' if mode == 'rehearsal' else 'student')
    cfg = P.REHEARSAL if mode == 'rehearsal' else P.EXAM
    labels = {t['label']: t['key'] for t in PC.tasks(cfg)}
    current = None
    for cell in nb['cells']:
        text = src(cell)
        m = re.match(r'^## Task (\w+):', text)
        if cell['cell_type'] == 'markdown' and m:
            current = labels.get(m.group(1))
            continue
        if cell['cell_type'] == 'code' and text.startswith('# Your code here.'):
            cell['source'] = W.answer(current, cfg['split_seed']).splitlines(True)
        elif cell['cell_type'] == 'code' and text.startswith('# Fill in every field'):
            cell['source'] = PC.memo_solution(code, cfg).splitlines(True)
    if mode == 'rehearsal':
        nb['cells'][0]['source'] = TITLE.format(code=code).splitlines(True)
        setup = nb['cells'][1]
        s = src(setup)
        for call in ('_iuea_backup_start()\n', '_iuea_countdown_start()\n'):
            assert s.count('\n' + call) == 1, call
            s = s.replace('\n' + call, '\n# ' + call.strip() + '  (switched off in the lecturer copy)\n')
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
