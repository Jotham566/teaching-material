## 23 October 2026, 20:35 Kampala — Colab URL correction

The exact email-valued `authuser` query returned by the portal reproduced a Colab invalid-authentication error even after the account session was restored. Removed that parameter from both new and resumed Colab links. Verified that the canonical notebook URL opens, and Colab's account selector offers the signed-in learner account with Google's own numeric account routing. No account number is hardcoded into student links. Submission-form account routing is unchanged; it was separately verified in the earlier end-to-end rehearsal. Apps Script version 10 publishes the correction; added a regression assertion that issued Colab URLs contain no `authuser` parameter.

## 23 October 2026 — resumable working notebooks and countdown

Published Apps Script version 9 and Worker `2eb3e01b-8abe-488a-abc6-cde90a542d9b`. New timed allocations use one lecturer-owned notebook privately editable by the named student; editors cannot reshare through Drive. Resume returns that same file and original deadline. Existing reader-original allocations remain in saved-copy mode; their student copies are not overwritten or replaced.

The first identity cell displays a countdown after execution. It uses an absolute deadline, never a new three-hour duration. The display is advisory and uses device time; collection continues to enforce the saved server deadline. Registration matching tolerates whitespace and case only, rejecting different identities and ambiguous duplicate allocations.

Live isolated Apps Script rehearsal passed for all three programmes: editable access for the test account, same notebook URL and same deadline on repeat. Synthetic records are in a separate rehearsal workbook, not the student ledger. Automated checks passed for resume, formatting variants, conflicting identities, strict expiry, global cutoff, countdown rerun/expiry, old-copy handling and existing gateway/collection paths. Notebook timer Python compiles. Live Colab follow-up passed at approximately 20:32 Kampala: signed in as the test account, opened the new CML3111 private editable notebook, executed the top cell and observed a ticking countdown. Added a harmless rehearsal comment, waited for All changes saved, closed the tab, reopened the same notebook and confirmed the comment remained. Rerunning the countdown showed less remaining time, with the original 22:24:42 Kampala deadline unchanged. This was a closed-tab rehearsal, not a physical laptop shutdown or forced network outage. Only synthetic notebook data were edited; no student marks or allocations changed.

## 23 October 2026, 19:19 Kampala — student instructions

Published portal version 8 and Worker version `725d84f5-cf68-4831-8d00-bd99dfefc36e`. Updated the entry page, Test 1 notebook introductions, student instructions/packages and live submission-form descriptions. Instructions cover the unpaused timer, saved working copy, automatic CSV setup, account selection, final form confirmation and technical problems. Previously issued Drive files and student working copies are preserved; updated introductions apply to newly issued files and current downloads.

Verified all three live entry pages and form descriptions. Collector schedule verification confirms CML3111/CML3113 accepting responses, CML3112 closed until 27 October, all with 180-minute duration and the approved global cutoffs; exactly one scheduler trigger remains. No windows or allocations were reset.

Automated timed portal, gateway, collection, export and submission/intake checks passed, including a new regression check for a second Start/Resume click on all three entry pages. Compared all 18 source notebooks with the preceding commit: executable code, question cells and assessment metadata unchanged. This follow-up changed instructions only; the live end-to-end rehearsal documented below remains the submission evidence.

# Colab submission and Mac batch grading verification

## Take-home readiness recheck — 23 October 2026, 19:07 Kampala

- Completed a fresh live Colab → snapshot → Google Form → collector → ZIP export rehearsal in the **separate rehearsal workbook**, using the saved three-hour allocation. The synthetic receipt was COLLECTED at 19:04:38 Kampala, against a saved start of 18:34:51 and deadline of 21:34:51. Export included that receipt plus the older rehearsal, with zero collection issues. No rehearsal marks entered the student cumulative workbook. The rehearsal form was closed afterwards.
- Confirmed the real CML3111 and CML3113 Test 1 forms had opened automatically by 19:07; CML3112 remained closed until 27 October at 19:00. All six test forms have one submission trigger each; one scheduler is installed. Form availability follows the existing five-minute scheduler; portal access and accepted submission timestamps enforce the exact configured times independently.
- Found and fixed a multi-account handoff problem: Google could open the final form under the browser's default email. Submission links now include the learner email as an account hint; verified live that this selected the correct account and preserved all prefilled fields. Issued Colab links also include the account hint. The collector still verifies account ownership; a hint is not authentication. Existing saved notebook copies are not rewritten: their users can use **Switch account** if necessary.
- Published portal version 7 on the existing endpoint, keeping all student entry URLs, QR codes, allocations and deadlines unchanged. Updated all 18 source notebooks and their ZIPs with the submission-link fix.
- Expanded automated timed checks to all nine Test 1 cohort/variant combinations: exact supplied CSV, unchanged task code, recorded learner details, stable file/deadline on resume, strict personal expiry, global cutoff, and missing-timer rejection.
- Reran actual isolated Docker grading for all 18 Test 1/Test 2 reference notebooks: each scored 100/100. The blank-notebook check passed. Portal, gateway, collector, export-menu, intake and submission-helper regression suites passed.
- Decoded all six QR PNGs with OpenCV and fetched each matching live entry page successfully. No physical phone-camera test was performed in this pass.
- Colab authorization stalled in the embedded browser; the normal Edge browser completed the live submission. Students should use a normal browser tab, select their declared Google account, and finish the final Form **Submit** step before their deadline. These checks do not guarantee external Google availability or every student's internet connection.

Historical verification on 19 October 2026. Applies to Test 1 and Test 2 in CML3111, CML3112 and CML3113, variants A/B/C.

## Cloudflare live rehearsal, 19 October 2026, 17:26–18:26 Kampala

The lecturer authorised CML3111 Test 1 to open from 17:26:54 to 18:26:54 Kampala. The exact closing timestamp is enforced by the portal and collector; the existing five-minute scheduler updates the form. Other test windows were not changed.

- Downloaded the issued notebook and matching CSV through both live Cloudflare download buttons. A repeat request returned the same allocation and file contents.
- Opened the downloaded notebook in Colab using the approved rehearsal account in a normal Edge session with multiple Google accounts signed in. No incognito window or account sign-out was needed. The embedded browser had a Colab loading timeout; native Edge completed the flow.
- Ran a synthetic reference solution against the downloaded CSV. The supplied final submission cell was unchanged. Its button saved a snapshot and opened the prefilled form; fields survived switching to the matching Google account.
- Submitted the form and saw “Your response has been recorded.” The collector verified the allocation, identity, ownership and snapshot hash and exported one attempt without collection errors.
- Downloaded the private ZIP and graded it in Docker: GRADED, 100/100. Workbook: `test_operations/grading_output/cloudflare_rehearsal_20261019/graded/Test_Marks.xlsx`.
- Marked the synthetic collection row REHEARSAL so normal student exports exclude it. Its separate local grading ledger cannot affect students’ marks. No marks were sent to students.

This completes the successful live Cloudflare download-to-workbook check for CML3111 Test 1. The other five routes were checked live while closed/future; all 18 packets passed local checks. Physical phone-camera scanning was not performed.

## Original isolated live rehearsal

A separate rehearsal form and workbook were used. No real student marks or real test windows were changed.

- Opened the synthetic notebook in Colab using the approved rehearsal account.
- Ran notebook cells and completed Google authorization with the user's explicit approval.
- Clicked Submit test; the helper captured the live notebook, saved a separate Drive file and granted the lecturer reader access without notification email.
- Opened the generated form. Name, a deliberately freeform registration number, variant, file ID and SHA-256 were correctly prefilled. Google collected the signed-in account email.
- Submitted the form and observed its confirmation page.
- Exported the rehearsal through the same snapshot collector used by production: one notebook collected, zero issues. SHA-256 and source ownership checks passed.
- Downloaded the real exported ZIP from Drive and ran grade_test_batch.py against it on the Mac in the isolated Docker grader.
- Result: GRADED, 100/100, 15 semester points. Correct identity and Kampala submission time appeared in the local workbook. Formula-error scan found no errors. Workbook sheets were rendered and visually checked.
- Closed the rehearsal form after testing. The rehearsal does not contribute to the production ledger.

The in-app browser initially had a runtime connection interruption and a slow authorization prompt. Reconnecting/restarting and authorizing before displaying the button resolved the submission flow. Students should rehearse account authorization before test day.

## Automated checks

- All 18 completed reference notebooks: 100/100 in Docker.
- Blank notebook: zero awarded marks.
- Unfinished cleaning function with other tasks correct: 80/100, preserving independent-task credit.
- Structured interpretation partial credit: correct choices receive their individual 5 marks.
- Identity ledger: duplicate receipt, receipt metadata mismatch, unverified email, conflicting identities, missing/mismatched notebook identity, late submission, infrastructure failure and latest pending attempt checked.
- Collector: source ownership, changed snapshot hash, early/late timestamp, duplicate response and spreadsheet formula text checked.
- Batch import: path traversal, altered bytes, duplicate response IDs and continuation after a bad job checked.
- Repeat batch import: no duplicate attempt or mark.
- Student ZIPs: only notebook, CSV and instructions; no grader, private solutions or answer-key file.
- Existing later-week assessment contract tests passed after separating the new deterministic tests.
- Six PowerPoint test briefings rebuilt, package/layout validation passed, rendered slides checked; matching lecturer notes published.

## Live configuration

All six production forms have Verified email collection, required freeform Student Registration Number, one submission trigger each and a shared five-minute scheduler. A live trigger audit confirmed these. At the original audit, production test windows were unscheduled and closed; subsequent authorised rehearsal windows are recorded above. The lecturer sets dates in the Test windows tab and runs syncColabExams at the start.

The rehearsal was collected on export. Production form-submit triggers were installed and audited; the export also recovers uncollected responses, so batch grading does not depend solely on immediate trigger delivery.

## Limits to keep in mind

No enrolled roster is available. The system records attendees and flags conflicting email/registration combinations; it cannot infer absence or independently establish that a registration number belongs to the person who typed it. Final marks stay blank for unresolved identity or technical errors. Google Forms confirmation acknowledges the response, not successful grading. Keep backups and resolve the workbook's exceptions before releasing marks.

## Test 1 revision alignment and unit grading, 19 October 2026

All three Week 7 decks now contain 68 slides with the same practice CSVs. Added explicit worked examples for list-of-record input/output, non-mutating cleaning, summary dictionaries, returned matplotlib Figures, alphabetical bars, ten-bin histograms, group gap, nested findings with units, and interpretation limits. The revised examples include specific lecturer notes. Current student bundles contain only PDF slides, practice CSV and starting instructions.

Checks completed:
- All six revision sequences execute against their shipped CSVs. The additional two-record exercise produces count 2, mean 15, group gap 0 and ambient replacement 20 without changing the original records.
- Slide-defined practice functions, with only the documented column/function-name mapping, pass the real hidden coding checks in Docker for all three cohorts.
- All 18 completed Test 1/Test 2 reference packets score 100/100. Blank submission and interpretation partial-credit checks pass.
- Celsius aliases pass both actual Figure and findings checks. Fahrenheit and swapped power/energy units fail. Unit comparison does not relax numerical checks.
- The earlier live rehearsal ZIP was graded in a separate output ledger using version 2026.10-colab-v2-units: GRADED, 100/100, workbook generated. No student marks were modified.
- Three PPTX files passed package/layout validation, rendered, and their new worked examples were reviewed. Speaker notes match the source. The timed Cloudflare entry links remain in the decks.

The grader runs locally, so this change requires no portal deployment. Existing ledger receipts remain immutable on re-import; previously graded production attempts would require an explicit regrading workflow. The check above used a separate rehearsal ledger.


## 23 October 2026 — timed take-home Test 1

- Saved and read back all three authorised windows and duration_minutes=180; one existing syncColabExams scheduler trigger remains installed. Test 2 windows and existing submissions were preserved.
- Deployed Apps Script version 6 at the existing endpoint and Worker version 8e0a4d18-090f-4ef2-8be6-49af51e22084 at the existing student host. No student URL or QR payload changed.
- Live requests for all three Test 1 routes before opening return their correct opening date and no files.
- An editor-only rehearsal used a separate synthetic workbook, never the student collection. All three programmes created private Colab files. Repeat requests reused each file and saved personal deadline. The rehearsal function was removed before final deployment.
- CML3111's private notebook opened in Colab as the designated test account. Copy to Drive created an editable student-owned copy. The CSV setup cell ran successfully and loaded 91 rows without a manual file upload.
- Local tests cover persisted identity/timer, repeats, personal expiry, global cutoff, historical allocation migration, accepted on-time snapshot with personal timestamps, missing timer rejection, late form exclusion, all 18 existing packets and six routes, export menu replay/deduplication, and local intake/submission regression tests.
- No new live student form was submitted in this check: the real windows remained closed until the authorised times. Timed collector enforcement was tested with synthetic automated responses; the unchanged snapshot/form flow has its earlier live rehearsal record.
- Entry identity evidence is explicitly unverified. Verified name/email/registration evidence comes from the collected form and matching snapshot owner. No existing marks were modified.

## 23 October 2026 — final live rehearsal of current Test 1 notebooks

All three programmes completed a fresh, isolated rehearsal using the current portal packet generation and collector. Synthetic allocations used separate windows, forms and a workbook; production windows and student marks were not changed. The public Cloudflare pages and all three QR payloads were checked separately. This was not a new student allocation through the production Start button.

| Programme | Issued version | Live collection | Actual snapshot grade |
| --- | --- | --- | --- |
| CML3111 | A | Accepted | 100/100; 15 semester points |
| CML3112 | C | Accepted | 100/100; 15 semester points |
| CML3113 | B | Accepted | 100/100; 15 semester points |

- Opened the private notebooks in Colab, authorized the rehearsal Google account, ran the CSV preparation and reference answers, and used each submission control. All three Google Forms confirmed submission. The collector exported three notebook snapshots with zero collection issues.
- Graded the downloaded export in Docker, not merely the local reference notebooks. Each result contains the correct synthetic name, registration number, email and cohort. The generated Test_Marks.xlsx contains three GRADED rows, each 100/100 and 15 semester points. Re-importing the same ZIP retained exactly three attempts.
- Found that Colab discarded custom cell tags in one saved snapshot. The worker now recognizes the exact paired headers on supplied countdown/submission cells when tags are missing. Literal identity fields are still read without executing browser controls. Regression checks confirm full marks without spurious cell errors, while genuine answer errors remain visible. All three live snapshots now have no cell execution errors.
- Re-ran all nine Test 1 and nine Test 2 reference packets after the worker fix; all score 100/100. Blank/partial-answer checks and nine beginner-workflow tests pass. Intake, submission, batch, cumulative integration, timed portal, gateway, collector and export-menu checks also passed during this review.
- Timed checks cover resuming the same allocation, preserving its deadline, rejecting late submission and enforcing the global cutoff. Production configuration remains CML3111/CML3113: 23 October 19:00–29 October 23:59; CML3112: 27 October 19:00–2 November 23:59, Kampala time. Each attempt lasts at most 180 minutes. One scheduler remains installed.
- Closed the three rehearsal forms and restored the collector's original source after removing temporary rehearsal helpers. Private evidence and the rehearsal workbook remain under test_operations/private and test_operations/grading_output; they are excluded from Git.

Google authorization was slow in the embedded browser; CML3111 completed in normal Edge, and the other two completed in Colab in the embedded browser. This check cannot guarantee Google availability, a student's connection, or every phone/browser. QR payloads were decoded and their destinations checked; a physical phone scan was not part of this run. Students must still finish the Google Form and see its confirmation before their deadline. Grading is the lecturer's batch operation after export, not an immediate student-facing mark.

## 23 October 2026 — opening-time adjustment

At the lecturer's request, changed only CML3111 and CML3113 Test 1 opening times to 24 October 2026 at 11:00 Kampala time. Live read-back confirmed both retain 29 October 23:59 cutoffs and 180-minute attempts. Both forms are currently closed. CML3112 remains 27 October 19:00–2 November 23:59 with 180-minute attempts. The existing scheduler remains installed (one trigger). Updated the stored schedule helper to prevent an accidental reset to the earlier opening time; removed the temporary updater after verification.

## 23 October 2026 — beginner navigation improvements (portal version 16)

Added a Start here checklist (Connect, run support cells, then write answers), explicit run/do-not-edit versus answer instructions, a technical troubleshooting table, and a five-step Save and submit checklist. Existing task headings retain their marks/time estimates. Support cells remain collapsed. The countdown now labels the deadline in Kampala time and shows a non-blocking reminder during the last 20 minutes. The original deadline is unchanged on rerun.

Verified all nine variants against the preceding revision: task prompts, answer-cell code, setup/submission code, CSV bytes and grading specifications are unchanged. All nine Test 1 and nine Test 2 reference packets still score 100/100. Beginner-workflow, missing-cell-tag, partial-answer, timed portal, countdown/reminder, gateway, collector, submission, intake, batch and export-menu tests pass. Published the exact saved Portal.gs + Packets.gs bundle as version 16 at the existing deployment; Google confirmed success. Production schedules and existing issued files were not edited. The three successful live Google Form rehearsals above tested the unchanged submission helper; this guidance-only release did not repeat their OAuth/form submissions.

## 23 October 2026 — synchronize displayed opening dates

Corrected the separately maintained availability text in Index.html and regenerated/deployed the Cloudflare page (Worker version 97b2e5f0-fbe1-4289-b691-ea1b1165ce59). Published matching Apps Script fallback page as version 17. Live HTTP reads of all three routes confirm CML3111/CML3113 show 24 October 11:00 AM–29 October 11:59 PM; CML3112 retains 27 October 7:00 PM–2 November 11:59 PM. Visually confirmed the CML3111 landing page. Updated active checklist, link index and content-review schedule. Historical audit entries above describe the schedule at the time of those checks and are superseded by this entry.

All nine notebook templates have no hard-coded old opening date; issued notebook deadlines continue to come from Test windows and the persisted personal timer. No questions or marking changed. The gateway regression now checks that the human-readable availability text matches the schedule helper, alongside the existing route/allocation/window tests.

## 23 October 2026 — one submission per identity

Applied and read back one_response=true and edits=false on all six Test 1/Test 2 production forms. Added a locked collector guard: a second otherwise-valid response matching either the accepted email or registration (case/whitespace normalized), within the same course/test, is recorded as DUPLICATE_SUBMISSION and omitted from grading exports. Existing responses, collected snapshots and marks were not rewritten. Portal allocation already binds one email and registration to one attempt; resume remains available without resetting the timer. Collector tests cover duplicate email, duplicate registration from another email, repeated receipt idempotence, separate tests, and an earlier failed collection. Timed portal, gateway and export tests passed. Live collector source was replaced with and read back against the canonical combined source, removing accumulated duplicate function definitions from earlier editor updates.
