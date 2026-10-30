# Weeks 8 to 12 rebuild: what changed, how it was checked, and coverage against industry standards

30 October 2026. Follows [Week8_Benchmark_and_Change_Log_2026-10-30.md](Week8_Benchmark_and_Change_Log_2026-10-30.md). Original decks are in `decks/_backup_2026-10-30/`.

## 1. What every deck now does

Every term is explained in plain words before a slide uses it. Each week opens with objectives written for that week and a vocabulary table with a plain meaning and an example from the student's own data. Each week closes with a "Words from today" slide and an exit check that asks for an explanation in the student's own words. Every one of the 15 decks (3 cohorts, Weeks 8 to 12) has a spoken-script note on every slide, in first person plural, written in the style of the AI and Data Science Professional course. No note uses the old "Explanation to give" labels.

| Week | Slides now (was) | New slides | What was removed |
|---|---|---|---|
| 8 | 71 (60) | Kinds of ML; two vocabulary tables; why rows are held back; scatter of the cohort's own data; the line as an equation; error measures MAE, MSE, RMSE; NumPy shape (two slides); loss and gradient descent (two slides); blanks and the imputer; pipeline; decision tree; one MAE per model; results table; words from today | Data Analysis Project block (6 slides) |
| 9 | 51 (42) | Vocabulary; classification as a yes or no question; building the alert label; why accuracy misleads; logistic regression; scaling; split and fit a classifier; threshold; scoring vocabulary; confusion matrix of our model; F1; moving the threshold; ROC and AUC; decision tree classifier; words from today | Three repeated "operations" cards, the get_dummies detour |
| 10 | 48 (54) | Vocabulary (two tables); overfitting in three pictures, a loop and a curve; why one validation group can mislead; the Week 8 pipeline inside cross-validation; leakage in four slides including a computed leaky score; words from today | About 25 slides that repeated Week 8 |
| 11 | 40 (50) | Vocabulary; why derived features help (curved example); which input moves the prediction more; an honest ablation verdict; inputs available at prediction time; words from today | About 20 slides that repeated Week 8 |
| 12 | 45 (64) | Vocabulary; Week 8 line rebuilt; three candidates compared; a three-row candidate table; random forest (two slides); boosting; model card; who is affected when a model is wrong; care with personal data; words from today | About 30 slides that repeated Week 8 |

The Week 8 assignment, the form links, the quizzes, the deadlines and every graded function name are unchanged. All 15 decks carry the correct Week form (A7 to A11) and the correct quiz link.

## 2. How the new slides were checked

1. **Every number on a new slide is computed**, from the cohort's own CSV or from the code printed on the slide, by `scripts/week_reference_numpy.py`. Nothing is typed by hand.
2. **The code on the slides was run, in slide order**, for all 15 decks (`scripts/verify_week_slides_20261030.py`). Each printed result was compared with the output panel. Result: 0 problems. This ran against a NumPy stand-in for scikit-learn, because scikit-learn is not installed where the slides were written. It proves the cells run in order with consistent names and formats. It does not prove that real scikit-learn prints the same digits.
3. **Terms before use**: `scripts/audit_term_order_20261030.py` checks that each key term is defined on an earlier slide than its first use. Result: 0 flagged, with four reviewed exceptions recorded in the script.
4. **Two independent reviewers** read the decks cold and recomputed the numbers. They found three critical errors in Weeks 10 to 12 and five in Weeks 8 and 9, all fixed:
   - the Week 11 ablation numbers did not match the slide code (the real result is that the extra feature makes the error slightly larger, and the slides now say so and explain why);
   - claims in Weeks 8 and 9 used the sealed test group E6 (the 0.95 correlation, the alert counts and the "always no" accuracy). They now use training rows only, so E6 stays unopened;
   - a leftover renaming artifact (`baseline_errors`), a fill demonstration that described blanks the validation rows do not contain, a threshold story that the data does not show, gradient described as pointing downhill, and `y` described as a "row" when it is a one-dimensional array.
5. Style rules from your standing feedback were applied and scanned: no "X, not Y" constructions, no em dashes in titles or notes, no stage directions in the notes.

**Still to do on your Mac, about ten minutes:** run `python3 scripts/verify_week_slides_20261030.py` inside the environment that has scikit-learn. It runs the same cells against the real library and reports any digit that differs. Then open each deck once in PowerPoint and click through; I could only render in LibreOffice.

## 3. Coverage against industry standards

Sources: the ACM/IEEE-CS/AAAI Computer Science Curricula 2023 AI knowledge area (machine learning unit), Google's Machine Learning Crash Course (linear regression module checked; the rest from its published outline), DeepLearning.AI Machine Learning Specialization Course 1 (week topics checked), CMU 10-301/601 and CU Boulder CSCA 5622 (outlines as returned by search), plus your own Professional course.

| Topic expected in an introductory ML course for engineers | Source | Where it is taught |
|---|---|---|
| ML task types: regression, classification, clustering, reinforcement | CS2023 core | Week 1 named; Week 8 map; clustering in Semester 2; reinforcement learning is outside both semesters |
| Training as minimising a loss, gradient descent, learning rate | MLCC, DeepLearning.AI | Week 8 introduced with a computed example; neural-network training in Semester 2 |
| Linear regression and its coefficients | all | Week 8, Week 11 |
| Logistic regression and probabilities | MLCC, DeepLearning.AI | Week 9 (new) |
| Decision trees | CMU, B.Tech syllabi | Week 8 regression, Week 9 classification |
| Random forests, boosting | CU Boulder, B.Tech | Week 12 concept and one line of code (no printed result); boosting in depth in Semester 2 |
| Metrics: error measures, confusion matrix, precision, recall, F1, ROC and AUC | CS2023 knowledge-area core | Weeks 8 and 9 |
| Train, validation and test sets; overfitting; sources of error | CS2023 core | Weeks 8 and 10; bias and variance named in Week 10 |
| Cross-validation and spread | CS2023, all | Week 10 |
| Data leakage | professional practice | Week 10 (new, four slides) |
| Feature engineering and scaling | all | Weeks 9 and 11 |
| Model selection under constraints; model documentation | professional practice | Week 12; model card (new) |
| Ethics, privacy, who is affected by errors | CS2023 core ("ethics for ML"), MLCC fairness | Week 12 (new, two slides and the model card); the course had none before |
| Reproducible workflow | MLCC production | Week 13 |
| Regularisation (Ridge, Lasso) | CU Boulder, DeepLearning.AI, most syllabi | **Gap in Semester 1.** Planned for Semester 2 |
| K-nearest neighbours, support vector machines | most syllabi | **Gap in Semester 1.** Planned for Semester 2 |
| Neural networks, explainable ML, unsupervised learning | CS2023 core and knowledge area | Semester 2 |

Semester 2 as planned in your roadmap benchmark: regularisation, KNN and SVM, boosting in depth, clustering and PCA, neural networks with PyTorch, convolutional networks with transfer learning, time series, explainable AI, text embeddings, deployment basics, and SQL and API data ingestion.

**Decision for you.** The two Semester 1 gaps that most introductory syllabi cover are regularisation and KNN. Week 13 currently has no new assignment and no machine-learning content, so a short block there (Ridge as the standard fix for the overfitting seen in Week 10, and KNN as a one-slide contrast with trees) would close both without touching any assessment. I have not built it. Say the word and I will, using the same format.

## 4. Known limits and items I left alone

- **Real scikit-learn has not run on the new cells** (section 2, point 2). Two places most likely to differ in the last digit: the first five logistic probabilities (Week 9) and the tree errors (Weeks 8 and 10).
- **Not regenerated:** the lecturer-notes Markdown files, the guided-practice notebooks and the student ZIPs. Their slide numbers no longer match Weeks 8 to 12. The graded notebooks and assignment ZIPs are unaffected.
- **Rebuilds overwrite these edits.** After any run of `build_decks.py`, re-apply with:
  `python3 scripts/patch_week8_20261030.py && python3 scripts/patch_weeks8b_12_20261030.py --from-backup && python3 scripts/apply_spoken_notes_20261030.py`
- **Left as found:** the Week 12 optional video repeats the Week 10 cross-validation video; the original Week 10 function-example slides name `to_dict` before the cards that explain it; some generic captions under older code slides do not name the variable the cell creates; the Week 12 assignment window is three hours, which matches the registry.
- **Spoken notes for Weeks 1 to 7 and 13 to 15 are not yet in the new style.** Weeks 13 to 15 also carry renaming damage ("state the operational test_data"). Both are the natural next job.
- The limits used for the alert label (80 deg C, 54 kW, 13.5 kWh/t) are teaching assumptions and are labelled so on the slides.

## 5. Files

Scripts in `scripts/`: `patch_week8_20261030.py`, `patch_weeks8b_12_20261030.py`, `wk_8b_9_20261030.py`, `wk_10_12_20261030.py`, `deckkit_20261030.py`, `week_figs_20261030.py`, `week_reference_numpy.py`, `apply_spoken_notes_20261030.py`, `verify_week_slides_20261030.py`, `audit_term_order_20261030.py`. Spoken notes for the retained slides: `data/spoken_notes_w8_12_20261030.json`. Figures: `figs/week8b_12_20261030/`.


## 6. Update: the full rebuild (Weeks 1 to 15 and the new Week 13)

**Week 13 is a new deck, 41 slides** (was 25). The first half is new: regularisation with polynomial features and ridge regression (what alpha does to the coefficients and the errors, with the cohort's own numbers), nearest neighbours (a worked prediction from three neighbours, choosing k), five candidates compared on the same validation rows, and a guide to which model for which job. Lasso, forests and boosting are named and not coded. The second half keeps the reproducibility slides and adds two: recording the versions you used, and a fresh start in Colab. There is no new assignment. This closes the two Semester 1 gaps listed in section 3 (regularisation, and KNN). SVM stays in Semester 2.

**Spoken-script notes now cover all 45 decks (2,434 slides).** Every note is in first person plural, with no stage directions and none of the old "Explanation to give" labels. Where a slide differs between cohorts, each cohort has its own script. A scan of every note found no em dashes, no "X, not Y" constructions, no unfilled placeholders and no empty notes. Four independent reviewers read the Week 1 to 7, 13, 14 and 15 scripts against the slides. They found no critical errors in Weeks 1 to 7, 14 and 15. In Week 13 they found one contradicted claim, the ridge loss written as an average where scikit-learn's Ridge uses a sum, a ridge candidate that was not like-for-like, a Colab example that named the wrong target, and some terms used before they were explained. All of those are fixed. About 100 smaller points were also fixed: rules and procedures in notes that the slides do not state (mostly on the test-day and submission slides), line-number mismatches in code walkthroughs, and the remaining antithesis phrasing.

**Slide-text repairs.** Weeks 13 to 15: leftover renaming damage ("the operational test_data", "the linear_model", "a separate equipment_data"). Week 4: a caption describing `from` where the code has none. Week 6: a leftover crusher-energy caption on the motor-temperature deck, and a doubled "demand".

**Companion files regenerated from the finished decks:**
- `decks/lecturer_notes/*.md` for all 45 decks (slide text plus the spoken script).
- `guided_practice/<cohort>/W08` to `W13`: new guided notebooks. Every code cell was run in slide order for all 18 notebooks with no errors (against the same NumPy stand-in, see section 2).
- `student_packages/<cohort>_W08` to `W12` student ZIPs: the guided notebook inside each ZIP is replaced. The assignment notebooks, data files and instructions inside are untouched, and the previous ZIPs are saved in `student_packages/_backup_2026-10-30/`. Share the refreshed ZIPs; students who already downloaded one can keep working in it.

**To re-apply everything after a rebuild with `build_decks.py`:**

```
python3 scripts/patch_week8_20261030.py
python3 scripts/patch_weeks8b_12_20261030.py --from-backup
python3 scripts/patch_weeks1_7_text_20261030.py
python3 scripts/apply_spoken_notes_20261030.py
python3 scripts/build_companions_20261030.py
python3 scripts/verify_week_slides_20261030.py
python3 scripts/audit_term_order_20261030.py
```

**Still open:**
- The real scikit-learn run of `verify_week_slides_20261030.py` on your Mac, and a click-through in PowerPoint.
- The Week 5 title slide shows a normal Friday 9 October class, while a later slide says that Friday has no class.
- The Week 12 optional video repeats the Week 10 cross-validation video.
- Minor items from the reviews that I left as the slide text stands: the "Save your work" line appears twice on the Week 13 exit slide, a few generic captions, and the repeated "check the slide for the date, time and room" pointer in opening notes.
- Weeks 1 to 7 already taught: their slide content is unchanged apart from the repairs above. Only the notes changed.

## 7. Block assessment arrangement and final fixes (30 Oct 2026)

Week 8 onwards moves from weekly quizzes and assignments to one assignment pack and one quiz sitting per three classes. Policy, grading and hand steps: `Block_Assessment_Arrangement_2026-10-30.md`. Scripts: `patch_blocks_20261030.py` (decks and notes), `apply_block_policy_20261030.py` (registry, deadlines, Apps Script), `patch_block_docs_20261030.py` (guides, banks, ZIPs, index, grader README), `patch_block_docx_20261030.py` (syllabi, master plan, quiz operations guide). Also fixed: Week 5 title slide contradiction, Week 12 video (now StatQuest bias and variance), duplicate exit slide, generic captions, repeated date pointer. Checks after the last run: verify 0 problems (NumPy stand-in), term-order audit 0, note lint clean on 2,431 slides, links 0 missing. Open: real scikit-learn run on the Mac, PowerPoint click-through, Q12 bank.

### 7a. Corrections after section 7

Week 6 is waived for all three cohorts (`Practical_Revision_Week6_Waiver.md`). Section 7 first assumed CML3111 kept it. Everything now says: weekly Weeks 1 to 5, best 3 of 5, quizzes out of 45, assignments out of 160. Fixed in the policy JSON, the Week 1 decks (slide 9), the B1/B2 guides, the CML3111 syllabus, the master plan and the quiz guide. `grader/continuous_assessment.py` gained `coursework_totals()` (block rule applied to the ledger, receipts named by teaching week: Q8 is the Week 8 quiz) with tests. The Week 13 quiz (Q12) was rewritten: ridge penalty table, choosing k, nearest neighbours without scaling, a missing data file, a saved output that will not rebuild. The earlier `pandas_quiz_revision.py` layer no longer overrides Week 13. `create_quiz_forms.gs` was regenerated (only Week 13 changed) and now has `replaceWeek13Questions()`. `verify_quiz_arithmetic.py` has new Week 13 checks, all passing; its Week 6 to 12 mix, antithesis and View-score failures come from the earlier pandas revision and were not touched.

### 7b. Student packages, Weeks 8 to 12

Each ZIP now holds the notebook, its CSV files, `guided_practice.ipynb` and one `START_HERE.md` of about 300 words (block part, deadline, form link, seven steps, four rules). The old `00_START_HERE.txt`, `ASSIGNMENT_INSTRUCTIONS`, `TASKS.md`, `STUDENT_HOW_TO.md` and `SUBMIT_HERE.txt` are gone from the ZIPs. The same text is the web guide `student_guides/<cohort>/W0X.md`, the bank copy and the notebook's first instruction cell, so all four agree. `data/submission_links.json` closing times moved to the block deadlines. Build: `scripts/build_block_packages_20261030.py`. `build_companions_20261030.py` now refreshes the guided notebook inside the current ZIP instead of restoring the backup.

### 7c. First real scikit-learn run (30 Oct 2026, scikit-learn 1.9.1)

Seven outputs differed, all deep decision trees (Week 10 depth sweep and leakage demo, and the Week 8 tree for CML3113). My NumPy tree broke ties between equal splits differently from scikit-learn. `scripts/sk_tree_replica.py` now copies scikit-learn's tree growth (float32 inputs, random feature order from `random_state`, strictly-greater improvement, midpoint thresholds, left-first depth-first order) and reproduces all seven real outputs exactly. The decks, figures, notes, guided notebooks and ZIPs were rebuilt from it. Changed numbers: Week 10 depth 5 to 10 validation errors, the honest and leaky demo, the CML3113 tree MAE (1.18 became 1.20, so the Week 8, 11, 12 and 13 tables follow), and the displayed split thresholds (42.94 became 42.93). The Week 10 slide "validation error stalls" was not true for CML3111 and CML3112 at depth 8, so it now says training error falls to almost zero while validation error stays far above it. Ridge, nearest neighbours, logistic regression and the Week 9 classifier already matched scikit-learn.

### 7d. Test 1 and Test 2 rubrics

The grader rubrics (`grader/rubrics/TEST1.json`, `TEST2.json`) are correct. They match the student notebooks (Test 1: 20, 10, 20, 10, 15, 10, 5, 10; Test 2: 20, 30, 20, 30) and the Week 14 deck. The syllabi, master plan, lecturer guide and `plan_content.RUBRICS` still described the first design: a report-style Test 1 and an end-to-end Test 2 with cross-validation, three limitations and a typed Part B in an offline lab. `scripts/patch_test_rubrics_20261030.py` brings them in line: the Rubrics sheet, test rows, the Week 7 and Week 14 session cells, the "why the tests are unaided" text, the integrity risks, and `plan_content.py`. It is idempotent; re-run it after `build_syllabi.py` or `build_xlsx.py`. `tests/test_course_content.py` now checks titles and marks for the two tests. Not changed: the Week 7 session logistics (past), the Week 1 pre-flight checklist and the beginner guide, which still say the tests are offline.

### 7e. Practical Test 2 now covers Weeks 8 to 13

New marks (version `2026.12-colab-v3-weeks8-13`): group split 10, baseline, linear and tree predictions 15, MAE and RMSE 5, classification and cost 10, group cross-validation 10, feature ablation 10, model selection 10, ridge and nearest neighbours 15, six interpretation choices 15 (2.5 each). Two functions are new (`group_cv_mae`, `ridge_and_knn`); the other new tasks reuse existing contracts (`classification_metrics`, `ablation_metrics`, `select_model`). Expected values for the new tasks come from NumPy (`grader/test2_numpy_reference.py`), so the hidden checks do not depend on a scikit-learn build. Changed: `engineering_contracts.TASKS`, `colab_exam_contracts.py`, `engineering_pandas_reference.py` (reference solutions), `build_colab_exams.py` (now `build(only=('TEST2',))`), the 9 Test 2 notebooks, zips and guides, `specs/spec_TEST2*.py`, `rubrics/TEST2.json`, `test_portal/Packets.gs`. The Week 14 decks gained nine revision slides with spoken notes (`patch_test2_deck_20261030.py`, run last in the deck pipeline), and the marks and order-of-work slides were rewritten. The Week 14 PDFs and revision ZIPs were re-exported with LibreOffice. Test: `tests/test_test2_weeks8_13.py`. The sandbox has no Docker or scikit-learn, so `tests/test_colab_exams.py` and a real-scikit-learn run of the new test still need to be done on the Mac.

Offline wording: the plan, syllabi, lecturer guide, beginner guide, Week 1 pre-flight checklist and student setup guide now say both tests run in Colab. Teaching-session mentions of datasets "distributed offline" and the Windows offline installer are unchanged because they are about classes, not the tests.
