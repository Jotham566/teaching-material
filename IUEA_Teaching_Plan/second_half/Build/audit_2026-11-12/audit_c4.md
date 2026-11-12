# Audit: CML3111 Class 4 (Week 11, 27 Nov 2026), "Features and choosing a model, and your project"

**Verdict.**
1. The numbers are right. I recomputed every one on the slides and in the notes, the check table and the guide with real scikit-learn 1.9.1, independently of the reference, and all of them match. The deck is clean, readable and well illustrated.
2. The main weakness is the hand-off to the project. The model-selection rule taught on slide 24 is not the rule the project marks (Task 7: client MAE limit plus latency limit, then lowest MAE). Latency, refitting on E1 to E5 before the test, the test-set limits and the threshold or warning part of the memo are never taught.
3. The student PDF (3 Nov) is stale and says the project is worth 45 percent, while the pptx says 40 percent. Class 3 tells students to keep tree depth 7 and to use 5 percent parsimony with ddof=0. Class 4 and the project use depth 4, a 10 percent rule, and ddof=1 over 5 folds.

Severity counts: High 3, Medium 11, Low 12 (26 findings).

## Findings

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| F1 | Slide 24 (and 7, 32, lab step 7 READ) | 2, 3 | **High** | The taught rule is "1 Beat the baseline clearly, 2 Score within 10 percent of the lowest validation error, 3 Score well in cross-validation, 4 pick the simplest". The project's Task 7 `choose_model` keeps candidates with `validation_mae <= MAX_MAE` (2.0 deg C, client limit) **and** `latency_ms <= MAX_MS` (50 ms), then takes the **smallest** validation MAE, with ties broken by latency and then by name. That rule has no parsimony step and no 10 percent band. A student who applies the slide rule cannot write the project function. | Add one slide after 24: "In industry the client sets limits. Keep the models that meet every limit (MAE at most X deg C, prediction time at most Y ms), then choose the lowest validation MAE, and break ties by the faster model." Work it by hand on the five-model table with invented latencies. Add a lab cell `choose_model(...)` with a list comprehension and `sorted(key=lambda ...)`. Alternatively, change the project rule to match the slides. |
| F2 | Whole deck, all classes | 2 | **High** | **Latency (prediction time in ms) is never taught** in Classes 1 to 4. The only hit for "prediction time" is in c3 target leakage, with another meaning. The project uses `LATENCY_MS`, `MAX_MS` and the latency tie-break. | Define latency (inference time, ms) on the new slide from F1. Give the invented teaching numbers and say why a client cares about it, for example a controller that must answer within 50 ms. |
| F3 | Student Slides PDF (3 Nov) vs pptx (10 Nov), slides 28, 29, 37 | 1, 2 | **High** | The PDF says "worth **45** percent" on three slides; the pptx says 40 percent, scaled from 45. PDF slide 37 also lacks "It is practice and does not count toward your final mark." Students revise from the PDF. | Re-export the Class 4 student PDF from the current pptx before it is released. |
| F4 | Slide 26 and the memo slide 27 | 2 | Medium | The project's `open_test_set` **retrains on all development rows E1 to E5** and then scores E6. It also reports warning precision and recall at the chosen threshold. The deck never says that the final model is refitted on train plus validation before the test, or that the threshold is tested too. | Add one line to slide 26: "After you choose, the model is retrained on E1 to E5 (training plus validation) and scored once on E6. The decision threshold you chose is tested at the same time." |
| F5 | Slides 25, 27; lab step 8 | 2 | Medium | The Part B limits list rewards "test set is a single group, so one estimate that may be luckier or unluckier" (D) and "client limits, thresholds and costs are invented teaching numbers" (A). Slide 25 teaches only three limits: synthetic data, 15 validation rows, and test not yet used. It never mentions that the test set is one group or that the costs and limits are invented. The project's "next step" answer (E: collect real data from more motors and re-validate with group CV) is also not the next step the deck models ("Score the held-out test set once"). | Add the two missing limits to slide 25. In the memo example, show a post-test next step ("collect real measurements from more motors and re-validate"). |
| F6 | Slides 7, 21 to 27; lab | 2, 3 | Medium | The project memo combines **Question 1 (regression model) and Question 2 (warning threshold chosen by cost)**. Class 4 never returns to classification, so there is no bridge from Class 2's cost and threshold to the final recommendation. | Add one line on slide 27, "Recommendation: a model **and** a decision threshold", plus one row in the memo example. Recall the Class 2 cost rule (`cost = 5 FN + 1 FP`, choose the lowest cost, take the higher threshold on a tie) in the lab. |
| F7 | Slides 21 to 23 vs project Task 5 vs Class 3 | 2, 3 | Medium | Class 3 and Class 4 use **4** folds (E1 to E4). Class 3 reports `np.std` with **ddof=0** (lab3), and Class 4 reports a min-to-max range. The project uses **5** folds (E1 to E5) and a "spread" with **ddof=1**. Neither difference is taught. | In Class 4, show "standard deviation of the fold MAEs (sample, ddof=1)" beside the range, and say once that the project rotates through all five development groups because the validation group joins in. Alternatively, align the project with Class 3. |
| F8 | Slides 23 and 31 vs Class 3 | 3 | Medium | Class 3 (CML3111) chose **max_depth 7** with the 5 percent parsimony rule, and its take-away says "keep the chosen max_depth". Class 4 and the project use a depth-4 tree (MAE 4.79) without a word. Class 3 also used **5 percent** and Class 4 uses **10 percent** for "close". | Add one sentence on slide 23 or 21: "Depth 4 is fixed here, as in Class 1 and the project. Class 3's tuned depth 7 scores 3.91." Use one tolerance across Classes 3 and 4, or say why it changed. |
| F9 | Slide 9 symbol table and notes; lab cell 12 | 1 | Medium | "Weights: one more unit of a feature adds its weight … while the other features stay fixed." In model B that is false for x₁ and x₂, because x₃ = x₁x₂ moves with them: one more percent of load adds 0.6181 + 0.0031·x₂ ≈ 0.72 deg C at 31.71 deg C. | Add: "In model B, x₃ changes when x₁ or x₂ changes, so b₁ alone is not the effect of load. The effect is b₁ + b₃·x₂." Alternatively, limit the sentence to model A. |
| F10 | Slide 24 ladder | 4 | Medium | "Beat the baseline model clearly" and "Score well in cross-validation" are undefined, so a beginner cannot apply them. "Simplest" is not ordered either; whether linear is simpler than ridge or the tree is never stated. | State thresholds and a simplicity order (baseline < linear < ridge < tree, k-NN), or replace the ladder with the project rule (F1). |
| F11 | Lab step 5, cells 20 to 21 | 6 | Medium | The **PREDICT** prompt ("Will a stronger penalty help it?") comes *after* the code cell that prints the ridge MAEs (lab4.py lines 100 to 103). Part B (cell 23) has no PREDICT, and neither does step 4. | Move `nb.predict` above the part A code. Add a PREDICT before part B ("Which alpha will give the lowest validation error?"). |
| F12 | Slide 37 | 2 | Medium | "Block 2 assignment closes Friday 4 December, 11:00", the same minute the CML3111 project sitting starts (11:00 to 14:00). | Move the deadline earlier, for example Thu 3 Dec, or confirm with the lecturer. |
| F13 | Slide 3 caption vs clock | 4 | Medium | The caption says the quiz opens "in the last 20 minutes". The clock puts the quiz at 2:25 (last 35 minutes) and the "project briefing" at 2:50, but the project slides (28 to 30) sit in the concepts half. | Make the caption match the clock ("the quiz opens at 2:25"). Rename the 2:50 block "Close and questions on the project". |
| F14 | Concepts half (slides 4 to 32) | 3 | Medium | 29 concept slides, 5 of them formula or worked tables, in 75 minutes (10+35+30). That is about 2.6 minutes per slide for ridge, k-NN, ablation, one-hot, scaling, CV formulas, selection, memo and 3 project slides. Ridge and k-NN are "previews" that the project does not test. | Move slides 15, 16, 18 and 19 (ridge and k-NN formulas and worked tables) to an appendix after slide 38, and spend the time on F1, F4 and F5. |
| F15 | Slide 9 y-hat row | 1 | Low | "6.3765 + 36.56 + 27.45 + 5.81 = 76.2". With the unrounded b₃ (0.0030679) the term is 5.75 and the prediction is **76.1**. The 5.81 comes from rounding b₃ to 0.0031 and then multiplying by 1875.6. | Show b₃ as 0.00307 and the term as 5.75 = 76.1, or add "(with rounded weights)". |
| F16 | Slide 22 | 3, 5 | Low | The CV formula uses index f and MAE_{m,f}, but f is not in the symbol table. The formulas render small (size 15). The fold list "0.79, 0.87, 0.75, 0.76" does not say which group is which (it is E1, E2, E3, E4). | Add the row "f: fold, one held-out group (E1 to E4)". Label the folds by group. Raise the formula size. |
| F17 | Slide 18 vs 19 | 3 | Low | The formula is (x_j − x′_j), new minus training, and the notes say "subtract the training row from the new row". The worked line computes training minus new: (−0.123 − (−0.100)). Squaring hides the difference, but a beginner may stall on it. The symbol table names "N" while the formula uses N_k, and "y" while it uses y_i. | Write the worked line as (−0.100 − (−0.123))². Use N_k and y_i in the table. |
| F18 | Slide 17 picture | 5 | Low | The plot shows about 20 of the 58 training rows (a zoomed window), but the caption says "Grey dots: training rows". | Change the caption to "Grey dots: the training rows near the new row (zoomed in)". |
| F19 | Slide 38 take-away card | 5 | Low | The label "Model comparison table" overlaps its value text "Five candidate models, one protocol". | Shorten the value or increase the line spacing. |
| F20 | Slide 14 point 2; slide 16 title | 4, 7 | Low | "Not the later two-feature model." is a fragment. "but on this ridge regression on two features the error grows" is clumsy. | Use "These errors belong to the degree-6 curve, not to the two-feature ridge model on slide 16." and "A bigger alpha shrinks the weights, and here the validation error grows". |
| F21 | Lab step 7 markdown | 6 | Low | It says the folds hold out "E1, then E2, E3 and E4". Real `GroupKFold(4)` order is E2, E1, E4, E3 (checked). The output shows only mean, min and max, so nothing breaks. | Say "each of E1 to E4 is held out once". |
| F22 | Facilitator prep (guide p1) | 1 | Low | "The deck has 32 authored slides"; the deck has 38. | Change it to 38, or "about 30 authored". |
| F23 | Slide 20 notes | 1 | Low | "Next semester you meet support vector machines, random forests and boosting" is a curriculum promise. | Hedge it: "are planned for next semester". |
| F24 | Slide 29 note | 1 | Low | "Nothing in the project is taught after Class 4" is true only after F1 and F2 are fixed. | Fix F1 and F2. |
| F25 | Notes throughout | 7 | Low | Every note ends on a question ("Which … do you find hardest …?"), and seven notes open with "Here is/are". | Vary the endings. Drop some questions on formula and table slides. |
| F26 | Project notebook (outside this deck, for information) | 4 | Low | The Task 7 heading says "(1 automatic marks…)". The draft banner says the form is not set up. | Make "marks" singular. |

## Category 1 checks (Python, real scikit-learn 1.9.1, script `c4work/check.py`)

```
clean 88 | n 58 15 15 | missing ambient: train 1, valid 0
base  val MAE 14.8506 RMSE 16.9297 cv [15.46 14.12 9.86 13.47] mean 13.23
lin   0.7775 0.9211 cv [0.874(E2) 0.785(E1) 0.756(E4) 0.747(E3)] mean 0.7907  -> slide 0.78/0.92/0.79 (0.75 to 0.87) OK
tree  4.7886 6.2871 cv mean 4.149 (3.67 to 5.08) OK
ridge1 0.9327 1.1228 cv mean 0.891 (0.64 to 1.06) OK
knn3  1.5796 1.9560 cv mean 2.787 (2.60 to 3.24) OK
ablation: load only 4.2962, base 0.7775, +load_x_ambient 0.7992, +load_squared 0.7809  OK (4.30, 0.78, 0.80, 0.78; change 0.022)
coef A: 1.6619, 0.6949, 1.0542 | B: 6.3765, 0.6181, 0.8657, 0.00307  OK
row 1: 59.15 x 31.71 = 1875.6, target 76.847; B prediction exact 76.14 (slide 76.2 with rounded b3) -> F15
scaler mu 59.89, sd 22.73 (ddof 0, as StandardScaler); row 1 z = -0.033  OK
ridge (scaled, 2 features) alpha 0/0.1/1/10: weights 15.80 4.80 | 15.77 4.79 | 15.51 4.68 | 13.35 3.80;
  SSE 60.3/60.4/65.3/424.2; penalty 0/27.2/262.5/1928.3; loss 60.3/87.5/327.8/2352.4; val 0.78/0.79/0.93/2.63  OK
poly-6 load: none train 4.02 val 4.60 maxcoef 18454; alpha1 4.16/4.20/11; alpha100 5.82/6.87/3  OK
kNN k=1/3/20: 2.42 / 1.58 / 5.55  OK
kNN example: query record 5 z=(-0.100,-0.643) actual 67.034; neighbours 67 (0.129, 65.4), 22 (0.305, 70.6), 45 (0.413, 74.0); 4th 81 (0.423, 68.2); mean 70.02  OK
marginal effect of load in model B at ambient 31.71: 0.6181 + 0.00307*31.71 = 0.715 deg C per percent  -> F9
```
The lecturer guide's per-cohort table (CML3111 column) matches all of the above.

## Project coverage (everything Week 12 tests, against Classes 1 to 4)

| Project item | Taught? |
|---|---|
| Clean rows, split by group, baseline, linear, tree, MAE and RMSE, charts | Yes (Weeks 3 to 7, Class 1; repeated in lab 4 steps 1 and 2) |
| Logistic probabilities, confusion matrix, P/R/F1, cost, AUC, threshold by cost | Class 2. Class 4 never revisits it, and the memo needs it (F6) |
| Group CV | Class 3 and Class 4, but 4 folds with ddof=0 or a range; the project uses 5 folds with ddof=1 (F7) |
| Feature ablation with an interaction feature | Yes (slides 8 to 11, lab step 3) |
| Choose a model by a rule (MAE limit + latency limit, lowest MAE, tie-breaks) | **No**: a different rule is taught and latency is never taught (F1, F2) |
| Test set opened once after the choice | Concept yes (slide 26). Refit on E1 to E5 and the threshold test: no (F4) |
| No leakage, seed 17, pipeline | Yes (Class 3, slides 13 and 21, `with_imputer`) |
| Decision memo form (limits letters, next step, two short answers) | Partly: the seven-part prose memo is taught; two of the true limits and the "collect more data" next step are not (F5) |
| Python idioms the functions need: records as dicts, `set`, `continue`, list comprehension, `sorted(key=lambda)` | Not taught in Classes 1 to 4; check Weeks 1 to 7 |

## Cross-class notes
- **Assumes from earlier classes:** StandardScaler and z-score (Class 2, recalled on slide 13); GroupKFold, leakage, parsimony and the seed (Class 3); the baseline, linear and tree table and depth 4 (Class 1). Class 3's chosen depth 7, 5 percent tolerance and ddof=0 conflict with Class 4 and the project (F7, F8).
- **Hands to the project:** ablation, model table, test-once rule, memo. **Missing:** the client-limit and latency selection rule, refit before test, the threshold in the final recommendation, and the "one test group = one estimate" limit.
- **Before tomorrow (Class 2, 13 Nov):** nothing in Class 4 blocks Class 2. The Class 2 student PDF is also dated 3 Nov against a 10 Nov pptx; check it the same way, since the Class 4 PDF had a real weighting error.

## CML3112 and CML3113 (scope extension)

All three decks come from the same `c4.py`. Findings F1 to F26 above apply to **all cohorts** unless they cite a CML3111-only number. That includes F1 and F2 (the selection rule and latency), F4 to F8, F9 (interaction weights), F11 (PREDICT order), F13, F14 and F16 to F22. Only per-cohort differences follow.

**Numbers.** I re-ran `c4work/checkc.py <code>` (real scikit-learn 1.9.1) on each cohort's `Lab Notebooks/<code>/engineering_data.csv`. Every number on the slides, in the notes, in the check table and in the guide's per-cohort table matches. That covers ablation, coefficients, scaler, the ridge table, the degree-6 curves, the k-NN example and k sweep, the comparison table, CV folds and the chosen model.

| | CML3112 (kW) | CML3113 (kWh/t) |
|---|---|---|
| Ablation (load only / base / +int / +sq) | 3.12 / 0.74 / 0.75 / 0.75 | 0.98 / 0.67 / 0.67 / 0.67 (0.6732 / 0.6740 / 0.6749) |
| Ridge, 2 features, alpha 0 / 0.1 / 1 / 10 val MAE; loss at alpha 1 | 0.74 / 0.75 / 0.84 / 1.82; 50.4 + 110.6 = 161.1 | 0.67 / 0.68 / 0.70 / 0.90; 35.7 + 7.7 = 43.4 |
| Degree-6 curve: none / alpha 1 / alpha 100 | 3.32 / 3.05 / 4.68 | **0.98 / 0.99 / 1.48** |
| k-NN k = 1 / 3 / 20; example prediction (actual) | 1.69 / 1.16 / 3.72; 47.5 (45.6) | 0.94 / 0.63 / 1.37; 13.1 (12.6) |
| Lowest validation MAE (excluding baseline) | Linear 0.74 | **k-NN 0.63** (linear 0.67, ridge 0.70) |
| Linear CV mean (range) | 0.76 (0.74 to 0.77) | 0.70 (0.57 to 0.78); ridge 0.71, very close |

| ID | Cohort, where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| P1 | CML3113, slide 14 (point and notes) | 1 | **Medium** | The generated sentence reads "On your data a little penalty barely helps…", but alpha 1 is *worse* (0.98 to 0.99). The title "so a flexible curve stops fitting noise" is also not shown by this cohort's numbers. | Add a third branch in `c4.py` for `rp[1] >= rp[0]`: "Here a little penalty does not help, and a lot clearly hurts (0.98, 0.99, 1.48)." Soften the title for all cohorts: "...penalty on large weights, which can stop a flexible curve fitting noise". |
| P2 | CML3113, slides 24 and 27 vs project Task 7 | 2, 3 | **High (sharpest form of F1)** | The deck tells students: "k-NN wins on validation (0.63 against 0.67), but linear regression wins in cross-validation, so choose linear". The project rule picks the **lowest validation MAE** inside the client limits and ignores CV. The two lessons point opposite ways for this cohort. | Same fix as F1. Here the slide should name the project rule explicitly and explain why CV is used only as a report, not as a selection rule. Alternatively, align the project rule. |
| P3 | CML3113, slides 10, 11 and 35 | 5, 4 | Low | The ablation picture shows 0.67 / 0.67 / 0.67. The notes still say "slightly the wrong way" and ask "Which one is better, A or B?", which cannot be seen at two decimals. | For CML3113, print three decimals on slides 10, 11 and 35 (0.673 / 0.674 / 0.675), or say "the same to two decimals". |
| P4 | CML3113, slide 11 title | 4 | Low | "Removing ambient_c hurts a lot" describes a rise from 0.67 to 0.98 (+46 percent), which is much milder than CML3111 (+450 percent). | Use a cohort-neutral title: "Removing ambient_c makes the error clearly worse, and the new features do not help". |
| P5 | CML3112 (and 3113), slides 8, 12 and 25 | 4 | Low | The text is built for machines: "what you know about the machine", "E5 (new machine)", "a machine group it never saw", "Real plant data". For CML3112 the rows are buildings. | Use the cohort's `thing` (building, crusher, motor) in these strings. |
| P6 | All cohorts, slide 37 | 2 | **Medium** | The Block 2 assignment closes **at the start minute of each cohort's project sitting**: CML3112 Tue 1 Dec 11:00 (sitting 11:00 to 14:00), CML3113 Fri 4 Dec 08:00 (sitting 08:00 to 11:00), CML3111 Fri 4 Dec 11:00 (sitting 11:00 to 14:00). This replaces F12. | Close Block 2 at least 24 hours before each sitting, or confirm the overlap is intended. |
| P7 | All cohorts, Student Slides PDF (all dated 3 Nov) | 1 | **High** | The CML3112 and CML3113 Class 4 PDFs also say "worth **45** percent" three times and lack "It is practice and does not count toward your final mark". This is the same as F3. | Re-export all three Class 4 PDFs. |
| P8 | All cohorts: the project notebook's per-cohort constants | 2 | Medium | The projects differ only in wording, unit, `LIMIT` (80 deg C / 54 kW / 13.5 kWh/t) and **`MAX_MAE` (2.0 deg C / 2.0 kW / 1.0 kWh/t)**. Latency (1/3/30 ms, max 50) and costs (5/1) are the same everywhere. The limit and next-step lists are re-lettered per student with the same content. The deck never mentions a client MAE limit in any unit. For CML3113, 1.0 kWh/t is the limit that removes the tree (1.20 on the lab data), so the limit decides the choice there. Note that the project CSVs differ from the lab CSVs, so the lab numbers will not carry over. | Use each cohort's `MAX_MAE` in the new slide from F1, and run the rule on the lab table. Tell students that the project data are new, so their numbers will differ from the lab. |
| P9 | CML3112 and CML3113, slide 9 | 1 | Low | The F15 rounding pattern repeats harmlessly (B row 51.8 kW and 13.3 kWh/t match the exact values to one decimal). For CML3113, b₃ shows as 0.0005 (exact 0.000506), so a beginner reading four decimals loses precision. | Show b₃ to three significant figures. |

Dates and wording otherwise check out. CML3112's cover is Tue 24 Nov 11:00 to 14:00 with the project proposed for Tue 1 Dec 11:00 to 14:00. CML3113's slot is Fri 27 Nov 08:00 with the project on Fri 4 Dec 08:00 to 11:00. The payer wording is correct per cohort ("client who pays for the cooling plant", "mine manager who pays for the crusher power"), and units are consistent throughout. The guide's per-cohort table matches.
