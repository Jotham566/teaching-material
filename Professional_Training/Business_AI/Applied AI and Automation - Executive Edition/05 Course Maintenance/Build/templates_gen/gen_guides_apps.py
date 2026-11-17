"""Apps Script Build Guide and Apps Script Rehearsal Checklist (Word). Run: python3 gen_guides_apps.py"""
from guide_kit import *

OUT = EDITION / '03 Learner Materials' / 'Practice Files' / '03 Apps Script Build'
SHEET = 'NVF Apps Script Practice'
CHK_W = [1.1, 7.7, 3.5, 3.6, 1.5]
CHK_H = ['#', 'Verify', 'Where to look', 'Observed (write here)', 'Guide OK? Y/N']


def chk(doc, rows):
    TABLE(doc, CHK_H, [list(r) + [''] * (5 - len(r)) for r in rows], CHK_W, size=9)


# =============================================================== BUILD GUIDE
def guide():
    name = 'Apps Script Build Guide'
    d = new_guide(name, 'Session 8: a script you can read, run, adapt and measure', 'Apps Script build guide for learners')
    GOLD_BOX(d, 'Read this first', [
        'Your screen may use slightly different names. Follow what you see.',
        'This guide has no screenshots. You read short code and change three words. Your instructor prepares the practice sheet and tries the steps in a real Google account before the session.',
        'The scripts were checked with a test program that stands in for Google\'s services (50 checks pass). That checks the arithmetic and the safety rules. Your own screen is the final check.'])

    H1(d, '1. What you will build')
    P(d, 'Google Apps Script is JavaScript that runs on Google\'s servers, free with a Google account. Your instructor has pasted three scripts into a practice sheet called **%s**. You make your own copy, run the scripts on sample data, read them, and change three words to point one script at your own sample sheet.' % SHEET)
    TABLE(d, ['File', 'What it does'], [
        ['weekly_digest.gs', 'Reads the sheet weekly_sales, adds up each region, works out the change on the week before, lists the total for every week, and saves a **draft** email in your Gmail. It never sends. Sets one weekly trigger if you ask.'],
        ['invoice_check.gs', 'Reads the sheet supplier_invoices and writes every problem to a sheet called Flags: wrong total, duplicate, missing purchase order (PO) number, zero VAT.'],
        ['ai_helper.gs', 'A safe wrapper for one call to the Gemini AI service, plus the run log and the off switch. Used only for an optional three-sentence comment.'],
    ], [4.0, 13.4])
    P(d, 'The practice sheet has three tabs:', keep=True)
    TABLE(d, ['Tab', 'What it holds'], [
        ['weekly_sales', '360 rows of fictional Nile Valley Foods (NVF) sales: 12 weeks, 6 regions, 5 products.'],
        ['supplier_invoices', '60 fictional supplier invoices.'],
        ['hand_summary', 'The Sales Manager\'s hand-made weekly totals for the same 12 weeks. You compare it with the script\'s totals in Step 10.'],
    ], [4.0, 13.4])
    BOX(d, 'The rule of this build', [
        'All arithmetic and all flagging is done by plain code. The AI never adds, compares or flags anything. It may write three sentences about a table the code already built, and you may leave it switched off. Check every AI sentence against the table before you use it.'])
    H2(d, 'Words used in this guide')
    TABLE(d, ['Word', 'Meaning'], [
        ['Script', 'A short program. Here, three files of JavaScript.'],
        ['Trigger', 'In Apps Script, a timer or event that runs a function by itself, for example every Monday. It runs as the account that created it.'],
        ['Script Properties', 'A private store inside the project for secrets such as the AI key. Code reads from it. The key is never typed into the code.'],
        ['Dry run', 'A run that calculates and logs but changes nothing: no draft, no Flags sheet. Every script starts in dry run.'],
        ['Run log', 'A sheet called "Run log". Each run adds one line: time, script, mode, summary.'],
        ['API key', 'A secret code that lets a program use the Gemini service on your account.'],
        ['Sanitised data', 'A copy of real data with names, phone numbers, email addresses, ID numbers and real prices removed or replaced by made-up values.'],
    ], [4.0, 13.4])

    H1(d, '2. Before Session 8: a 10-minute setup')
    P(d, 'This covers your account and its permissions. The practice sheet is already made: your instructor sends you a view-only link, and your first step in class is File, Make a copy.')
    TABLE(d, ['Done', 'What you need'], [
        ['[ ]', 'A **personal Google account** (a free Gmail address is fine), signed in to your browser.'],
        ['[ ]', '**Sample or sanitised data only.** Do not put real customer, staff or supplier data into this exercise. If you want to use a company Google Workspace account, ask your IT team or administrator first. Many companies switch Apps Script or outside services off. A company account needs IT approval. When in doubt, use your personal account and sample data.'],
        ['[ ]', 'Open any Google Sheet and look at the Extensions menu. You should see Apps Script. If it is missing, tell the instructor before the session.'],
        ['[ ]', 'Open myaccount.google.com/permissions once. At the end of the session you remove the access you give today from this page.'],
        ['[ ]', 'Nothing else is needed. The Gemini key is optional (Step 5) and the instructor tells you in class whether to make one.'],
    ], [1.6, 15.8], label_cols=())

    H1(d, '3. Limits to know before you start')
    TABLE(d, ['Limit', 'Value'], [
        ['Email recipients per day, consumer Gmail', '100'],
        ['Email recipients per day, Google Workspace', '1,500'],
        ['Run time for one run of a script', '6 minutes'],
        ['URL fetch calls per day (consumer)', '20,000'],
        ['AI calls per run in these scripts', '3 (a setting you can lower: AI_MAX_CALLS_PER_RUN)'],
        ['Gemini free key', 'Rate limits change. Check them in the Google AI Studio console. Content sent on the free tier may be used by Google to improve its products.'],
    ], [7.0, 10.4])
    P(d, 'Google changes these values from time to time. Your instructor checks them before the session.', 9.5)
    GOLD_BOX(d, 'Sample or sanitised data only, in a personal account', [
        'Use only fake, sample or sanitised data. Do not send customer, staff or supplier personal data, contracts or real figures you would not post in public. The helper refuses rows marked as personal data and text that looks like an email address, a phone number or a national ID number. That is a safety net with gaps, so you remain responsible for what goes in.'])

    H1(d, '4. Build steps')
    H2(d, 'Step 1. Make your copy of the practice sheet')
    NUM(d, [
        'Sign in to your personal Google account. Open the view-only link your instructor sent.',
        'Choose **File**, then **Make a copy**. Name it "%s (mine)" and choose a folder in your own Drive. You own this copy and can change it. The original stays as it is.' % SHEET,
        'Check the three tabs at the bottom: weekly_sales, supplier_invoices and hand_summary. Row 1 of weekly_sales holds week_start, region, product, units, revenue_ugx. Row 1 of supplier_invoices holds invoice_id, date, supplier, description, qty, unit_price_ugx, vat_pct, total_ugx, po_number. Row 1 of hand_summary holds week_start, total_revenue_ugx.',
        'Sheets may show week_start as real dates. That is fine. The script reads both dates and text.',
        'Choose **Extensions**, then **Apps Script**. A new tab opens with the editor. Under Files on the left you should see three files: ai_helper, weekly_digest and invoice_check. If you see them, go to Step 2. If you see only Code.gs or an empty list, use the box below.',
    ])
    BOX(d, 'If your copy has no scripts', [
        'Tell the instructor. They give you the three files ai_helper.gs, weekly_digest.gs and invoice_check.gs.',
        'In the editor, select all the text in Code.gs and delete it. Rename the file to ai_helper (point at the file name, open its menu, choose Rename) and paste in the whole of ai_helper.gs. The editor adds .gs itself.',
        'Next to Files choose the plus sign, then Script. Name it weekly_digest and paste in weekly_digest.gs. Repeat for invoice_check. Choose Save project (the disk symbol). Keep all three files: they share their functions.'])

    H2(d, 'Step 2. Read the code before you run it')
    NUM(d, [
        'Open weekly_digest. Under the heading CHANGE THESE THREE LINES you see the name of the tab, the heading to group by and the heading to add up. You change these in Step 8.',
        'Read the one-line comment above each function. Section 6 of this guide says in plain words what each function does.',
        'Find the line `var DIGEST_DRY_RUN = true;`. While it says true, the script calculates and logs but creates no draft.',
    ])

    H2(d, 'Step 3. First run: the weekly digest as a dry run')
    NUM(d, [
        'In the toolbar choose the function `createWeeklyDigest` from the dropdown, then **Run**.',
        'A box says Authorization required. Choose **Review permissions** and pick your personal account.',
        'A warning page says Google hasn\'t verified this app. This is normal for a script that you or your instructor pasted in. Choose **Advanced**, then **Go to** the project name **(unsafe)**, then **Allow**. The button wording may differ on your screen.',
        'Read the permissions list before you allow. The code reads and writes your spreadsheet, creates Gmail drafts and can call outside web services. Google words the Gmail permission broadly (read, compose and send email) even though the code only creates drafts. That is why you use a personal account with sample data.',
        'After Allow, the run starts. When it ends, open the Execution log at the bottom. The script is in dry run, so it prints the email text and creates no draft. The text shows the table for each region, then the total for every week in the sheet.',
        'Open the new Run log tab in the sheet. One line says dry-run and shows the rows read, the latest week and the total.',
        'Check the total yourself. In any empty cell of a new tab type a formula that adds the latest week, for example `=SUMIFS(weekly_sales!E:E, weekly_sales!A:A, "<the latest week>")` (check the column letters on your sheet). The number must match the script. If it does not, stop and tell the instructor.',
    ])

    H2(d, 'Step 4. The invoice check')
    NUM(d, [
        'Choose the function `runInvoiceCheck` and run it. The Execution log lists the flags. The Run log shows how many invoices were read and how many flags of each type.',
        'In the file invoice_check find the line `var INVOICE_DRY_RUN = true;`, change true to false, save and run again. Now a Flags sheet appears with one row per problem.',
        'Pick three flags and check them by hand with a calculator: quantity times unit price times (1 plus VAT rate) against the total. The instructor tells you how many problems exist after you have counted yours.',
        'One setting needs your eye: `TOTAL_INCLUDES_VAT`. It is true when the total on the invoice already includes VAT. Look at one correct-looking invoice and confirm which way your data works.',
    ])

    H2(d, 'Step 5. Store the Gemini key (optional)')
    P(d, 'Skip this step if you do not want the AI comment. The digest works without it.')
    NUM(d, [
        'Open Google AI Studio (aistudio.google.com) with your personal account and create an API key (the screen is called something like "Get API key"). Copy it.',
        'In the Apps Script editor choose **Project Settings** (the gear symbol on the left). Scroll to Script Properties and choose **Add script property**.',
        'Name: `GEMINI_API_KEY`. Value: paste the key. Choose **Save script properties**.',
        'Never paste the key into the code, a chat, an email or a screenshot. If it leaks, delete it in AI Studio and make a new one.',
    ])

    H2(d, 'Step 6. Turn on the AI comment and create the draft')
    NUM(d, [
        'In weekly_digest set `DIGEST_DRY_RUN = false` and `USE_AI_COMMENTARY = true`. Save and run `createWeeklyDigest`.',
        'Open Gmail, then Drafts. A draft titled "Weekly sales digest (draft)" sits there. Nothing was sent. The table comes from the code. The last paragraph, labelled as an AI comment, is from Gemini.',
        'Read the three sentences against the table. Does every number in them match? Write down what you find.',
        'If the log says the AI was skipped, the reason is in the Run log: no key, an http code, or the call limit. The draft is still created without the comment.',
        'If you see "model not found" or http 404, the model name is out of date. In ai_helper change the text in `var GEMINI_MODEL` to a current model name from AI Studio. Model names change. The address in `GEMINI_BASE_URL` can change too. The instructor tells you if it has.',
    ])

    H2(d, 'Step 7. Test with sample data only')
    NUM(d, [
        '**Figures:** the total matches your SUMIFS formula (Step 3).',
        '**Change:** pick one region and calculate this week minus last week by hand. It matches the table and the percent is right to one decimal.',
        '**Break it on purpose:** rename the tab weekly_sales to weekly_sales2 and run. The script stops with a plain message and writes an error line in the Run log. Rename it back.',
        '**Bad data:** blank one revenue cell. The script skips that row and reports how many rows it skipped, in the email text. Put the figure back.',
        '**Safety:** confirm that only drafts appear in Gmail and nothing appears in Sent.',
    ])

    H2(d, 'Step 8. Change three words (adapt to your own sample sheet)')
    P(d, 'Use a sheet of your own task that holds only sample or sanitised data, in your personal account. Delete the personal data columns and replace real amounts by made-up values. A real company sheet in a company account needs IT approval first. Keep dry run on for the first runs.')
    P(d, 'In weekly_digest, at the top, you change three lines:', keep=True)
    CODE(d, "var SALES_SHEET_NAME = 'weekly_sales';  // CHANGE 1: the name of your tab\n"
            "var GROUP_COLUMN = 'region';            // CHANGE 2: the heading to group by\n"
            "var VALUE_COLUMN = 'revenue_ugx';       // CHANGE 3: the heading to add up")
    NUM(d, [
        'Keep the single quotes around each name. Type the heading exactly as it is in row 1, including capitals and spaces.',
        'Your sheet needs a column with the week or date. It is called week_start in the code (`PERIOD_COLUMN`). Rename your heading to week_start or change that one line as well. Dates should be real dates or in year-month-day order.',
        'In invoice_check change `INVOICE_SHEET_NAME` and, if your headings differ, the right-hand text in `INVOICE_COLUMNS`.',
        'If the script says there is no sheet or no column with your name, you have a spelling difference. Fix the text and run again.',
    ])

    H2(d, 'Step 9. Set the trigger')
    NUM(d, [
        'Choose the function `setupWeeklyTrigger` and run it once. It creates one trigger for `createWeeklyDigest` that runs every Monday between 7:00 and 8:00. Google picks a moment inside that hour. Change `DIGEST_WEEKDAY` and `DIGEST_HOUR` first if you want another time (`DIGEST_HOUR = 7` means between 7:00 and 8:00).',
        'Open Triggers (the clock symbol on the left). You should see exactly one trigger. Running `setupWeeklyTrigger` again replaces it and never adds a second.',
        'A trigger runs even when the sheet is closed. It runs as its owner, the account that created it. If that account is deleted or loses access to the sheet, the trigger stops. Write the owner\'s name in the test log. In a company, the owner is a named person\'s company account and a second person checks the trigger each month.',
        'Leave `DIGEST_DRY_RUN = true` until you trust the numbers. A dry run each Monday still writes a line to the Run log, so you can watch it work.',
        'Open Executions (left side) later to see each run, how long it took and any error.',
    ])

    H2(d, 'Step 10. Measure the time saved and the errors')
    P(d, 'Use the Automation Test Log template. It has one column for the minutes by hand, one for the minutes to start and one for the minutes to review, and it adds start and review for you.')
    TABLE(d, ['Measure', 'How'], [
        ['Time by hand (your baseline)', 'This is the baseline on your Task Card. Time **one region** by hand: find its rows for the latest week, add the revenue and work out the change on the week before. Multiply by the number of regions. Example: 12 minutes for one region and 6 regions is 72 minutes. Write the result on your Task Card and mark it M (measured). For your own task, time one unit of the work (one report, one branch, one customer) and scale it.'],
        ['Time with the script', 'Assisted time is **start plus review**. Start: the minutes from clicking Run to having the draft. Review: the minutes you spend checking the draft against the sheet. Write each in its own column of the Test Log. Do it three times.'],
        ['Errors by hand', 'Open the hand_summary tab: the Sales Manager\'s hand-made summary of the same 12 weeks. **An error is any figure in it that differs from the script\'s total** for the same week. Find each week in the digest under "Total for every week in the sheet" and compare. Count the differences. The instructor tells you the right number after you have counted.'],
        ['Errors with the script', 'Any figure in the script\'s draft that differs from your own SUMIFS check (Step 3). Write what you find, even when it is none.'],
        ['Saving per run', 'Minutes by hand minus (minutes to start plus minutes to review). Multiply by how often you do the task. Count the review minutes as a cost.'],
        ['Cost of an error', 'Take the cost of one error from the "Usual errors" line of your Task Card.'],
        ['Payback', 'Minutes you spent building and adapting, divided by the saving per week. State the answer in weeks.'],
        ['Decision', 'Keep, change or stop. Write the owner and the review date.'],
    ], [4.0, 13.4])
    P(d, 'NVF illustration (a plan made before any measuring): 90 minutes by hand; with the script 5 minutes to start and 20 to review, which is 25 minutes. In Session 12 you compare a plan like this with what you measured.', 9.5, italic=True)

    H2(d, 'Step 11. Clean up at the end')
    NUM(d, [
        'Run the function `turnEverythingOff`. It deletes every trigger in the project. Open Triggers and check that the list is empty.',
        'Revoke the permission: go to myaccount.google.com/permissions, find the project name under third-party apps and services, and choose Remove access. The screen name may differ on your account.',
        'Delete the Gemini key in AI Studio and delete the Script Property.',
        'Delete the drafts you made. Delete your copy of the practice sheet (this removes the script with it) or keep it with all triggers off.',
    ])

    H1(d, '5. Guardrails')
    TABLE(d, ['Guardrail', 'In this build'], [
        ['Personal account', 'A mistake cannot touch your company mail or files. A company Workspace account needs IT approval.'],
        ['Sample or sanitised data only', 'Free-tier Gemini content may be used by Google to improve its products.'],
        ['Secret in Script Properties', 'The key is never in the code, the log or the address of the call.'],
        ['Drafts only', 'No script can send an email. The tests check that sendEmail is never used.'],
        ['Dry run first', 'Every script starts in dry run and says so in the Run log.'],
        ['Call limit', 'At most 3 AI calls per run. A refused call does not use up the limit.'],
        ['Personal data', 'Rows marked yes in the column contains_personal_data and text that looks like an email, phone number or ID number are never sent.'],
        ['Owner and off switch', 'Write your name as owner in the test log. The off switch is the function turnEverythingOff. A trigger runs as its owner and stops if that account is deleted.'],
        ['Run log', 'Every run writes one line, including errors.'],
    ], [4.6, 12.8])

    H1(d, '6. What the main functions do')
    P(d, 'Use this list when you read the code. Each function has a one-line comment above it in the file.')
    TABLE(d, ['Function', 'What it does'], [
        ['createWeeklyDigest', 'Main digest function: read the sheet, build the table, log the run, and unless dry run, save the draft.'],
        ['buildDigest', 'Adds up each group per week and finds the latest week, the week before and the changes. Skips rows with a blank week, group or value and counts them. Plain arithmetic.'],
        ['setupWeeklyTrigger', 'Makes the one weekly trigger.'],
        ['runInvoiceCheck', 'Main invoice function: read the sheet, find the flags, log the run, and unless dry run, write the Flags sheet.'],
        ['checkInvoices', 'Applies the five checks to every row.'],
        ['askGemini', 'One safe call to Gemini. Refuses flagged or personal-looking text, stops at the call limit, never crashes.'],
        ['logRun', 'Adds one line to the Run log.'],
        ['turnEverythingOff', 'The off switch: removes all triggers.'],
    ], [4.6, 12.8])

    H1(d, '7. When it goes wrong')
    TABLE(d, ['What you see', 'Likely cause', 'What to do'], [
        ['No Make a copy choice in the File menu', 'You are not signed in, or you opened the link in a private window.', 'Sign in to your personal account and open the link again. Tell the instructor if it stays missing.'],
        ['Extensions has no Apps Script', 'A company account has switched it off.', 'Use your personal account with sample data.'],
        ['No scripts in your copy', 'The copy did not bring the code with it.', 'Use the box in Step 1.'],
        ['"Authorization is required"', 'You have not allowed the project yet, or access was removed.', 'Run a function again and go through Advanced, then Go to project, then Allow.'],
        ['"There is no sheet named ..."', 'The tab name differs from the setting at the top of the file.', 'Fix the name in CHANGE 1 or INVOICE_SHEET_NAME. Match capitals and spaces.'],
        ['"There is no column headed ..."', 'A heading differs from the setting.', 'Fix CHANGE 2 or CHANGE 3, or the heading in row 1.'],
        ['A total of zero or many rows skipped', 'Numbers stored as text with symbols, or the wrong column.', 'Look at the cells. Remove text such as UGX. Check VALUE_COLUMN.'],
        ['Reason in the Run log: "no key"', 'The Script Property is missing or misspelt.', 'Add GEMINI_API_KEY in Project Settings, Script Properties.'],
        ['http 400, 403, 404 or 429', '400 bad request, 403 key problem, 404 wrong model or address, 429 too many calls.', 'Check the key, the model name in GEMINI_MODEL and the rate limits. Wait for 429. The draft is still made without the comment.'],
        ['"refused: ..."', 'The safety rules blocked the call.', 'This is the design. Remove personal data, or leave the AI off.'],
        ['"Exceeded maximum execution time"', 'The run passed 6 minutes.', 'Use fewer rows or split the work. Turn the AI off.'],
        ['"Service invoked too many times"', 'A daily quota was reached.', 'Stop and try the next day. Check you have no loop or extra trigger.'],
        ['No draft in Gmail', 'Dry run is still true, or the run stopped with an error.', 'Set DIGEST_DRY_RUN to false. Read the Run log.'],
        ['The trigger did not run', 'No trigger exists, it was deleted by the off switch, or the owner\'s account was deleted or lost access.', 'Open Triggers. Run setupWeeklyTrigger again from an account that can open the sheet.'],
        ['Two triggers appear', 'Another trigger was added by hand.', 'Run turnEverythingOff, then setupWeeklyTrigger once.'],
        ['Too many flags', 'TOTAL_INCLUDES_VAT has the wrong setting for your data.', 'Check one invoice by hand and set the line to true or false.'],
    ], [4.6, 5.6, 7.2], label_cols=())
    save(d, OUT / f'{name}.docx')


if __name__ == '__main__':
    guide()
    import gen_guides_apps_checklist
    gen_guides_apps_checklist.checklist()
