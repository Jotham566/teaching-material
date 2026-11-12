# Audit: CML3111 Class 3 (Week 10, Friday 20 November 2026), "Can I trust this model?"

**Verdict**
1. Every number on the slides, in the notes and in the notebook matches what real scikit-learn 1.9.1 prints. I ran the notebook's code cells with real sklearn from `.iuea-grader-env`, and the sk_tree_replica stand-in turned out to be exact. The seed values 4.70, 3.95 and 3.85 are now confirmed, so the lecturer-guide prep note saying they "cannot be checked" is out of date.
2. The main weakness is in the concepts. The chosen depth 7 is called a "good fit", yet its own gap is 3.79 deg C, which the deck's rule ("a big gap means overfitting") calls overfitting. Depths 8 to 10 are labelled overfitting with no evidence, and the chosen depth itself changes with the random seed (6, 7 or 8). A beginner revising from the PDF will hit these contradictions.
3. The structure, formulas, worked examples, lab map and check table are sound. Fix 4 High and 11 Medium items before 20 November. Nothing in Class 3 blocks Class 2 tomorrow, but two cross-class items touch Class 2 (C3-09 and X1 below).

## Findings

| ID | Slide / cell | Cat | Sev | What is wrong | Concrete fix |
|---|---|---|---|---|---|
| C3-01 | s11 picture, s13, s14, notes s13 | 1, 3 | High | s13 says "A big gap means overfitting". The chosen depth 7 has a gap of 3.79, almost the same as depth 10 (3.95) and larger than depth 4 (3.06). Yet the s11 picture labels depth ~7 "Good fit" and depths 8 to 10 "Overfitting". The validation curve is flat from 7 to 10 (3.91, 3.97, 3.84, 3.95), so nothing in the data marks 8 to 10 as worse than 7. | Say plainly: "We choose by validation error, not by the gap. Every tree from depth 5 up fits the training rows almost perfectly (overfits). Their validation errors are about the same, so we take the simplest." Relabel the s11 bands as 1 to 3 "underfitting (both errors high)" and 5 to 10 "training error near 0: overfitting the training rows; validation flat". Drop the "Good fit" label at 7, or explain it on the slide. |
| C3-02 | s15, s16, s37, notebook Step 2 | 1 | High | "Chosen max_depth 7" is presented as a property of the data. It depends on random_state: seed 17 gives 7, seeds 1, 0 and 42 give 6, and seed 99 gives 8. Depths 6 to 10 swing by up to 1 deg C between seeds, yet s31 shows only the depth-10 tree moving. | Add one line to s31 (and a CHANGE task in Step 5): "With random_state 1 the rule picks depth 6, with 99 it picks 8. On 15 validation rows the choice itself is partly luck. That is why we cross-validate." Or choose the depth with GroupKFold CV instead of the single E5 split. |
| C3-03 | s30 checklist + notes | 1, 4 | High | The notes say "If you can answer yes to all five, you may trust the number". Question 3 ("Does any feature come from the target, or only exist after the event?") must be answered **no**, so a "yes" means leakage. | Reword Q3 so that yes is the safe answer: "Is every feature available at the moment you need the prediction, and none built from the target (no target leakage)?" |
| C3-04 | s17 picture and text, s21 | 3, 5 | High | A beginner revising without notes cannot tell why K-fold and GroupKFold differ. The s17 picture shows tidy blocks and never says that each K-fold fold mixes all four motors (fold 1 = E1 4, E2 4, E3 2, E4 2 rows), so the same motor is in training and validation. That reason is only in the s21 notes. | Add to s17 or s21: "The rows of E1 to E4 are interleaved, so every K-fold fold holds rows of all four motors. The model has already met each motor in training. GroupKFold removes that." Optionally colour the fold cells by group. |
| C3-05 | s27 caption, s28 table, notebook print "all rows (leaky)" | 1 | Medium | "25.37 from all rows" is false. All 88 cleaned rows give a median of **26.07**, the same as the training rows. 25.37 is the median of training plus validation (73 rows). The notebook markdown says this correctly, but the slides and the printed label do not. | Write "25.37 from the training and validation rows together (73 rows)" on s27 and s28, and change the notebook print label to match. |
| C3-06 | s24 lead, s6, Class 4 recall | 1, 3 | Medium | s24 defines leakage as "information from held-out data ... reaches the model". Target leakage (s29) comes from the target of the training rows themselves, not from held-out rows, so the definition contradicts its own third kind. | Use the s6 wording everywhere: "information the model would not have at prediction time (held-out rows, or the target itself) reaches it while it is trained." |
| C3-07 | Guide p1 prep | 1 | Medium | The guide says the slides show "about 4.7 and about 3.9" for seeds 1 and 99. The slides show **about 3.8** for seed 99 (real value 3.85), and the guide's own table says 3.85. The guide also says the stand-in "cannot check them", but real sklearn 1.9.1 confirms 4.70, 3.95 and 3.85. | Change the prep note to "4.7 and 3.8 (real scikit-learn 1.9.1 gives 4.70 and 3.85)" and drop the "cannot check" wording. |
| C3-08 | Notes s3 (plan_note) | 1 | Low | "The first seventy minutes are concepts only". The clock gives 10 + 40 + 30 = **80** minutes. | Say "eighty minutes". |
| C3-09 | Notes s39 (and c1, c2, c4) | 1 | Medium | "it does not count toward your final mark (only A1 to A5 and Q1 to Q5 do)". The Week 12 project, worth 40 percent, is left out, which contradicts c4. | Say "only A1 to A5, Q1 to Q5 and the Week 12 project do". |
| C3-10 | s39 | 1, 2 | Medium | The Block 2 assignment closes "Friday 4 December, 11:00". c4 puts the 3-hour project sitting in the class slot on Week 12, which for CML3111 is Friday 4 December at 11:00. The deadline is the minute the project starts. | Confirm with the lecturer. Move the deadline earlier (for example Thursday 3 December) or state the clash on purpose. |
| C3-11 | Student PDF s39 (3 Nov) vs pptx (10 Nov) | 1 | Low | The PDF students revise from lacks "Block 2 is practice: it does not count toward your final mark, but it is collected and you get feedback." No other text differs on the 40 slides. | Re-export the student PDF after the fixes above. |
| C3-12 | s22 symbol table "E1, then E2, E3, E4 in turn" (also lab4) | 1 | Low | Real GroupKFold(4) holds out E2, E1, E4, E3 in that order. It balances by group size and does not go alphabetically. The notebook sorts its output, so the printed result is fine. | Say "each of E1 to E4 once (scikit-learn chooses the order)". |
| C3-13 | s34 notes | 1 | Low | "the workflow in six lines". The code has 7 lines. | "seven lines" (or "four statements"). |
| C3-14 | s14 note and question, notebook cell 12 | 2, 4 | Medium | "The linear regression model from Class 1 scores 0.78 deg C, better than every tree" and "What does that suggest about the shape of this data?" are never answered on a slide, in the notebook or in the guide. A student revising alone is left wondering why we spend the class tuning a model that is 5 times worse. | Add one sentence: "The target rises smoothly, close to a straight line, with load and ambient temperature. A tree can only make steps, so the straight line wins here. Today the tree is our test case for trust. Class 4 compares models with these same tools." |
| C3-15 | s26 | 3 | Low | "it reproduces their answers (overfitting)". Contamination is memorising rows that were seen in training, so calling it overfitting mixes two ideas. | "...so it reproduces their answers: it has already seen them." |
| C3-16 | s17 points | 4 | Medium | "In each row, the tree is trained on 4 folds" and "After 5 rows each fold has been..." use "row" for a line of the picture on the same slide that uses "rows" for data rows. | "In each line of the picture..." / "After 5 rounds...". |
| C3-17 | s16 notes; notebook CHANGE cell 13 | 4 | Low | "What would change if the limit were 1.00?" The limit is in deg C (4.03), so 1.00 deg C would admit no depth. The notebook means the multiplier. | "...if we multiplied by 1.00 instead of 1.05?" |
| C3-18 | s18 and s28 symbol tables | 3 | Low | The tables list "s" and "σ" while the formulas use s_j, σ_s and σ_j. σ means the spread of fold scores on s18 and the spread of a column on s28. s10 never names i. | Write s_j, σ_s and σ_j in the tables. Add "i: row number" to s10. |
| C3-19 | s36 picture | 5 | Low | The Step 4 key icon renders as a lone yellow dot (the key shaft is missing), and "Contamination," touches the box edges. | Fix the icon size, or use the same key glyph as s25, and wrap the text. |
| C3-20 | s39 | 5 | Low | Item 2 is 4 lines at 18 pt and sits on the dividers. | Split it into two list items. |
| C3-21 | s36 title vs notebook | 6 | Medium | "the first five [steps] end with a check". Only Step 1's READ points to the check slide. Steps 2 to 5 have no check cell or expected value, and students are told to keep the slides closed. | Add a short markdown "CHECK: you should see ..." after the key cell in Steps 2 to 5, with the s37 numbers. |
| C3-22 | Notebook Step 4, Leakage 2 and 3 | 6 | Low | There is no PREDICT before these two cells, and the READ for Leakage 2 gives the answer away ("the two scores are the same"). | Add PREDICT: "Will the leaky median change the MAE?" and "What MAE will the target feature give?" |
| C3-23 | Notebook cell 34 THINK | 6 | Low | It asks which checklist question each leak breaks, but students were told to keep the slides closed. | Paste the five questions into the notebook. |
| C3-24 | s34 vs notebook | 6 | Low | The slide recipe negates at print (`-cv_scores.mean()`). The notebook negates at assignment (`cv_scores_group = -cross_val_score(...)`) and names the pipeline `pipe`. | Use one convention in both. |
| C3-25 | Guide slide map | 6 | Low | The single guide shows CML3112 titles and numbers (slide 20 "mean 3.27, standard deviation 0.29 kW"). A CML3111 lecturer reading the map sees the wrong numbers. | Make titles cohort-neutral in the map, or add a note. |
| C3-26 | Clock s3 | 2 | Low | Concepts part 1 covers 16 slides, 7 of them formula or worked tables, in 40 minutes. The rescue line covers only the by-hand table. | Add a second rescue option: skip s22 (the GroupKFold formula repeats s18). |
| C3-27 | Notes s8, s24, s32, s33 | 7 | Low | Slogans: "Same model, same data, two very different stories", "the first real machine breaks the spell", "It is the difference between a result and a claim", "These habits are the rulebook". s11 and s14 repeat the title "As max_depth grows, training error keeps falling but validation ...". | Cut the slogans. Retitle s14 "Five depths in one table: leaf nodes, errors and the gap". |
| C3-28 | s30 notes / c4 recall | 3 | Low | "I will ask for it again next class". The Class 4 recall does not ask for the checklist. | Make one Class 4 recall question "Name three questions from the trust checklist", or drop the promise. |

Counts for the CML3111 table: 28 findings in all, High 4, Medium 8, Low 16. By primary category: 1 = 12, 2 = 2, 3 = 5, 4 = 2, 5 = 2, 6 = 6, 7 = 1. All 28 come from the shared `c3.py` / `lab3.py` / guide text, so they apply to **all cohorts**, except where the CML3112 and CML3113 section below says how a finding changes for that cohort.

## Category 1 checks (Python, real scikit-learn 1.9.1, `.iuea-grader-env`)

All notebook code cells were run as written (`c3work/nb3.py`, extracted from `Class3_Lab_Trust.ipynb`) against `Lab Notebooks/CML3111/engineering_data.csv`, which is identical to `Build/data/CML3111` (md5 3d50393b...). Output, abridged:

```
rows left 88; training, validation, test 58 15 15
depth 1 train 7.04 val 7.86 gap 0.82 | depth 2 4.28 7.74 3.46 | depth 4 1.73 4.79 3.06
depth 7 0.12 3.91 3.79 | depth 9 0.01 3.84 | depth 10 0.00 3.95 3.95
lowest 3.84, within tolerance [7, 8, 9, 10], chosen 7; linear MAE 0.78 (RMSE 0.92)
5-fold 4.66 4.17 3.95 4.65 4.82 -> mean 4.45 std 0.33 (np.std, ddof 0)
GroupKFold E1 5.08 E2 4.11 E3 3.73 E4 3.67 -> mean 4.15 std 0.56; E5 single split 4.79
honest 3.95, leaky 0.00; fill 26.07 vs 25.37, MAE 3.95 both; target_rounded 1.09
seeds tree 1/17/99: 4.70 3.95 3.85; shuffled CV 1/17/99: 4.83 4.35 4.13
```
All of these match the slides, the s37 check table, the guide table and `c3.refs` (seed_tree 99 = 3.8495, so "about 3.8" is right).

Leaf counts (real `get_n_leaves`): depths 1, 2, 4, 7, 10 give 2, 4, 15, 47, 58. These match s14. 58 unique (load, ambient) pairs, so depth 10 is exactly one leaf per training row. Scaler μ and σ for load_pct are 59.89 and 22.73; row 1 gives (59.15 - 59.89) / 22.73 = -0.03. Missing values: 1 (ambient_c, training only). Illustrative figures: MAE 2, MSE 14/3 = 4.67, RMSE 2.16. By hand: mean 3, sd sqrt(0.5) = 0.71. Class 2 recall: always-no accuracy 0.80; threshold 0.5 gives recall 0.67 and FP 0, threshold 0.3 gives recall 1.00 and FP 0.

C3-05:
```python
m.ambient_c.median()                      # all 88 cleaned rows -> 26.07
pd.concat([tr, va]).ambient_c.median()    # training + validation -> 25.365
tr.ambient_c.median()                     # 26.07
```
C3-02:
```python
for s in [1,17,99,0,42]:
    v=[mae(va.target, make_pipeline(SimpleImputer(strategy="median"),
        DecisionTreeRegressor(max_depth=d, random_state=s)).fit(tr[F],tr.target).predict(va[F])) for d in range(1,11)]
    lo=min(v); print(s, min(d for d,x in zip(range(1,11),v) if x<=lo*1.05))
# seed 1 -> 6, 17 -> 7, 99 -> 8, 0 -> 6, 42 -> 6
```
C3-04:
```python
for i,(a,t) in enumerate(KFold(5).split(tr)): print(i+1, tr.equipment_id.iloc[t].value_counts().to_dict())
# fold 1 {'E1': 4, 'E2': 4, 'E3': 2, 'E4': 2} ... every fold holds all four groups
```
C3-12: `[tr.equipment_id.iloc[t].unique() for _,t in GroupKFold(4).split(tr[F],tr.target,tr.equipment_id)]` gives E2, E1, E4, E3.
C3-01: the gaps at depths 4, 7 and 10 are 3.06, 3.79 and 3.95 (from the output above).

## Cross-class notes

- **What Class 3 assumes from earlier classes.** These are all taught: MAE and RMSE (Class 1, recalled on s10); the E1 to E4 / E5 / E6 split and the cleaning to 88 rows (Class 1); max_depth and leaf nodes (Class 1, and lab1 CHANGE tried depths 1, 2 and 8, as s11 says); SimpleImputer and make_pipeline (Class 1 lab); StandardScaler and the z-score (Class 2, lab2 cell on standardisation); recall, FN/FP and thresholds 0.5 and 0.3 (Class 2 lab). One gap: "hyperparameter" appears in the notebook but not on the slides. Class 1 defined it, so add a one-word recall on s11.
- **What Class 3 hands to Class 4 and the project.** Group cross-validation (mean ± std), the tolerance or parsimony rule for choosing, no leakage via Pipeline, a reproducible seed and run record, and a sealed test set.
  - Class 3 never states when the test set is opened ("once, after the choice"). It only says "never tune on it". Check that Class 4 says this.
  - Class 3 cross-validates only the depth-4 tree, never the linear model. The model comparison under GroupKFold is left to Class 4 (lab4 does it).
- **X1 (touches Class 2 tomorrow).** c1, c2, c3 and c4 notes all say "only A1 to A5 and Q1 to Q5" count toward the final mark, leaving out the 40 percent project. In c2 this is in the notes for slide "How this class counts". Fix it before tomorrow if the lecturer reads it aloud.
- **X2.** The Class 4 recall (c4 line 198) repeats the narrow leakage definition "from held-out rows" (see C3-06). Fix both together.
- **X3.** The Block 2 deadline is Friday 4 December at 11:00 (C3-10). Check it against the Class 4 project-sitting time.
- **X4.** lab4 repeats "E1, then E2, E3, E4" for the GroupKFold order (C3-12).
- **X5.** Student PDFs date from 3 November. For Class 3 only s39 differs, but re-export all four after the fixes.

## CML3112 and CML3113

**How I checked.** I ran each cohort's notebook code cells as written, with real scikit-learn 1.9.1, against `Lab Notebooks/<code>/engineering_data.csv`. Those files are identical to `Build/data/<code>` (md5 8f932237... for CML3112, 17dc9827... for CML3113). I then compared the printed output with the slide text dump, the slide PNGs (s8, 11, 14, 16, 17, 20, 21, 23, 26, 29, 31, 37), `c3.refs` and the guide's per-cohort table.

**Every printed number matches** the slides, the notes, the s37 check table and the guide table for both cohorts:
- validation curve, leaf counts, linear MAE and RMSE (0.74 / 0.88 kW; 0.67 / 0.81 kWh/t);
- the five K-fold scores and their worked sums (16.37, 0.427, 0.085, 0.29; 5.82, 0.276, 0.055, 0.24);
- GroupKFold scores, honest and leaky MAE, medians, target-leakage MAE, and the seed values.

The features are the same in all three CSVs, so the scaler and median numbers (59.89, 22.73, 26.07, 25.37) are correct for every cohort. In every cohort, each plain K-fold fold contains all four groups, so C3-04 holds everywhere. The student PDFs (3 November) differ from the pptx only on s39, the same as for CML3111 (C3-11).

Dates, times and wording are correct:
- CML3112: Tuesday 17 November 2026, 11:00 to 14:00. Cooling load in kW; story about buildings and the cooling plant.
- CML3113: Friday 20 November 2026, 08:00 to 11:00. Crusher energy demand in kWh/t; story about crushers and the pit power plan.
- Units appear in every table caption and figure axis.

### Cohort-specific findings

| ID | Cohort | Slide / cell | Cat | Sev | What is wrong | Concrete fix |
|---|---|---|---|---|---|---|
| K1 | CML3113 | s4 notes, s5 table, s5 notes (also in the 3 Nov student PDF) | 1 | **High** | "Recall rose from 1.00 to 1.00. False positives went from 1 to 2." and "moved recall from 1.00 to 1.00". At thresholds 0.5 and 0.3 recall is already 1.00. The `recall` template in c3.py only branches on FP, never on recall. The Class 2 CML3113 deck says this correctly ("recall stays at 1.00; FP goes from 1 to 2"). | Branch on `t5["recall"] == t3["recall"]` and say "Recall stayed at 1.00. False positives went from 1 to 2." in the answer and both notes. |
| K2 | CML3113 | s16, s14, notebook Step 2 | 1, 4 | Medium | The rule is on a knife edge. Depth 3 has V = 1.1749 and the limit is 1.1743, so depth 3 fails by 0.0006. Both print as **1.17**: the notebook prints "depth 3 ... validation 1.17" and the slide prints "limit 1.17 kWh/t". A student checking by hand concludes depth 3 passes and should be chosen. s14 does not show depth 3. | Print the limit and the curve to 3 decimals in this cell and on s16 (1.174 vs 1.175), or add one line: "Depth 3 (1.175) misses the limit (1.174) by a hair. With so few rows the rule is sensitive." |
| K3 | CML3112 | s16 table and notes, notebook Step 2 | 3, 4 | Medium | Only depth 7 passes ("Depths that pass: 7"), so the tolerance rule just returns the lowest score and parsimony is never shown. The notes read "The depths that pass are 7. We take the smallest of them". | Write a single-pass branch: "Only depth 7 is within 5 percent, so here the rule and the lowest score agree." The CHANGE task (×1.00) then shows nothing new, so for this cohort ask for ×1.10, which gives depths 6, 7 and 8 and picks 6. |
| K4 | CML3113 (and CML3112 CV column) | s31, s37, s31 notes | 1, 4 | Medium | At one decimal the seed demonstration shows no change. For CML3113 the tree gives "about 1.2, about 1.2, about 1.3" (real values 1.21, 1.18, 1.28) and shuffled CV gives "1.1, 1.1, 1.0" (1.06, 1.08, 1.00). The notes say "about 1.2, 1.2 or 1.3 ... depending on the seed". For CML3112, CV for seeds 17 and 99 are both "about 2.9" (2.90, 2.87). | Show 2 decimals for all cohorts. Real scikit-learn 1.9.1 reproduces the reference exactly (checked), so "about" is no longer needed. Keep "a difference in the second decimal is fine" only for other library versions. |
| K5 | CML3112 | C3-02 | 1 | Medium | The chosen depth depends on the seed for this cohort too: seed 1 gives 6, seeds 17, 0 and 42 give 7, seed 99 gives 8. CML3113 is stable at 5 for all five seeds tried. | As C3-02 (all cohorts). The CML3113 deck can say the choice is stable there. |
| K6 | CML3113 | s23 note and notes | 1 | Low | "Group E5 turned out harder than the average group ... the single split gave a gloomier answer." The difference is 1.20 vs 1.16 (K-fold sd 0.24) and vs 1.09 (sd 0.15), and held-out group E2 scores 1.20 too. That is well inside the spread. | For CML3113 say "E5 is close to the cross-validation means; the standard deviation shows the difference is within normal spread." Use a threshold such as gap > 1 sd to choose the sentence. |
| K7 | CML3113 | s26 notes | 1 | Low | "The error drops to 0.01 ... so the leaky score is perfect". | "almost perfect". |
| K8 | per cohort | C3-01 | 3 | (cohort severity) | C3-01 differs by cohort. CML3112: the validation curve rises after depth 7 (2.62, then 2.88 and 2.93), so "Good fit at 7" is defensible and only the gap sentence on s13 conflicts. CML3113: the curve is flat from depth 3 (1.12 to 1.26). The chosen depth 5 has gap 0.79 against 0.72 at depth 4, and the "Overfitting" band on depths 8 to 10 is not shown by the data. CML3111 is the worst case (High). | Same fix as C3-01. The wording must not assume a U-shaped curve. |
| K9 | per cohort | C3-10 | 1 | Medium | Block 2 closes CML3112 Tuesday 1 December 11:00 and CML3113 Friday 4 December 08:00. Each is the start of that cohort's own Week 12 class slot, where c4 places the project sitting. | As C3-10. |
| K10 | Guide | p1 prep, p5 table | 1 | Low | The guide's per-cohort table is right for all three cohorts. The prep note quotes only CML3111 seed values, and wrongly (C3-07). The CML3112 and CML3113 lecturers get no "confirm in Colab" values. | Point the prep note at the table row "Depth-10 tree, random_state 1, 17, 99", which is correct for all cohorts. |

**Cross-class, cohort-dependent.** The coordinator already knows that Class 3 uses a 5 percent tolerance while Class 4 uses 10 percent. Under 10 percent the chosen depth changes for two cohorts: CML3112 goes from 7 to **6** (limit 2.877, depths 6, 7 and 8 pass) and CML3113 goes from 5 to **3** (limit 1.230). CML3111 stays at 7 (limit 4.22). If Class 4 or the project recalls "your chosen max_depth from Class 3", two cohorts get a different answer under the later rule. The same applies to the known ddof difference: Class 3 divides by k (np.std, ddof 0) and the project asks for ddof=1. For example, CML3113 K-fold sd is 0.24 with ddof 0 and 0.26 with ddof 1.
