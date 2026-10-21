# New submissions: repeat checklist

Use this after [setup](README.md), whenever more students submit work. You can grade in batches; you do not need to wait for everyone.

**Current scope: Quizzes 1–5 and Assignments A1–A5 across all three programmes.** Later weeks need the exporter/importer extended and their grading rules checked first. Practical tests use the [test checklist](../test_operations/TEST_CHECKLIST.md).

After downloading, **one command imports, grades and updates Excel**. Google downloads are still manual. Keep native Ollama running; the command starts Docker when needed and stops it before written grading.

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

## 4. Run one command

Close the marks workbook in Excel. In Terminal:

```sh
~/Projects/teaching-material/grade-submissions ~/Downloads/IUEA_CA_2026-10-22
```

Replace the download folder with yours. Keep the Mac powered and connected. The command prevents idle sleep. Do not start another grader or pull changes during the run.

**If interrupted:** repeat the exact command. Saved grading checkpoints are reused; a completed batch is not added twice. The previous workbook remains available until the new workbook passes validation. Missing or inconsistent downloads stop the run with an explanation.

Existing completed marks and earlier attempts are retained. Changed files are checked again. Unreadable work, conflicting identities and disputed written judgements stay in **Review needed**, not zero.

If a quiz was reopened after the last saved deadline audit, later receipts remain pending until that timing is verified. Include a freshly verified `quiz_deadlines.json` in the batch folder when needed; ask Codex to obtain it from the lecturer quiz controls. This command never changes forms or deadlines.

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
