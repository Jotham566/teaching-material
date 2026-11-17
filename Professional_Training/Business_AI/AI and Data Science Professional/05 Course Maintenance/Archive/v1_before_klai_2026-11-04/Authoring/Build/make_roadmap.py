"""One-page student roadmap (A4 landscape): editable PowerPoint and PDF.   python3 make_roadmap.py

Design: type and hairlines, one ink colour, one accent. The sessions are stations on a line; the three checkpoint sessions
carry the accent. No fills, no cards, no icons. Every size is a multiple of 0.5 and comes from the scale T below.
"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import deckkit as dk
ROOT = HERE.parents[2]
OUT = ROOT / '01 Course Overview'; OUT.mkdir(exist_ok=True)

INK, BODY, SOFT, RULE, ACCENT, WHITE = '1F2328', '3B4046', '6A6F75', 'C9C5BC', 'B04A2B', 'FFFFFF'
SERIF, SANS = 'Cambria', 'Calibri'
T = dict(display=30.0, row=16.5, lead=14.0, body=12.5, small=11.0, dot=10.5)
PW, PH = 11.693, 8.268; MX = 0.6

prs = Presentation(); prs.slide_width = Inches(PW); prs.slide_height = Inches(PH)
s = prs.slides.add_slide(prs.slide_layouts[6]); sh = s.shapes
bg = s.background.fill; bg.solid(); bg.fore_color.rgb = RGBColor.from_string(WHITE)

def text(x, y, w, h, t, size, face=SANS, color=BODY, bold=False, align='l', anchor='t', italic=False, name=None):
    tb, sz = dk.add_text(sh, x, y, w, h, t, size, bold, color, face, align, anchor, min_size=size, italic=italic, name=name)
    return tb
def line(x1, y1, x2, y2, color=RULE, w=0.75):
    c = sh.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = RGBColor.from_string(color); c.line.width = Pt(w)
    st = c._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if st is not None: c._element.remove(st)
    return c
def dot(cx, cy, d, label, filled):
    o = sh.add_shape(MSO_SHAPE.OVAL, Inches(cx - d / 2), Inches(cy - d / 2), Inches(d), Inches(d))
    st = o._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if st is not None: o._element.remove(st)
    o.fill.solid(); o.fill.fore_color.rgb = RGBColor.from_string(ACCENT if filled else WHITE)
    o.line.color.rgb = RGBColor.from_string(ACCENT if filled else INK); o.line.width = Pt(1.25)
    tf = o.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = str(label)
    r.font.name = SANS; r.font.size = Pt(T['dot']); r.font.bold = True; r.font.color.rgb = RGBColor.from_string(WHITE if filled else INK)

# ---- header
text(MX, 0.42, 8.0, 0.62, 'AI and Data Science Professional', T['display'], SERIF, INK, True, name='Title')
text(MX, 1.06, 7.6, 0.62, 'Twenty-four sessions of two hours. You arrive knowing Excel, and you leave with a model you built, tested and put online.', T['lead'], SANS, BODY)
text(8.55, 0.5, PW - MX - 8.55, 1.15, [[('Bring', {'bold': True, 'color': INK})], [('A laptop with a browser, a free Google account, and one question from your own work that you would like data to answer.', {})]], T['body'], SANS, BODY)
line(MX, 1.68, PW - MX, 1.68, INK, 1.25)

# ---- column heads
cols = [MX, 3.5, 7.3, 9.5]; widths = [2.8, 3.65, 1.95, PW - MX - 9.5]
for x, w, h in zip(cols, widths, ['Module and sessions', 'What you do', 'Tools', 'What you make']):
    text(x, 1.76, w, 0.26, h, T['small'], SANS, SOFT)
line(MX, 2.04, PW - MX, 2.04, RULE, 0.75)

rows = [
 ('Think with data', range(1, 5), 'Read a table by its grain and keys. Chart data without misleading anyone. Simulate to see how far a sample can be trusted.', 'Google Sheets', 'A pivot table and two clear charts'),
 ('Python for data', range(5, 10), 'Write your first Python beside the spreadsheet formula it replaces. Load, filter and clean a messy export. Group and join tables.', 'Google Colab, pandas', 'A cleaned file that reconciles to a known total'),
 ('Analyse and explain', range(10, 14), 'Query a database with SQL. Explore a new dataset in one sitting. Test whether a difference is real and fit a regression line.', 'SQLite, matplotlib, statsmodels', 'A one-page analysis report'),
 ('Machine learning', range(14, 20), 'Split data, fit a model and beat a baseline. Judge it with a confusion matrix and catch leakage. Segment customers, forecast visits.', 'scikit-learn', 'A tested model with its baseline'),
 ('Neural networks and text', range(20, 23), 'Watch a neural network learn in your browser. Turn text into numbers and search by meaning. Test a document search.', 'TensorFlow Playground, sentence-transformers', 'A test sheet that scores the search'),
 ('Ship it and present', range(23, 25), 'Save a model and publish a small app. Check it for fairness and data protection. Present your capstone in ten minutes.', 'GitHub, Streamlit', 'Your app and a ten-minute talk'),
]
CHECK = {8, 13, 19}
y = 2.12; rh = 0.8
for i, (name, rng, what, tools, make) in enumerate(rows):
    text(cols[0], y + 0.04, widths[0], 0.32, name, T['row'], SERIF, INK, True, name=f'Module {i+1}')
    nums = list(rng); d = 0.3; step = 0.4; cy = y + 0.56
    line(cols[0] + d / 2, cy, cols[0] + d / 2 + step * (len(nums) - 1), cy, INK, 1.0)
    for k, n in enumerate(nums): dot(cols[0] + d / 2 + k * step, cy, d, n, n in CHECK)
    text(cols[1], y + 0.05, widths[1], rh - 0.1, what, T['body'], SANS, BODY)
    text(cols[2], y + 0.05, widths[2], rh - 0.1, tools, T['body'], SANS, BODY)
    text(cols[3], y + 0.05, widths[3], rh - 0.1, make, T['body'], SANS, BODY)
    y += rh
    line(MX, y, PW - MX, y, RULE, 0.5 if i < len(rows) - 1 else 1.25) if i < len(rows) - 1 else line(MX, y, PW - MX, y, INK, 1.25)

# ---- below the table
y += 0.1
dot(MX + 0.11, y + 0.13, 0.22, '', True)
text(MX + 0.32, y, 4.6, 0.28, 'Checkpoint sessions: 8, 13 and 19', T['small'], SANS, BODY)
text(MX, y + 0.3, 5.2, 0.5, [[('Capstone. ', {'bold': True, 'color': INK}), ('Question in session 13, dataset in 14, tested model in 19, app in 23, ten-minute talk in 24.', {})]], T['body'], SANS, BODY)
text(6.0, y, PW - MX - 6.0, 0.5, [[('Every session. ', {'bold': True, 'color': INK}), ('Recall 10 minutes, learn 30, see it done live 25, break 5, lab 40, check 10.', {})]], T['body'], SANS, BODY)
text(6.0, y + 0.58, PW - MX - 6.0, 0.5, [[('Everything is free. ', {'bold': True, 'color': INK}), ('No paid tool, key or graphics card. Windows or Mac, in a browser. All course data is fictional.', {})]], T['body'], SANS, BODY)
text(MX, PH - 0.33, 8, 0.26, 'KLAi Professional Learning. Tutor: Jotham Martin Wambi.', T['small'], SANS, SOFT)

pp = OUT / 'Student Roadmap (one page).pptx'; prs.save(str(pp))
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(OUT), str(pp)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=200)
print('written', pp.name)
