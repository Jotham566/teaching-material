# Continuous assessment marks

The private workbook is `private/IUEA_Continuous_Assessment.xlsx`.
It has one summary per programme, current marks, the receipt history and marking rules.
Do not share this workbook with the class: it contains students' private information.

## What the totals mean

- Quiz and assignment marks contribute 10 points each to the semester total.
- Data project: 10; Test 1: 15; Test 2: 20; ML project: 25; demo/reflection: 10.
- Best-of rules and the CML3112/CML3113 A6 and Quiz 6 waivers are retained.
- A blank is pending or not yet submitted, **not a zero**. A numeric zero is a completed mark.
- The total is earned semester points so far, not a final grade.
- “Source mark” retains a recorded score even when an identity conflict prevents it from entering a student's total.
- Names were not collected by the original assignment forms. They must come from a verified roster or test receipt; they are not guessed from email addresses.

## Updating after more submissions

1. Export a fresh private source snapshot using `startCAExport`, then `exportCANext` in the assignment Apps Script project. This copies submissions without changing forms or deadlines. The temporary export trigger removes itself on completion.
2. Confirm `inspectCAExportProgress` reports 15 quizzes and 15 assignments. Download that private Drive folder. Keep earlier snapshots.
3. Extract with `scripts/unpack_ca_export.py`. Check `download_check.json`: missing files and export errors need a retry, not a zero.
4. Refresh the three quiz response spreadsheets and assignment audit. Record the current quiz deadlines from the quiz project. Reconcile receipts with `scripts/reconcile_ca_sources.py`; never combine two copies of the same quiz.
5. Rebuild the ledger, grade new eligible notebooks using `grader/grade_ca_batch.py`, then rebuild the ledger with its `results.json`. The grader reuses unchanged results and rechecks changed submissions, checks or CSV data.
6. Rebuild the Excel workbook using `scripts/build_continuous_assessment.mjs`. Check pending statuses before using the totals. Do not edit calculated cells manually.

All paths above are relative to the repository root except `grader`, which is inside `IUEA_Teaching_Plan`.

## Written assessments

A1 requires a passing calibration of the local AI grader against authored examples.
A2 combines 14 coding marks and 6 written marks; coding alone is not a final A2 mark.
The current coding batch tool leaves these incomplete marks blank. Do not bypass calibration or convert a failed model run into a student zero.

On this Mac, run document extraction while Docker is available, then stop Docker before local AI grading. Running both together exhausts memory. `prepare_ca_written.py` saves verified text linked to each original attachment; image-only, damaged or unsupported files remain pending.

On macOS, the A1/A2 written grader now checks before each uncached submission that Docker Desktop has stopped. It requests a graceful shutdown if necessary and stops the batch if shutdown cannot be verified. Calibration uses the same check. Finish all Docker work first and do not reopen Docker during model inference. See `MAC_MINI_SETUP.md` for native Ollama settings and the separate 9B trial; existing production marks and model choices are not changed by downloading a candidate.

The validated queue is `grader/run_ca_written_queue.py`. It takes the reconciled source directory, ledger, coding results, prepared text and passing A1/A2 calibration reports. It saves each receipt separately and refreshes the workbook after every 20 processed records and at completion. Repeating the queue reuses only results that still match the source files, model, rubric and grader. Keep the Mac powered and awake; the queue does not use a cloud AI service.

Check `private/written_queue/queue_status.json`:

- `RUNNING`: written grading is still underway; the workbook is provisional.
- `COMPLETE`: the queue has finished, but identity, unreadable-file or inconsistent-judgement exceptions may still need resolution.
- `STOPPED`: inspect the private log and resolve the processing error before restarting. Unfinished work has not been assigned zero.

To resume the existing downloaded snapshot, double-click `Resume_Written_Grading.command`. Start the local model server first if it is not running. This command refuses a second concurrent queue; it does not export newly submitted work. Follow the refresh steps above for new submissions.

Before using marks, check **Current marks** for pending statuses and **Source mark** for marks held because of identity conflicts. Do not distribute the workbook to students.

## Identity and timing exceptions

The ledger reconciles punctuation variants within the same programme and Google account when no competing account uses that number. A single early digit typo can also be reconciled when at least three later receipts consistently use the dominant number, that family represents at least 75% of the account's receipts, and neither number belongs to another account. Original entries and the reason are retained. Similar numbers alone are not sufficient.
Remaining account/registration conflicts need verified identity evidence. Keep all original receipts and scores. `scripts/reconcile_ca_notebook_identity.py` also releases existing valid code checks when the notebook and form differ only in punctuation, spacing or case; it does not change the checker results.
Multiple accounts can share a student record when every account consistently uses that exact registration across at least two different assessments and none uses another registration in the programme. A single matching upload is not enough.

Summary statuses:

- **Current marks recorded**: no unresolved submitted receipts for this record in the imported snapshot. Future assessments can still be blank; this is not a final semester grade.
- **Submitted work pending**: one or more received submissions still need grading, a readable/correct file or a timing decision. The adjacent count is submissions awaiting resolution, not missing uploads.
- **Verify identity**: conflicting student details still prevent some marks from entering the total. Check the receipt-level status and retained source mark in **Current marks**.

Keep an immutable `private/grading_input.json` for each grading snapshot, using the original receipt identities. Grade results must continue to match those original identities; reconciliation happens only when building the cumulative ledger. Do not use the reconciled output ledger as the next grading input.

Reopening a form has previously overwritten older receipts' timing labels. An `EARLY` label must be checked against the earlier authorized window. Any timing correction needs its evidence recorded in the private timing file.

## Reviewing unresolved receipts

Open **Review needed** and filter by programme or issue. Each row includes the response ID, any held mark or coding component, related registration numbers/accounts, and links to the original uploaded files. Open those links while signed into the lecturer account that already has access. Links do not make student work public.

For **WRITTEN_REVIEW**, compare the two passes and processing detail with **Written rubrics** and the uploaded work. A disagreement is not a final mark. For file problems, inspect the linked original; unreadable work remains pending, not zero. For identity problems, verify the student against the receipt and related accounts before allocating a retained mark. Names that were not collected remain explicitly unavailable.

Keep any manual decisions separately with the response ID and reason. This workbook is generated and overwrites direct edits on refresh; approved decisions must be incorporated into the grading inputs before rebuilding totals. **Current marks recorded** means all received work for that record is resolved in the imported snapshot, not that all future assessments are complete.

The 21 October refresh is tracked in `private/refresh_status.json`. `COMPLETE` means automatic processing has finished; the review sheet can still contain unresolved cases. The old resume launcher refuses to replace results after this snapshot refresh.

## Tests and later projects

Use `continuous_assessment.py --test-ledger PATH` to add each trusted **production** test batch ledger. Entries explicitly marked `REHEARSAL` are excluded; never supply a rehearsal ledger whose synthetic entries are marked `GRADED`. Rebuilding replaces the calculated view without adding marks twice.
Project columns are reserved in the workbook; project marks must come from their validated grading process and source receipts. They are not automatically awarded by this early-assessment importer.

## Privacy

Source exports, uploaded work, identity mappings, feedback and marks belong under `private/`, which is ignored by Git.
Only grading code, synthetic tests and general instructions belong in the public repository.
