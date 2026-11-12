"""Generate the Word documents of the Leading with AI Leadership Edition from the session files, so slides, workbook and guide never disagree.

Run from Build/:  python3 kit/make_docs.py            (all documents)
Writes: 01 Course Overview/Course Overview.docx (+ .pdf), 03 Learner Materials/Learner Workbook.docx (+ .pdf),
        04 Facilitator Materials/Facilitator Guide.docx (+ .pdf) and Rehearsal Record.docx, 00 Start Here/Start Here.docx (+ .pdf).
Uses the KLAi Word kit in templates_gen/docx_kit.py (Lato, black header band with the logo, hairline grids).
"""
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

SESS_ALL = [deck.load(n) for n in range(0, deck.NSESS + 1)]
SESS = SESS_ALL[1:]   # the fourteen numbered sessions (Session 0 is the introduction)
W = CONTENT_CM
import worksheets  # noqa: E402
worksheets.SHEETS = {}   # Leadership Edition: no maths worksheets


def page_break(doc):
    """A tiny paragraph that itself starts the new page, so a full page never leaves a blank page behind it."""
    p = doc.add_paragraph(); fmt(p, 0, 0)
    p.paragraph_format.page_break_before = True
    p.paragraph_format.line_spacing = Pt(1)
    r = p.add_run(''); r.font.size = Pt(1)


def to_pdf(path):
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_docs', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True)


def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True, False, GOLD if False else BLACK)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def session_table():
    return [[str(s['num']), s['title'], s['keep'].split('. ')[0].rstrip('.')] for s in SESS]



def slide_map(s, spec):
    """Rows [number, title, what it is] for every slide in the deck, so the guide's slide numbers always match the deck."""
    names = {'demo': 'Demonstration', 'practice': 'Learner works', 'decision': 'Decision', 'example': 'Worked example', 'stat': 'One number', 'table': 'Table', 'steps': 'Diagram',
             'idea': 'Idea', 'wide': 'Diagram', 'list': 'List', 'statement': 'Points', 'compare': 'Comparison'}
    meta = ['Cover', 'Outcomes', 'Plan']
    if s['recall']:
        meta.append('Recall')
    if s['num'] >= 1:
        meta.append('How today connects')
    if s.get('words'):
        meta.append('Words')
    seen_demo = False
    for sl in s['slides']:
        k = sl['kind']
        if k == 'demo':
            seen_demo = True
        lab = names.get(k, k)
        if k in ('idea', 'wide', 'steps', 'table', 'list', 'statement', 'compare', 'stat', 'example') and seen_demo:
            lab = 'After the demonstration'
        meta.append(lab)
    meta.append('Close')
    rows = []
    for i, sl in enumerate(spec['slides']):
        ttl = ((sl.get('title') or {}).get('text') or sl.get('title_raw') or '').replace('\n', ' ')
        rows.append([str(i + 1), ttl, meta[i] if i < len(meta) else ''])
    return rows


def spec_for(n):
    import json
    specs = sorted((BUILD / '_specs').glob('[0-9][0-9]_-_*.json'))
    return json.loads(specs[n].read_text())


# ---------------------------------------------------------------- Course Overview
def overview():
    name = 'Course Overview'
    d = new_doc(name)
    title(d, 'Leading with AI', 'Where AI pays in your industry, and what it changes for your staff  |  15 sessions of 2 hours  |  dates and format agreed with you')
    para(d, 'For CEOs, managing directors, board members, directors and senior managers who want to know where AI creates value in their industry, at work and for their employees. No mathematics and no technical background: each idea is taught with a diagram, an everyday comparison and named cases from banking and microfinance, telecom and mobile money, agriculture, manufacturing and FMCG, healthcare and insurance and the public sector, Uganda and East Africa first.', 10.5, after=4)
    para(d, 'Session 0 sets out the map. Sessions 1 to 5 show what AI can do (see and read, predict, understand language, write) and how to judge it. Sessions 6 to 8 cover choosing models and vendors, getting good work from assistants, and making AI know your documents. Sessions 9 and 10 cover failures and agents. Sessions 11 to 14 are practical: you redesign work and cost it, plan for your people, set the rules and check your data, and leave with your AI Opportunity Portfolio and a 90-day plan. Every session ends with a one-page take-away. There are no tests and no marks.', 10.5, after=6)
    h2(d, 'The fifteen sessions')
    grid(d, session_table(), [1.0, 6.4, 10.0], header=['No.', 'Session', 'You keep'], size=9, label_cols=(0,))
    spacer(d, 4)
    h2(d, 'What you will be able to do')
    bullets(d, ['Spot where AI creates value in your industry and your organisation, with named examples from your sector.',
                'Judge an accuracy claim, a pilot, a vendor and a risk, and know what to ask about each.',
                'Get reliable work from AI assistants, and know when not to trust the answer.',
                'Redesign a workflow, cost it and decide where a rule, an AI step, an agent or a person fits.',
                'Plan the change for your staff: which roles and tasks change, the skills they need, what they fear and how the tools get used.',
                'Set the rules, check your data and start a governed 90-day plan from your AI Opportunity Portfolio.'], 10)
    h2(d, 'How we work')
    para(d, 'Each session pairs short explanations with demonstrations that the instructor runs while you watch, and you may join in. Sessions 1 to 10 each end with a hands-on step on your own organisation. Sessions 11 to 14 are practical and most of the time is yours. Examples come from a fictional company, Nile Valley Foods Ltd, and from finance, operations, customer service, HR, sales, compliance and legal settings, so you never need to share company data in class. Other tools on the market are discussed as options only.', 10.5, after=6)
    h2(d, 'Before the first session')
    bullets(d, ['Nothing to prepare. Read the Course Handbook if you can.',
                'Bring a laptop and one AI assistant account you already use, if you want to join in the demonstrations.',
                'Choose your industry in Session 0 and note two or three decisions or workflows in your organisation you would like AI to help with.',
                'Use only sample or invented data for practice. Never paste personal or confidential data into a tool you have not approved.'], 10)
    h2(d, 'After the course')
    para(d, 'You receive a follow-up kit. At 30, 60 and 90 days the instructor checks what is running, how much time it saves and what changed in your policy, and you return a one-page check-in form and a results tracker.', 10, after=6)
    para(d, 'Jotham Martin Wambi  |  KLAi Professional Learning  |  jothammartin.wambi@gmail.com  |  +256 750 990 718', 9, color='404040')
    out = EDITION / '01 Course Overview' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Learner Workbook
def workbook():
    name = 'Learner Workbook'
    d = new_doc(name)
    title(d, 'Learner Workbook', 'Leading with AI. One page for each session. Write in it, or type in Word.')
    box(d, 'How to use this workbook', ['Each page has the day’s question, your steps for the hands-on, the fields to fill in, two questions to think about and one decision.',
                                        'Every session adds to your AI Opportunity Portfolio (the Templates folder has it as a spreadsheet). The templates named on a page are in your Templates folder.',
                                        'Work on your own organisation from the start. The fictional Nile Valley Foods examples show what a filled entry looks like.'], size=9.5)
    h2(d, 'My industry and organisation (fill in at Session 0)')
    grid(d, [['My industry', ''], ['My organisation and role', ''], ['Two decisions or workflows I want AI to help with', ''], ['AI tools my staff already use', ''], ['What success would look like in a year', '']], [6.0, 11.4], label_cols=(0,), size=10, min_h=0.9)
    page_break(d)
    for s in SESS_ALL:
        w = s['workbook']
        para(d, f'Session {s["num"]}' + (', the introduction' if s['num'] == 0 else ''), 10, True, color=RED, after=0, keep=True)
        para(d, s['title'], 17, True, after=2, keep=True)
        para(d, w['question'], 11, False, True, color='404040', after=6)
        h2(d, 'Your steps for today', before=2)
        bullets(d, w['steps'], 10)
        h2(d, 'Fill in')
        many = len(w['fields']) > 8
        grid(d, [[f, ''] for f in w['fields']], [7.0, 10.4], label_cols=(0,), size=9.5, min_h=0.62 if many else 0.85)
        h2(d, 'Think about')
        for r in w['reflect']:
            para(d, r, 10, after=1)
            para(d, '_' * 78, 10, color='A6A6A6', after=2 if many else 4)
        h2(d, 'My decision')
        grid(d, [[w['decision'], '']], [7.0, 10.4], label_cols=(0,), size=9.5, min_h=1.0 if many else 1.3)
        para(d, 'I keep: ' + s['keep'], 9, True, before=4, after=0)
        if s['num'] in worksheets.SHEETS:
            ttl, fns = worksheets.SHEETS[s['num']]
            page_break(d)
            para(d, f'Session {s["num"]}: worksheet for the paper exercise', 10, True, color=RED, after=0, keep=True)
            para(d, ttl, 17, True, after=4, keep=True)
            for fn in fns:
                fn(d)
        if s['num'] < deck.NSESS:
            page_break(d)
    page_break(d)
    title(d, 'Words used in this course')
    rows = []
    seen = set()
    for s in SESS_ALL:
        for a, b in s['words']:
            if a.lower() not in seen:
                seen.add(a.lower())
                rows.append([a, b, f'Session {s["num"]}'])
    grid(d, rows, [3.6, 11.4, 2.4], header=['Word', 'What it means', 'First used'], size=9, label_cols=(0,))
    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Facilitator Guide
def clock_rows(s):
    t = 0
    rows = []
    for m, label in s['clock']:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), label])
        t += m
    return rows


def facilitator():
    name = 'Facilitator Guide'
    d = new_doc(name)
    title(d, 'Facilitator Guide', 'Leading with AI. For the instructor only: it holds answers and rehearsal notes.')
    h2(d, 'How to teach this course', before=4, after=2)
    bullets(d, [('What the course is.', 'No maths. Sessions 1 to 10 teach one idea each through pictures, everyday analogies, named industry cases and recorded demonstrations, then the learner adds to the AI Opportunity Portfolio. Sessions 11 to 14 are the practicals. Keep asking “where would this help or hurt in your organisation, and who would it affect?”.'),
                ('No tests, no marks.', 'Progress is what the learner builds and keeps. Never rank learners. Give one strength and one next step.'),
                ('Be honest about AI results.', 'Never describe an AI output as observed unless you ran it. Record real runs in the Rehearsal Record and label saved runs and live runs apart.'),
                ('Rehearse the demonstrations.', 'Every demonstration has a fallback in this guide. The AI results on the slides are recorded; a live run is optional, and results can differ on another day or product.'),
                ('Teach the learner’s industry.', 'Each leader chooses an industry in Session 0. In every industry tour, spend longest on their tile and their case. Every case is named and sourced in 05 Course Maintenance/Build/research: re-check figures in the week you teach. Nile Valley Foods Ltd is fictional and always said to be.'),
                ('Answer keys stay with you.', 'They are in this folder only. Do not send them to learners.')], 10)
    h2(d, 'Before you teach', before=4, after=2)
    bullets(d, ['Read the saved results in each scenario and demonstration session (Case Runs folder) so you can explain them, and say whose results they are. If you run a case in your own assistant, note it in Rehearsal Record.docx.',
                'No learner writes code and no trial accounts are needed. Demonstration results are recorded in advance and kept in 05 Course Maintenance/Build/demo_runs; the scripts there can be re-run live. Rehearse each demonstration once.',
                'Check Uganda’s national AI strategy status (a draft awaiting Cabinet on 11 November 2026), the EU AI Act dates and any data-protection rulings before Sessions 6 and 13, and update the slides if they changed.',
                'Send each learner the Course Overview and the Course Handbook before Session 1.'], 10)
    h2(d, 'Course map', before=4, after=2)
    grid(d, session_table(), [1.0, 6.4, 10.0], header=['No.', 'Session', 'The learner keeps'], size=9)
    h2(d, 'Running each part of a session', before=4, after=2)
    grid(d, [
        ['Open (first 10 minutes)', 'Greet, say the question of the day, then run the recall. Ask for answers aloud and give the good answer. Say what each learner will leave with. In Sessions 11 to 14, if someone has no workflow in mind, use the NVF example and ask them to choose theirs before the next practical.'],
        ['The idea and the industry tour (about 40 minutes in Sessions 1 to 10, 20 in Sessions 11 to 14)', 'Before you read the notes for a slide, say in one sentence what it shows. Stop at every question in the script and wait for a real answer. Link each idea to the learner’s work: “Where would you meet this?”. Never rush past a diagram: ask “what do you see?”.'],
        ['The demonstration (about 15 minutes in Sessions 1 to 10, 10 in Sessions 11 to 14)', 'Say what you will do and what to watch for, then do it slowly and out loud. Run it once before class. If it fails, say what the failure shows, switch to the saved run and tell the room it is saved. Ask the learners to predict before you press the key.'],
        ['The hands-on (about 25 minutes in Sessions 1 to 10 on the AI Opportunity Portfolio; about 60 minutes of the learner’s own work in Sessions 11 to 14)', 'Read the steps once, then be quiet and walk round. Ask three questions: “What did you choose?”, “How will you check it?”, “What would make you stop?”. Do not do it for them. With a group, ask learners who finish early to swap and check each other’s result.'],
        ['Your people and the decision (about 15 minutes in Sessions 1 to 10, 10 in Sessions 11 to 14)', 'Ask each learner to say the decision and the reason in one sentence, and to write it in the workbook. A decision to stop or revise is a good result: praise the reasoning.'],
        ['The close', 'Answer the cover question together. Point to the artefact each learner keeps. Name the optional step before the next session and the first thing you will ask next time.']],
         [4.0, 13.4], label_cols=(0,), size=9)
    h2(d, 'Handling the room', before=4, after=2)
    grid(d, [
        ['A learner is excited about AI', 'Welcome it and ask for the task and the number: “What would you measure?”'],
        ['A learner is sceptical', 'Agree that errors are real and move to the checks: “That is why we test it on your own text.”'],
        ['A learner asks something you do not know', 'Say “I do not know. Let us test it”, or “I will check and tell you next session.” Write it down and follow up. Do not guess about law, prices or product limits.'],
        ['A learner asks for legal advice', 'Say “I teach how to think about it and what to ask. Your lawyer decides.” Use the hedged answers under If a learner asks.'],
        ['The group is quiet', 'Ask for one example from their own company, or ask them to turn to a colleague for 30 seconds and then report one point.'],
        ['The group is running late', 'Shorten your talking and keep the learners’ working time. Cut optional examples and keep the demonstration and the decision.']],
         [5.0, 12.4], label_cols=(0,), size=9)
    h2(d, 'Follow-up at 30, 60 and 90 days', before=4, after=2)
    para(d, 'Diary three check-ins with each learner after Session 14. Send the 30-60-90 Check-in Form and the Results Tracker. At each check-in ask: what is running, how many hours were saved, what went wrong, what changed in the policy, what next. Record results and, with the learner’s permission, use them to improve the course.', 10, after=4)
    page_break(d)
    for s in SESS_ALL:
        f = s['facilitator']
        para(d, f'Session {s["num"]}' + (', the introduction' if s['num'] == 0 else ''), 10, True, color=RED, after=0, keep=True)
        para(d, s['title'], 18, True, after=2, keep=True)
        para(d, s['question'], 11, False, True, color='404040', after=6)
        h2(d, 'The 120 minutes', before=2, after=2)
        grid(d, clock_rows(s), [1.6, 1.8, 14.0], header=['Start', 'Minutes', 'What happens'], size=8.5, label_cols=())
        spacer(d, 3)
        h2(d, 'The learner keeps', before=4, after=2)
        para(d, s['keep'], 10, after=3)
        h2(d, 'Before class', before=4, after=2)
        bullets(d, f['prep'], 9, after=1)
        h2(d, 'Slides in order', before=4, after=2)
        grid(d, slide_map(s, spec_for(s['num'])), [1.0, 11.0, 5.4], header=['No.', 'Slide', 'What it is'], size=8.5, label_cols=())
        if s['recall']:
            h2(d, 'Recall at the start (questions about the previous session)', before=4, after=2)
            grid(d, [[q, a] for q, a in s['recall']], [8.0, 9.4], header=['Ask', 'Expected'], size=8.5, label_cols=(0,))
        if f.get('demo_steps'):
            h2(d, 'Demonstration: steps', before=4, after=2)
            bullets(d, f['demo_steps'], 9, after=1)
            fb = f.get('fallback') or f.get('fallbacks')
            if fb:
                para(d, 'Fallback', 9.5, True, before=2, after=1)
                if isinstance(fb, str):
                    para(d, fb, 9.5, after=3)
                else:
                    bullets(d, fb, 9.5)
        if f.get('probes'):
            h2(d, 'If a learner asks', before=4, after=2)
            grid(d, [[a, b] for a, b in f['probes']], [6.0, 11.4], header=['Question', 'Answer'], size=8.5, label_cols=(0,))
        if f.get('one_learner'):
            h2(d, 'With one learner', before=4, after=2)
            bullets(d, f['one_learner'], 9, after=1)
        h2(d, 'Misconceptions and how to respond', before=4, after=2)
        grid(d, [[a, b] for a, b in f['misconceptions']], [6.0, 11.4], header=['You may hear', 'Respond with'], size=8.5, label_cols=(0,))
        h2(d, 'Questions to ask, with expected answers', before=4, after=2)
        grid(d, [[a, b] for a, b in f['questions']], [8.0, 9.4], header=['Ask', 'Expected'], size=8.5, label_cols=(0,))
        if f.get('rescue'):
            h2(d, 'If it goes wrong', before=4, after=2)
            bullets(d, f['rescue'], 9, after=1)
        para(d, 'Next session: ' + s['next'], 9, True, before=4, after=0)
        page_break(d)
    h2(d, 'Answer keys and where they are', before=4, after=2)
    bullets(d, ['customer_messages_key.csv: the true category of each of the 40 messages (Sessions 0, 2 and 11).',
                'handbook_questions_key.csv: ten questions, two not answerable from the handbook (Sessions 8 and 9).',
                'market_notes_conflict_key.txt, hand_summary_errors_key.txt and cv_screening_key.txt: the recorded failure cases (Session 9).',
                'vendor_proposal_red_flags.txt: the red flags in the sample proposal (Session 13).'], 9.5)
    h2(d, 'Sources behind the cases and figures')
    para(d, 'Every named case is in 05 Course Maintenance/Build/research (one block per case: what it does, the result, the source with its date, the confidence and the caution to say aloud). Recorded demonstrations are in 05 Course Maintenance/Build/demo_runs. Check each figure again in the week you teach, and say company figures are company figures.', 9.5, after=3)
    out = EDITION / '04 Facilitator Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Rehearsal Record
def rehearsal():
    name = 'Rehearsal Record'
    d = new_doc(name)
    title(d, 'Rehearsal Record', 'Fill this in if you run any demonstration yourself. The results on the slides come from real recorded runs, listed in 05 Course Maintenance/Build/demo_runs and Case Runs (AI assistant runs: Claude, fresh sessions, answer keys hidden). Anything you run yourself goes here and nowhere else.')
    h2(d, 'Accounts and versions')
    grid(d, [['AI assistant and plan you used yourself (if any)', ''], ['Date and version or model name shown on screen', ''], ['Did your result match the slide? (Yes / No, and what differed)', '']],
         [8.4, 9.0], label_cols=(0,), size=9.5, min_h=0.9)
    h2(d, 'Demonstrations')
    rows = []
    for s_ in SESS:
        rows.append([f'Session {s_["num"]}: {s_["title"]}', '', '', ''])
    grid(d, rows, [6.2, 3.2, 5.0, 3.0], header=['Demonstration', 'Date run', 'What I observed (paste the real result)', 'Fallback needed?'], size=9, label_cols=(0,), min_h=1.4)
    h2(d, 'Problems found and fixes')
    grid(d, [['', ''], ['', ''], ['', '']], [8.7, 8.7], header=['Problem', 'Fix or change to the slides'], size=9.5, min_h=1.2)
    out = EDITION / '04 Facilitator Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Start Here
def start_here():
    name = 'Start Here'
    d = new_doc(name)
    title(d, 'Start here', 'Leading with AI, Leadership Edition, KLAi Professional Learning')
    para(d, 'Fifteen sessions of two hours for senior leaders, with no mathematics. Sessions 0 to 10 show what AI does, where it pays in each industry (with named, sourced cases), what goes wrong and how to judge it. Sessions 11 to 14 are practicals in which the leader redesigns a workflow, plans for their people, sets the rules, checks the data and leaves with an AI Opportunity Portfolio and a 90-day plan.', 10.5, after=6)
    h2(d, 'What is in this folder')
    grid(d, [['01 Course Overview', 'One page to share with a learner before the course.'],
             ['02 Class Slides', 'Fifteen decks (Session 0 to Session 14), with a spoken script in the speaker notes.'],
             ['03 Learner Materials', 'The Learner Workbook, the Take-away Sheets (one page per session), the Industry Use-Case Atlas (uses and named cases by industry), the Questions to Ask sheet, the Templates for the practicals, the Follow-up Kit, and the Practice Files (the case company data).'],
             ['04 Facilitator Materials', 'The Presenter Script (every slide’s spoken script in order, to read from paper or a tablet), the Facilitator Guide with answers and fallbacks, the Answer Keys and the Rehearsal Record. Keep this folder away from learners.'],
             ['05 Course Maintenance', 'The sources that build the decks and documents, checks, and notes for whoever maintains the course.']], [5.0, 12.4], label_cols=(0,), size=9.5)
    h2(d, 'Before the first class')
    bullets(d, ['Send the Course Overview and the Course Handbook.',
                'Rehearse each demonstration once and complete the Rehearsal Record. The scripts are in 05 Course Maintenance/Build/demo_runs.',
                'Read the Facilitator Guide section “How to teach this course”.'], 10)
    h2(d, 'Three rules')
    bullets(d, ['Never describe an AI result as observed unless you ran it and recorded it.',
                'Use only sample or invented data with free tools. The demonstration mailbox is invented.',
                'Rebuild the decks and documents from 05 Course Maintenance/Build. Do not edit generated files by hand.'], 10)
    out = EDITION / '00 Start Here' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Presenter Script
def presenter_script():
    """Every slide's spoken script in order, so the presenter can read from a tablet or paper. Built from the deck specs."""
    import json
    name = 'Presenter Script'
    d = new_doc(name)
    title(d, 'Presenter Script', 'Leading with AI. The words to say, slide by slide. The same text is in the speaker notes of each deck.')
    box(d, 'How to use this script', ['Read it aloud. Where a paragraph ends on a question, stop and wait for an answer before the next paragraph.',
                                     'The grey line under each slide title tells you what kind of slide it is. Steps for demonstrations, answers and fallbacks are in the Facilitator Guide.',
                                     'Never describe an AI result as observed unless you ran it.'], size=9.5)
    specs = sorted((BUILD / '_specs').glob('[0-9][0-9]_-_*.json'))
    for sp, s in zip(specs, SESS_ALL):
        spec = json.loads(sp.read_text())
        slides = spec['slides']
        # meta line for each slide: auto slides first, then authored, then keep
        meta = ['Cover', 'Outcomes for today', 'The plan for the two hours']
        if s['recall']:
            meta.append('Recall: ask the questions, then give the answers')
        if s['num'] >= 1:
            meta.append('How today connects to the sessions before and after')
        if s.get('words'):
            meta.append('Words for today')
        for sl in s['slides']:
            k = sl['kind']
            m = {'demo': 'Demonstration. Steps and fallback: Facilitator Guide, Session %d' % s['num'], 'practice': 'Practice, %d minutes, on the learner’s own task' % sl.get('minutes', 0),
                 'decision': 'Decision. The learner writes the choice and the reason', 'example': 'Worked example from Nile Valley Foods', 'stat': 'One number and its source',
                 'table': 'Table', 'steps': 'Diagram: steps', 'idea': 'Idea with a diagram', 'wide': 'Diagram', 'list': 'List', 'statement': 'Points', 'compare': 'Comparison'}.get(k, k)
            meta.append(m)
        meta.append('Close')
        para(d, f'Session {s["num"]}' + (', the introduction' if s['num'] == 0 else ''), 10, True, color=RED, before=6, after=0, keep=True)
        para(d, s['title'], 18, True, after=1, keep=True)
        para(d, s['question'], 10.5, False, True, color='404040', after=4)
        for i, sl in enumerate(slides):
            ttl = (sl.get('title') or {}).get('text') or (sl.get('title_raw') or '')
            ttl = ttl.replace('\n', ' ')
            para(d, f'Slide {i + 1}.  {ttl}', 10.5, True, before=7, after=0, keep=True)
            para(d, meta[i] if i < len(meta) else '', 8.5, color='767676', after=2, keep=True)
            for ptxt in sl['notes'].split('\n\n'):
                para(d, ptxt, 10.5, after=4)
        page_break(d)
    out = EDITION / '04 Facilitator Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


# ---------------------------------------------------------------- Take-away sheets
def takeaways():
    name = 'Take-away Sheets'
    d = new_doc(name)
    title(d, 'Take-away Sheets', 'Leading with AI. One page for each session: what you keep.')
    for s in SESS_ALL:
        f = s.get('facilitator', {})
        lines = f.get('takeaway')
        if not lines:
            continue
        para(d, f'Session {s["num"]}', 10, True, color=RED, after=0, keep=True)
        para(d, s['title'], 17, True, after=2, keep=True)
        para(d, s['question'], 11, False, True, color='404040', after=6)
        bullets(d, lines, 10.5, after=3)
        para(d, 'I keep: ' + s['keep'], 9, True, before=6, after=0)
        page_break(d)
    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out); to_pdf(out)


if __name__ == '__main__':
    overview(); workbook(); facilitator(); rehearsal(); start_here(); presenter_script(); takeaways()
    import make_atlas; make_atlas.build()
