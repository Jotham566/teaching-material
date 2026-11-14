# Deploying the ML project collection (updated 14 November 2026)

Nothing live has been changed. Every file in this folder is a patched copy of a live file, or a new file. All times are Kampala. The window is confirmed: 23 November 2026, 00:00 to 25 November 2026, 23:59, the same for all three courses, 180 minutes per student from Start.

## The set-up

Run `deploy/setup_pipeline.sh` (first with `--dry-run`). The steps it takes, and the two things you do by hand, are in `SETUP_GITHUB_ACTIONS.md`. The script is safe to run again.

## How the time limit and the collection work

| Question | Answer |
|---|---|
| Where is the limit set? | The `Test windows` row: `opens_at`, `closes_at`, `enabled`, and `duration_minutes` (180). `openMlProjectWindow` in the collector sets it. |
| Who starts the clock? | The student, by pressing Start on the entry page after the registration number is found on the class list and the name is confirmed. The portal saves `started_at` and `personal_deadline` (start plus 180 minutes, capped at `closes_at`). |
| What is issued? | A copy of the notebook in your Drive folder, named by registration and allocation, shared with the student's Google email as an editor, opened in Colab. Returning to the page gives the same file and the same deadline. |
| Is there a Submit step? | No. Colab saves to the shared file. The setup cell also sends a backup every 5 minutes. |
| What happens at the deadline? | The collector's every-minute trigger makes the file read only and collects the newer of the last Drive save at or before the deadline (Drive's modifiedTime) and the last backup received before the deadline. The source and its time go on the Collection row and the spot-check list. It then asks GitHub Actions to mark it. |
| Late work | Backups after the deadline are kept and never used. Work in a copy after the deadline never reaches the grader. |
| Finishing early | "I have finished" on the entry page does the deadline step at once. |
| Failures | `freshMlProjectAttempt(registration, reason, email)` gives a fresh attempt (also for a wrong Google account). `extendMlProject(who, minutes, reason)` extends one student, one course or everyone; the window close moves for a course or everyone. Both are logged; never edit the sheets by hand. |

## What was patched (and why)

| File in this folder | Based on | Change |
|---|---|---|
| `Portal.gs` | `test_portal/Portal.gs` | Accepts `ML_PROJECT` and `ML_REHEARSAL`; the class list decides the name and registration; the identity cell gets the allocation code; the Drive copy is named by registration and allocation; the countdown has Ctrl+S reminders at 30 and 10 minutes; the entry page gets the allocation code; the rehearsal is never closed by its timer. |
| `Gateway.gs` | `test_portal/Gateway.gs` | Also answers the class-list check. |
| `PacketsMLProject.gs` | new, generated | The project and rehearsal notebooks for the 18 packet keys (3 courses, 2 kinds, 3 allocation labels) and the data block once. Student files only. |
| `Index.html`, `ProjectIndex.html` | `test_portal/Index.html`, new | The project entry page: the registration checked as it is typed, the name to confirm, Check my work, I have finished, the status. |
| `gateway/worker.mjs`, `page.mjs`, `project_page.mjs` | `test_portal/gateway/` | Routes `/api/check`, `/api/backup`, `/api/mywork`, `/api/finish`, `/api/status`. |
| `ml_project_pipeline.gs` | new | The collector web app (a separate Apps Script project): backups, the deadline trigger, collection, Check my work, status, the release switch, extensions, fresh attempts, the class list loader, the batch export. |
| `clasp/collector.appsscript.json` | new | Its manifest (Drive advanced service v3, web app as you, access Anyone). |
| `setup_pipeline.sh` | new | The set-up script. |
| `exam_collection.gs`, `test_monitor.gs`, `ml_project_collection.gs` | `grader/` and new | Kept for Test 1. The project no longer needs them. |
| `test_ml_project_portal.cjs` | new | The offline proof of the portal bundle. The full proof is `actions/test_actions_e2e.py`. |

## Before anything: two checks only you can do

1. **The Colab-matching sandbox.** Built on 13 November 2026: `docker build -t iuea-notebooks:colab-2026.11 sandbox`. Re-read Colab's version list (`sandbox/colab_versions.json`) on 20 November and rebuild if a version moved.
2. **Real Colab.** The Colab dry run in `SETUP_GITHUB_ACTIONS.md` (section 3). Check especially that the notebook opens without the "Copy to Drive" banner and that the setup cell shows "Automatic backup sent".

## Window

On 22 November, in the collector editor: `openMlProjectWindow('ALL','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED')`. For the rehearsal on the revision class day: `openMlProjectWindow('CML3112','2026-11-17T08:00:00+03:00','2026-11-22T23:59:00+03:00','CONFIRMED','ML_REHEARSAL')`, and the same for CML3113 and CML3111 on 20 November.

## Rehearsal release

Share the rehearsal entry links (`?test=<course>|ML_REHEARSAL` on the same host). Students practise Start, autosave, Check my work and I have finished. Nothing is locked or marked.

## After the window

`exportMlProjectBatch()` in the collector, then on the Mac `python3 actions/final_regrade.py --zip <batch> --roster Grades.csv`. Then `releaseMlProjectMarks("RELEASE")`.

## Rollback

Each change is a whole-file paste or a new project. To roll back the portal, push the previous files and redeploy the same deployment; the collector can simply be left disabled (`hideMlProjectMarks`, and delete its trigger).
