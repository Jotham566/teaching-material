"""Course map for approval, Leading with AI (11 November 2026). Run from Build/: python kit/make_map_leadership.py"""
import json, re, subprocess, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(BUILD / 'templates_gen')); sys.path.insert(0, str(HERE))
from docx_kit import *  # noqa
from sessions_plan import S, PHASES

IDX = json.load(open(BUILD / 'research' / 'case_index.json'))
IND = dict(BNK='Banking and microfinance', TEL='Telecom and mobile money', AGR='Agriculture and agribusiness', MFG='Manufacturing and FMCG',
           HLT='Healthcare and insurance', PUB='Public sector', ENR='Energy and mining', RTL='Retail and logistics', EDU='Education',
           LGL='Legal and professional services', PPL='People (cross-industry)', ADO='Adoption (cross-industry)', GOV='Governance and law', GAP='Search, language models, Uganda')


def short(cid):
    v = IDX[cid]
    org = re.sub(r'\s*\(.*?\)', '', v['org']).strip()
    org = org.split(':')[0][:48]
    reg = v['region'].split('/')[0].split('+')[0].strip()[:22]
    if not org:
        org = cid
    return f'{org} ({reg})' if reg and reg not in org else org


def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.6); p.paragraph_format.first_line_indent = Cm(-0.5)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True); add_run(p, it[1], size)
        else:
            add_run(p, it, size)


d = new_doc('Course map for approval', 'Leading with AI, Leadership Edition')
title(d, 'Leading with AI: course map for approval', '11 November 2026  |  15 sessions of 2 hours  |  the Leadership Edition, sister of the Executive Edition  |  nothing is built until this is approved')

h2(d, 'Who it is for, and the promise', 0)
para(d, 'For CEOs, managing directors, board members, directors and senior managers who want to know where AI pays in their industry, at work and for their employees, without the mathematics. Subtitle: Where AI pays in your industry, and how to lead your people through it.', 10)
bullets(d, [('Spot value.', 'Where AI creates value in your industry and your organisation.'),
            ('Ask the right questions.', 'Of vendors, of your own teams and of every accuracy claim.'),
            ('Judge.', 'A claim, a pilot, a cost and a risk.'),
            ('Lead people.', 'Roles, skills, fears and adoption.'),
            ('Start.', 'A costed, governed 90-day plan and your AI Opportunity Portfolio.')])

h2(d, 'Design rules')
bullets(d, [
 ('No mathematics.', 'No formulas, symbols or algebra on slides or in notes. Counts, percentages and shillings only, as a leader uses them. Every idea is a picture and an everyday analogy.'),
 ('Explain before use.', 'Every term is explained the first time, in plain words first and then the industry term; when it returns, one line recalls the session where it was built.'),
 ('Sessions build on each other.', 'Four phases: understand what AI can do, choose and use it, control the risk, lead the change. Each session names what it builds on and what it feeds.'),
 ('Illustration rich.', 'Every concept slide and every case slide has a purpose-drawn figure: process pictures, icon grids, before and after, value and risk grids, timelines.'),
 ('Real, named cases.', 'Each session tells named organisations\' stories: the problem, what the AI does, the result, the catch. Uganda and East Africa first, then Africa, then global. Every figure carries a source line.'),
 ('Three threads.', 'Industry (each leader follows their industry), people (one slide every session), and the AI Opportunity Portfolio (it grows every session and becomes the final plan).'),
 ('Same format as the Executive Edition.', '15 sessions of 2 hours, the same brand, build kit, recorded demonstrations, templates and follow-up kit.')])

h2(d, 'How the sessions build on each other')
rows = []
for code, name, ss in PHASES:
    for n in ss:
        rows.append([str(n), S[n]['title'], S[n]['q'], S[n]['builds']])
grid(d, rows, [1.2, 4.6, 5.0, 6.6], header=['No.', 'Session', 'The leader\'s question', 'Builds on, and feeds'], size=8, hdr_size=8)

for code, name, ss in PHASES:
    page_break(d)
    h2(d, f'Phase {code}: {name}', 0)
    rows = []
    for n in ss:
        s = S[n]
        rows.append([str(n), s['title'], s['idea'], '; '.join(short(c) for c in s['cases']), s['demo'], s['people'], s['keep']])
    grid(d, rows, [0.9, 2.3, 4.1, 3.6, 2.6, 2.4, 2.3], header=['No.', 'Session', 'The idea, in pictures', 'Named cases', 'Demonstration', 'Your people', 'You keep'], size=7, hdr_size=7.5)

page_break(d)
h2(d, 'Every session from 1 to 10 has the same shape', 0)
bullets(d, [('Recall and hook (10 min).', 'Last session in one picture, then today\'s question opened with a real case.'),
            ('The idea (25 min).', 'Everyday picture, what the AI takes in and gives out, how it works in plain words with a drawing, what it is good and bad at. One idea per slide.'),
            ('Industry tour (15 min).', 'One picture with the six main industries and today\'s idea in each, then two or three named cases, one slide each.'),
            ('Demonstration (15 min).', 'Live or recorded, labelled with the model, the date and the number of runs.'),
            ('Break (5 min).', ''),
            ('Hands-on (25 min).', 'Add one or two entries to your AI Opportunity Portfolio using today\'s idea.'),
            ('Your people and your decision (15 min).', 'Roles, tasks, skills and fears; what you would do.'),
            ('Close (10 min).', 'Take-away sheet and the bridge to next time.')])
para(d, 'Practicals (11 to 14): 10 recall, 20 idea with cases, 10 demonstration or worked example, 5 break, 60 the leader works on their own organisation, 10 decision, 5 close.', 10)

h2(d, 'Industry balance: named cases per session')
cnt = collections.defaultdict(collections.Counter)
for n, s in S.items():
    for c in s['cases']:
        cnt[c[:3]][n] += 1
order = ['BNK', 'TEL', 'AGR', 'MFG', 'HLT', 'PUB', 'ENR', 'RTL', 'EDU', 'LGL', 'PPL', 'ADO', 'GOV', 'GAP']
rows = [[IND[k]] + [str(cnt[k][n]) if cnt[k][n] else '' for n in range(15)] + [str(sum(cnt[k].values()))] for k in order if cnt[k]]
grid(d, rows, [4.2] + [0.78] * 15 + [1.0], header=['Industry'] + [str(n) for n in range(15)] + ['All'], size=7.5, hdr_size=7.5)
para(d, 'The industry tour slide in every session covers all six main industries; the counts above are the cases told in depth. Search, language-model and Uganda cases (GAP) include Sunbird AI, Makerere AI Lab and AirQo, ULII and the Judiciary, the Data Protection Office, Centenary Group and MTN MoMo Uganda.', 9)

h2(d, 'The evidence base')
para(d, f'{len(IDX)} named cases, researched on 11 November 2026 from pages actually read, each with its source, date and confidence (High or Medium; weaker ones were dropped). They are in 05 Course Maintenance/Build/research/. Rules for teaching them:', 10)
bullets(d, ['Every figure on a slide has a source line; company claims are said to be company claims.',
            'Failures and mixed results are taught as well as successes (for example Gro Intelligence, GE Predix, Air Canada, the Dutch childcare benefits scandal, Commonwealth Bank of Australia, Babyl Rwanda, Kenya SHA).',
            'Figures are re-checked in the week a session is taught; the regulatory status (Uganda\'s national AI strategy, the EU AI Act dates) especially.'])
para(d, 'Honest gaps found: no published, measured AI result yet for a named Ugandan bank, telecom or government agency (Ugandan cases are pilots, partnerships, research or regulation); Uganda\'s national AI strategy is still a draft awaiting Cabinet (re-checked 11 November 2026); few African cases publish false-alarm rates. The course says so where it matters.', 10)

h2(d, 'What the leader takes home')
bullets(d, ['A one-page take-away sheet from every session.',
            'The AI Opportunity Portfolio: candidate uses in your organisation, scored for value and feasibility, with people impact, risk and data readiness.',
            'From the practicals: a mapped workflow and business case, a people and skills plan, an AI use policy draft, a risk register, a vendor question list, a data inventory and scorecard, a roadmap and a 90-day plan, and the 30, 60 and 90-day follow-up kit.',
            'New learner documents: the Industry Use-Case Atlas (uses and named cases by industry) and the Questions to Ask sheet (for vendors, IT and the board). The Executive Edition\'s Formula Sheet is not part of this edition.'])

h2(d, 'How it will be built after approval')
bullets(d, [('Pilot.', 'Sessions 0 and 2 built in full (decks, notes, figures, take-aways) for your review: Session 0 sets the map and the threads, Session 2 shows the pattern of a concept session with its industry tour.'),
            ('Then the rest.', 'Sessions 1 and 3 to 14 in parallel, followed by a coherence pass across all fifteen, like the one done for the Executive Edition.'),
            ('Then the documents.', 'Handbook, workbook, take-away sheets, facilitator guide, presenter script, Industry Use-Case Atlas and Questions to Ask.')])

name = 'Course Map for Approval (11 Nov 2026)'
out = EDITION / '01 Course Overview'
save(d, out / (name + '.docx'))
__import__('lo_fonts').seed('-env:UserInstallation=file:///tmp/lo_map_lead')   # brand font for the PDF
subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_map_lead', '--headless', '--convert-to', 'pdf', '--outdir', str(out), str(out / (name + '.docx'))], capture_output=True, timeout=200)
print('wrote', out / (name + '.docx'))
