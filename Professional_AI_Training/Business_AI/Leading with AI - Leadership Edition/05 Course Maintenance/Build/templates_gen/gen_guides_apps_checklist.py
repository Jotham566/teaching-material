"""Apps Script Rehearsal Checklist (Word). Called from gen_guides_apps.py."""
from guide_kit import *

OUT = EDITION / '03 Learner Materials' / 'Practice Files' / '03 Apps Script Build'
SHEET = 'NVF Apps Script Practice'
CHK_W = [1.1, 7.7, 3.5, 3.6, 1.5]
CHK_H = ['#', 'Verify', 'Where to look', 'Observed (write here)', 'Guide OK? Y/N']


def chk(doc, rows):
    TABLE(doc, CHK_H, [list(r) + [''] * (5 - len(r)) for r in rows], CHK_W, size=9)


def checklist():
    name = 'Apps Script Rehearsal Checklist'
    d = new_guide(name, 'For the instructor: prepare the practice sheet and confirm the screens, the AI service and the quotas in a real account before Session 8', 'Apps Script rehearsal checklist for instructors')
    BOX(d, 'How to use this checklist', [
        'The scripts pass offline tests that use hand-written stand-ins for Google\'s services (`node tests/run_tests.js`: 50 checks; `node tests/integration_case_data.js`: 17 checks). Nothing here has been run in a real Google account. Do not teach until sections A to E are done.',
        'Write what you saw in the Observed column and leave a box empty if you did not check it. Record full runs, with dates, in the Rehearsal Record.'])
    TABLE(d, ['Rehearsal details', 'Fill in'], [[x, ''] for x in (
        'Rehearsed by', 'Date and time', 'Account type (personal Gmail or Workspace)', 'Browser and version', 'Gemini model name used')], [7.0, 10.4])

    H1(d, 'A. Prepare the practice sheet "%s"' % SHEET)
    P(d, 'Learners do not build this sheet. They open a view-only link and choose File, Make a copy. Prepare it once, in a personal Google account that you control.')
    chk(d, [
        ('A1', 'Create a blank Google Sheet named **%s**. Make three tabs named exactly weekly_sales, supplier_invoices and hand_summary.' % SHEET, 'sheets.new'),
        ('A2', 'Import weekly_sales.csv and supplier_invoices.csv from 01 Case Company, and last_month_summary_by_hand.csv from 03 Apps Script Build. Use File, Import, Insert new sheet(s), then rename each tab. Delete the empty first tab. Row 1 headings must match the code.', 'File, Import'),
        ('A3', 'Open Extensions, Apps Script. Paste the three scripts: rename Code.gs to ai_helper and paste ai_helper.gs; add weekly_digest and invoice_check. Keep the shipped defaults (dry run true, AI off). Store no key in the project. Save.', 'Editor'),
        ('A4', 'Run createWeeklyDigest once as the owner and read the Execution log. Does it list a total for every week? Do the totals match verify_case_data.py (first week 592,861,000, last week 739,684,000)?', 'Execution log'),
        ('A5', 'Open the hand_summary tab and compare it with the digest\'s weekly totals. Exactly two weeks differ (2026-08-24 and 2026-10-12). Check against hand_summary_errors_key.txt.', 'hand_summary tab'),
        ('A6', 'Set sharing: General access, Anyone with the link, role Viewer. Give no edit rights. Optional: change the end of the link from /edit to /copy so that it opens the copy dialog. Test it before you rely on it.', 'Share button'),
        ('A7', 'Test as a learner: open the link in a private window signed in to a second personal account. Choose File, Make a copy. Does the copy include the three scripts (Extensions, Apps Script)? If not, the guide fallback applies: hand out the three .gs files and tell learners to use the box in Step 1.', 'Second account'),
        ('A8', 'In the copy, run createWeeklyDigest. Does the authorization flow start from the beginning (each copy needs its own permission)? How long does it take?', 'Copy'),
        ('A9', 'Send the link to learners at least two days before Session 8, with the 10-minute setup (section 2 of the guide). Record the date sent.', 'Email'),
    ])

    H1(d, 'B. Before the real account: run the tests and check the data')
    chk(d, [
        ('B1', 'In the folder 03 Apps Script Build run `node tests/run_tests.js`. Record passed and failed. Expected: 50 passed, 0 failed.', 'Terminal'),
        ('B2', 'Run `node tests/integration_case_data.js` (instructor only, needs folders 04 and 05). Expected: 17 passed, 0 failed. One test checks that the hand summary differs from the true weekly totals in exactly two weeks.', 'Terminal'),
        ('B3', 'Do the headings of the full CSV files match the code (week_start, region, product, units, revenue_ugx and invoice_id, date, supplier, description, qty, unit_price_ugx, vat_pct, total_ugx, po_number)?', 'Open both CSV files'),
        ('B4', 'Does total_ugx in supplier_invoices.csv include VAT? The code assumes it does (qty x price x (1 + VAT/100)). Compare 3 correct rows by hand. If not, set TOTAL_INCLUDES_VAT to false in the code and in the guide.', 'Calculator'),
        ('B5', 'Run the invoice check on the full file. Compare the flags with invoice_errors_key.csv: every planted error found, no false flags?', 'Answer Keys'),
    ])

    H1(d, 'C. Google screens and wording')
    chk(d, [
        ('C1', 'Extensions, Apps Script opens the editor. Names of: Files, plus sign, Script, Rename, Project Settings, Script Properties, Triggers, Executions. Does a new project use the V8 runtime? How do you check it?', 'Editor left bar'),
        ('C2', 'The authorization flow: exact wording of the prompts. "Google hasn\'t verified this app", Advanced, "Go to ... (unsafe)", Allow. Same on a personal account and a Workspace account? A Workspace admin may block the step.', 'First Run of a function'),
        ('C3', 'The list of permissions requested. Copy the wording of the Gmail line. Does it say read, compose and send, even though the code only creates drafts?', 'Consent screen'),
        ('C4', 'Where is the Execution log? What does a failed run show?', 'Bottom of editor'),
        ('C5', 'Importing a CSV: do dates in week_start become real dates? Does the script read them? What time zone applies?', 'Sheet import, Run createWeeklyDigest'),
        ('C6', 'Run createWeeklyDigest in dry run, then live. The total matches a SUMIFS formula? A draft appears in Drafts and nothing in Sent? Does the email text show a total for every week?', 'Sheet, Gmail'),
        ('C7', 'Blank one revenue cell: does the draft report how many rows were skipped? (This is the behaviour the Tool Boundary Sheet example describes.)', 'Draft text'),
        ('C8', 'Run runInvoiceCheck live. The Flags sheet shows the right rows? Run twice: does Flags stay the same size?', 'Flags tab'),
        ('C9', 'setupWeeklyTrigger: exactly one trigger? Run it twice: still one? Does turnEverythingOff empty the list?', 'Triggers page'),
        ('C10', 'Does the trigger fire inside the hour you set (the guide says "runs between 7:00 and 8:00")? Set it for the next hour for the rehearsal and record the real time.', 'Executions'),
        ('C11', 'A trigger runs as its owner. In a test account, delete the owner or remove its access to the sheet and record what happens to the trigger. The guide says it stops.', 'Test account, Executions'),
        ('C12', 'Revoking: where is the project listed at myaccount.google.com/permissions and what is the button called? Does Remove access work?', 'Google account page'),
    ])

    H1(d, 'D. Gemini service and quotas')
    chk(d, [
        ('D1', 'Endpoint format. Check the current Gemini API documentation for the generateContent address, the request body and the header for the key. The code uses https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent, the header x-goog-api-key and a body with contents, parts and text. Does it match?', 'Gemini API documentation'),
        ('D2', 'Model name. Which model name works today on a free key? Put it in GEMINI_MODEL (the file ships with gemini-2.5-flash, which may be retired). Record the name and the date.', 'AI Studio model list'),
        ('D3', 'Make one real call from the script with sample data only (USE_AI_COMMENTARY true, live). Record the HTTP code, the seconds taken and the reply text. Is it three sentences?', 'Execution log, Run log'),
        ('D4', 'Does the reply shape match the code (candidates, content, parts, text)? Try a short and a long table. With maxOutputTokens 600, is the comment ever cut short?', 'Reply text'),
        ('D5', 'Free-tier rate limits for the chosen model: requests per minute and per day. Does a class of five learners hit them?', 'AI Studio console'),
        ('D6', 'Re-read the statement that free-tier content may be used to improve Google products and that paid-tier content is not. Record the date and where you read it.', 'Gemini API terms page'),
        ('D7', 'Make a wrong key and a wrong model name on purpose. What HTTP code and message come back? Does the digest still produce a draft?', 'Run log'),
        ('D8', 'Quotas on the day: Gmail recipients per day (consumer 100, Workspace 1,500), 6 minutes per run, URL fetch calls per day (consumer 20,000). Do they match Google\'s quotas page? (Section 3 of the guide.)', 'Apps Script quotas page'),
        ('D9', 'Is the key shown anywhere it should not be (Run log, Execution log, URL)? It should not be.', 'All logs'),
    ])

    H1(d, 'E. Measurement and teach-through timing')
    chk(d, [
        ('E1', 'Measurement method (Step 10). Time one region by hand and multiply by 6. Compare with the 90 minutes on the NVF Task Card. Is the scaling fair?', 'Stopwatch'),
        ('E2', 'Assisted time. Run the digest three times and record minutes to start and minutes to review in the Automation Test Log. Are the two columns clear?', 'Automation Test Log'),
        ('E3', 'Count the errors in the hand_summary tab by comparing it with the digest\'s weekly totals. Expected: 2. Time how long the comparison takes a learner.', 'hand_summary tab'),
        ('E4', 'Time the instructor walk-through of the supplied script (20-minute slot).', 'minutes'),
        ('E5', 'Time a learner doing steps 1 to 4 for the first time (ask a volunteer).', 'minutes'),
        ('E6', 'Time Step 8 (change three words) on a sample sheet with different headings.', 'minutes'),
        ('E7', 'Time the 10-minute setup (section 2) with a volunteer on a new personal account.', 'minutes'),
        ('E8', 'Fallback: run the code with the fixtures in the tests folder in node, shown on the projector if Google is not reachable. Does it work as a demonstration?', ''),
    ])

    H1(d, 'F. Items collected from the learner guide for confirmation')
    P(d, 'These statements in the learner guide were written from general knowledge. Each needs a screen or a page to confirm. The learner text carries no confirmation markers. It tells learners that their screen may use slightly different names.')
    chk(d, [
        ('F1', 'Step 3: wording of the authorization buttons (Review permissions, Advanced, Go to project (unsafe), Allow). See C2.', 'First run'),
        ('F2', 'Step 3: the exact wording of the Gmail permission. See C3.', 'Consent screen'),
        ('F3', 'Step 5: the name of the key screen in AI Studio ("Get API key"?).', 'aistudio.google.com'),
        ('F4', 'Step 6: the GEMINI_BASE_URL address format and the current model name. See D1 and D2.', 'API documentation'),
        ('F5', 'Step 1: File, Make a copy brings the bound script along. See A7.', 'Second account'),
        ('F6', 'Step 9: the trigger runs between 7:00 and 8:00 and stops when the owner\'s account is deleted. See C10 and C11.', 'Triggers, Executions'),
        ('F7', 'Step 11: the screen name for removing access at myaccount.google.com/permissions. See C12.', 'Google account page'),
        ('F8', 'Section 3: the quota values. See D8.', 'Quotas page'),
        ('F9', 'The V8 runtime is the default for a new project. See C1. The guide no longer asks learners to check it.', 'Project Settings'),
    ])

    H1(d, 'G. Decisions after the rehearsal')
    TABLE(d, ['Decision', 'Your answer'], [[x, ''] for x in (
        'Model name to ship in GEMINI_MODEL and in the guide:',
        'Endpoint format confirmed or changed (describe):',
        'Does Make a copy bring the script? If not, who hands out the three .gs files?',
        'Should learners on Workspace accounts use a personal Gmail instead, because of admin blocks or IT approval?',
        'TOTAL_INCLUDES_VAT final setting for the supplied data:',
        'Changes needed in the Apps Script Build Guide (section and line):',
        'Changes needed in the Session 8 slides or notes:')], [10.4, 7.0])
    spacer(d, 6)
    P(d, 'Sign-off. I confirmed the items above in a real Google account on ____ / ____ / ________ . Items I did not check are left empty.   Signed: ______________________', 9.5)
    save(d, OUT / f'{name}.docx')
