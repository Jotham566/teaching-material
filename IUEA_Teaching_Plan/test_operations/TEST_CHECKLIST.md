# Running and grading the IUEA Colab tests

For Test 1 (Week 7) and Test 2 (Week 14) in CML3111, CML3112 and CML3113.
Students submit during the test; your Mac grades the collected work afterwards. Google AI Plus is not needed. Keep using **wirmbeesubs@gmail.com** for the lecturer forms and Drive files.

## A few days before each test

Share the course’s Week 7 (Test 1) or Week 14 (Test 2) PDF slides **together with their matching practice CSV** from [the revision sharing index](../test_revision/README.md). Students upload that CSV into a blank Colab notebook and follow the worked examples in slide order. Practice is ungraded and needs no form submission. The optional revision ZIP contains only the PDF slides, CSV and starting instructions.

The entry link and QR code may be shared in advance. The portal releases the assigned notebook and CSV only during the enabled test window; opening the page does not open the test. The teaching repository remains public, so this restriction applies to portal downloads, not to copies available elsewhere.

## Before each test

1. Sign into **wirmbeesubs@gmail.com**. Open [Test collection workbook](https://docs.google.com/spreadsheets/d/1BveqLGvv-6C-00TMbUF0qti6VoEnAcRX9K1s9eja8uM/edit), then **Test windows**.
2. Find the correct row, such as `CML3111|TEST1`. Enter the authorised opening and closing times with the Kampala offset: `YYYY-MM-DDTHH:MM:SS+03:00`. Set **enabled** to `YES`. Dates must be real dates, with closing later than opening. Do not copy example dates as the actual schedule.
3. Open [Assignment Controls in Apps Script](https://script.google.com/home/projects/1XLdUAzi6wnSjQ2iFTV3hl5BQk9XWw-PIi1_vodC_l107B6S13yW_ZObw/edit). Select **Colab_Test_Collection.gs**, choose **syncColabExams** in the function dropdown, and click **Run**. The automatic check also runs every five minutes; run it at the start for immediate opening. The recorded submission time is checked against the exact deadline.
4. Share the course/test entry link or display its QR code from the Week 7 or Week 14 deck. Learners enter their details and download their own notebook and CSV; do not distribute the A/B/C ZIPs to the class. The private Test allocations tab records the assigned version and allocation code. Keep solutions and grader files private.
5. Rehearse the entry page, both downloads and the submission flow before the actual test. In each form’s **Settings → Responses**, keep **Collect email addresses = Verified**, response editing off, and Student Registration Number required with no pattern restriction. Confirm the correct test form opens at its start time.

## If the test entry link will not open

Use the current Cloudflare course/test link from [TEST_ENTRY_LINKS.md](TEST_ENTRY_LINKS.md), or the updated Week 7/14 QR code. Students can open it in their normal browser without signing out or using incognito. Old copies of the decks still contain Google Apps Script links: replace those copies. Colab and the final submission form still use each student’s own Google account.

Google does not support multiple simultaneous account logins for Apps Script web apps: [Google troubleshooting guidance](https://developers.google.com/apps-script/guides/support/troubleshooting).

If the entry page loads but says **“not open yet”** or **“closed”** after Get my test files, the link is working and the test window is restricting downloads. Check the authorised schedule in Test windows. Do not extend a real test just to troubleshoot a browser error.

## Tell students

“Use your own Google account in Colab and in the form. Complete your name and Student Registration Number in the notebook. Run the final submission cell and approve the Google prompt. Click **Submit test**, open the generated form link, check the details, tick the email confirmation box and press **Submit** on the form. Wait for the confirmation. Keep the snapshot in Drive until marks are released. Tell me immediately if anything fails.”

The notebook button prepares a snapshot; **the form’s final Submit records the submission**. No manual notebook download or upload is needed. Students still upload the supplied CSV into Colab when setting up their work. A replacement attempt needs a new snapshot and a new form submission before the deadline.

## After each test

This is a separate workflow from [weekly assignment/quiz grading](../assessment_operations/CONTINUE_GRADING.md). The **Export Grading ZIP** spreadsheet menu currently exports A1–A5/Q1–Q5, not practical tests. Use the test export and `Grade_Tests.command` below for Test 1 and Test 2.

1. Leave the completed window’s **enabled = YES** and its closing time unchanged. It closes by time. This allows delayed collection of responses that were submitted on time.
2. In Apps Script, select **exportCollectedColabTests**, then **Run**. Open the **DOWNLOAD BATCH** link shown in **Execution log** and download that ZIP from Drive. The export collects any outstanding responses first.
3. Start **Docker Desktop** on the Mac. Wait until Docker is running. Double-click **Grade_Tests.command** in this folder. Drag the downloaded ZIP into the Terminal window and press Return. Keep the Mac on until it finishes; the command prevents idle sleep while grading.
4. Open **Test_Marks.xlsx** in `IUEA_Teaching_Plan/test_operations/grading_output/` inside this repository. It also opens automatically after grading. **Current marks** contains the latest on-time attempt per learner/test; **All attempts** preserves the audit; **Collection issues** lists collection or batch problems. Identity includes name, verified email and Student Registration Number.
5. Check that the submission count matches the collection workbook and resolve any pending/error/conflict rows before releasing marks. Blank marks mean unresolved, not zero. Re-running the same batch does not duplicate marks. Keep the ZIP, original snapshots and local results folder private and backed up.

6. After checking the results, follow [the private snapshot save steps](../assessment_operations/CONTINUE_GRADING.md#6-save-the-results-before-another-batch-or-switching-macs) before changing Macs. To include new test marks in the cumulative assessment workbook, use the [production test-ledger integration guidance](../assessment_operations/reference/GRADING.md#tests-and-later-projects); the weekly ZIP command does not import new test results automatically.

Test 1 is marked out of 100 and contributes 15 semester points; Test 2 contributes 20. A later attempt with a technical or identity problem stays pending rather than silently releasing an earlier mark. Students without a submission cannot be labelled absent until you have an enrolled class roster.

## If something fails

- **No button:** connect the Colab runtime and run the final cell; approve the account prompt. Reconnecting may require rerunning the identity and submission cells.
- **Wrong account or collection error:** use the same account that created the snapshot in Colab and submitted the form. Check the Collection tab’s detail column. Do not edit a prepared snapshot.
- **Docker unavailable:** start Docker Desktop and rerun the command. It does not run student code directly on the Mac.
- **Pending grading error:** preserve the batch and results; resolve the technical/identity issue before marking the row final. Do not replace it with zero.
- **Form is closed:** check the correct course/test row and Kampala times, then run syncColabExams. Do not extend deadlines without an explicit teaching decision.

## Account ownership

The Google AI Plus subscription on **jothammartin.wambi@gmail.com** is not used for grading. That account may serve as a rehearsal student account. **wirmbeesubs@gmail.com is still needed** because it owns the submission forms, collection workbook and snapshot folder. No account migration has been performed.
