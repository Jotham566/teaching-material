"""Build the project notebooks. python3 tools/build_project_notebooks.py [--require-forms]

Plain code (lecturer's redesign of 14 November 2026). Each notebook is:
  a short opening (at most 7 short lines, the deadline among them once issued), ONE supplied code cell "Setup: run me first" (collapsed), then for each task a heading with two or three
  lines, the INPUT and the RESULT names, and one empty code cell (students add as many cells as they like), and the Part B MEMO form.
  The rehearsal is the project exactly (same files, tasks, result names and memo) with the split's random_state=29, and short notes
  (at most 4 bullets) before the tasks that need them.
Writes, for each cohort (CML3112, CML3113, CML3111):
  Notebooks/<cohort>/ML_PROJECT_student.ipynb, Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb,
  grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb (NEVER give to students) and grader_spec/supplied_cell_hashes.json.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402


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
    """The notebook is ready to hand out when tools/pipeline_ready.json exists (written by deploy/setup_pipeline.sh)."""
    ready = (HERE / 'pipeline_ready.json').exists()
    if require and not ready:
        raise SystemExit('The collection pipeline is not marked ready. Run deploy/setup_pipeline.sh first.')
    return '', {}, ready


def intro_cell(code, mode, configured, deadline_slot=False):
    """At most 5 lines. deadline_slot is kept for the bundle builder; the deadline is shown by the countdown line after every cell."""
    w = PC.WINDOW
    data = '*Data: Ames, Iowa house sales 2006 to 2010 (De Cock 2011); AI4I 2020 machine data, which is synthetic (Matzka 2020, CC BY 4.0).*'
    steps = f"""1. Run **Setup** (the next cell) first. **Do not edit it.** It shows your time left, and the time shows again after every cell.
2. Do the tasks in order. {PC.OWN_CELLS}"""
    if mode == 'rehearsal':
        return f'''# {code} Engineering ML project: REHEARSAL (practice, not marked)
The same tasks as the project. The split uses random_state=29, so the numbers differ from the project's.
{steps}
3. Nothing is locked or marked.
{data}'''
    draft = '' if configured or mode == 'solution' else ' (DRAFT: do not hand out)'
    return f'''# {code} Engineering ML project{draft}: Part A {K.PART_A_MAX} + Part B {K.PART_B_MAX} marks, scaled to 40 percent
{steps}
3. There is no Submit button. Your work is collected at your deadline. Press Ctrl+S now and then.
No AI tools and no help from other people. You may be asked to explain your code.
{data}'''


def build_notebook(code, mode, require_forms=False):
    """mode: 'student', 'solution' or 'rehearsal'. Returns (notebook, setup source, starter sources)."""
    cfg = PC.CFGS['rehearsal' if mode == 'rehearsal' else 'exam']
    _, _, configured = load_forms(code, require_forms and mode == 'student')
    test_id = 'ML_REHEARSAL' if mode == 'rehearsal' else 'ML_PROJECT'
    setup = PC.setup_cell(cfg, code, test_id)
    cells = [cell(intro_cell(code, mode, configured)), cell(setup, True, ['iuea-support'], True)]
    cells.append(cell(PC.data_markdown()))
    starters = []
    tasks = PC.tasks(cfg)
    for i, task in enumerate(tasks, 1):
        if mode == 'rehearsal' and task['key'] in PC.REHEARSAL_NOTES:
            cells.append(cell(PC.REHEARSAL_NOTES[task['key']]))
        cells.append(cell(PC.task_markdown(i, task)))
        starters.append(task['starter'])
        cells.append(cell(task['solution'] if mode == 'solution' else task['starter'], True))
    cells.append(cell(PC.memo_markdown(code, cfg, PC.memo_task_no(cfg))))
    memo = PC.memo_solution(code, cfg) if mode == 'solution' else PC.MEMO_STARTER.replace('UNIT', cfg['h_unit'])
    starters.append(PC.MEMO_STARTER.replace('UNIT', cfg['h_unit']))
    cells.append(cell(memo, True))
    nb = dict(cells=cells, metadata=dict(iuea_exam_version=PC.VERSION, kernelspec=dict(display_name='Python 3', language='python', name='python3')), nbformat=4, nbformat_minor=4)
    return nb, setup, starters


def write_nb(path, nb):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-forms', action='store_true', help='Refuse to build a release notebook before the pipeline is marked ready (tools/pipeline_ready.json)')
    a = ap.parse_args()
    hashes, stubs = {}, set()
    for code in PC.CODES:
        nb, setup, starters = build_notebook(code, 'student', a.require_forms)
        write_nb(PC.PROJECT / 'Notebooks' / code / 'ML_PROJECT_student.ipynb', nb)
        sol, _, _ = build_notebook(code, 'solution')
        write_nb(PC.PROJECT / 'grader_spec/solutions' / code / 'ML_PROJECT_solution.ipynb', sol)
        reh, reh_setup, _ = build_notebook(code, 'rehearsal')
        write_nb(PC.PROJECT / 'Rehearsal' / code / 'ML_PROJECT_rehearsal.ipynb', reh)
        hashes[code] = dict(setup=K.source_hash(setup), rehearsal_setup=K.source_hash(reh_setup))
        stubs |= {K.source_hash(s) for s in starters}
        print('built', code)
    hashes['stubs'] = sorted(stubs)
    (PC.PROJECT / 'grader_spec/supplied_cell_hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')


if __name__ == '__main__':
    main()
