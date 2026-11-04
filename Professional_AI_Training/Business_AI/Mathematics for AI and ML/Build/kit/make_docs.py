"""Word and PDF documents generated from the session files so slides, labs and guides never disagree.
python3 kit/make_docs.py [guide|script|learner|all]
Writes: Facilitator Materials/Facilitator Guide, Presenter Script; Learner Materials/Start Here, Formula Sheet (template), Glossary of Terms and Symbols (each .docx and .pdf)."""
import os
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
import deck  # noqa: E402
from docx_kit import *  # noqa: E402,F401,F403

W = CONTENT_CM
SESS = [deck.load(n) for n in range(1, 19)]


def to_pdf(path):
    subprocess.run(['soffice', f'-env:UserInstallation=file:///tmp/lo_docs{os.getpid()}', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True, timeout=240)


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


def clock_rows(s):
    t, rows = 0, []
    for m, lab in s['clock']:
        rows.append([f'{t // 60}:{t % 60:02d}', str(m), lab])
        t += m
    return rows


def guide():
    d = new_doc('Facilitator Guide', 'Mathematics for AI and Machine Learning')
    title(d, 'Facilitator Guide', 'Mathematics for AI and Machine Learning  |  18 sessions of 2 hours  |  Keep it private')
    h2(d, 'How to teach this course', 0)
    para(d, 'Every session has the same shape: recall, a concept told with a picture and one example worked by hand, a break, a lab, and then where the idea appears in AI. Learners choose the Python notebook (Google Colab) or the spreadsheet workbook (Excel or Google Sheets). Both labs use the same data and give the same numbers, so you can teach one class that mixes coders and non-coders. Do the concept half with no laptops open. Switch to the lab once, at the black "Part 2" slide.', 10, after=4)
    h2(d, 'Before the first session')
    bullets(d, ['Check that every learner can open Google Colab with a Google account, and can open an .xlsx file in Excel or in Google Sheets (File, Import, Upload, Replace spreadsheet).',
                'Install the Lato fonts from brand/fonts on the teaching laptop so the slides look right. Open each deck in Presenter View: the spoken script is in the notes.',
                'Share the notebooks and workbooks in the Notebooks and Workbooks folders. Keep Facilitator Materials private: it holds the solution notebooks and the capstone grader.',
                'Run each lab yourself once in Colab and in a spreadsheet before the session. The notebooks were proved with numpy only, not on Colab itself.'], 10)
    h2(d, 'What you can say about ChatGPT, Gemini, Claude and other AI')
    para(d, 'These are products built on large language models. Their exact internals are not published. Say what published research describes (transformers, attention, next-token prediction trained with cross-entropy, Adam, low-rank adaptation) and what open models such as Llama, Gemma and Mistral publish. Do not quote parameter counts, layer counts or training details of closed models. The "Where this appears in AI" slides are written to that rule. If a learner asks about a closed product, answer "my understanding is that the maker has not published that; here is what published models of this kind do".', 10, after=4)
    h2(d, 'Automatic checks')
    bullets(d, ['Each notebook has check cells that print OK or NOT YET and finish with "All N checks pass". Each workbook has a Check sheet with the same idea. Learners can run them as often as they like.',
                'The capstone (Session 18) is individual and graded. The learner types a student ID; their data come from a seed made from that ID. Run Facilitator Materials/Autocheck/grade_capstone.py on a submitted notebook. Change the secret seeds in that script before real use.',
                'Marks are not given for the other sessions; the checks are for the learner to see that the lab worked.'], 10)
    page_break(d)
    for s in SESS:
        n = s['num']
        title(d, f'Session {n}: {s["short_title"]}', f'{s["block"]}  |  {s["title"]}')
        para(d, 'The question of the day: ' + s['question'], 10.5, italic=True, after=4)
        h2(d, 'The clock', 4)
        grid(d, clock_rows(s), [2.0, 2.0, 13.4], header=['Starts', 'Minutes', 'What happens'], size=9)
        f = s['facilitator']
        if f.get('prep'):
            h2(d, 'Before the session')
            bullets(d, f['prep'])
        h2(d, 'Slide map')
        spec = deck.build_spec(s)
        rows, part = [], 'Concepts'
        for i, sl in enumerate(spec['slides'], 1):
            t = sl['title']['text'].replace('\n', ' ') if sl.get('title') else (sl.get('title_raw') or '')
            if t.startswith('Part 2'):
                part = 'Lab'
            if t.lower().startswith('where this appears'):
                part = 'AI'
            rows.append([str(i), t, part])
        grid(d, rows, [1.1, 13.0, 3.3], header=['Slide', 'Title', 'Part'], size=8, label_cols=(0,))
        if f.get('probes'):
            h2(d, 'Questions to ask, and a good answer')
            grid(d, [[q, a] for q, a in f['probes']], [6.6, 10.8], header=['Ask', 'A good answer'], size=8.5, label_cols=())
        if f.get('misconceptions'):
            h2(d, 'Ideas learners often get wrong')
            grid(d, [[a, b] for a, b in f['misconceptions']], [6.6, 10.8], header=['What a learner may say', 'What to say back'], size=8.5, label_cols=())
        if f.get('lab_steps'):
            h2(d, 'Walking the lab (Python and spreadsheet)')
            grid(d, [[a, b] for a, b in f['lab_steps']], [4.4, 13.0], header=['Step', 'What to look for'], size=8.5)
        if f.get('lab_answer_key'):
            h2(d, 'Answer key for the PREDICT, READ and CHANGE prompts')
            grid(d, [[a, b] for a, b in f['lab_answer_key']], [7.4, 10.0], header=['Prompt', 'Answer'], size=8.5, label_cols=())
        if f.get('rescue'):
            h2(d, 'If things go wrong')
            bullets(d, f['rescue'])
        if f.get('after'):
            h2(d, 'After the session')
            bullets(d, f['after'])
        if n < 18:
            page_break(d)
    p = ROOT / 'Facilitator Materials' / 'Facilitator Guide.docx'
    save(d, p)
    to_pdf(p)


def script():
    d = new_doc('Presenter Script', 'Mathematics for AI and Machine Learning')
    title(d, 'Presenter Script', 'The spoken script of every slide, in order. The same words are in the notes of each deck.')
    for s in SESS:
        page_break(d) if s['num'] > 1 else None
        h2(d, f'Session {s["num"]}: {s["short_title"]}', 0)
        spec = deck.build_spec(s)
        for i, sl in enumerate(spec['slides'], 1):
            t = sl['title']['text'].replace('\n', ' ') if sl.get('title') else (sl.get('title_raw') or '')
            para(d, f'Slide {i}. {t}', 9.5, True, before=5, after=1, keep=True)
            for ptxt in sl['notes'].split('\n\n'):
                para(d, ptxt, 9.5, after=2)
    p = ROOT / 'Facilitator Materials' / 'Presenter Script.docx'
    save(d, p)
    to_pdf(p)


def learner():
    out = ROOT / 'Learner Materials'
    d = new_doc('Start Here', 'Mathematics for AI and Machine Learning')
    title(d, 'Start here', 'Mathematics for AI and Machine Learning  |  KLAi Professional Learning')
    para(d, 'Welcome. This course teaches the mathematics under machine learning and AI, one idea at a time: a picture, a small calculation by hand, the same idea on a computer, and where it shows up in tools such as ChatGPT, Gemini and Claude. You need high school algebra and nothing else.', 10, after=4)
    h2(d, 'What you get')
    bullets(d, [('Slides as PDF.', 'Read them again after class. They make sense without the speaker.'), ('A notebook for every session.', 'For learners who code. Open it in Google Colab (free) with a Google account.'),
                ('A workbook for every session.', 'For everyone else, and for coders who like spreadsheets. It works in Excel and in Google Sheets.'), ('A Check sheet or check cells.', 'They tell you which of your answers are right. You can try as often as you like.'),
                ('A formula sheet template.', 'You fill it in as the course goes, in your own words.')], 10)
    h2(d, 'How a session runs')
    grid(d, [['10', 'Recall, then a real question from AI'], ['35', 'Concept: a picture, then one example worked by hand'], ['10', 'Break'], ['45', 'Lab in Python, Google Sheets or Excel'], ['15', 'Where this appears in AI, and an exit check'], ['5', 'Save your work']], [2.2, 15.2], header=['Minutes', 'What happens'], size=9.5)
    h2(d, 'Using the notebook')
    bullets(d, ['Upload the notebook to Colab (File, Upload notebook). Run the cells from the top with Shift and Enter.', 'Each step is PREDICT, RUN, READ, CHANGE. Write your guess before you run. Type your answer in the line that starts with a greater-than sign.',
                'Cells with "your code here" are yours to fill. The check cells say OK or NOT YET, and finish with how many checks pass.', 'Before you finish, choose Runtime, then Restart session and run all.'], 10)
    h2(d, 'Using the workbook')
    bullets(d, ['Open the .xlsx in Excel. In Google Sheets choose File, Import, Upload, then Replace spreadsheet.', 'Gold cells are yours to fill. Everything else is given. The sheet called Check tells you which answers are right.',
                'Use the formulas shown on the Start here sheet. No add-ins, no macros.'], 10)
    h2(d, 'Using AI tools while you learn')
    para(d, 'You may ask an assistant such as ChatGPT, Gemini or Claude to explain an idea. Check what it says against your own numbers from the lab. Never paste private or confidential data into an assistant. The final capstone is your own work.', 10, after=4)
    p = out / 'Start Here.docx'
    save(d, p)
    to_pdf(p)
    # formula sheet template
    d = new_doc('Formula Sheet', 'Mathematics for AI and Machine Learning')
    title(d, 'My formula sheet', 'One page that you write yourself as the course goes. Name every symbol in plain words, and write the industry term.')
    blocks = [('Linear algebra', ['Dot product', 'Cosine similarity', 'Matrix multiplication', 'Least squares (normal equation)', 'Eigenvalue and eigenvector', 'PCA']),
              ('Calculus and optimisation', ['Derivative', 'Gradient', 'Chain rule', 'Gradient descent update', 'Backpropagation step']),
              ('Probability and statistics', ['Expectation and variance', 'Gaussian distribution', 'Bayes\' theorem', 'Maximum likelihood']),
              ('Information theory and attention', ['Entropy and cross-entropy', 'Softmax', 'Attention'])]
    for head, items in blocks:
        h2(d, head, 4)
        grid(d, [[x, '', '', ''] for x in items], [4.0, 5.2, 5.0, 3.2], header=['Name', 'Formula', 'What each symbol means', 'Where it appears in AI'], size=9, min_h=1.0)
    save(d, out / 'Formula Sheet (template).docx')
    to_pdf(out / 'Formula Sheet (template).docx')
    # glossary from the Words tables
    d = new_doc('Glossary', 'Mathematics for AI and Machine Learning')
    title(d, 'Glossary of terms', 'The words of every session, with the plain meaning. Learn the industry term; the plain words explain it.')
    rows = []
    for s in SESS:
        for term, meaning in s['words']:
            rows.append([term, meaning, str(s['num'])])
    rows.sort(key=lambda r: r[0].lower())
    grid(d, rows, [4.2, 11.8, 1.4], header=['Term', 'Plain meaning', 'Session'], size=9)
    save(d, out / 'Glossary of Terms.docx')
    to_pdf(out / 'Glossary of Terms.docx')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    (ROOT / 'Learner Materials').mkdir(exist_ok=True)
    (ROOT / 'Facilitator Materials').mkdir(exist_ok=True)
    if which in ('learner', 'all'):
        learner()
    if which in ('guide', 'all'):
        guide()
    if which in ('script', 'all'):
        script()
