# CML3112 ML_PROJECT: Engineering ML project (online, timed)

<!-- BLOCK_ASSESSMENT_20261103 -->
<!-- PROJECT_SITTING_20261104 -->
<!-- PROJECT_ONLINE_20261113 -->
<!-- PROJECT_CORE_20261114 -->
<!-- PROJECT_NO_SUBMIT_20261114 -->
<!-- PROJECT_AMES_AI4I_20261114 -->
**What:** an individual, timed, auto-marked project in Google Colab. 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).

**When:** opens **Monday 23 November 2026, 00:00**, closes **Wednesday 25 November 2026, 23:59** (Kampala time). You have 3 hours from **Start**; they cannot be paused and stop at the window's close. **Start by Wednesday 25 November, 20:59** for the full 3 hours.

**Where:** online, from anywhere: your own laptop, Google account and internet. There is no Submit button: your notebook saves itself and is collected automatically at your deadline.

## The data

Two tables, the same for everyone. Both are inside the notebook, organised with plain column names and metric units. **A few problems were added on purpose for you to clean:** duplicate rows, rows with no target value, and impossible values.

- **Houses (real):** 2,935 rows of house sales in Ames, Iowa, 2006 to 2010, with 18 columns such as `neighbourhood`, `overall_quality`, `year_built`, `living_area_m2` and the target `sale_price_usd`. Source: Dean De Cock (2011), Journal of Statistics Education 19(3), https://doi.org/10.1080/10691898.2011.11889627.
- **Machines (synthetic):** 10,012 runs of a metal-cutting machine: `product_type`, temperatures, `rotation_speed_rpm`, `torque_nm`, `tool_wear_min` and the target `failure`. The data are generated to behave like a real machine, not measured on one. Source: Stephan Matzka (2020), UCI Machine Learning Repository, https://doi.org/10.24432/C5HS5C, CC BY 4.0.

- **Question 1:** predict a house's `sale_price_usd` from its numeric columns (`H_FEATURES`). Task 3b (2 marks) adds the three text columns (`TEXT_FEATURES`) with one-hot encoding; the recipe is given in the task.
- **Question 2:** warn when a machine fails (`failure` is 1). Logistic regression probabilities; a warning at 0.5 or more; confusion matrix counts, precision and recall.
- **Cleaning:** remove duplicate rows, rows with no target, and rows with an impossible value (a living area of 0 or less, a house built after 2010; a torque or speed of 0 or less); change `product_type` to a number. Other missing values stay for the imputer.
- **Split:** you split each table yourself with the given lines: 20 percent test, then 25 percent of the rest for validation (`random_state=17`), so 60/20/20. The test rows are used once, at the end.

## Tasks

Each task names its inputs and the results to store. Write plain code in as many cells as you like.

1. Clean `houses_raw` and `machines_raw` into `houses` and `machines`; Chart 1.
2. Split into `houses_train`, `houses_valid`, `houses_test`, `machines_train`, `machines_valid`, `machines_test`.
3. Baseline, linear regression and decision tree on `houses_train`, predicting `houses_valid`: `baseline_pred`, `linear_pred`, `tree_pred`, the three `_mae` and three `_rmse`; Chart 2.
3b. Do the text columns help? The given one-hot recipe on `houses_train`, predicting `houses_valid`: `encoded_pred`, `encoded_mae`. A comparison only, not part of the choice.
4. Warnings at 0.5 on the machines: `warning_proba`, `tp`, `fp`, `fn`, `tn`, `precision`, `recall`.
5. `chosen_model = choose_model({...})` with the supplied rule.
6. Only now use the test rows, once: refit on training and validation rows; `test_mae`, `test_recall`.
7. Fill in the `MEMO` form.

The only supplied cell is **Setup: run me first** (do not edit it). Each task's cells are also run on hidden data, so typed numbers fail and a mistake in one task does not cost the next.

## Marks

- **Part A (30):** A1 cleaning 6; A2 two labelled charts 2; A3 split 2; A4 three models 6; A5 MAE and RMSE 3; A6 no leakage 2; A7 warnings 3; A8 test set used once, after the choice 2; A9 results, reproducible (`random_state=17`), results and MEMO present 2; A10 Task 3b, the text columns 2.
- **Part B (15):** recommended model 3, validation MAE 3, test MAE and recall 2, improvement over the baseline 1, three limits 3, next step 1, two written answers 2.
- Final by Wednesday 2 December 2026.

## Steps

1. Open the entry link. Choose your course and type your registration number (for example 26/BCE/001/PS). Tick **This is me**; if your name is not shown, type your full name instead. type the Google email you use in Colab twice, press **Start**. Your 3 hours begin. A typo in the email can be corrected once on the page in the first 15 minutes.
2. Click **Open my project in Colab** with that Google account. Do not use Save a copy.
3. Run **Setup: run me first** (it starts a backup every 5 minutes and shows the time left after every cell).
4. Work from the top. Store the results under the names each task gives. Press **Ctrl+S** now and then.
5. Choose **Runtime, Restart session and run all**. Fix any error.
6. On the entry page, **Check my work** shows whether your saved notebook runs. It shows no mark.
7. At your deadline your work is collected. Finished early? Press **I have finished**.

After a disconnect, open the entry page and click Resume; the timer continues.

## Rules

- Individual work. Allowed: your slides, lab notebooks, revision guide, cheatsheet and own notes.
- **No AI** (Gemini, ChatGPT, Copilot or any other) and no help from another person.
- Any student may be asked afterwards, in an online call, to explain or change their code.

## Help

- Class channel, 08:00 to 20:00 each day of the window (hours to be confirmed by the lecturer).
- If something fails, post a screenshot there at once. The lecturer can give one fresh attempt; it still ends at the window's close.

**Rehearsal (unmarked):** released **Tuesday 17 November 2026** for the revision class. Exactly the project's tasks, files, result names and memo, with one change: the split uses `random_state=29`, so the numbers differ from the project's. Nothing is locked or marked. It has short self-study notes. Do it with a 3-hour timer.
