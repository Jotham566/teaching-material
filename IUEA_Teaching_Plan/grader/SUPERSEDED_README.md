# Grader files for retired or replaced assessments (4 November 2026)

| File(s) | Status |
|---|---|
| `rubrics/TEST2.json`, `rubrics/hybrid/TEST2.json`, `specs/spec_TEST2.py`, `specs/hidden/spec_TEST2_hidden.py`, `specs/hidden/colab_decision_keys.json` (TEST2 key), `colab_exam_contracts.py` (TEST2 parts), `test2_numpy_reference.py` | **Practical Test 2 is retired** (2 November 2026). Kept as inert code and tests (`tests/test_test2_weeks8_13.py` still proves them). Nothing grades Test 2 now. |
| `rubrics/DEMO.json` | **The demo is retired** (3 November 2026). Not used. |
| `rubrics/ML_PROJECT.json`, `rubrics/hybrid/ML_PROJECT.json`, `specs/spec_ML_PROJECT.py` | Describe the OLD 100-mark take-home project (notebook and report). **Superseded** by the individual timed sitting graded by `../second_half/Project/grader_spec/grade_project.py` (Part A /30, Part B /15, both automatic; rubrics in `../second_half/Project/grader_spec/rubrics/ML_PROJECT_partA.json` and `ML_PROJECT_partB.json`). Do not use `grade_assessment.py --assessment ML_PROJECT` for Semester 1. |
| `retire_demo_forms_20261103.gs` | Run once to retire the three DEMO forms. |
| `exam_collection.gs`, `test_monitor.gs`, `../test_portal/Portal.gs`, `Packets.gs` | The LIVE deployed collector and portal. They still list TEST2 rows because the live Test windows rows exist. The patched copies that add `ML_PROJECT` are in `../second_half/Project/deploy/`; paste them when you deploy the sitting. |
| `../../data/test_portal_config.json`, `../../data/colab_test_submission_config.json` | Mirror the live portal and collector, so they still hold the TEST2 entries. The `ML_PROJECT` entries are added at deployment (`deploy/DEPLOYMENT_STEPS.md`, step 1.5). |
| `Grades_template.csv`, `gradebook.gs` | Keep the `Q11` and `Q12` columns (retired quizzes, ignored by the totals) and the old `ML Project` and `Demo` columns where a live sheet already has them. |
