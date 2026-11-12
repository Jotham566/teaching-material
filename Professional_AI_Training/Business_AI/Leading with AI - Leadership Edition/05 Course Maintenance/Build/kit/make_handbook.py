"""Course Handbook, Leadership Edition: given to every leader in Session 0.

Run from Build/:  python3 kit/make_handbook.py
Writes 03 Learner Materials/Course Handbook.docx and .pdf, with the KLAi Word kit (templates_gen/docx_kit.py) and the drawn figures
of the slides (kit/diagrams_l00.py ... diagrams_l14.py, rendered through kit/diagrams.py and figkit at their slide sizes).

Single source: every session page is built from content/sNN.py (title, question, the titles of 'The idea' slides, the case slides
with their source lines, the words, what you keep) and kit/chain.py, so the handbook never disagrees with the slides. The industry
pages quote figures only as stated in research/*.md, and say so where a figure is the company's own.
Writing rules: LEADERSHIP_BIBLE.md (plain words, no maths, no em dashes, no prices of AI products).
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa: E402,F401,F403
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
import diagrams as DG  # noqa: E402
import chain as CH  # noqa: E402
import sessions_plan as SP  # noqa: E402

W = CONTENT_CM
BODY_SIZE = 10.5
IDEA_SIZE = (7.7, 4.8)     # slide placement of an 'idea' visual, inches (kit/deck.py k_idea)
WIDE_SIZE = (11.9, 4.25)   # slide placement of a 'wide' visual (kit/deck.py k_wide)
SHOWN = {'l00_family', 'l00_jobs', 'l00_grid', 'l00_promise', 'l00_route', 'l00_threads'}   # figures already drawn in Parts 1 to 3
SUBTITLE = 'Leading with AI  |  KLAi Professional Learning, Kampala  |  Instructor: Jotham Martin Wambi'


# ------------------------------------------------------------------ sessions, read fresh from content/
def load_sessions():
    out = {}
    for n in range(15):
        f = BUILD / 'content' / f's{n:02d}.py'
        spec = importlib.util.spec_from_file_location(f'hb_s{n:02d}', f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out[n] = m.SESSION
    return out


def phase_of(n):
    for code, name, nums in SP.PHASES:
        if n in nums:
            return code, name
    return '', ''


def idea_slides(S):
    """The slides of the 'The idea' section, in order."""
    out, on = [], False
    for sl in S['slides']:
        if sl.get('section') == 'The idea':
            on = True
        elif sl.get('section'):
            on = False
        if on:
            out.append(sl)
    return out


def _org(sl):
    v = sl.get('visual') or {}
    if v.get('org'):
        return v['org']
    t = sl['title']
    return t.split(':')[0] if ':' in t[:60] else ''


def case_slides(S, seen):
    """Named case slides (any drawn case with a source line, not the six-industry tour). Prefers organisations not yet met earlier."""
    cases = []
    for sl in S['slides']:
        v = sl.get('visual') or {}
        k = str(v.get('kind', ''))
        if isinstance(v, dict) and (v.get('source') or v.get('src')) and not k.endswith(('_six', '_tour')):
            cases.append(sl)
    fresh = [c for c in cases if _key(c) not in seen]
    pick = fresh[:3]
    if len(pick) < 2:
        pick += [c for c in cases if c not in pick][:2 - len(pick)]
    return pick


def _key(sl):
    return (_org(sl) or sl['title']).split(',')[0].split(':')[0].split('’')[0].strip().lower()[:18]


# ------------------------------------------------------------------ layout helpers
def page_break(doc):
    p = doc.add_paragraph(); fmt(p, 0, 0)
    p.paragraph_format.page_break_before = True
    p.paragraph_format.line_spacing = Pt(1)
    r = p.add_run(''); r.font.size = Pt(1)


def to_pdf(path):
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_docs', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True)


def bullets(d, items, size=BODY_SIZE, after=2):
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


def body(d, text, after=6, size=BODY_SIZE):
    return para(d, text, size, after=after)


def fig(d, data, size, width_cm=16.0, caption=None, after=6):
    """Embed a drawn figure rendered at its slide size (inches) and scaled to width_cm on the page."""
    w_in, h_in = size
    try:
        path = DG.render(data, w_in, h_in)
    except Exception as e:   # a figure another writer is editing must not stop the handbook
        print('SKIPPED FIGURE', data.get('kind'), type(e).__name__, str(e)[:160])
        return False
    if d.paragraphs:
        d.paragraphs[-1].paragraph_format.keep_with_next = True
    p = d.add_paragraph(); fmt(p, 2, 2 if caption else after, keep=bool(caption), align=WD_ALIGN_PARAGRAPH.CENTER)
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    if caption:
        para(d, caption, 8.5, italic=True, color='595959', after=after, align=WD_ALIGN_PARAGRAPH.CENTER)
    return True


def section(d, num, text, first=False, new_page=True):
    if not new_page:
        spacer(d, 18)
    elif not first:
        page_break(d)
    para(d, f'Part {num}', 9.5, True, color=RED, after=0, keep=True)
    para(d, text, 18, True, after=6, keep=True)


def _short(label):
    """A short bar label for a clock line of a session file."""
    lo = label.lower()
    for key, short in (('recall', 'Recall and question'), ('idea', 'Idea, tour, cases'), ('demonstration', 'Demonstration'), ('break', 'Break'),
                       ('people', 'Your people'), ('hands-on', 'Hands-on: portfolio'), ('decision', 'Decision'), ('close', 'Close')):
        if key in lo:
            return short
    return label.split(':')[0]


def _limit(v, title=''):
    """The caution of a case slide, as plain sentences (never labelled 'the catch'), without sentences that repeat the title."""
    t = v.get('catch')
    if not isinstance(t, str):
        return ''
    t = re.sub(r'^\s*the catch\s*[:,.-]?\s*', '', t, flags=re.I).strip()
    seen = set(re.findall(r'[a-z]{5,}', title.lower()))
    keep = []
    for sent in re.split(r'(?<=[.!?])\s+', t):
        words = set(re.findall(r'[a-z]{5,}', sent.lower()))
        if words and len(words & seen) / len(words) >= 0.6:
            continue
        keep.append(sent)
    t = ' '.join(keep)
    return t[:1].upper() + t[1:] if t else ''


def _src(text):
    t = text.strip()
    return t if t.lower().startswith('source') else 'Source: ' + t


# ------------------------------------------------------------------ the six industries (figures as stated in research/*.md)
CO = 'Company figures.'
INDUSTRIES = [
    ('Banking and microfinance', 'cases_banking_telecom.md',
     'Prediction pays first: credit scoring for small loans and fraud blocking. Most African results are the banks’ own figures.',
     [('KCB Group, Kenya (BNK-02)', 'Scoring models decide who gets a mobile loan and how much.',
       'Mobile lending of Sh544 billion in 2025, up 30% year on year. No figure on loan quality was published.', 'From KCB’s integrated report, as reported.', 'The Star (Kenya), 7 May 2026'),
      ('Capitec Bank, South Africa (BNK-07)', 'AI blocks fraudulent payees and scam payments.',
       'More than 394,000 scam payments prevented and about R673 million in potential client losses avoided. Total staff rose by 711.', CO, 'TechCentral, 22 Apr 2026'),
      ('Numida, Uganda (BNK-03)', 'Scores micro-businesses only from what the customer enters in the app.',
       '$20 million of working capital lent to date (Sept 2022). No repayment or default rates were published.', 'Figures from 2022 fundraising coverage.', 'TechCrunch, 28 Sep 2022'),
      ('Commonwealth Bank of Australia (BNK-09)', 'Cut 45 call-centre jobs for a voice bot.',
       'The roles were reinstated: the bank said its assessment “did not adequately consider all relevant business considerations”.', 'Two independent sources.', 'The Register, 22 Aug 2025')],
     'Bank of Uganda is building an AI governance framework that requires human oversight (BNK-04; in development, November 2025).'),
    ('Telecom and mobile money', 'cases_banking_telecom.md',
     'Mobile-money records feed credit scores, and AI watches billions of transactions for fraud and scams.',
     [('M-Shwari, Kenya (TEL-01)', 'Lending decisions from phone and M-Pesa history.',
       '20.6 million loans worth $277 million to 2.8 million borrowers since November 2012; non-performing loans 2%.', 'CGAP, with the partners’ data; figures from 2015.', 'CGAP, 2 Apr 2015'),
      ('Safaricom, Kenya (TEL-03)', 'Machine-learning models watch M-Pesa transactions and flag unusual patterns.',
       'Found inflated agent deposits totalling 1.7 billion shillings and laundering through betting platforms. No detection or false-alarm rate is published.', CO + ' Not audited.', 'iGamingToday, 21 Oct 2025'),
      ('Airtel Africa, Uganda and Tanzania (TEL-05)', 'An AI spam alert on SMS scams; launched in Uganda on 16 Apr 2025.',
       'Tanzania: fraud cases on Airtel’s network fell about 56% in a quarter, while TTCL fell 58% without this product.', 'Regulator data, reported by a daily paper. Before and after, so it does not prove the cause.', 'The Citizen (Tanzania), 18 Jul 2025'),
      ('Airtel Money Uganda and GnuGrid CRB (TEL-06)', 'A credit score built from mobile-money data.',
       'Draws on data from 14 million Airtel Money wallets. No result on approvals or defaults has been published.', 'A launch announcement.', 'TechAfrica News, 24 Jan 2024')],
     'In 2026 Safaricom’s Zuri chatbot and credit algorithms were challenged in Kenya’s High Court (TEL-04).'),
    ('Agriculture and agribusiness', 'cases_agri_manufacturing.md',
     'AI reads crop photos and farm paperwork, scores farmers for input credit, and answers advisory questions in local languages.',
     [('PlantVillage Nuru, Tanzania and Kenya (AGR-01)', 'Names cassava disease from a phone photo, even offline.',
       '74 to 88% accurate when it examined six leaves per plant; 49% on a single leaf in the field.', 'Peer-reviewed; figures from 2020.', 'Frontiers in Plant Science, 18 Dec 2020'),
      ('Apollo Agriculture, Kenya (AGR-03)', 'Satellite images and machine learning decide which smallholders get seed and fertiliser on credit.',
       'About 100,000 farmers served by the end of 2021. No repayment or default rate is published.', CO + ' From funding announcements.', 'TechCrunch, 21 Mar 2022'),
      ('One Acre Fund, Burundi (AGR-07)', 'Software reads scanned delivery forms; staff check what it flags.',
       'More than 80,000 forms in 2 to 3 weeks; work fell from more than 1,000 person-days per cycle to an estimated 300 to 500.', 'A vendor’s customer story; the cut is an estimate.', 'Dataiku, 30 Jul 2026'),
      ('Digital Green Farmer.Chat, Kenya and India (AGR-04)', 'A chatbot that answers only from a checked library of farming advice.',
       'More than 15,000 users asked more than 300,000 questions; it answered about 75% of them.', 'Research paper by the builders.', 'arXiv, 8 Oct 2024')],
     'Gro Intelligence, founded in Kenya, shut down in June 2024 after failing to raise new financing (AGR-05).'),
    ('Manufacturing and FMCG', 'cases_agri_manufacturing.md',
     'Ordering suggestions for shops, shelf photos read by AI, and factory lines tuned by AI. East African results so far are about digital ordering.',
     [('Coca-Cola and its bottlers, Malaysia (MFG-03)', 'AI suggests an order for each shop; the shopkeeper decides.',
       '83% of the shops that joined the campaign adopted the recommendations (January to April 2026). No sales uplift was disclosed.', CO, 'AI News, 8 Sep 2026'),
      ('Coca-Cola HBC, Europe and Africa (MFG-04)', 'Image recognition reads shelf photos taken on sales visits.',
       'About 60 to 70% of sales visits use image recognition.', 'From an interview with the company’s chief digital officer.', 'Just Drinks, 12 Dec 2023'),
      ('Unilever with Accenture (MFG-07)', 'A live digital copy of each factory line predicts problems.',
       'At Gandhidham, India, quality defects fell 30% over four years. At Poznan, Poland, waste fell nearly 30%.', CO + ' Most without a period or baseline.', 'Intelligent CIO, 16 Jun 2026'),
      ('Heidelberg Materials, Czech Republic (MFG-11)', 'AI adjusts a cement kiln through the day.',
       'In the first month the fuel cost index fell 4.1%, checked by switching the system on for one month and off for the next.', CO + ' One plant, one month.', 'World Cement, 8 Oct 2024')],
     'Nile Breweries’ BEES ordering app in Uganda had about 1,000 users in its first nine days (2022). It does not use AI yet: digital ordering comes first (MFG-05).'),
    ('Healthcare and insurance', 'cases_health_public.md',
     'AI checks clinicians’ notes, sorts scans and messages, and screens claims for fraud. The person still decides.',
     [('Penda Health, Nairobi (HLT-01)', 'A language model reads clinical notes and shows a traffic-light alert.',
       'Across 39,849 visits in 15 clinics: 16% fewer diagnostic errors and 13% fewer treatment errors.', 'A preprint; OpenAI co-built the tool and funded the study.', 'arXiv, 22 Jul 2025'),
      ('Jacaranda Health PROMPTS, Kenya (HLT-02)', 'AI triages mothers’ text messages so the urgent ones reach a person first.',
       'Cut help-desk workload by about 12%; more than 350,000 active users (Feb 2023).', 'User numbers are the organisation’s own.', 'Penn State News, 6 Feb 2023'),
      ('MASAI trial, Sweden (HLT-10)', 'AI scores mammograms; low-risk scans get one radiologist, high-risk two.',
       '80,033 women; 41 more cancers found and 44% less radiologist reading work.', 'A randomised trial, interim results.', 'News-Medical, reporting The Lancet Oncology, 1 Aug 2023'),
      ('Kenya Social Health Authority (HLT-05)', 'An AI engine screens insurance claims for fraud.',
       'A ministry audit found Sh11 billion lost to fraudulent claims; a parliamentary committee found reliance on AI “with insufficient human oversight” led to unjust denials.', 'Government and parliamentary sources.', 'Capital FM, 29 Jan 2026; The Star, 15 Oct 2025')],
     'The Epic Sepsis Model, tested independently at one US hospital, missed 67% of sepsis patients and alerted on 18% of all inpatients (HLT-11).'),
    ('Public sector', 'cases_health_public.md',
     'Revenue authorities cross-check records and pre-fill returns; courts transcribe hearings. Failures here hurt citizens at scale.',
     [('Uganda Revenue Authority (PUB-01)', 'AI cross-checks records and flags the ones that do not match.',
       'The Commissioner General said URA recovered 200 billion shillings in revenue leakages uncovered through AI in one year.', 'A speech claim with no published method.', 'URA, 8 Apr 2025'),
      ('South African Revenue Service (PUB-03)', 'Assessments issued without a return; refunds checked before money leaves.',
       'Nine days into the July 2025 filing season, 65% of taxpayers had been assessed without filing.', 'SARS’s own figures, reported by media.', 'The Citizen, 18 Jul 2025'),
      ('Judiciary of Kenya (PUB-04)', 'Speech-to-text software types court records.',
       'The Chief Justice put accuracy at about 80%, up from about 30% when testing began.', 'From a speech; not measured independently.', 'Tech-ish, 13 Aug 2025'),
      ('Togo, Novissi (PUB-07)', 'Machine learning on phone data targets emergency cash to the poorest.',
       'Enrolled 138,500 recipients; cut exclusion errors by 4 to 21% against giving to everyone in selected villages. Households without a phone, about 15%, would be missed.', 'Peer-reviewed research.', 'J-PAL, updated Jun 2026')],
     'The Dutch childcare benefits scandal: tens of thousands of parents were wrongly told to repay benefits (PUB-11).'),
]

TEMPLATES = [
    ('AI Opportunity Portfolio', 'Your one-page register of possible AI uses. It grows every session and becomes your main take-home.', 'Every session'),
    ('Vendor Question List', 'The questions to put to a supplier, and the answers that should worry you.', '6, 13'),
    ('Reusable Brief Template', 'A five-part brief for a team task: role, context, examples, format, constraints.', '7'),
    ('Reliability Test Record', 'The count from testing a brief on ten past cases whose answers you know.', '7'),
    ('Tool Boundary Sheet', 'What an agent may read, write, send and spend; who approves; the log and the off switch.', '10'),
    ('Task Card', 'One task on a card: owner, how often, time today.', '11'),
    ('Use-Case Scorecard', 'Several candidate tasks side by side, to choose the one to map first.', '11'),
    ('Business Case Workbook', 'Time saved, errors avoided and revenue in shillings: the payback period and the first-year gain.', '11'),
    ('People and Skills Plan', 'One role redesigned task by task, skills by level, the fears and your answers, champions and the briefing.', '12'),
    ('AI Use Policy Template', 'A one-page acceptable use policy: tools, data, review, owners, incidents, a review date.', '13'),
    ('Risk Register', 'Each risk scored for how likely and how bad, with an owner and a control.', '13'),
    ('Information Inventory', 'Every data source with its owner, who may see it, and whether it is ready.', '14'),
    ('90-Day Roadmap', 'Owners, dates, success measures and check-ins at day 30, 60 and 90.', '14'),
]
FOLLOW_UP = [
    ('30-60-90 Check-in Form', 'A one-page form you return at day 30, 60 and 90: what is running, what it saves, what changed.'),
    ('Results Tracker', 'The few numbers you record each month for your first AI use.'),
    ('Sponsor Briefing', 'A short brief for the senior sponsor of your first 90 days.'),
]


# ------------------------------------------------------------------ the document
def build():
    SS = load_sessions()
    name = 'Course Handbook'
    d = new_doc(name, 'Leading with AI, Leadership Edition: Course Handbook')

    # ---------------------------------------------------------------- cover and contents
    title(d, 'Course Handbook', SUBTITLE)
    para(d, 'Where AI pays in your industry, and what it changes for the people who work for you.', 13, True, after=8)
    body(d, 'You receive this handbook in Session 0; read it in any order. It covers who the course is for, how it runs, one page for each of the fifteen '
            'sessions, the four jobs AI does, four cases from each of the six main industries, the glossary and the templates. The session pages are '
            'generated from the same files as the slides, so the two agree.')
    h2(d, 'What is inside')
    grid(d, [
        ['1', 'Who this course is for, and the promise'],
        ['2', 'How the course works: four phases, three threads, no maths and no tests'],
        ['3', 'The four jobs AI does'],
        ['4', 'Session by session: one page for each of Sessions 0 to 14'],
        ['5', 'The six main industries at a glance'],
        ['6', 'Glossary: every word from every session'],
        ['7', 'The templates and the follow-up kit'],
        ['8', 'What to prepare'],
    ], [1.2, W - 1.2], header=['Part', 'Title'], size=10, label_cols=(0,))
    spacer(d, 8)
    box(d, 'A note on numbers', [
        'There is no mathematics in this course or in this handbook. Numbers appear only as a leader uses them: counts, percentages and shillings.',
        'Every figure about a real organisation comes from a named, dated source, given in a short line. Where a figure is the company’s own, we say so. '
        'Nile Valley Foods Ltd, the distributor in Jinja used in the demonstrations, is fictional.'])

    # ---------------------------------------------------------------- 1 promise
    section(d, 1, 'Who this course is for, and the promise')
    body(d, 'Leading with AI is for the people who decide where AI goes in an organisation: chief executives, managing directors, board members, directors and '
            'senior managers, in any sector. The main industries are banking and microfinance, telecom and mobile money, agriculture and agribusiness, '
            'manufacturing and FMCG, healthcare and insurance, and the public sector. Energy, retail and logistics, education, and legal and professional '
            'services also appear. You need no maths and no technical background, and none is taught.')
    fig(d, {'kind': 'l00_promise'}, IDEA_SIZE, 13.0)
    h2(d, 'By the end of Session 14 you will be able to')
    bullets(d, ['Name where AI creates value in your industry and in your own organisation.',
                'Question a vendor or your own team about the evidence, the data, the cost and the risk of an AI proposal.',
                'Judge an accuracy claim, a pilot result and a risk.',
                'Plan the change for your staff: which roles and tasks change, what skills they need and what they fear.',
                'Start a costed, governed 90-day plan from an AI Opportunity Portfolio of your own organisation.'])
    h2(d, 'Uganda and East Africa first')
    body(d, 'Examples start at home, then the rest of Africa, then the world. Every real case is named, dated and sourced, and comes with its limits: '
            'what it cost, what went wrong, or what the figure does not prove.')

    # ---------------------------------------------------------------- 2 how it works
    section(d, 2, 'How the course works')
    body(d, 'Fifteen sessions of two hours, Session 0 to Session 14, each built on the one before. They fall into four phases.')
    fig(d, {'kind': 'l00_route'}, WIDE_SIZE, 16.0)
    rows = []
    for code, pname, nums in SP.PHASES:
        rows.append([f'{code}. {pname}', '\n'.join(f'{n}  {SS[n]["title"]}' for n in nums)])
    grid(d, rows, [5.0, W - 5.0], header=['Phase', 'Sessions'], size=9.5, label_cols=(0,))
    spacer(d, 4)
    body(d, 'Sessions 0 to 10 explain one idea at a time, with an industry tour, real cases, a recorded demonstration and a hands-on on your own organisation. '
            'Sessions 11 to 14 are practicals: about an hour of each goes to your own workflow, people plan, rules and 90-day plan, with the instructor beside you.')

    page_break(d)
    h2(d, 'Three threads run through every session', before=0)
    fig(d, {'kind': 'l00_threads'}, WIDE_SIZE, 16.0)
    bullets(d, [('Your industry.', 'In Session 0 you choose your industry. Sessions 1 to 10 each tour six industries with one use of the day’s idea, then tell one to three named cases: what the AI does, the result, and what the figure leaves out.'),
                ('Your people.', 'Sessions 1 to 10 each ask which roles use the idea, which tasks change, what skills staff need, and what employees fear or gain. Session 12 brings these together into a people plan.'),
                ('Your AI Opportunity Portfolio.', 'A one-page register of possible AI uses in your organisation. Sessions 1 to 10 each add one or two entries. Session 11 scores them on value and feasibility, 12 adds the people impact, 13 the risk, and 14 the data readiness and the 90-day plan.')])
    h2(d, 'How a session runs')
    c1 = SS[1]['clock']
    fig(d, {'kind': 'bars', 'unit': ' min', 'items': [{'label': _short(lab), 'value': v, 'hl': lab.lower().startswith('hands-on')} for v, lab in c1]},
        (11.9, 3.6), 14.0, caption='The two hours of Session 1, as an example of Sessions 1 to 10. In the practicals, 11 to 14, about an hour goes to your own work.')
    h2(d, 'No maths, no tests, no homework')
    body(d, 'Every idea is explained with a picture and an everyday comparison: a new employee learning from past files, a house-sitter with only the keys you give. '
            'There are no tests and no marks, and anything between sessions is optional. You show progress by what you decide and what you keep.')
    h2(d, 'After the course')
    body(d, 'The instructor checks in with you at day 30, 60 and 90. You return a one-page check-in form and a results tracker: what is running, what it saves, what changed.')

    # ---------------------------------------------------------------- 3 four jobs
    section(d, 3, 'The four jobs AI does')
    body(d, 'AI is a family. Rules are written by people and do not learn. Machine learning learns a pattern from past examples. Inside it, generative AI writes new '
            'text, pictures or code. Inside that, agents are generative AI given tools so they can act.')
    fig(d, {'kind': 'l00_family'}, IDEA_SIZE, 12.5)
    body(d, 'Every AI use in your industry is one of four jobs, or a chain of them. When a vendor pitches you something, ask which of the four it does.')
    fig(d, {'kind': 'l00_jobs'}, WIDE_SIZE, 16.0)
    h2(d, 'Where to start')
    body(d, 'Two questions place any use: what does a mistake cost, and how easily can someone check the answer? Start where a mistake is cheap and checking is easy, '
            'such as drafting replies or sorting messages. Where a mistake is costly and hard to check, such as a loan decision or a diagnosis, keep a person in charge.')
    fig(d, {'kind': 'l00_grid'}, IDEA_SIZE, 12.5)

    # ---------------------------------------------------------------- 4 sessions, one page each
    seen = set()
    for n in range(15):
        S = SS[n]
        page_break(d)
        code, pname = phase_of(n)
        para(d, f'Part 4  |  Session {n}  |  Phase {code}: {pname}', 9, True, color=RED, after=0, keep=True)
        para(d, S['title'], 17, True, after=4, keep=True)
        p = para(d, '', 11.5, after=6, keep=True)
        add_run(p, 'The question:  ', 11.5, True)
        add_run(p, S['question'], 11.5, False, True)
        ideas = idea_slides(S)
        vis = next((sl for sl in ideas if isinstance(sl.get('visual'), dict) and sl['visual'].get('kind') not in SHOWN), None)
        if vis:
            size = IDEA_SIZE if vis['kind'] == 'idea' else WIDE_SIZE
            fig(d, vis['visual'], size, 11.0 if size == IDEA_SIZE else 15.0, after=4)
        h2(d, 'What the session explains', before=2, after=2)
        bullets(d, [sl['title'] for sl in ideas], size=9.5, after=1)
        cases = case_slides(S, seen)
        if cases:
            h2(d, 'Named cases', before=6, after=2)
            for sl in cases:
                seen.add(_key(sl))
                v = sl['visual']
                p = para(d, '', 9.5, after=0, keep=True)
                add_run(p, sl['title'] + '.', 9.5, True)
                lim = _limit(v, sl['title'])
                if lim:
                    add_run(p, '  ' + lim, 9.5)
                para(d, _src(v.get('source') or v.get('src')), 8, italic=True, color='595959', after=4)
        words = [w[0] for w in S.get('words', [])]
        if words:
            p = para(d, '', 9.5, before=2, after=4)
            add_run(p, 'New words:  ', 9.5, True)
            add_run(p, ', '.join(words) + ' (see the glossary, Part 6).', 9.5)
        box(d, 'What you keep', [S['keep']], size=9.5)
        if n in CH.CHAIN:
            c = CH.CHAIN[n]
            on = '; '.join(f'Session {k}, {t}' for k, t in c['on'])
            line = f'Builds on: {on}.   Leads to: {c["leads"]}.'
        else:
            line = 'The start: the vocabulary and the map every later session uses. Leads to: ' + S.get('next', 'Session 1')
        para(d, line, 8.5, color='404040', after=0)

    # ---------------------------------------------------------------- 5 industries
    section(d, 5, 'The six main industries at a glance')
    body(d, 'One real organisation and its AI job in each of the six main industries. The tables that follow give four cases per industry from the course case bank, '
            'with the result as the source states it. A note says where a figure is the company’s own, and the source line gives the publisher and date. '
            'The Industry Use-Case Atlas has more cases for every industry.')
    fig(d, {'kind': 'l00_tour'}, WIDE_SIZE, 16.0)
    for i, (ind, _f, pays, cases, watch) in enumerate(INDUSTRIES):
        if i % 2 == 0:
            page_break(d)
        h2(d, ind, before=0 if i % 2 == 0 else 10, after=2)
        para(d, pays, 10, after=4, keep=True)
        grid(d, [[f'{org}\n~{what}', f'{res}\n~{note}', src] for org, what, res, note, src in cases],
             [5.4, 8.6, W - 14.0], header=['Organisation and what the AI does', 'Result as reported', 'Source'], size=8.5, label_cols=())
        p = para(d, '', 9, before=4, after=2)
        add_run(p, 'Also in this sector:  ', 9, True)
        add_run(p, watch, 9)

    # ---------------------------------------------------------------- 6 glossary
    section(d, 6, 'Glossary')
    body(d, 'Every word from the “Words” slide of each session, with the sessions that use it. Where a word returns in a later session, '
            'the first explanation is the one given here.')
    G = {}
    for n in range(15):
        for term, text in SS[n].get('words', []):
            k = term.lower()
            if k in G:
                G[k][2].append(n)
            else:
                G[k] = [term, text, [n]]
    rows = sorted(G.values(), key=lambda t: t[0].lower())
    grid(d, [[a, b, ', '.join(str(x) for x in c)] for a, b, c in rows], [4.4, W - 6.2, 1.8], header=['Word', 'Meaning', 'Session'], size=9, label_cols=(0,))

    # ---------------------------------------------------------------- 7 templates
    section(d, 7, 'The templates and the follow-up kit')
    body(d, 'You keep and reuse everything you fill in during the course. The templates are in the Templates folder of your learner materials, the follow-up kit in '
            'the Follow-up Kit folder, and each session has a one-page take-away sheet.')
    fig(d, {'kind': 'l00_portfolio'}, IDEA_SIZE, 12.0, caption='The AI Opportunity Portfolio: one row per possible use, one more column every few sessions.')
    grid(d, [list(t) for t in TEMPLATES], [4.6, W - 6.6, 2.0], header=['Template', 'What it is for', 'Session'], size=9, label_cols=(0,))
    h2(d, 'Your other learner materials', before=10)
    grid(d, [['Learner Workbook', 'One page for each session: the steps for the hands-on, the fields to fill in, and your decision.'],
             ['Take-away Sheets', 'One page for each session: what to remember and what you keep.'],
             ['Industry Use-Case Atlas', 'Every named case of the course and more, grouped by industry: what the AI does, the result, its limits and the source.'],
             ['Questions to Ask', 'The questions from every session, for your vendors, your IT and data teams and your board.']],
         [4.6, W - 4.6], header=['Document', 'What it is for'], size=9, label_cols=(0,))
    h2(d, 'The follow-up kit', before=10)
    grid(d, [list(t) for t in FOLLOW_UP], [4.6, W - 4.6], header=['Item', 'What it is for'], size=9, label_cols=(0,))
    spacer(d, 6)
    body(d, 'The Practice Files folder holds the files of Nile Valley Foods Ltd, the fictional distributor used in the demonstrations: customer messages, '
            'sales, supplier invoices and agreements, a staff handbook extract and a vendor proposal. Use them, or invented information, never real personal data.', size=10)

    # ---------------------------------------------------------------- 8 prepare
    section(d, 8, 'What to prepare', new_page=False)
    body(d, 'There is nothing to read, install or study before the course. The one decision is your industry, which you choose in Session 0: the one you lead in, '
            'or the one you most want to understand. Sessions 1 to 10 each give your industry one use of the day’s idea, and your portfolio fills with uses for your own organisation.')
    h2(d, 'If you have time before Session 0')
    bullets(d, ['Note two or three tasks in your organisation that take many hours, repeat every week, or wait on one person.',
                'Ask your team three questions, without blame: which AI tools do you already use, for what, and what would help you use them safely?',
                'Bring a laptop or phone with an AI assistant you already use, if you wish to try the demonstrations. Use invented or sample information only.'])
    spacer(d, 10)
    box(d, 'Your industry', ['~Write it here, and keep it for the whole course:', ' ', ' '])
    spacer(d, 10)
    para(d, 'Jotham Martin Wambi  |  KLAi Professional Learning, Kampala  |  jothammartin.wambi@gmail.com  |  +256 750 990 718', 9, color='404040')

    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out)
    to_pdf(out)


if __name__ == '__main__':
    build()
