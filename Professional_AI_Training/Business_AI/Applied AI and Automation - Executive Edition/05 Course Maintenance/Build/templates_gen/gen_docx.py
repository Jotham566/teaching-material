"""Generate the Word templates and follow-up documents. Run: python3 gen_docx.py"""
from docx_kit import *

W = CONTENT_CM
NVF = 'Examples use the fictional company Nile Valley Foods Ltd (NVF).'


# ---------------------------------------------------------------- Task Card
def task_card():
    name = 'Task Card'
    d = new_doc(name)
    title(d, 'Task Card', 'One page that names your task and records how it performs today. This is your baseline.')
    box(d, 'How to use this page', [
        'Fill the middle column for your own task. Grey italic text is an example from the fictional company Nile Valley Foods Ltd (NVF): type over it, then select it and press Ctrl+Space to turn it black.',
        'In the last column write E if the number is an estimate (your best guess) or M if you measured it (you timed or counted it). Estimates are fine today.'], size=9)
    rows = [
        ['Task', '~Draft and send the Monday sales summary email to the directors', '-'],
        ['Owner (one named person)', '~Peter Okello, Sales Manager', '-'],
        ['How often', '~Every Monday at 8:00', '~M'],
        ['Time today\n(minutes each time, and how many people)', '~90 minutes, one person', '~E'],
        ['Volume\n(how many a month)', '~4 emails a month, each covering 6 regions and 5 products', '~M'],
        ['Hours a month today\n(how often x minutes / 60)', '~4 x 90 minutes = 6 hours a month', '~E'],
        ['Usual errors and what each costs', '~Wrong week selected, or two figures mistyped, in 4 emails out of 10. One error costs about UGX 150,000 in staff time and a correction email.', '~E'],
        ['What better means\n(a number you can check)', '~Draft ready in 10 minutes, checked in 20 minutes, no wrong week', '~E'],
        ['Why this task\n(safest, biggest saving or most visible; give one reason)', '~Safest: low risk, easy to check, and the directors see the result every week', '-'],
    ]
    grid(d, rows, [5.2, 10.4, 1.8], header=['Field', 'Your entry', 'E or M'], min_h=[0.8, 0.8, 0.8, 1.0, 1.0, 1.0, 1.5, 1.2, 1.4], size=9.5)
    spacer(d, 4)
    h2(d, 'Six tests for a good first task', before=4)
    para(d, 'Write Yes or No for each test. Five or more Yes answers make a good first choice.', 9.5, color='404040', after=3)
    grid(d, [
        ['1  It happens at least weekly', '~Yes', '4  A mistake is caught before a customer or the bank sees it', '~Yes'],
        ['2  The inputs exist as text, files or a sheet', '~Yes', '5  One person owns it and will use the result', '~Yes'],
        ['3  I can check a result in a few minutes', '~Yes', '6  I can measure it today: time, volume, errors', '~Yes'],
    ], [6.6, 1.6, 7.6, 1.6], label_cols=(), size=9)
    spacer(d, 4)
    h2(d, 'Sign-off', before=4)
    signoff(d, ['Task owner (name)', 'Signature', 'Date'], [7.4, 6.0, 4.0], height=1.0)
    spacer(d, 3)
    signoff(d, ['Reviewed by sponsor or instructor (name)', 'Signature', 'Date'], [7.4, 6.0, 4.0], height=1.0)
    save(d, TEMPLATES / 'Task Card.docx')


# ------------------------------------------------- Reliability Test Record
def reliability():
    name = 'Reliability Test Record'
    d = new_doc(name)
    title(d, 'Reliability Test Record', 'Three quick tests that show how far you can trust an AI tool on your own task.')
    box(d, 'How to use this record', [
        'Use the same text from your own task for all three tests (for example one customer message, one invoice or one report). Use the same AI tool each time and write its name below.',
        'After each test write what happened, what went wrong, and the check that would catch it. Grey italic text is an example from NVF: type over it. ' + NVF,
        'If you find no problem, write "none found" and say how many times you tried.'])
    h2(d, 'About this record', before=2)
    grid(d, [
        ['Own task', '~Sort 200 customer messages into order, payment, complaint, other', 'Date', '~4 Nov 2026'],
        ['AI tool used', '~(name of the assistant you use)', 'Tested by', '~David Kato, Customer Service Lead'],
    ], [3.0, 7.4, 2.4, 4.6], label_cols=(0, 2), min_h=1.0)
    spacer(d, 6)
    hdr = ['Test', 'What I did', 'Result', 'What went wrong', 'The check that would catch it']
    widths = [3.0, 4.0, 3.1, 3.5, 3.8]
    h2(d, 'Test 1: Ask twice')
    para(d, 'Give the tool the same request two or three times in separate chats. Compare the answers.', 9.5, color='404040', after=3)
    grid(d, [['Ask twice\n\nSame? Different? Different in a way that matters?',
              '~Pasted message 14 ("Thank you, the oil arrived on time. Please do not be late next Friday") three times',
              '~Order, Complaint, Order\nDifferent on 1 of 3 runs',
              '~One run read the word "late" as a complaint',
              '~Fix the category list and add the rule "a compliment with an order is an order". Run each message twice and have a person look at any message where the two runs differ.'],
             ['', '', '', '', '']], widths, header=hdr, min_h=[2.8, 2.0], size=9.5)
    h2(d, 'Test 2: Remove a fact')
    para(d, 'Leave out one fact the answer needs (a date, a number, a name). Does the tool ask for it, or does it invent it?', 9.5, color='404040', after=3)
    grid(d, [['Remove a fact\n\nDid it ask? Did it guess? Did it say so?',
              '~Removed the invoice number from a payment query and asked "which invoice is this about?"',
              '~Guessed',
              '~It named a real-looking invoice number that was not in the text',
              '~Add to the brief: "If a fact is missing, write MISSING and ask me." Check every reference number against the sheet before sending.'],
             ['', '', '', '', '']], widths, header=hdr, min_h=[2.8, 2.0], size=9.5)
    h2(d, 'Test 3: Ask for the source')
    para(d, 'Ask the tool to show exactly where in your text each part of its answer comes from. Check three of the quotes yourself.', 9.5, color='404040', after=3)
    grid(d, [['Ask for the source\n\nIs each quote really in the text?',
              '~Asked for a word-for-word quote behind each category and checked 3 of 20',
              '~2 of 3 correct',
              '~One quote was reworded and one was not in the message',
              '~Search for each quote in the original (Ctrl+F). If it is not found, a person re-reads that item.'],
             ['', '', '', '', '']], widths, header=hdr, min_h=[2.8, 2.0], size=9.5)
    spacer(d, 6)
    h2(d, 'What I conclude for my own task')
    grid(d, [
        ['I can rely on the tool for', '~First sorting of messages, with a person reading every complaint'],
        ['I must always check', '~Reference numbers, amounts and any quote'],
        ['I will not use it for', '~Deciding refunds or replying to customers without a person'],
        ['Next test to run', '~Ten messages with two facts removed, in a second tool'],
    ], [4.6, 12.8], min_h=1.0)
    save(d, TEMPLATES / 'Reliability Test Record.docx')


# ---------------------------------------------------- Reusable Brief
def brief():
    name = 'Reusable Brief Template'
    d = new_doc(name)
    title(d, 'Reusable Brief Template', 'A brief is the instruction you give an AI tool. Write it once, check it, and reuse it every time.')
    box(d, 'How to use this template', [
        'Write one line or short paragraph for each of the seven parts. Grey italic text is an example from NVF: the Monday sales email. Type over it with your own task. ' + NVF,
        'Part 7 matters most. Telling the tool what to say when it is unsure is the cheapest way to stop invented answers.',
        'When your brief works, copy it into a saved note and change only the inputs each time.'])
    rows = [
        ['1  Goal\nWhat should exist at the end, and who will read it?', "~Draft the Monday email to the directors that summarises last week's sales, ready for me to check and send."],
        ['2  Context\nWho we are, who reads it, what they care about', '~Nile Valley Foods Ltd, a food distributor in Jinja. The readers are the directors. They want to see which regions grew or fell and which products drove it.'],
        ['3  Inputs\nExactly what I am giving you', '~The weekly_sales sheet for the last two weeks: region, product, units, revenue in UGX. Use only these figures.'],
        ['4  Constraints\nLength, tone, what to leave out', '~Maximum 150 words. Plain language. Money as UGX with a space (UGX 500,000). Give no reasons for a change unless the sheet shows them. Do not invent figures.'],
        ['5  Output format\nThe exact shape of the answer', '~Subject line. Three bullet points: total revenue and change on the week, best region, weakest region. Then one table of revenue by region.'],
        ['6  How I will check\nWhat I will compare before I send', '~I will add up the table and compare it with the sheet total, and recompute the change for the top two regions myself.'],
        ['7  What to say when unsure\nThe words I want instead of a guess', '~If a figure is missing or two figures disagree, write NOT IN DATA next to it and list your questions at the end. Do not estimate.'],
    ]
    grid(d, rows, [5.0, 12.4], header=['Part', 'Your brief'], min_h=[1.6, 1.8, 1.6, 1.9, 1.6, 1.6, 1.8], size=9.5)
    spacer(d, 8)
    h2(d, 'Ready to paste')
    para(d, 'Replace everything in square brackets with your own text, then paste the whole block into your AI tool.', 9.5, color='404040', after=3)
    t = d.add_table(rows=1, cols=1); fix_table(t, [W]); cell_margins(t, 100, 100, 160, 160)
    c = t.rows[0].cells[0]; cell_borders(c, '808080')
    lines = ['Goal: [what should exist at the end, and who reads it]', 'Context: [who we are, who reads it, what they care about]',
             'Inputs: [what I am giving you; use only these]', 'Constraints: [length, tone, what to leave out]',
             'Output format: [the exact shape of the answer]', 'Checks I will make: [what I will compare]',
             'If you are unsure: [write NOT IN DATA, list questions, do not guess]']
    c.paragraphs[0].text = ''
    for i, l in enumerate(lines):
        p = c.paragraphs[0] if i == 0 else c.add_paragraph(); fmt(p, 0, 3)
        add_run(p, l, 9.5)
    spacer(d, 8)
    h2(d, 'One checked result')
    para(d, 'Run the brief once on real input and record what you found.', 9.5, color='404040', after=3)
    grid(d, [
        ['Date and tool used', '~12 Nov 2026, (name of your assistant)'],
        ['What I checked', '~Table total against the sheet; change on the week for Jinja and Mbale'],
        ['What was wrong', '~Mbale change was rounded to 8% when the sheet gives 7.6%'],
        ['What I changed in the brief', '~Added "give percentages to one decimal place"'],
        ['Would I send it now?', '~Yes, after my 20-minute check'],
    ], [5.0, 12.4], min_h=0.9, size=9.5)
    save(d, TEMPLATES / 'Reusable Brief Template.docx')


# ------------------------------------------------- Tool Boundary Sheet
def boundary():
    name = 'Tool Boundary Sheet'
    d = new_doc(name)
    title(d, 'Tool Boundary Sheet', 'One page that says what an automation or AI assistant may do on its own, what needs a person, and how to stop it.')
    box(d, 'How to use this sheet', [
        'Session 11 is a writing exercise: you build nothing. Fill this sheet for one automation or assistant you might use in your own company, before anyone switches it on. Name the mail label, folder or sheet: "company data" is too vague to enforce. Start narrow: you can widen a limit later.',
        'Grey italic text is an example from the fictional company Nile Valley Foods Ltd (NVF), a supplier email assistant. Type over it.'], size=8.5)
    grid(d, [['Automation or assistant', '~Supplier email assistant', 'Date set', '~16 Nov 2026'],
             ['Owner (one named person)', '~Grace Akello, Operations Manager', 'Reviewed with', '~Joseph Mugisha, Finance Manager']],
         [3.4, 7.0, 2.4, 4.6], label_cols=(0, 2), min_h=1.0)
    spacer(d, 2)
    h2(d, 'The boundary table', before=2, after=1)
    para(d, 'Four rows: read, write, send and spend. Name a place in every cell.', 9, color='404040', after=2)
    grid(d, [
        ['Read', '~One mail label: Suppliers', '~The price list, if a task needs it', '~Other mail, Drive, payroll'],
        ['Write', '~A summary and a draft reply', '~A change to a saved file', '~Delete mail or files'],
        ['Send', '~Nothing', '~Every reply and forward', '~Forward outside NVF alone'],
        ['Spend', '~AI calls under the limit', '~Any extra cost', '~Pay or change a bank detail'],
    ], [2.4, 5.0, 5.0, 5.0], header=['', 'It may', 'A person approves', 'It must never'], min_h=0.8, size=9)
    spacer(d, 2)
    h2(d, 'Controls around the table', before=2, after=2)
    rows = [
        ['Limits\n(cost, count, hours)', '~Cost: at most UGX 20,000 a month for AI calls. Count: at most 20 supplier emails a day. Hours: working days only. These are invented NVF values.'],
        ['The log\n(what it records)', '~Every tool call: the time, the tool, what it did and who approved it.'],
        ['Stop conditions\n(it stops and tells a person when)', '~A line in an email aimed at assistants. A figure that differs from the source.'],
        ['Off switch\n(who, where, how fast)', '~Grace or Joseph remove its access to the Suppliers label. Takes under 2 minutes. If nobody could do this in minutes today, write that here.'],
        ['Tested against the hidden instruction\n(which row stops it?)', '~The Send row: it may send nothing alone, and may never forward outside NVF. The log would show the attempted forward and that nobody approved it.'],
        ['Level of freedom I chose, and why', '~An agent that drafts only: it chooses its steps but cannot send or pay. A person approves every reply.'],
        ['Review date', '~Every 3 months, and after any incident'],
    ]
    grid(d, rows, [5.4, 12.0], header=['Control', 'What I decide'], min_h=[1.0, 0.7, 0.7, 1.0, 1.1, 0.9, 0.6], size=9)
    spacer(d, 2)
    h2(d, 'Approval', before=2, after=2)
    signoff(d, ['Owner (name and signature)', 'Approved by (name and signature)', 'Date'], [6.4, 6.4, 4.6], height=1.0)
    save(d, TEMPLATES / 'Tool Boundary Sheet.docx')


# ----------------------------------------------------- AI Use Policy
def policy():
    name = 'AI Use Policy Template'
    d = new_doc(name)
    title(d, 'AI Use Policy', '[Company name]  |  Version [1.0]  |  Effective [date]')
    box(d, 'How to use this template', [
        'Replace every [square bracket] with your own text and delete this box when you finish. The wording is plain on purpose: every member of staff should understand it in one reading.',
        'Draft it in Session 13, share it with the people it affects, and have your lawyer check it before the owner signs. In class you write sections 3, 4, 5, 7, 8 and 10 (approved tools, the data table, review and records, ownership, incidents and the review date); the other sections can follow.'], size=9)
    S = lambda n, t: h2(d, f'{n}. {t}', before=6, after=2)
    B = lambda t, **k: para(d, t, 9.5, after=3, **k)
    S(1, 'Purpose')
    B('This policy tells everyone at [company name] how we use artificial intelligence (AI) tools at work, so that we gain time and quality without exposing our customers, our staff or our business to harm. [Add one sentence on why the company is adopting AI.]')
    S(2, 'Scope')
    B('It applies to [all employees, contractors and temporary staff] using any AI tool for company work, on company or personal devices. It covers [chat assistants, writing and translation tools, automation tools, and AI features inside software we already use].')
    S(3, 'Approved tools')
    B('Only the tools in this list may be used for company work: [tool 1, plan, owner]; [tool 2]; [tool 3]. Using a tool that is not on the list needs written approval from [role]. The list is kept by [role] at [location]. Each approved tool has a named owner, a company account (never a personal one) and a note of where it keeps our data.')
    S(4, 'What data may and may not go in')
    grid(d, [
        ['Public', 'Already published: prices, product lists, marketing text', '[Yes, in an approved tool]'],
        ['Internal', 'Day-to-day business information: internal emails, sales summaries, process notes', '[Company accounts only]'],
        ['Confidential', 'Supplier agreements, price lists and contracts, financial results, prices not yet announced', '[Written approval of role; never in free or personal accounts]'],
        ['Personal flag', 'Added to any class when the information identifies a living person: names with phone numbers, CVs, payroll, customer details', '[No, unless the tool is approved for personal data and the person in charge of data protection agrees]'],
    ], [2.6, 8.0, 6.8], header=['Data class', 'What it is', 'May it go into an AI tool?'], size=9, min_h=0.9)
    para(d, 'When unsure, treat the data as one level more sensitive and ask [role].', 9, italic=True, before=3, after=2)
    S(5, 'Human review and records')
    B('A person is responsible for everything AI helps to produce. Before anything leaves the company or affects a person, a named reviewer checks it. [List what always needs review: payments, contracts, hiring, customer replies on money, anything legal or tax.] AI never makes the final decision on [hiring, firing, credit, refunds above UGX ____]. The reviewer checks facts, numbers and quotes against the source. For anything sent out, we keep [the prompt, the result and the name of the checker] in [location] for [period].')
    S(6, 'Disclosure')
    B('We tell customers, suppliers and staff when [an AI tool wrote or decided something that affects them, or when they talk to an automated assistant]. Wording to use: "[This was drafted with AI and checked by a member of our team.]" Where we publish AI-assisted work, we keep a record of who checked it.')
    S(7, 'Accounts and ownership')
    B('Every AI tool and automation has a named owner: [role]. Accounts use company email addresses and two-step sign-in. Passwords and API keys are kept in [a password manager] and never in documents or chat. Our prompts and workflows belong to [company name] and are stored in [location]. When an owner leaves, [role] takes over access on the last working day.')
    S(8, 'Incidents')
    B('An incident is any wrong, harmful or leaked output, or any data put into a tool where it should not be. Anyone who notices one tells [role] within [4 hours] by [phone or email]. Nobody is blamed for a report made in good faith. The five steps are: 1 stop or switch off the tool; 2 tell the owner; 3 do the task by hand; 4 record what happened, when and which data in [incident log]; 5 decide who must be told, including customers, staff and the Personal Data Protection Office, and ask [our lawyer]. We fix the cause and update this policy where the incident shows a gap.')
    S(9, 'Training and AI literacy')
    B('Everyone who uses an approved tool completes [a short briefing] before first use and [a refresher every 12 months]. The briefing covers what AI gets wrong, what data may go in, and how to check a result. [Role] keeps the training record.')
    S(10, 'Review date')
    B('This policy is reviewed every [6 months] or sooner after an incident, a new tool or a change in law. Next review: [date]. Policy owner: [role].')
    S(11, 'Approval')
    signoff(d, ['Approved by (name and title)', 'Signature', 'Date'], [7.4, 6.0, 4.0], height=1.2)
    spacer(d, 6)
    t = d.add_table(rows=1, cols=1); fix_table(t, [W]); cell_margins(t, 80, 80, 140, 140)
    c = t.rows[0].cells[0]; cell_borders(c, '808080')
    p = c.paragraphs[0]; fmt(p, 0, 2)
    add_run(p, 'Note on the law. ', 9, True)
    add_run(p, 'In Uganda the Data Protection and Privacy Act, 2019 applies to personal data, including personal data used with AI tools. It sets duties for collecting, using, storing and sharing personal data and, where required, for registering with the Personal Data Protection Office. Companies that serve customers in other countries may face other laws. This template gives general guidance and is not legal advice. Have a qualified Ugandan lawyer review your final policy.', 9)
    spacer(d, 6)
    h2(d, 'Questions to take to my lawyer', before=4)
    for q in ['Which of our AI uses involve personal data?', 'What are our duties under the 2019 Act for each use?', 'Whether and when must we report a breach?',
              'What must a vendor contract say about our data?', 'What must we tell staff and customers?']:
        para(d, '[ ]  ' + q + '  [answer and date]', 9.5, after=2)
    save(d, TEMPLATES / 'AI Use Policy Template.docx')


# ----------------------------------------------- 30-60-90 Check-in Form
def checkin():
    name = '30-60-90 Check-in Form'
    d = new_doc(name)
    pts = [
        (30, 'Day 30 check-in', 'Short and practical: what is running, what did it save, what went wrong.',
         ['~The data-sharing rule is signed and filed (24 Feb). The invoice file is fixed: 0 faults on the recheck. The Monday sales email is drafted by one approved assistant on a company account, from a written brief, and Peter checks every figure before it is sent.',
          '~From 90 to 35 minutes an email, with checking (plan was 25). About 3.7 hours saved this month, from timing four emails.',
          '~Week 2: the wrong week was selected because the sheet had two tabs. The brief now names the tab. The check caught it before sending.',
          '~Rule added: no customer names in prompts. Policy owner named. Roadmap: 2 of 6 actions done, both on time.',
          '~Write the data dictionary (Peter Okello, due 26 Mar).'],
         'Are the Session 13 controls in place? Is gap 1 closed?', '~Yes: policy owner named and the rule signed. Gap 1 (rights) moves from Red to Amber.'),
        (60, 'Day 60 check-in', 'Is it stable, and has anything changed in how we work?',
         ['~The same Monday email routine, plus the weekly stock summary drafted the same way. The data dictionary is done (26 Mar) and phone numbers are masked in the export (2 Apr).',
          '~Total 7.3 hours saved so far, from the Results Tracker.',
          '~One incident: a draft was shared with the wrong person. The boundary sheet now says the assistant drafts only and Peter sends. No stop rule met.',
          '~The policy now lists the two approved tools. Roadmap: 4 of 6 actions done, none late.',
          '~Test retrieval on 20 questions (Grace Akello, due 23 Apr). Start the business case for the invoice check.'],
         'Is any Session 12 stop rule met? Are actions on time?', '~No stop rule met. All four due actions are done on time.'),
        (90, 'Day 90 check-in', 'Decide: continue, expand, pause or stop.',
         ['~The Monday email and stock summary routines continue. The retrieval test ran on 20 questions with known answers: 16 right, none invented.',
          '~Total 11 hours saved. Errors in the Monday email: 0 in the last 6 weeks.',
          '~The cost rose when the assistant was used twice for each email. A limit of 3 uses is now on the boundary sheet.',
          '~Policy reviewed once; the incident section was added. Roadmap: 6 of 6 actions done. Six areas re-scored: 9 of 12 (was 6).',
          '~Present results to the board and ask for approval to apply the method to invoice checking.'],
         'Re-score the six areas. Continue, expand, pause or stop.', '~Re-scored 9 of 12. Decision requested: expand.'),
    ]
    qs = ['1  What is running?\n(the changes to your workflow that are in use, who owns each, and how often)',
          '2  How much time did it save?\n(minutes or hours, and how you know)',
          '3  What went wrong?\n(errors, near misses, complaints, anything stopped)',
          '4  What changed in the policy, the boundary sheet or the data?\n(roadmap actions done)',
          '5  What next?\n(one action, one owner, one date)']
    cum = ['3.7', '7.3', '11.0']
    dates = ['3 Mar 2027', '2 Apr 2027', '2 May 2027']
    done = ['2 of 6', '4 of 6', '6 of 6']
    for i, (day, ttl, sub, ex, test, test_ex) in enumerate(pts):
        if i: page_break(d)
        title(d, ttl, sub)
        if i == 0:
            box(d, 'How to use this form', [
                'Fill one page at day 30, day 60 and day 90 of your 90-day plan. In the NVF example the plan starts on 1 February 2027, so the pages are dated 3 March 2027 (day 30), 2 April 2027 (day 60) and 2 May 2027 (day 90). Your lecturer contacts you by message or call at each of the three dates, and you return this form and your Results Tracker. Answer in a few lines and use numbers from your Results Tracker and your data roadmap where you can. Grey italic text is an example from the fictional company Nile Valley Foods Ltd (NVF). Type over it.'], size=9)
        grid(d, [['Name and company', '~Peter Okello, Nile Valley Foods Ltd', 'Date', f'~{dates[i]}'],
                 ['Own task', '~Monday sales summary email', 'Days since plan start', f'~{day}']],
             [3.2, 7.2, 3.0, 4.0], label_cols=(0, 2), min_h=0.7, size=9)
        spacer(d, 3)
        rows = [[q, e] for q, e in zip(qs, ex)]
        grid(d, rows, [6.0, 11.4], header=['Question', 'Your answer'], min_h=[1.0, 0.8, 0.8, 0.8, 0.7], size=9)
        spacer(d, 3)
        h2(d, 'The test for this check-in', before=2)
        grid(d, [[test, test_ex]], [7.0, 10.4], header=['The test', 'My answer'], label_cols=(0,), min_h=0.8, size=9)
        spacer(d, 3)
        h2(d, 'Result numbers', before=2)
        grid(d, [
            ['Hours saved in this period', '~3.7', 'Cumulative hours saved', f'~{cum[i]}'],
            ['Roadmap actions done (of those planned)', f'~{done[i]}', 'Roadmap actions late', '~0'],
            ['Errors found before release', '~1', 'Errors that reached a customer or the board', '~0'],
            ['Cost this period (UGX)', '~UGX 145,000', 'Baseline minutes a run (Task Card)', '~90'],
        ], [5.0, 3.4, 5.8, 3.2], label_cols=(0, 2), min_h=0.7, size=9)
        spacer(d, 3)
        h2(d, 'Sponsor sign-off', before=2)
        para(d, 'The sponsor is the person who owns the budget or answers to the board for this work.', 9, color='404040', after=3)
        signoff(d, ['Sponsor name and title', 'Decision (continue / expand / pause / stop)', 'Signature and date'], [5.6, 6.2, 5.6], height=1.0)
    save(d, FOLLOWUP / '30-60-90 Check-in Form.docx')


# ------------------------------------------------------ Sponsor Briefing
def sponsor():
    name = 'Sponsor Briefing'
    d = new_doc(name)
    title(d, 'Sponsor Briefing', 'Draft now with planned numbers; update at day 90')
    box(d, 'How to use this page', [
        'One page for the board or owner: plain words, real numbers, one decision. Fill it in now with the planned numbers from your Business Case Workbook and label them plan. At day 90 replace them with the measured numbers from your Results Tracker. Grey italic text is an example from the fictional company Nile Valley Foods Ltd (NVF), with invented figures. Type over it.'], size=9)
    h2(d, 'What we did', before=2)
    grid(d, [['~We changed how the Monday sales email is made. One approved assistant drafts it from the weekly sales sheet using a written brief, and Peter checks every figure before it is sent. We used it every week for 12 weeks. We also fixed the invoice file, wrote a data-sharing rule and a data dictionary, and masked phone numbers in the export. A test of 20 questions with known answers scored 16 right, none invented.']],
         [W], label_cols=(), min_h=0.9, size=9)
    spacer(d, 1)
    h2(d, 'Result against baseline', before=2)
    grid(d, [
        ['Minutes for each email', '~90', '~25', '~35', '~55 fewer'],
        ['Hours a month (4 emails)', '~6.0', '~1.7', '~2.3', '~3.7 saved'],
        ['Emails with an error', '~4 in 10', '~0', '~0 in 12', '~Better'],
        ['Hours saved over twelve runs', '~-', '~13.0', '~11.0', '~2.0 below plan'],
    ], [5.4, 3.0, 2.8, 3.2, 3.0], header=['Measure', 'Baseline (before)', 'Plan', 'Measured at day 90', 'Change on baseline'], min_h=0.7, size=9)
    spacer(d, 1)
    h2(d, 'Cost', before=2)
    grid(d, [
        ['One-off (set-up, data preparation and training)', '~UGX 480,000'],
        ['Each month (tool, review time, upkeep)', '~UGX 145,000'],
        ['Payback on plan numbers (Business Case Workbook)', '~2.8 months. Replace with measured numbers at day 90.'],
    ], [9.0, 8.4], min_h=0.7, size=9)
    spacer(d, 1)
    h2(d, 'Risk', before=2)
    grid(d, [['~One incident: a draft was shared with the wrong person. The boundary sheet now says the assistant drafts only and Peter sends. The policy and the boundary sheet are updated. The remaining risk is a wrong figure that nobody checks, so the owner checks the table total every week.']],
         [W], label_cols=(), min_h=0.9, size=9)
    spacer(d, 1)
    h2(d, 'Stop rules I wrote in advance', before=2)
    grid(d, [['~Stop if one error reaches a customer or the bank. Revise if review minutes rise above 30 an email. Revise if the 12-month net after the haircut turns negative.']],
         [W], label_cols=(), min_h=0.7, size=9)
    spacer(d, 1)
    h2(d, 'Decision requested', before=2)
    grid(d, [['~Approve UGX 600,000 and 30 hours of Joseph Mugisha\'s time to apply the same method to supplier invoice checking, starting in May 2027. We will report in 60 days.']],
         [W], label_cols=(), min_h=0.7, size=9)
    spacer(d, 2)
    grid(d, [['Continue as is', 'Expand', 'Pause', 'Stop']], [W / 4] * 4, label_cols=(), min_h=0.7, size=9)
    para(d, 'Write an X in one box.', 8.5, color='404040', before=2, after=4)
    signoff(d, ['Prepared by (name, role)', 'Decided by (name, role)', 'Signature and date'], [5.6, 5.6, 6.2], height=1.0)
    save(d, FOLLOWUP / 'Sponsor Briefing.docx')


if __name__ == '__main__':
    task_card(); reliability(); brief(); boundary(); policy(); checkin(); sponsor()
