# Engineering ML project: online, 3 hours, individual, fully automatic

Decisions of 13 November 2026 (they replace those of 4 November; see `CHANGE_BRIEF_2026-11-13.md`). The project is **individual**, **timed** (3 hours from Start test, in Colab) and **fully auto-graded** like Practical Test 1. It is taken **online, from anywhere**, in one window for all three courses: **opens Monday 23 November 2026, 00:00 and closes Wednesday 25 November 2026, 23:59 Kampala time** (confirmed). It follows the lecturer's blueprint **"Weeks 1-8 core" (14 November 2026)**: no cross-validation, no cost table, no threshold choice; a light warning question at the fixed threshold 0.5; the model-choice rule is a supplied cell. It counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).

| Part A item | Marks |
|---|---|
| A1 Clean the real data (date fix, all-zero reading, CO2 removed, repeats and impossible values, input unchanged) | 7 |
| A2 Two labelled charts | 2 |
| A3 Split by month | 2 |
| A4 Baseline, linear regression, decision tree (max_depth 4, random_state 17), each with median imputation | 6 |
| A5 MAE and RMSE | 3 |
| A6 No leakage (imputation and the baseline mean from training rows only) | 2 |
| A7 Warning question: probabilities 1; confusion counts, precision and recall at 0.5: 2 | 3 |
| A8 Test set opened once with the supplied cell, after the choice, and its result | 2 |
| A9 Results on the file 1, reproducible 1, functions and MEMO present 1 | 3 |

Part B (15): recommended_model 3, validation_mae 3, test_mae and test_recall 2, improvement_over_baseline 1, limits 3, next_step 1, two written answers 2. No mark is entered by hand. Marks are final by Wednesday 2 December 2026.

**Data.** One real file for every student: Sathishkumar V E, Changsun Shin, Yongyun Cho (2021). Steel Industry Energy Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C52G8C. Licence CC BY 4.0. DAEWOO Steel, Gwangyang, 2018, 35,040 readings, one every 15 minutes. The checked copy is `data_source/steel_uci_851/Steel_industry_data.csv` (SHA-256 `9b1cee6f...2eacc`). It is stored inside the supplied setup cell (bzip2 and base64) and written out with a SHA-256 check, so nothing is downloaded during the window. Question 1 predicts `Usage_kWh` from lagging and leading reactive power, NSM and a weekend flag (the power factors and CO2 are calculated from the target, so they are left out); Question 2 warns when `Usage_kWh` is at or above 60 kWh. Split by month: training January to August (23,328 rows), validation September and October (5,856), test November and December (5,855 after cleaning), opened once. Cross-validation by month over January to October.

**Rehearsal** (unmarked): the same task list on the same file with another target (lagging reactive power, kVarh, warning at 40 kVarh), released for the revision class: CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November. It has short self-study notes before the tasks that need them (the month split and why a random split leaks; fitting on the training rows only; logistic regression, the confusion matrix, precision and recall; opening the test set once and refitting), each pointing to the Class 2 or Class 3 slide by title.

**Collection and instant checks** (collection design of 14 November 2026, no Submit step): the entry page checks the registration number against the class list as it is typed and shows the name to confirm. Start copies the issued notebook into the lecturer's Drive, shares it with the student's Google email as an editor and opens it in Colab, which saves to it. The setup cell sends a silent backup every 5 minutes and warns a student who is in another file. At the deadline a time trigger makes the file read only and collects the newer of the last Drive save before the deadline and the last on-time backup; GitHub Actions marks it in the Colab-matching sandbox. Students use Check my work and I have finished on the entry page; marks are shown only after the release switch. The rehearsal runs the same flow without locking or marking. Set-up: `deploy/setup_pipeline.sh` and `deploy/SETUP_GITHUB_ACTIONS.md`.

**Own cells count** (13 November 2026): students may add their own cells; work is marked wherever it is, as long as the required function names exist when the notebook runs from the top. See `grader_spec/own_cells.py`.

## Files

| Path | What |
|---|---|
| `Student_Brief_<cohort>.docx` and `.pdf` | The student brief: the data, the two questions, the test set and how it is opened once, how the window and the deadline work, help and failures, the time plan, the AI rule, the rules that make a notebook run, how Part A and Part B are marked. |
| `Lecturer_Marking_Guide.docx` and `.pdf` | The data, the reference results, how the time limit works, the timeline, the grading commands, the column mapping, the window, the spot-check list, the marks and the own-cells rule, a worked example, common errors, integrity, what is proved and not proved, open points. |
| `Dean_Summary_ML_Project.docx` and `.pdf` | A short summary for the Dean's office (`tools/build_dean_summary.py`). |
| `Notebooks/<cohort>/ML_PROJECT_student.ipynb` | The marked notebook (the data is inside it). Marked DRAFT until the submission forms exist (`--require-forms`). |
| `Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb` | The unmarked rehearsal. No submit cell. |
| `data_source/steel_uci_851/` | The UCI file and zip as downloaded on 13 November 2026. |
| `deploy/` | The patched portal, gateway (with `/api/check`, `/api/submit`, `/api/status`) and collector files, the collector web app `ml_project_pipeline.gs` (backups, the deadline trigger, collection, extensions), `setup_pipeline.sh`, the project entry page, the packets, the entry links and QR codes, `DEPLOYMENT_STEPS.md`, `SETUP_GITHUB_ACTIONS.md` and `test_ml_project_portal.cjs`. The live files are not touched. |
| `sandbox/` | The Colab-matching grading image (`Dockerfile`, `colab_versions.json`, `requirements.txt`): `docker build -t iuea-notebooks:colab-2026.11 sandbox`. |
| `actions/` | The GitHub Actions workflow (`workflow/grade-ml-project.yml`), `actions_grade.py` (one submission), `final_regrade.py` (the one command after the window), `make_repo_bundle.py` (the private repository's contents), `local_stack.mjs` and `test_actions_e2e.py` (the end-to-end proof with no network). |
| `grader_spec/project_contracts.py`, `memo_spec.py`, `project_numpy_reference.py`, `own_cells.py` | The hidden checks, the Part B keys and keyword rules, the NumPy expected values, the own-cells preparation. PRIVATE. |
| `grader_spec/spec_ML_PROJECT.py`, `hidden/spec_ML_PROJECT_hidden.py` | Handout spec and hidden spec (16 questions: q01 to q09 Part A, q10 to q16 Part B). |
| `grader_spec/rubrics/ML_PROJECT_partA.json`, `ML_PROJECT_partB.json` | The mark schemes (all automatic; 30 and 15). |
| `grader_spec/hidden_data/` | The hidden rows of the function checks (sampled from the file with a small seeded change and problems added), with hashes, for audit. |
| `grader_spec/supplied_cell_hashes.json` | Hashes of the three supplied cells and of every issued TODO cell. |
| `grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb` | Model solutions for the proofs. NEVER give to students. |
| `grader_spec/grade_project.py` | The grading command. Writes the results, the spot-check list, feedback and memo files. |
| `tools/export_for_gradebook.py` | Writes the two gradebook import files. |
| `grader_spec/similarity_check.py`, `offline_harness.py`, `gradebook_import_check.cjs` | Copy check, the no-Docker harness (proofs only) and the real-gradebook import check. |
| `grader_spec/run_proofs.py`, `test_project_grader.py`, `proof_results.txt`, `.json` | The proof matrix, the quick regression test and the recorded result. |
| `tools/project_content.py` | One source for course facts, the window, tasks, starter and solution code, the memo form, the rehearsal notes. |
| `tools/pipeline_cells.py` | The supplied backup code (in the setup cell), the optional Check my notebook cell and the information cell (built from the spec). |
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
