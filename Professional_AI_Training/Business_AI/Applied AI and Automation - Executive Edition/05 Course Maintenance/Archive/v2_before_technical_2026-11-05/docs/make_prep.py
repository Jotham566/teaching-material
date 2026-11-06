"""Session 1 preparation pack (Word and PDF), built from the Session 0 and Session 1 files and the case data so it always matches the slides.
python3 kit/make_prep.py   ->  04 Facilitator Materials/Session 1 Preparation Pack.docx and .pdf"""
import csv
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
import deck  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

S0, S1 = deck.load(0), deck.load(1)
f1 = S1['facilitator']
ids = 'M01 M02 M03 M07 M10 M14 M15 M21 M26 M28 M32 M38'.split()
msgs = {r['id']: r for r in csv.DictReader(open(EDITION / '03 Learner Materials' / 'Practice Files' / '01 Case Company' / 'customer_messages.csv', encoding='utf-8'))}
key = {r['id']: r for r in csv.DictReader(open(EDITION / '04 Facilitator Materials' / 'Answer Keys' / 'customer_messages_key.csv', encoding='utf-8'))}


def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def short(t, n=96):
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' ...'


d = new_doc('Session 1 Preparation Pack', 'Applied AI and Automation, Executive Edition')
title(d, 'Session 1 preparation pack', 'Where AI fits in your business  |  everything you need, in the order you need it')

h2(d, 'Read this first', 0)
para(d, 'This pack takes you from the end of Session 0 to the end of Session 1, in time order. It says what to send, what to set up, what to build, what to rehearse, what to say and what you should see. The demonstration results are already on the slides, so you do not need to switch between tools in class. The keyword rule result is exact, because it is plain arithmetic on the text. The AI result comes from three runs of the exact prompt with Claude on 4 November 2026, with the answer key hidden (page 6). It is not ChatGPT or Gemini, so say whose result it is. If you run another assistant yourself, record what you saw and do not describe results you did not see.', 10, after=4)

h2(d, 'The plan at a glance')
grid(d, [['Today', 'Finish Session 0, hand out the handbook, send the preparation message (page 2).'],
         ['Within 2 days', 'Install and test your tools and accounts (page 3). Print the learner sheets.'],
         ['The day before', 'Read the results (pages 4 to 6). Rehearse the person step. Building the sheet and a live AI run are optional (pages 4 to 7).'],
         ['The morning', 'Pack the kit, open the tabs, smoke-test the projector and the internet (page 8).'],
         ['In class', 'Follow the minute-by-minute run sheet (pages 8 to 10).'],
         ['Straight after', 'Save, send the follow-up message, update the Rehearsal Record (page 11).']], [3.2, 14.2], header=['When', 'What'], size=9.5)

# ------------------------------------------------------------ today: finish session 0
page_break(d)
h2(d, 'Today: finish Session 0', 0)
para(d, 'Session 0 now has 42 slides in 120 minutes, because it also covers how a model is measured, what happens behind a chat message, data readiness, foundation models, costs and the roles. If Monday ended part-way through the first half, the table shows the order of what is left. Tell me the last slide you reached and I will shorten the plan to fit. Slide numbers are from the current deck.', 10, after=4)
grid(d, [['Measures: accuracy, precision, recall, F1, ROC and AUC, benchmarks', '15 to 19', '20'], ['Data: five kinds, quality, and the law-firm data readiness example', '20 to 25', '15'],
         ['How a language model is trained, then training versus inference and what happens behind a chat message with a file', '26 to 29', '15'], ['Foundation models, open versus proprietary, adapting a model, costs', '30 to 33', '15'],
         ['What AI does well and badly, and industry uses', '34 to 35', '5'], ['Roles, including MLOps, and the model lifecycle', '36 to 38', '10'], ['Rules, workflows and agents, then the twelve sessions', '39 to 40', '5'],
         ['What you take home, and the three things to prepare', '41 to 42', '10']], [10.8, 3.4, 3.2], header=['Block', 'Slides', 'Minutes'], size=9.5)
para(d, 'If you are short of time, cut in this order: industry table (35), the rules-workflows-agents slide (39), the twelve-sessions table (40), then slides 17 and 19. The handbook covers them. Keep the measures slides 15 and 16, the behind-the-screen slides 28 and 29, and the data readiness scorecard 23.', 10, before=4, after=4)
h2(d, 'Hand out at the end of Session 0')
bullets(d, ['The Course Handbook (PDF), the Course Overview and the Learner Workbook, as one shared folder link and, if you wish, as a WhatsApp document.',
            'The Templates and Practice Files folders. Learners will use the Use-Case Scorecard and the Task Card in Session 1.',
            'Ask each learner to say their three candidate tasks aloud before they leave, and write them down. It saves ten minutes in Session 1.'], 10)
h2(d, 'The message to send tonight (edit as you like)')
box(d, 'Message to learners', ['Thank you for today. Please read the Course Handbook before Session 1.',
                               'Before Session 1, choose three tasks from your own company that you repeat every week or month, for example a weekly report, answering customer questions, checking invoices or writing meeting notes.',
                               'Please bring: a charged laptop, a Google account, and one AI assistant account you already use (ChatGPT, Gemini or Claude, the free version is fine).',
                               'Please do not paste confidential company information into any AI tool in class. We use made-up company data.'])

# ------------------------------------------------------------ tools
page_break(d)
h2(d, 'Your tools and accounts: install and test within two days', 0)
grid(d, [['PowerPoint with Presenter View', 'Shows the slides and your spoken script in the notes.', 'Open "01 - Where AI fits in your business.pptx". Install the Lato fonts from brand/fonts first.'],
         ['Google account with Google Sheets', 'You build the demonstration sheet.', 'Open sheets.google.com, make a blank sheet, type =1+1 in a cell.'],
         ['One AI assistant (ChatGPT, Gemini or Claude)', 'The live demonstration.', 'Sign in. Paste a short test message. Write down which model name the chat shows. Use a new chat for the real run.'],
         ['Phone timer', 'Times the person step and the AI step.', 'Check it starts, stops and shows seconds.'],
         ['Projector and internet, plus a phone hotspot', 'Backup if the room internet fails.', 'Test the hotspot with the laptop the day before.'],
         ['Printer or copy shop', 'The twelve-message sheet and, if you wish, printed templates.', 'One printed sheet per learner, with NO answer key on it.'],
         ['Board or flip chart and markers', 'Times, tallies and learners\' candidate tasks.', 'Draw three columns: Rule, Person, AI.']],
     [4.2, 5.4, 7.8], header=['Tool', 'What it is for', 'Test it like this'], size=9)
para(d, 'Data safety: the twelve customer messages belong to a made-up company, Nile Valley Foods Ltd, so they are safe to paste into any assistant. Tell learners to use made-up or anonymised text in class, and keep real company data out of any assistant.', 10, before=4, after=3)

# ------------------------------------------------------------ build the demo
page_break(d)
h2(d, 'The day before: the demonstration sheet (optional, about 30 minutes)', 0)
para(d, 'The slides already show the rule result and the AI result. Build the sheet only if you want to show the formula working live. The instructions are below.', 10, after=3)
for t in f1['demo_steps'][:3]:
    para(d, t, 10, after=3)
h2(d, 'The twelve messages, the key, and what the keyword rule does')
rows = []
for i in ids:
    t = msgs[i]['text']
    fl = ('late' in t.lower()) or ('delay' in t.lower())
    truth = key[i]['true_category'] == 'complaint'
    rows.append([i, short(t, 78), key[i]['true_category'].capitalize() + (' (tricky)' if key[i]['tricky'] == 'yes' else ''), 'Complaints' if fl else 'Not a complaint', 'yes' if fl == truth else 'NO'])
grid(d, rows, [1.1, 8.4, 3.2, 3.0, 1.7], header=['Id', 'Message (shortened)', 'The key', 'The rule says', 'Right?'], size=8, label_cols=(0,))
para(d, 'Result, exact: the rule sends M07 and M38 to Complaints, which is wrong for both, and it misses the three real complaints M03, M10 and M32. On the question "is this a complaint", the rule is wrong for 5 of 12 and right for 7. You can say this without a live run, but still show the sheet.', 10, before=4, after=3, bold=True)
h2(d, 'Why each tricky message is tricky (from the key)')
grid(d, [[i, key[i]['note'].replace('TRICKY. ', '')] for i in ids if key[i]['tricky'] == 'yes'], [1.2, 16.2], header=['Id', 'What makes it tricky'], size=8.5, label_cols=(0,))

# ------------------------------------------------------------ rehearse
page_break(d)
h2(d, 'The day before: the three runs and their results', 0)
para(d, 'Rule and AI results are on slides 12 to 15. Only the person step is live. If you also want to run an assistant yourself (for example ChatGPT or Gemini), use the table at the end of this section and tell learners that it is a different product from the slides.', 10, after=4)
grid(d, [['1  The rule', 'Apply the sheet formula (or the filter). It takes seconds.', 'Wrong for 5 of 12. M07 and M38 become Complaints. M03, M10, M32 are missed.'],
         ['2  A person', 'One learner sorts the printed sheet into Order, Payment, Complaint, Other. Start the timer, stop at the twelfth message. Check the sort against the key together.', 'Time: you record it. Expect disagreement with the key on M14, M26 and M28. That is a finding: mixed messages need a rule about which topic comes first.'],
         ['3  The AI', 'Already run: Claude, three separate fresh chats, 4 November 2026, key hidden, the exact prompt below. Your own live run is optional.', '9 of 12 match the key, 2 are flagged UNSURE, and one differs (M14). All three runs gave the same answers. Table below.']],
     [2.6, 8.0, 6.8], header=['Run', 'How', 'What you should see'], size=8.5)
box(d, 'The prompt for the AI run (paste exactly)', ['Sort each message into Order, Payment, Complaint or Other. For each, give the id, the category and one sentence of reason. If you cannot tell, write UNSURE.'])
h2(d, 'What to watch for in the AI answer')
bullets(d, ['Does it say UNSURE for M28, the ambiguous one? A confident wrong answer there is a good teaching moment for Session 2.', 'Does it catch the polite complaint M10 and the sarcastic complaint M32? Does it mistake M07 or M38 for complaints, as the rule does?',
            'For M14 and M26, does it notice there are two topics? What does it choose first?', 'Does it write a reason that sounds right but is wrong? Point to one example.'], 10)
h2(d, 'What the AI actually did (three runs, same answers)')
grid(d, [[i, key[i]['true_category'].capitalize(), {'M26': 'UNSURE (order plus complaint)', 'M28': 'UNSURE', 'M14': 'Complaint'}.get(i, key[i]['true_category'].capitalize()), 'differs' if i == 'M14' else ('flagged' if i in ('M26', 'M28') else 'matches')] for i in ids], [1.2, 4.2, 7.2, 4.8], header=['Id', 'The key', 'The AI said', 'Result'], size=8.5, label_cols=(0,))
para(d, 'The AI got right all four messages that fool the rule (M07, M10, M32, M38) and said UNSURE where a careful person would hesitate. It chose Complaint for M14 where the key says Payment first. Twelve messages and three similar runs are a small sample: do not claim the AI is always right.', 10, before=3, after=3)
h2(d, 'Optional: fill in if you run an assistant yourself')
grid(d, [[i, key[i]['true_category'], '', '', ''] for i in ids], [1.2, 3.4, 4.0, 4.4, 4.4], header=['Id', 'The key', 'AI category', 'AI sure or UNSURE?', 'Right? Note'], size=9, label_cols=(0,), min_h=0.8)
grid(d, [['Time for the rule', ''], ['Time for the person', ''], ['Time for the AI to answer', ''], ['Time for the class to check the AI', ''], ['AI product and model name shown', ''], ['Date and time of the run', '']], [7.0, 10.4], size=9.5, min_h=0.8)

# ------------------------------------------------------------ morning
page_break(d)
h2(d, 'The morning of Session 1', 0)
bullets(d, [('Pack:', 'laptop, charger, adapter, phone with timer and hotspot, printed twelve-message sheets (one per learner, no key), printed Use-Case Scorecard and Task Card if wanted, markers, spare pens.'),
            ('Open, in this order:', '1) the deck in Slide Show with Presenter View; 2) the demonstration Google Sheet; 3) the AI assistant in a NEW chat; 4) customer_messages_key.csv (keep it off the projector); 5) the saved result of your rehearsal; 6) the Use-Case Scorecard.'),
            ('Check:', 'projector shows the slides, sound is not needed, internet works, hotspot is ready, the board has three columns for Rule, Person and AI.'),
            ('Welcome list:', 'a page ready to write each learner\'s three candidate tasks.')], 10)

# ------------------------------------------------------------ run sheet
h2(d, 'In class: the minute-by-minute run sheet', 6)
spec = deck.build_spec(S1)
titles = [(sl['title']['text'].replace('\n', ' ') if sl.get('title') else (sl.get('title_raw') or '')) for sl in spec['slides']]
def sl_no(prefix):
    for i, t in enumerate(titles, 1):
        if t.startswith(prefix):
            return i
    return '?'
n_demo, n_tricky, n_p1, n_p2, n_card, n_p3, n_dec, n_keep = sl_no('Demonstration'), sl_no('The messages that fool'), sl_no('Practice: list'), sl_no('Practice: score'), sl_no('A finished task card'), sl_no('Practice: choose'), sl_no('Decision'), sl_no('Save it')
t = 0
rows = []
steps = {
 0: ('Slides 1 to 5', 'Welcome. Read the question of the day aloud: Which tasks in my company should AI touch first? Learners say their three candidate tasks and you write them down. Show the words slide: Task, Use case, Baseline, Checkable.'),
 1: (f'Slides 6 to 10', 'The idea. Most companies use AI and far fewer see a profit. Four kinds of work, four kinds of tool: rules, patterns, drafting, judgement. The five tasks from one company. The six tests of a good first task. Ask the three questions from the facilitator guide.'),
 2: (f'Slides {n_demo} to {n_tricky}', 'The demonstration. Rule, then person, then AI, in that order, with times on the board. End on slide ' + str(n_tricky) + ': the messages that fool a keyword rule.'),
 3: ('Break', 'Leave the board as it is. Learners may refresh tea or coffee. Do not open the AI.'),
 4: (f'Slides {n_p1} to {n_card}', 'Learners list ten tasks and sort them by kind of work, then score five and place them on the picture. Walk the room. Use the finished task card (slide ' + str(n_card) + ') as the model.'),
 5: (f'Slides {n_p3} to {n_dec}', 'Each learner chooses one task and writes its baseline: how long, how often, what goes wrong, each number marked E or M. Then the decision slide: my chosen task and the reason.'),
 6: (f'Slide {n_keep}', 'Close. Everyone saves their scorecard and one-page task card. Preview Session 2: bring one piece of task text to test. Ask for one question to answer at the start of Session 2.'),
}
for k, (m, lab) in enumerate(S1['clock']):
    rows.append([f'{t // 60}:{t % 60:02d}', str(m), lab, steps[k][0], steps[k][1]])
    t += m
grid(d, rows, [1.2, 1.2, 3.4, 2.4, 9.2], header=['Starts', 'Min', 'Block', 'Slides', 'What you do'], size=8, label_cols=(0,))

# ------------------------------------------------------------ the three practices
page_break(d)
h2(d, 'Coaching the practice blocks', 0)
grid(d, [[f'Slide {n_p1}', 'List ten recurring tasks and mark the kind of work each one is: rules, patterns, drafting or judgement.', 'Offer five common tasks to anyone stuck: weekly report, invoice check, enquiry triage, CV shortlist, meeting minutes. If someone brought none: what did you do last week that you also did the week before?'],
         [f'Slide {n_p2}', 'Score five of them for value, risk and checkability, and place them on the picture.', 'Cross out anything a formula already does (that is rules work). A task whose mistake reaches a customer before anyone checks scores high on risk.'],
         [f'Slide {n_p3}', 'Choose one task. Write its task card with a baseline, and mark every number E (estimate) or M (measured).', 'A plain estimate marked E is enough today. Measured numbers come later in the course. Ask: what would make you stop and not use AI for this task?']],
     [2.0, 7.0, 8.4], header=['Slide', 'What learners do', 'How you help'], size=8.5, label_cols=(0,))
h2(d, 'Three questions to ask during the idea section, and good answers')
grid(d, [[q, a] for q, a in f1['questions']], [8.2, 9.2], header=['Ask', 'A good answer'], size=8.5, label_cols=())
h2(d, 'Ideas learners often get wrong')
grid(d, [[a, b] for a, b in f1['misconceptions']], [6.8, 10.6], header=['What a learner may say', 'What to say back'], size=8.5, label_cols=())
h2(d, 'If a learner asks')
grid(d, [[q, a] for q, a in f1['probes']], [6.4, 11.0], header=['Question', 'A good answer'], size=8.5, label_cols=())

# ------------------------------------------------------------ if things go wrong
h2(d, 'If something goes wrong')
bullets(d, f1['rescue'] + f1['fallback'], 9.5)

# ------------------------------------------------------------ after
page_break(d)
h2(d, 'Straight after the session', 0)
bullets(d, ['Save the board: photograph the three columns (Rule, Person, AI) with their times.', 'Write every live result in the Rehearsal Record as observed. If the AI behaved differently from the rehearsal, say so. That is a useful finding for Session 2.',
            'Collect each learner\'s scorecard and task card (or a photo of it). The chosen task stays with them for the whole course.', 'Write down any question you could not answer, and answer it at the start of Session 2.'], 10)
box(d, 'Follow-up message after Session 1 (edit as you like)', ['Thank you for today. Please keep your completed use-case scorecard and your one-page task card. Your chosen task stays with you for the whole course.',
                                                              'Before Session 2, please bring one piece of text from your task to test (a real example with anything confidential removed, or a made-up one). Optional but useful.',
                                                              'If you have a question from today, send it and I will answer it at the start of Session 2.'])
para(d, 'What Session 2 does next: ' + S1['next'], 10, before=4, after=4)

# ------------------------------------------------------------ one page checklist
page_break(d)
h2(d, 'One-page checklist (print this)', 0)
grid(d, [['Today', 'Finish Session 0. Hand out handbook, overview, workbook, folders.'], ['Today', 'Send the preparation message (three tasks, laptop, Google account, AI account, no confidential data).'],
         ['2 days before', 'Test PowerPoint with notes, Google Sheets, the AI assistant, timer, hotspot. Print the twelve-message sheets (no key).'],
         ['Day before', 'Build the demonstration sheet with the rule formula. Run the rule, the person and the AI once. Fill in the rehearsal table. Save the AI result.'],
         ['Morning', 'Pack the kit. Open the tabs in order. Board with three columns. Page ready for the learners\' candidate tasks.'],
         ['In class', '0:00 welcome and candidate tasks. 0:10 the idea. 0:35 demonstration. 0:55 break. 1:00 practice. 1:45 decision. 1:55 close.'],
         ['After', 'Photograph the board. Update the Rehearsal Record. Send the follow-up. Note unanswered questions.']], [3.0, 14.4], header=['When', 'Done?  What'], size=9.5, min_h=0.9)

save(d, EDITION / '04 Facilitator Materials' / 'Session 1 Preparation Pack.docx')
subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_prep', '--headless', '--convert-to', 'pdf', '--outdir', str(EDITION / '04 Facilitator Materials'), str(EDITION / '04 Facilitator Materials' / 'Session 1 Preparation Pack.docx')], capture_output=True, timeout=200)
