"""Write the grader specification in the same conventions as grader/specs: python3 tools/build_grader_spec.py

  grader_spec/spec_ML_PROJECT.py                 handout spec (marks, prompts); no check functions
  grader_spec/hidden/spec_ML_PROJECT_hidden.py   hidden checks; the only file that holds check functions
  grader_spec/rubrics/ML_PROJECT_partA.json, ML_PROJECT_partB.json   the mark schemes in the grader's rubric format (all automatic)
  grader_spec/hidden_data/<cohort>/hidden_<seed>_<role>.csv and hidden_sets.json   the hidden rows for the function checks, for audit
The data is the one real file in data_source/steel_uci_851/ (its SHA-256 is checked). Run this BEFORE build_project_notebooks.py.
"""
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402
import project_numpy_reference as P  # noqa: E402

G = PC.PROJECT / 'grader_spec'


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows([{k: ('' if r.get(k) is None else r.get(k)) for k in fields} for r in rows])


def screen():
    """The design must hold on the real file: both classes in every part, and a choice the rule can make."""
    for cfg in (P.EXAM, P.REHEARSAL):
        p = P.pipeline(cfg)
        for part in ('train', 'validation', 'test'):
            assert 0.05 < p['positive_share'][part] < 0.5, f'{cfg["key"]}: the {part} set has too few of one class'
        assert p['chosen_model'] is not None, f'{cfg["key"]}: no model meets the client limit'
        assert p['n']['train'] == 23328 and p['n']['validation'] == 5856 and p['n']['test'] == 5855, p['n']


def main():
    P.file_bytes()
    screen()
    (G / 'hidden').mkdir(exist_ok=True)
    (G / 'rubrics').mkdir(exist_ok=True)
    for old in ('data',):                                       # the synthetic variant files of 3 November are superseded
        if (G / old).exists():
            shutil.rmtree(G / old)
    questions = {}
    for i, (task, marks) in enumerate(K.ALL_TASKS, 1):
        questions[f'q{i:02d}'] = dict(marks=marks, visible=False, prompt=K.TITLES[task], answer_vars=[])
    (G / 'spec_ML_PROJECT.py').write_text(
        f'ASSIGNMENT="ML_PROJECT"\nTITLE="Engineering ML project, Parts A and B (automatic marks)"\nVERSION={K.VERSION!r}\nDEFAULT_COHORT=""\n'
        f'QUESTION_ORDER={list(questions)!r}\nQUESTIONS={questions!r}\n')
    (G / 'hidden/spec_ML_PROJECT_hidden.py').write_text(
        'import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent))\n' + K.hidden_spec_source())
    desc = dict(clean='Hidden rows built from the real file with the real problems and others added (midnight readings, an empty reading, repeats, impossible values, a missing target); input unchanged.',
                split='Hidden rows, also in reverse order: months 1 to 8 training, 9 and 10 validation, 11 and 12 test.',
                results='Validation MAE, cross-validated mean and spread, AUC and the chosen model, compared with the NumPy reference wherever they appear in the notebook.',
                test='Supplied cells intact and the test set result equals the reference for the student\'s own choice.',
                sealed='Test set opened once, after the choice, with that choice; no November or December row in the development variables.',
                leakage='Probes: imputation, baseline model, scaler and cross-validation by month use only the rows they are given for training.',
                repro='Two calls agree, random_state=17 is kept, no unseeded randomness, saved predictions equal a fresh run.',
                charts='Chart 1 and Chart 2 (under any name) have a title, named axes and the unit; the plotted data match; the required functions and the MEMO form exist.')
    partA = [dict(id=f'q{i:02d}', title=K.TITLES[t], maximum=m, description=desc.get(t, 'Hidden rows built from the real file. Partial credit by the share of checks passed.')) for i, (t, m) in enumerate(K.PARTS, 1)]
    off = len(K.PARTS)
    partB = [dict(id=f'q{off + i:02d}', title=K.PART_B_TITLES[t], maximum=m, description=d) for i, ((t, m), d) in enumerate(zip(K.PARTB, [
        'Recommended model was trained, equals the student\'s own rule choice; threshold equals the student\'s own choice.',
        'Validation MAE of the three models agrees with the student\'s own values within 0.011.',
        'Test MAE and test recall agree with the grader\'s value on the same predictions within 0.011.',
        'Mean cross-validated MAE agrees with the student\'s own cv_summary within 0.011.',
        'Three different statements chosen from ten, one mark for each true limit.',
        'One statement chosen from five.',
        'Two short answers, one mark each: length 8 to 80 words and keyword groups (several wordings accepted).']), 1)]
    assert sum(c['maximum'] for c in partA) == 30 and sum(c['maximum'] for c in partB) == 15
    (G / 'rubrics/ML_PROJECT_partA.json').write_text(json.dumps(dict(id='ML_PROJECT-PARTA-' + K.VERSION, title='Engineering ML project, Part A', maximum=K.PART_A_MAX, grading='deterministic',
                                                                     automatic_maximum=K.PART_A_MAX, rubric_maximum=0, criteria=partA), indent=2) + '\n')
    (G / 'rubrics/ML_PROJECT_partB.json').write_text(json.dumps(dict(id='ML_PROJECT-PARTB-' + K.VERSION, title='Engineering ML project, Part B (structured memo form)', maximum=K.PART_B_MAX, grading='deterministic',
                                                                     automatic_maximum=K.PART_B_MAX, rubric_maximum=0, criteria=partB), indent=2) + '\n')
    if (G / 'hidden_data').exists():
        shutil.rmtree(G / 'hidden_data')
    sets = {}
    for code, seeds in K.HIDDEN_SEEDS.items():
        folder = G / 'hidden_data' / code
        sets[code] = []
        for seed in seeds:
            training, features = K.regression_case(seed)
            for label, rows in (('clean', K.clean_case(seed)), ('train', training), ('held_features', features),
                                ('cv', P.clean_rows(P.hidden_rows(seed, 25))), ('split', P.clean_rows(P.hidden_rows(seed, 15)))):
                path = folder / f'hidden_{seed}_{label}.csv'
                write_csv(path, rows)
                sets[code].append(dict(seed=seed, role=label, rows=len(rows), file=str(path.relative_to(G)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (G / 'hidden_data/hidden_sets.json').write_text(json.dumps(dict(note='Rows sampled from the real UCI file with a small seeded change to the energy and reactive power, '
                                                                    'plus added problems for the cleaning check. Test data for the grader only; never presented as real readings.',
                                                                    source=P.CITATION, sets=sets), indent=2) + '\n')
    print('grader_spec written; Part A', K.PART_A_MAX, 'automatic, Part B', K.PART_B_MAX, 'automatic;', len(K.ALL_TASKS), 'questions')


if __name__ == '__main__':
    main()
