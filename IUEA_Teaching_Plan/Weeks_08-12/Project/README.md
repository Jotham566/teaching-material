# Engineering ML project: online, 3 hours, individual, fully automatic

Decisions of 13 November 2026 (they replace those of 4 November; see `CHANGE_BRIEF_2026-11-13.md`). The project is **individual**, **timed** (3 hours from Start test, in Colab) and **fully auto-graded** like Practical Test 1. It is taken **online, from anywhere**, in one window for all three courses: **opens Monday 23 November 2026, 00:00 and closes Wednesday 25 November 2026, 23:59 Kampala time** (confirmed). It follows the lecturer's blueprint **"Weeks 1-8 core" (14 November 2026)**: no cross-validation, no cost table, no threshold choice; a light warning question at the fixed threshold 0.5; the model-choice rule is a supplied cell. It counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).

Two separate questions, no baseline model (lecturer, 16 November 2026). Question 1 uses only the houses, Question 2 only the machines.

| Part A item | Marks |
|---|---|
| Q1 Task 1: clean the houses (duplicates, missing prices, impossible values; other gaps kept; raw table unchanged) | 3 |
| Q1 Task 2: split the houses 60/20/20 (four given lines, `random_state=17`) | 1 |
| Q1 Task 3: linear regression and a decision tree (max_depth 4, random_state 17), each with median imputation | 4 |
| Q1 MAE and RMSE | 3 |
| Q1 no leakage (imputation learned from the training rows only) | 2 |
| Q1 two labelled charts | 2 |
| Q1 Task 3b: do the text columns help? One-hot recipe, a comparison only | 2 |
| Q1 Task 4: `choose_model` (MAE limit), then the test set once (`test_mae`) | 1 |
| Q2 Task 5: clean the machines (and `product_type` as a number) | 3 |
| Q2 Task 6: split the machines 60/20/20 | 1 |
| Q2 Task 7: logistic regression and a decision tree classifier (max_depth 3, random_state 17) | 3 |
| Q2 counts, precision, recall and F1 for both | 2 |
| Q2 Task 8: `choose_warning_model` (higher F1), then the test set once (`test_f1`) | 1 |
| Results on the tables, reproducible, results and MEMO present | 2 |

Part B (15): house_model 2, house_validation_mae 2, warning_model 2, warning_validation_f1 1, test_mae and test_f1 2, limits 3, next_step 1, two written answers 2. No mark is entered by hand. Marks are final by Wednesday 2 December 2026.

**Data** (tidy tables, lecturer's decision of 16 November 2026). Two tables for every student, stored inside the supplied setup cell (bzip2 and base64, one SHA-256 check), so nothing is downloaded during the window. Both are built from published files and organised before students see them: plain column names, metric units, the columns that matter. Houses: Ames, Iowa sales 2006 to 2010 (De Cock 2011, `data_source/ames_decock/AmesHousing.txt`, SHA-256 `6cfe6cb5...`), 18 columns, the 5 sales above 4000 sq ft left out as De Cock advises. Machines: AI4I 2020 (Matzka 2020, UCI 601, CC BY 4.0, synthetic), 8 columns, the failure-type columns left out. A fixed set of problems is ADDED on purpose and the notebook says so: houses 10 duplicates, 6 missing prices, 6 impossible values; machines 12 duplicates, 8 missing failures, 8 impossible values, 15 missing tool wear. Given 2,935 houses and 10,012 machines; cleaned 2,913 and 9,984; split 1,748 / 582 / 583 and 5,990 / 1,997 / 1,997. A notebook cell "The data" explains every column.

**Rehearsal** (unmarked; lecturer, 14 November 2026): exactly the project's tasks 1 to 7 including 3b, files, result names and memo, with one change: the split uses `random_state=29`, so every number differs (validation MAE linear 22,005, tree 27,785 USD; F1 logistic 0.238, tree 0.244). Run by the lecturer in the revision class (CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November); only the demo numbers 26/DEMO/001/LECTURER and 26/SMOKE/001/TEST open it. It has short self-study notes before the tasks that need them (the fixed seeded split and why the test rows stay apart; fitting on the training rows only; one-hot encoding for Task 3b; logistic regression, the confusion matrix, precision and recall; opening the test set once and refitting), each pointing to the Class 2 or Class 3 slide by title.

**Collection and instant checks** (collection design of 14 November 2026, no Submit step): the student picks the course and types the registration number, which must match the usual pattern (for example 26/BCE/001/PS). On the class list the page shows the name to confirm (This is me). Not on the list: the student types a full name, starts normally and is graded; the result carries the flag NOT_ON_LIST (spot-check list and Collection sheet, information only). One attempt per registration and per email. Start copies the issued notebook into the lecturer's Drive, shares it with the student's Google email as an editor and opens it in Colab, which saves to it. The setup cell sends a silent backup every 5 minutes and warns a student who is in another file. At the deadline a time trigger makes the file read only and collects the newer of the last Drive save before the deadline and the last on-time backup; GitHub Actions marks it in the Colab-matching sandbox. Students use Check my work and I have finished on the entry page; marks are shown only after the release switch. The rehearsal runs the same flow without locking or marking. Set-up: `deploy/setup_pipeline.sh` and `deploy/SETUP_GITHUB_ACTIONS.md`.

**Plain code** (14 November 2026): students write ordinary code under each task heading and store the named results (no function placeholders). The notebook has ONE supplied cell, "Setup: run me first" (the data files, the backup and the clock; labelled DO NOT EDIT); the imports, column names and model-choosing rules are visible supplied cells at the step that first uses them. The grader puts the original setup cell back, runs the notebook from the top, then re-runs each task's cells (its own added cells included) in a fresh namespace with hidden inputs. See `grader_spec/own_cells.py` and `project_contracts.py`.

## Files

| Path | What |
|---|---|
| `Student_Brief_<cohort>.docx` and `.pdf` | The student brief: the data, the two questions, the test set and how it is opened once, how the window and the deadline work, help and failures, the time plan, the AI rule, the rules that make a notebook run, how Part A and Part B are marked. |
| `Lecturer_Marking_Guide.docx` and `.pdf` | The data, the reference results, how the time limit works, the timeline, the grading commands, the column mapping, the window, the spot-check list, the marks and the own-cells rule, a worked example, common errors, integrity, what is proved and not proved, open points. |
| `Dean_Summary_ML_Project.docx` and `.pdf` | A short summary for the Dean's office (`tools/build_dean_summary.py`). |
| `Notebooks/<cohort>/ML_PROJECT_student.ipynb` | The marked notebook (the data is inside it). Marked DRAFT until the submission forms exist (`--require-forms`). |
| `Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb` | The unmarked rehearsal. No submit cell. |
| `data_source/ames_decock/` | `AmesHousing.txt` and `DataDocumentation.txt` (De Cock 2011). |
| `data_source/ai4i_uci_601/` | `ai4i2020.csv` and the UCI zip (Matzka 2020, synthetic). |
| `deploy/` | The patched portal, gateway (with `/api/check`, `/api/backup`, `/api/mywork`, `/api/finish`, `/api/status`, `/api/fixemail`) and collector files, the collector web app `ml_project_pipeline.gs` (backups, the deadline trigger, collection, extensions), `setup_pipeline.sh`, the project entry page, the packets, the entry links and QR codes, `DEPLOYMENT_STEPS.md`, `SETUP_GITHUB_ACTIONS.md` and `test_ml_project_portal.cjs`. The live files are not touched. |
| `sandbox/` | The Colab-matching grading image (`Dockerfile`, `colab_versions.json`, `requirements.txt`): `docker build -t iuea-notebooks:colab-2026.11 sandbox`. |
| `actions/` | The GitHub Actions workflow (`workflow/grade-ml-project.yml`), `actions_grade.py` (one submission), `final_regrade.py` (the one command after the window), `make_repo_bundle.py` (the private repository's contents), `local_stack.mjs` and `test_actions_e2e.py` (the end-to-end proof with no network). |
| `grader_spec/project_contracts.py`, `memo_spec.py`, `project_numpy_reference.py`, `own_cells.py` | The hidden checks, the Part B keys and keyword rules, the NumPy expected values, the own-cells preparation. PRIVATE. |
| `grader_spec/spec_ML_PROJECT.py`, `hidden/spec_ML_PROJECT_hidden.py` | Handout spec and hidden spec (16 questions: q01 to q09 Part A, q10 to q16 Part B). |
| `grader_spec/rubrics/ML_PROJECT_partA.json`, `ML_PROJECT_partB.json` | The mark schemes (all automatic; 30 and 15). |
| `grader_spec/hidden_data/` | The hidden inputs of the task re-runs (sampled from the file with a small seeded change and problems added), with hashes, for audit. |
| `grader_spec/supplied_cell_hashes.json` | Hashes of the three supplied cells and of every issued TODO cell. |
| `grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb` | Model solutions for the proofs. NEVER give to students. |
| `grader_spec/grade_project.py` | The grading command. Writes the results, the spot-check list, feedback and memo files. |
| `tools/export_for_gradebook.py` | Writes the two gradebook import files. |
| `grader_spec/similarity_check.py`, `offline_harness.py`, `gradebook_import_check.cjs` | Copy check (task-code similarity is information only, SIMILAR_CODE, because the rehearsal has the same tasks; identical written answers still flag SAME_WRITTEN_ANSWERS), the no-Docker harness (proofs only) and the real-gradebook import check. |
| `grader_spec/run_proofs.py`, `test_project_grader.py`, `proof_results.txt`, `.json` | The proof matrix, the quick regression test and the recorded result. |
| `tools/project_content.py` | One source for course facts, the window, tasks, starter and solution code, the memo form, the rehearsal notes. |
| `tools/pipeline_cells.py` | The backup code and the countdown line inside the setup cell, and the runner of Check my work (built from the spec). |
| `tools/build_grader_spec.py`, `build_project_notebooks.py`, `build_deploy_bundle.py`, `build_project_docs.py`, `build_dean_summary.py` | The builders. |
| `tools/install_project_bank.py` | Copies the notebooks to `assessment_banks/ML_PROJECT/<cohort>/A/`. |

## Run order

From `IUEA_Teaching_Plan/Weeks_08-12/Project/`, with a Python that has scikit-learn, pandas, matplotlib, openpyxl and python-docx (`PY=../../../.iuea-grader-env/bin/python`):

1. `$PY tools/build_grader_spec.py` (checks the data file, writes the specs, the rubrics and the hidden rows).
2. `$PY tools/build_project_notebooks.py` (draft) or with `--require-forms` (release, needs `tools/pipeline_ready.json`). Writes the notebooks, the rehearsal, the solutions and the hashes.
3. `$PY tools/build_deploy_bundle.py`, then `node deploy/test_ml_project_portal.cjs` and `$PY actions/test_actions_e2e.py` (Docker running).
4. Prove the grader in the Colab-matching sandbox: `cd grader_spec && $PY run_proofs.py --docker` (all three courses; without `--docker` it runs offline in a local process). Expect every case to pass. Quick check: `$PY -m unittest test_project_grader`.
5. `$PY tools/build_project_docs.py` (briefs and guide; the worked example comes from the proof results), then `$PY tools/build_dean_summary.py`. The PDFs are written by LibreOffice with a private profile that holds the Lato fonts, and the build stops if a PDF does not embed Lato.
6. Deployment: `deploy/DEPLOYMENT_STEPS.md`. Then `$PY tools/install_project_bank.py`.
7. After the window, with Docker running: `exportMlProjectBatch()` in the collector, then `python3 actions/final_regrade.py --zip <batch zip> --roster <Grades.csv>` (grade_project.py, the gradebook files and the comparison with the instant marks), read the spot-check list, then `importMarkedResults(<file id>, "ML Project Part A")` and `"ML Project Part B"` in the gradebook, then `recomputeAll()`.

Slides, notes and the lab wording are in `../Build/` (another session owns them).

## What is not proven

Colab itself, the Apps Script deployments, the GitHub repository and its minutes, and the Cloudflare gateway were not available (nothing was created or deployed). See the marking guide (section 10) and `deploy/DEPLOYMENT_STEPS.md`.
