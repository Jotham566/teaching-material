# Rework status — 15 September 2026

The codebase, teaching materials and live assessment infrastructure have been substantially reworked. **The whole semester is not yet ready for unattended assessment.** Week 2 has a passing local calibration and a successful end-to-end synthetic submission. Later assessment release is now separately gated, so a scheduled date cannot open a draft assignment merely because its upload settings are verified.

The original findings remain in `REVIEW.md`; that document describes the pre-change state. No real student marks or submitted answers were changed. Week 1 earned marks remain protected.

## Completed delivery and content work

- Reconciled Week 2 around Colab, the cohort dataset, proof-of-life notebook, four repair exercises, README/versioning evidence and the actual upload workflow. Built thirty student-only practical packages for Weeks 2–6 and 8–12, plus the separate independent S09 package with live submission links and Kampala deadlines.
- Supplied cohort-specific Week 3–5 practicals and 42 later cohort/variant banks spanning W06, W08–W12, both practical tests and both major projects. Later banks remain draft until all task and marking checks pass.
- Corrected the gradebook's challenge weeks, required headers, mark ranges and identity matching. IUEA and the independent DA track have separate aggregation. Unresolved marks stay blank; letter bands remain withheld pending Faculty policy.
- Corrected DA delivered-order AOV, SQL checkpoint criteria, cleaning/reconciliation guidance, current Power BI routes and capstone timing. The SQL reference now combines repeated return events before joining to sales, preventing inflated gross revenue.
- Updated Week 7/14 exams to typed offline written evidence, with code execution prohibited during Part B, explicit collection time and matching advance briefings. Removed unsupported penalties and obsolete manual-marking/self-reported-score instructions.
- Rebuilt the affected decks and lecturer guides. The geometry inventory covers 60 decks / 1,944 slides with no shapes outside slide bounds. This is not a claim of full visual inspection of every slide. The independent track now contains 356 slides.

## Live forms and identity

- All 52 assignment forms exist, with upload folders and verified-account email collection checked. Opening/expiry is a shared scheduled window; server timestamps determine timeliness even if a trigger runs late. Latest on-time responses are selected as whole packets.
- The new live **Assessment release** gate passed an audit of all 52 forms: 32 are eligible for scheduled opening (IUEA W02–W06 and W08–W12, plus independent S05/S09), and 20 are held closed. Dates and upload readiness still apply to the eligible forms. The four DA dates remain unset, so those forms remain closed. Later releases require an explicit validation-evidence record.
- All 36 quiz forms were checked for immediate score release, visible point values, missed-question feedback and verified email collection. Correct answers remain hidden. The identity field now reads **Student Registration Number** across the IUEA assignment and quiz forms. Slash-separated registration numbers are accepted without restricting programme codes. Current illustrations use the fictional `99/TEST/000/DEMO-X`; live student forms ask for the learner’s own number without a sample.
- A private owner-account quiz submission displayed 5/5 and imported by registration number plus verified email. Unscored registration fields are excluded from quiz arithmetic. Google may show a cosmetic “Final score pending” indicator for that text field.
- A private owner-account assignment test covered two attachments, receipt, replacement response, expiry, local download and grading, and live gradebook import. The latest complete packet was selected; closure occurred five seconds after the test deadline. Control marks and existing Week 1 marks were preserved.
- A separate verified Google account passed the private student rehearsal: two complete two-file uploads and receipts, newest packet selection, immediate quiz 5/5 and local assignment grading 14+6=20. Natural expiry was observed within 28 seconds of the deadline; the student-account view rejected further submissions. The private quiz was closed and temporary QA trigger removed. Evidence: `rework/nonowner-rehearsal/`. Google rejected custom closed-message updates; dates are therefore supplied in the link index and student packages, with the default closed notice retained.

Live URLs, the exact deployed script hash and audit evidence are recorded in `rework/live_setup.json`. The latest release audit is `rework/assessment_release_gate_v2.log`; the earlier audit is retained.

## Automatic grading

Student notebooks and SQL run in restricted Docker containers with no network, no hidden-check or host filesystem access, and bounded resources. Document parsing/rendering is also isolated. Hidden numerical checks execute separately on the lecturer's computer. Practice receipts are never final marks.

The local reasoning service uses loopback Ollama with cloud features disabled. Student work has not been sent to a cloud model. Google Forms uploads themselves remain stored in the lecturer's Google Drive until downloaded; local AI does not make Forms storage local.

Every reasoning result is bound to the input, rubric, evaluator and model hashes. It contains two criterion-level evaluations and supporting excerpts. Failed, incomplete or stale calibration cannot authorize final marks. Disagreement produces an exception with a blank mark. Individual feedback files stay private and are not automatically emailed or published.

Current verified results:

| Assessment | Evidence | Result |
|---|---|---|
| W02 reasoning | `rework/local_calibration_v10.json` | All 7 known-answer cases passed for the current qwen3:4b evaluator. |
| W02 whole packet | `rework/qa_current_v10/` | 14/14 executed + 6/6 reasoning = 20/20; private feedback and import-ready CSV generated. |
| W09 reasoning | `rework/calibration_W09_v2.json` | All 6 cases passed. |
| W09 whole packet | `rework/qa_W09_current_v2/` | 9/9 executed + 11/11 reasoning = 20/20; private feedback and import-ready CSV generated. |
| W11 reasoning and whole packet | `rework/calibration_W11_v2.json`; `rework/qa_W11_complete_v1/` | All 6 cases passed; full synthetic packet scored 20/20 with private feedback and import output. |
| W06 reasoning and whole packet | `rework/calibration_W06_qwen35_r7_v1.json`; `rework/qa_W06_complete_v1/` | All 9 cases passed. The executed cleaning audit supplies 2 verification marks: 12 executed + 8 written = 20/20 in the complete packet. Original criterion totals are preserved. |
| W08 reasoning and whole packet | `rework/calibration_W08_atomic_r5_v1.json`; `rework/qa_W08_complete_v1/` | All 11 cases passed, including valid paraphrases and a contradictory justification. Atomic criterion evaluation; full packet scored 20/20. |
| W10 reasoning | `rework/calibration_W10_qwen35_v1.json` | All 6 cases passed; `qa_W10_complete_v1/` scored the full 20/20. |
| W12 reasoning and whole packet | `rework/calibration_W12_v2.json`; `rework/qa_W12_complete_v1/` | All 6 cases passed; full packet scored 20/20. |
| S09 reasoning and whole packet | `rework/calibration_S09_qwen35_v1.json`; `rework/qa_S09_complete_v3/` | All 6 cases passed; the quiet complete-packet pilot scored 50 executed + 50 written = 100/100 in one inference attempt. |

The separate reasoning-enabled profile timed out on both diagnostic cases (360 seconds each), so it is unapproved. Standard-profile grading remains separate. Complete-packet pilots passed for W06 and W10–W12. S09 first rejected a synthetic manifest lacking the shared response ID; after correcting the fixture, its executed component passed 50/50 but the model timed out, leaving the final mark blank. The quiet retry then passed the complete packet with 100/100. A partially written report is not a passing calibration. Earlier failures are retained.

The independent S09 draft bank adds 50 executed marks plus 50 cleaning-log marks, preserving the original 40/40/20 criterion totals. Unseen tests vary exchange rates, categories and aliases, include repeat returns and reject input mutation. Its required notebook and separate accessible DOCX/PDF log are checked as a complete packet. Its text calibration and quiet complete-packet pilot now pass. Release evidence is recorded, but actual dates are still required before its form can open.

The batch workflow now isolates incomplete individual packets instead of blocking completed learners. TEST2 applies the published leakage-related written-mark cap using the executed split result. The separate DA aggregator preserves 15/15/30/40 weights and withholds a final percentage until all four components are resolved.

## Further findings corrected

- The independent track plan still contained the old four-week/twelve-session schedule, duplicated section numbers, obsolete Power BI limitations and unsupported claims that every activity had been run. Its generator now follows five weeks, fifteen sessions and 45 hours, has ten unique sections and states actual assessment-release limits. `verify_da_plan.py` checks the generated document for this drift.
- Staged and hashed the Bank Marketing full variant, synthetic AI4I data and a fixed Uganda GDP series. Source attribution and interpretation limits are in `DataAnalysis_Track/data/sector_snapshots/README.md`.
- S13 numeric component: five findings per sector, 8 marks each; all three sector packets passed isolated execution. Six focused tests passed, including denominator direction, units, missing GDP and rejection as a final grade.
- S15 reported-value component: five revenue/order/AOV contexts, independently reconciled to SQL and tested through isolated DOCX extraction. Four focused tests passed. The output is explicitly `COMPONENT_ONLY`; it does not certify a live Power BI model.
- Corrected the risk register to use Colab first, preserve both Friday cohorts’ teaching time, and distinguish outage recovery, restricted records storage and unverified workload estimates. The recalculated master workbook retains the 13 applicable formulas without cached errors; the obsolete automatic-marking coverage estimate was deliberately removed.
- Corrected the cohort summary to treat Mechatronics and Robotics Engineering as one combined programme. The actual roster remains authoritative; the sample registration suffix is not used to infer a programme. A header-only IUEA roster template is supplied.
- `assessment_readiness.py` reports current calibration coverage without changing forms or marks. The new `.iuea-grader-env` leaves the old Python 3.9 environment intact.

- Replaced the obsolete platform architecture and weekly quiz operations documents with three-page guides to the actual deployed workflow. Both were rendered and all six pages visually checked.
- Fixed lecturer-note indexing to use actual slide positions, regenerated all deck note records and both guides, and verified all 1,290 directions against 60 saved decks.
- Corrected remaining Week 15 manual-viva/paper-reflection instructions, the unsupported 55-mark blanket penalty, an incorrect split-timing explanation and an overbooked plenary. Individual evidence is uploaded; live and peer feedback are formative; three six-minute demos fit the twenty-minute plenary.
- Submission preparation now rejects missing/unknown cohort mappings and reports missing learners only within the assigned cohort. `missing.csv` records pending absence without manufacturing zero marks.
- Calibration validation now checks the current authored case set, exact input hashes and expected score ranges, preventing older reports from bypassing newly added boundary cases.

## Final alignment and release pass

- Added eighteen cohort-specific weekly upload slides with actual live form links, Kampala deadlines and required written-evidence cells. Removed contradictory homework/manual in-session marking instructions. Weekly student banks now explicitly distinguish graded work from broader project practice.
- Corrected MCAR/MAR/MNAR definitions and removed claims that a missingness pattern establishes its cause. Statistical reference: [National Research Council, Drawing Inferences from Incomplete Data](https://www.ncbi.nlm.nih.gov/books/NBK209900/).
- Corrected the claim that exceeding fold spread establishes a real model improvement. Fold standard deviation is not a significance test or confidence interval; paired results and practical importance matter. Reference: [scikit-learn statistical model comparison](https://scikit-learn.org/1.5/auto_examples/model_selection/plot_grid_search_stats.html).
- Reconciled Weeks 12–13 timing across plans, figures and decks. Every written weekly timeline now covers exactly 180 minutes without gaps or overlap. Week 12 reserves thirty minutes within the work block for the issued individual notebook; project discussion is formative. Week 13 has a 95-minute studio with cohort-sized clinic slots.
- Corrected the independent S13 sector labels to the actual fixed snapshots and S14 date relationship direction. Thirty-one ZIP packages passed archive/allowlist checks without private keys or lecturer files.
- Released nineteen newly validated cohort/assessment combinations through the existing live release controls. The audit checked all 52 forms and held twenty closed. Release does not bypass date, upload, roster or grading checks. Updated and read-back-verified all nineteen corresponding live form descriptions against the issued notebook/log requirements; response counts were preserved (`validated_submission_briefs_v1.log`).
- Added one bounded automatic retry for transport timeouts, plus strict calibration case/input binding. Neither model disagreement nor a low score triggers score-seeking retries.
- Visual review covered twenty-six selected revised slides and nine selected pages of the rendered guides/plans/syllabi; earlier visual evidence remains available. Geometry checks found no shapes outside any of the sixty decks. This is not a claim that every slide was visually inspected.

## Verification

- **103 Python unit/integration tests passed** in 44.559 seconds in the new pinned Python 3.12 grading environment: `rework/test-results/project-environment-full-v3.log`. This includes all engineering cohort reference contracts, SQL isolation and repeated returns, document boundaries, input-preserving cleaning, identity matching, incomplete-packet handling, feedback and mark combination.
- The subsequent S05 packet-handling change passed all 9 focused SQL tests, including two new incomplete/ambiguous-packet cases: `rework/test-results/sql-packets-current-v4.log`.
- All-cohort numerical contracts were rechecked after final bank generation: four tests passed in 18.583 seconds (`rework/test-results/later-banks-final-v4.log`).
- Forms/registry, release-gate, quiz import and quiz-feedback repair checks passed. The new release test proves a verified draft form stays closed during an active time window.
- DA track validation: 41 checks passed; DA deck validation: 24 checks passed; quiz arithmetic validation passed after the latest content edits.
- Prior gradebook self-tests: 74 passed; student practice checks: 18 passed. The 196-notebook synthetic cohort test exposed corrupt inputs, forged checking, cell errors and identity mismatches.
- Master workbook recalculation reported no formula errors. Master plan rendered to 21 pages. Latest IUEA lecturer guide rendered to 45 pages and independent DA guide to 31 pages, with no empty pages.
- Revised Week 7 and S05 checkpoint slides were rendered and visually checked: `rework/content-final-current/`. Earlier Week 2, capstone, exam and operational-document render evidence is retained. The individual HTML feedback output passed content tests and source inspection; browser policy blocked its local-file visual preview.

## Still required

1. Complete the major-assessment evidence routes and their authored known-answer cases. The weekly IUEA rubrics and independent S09 now have passing current calibration and full-packet pilots; this does not validate the remaining assessments.
2. Finish the remaining S13/S15 criteria and complete-packet workflows, plus major-project/exam/demo known-answer cases and release checks. S13 now has 40/100 numerical marks verified across three sectors; S15 has 20/100 reported-value checks. These are partial components, not final grades. Generic prose grading does not establish that an arbitrary notebook, interactive dashboard or repository history is correct.
3. Resolve visual-assessment coverage. Text/notes extraction does not verify presentation design, spoken delivery, animations or interactive dashboard behavior; both standard and atomic visual candidates failed calibration. These marks cannot currently be described as verified automatically.
4. Obtain the actual roster with registration numbers, cohort and verified-account email mapping, and configure the production gradebook. The working live import demonstrations used private synthetic QA records.
5. Supply the independent track's S05/S09/S13/S15 dates, confirm Faculty grading bands and any mandated assessment rules, and rehearse the actual lab/Power BI environment. The separate-account Forms rehearsal has passed.

Operational commands are in `IUEA_Teaching_Plan/grader/README.md`. Distribute only student packages and intended student-facing materials; keep lecturer guides, answer keys, hidden checks and grade exports private.

## Registration example correction

The supplied registration number belongs to a real student and is no longer used as an example. Active generators, tests, setup notebooks, guides and student ZIPs use the explicitly fictional `99/TEST/000/DEMO-X`. The live correction updated 84 IUEA assignment/quiz forms plus two private QA forms; student forms contain no sample in their identity help. Existing response counts were preserved. A recursive scan of 580 current files, including nested Office/ZIP contents, found no remaining occurrence of the real number. All 103 regression tests passed after the fixture change. Original private historical QA/calibration records remain audit evidence, not material to distribute or reuse as current test fixtures. The completed separate-account rehearsal used the new fictional fixture.

## Week 1 catch-up authorized 15 September

CML3112 Week 1 quiz and upload opened at 06:31 Kampala on 15 September; both expire at 11:00 on 22 September, matching the Week 2 upload deadline. Verified from the separate student account; both had zero responses before and after setup. Quiz answers/scoring and existing marks were not changed. Assignment collection is explicitly distinct from grading release: new W01 written grading remains held. The live Assignment links and Assessment release rows were updated. Other cohorts’ Week 1 windows are unchanged. Evidence: `../2026-09-15/week1-catchup/`. Lecturer checklist: `IUEA_Teaching_Plan/Before_Each_Class_Checklist.md`; student announcement: `IUEA_Teaching_Plan/Week2_CML3112_Student_Links.md`.

## Quiz duration correction on 15 September

The instructor clarified that quizzes run for 24 hours from activation. This supersedes the earlier 48-hour standard and the Week 1 catch-up quiz’s extended deadline. Both live scripts were updated and read back; 36 quiz descriptions were checked, response counts preserved, and activation timing tests passed. CML3112 Q1 retains its original 15 September 06:31:20 activation and now closes 16 September 06:31:20 Kampala. W01/W02 uploads remain due 22 September 11:00. Evidence: `../2026-09-15/quiz-24-hours/`. The new lecturer-only repair walkthrough supplies actual code, causes, corrections and cohort CSV names.
