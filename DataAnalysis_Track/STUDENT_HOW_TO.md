# Independent Data Analyst track — getting started

Use your DA learner ID from the class roster, not an IUEA Student Registration Number. Your identity remains the same across the track. The lecturer supplies the assignment dates; a draft guide does not mean the form is open.

## Accounts and files

1. Use your existing Google account for Colab and submission forms. If you do not have one, go to https://accounts.google.com, choose Create account and follow the personal-account prompts and verification. Use the email registered with the lecturer. Never share a password or verification code.
2. GitHub is only needed when the task asks for a repository. At https://github.com choose Sign up, complete the prompts and verify your email, or sign in to your existing account. A free account is sufficient. Create a private repository using + > New repository, enable Add README and create it. Use Add file > Upload files and Commit changes to save your work there. A repository is a project folder with saved history, not a submission form.
3. Download the lecturer's session files. A ZIP is a compressed folder: on Windows right-click > Extract All; on Mac double-click it in Finder. Work in the extracted folder, keeping raw data unchanged. Do not download a different version of the data to fix a mismatch.
4. Before starting, read the matching guide in student_guides/DA, or ASSIGNMENT_INSTRUCTIONS.md in the issued folder. It specifies the exact starting files and submission set.

## SQL in Session 5

Install DB Browser for SQLite from https://sqlitebrowser.org/dl/ for your operating system, or use the prepared installation. No SQL account or database server is needed. Open the app, choose Open Database, select the supplied riverside.db and choose Execute SQL. Type a query and use Execute to see its result table. Follow the SQL lab before the assessment.

Save the final query as a plain-text .sql file using the SQL editor's save command. Reopen it and run it against the issued database. Check that it did not acquire an extra .txt extension. Submit the query, not a screenshot of its output or the database itself. Read S05.md for the six required output columns and marking checks.

## Colab in Python sessions

1. Open https://colab.research.google.com. Choose File > Open notebook > Upload and select the assignment .ipynb. A notebook has code cells to execute and text cells to read or edit. Save your own copy with File > Save a copy in Drive.
2. Click Connect if needed. In the left Files sidebar click Upload and select the named CSV/database/helper files. This is different from opening the notebook. Check all filenames appear, including riverside.db when required. Upload again if a disconnected runtime loses its files.
3. Replace YOUR_ID inside STUDENT_ID with your own DA roster ID, keeping quotes. Keep COHORT="DA". Read each task, edit the answer cell and run it with Shift+Enter. Do not change required function names or supplied check code.
4. A function must return the requested value. Printing alone is not a substitute. Blank starter functions can fail checks until you complete them. Read the first error and fix it before continuing.
5. Double-click a text cell to write your reasoning. For S09, the cleaning log must be a separate DOCX/PDF, not only notebook comments. For S13, follow your chosen sector's published finding keys and units.
6. Choose Runtime > Restart session and then Run all. Check the outputs and any errors. Download using File > Download > Download .ipynb. Rename using your actual learner ID and session, such as your ID followed by _S09.ipynb. Reopen the downloaded file to check that it contains your final work.

## Reports and presentations

In Word or Google Docs create a blank document. Add your learner ID, session and title, then the headings specified by the brief. Explain your method, numerical evidence, interpretation and limitations. In Google Docs use File > Download > Microsoft Word (.docx) or PDF Document (.pdf). Reopen the export and check the text is selectable. A photo of a page is not a text report.

In PowerPoint or https://slides.google.com create your slides and add your narration in the Notes area below each slide. Export as PPTX (Google Slides: File > Download > Microsoft PowerPoint). Check the exported notes. Screenshots can illustrate results but must not replace required written explanations or S15CHECK lines.

## Power BI access before Session 14

Windows users obtain Power BI Desktop from https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop. Follow the installation prompts, open the app and check that you can load the supplied CSVs. Desktop is a Windows application; do not attempt to install it directly on macOS.

For a Mac, use the lecturer-provisioned browser workspace at https://app.powerbi.com only after testing its model-editing permissions with your authorised teaching account. Sign in with that account and verify you can open the designated semantic model (the shared tables and relationships). A personal Gmail sign-in does not provide those permissions. If access fails, arrange a prepared Windows lab machine before class. Do not buy a licence or start a trial to solve a classroom access problem.

Follow lab_powerbi.md to load five tables into one model, establish relationships, create measures and check totals. Save the editable PBIX or authorised report link as supporting work. Read S15.md for the accessible PPTX/DOCX/PDF evidence to upload; the form does not accept PBIX or ZIP. The S15 assessment remains closed until the full grading workflow is validated and dates are published.

## Submit and check confirmation

1. Open the matching session's student form from its assignment guide. Check its title and the exact Kampala closing time. Use the Google email on your roster and enter your DA learner ID.
2. Choose Add file > Upload. Select the complete file set in the brief. S05: one SQL file. S09: notebook and cleaning log. S13: notebook and report. S15: presentation with notes and any separate evidence document.
3. Wait until all filenames appear, then Submit. Keep the confirmation page and your local files. Attaching a file or saving a repository is not submission. Each file must be at most 10 MB.
4. A correction before the deadline must contain the complete set again; the latest on-time response replaces the earlier set. A form that is closed is not permission to use a different session's form. Contact the lecturer with the session and error, while keeping your work.

Official help: https://support.google.com/accounts/answer/27441 and https://research.google.com/colaboratory/faq.html
