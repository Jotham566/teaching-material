# Engineering ML project: one 3-hour sitting, individual, timed, fully automatic

Decision of 4 November 2026 (it replaces the decisions of 3 November). The project is **individual**, **timed** (one supervised 3-hour sitting in the Week 12 class slot, in Colab) and **fully auto-graded** like Practical Test 1. It covers only Weeks 1 to 11. It counts 45 percent of the course: **Part A, the coded notebook, 30 marks** (24 for the functions and results, 6 for process checks) and **Part B, the decision memo, 15 marks** (a form of fields inside the notebook). No mark is entered by hand. The lecturer reads a short **spot-check list** of flagged cases. A flag never changes a mark.

Proposed sitting (all **proposed, lecturer to confirm**): CML3112 Tuesday 1 December 2026, 11:00 to 14:00; CML3113 Friday 4 December, 08:00 to 11:00; CML3111 Friday 4 December, 11:00 to 14:00 (Kampala). An unmarked **rehearsal** (practice notebook, practice data file, same structure, no solved walk-through) is released right after Class 4 (CML3112 Tuesday 24 November, CML3113 and CML3111 Friday 27 November). Each student receives one of three data variants (A, B, C), allocated at random by the portal as for Test 1.

## Files

| Path | What |
|---|---|
| `Student_Brief_<cohort>.docx` and `.pdf` | The student brief: the two questions, the test set and how it is opened once, how the sitting and the deadline work, the time plan, the AI rule, the rules that make a notebook run, how Part A and Part B are marked. |
| `Lecturer_Marking_Guide.docx` and `.pdf` | How the time limit works, the timeline for the week before and after, the grading commands, the column mapping to the gradebook, what to do on the day, how to read the spot-check list, the marks, a worked example, common errors, what is proved and not proved, open decisions. |
| `Notebooks/<cohort>/<A\|B\|C>/ML_PROJECT_student.ipynb` and `engineering_data.csv` | The three marked variants (Part A cells, memo form, self-checks, Test 1 submit cell). The portal issues these. Marked DRAFT until the submission forms exist (`--require-forms`). |
| `Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb` and `engineering_data_practice.csv` | The unmarked rehearsal on practice data (variant P). Same structure; no submit cell; send it after Class 4. |
| `deploy/` | The patched portal, gateway and collector files, the new form installer, the 9 packets, the entry links and QR codes, `DEPLOYMENT_STEPS.md` and `test_ml_project_portal.cjs`. The live files are not touched. |
| `grader_spec/project_contracts.py`, `memo_spec.py`, `project_numpy_reference.py` | The hidden checks, the Part B keys and keyword rules, the NumPy expected values. PRIVATE. |
| `grader_spec/spec_ML_PROJECT.py`, `hidden/spec_ML_PROJECT_hidden.py` | Handout spec and hidden spec (22 questions: q01 to q15 Part A, q16 to q22 Part B). |
| `grader_spec/rubrics/ML_PROJECT_partA.json`, `ML_PROJECT_partB.json` | The mark schemes (all automatic). |
| `grader_spec/data/<cohort>/<A\|B\|C\|P>/engineering_data.csv` | The data variants. The older single-file `engineering_data.csv` per cohort is superseded and unused. |
| `grader_spec/hidden_data/` | The unseen data for the function checks, with hashes. |
| `grader_spec/supplied_cell_hashes.json` | Hashes of the two supplied cells for every variant. |
| `grader_spec/solutions/<cohort>/<A\|B\|C>/ML_PROJECT_solution.ipynb` | Model solutions for the proofs. NEVER give to students. |
| `grader_spec/grade_project.py` | The grading command. Writes the results, the spot-check list, feedback and memo files. |
| `tools/export_for_gradebook.py` | Writes the two gradebook import files (see the column mapping in its docstring and in the marking guide). |
| `grader_spec/similarity_check.py`, `offline_harness.py`, `gradebook_import_check.cjs` | Copy check, the no-Docker harness (proofs only) and the real-gradebook import check. |
| `grader_spec/run_proofs.py`, `test_project_grader.py`, `proof_results.txt`, `.json` | The proof matrix (135 cases), the one-minute regression test and the recorded result. |
| `tools/project_content.py` | One source for cohort facts, tasks, starter and solution code, memo form and sitting facts. |
| `tools/build_grader_spec.py`, `build_project_notebooks.py`, `build_deploy_bundle.py`, `build_project_docs.py` | The builders. |
| `tools/install_project_bank.py` | Deployment only: copies the notebooks to `assessment_banks/ML_PROJECT/<cohort>/<variant>/`. |

Slides, notes and the Class 4 lab wording are in `../Build/content/c4.py` (another session owns them). The plan is `../Build/kit/make_plan.py`.

## Run order

From `IUEA_Teaching_Plan/second_half/Project/`:

1. `python3 tools/build_grader_spec.py` (writes the data variants, the specs and the rubrics).
2. `python3 tools/build_project_notebooks.py` (draft) or with `--require-forms` (release). Writes the sitting notebooks, the rehearsal, the solutions and the hashes.
3. `python3 tools/build_deploy_bundle.py` (the portal, gateway and collector copies and the packets), then `node deploy/test_ml_project_portal.cjs`.
4. Prove the grader offline (numpy, pandas, matplotlib, openpyxl, node; about 80 to 100 seconds per cohort): `cd grader_spec && python3 run_proofs.py --cohorts CML3112`, then `CML3113`, then `CML3111`. Expect "135 of 135 proof cases behave as required." Quick check: `python3 -m unittest test_project_grader`.
5. `python3 tools/build_project_docs.py` (briefs and guide; the worked example comes from the proof results).
6. Deployment: `deploy/DEPLOYMENT_STEPS.md`.
7. After each sitting, with Docker running: `python3 grader_spec/grade_project.py --zip <IUEA-test-batch zip>`, read the spot-check list, then `python3 tools/export_for_gradebook.py --roster <Grades.csv>`, then `importMarkedResults(<file id>, "ML Project Part A")` and `"ML Project Part B"` in the gradebook, then `recomputeAll()`.

Plan slides and guides: from `../Build/` run `python3 kit/make_plan.py`.

## What is not proven

Real scikit-learn, Docker, Colab, the real Google Forms, the Apps Script deployments and the Cloudflare gateway were not available. See the marking guide (section 10) and `deploy/DEPLOYMENT_STEPS.md`.
