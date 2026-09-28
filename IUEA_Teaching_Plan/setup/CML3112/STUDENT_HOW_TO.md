# Student setup and assignment guide

For CML3111, CML3112 and CML3113. Start here even if you have never written code. This guide explains the tools and the submission process; your assignment notebook contains the questions.

## 1 Prepare your accounts before class

A Google account lets you use Colab and the upload form. Colab runs Python in a web browser. A GitHub account stores copies of your work in a repository, which is a project folder with a history of saved changes. These are two different services.

1. If you already use Gmail, use that Google account. Otherwise open https://accounts.google.com, select Create account, choose personal use and follow the name, email, password and verification prompts. You may use an existing email address when offered. Do not create a second account unnecessarily.
2. Sign in at https://colab.research.google.com. Check the profile icon shows the email registered with your lecturer. If the class roster has a different email, tell the lecturer before submitting. Never send anyone your password or verification code.
3. Open https://github.com and select Sign up. Follow the email, password, username and verification steps. Open your email inbox and complete GitHub's verification. If you already have an account, sign in instead. A free account is sufficient.
4. Keep your usernames and recovery details somewhere you can retrieve them. Check you can sign out and sign back in yourself. If verification fails, check spam and request a new code; ask for help if still blocked.

**Ready check:** Colab opens under your own Google account and GitHub shows your profile. You do not need to install Python, Git or a paid AI tool for Week 2.

## 2 Download and extract the right student ZIP

1. Download the ZIP shared by the lecturer for YOUR cohort and week. CML3111, CML3112 and CML3113 use different practical data. A ZIP is a compressed folder; extract it before opening its files.
2. On Windows, find it in Downloads, right-click and choose Extract All, then Extract. On a Mac, double-click the ZIP in Finder. Open the resulting ordinary folder.
3. Keep a separate folder for each week. Do not mix Week 2's four-row CSV with Week 4's larger file even when their names match.
4. Open 00_START_HERE.txt. Open .md instruction files with Notepad on Windows or TextEdit on Mac; they are plain text. Before class, prepare accounts and files; complete exercises as the lecturer introduces them.

Use a laptop or a prepared lab computer for coding. A phone can open links but makes file editing and checking difficult. If you lack a working computer or internet, tell the lecturer before class so a lab arrangement can be made.

---PAGE---

# Opening and running a notebook

## 3 Open the notebook and upload its data

A notebook (.ipynb) contains text and code in separate blocks called cells. A CSV (.csv) is a table stored as text. The runtime is the temporary computer Colab uses to run your code.

1. Go to https://colab.research.google.com. Choose File > Open notebook, then Upload. Choose proof_of_life.ipynb for A2. In later weeks choose the assignment notebook named in ASSIGNMENT_INSTRUCTIONS.txt.
2. Use File > Save a copy in Drive to keep your own editable working copy. This saves a notebook to your Google Drive; it does not submit the assignment.
3. Click Connect if needed. Select the folder icon in the left sidebar to open Files. Click its Upload button and choose the CSV from the SAME extracted weekly folder. For weeks with helper .py files, upload those too. A helper is supplied code the notebook imports; do not edit it.
4. Check the exact filenames appear in Files, including their extensions. Uploading a CSV through File > Open notebook is the wrong route: that dialog is for .ipynb files.
5. Find STUDENT_ID in the first code cell. Replace only YOUR_ID, keeping the quotation marks, with your own Student Registration Number exactly as on your university record. Keep any slashes here. Check COHORT matches your course code.

## 4 Run and edit cells in order

1. Click inside a code cell, then press Shift+Enter or its triangular Run button. Read the output below it before moving to the next cell.
2. A text cell gives instructions or holds your written answer. Double-click it to edit; write your own explanation and click outside it to finish. Do not type an explanation into a code cell unless it is a Python comment.
3. For A2, follow the main notebook first. Open 01, 02, 03 and 04 only when the lecturer directs the error-repair practice. These files are deliberately broken. Keep your repairs for practice; none is a required upload. hello_engineering.py is an optional demonstration, also not an upload.
4. Return to proof_of_life.ipynb and write your own answer after My explanation: and keep that prefix. Describe what changed when you repeated the increment cell and what a fresh ordered run does.
5. Choose Runtime > Restart session, then Runtime > Run all (or the combined restart-and-run-all command if shown). A restart clears remembered variable values. If the runtime was deleted or reconnected, upload the data again when missing.

**A2 ready check:** the fresh run completes without a red error; proof_sum is 4, readings is 17, and rows contains the four records from your cohort CSV. Explain your observation rather than just copying those numbers.

---PAGE---

# Saving A2 and creating its repository

## 5 Download your completed notebook

1. In Colab choose File > Download > Download .ipynb. Find the file in your computer's Downloads folder. A saved Drive copy and a downloaded file are different copies; download again after your final edit.
2. Rename the downloaded file using your own registration number, replacing slashes with underscores, followed by _W02.ipynb. STUDENT_ID_W02.ipynb is a naming instruction, not a name to copy literally. Leave the identity inside the notebook unchanged.
3. Show file extensions in your file manager if needed. Check it ends in .ipynb, not .ipynb.txt, .html or .pdf. Reopen the downloaded notebook through Colab's Upload tab to check it is your completed version.

## 6 Create a private repository on GitHub

Use this browser route for A2. You do not need to connect Colab to GitHub or use terminal commands.

1. Sign in at https://github.com. Select the + menu, then New repository. Name it iuea-week02. This name is a project label, not your registration number.
2. Select Private because the notebook contains your registration number. Turn Add README on, then Create repository. A private repository is visible to you and people you explicitly grant access to. The automated A2 grader uses the uploaded files, so making it public is unnecessary.
3. In the new repository select Add file > Upload files. Choose your completed renamed notebook and the supplied Week 2 CSV. Do not upload the whole ZIP, the supplied instruction README or passwords.
4. Enter a short commit message such as Add Week 2 notebook and data. Save with Commit changes, using the current main branch for this individual exercise. A commit records a saved version. If offered a new branch instead, complete its pull request and merge so the files appear on the main repository page.
5. Check both filenames appear in the repository's main file list. Click the notebook to check you uploaded the completed version. Copy the repository page address from your browser for the form's Repository URL field.

**Ready check:** the repository contains your completed notebook, your cohort's four-row CSV and a README.md that you will complete next. A repository URL alone is not an assignment submission.

---PAGE---

# Writing your own README and submitting A2

## 7 Write and download README md

A README is a short instruction file for the next person opening your work. Markdown (.md) is plain text with optional formatting such as # for a heading. The instruction README in the ZIP is not your answer.

1. In your GitHub repository click README.md, then the pencil/Edit button. Replace the default text with your own short instructions. Include all three sections below; fill them with YOUR programme and filenames.
2. Programme: state the engineering programme you study and your cohort code.
3. Files: list your completed notebook and CSV by their exact filenames, and explain what each contains. Mention README.md as the run instructions.
4. How to run: explain how to open the notebook in Colab, upload the named CSV through Files, restart the session and run all cells from top to bottom. State the expected A2 checks and that the explanation is inside the notebook.
5. Click Commit changes and save. Open README.md again and check the saved text is yours.
6. Use Download raw file (the download icon in the file toolbar). If only Raw is shown, open it and save the raw text as README.md. Avoid saving the formatted GitHub webpage as HTML. Check your downloaded file is named README.md, not README.md.txt or README.md.html. Open it in a text editor and read it before uploading.

## 8 Upload both files in one response

1. Open SUBMIT_HERE.txt in your cohort ZIP and follow its student form link. Check the title says YOUR cohort and A2 / Week 2. Read the exact closing date and time in Kampala time.
2. Sign in with the Google email on the class roster. Enter your own Student Registration Number in the required freeform field. It is not a sample number. Leave Team ID blank for individual A2 work.
3. Paste the repository URL. In the file-upload question choose Add file, choose the Upload tab and select your renamed notebook AND your own README.md. Wait until both filenames appear.
4. Recheck the two filenames, then click Submit. Merely attaching files does not submit them. Wait for the confirmation page and keep a screenshot or receipt if offered. Do not assume an email receipt will always arrive.
5. Keep the two submitted files locally. If correcting work before the deadline, submit the complete two-file set again; the latest on-time response replaces the earlier set.

**Final check:** two uploaded files, one repository URL, correct identity, confirmation received. The CSV belongs in your repository and runtime, not in the A2 form. Do not upload repairs 01–04, guided_practice.ipynb, hello_engineering.py or the ZIP.

---PAGE---

# Week 1 catch up and written reports

## 9 Complete four separate tasks during Week 2

A1 is the Week 1 report. Quiz 1 tests Week 1. A2 is the Week 2 notebook and README. Quiz 2 tests Week 2. Completing one does not complete the others. WEEK1_CATCHUP.txt gives the Week 1 links; SUBMIT_HERE.txt gives A2. The lecturer shares the quiz links and announces their closing times.

Each quiz is open for 24 hours from its own lecturer activation. It is not 24 hours from when you open the link. Assignment closing times are separate; use the exact date shown on the form. A1 catch-up uses the same deadline as your cohort's A2.

## 10 Write A1 without needing to code

1. Open Word and create a blank document, or go to https://docs.google.com/document using your Google account and choose Blank. Name it with your own registration number (slashes changed to underscores) followed by _W01.
2. At the top write your Student Registration Number, engineering programme, cohort code and A1 title. Add headings Problem 1, Problem 2, Problem 3 and My selected problem and dataset.
3. For each problem describe a specific engineering decision. State what quantity or category you would want to estimate, and why machine learning would or would not help. A feature is information used as an input; a target is the result to predict. Identify plausible inputs, a target when appropriate, a possible data source and a limitation.
4. Choose one of the three problems. Explain why the proposed dataset could answer that question and what it cannot establish. A source is where data would come from; a limitation is a reason the data may not support a strong conclusion. You do not need to train a model for A1.
5. Read your own report against those headings. Remove unfilled placeholders. Save as DOCX, or export a PDF whose text you can select. In Google Docs use File > Download > Microsoft Word (.docx) or PDF Document (.pdf). Reopen the downloaded file to check it.
6. Open the A1 form for your cohort from WEEK1_CATCHUP.txt. Upload your report there, separately from A2. Complete the identity fields and Submit; keep confirmation.

DOCX is the simplest A1 route. If you choose the accepted PPTX alternative, put your full explanations in slide text or speaker notes; pictures alone are insufficient. If you choose a notebook, put the report in text cells. Submit one complete version, not several competing drafts.

For later report assignments, use the required headings in their brief. Explain the question, method, result with units, interpretation and limitation. A chart needs a readable caption stating its finding. Preserve the original data and label supplied scenarios separately from results you measured.

---PAGE---

# Later assignments and solving common problems

## 11 Follow each assignment in order

1. Read ASSIGNMENT_INSTRUCTIONS.txt in the weekly folder before coding. It names the starting notebook, required input files and exact upload set. Guided practice follows the lecture; the assignment notebook is your assessed work.
2. Read each task's text, edit its Your answer here cell, then run that cell and its visible check if provided. Keep the given variable and function names: the grader looks for them. A function must return the requested value; printing it alone is not a replacement for return.
3. A blank starter may fail checks or raise NotImplementedError until you implement it. Read the first error, find its cell and correct your work. Do not delete checks, change expected values or paste answers into the helper files. Passing visible checks is useful feedback, not a guarantee of full marks.
4. For weeks with My written evidence, double-click that text cell and write your reasoning there, keeping its heading. Code comments and copied task prompts do not replace your explanation. Use the published marking criteria to check coverage.
5. Restart, run all, download the final version and reopen it. Use that week's suffix in the filename. Follow the exact upload list in the brief; most weekly assignments after A2 require only one notebook.

## 12 If something goes wrong

- FileNotFoundError: check Files contains the exact CSV name from this week's folder, including capitals. Upload it again after a disconnected or deleted runtime. Do not use a different week's dataset to make the error disappear.
- No module named iuea_grader or spec_W03: upload the supplied helper .py files through Files, then rerun the notebook from the top. Do not search for an unrelated package to install.
- NameError: a value may not yet have been defined. Read earlier cells and run in order. SyntaxError: check spelling, quotes, brackets, colons and indentation against the taught example.
- You cannot upload: check the Google account, file types and file size. The form allows up to 10 MB per file. A2 needs .ipynb and .md; a screenshot or Drive shortcut is not either file.
- The form is closed: reread the published window, keep your work and notify the lecturer promptly with the cohort, assignment and error. An upload problem does not automatically extend a deadline. Never put work in a different assignment form.
- Wrong email or registration number: contact the lecturer to correct the roster/response. Do not invent another identity to bypass an error. The IUEA registration field is required and accepts freeform text.

Before offline tests, practise on the designated lab computer. No online sign-in, internet or AI is used during those tests; follow the invigilator's collection instructions.

## Official tool help

Google account: https://support.google.com/accounts/answer/27441
Colab: https://research.google.com/colaboratory/faq.html
GitHub repository: https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories
GitHub uploads: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
