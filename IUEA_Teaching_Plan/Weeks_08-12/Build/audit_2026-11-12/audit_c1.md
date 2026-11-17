# Audit: CML3111 Class 1 (Week 8, "Your first model")

**Verdict.** Every number on the 40 slides, in the notes, the notebook CHECK and the lecturer guide recomputes exactly from the CSV (no numeric error found).
The main weaknesses are order and framing: the train/validation/test split (slide 28) and imputation (29) come after validation scores and "58 training rows" have already been used (13 to 27), and nothing on the slides says that LinearRegression does not use gradient descent.
The guide still calls the Block 1 assignment "graded", which contradicts slide 39. Slide 20 has headers broken mid-word, and the 3 November student PDF lacks the "practice" sentence on slide 39.

Sources checked: `Build/content/c1.py`, `lab1.py`, deck text and all 40 slide renders, `Class1_Lab_First_Model.ipynb` (44 cells, outputs cleared), `Class1_Week8_Lecturer_Guide.pdf` (5 pages), the student PDF dated 3 November compared slide by slide with the 10 November pptx render.

## Findings

**Scope of F1 to F29: all cohorts.** c1.py builds the CML3112 and CML3113 decks from the same source, and I checked the text and renders of all three. Every finding in this table applies to all three cohorts. Only the example numbers change, for instance 71.0 deg C, 48.1 kW and 12.5 kWh/t in F15. Cohort-specific issues are in the section "CML3112 and CML3113" below.

| ID | Slide / cell / page | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|
| F1 | Slides 22 to 26 (and 25 notes "In the lab scikit-learn trains the model for us") | 1 | Medium | The deck teaches gradient descent as "how the computer trains the model", then moves straight on to LinearRegression. A student revising from the PDF will believe LinearRegression runs gradient descent. It uses a direct least-squares solution. Only the lecturer guide (p.3) says so, and with a hedge. | Add one line on slide 25 or 26: "scikit-learn's LinearRegression finds b0, b1 and b2 directly with a formula (least squares). Gradient descent reaches the same answer step by step and is used where no formula exists (Class 2 logistic regression, neural networks)." Drop the "My understanding is" hedge in the guide, because the fact is certain. |
| F2 | Guide p.1 ("The graded assignment notebook (W08_student.ipynb)"), p.5 ("The graded part A follows...") vs slide 39 | 1 | Medium | The guide calls the assignment graded. Slide 39 and the Class 2 deck say it is practice and does not count. | Change "graded" to "practice (collected, feedback, not counted)" in the facilitator `prep` and `after` lists in c1.py. |
| F3 | Student Slides PDF (3 Nov), slide 39 | 1/6 | Medium | The PDF students revise from lacks "It is practice: it does not count toward your final mark...". Text diff against the 10 Nov pptx: this is the only content difference in Class 1. | Re-export the student PDF from the current pptx before the Block 1 quiz opens tomorrow (it covers Class 1). |
| F4 | Slides 12 to 27 vs 28 | 3 | Medium | Validation scores (14, 20), "58 rows (E1 to E4)" (13), "validation set plays no part" (13) and "15 validation rows" (19) all appear before slide 28 explains the split by equipment group. Slide 6 defines the two words, but the 58/15/15 split and its picture come 15 slides later. | Move slide 28 (hold-out split) to just after slide 11 (cleaning). The order then follows the lab: clean, split, baseline. |
| F5 | Slide 29 vs 26 and 34 | 3 | Low | Imputation is explained after the multiple regression parameters (26). The fitted values depend on the imputed median. | Place slide 29 right after the moved split slide, or just before slide 26. |
| F6 | Slide 1 and slide 40 question: "predict motor winding temperature from load and temperature" | 4 | Medium | For this cohort the target is itself a temperature, so "from ... temperature" reads as circular. | "...from load and air (ambient) temperature". This is cohort text in `common`/c1, so check that the other cohorts still read well. |
| F7 | Slide 10 figure | 5 | Medium | Spreadsheet row labels 1 to 4 sit beside record_ids 1, 2, 3, 5. Directly beside it the text says "Record 4 is left out", and the row labelled "4" is record 5. A beginner reads row 4 as record 4. | Remove the row-number column, or show the true file rows (1, 2, 3, 5) as slide 11 does. |
| F8 | Slide 20 table header | 5 | Medium | Headers break mid-word: "record_i / d", "Actua / l". This shows in the PDF. | Narrow the "Linear regression error" column or shorten headers ("Baseline error" to "Error (baseline)"), or use 14 pt headers. |
| F9 | Slide 23 | 3 | Medium | The slide gives dL/dw but never writes L itself. It also writes (w x_i - y_i), which is predicted minus actual: the opposite sign to e_i = y_i - y-hat_i from slides 16 to 17. Students meet a derivative of an unseen function, with the sign flipped. | Add the line L = (1/n) sum (w x_i - y_i)^2 = (1/n) sum e_i^2 (the MSE of slide 19). Add one sentence: "(w x_i - y_i) is minus the residual, so squaring gives the same loss." |
| F10 | Slides 15, 18, 25 ("0.666 x 60", "e x e", "(2/3) x (1 x (0 - 2) ...") | 4 | Medium | The letter x is used for multiplication on the same slides where x is the feature symbol. Slide 25 reads "dL/dw = (2/3) x (1 x (0 - 2) + 2 x ...)", which is ambiguous. | Use the multiplication sign × (or a centred dot) in all arithmetic text. |
| F11 | Slide 33 figure | 5 | Medium | The flow is drawn Imputer → Model → Pipeline, so the pipeline looks like a third step after the model. In fact it is the container for the other two. | Draw the pipeline as a gold frame around Imputer → Model, with "fit" and "predict" arrows entering it. |
| F12 | Slide 26 | 4 | Low | "b1 = 0.695 per percent, b2 = 1.054 per deg C" has no output unit. b0 = 1.66 deg C is "the prediction if both features were 0", which is far outside the data (training load 20.5 to 93.2 %), and the slide does not warn about this. | "0.695 deg C per percent of load; 1.054 deg C per deg C of air". Add: "b0 is where the plane crosses zero; no motor runs at 0 % load in 0 deg C air, so read it as an anchor, not a real reading." |
| F13 | Slide 31 "The last tree had max_depth 2" | 4 | Low | "The last tree" has no clear referent in a PDF read alone. | "The tree on the previous slide (slide 30) had max_depth 2." |
| F14 | Slide 29 caption | 4 | Low | Fragment: "Medians: load_pct 62.8, ambient_c 26.1." The slide does not say which row is missing (record_id 14, E2). | "The training medians are 62.8 percent for load_pct and 26.1 deg C for ambient_c. Record 14 (group E2) has no ambient_c, so it gets 26.1." |
| F15 | Slides 12/13 (71.0) vs 17/20 (71.03) | 4 | Low | The same baseline is shown at two precisions. | Use 71.03 deg C throughout, or say "about 71.0". |
| F16 | Slide 25 loss column | 4 | Low | Mixed precision: 18.667, 5.31, 1.51, 0.43, 0.122, 0.035. | Use three decimals in every row (5.310, 1.510, 0.430). |
| F17 | Slide 37 check table | 6 | Low | It omits outputs the notebook prints and the guide lists: "after removing repeats: 90", baseline prediction 71.03, RMSE 0.92 / 6.29 / 16.93. | Add rows for 90 and RMSE, or note "RMSE values are in the guide". |
| F18 | Guide p.4, Step 2: "If someone has 89 or 87 they ran a cell twice" | 1 | Low | The Step 2 cell rebuilds from `raw_data`, so re-running it is idempotent and cannot give 87 or 89. A different count comes from leaving the CHANGE edit (between(0, 90)) in place. | "If someone has a different count, they left between(0, 90) in place." |
| F19 | Notebook Steps 3 and 7 | 6 | Low | Steps 3 and 7 have no PREDICT prompt. The other steps have one. | Step 3: "How many rows will each set get?" Step 7: "Which model will have the smallest RMSE?" |
| F20 | Notebook Step 5 plot (actual vs predicted) | 2 | Low | The plot is never shown or explained on a slide. The project needs charts. | Add one sentence or a small figure to slide 32 or 34: "points on the dashed diagonal are perfect predictions". |
| F21 | Slide 34 code `model = make_pipeline(...)` vs notebook `linear_model` | 6 | Low | The variable name differs from the notebook and from the TERMS convention. DummyRegressor and DecisionTreeRegressor are never named on any slide. | Use `linear_model`, and add one line "Baseline: DummyRegressor(strategy='mean'); tree: DecisionTreeRegressor(max_depth=4, random_state=17)". |
| F22 | Slide 31 / notebook Step 6 `random_state=17` | 2 | Low | The seed is used in the lab, but no slide in Class 1 says what it is. Class 3 teaches it. | One clause on slide 31: "random_state=17 fixes the tree's random tie-breaking so everyone gets the same tree (Class 3 explains)". |
| F23 | Slides 7, 21, 37, 39 icons | 5 | Low | The icons are decorative and mark nothing: a chart icon for "warn", a plain yellow circle (slide 7), check/flag for MAE/RMSE (21), a red error icon beside "Baseline model MAE" (37), the same clock icon twice (39). | Use meaningful icons (thermometer/alarm, wrench, fan) or drop them. On 37, use no icons. |
| F24 | Slide 39, second bullet | 5 | Low | The three-line text runs over the row separator rule. | Shorten the bullet (split the practice sentence into its own bullet) or raise the row height. |
| F25 | Slide 12 figure | 5 | Low | The baseline label "71.0 deg C" is partly covered by a data dot. The axes show only end ticks (37/97, 21/93). | Move the label to the left above the line; add mid ticks (50, 70, 90 deg C; 40, 60, 80 %). |
| F26 | Slides 16/17 titles; 12/13; 14/15 | 7 | Low | Pairs repeat nearly identical titles ("The prediction error (residual) is the actual value minus the predicted value" / "The prediction error of one row is the actual value minus the predicted value"). | Give the formula slides titles that say what is new: "e_i = y_i - y-hat_i: record 5 is off by -4.00 deg C". |
| F27 | Notes slide 4 ("Think about your own task as you answer" for a data.shape question; "If an answer was missing, do not worry"), slide 6 notes read the table verbatim | 7 | Low | Stock lecture-script openers and closers from the template. | Write question-specific prompts. Make slide 6 notes add an example instead of repeating the table. |
| F29 | Slides 17 and 20, all cohorts | 1/4 | Medium | The errors are computed from unrounded values, but the slide shows rounded actual and predicted values. A student who checks by hand (the notes say "Work out the same error yourself with a calculator") gets a different last digit. CML3111: 80.29 - 71.03 = 9.26, shown +9.25; 47.95 - 71.03 = -23.08, shown -23.09. CML3112: -11.51/+6.42/-14.62, shown -11.50/+6.43/-14.61. CML3113: 12.55 - 12.53 = 0.02, shown 0.03 (slide 17 formula line too); 0.28, shown +0.29; 0.88, shown +0.87. | Compute the error columns from the displayed two-decimal values, or show three decimals, or add "errors use unrounded values" under the table. |
| F28 | Slide 40 notes "fault or no fault" vs Class 2 "overheating" | 3 | Low | The hand-off example differs from what Class 2 actually builds. | "...for example: will the winding pass 80 deg C (overheating) or not?" |

## Category 1 checks (Python, independent of the reference module)

Run with `.iuea-grader-env/bin/python` on `Lab Notebooks/CML3111/engineering_data.csv` (byte-identical to `Build/data/CML3111/engineering_data.csv`). The script is at `/private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/d327a2a5-164d-49e1-94aa-14fa1a0cd931/scratchpad/c1check.py`.

```
raw = pd.read_csv(...); raw.shape                         -> (91, 5); NaN: ambient_c 1, target 1
dup record_id 1 at file rows 1 and 91; record 4 target NaN; record 9 load -5   (slide 11 OK)
drop_duplicates -> 90; clean -> 88; split E1-4/E5/E6 -> 58, 15, 15               (slides 28, 37 OK)
training medians: load 62.845, ambient 26.07; missing ambient is record 14 (E2)   (slide 29 62.8/26.1 OK)
baseline mean 71.0331; val MAE 14.8506 (sum |e| 222.76), RMSE 16.93, MSE 286.6    (12,13,17,20,32 OK)
simple LR (load only, lstsq): b0 31.174, b1 0.66551; val MAE 4.2962 (sum 64.44)   (14,15,20 OK)
  at 60 %: 71.10 deg C                                                            (15 "about 71.1" OK)
multiple LR: b0 1.66193, b1 0.69486, b2 1.05420; val MAE 0.7775, RMSE 0.9211      (26,32,37 OK)
  (60,25)=69.709 (61,25)=70.404 (60,26)=70.763 (61,26)=71.458                    (27 OK)
first val rows: rec 5 67.03 / base -4.00 / lin 69.52 -2.49; rec 11 -17.67 / +4.79;
  rec 17 +9.25 / +8.01; rec 23 -23.09 / +2.98                                     (17, 20 OK)
own CART (variance split, both features, median-filled):
  depth1: load<=42.935 -> 50.29 | 79.63                                           (31 OK)
  depth2: 42.935 / 22.92 / 80.905 -> 42.60, 52.65, 74.15, 90.22                   (30 OK)
  depth4: val MAE 4.789, RMSE 6.287                                               (32, 37 OK)
gradient descent x=1,2,3 y=2,4,6 lr 0.05: L0 18.667, g0 -18.667;
  w = 0.9333, 1.4311, 1.6966, 1.8382, 1.9137; L = 5.310, 1.510, 0.430, 0.122, 0.035  (23-25 OK)
hypothetical MAE 2.75, MSE 12.25, RMSE 3.5                                        (18 OK)
```
Guide table (CML3111 column) and the notebook `CHECK` strings match all of the above. The notebook ships with outputs cleared, so its printed values were checked through the CHECK definitions.

## Cross-class notes
- **What Class 1 assumes:** the Weeks 1 to 7 pandas work (shape, isna, drop_duplicates, boolean filters, `.isin`), recalled on slides 4 and 5. It also assumes basic differentiation for slide 23 (reasonable for Year 3 engineers, but the loss L itself should be written, F9).
- **What it hands on:** baseline, MAE/RMSE, the group split with E6 sealed, training-only imputation, the pipeline, and the numbers 0.78 / 4.30 / 4.79 / 14.85. Class 2's recall (slides 4 and 5), Class 3 (0.78, 0.92, tree 4.79) and Class 4 (ablation 0.78 to 4.30, comparison table 14.85/16.93/0.78/0.92/4.79/6.29) quote these consistently. Notation (y, y-hat, b0/b1/b2, e_i = y - y-hat) is consistent with Classes 3 and 4.
- **Introduced lightly here and formalised later:** random seed (Class 3), overfitting (Class 3), the test set opened once (Class 4). Class 1 says only "untouched until the end of the block", which is consistent.
- **Gradient descent:** Class 2 logistic regression is fitted iteratively, so a single sentence in Class 1 separating LinearRegression (direct formula) from gradient descent (F1) would also set up Class 2 correctly.
- **Before tomorrow (Class 2 day, Block 1 quiz on Classes 1 and 2):** re-export the Class 1 student PDF from the 10 November pptx (F3). If possible, add the F1 sentence, because a quiz item on "how LinearRegression is trained" would expose the misconception.

## CML3112 and CML3113

**Summary.** Every number on the two decks, in the notes, on the check slide 37, in the guide's per-cohort table and in the notebook CHECK strings recomputes correctly from each cohort's own CSV. I checked them with my own NumPy code and with real scikit-learn 1.9.1, which is installed in `.iuea-grader-env`. Dates and closing times are right. The problems are cohort wording, one weak worked example (CML3113 slide 17), and one decision-tree score that changes with the random seed (CML3113).

### Per-cohort findings

| ID | Cohort | Slide / place | Cat | Sev | What is wrong | Fix |
|---|---|---|---|---|---|---|
| X1 | CML3113 | Slide 17 (formula line and caption), slide 20 row 1 | 1/4 | Medium | The worked residual is "e = 12.55 - 12.53 = 0.03 kWh/t". The arithmetic is visibly wrong: the shown values give 0.02 (see F29). The row is also a poor teaching example, because the error is almost zero and positive, while the symbol table explains the negative sign. | For CML3113, use a validation row with a clear error, such as record 11: 7.62 - 12.53 = -4.91 kWh/t. Better still, let c1.py choose the example row by size of error, not "first validation row". |
| X2 | CML3113 | Slides 32 and 37, guide table, lab Step 6 | 1/6 | Medium | The decision tree's validation MAE depends on random_state, because two splits tie. With scikit-learn 1.9.1, random_state 17 gives 1.20 / RMSE 1.45 (matches the slides). Seeds 0, 1, 2, 7 to 10, 12, 13, 15, 18 and 19 give 1.18 / 1.45. A student who leaves out `random_state=17`, or whose library version breaks ties differently, sees 1.18. Slide 37 then says "stop and ask". (CML3111 4.79 and CML3112 3.39 do not depend on the seed at depth 4.) | In the guide's Step 6 row, say "CML3113: 1.18 is also correct if random_state differs". On slide 37 for CML3113, write "about 1.2 kWh/t". |
| X3 | CML3112 | Slide 1 and slide 40 question: "predict cooling load from load and temperature" | 4 | Medium | "Predict cooling load from load" reads as circular: the target and the feature are both called "load". It is worse than the CML3111 wording issue in F6. | "...predict a building's cooling load (kW) from how hard the plant is working (load_pct) and the outdoor air temperature". |
| X4 | CML3112, CML3113 | Slide 21 notes | 4 | Low | The notes say "the right one when a large error is dangerous, such as a motor overheating". That is the CML3111 example, left in the other two decks. The notes are not in the PDF, but the lecturer reads them aloud. | Make the example a per-cohort field: "such as an undersized chiller on a hot day" (CML3112), "such as tripping the crusher motor" (CML3113). |
| X5 | CML3113 | Slide 15 example | 4 | Low | "5.60 + 0.116 x 60, which is about 12.5 kWh/t". With the rounded numbers on the slide the result is 12.56, which rounds to 12.6. The unrounded coefficients give 12.54. | "...= 12.56, about 12.6 kWh/t", or use load_pct 50. |
| X6 | CML3113 | Slide 32 bar label "1.2 kWh/t" vs slide 37 "1.20 kWh/t" | 4 | Low | The bar chart drops the trailing zero, so the two slides show the same number differently. | Use two decimals in the bar labels. |
| X7 | CML3112, CML3113 | Slide 18 (hypothetical 70/80/90/60) | 4 | Low | The hypothetical readings are on the CML3111 scale. For kWh/t (mean 12.5) they look unrelated to the cohort's data. They are labelled hypothetical and have no unit, so this is harmless but odd. | Optional: scale the example per cohort, or keep it and say "no unit". |
| X8 | CML3112, CML3113 | Slide 10 notes, slide 28 notes | 4 | Low | "how hard it was working" fits a crusher. For a building the input is the cooling plant load, not the building working. "whole building groups" in the slide 28 notes is fine. | CML3112 notes: "how hard the cooling plant was working". The `example_input` field in common.py already has this wording. |
| X9 | CML3113 | Slide 30 tree | 5 | Low (positive) | The depth-2 tree splits on ambient_c <= 21.1 in its left branch, so it shows two different features (scikit-learn confirms). The slide caption is generic and still true. | No fix needed. A note could point out that this tree uses both features. |

### Numbers recomputed (independent NumPy code; trees and coefficients confirmed with scikit-learn 1.9.1)
```
                              CML3112 (kW)                 CML3113 (kWh/t)
raw / dedup / clean / split   91 / 90 / 88 / 58,15,15      same (bad rows: rec 1 dup, 4 NaN target, 9 load -5)
training medians              62.845 %, 26.07 deg C (rec 14 missing ambient)   same
baseline mean                 48.1374  (slides 48.1 / 48.14)   12.5279 (12.5 / 12.53)
baseline val MAE, sum, RMSE   9.6866, 145.30, 11.127          2.7125, 40.69, 3.276
simple LR b0, b1              22.6496, 0.4256                 5.6007, 0.1157
simple LR val MAE, sum        3.1237, 46.86                   0.9770, 14.65
multiple LR b0, b1, b2        1.4935, 0.4466, 0.7557          1.1568, 0.1201, 0.1587
multiple LR MAE, RMSE         0.7427, 0.8835                  0.6732, 0.8148
slide 27 (60,25)..(61,26)     47.182 47.629 47.938 48.385     12.330 12.450 12.489 12.609
tree depth1 leaves            34.77 | 53.68                   8.90 | 14.03
tree depth2 leaves            29.82 36.30 50.12 60.54         7.09 9.14 13.03 15.97 (ambient_c<=21.10 split)
tree depth4 MAE, RMSE         3.392, 4.451                    1.200, 1.453 (rs=17); 1.179, 1.446 (other seeds)
slide 20 rows 5/11/17/23      base err -2.53 -11.50 +6.43 -14.61; lin err -1.56 +2.86 +5.63 +2.05   (OK to rounding, F29)
                              CML3113: base +0.03 -4.91 +1.09 -4.33; lin +0.29 -1.00 +0.87 +0.20  (OK to rounding, F29)
```
All agree with the slides, the notes, slide 37, the guide table (p.4) and `lab1.CHECK`.

### Dates, clock, notebooks, guide, student PDFs
- **CML3112:** slide 1 shows Tuesday 3 November 2026, 11:00 to 14:00. The Block 1 close is Tuesday 17 November, 11:00 (the start of its Class 3). The slide 3 clock (10/35/30/15/80/10, break before the lab) matches the guide's Tuesday clock and the notes ("an hour and a quarter", "an hour and twenty minutes").
- **CML3113:** slide 1 shows Friday 6 November 2026, 08:00 to 11:00. The close is Friday 20 November, 08:00. It uses the Friday recap clock, the same as CML3111.
- **Notebooks:** both `Class1_Lab_First_Model.ipynb` files have 44 cells and no saved outputs. The header and target wording are cohort-correct (cooling load, kW; crusher energy demand, kWh/t), and no "motor" or "deg C" target text leaks in.
- **Guide:** the per-cohort table (p.4) is correct for all three cohorts. The "class in one paragraph" on p.1 uses the CML3112 question only, which is fine for a shared guide, but the X3 wording problem carries into it.
- **Student PDFs (3 Nov):** for both cohorts, the only text difference from the current pptx is the missing "It is practice..." sentence on slide 39 (F3). CML3112's Class 1 was taught on 3 November, so its students have only ever had the older PDF.
