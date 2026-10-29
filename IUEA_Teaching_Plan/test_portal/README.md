# Student test entry portal

## Timed take-home Test 1 (23 October 2026)

Live Apps Script version 6 and the Cloudflare page were updated on 23 October 2026.

See [the current test checklist](../test_operations/TEST_CHECKLIST.md). Test windows column E (`duration_minutes=180`) enables a persisted personal deadline. Test allocations append full name, started_at, personal_deadline, notebook_id and window_opens_at; original allocation columns and collected submissions remain intact. Old rehearsal allocations start their timer only on their first timed request. The collector checks the server-stored timer, independently of the notebook metadata or browser clock.

Issued Colab files are private, shared as reader only with the declared Google account, without notification emails. Students save their own copy and run the bundled CSV setup cell. Entry email is unverified until the Google Form account and snapshot ownership match. The export includes entry identity evidence marked unverified alongside verified collected jobs.


## Deployment status

Published on 19 October 2026 through Cloudflare Workers Free. Students use the Cloudflare links below; Google redirects happen server-to-server, not in their browser. Apps Script version 4 runs as wirmbeesubs@gmail.com with access Anyone and authenticates the Worker using a private Script Property. Historical diagnosis below records earlier access settings.

Student host: https://iuea-test-entry.jothammartin-wambi.workers.dev/

Use a course/test link, not the bare host. All six live routes were checked in the normal multi-account browser. Existing opening times and deadlines were preserved. See [gateway/README.md](gateway/README.md) for deployment and verification details.

Deployment: https://script.google.com/macros/s/AKfycbxRlh_k0QbbgWbTE5gukY4QTEBFJ8Y8BNg9VL38Rtf5cYdq2RS93V6tn6ULgvzevrc/exec

Use the course-specific links in [TEST_ENTRY_LINKS.md](../test_operations/TEST_ENTRY_LINKS.md). Downloads follow the existing Test windows; publication does not open all tests.

Project: https://script.google.com/home/projects/1QHfTCL-vxjaWjrQLvDhg8PlGaHoUDzT5MdvJ7Tz46JK6VSz-4lgYFJay/edit

The separate project contains Portal.gs plus generated Packets.gs in Code.gs, Index.html, and Gateway.gs. It must not contain any administrative functions from the lecturer's collection project. Its only student-callable data function is requestTestFiles. Helper functions end in an underscore and are not callable through google.script.run.

## Cloudflare live rehearsal, 19 October 2026, 17:26–18:26 Kampala

The lecturer authorised CML3111 Test 1 to open from 17:26:54 to 18:26:54 Kampala. The exact closing timestamp is enforced by the portal and collector; the existing five-minute scheduler updates the form. Other test windows were not changed.

- Downloaded the issued notebook and matching CSV through both live Cloudflare download buttons. A repeat request returned the same allocation and file contents.
- Opened the downloaded notebook in Colab using the approved rehearsal account in a normal Edge session with multiple Google accounts signed in. No incognito window or account sign-out was needed. The embedded browser had a Colab loading timeout; native Edge completed the flow.
- Ran a synthetic reference solution against the downloaded CSV. The supplied final submission cell was unchanged. Its button saved a snapshot and opened the prefilled form; fields survived switching to the matching Google account.
- Submitted the form and saw “Your response has been recorded.” The collector verified the allocation, identity, ownership and snapshot hash and exported one attempt without collection errors.
- Downloaded the private ZIP and graded it in Docker: GRADED, 100/100. Workbook: `test_operations/grading_output/cloudflare_rehearsal_20261019/graded/Test_Marks.xlsx`.
- Marked the synthetic collection row REHEARSAL so normal student exports exclude it. Its separate local grading ledger cannot affect students’ marks. No marks were sent to students.

This completes the successful live Cloudflare download-to-workbook check for CML3111 Test 1. The other five routes were checked live while closed/future; all 18 packets passed local checks. Physical phone-camera scanning was not performed.

## Student flow

One course/test link and QR code leads to the entry page. Students enter their name, Google email and freeform Student Registration Number. The server assigns one of the least-used versions at random and privately saves the allocation. The same registration and email retrieve the same allocation on another device or after refresh. Students receive a notebook, its CSV and instructions; there is no version selector and no ZIP extraction.

Downloads are available only within the existing Test windows row. The notebook has the entered identity details filled in. Its final submission cell is collapsed in Colab and includes an opaque allocation code. The code is filled into the submission form automatically. The lecturer collector checks the code against the assigned course/test, registration and verified Google email, then checks the notebook snapshot metadata and hash before copying it privately.

The portal's email is initially self-declared. Actual ownership is checked by the verified Google Form email and Drive snapshot ownership at submission. With no enrolled roster, this does not prove that a registration number belongs to the claimant. It does not prevent students sharing code, and the notebook's internal code is inspectable. The purpose is straightforward distribution and consistent file matching, not a claim of complete cheating prevention.

## Original deployment procedure (historical)

1. Publish as a web app running as wirmbeesubs@gmail.com, available to anyone with a Google account. Obtain the required account authorization.
2. Save the returned /exec URL in data/test_portal_config.json and generate the six links with a URL-encoded test parameter, such as CML3111|TEST1. Generate matching QR PNGs under qr/test_entry.
3. Update only Colab_Test_Collection.gs in the existing private lecturer project with grader/exam_collection.gs. Run enableTestPortalCollection once. This renames the form field, retains its entry ID, and requires portal allocation codes for new submissions. Old collected records are untouched.
4. Build the six Week 7/14 decks from the updated source. Render and inspect the changed slides, links and QR codes before publishing the PPTX files and lecturer notes.
5. Rehearse the live page, returning for the same files, both downloads and a portal-issued notebook submission. Confirm COLLECTED and the correct internal variant in the private ledger. Verify grading with the downloaded batch.
6. Preserve current test windows. Do not open additional real tests for verification without a teaching decision. Use an explicitly authorised rehearsal window.

## Maintaining the files

Run scripts/build_colab_exams.py, then scripts/build_test_portal.py after any test-content change. Update the portal's server source and deployment version so new downloads match the current tests. No solutions or graders are included in Packets.gs.

The private Test allocations tab has one row per course/test and registration number. Do not delete allocations to reshuffle versions. For a genuine typo, verify the student's identity and check existing submissions before correcting the registration/email in that allocation row; keep its allocation code and variant. The student then retrieves the files with the corrected details. Already collected identity conflicts require separate resolution before releasing marks.

### Authorising one fresh attempt after a technical failure

Do **not** delete allocation rows, Collection rows, notebook snapshots, or marks to let a learner retry. The private lecturer collector now includes `authoriseFreshTestAttemptForRegistration(registration, reason)` and `authoriseFreshTestAttempt(key, registration, reason, replacementEmail)`. Run either only in the private collector Apps Script project after checking the technical issue and the learner's identity.

The registration-only helper works when that registration has exactly one currently open test. It records the decision in **Test Retry Authorisations**, preserves the earlier Collection row and snapshot as audit evidence, marks an accepted receipt `SUPERSEDED_FOR_RETRY`, deletes the matching Google Form response so Forms will allow another response, revokes the old allocation code, and clears the old timer/notebook reference. The learner must then revisit the normal entry link with the same registration number and Google email; the portal issues a fresh timer and private notebook.

If a wrong Google account caused the failure, use the keyed function with `replacementEmail` after verifying the correct account. Do not add these administrative functions to `Portal.gs`, the public web app, or the Cloudflare gateway.

## Verification completed locally

- All 18 packets load and contain only student material.
- Stable allocation across repeat requests; 30 synthetic learners distributed 10 per version.
- No files before opening, after closing or when disabled.
- Identity mismatch and email reuse are rejected.
- Freeform registration text, including formula-like text, is stored literally.
- Collector rejects wrong allocation, wrong course or altered identity; legacy letter bypass is rejected after migration.
- All 18 reference solutions still score 100/100; submission-helper and existing collector checks pass.
- Browser preview reviewed. Student and lecturer DOCX guides rendered and visually checked.

## Live verification, 19 October 2026

- CML3111 Test 1 entry accepted the synthetic registration `DEMO / portal` and issued the matching notebook and CSV.
- A repeat request returned a byte-identical notebook, including its allocation code.
- The CSV loaded in Colab under jothammartin.wambi@gmail.com. A synthetic reference solution ran and the final button created a private snapshot.
- The generated form retained the allocation code and snapshot fields through account switching. Submission was confirmed at 15:54 Kampala.
- The lecturer collector exported the attempt with the correct internal version, verified email and no collection errors.
- The downloaded attempt passed isolated Docker grading at 100/100. Test_Marks.xlsx was generated in the private rehearsal output directory. No marks were sent to students.
- The synthetic attempt is retained with REHEARSAL status and excluded from subsequent student exports. The earlier lecturer test attempt remains untouched.
- Six Week 7/14 decks rebuilt, rendered and reviewed. Every QR decoded to its matching course/test URL. Lecturer notes and student/lecturer guides use the portal flow.
- Other test windows were not opened or extended. The existing CML3111 rehearsal window ends at 16:01 on 19 October.

All 18 packet reference solutions passed local isolated grading. One course/test completed the live portal-to-workbook rehearsal; the remaining five use the same shared implementation and were not opened for testing.

## QR and download audit, 19 October 2026

All six final Week 7/14 PPTX QR images and their rendered-slide QR images decode to the correct course/test URL using an independent ZXing decoder. Each PowerPoint hyperlink matches its QR. The production deployment URL and signed-in-user access setting were checked in Manage deployments.

The browser reproduced Google's “unable to open” page after redirecting to `/macros/u/1/`, with two Google accounts signed in. This happens before the portal code runs. The lecturer also reported the same failure in a single-account private window, so multiple accounts are not a confirmed root cause. Further live deployment diagnosis is required; the private-window suggestion is only a troubleshooting step. Do not describe the QR as broken or a closed test as a missing file. A fresh single-account live download remains to be verified after this audit; no real test windows were changed.

The expanded `tests/test_test_portal.cjs` exercises all 18 download packets and compares their questions, CSV and instructions with the current assessment files. It checks correct identity/allocation insertion and disabled, early and expired windows across all six entry points. These are local automated checks, separate from live browser verification.

### Follow-up live diagnosis, 19 October, 16:37 Kampala

The lecturer confirmed the same access error in a single-account private window. Refreshing the original deployment to version 2 did not restore access. A replacement deployment with identical Google-account permissions also returned Google's error before portal execution. Replacement diagnostic endpoint: `https://script.google.com/macros/s/AKfycbx0CfUt_3EWjK9BxI3Gbdp3NNYwfIgWB4CU3F-mj3uhGHPYCMhskLLdVoso4jaKoy4Q/exec`. It has not replaced student links. No test windows, allocation records or marks were changed. Root cause is not yet confirmed.

The lecturer subsequently reported that opening the URL directly works, while scanning fails. Two successful `doGet` calls appeared at 16:38 and 16:39. The original links and Google-account permissions are retained. All six test decks now show the full clickable/copyable URL as well as the QR. All six revised access slides were rendered, visually reviewed, and independently decoded; displayed text, hyperlink and QR match. Phone-scan diagnosis remains pending comparison of the working and failing browser addresses.

## Public access verification, 19 October 2026

The lecturer approved changing the original deployment to Anyone. The saved deployment settings were read back and confirmed. The original six links and QR codes are unchanged; no schedules were edited.

- All six URLs returned HTTP 200 with the correct course/test portal without authentication.
- All six were opened in a fresh Edge InPrivate window without signing into Google. Synthetic requests returned closed for CML3111 Test 1 and not open yet for the other five. None displayed download links.
- Each embedded PPTX QR independently decoded to the matching direct hyperlink.
- Local tests checked all 18 notebook/CSV/instruction payloads and early, expired and disabled windows for all six entry points. Successful downloads were not re-run live because all real windows were closed; the earlier live rehearsal remains documented above.
- An existing multi-account browser still redirected to an account-specific error page. The verified fallback is a fresh private window with no Google sign-in for entry. Google sign-in is still needed for Colab and final form submission. Physical phone-camera scanning remains device-dependent and was not simulated.

Grading output now defaults to `IUEA_Teaching_Plan/test_operations/grading_output/` within this repository. Existing results were moved from the old Application Support location, with all nine file hashes preserved and SQLite integrity verified. The directory is Git-ignored and owner-only. Batch regression tests passed; the one-page lecturer DOCX was updated and rendered for review.
