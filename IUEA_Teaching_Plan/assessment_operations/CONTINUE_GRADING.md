# New submissions: repeat checklist

Use this after [setup](README.md), whenever more students submit work. You can grade in batches; you do not need to wait for everyone.

**Current scope: Quizzes 1–5 and Assignments A1–A5 across all three programmes.** Later weeks need the exporter/importer extended and their grading rules checked first. Practical tests use **Export Test ZIP** in their own collection workbook and the [test checklist](../test_operations/TEST_CHECKLIST.md).

Use the workflow that matches the submission:

| Submission | Export and grading route |
| --- | --- |
| A1–A5 notebook assignments | This guide: Export Grading ZIP → `grade-submissions`; student code runs in Docker. |
| A1–A5 written/document assignments | The same ZIP and command; document preparation uses Docker, then native Ollama checks written answers. |
| Quizzes 1–5 | The same ZIP and command imports the recorded Google Forms scores. |
| Test 1 / Test 2 notebooks | [Test checklist](../test_operations/TEST_CHECKLIST.md#after-each-test): Export Test ZIP → `Grade_Tests.command`; updates both test marks and the cumulative workbook automatically. |

After downloading, **one command imports, grades and updates Excel**. Google downloads are still manual. Keep native Ollama running; the command starts Docker when needed and stops it before written grading.

## When Docker and Ollama are used

**Docker** runs submitted notebook code in an isolated environment called a container, instead of running student code directly on your Mac. It also helps prepare documents for reading. **Ollama** runs the local AI models that assess written explanations against the marking rubric. “Native Ollama” means it runs directly on macOS, outside Docker. A model is the downloaded AI used to assess the text; the Ollama server is the background program that receives the grader's requests.

After you run `grade-submissions`, the command handles this sequence automatically:

| Order | What happens | What is used |
| --- | --- | --- |
| 1 | Read the downloaded ZIP, identify submissions and import recorded quiz scores. | Grading scripts; quiz scores do not need AI. |
| 2 | Run submitted notebook code and check its results against the marking rules. | Docker. The command starts it if needed and first asks Ollama to unload the grading models from memory. |
| 3 | Extract and prepare written content from submitted documents. | Document tools, including Docker where needed. |
| 4 | Stop Docker to free memory, then assess written answers against the rubric. | Native Ollama. The command checks that Docker has stopped before AI grading. |
| 5 | Combine available marks, validate the workbook and update Excel. | Grading scripts. Unresolved records remain available for review. |

Completed work is reused, so a batch with nothing new to grade can skip the grading stages.

**Your part:** after the one-time setup, start the Ollama server in step 3 and leave its Terminal window open. Run the grading command in a second Terminal window in step 4. You do not manually switch between Docker and Ollama. The server can stay open during the Docker stage; an open server does not mean its AI model is currently grading. Do not reopen Docker during written grading.

**Test 1 and Test 2 are different:** follow the [test checklist](../test_operations/TEST_CHECKLIST.md#after-each-test). Start Docker Desktop yourself, wait for it to be running, then run `Grade_Tests.command`. Those tests use fixed checks for code and structured answers; Ollama is not needed.

## 1. Get ready

Use only one Mac. Finish and save any earlier grading run before pulling:

```sh
git -C ~/Projects/teaching-material pull --ff-only
git -C ~/Projects/IUEA-Grading-Private pull --ff-only
```

**Continuing on the same Mac:** keep its existing grading files and proceed to step 2. Do not restore the snapshot again.

**First setup or switching to this Mac:** after saving and pushing results from the previous Mac, restore the latest private snapshot here:

```sh
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py restore ~/Projects/teaching-material
```

If restore reports differing local files, it has copied nothing. This can happen even before grading has run. Identify the files first:

```sh
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py compare ~/Projects/teaching-material
```

This only reads files. `CHANGED` means different contents; `MISSING` means a file has not been restored. Review the changed paths before choosing which copy to keep. Do not run `capture` or `restore --replace` just to clear the error.

## 2. Export the latest submissions

Sign into Google as **wirmbeesubs@gmail.com**.

1. Open the [assignment collection workbook](https://docs.google.com/spreadsheets/d/1FxAVXwSvLEd7TEd3pJ2E0_ka7Mp6ZM6pW1yNsXKWdm4/edit#gid=534991827). Choose **Export Grading ZIP → Start / resume export**. Refresh the workbook once if the menu is missing. On first use, Google may ask you to authorize the workbook’s menu script.
2. Allow about a minute for the request to start. Choose **Export Grading ZIP → View progress / download** to open **CA Export**. Wait until the new export says **COMPLETE**; while the request says **PENDING**, the previous download may still be displayed. Large batches can take tens of minutes. You can close the browser while Google collects the files.
3. Open the **Download / detail** link and download that **one ZIP**. Do not download the whole folder or any Excel source files. Keep the ZIP unchanged. If Google shows its large-file scan notice, choose **Download anyway**.

The ZIP contains original submissions, recorded quiz scores, assignment audit details and quiz deadlines for all three programmes. It uses a fixed cutoff: later submissions belong to the next export. Existing marks, forms and deadlines are unchanged.

If the status says **STOPPED**, read its explanation. After resolving the issue, choose **Export Grading ZIP → Start / resume export** again. A running export is not restarted. If **Request status** shows **ERROR**, read that explanation before trying again.

## 3. Start the local model server

If your native Ollama server is already running with the setup-guide settings, leave it running. Otherwise, open Terminal (press Command–Space, type `Terminal`, then press Return). Choose **Shell → New Window** and run:

```sh
OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 \
  OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 ollama serve
```

Leave that window open. If it reports **address already in use**, follow [the port-conflict instructions](reference/MAC_MINI.md#native-ollama-written-grading); do not start another server. You do not need to download the models again.

Before the first grading run on a new Mac, or after an Ollama/model update, check the saved calibration (known-answer grading checks):

```sh
~/Projects/teaching-material/.iuea-grader-env/bin/python ~/Projects/teaching-material/IUEA_Teaching_Plan/grader/check_written_setup.py
```

Both A1 and A2 must say **PASS**. This reads the model information and saved reports without grading anything. If it says **BLOCKED**, keep the output for diagnosis. Do not edit the reports or bypass validation: the exact Ollama version, model files and rubric must match, or new calibration is needed. If a batch already stopped for this reason, preserve its files and resume the same ZIP after the issue is resolved.

If the diagnostic confirms that the installed model files or Ollama version changed, recalibrate them with this command while Ollama is running:

```sh
caffeinate -i ~/Projects/teaching-material/.iuea-grader-env/bin/python ~/Projects/teaching-material/IUEA_Teaching_Plan/grader/recalibrate_written_setup.py
```

It stops Docker, tests A1 and A2 using synthetic known-answer examples, and saves the evidence privately. Only after both pass does it activate the new reports, backing up the originals. It does not change student marks. Wait for **PASS: both calibrations activated**, then repeat the original `grade-submissions` command with the same ZIP. If a case fails, retain the output for review; do not bypass the check or restore a snapshot over the interrupted batch.

To try a larger model without changing anything live, pull it first (`ollama pull qwen3.5:9b`), then run the same script with `--trial --a1-model qwen3.5:9b --a2-model qwen3.5:9b`. A trial runs both calibrations and prints **TRIAL PASS** or fails; it activates nothing and leaves marks untouched. Evidence is saved under `model_trials/`.

Written grading is also given the cohort's student instructions (`student_guides/<cohort>/<W01|W02>.md`). A submission containing only ZIP, script, CSV or spreadsheet files is scored 0 with the reason recorded in the Grading note.

Finish any unrelated Docker work first. The grading command manages Docker for code/document checks, then stops it before written grading. Do not reopen Docker during written grading.

## 4. Run one grading command

Close the marks workbook in Excel. Keep the Ollama window open. Choose **Shell → New Window** in Terminal, then run the following command in that second window:

```sh
~/Projects/teaching-material/grade-submissions ~/Downloads/IUEA_CA_20261022_120000.zip
```

The filename above is an example. Replace it with your downloaded ZIP. To avoid typing the path, type `~/Projects/teaching-material/grade-submissions ` (including the space), drag the ZIP from Finder into Terminal, then press Return. Keep the Mac powered and connected. The command prevents idle sleep. Do not start another grader or pull changes during the run.

**If interrupted:** repeat the exact command before pulling or restoring anything. Saved grading checkpoints are reused; a completed batch is not added twice. The previous workbook remains available until the new workbook passes validation. Missing or inconsistent downloads stop the run with an explanation.

Existing completed marks and earlier attempts are retained. Changed files are checked again. Unreadable work, conflicting identities and disputed written judgements stay in **Review needed**, not zero.

Current quiz windows are included automatically. Earlier reopening windows are retained from the private history; ambiguous timing remains pending for review.

## 5. Review the updated marks

```sh
open ~/Projects/teaching-material/IUEA_Teaching_Plan/assessment_operations/private/IUEA_Continuous_Assessment.xlsx
```

Check programme totals and **Review needed**. Pending work is blank, not zero. A new unresolved attempt can leave the current mark pending; the prior mark remains in history. Keep manual decisions against the response ID and ask Codex to apply approved decisions; direct Excel edits are overwritten on refresh.

## 6. Save the results before another batch or switching Macs

After the batch finishes, close Excel and run:

```sh
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py capture ~/Projects/teaching-material &&
python3 ~/Projects/IUEA-Grading-Private/sync_snapshot.py verify &&
git -C ~/Projects/IUEA-Grading-Private add -A snapshot manifest.json &&
(git -C ~/Projects/IUEA-Grading-Private diff --cached --quiet || git -C ~/Projects/IUEA-Grading-Private commit -m "Update private grading results") &&
git -C ~/Projects/IUEA-Grading-Private push
```

The `&&` symbols mean “continue only if the previous command succeeded.” Paste this whole block together. If capture or verification fails, commit and push will not run. Do not restore a failed snapshot; preserve the teaching folder and resolve the error first. No new snapshot changes means the commit step is skipped. Before switching Macs, finish this save/push step; on the other Mac repeat step 1.

Repeated receipts are matched by response ID, not added again. Different submissions remain as separate attempts, with the eligible current attempt selected under the assessment rules. Original files and previous marks remain available for review.

## Automatic identity checks and optional deeper review

Every new `./grade-submissions <ZIP>` run now gathers explicit names and registrations from new submission files, retains earlier local-AI identity evidence, and applies the full reconciliation rules before rebuilding Excel. This includes supported programme-letter typos, IG/UG entries and incomplete years. You do not need a separate reconciliation command after grading. The terminal reports **Identity checks complete**, with correction and released-mark counts. Test imports also rerun reconciliation before updating cumulative marks. Original receipts, duplicate-submission rules and uncertain identity holds are preserved.

**Current lecturer policy:** Student Registration Number determines mark allocation. Different emails or missing/conflicting display names alone do not withhold marks for the same resolved registration. When the notebook and form disagree, the registration recorded by the notebook grader takes precedence only after verifying the original uploaded file and grader hashes. Original form entries remain in the audit. Names are descriptive and never invented from an email address. Unresolved malformed registrations, unreadable notebooks, incomplete grading and timing holds still need attention.

Specific lecturer-confirmed registration corrections and names are saved privately in `identity_policy.json`. They are carried into later grading generations. The private root copy can also be updated separately without restoring or replacing the marks workbook. The older account/name evidence rules below describe supporting evidence; the current registration-first policy takes precedence for allocating marks.

Automatic checks also handle a name attached to a complete registration, an `L` separator, a missing suffix and programme spelling errors when a unique observed target is supported by the account's assessment history. A name-only entry needs an exact confirmed/submission name and one repeated registration. A missing serial component additionally needs consistent names in distinct files and repeated target declarations. Conflicting complete numeric IDs or multiple possible suffixes are not merged by popularity.

Document identity text is extracted in the existing Docker phase, before Docker stops for written AI grading. The automatic identity pass then reads the saved text and notebook declarations without extra AI inference. Names that are not explicitly labelled or supported by earlier evidence remain for review. To request a deeper local-AI name extraction for those cases, use the optional command below.

After grading finishes, close Excel and leave native Ollama running. Run:

```sh
~/Projects/teaching-material/review-identities --resolve
```

This reads original files. It starts Docker to extract private, unredacted document text, then stops Docker before using native Ollama. It also reads notebook/README text and bounded text files inside ZIPs. Identity extraction is separate from the redacted text used to grade written answers. It never executes notebook code. Local AI proposes names with exact quotations; email spelling is only supporting evidence. Missing names are filled only when corroborated by distinct files, or by both the registration in the file and the email spelling. Existing names are preserved. Unreadable files, conflicting names and uncertain identities go into **Identity review**, with the original file links and evidence. No name is invented from an email address.

The `--resolve` option also reconciles supported identities and rebuilds totals in the same run. To reuse already collected evidence without another extraction or AI pass, run:

```sh
~/Projects/teaching-material/reconcile-identities
```

For separator-only corrections (leaving letter, digit and programme-code differences for review), use `reconcile-identities --separators-only`. It requires the same account to have submitted an unambiguous structured registration, repeated across assessments; it never guesses where to split digits.

The full `reconcile-identities` command also checks repeated programme letters (for example BBARC/BARC), IG/UG entries and incomplete one-digit years. Course context is Electrical/Robotics & Mechatronics for CML3111, Architecture/Civil for CML3112, and Petroleum/Mining for CML3113. Corrections require the same account, repeated registration declarations in distinct files across assessments, compatible names and no competing account. An incomplete year additionally requires the affected submission itself to declare the full target registration. Serial-number changes and unexplained suffix changes remain for review. Notebook declarations are checked too; code marks are released only when the original file hashes and complete grader results still verify.

If you already ran `review-identities`, run only this second command. It reuses the saved names and submission evidence; neither Docker nor Ollama is needed. Close Excel first and wait for **Complete**.

This normalizes supported punctuation differences, including stray apostrophes and a slash before the final programme suffix. A missing letter is corrected only when the same account has a consistent name, two independently hashed files declare the target registration, and no competing account uses either number. Separate email accounts are linked only when each has a distinct submission declaring the same full name and registration, with no conflicting evidence. Other spelling/number differences remain for review. Each course group contains multiple degree programmes; the most common programme is never imposed on other students.

The workbook regroups supported matches and recalculates totals using the existing attempt rules. It preserves every original receipt, the registration as entered, and the previous workbook generation. A complete notebook score is released only when its file hashes and recorded checks support the corrected registration. A2 code-only marks remain partial until its written component is graded. Timing and other grading holds remain in force. Check **Registration corrections** for the before/after audit and **Identity review** / **Review needed** for unresolved cases. Do not manually replace calculated totals.

Open the cumulative workbook as in step 5. Check **Identity review**, then save the private snapshot as in step 6. Later weekly/test updates retain the name evidence and repeat registration reconciliation automatically. If a document could not be read, use its link to review it manually. This uses the local model only; no student work is sent to a cloud AI service.

### Confirm the remaining identity cases

The separate **Identity_Review.xlsx** has two tabs. In **Cases**, read the possible registrations/accounts and the exact question. Filter **Submission evidence** by the Case ID and click **Open submission** to inspect the files. Fill the yellow columns in **Cases**. If the accounts belong to different students, fill the yellow fields beside the affected receipts in **Submission evidence** instead. Leave uncertain cases marked **Still uncertain**. Save a working copy and return it for reconciliation; editing this sheet does not automatically change marks.

The review file is in the private snapshot under `IUEA_Teaching_Plan/assessment_operations/private/outputs/identity-review-20261022/`. Copy it outside the snapshot before editing so later snapshot captures do not overwrite your decisions. The review reflects the receipts available when generated.

If a pull fails with `HTTP/2`, `curl 92`, or `early EOF`, retry using `git -C ~/Projects/IUEA-Grading-Private -c http.version=HTTP/1.1 pull --ff-only`. This changes the transfer protocol for that command only. A failed first command in an `&&` chain prevents the later grading commands from running. Do not reset your working copy or restore over local marks to fix a download failure.

## ZIPs, GitHub links, scanned PDFs and the workbook tabs

- A ZIP, or an HTML file linking to a public GitHub repo, is opened when no notebook was uploaded directly. The notebook/README inside is graded with no penalty, and the Grading note says where it came from. Nothing is run outside the grading container. GitHub downloads are cached in `private/…/expanded`.
- Scanned PDFs are read with Apple Vision (`pip install ocrmac pypdfium2` in `.iuea-grader-env`); Tesseract is the fallback.
- Lecturer test submissions (TEST… registrations, the lecturer's emails/name) are dropped from the compiled marks.
- The workbook opens on **Start here**, which lists every tab and the live count of items needing manual review. Work through **Review needed** by Category; each row links to that student's own form response and uploaded files.
