# CML3113 ML_PROJECT: Engineering ML project (online, timed)

<!-- BLOCK_ASSESSMENT_20261103 -->
<!-- PROJECT_SITTING_20261104 -->
<!-- PROJECT_ONLINE_20261113 -->
**What it is:** the Engineering ML project is an INDIVIDUAL, TIMED, AUTO-GRADED test of 3 hours in Google Colab. It is worth 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40). There is no demo, no upload form and no take-home. It covers only what was taught in Weeks 1 to 10: the first half of the semester and Classes 1 to 3 of the second half. Class 4 (Week 11) is not in the project.

**When:** one online window for all three classes. It opens on **Monday 23 November 2026 at 00:00** Kampala time and closes on **Wednesday 25 November 2026 at 23:59**. You choose when to start. Your 3 hours (180 minutes) begin when you press **Start test** on the entry page, and they stop at the window's close if that comes first. **Start by Wednesday 25 November at 20:59** to get the full 3 hours. These dates are confirmed.

**Where:** online, from anywhere. You need your own laptop, your own Google account and a working internet connection for the whole 3 hours. There is no room and nobody watches you in person. The entry page, the countdown and the Submit test steps are the same as in Practical Test 1.

## The data

Every student in all three classes works on the same real file. There are no data variants. It is the "Steel Industry Energy Consumption" dataset from DAEWOO Steel in Gwangyang, South Korea: one reading every 15 minutes through 2018, 35,040 rows. Your client is the plant's energy manager. The file is built into the notebook, so you download nothing during the window.

Source: Sathishkumar V E, Changsun Shin, Yongyun Cho (2021). Steel Industry Energy Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C52G8C. Licence CC BY 4.0.

- **Question 1 (regression):** predict `Usage_kWh`, the energy used in each 15-minute reading, from the lagging and leading reactive power, `NSM` (seconds since midnight) and a weekend flag made from `WeekStatus`. The power factors and `CO2(tCO2)` are left out because they are calculated from `Usage_kWh`: using them would be target leakage. Errors are in kWh.
- **Question 2 (warnings):** a warning is a reading with `Usage_kWh` at or above 60 kWh, a high-demand quarter hour. You fit logistic regression and compare the thresholds 0.3, 0.5 and 0.7 using a missed warning cost of 5 and a false alarm cost of 1.
- **Split by month:** training is January to August, validation is September to October, and the test set is November to December. Cross-validation uses folds by month over January to October.

## What you do

The notebook has eight tasks:

1. Clean the rows.
2. Split the data by month.
3. Fit three models: a baseline, linear regression and a decision tree. Score them with MAE and RMSE.
4. Warnings: fit logistic regression, then use the confusion matrix, precision, recall, F1, AUC and the cost table to choose a threshold.
5. Run cross-validation by month.
6. Choose a model. Build `candidate_table` from your own validation MAEs and the supplied `LATENCY_MS`, then call the supplied `choose_model` cell. Do not edit that cell. The rule it applies: keep the models whose validation MAE is at most `MAX_MAE` and whose time is at most `MAX_MS`, then take the smallest validation MAE.
7. Open the test set once, with the supplied `open_test_set` cell, after you have chosen your model and threshold.
8. Fill the Part B memo form (`MEMO`).

You may add your own cells anywhere. Your work is marked wherever it is, as long as the required function names exist when the notebook runs from the top. Do not edit or delete the supplied cells.

## How it is marked

- **Part A: coded notebook, 30 marks.** Functions you write are run on data you cannot see (24 marks): A1 Clean the rows 3; A2 Split by month 2; A3 Baseline model, linear regression and decision tree 4; A4 MAE and RMSE 2; A5 Warning probabilities 2; A6 Confusion matrix, precision, recall, F1, cost and AUC 4; A7 Cross-validation by month 4; A8 Your results on the data 1; A9 The test set result 2. Six more marks check how you worked: A10 the test set (November to December) is opened **once** and only **after** you have chosen your model and threshold (2); A11 no data leakage, so preprocessing is fitted on the training months only (2); A12 you keep `random_state=17` so the result is reproducible (1); A13 your charts have a title, named axes and the unit, and the pipeline requirements are met (1).
- **Part B: decision memo, 15 marks.** The memo is a form of fields inside the notebook: your recommendation 3, validation results 3, test results 2, cross-validation 1, three limits chosen from a list 3, one next step chosen from a list 1, and two short written answers 2. It is marked automatically. Nothing is marked by hand.

**Results:** marks are final about a week after the window closes, by Wednesday 2 December 2026.

**Rehearsal (unmarked):** a practice notebook on the same steel file, with a different target (lagging reactive power, in kVarh) and its own warning, is released right after Class 3, on **Friday 20 November 2026**. Nothing is submitted or marked. A fully solved walk-through is not given: do the rehearsal yourself, with a 3-hour timer if you can. It is also a good way to check that your laptop, Google account and internet work.

## Rules

The rules are the same as in Practical Test 1. This is individual work. You may use your lecture slides, lab notebooks, revision guide, cheatsheet and your own notes. **No AI or outside help:** do not use Gemini, ChatGPT, Copilot or any other AI tool, and do not get answers from another person. When you submit, you confirm a declaration that the work is your own.

After the window, the lecturer may ask any student to an online call to explain part of their code or change it while the lecturer watches. This is the understanding check. Being asked does not mean you are suspected of anything. The copy checks and the identity checks still run on every submission. A short list of unusual cases (for example identical written answers or copied code) is checked by the lecturer; a flag alone never lowers a mark.

## Help during the window

- Questions about the wording of a task or about a technical problem: post them on the class channel. The lecturer answers from 08:00 to 20:00 each day of the window (these hours are for the lecturer to confirm). The lecturer will not write or debug your answers.
- If something fails (your laptop crashes, the internet goes down, the entry page or Colab breaks), report it on the class channel **at once**, with a screenshot. The lecturer can allow you one fresh attempt. It still ends at the window's close, so do not leave your start late.

## Steps

1. Open the entry link your lecturer shares. Enter your full name, your Google account email and your Student Registration Number, then press **Start test**. **Your 3 hours start now** and the timer cannot be paused.
2. Click **Open my test in Colab** and use the same Google account. Open your private notebook (`ML_PROJECT`).
3. Run the countdown cell (check your name, registration number and email), then the supplied setup cell. It loads the steel data; nothing is uploaded or downloaded.
4. Work from top to bottom. Replace each TODO. Keep function names and variable names exactly as printed. Use the self-check cells.
5. Fill the `MEMO` form (Task 8). Use the lists in the notebook for limits and next step.
6. Choose **Runtime, then Restart session and run all**. Fix any error. Choose **File, then Save**.
7. Allow **at least 20 minutes** to submit. Run the **Submit your test** cell, choose the same Google account, click **Submit test**, open the form link, check your details, confirm the declaration and press **Submit** before your personal deadline. Wait for the confirmation.

**Do not submit** a ZIP, CSV, PDF or a separate memo. The notebook button alone is not a submission: you must submit the form. Late forms are not graded.

Prepare with the rehearsal until the window opens. This guide does not open any form.
