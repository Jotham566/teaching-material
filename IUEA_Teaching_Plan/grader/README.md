# Assessment operations

Student notebooks run in a restricted Docker container. The authoritative checks run separately on the lecturer's computer. Practice receipts never become final marks. Report and presentation text is assessed by a local Ollama model; this tool has no cloud grading mode.

## First setup

On this Mac, run `source .iuea-grader-env/bin/activate` from the repository root. The Python 3.12 environment and pinned dependencies are installed. Keep using that environment for the commands below; the older `.iuea-env` is Python 3.9. On another computer, create a Python 3.11+ environment and install `requirements.txt`. Start Docker Desktop, then build the pinned grading image:

```sh
docker build -t iuea-notebooks:2026.09 IUEA_Teaching_Plan/grader
python3 -m unittest discover -s tests -v
node tests/test_assessment_pipeline.cjs
```

The container has no network, an unprivileged user, a read-only system, bounded temporary storage, memory and process limits, and a hard wall-clock timeout. Only copied teaching inputs are mounted. Hidden checks and the host filesystem are not available to student code. This reduces risk; it does not prove a container runtime has no vulnerabilities.

Only distribute `IUEA_Teaching_Plan/student_packages/` and the student-facing decks. Keep `grader/specs/hidden/`, lecturer guides, answer keys and grade exports private. Week 1 earned marks are preserved.

## Submission forms and expiry

`submission_forms.gs` is a separate lecturer-owned Apps Script project. Uploads are stored in your Google Drive; the AI assessment happens only after download to this Mac. Local inference does not make Google Forms storage local. It defines 52 assignment forms across the two tracks. The live deployment on 14 September 2026 created all 52; use `../Assignment_Submission_Links.md` and the live Assignment links sheet recorded in `review/2026-09-14/rework/live_setup.json`. Creating the script locally alone does **not** create live forms.

1. In Google Forms create a private upload template with exactly one **required** file-upload question. Allow multiple files (up to 10), with a 10 MB per-file limit. The broad upload template accepts notebooks too; the assignment description specifies the required formats. Google requires respondents to sign in for file uploads. In Settings → Responses, select **Verified** email collection (not Responder input).
2. Paste `submission_forms.gs` into a standalone Apps Script project. Run a small wrapper calling `configureSubmissionSystem('TEMPLATE_ID')`. Google requires the owner to authorize Forms, Drive, Sheets and trigger access.
3. Run `buildSubmissionForms()` until every entry reported by `submissionStatus()` is ready. Reruns resume. It publishes forms closed and installs one five-minute scheduler. It does not send invitations or email.
4. Open each copied form in the editor, click **Restore** if Google reports missing upload folders, and confirm Settings → Responses → Collect email addresses is **Verified**. Only after these checks, run `confirmSubmissionReadiness(['COHORT|ASSESSMENT', ...])` for the checked keys. Unverified forms cannot open. Run `finalizeSubmissionSetup()` to refresh the **Assignment links** sheet and attempt closed-message updates. Google currently rejects the custom closed-message update on these published forms; errors are logged per form, and students should use the dated link index.
5. Review the cohort-specific deadlines in Kampala time. Run `setSubmissionWindow('CML3112|W02','2026-09-15T11:00:00+03:00','2026-09-22T11:00:00+03:00')` to set a window explicitly. DA dates remain unset and those forms remain closed until actual teaching dates are provided.
6. Test with a non-owner student account: identity, two attachments, receipt, replacement response, closure and audit. Check owner storage capacity before releasing links.

This is a shared opening/closing window, not an individual countdown. The server-recorded response timestamp determines timeliness even if a Google time trigger runs late. The form may remain visible briefly after expiry; such responses are marked LATE. No late mark is silently accepted. Any outage extension must be explicit.

Run `exportSubmissionFiles('CML3112|W02')` after `syncSubmissions()`. It creates a private Drive folder with file-ID filenames and an audit CSV. Download/extract that folder locally. Export the roster as CSV with `student_id,name,email,cohort`. Then:

```sh
python3 IUEA_Teaching_Plan/grader/prepare_submissions.py \
  --audit downloads/submission_audit.csv --downloads downloads \
  --roster roster.csv --assessment 'CML3112|W02' --out prepared/W02
```

The latest on-time response wins as a whole; attachments from competing responses are not mixed. IDs, email and cohort must match the roster. A missing roster email for a submitting student stops preparation. Unknown IDs, ambiguous files and equal-time conflicts stop the batch. Original uploads remain intact. Use registered team membership with `expand_team_grades.py` for a shared project component; individual reflection remains individual.

## Deterministic grading

Run from the repository root. For Week 4:

```sh
python3 IUEA_Teaching_Plan/grader/batch_grade.py -a W04 \
  --cohort CML3112 -n prepared/W04 \
  --data-dir IUEA_Teaching_Plan/practicals/W04/CML3112 -o results/W04
```

Week 3 uses W03 with no dataset. Week 5 uses W05 with the cohort practical directory. Always grade the complete roster submission set; `--sample` is a diagnostic audit, not a final-mark pipeline. Do not paste marks by row order.

Week 2 has a 14-point deterministic component and a 6-point explanation component:

```sh
python3 IUEA_Teaching_Plan/grader/batch_grade.py -a W02 \
  --cohort CML3112 -n prepared/W02 \
  --data-dir IUEA_Teaching_Plan/setup/CML3112 -o results/W02_code
python3 IUEA_Teaching_Plan/grader/artifact_grade.py \
  --submissions prepared/W02/manifest.csv \
  --rubric IUEA_Teaching_Plan/grader/rubrics/W02.json \
  --deterministic-results results/W02_code/results.csv \
  --calibration-report review/2026-09-14/rework/local_calibration_v10.json --out results/W02
```

DA Session 5 uses the local read-only Riverside SQL grader:

```sh
python3 IUEA_Teaching_Plan/grader/da_sql_grade.py \
  --submissions prepared/S05/manifest.csv --out results/S05
```

SQL runs inside the restricted Docker image, using a read-only database with bounded execution and output. It checks report row keys, gross, returns and net amounts, 25 marks each. Repeated return events are combined before joining to sales, so they cannot multiply gross revenue. Columns must be `region,rep_name,month,gross_ugx,returned_ugx,net_ugx`; amount tolerance is 1 UGX. Writes, attached databases, extension loading and unbounded recursive execution are rejected. Missing, unreadable or ambiguous SQL files produce an individual pending result while other learners' reports proceed.

## Local report and presentation grading

On this Mac, double-click `start_local_model.command` before grading. Run Ollama on loopback with cloud features disabled (`OLLAMA_NO_CLOUD=1`, `OLLAMA_HOST=127.0.0.1:11434`). The configured candidate is `qwen3:4b`, chosen for this Mac's 8 GB memory. Installation and a successful model calibration are separate from the existence of the grading script: check the rework status before using it for real grades.

```sh
python3 IUEA_Teaching_Plan/grader/artifact_grade.py \
  --submissions prepared/DEMO/manifest.csv \
  --rubric IUEA_Teaching_Plan/grader/rubrics/DEMO.json \
  --calibration-report calibration/DEMO.json --out results/DEMO
```

DOCX, selectable-text PDF and PPTX speaker notes are supported. PPTX submissions must include narration as text in notes. Native PBIX and ZIP files are not readable grading evidence; provide accessible report/slide exports. Images, animation, spoken delivery and interactive dashboard behaviour are not assessed by this text pipeline. Do not claim a visual-design mark has been verified from extracted text alone.

Files from one response are assessed together. The combined supported text limit is 12,000 characters; longer packets produce an exception instead of silent truncation. Each result retains source and rubric hashes, model name, two criterion-level evaluations and exact supporting quotations. A rerun reuses successful results only when the input, rubric, model and deterministic marks/status match. Temporary notebook staging paths and execution duration do not trigger fresh AI marking. The CLI selects the model recorded in the passing calibration unless an explicit matching `--model` is supplied. Transport timeouts receive one automatic retry of the complete two-pass evaluation. Model disagreement and low marks are not retried to search for a different score. Unresolved packets remain blank; a later explicit rerun can retry them. The CLI requires a passing calibration report covering the exact current authored cases, expected score ranges and input hashes, as well as the rubric, evaluator and local model digest. Incomplete or stale case sets cannot authorize marks. The DEMO example requires a report that has not yet been created; it is not a ready-to-run assessment. Agreement between two passes is not evidence of grading accuracy; calibration against known work is required.

Exceptions have blank scores, never invented zeros. Resolve a file-format issue through a corrected accessible export; retain the original timestamp and a documented resubmission decision. Inconsistent substantive judgements need a calibrated stronger local model or a revised objective assessment, not blind acceptance.

## Gradebook

Run `python3 IUEA_Teaching_Plan/grader/prepare_grade_import.py results/W04/results.csv --out results/W04/import` to generate `import_ready.csv` and a separate `exceptions.csv`. This lets completed marks proceed while exceptions remain blank. Upload only `import_ready.csv` for the final component; a 14-point W02 code component is deliberately rejected until combined with its reasoning marks.

Create a `Grades` sheet using `Grades_template.csv` and paste `gradebook.gs` into its bound Apps Script. `importMarkedResults('DRIVE_CSV_ID','W04')` imports authoritative results by student registration number, rejecting duplicates, unknown IDs, invalid marks, wrong maxima and unresolved statuses before any marks are written. Use the combined 20-point output for W02. The IUEA gradebook does not mix in the independent DA track.

`configureQuizImports(...)` and `importQuizScores()` import Google Forms quiz marks by roster ID and cohort. Supply the actual close time for every quiz source. Practice tokens are diagnostic receipts only. They can be forged because their key is distributed; they are never a mark source.

| Component | Weight | Rule |
|---|---:|---|
| Quizzes | 10% | Best 10 of 12, each /5 |
| Challenges | 10% | Best 8 of 11, each /20; W01–W06 and W08–W12 |
| Data analysis project | 10% | /100 |
| Practical Test 1 | 15% | /100 |
| Practical Test 2 | 20% | /100 |
| ML project | 25% | /100 |
| Demo / reflection | 10% | /100 |

Letter bands remain placeholders until verified against the Faculty's actual rules. The weighted percentage is separate from that policy. Existing Week 1 marks cannot be overwritten by the results importer.

## Verification

```sh
python3 IUEA_Teaching_Plan/grader/iuea_grader.py --selftest
node IUEA_Teaching_Plan/grader/gradebook.gs --test
python3 -m unittest discover -s tests -v
node tests/test_assessment_pipeline.cjs
```

See `review/2026-09-14/rework/` for the actual notebook isolation and cohort-simulation evidence. Rubrics for later reports/projects exist, but an arbitrary notebook's correctness is not proved by an AI reading its source. Practical exams need their issued task-specific deterministic checks before release.

## IUEA identity terminology

The official student-facing term is **Student Registration Number**. Legacy machine fields `student_id` and `STUDENT_ID` remain for compatibility; they are not the display label. Form imports recognize both the old and new labels. The fictional format example (never a student identity) is `99/TEST/000/DEMO-X`. Four slash-separated components are accepted; the roster remains authoritative, and program codes are not restricted to this single example. Use `99_TEST_000_DEMO-X_W02.ipynb` for the filename, keeping the original slash-separated number in notebook values and grade records. Legacy S-numbers are retained only for compatibility with existing internal fixtures and the independent DA roster.

## Later assessment contracts (release checks pending)

`../assessment_banks/` contains cohort-specific task sheets and starter notebooks for W06, W08–W12, both practical tests and both major projects. Each exam has variants A/B/C with the same schema and defect counts. These are synthetic engineering scenarios, labelled as such. `assessment_components.json` maps every deterministic mark back to its published rubric criterion; original criterion totals are preserved. The remaining marks use the corresponding `rubrics/hybrid/` rubric. Do not issue a draft bank until its release status, reference tests and calibration are complete.

The fixed function interfaces are a machine-checkable skills component. Students still explain and justify the broader investigation. Checks use unseen inputs, not a saved screenshot or a claim that code ran. Figure checks inspect actual matplotlib figures, their plotted values and unit labels. They do not assess aesthetic quality or spoken delivery.

A prepared hybrid assessment can be run with:

```sh
python3 IUEA_Teaching_Plan/grader/grade_assessment.py \
  --assessment W06 --cohort CML3112 --prepared prepared/W06 \
  --calibration validated/W06.json --out results/W06
```

The calibration gate verifies the exact rubric, local model and evaluator implementation (including extraction and prompt). Changing the evaluator invalidates earlier calibration reports; retained historical reports are evidence, not current release approval.

## Offline practical-test collection

Google upload time must not replace the invigilator's offline collection time. Run `collect_offline.py` on the lecturer's machine with an invigilator-controlled intake folder, cohort roster, assessment and explicit deadline. It records the lecturer's clock, hashes copied notebooks, preserves originals and prepares only on-time files in its manifest. Keep the receipt with any later transport copy. Students do not run this receipt tool. Part B is 25 minutes of typed offline responses with code execution prohibited; printed/handwritten answers are not automatically graded by this system.

```sh
python3 IUEA_Teaching_Plan/grader/collect_offline.py \
  --intake collected --roster roster.csv --assessment TEST1 --cohort CML3111 \
  --deadline '2026-10-23T14:00:00+03:00' --out receipts/TEST1-sitting1
```


Document rendering and extraction require the separate local image:

```sh
docker build -t iuea-document-renderer:2026.09 IUEA_Teaching_Plan/grader/document_renderer
python3 IUEA_Teaching_Plan/grader/render_submission.py report.docx --out rendered/report
```

DOCX/PDF/PPTX parsing is isolated as well as rendering. Rendered pages alone do not authorize visual marks: `visual_grade.py` has its own local model and calibration gate. A completed calibration report has a matching `.complete.json` record; interrupted or modified reports are rejected. A model or evaluator change requires recalibration.

The quiz importer requires a populated roster email and a matching respondent email. It ignores the unscored registration field when summing five one-point questions. Existing Week 1 quiz marks are protected against replacement. Later notebook explanations belong in `## My written evidence`; starter instructions and source-code comments are excluded from reasoning marks. For exam variants use `grade_assessment.py --variant A`, `B` or `C` as issued. Submit only one cohort/variant per batch.


### One command for prepared Weeks 2–5

`grade_assessment.py --assessment W03 --cohort CML3112 --prepared prepared/W03 --out results/W03` selects the issued cohort data, grades only the eligible manifest packets and writes `results/W03/import/import_ready.csv`. W04 and W05 work the same way. W02 additionally requires `--calibration PATH_TO_CURRENT_PASSING_REPORT`; its notebook and README are combined to 20 marks. Failed or stale calibration cannot produce final marks.

### Independent-track gradebook

Fill `DataAnalysis_Track/learner_roster_template.csv` with learner IDs in the form `S10001`, names, Google account emails and cohort `DA`. After each assessment, pass its authoritative 100-point results to `da_gradebook.py --roster ROSTER.csv --s05 S05_RESULTS.csv --s09 S09_RESULTS.csv --s13 S13_RESULTS.csv --s15 S15_RESULTS.csv --out results/DA`. Omit sessions not yet graded. The weights are 15%, 15%, 30%, 40%; a missing or unresolved component leaves the final percentage blank. No Faculty grade bands are applied to this independent track.

Session 5 is assessed through four 25-point SQL result checks: grain, gross amount, returned amount and net amount. The judgement comment is formative discussion, not an additional manually assessed component.

### Live quiz settings checked on 15 September 2026

All 36 existing quizzes have immediate grade release, Point values, Missed questions and Verified email collection selected. Their identity field is Student Registration Number. The generator preserves an existing email-collection mode rather than resetting Verified to typed input. New forms still require these UI settings to be checked. The owner-account synthetic quiz displayed 5/5 and imported it correctly without changing the control or prior Week 1 marks. Google may show a pending icon for the unscored identity field; the importer reads only the five marked questions. No score-release emails were sent.


Hybrid marking also writes one private HTML feedback page per learner in `results/.../feedback/`. These show the final total, executed component, written-criterion feedback and any published execution requirements applied. Unresolved results say “pending”, not zero. Share only the named learner's page; the command does not send messages or publish the folder. Weeks 3–5 retain the deterministic grader's individual text feedback.

## Independent Session 9 checkpoint (draft)

`DataAnalysis_Track/assessment_banks/S09/TASKS.md` specifies a notebook plus a separate accessible PDF/DOCX cleaning log. Executed checks contribute 50/100; the log contributes 50/100, preserving the published 40/40/20 criterion totals. Unseen fixtures vary aliases, rates and categories and include repeat returns. Cleaning functions must preserve their inputs. The reasoning grader reads only the log, not starter prompts or code comments.

After a current passing S09 calibration exists, use:

```sh
python3 IUEA_Teaching_Plan/grader/grade_assessment.py \
  --assessment S09 --cohort DA --prepared prepared/S09 \
  --calibration validated/S09.json --out results/S09
```

This command is not authorized for marks until calibration passes. Session 13/15 numerical contracts and reasoning calibration remain unfinished.

The batch wrapper isolates incomplete packets: their marks remain blank with a correction message while complete packets proceed. Final results are in `results.csv`, importable rows in `import/import_ready.csv`, and individual HTML feedback in `feedback/`. These files remain private until the lecturer distributes them through an appropriate individual channel.

## Assessment release gate

Upload verification and grading readiness are separate. The scheduler permits IUEA W02–W05 and independent S05 through the release gate; normal dates and upload verification still apply. Other assignment forms are held closed by default, including draft later banks. The private **Assessment release** sheet records the audit.

After validating the issued task, deterministic checks and current local rubric calibration, call `setAssessmentRelease('CML3112|W06', true, 'Reference to the exact passing calibration and task-check evidence')`. This is an explicit lecturer release record, not a cloud-side check of local files. Passing a prose calibration alone does not certify the whole assessment. To withdraw release, call the same function with `false` and a reason; the form closes immediately. Existing response timestamps and marks remain intact.

## Optional reasoning-enabled profile

`reasoned_artifact_grade.py` reuses the standard extraction, validation, caching and mark-combination code in an isolated module instance. It enables local model reasoning, allows up to 4,096 generated tokens and a six-minute deadline per request. It has a separate evaluator fingerprint: a standard-profile calibration cannot authorize it.

Evaluate it with `calibrate_rubric.py --profile reasoned --model qwen3.5:4b` and the appropriate rubric/cases/output arguments. The complete known-answer case set must pass. `grade_assessment.py` selects the recorded model and profile from a passing calibration automatically. A two-case diagnostic probe is not sufficient and receives no calibration completion marker. No reasoning-profile rubric is approved until its full report passes.

### Later independent-track numerical components

The fixed sector snapshots and their source hashes are in `DataAnalysis_Track/data/sector_snapshots/`. `scripts/verify_sector_snapshots.py` checks them offline. The draft S13 notebook exposes `SECTOR` and five `FINDINGS` values, with published populations and units. Its isolated specification awards at most 40 Analysis marks; the final DA importer rejects a 40-point component. The remaining 60 marks and complete-packet calibration are still required before release.

For S15, `dashboard_numbers.py --file REPORT.docx --out CHECK.json` verifies five reported revenue/order/AOV contexts from the accessible appendix specified in `DataAnalysis_Track/assessment_banks/S15/NUMERICAL_EVIDENCE.md`. It returns `COMPONENT_ONLY` (20 marks), never final marks or an import-ready CSV. It checks reported numbers against the hashed clean Riverside inputs; it does not execute DAX or prove relationships, interactive filters, design or spoken delivery. Those remain release requirements. Both forms stay held closed.

### Check current calibration coverage

```sh
python IUEA_Teaching_Plan/grader/assessment_readiness.py \
  --evidence review/2026-09-14/rework \
  --out review/2026-09-14/rework/current_readiness.json
```

This reads the locally installed model identities and accepts only completed passing reports that match the current rubric and evaluator. It does not load a model for inference, open any form or change marks. `CALIBRATED` records known-answer coverage; `whole_packet` records a separate successful synthetic packet. Neither replaces the live release gate, dates or Faculty requirements.

The header-only `IUEA_Teaching_Plan/roster_template.csv` is ready for the actual roster. Its technical `student_id` column stores the full **Student Registration Number**, including slashes. Use the assigned course code in `cohort` and the Google-account email students will use for verified submissions in `email`. Keep populated rosters and grade exports private. The template contains no invented student records.

## Verified releases — 15 September 2026

The live audit records 32 assessments eligible for scheduled opening and 20 held. W06, W08–W12 across all three IUEA cohorts and independent S09 were released after current calibration and complete-packet pilots passed. The four independent dates remain unset, so those forms stay closed. Week 1 stays protected. Both exams, both major IUEA projects, DEMO, S13 and S15 remain held for incomplete assessment coverage.

Use the 30 IUEA ZIPs in `../student_packages/` and the S09 ZIP in `../../DataAnalysis_Track/student_packages/`; they contain intended student materials only. Later weekly submissions require one complete notebook, including the student's own `## My written evidence` cell. S09 requires the notebook and a separate accessible PDF/DOCX log in one response.

W08 uses the calibrated atomic criterion mode with local qwen3.5:4b; its full calibration has eleven cases. W06 and W10 also use qwen3.5:4b; W09/W11/W12 use the model recorded in their passing reports. Let the CLI select that model from the report. S09's successful quiet pilot scored 100/100 after an earlier timeout; run inference serially on this 8 GB Mac.

The standard and atomic visual candidates both failed known-answer checks. Neither authorizes final visual-design marks. A document upload working correctly does not mean every criterion in that document can yet be assessed reliably. The remaining coverage is listed in `review/2026-09-14/REWORK_STATUS.md` at the project root.

### A6 and Quiz 6 waiver — 19 October 2026

CML3112 and CML3113: exclude W06 and Q6 from final marks and missing-work flags. The updated gradebook uses best 7 of 10 assignments and best 9 of 11 quizzes, preserving the normal drop allowance and 10% weight for each component. Raw submissions and marks are retained. CML3111 stays best 8 of 11 and best 10 of 12. See `../Practical_Revision_Week6_Waiver.md`. Use this updated `gradebook.gs` for any future gradebook installation. The current collection workbook holds responses and the waiver register; it does not have a `Grades` sheet.
