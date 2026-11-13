# Engineering ML project: online, 3 hours, individual, fully automatic

Decisions of 13 November 2026 (they replace those of 4 November; see `CHANGE_BRIEF_2026-11-13.md`). The project is **individual**, **timed** (3 hours from Start test, in Colab) and **fully auto-graded** like Practical Test 1. It is taken **online, from anywhere**, in one window for all three courses: **opens Monday 23 November 2026, 00:00 and closes Wednesday 25 November 2026, 23:59 Kampala time** (confirmed). It covers Weeks 1 to 10 (up to Class 3); the Week 11 tasks are cut and the model-choice rule is a supplied cell. It counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40): **Part A, the coded notebook, 30 marks** (21 for functions checked on hidden rows, 3 for results on the file, 6 for process) and **Part B, the decision memo form, 15 marks**. No mark is entered by hand. Marks are final by Wednesday 2 December 2026.

**Data.** One real file for every student: Sathishkumar V E, Changsun Shin, Yongyun Cho (2021). Steel Industry Energy Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C52G8C. Licence CC BY 4.0. DAEWOO Steel, Gwangyang, 2018, 35,040 readings, one every 15 minutes. The checked copy is `data_source/steel_uci_851/Steel_industry_data.csv` (SHA-256 `9b1cee6f...2eacc`). It is stored inside the supplied setup cell (bzip2 and base64) and written out with a SHA-256 check, so nothing is downloaded during the window. Question 1 predicts `Usage_kWh` from lagging and leading reactive power, NSM and a weekend flag (the power factors and CO2 are calculated from the target, so they are left out); Question 2 warns when `Usage_kWh` is at or above 60 kWh. Split by month: training January to August (23,328 rows), validation September and October (5,856), test November and December (5,855 after cleaning), opened once. Cross-validation by month over January to October.

**Rehearsal** (unmarked): the same file with another target (lagging reactive power, kVarh, warning at 40 kVarh), released right after Class 3: CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November.

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
| `deploy/` | The patched portal, gateway and collector files, the form installer, the packets, the entry links and QR codes, `DEPLOYMENT_STEPS.md` and `test_ml_project_portal.cjs`. The live files are not touched. |
| `grader_spec/project_contracts.py`, `memo_spec.py`, `project_numpy_reference.py`, `own_cells.py` | The hidden checks, the Part B keys and keyword rules, the NumPy expected values, the own-cells preparation. PRIVATE. |
| `grader_spec/spec_ML_PROJECT.py`, `hidden/spec_ML_PROJECT_hidden.py` | Handout spec and hidden spec (20 questions: q01 to q13 Part A, q14 to q20 Part B). |
| `grader_spec/rubrics/ML_PROJECT_partA.json`, `ML_PROJECT_partB.json` | The mark schemes (all automatic; 30 and 15). |
| `grader_spec/hidden_data/` | The hidden rows of the function checks (sampled from the file with a small seeded change and problems added), with hashes, for audit. |
| `grader_spec/supplied_cell_hashes.json` | Hashes of the three supplied cells and of every issued TODO cell. |
| `grader_spec/solutions/<cohort>/ML_PROJECT_solution.ipynb` | Model solutions for the proofs. NEVER give to students. |
| `grader_spec/grade_project.py` | The grading command. Writes the results, the spot-check list, feedback and memo files. |
| `tools/export_for_gradebook.py` | Writes the two gradebook import files. |
| `grader_spec/similarity_check.py`, `offline_harness.py`, `gradebook_import_check.cjs` | Copy check, the no-Docker harness (proofs only) and the real-gradebook import check. |
| `grader_spec/run_proofs.py`, `test_project_grader.py`, `proof_results.txt`, `.json` | The proof matrix, the quick regression test and the recorded result. |
| `tools/project_content.py` | One source for course facts, the window, tasks, starter and solution code, the memo form. |
| `tools/build_grader_spec.py`, `build_project_notebooks.py`, `build_deploy_bundle.py`, `build_project_docs.py`, `build_dean_summary.py` | The builders. |
| `tools/install_project_bank.py` | Copies the notebooks to `assessment_banks/ML_PROJECT/<cohort>/A/`. |

## Run order

From `IUEA_Teaching_Plan/second_half/Project/`, with a Python that has scikit-learn, pandas, matplotlib, openpyxl and python-docx (`PY=../../../.iuea-grader-env/bin/python`):

1. `$PY tools/build_grader_spec.py` (checks the data file, writes the specs, the rubrics and the hidden rows).
2. `$PY tools/build_project_notebooks.py` (draft) or with `--require-forms` (release). Writes the notebooks, the rehearsal, the solutions and the hashes.
3. `$PY tools/build_deploy_bundle.py`, then `node deploy/test_ml_project_portal.cjs`.
4. Prove the grader offline (no Docker; real scikit-learn when the Python has it): `cd grader_spec && $PY run_proofs.py --cohorts CML3112`, then `CML3113`, then `CML3111` (or all three at once). Expect every case to pass. Quick check: `$PY -m unittest test_project_grader`.
5. `$PY tools/build_project_docs.py` (briefs and guide; the worked example comes from the proof results), then `$PY tools/build_dean_summary.py`. The PDFs are written by LibreOffice with a private profile that holds the Lato fonts, and the build stops if a PDF does not embed Lato.
6. Deployment: `deploy/DEPLOYMENT_STEPS.md`. Then `$PY tools/install_project_bank.py`.
7. After the window, with Docker running: `python3 grader_spec/grade_project.py --zip <IUEA-test-batch zip>`, read the spot-check list, then `python3 tools/export_for_gradebook.py --roster <Grades.csv>`, then `importMarkedResults(<file id>, "ML Project Part A")` and `"ML Project Part B"` in the gradebook, then `recomputeAll()`.

Slides, notes and the lab wording are in `../Build/` (another session owns them).

## What is not proven

Colab itself, the real Google Forms, the Apps Script deployments and the Cloudflare gateway were not available. See the marking guide (section 10) and `deploy/DEPLOYMENT_STEPS.md`.
