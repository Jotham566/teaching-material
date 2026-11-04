"""Course-level Word and PDF documents for AI and Data Science Professional (KLAi edition).
    python3 kit/make_course_docs.py [outline|setup|projects|benchmark|all]
Writes (each .docx and .pdf):
  01 Course Overview/Course Outline
  03 Learner Materials/Student Setup Guide
  03 Learner Materials/Course Projects Guide
  04 Facilitator Materials/Benchmark and Design Report
Session titles, questions, deliverables and project milestone tables are read from content/sNN.py through kit/deck.load, so the documents match the decks.
Never edit the generated files by hand; change this file and run it again. Reuses the KLAi Word kit in templates_gen/docx_kit.py."""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
import docx_kit  # noqa: E402
import deck  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

W = CONTENT_CM
COURSE = 'AI and Data Science Professional'
docx_kit.FOOT = f'KLAi | {COURSE} | '
UPDATED = '4 November 2026'

# Short lab deliverables: one source, shared with the roadmap.
sys.path.insert(0, str(HERE))
from make_roadmap_klai import DELIVERABLE, MARK_LONG as MARK  # noqa: E402

_SESS = {}


def S(n):
    if n not in _SESS:
        _SESS[n] = deck.load(n)
    return _SESS[n]


def all_sessions():
    return [S(n) for n in range(1, 25)]


def to_pdf(path):
    subprocess.run(['soffice', f'-env:UserInstallation=file:///tmp/lo_docsB{os.getpid()}', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)],
                   capture_output=True, timeout=300)


def new(template_name, subject=COURSE):
    d = new_doc(template_name, subject)
    for tbl in d.sections[0].header.tables:
        for row in tbl.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        if 'Mathematics for AI' in r.text:
                            r.text = f'{COURSE}  |  KLAi'
    d.core_properties.keywords = 'KLAi, AI, data science, course'
    return d


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


def numbered(d, items, size=10, after=2):
    for i, it in enumerate(items, 1):
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        add_run(p, f'{i}.  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def body(d, text, size=10, after=4, **kw):
    return para(d, text, size, after=after, **kw)


def clock_rows(s):
    t, rows = 0, []
    for m, lab in s['clock']:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), lab])
        t += m
    return rows


def slide_table(num, starts):
    for x in S(num)['slides']:
        if x['title'].startswith(starts):
            return x
    raise KeyError((num, starts))


MODULES = [('A', 'Think with data', 1, 4), ('B', 'Python for data', 5, 9), ('C', 'Analyse and explain', 10, 13),
           ('D', 'Machine learning', 14, 19), ('E', 'Neural networks and text', 20, 22), ('F', 'Ship it and present', 23, 24)]


# ====================================================================================== COURSE OUTLINE
def outline():
    d = new('Course outline')
    title(d, COURSE, f'Course outline  |  48 hours, 24 sessions of 2 hours  |  Updated {UPDATED}')
    h2(d, 'What it is', 0)
    body(d, 'A live course that takes a working professional from an Excel spreadsheet to a tested model and a small web app. It follows one path in 24 sessions: think with data, '
            'Python for data, analyse and explain, machine learning, neural networks and text, then ship it and present. Every tool is free. Every dataset is fictional and set in Uganda '
            '(a retail chain, a microfinance lender, district clinics and customer messages, in shillings), so no real person or company is exposed. The tutor is Jotham Martin Wambi of KLAi Professional Learning.')
    h2(d, 'Who it is for')
    bullets(d, [('Working professionals in Uganda and East Africa', 'who handle tables and reports: analysts, accountants, credit and finance officers, programme and monitoring staff, ministry and NGO officers, managers.'),
                ('Employers', 'who want staff to move from spreadsheets to data work they can check, explain and repeat, without buying software.')])
    h2(d, 'Entry requirements')
    bullets(d, [('Confident in Excel or Google Sheets.', 'You can write a formula, sort and filter, and have seen a pivot table.'),
                ('No code needed.', 'Python is taught from the first line, beside the spreadsheet idea it replaces.'),
                ('No statistics needed.', 'Averages, spread, sampling and tests are taught with pictures and small examples.'),
                ('A laptop and a free Google account.', 'Windows or Mac, with a browser and a charger. Nothing to install. A free GitHub account is needed from Session 23. No paid account, API key or graphics card is ever required.')])
    h2(d, 'What you will be able to do')
    bullets(d, ['Turn a business question into a decision, and check the data behind it before you report a number.',
                'Read a table by its records, variables and keys, then summarise and chart it fairly in a spreadsheet.',
                'Load, clean, group and join data in Python with pandas, keep a data cleaning log, and prove that a total reconciles to a control total.',
                'Ask a database the same questions in SQL, and check the answer against pandas.',
                'Explore a new dataset in a fixed order and write a finding with a number, a comparison and a limit.',
                'Test whether a difference between two groups is real, and fit and read a regression model.',
                'Build, test and judge classification, clustering and forecasting models against a baseline model, and catch data leakage.',
                'See how a neural network learns, turn text into numbers, and make a small assistant answer from your own documents, with a test and an audit log.',
                'Save a model, publish a small app, and check it for fairness and data protection before anyone relies on it.',
                'Present a result to a manager: the answer, the evidence beside a baseline, and the limits.'])
    h2(d, 'How every session runs (2 hours)')
    grid(d, clock_rows(S(2)), [2.0, 2.0, 13.4], header=['Starts', 'Minutes', 'What happens'], size=9)
    spacer(d, 5)
    body(d, 'Concepts come first. For 45 minutes the laptops stay closed while you see a picture, hear the idea in plain words, and follow one example by hand. Each idea is given its real industry name '
            'with a plain explanation beside it (for example record, standard deviation, residual, decision threshold), so you can follow documentation, job interviews and later courses. '
            'Then you open the notebook or the sheet once and work for 45 minutes: predict the answer, run the cell, read the output, and change one thing. Automatic check cells tell you whether your numbers match. '
            'Every session ends with an exit check and a file or note you keep. Slides are shared as PDFs, written in full sentences, so you can revise without the tutor.')
    h2(d, 'The 24 sessions')
    for letter, name, a, b in MODULES:
        h2(d, f'Module {letter}: {name}  (Sessions {a} to {b})', 4, 2)
        rows = []
        for n in range(a, b + 1):
            s = S(n)
            mark = f'\n{MARK[n]}' if n in MARK else ''
            rows.append([str(n), s['title'], s['question'], DELIVERABLE[n] + mark])
        grid(d, rows, [0.9, 5.0, 6.7, 4.8], header=['#', 'Session', 'Question of the day', 'Lab deliverable'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    body(d, 'Sessions 1 to 4 and the planning half of Session 24 are spreadsheet work with no code. Sessions 5 to 23 have a Python notebook for Google Colab.', 9.5)
    h2(d, 'Tools: all free')
    grid(d, [['Spreadsheets', 'Google Sheets, or Excel, or LibreOffice Calc'],
             ['Python in the browser', 'Google Colab, with pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib and seaborn'],
             ['Databases', 'SQLite, run inside Python'],
             ['Neural networks and text', 'TensorFlow Playground in the browser; sentence-transformers (all-MiniLM-L6-v2) run inside Colab'],
             ['Sharing and shipping', 'Git and GitHub; Streamlit Community Cloud for a small public app'],
             ['Optional help', 'Any free chat assistant you already use. Every lab runs without one.']], [4.4, 13.0], size=9, label_cols=(0,))
    spacer(d, 3)
    body(d, 'Free services change their limits. Where the course quotes a limit it says so, and tells you to check the current terms.', 9.5)
    h2(d, 'What your employer gets')
    body(d, 'Each session ends with a task you can do at work the next Monday. A few examples taken from the sessions:', 9.5, after=2)
    bullets(d, [S(n)['use_at_work'] for n in (8, 10, 12, 15, 22, 23)], 9.5)
    h2(d, 'No exams, no marks: practical projects you keep')
    bullets(d, ['There is no exam and no assessment of any kind. No marks, grades, pass marks or weights. You build practical projects and you keep them.',
                'Each lab has automatic check cells that print OK or NOT YET, so you see at once whether your numbers match. The check cells, the recall questions and the exit-check questions are self-checks. Nobody marks them.',
                'Three project milestones: Session 8 (a cleaned file with its log and a reconciliation note), Session 13 (a one-page analysis report) and Session 19 (a tested model beside a baseline model). You show each to your tutor for feedback.',
                'The course project: you scope a question in Session 13, choose a dataset in Session 14, test a model in Session 19, publish a small app and model card in Session 23, and present for ten minutes in Session 24. The Course Projects Guide has the details and a project checklist for feedback.'])
    h2(d, 'Certificate and what you keep')
    bullets(d, ['A certificate of completion from KLAi Professional Learning, given for completing the course project. There are no criteria beyond that.',
                'A project from your own question: your course project notebook, a small app and model card on your own GitHub, and your ten-minute talk. Most learners use a course dataset. If your employer agrees in writing and the data holds no personal details, you may use work data.',
                'A folder of files from the 24 labs (cleaned data, query book, charts, model comparison, scored files) that you can show an employer.',
                'An external credential or university accreditation is not part of the course.'])
    h2(d, 'What the course does not cover')
    body(d, 'Forty-eight hours is short, so the course teaches the working core and says where it stops. These are covered in Session 24 with a free next step for each.', 9.5, after=2)
    bullets(d, [r[0] + ': ' + r[1] for r in slide_table(24, 'What this course did not cover')['rows']], 9.5)
    body(d, 'Dates and fees are on the course flyer.', 9.5, before=4)
    return d


# ====================================================================================== STUDENT SETUP GUIDE
def setup():
    d = new('Student Setup Guide')
    title(d, f'Get ready for {COURSE}', 'Student Setup Guide  |  About 30 minutes  |  Costs nothing  |  Do this before Session 1')
    body(d, 'Every tool in this course is free. You never need a paid account, an API key, a graphics card or software to install. You need a laptop (Windows or Mac) with a browser and a charger. '
            'Free services change their limits from time to time. Where this guide gives a limit it says "at the time of writing", which means early November 2026. Check the provider\'s page for the current terms.')
    grid(d, [['1', 'A Google account', 'Session 1', ''], ['2', 'Open Google Colab once, run a cell and save a copy', 'Session 5 (a try before Session 1 helps)', ''],
             ['3', 'Know how the data file, data.zip, reaches a notebook (Google Drive link)', 'Sessions 5 to 23', ''], ['4', 'Open the Lakeside workbook in Google Sheets or Excel', 'Sessions 1 to 4', ''],
             ['5', 'A free GitHub account', 'Session 23', ''], ['6', 'Streamlit Community Cloud (optional, after Session 23)', 'After Session 23', '']],
         [1.0, 8.4, 5.6, 2.4], header=['#', 'What', 'Needed for', 'Done'], size=9, label_cols=(0,))
    h2(d, '1. A Google account', 10)
    body(d, 'Google Colab (where you run Python) and Google Sheets both use a free Google account. If you have a Gmail address, you have one. If not, make one at accounts.google.com and write the password somewhere safe. '
            'If you do not want a Google account, tell your tutor before Session 1. There is a route that runs Python on your own laptop.')
    h2(d, '2. Open Google Colab once')
    numbered(d, ['Go to colab.research.google.com and sign in with your Google account.',
                 'Choose New notebook.',
                 'In the first cell type: print("Hello from Colab")',
                 'Press the play button beside the cell. You should see Hello from Colab under the cell.',
                 'Choose File, then Save a copy in Drive. Your tutor\'s notebooks open the same way: in Google Drive, double-click the notebook file, or choose Open with, then Google Colaboratory.'])
    body(d, 'Menu names can change a little when Google updates Colab. If a name is missing, look for the same words in the nearby menu or ask your tutor.', 9.5, before=2)
    box(d, 'Two menu items you will use in every session', ['Runtime, then Run all: runs every cell from the top.',
                                                              'Runtime, then Restart session and run all: starts from a clean session. If the notebook finishes with no red text, it works from the top.'])
    h2(d, '3. The data file: how data.zip reaches a notebook')
    body(d, 'Your tutor keeps data.zip on Google Drive and shares it with the setting "Anyone with the link". Each Python lab notebook starts with a cell headed "Run this cell first". '
            'The notebook downloads data.zip from the tutor\'s link and unpacks it. This is what to do:', after=2)
    numbered(d, ['Open the notebook and look at the first code cell. Near the top is a line that starts DATA_LINK = followed by quotation marks.',
                 'If a link is already between the quotation marks, you have nothing to paste. Run the cell.',
                 'If the quotation marks are empty and your tutor gives you a link, paste the link between them, then run the cell. Do not unzip anything.',
                 'If your tutor gives you the file itself instead of a link, leave DATA_LINK empty and run the cell. It prints "Choose the file data.zip from your computer" and shows a Choose files button. Click it and pick data.zip. If your browser renamed the file to data (1).zip, pick that one. It still works.',
                 'Wait a few seconds. The cell prints "Data files ready:" with a list of the csv and db files.',
                 'Open the folder icon on the left of Colab to see the files. They sit in the temporary space of your Colab session. Your Drive does not hold them.'])
    body(d, 'If the download fails, check that you pasted the whole link and that you are signed in to the internet. Ask your tutor to confirm that the link is shared with "Anyone with the link". '
            'Because the files live in the session, the cell runs again each time you start a new session, open a new notebook, or Colab disconnects. The next page says what to do then.', before=2)
    h2(d, '4. The Lakeside workbook in Google Sheets or Excel')
    body(d, 'Sessions 1 to 4 are spreadsheet work. Your tutor will give you lakeside_for_sheets.xlsx (it is also inside data.zip). To use it in Google Sheets, upload it to Google Drive, open it, and choose File, then Save as Google Sheets. '
            'To use Excel or LibreOffice Calc, open the file directly. Look at the tabs along the bottom. In Session 2 you describe each one. The task lists are in the Sheets Lab Sheets document you receive in Session 1.')
    h2(d, '5. A free GitHub account')
    body(d, 'GitHub is a website that keeps a copy of your project online. You need an account in Session 23, and it is easier to make it now. Go to github.com, choose Sign up, and use your email address. '
            'Pick a username you would be happy to show an employer, because your course project will sit under it. A public repository can be read by anyone, so never upload personal data, passwords or anything your employer has not cleared. '
            'GitHub offers free accounts at the time of writing. Check the current terms if you want a private repository.')
    h2(d, '6. Streamlit Community Cloud (optional, after Session 23)')
    body(d, 'In Session 23 you write a small app. Streamlit Community Cloud can put it on the internet from your GitHub repository. You sign in with your GitHub account at share.streamlit.io. '
            'At the time of writing it is free for public apps, and an app that nobody visits for a while goes to sleep (reports say about 12 hours). That suits learning and demonstrations. It is not a place for a service a business depends on. Check the current limits and terms before you rely on it. '
            'Publishing is not part of the 45-minute lab. You do it afterwards.')
    h2(d, 'Other tools you will meet')
    bullets(d, ['TensorFlow Playground (Session 20): a web page, no account.',
                'sentence-transformers (Sessions 21 and 22): the notebook downloads a small model inside Colab once (about 90 MB at the time of writing). It needs a stable connection that day.',
                'A free chat assistant (optional): it can explain an error or suggest code, and you check what it says. Never paste personal or confidential data into one.'])
    h2(d, 'When Colab disconnects')
    body(d, 'It happens to everyone. Free Colab sessions end after you leave them idle for a while, after a long time connected, when the browser tab is closed, or when the laptop sleeps. '
            'Google does not publish fixed limits for the free service. At the time of writing, community reports give an idle disconnect of roughly 90 minutes and a longest session of roughly 12 hours, and both can change. Check the Colab FAQ for the current position.', after=3)
    grid(d, [['Lost when it disconnects', 'The values held in memory (your variables and tables) and the files in the Colab Files panel, including data.zip contents and any csv you wrote.'],
             ['Kept', 'The notebook itself, if you saved a copy in Drive. Anything you downloaded to your laptop.']], [4.4, 13.0], size=9, label_cols=(0,))
    spacer(d, 4)
    numbered(d, ['Do not panic and do not retype. Choose Connect, or reload the page.',
                 'Run the data cell again. It downloads data.zip from the tutor\'s link, or asks you to choose the file.',
                 'Choose Runtime, then Run all (or Restart session and run all). Cells run from the top and rebuild your variables.',
                 'If a cell shows NameError, such as name df is not defined, a cell above it has not run in this session. Run the cells from the top.',
                 'Before you leave a lab, download the files you made (for example orders_clean.csv) and choose File, then Save a copy in Drive. Do this when the lab ends, not later.'])
    h2(d, 'If something goes wrong')
    grid(d, [['Colab will not open', 'Try another browser (Chrome or Edge), and turn off any extension that blocks pages.'],
             ['A cell shows red text', 'Read the last line first. It says what went wrong. We practise this in Session 5.'],
             ['The data cell finishes but later cells cannot find orders.csv', 'Run the first cell again. If it asks for a file, choose data.zip. An unzipped folder does not work.'],
             ['ModuleNotFoundError', 'The library is not installed in this session. Run pip install and the library name in a cell, then run the cell again. Ask your tutor if it still fails.'],
             ['The page is stuck on Connecting', 'Check your internet connection, then reload. Free capacity can run short at busy times. Try again in a few minutes.']], [5.6, 11.8], header=['What you see', 'What to do'], size=9, label_cols=(0,))
    h2(d, 'Data and privacy')
    body(d, 'Use only the fictional course data. Never put real customer, patient or staff data into a notebook, a chat assistant or an app you share.')
    h2(d, 'What to bring')
    body(d, 'A laptop with a browser and a charger. A notebook and pen. A question from your own work that you would like data to answer: you will use it in Session 1.')
    h2(d, 'Your other documents')
    body(d, 'Your tutor gives you these in Session 1: the Sheets Lab Sheets (the task lists for Sessions 1 to 4 and the presentation preparation in Session 24), the Glossary (every term the course teaches, with the spreadsheet idea it matches), '
            'and the Course Projects Guide (the projects you build, how to present your course project, the project checklist for feedback, and what the certificate of completion means).')
    return d


# ====================================================================================== COURSE PROJECTS GUIDE
def projects():
    d = new('Course Projects Guide')
    title(d, 'Course Projects Guide', f'{COURSE}  |  What you build, keep and present  |  Updated {UPDATED}')
    box(d, 'How this course works', ['There are no exams, marks, grades, pass marks or weights in this course. You build practical projects and you keep them.',
                                     'The check cells (OK or NOT YET), the recall questions and the exit-check questions are self-checks for you. Nobody marks them.',
                                     'You finish the course by finishing your course project. Then you receive a certificate of completion from KLAi Professional Learning.'])
    h2(d, '1. What you build across the course', 6)
    body(d, 'Every lab ends with something you keep. Together they are your portfolio of practical work.', after=3)
    for letter, name, a, b in MODULES:
        h2(d, f'Module {letter}: {name}  (Sessions {a} to {b})', 4, 2)
        grid(d, [[str(n), S(n)['title'], DELIVERABLE[n]] for n in range(a, b + 1)], [0.9, 7.6, 8.9], header=['#', 'Session', 'What you keep from the lab'], size=8.5, label_cols=(0,))
    h2(d, '2. Three project milestones')
    body(d, 'A project milestone is a practical piece of work that you produce in a session and show to your tutor. The tutor reviews it with you and gives feedback: what works and what to improve. '
            'A milestone is never scored. It is a step toward your course project.', after=3)
    t1 = slide_table(8, 'Project milestone 1')
    h2(d, 'Project milestone 1, Session 8: clean a raw file and reconcile it', 4, 2)
    body(d, 'A raw order export is cleaned one defect at a time. You produce four things.', after=2)
    grid(d, t1['rows'], [5.4, 12.0], header=t1['headers'], size=9, label_cols=(0,))
    spacer(d, 3)
    body(d, 'A reconciliation difference you can explain is worth more than one you have hidden. The explanation in your note is in your own words.', 9.5)
    t2 = slide_table(13, 'Your Project milestone 2 keepsake')
    h2(d, 'Project milestone 2, Session 13: a one-page analysis report', 4, 2)
    body(d, 'One page. A manager who has never seen the data should understand it. You also write your project question in this session (section 3).', after=2)
    grid(d, [[r[0], r[1]] for r in t2['rows']], [3.0, 14.4], header=['Section', 'What you write'], size=9, label_cols=(0,))
    h2(d, 'Project milestone 3, Session 19: a tested model', 8, 2)
    body(d, 'You forecast clinic cases by district and month, and keep your notebook and the results file it writes. It shows:', after=2)
    bullets(d, ['a baseline (a seasonal naive forecast) and a model scored on months it never saw, split by date at 2025;',
                'the error in the units of the business (cases), reported with MAE, RMSE and MAPE;',
                'a scikit-learn Pipeline that packs the modelling job into one object;',
                'three sentences for a district manager: whether the model beats the baseline, by how much, and what could mislead.'], 9.5)
    body(d, 'The same three moves apply to your course project: a baseline, a score on records the model never saw, and an error in business units. Check for data leakage.', 9.5, before=2)
    h2(d, '3. The course project')
    body(d, 'You choose a question and a dataset and carry them through the second half of the course. A good question names the target, the predictors, the data and the decision. Session 13 gives examples.', after=3)
    grid(d, [['13', 'Write and scope the question (Project milestone 2)'], ['14', 'Choose the dataset'], ['19', 'Baseline and tested model (Project milestone 3)'],
             ['23', 'Learn to publish the app and model card; apply it to your course project before Session 24'], ['24', 'Present for ten minutes']],
         [2.4, 15.0], header=['Session', 'Course project step'], size=9, label_cols=(0,))
    h2(d, 'Dataset options', 8, 2)
    bullets(d, ['Lakeside Mart: orders, order lines, branches, customers and weekly branch figures (a fictional retailer).',
                'Nile Microfinance loans: 8,000 loans, and whether each defaulted (fictional).',
                'District Clinics: monthly clinic visits by district (fictional).',
                'Customer feedback messages: 800 short messages (fictional).',
                'Your own question about one of the tables above. If you want to use data from your workplace, ask your employer in writing, remove names and phone numbers first, and never put it in a public repository.'], 9.5)
    h2(d, 'What your course project contains', 8, 2)
    numbered(d, ['A one-sentence question and the decision it serves.',
                 'The data cleaned, with a data cleaning log.',
                 'One analysis that answers part of the question.',
                 'One model with a baseline model and a metric chosen for the cost of a mistake, scored on records it has not seen.',
                 'The limits: what the data cannot show, who could be harmed by an error, and which groups you compared.',
                 'A small app (Session 23) with a model card and a data protection checklist.',
                 'A ten-minute presentation (Session 24).'], 9.5)
    h2(d, '4. How to prepare and present it')
    parts = slide_table(24, 'A ten-minute talk')['visual']['parts']
    body(d, 'Five slides in ten minutes: ' + ', '.join(f'{p[0].lower()} ({p[1]} min)' for p in parts) + '. Evidence gets the most time.', after=3)
    bullets(d, ['Tell the result as a story in three parts: the answer, the evidence beside a baseline model, and the limits.',
                'Write an executive summary of four sentences: the answer, the evidence, the main limit and the decision you ask for. It becomes your opening.',
                'Say the limits before the result. People trust a speaker who names them first.',
                'Use the real term once, then say what it means for a decision. Recall, for example, is how many of every 100 defaults you flag.',
                'Rehearse aloud with a timer. Most people run long.',
                'Prepare three answers: one on method, one on the metric and one on risk. An answer that says a check is not finished is a good answer.'], 9.5)
    body(d, 'Session 24 is a planning and rehearsal lab in a Google Sheet. If you have no project of your own, you present the Nile Microfinance loan story from the slides.', 9.5, before=2)
    h2(d, '5. The project checklist: feedback for yourself and for a partner')
    rb = slide_table(24, 'What a finished project contains')
    body(d, 'Some people call a list like this a rubric. Here it is a checklist of four qualities that a finished project has. Use it on your own project before you present. '
            'In the Session 24 lab your partner uses the same four rows to give you feedback: Yes or Not yet for each row, and one comment that points to a named slide. Nothing is scored and nothing is weighted.', after=3)
    grid(d, rb['rows'], [3.3, 7.4, 6.7], header=rb['headers'], size=9, label_cols=(0,))
    spacer(d, 3)
    body(d, 'When you receive feedback, write it down and do not defend yourself. Ask a question if you need to understand it.', 9.5)
    h2(d, '6. What the check cells mean')
    body(d, 'Every Python notebook has check cells. After each answer you run a line such as check("label", value, expected). It prints OK or NOT YET, and the last cell, show_checks(), prints "All N checks pass" or "k of N checks pass". They are self-checks. Nobody marks them.', after=3)
    grid(d, [['What OK means', 'Your value is within a small tolerance of the expected value (0.01 unless the lab says otherwise). Your cell ran and produced that number.'],
             ['What NOT YET means', 'Your value is outside the tolerance, or the cell has not been filled in, or it raised an error. It means look again.'],
             ['What a check cannot tell you', 'That you understand the method or that your reasoning is right. A correct number can come from a wrong method, and a wrong number can come from a harmless rounding or a setup problem.'],
             ['Only the checks you ran count', '"All 7 checks pass" means the 7 checks you ran passed. A check you skipped is not counted. Run the cells in order and look at the total.'],
             ['Libraries differ a little', 'Models from scikit-learn can differ from the slides by a few records or a unit in the second decimal. The checks use a tolerance for this. Random exercises (Session 4) use ranges.'],
             ['A learner notebook starts with NOT YET', 'That is expected. The answer cells hold answer = None until you fill them in. The solution notebook ends with "All N checks pass".'],
             ['Sheets sessions', 'Sessions 1 to 4 and 24 have a "Check your numbers" table on the slides. You compare your sheet with it by eye. There are no check cells.']],
         [4.4, 13.0], size=9, label_cols=(0,))
    h2(d, '7. The certificate of completion')
    body(d, 'You receive a certificate of completion from KLAi Professional Learning when you complete your course project. There are no criteria beyond that: no marks, no pass mark and no weights. '
            'It says that you finished the course and your project. It is not an external credential or a university accreditation.', after=3)
    h2(d, '8. Working rules')
    bullets(d, ['Use the course data. It is fictional and generated.',
                'A free chat assistant may explain an error or suggest code. Keep a short audit log: what you asked, what it gave, how you checked it, and whether you kept it. You must be able to explain every line in your project.',
                'List what you did not check. A stated limit builds trust. A hidden one costs it.',
                'Your published work is public. Check it for personal data, passwords and keys before you push it to GitHub.',
                'Never paste real customer or patient data into a notebook, an assistant or an app you share.'])
    return d


# ====================================================================================== BENCHMARK AND DESIGN REPORT
def counts():
    n_slides, words = 0, 0
    for n in range(1, 25):
        sp = deck.build_spec(S(n))
        n_slides += len(sp['slides'])
        for sl in sp['slides']:
            nt = sl.get('notes')
            if isinstance(nt, list):
                nt = ' '.join(nt)
            words += len((nt or '').split())
    n_nb = len(list((BUILD / 'content' / 'labs').glob('s[0-9][0-9]_nb.py')))
    return n_slides, words, n_nb


def benchmark():
    n_slides, words, n_nb = counts()
    hours = words / 130 / 60
    d = new('Benchmark and Design Report', COURSE)
    title(d, 'Benchmark and design report', COURSE)
    body(d, 'First prepared 28 October 2026 for Jotham Martin Wambi, KLAi Professional Learning. Design sections rewritten on 4 November 2026 for the KLAi edition. '
            'A 48-hour course for working professionals who know Excel and have never coded. Every external fact in this report was gathered on 28 October 2026 and may have changed since. Re-check before you quote it.', 10, after=6)
    h2(d, '1. The verdict', 0)
    body(d, 'A good fit for working professionals who start from Excel. It is far shorter than a 150-hour certificate. The course teaches one path from data to a deployed app (data, Python, SQL, inference, regression, machine learning, text and language models, responsible use) in 48 live hours, '
            'with free tools only, an Excel starting point and Ugandan data. As at 28 October 2026 it is shorter and shallower than the Google and IBM certificates, and Session 24 lists what it leaves out. '
            'Those programmes offer more depth, more mathematics, more tools and a recognised credential. This course offers live teaching, no cost, a start for non-technical learners, local context, and newer topics such as embeddings, retrieval, small local language models and data protection law.')
    h2(d, 'What was compared')
    body(d, 'The course was set against the AI and Data Scientist roadmap on roadmap.sh and against the programmes most employers and learners already know: the IBM Data Science Professional Certificate, the Google Data Analytics and Advanced Data Analytics certificates, '
            'the DeepLearning.AI Machine Learning Specialization and AI for Everyone, Google\'s Machine Learning Crash Course, Kaggle Learn, fast.ai, Harvard\'s CS50P and the University of Helsinki\'s Elements of AI. '
            'Facts come from public pages found by web search on 28 October 2026 and checked again on 29 October 2026. Where sources disagree on hours, course counts or prices, the table gives the range and says so. '
            'The roadmap.sh page itself could not be fetched from the build environment, so its stages were taken from the roadmap PDF and curricula that follow it. Re-check the live page before quoting it.')
    h2(d, '2. The comparators (as at 28 October 2026)')
    comp = [
        ['IBM Data Science Professional Certificate (Coursera)', 'About 178 hours, 12 courses; roughly 4 months at 10 hours a week (Coursera)', 'USD 49 to 59 a month, depending on source and date', 'Methodology, Python, SQL, Jupyter, GitHub, RStudio, pandas, NumPy, scikit-learn, matplotlib, browser labs; a generative AI course and career guide added', 'Self-paced, no live tutor, paid. One reviewer notes classical data science only, no retrieval or agents. Much deeper and longer.'],
        ['Google Data Analytics Professional Certificate', 'Nine courses, over 180 hours (Coursera); older reviews describe eight courses and R; under 6 months at under 10 hours a week', 'About USD 49 a month (reported)', 'Spreadsheets, SQL, Tableau, Python (the Python course is 27 hours), and a last course on job searching with AI', 'Analytics only; no modelling. Paid. Tableau is outside our free set.'],
        ['Google Advanced Data Analytics Certificate', 'Seven courses; Coursera says about 6 months at 10 hours a week, third parties say about 200 hours', 'Coursera subscription (about USD 49 a month reported)', 'Python, statistics, regression, supervised machine learning, Tableau; no deep learning listed', 'Needs analytics background first. Paid. No text or language models.'],
        ['DeepLearning.AI Machine Learning Specialization', 'Three courses, about 95 hours (DeepLearning.AI)', 'Coursera subscription', 'Supervised learning, neural networks, trees, unsupervised learning, recommenders, reinforcement learning, in NumPy, scikit-learn and TensorFlow', 'Assumes programming comfort. Deeper theory.'],
        ['AI for Everyone (DeepLearning.AI)', 'About 7 hours', 'Coursera', 'What AI is, how to run AI projects, AI in a company, society. No code.', 'No hands-on data work.'],
        ['Google Machine Learning Crash Course', 'About 15 hours by Google\'s estimate; learners report 10 to 30', 'Free', 'Regression, classification, data, neural networks, embeddings, large language models, production and fairness; exercises in Colab', 'Assumes Python, pandas and NumPy. No live teaching.'],
        ['Kaggle Learn micro-courses', 'About 3 to 5 hours each (Python 5, Pandas 4, Intro to Machine Learning 3, Intro to SQL 3)', 'Free, free certificates', 'Hands-on notebooks', 'Short and disconnected; best as free follow-up.'],
        ['fast.ai Practical Deep Learning for Coders', 'Part 1 lists 9 lessons of about 90 minutes (the announcement post lists 8)', 'Free', 'Image, text, tabular deep learning and deployment', 'Needs a year of coding. Deep learning only.'],
        ['Harvard CS50P', '9 or 10 weeks (sources differ) at 3 to 9 hours a week', 'Free to take; free certificate through Harvard OpenCourseWare, or a paid edX certificate', 'Python programming', 'Python only; no data science.'],
        ['Elements of AI (University of Helsinki)', 'University of Helsinki says about 30 hours; other sources say 10 to 50', 'Free', 'What AI is and is not, no maths or code', 'No hands-on skills.'],
    ]
    grid(d, comp, [3.0, 3.6, 2.5, 4.4, 3.9], header=['Programme', 'Length', 'Cost', 'What it teaches', 'Gap against this course'], size=8, label_cols=(0,), hdr_size=8.5)
    h2(d, '3. Coverage against the roadmap.sh stages')
    body(d, 'The stage list below is the one in the roadmap.sh AI and Data Scientist PDF and the curricula built on it (as at 28 October 2026). The right-hand column says how deeply this course goes. "Light" means the course keeps it short for non-technical learners. The Module column says where the stage sits in the course.', after=3)
    cov = [['Mathematics', 'Intuition only: slope, area, vectors, matrices as tables. No proofs, no hand calculation.', '4, 13, 20', 'A, C, E', 'light'],
           ['Statistics', 'Distributions, sampling, confidence intervals, hypothesis tests, A/B tests, correlation.', '3, 4, 12', 'A, C', 'core'],
           ['Econometrics', 'Linear and logistic regression, time series and forecasting basics.', '13, 15, 19', 'C, D', 'core'],
           ['Coding', 'Python, pandas, SQL. Data structures and interview algorithms are left out on purpose.', '5, 6, 7, 8, 9, 10', 'B, C', 'core'],
           ['Exploratory data analysis', 'Cleaning, charts, summary, communication.', '2, 3, 8, 11', 'A, B, C', 'core'],
           ['Machine learning', 'Supervised, unsupervised, ensembles, evaluation, leakage.', '14, 15, 16, 17, 18', 'D', 'core'],
           ['Deep learning', 'Neural networks, one pretrained model. No training from scratch on images.', '20', 'E', 'light'],
           ['MLOps', 'Save a model, version code, deploy an app, watch for drift. No Docker or cloud.', '23', 'F', 'light'],
           ['AI engineering', 'Text vectors, search, a retrieval pattern with a small local model.', '21, 22', 'E', 'core'],
           ['AI-assisted coding', 'An assistant is used and its code is checked in Sessions 5, 6 and 22. It is never required.', '5, 6, 22', 'B, E', 'core']]
    grid(d, cov, [3.0, 7.4, 2.9, 2.1, 2.0], header=['Roadmap stage', 'What this course does', 'Sessions', 'Module', 'Depth'], size=8.5, label_cols=(0,))
    spacer(d, 4)
    body(d, 'Left out on purpose: proofs and hand calculation in linear algebra and calculus, data structures and interview algorithms, big-data engines, cloud platforms, containers and training deep networks from scratch. Session 24 lists each gap with a free next step.', 9.5)
    h2(d, 'How the 24 sessions map to the six modules')
    mods = [['A  Think with data', '1 to 4', 'Spreadsheets, no code', 'Framing a question, records and keys, summaries and charts, samples, uncertainty and cause'],
            ['B  Python for data', '5 to 9', 'Colab, pandas', 'Variables and functions, loading, cleaning with a log, grouping and joining'],
            ['C  Analyse and explain', '10 to 13', 'SQLite, matplotlib, statsmodels', 'SQL, exploratory data analysis, inference, regression'],
            ['D  Machine learning', '14 to 19', 'scikit-learn', 'The workflow, classification, judging a model, forests and boosting, clustering, forecasting and a Pipeline'],
            ['E  Neural networks and text', '20 to 22', 'TensorFlow Playground, sentence-transformers', 'Neural networks, text as numbers, language models, retrieval and evaluation'],
            ['F  Ship it and present', '23 to 24', 'GitHub, Streamlit', 'Reproducibility, an app, a model card, fairness and data protection, the course project talk']]
    grid(d, mods, [4.0, 1.9, 4.3, 7.2], header=['Module', 'Sessions', 'Main tools', 'Roadmap content'], size=8.5, label_cols=(0,))
    h2(d, '4. Where the course is competitive')
    bullets(d, [('Live teaching with a script.', f'Every programme above is self-paced. This course puts a tutor in the room, with {n_slides} slides in 24 decks and read-aloud notes for every slide (about {hours:.0f} hours of spoken script, counted at 130 words a minute), so the tutor does not have to improvise.'),
                ('Concepts first, then the lab.', 'Each session spends 45 minutes on picture, plain words and one example by hand with laptops closed, then 45 minutes in the notebook or sheet. Learners meet an idea before they have to code it.'),
                ('A start for people who are not technical.', 'The design assumes beginners drop out because of overload (code, mathematics and tools at once), fear of mathematics, and getting stuck early. This is a design assumption and no source for it was checked. '
                 'Excel is the anchor (Sessions 1 to 4 have no code), statistics is learned through simulation and pictures, every session begins with recall and ends with a check, and a first error is read and fixed in Session 5.'),
                ('Real industry terms.', 'Learners are taught the words they will meet in documentation, interviews and later courses, each with a plain explanation (section 8).'),
                ('No cost for the learner or the tutor.', 'Every tool is free, and several common choices were avoided for cost or compatibility reasons (see section 6). No lab needs a paid account, a key or a GPU.'),
                ('Modern topics most certificates add late or leave out.', 'Text as numbers, embeddings, retrieval over a company\'s own documents and a test sheet for a small language model run inside Colab (Sessions 21 and 22). '
                 'As at 28 October 2026 the Google Advanced Data Analytics outline lists no deep learning, and the IBM certificate added generative AI as a later course.'),
                ('Local data and local law.', 'The practicals use fictional Uganda businesses (a supermarket chain, a microfinance lender, district clinics) in shillings, and Session 23 teaches the principles and rights in the Data Protection and Privacy Act, 2019 as a teaching summary that is not legal advice.'),
                ('Checks built into every session.', 'Every number in the practicals comes from generated data with an answer key. The sessions teach the habits that catch wrong numbers: records and granularity, join fan-out, data leakage, residuals, and the row count beside every figure.')], 9.5)
    h2(d, '5. Where it is not competitive')
    bullets(d, [('Depth and hours.', '48 hours against roughly 150 to 240 for the certificates (as at 28 October 2026). A graduate can do junior analyst work and can build and test a first model. A finished data scientist needs more.'),
                ('Credential.', 'The course gives a certificate of completion from KLAi Professional Learning (the wording is to be confirmed by KLAi). No external credential or university accreditation is arranged. A certificate from a university partner would need to be arranged separately. The course project and a public GitHub portfolio are the proof of skill.'),
                ('Mathematics.', 'Intuition and simulation only. Learners who want machine learning research or engineering roles need linear algebra, calculus and probability next.'),
                ('Engineering practice.', 'Version control, one deployed app and a model card, but no containers, testing frameworks, pipelines or monitoring tools.'),
                ('Free-tool limits.', 'Google does not publish Colab\'s free limits. Reports give an idle disconnect of about 90 minutes and a longest session of about 12 hours. Streamlit Community Cloud apps sleep after about 12 hours without visitors. Both suit learning, and neither suits a business-critical service.')], 9.5)
    h2(d, '6. Tools and licences (as at 28 October 2026)')
    body(d, 'Status "confirmed" means the free-use terms were read from public sources on 28 October 2026. Status "check" means confirm on the day before class.', after=3)
    tools = [['Google Colab', 'Run Python notebooks in the browser. Nothing to install.', 'Free tier. Needs a free Google account. GPU not needed for this course. Google does not publish its limits; reports give an idle disconnect of about 90 minutes and a longest session of about 12 hours. Save to Drive or GitHub.', 'confirmed'],
             ['Google Sheets (or Excel, or LibreOffice Calc)', 'Sessions 1 to 4 and every Excel comparison.', 'Free. Any spreadsheet works. Excel is used if students already own it.', 'confirmed'],
             ['Python 3 with pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib, seaborn', 'The data science stack.', 'Free, open source (BSD or PSF licences). All preinstalled in Colab.', 'confirmed'],
             ['SQLite (inside Python)', 'SQL practice with no server.', 'Free, public domain. Included in Python. DB Browser for SQLite is optional.', 'confirmed'],
             ['Git and GitHub Free', 'Save work, share a portfolio, deploy the app.', 'Free account. Public repositories for the course.', 'confirmed'],
             ['Streamlit and Streamlit Community Cloud', 'Turn a model into a small web app.', 'Free for public apps. Apps sleep after about 12 hours without visitors.', 'confirmed'],
             ['TensorFlow Playground', 'See a neural network learn, in the browser.', 'Free, Apache licence, no login. Web page only.', 'confirmed'],
             ['sentence-transformers (all-MiniLM-L6-v2)', 'Turn text into vectors for search and similarity.', 'Free. Apache 2.0. Downloads about 90 MB once in Colab. No API key, no hosted service.', 'confirmed'],
             ['A small open language model run inside Colab (for example Qwen2.5-0.5B-Instruct)', 'Show how a language model answers, with nothing sent to a vendor.', 'Free. Confirm the licence on the model card before class. Optional; the session still works with embeddings alone.', 'check'],
             ['Any free chat assistant the student already has', 'Explain errors, suggest code, critique drafts.', 'Free tiers; limits change. Never required. Every lab runs without one.', 'check'],
             ['Visual Studio Code (optional local setup)', 'Local editing once students outgrow Colab.', 'Free to use. Optional only.', 'confirmed']]
    grid(d, tools, [4.2, 4.0, 7.4, 1.8], header=['Tool', 'Use', 'Cost and terms', 'Status'], size=8, label_cols=(0,), hdr_size=8.5)
    h2(d, 'Avoided, and why', 8, 2)
    bullets(d, [('Anaconda Distribution and Miniconda.', 'Free for individuals, but organisations with 200 or more staff need a paid licence under the 2024 terms, which includes government and non-profits. Miniconda\'s installer is free, but its default package channel falls under the same terms. Use Colab, or python.org with venv, or Miniforge.'),
                ('Hugging Face hosted inference.', 'Several sources report that free accounts stopped receiving included monthly inference credits on 7 October 2026. The date rests on a forum thread and a GitHub issue. No official notice was found, and some roundups still list the credits. Models are downloaded and run inside Colab instead, so nothing is sent to a vendor and no key is needed. Check the current terms and the model card licence before teaching Session 22.'),
                ('Power BI Desktop.', 'Windows only, which fails on mixed laptops. Charts are made in Python and Sheets, and the course shows how to hand a file to Power BI or Excel.'),
                ('Docker Desktop and paid cloud GPUs.', 'Not needed. Deployment uses Streamlit Community Cloud.'),
                ('Paid AI APIs.', 'Any lab needing a paid key would break the no-cost rule.')], 9.5)
    h2(d, '7. Market and local relevance (as at 28 October 2026)')
    bullets(d, ['The World Economic Forum Future of Jobs Report 2025 ranks AI and big data as the fastest-growing skills, and analytical thinking as the most sought-after core skill (about seven in ten employers).',
                'The Stack Overflow Developer Survey 2025 reports Python used extensively by 57.9 percent of all respondents (51 percent a year earlier). That is fourth, behind JavaScript, HTML and CSS, and SQL. Among respondents who are learning to code, Python comes first (secondary sources give about 69 to 72 percent). The 2024 Python Developers Survey by JetBrains and the Python Software Foundation puts pandas at 80 percent of the respondents who do data exploration and processing.',
                'For Uganda, third-party career guides describe a shortage of applied AI skills among computer science graduates, and universities (for example Makerere) are building AI and data science capacity. These guides are secondary sources that were not checked. Treat their pay figures as unverified.'], 9.5)
    h2(d, '8. Design: the KLAi look, concepts then lab, and the terminology rule')
    h2(d, 'The KLAi look', 4, 2)
    body(d, 'Decided 4 November 2026. All decks, figures, the roadmap and the Word documents use the KLAi brand: black, white, red and gold, the Lato typeface and the KLAi logo. It replaces the first look of October 2026 (clay accent, charcoal text, Cambria headings). '
            'The rules: hairline rules and type, almost no tinted fill, one idea per slide, and titles that state the finding. Red marks what needs attention, such as an error or a project milestone. Gold marks the thing to look at, used as a fill or on black and never as text on white, because its contrast on white is weak. '
            'There are no kicker labels above titles, numbered step cards, accent stripes or repeated tile rows. Every concept slide carries a drawn figure. Word documents share one header band with the logo and a gold rule, with hairline tables. '
            'Decks are shared as PDFs and learners revise from them without the tutor, so slides use full sentences, define every term where it first appears, give units, and say what each picture shows.')
    h2(d, 'Concepts first, then the lab', 8, 2)
    body(d, 'Every session has the same clock: 10 minutes of recall and the question of the day, 45 minutes of concepts, a 10-minute break, 45 minutes of lab, and 10 minutes for the exit check, what you keep and what comes next. '
            'The concepts half has no laptops open. It uses diagrams, plain words, one example worked by hand, and code shown only as a recipe to read aloud. One slide in each session, "Where you will use this at work", gives East African examples with the real job tasks and real tool names. '
            'A divider slide titled "Part 2" marks the switch, and the tutor moves from the slides to the notebook or sheet once. In the lab each step follows the same rhythm: predict, run, read, change one thing. '
            'The lab ends with a deliverable the learner keeps (a cleaned file, a notebook, a one-page finding). Earlier decks mixed demonstration code and lab work inside the slides. That mix was moved apart.')
    h2(d, 'The terminology rule', 8, 2)
    body(d, 'Decided 4 November 2026. Every idea is named with the real industry term first, and a plain explanation follows beside it. Examples: record (also called an observation, an instance or a row), standard error, residual, confounder, decision threshold, data leakage. '
            'Where the course starts from a spreadsheet idea, the Excel word comes first and the industry term follows on the same slide. Friendly invented names such as "grain" for the meaning of a row (data warehouse people say granularity), "the wobble" for sampling variability or "the misses" for residuals stay out of the vocabulary. They may appear inside an explanation. '
            'The reason is practical: learners will meet the real words in documentation, job interviews, Kaggle and textbooks, and a learner who knows only an invented name has no anchor. The full list is in TERMS.md in the build folder. A list of the qualities of good work is called a rubric, and a project summary is an executive summary.')
    h2(d, 'How the 24 sessions map to the roadmap stages', 8, 2)
    body(d, 'The module table in section 3 gives the full mapping. In short: Modules A to C cover statistics, coding, SQL and exploratory data analysis. Module D covers econometrics and machine learning. '
            'Module E covers deep learning in light form and AI engineering. Module F covers MLOps in light form, responsible use and communication. The course project ties them together: a question in Session 13, a dataset in 14, a tested model in 19, an app and model card in 23, and a ten-minute talk in 24.')
    h2(d, '9. What was built')
    sheets_sessions = [1, 2, 3, 4, 24]
    built = [['Sessions', '24 sessions of 2 hours (48 hours), in six modules'],
             ['Slide decks', f'{n_slides} slides in 24 decks, counted from the build on {UPDATED}'],
             ['Read-aloud speaker notes', f'Every slide, about {hours:.0f} hours of script ({words:,} words at 130 words a minute)'],
             ['Vocabulary', 'Up to five new terms per session, each with an industry name and a plain meaning; the Glossary collects them'],
             ['Lab notebooks', f'{n_nb} coding labs (learner and solution versions), Sessions 1 and 5 to 23'],
             ['Task sheets', 'Sessions 1 to 4 (Google Sheets) and Session 24 (presentation preparation), with a tutor copy of the answers'],
             ['Handouts', 'Student Roadmap, Course Outline, Student Setup Guide, Sheets Lab Sheets, Glossary, Course Projects Guide'],
             ['Facilitator documents', 'Facilitator Guide, Presenter Script, Sheets Lab Answers, this report, Playback and Rehearsal Checklist'],
             ['Datasets', 'Lakeside Mart (retail), Nile Microfinance (loans), District Clinics, 800 feedback messages, 8 policy documents, a dirty export with 8 seeded defects']]
    grid(d, built, [4.2, 13.2], header=['Item', 'Quantity'], size=9, label_cols=(0,))
    h2(d, '10. What is verified, and what is not')
    body(d, 'The full list is in 05 Course Maintenance/Verification Record.txt. In short:', after=2)
    bullets(d, [('Verified here:', 'every deck builds and passes the content lint (required fields, 20 to 40 authored slides, spoken notes of 45 to 150 words per slide, no stage directions, house style); numbers on slides come from the generated data; the notebooks of Sessions 1, 5 to 11, 19, 21 and 22 ran on real pandas and NumPy in the build environment.'),
                ('Not verified here:', 'the other notebooks (Sessions 12 to 18, 20 and 23) need SciPy, statsmodels, scikit-learn, joblib or Streamlit that the build environment lacks, so only their cell flow was run against a stand-in or their code was checked to compile. Model outputs such as AUC and the forest and boosting scores are expectations until the notebooks run in Colab. '
                 'Nothing was rehearsed aloud, and PowerPoint playback was not tested. The external facts in sections 2, 6 and 7 are as at 28 October 2026 and need a re-check before they are quoted.')], 9.5)
    h2(d, '11. Decisions for you')
    bullets(d, [('Hosting the data.', 'Put data.zip somewhere students can reach (a public GitHub release, Google Drive link or WhatsApp). The setup cell accepts a link or an upload.'),
                ('The certificate.', 'The KLAi certificate of completion is given for completing the course project, with no other criteria (lecturer decision, 4 November 2026). Confirm the wording on the certificate itself.'),
                ('The course project dataset.', 'Four are offered (Lakeside, Nile loans, clinics, feedback). Add one drawn from students\' own workplaces if their employers permit and data protection allows.'),
                ('Account policy.', 'Every student needs a free Google account for Colab. Ask in Session 1 who has none and plan a local-install route (VS Code and Python) for them.'),
                ('Screenshots.', 'No tool screenshots are included because none could be captured here. Add them for the tools you demonstrate (Colab, GitHub, Streamlit Community Cloud).')], 9.5)
    h2(d, 'Sources (as at 28 October 2026)')
    src = ['IBM Data Science Professional Certificate, Coursera. https://www.coursera.org/professional-certificates/ibm-data-science',
           'Google Data Analytics Professional Certificate. https://www.coursera.org/professional-certificates/google-data-analytics',
           'Google Advanced Data Analytics Professional Certificate. https://www.coursera.org/professional-certificates/google-advanced-data-analytics',
           'DeepLearning.AI Machine Learning Specialization. https://www.deeplearning.ai/specializations/machine-learning',
           'AI for Everyone. https://www.deeplearning.ai/courses/ai-for-everyone',
           'Google Machine Learning Crash Course. https://developers.google.com/machine-learning/crash-course',
           'Kaggle Learn. https://www.kaggle.com/learn',
           'fast.ai Practical Deep Learning for Coders. https://course.fast.ai/',
           'Harvard CS50P. https://cs50.harvard.edu/python/',
           'roadmap.sh AI and Data Scientist (PDF). https://roadmap.sh/pdfs/roadmaps/ai-data-scientist.pdf',
           'WEF Future of Jobs Report 2025. https://reports.weforum.org/docs/WEF_Future_of_Jobs_Report_2025.pdf',
           'Uganda Data Protection and Privacy Act, 2019 (ULII). https://media.ulii.org/media/legislation/18002/source_file/b6ae5cce4290322a/2019-9.pdf',
           'Streamlit Community Cloud status and limits. https://docs.streamlit.io/deploy/streamlit-community-cloud/status',
           'TensorFlow Playground. https://playground.tensorflow.org/',
           'Anaconda terms of service for academia and research. https://www.anaconda.com/blog/update-on-anacondas-terms-of-service-for-academia-and-research',
           'Hugging Face inference providers pricing. https://huggingface.co/docs/inference-providers/pricing',
           'Stack Overflow Developer Survey 2025. https://survey.stackoverflow.co/2025/',
           'Python Developers Survey 2024 (JetBrains and the Python Software Foundation). https://lp.jetbrains.com/python-developers-survey-2024/',
           'Elements of AI. https://www.elementsofai.com/',
           'Google Colab FAQ. https://research.google.com/colaboratory/faq.html']
    for s_ in src:
        para(d, s_, 8, after=1)
    return d


DOCS = {
    'outline': (outline, '01 Course Overview', 'Course Outline'),
    'setup': (setup, '03 Learner Materials', 'Student Setup Guide'),
    'projects': (projects, '03 Learner Materials', 'Course Projects Guide'),
    'benchmark': (benchmark, '04 Facilitator Materials', 'Benchmark and Design Report'),
}

ASSESS = [r'\bcheckpoints?\b', r'\bmarking\b', r'\bmark scheme', r'\bhand(ed)? in\b', r'\bpasses when', r'\bscore your partner']
BAN = [r'honestly', r'genuinely', r'straightforward', r'dive into', r'\bunlock', r'\bjourney\b', r'embark', r'game-changer', r"in today's world", r'delve', r'leverage\b']
ANTI = [r',\s+not\s+(a|an|the|just|only|about|because|to|for|in|on|by|with|every|all|any)\b', r'\bnot\s+just\b', r'\bnot\s+only\b[^.]*\bbut\b', r'\binstead of\b[^.]*\bnot\b']


def style_check(path):
    """House style on the generated text: no em or en dash, no X-not-Y, no banned filler, no price."""
    import docx
    doc = docx.Document(str(path))
    texts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                texts.append(c.text)
    bad = []
    for t in texts:
        if '—' in t or '–' in t:
            bad.append(('dash', t[:80]))
        for pat in BAN + ANTI + ASSESS:
            if re.search(pat, t, re.I):
                bad.append((pat, t[:80]))
        if re.search(r'\bUGX\s*1[ ,]?000[ ,]?000|\b1,000,000\b|\bUSD\s*\d+\s*(per|a) course', t) and 'Outline' in path.name:
            bad.append(('price', t[:80]))
    return bad


def main(argv):
    which = [a for a in argv if a in DOCS] or list(DOCS)
    if 'all' in argv:
        which = list(DOCS)
    for key in which:
        fn, folder, name = DOCS[key]
        d = fn()
        path = ROOT / folder / f'{name}.docx'
        save(d, path)
        to_pdf(path)
        bad = style_check(path)
        print(name, 'style problems:', len(bad))
        for b in bad[:12]:
            print('   ', b)


if __name__ == '__main__':
    main(sys.argv[1:])
