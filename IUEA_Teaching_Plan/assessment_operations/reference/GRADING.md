# Continuous assessment marks

Technical reference only. For setup use [Start here](../README.md); for new submissions use [Continue grading](../CONTINUE_GRADING.md). Paths below are relative to assessment_operations unless stated otherwise.

The private workbook is `private/IUEA_Continuous_Assessment.xlsx`.
It has one summary per programme, current marks, the receipt history and marking rules.
Do not share this workbook with the class: it contains students' private information.

## What the totals mean

- Quiz and assignment marks contribute 10 points each to the semester total.
- Data project: 10; Test 1: 15; Test 2: 20; ML project: 25; demo/reflection: 10.
- All three programmes waive A6 and Quiz 6, including previously completed CML3111 work. Use best 9 of 11 quizzes and best 7 of 10 weekly assignments. Separate weekly quizzes/assignments are not assigned in Weeks 7, 14 and 15; Test 1, Test 2, final project and demo retain their own marks and weights.
- A blank is pending or not yet submitted, **not a zero**. A numeric zero is a completed mark.
- The total is earned semester points so far, not a final grade.
- “Source mark” retains a recorded score even when an identity conflict prevents it from entering a student's total.
- Names were not collected by the original assignment forms. They must come from a verified roster or test receipt; they are not guessed from email addresses.

## Updating after more submissions

Use `./grade-submissions EXPORT.zip` from the teaching repository. It coordinates the stages below; do not run them separately for routine batches. Validated generations are stored under `private/batches/`, with the current generation recorded in `private/refresh_active.json`. The normal workbook path remains unchanged. Back up the entire private snapshot after completion.

The command preserves unchanged completed marks and held written-review decisions, merges receipts by response ID, saves older generations, and rebuilds totals. Changed attachment hashes trigger new checks. It retains existing test/project marks. `Grade_Tests.command` imports new production test results into the same cumulative generation automatically. Restoring or manually changing the active ledger outside this runner is detected and requires reconciliation before another refresh.

### Underlying stages (reference only)

1. In the assignment collection spreadsheet, choose **Export Grading ZIP → Start / resume export**. The menu queues a request; the existing exporter processes it automatically and checkpoints its progress. Its temporary work trigger removes itself on completion; the menu listener remains installed. Forms, marks and deadlines are unchanged.
2. Wait for **COMPLETE** in the collection workbook's **CA Export** tab; download the linked ZIP. It includes 15 assignment manifests, 15 quiz exports, original files, audit timing and quiz deadlines at a fixed cutoff.
3. The runner verifies `ca_bundle.json` inventory, sizes and SHA-256 hashes before extraction, then validates source receipts and original attachment hashes. Missing files and export errors stop import, not award zero.
4. Quiz marks come from saved response-sheet scores. Legacy receipts without a unique matching sheet row use existing recorded Form item scores, with a warning; missing scores remain pending. The quiz project mirrors its 15 current windows to the private collection workbook every 15 minutes and when links are saved. A stale/incomplete mirror blocks a new export. Previous window evidence is retained during import.
5. Rebuild the ledger, grade new eligible notebooks using `grader/grade_ca_batch.py`, then rebuild the ledger with its `results.json`. The grader reuses unchanged results and rechecks changed submissions, checks or CSV data.
6. Rebuild the Excel workbook using `scripts/build_continuous_assessment.mjs`. Check pending statuses before using the totals. Do not edit calculated cells manually.

All paths above are relative to the repository root except `grader`, which is inside `IUEA_Teaching_Plan`.

Legacy download folders containing the submissions ZIP plus four source XLSX files are still accepted for older snapshots; they are no longer required for new exports.

## Written assessments

A1 requires a passing calibration of the local AI grader against authored examples.
A2 combines 14 coding marks and 6 written marks; coding alone is not a final A2 mark.
The current coding batch tool leaves these incomplete marks blank. Do not bypass calibration or convert a failed model run into a student zero.

On this Mac, run document extraction while Docker is available, then stop Docker before local AI grading. Running both together exhausts memory. `prepare_ca_written.py` saves verified text linked to each original attachment; image-only, damaged or unsupported files remain pending.

On macOS, the A1/A2 written grader now checks before each uncached submission that Docker Desktop has stopped. It requests a graceful shutdown if necessary and stops the batch if shutdown cannot be verified. Calibration uses the same check. Finish all Docker work first and do not reopen Docker during model inference. See [the Mac reference](MAC_MINI.md) for native Ollama settings and the separate 9B trial; existing production marks and model choices are not changed by downloading a candidate.

The validated queue is `grader/run_ca_written_queue.py`. It takes the reconciled source directory, ledger, coding results, prepared text and passing A1/A2 calibration reports. It saves each receipt separately and refreshes the workbook after every 20 processed records and at completion. Repeating the queue reuses only results that still match the source files, model, rubric and grader. Keep the Mac powered and awake; the queue does not use a cloud AI service.

Check `private/written_queue/queue_status.json`:

- `RUNNING`: written grading is still underway; the workbook is provisional.
- `COMPLETE`: the queue has finished, but identity, unreadable-file or inconsistent-judgement exceptions may still need resolution.
- `STOPPED`: inspect the private log and resolve the processing error before restarting. Unfinished work has not been assigned zero.

For a current batch that was interrupted, rerun the same `grade-submissions` command with the same ZIP. It reuses valid checkpoints. `Resume_Written_Grading.command` belongs to the older snapshot workflow and is not the routine resume command; do not run it alongside or instead of the current runner.

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

Use `Grade_Tests.command` for production test ZIPs. After grading, it automatically rebuilds and validates the cumulative workbook, preserving coursework, project marks and previous attempts. Both workbooks open on success. Repeating the command reuses saved test attempts and does not duplicate marks. If publication fails, fix the reported issue and repeat it; test results remain saved. Close Excel and finish any interrupted weekly batch first.

Developer/rehearsal runs using `--out` outside the standard production folder do not update cumulative marks unless an explicit `--ca-private` directory is supplied. `--no-workbook` skips cumulative publication. Entries explicitly marked `REHEARSAL` are excluded; synthetic records labelled `GRADED` must remain in isolated rehearsal output directories. The low-level `continuous_assessment.py --test-ledger` option is not the routine workflow: it bypasses the refresh publication journal.
Project columns are reserved in the workbook; project marks must come from their validated grading process and source receipts. They are not automatically awarded by this early-assessment importer.

## Privacy

Source exports, uploaded work, identity mappings, feedback and marks belong under `private/`, which is ignored by Git.
Only grading code, synthetic tests and general instructions belong in the public repository.

### Spreadsheet export menu maintenance

`assessment_operations/ca_export_menu.gs` is bound to the collection spreadsheet (project **IUEA Grading ZIP Menu**). Its `onOpen` adds **Export Grading ZIP**; it uses only the current spreadsheet. Requests occupy `CA Export!D1:E3`, separate from export progress in `A1:B5`. Do not edit these request cells manually.

The existing standalone assignment project runs `installCAExportMenuListener` once to install one minute-based `processCAExportRequest` trigger. Programmatic sheet writes do not fire edit triggers. The listener queues the existing checkpointed exporter, preserves schedules and submissions, and records request IDs to prevent a completed request being replayed as a fresh export. Routine use requires no Apps Script editor.
