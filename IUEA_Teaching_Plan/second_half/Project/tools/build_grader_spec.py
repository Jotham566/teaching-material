"""Write the grader specification in the same conventions as grader/specs: python3 tools/build_grader_spec.py

  grader_spec/data/<cohort>/<A|B|C|P>/engineering_data.csv   the data variants students receive (A, B, C marked; P the rehearsal)
  grader_spec/spec_ML_PROJECT.py                 handout spec (marks, prompts); no check functions
  grader_spec/hidden/spec_ML_PROJECT_hidden.py   hidden checks; the only file that holds check functions
  grader_spec/rubrics/ML_PROJECT_partA.json, ML_PROJECT_partB.json   the mark schemes in the grader's rubric format (all automatic)
  grader_spec/hidden_data/<cohort>/hidden_<seed>_<role>.csv and variants.json   the unseen data variants for the function checks, for audit
Run this BEFORE build_project_notebooks.py.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402
import memo_spec as M  # noqa: E402
import project_numpy_reference as P  # noqa: E402
from engineering_contracts import dataset  # noqa: E402

G = PC.PROJECT / 'grader_spec'


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def screen(code, rows):
    """Every variant must have both classes in the training, validation and test sets and a linear model that wins on the validation set."""
    p = P.cohort_pipeline(code, rows)
    lim = P.LIMITS[code]
    for name, part in (('validation', p['valid']), ('test', p['test'])):
        y = [r['target'] >= lim for r in part]
        assert 4 <= sum(y) <= len(y) - 4, f'{code}: the {name} set has too few of one class'
    y = [r['target'] >= lim for r in p['train']]
    assert 8 <= sum(y) <= len(y) - 8, f'{code}: the training set has too few of one class'
    best = min(p['validation_mae'], key=p['validation_mae'].get)
    assert best == 'linear' and p['validation_mae']['linear'] < PC.COHORT[code]['max_mae'], f'{code}: unexpected model ranking'


def main():
    (G / 'hidden').mkdir(exist_ok=True)
    (G / 'rubrics').mkdir(exist_ok=True)
    for code in PC.CODES:
        for v, seed in K.VARIANT_SEEDS.items():
            rows = dataset(code, seed, n=90, dirty=True)
            screen(code, rows)
            write_csv(K.csv_path(code, v), rows)
    questions = {}
    for i, (task, marks) in enumerate(K.ALL_TASKS, 1):
        questions[f'q{i:02d}'] = dict(marks=marks, visible=False, prompt=K.TITLES[task], answer_vars=[])
    (G / 'spec_ML_PROJECT.py').write_text(
        f'ASSIGNMENT="ML_PROJECT"\nTITLE="Engineering ML project, Parts A and B (automatic marks)"\nVERSION={K.VERSION!r}\nDEFAULT_COHORT=""\n'
        f'QUESTION_ORDER={list(questions)!r}\nQUESTIONS={questions!r}\n')
    (G / 'hidden/spec_ML_PROJECT_hidden.py').write_text(
        'import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent))\n' + K.hidden_spec_source())
    desc = dict(clean='Hidden checks on unseen data.', split='Hidden checks on unseen data, also in reverse order.', results='Compared with the NumPy reference on the data variant the student was issued.',
                test='Supplied cells intact and the test set result equals the reference for the student\'s own choice.',
                sealed='Test set opened once, after the choice, with that choice; no test-set row in the development variables.',
                leakage='Probes: imputation, baseline model, scaler and group cross-validation use only the rows they are given for training.',
                repro='Two calls agree, random_state=17 is kept, no unseeded randomness, saved predictions equal a fresh run.',
                charts='Chart 1 and Chart 2 have a title, named axes and the unit; the plotted data match; every required variable exists.')
    partA = [dict(id=f'q{i:02d}', title=K.TITLES[t], maximum=m, description=desc.get(t, 'Hidden checks on unseen data. Partial credit by the share of checks passed.')) for i, (t, m) in enumerate(K.PARTS, 1)]
    off = len(K.PARTS)
    partB = [dict(id=f'q{off + i:02d}', title=K.PART_B_TITLES[t], maximum=m, description=d) for i, ((t, m), d) in enumerate(zip(K.PARTB, [
        'Recommended model was trained, equals the student\'s own rule choice; threshold equals the student\'s own choice.',
        'Validation MAE of the three models agrees with the student\'s own values within 0.011.',
        'Test MAE and test recall agree with the grader\'s value on the same predictions within 0.011.',
        'Mean cross-validated MAE agrees with the student\'s own cv_summary within 0.011.',
        'Three different statements chosen from ten, one mark for each true limit.',
        'One statement chosen from five.',
        'Two short answers, one mark each: length 8 to 80 words and keyword groups (several wordings accepted).']), 1)]
    (G / 'rubrics/ML_PROJECT_partA.json').write_text(json.dumps(dict(id='ML_PROJECT-PARTA-' + K.VERSION, title='Engineering ML project, Part A', maximum=K.PART_A_MAX, grading='deterministic',
                                                                     automatic_maximum=K.PART_A_MAX, rubric_maximum=0, criteria=partA), indent=2) + '\n')
    (G / 'rubrics/ML_PROJECT_partB.json').write_text(json.dumps(dict(id='ML_PROJECT-PARTB-' + K.VERSION, title='Engineering ML project, Part B (structured memo form)', maximum=K.PART_B_MAX, grading='deterministic',
                                                                     automatic_maximum=K.PART_B_MAX, rubric_maximum=0, criteria=partB), indent=2) + '\n')
    old = G / 'rubrics/ML_PROJECT_partA.json'
    variants = {}
    for code, seeds in K.HIDDEN_SEEDS.items():
        folder = G / 'hidden_data' / code
        folder.mkdir(parents=True, exist_ok=True)
        variants[code] = []
        for seed in seeds:
            for label, n, extra in (('train', 90, 0), ('held', 18, 300), ('cv', 60, 0)):
                rows = dataset(code, seed + extra, n=n)
                path = folder / f'hidden_{seed}_{label}.csv'
                write_csv(path, rows)
                variants[code].append(dict(seed=seed + extra, role=label, rows=n, file=str(path.relative_to(G)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (G / 'hidden_data/variants.json').write_text(json.dumps(variants, indent=2) + '\n')
    print('grader_spec written; Part A', K.PART_A_MAX, 'automatic, Part B', K.PART_B_MAX, 'automatic;', len(K.ALL_TASKS), 'questions')


if __name__ == '__main__':
    main()
