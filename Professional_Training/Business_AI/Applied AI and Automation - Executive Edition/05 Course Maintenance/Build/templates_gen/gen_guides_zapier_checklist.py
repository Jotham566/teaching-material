"""Zapier Rehearsal Checklist (Word). Called from gen_guides_zapier.py."""
from guide_kit import *

OUT = EDITION / '03 Learner Materials' / 'Practice Files' / '02 Zapier Build'
SHEET = 'Zapier Practice'
CHK_W = [1.1, 7.7, 3.5, 3.6, 1.5]
CHK_H = ['#', 'Verify', 'Where to look', 'Observed (write here)', 'Guide OK? Y/N']


def chk(doc, rows):
    TABLE(doc, CHK_H, [list(r) + [''] * (5 - len(r)) for r in rows], CHK_W, size=9)


def checklist():
    name = 'Zapier Rehearsal Checklist'
    d = new_guide(name, 'For the instructor: prepare the practice sheet and confirm every screen and fact in a real account before Session 6', 'Zapier rehearsal checklist for instructors')
    BOX(d, 'How to use this checklist', [
        'The Zapier Build Guide was written from general knowledge. It has no screenshots and no recorded run. Do not teach from it until you have done this rehearsal in a real account.',
        'Write what you saw in the Observed column. Leave a box empty if you did not check it. Record full runs, with dates, in the Rehearsal Record. Never fill a box from memory or from the guide.'])
    TABLE(d, ['Rehearsal details', 'Fill in'], [[x, ''] for x in (
        'Rehearsed by', 'Date and time', 'Zapier plan or trial seen on screen', 'Google account used', 'Browser and version', 'Trial start date and end date shown')], [7.0, 10.4])

    H1(d, 'A. Prepare the practice sheet "%s"' % SHEET)
    P(d, 'Learners do not build this sheet. They open a view-only link and choose File, Make a copy. Prepare it once, in a Google account that you control.')
    chk(d, [
        ('A1', 'Create a blank Google Sheet named **%s**. Make two tabs named exactly Enquiries and Log.' % SHEET, 'sheets.new'),
        ('A2', 'Enquiries tab, row 1: enquiry_id, received, channel, customer_name, customer_email, message. Row 2: enquiry E01 from sample_enquiries.csv (the first six columns only; leave out expected_category_for_checking_only).', 'Enquiries tab'),
        ('A3', 'Log tab, row 1: logged_at, enquiry_id, ai_output, approved_reply, decision, owner. No other rows.', 'Log tab'),
        ('A4', 'Set sharing: General access, Anyone with the link, role Viewer. Give no edit rights. Optional: change the end of the link from /edit to /copy so that it opens the copy dialog. Test it before you rely on it.', 'Share button'),
        ('A5', 'Test as a learner: open the link in a private window signed in to a second Google account. Choose File, Make a copy. Does the copy hold both tabs, the headings and E01 in row 2?', 'Second account'),
        ('A6', 'Send the link to learners with the "Before Session 6 (15 minutes)" page at least two days before the session. Record the date sent.', 'Email'),
        ('A7', 'Time the "Before Session 6" page with a volunteer on a new Google account: Zapier account created, trial NOT started, sheet copied. Does it fit in 15 minutes?', 'minutes'),
        ('A8', 'Check that the Zapier sign-up does not start a trial by itself. Record what the screen says after sign-up.', 'Zapier sign-up'),
    ])

    H1(d, 'B. The three open questions from the course bible')
    P(d, 'These are the facts that the bible lists under "verify in a real account". They decide whether the build works as written.')
    chk(d, [
        ('B1', 'What does the free trial of the paid plan allow? Number of days, tasks, multi-step Zaps, premium apps including Human in the Loop. Does it ask for card details? What happens on the last day?', 'Pricing page, the trial sign-up screens, the billing page'),
        ('B2', 'Does "AI by Zapier" run on the trial without your own AI key? How many tasks or credits does one AI step use?', 'Add the AI step. Run Test step. Check usage before and after'),
        ('B3', 'Does an external approver (a person with no Zapier login) need a Zapier login to approve or edit in Human in the Loop? Does the emailed link work for a Gmail address that is not the Zap owner?', 'Human in the Loop step settings. Send a request to a second Gmail address and try it'),
        ('B4', 'Fallback A needs no card: create a free account, build the two-step Zap and check that nothing asks for card details.', 'Free account'),
    ])

    H1(d, 'C. Facts the guide states that need a screen to confirm')
    chk(d, [
        ('C1', 'Exact name of the Google Sheets trigger event ("New Spreadsheet Row"?) and what it needs (headings in row 1, at least one row for the test).', 'Trigger step, Test tab'),
        ('C2', 'How often the trigger checks the sheet on the trial (minutes). Time from pasting a row to the Zap starting.', 'Time three runs with a clock'),
        ('C3', 'Names of the AI step events. Which one takes an instruction plus a message and returns text? Are output fields offered?', 'AI by Zapier step, event list'),
        ('C4', 'Human in the Loop: which event lets the reviewer EDIT the draft text, Request Approval or Collect Data? Can the field start filled with the AI output?', 'Both events, try each'),
        ('C5', 'On Reject, does the Zap stop by itself? What is the field name that holds the approval result for the Filter in step 4?', 'Human in the Loop settings, then run a rejection'),
        ('C6', 'Step 4 Filter with two rules joined by AND: "approval result is approved" and "AI output does not contain FLAG". Is the operator called "does not contain"? Is the match case sensitive? Does a reply that contains the lower-case word "flag" stop by mistake?', 'Filter step, Test step'),
        ('C7', 'Does a Filter that stops a run count as a Zapier task? Do the Human in the Loop and Filter steps count? How many tasks does one full run use? (Record the usage number before and after one run.)', 'Usage page'),
        ('C8', 'Do the live test runs (enquiries E01 and E18, section 4 of the guide) fit inside the trial allowance? Total tasks used for the live runs.', 'Usage page after the live runs'),
        ('C9', 'Does the approval request wait for ever, or does it time out? After how long?', 'Step settings, Zapier help'),
        ('C10', 'Where do you set a usage alert? Can you set a cap that stops the Zap?', 'Settings, Billing or Usage'),
        ('C11', 'Name of the run history page (Zap runs, Zap History, Task History) and the status words shown (Success, Waiting, Held, Stopped, Filtered, Error).', 'Left menu, open a run'),
        ('C12', 'Does the Replay button use tasks again?', 'Replay one run and compare usage'),
        ('C13', 'What does the Google sign-in ask to access? Can access be limited to chosen files? Write the exact wording of the permissions.', 'Google consent window for Sheets and Gmail'),
        ('C14', 'Gmail Send Email and Slack Send Direct Message: exact event names. Does a free Slack workspace work? The alternative Gmail trigger (new email matching a search or label): exact name.', 'Action step event lists, trigger list'),
        ('C15', 'Is the To box free text, so a typed address works? Check that the Insert data picker is not filled by default.', 'Gmail Send Email step'),
        ('C16', 'Does the Log step offer a date and time field for logged_at?', 'Create Spreadsheet Row step'),
        ('C17', 'Where are connected accounts listed and removed in Zapier? How is the trial cancelled? Does myaccount.google.com/permissions list Zapier afterwards and allow removal?', 'Zapier connections page, billing page, Google permissions page'),
        ('C18', 'Re-read Zapier\'s trust or security page: SOC 2 Type II and US data hosting (bible section 5). Record the date read.', 'Zapier trust page'),
    ])

    H1(d, 'D. Run the whole build')
    P(d, 'Build the Zap from the guide, step by step, in a copy of the practice sheet. Time yourself. Use the six test rows in section 4 of the guide.')
    chk(d, [
        ('D1', 'Practice sheet copied from the link (two tabs, headings exact, E01 in row 2).', 'minutes'),
        ('D2', 'Instructor build of the six parts live (trigger, AI step, human approval, filter, log, notify), as in the 15-minute slot of Session 6.', 'minutes'),
        ('D3', 'Run 1, E01. Category right? Reply under 80 words? Three-line format kept?', ''),
        ('D4', 'Run 2, E08.', ''),
        ('D5', 'Run 3, E14.', ''),
        ('D6', 'Run 4, E07 (mixed). Did the AI choose complaint and note it?', ''),
        ('D7', 'Run 5, E13 (very short). Did the reply ask which enquiry is meant?', ''),
        ('D8', 'Run 6, E18 (instruction inside the message). Did the AI obey it? Did NOTE say FLAG? Approve the draft on purpose: did the Filter in step 4 stop the run and keep the Log empty? Write what happened. If the AI obeyed the instruction, the guide\'s wording of the lesson is still right, but note it.', ''),
        ('D9', 'A rejection: reject a draft and confirm nothing reaches the Log or the notification.', ''),
        ('D10', 'Paste three rows at once with the Zap off and then turn it on: how many runs start? (Shows the cost risk. Do this only if the trial allows.)', 'runs'),
        ('D11', 'Record the minutes to start and the minutes to review for each run. These feed the new columns of the Automation Test Log. Are the columns clear to a learner?', 'Automation Test Log'),
        ('D12', 'Fallback A: the two-step Zap on a free account, the approval dropdown and the FILTER formula in the Log tab.', ''),
        ('D13', 'Fallback B: print the paper walk-through and time it with a volunteer.', 'minutes'),
        ('D14', 'Clean-up list: complete every item and confirm each worked.', ''),
    ])

    H1(d, 'E. Items collected from the learner guide for confirmation')
    P(d, 'The learner guide no longer carries confirmation markers. It tells learners that their screen may use slightly different names. These are the statements that carried a marker before. Each is also covered by an item above.')
    chk(d, [
        ('E1', 'Which steps count as Zapier tasks on the plan (Words table, Cost watch). See C7.', 'Usage page'),
        ('E2', 'What the trial allows, and whether it asks for card details. See B1.', 'Trial screens'),
        ('E3', 'Whether AI by Zapier runs on the trial without your own key. See B2.', 'AI step'),
        ('E4', 'The names of the alternative Gmail trigger events. See C14.', 'Trigger list'),
        ('E5', 'What the Google sign-in lets you share (selected files). See C13.', 'Consent window'),
        ('E6', 'The trigger check interval. See C2.', 'Clock'),
        ('E7', 'The AI step event names. See C3.', 'Event list'),
        ('E8', 'Which Human in the Loop event allows an edit. See C4.', 'Both events'),
        ('E9', 'Whether someone without a Zapier login can approve. See B3.', 'Second Gmail address'),
        ('E10', 'The approval result field name used by the Filter. See C5 and C6.', 'Filter step'),
        ('E11', 'Whether the Filter counts as a task. See C7.', 'Usage page'),
        ('E12', 'The date and time field offered for logged_at. See C16.', 'Log step'),
        ('E13', 'The Slack and Gmail action names. See C14.', 'Action lists'),
        ('E14', 'Tasks per run (Cost watch). See C7 and C8.', 'Usage page'),
        ('E15', 'The name of the run history page and its status words. See C11.', 'Left menu'),
        ('E16', 'Where the usage alert lives. See C10.', 'Settings'),
        ('E17', 'The name of the connected accounts area. See C17.', 'Zapier settings'),
    ])

    H1(d, 'F. Decisions after the rehearsal')
    TABLE(d, ['Decision', 'Your answer'], [[x, ''] for x in (
        'Is the trial usable for learners in the class (B1, B2)? If not, which fallback is the default for the cohort?',
        'Is the AI step usable without a key (B2)? If not, what do learners bring?',
        'Who approves in class, the learner only, or the instructor too (B3)?',
        'Which Human in the Loop event do you teach (C4)?',
        'Does the Filter with two rules work as the guide says (C6)? If not, what do you teach instead?',
        'Did every learner create a Zapier account without starting the trial before the session (A7, A8)?',
        'Changes needed in the Zapier Build Guide (list section and line):',
        'Changes needed in the Session 6 slides or notes (the slides may still say five steps; the guide says six parts):')], [10.4, 7.0])
    spacer(d, 6)
    P(d, 'Sign-off. I confirmed the items above in a real Zapier account on ____ / ____ / ________ . Items I did not check are left empty.   Signed: ______________________', 9.5)
    save(d, OUT / f'{name}.docx')
