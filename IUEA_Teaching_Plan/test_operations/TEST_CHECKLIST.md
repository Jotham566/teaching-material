## Resuming a take-home Test 1

- New allocations now use one private editable notebook. Students return through the same QR/link, enter the same email and Student Registration Number, then select **Resume my test in Colab**. Full name is still required on the entry page. The original deadline stays fixed.
- Students must save regularly. Only saved work survives a lost tab or shutdown. After reconnecting, run the top identity/countdown cell and CSV setup, then their completed code cells to recreate runtime values.
- The top countdown appears after running the first cell. It is a reminder based on device time; the server enforces the actual deadline regardless of the displayed clock or edited notebook.
- Students with older read-only originals must reopen the saved Drive copy containing their answers. The portal labels that route clearly; it never replaces their copy or claims the blank original contains saved work.
- Registration matching ignores whitespace and letter case only. Different digits or programme letters require lecturer review of the original allocation. Do not instruct students to change email accounts to bypass a conflict.

# Running and grading the IUEA Colab tests

## Test 1 take-home windows — October 2026

All times are Kampala time. CML3111 and CML3113: 23 October, 19:00 to 29 October, 23:59. CML3112: 27 October, 19:00 to 2 November, 23:59.

1. Share the existing course-specific test-entry link/QR. Students should read the page before starting and arrange a laptop and internet access.
2. Students enter their full name, Google-account email and Student Registration Number, then click **Start test / Resume my test** only when ready. The server saves one start time. Their deadline is the earlier of start + 180 minutes or the class closing time. Refreshing does not restart it.
3. Click **Open my test in Colab**, sign in with that account, then **File → Save a copy in Drive**. Run the identity cell and **Load the supplied CSV and Python libraries**. The assigned CSV is created automatically; no CSV upload is needed. Downloads remain a backup.
4. Finish the notebook's submission process AND press Submit on its generated Google Form before the personal deadline. Allow 20 minutes for checking and submission. Google Form confirmation records receipt, but does not override a late timestamp.
5. Export practical submissions from the existing spreadsheet menu and run the normal grading command. The collector exports the saved personal opening/closing timestamps, and the local grader checks them again. Late receipts remain in collection issues for review; earlier submissions are not deleted.

Use a normal Chrome or Edge browser tab for Colab and allow its Google authorization window. New links select the entered Google email; still check the account displayed on the final form. If it is wrong, use **Switch account** and choose the same account used in Colab. You do not need to sign out of your other accounts.

Entry names and emails are self-declared. Final submission verifies the Google account and snapshot ownership; use that verified evidence when matching earlier assignments/quizzes. A shared email or similar name alone must not merge different valid registration numbers.

Colab cannot be remotely locked at expiry. The server rejects late work for grading. Timers include setup and internet interruptions; handle genuine exceptions individually with an audit record, not by deleting allocations.


For Test 1 (Week 7) and Test 2 (Week 14) in CML3111, CML3112 and CML3113.
Students submit during the test; your Mac grades the collected work afterwards. Google AI Plus is not needed. Keep using **wirmbeesubs@gmail.com** for the lecturer forms and Drive files.

## A few days before each test

Share the course’s Week 7 (Test 1) or Week 14 (Test 2) PDF slides **together with their matching practice CSV** from [the revision sharing index](../test_revision/README.md). Students upload that CSV into a blank Colab notebook and follow the worked examples in slide order. Practice is ungraded and needs no form submission. The optional revision ZIP contains only the PDF slides, CSV and starting instructions.

The entry link and QR code may be shared in advance. The portal releases the assigned notebook and CSV only during the enabled test window; opening the page does not open the test. The teaching repository remains public, so this restriction applies to portal downloads, not to copies available elsewhere.

## Before each test

1. Sign into **wirmbeesubs@gmail.com**. Open [Test collection workbook](https://docs.google.com/spreadsheets/d/1BveqLGvv-6C-00TMbUF0qti6VoEnAcRX9K1s9eja8uM/edit), then **Test windows**.
2. Find the correct row, such as `CML3111|TEST1`. Enter the authorised opening and closing times with the Kampala offset: `YYYY-MM-DDTHH:MM:SS+03:00`. Set **enabled** to `YES`. Dates must be real dates, with closing later than opening. Do not copy example dates as the actual schedule.
3. Open [Assignment Controls in Apps Script](https://script.google.com/home/projects/1XLdUAzi6wnSjQ2iFTV3hl5BQk9XWw-PIi1_vodC_l107B6S13yW_ZObw/edit). Select **Colab_Test_Collection.gs**, choose **syncColabExams** in the function dropdown, and click **Run**. The automatic check also runs every five minutes; run it at the start for immediate opening. The recorded submission time is checked against the exact deadline.
4. Share the course/test entry link or display its QR code from the Week 7 or Week 14 deck. For timed Test 1, learners enter their details, start their timer and open their private notebook in Colab. For untimed Test 2, they download their notebook and CSV; do not distribute the A/B/C ZIPs to the class. The private Test allocations tab records the assigned version and allocation code. Keep solutions and grader files private.
5. Rehearse the entry page, both downloads and the submission flow before the actual test. In each form’s **Settings → Responses**, keep **Collect email addresses = Verified**, response editing off, and Student Registration Number required with no pattern restriction. Confirm the correct test form opens at its start time.

## If the test entry link will not open

Use the current Cloudflare course/test link from [TEST_ENTRY_LINKS.md](TEST_ENTRY_LINKS.md), or the updated Week 7/14 QR code. Students can open it in their normal browser without signing out or using incognito. Old copies of the decks still contain Google Apps Script links: replace those copies. Colab and the final submission form still use each student’s own Google account.

Google does not support multiple simultaneous account logins for Apps Script web apps: [Google troubleshooting guidance](https://developers.google.com/apps-script/guides/support/troubleshooting).

If the entry page loads but says **“not open yet”** or **“closed”** after Start test / Resume my test (or Get my test files for Test 2), the link is working and the test window is restricting downloads. Check the authorised schedule in Test windows. Do not extend a real test just to troubleshoot a browser error.

## Tell students

“Use your own Google account in Colab and in the form. Complete your name and Student Registration Number in the notebook. Run the final submission cell and approve the Google prompt. Click **Submit test**, open the generated form link, check the details, tick the email confirmation box and press **Submit** on the form. Wait for the confirmation. Keep the snapshot in Drive until marks are released. Tell me immediately if anything fails.”

The notebook button prepares a snapshot; **the form’s final Submit records the submission**. No manual notebook download or upload is needed. For timed Test 1, the setup cell creates the supplied CSV automatically. Untimed Test 2 still uses a manual CSV upload. A replacement attempt needs a new snapshot and a new form submission before the deadline.

## After each test

This is a separate workflow from [weekly assignment/quiz grading](../assessment_operations/CONTINUE_GRADING.md). The **Export Grading ZIP** spreadsheet menu currently exports A1–A5/Q1–Q5, not practical tests. Use **Export Test ZIP** in the **test collection workbook**, then `Grade_Tests.command`, for Test 1 and Test 2.

1. Leave the completed window’s **enabled = YES** and its closing time unchanged. It closes by time. This allows delayed collection of responses that were submitted on time.
2. Open the [test collection workbook](https://docs.google.com/spreadsheets/d/1BveqLGvv-6C-00TMbUF0qti6VoEnAcRX9K1s9eja8uM/edit). Choose **Export Test ZIP → Export latest submissions**. Refresh the workbook once if the menu is missing; authorize the menu script on first use. Choose **View progress / download** and wait for the new export to say **COMPLETE** in **Test Export**. While **Request status** says **PENDING**, the previous download may still be displayed. Open **Download / detail** and download the ZIP unchanged. The export first collects outstanding responses and includes Test 1 and Test 2 across all three programmes, plus collection issues; rehearsal entries are excluded. You can close the browser while it works.
3. Finish any weekly grading run and close both marks workbooks in Excel. Start **Docker Desktop** on the Mac. Wait until Docker is running. Double-click **Grade_Tests.command** in this folder. Drag the downloaded ZIP into the Terminal window and press Return. Keep the Mac on until it finishes; the command prevents idle sleep while grading.
4. Open **Test_Marks.xlsx** in `IUEA_Teaching_Plan/test_operations/grading_output/` inside this repository. It and **IUEA_Continuous_Assessment.xlsx** both open automatically after grading. The command adds the saved Test 1/Test 2 results to the cumulative workbook; no manual import is needed. **Current marks** contains the latest on-time attempt per learner/test; **All attempts** preserves the audit; **Collection issues** lists collection or batch problems. Identity includes name, verified email and Student Registration Number.
5. Check that the submission count matches the collection workbook and resolve any pending/error/conflict rows before releasing marks. Blank marks mean unresolved, not zero. Re-running the same batch does not duplicate marks. Keep the ZIP, original snapshots and local results folder private and backed up.

6. After checking the results, follow [the private snapshot save steps](../assessment_operations/CONTINUE_GRADING.md#6-save-the-results-before-another-batch-or-switching-macs) before changing Macs. The automatic update retains coursework, project marks and previous test attempts. Review the cumulative workbook’s **Review needed** sheet as well as the test workbook. Test 1 and Test 2 keep their existing weights.

Test 1 is marked out of 100 and contributes 15 semester points; Test 2 contributes 20. A later attempt with a technical or identity problem stays pending rather than silently releasing an earlier mark. Students without a submission cannot be labelled absent until you have an enrolled class roster.

## If something fails

- **Export STOPPED or request ERROR:** read **Download / detail**, fix the reported problem, then choose **Export latest submissions** again. A timed-out export is marked STOPPED after about ten minutes. Original submissions are preserved. Repeated clicks while queued/running do not start another export.
- **No button:** connect the Colab runtime and run the final cell; approve the account prompt. Reconnecting may require rerunning the identity and submission cells.
- **Wrong account or collection error:** use the same account that created the snapshot in Colab and submitted the form. Check the Collection tab’s detail column. Do not edit a prepared snapshot.
- **Cumulative update failed:** test results remain saved. Close Excel or fix the reported setup issue, then repeat the same test command with the same ZIP. Previously saved test attempts are reused, not added twice. Finish an interrupted weekly batch before importing tests.
- **Docker unavailable:** start Docker Desktop and rerun the command. It does not run student code directly on the Mac.
- **Pending grading error:** preserve the batch and results; resolve the technical/identity issue before marking the row final. Do not replace it with zero.
- **Form is closed:** check the correct course/test row and Kampala times, then run syncColabExams. Do not extend deadlines without an explicit teaching decision.

## Account ownership

The Google AI Plus subscription on **jothammartin.wambi@gmail.com** is not used for grading. That account may serve as a rehearsal student account. **wirmbeesubs@gmail.com is still needed** because it owns the submission forms, collection workbook and snapshot folder. No account migration has been performed.

## Menu maintenance only

The workbook-bound source is `test_export_menu.gs`. The existing assignment Apps Script project uses `grader/exam_collection.gs` plus `grader/exam_export_menu_listener.gs` (installed together in **Colab_Test_Collection.gs**). Run `installTestExportMenuListener` once after installation; it creates the **Test Export** status tab and one minute-based request listener. Do not run it for each batch. Request cells `D1:E3` and progress cells `A1:B5` are managed by the scripts. Exporting applies existing collection rules and does not alter the authorised opening or closing times.
