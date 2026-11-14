# Setting up collection and instant marking

Nothing has been set up yet. No repository, secret, token, script or Worker change exists. You do three things.

## 1. Run the script

From the repository root, on this Mac:

    bash IUEA_Teaching_Plan/second_half/Project/deploy/setup_pipeline.sh --dry-run     # read what it will do; it changes nothing
    bash IUEA_Teaching_Plan/second_half/Project/deploy/setup_pipeline.sh

It uses the tools already signed in here: `gh` (Jotham566), clasp and wrangler. You can run it again at any time; each step checks first. It:

- makes three secrets and keeps them in `~/.iuea_pipeline_secrets`, outside the repository;
- creates the private repository `iuea-ml-grading` and pushes the grader, hidden checks, sandbox and workflow (no student data);
- asks you once for the GitHub token: it opens a page with the form already filled in. Choose **Only select repositories**, pick `iuea-ml-grading`, check that **Contents** is **Read and write**, press **Generate token** and paste it into the Terminal;
- creates the collector web app `IUEA ML Project Submissions`, sets its properties, installs the every-minute deadline trigger, and sets the repository secrets;
- pushes the student portal and redeploys it at the same `/exec` address;
- sets the Worker secrets and deploys the gateway;
- runs a smoke test against the live pages with a made-up registration number, then builds the release notebooks.

## 2. Approve the Google consent screen

When the script stops at step 6, the collector opens in the Apps Script editor. Choose **authorizeMlProject**, press **Run**, approve the screen with your own Google account, then press Enter in the Terminal.

## 3. One Colab dry run

1. Load the class list. Export the roster from the gradebook as CSV and upload it to your Drive. In the collector editor run `loadClassListFromCsv("<file id>")`. If the CSV has no course column, give it: `loadClassListFromCsv("<file id>", "CML3112")`. The list stays in your workbook; nothing goes to the repository.
2. Open the rehearsal window for one course: `openMlProjectWindow('CML3112','<now>','<in 4 hours>','CONFIRMED','ML_REHEARSAL')`.
3. Open the rehearsal entry link. Type a registration number from the list, confirm the name, press Start, open the notebook in Colab, run the first cells and paste in a few solution cells. Wait 5 minutes. Then, on the entry page, press **Check my work** (the result appears within about three minutes) and **I have finished**.
4. Check that the notebook opened without the "Copy to Drive" banner, that the setup cell showed "Automatic backup sent", and that **Actions** in `iuea-ml-grading` shows the run.

## How it works

- **Start.** The portal copies the issued notebook into your Drive folder, names it by registration number and allocation, shares it with the student's Google email as an editor, and opens it in Colab. Colab saves to that file.
- **Backups.** Every 5 minutes the setup cell sends the notebook on screen to the collector. If the student is in another file (for example after "Save a copy"), the cell shows a warning and the backup still counts.
- **Deadline.** Every minute the trigger looks for attempts past their deadline (start plus 180 minutes, capped at the window close). For each one it makes the file read only, takes the newer of the last Drive save before the deadline and the last on-time backup, and sends it to GitHub Actions for marking. Backups that arrive late are kept and never used. The source and its time appear on the spot-check list; no action is needed.
- **Students** see Check my work and I have finished on the entry page. Marks stay hidden until you release them.
- **The rehearsal** works the same way, except that editing is never stopped and nothing is marked.

## One-line functions in the collector editor

| When | Run |
|---|---|
| 22 November | `openMlProjectWindow('ALL','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED')` |
| Extension, whole course or everyone | `extendMlProject('CML3113', 30, 'reason')` or `extendMlProject('ALL', 30, 'reason')`. The window close moves too. |
| Extension, one student | `extendMlProject('24/351/BSCE-S', 20, 'reason')`. If the work was already collected, editing is restored. |
| Technical failure, or the wrong Google account | `freshMlProjectAttempt('24/351/BSCE-S', 'reason', 'right.email@gmail.com')`. The student opens the entry link again. |
| A check did not run | `redispatchMlProject()` |
| After the window | `exportMlProjectBatch()`. Then on the Mac: `python3 actions/final_regrade.py --zip <batch> --roster Grades.csv` |
| Show the marks | `releaseMlProjectMarks("RELEASE")` (`hideMlProjectMarks()` hides them again) |

Every call is logged in the `Extensions` sheet. Never edit the sheets by hand.

## Minutes budget

Each collection or check costs about 2 to 3 billed minutes. About 250 students, one collection each plus two or three Check my work presses, comes to about 2,000 to 2,500 minutes. That is above the 2,000 free minutes a month for private repositories (GitHub Pro gives 3,000). Check my work is limited to one press every two minutes. Watch **Settings, Billing, Usage** on 24 November. If the minutes run out, collection still happens and nothing is lost: `redispatchMlProject()` catches up later, or the Mac run does everything.
