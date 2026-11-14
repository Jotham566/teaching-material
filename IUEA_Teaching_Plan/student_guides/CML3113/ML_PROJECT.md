# CML3113 ML_PROJECT: Engineering ML project (online, timed)

<!-- BLOCK_ASSESSMENT_20261103 -->
<!-- PROJECT_SITTING_20261104 -->
<!-- PROJECT_ONLINE_20261113 -->
<!-- PROJECT_CORE_20261114 -->
<!-- PROJECT_NO_SUBMIT_20261114 -->
**What it is:** the Engineering ML project is an INDIVIDUAL, TIMED, AUTO-GRADED test of 3 hours in Google Colab. It is worth 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40). There is no demo, no upload form and no take-home. It is built on the Weeks 1 to 8 core: cleaning, charts, the month split, three regression models with MAE and RMSE, and no leakage, plus a light warning question (Week 9) and the test set opened once (Week 10). There is no cross-validation, no cost table and no threshold choice in the project.

**When:** one online window for all three classes. It opens on **Monday 23 November 2026 at 00:00** Kampala time and closes on **Wednesday 25 November 2026 at 23:59**. You choose when to start. Your 3 hours (180 minutes) begin when you press **Start test** on the entry page, and they stop at the window's close if that comes first. **Start by Wednesday 25 November at 20:59** to get the full 3 hours. These dates are confirmed.

**Where:** online, from anywhere. You need your own laptop, your own Google account and a working internet connection for the whole 3 hours. There is no room and nobody watches you in person. There is no Submit button and no form: your notebook is your own file in Google Drive, it saves itself, and it is collected automatically at your deadline.

## The data

Every student in all three classes works on the same real file. There are no data variants. It is the "Steel Industry Energy Consumption" dataset from DAEWOO Steel in Gwangyang, South Korea: one reading every 15 minutes through 2018, 35,040 rows. Your client is the plant's energy manager. The file is built into the notebook, so you download nothing during the window.

Source: Sathishkumar V E, Changsun Shin, Yongyun Cho (2021). Steel Industry Energy Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C52G8C. Licence CC BY 4.0.

- **Question 1 (regression):** predict `Usage_kWh`, the energy used in each 15-minute reading, from the lagging and leading reactive power, `NSM` (seconds since midnight) and a weekend flag made from `WeekStatus`. The power factors and `CO2(tCO2)` are left out because they are calculated from `Usage_kWh`: using them would be target leakage. Errors are in kWh.
- **Question 2 (warnings):** a warning is a reading with `Usage_kWh` at or above 60 kWh, a high-demand quarter hour. You fit logistic regression for the probability of a warning, raise a warning when the probability is 0.5 or more (one fixed threshold), and report the confusion matrix counts, precision and recall.
- **Split by month:** training is January to August, validation is September to October, and the test set is November to December.

## What you do

The notebook has seven tasks:

1. Clean the rows and draw Chart 1.
2. Split the data by month.
3. Fit three models: a baseline, linear regression and a decision tree (each with median imputation learned from the training rows). Score them with MAE and RMSE and draw Chart 2.
4. Warnings: logistic regression probabilities, then the confusion matrix counts, precision and recall at the threshold 0.5.
5. Choose a model. Build `candidate_table` from your own validation MAEs and the supplied `LATENCY_MS`, then call the supplied `choose_model` cell. Do not edit that cell. The rule it applies: keep the models whose validation MAE is at most `MAX_MAE` and whose time is at most `MAX_MS`, then take the smallest validation MAE.
6. Open the test set once, with the supplied `open_test_set(chosen_model)` cell, after you have chosen your model.
7. Fill the Part B memo form (`MEMO`).

Work only in the notebook the entry page opens for you. Do not use "Save a copy in Drive". If you do, your work is still backed up and the setup cell shows a warning; go back to the entry page and click Resume.

You may add your own cells anywhere. Your work is marked wherever it is, as long as the required function names exist when the notebook runs from the top. Do not edit or delete the supplied cells.

## How it is marked

- **Part A: coded notebook, 30 marks.** A1 Clean the real data 7 (the date fix, the all-zero reading, CO2 removed, repeats and impossible values, your input left unchanged); A2 two labelled charts 2; A3 split by month 2; A4 baseline, linear regression and decision tree 6; A5 MAE and RMSE 3; A6 no leakage (imputation and the baseline mean fitted on the training rows only) 2; A7 the warning question 3 (probabilities 1; confusion matrix counts, precision and recall at 0.5: 2); A8 the test set opened once with the supplied cell, after your choice, and its result 2; A9 your results on the file 1, the same answer every time with `random_state=17` 1, and every required function and the MEMO form present 1. Your functions are run on rows you cannot see.
- **Part B: decision memo, 15 marks.** The memo is a form of fields inside the notebook: your recommended model 3, the validation MAE of the three models 3, the test MAE and test recall from your one opening 2, the improvement over the baseline (the baseline's validation MAE minus your model's, in kWh) 1, three limits chosen from a list 3, one next step chosen from a list 1, and two short written answers 2. It is marked automatically. Nothing is marked by hand.

**Results:** marks are final about a week after the window closes, by Wednesday 2 December 2026.

**Rehearsal (unmarked):** a practice notebook on the same steel file, with a different target (lagging reactive power, in kVarh) and its own warning, is released for the revision class on **Friday 20 November 2026**, where it is worked through live. It has the same seven tasks and short self-study notes before the tasks that need them, so you can do it alone if you missed the class. It uses the same steps as the project (Start, autosave, Check my work, I have finished), but nothing is locked or marked. A fully solved walk-through is not given: do the rehearsal yourself, with a 3-hour timer if you can. It is also a good way to check that your laptop, Google account and internet work.

## Rules

The rules are the same as in Practical Test 1. This is individual work. You may use your lecture slides, lab notebooks, revision guide, cheatsheet and your own notes. **No AI or outside help:** do not use Gemini, ChatGPT, Copilot or any other AI tool, and do not get answers from another person. When you submit, you confirm a declaration that the work is your own.

After the window, the lecturer may ask any student to an online call to explain part of their code or change it while the lecturer watches. This is the understanding check. Being asked does not mean you are suspected of anything. The copy checks and the identity checks still run on every submission. A short list of unusual cases (for example identical written answers or copied code) is checked by the lecturer; a flag alone never lowers a mark.

## Help during the window

- Questions about the wording of a task or about a technical problem: post them on the class channel. The lecturer answers from 08:00 to 20:00 each day of the window (these hours are for the lecturer to confirm). The lecturer will not write or debug your answers.
- If something fails (your laptop crashes, the internet goes down, the entry page or Colab breaks), report it on the class channel **at once**, with a screenshot. The lecturer can allow you one fresh attempt. It still ends at the window's close, so do not leave your start late.

## Steps

1. Open the entry link your lecturer shares. Type your registration number: the page checks it against your class list and shows your name. Tick **This is me**, enter your Google account email and press **Start**. **Your 3 hours start now** and the timer cannot be paused.
2. Click **Open my project in Colab**, signed in to that same Google account. It is your own notebook in Drive; Colab saves it as you work.
3. Run the countdown cell (check your name and registration number), then the supplied setup cell. It loads the steel data and starts an automatic backup every 5 minutes.
4. Work from top to bottom. Replace each TODO. Keep function names and variable names exactly as printed. Use the self-check cells. Press **Ctrl+S** now and then; the countdown reminds you 30 and 10 minutes before your deadline.
5. Fill the `MEMO` form (Task 7). Use the lists in the notebook for limits and next step.
6. Choose **Runtime, then Restart session and run all** and fix any error. On the entry page press **Check my work**: within a few minutes it shows whether your saved notebook runs from the top, whether every required function and the MEMO form are there, and whether it is the notebook issued to you. It never shows a mark.
7. There is **nothing to submit**. At your deadline your notebook becomes read only and your work is collected: the last version saved before the deadline, or the newest automatic backup if that is newer. If you finish early, press **I have finished** on the entry page.

If your laptop dies or Colab disconnects, open the entry page again and click Resume; your work up to the last save or backup is safe. **Do not** send a ZIP, CSV, PDF or a separate memo. Work done after your deadline is not marked.

Prepare with the rehearsal until the window opens.
