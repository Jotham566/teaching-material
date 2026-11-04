"""Session 1: What data science is and how to think in it (roles, the CRISP-DM lifecycle, AI against ML against deep learning, the free toolset, a first Colab cell).
Lab: a Google Sheets part (sheet_tasks) and a short notebook (content/labs/s01_nb.py).

Every number on a slide, in a note or in sheet_tasks is computed in facts() with pandas from the real course data. Nothing is typed from memory.
"""
import contextlib
import io
from functools import lru_cache

import pandas as pd

import b_facts as BF
from b_facts import n

CODE = ["message = 'Hello from Lakeside Mart analytics'", 'print(message)', 'total = 4500 + 2800', 'print(total)']


@lru_cache(maxsize=None)
def facts():
    B = BF.base()
    T = B['T']
    F = dict(B=B)
    F['tabs'] = B['tabs']
    F['rows'] = {t: len(T[t]) for t in BF.TABS}
    F['vars'] = {t: T[t].shape[1] for t in BF.TABS}
    o, ol = T['orders'], T['order_lines']
    F['blank'] = int(o.customer_id.isna().sum())
    F['blank_pct'] = F['blank'] / len(o) * 100
    F['lpo'] = len(ol) / len(o)
    F['mm'] = B['pay']['Mobile money']
    F['mm_share'] = F['mm'] / len(o)
    # the rule a person wrote: revenue = quantity x unit price x (1 - discount) holds on every order line
    calc = ol.quantity * ol.unit_price_ugx * (1 - ol.discount)
    F['formula_ok'] = bool((abs(calc - ol.line_revenue_ugx) <= 1).all())
    loans = pd.read_csv(BF.DATA / 'loans.csv')
    F['loans_n'], F['loans_default'] = len(loans), int(loans.default.sum())
    cl = pd.read_csv(BF.DATA / 'clinic_visits.csv')
    F['clinic_rows'], F['clinic_blank'] = len(cl), int(cl.total_visits.isna().sum())
    # run the first cell for real
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec('\n'.join(CODE), {})
    F['cell_output'] = buf.getvalue().strip().split('\n')
    F['price_sum'] = 4500 + 2800
    br = B['by_branch']
    F['jinja_mean'] = float(br.loc['B04', 'mean'])
    _j = o[o.branch_id == 'B04'].order_value_ugx
    F['jinja_wo'] = float(_j.drop(_j.idxmax()).mean())
    F['jinja_delta'] = F['jinja_mean'] - F['jinja_wo']
    F['jinja_median'] = float(_j.median())
    F['branch_mean_rank'] = br['mean'].sort_values(ascending=False).index.tolist()
    return F


def br2_second(F):
    return float(F['B']['by_branch']['mean'].sort_values(ascending=False).iloc[1])


def br_max_median(F):
    return float(F['B']['by_branch']['median'].max())


def build():
    F = facts()
    B = F['B']
    R, V = F['rows'], F['vars']
    blank = F['blank']
    assert F['formula_ok'] and F['cell_output'] == ['Hello from Lakeside Mart analytics', str(F['price_sum'])]
    assert round(F['jinja_delta'], -2) == 7300 and F['jinja_wo'] > br2_second(F) and F['jinja_median'] == br_max_median(F)
    assert B['max_order_branch'] == 'B04' and B['branch_names']['B04'] == 'Jinja' and F['branch_mean_rank'][0] == 'B04'
    assert len(F['tabs']) == 7 and F['tabs'][-1] == 'READ ME' and B['full_n'] == 30229
    sess = dict(
        num=1, block='Module A: Think with data', short_title='What data science is',
        title='What data science is and how to think in it',
        question='What does a data scientist do, and what will you be able to do after 24 sessions?',
        outcomes=['Name the four roles on a data team, and the six phases of the CRISP-DM lifecycle from business question to deployment',
                  'Tell artificial intelligence, machine learning, deep learning and data science apart by what each one produces',
                  'Count the records and variables of a table in Google Sheets, then open Google Colab and run your first cell'],
        outcome_icons=['people', 'robot', 'laptop'],
        outcome_note=('Here is what you can do by the end of today. You can name the four roles on a data team and the six phases of the CRISP-DM lifecycle, which is the industry reference for how a data project runs. '
                      'You can tell artificial intelligence, machine learning, deep learning and data science apart by what each one produces. '
                      'And you can count the records and variables of a table in Google Sheets and run your first cell in Google Colab. Today is the lightest session of the course, so enjoy it.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: Sheets first, then your first Colab cell'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Sheets and Colab lab',
        plan_caption='Ideas with pictures first. Then the sheet and a notebook. Then what you keep.',
        plan_note=('We have two hours. The first ten minutes set the question of the day. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures and ask questions. '
                   'After a ten minute break you open the Lakeside Mart workbook in Google Sheets and then a Google Colab notebook, for a forty-five minute lab. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 0',
        recall=[],
        words=[('Data science', 'Using data, tools and careful thinking to answer a question and support a decision. It is a way of working that runs from question to decision.'),
               ('Machine learning (ML)', 'A computer finds a rule from examples. A person does not type the rule.'),
               ('Dataset', 'A collection of data about one subject, arranged in tables. In Excel words: a workbook in which each tab is one table.'),
               ('Model', 'A rule found from data that turns inputs into a prediction or an explanation.'),
               ('Lifecycle (CRISP-DM)', 'The phases a data project passes through. CRISP-DM is the industry reference: six phases, from business understanding to deployment.')],
        word_icons=['magnifier', 'robot', 'folder', 'gear', 'flag'],
        words_note=('Five words for today, and each has a spreadsheet cousin. Data science is the whole way of working, from question to decision. Machine learning is a computer finding a rule from examples. '
                    'A dataset is a workbook in which each tab is one table. A model is a rule found from data. And the lifecycle is the route a project follows. The industry reference for it is called CRISP-DM. '
                    'You already know more of these ideas than you think.'),
        keep='Keep your saved Session 1 notebook in Google Drive, and your one-sentence business question with the decision it would feed.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A saved Colab notebook'), dict(label='Your question', value='One decision, one question'), dict(label='Next session', value='Data as tables')]),
        keep_title='Save your notebook and your question, then bring one question to Session 2',
        next='Session 2: Data as tables: records, variables and keys. We open every tab of the Lakeside workbook and learn how the tables connect.', next_label='Next session',
        keep_note=('Before you go, make sure your notebook is saved to your own Google Drive, and that you have written down your business question with the decision it would feed. '
                   'Those two things are your keepsake from today. A good question names something to measure and a decision that someone must make. '
                   'Next session we look closely at the thing every later session depends on, the table. If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome, everyone, and well done for coming after a full day of work. Over twenty-four sessions you will learn how people turn data into decisions. '
                    'You start in a spreadsheet, which you already know, and you finish with a tested model and a small app that a colleague can open. '
                    'Today is the map. We look at what a data scientist does, how a data project is organised, and which free tools we use. Then you open a notebook and run your first line of Python.'),
        use_at_work='Frame a business question as a decision, and recompute any figure before you report it.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 definition and flow
    S.append(dict(kind='idea', title='Data science turns a question and data into a decision',
                  visual=dict(kind='flow', steps=[dict(head='Question', text='A decision to make', icon='question'), dict(head='Data', text='Rows and columns', icon='grid'),
                                                  dict(head='Method', text='Counts, charts, models', icon='chart'), dict(head='Decision', text='Advice to act on', icon='check')]),
                  lead='Data science is a way of working: someone asks, data answers, and a person decides.',
                  points=['Dataset: a workbook in which each tab is one table.', 'Model: a rule found from data. You fit your first model in Session 13.', 'A chart nobody uses has failed.'],
                  notes=('So what is data science? My answer is simple. It is a way of working that turns a question and some data into a decision. It starts with a decision that somebody has to make. '
                         'Then you find the data, which means rows and columns, the same as in your spreadsheets. In Excel words, a dataset is a workbook where each tab is one table. '
                         'Then you apply a method. Mostly that is counting, charts and careful comparisons, and sometimes a model, which is a rule found from data. It ends with advice a manager can act on. Which of the four boxes do you think people forget most often?')))

    # ------------------------------------------------------------------ 2 business question
    S.append(dict(kind='compare', title='A business question worth asking names the decision it feeds',
                  left=dict(head='A weak question', icon='cross', points=['Tell me about sales.', 'No decision attached.', 'No number to find.']),
                  right=dict(head='A strong question', icon='check', points=['Which branch has the lowest median order value this quarter, so it gets next month\'s support visit?', 'It names the measure (median order value) and the decision (the support visit).', 'The Lakeside workbook has the data.']),
                  verdict='Write the decision first, then the question.',
                  notes=('Every project starts with a question, and most weak projects start with a weak question. Tell me about sales is weak. It has no decision attached, no number to find, and no sign of when you are done. '
                         'Which branch has the lowest median order value this quarter, so it gets next month\'s support visit, is strong. It names what to measure, which is the median order value. It names the decision it feeds, which is the support visit. '
                         'And it needs data you can actually get, which is the Lakeside workbook. So write the decision first, then the question. Think of one question from your own work. Is it weak or strong?')))

    # ------------------------------------------------------------------ 3 CRISP-DM
    S.append(dict(kind='wide', title='CRISP-DM, the industry reference, splits a data project into six phases',
                  visual=dict(kind='cycle', items=['Business understanding', 'Data understanding', 'Data preparation', 'Modelling', 'Evaluation', 'Deployment'], center='Data'),
                  caption='CRISP-DM: Cross-Industry Standard Process for Data Mining. A later phase can send you back.',
                  notes=('This circle is the lifecycle, and it has a real name that you will meet in job adverts and textbooks. It is called CRISP-DM, which stands for Cross-Industry Standard Process for Data Mining. '
                         'It was written down in the late 1990s and many teams still use it. It has six phases. Business understanding, data understanding, data preparation, modelling, evaluation and deployment. '
                         'Data sits in the middle because every phase touches it. The arrows go round, but you also go back. If evaluation shows a problem, you return to an earlier phase. Which phase do you expect to take the most time?')))

    # ------------------------------------------------------------------ 4 phases table
    S.append(dict(kind='table', title='Each CRISP-DM phase answers a plain question, and this course covers all six',
                  headers=['CRISP-DM phase', 'The plain question', 'Where in this course'],
                  rows=[['Business understanding', 'What decision are we helping with?', 'Session 1 and the course project, Session 24'],
                        ['Data understanding', 'What does each table and variable mean?', 'Sessions 2 to 4 and Session 11'],
                        ['Data preparation', 'How do we clean and join the data?', 'Module B, with the cleaning milestone in Session 8'],
                        ['Modelling', 'Which rule fits the data?', 'Sessions 13 to 22'],
                        ['Evaluation', 'Is the result good enough and fair?', 'Inside every modelling session and Session 19'],
                        ['Deployment', 'How do other people use it?', 'Session 23 (a small app) and Session 24']],
                  widths=[3.2, 4.4, 4.4], icons=['flag', 'magnifier', 'gear', 'chart', 'check', 'laptop'],
                  note='Many teams add a seventh step after deployment: monitor, which means check later that it still works.',
                  notes=('Here is each phase with the plain question it answers, and where we do it in this course. Business understanding asks what decision we are helping with. Data understanding asks what each table and variable means. '
                         'Data preparation is cleaning and joining. Modelling asks which rule fits the data. Evaluation asks whether the result is good enough and fair. Deployment asks how other people use it. '
                         'Many teams add a seventh step, monitoring, where you check later that it still works. The session numbers are the plan today and may shift a little. Which phase is the first one you would hand to a colleague?')))

    # ------------------------------------------------------------------ 5 Lakeside walk-through
    br = B['by_branch']
    S.append(dict(kind='table', title='One Lakeside question walks through all six phases',
                  headers=['CRISP-DM phase', 'The Lakeside example'],
                  rows=[['Business understanding', 'Decide which branch gets next month\'s promotion budget.'],
                        ['Data understanding', f'The orders tab has {n(R["orders"])} records. The branches tab has {R["branches"]} records.'],
                        ['Data preparation', f'{n(blank)} orders have a blank customer_id. They are walk-in shoppers, so keep them.'],
                        ['Modelling', 'A pivot table of orders and total sales for each branch. A predictive model comes in Module D.'],
                        ['Evaluation', f'Jinja leads on the mean order, {n(F["jinja_mean"])} UGX. One order of {n(B["max"])} UGX adds about {n(round(F["jinja_delta"], -2))} UGX to that mean, but Jinja still leads without it. Check the median and the count too.'],
                        ['Deployment', 'One page for the manager that shows the count of orders behind each figure.']],
                  widths=[3.2, 8.8], icons=['flag', 'magnifier', 'gear', 'chart', 'check', 'laptop'],
                  notes=(f'Let us walk one real question through the six phases. The question: which branch gets next month\'s promotion budget? Data understanding: the orders tab has {n(R["orders"])} records and branches has {R["branches"]}. '
                         f'Data preparation: {n(blank)} orders have a blank customer id. They are walk-in shoppers, so we keep them. Modelling: a pivot table is enough here. '
                         f'Evaluation matters most. Jinja leads on the mean order, about {n(F["jinja_mean"])} shillings, but one single order of {n(B["max"])} shillings adds about {n(round(F["jinja_delta"], -2))} shillings to it. Jinja still leads without that order, so we check the median and the count before we decide. And deployment is one page for the manager. Would you have caught that large order?')))

    # ------------------------------------------------------------------ 6 habits
    S.append(dict(kind='statement', title='Thinking in data means four habits, and you practise each one in this course',
                  lead='Before you touch a number, ask these four things.',
                  points=['What decision is this for?', 'What does one record stand for?', 'Where did the data come from, and how many records are there?', 'Did I calculate this number, or did someone tell me?'],
                  icons=['flag', 'notebook', 'folder', 'calculator'],
                  notes=('Beyond the lifecycle, here are four habits that mark someone who thinks in data. First, what decision is this for? Second, what does one record stand for? Is each row an order, a product on an order, or a customer? '
                         'Third, where did the data come from, and how many records are there? A figure from twenty records means something different from a figure from twenty thousand. '
                         'Fourth, did I calculate this number, or did someone tell me? Session 2 teaches the second habit properly. Which of the four is hardest for you at work?')))

    # ------------------------------------------------------------------ 7 roles
    S.append(dict(kind='wide', title='Four roles share the work on a data team',
                  visual=dict(kind='icons', items=[dict(icon='folder', head='Data engineer', text='Builds pipelines and databases.'),
                                                   dict(icon='chart', head='Data analyst', text='Answers questions about the past.'),
                                                   dict(icon='magnifier', head='Data scientist', text='Tests ideas and builds models.'),
                                                   dict(icon='gear', head='Machine learning engineer', text='Puts a model into a product.')]),
                  caption='One person often does several jobs. You practise the analyst and scientist jobs.',
                  notes=('Data work is a team sport, and four job titles come up again and again. The data engineer builds the pipelines that move data and keeps the databases running. '
                         'The data analyst answers questions about the past with tables, charts and dashboards. The data scientist tests ideas and builds models that explain or predict. '
                         'And the machine learning engineer puts a model into a product and keeps it running. In a small organisation in Uganda, one person often does several of these jobs. '
                         'In this course you practise the analyst and the data scientist jobs. Which of the four is closest to your job today?')))

    # ------------------------------------------------------------------ 8 AI, ML, DL, DS
    S.append(dict(kind='wide', title='Artificial intelligence, machine learning, deep learning and data science differ',
                  visual=dict(kind='dsb_nested', items=[('Software that does tasks we call smart', 'Example: a spam filter.'),
                                                        ('Rules learned from examples', 'Produces a model. Example: loan default.'),
                                                        ('Neural networks with many layers', 'Example: speech recognition.')],
                              data_science='Data science: a way of working from question to decision. It produces advice, and uses any circle only when it helps.'),
                  caption='Data science is the way of working, and often needs no machine learning.',
                  notes=('You hear three big words in the news. Artificial intelligence is the biggest circle. It means any software that does a task we would call smart, like a spam filter. '
                         'Machine learning sits inside it. These programs find rules from examples, and the result is a model. Deep learning is a smaller circle inside machine learning. It uses neural networks with many layers, and it powers speech recognition. '
                         'Data science is different. It is a way of working from question to decision, and it uses machine learning only when that helps. Often a pivot table is enough. Which circle did you think data science was?')))

    # ------------------------------------------------------------------ 9 formula versus model
    S.append(dict(kind='compare', title='A formula is a rule you write; a model is a rule found from data',
                  left=dict(head='Rule written by a person', icon='calculator', points=['Revenue = quantity × price × (1 − discount).', f'It holds on all {n(R["order_lines"])} order lines.']),
                  right=dict(head='Rule found from examples', icon='robot', points=[f'Nile Microfinance: {n(F["loans_n"])} loans, {n(F["loans_default"])} defaulted.', 'An algorithm finds which loan details go with default.']),
                  verdict='A model is a rule found from data.',
                  notes=(f'Here is the difference between a formula and a model. On the left, a rule that a person wrote. Revenue of an order line is quantity times unit price times one minus the discount. '
                         f'We checked, and it holds on all {n(R["order_lines"])} order lines in the workbook. On the right, a rule found from examples. In the fictional Nile Microfinance file, {n(F["loans_n"])} past loans are recorded and {n(F["loans_default"])} of them defaulted. '
                         'A learning algorithm looks at the loan details and finds which ones go with default. Nobody typed that rule. That is machine learning, and you fit your first model in Session 13 (regression) and build machine learning models from Session 14. Can you think of a rule in your work that nobody could write by hand?')))

    # ------------------------------------------------------------------ 10 the Lakeside workbook
    S.append(dict(kind='wide', title='Lakeside Mart is the real data for the whole course',
                  visual=dict(kind='icons', items=[dict(icon='receipt', head=f'{n(R["orders"])} orders', text='One record per till order'),
                                                   dict(icon='bag', head=f'{n(R["order_lines"])} order lines', text='One per product on an order'),
                                                   dict(icon='shop', head=f'{R["branches"]} branches', text='Eight shops in Uganda'),
                                                   dict(icon='tag', head=f'{R["products"]} products', text='One record per product')]),
                  caption=f'Fictional, generated data. A sample of a {n(B["full_n"])}-order file.',
                  notes=(f'Now the data we use all course. Lakeside Mart is a fictional chain of eight mini-markets in Uganda. The workbook has {len(F["tabs"])} tabs: six data tabs and a READ ME. '
                         f'The orders tab has {n(R["orders"])} records. Each record is one till order. The order lines tab has {n(R["order_lines"])} records, one for each product on an order. There are {R["branches"]} branches and {R["products"]} products. '
                         f'The workbook is a sample of {n(R["orders"])} orders from a full file of {n(B["full_n"])}. Everything is generated, so no real person or company appears. In Session 2 we look at every tab closely. Which table would you open first?')))

    # ------------------------------------------------------------------ 11 the unchecked assistant
    S.append(dict(kind='compare', title='A chat assistant can state a figure that nobody calculated',
                  left=dict(head='Unchecked', icon='cross', points=['You ask for the share of orders paid by Mobile money.', 'It answers with a clean percentage.', 'It predicts likely words and may not calculate.']),
                  right=dict(head='Checked', icon='check', points=['One COUNTIF formula in Sheets gives it.', f'{n(F["mm"])} of {n(R["orders"])} orders: {F["mm_share"] * 100:.1f} percent.', 'Write the source beside the figure.']),
                  verdict='Recompute every number you did not calculate yourself.',
                  notes=(f'This habit will protect your reputation. You ask a chat assistant what share of orders is paid by mobile money. It answers with a clean percentage in a friendly tone. An assistant predicts likely words, so it can state a figure that nobody calculated. '
                         f'Nothing in its tone tells you which figures are real. The check takes one formula in Sheets: count the orders paid by mobile money and divide by all orders. The answer is {n(F["mm"])} out of {n(R["orders"])}, which is {F["mm_share"] * 100:.1f} percent. '
                         'Write the source beside the figure. A free assistant is welcome as a helper in this course, but never as the source of a number. Have you ever pasted a number you did not check?')))

    # ------------------------------------------------------------------ 12 toolset
    S.append(dict(kind='table', title='Every tool in this course is free for you and for the tutor',
                  headers=['Tool', 'What you use it for', 'Cost'],
                  rows=[['Google Colab', 'Python notebooks in your browser', 'Free with a Google account'], ['Google Sheets (or Excel, LibreOffice)', 'Tables, pivot tables and charts', 'Free, or what you own'],
                        ['pandas, NumPy, scikit-learn, matplotlib', 'Data work, models and charts in Python', 'Free, open source'], ['SQLite', 'Questions to a database with SQL', 'Free, inside Python'],
                        ['GitHub', 'Save and share your work', 'Free account'], ['Streamlit Community Cloud', 'A small web app for your model', 'Free for public apps']],
                  widths=[4.4, 4.6, 3.0], icons=['laptop', 'grid', 'chart', 'folder', 'people', 'phone'], note='At the time of writing these are free. Free plans can change, so check current terms before you rely on one.',
                  notes=('Every tool in this course is free for you and for me. Google Colab runs Python notebooks in your browser, so there is nothing to install. Google Sheets, Excel or LibreOffice give you tables, pivot tables and charts. '
                         'The Python libraries pandas, NumPy, scikit-learn and matplotlib do the data work, the models and the charts. SQLite lets you ask questions of a database with SQL. '
                         'GitHub saves and shares your work, and Streamlit Community Cloud turns a model into a small web app. At the time of writing all of these are free, but free plans change, so check the current terms. Which of these have you already used?')))

    # ------------------------------------------------------------------ 13 course path
    S.append(dict(kind='table', title='The course is six modules, and each builds on the one before',
                  headers=['Module', 'Sessions', 'What you do'],
                  rows=[['A  Think with data', '1 to 4', 'Sheets, no code'], ['B  Python for data', '5 to 9', 'Python, pandas, first SQL'], ['C  Analyse and explain', '10 to 13', 'SQL, charts, inference, regression'],
                        ['D  Machine learning', '14 to 19', 'Build, test and judge models'], ['E  Neural networks and text', '20 to 22', 'Networks, text, embeddings'], ['F  Ship it and present', '23 and 24', 'A small app, then your course project']],
                  widths=[4.4, 2.0, 5.6], icons=['grid', 'laptop', 'chart', 'robot', 'speech', 'flag'], note='Project milestones are in Sessions 8, 13, 19 and 24. Every session has a concepts half, then a lab where you work.',
                  notes=('Here is the path for the whole course. Module A, today and the next three sessions, is thinking with data in Sheets, with no code. Module B teaches Python for data. Module C is analysing and explaining: SQL, charts, inference and regression. '
                         'Module D is machine learning, where you build, test and judge models. Module E covers neural networks and text. Module F is shipping and presenting: a small app, then your course project. '
                         'Sessions 8, 13, 19 and 24 have a project milestone, a practical piece of work that you show me and get feedback on. Nothing in this course is scored, and you keep everything you build. Forty-eight hours is short, so we choose the working core of the field. Which module are you most looking forward to?')))

    # ------------------------------------------------------------------ 14 Colab limits
    S.append(dict(kind='wide', title='Colab is free, with limits to plan for',
                  visual=dict(kind='icons', items=[dict(icon='clock', head='Idle time', text='A session ends when you stop working.'), dict(icon='calendar', head='Length', text='A maximum session time applies.'),
                                                   dict(icon='question', head='Quota', text='Limits are not published and can change.'), dict(icon='folder', head='Save', text='Keep notebooks in Drive or GitHub.')]),
                  caption='My understanding at the time of writing. Check current limits.',
                  notes=('Colab is free, and free comes with limits. A free session ends after you stop working for a while, which is the idle time. A session also ends after a maximum length. Reports mention about twelve hours, but Google does not publish exact limits, and they can change. '
                         'So plan for it from day one. Save your notebooks in Google Drive or on GitHub, and run the cells again from the top when a session ends. '
                         'That is my understanding at the time of writing, so check the current limits before you rely on a long run. Where will you keep your notebooks?')))

    # ------------------------------------------------------------------ 15 notebook anatomy
    S.append(dict(kind='wide', title='A notebook is made of cells: text cells you read and code cells you run',
                  visual=dict(kind='dsb_notebook', title='Session 1 lab.ipynb', text_cell='Task 1. Print a sentence', code=CODE[:2], output=F['cell_output'][:1],
                              labels=['A text cell holds instructions you read.', 'A code cell holds Python. Press its play button to run it.', 'The output appears under the cell.']),
                  caption='Python is the programming language. A cell is one box of code. Run it, read it, change it, save it.',
                  notes=('This is what a notebook looks like. It is a document made of cells. A text cell, marked one, holds instructions that you read. A code cell, marked two, holds Python, and you run it with the play button beside it. '
                         'The output, marked three, appears under the cell. In this picture the code stores a sentence in a name called message and then prints it, and the sentence appears. We ran this exact code to get that output. '
                         'You can edit any cell, run it again, and see the output change. That is the whole loop. Does anything on this picture look unfamiliar?')))

    # ------------------------------------------------------------------ 16 use at work
    S.append(dict(kind='table', title='Where you will use this at work: frame the question before you open the data',
                  headers=['Your job', 'The question you start from', 'What today lets you do'],
                  rows=[['Credit officer at a bank in Kampala', 'Which loan applications are likely to go unpaid?', 'Write the decision first, then find the loans table.'],
                        ['Monitoring and evaluation officer at an NGO', 'Did the training raise farmers\' yields?', 'Name the data you need before you promise a report.'],
                        ['Operations manager at a retail chain', 'Which branch has the lowest median order value, so it gets next month\'s support visit?', 'Check any figure an assistant gives you against your own workbook.'],
                        ['Health records officer at a district office', 'Which months do clinics run short of drugs?', 'Use the six phases as a checklist for a monthly report.']],
                  widths=[3.7, 4.2, 4.1], icons=['coin', 'people', 'shop', 'clinic'],
                  notes=('Where will you use this on Monday? Four examples. A credit officer at a bank in Kampala starts from the question: which loan applications are likely to go unpaid? Writing the decision first points to the loans table. '
                         'A monitoring and evaluation officer at an NGO asks whether training raised farmers\' yields, and names the data needed before promising a report. An operations manager at a retail chain asks which branch has the lowest median order value, so it gets the support visit, and checks any figure an assistant gives against the workbook. '
                         'A health records officer uses the six phases as a checklist for a monthly report. Which of these is closest to your job?')))

    # ------------------------------------------------------------------ 17 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: four lines make your first cell',
                  code='\n'.join(CODE), output=list(F['cell_output']),
                  reads=['Line 1 stores a sentence in a name called message.', 'Line 2 prints it under the cell.', 'Line 3 adds two illustrative prices in UGX, rice 4,500 and sugar 2,800, and stores the sum in total.', f'Line 4 prints {F["price_sum"]}.'],
                  notes=(f'Before the lab, read the recipe. This is real Python, and we ran it. Line one stores a sentence in a name called message. Line two prints it. Line three adds two illustrative prices, 4,500 shillings for rice and 2,800 for sugar, and stores the result in a name called total. '
                         f'Line four prints it, and the answer is {F["price_sum"]}. In Python a name that holds a value is called a variable. This is a second meaning of the word: in a table, a variable is a column. Context tells you which. In the lab you write these lines yourself, run them with the play button, and read what comes out. '
                         'Then you change one thing and run it again. What do you expect if you change the sentence?')))

    # ------------------------------------------------------------------ 18 divider
    S.append(dict(kind='divider', title='Part 2: the Sheets and Colab lab', lead='Close the slides. Open the sheet.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen. First, open the Lakeside Mart workbook in Google Sheets, or in Excel if you prefer. The file is called lakeside for sheets. '
                         'You count the records and variables of each tab, and recompute one share. After that you open the Session 1 notebook in Google Colab and run your first cells. '
                         'In every task, predict the answer first, then run it, then read what you see.')))

    # ------------------------------------------------------------------ 19 lab map
    S.append(dict(kind='steps', title='The lab has five steps: two in Sheets and three in Colab',
                  steps=[dict(head='1 Open', text='The workbook', icon='folder'), dict(head='2 Count', text='Records and variables', icon='calculator'), dict(head='3 Run', text='Your first Colab cell', icon='laptop'),
                         dict(head='4 Store', text='A sum and a list', icon='notebook'), dict(head='5 Ask', text='Your own question', icon='question')], highlight=None,
                  caption='About 45 minutes. For each task, predict first, then run it, then read the answer. Save your notebook to your Drive at the end.',
                  notes=('Here is the map of the lab. Step one, open the workbook and find its tabs. Step two, count the records and variables of each tab, and recompute the mobile money share. '
                         'Step three, open the notebook in Colab and run your first cell. Step four, store a sum and a list, and load the full orders file to count its records. '
                         'Step five, write your own business question with the decision it would feed. In every task, predict first. Please do not skip the predictions, because they are where you learn the most.')))

    # ------------------------------------------------------------------ 20 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Tabs in the workbook, with READ ME', str(len(F['tabs']))], ['Records in orders, and in order_lines', f'{n(R["orders"])} and {n(R["order_lines"])}'], ['Variables in orders, and in order_lines', f'{V["orders"]} and {V["order_lines"]}'],
                        ['Blank customer_id in orders', n(blank)], ['Share of orders paid by Mobile money', f'{n(F["mm"])} of {n(R["orders"])}, which is {F["mm_share"] * 100:.1f} percent'],
                        ['Output of your first cell', F['cell_output'][0]], ['The sum of 4500 and 2800', str(F['price_sum'])], ['Records in the full orders.csv file', n(B['full_n'])]],
                  widths=[6.0, 6.0], icons=['folder', 'grid', 'doc', 'question', 'phone', 'laptop', 'calculator', 'receipt'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The most common cause in Sheets is a range that includes the header row, which makes every count one too big. In Colab it is a cell run out of order. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your count of records in orders comes out as two thousand and one?')))

    # ------------------------------------------------------------------ 21 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'A count of {n(R["orders"] + 1)} where you expected {n(R["orders"])}', 'The range includes the header cell in row 1.', 'Start the range in row 2: A2:A2001.'],
                        ["NameError: name 'message' is not defined", 'You ran a cell before the cell that creates the name.', 'Run the cells from the top, one after the other.'],
                        ['SyntaxError: unterminated string', 'A quote mark is missing at one end of the text.', 'Put the same quote mark at both ends: \'text\'.'],
                        ['FileNotFoundError: orders.csv', 'The setup cell has not run, or data.zip was not chosen.', 'Run the setup cell and choose data.zip.'],
                        ['Runtime disconnected', 'A free session timed out.', 'Reconnect, run from the top, and save a copy to Drive.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'clock'],
                  notes=('Five messages you may meet. A count that is one too big means your range includes the header row. A NameError means you ran a cell before the cell that creates the name, so run from the top. '
                         'A SyntaxError about a string means a quote mark is missing at one end of the text. A FileNotFoundError for orders dot csv means the setup cell has not run, or you did not choose the data zip file. '
                         'And a disconnected runtime means the free session timed out, so reconnect and run again. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 22 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['In CRISP-DM, which phase comes straight after business understanding, and what do you do in it?', 'Data understanding: find the tables that could answer the question and check what they mean.'],
                        ['In Excel words, what is a dataset, and how does a model differ from a formula?', 'A dataset is a workbook in which each tab is one table. A model is a rule found from data, where a formula is typed by a person.'],
                        ['An assistant gives you the share of orders paid by Mobile money. What do you do before you report it?', f'Recompute it from your own data: {F["mm_share"] * 100:.1f} percent, {n(F["mm"])} of {n(R["orders"])}. Write the source beside it.']],
                  widths=[5.6, 6.4], icons=['magnifier', 'folder', 'phone'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, in CRISP-DM, which phase comes straight after business understanding, and what do you do in it? '
                         'Two, in Excel words, what is a dataset, and how does a model differ from a formula? Three, an assistant gives you a share of orders paid by Mobile money. What do you do before you report it? '
                         'The short answers are on the slide. These three are also the warm-up questions in Session 2. If one surprised you, look at that slide again tonight.')))

    # ------------------------------------------------------------------ sheet tasks
    T = B['T']
    sess['sheet_tasks'] = [
        dict(task='Open lakeside_for_sheets.xlsx in Google Sheets (File, Import, Upload), or open it in Excel. How many tabs does it have, and what are their names?',
             answer=f'{len(F["tabs"])} tabs: ' + ', '.join(F['tabs']) + '. Six are data tabs and READ ME is a note.'),
        dict(task='Orders tab. Count the records with =COUNTA(orders!A2:A2001) and the variables with =COUNTA(orders!A1:G1). Leave out the header row when you count records.',
             answer=f'{n(R["orders"])} records and {V["orders"]} variables. The last row number is {n(R["orders"] + 1)} because row 1 holds the variable names.'),
        dict(task='Order_lines tab. Count its records (=COUNTA(order_lines!A2:A6591)) and variables (=COUNTA(order_lines!A1:G1)). Then divide the lines by the orders: =COUNTA(order_lines!A2:A6591)/COUNTA(orders!A2:A2001).',
             answer=f'{n(R["order_lines"])} records and {V["order_lines"]} variables. {n(R["order_lines"])} divided by {n(R["orders"])} is {F["lpo"]:.2f} lines for each order on average.'),
        dict(task='Write one sentence for each of the two tabs: what does one record stand for?',
             answer='orders: one record is one till order. order_lines: one record is one product on one order.'),
        dict(task='Find the number of records and variables of branches, products, customers and branch_weeks (the same two formulas, with the tab name and the last row changed).',
             answer=f'branches: {R["branches"]} records, {V["branches"]} variables. products: {R["products"]}, {V["products"]}. customers: {n(R["customers"])}, {V["customers"]}. branch_weeks: {R["branch_weeks"]}, {V["branch_weeks"]}.'),
        dict(task='On the orders tab, count the blank customer_id cells: =COUNTBLANK(orders!D2:D2001). What share of the orders is that, and what do you think the blank means?',
             answer=f'{n(blank)} blank cells, which is {F["blank_pct"]:.0f} percent of the orders (=COUNTBLANK(orders!D2:D2001)/COUNTA(orders!A2:A2001)). The data dictionary says a blank means a walk-in shopper with no loyalty number.'),
        dict(task='An assistant says that about half of the orders are paid by Mobile money. Check it: =COUNTIF(orders!E2:E2001,"Mobile money")/COUNTA(orders!A2:A2001). Format the cell as a percentage.',
             answer=f'{n(F["mm"])} of {n(R["orders"])} orders, which is {F["mm_share"] * 100:.1f} percent (0.{round(F["mm_share"] * 1000):03d}). The assistant was close, but only your own formula can be written down as a source.'),
        dict(task='Write one business question from your own work, with the decision it would feed and the data you would need. Choose which CRISP-DM phase you think would be hardest.',
             answer='Open answer. A good one names something to measure, a decision, and data you could get. Example: Which of our 8 branches should get next month\'s promotion budget? Data: orders and branches.'),
    ]

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck, the workbook lakeside_for_sheets.xlsx in Google Sheets, and the Session 1 notebook in Colab before anyone arrives. Share the workbook so every learner can make a copy.',
              'Check that learners can sign in to Google. Any learner without a Google account should create a free one before the lab, or work from Excel and a local setup that you arrange.',
              'On your own account, run the notebook from the top, including the setup cell with data.zip, so you know what the upload dialog looks like.',
              'Write the check table (slide 24 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the workbook only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated, and that Colab limits can change: check the current limits before the session.'],
        misconceptions=[('Data science, machine learning and AI are the same thing', 'AI is the widest circle, machine learning sits inside it, and deep learning inside that. Data science is a way of working that may use any of them.'),
                        ('Machine learning is needed for every data project', 'Many projects need only a pivot table or a chart. Use a model only when it helps the decision.'),
                        ('An AI assistant gives facts, so I can paste its figures into a report', 'An assistant predicts likely words and can state a number nobody calculated. Recompute and cite the source.'),
                        ('A data scientist is only someone who builds models', 'Four roles share the work: data engineer, analyst, data scientist and machine learning engineer. Most of the time goes on data preparation.'),
                        ('If Colab shuts down I have lost my work', 'Saved notebooks in Drive survive. Run the cells again from the top.')],
        probes=[('Which CRISP-DM phase comes after business understanding?', 'Data understanding.'),
                ('Name the four roles on a data team.', 'Data engineer, data analyst, data scientist, machine learning engineer.'),
                ('What does one record of the orders tab stand for?', 'One till order.'),
                ('What is a model?', 'A rule found from data that turns inputs into a prediction or an explanation.'),
                ('Why do we say CRISP-DM is the industry reference?', 'It is a widely used standard process for data projects, published in the late 1990s and still used by many teams.'),
                ('What do you do with a number from a chat assistant?', 'Recompute it from your own data and write the source beside it.')],
        lab_steps=[('Task 1: tabs', f'{len(F["tabs"])} tabs including READ ME. Learners who see six tabs have missed READ ME.'),
                   ('Task 2: orders counts', f'{n(R["orders"])} and {V["orders"]}. A count of {n(R["orders"] + 1)} means the range includes the header.'),
                   ('Task 3: order_lines counts', f'{n(R["order_lines"])} and {V["order_lines"]}; {F["lpo"]:.2f} lines for each order.'),
                   ('Task 4: record sentences', 'One till order; one product on one order. Accept any clear wording.'),
                   ('Task 5: other tabs', f'{R["branches"]}, {R["products"]}, {n(R["customers"])}, {R["branch_weeks"]} records.'),
                   ('Task 6: blank customer_id', f'{n(blank)}, {F["blank_pct"]:.0f} percent. Make sure the word walk-in is used.'),
                   ('Task 7: the share check', f'{F["mm_share"] * 100:.1f} percent. Praise anyone who writes the formula as the source.'),
                   ('Notebook tasks 1 to 4', 'Message printed, total 7300, a list of three branch names, and 30,229 records in orders.csv. Learners who press play on a later cell first get a NameError: run from the top.'),
                   ('Your own question', 'A good question names a measure, a decision and data that exists. Weak: Tell me about sales.')],
        rescue=['If the concepts run over, shorten the toolset table (slide 16) and the course path (slide 17) to a quick look.',
                'If only 30 minutes of lab remain, do tasks 1, 2, 6 and 7 in Sheets and notebook tasks 1 and 2, and set the rest as homework.',
                'If a learner cannot reach Google Colab, pair them with a neighbour for the notebook part and have them redo it at home.',
                'If the upload of data.zip fails, ask the learner to upload orders.csv alone: only the last task needs it.'],
        after=['Share the workbook, the deck and the solution notebook again for learners who were absent.', 'Ask each learner to bring one question about their own data to Session 2.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 2 PREDICT: how many records will orders have?', f'{n(R["orders"])}. The sheet shows {n(R["orders"] + 1)} rows because of the header.'],
                        ['Task 3 PREDICT: lines for each order, more or less than 3?', f'{F["lpo"]:.2f}, a little more than 3.'],
                        ['Task 6 READ: what does a blank customer_id tell you?', 'The order was placed by a walk-in shopper with no loyalty number. It is real data, not an error.'],
                        ['Task 7 READ: how close was the assistant?', f'Close ({F["mm_share"] * 100:.1f} percent) but it had no calculation behind it. Your formula is the source.'],
                        ['Notebook 1 CHANGE: change the sentence and run again.', 'The output changes to the new sentence.'],
                        ['Notebook 2 READ: why does print(total) show a number with no UGX?', 'Python stores the number only. The unit UGX is in your head and in the comment.'],
                        ['Notebook 4 READ: why does orders.csv have more records than the workbook?', f'The workbook is a {n(R["orders"])}-order sample of the full file of {n(B["full_n"])} orders.']])
    return sess
