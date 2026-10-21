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

1. Open [Assignment Apps Script](https://script.google.com/home/projects/1XLdUAzi6wnSjQ2iFTV3hl5BQk9XWw-PIi1_vodC_l107B6S13yW_ZObw/edit). Select **Continuous_Assessment_Export.gs**, choose **exportCAGradingZip** and click **Run** once.
2. In the [assignment collection workbook](https://docs.google.com/spreadsheets/d/1FxAVXwSvLEd7TEd3pJ2E0_ka7Mp6ZM6pW1yNsXKWdm4/edit#gid=534991827), open the **CA Export** tab. Wait until it says **COMPLETE** (refresh the page to check). The export continues automatically; large batches can take tens of minutes. You can close the browser while Google collects the files.
3. Open the **Download / detail** link and download that **one ZIP**. Do not download the whole folder or any Excel source files. Keep the ZIP unchanged. If Google shows its large-file scan notice, choose **Download anyway**.

The ZIP contains original submissions, recorded quiz scores, assignment audit details and quiz deadlines for all three programmes. It uses a fixed cutoff: later submissions belong to the next export. Existing marks, forms and deadlines are unchanged.

If the status says **STOPPED**, read its explanation. After resolving the issue, run **exportCAGradingZip** again to resume. Never run **startCAExport** while an export is underway.

## 3. Run one command

Close the marks workbook in Excel. In Terminal:

```sh
~/Projects/teaching-material/grade-submissions ~/Downloads/IUEA_CA_20261022_120000.zip
```

Replace the ZIP filename with yours (you can drag the downloaded ZIP into Terminal to insert its path). Keep the Mac powered and connected. The command prevents idle sleep. Do not start another grader or pull changes during the run.

**If interrupted:** repeat the exact command. Saved grading checkpoints are reused; a completed batch is not added twice. The previous workbook remains available until the new workbook passes validation. Missing or inconsistent downloads stop the run with an explanation.

Existing completed marks and earlier attempts are retained. Changed files are checked again. Unreadable work, conflicting identities and disputed written judgements stay in **Review needed**, not zero.

Current quiz windows are included automatically. Earlier reopening windows are retained from the private history; ambiguous timing remains pending for review.

## 4. Check and save

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
