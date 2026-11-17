"""Write the grader specification in the same conventions as grader/specs: python3 tools/build_grader_spec.py

  grader_spec/spec_ML_PROJECT.py                 handout spec (marks, prompts); no check functions
  grader_spec/hidden/spec_ML_PROJECT_hidden.py   hidden checks; the only file that holds check functions
  grader_spec/rubrics/ML_PROJECT_partA.json, ML_PROJECT_partB.json   the mark schemes in the grader's rubric format (all automatic)
  grader_spec/hidden_data/<cohort>/hidden_<seed>_<role>.csv and hidden_sets.json   the hidden rows for the function checks, for audit
The data is two real files in data_source/ (Ames houses, AI4I 2020 machines; their SHA-256 is checked). Run this BEFORE build_project_notebooks.py.
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
            assert 0.02 < p['positive_share'][part] < 0.5, f'{cfg["key"]}: the {part} set has too few of one class'
        assert p['chosen_model'] is not None, f'{cfg["key"]}: no model meets the client limit'
        assert (p['n']['houses_raw'], p['n']['houses'], p['n']['machines_raw'], p['n']['machines']) == (2935, 2913, 10012, 9984), p['n']
        assert (p['n']['houses_train'], p['n']['houses_valid'], p['n']['houses_test'], p['n']['machines_train'], p['n']['machines_valid'], p['n']['machines_test']) == (1748, 582, 583, 5990, 1997, 1997), p['n']
        # The added problems never touch a column an invalid-value rule reads with a missing value (so every way of writing the rule agrees).
        assert not any(r[c] is None for r in P.houses_given() for c in ('living_area_m2', 'year_built')), 'a rule column is missing'
        assert not any(r[c] is None for r in P.machines_given() for c in ('torque_nm', 'rotation_speed_rpm')), 'a rule column is missing'


def screen_encoded():
    """Task 3b's hidden sets must stay dense in scikit-learn (density 0.3 or more, so LinearRegression solves exactly, as the reference does)
    and must show categories the training rows never saw (so handle_unknown is tested)."""
    for code, seeds in K.HIDDEN_SEEDS.items():
        for seed in seeds:
            ht, hv, *_ = K.model_case(seed)
            for cfg in (P.EXAM, P.REHEARSAL):
                d = K.encoded_density(ht, cfg)
                assert d >= 0.32, f'{code} {seed}: encoded density {d:.3f} would make scikit-learn go sparse'
            assert len(K.unseen_categories(ht, hv)) >= 2, f'{code} {seed}: no unseen category in the hidden validation rows'
            base = P.encoded_regression(ht, P.strip(hv, P.EXAM['h_target']))
            fused = P.encoded_regression(ht + hv + K.extreme_rows(hv), P.strip(hv, P.EXAM['h_target']))
            assert max(abs(a - b) for a, b in zip(base, fused)) > 1, f'{code} {seed}: fitting on train and valid would go unnoticed'


def main():
    P.houses_text(); P.machines_text()
    screen()
    screen_encoded()
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
    desc = dict(clean_h='Task 1 cells re-run on two hidden raw house tables with added duplicates, missing prices and impossible values: the whole result, no duplicates, no missing price, no impossible value with valid rows kept, other gaps kept, raw table unchanged.',
                split_h='Task 2 cells re-run on hidden clean houses (and the same rows reversed): the three sets of the stated rule.',
                regression='Task 3 cells re-run on hidden train and valid houses: linear regression and decision tree (max_depth 4, random_state 17) predictions, each with median imputation.',
                errors='MAE and RMSE of the student\'s own Task 3 predictions on the hidden valid houses; printed values count.',
                leakage='Task 3 re-run with extreme rows added to valid: the other predictions must not change (imputation learned from the training rows only).',
                charts='Chart 1 and Chart 2 from the run from the top (under any name, or only shown): a title, named axes, the unit, the right data.',
                encoded='Task 3b (under Task 3): re-run on the Task 3 hidden sets, each with categories the training rows never show; encoded_pred equals the one-hot reference, encoded_mae from the own predictions, extra validation rows change nothing else.',
                test_h='Task 4 re-run on hidden train, valid and test houses with validation numbers that make the rule choose each model once: the choice and the test MAE; the test rows read only after chosen_house_model; no test house in train or valid.',
                clean_m='Task 5 cells re-run on two hidden raw machine tables with added problems: the whole result, no duplicates, no impossible value, product_type mapped, raw table unchanged.',
                split_m='Task 6 cells re-run on hidden clean machines (and reversed): the three sets of the stated rule.',
                classify='Task 7 re-run on hidden train and valid machines: logistic probabilities (solver tolerance), logistic warnings at 0.5 from the own probabilities, tree warnings equal to DecisionTreeClassifier(max_depth=3, random_state=17).',
                scores='Task 7: for each model, the counts (tn, fp, fn, tp), precision, recall and F1 from the student\'s own warnings.',
                test_m='Task 8 re-run on hidden train, valid and test machines with F1 values that make the rule choose each model once: the choice and the test F1; the test rows read only after chosen_warning_model; no test machine in train or valid.',
                results='A third each: validation MAE (houses) and F1 (machines) of both models on the real tables, calculated, and both rule choices; the same predictions twice, random_state=17 on both trees, no unseeded randomness; every result and the MEMO form present (Task 3b excluded).')
    partA = [dict(id=f'q{i:02d}', title=K.TITLES[t], maximum=m, description=desc.get(t, 'Hidden rows built from the real file. Partial credit by the share of checks passed.')) for i, (t, m) in enumerate(K.PARTS, 1)]
    off = len(K.PARTS)
    partB = [dict(id=f'q{off + i:02d}', title=K.PART_B_TITLES[t], maximum=m, description=d) for i, ((t, m), d) in enumerate(zip(K.PARTB, [
        'The recommended house model was trained and equals the student\'s own rule choice.',
        'Validation MAE of linear regression and the decision tree agree with the student\'s own values within 0.011 (USD).',
        'The recommended warning model was trained and equals the student\'s own rule choice (the higher validation F1).',
        'Validation F1 of logistic regression and the decision tree agree with the student\'s own values within 0.011.',
        'Test MAE (houses) and test F1 (machines) agree with the notebook\'s own values within 0.011.',
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
            ht, hv, hx, mt, mv, mx = K.model_case(seed)
            h2, m2 = K.split_case(seed)
            for label, rows in (('houses_raw_task1', K.raw_houses_case(seed)), ('machines_raw_task1', K.raw_machines_case(seed)),
                                ('houses_task2', h2), ('machines_task2', m2), ('houses_train', ht), ('houses_valid', hv), ('houses_test', hx),
                                ('machines_train', mt), ('machines_valid', mv), ('machines_test', mx)):
                path = folder / f'hidden_{seed}_{label}.csv'
                write_csv(path, rows)
                sets[code].append(dict(seed=seed, role=label, rows=len(rows), file=str(path.relative_to(G)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (G / 'hidden_data/hidden_sets.json').write_text(json.dumps(dict(note='Rows sampled from the Ames and AI4I files with a small seeded change to the numbers, '
                                                                    'plus added problems for the cleaning check. Test data for the grader only; never presented as real readings.',
                                                                    source=P.CITATION, sets=sets), indent=2) + '\n')
    print('grader_spec written; Part A', K.PART_A_MAX, 'automatic, Part B', K.PART_B_MAX, 'automatic;', len(K.ALL_TASKS), 'questions')


if __name__ == '__main__':
    main()
