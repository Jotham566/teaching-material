# Deploying the project sitting on the Test 1 machinery (4 November 2026)

Nothing live has been changed. Every file in this folder is a patched COPY of the live file, or a new file. The live files in `test_portal/` and `grader/` are untouched, so you can compare each copy with its original (`diff`) before you paste it. All times are Kampala. All sitting times are proposed; the lecturer confirms them.

## How Test 1 enforces time, and what the project reuses unchanged

| Question | Answer (read from `Portal.gs`, `exam_collection.gs`, `colab_submit_cell.py`) |
|---|---|
| Where is the limit set? | The row of the `Test windows` sheet: `assessment_key`, `opens_at`, `closes_at`, `enabled`, and column E `duration_minutes` (180). A row with a duration makes the test timed. |
| Who starts the clock? | The student, by pressing Start test on the entry page. The portal then saves `started_at` and `personal_deadline` in the `Test allocations` sheet. |
| What is the personal deadline? | The earlier of `started_at` plus 180 minutes and `closes_at`. A student who starts late has only the time left until `closes_at`. Refreshing, a new device or reopening Colab returns the same notebook and the same deadline. |
| What happens in the notebook? | The first cell shows a countdown (a reminder from the device clock). The last cell holds `_IUEA_DEADLINE`; the Submit test cell refuses to run after it and switches its button off. |
| What happens at the end? | The server refuses the entry page after the personal deadline. A form response stamped after the personal deadline becomes `OUTSIDE_PERSONAL_WINDOW`, one after `closes_at` becomes `OUTSIDE_WINDOW`; neither is exported for grading. Colab cannot be locked remotely: a student can still type, and nothing typed after the deadline reaches the grader. |
| One attempt | One accepted submission per Google email and registration number. A technical retry is `authoriseFreshTestAttemptForRegistration(registration, reason)` in the collector; the retry is still capped at `closes_at`. |

The project reuses all of this. The only code changes are listed below, each with the match count its patch asserted.

## What was patched (and why)

| File in this folder | Based on | Change |
|---|---|---|
| `Portal.gs` | `test_portal/Portal.gs` | The key pattern accepts `ML_PROJECT` (2 places); the packet lookup falls back to `PORTAL_PACKETS_ML`; the issued notebook gets the project instructions (`portalMlInstructions_`, new function at the end). Nothing else. |
| `PacketsMLProject.gs` | new, generated | `var PORTAL_PACKETS_ML`: 9 packets (3 cohorts by variants A, B, C). Student files only. No answer keys. |
| `Index.html` | `test_portal/Index.html` | Heading, the sitting time for the three keys, project wording for the data step. Test 1 and Test 2 pages are unchanged in behaviour. |
| `gateway/page.mjs`, `gateway/worker.mjs` | `test_portal/gateway/` | The page regenerated with the same transformation as `scripts/build_test_gateway.py`; the worker's key pattern accepts `ML_PROJECT`. |
| `exam_collection.gs` | `grader/exam_collection.gs` | The key pattern of `authoriseFreshTestAttempt` accepts `ML_PROJECT`; the form text says TIMED PROJECT SITTING for project forms. Nothing else. |
| `test_monitor.gs` | `grader/test_monitor.gs` | The monitor lists `ML_PROJECT` rows. |
| `ml_project_collection.gs` | new | `installMlProjectCollection()` creates the three forms (closed) and the three `Test windows` rows (enabled NO, duration 180); `showMlProjectWindows()` (read only); `setMlProjectWindow(cohort, opens, closes, 'CONFIRMED')`. |
| `Test_windows_rows.csv` | new | The three proposed rows, ready to type. |
| `ML_PROJECT_ENTRY_LINKS.md`, `qr/` | new | The three entry links and QR codes on the existing Cloudflare host. |
| `test_ml_project_portal.cjs` | new | The offline proof (run it before and after you paste anything). |

`Gateway.gs` needs no change (its safe-message pattern already matches the portal's messages).

## Before anything: two checks only you can do

1. **Real scikit-learn.** On your Mac: `pip install scikit-learn`, then run `python3 IUEA_Teaching_Plan/second_half/Project/grader_spec/run_proofs.py --cohorts CML3112` with the stand-in removed from the path (remove `second_half/Build/ref` from `PYTHONPATH` in `grader_spec/offline_harness.py`, or run the Docker route below). Every case should be PASS. If a tree or logistic value differs in a late digit, send me the case name before the notebooks go out.
2. **Real Colab.** Open `Rehearsal/<cohort>/ML_PROJECT_rehearsal.ipynb` and `grader_spec/solutions/<cohort>/A/ML_PROJECT_solution.ipynb` in Colab, Restart session and run all. The solution should finish with no error and every line of both self-check cells should read PASS. Compare Part A numbers with `second_half/Project/grader_spec/proof_results.txt`.

## Steps, in order

1. **Collector project** (the lecturer-owned Apps Script project that holds `Colab_Test_Collection.gs`). Keep a copy of the current files first.
   1. Open the file that holds `exam_collection.gs`, select all, paste `deploy/exam_collection.gs`, Save.
   2. Add a new file `ml_project_collection` and paste `deploy/ml_project_collection.gs`. Save.
   3. Open `Test_Monitor.gs`, select all, paste `deploy/test_monitor.gs`. Save.
   4. Run `installMlProjectCollection()` once. Expect two lines: `Created forms: CML3111|ML_PROJECT, CML3112|ML_PROJECT, CML3113|ML_PROJECT. Every Test windows row is enabled NO. Nothing was opened.` and a long line starting `PUBLIC_NOTEBOOK_CONFIG`. A second run creates nothing.
   5. Copy the three `...|ML_PROJECT` entries from that `PUBLIC_NOTEBOOK_CONFIG` line into `data/colab_test_submission_config.json` under `forms` (keep the five item names exactly: Full name, Student Registration Number, Variant, Snapshot file ID, Snapshot SHA-256). Alternatively copy `tools/project_forms.template.json` to `tools/project_forms.json` and fill it.
   6. Run `showMlProjectWindows()`. You should see three rows with empty times, `enabled NO` and `minutes 180`.
2. **Rebuild the notebooks with the real forms** (on the Mac, from `second_half/Project/`):
   `python3 tools/build_grader_spec.py` (only if you changed anything), `python3 tools/build_project_notebooks.py --require-forms`, `python3 tools/build_deploy_bundle.py`, then `node deploy/test_ml_project_portal.cjs`. Expect `PASS ML_PROJECT deployment bundle`. The `--require-forms` build removes the DRAFT banner; without it the notebooks refuse to be handed out.
3. **Student portal project** (the SEPARATE Apps Script project `IUEA Student Test Entry`; never the collector).
   1. `Portal.gs`: select all, paste `deploy/Portal.gs`, Save. `Index.html`: paste `deploy/Index.html`.
   2. Add a new file `PacketsMLProject` and paste `deploy/PacketsMLProject.gs` (the file order does not matter: the portal reads `PORTAL_PACKETS_ML` only when a request arrives).
   3. Deploy, Manage deployments, edit the existing web app deployment, New version. Keep execution as the lecturer and access Anyone, and keep the `/exec` URL.
4. **Cloudflare gateway.** Copy `deploy/gateway/worker.mjs` and `deploy/gateway/page.mjs` over the files in `test_portal/gateway/` and deploy as before (`gateway/README.md`, steps 4 and 5). The Worker secret and `APPS_SCRIPT_URL` do not change.
5. **Links and QR codes.** `deploy/ML_PROJECT_ENTRY_LINKS.md` and `deploy/qr/` hold the three links and images. Check that the page for each opens and says `not open yet` (the rows are still disabled). Do not open a window to test: use a rehearsal registration and the rehearsal window procedure in `test_operations/TEST_CHECKLIST.md`.
6. **Dry run** (D minus 3 days): in `Test windows` set one cohort's row to a 30 minute window ending in 30 minutes (`2026-12-..T..+03:00`), enabled YES, run `syncColabExams`, then as the rehearsal account: enter the page with registration `DEMO / ML 1`, press Start, finish the solution notebook (paste the model solution cells), Submit test, press Submit on the form. Export Test ZIP, run `grade_project.py --zip`, check the row, mark the collection row REHEARSAL.
7. **Windows.** After you confirm the times in writing to the class: `setMlProjectWindow('CML3112','2026-12-01T11:00:00+03:00','2026-12-01T14:00:00+03:00','CONFIRMED')` and the same for the other two (CML3113 `2026-12-04T08:00:00+03:00` to `2026-12-04T11:00:00+03:00`; CML3111 `2026-12-04T11:00:00+03:00` to `2026-12-04T14:00:00+03:00`), then `syncColabExams`. Or type the rows from `Test_windows_rows.csv` yourself with `enabled` YES. The function refuses a window longer than 3 hours 15 minutes.
8. **After each sitting**: see section 3 of `Lecturer_Marking_Guide.pdf`.

## Rehearsal release (after Class 4)

The rehearsal needs no portal, no form and no timer. Send each cohort its folder `Rehearsal/<cohort>/` (the notebook and `engineering_data_practice.csv`; the notebook already embeds the data, so the CSV is a backup) the same way you send class packs. CML3112: Tuesday 24 November. CML3113 and CML3111: Friday 27 November (proposed).

## Rollback

Every change above is a paste of a whole file. To roll back, paste the original file (kept as the copy you made in step 1) and publish a new version. Nothing in `data/`, the Test 1 packets or the Test windows rows for TEST1 and TEST2 is changed by these steps.
