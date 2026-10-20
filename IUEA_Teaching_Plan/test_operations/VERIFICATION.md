# Colab submission and Mac batch grading verification

Verified on 19 October 2026. Applies to Test 1 and Test 2 in CML3111, CML3112 and CML3113, variants A/B/C.

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
