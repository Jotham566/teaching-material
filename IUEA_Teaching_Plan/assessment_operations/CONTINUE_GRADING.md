# New submissions: repeat checklist

Use this when more students submit quizzes or assignments. Process batches whenever convenient; you do not need to wait for everyone.

**Current scope: Quizzes 1–5 and Assignments A1–A5 across all three programmes.** Later weeks need the exporter/importer extended and their grading rules checked first. Practical tests use the [test checklist](../test_operations/TEST_CHECKLIST.md).

This refresh is assisted by Codex. It is **not** an unattended Google-to-Excel sync or a single safe terminal command yet.

## 1. Get ready

Use only one Mac. Finish and save any earlier grading run before pulling:

```sh
git -C ~/Projects/teaching-material pull --ff-only
git -C ~/Projects/IUEA-Grading-Private pull --ff-only
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py restore ~/Projects/teaching-material
```

If restore reports differing local files, stop. Save the local batch first; do not use `--replace` to bypass the message.

## 2. Export the latest submissions

Sign into Google as **wirmbeesubs@gmail.com**.

1. Open [Assignment Apps Script](https://script.google.com/home/projects/1XLdUAzi6wnSjQ2iFTV3hl5BQk9XWw-PIi1_vodC_l107B6S13yW_ZObw/edit).
2. Run **startCAExport** once, then **exportCANext** once. The scheduled exporter continues the work.
3. Run **inspectCAExportProgress** to check progress. Wait for **15 quizzes and 15 assignments**. Do not run startCAExport again during that export.
4. Open the private Drive folder linked in the execution log. Download the complete folder as a ZIP. Keep every part if Drive splits the download.

This copies submissions; it does not reopen forms, change deadlines or award marks.

## 3. Download the recorded quiz marks

For each programme, open its quiz response spreadsheet from a quiz form's **Responses → View in Sheets**. Use **File → Download → Microsoft Excel (.xlsx)**. Download the whole workbook, not one CSV tab.

Save the three workbooks with these names:

```text
CML3111_quiz_source.xlsx
CML3112_quiz_source.xlsx
CML3113_quiz_source.xlsx
```

Also download the assignment collection workbook containing the **Submission audit** tab as `assignment_source.xlsx`.

Keep this batch's ZIP and four spreadsheets together in a **new folder**, for example `~/Downloads/IUEA_CA_2026-10-22`. Never overwrite the previous batch. Quiz marks come from recorded response-sheet scores; the ZIP alone is insufficient. If a form was reopened or its deadline changed, tell Codex so timing records can be refreshed before marks are allocated.

## 4. Ask Codex to refresh the marks

Open `~/Projects/teaching-material` in Codex on the Mac mini. Paste this request, replacing the download folder with yours:

> Import and grade new Week 1–5 submissions from ~/Downloads/IUEA_CA_2026-10-22. Preserve the current source snapshot, existing marks and attempt history. Verify all export parts and downloads, import fresh response-sheet scores and the assignment audit, and verify current deadlines plus authorized historical windows. Compare receipts and attachment hashes with the prior batch; grade new or changed eligible work and preserve unchanged completed marks. Keep raw submitted identities for grading. Stop Docker before local AI inference and require valid model calibration. Merge by response ID without duplicate marks; retain unresolved cases with original file links. Rebuild the cumulative Excel workbook, preserving any existing test/project marks. Verify totals and report new, held and failed records. Do not publish marks, alter deadlines or run the old one-time finish_ca_refresh.py script.

Keep the Mac awake. Docker is used first for code/document extraction, then stopped for written grading. Keep Ollama running natively. Do not run another grader or pull code during the batch.

If processing stops, ask Codex to **resume that same batch from its checkpoints**. Do not delete its results or replace the snapshot to hide an error.

## 5. Check and save

```sh
open ~/Projects/teaching-material/IUEA_Teaching_Plan/assessment_operations/private/IUEA_Continuous_Assessment.xlsx
```

Check programme totals and **Review needed**. Pending work is blank, not zero. A new unresolved attempt can leave the current mark pending; the prior mark remains in history. Keep manual decisions against the response ID and ask Codex to apply approved decisions; direct Excel edits are overwritten on refresh.

After the batch finishes, close Excel and save the private snapshot:

```sh
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py capture ~/Projects/teaching-material
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py verify
git -C ~/Projects/IUEA-Grading-Private add snapshot manifest.json
git -C ~/Projects/IUEA-Grading-Private commit -m "Update private grading results"
git -C ~/Projects/IUEA-Grading-Private push
```

**Nothing to commit** means there is no new snapshot change to save. Before switching Macs, finish this save/push step; on the other Mac repeat step 1.

Repeated receipts are matched by response ID, not added again. Different submissions remain as separate attempts, with the eligible current attempt selected under the assessment rules. Original files and previous marks remain available for review.
