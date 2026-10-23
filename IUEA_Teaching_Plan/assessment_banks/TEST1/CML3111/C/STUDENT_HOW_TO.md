# CML3111 TEST1 — Take-home practical test

Individual work • 100 marks • Up to three hours from **Start test**.

**Check your personal deadline on the official test entry page. Start only when ready to work.**
The timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the class closing time. Colab may still allow editing afterwards, but late work is not accepted for grading.

## 1. Open your own working copy
On the entry page, enter your full name, Google account email and Student Registration Number. Use that same Google account throughout. Click **Open my test in Colab**, and work in that private editable notebook. You do not need to make a copy. Click **Connect** if shown. To resume, use the entry link with the same email and Student Registration Number; it opens the same saved notebook without restarting the timer.

## 2. Load the data
Check the identity cell near the top. Tell your lecturer immediately if the details are wrong; do not change the supplied course, test or allocation settings. Run the identity cell using the triangle beside it. Then run **Load the supplied CSV and Python libraries**. In the issued notebook this creates `engineering_data.csv` automatically; no separate CSV upload is needed. Wait for the preview and row count. After a runtime reset, rerun these setup cells before your work. If using a backup notebook without an embedded CSV setup cell, upload your assigned `engineering_data.csv` through Colab's folder icon first.

## 3. Complete the questions
Work from top to bottom. Read each question, write your code in its code cell and run it. Keep supplied function names and required output formats unchanged. Use pandas as instructed. Complete the eight coding tasks using pandas, matplotlib and ordinary Python. There are no interpretation choices or written report. Save regularly using **File → Save**.

## 4. Submit — allow at least 20 minutes
1. Run your completed cells, check the results and save. Submit your completed work even if some questions are unfinished.
2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.
3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.
4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.
5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.

**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. Marks are calculated after the test. If you replace your submission, submit a complete new snapshot and its form before the same deadline.

## If something fails
Record the error and contact your lecturer immediately, before the deadline. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun setup; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.

No AI-generated solutions, collaboration, messaging or copied answers.

## Coding tasks and time plan
Setup: 10 minutes. Tasks 1–8: about 135 minutes. Check and save: 15 minutes. Submit: 20 minutes. Total: 180 minutes. These are planning estimates; your personal deadline is authoritative.

Use only pandas, matplotlib and ordinary Python. No modelling, scikit-learn, SQL, written report or multiple-choice answers. All 100 marks come from coding.

Each question has a supplied function header and a separate supplied run cell. Write your answer inside the function, indented by four spaces. The input argument contains rows from the CSV; the first supplied line converts these to a DataFrame. Do not change function names or returned dictionary keys. `return` sends your answer to the caller; `print` only displays it. The run cell calls the function with your dataset.

The grader also calls each function independently on other values with the same columns and cleaning rules. Use its input argument, not a global table or typed-in final answer. An unfinished cleaning function may prevent later demonstration cells running, but later functions can still earn marks independently. Submit partial work before the deadline.
