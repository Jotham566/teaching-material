# Second half (Classes 1 to 4): review summary, 12 November 2026

Scope: all four classes for CML3111, CML3112 and CML3113: decks (every slide image and note), lab notebooks, lecturer guides, student PDFs, and the Week 12 project notebooks for coverage. Four reviewers recomputed every number with real scikit-learn 1.9.1 on each cohort's CSV. Per-class detail is in `audit_c1.md` to `audit_c4.md` beside this file. No course file was changed.

**Every number on every slide, note, check table, guide table and notebook output is correct for all three cohorts.** The problems are wording that contradicts the numbers, the order of ideas, rules that differ between classes and the project, things the project tests that no class teaches, and stale student PDFs.

## 1. Before tomorrow's Class 2 (CML3113 08:00, CML3111 11:00)
| Cohort | Where | Problem | Fix |
|---|---|---|---|
| All | Student Slides PDF | All 12 PDFs are dated 3 November, older than the 10 November decks. They lack "practice, does not count", and the Class 4 PDFs say the project is worth 45 percent (it is 40). | Re-export the 12 PDFs from the current pptx. |
| CML3111 | C2 s24 to s26 | Title and notes say no threshold adds a false positive; the lab's own CHANGE task (0.1, 0.2) prints FP 2. | Say "between 0.3 and 0.7" or reword. |
| CML3113 | C2 s24 | Says a lower threshold raises recall; from 0.5 to 0.3 recall stays 1.00 and only FP rises (1 to 2). s25 says it correctly. | Reword s24 to match s25. |
| CML3113 | C2 s16 tree | Splits 22.05 and 21.96 both print "ambient_c <= 22.0?", one under the other; the leaf holds one training row. | Show two decimals, or say it aloud. |
| CML3113 | C2 s28 | Labels for thresholds 0.3 and 0.5 look swapped on the ROC figure. | Move labels. |
| All | C2 slide 28 | "16 points" on the ROC curve; students' plots show 4 or 6. | Say the number the lab produces. |
| All | Lab 2 Step 3 CHANGE and guide answer | Asks whether the products are "close to" the weights (they are not: CML3111 17.38 and 5.64 against 2.81 and 0.93). Guide says probabilities stay almost the same; without the scaler the model finds all positives (TP 3, FN 0), because of LogisticRegression's default penalty, never taught. | Rewrite the prompt and the guide answer. |
| All | Lecturer guide C2 | "Walking the lab" uses CML3112 numbers (19 of 58, weights 2.79/0.73, tree FP 1). Deadline and quiz format contradict the deck (paper quiz vs open 24 hours). | Use the per-cohort table; pick one quiz format. |

## 2. The project tests things the classes do not teach, or teach differently (High)
1. **Choosing a model: three rules.** C3: simplest max_depth within 5 percent of the best. C4 s24: beat the baseline, within 10 percent, good in CV, then simplest (parsimony). Project Task 7: keep models with validation MAE ≤ the client limit (2 deg C, 2 kW, 1.0 kWh/t) and latency ≤ 50 ms, then the lowest MAE. For CML3113, C4 tells students to pick linear over a better-scoring k-NN, the opposite of the project rule. The 10 percent rule also changes C3's chosen depth for CML3112 (7 to 6) and CML3113 (5 to 3).
2. **Latency** (prediction time) is never taught.
3. **Cost of errors.** C2 says only that a missed warning "costs more". The project computes cost = 5 FN + 1 FP and picks the threshold (0.3, 0.5, 0.7) from a cost table.
4. **Standard deviation.** C3 teaches dividing by k (np.std; CML3111 0.33). Project Task 5 requires ddof=1 (0.37).
5. **Group CV.** C3 holds out E1 to E4 (4 folds); the project holds out E1 to E5. Lab 4 says folds go E1, E2, E3, E4; real GroupKFold holds out E2, E1, E4, E3.
6. **Test set.** C3 never says when the test set is opened; the project's test cell refits on E1 to E5 and also scores the threshold, neither taught. Two of the project's true "limits" (one test group; invented costs) are not taught.
7. **Functions on records.** The project's functions take lists of dictionaries and need list comprehensions and sorted(key=...); the labs work only on DataFrames.
8. **Deadline collision.** Block 2 closes the minute each cohort's project sitting starts (CML3112 Tue 1 Dec 11:00; CML3113 Fri 4 Dec 08:00; CML3111 Fri 4 Dec 11:00). The Block 1 close for CML3112 is the start of its Class 3.

## 3. Concept build-up and correctness of wording
- **C1:** the training/validation/test split (s28) and imputation (s29) come after "58 training rows" and validation scores are used from s13. Move s28 to after s11. Gradient descent (s22 to s26) reads as how LinearRegression learns; it uses a direct least-squares formula. s23 shows a loss slope for a loss it never writes, with the error sign flipped. Worked errors on s17 and s20 come from unrounded values (9.25 shown, 9.26 by hand). CML3113 s17 example error 0.03 (0.02 by hand) is a poor choice; record 11 is better. random_state=17 used without saying why.
- **C2:** standard deviation used but never taught (StandardScaler 22.73 vs pandas .std() 22.93). The letter z means the z-score, the logistic score and (C4) scaled features. The tree's one-row leaves are a ready overfitting example for C3.
- **C3:** chosen depth contradicts the gap slide (CML3111 depth 7 has a 3.79 deg C gap, labelled "Good fit" while 8 to 10 are "Overfitting" on a flat curve); the chosen depth changes with the seed. The checklist notes say "yes to all five" means trust, but yes to Q3 means target leakage. Nothing says plain K-fold mixes all groups, which is why GroupKFold scores differ. "25.37 from all rows" is training plus validation. CML3113 recall answer reads "Recall rose from 1.00 to 1.00" (template has no no-change branch; also in the student PDF).
- **C4:** s9 says each weight is the effect of its feature, false once an interaction feature is in. CML3113 s14 "a little penalty barely helps" while alpha 1 is worse. CML3113 ablation bars all read 0.67. CML3112 text says "machine" and "plant" for buildings. Lab step 5 PREDICT comes after its output.

## 4. Recommended order of work
1. Tonight: section 1 (Class 2 fixes and PDF re-export for all cohorts).
2. Before Class 3 (17 and 20 Nov): one model-choice rule and ddof=1 everywhere, matching the project (or change the project to match); the C3 depth and checklist fixes; the CML3113 recall template.
3. Before Class 4 (24 and 27 Nov): teach cost tables, latency, opening the test set once with refit, and one lab step that wraps a pipeline in a function on records; move the Block 2 close off the sitting start.
4. Polish: C1 order and gradient-descent framing (for revision PDFs), notation (z), figures and wording.
