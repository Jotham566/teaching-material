"""Two-page parent outlines (A4 PDF, KLAi brand), one per track.

Run from build/:  python3 build_parent_outlines.py
Output: ../marketing/parent_outlines/KLAi_Camp_Parent_Outline_{ML,DA}.pdf
Facts come from curriculum/, handbook/ASSESSMENT_AND_SHOWCASE.md and programme/PROGRAMME_DECISIONS.md.
Fee, venue and contact are set once in FACTS below.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CAMP = Path(__file__).resolve().parents[1]
FONTS = CAMP / 'brand' / 'fonts'
OUT = CAMP / 'marketing' / 'parent_outlines'
OUT.mkdir(parents=True, exist_ok=True)
for n, f in [('Lato', 'Lato-Regular.ttf'), ('LatoB', 'Lato-Bold.ttf'), ('LatoBlack', 'Lato-Black.ttf'), ('LatoI', 'Lato-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(FONTS / f)))
pdfmetrics.registerFontFamily('Lato', normal='Lato', bold='LatoB', italic='LatoI', boldItalic='LatoB')

INK = HexColor('#111111'); BODY = HexColor('#333333'); MUTE = HexColor('#666666'); HAIR = HexColor('#CFCFCF')
RED = HexColor('#AE2525'); GOLD = HexColor('#E0BE36'); BLACK = HexColor('#000000')
W, H = A4
M = 40
LOGO_BLACK = str(CAMP / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png')

FACTS = {
    'fee': 'UGX 1,000,000 per learner',
    'venue': 'The National ICT Innovation Hub, Nakawa',
    'contact': '+256 750 990 718  |  jothammartin.wambi@gmail.com',
    'tutor': 'Jotham Martin Wambi, data scientist and ML/AI engineer, AI and ML lecturer at IUEA.',
}

COMMON_SESSION = ('Each three-hour class has the same shape. A short recall, then a guess written on paper before anything is run, '
                  'then the code is run and investigated, a 15-minute break away from the screen, a second block, and a make time where each '
                  'learner builds their own version. Every class ends with a sentence the learner writes in their own words.')

TRACKS = {
    'ML': {
        'name': 'Machine Learning',
        'line': 'Learn to teach a computer to make predictions, and to test whether it works.',
        'who': 'S.4 to S.6 students and school leavers. No coding experience is needed. Basic school maths is enough.',
        'tools': 'Python, Jupyter notebooks, NumPy, pandas, matplotlib, seaborn and scikit-learn.',
        'build': ('Each learner builds a prediction project from start to finish. They choose a question, prepare the data, '
                  'set a simple baseline to beat, train a model, and test it once on data it has never seen. '
                  'They present it in a five-minute talk and a short written report.'),
        'leave': ['A working project notebook that can be rerun from the top.',
                  'A report that states what the model can and cannot do.',
                  'A completion certificate, once the requirements below are met.'],
        'weeks': [
            ('1', 'Python and a first prediction', 'A computer guesses a rent from 120 homes. Notebooks, values, arithmetic and reading error messages.'),
            ('2', 'Python you need', 'Decisions, lists, loops and functions. A hand-written rule that names flowers, then a test of how often it is right.'),
            ('3', 'Tables and statistics', 'Tables in pandas, picking and filtering rows, averages and spread, with NumPy.'),
            ('4', 'Clean, chart, question', 'Fixing messy data, drawing charts that say something, choosing a project question. Checkpoint one.'),
            ('5', 'Baselines and a line', 'Why a model must beat a simple guess. Fitting a line and measuring its error.'),
            ('6', 'Trees and fair tests', 'Decision trees, and keeping a test set locked until the end. Checkpoint two.'),
            ('7', 'Your project', 'An approved plan, a baseline and a compared model. Modern AI assistants are shown and critiqued.'),
            ('8', 'Hand over', 'The final test, the report, and each learner demonstrates their work to parents and guardians.'),
        ],
        'extra': 'Four extra two-hour foundation labs in weeks 1 to 4 (a fourth day) give more practice with Python and maths. An optional extension follows week 8 and is not assessed.',
        'hours': '24 classes of 3 hours, plus 4 labs of 2 hours: 80 scheduled hours including breaks.',
        'file': 'KLAi_Camp_Parent_Outline_ML.pdf',
        'data': 'All project data is practice data made for the camp, so no real person\'s information is used.',
    },
    'DA': {
        'name': 'Python for Data Analysis',
        'line': 'Learn to turn a messy table into a clear answer, using the tools data analysts use.',
        'who': 'S.4 to S.6 students and school leavers. No coding, spreadsheet or statistics experience is needed.',
        'tools': 'Python, Jupyter notebooks, NumPy, pandas, matplotlib and seaborn.',
        'build': ('Each learner analyses a set of data and answers one question. They clean it, keep a log of every change, '
                  'summarise it, draw labelled charts, and check their totals two different ways. '
                  'They present it in a five-minute talk and a short written report.'),
        'leave': ['An analysis notebook that can be rerun from the top.',
                  'A cleaning log and a set of labelled charts.',
                  'A completion certificate, once the requirements below are met.'],
        'weeks': [
            ('1', 'Meet the data', 'Open a notebook, read a table of shop sales, store values and read error messages.'),
            ('2', 'Python you need', 'Decisions, lists, loops and functions, with checks that stop the program when something is wrong.'),
            ('3', 'Tables in pandas', 'Select, filter, sort and group a table. Revenue by item and by branch, checked by hand.'),
            ('4', 'Clean and chart', 'Finding and fixing duplicates and gaps, bar, line, histogram and scatter charts. Checkpoint one.'),
            ('5', 'Explore with NumPy and seaborn', 'Spread, typical values, unusual values, and why two things moving together do not prove one causes the other.'),
            ('6', 'Messy data and two tables', 'Clean a raw export, join two tables, and explain any difference in the totals. Checkpoint two.'),
            ('7', 'Show it', 'An approved project plan and a notebook that reruns. Modern AI assistants are shown and critiqued.'),
            ('8', 'Hand over', 'The report, the five-minute talk, and each learner demonstrates their work to parents and guardians.'),
        ],
        'extra': 'The practice data comes from a made-up chain of three shops, Sunrise Shops. Final projects may use public real data once the licence has been read at its source.',
        'hours': '24 classes of 3 hours: 72 scheduled hours including breaks.',
        'file': 'KLAi_Camp_Parent_Outline_DA.pdf',
        'data': 'Practice data is made up for the camp, so no real person\'s information is used.',
    },
}

MARKS = [('Six weekly portfolios', '20%'), ('Checkpoint one, end of week 4', '15%'), ('Checkpoint two, end of week 6', '20%'),
         ('Final project', '30%'), ('Individual demonstration', '15%')]


def P(c, text, x, y, w, size=10.5, color=BODY, font='Lato', lead=None):
    st = ParagraphStyle('p', fontName=font, fontSize=size, leading=lead or size * 1.38, textColor=color)
    p = Paragraph(text, st)
    _, h = p.wrap(w, 2000)
    p.drawOn(c, x, y - h)
    return y - h


def T(c, text, x, y, size=10, color=INK, font='LatoB', align='left'):
    c.setFillColor(color); c.setFont(font, size)
    {'left': c.drawString, 'right': c.drawRightString, 'center': c.drawCentredString}[align](x, y, text)


def head(c, t, page):
    # black band with the logo, on both pages
    c.setFillColor(BLACK); c.rect(0, H - 74, W, 74, fill=1, stroke=0)
    c.drawImage(LOGO_BLACK, M, H - 56, width=74, height=32, mask='auto', preserveAspectRatio=True)
    T(c, 'Holiday Data and AI Camp  |  December 2026', W - M, H - 38, 9.5, white, 'Lato', 'right')
    T(c, f'Parent outline  |  page {page} of 2', W - M, H - 52, 9, HexColor('#9A9A9A'), 'Lato', 'right')


def foot(c, t):
    c.setStrokeColor(HAIR); c.setLineWidth(0.6); c.line(M, 40, W - M, 40)
    T(c, f"{FACTS['venue']}  |  {FACTS['contact']}", M, 27, 8.5, MUTE, 'Lato')


def section(c, label, y):
    y -= 10
    T(c, label, M, y, 12.5, INK, 'LatoB')
    return y - 16


def build(key):
    t = TRACKS[key]
    c = canvas.Canvas(str(OUT / t['file']), pagesize=A4)
    c.setTitle(f"{t['name']}: parent outline"); c.setAuthor('KLAi')
    cw = W - 2 * M

    # ---------------- page 1
    head(c, t, 1)
    y = H - 112
    T(c, t['name'], M, y, 28, INK, 'LatoBlack')
    y = P(c, t['line'], M, y - 12, cw, 13.5, INK, 'LatoB', 18) - 8
    y = P(c, f"<b>Who it is for.</b> {t['who']}", M, y, cw, 10.5) - 4
    y = P(c, f"<b>Tools.</b> {t['tools']} All are free and used in industry.", M, y, cw, 10.5) - 14

    y = section(c, 'What your child will build', y)
    y = P(c, t['build'], M, y, cw, 10.5) - 6
    y = P(c, t['data'], M, y, cw, 10.5) - 14

    y = section(c, 'The eight weeks', y)
    cols = [M, M + 36, M + 190]
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(M, y + 4, W - M, y + 4)
    for wk, name, what in t['weeks']:
        tw = P(c, what, cols[2], y - 2, W - M - cols[2], 9.5, BODY, 'Lato', 12.4)
        rowh = max(y - tw, 18) + 6
        T(c, wk, cols[0] + 2, y - 11, 11, RED, 'LatoB')
        P(c, name, cols[1], y - 2, 148, 10, INK, 'LatoB', 12.4)
        c.setStrokeColor(HAIR); c.setLineWidth(0.6)
        y -= rowh
        c.line(M, y + 3, W - M, y + 3)
    y -= 8
    y = P(c, t['extra'], M, y, cw, 9.5, MUTE, 'LatoI', 13)
    foot(c, t); c.showPage()

    # ---------------- page 2
    head(c, t, 2)
    y = H - 104
    y = section(c, 'What a class looks like', y)
    y = P(c, COMMON_SESSION, M, y, cw, 10.5) - 4
    y = P(c, 'Nobody is expected to know any of this beforehand. Every new word is explained with a picture and an everyday example, and the instructor works with each learner at their own pace.', M, y, cw, 10.5) - 14

    y = section(c, 'How progress is checked', y)
    y = P(c, 'Every mark points to something the learner made. Marks are private, and learners are never ranked in public.', M, y, cw, 10.5) - 6
    rx = M
    for name, pc in MARKS:
        c.setStrokeColor(HAIR); c.setLineWidth(0.6)
        T(c, name, rx, y - 12, 10.5, BODY, 'Lato'); T(c, pc, rx + 300, y - 12, 10.5, INK, 'LatoB', 'right')
        c.line(rx, y - 18, rx + 300, y - 18)
        y -= 21
    # right column beside the marks table: completion rule
    cx = M + 330
    P(c, '<b>To earn the certificate</b><br/>At least 20 of the 24 classes attended or made up.<br/>Both checkpoints, the final project and the demonstration handed in.<br/>An overall mark of at least 50 out of 100.', cx, y + 21 * len(MARKS) - 4, W - M - cx, 10, BODY, 'Lato', 14)
    y -= 12

    y = section(c, 'Using AI tools', y)
    y = P(c, 'In weeks 1 to 6 learners write and fix their own code, so that the foundations are theirs. In weeks 7 and 8 they see how modern AI coding assistants work, and learn to check what such a tool says before trusting it. '
              'The final demonstration is done without AI help, and the certificate shows what the learner can do themselves.', M, y, cw, 10.5) - 14

    y = section(c, 'What we ask of families', y)
    for line in ['Your child brings their own laptop and charger, Windows or Mac. We check it works with a short setup session before day one.',
                 'Learners attend on time and tell us ahead of any absence, so a class can be made up.',
                 'Parents and guardians come to the final demonstration in week 8.',
                 'Photographs and sharing a project publicly are optional, and need a separate written consent.']:
        c.setFillColor(GOLD); c.rect(M, y - 9, 4, 4, fill=1, stroke=0)
        y = P(c, line, M + 14, y, cw - 14, 10.5) - 3
    y -= 10

    # fact panel (hairline box, no fill)
    box_h = 128
    c.setStrokeColor(INK); c.setLineWidth(1.3); c.roundRect(M, y - box_h, cw, box_h, 6, fill=0, stroke=1)
    facts = [('Fee', f"{FACTS['fee']}. The same for a group of one to five."),
             ('Venue', FACTS['venue'] + '.'),
             ('Schedule', 'Three classes a week for eight weeks, starting December 2026. Dates and times are confirmed at enrolment.'),
             ('Time', t['hours']),
             ('Groups', 'No more than five learners in a group, so each one gets personal attention.')]
    fy = y - 16
    for k, v in facts:
        T(c, k, M + 14, fy - 8, 10, RED, 'LatoB')
        fy = P(c, v, M + 84, fy, cw - 98, 10, BODY, 'Lato', 13) - 5
    y -= box_h + 16
    y = P(c, f"<b>Your tutor.</b> {FACTS['tutor']}", M, y, cw, 10) - 3
    y = P(c, 'This is a beginner programme. It builds real skills and a project to show, and is not a professional qualification.', M, y, cw, 9.5, MUTE, 'LatoI', 13)
    foot(c, t)
    if y < 52:
        raise RuntimeError(f'{key}: page 2 overflows ({y:.0f})')
    c.showPage(); c.save()
    print(key, 'page 2 bottom', round(y))


if __name__ == '__main__':
    for k in TRACKS:
        build(k)
