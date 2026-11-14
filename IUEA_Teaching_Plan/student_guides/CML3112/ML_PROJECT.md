# CML3112 ML_PROJECT: Engineering ML project (online, timed)

<!-- BLOCK_ASSESSMENT_20261103 -->
<!-- PROJECT_SITTING_20261104 -->
<!-- PROJECT_ONLINE_20261113 -->
<!-- PROJECT_CORE_20261114 -->
<!-- PROJECT_NO_SUBMIT_20261114 -->
**What:** an individual, timed, auto-marked project in Google Colab. 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).

**When:** opens **Monday 23 November 2026, 00:00**, closes **Wednesday 25 November 2026, 23:59** (Kampala time). You have 3 hours from **Start**; they cannot be paused and stop at the window's close. **Start by Wednesday 25 November, 20:59** for the full 3 hours.

**Where:** online, from anywhere: your own laptop, Google account and internet. There is no Submit button: your notebook saves itself and is collected automatically at your deadline.

## The data

One real file for everyone: Steel Industry Energy Consumption, DAEWOO Steel, Gwangyang, 2018, one reading every 15 minutes, 35,040 rows. It is inside the notebook. Source: Sathishkumar V E, Changsun Shin, Yongyun Cho (2021), UCI Machine Learning Repository, https://doi.org/10.24432/C52G8C, CC BY 4.0.

- **Question 1:** predict `Usage_kWh` from the lagging and leading reactive power, `NSM` and a weekend flag. The power factors and `CO2(tCO2)` are calculated from `Usage_kWh`: do not use them.
- **Question 2:** a warning is a reading with `Usage_kWh` at or above 60 kWh. Logistic regression probabilities; a warning at 0.5 or more; confusion matrix counts, precision and recall.
- **Split by month:** train January to August, validate September and October, test November and December.

## Tasks

Each task names its inputs and the results to store. Write plain code in as many cells as you like; functions, loops and `if` are optional.

1. Clean `raw` into `clean`; Chart 1.
2. Split `clean` into `train` and `valid`.
3. Baseline, linear regression and decision tree on `train`, predicting `valid`: `baseline_pred`, `linear_pred`, `tree_pred`, the three `_mae` and three `_rmse`; Chart 2.
4. Warnings at 0.5: `warning_proba`, `tp`, `fp`, `fn`, `tn`, `precision`, `recall`.
5. `chosen_model = choose_model({...})` with the supplied rule.
6. `test_rows = open_test_set(chosen_model)` once; refit on `train` and `valid`; `test_mae`, `test_recall`.
7. Fill in the `MEMO` form.

The only supplied cell is **Setup: run me first**. Each task's cells are also run on hidden data, so typed numbers fail and a mistake in one task does not cost the next.

## Marks

- **Part A (30):** A1 cleaning 7; A2 two labelled charts 2; A3 split 2; A4 three models 6; A5 MAE and RMSE 3; A6 no leakage 2; A7 warnings 3; A8 test set opened once 2; A9 results, reproducible (`random_state=17`), results and MEMO present 3.
- **Part B (15):** recommended model 3, validation MAE 3, test MAE and recall 2, improvement over the baseline 1, three limits 3, next step 1, two written answers 2.
- Final by Wednesday 2 December 2026.

## Steps

1. Open the entry link. Type your registration number, tick **This is me**, type the Google email you use in Colab twice, press **Start**. Your 3 hours begin. A typo in the email can be corrected once on the page in the first 15 minutes.
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

**Rehearsal (unmarked):** released **Tuesday 17 November 2026** for the revision class. Same tasks and steps, same file, another target (lagging reactive power, kVarh). Nothing is locked or marked. It has short self-study notes. Do it with a 3-hour timer.
