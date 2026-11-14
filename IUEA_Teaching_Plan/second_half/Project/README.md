# Engineering ML project: online, 3 hours, individual, fully automatic

Decisions of 13 November 2026 (they replace those of 4 November; see `CHANGE_BRIEF_2026-11-13.md`). The project is **individual**, **timed** (3 hours from Start test, in Colab) and **fully auto-graded** like Practical Test 1. It is taken **online, from anywhere**, in one window for all three courses: **opens Monday 23 November 2026, 00:00 and closes Wednesday 25 November 2026, 23:59 Kampala time** (confirmed). It follows the lecturer's blueprint **"Weeks 1-8 core" (14 November 2026)**: no cross-validation, no cost table, no threshold choice; a light warning question at the fixed threshold 0.5; the model-choice rule is a supplied cell. It counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).

| Part A item | Marks |
|---|---|
| A1 Clean the two tables (keep `H_KEEP`, every column except PID, drop houses over 4,000 sq ft, add `living_m2`, drop the failure-type columns, map `Type`, gaps kept, inputs unchanged) | 6 |
| A2 Two labelled charts | 2 |
| A3 Split into training and validation rows (`sample(frac=0.25, random_state=17)`) | 2 |
| A4 Baseline, linear regression, decision tree (max_depth 4, random_state 17), each with median imputation | 6 |
| A5 MAE and RMSE | 3 |
| A6 No leakage (imputation and the baseline mean from training rows only) | 2 |
| A7 Warning question: probabilities 1; confusion counts, precision and recall at 0.5: 2 | 3 |
| A8 Test set opened once with the supplied cell, after the choice, and its result | 2 |
| A9 Results on the file, reproducible, results and MEMO present (a third each; Task 3b excluded) | 2 |
| A10 Task 3b, do the text columns help? One-hot encoding with a given recipe, fitted on the training rows only, `handle_unknown="ignore"`; a comparison, never part of `choose_model` | 2 |

Part B (15): recommended_model 3, validation_mae 3, test_mae and test_recall 2, improvement_over_baseline 1, limits 3, next_step 1, two written answers 2. No mark is entered by hand. Marks are final by Wednesday 2 December 2026.

**Data** (lecturer's decision of 14 November 2026). Two files for every student, stored inside the supplied setup cell (bzip2 and base64, one SHA-256 check), so nothing is downloaded during the window. Houses: the Ames housing data, De Cock (2011), Journal of Statistics Education 19(3), 2,930 real sales in Ames, Iowa, 2006 to 2010 (`data_source/ames_decock/AmesHousing.txt`, SHA-256 `6cfe6cb5...`). Machines: AI4I 2020 predictive maintenance, Matzka (2020), UCI Machine Learning Repository, CC BY 4.0, 10,000 rows; it is SYNTHETIC and the brief says so (`data_source/ai4i_uci_601/ai4i2020.csv`, SHA-256 `dc6630cd...`). Question 1 predicts `SalePrice` (USD) from all 36 numeric columns except `Order`, `PID` and `SalePrice`. Task 3b (lecturer, 14 November 2026; 2 marks, shown in the revision class) adds the 43 text columns with one-hot encoding: validation MAE about 15,440 USD against 20,538 for the numeric linear model. It is marked only on hidden rows (scikit-learn goes sparse on the real file and solves iteratively, so the real-file number is not compared). Question 2 warns when `Machine failure` is 1, from the five sensors and `Type` mapped L 0, M 1, H 2; UDI, Product ID and the failure-type columns TWF, HDF, PWF, OSF and RNF are dropped (they give the answer away). Cleaning: houses over 4,000 sq ft of living area removed (5), `living_m2` added, gaps kept for median imputation. Test rows (20 percent, fixed seed) are kept apart in the setup cell and opened once. Fixed seeded split for validation, `sample(frac=0.25, random_state=17)`: houses 1,754 training, 585 validation, 586 test; machines 6,000, 2,000, 2,000. Client limit (confirmed): validation MAE at most 25,000 USD (reference: linear 20,538, tree 26,993, baseline 59,328), latency 50 ms.

**Rehearsal** (unmarked; lecturer, 14 November 2026): exactly the project's tasks 1 to 7 including 3b, files, result names and memo, with one change: the split uses `random_state=29`, so every number differs (validation MAE baseline 54,133, linear 18,397, tree 24,854 USD). Released for the revision class: CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November. It has short self-study notes before the tasks that need them (the fixed seeded split and why the test rows stay apart; fitting on the training rows only; one-hot encoding for Task 3b; logistic regression, the confusion matrix, precision and recall; opening the test set once and refitting), each pointing to the Class 2 or Class 3 slide by title.

**Collection and instant checks** (collection design of 14 November 2026, no Submit step): the student picks the course and types the registration number, which must match the usual pattern (for example 26/BCE/001/PS). On the class list the page shows the name to confirm (This is me). Not on the list: the student types a full name, starts normally and is graded; the result carries the flag NOT_ON_LIST (spot-check list and Collection sheet, information only). One attempt per registration and per email. Start copies the issued notebook into the lecturer's Drive, shares it with the student's Google email as an editor and opens it in Colab, which saves to it. The setup cell sends a silent backup every 5 minutes and warns a student who is in another file. At the deadline a time trigger makes the file read only and collects the newer of the last Drive save before the deadline and the last on-time backup; GitHub Actions marks it in the Colab-matching sandbox. Students use Check my work and I have finished on the entry page; marks are shown only after the release switch. The rehearsal runs the same flow without locking or marking. Set-up: `deploy/setup_pipeline.sh` and `deploy/SETUP_GITHUB_ACTIONS.md`.

**Plain code** (14 November 2026): students write ordinary code under each task heading and store the named results (no function placeholders). The notebook has ONE supplied cell, "Setup: run me first" (data, constants, `choose_model`, `open_test_set`, the backup and the countdown line). The grader puts the original setup cell back, runs the notebook from the top, then re-runs each task's cells (its own added cells included) in a fresh namespace with hidden inputs. See `grader_spec/own_cells.py` and `project_contracts.py`.

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

From `IUEA_Teaching_Plan/second_half/Project/`, with a Python that has scikit-learn, pandas, matplotlib, openpyxl and python-docx (`PY=../../../.iuea-grader-env/bin/python`):

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
