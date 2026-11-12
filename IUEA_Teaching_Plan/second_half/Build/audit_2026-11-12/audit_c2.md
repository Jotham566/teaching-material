# Audit: CML3111 Class 2 (Week 9, "Classification: yes or no"), taught Friday 13 November 2026

**Verdict.**
1. Every number on the slides and in the notebook is correct. I recomputed each one with real scikit-learn 1.9.1 from `Lab Notebooks/CML3111/engineering_data.csv`, and the full notebook runs cleanly with real scikit-learn and prints exactly the slide numbers.
2. A few statements around those numbers are false for CML3111: "no threshold adds a false positive", the standardisation CHANGE task with its guide answer, the "16 points" ROC, and the ConvergenceWarning. The lecturer guide's narrative uses CML3112 numbers. Students will run into the first two in the lab tomorrow.
3. The structure, recall, build-up and pictures are good. The class is dense (29 concept slides in 75 minutes). The project's "cost" task is not taught here or anywhere else.

Paths: deck `IUEA_Teaching_Plan/second_half/Slides/CML3111/CML3111_Week09_Class2_Classification_yes_or_no.pptx`, sources `Build/content/c2.py` and `Build/content/lab2.py`, guide `Lecturer Guides/Class2_Week9_Lecturer_Guide.pdf`. Check scripts are in `/private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/d327a2a5-164d-49e1-94aa-14fa1a0cd931/scratchpad/cml3111/c2chk/` (`check.py`, `chk2.py`, `nbcode.py`).

## BEFORE TOMORROW (13 November)
| # | Item | Quick action if there is no time to rebuild |
|---|---|---|
| B1 (F1) | The title of slide 24 and the notes on slides 25 and 26 say no threshold adds a false positive on these 15 rows. The lab CHANGE (Step 6, thresholds 0.1 and 0.2) prints FP 2. | Rebuild with "none of the thresholds 0.3, 0.5, 0.7". Otherwise say aloud: "at 0.2 you will see 2 false positives, and that is the trade-off". |
| B2 (F2) | In the notebook Step 3 CHANGE, the "weights times standard deviation" products (17.38, 5.64) are nowhere near 2.81 and 0.93. The guide's answer ("weights become small", "probabilities stay almost the same") is false: without the scaler the model gets TP 3, FN 0. | Delete the product line, or tell the room the answer (F2 fix). |
| B3 (F3) | The lecturer guide's "Walking the lab", slide map and Step 2, 3, 4 and 6 numbers are CML3112 values: 19 of 58, weights 2.79/0.73/-1.71, tree FP 1, FP 0 to 1. | For CML3111 use only the per-cohort table on guide pages 4 and 5 (17 of 58, 2.81/0.93/-1.99, tree FP 0, FP 0/0/0). |
| B4 (F9) | Assessment details contradict each other. Slide 37 says the Block 1 assignment closes Friday 20 November 11:00. The guide says "do not give a date before it is decided". The guide says to bring a quiz *paper* that "learners sit in class", while the deck says the quiz is open for 24 hours. | Decide on the deadline and the quiz format, then say them consistently. |
| B5 (F6) | Slide 28 says "16 points". The student's `roc_curve` (default `drop_intermediate=True`) plots only 4 points. | Say it aloud, or add `drop_intermediate=False` in Step 7. |
| B6 (F17) | Rendered without the Lato font, slide 19's table header wraps ("Symbo l") and the footnote overlaps the last row. The student PDF (Lato) is fine. | Present from the PDF, or check that the classroom PC has Lato. |

## Findings
Categories: 1 correctness, 2 completeness, 3 build-up/flow, 4 understanding, 5 illustrations, 6 lab, 7 AI-like writing.

| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| F1 | Slide 24 title and text; slide 25 notes; slide 26 notes; `c2.py` l.98, l.369, l.394 | 1, 6 | **High** | Slide 24 says "on these 15 rows no threshold adds a false positive". Slide 26 notes say this is "an idea that our 15 rows cannot show". The two highest-scoring actual negatives have p = 0.296 and 0.207, so thresholds 0.2 and 0.1 give FP 2. The lab CHANGE in Step 6 makes students print this. | Change the title to "none of the thresholds 0.3, 0.5 or 0.7 adds a false positive". Better: show the real 0.2 row (TP 3, FN 0, FP 2, precision 0.60, recall 1.00) as the trade-off from our own data, and keep the illustrative table as a second example. Compute `trade` over a wider threshold grid. |
| F2 | Notebook Step 3 CHANGE (cell 15/16); guide "Walking the lab" Step 3; guide misconception "Standardisation changes the answer" (`c2.py` l.533, l.545) | 1, 6 | **High** | The prompt asks "Are the products close to the weights printed above?" They are 17.38 and 5.64 against 2.81 and 0.93. The guide says "the weights become small", but the ambient weight *grows* from 0.93 to 1.24. It also says "the probabilities of this model stay almost the same", but the largest change is 0.41 and the unscaled model's confusion matrix changes to TP 3, FN 0. The cause is never taught: `LogisticRegression` applies an L2 penalty by default (C=1), so the fitted model depends on the feature scale. The training data are also almost separable (training accuracy 0.97). | Drop the product line. Ask: "Which weight shrank, which grew, and did the confusion matrix change?" Add one sentence: "scikit-learn's LogisticRegression adds a penalty on large weights (regularisation, Class 4), so the scale of the features changes the fitted model. That is one more reason to standardise first." Correct the guide rows to match. |
| F3 | Lecturer guide pp. 1 to 4 | 1 | **High** (for the lecturer) | One guide covers three cohorts, but the narrative is built from CML3112: "Training 19 of 58", "Weights 2.79 and 0.73, intercept -1.71", "Depth 3. TP 2, FN 1, FP 1", "FP goes from 0 to 1", and slide-map titles with "p = 0.45", "different counts" and "trade-off: more positives found, more false positives". All of these are wrong for CML3111. | Generate the "Walking the lab" text per cohort, or remove the numbers from it and point to the table. |
| F4 | Project brief task "cost"; slides 22, 25, guide | 2 | **High** (project) | The project asks for a confusion-matrix **cost** and a threshold chosen by a rule. Class 2 only says "a false negative costs more, so we watch recall". No cost formula, no worked numbers, no rule. Classes 3 and 4 never teach it either (grep "cost" finds only unrelated uses). | Add one formula slide: total cost = c_FN x FN + c_FP x FP, with illustrative costs (for example FN = 10 units, FP = 1 unit) applied to the 0.2, 0.3, 0.5 and 0.7 rows of the real threshold table, and the rule "choose the threshold with the lowest validation cost". Add the same calculation as a lab cell. If there is no time before tomorrow, recall it in Class 3 or 4. |
| F5 | Slides 12 and 14 notation; Class 4 slide on ridge | 3, 4 | Medium | "z-score" is the name of the standardised value, which is written x'. Then z is reused as the logistic *score*, so on slide 14 "z = -0.13" sits next to "z-scores 0.08 and 1.75". Class 4 writes the scaled features as "z". The same letter has three meanings across the classes. | Call the logistic score s, or keep z and add "(this z is the score, not a z-score)". Align Class 4 with x'. |
| F6 | Slide 28 text and notes; notebook Step 7 | 1, 6 | Medium | "15 validation rows give only 16 points." That is true with `drop_intermediate=False`. The notebook calls `roc_curve(y_valid, y_proba)`, which returns 4 points: (0,0), (0,0.33), (0,1), (1,1). The student's plot will not match the slide. | Use `roc_curve(..., drop_intermediate=False)` in Step 7, or say on the slide "scikit-learn keeps only the corner points, so your plot shows 4". |
| F7 | Slide 16 tree figure; slide 17 | 4, 5 | Medium | The right branch says ambient_c <= 18.5 means **yes** and 18.5 to 19.1 means **no**. Each of those leaves holds a single training row (checked with `apply`), so a colder room "predicts overheating". A beginner will read this as physics. | Add one line: "The bottom-right split rests on one training row each, which is a first sign of overfitting (Class 3)." This turns it into a good bridge. |
| F8 | Slide 36 and notes; guide Step 3 | 1 | Medium | The notes say "A convergence warning ... appears when features are not standardised", and the guide says "A ConvergenceWarning may appear". With real scikit-learn the unscaled model converges in 30 iterations, even at the default max_iter=100, and gives no warning. | Change to "can appear when features are on very different scales". |
| F9 | Slide 37 and notes; slide 2 notes; guide "Before the class" and "After the class" | 3 | Medium | Slide 37 states the deadline "Friday 20 November, 11:00", but the guide says "Do not give a date before it is decided". The guide's quiz is a paper sat in class, while the deck's quiz is "open for 24 hours". The notes say "only A1 to A5 and Q1 to Q5" count, while the assignment is called "A7/A8" (no A6). The notebook says "It is not the graded upload", while slide 37 says part B "comes from today's lab". | Make one decision and state it the same way on slide 37, in the notes, the guide and notebook Step 9. |
| F10 | Clock (slide 3), slides 4 to 32 | 3 | Medium | 29 concept slides in 75 minutes: standardisation, sigmoid, logistic formula, worked example, tree classifier, four metrics, cost, thresholds, specificity, ROC and AUC. That is about 2.5 minutes per slide for students who are new to programming. | Mark slide 26 (the illustrative table) and slide 27 (specificity) as optional. Cut slide 21 or merge it with slide 19 and slide 20. |
| F11 | Slide 15 text; slide 14 table | 4 | Medium | "One more of ambient_c adds 0.93" reads as one more deg C. It means one *standard deviation* (4.55 deg C). The raw-unit effect is never given. | "One standard deviation more of ambient_c (4.55 deg C) adds 0.93 to z, which is about 0.20 per deg C. One percentage point of load adds about 0.12." Check: 2.808/22.73 = 0.124 and 0.9327/4.55 = 0.205. |
| F12 | Slide 24 figure | 5 | Medium | The actual negative at p = 0.296 is drawn on the 0.3 dashed line, and the figure itself cannot tell you that it is predicted negative. | Label it "0.296, just below 0.3", or nudge the marker. |
| F13 | Slide 14 formula line 2 (and the fractions on slides 19, 20, 27) | 5 | Medium | p = 1/(1 + e^-z) is rendered at about 8 pt, and the e^-z is barely legible in the PDF. ŷ is used but missing from the symbol table. | Draw the sigmoid fraction larger (its own line height) and add a ŷ row ("predicted class"). |
| F14 | Notebook Steps 4 and 7 | 6 | Low | Step 4 (tree) has no PREDICT or READ. Step 7 has no PREDICT. This breaks the PREDICT, RUN, READ rhythm. | Add PREDICT for Step 4 ("will the tree find the same positives?") and for Step 7 ("will the AUC be above 0.9?"). |
| F15 | Slide 13 figure | 5 | Low | The gold dot "validation row 3, p = 0.47" is drawn at score 0 and p = 0.5, exactly on the threshold, although its score is -0.13. | Plot it at (-0.13, 0.47), just below the line. |
| F16 | Slide 34 | 3, 5 | Low | The title says "five stages", but the boxes show Steps 1 to 7 plus 8 and 9, and Step 5 is highlighted gold for no stated reason. | Title: "The lab has nine steps in five stages". Remove the highlight or explain it. |
| F17 | Slide 19 (font fallback) | 5 | Low | Without Lato the header wraps to "Symbo l" and the footnote overlaps the n row. | Check the classroom PC, or present from the PDF. |
| F18 | Slide 35 header | 4 | Low | The header reads "What to check (validation set)", but the rows include training counts and the learned weights. | Header: "What to check". |
| F19 | Slide 32 recipe | 3 | Low | The recipe uses `train_features` and `model`. The notebook uses `training_data[feature_columns]` and `logistic_model`. | Use the notebook names. |
| F20 | Slides 11 and 12 | 4 | Low | StandardScaler divides by n (population SD 22.73 and 4.55). Students used pandas `.std()` in Weeks 1 to 7, which gives 22.93 and 4.59. A hand check with pandas will not match. | Add "StandardScaler divides by n: use `X_train.std(axis=0)` (NumPy), not pandas `.std()`". |
| F21 | Slide 29 | 1 | Low | AUC is given as "the chance that an actual positive row scores higher than an actual negative row" without saying how ties count. | Add "(ties count half)". |
| F22 | Slide 30 | 4 | Low | "If one prediction changed, recall would move by 0.33." That is only true if the changed prediction is on a positive row. | "If one positive row changed..." |
| F23 | Slide 27 | 3 | Low | Specificity is introduced and then never used again. It is also missing from the Words table. | Drop it or mark it as optional. |
| F24 | Notes on slides 18, 23, 25; slide 29 | 7 | Low | Template artefacts: "There are 1 false negatives" and "false positives (FP) stays at 0". Odd phrase: "a warm hint". Every recall answer opens with "A good answer is this", and most notes end on a stock question. | Fix plural agreement in the templates and vary the openers. |
| F25 | Student PDF (3 Nov) against pptx (10 Nov) | 3 | Low | The only text difference is on slide 37: the pptx adds "It is practice: it does not count toward your final mark." Everything else is the same apart from text-extraction splits. | Re-export the student PDF after the fixes above. |

## Category 1 checks (Python, real scikit-learn 1.9.1)
```python
# check.py / chk2.py (scratchpad cml3111/c2chk), run with .iuea-grader-env python -I
d = raw.drop_duplicates('record_id'); d = d[d.target.notna() & d.load_pct.between(0,100)]   # 88 rows
tr = E1..E4 (58), va = E5 (15); y = (target >= 80)
# pos tr 17/58, va 3/15, majority acc 0.80                       -> slides 9, 10, 35 OK
# StandardScaler mu [59.89 26.33] sd [22.73 4.55]; row1 [-0.03 1.18] -> slides 11, 12 OK
# LogisticRegression b0 -1.9945, w [2.808 0.9327]                -> slide 14 OK
# row 3 = record_id 17, z' [0.082 1.747], score -0.135, p 0.4664 -> slide 15 OK
# t=0.3: TN12 FP0 FN0 TP3 | t=0.5: 12 0 1 2 (acc .93 P 1 R .67 F1 .80) | t=0.7: 12 0 3 0  -> slides 18-25 OK
# AUC 1.0 (neg max 0.296 < pos min 0.466, 36/36 pairs)          -> slides 28, 29 OK
# Tree depth 3 rs=17: [12 0 1 2], acc 0.93; leaves 8 and 9 hold 1 training row each   -> F7
# neg probs sorted ... 0.0534 0.2072 0.2961  -> thresholds 0.1/0.2 give FP 2         -> F1
# roc_curve default: 4 points; drop_intermediate=False: 16                          -> F6
# unscaled LogisticRegression(max_iter=100 or 1000): 30 iters, no warning; w [0.765 1.239]
#   w*sd = [17.38 5.64]; probs max diff 0.413; cm at 0.5 = [12 0 0 3]             -> F2, F8
# pandas std (ddof=1) [22.93 4.59] vs StandardScaler [22.73 4.55]                    -> F20
```
The notebook's code cells, extracted and run end to end with real scikit-learn (`nbcode.py`), print exactly the numbers on slide 35 and the guide's CML3111 column. They match the NumPy reference bundle.

## Cross-class notes
- **Assumed from earlier classes but not taught there:** standard deviation (0 mentions in Class 1; slide 11 defines it only in brackets), `make_pipeline` (named once in Class 1), probability, and `random_state` (first used here, explained only in the notebook). Median imputation, the split by equipment group, leaf nodes, max_depth and hyperparameters were taught in Class 1 and are recalled correctly.
- **Handed to later classes and the project:** Class 3's recall slide reuses "recall 0.67 to 1.00, FP stayed at 0" (true for 0.3, so it stays consistent if F1 is fixed by naming the thresholds). Overfitting is promised on slide 17, and the one-row leaves (F7) are a ready example for Class 3. Regularisation (Class 4 ridge) should look back to F2: LogisticRegression is already penalised. Notation needs aligning with Class 4's "scaled features z" (F5). **The project needs a cost-of-errors calculation and a threshold-choice rule, and no class teaches them (F4).** The project's logistic probabilities, confusion matrix, precision, recall, F1 and AUC are all taught here.

---

# CML3112 and CML3113 (same `c2.py` / `lab2.py`; scope extension)

**Method.** I ran `c2chk/multi.py` (real scikit-learn 1.9.1) on each cohort's own CSV, `Lab Notebooks/<code>/engineering_data.csv`, with limits 54 kW and 13.5 kWh/t. I also ran every code cell of each cohort's `Class2_Lab_Classification.ipynb` end to end (`c2chk/<code>/nb.py`). Then I diffed each deck's text against CML3111 and looked at the number-bearing figures: slides 9, 13, 15, 16, 24 and 28.

**Result.** Every number on the slides, in the notes, in the check table (slide 35), in the notebook outputs and in the guide's per-cohort table is correct for both cohorts. The data are identical across cohorts except the target, so features, splits, StandardScaler numbers, record ids and the 3 validation positives (record_id 17, 59, 77) are shared.

| Check | CML3112 (limit 54 kW) | CML3113 (limit 13.5 kWh/t) | On slides |
|---|---|---|---|
| Positive labels, train / validation | 19 of 58 / 3 of 15 | 24 of 58 / 3 of 15 | OK |
| Logistic weights load, ambient, intercept | 2.79, 0.73, -1.71 | 2.64, 0.49, -0.95 | OK |
| Row 3 (record_id 17): score, p | -0.20, 0.45, so FN | +0.12, 0.53, so TP | OK |
| Confusion at 0.5 (TP, FN, FP, TN) | 2, 1, 0, 12 | 3, 0, 1, 11 | OK |
| Accuracy, precision, recall, F1 at 0.5 | 0.93, 1.00, 0.67, 0.80 | 0.93, 0.75, 1.00, 0.86 | OK |
| Thresholds 0.3 / 0.5 / 0.7: TP, FN, FP | 3,0,1 / 2,1,0 / 0,3,0 | 3,0,2 / 3,0,1 / 2,1,0 | OK |
| ROC points (FPR, TPR) at 0.3, 0.5, 0.7 | (0.08,1) (0,0.67) (0,0) | (0.17,1) (0.08,1) (0,0.67) | OK |
| AUC | 1.00 (36 of 36 pairs) | 0.97 (35 of 36: negative 0.600 > positive 0.530) | OK |
| Tree depth 3 (TP, FN, FP, TN) | 2, 1, 1, 11, accuracy 0.87, F1 0.67 | 3, 0, 1, 11, accuracy 0.93, F1 0.86 (same rows as logistic) | OK |
| Unscaled LogisticRegression, weights x SD | 12.44, 3.83; confusion matrix changes to TP 3, FP 0 | 7.42, 2.19; confusion matrix unchanged | F2 applies |
| roc_curve default points | 4 | 6 | F6 applies (slide says 16) |

**All-cohort findings from the CML3111 audit that apply unchanged to CML3112 and CML3113 (all cohorts):** F2 (the CHANGE "products close?" prompt: 12.44/3.83 and 7.42/2.19 are not close to the weights), F4 (cost of errors never taught), F5 (z clash), F6 (16 against 4 or 6 ROC points), F8 (no ConvergenceWarning: 32 and 28 iterations), F9 (assessment contradictions), F10 to F25. F3 (guide narrative) is *correct* for CML3112, because the guide was generated from it, and *wrong* for CML3113. F1 (the "no threshold adds a FP" title) is CML3111 only: the other two decks get the trade-off title, which has its own problem in CML3113 (C2 below). F7 (one-row leaves) applies in a different form (C1, C6).

## CML3113: BEFORE TOMORROW (Fri 13 Nov, 08:00, taught before CML3111)
| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| C1 | Slide 16 tree figure | 5, 4 | **High** | Splits are drawn to 1 decimal. The right branch reads "ambient_c <= 22.0?", and under its *yes* side it asks "ambient_c <= 22.0?" again, with leaves yes and no. The real thresholds are 22.05 and 21.96. As drawn the second question is impossible to fail, which is nonsense on the slide. The "no" leaf (21.96 to 22.05 deg C) holds 1 training row. | Draw the thresholds to 2 decimals (`tree_node(..., nd)` format `.1f` in `common.tree_node`, or a local formatter). Add the sentence from F7: "this split rests on one training row, a sign of overfitting". If there is no rebuild, say it aloud. |
| C2 | Slide 24 title and bold text | 1, 4 | **High** | "A lower decision threshold raises recall but gives more false positives... more positives found". From 0.5 to 0.3 (the move the slide shows) recall *stays* at 1.00 and only FP rises (1 to 2). Slide 25's footnote correctly says "recall stays at 1.00". The title is true only from 0.7 to 0.5 (recall 0.67 to 1.00, FP 0 to 1). | Title: "Lowering the threshold never lowers recall and can add false positives". Body: "From 0.7 to 0.5 recall rises from 0.67 to 1.00 and FP from 0 to 1. From 0.5 to 0.3 recall is already 1.00, so only FP rises." |
| C3 | Guide pp. 1 to 4 (as F3) | 1 | **High** (lecturer) | The narrative gives CML3112 values: "Training 19 of 58", "Weights 2.79 and 0.73, intercept -1.71", tree "TP 2, FN 1, FP 1", "recall 0.67 to 1.00, FP 0 to 1", "p = 0.45". The correct CML3113 values are 24 of 58; 2.64, 0.49, -0.95; tree TP 3, FN 0, FP 1; recall stays 1.00 and FP 1 to 2; p = 0.53, predicted yes (TP). | Use only the per-cohort table on guide pages 4 and 5 (CML3113 column, all correct). |
| C4 | Slide 28 figure | 5 | Medium | Two red dots sit on the top edge at FPR 0.08 and 0.17. The labels "threshold 0.3" and "threshold 0.5" are placed so that 0.3 reads as the left dot. It is the opposite: 0.5 is at (0.08, 1) and 0.3 is at (0.17, 1). | Put each label beside its own dot, or add the coordinates. Say it aloud tomorrow. |
| C5 | Slide 37; notes | 3 | Medium | "The Block 1 assignment closes on Friday 20 November, 08:00", which is the start of CML3113's Class 3. The guide says not to give a date (F9). | Confirm the date before saying it. |
| C6 | Notebook Step 3 CHANGE (F2) | 6 | Medium | For CML3113 the unscaled model's confusion matrix is unchanged (11, 1, 0, 3), but the products 7.42 and 2.19 are far from 2.64 and 0.49, and the probabilities move by up to 0.34. | As F2: drop the product line, or explain the default penalty. |
| C7 | Slide 10 notes | 1 | Low | "The data are imbalanced, which means one class is much rarer." The CML3113 training set is 24 of 58 positive (41 percent), which is mild. Only the validation set (3 of 15) is clearly imbalanced. | "The validation set is imbalanced: 3 of 15." |
| C8 | Slide 22 | 4 | Low | "Demand rises with no warning. It can strain the supply." The target is specific energy in kWh/t (energy per tonne), not power demand, so "strain the supply" mixes energy per tonne with power. The FP line, "The control room plans for demand that never comes", is fine. | "Energy per tonne runs high with no warning, so energy is wasted on every tonne crushed." Hedge as an illustration. |

## CML3113: after tomorrow
| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| C9 | **Class 3** recall answer (CML3113 Class 3 deck, Q3, slide 4 notes and slide 5 table) | 1, 7 | **High** (before 20 Nov) | "Recall rose from 1.00 to 1.00. False positives went from 1 to 2." The template does not handle the "no change" case. | "Recall stayed at 1.00; false positives went from 1 to 2." Fix in `c3.py`. |

## CML3112 (Class 2 already taught on 10 Nov; fix before the re-export of the student PDFs)
| ID | Where | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| D1 | Notebook Step 3 CHANGE (F2) | 1, 6 | Medium | The products are 12.44 and 3.83 against weights 2.79 and 0.73. Without the scaler the confusion matrix changes to TP 3, FN 0, FP 0 at 0.5. The guide's misconception answer, "probabilities stay almost the same", is false here too (largest change 0.35). | As F2. Mention it in the Class 3 recall if students asked. |
| D2 | Slide 16 tree | 4 | Low | The leaf "ambient_c > 28.7 means yes" under load 68.3 to 72.0 holds 1 training row. The leaf under load_pct <= 85.3 (ambient <= 22.0) holds 5 rows, of which 1 is positive. The figure is honest, but it does not show how few rows a leaf rests on. | Optional: show the training row count in each leaf. |
| D3 | Slide 37 | 3 | Low | The deadline "Tuesday 17 November, 11:00" is the start of CML3112's Class 3. The guide says not to give a date (F9). | Confirm in writing. |
| D4 | Student PDF (3 Nov) | 3 | Low | The student PDF lacks the slide 37 "practice" line (known). Numbers are otherwise the same. | Re-export after the fixes. |

**Wording check (cohort words).** CML3112: the label "high cooling load"; FN "the cooling plant is not ready, rooms can get too warm"; FP "extra cooling starts early for nothing, it wastes some energy"; "plant operator". Units are kW throughout, and the axis is 26 to 65 kW (data 25.8 to 65.4). All fine. CML3113: "high energy demand", "control room", kWh/t throughout, axis 7 to 17 (data 6.9 to 17.3). Fine apart from C8. In all three decks the slide 15 text says "ambient_c 34.28 deg C", which is correct (ambient is in deg C for every cohort). Slide 13's dot is drawn at score 0 in all cohorts (F15). For CML3113 the dot is drawn at p = 0.5, although p = 0.53 is above the threshold, so the problem is minor there.
