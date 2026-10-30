# Week 8 onwards: deck review and improvement plan

Reviewed 29 October 2026. Scope: CML3111, CML3112 and CML3113 decks for Weeks 8 to 15, read against what Weeks 1 to 7 actually taught. No deck, notebook or form was changed. Everything below is a finding or a proposal.

(You wrote "Week 5 is progressing to Machine Learning". I have read that as Week 8, the first model-fitting week.)

## 1. Bottom line

Weeks 1 to 7 are paced well. Week 3 spends 89 slides on Python basics, with trace tables and a worked example for each idea. From Week 8 that care stops. Week 8 puts a full modelling workflow into about 20 slides: train/validation/test groups, imputation, pipelines, linear regression, a baseline, a decision tree, MAE and RMSE. Several of these ideas are used before they are explained, and the deck contains one picture and no plot of the student's own data.

Weeks 10, 11 and 12 then spend 48% to 68% of their slides repeating Week 8's data preparation and model-fitting slides. Week 9 never fits a classifier. NumPy, the library you named, does not appear in any deck from Week 1 to Week 15.

The wrong link you spotted is real, and it is a placement problem: details in section 3.

## 2. What students arrive with after Week 7

| Weeks | What they can do | Teaching style that worked |
|---|---|---|
| 1 | Say what features, target, regression and classification mean. Predict "case 13" by hand and measure their own error. | Hand activity first, vocabulary second |
| 2 | Run cells in order, restart, save, use a repository | Deliberate order-of-execution trap |
| 3 | Values, types, operators, if/elif/else, functions, return, None, lists | Every idea traced step by step before the combined example |
| 4 | for/while, accumulators, dictionaries, tuples, sets, reading a CSV | Trace tables again |
| 5 | pandas: read_csv, shape, dtypes, head, column selection, Boolean masks, groupby, mean | Small 24-row file, hand-calculated totals before groupby |
| 6 | EDA, missing values, duplicates, copy(), median fill, histograms, scatter, bar charts | Raw copy kept, every cleaning step checked |
| 7 | Practical Test 1 rehearsal on the same skills | No new syntax |

Not yet seen by any student: NumPy, arrays, the idea of a model object, train/test splitting, overfitting, scikit-learn.

Week 1's hand-prediction activity is the best bridge into Week 8 and the current Week 8 deck does not use it.

## 3. The assignment link problem

Week 8 slide 51 is the correct form (A7, Regression and baseline, opens 30 Oct 11:00, closes 6 Nov 11:00). I matched it to `Assignment_Submission_Links.md` and it is right. The problem is what follows it. Slides 52 to 57 are a six-slide Data Analysis Project block with its own submission slide (slide 57, form DA_PROJECT, closed 30 Oct 11:00 for CML3111). The quiz slide comes after that. So the last assignment a student sees before the quiz is the Data Analysis one, and the deck calls it "Data analysis project submission".

The same block sits in all three Week 8 decks. CML3112's deadline was 27 Oct 11:00, the start of its own Week 8 class, so its link was already closed when the slide was shown. CML3113's closes at 08:00 on 30 Oct, the start of class.

I checked every form link in all 45 decks against the registry. All are valid forms for the right cohort. The mismatches are:

- CML3112 and CML3113 Week 6 have no A6 form link and no quiz link at all.
- The Week 1 quiz link is not in the Week 1 decks (they contain no links); each cohort's Week 1 catch-up quiz appears in its Week 2 deck instead.
- Every Week 8 to 12 quiz link matches the quiz registry.

Fix: remove slides 52 to 57 from the Week 8 flow. If you want a reminder that the project is due, make it one slide near the start, headed "Due today: Data Analysis Project (a separate submission)", and keep the Week 8 form as the final assignment slide. The rubric text on slides 52 to 56 ("Complete every original rubric criterion below") belongs in the project brief and not in this lesson.

## 4. Week 8 in detail (CML3111; the other two cohorts have the same structure, only the target changes)

Counts: 60 slides. About 10 re-teach Week 5 and 6 pandas, 9 are "Operations for the next example" cards repeating import, read_csv, shape and dtypes, 10 set up the data split, about 20 are machine learning, 4 wrap it in a function, 12 are assignment, link, quiz and exit material.

**Order of ideas.**
1. Slide 2, "Today's learning", says: "Use pandas tables for this week's data work." It is a generic line that appears unchanged in Weeks 8 to 12. A student reading it would not know the week is about prediction.
2. Slides 8 to 17 split the data into groups E1 to E4, E5 and E6 before any slide says why a model must be tested on rows it has not seen. That idea (and the group version of it) is not taught until Week 10 slide 8.
3. Slides 19 to 21 introduce SimpleImputer, make_pipeline and LinearRegression together. In the data, the training rows contain exactly 1 missing input cell and the validation rows contain 0, so the imputer demonstrates a problem students cannot see.
4. The straight-line idea gets one slide (18), a small figure of concrete strength against cement content, which is a different domain from the motor temperature students work on. There is no scatter of load against temperature, although the correlation in their file is 0.93 to 0.95. Students plotted scatters in Week 6, so the skill is there. The picture that makes regression obvious is missing.
5. X and y are named (slides 24, 25) and the notes say X is two-dimensional, but no slide shows a shape. `values[:5]` and `.tolist()` appear without any mention that predict returns a NumPy array.
6. DecisionTreeRegressor, DummyRegressor, MAE and RMSE each get one or two text slides. The tree has no picture of splits.
7. The assignment (predict_regression, 7 marks, plus regression_errors, 3 marks) asks for all of the above inside a function that takes lists of dictionaries. That is a large first step, and the deck shows how to wrap pandas in a function only after the modelling.

**Style.** Slides 3 to 6 and 19 to 38 are text boxes. Printed outputs sit in the speaker notes and not on the slide. The speaker notes are good; the slides themselves carry little of the explanation that Week 3 would have drawn.

**Text damage.** An automated renaming pass has replaced ordinary words with variable names. Examples in Week 8: "squared vertical baseline_errors" (slide 18, the caption), "MAE averages absolute baseline_errors" (slide 35), "selects the two input columns as a equipment_data" (slide 19), "maps group labels to validation_results" (slide 43), and in the notes "does not upload its modelling_data". In Weeks 8 to 15, `baseline_errors` appears 15 times and `test_data` 14 times in prose. Week 13 says "state the operational test_data" and "check the mean_load_by_equipment_group". The source is `scripts/descriptive_teaching_names.py` and `data/descriptive_names_manifest.json`; the substitutions need reversing in prose and keeping in code.

## 5. Weeks 9 to 15

| Week | What works | What to fix |
|---|---|---|
| 9 Classification and cost | The four-cell counting build-up (slides 12 to 21) is carefully paced | No classifier is ever fitted. The file `classification_case.csv` has 6 rows of actual and predicted labels. Probabilities and thresholds get one text slide (31) with no code. "Why accuracy alone is insufficient" is an assignment question, yet no slide shows accuracy being misleading. `get_dummies` (slides 32 to 34) is an unmotivated detour |
| 10 Validation and leakage | Group k-fold and the "negative MAE" convention are explained well | 33 of 54 slides (61%) repeat Week 8 or earlier. Overfitting is never shown: the word appears once in Weeks 8 to 15. "Three sets have different jobs" (slide 8) arrives two weeks after students used three sets |
| 11 Features and ablation | Ablation design is sound: same rows, one change | 24 of 50 slides repeat earlier weeks. Scaling is promised in the prerequisite map yet StandardScaler appears nowhere |
| 12 Model recommendation | Constraint filtering is clear | 44 of 64 slides (68%) repeat earlier weeks. The "candidate table" has one row (linear), so selection among models is never practised |
| 13 Reproducibility | Short and calm | Nothing machine-learning; the ML Project is regression only |
| 14 Test 2 rehearsal | Consistent with Test 1's approach | 19 of 69 slides repeat; check that the rehearsal covers what Weeks 8 to 12 now teach |
| 15 Presentations | Clear marking structure | The project brief is regression only, so Week 9 classification is not exercised again |

Across the whole course there is no `train_test_split`, no `matplotlib` use inside the ML weeks, no `LogisticRegression`, no `RandomForest`, no `predict_proba`, no learning of coefficients. I am not suggesting all of these be added. I list them so you can decide the boundary knowingly.

## 6. Proposed structure

Keep every graded item exactly as it is (function names, marks, forms, deadlines, hidden tests). All changes below are to how the lesson reaches the assignment.

### Week 8 rebuilt as five short blocks (180 minutes)

| Time | Block | Content | Visual |
|---|---|---|---|
| 0:00 | Bridge (10 min) | Reuse Week 1's "predict case 13". Today the computer does the pattern-reading | Week 1 figure beside the new plot |
| 0:10 | Look first (25) | Scatter of load against temperature using the matplotlib they know. Describe the pattern in words, draw a line by eye, read a prediction off it | Student's own data |
| 0:35 | Arrays in two slides (20) | NumPy: what an array is, `.shape`, why scikit-learn wants X as a table (2D) and y as a column (1D), `predict` returns an array, `.tolist()` converts it | Shape diagram: table, 2D box, 1D strip |
| 0:55 | Baseline and error (30) | Predict the mean for every row. Compute MAE on five rows by hand, then with pandas | Baseline line on the scatter |
| 1:25 | Break (10) | | |
| 1:35 | Fit and predict (30) | LinearRegression on one feature, then two. `coef_` and `intercept_` in °C per percent load. Create, fit, predict as three separate lines | Fitted line on the scatter |
| 2:05 | Why we hold rows back (20) | Taught before the split is used: a model scored on rows it learned from flatters itself. Then the E1–E4 / E5 / E6 split as already issued | Three-box diagram |
| 2:25 | Tree and imputer, briefly (15) | One picture of tree splits. One slide on filling missing inputs, noting the one missing cell | Tree drawn on the scatter |
| 2:40 | Assignment brief (15) and quiz (5) | The function wrapper demonstrated last, with the required return types | |

This is a heavy first ML week. If it cannot fit, defer the tree to the start of Week 9 and keep it in the assignment as a guided scaffold, which needs your decision (section 8).

### Week 9: add the missing classifier

Derive a binary label from the motor data (for example "overheating: target above a stated °C") so students stay with data they know. Fit `LogisticRegression` or `DecisionTreeClassifier`, show `predict_proba`, then move the threshold and watch the four counts change. Keep the existing 6-row file as the by-hand drill. Add one slide where a model that always predicts "no warning" scores high accuracy and finds no faults. Drop `get_dummies` from this week, or move it to Week 11.

### Weeks 10 to 12: replace the repeated block with a three-slide recap

Week 10 order: show a depth-1 and a depth-20 tree scored on training and validation rows (overfitting visible in numbers), then why three sets, then leakage, then group k-fold. Week 11: recap in three slides, add one plotted check that a derived feature helps, and either teach StandardScaler or remove "scaling" from the prerequisite map. Week 12: give students a candidate table with at least three real rows (baseline, linear, tree) built from fitted models, so selection is practised on something they produced. Each of these weeks drops by roughly 25 to 40 slides, which buys time for the visuals.

### Everywhere

1. Replace the generic "Today's learning" slide with week-specific outcomes (three sentences per week).
2. Replace the identical "Revision and submission checklist" text ("Explain each cleaning or modelling decision using your pandas table") with a week-specific exit check.
3. Reverse the renaming damage in prose.
4. Add at least one plot of the student's own data to every ML week.
5. Libraries: say once, in Week 8, what each library is for (pandas for tables, NumPy for the arrays scikit-learn uses, matplotlib for charts, scikit-learn for models) and repeat that line on the opening slide of Weeks 9 to 12.

## 7. Order of work

1. **Before Friday 30 October (CML3111 at 11:00, CML3113 at 08:00).** Remove or relocate the DA block in all three Week 8 decks. Reverse the renaming damage in Week 8. Replace slide 2 with real objectives. Add the scatter-and-line slide and a two-slide NumPy shape explanation. These are small edits to the content source.
2. **Weekend.** Rebuild the full Week 8 run as in section 6, and the CML3112 and CML3113 Week 6 link gap.
3. **Before Tuesday 3 November (CML3112 Week 9).** Week 9 classifier addition.
4. **Following two weeks.** Weeks 10 to 12 de-duplication and new visuals.

Because the decks are generated, edits to the `.pptx` files themselves would be overwritten by the next build. The content lives in `data/iuea_deck_content.json`, `scripts/pandas_continuity.py`, `scripts/stepwise_teaching_expansion.py` and `scripts/descriptive_teaching_names.py`, and the build is `scripts/build_decks.py`. Student notebooks are built from the same source, so the guided-practice notebooks and the ZIPs need regenerating with the decks to keep slide numbers in step.

CML3112 taught Week 8 on Tuesday 27 October, so for that cohort the improvements land as a short recap at the start of Week 9.

## 8. Decisions I need from you

1. May Week 8's tree and imputer move to a brief demonstration, keeping the assignment untouched, or must students be able to build them from the lesson alone?
2. Should Week 9 stay a metrics-only week, or gain the classifier demonstration in section 6? It would mean a new teaching dataset or a derived label.
3. Should I make the Week 8 edits now (section 7, step 1), then pause for you to look at the result before rebuilding the rest?

## 9. What I did and did not check

I read the full text and notes of CML3111 Weeks 5 and 8, the slide-by-slide text of Weeks 6, 7 and 9 to 15, the slide titles of Weeks 1 to 4, and compared Week 8 across cohorts. I rendered Week 8 to images and looked at 32 of its 60 slides. I checked the form links in all 45 decks against the registry and the quiz registry, computed the repeated-slide percentages by comparing slide text across weeks, and calculated the data facts (88 clean rows, 15/15/14/14/15/15 per group, 1 missing training input, correlation 0.93 to 0.95) from the issued CSVs.

I did not read CML3112 and CML3113 slide text in detail beyond the link and Week 8 comparisons, did not read Weeks 1 to 4 slide by slide, did not run scikit-learn (it is not installed here and there is no network), so I have not recomputed any model error. I have also not opened the student ZIP notebooks other than Week 8's guided practice, which mirrors the deck slide for slide. The memory notes I hold for this project were six weeks old and predate the rebuilt "beginner pathway" decks, so I relied on the files.
