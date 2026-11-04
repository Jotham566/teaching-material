"""One-page Student Roadmap in the KLAi look (A4 landscape): editable PowerPoint and PDF.
    python3 kit/make_roadmap_klai.py
Reads the 24 session titles from content/sNN.py through kit/deck.load, so the roadmap always matches the decks.
Writes: ../../01 Course Overview/Student Roadmap (one page).pptx and .pdf
Design: black header band with the logo and a gold rule, black and white type, red only for project milestones, hairlines, no panels,
no numbered circles, no kicker labels. Every text box is measured with the real Lato files before it is placed."""
import os
import subprocess
import sys
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent.parent
sys.path.insert(0, str(HERE))
import deck  # noqa: E402

OUT = ROOT / '01 Course Overview'
LOGO = BUILD / 'brand' / 'logos' / 'klai_logo_on_black_cropped.png'
FONTS = BUILD / 'brand' / 'fonts'

BLACK, INK, BODY, MUTE, HAIR, RED, GOLD, WHITE = '000000', '111111', '333333', '666666', 'BFBFBF', 'AE2525', 'E0BE36', 'FFFFFF'
FONT = 'Lato'
PW, PH = 11.693, 8.268
MX = 0.5
CW = PW - 2 * MX

# Short lab deliverables. Each is checked below against the 'keep' sentence of the session so that file names match the decks.
DELIVERABLE = {
    1: 'Notebook in Drive and your business question',
    2: 'Workbook dictionary tab: record, key, problems per tab',
    3: 'Workbook: three pivot tables and three charts',
    4: 'Simulation tab: 200 samples of 30 orders',
    5: 'Notebook: price list, one error read and fixed',
    6: 'Notebook: a tested loyalty_tier function',
    7: 'orders_profile.csv: a data profile',
    8: 'orders_clean.csv, cleaning log, reconciliation note',
    9: 'Revenue tables and a join log with row counts',
    10: 'Query book: ten SQL queries with pandas proofs',
    11: 'Notebook: eight charts and three findings',
    12: 'Notebook: the offer test five ways, a decision note',
    13: 'regression_summary.csv and a one-page report',
    14: 'loans_prepared.csv and a three-sentence note',
    15: 'loan_risk_scores.csv and a threshold note in UGX',
    16: 'model_comparison.csv and a note on the leaked column',
    17: 'Model comparison table and a decision memo',
    18: 'customer_segments.csv and unusual orders to review',
    19: 'Baseline, tested forecast, Pipeline, manager note',
    20: 'Notebook, results table and a recommendation',
    21: 'feedback_scored.csv and a three-sentence finding',
    22: 'eval_results.csv and audit_log.csv',
    23: 'Shipping folder: app.py, saved model, model card',
    24: 'Presentation sheet and a six month learning path',
}
MARK = {8: 'Milestone 1', 13: 'Milestone 2', 19: 'Milestone 3', 24: 'Project talk'}
MARK_LONG = {8: 'Project milestone 1', 13: 'Project milestone 2', 19: 'Project milestone 3', 24: 'Course project talk'}

_FONT_CACHE = {}


def _font(size, bold):
    key = (round(size * 10), bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(str(FONTS / ('Lato-Bold.ttf' if bold else 'Lato-Regular.ttf')), 200)
    return _FONT_CACHE[key]


def width_in(text, size, bold=False):
    return _font(size, bold).getlength(text) / 200 * size / 72


def wrap(text, size, w_in, bold=False):
    lines, cur = [], ''
    for word in text.split(' '):
        trial = (cur + ' ' + word).strip()
        if width_in(trial, size, bold) <= w_in or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


prs = Presentation()
prs.slide_width, prs.slide_height = Inches(PW), Inches(PH)
slide = prs.slides.add_slide(prs.slide_layouts[6])
sh = slide.shapes
bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = RGBColor.from_string(WHITE)
LEAD = 1.2


def text(x, y, w, h, runs, size, color=BODY, bold=False, align='l', anchor='t', name=None):
    """runs: a string, or a list of paragraphs, each a list of (text, dict) runs."""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    paras = [[(runs, {})]] if isinstance(runs, str) else runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'r': PP_ALIGN.RIGHT, 'c': PP_ALIGN.CENTER}[align]
        p.line_spacing = 1.0
        for t, o in para:
            r = p.add_run()
            r.text = t
            r.font.name = FONT
            r.font.size = Pt(o.get('size', size))
            r.font.bold = o.get('bold', bold)
            r.font.color.rgb = RGBColor.from_string(o.get('color', color))
        if para and para[0][1].get('after'):
            p.space_after = Pt(para[0][1]['after'])
    return tb


def line(x1, y1, x2, y2, color=HAIR, w=0.5):
    c = sh.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = RGBColor.from_string(color)
    c.line.width = Pt(w)
    st = c._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if st is not None:
        c._element.remove(st)


def rect(x, y, w, h, fill):
    from pptx.enum.shapes import MSO_SHAPE
    r = sh.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    st = r._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if st is not None:
        r._element.remove(st)
    r.fill.solid()
    r.fill.fore_color.rgb = RGBColor.from_string(fill)
    r.line.fill.background()
    return r


def main():
    sess = [deck.load(n) for n in range(1, 25)]
    for s in sess:   # keep file names in the short deliverables honest
        for tok in DELIVERABLE[s['num']].replace(',', ' ').split():
            if '.' in tok.strip('.') and tok.rsplit('.', 1)[-1] in ('csv', 'py'):
                assert tok in (s['keep'] + s['keep_title'] + s['keep_note']).replace(' dot ', '.') or tok in str(s['slides']), (s['num'], tok)

    # ---- header band
    rect(0, 0, PW, 0.72, BLACK)
    lh = 0.42
    lw = lh * 2310 / 736
    slide.shapes.add_picture(str(LOGO), Inches(MX), Inches((0.72 - lh) / 2), height=Inches(lh))
    text(MX + lw + 0.3, 0.0, 6.2, 0.72, 'AI and Data Science Professional', 22, WHITE, True, anchor='m', name='Title')
    text(PW - MX - 3.6, 0.0, 3.6, 0.72, '24 sessions of 2 hours  |  48 hours  |  free tools only', 10, WHITE, False, 'r', 'm')
    rect(0, 0.72, PW, 0.04, GOLD)

    lead = ('You arrive confident in Excel, with no code and no statistics. You leave able to take a business question from raw data to a tested model '
            'or analysis, explain it to a manager, and run it as a small app. Each session is concepts first, with laptops closed, then a lab where you work.')
    ll = wrap(lead, 10, CW)
    text(MX, 0.88, CW, 0.5, lead, 10, BODY, name='Lead')
    y = 0.88 + len(ll) * 10 * LEAD / 72 + 0.1

    # ---- table
    cx = [MX, MX + 1.55, MX + 1.9, MX + 1.9 + 4.95, PW - MX - 0.82]   # module, number, title, deliverable, mark
    wmod, wnum, wtit, wdel = 1.5, 0.3, 4.85, 2.95
    wmark = PW - MX - cx[4]
    TS, DS = 9.0, 8.5
    line(MX, y, PW - MX, y, BLACK, 1.0)
    text(cx[0], y + 0.04, wmod, 0.2, 'Module', 8.5, MUTE)
    text(cx[2], y + 0.04, wtit, 0.2, 'Session title', 8.5, MUTE)
    text(cx[3], y + 0.04, wdel, 0.2, 'What you keep from the lab', 8.5, MUTE)
    y += 0.24
    line(MX, y, PW - MX, y, HAIR, 0.5)
    modules = []
    for s in sess:
        name = s['block']
        if not modules or modules[-1][0] != name:
            modules.append((name, []))
        modules[-1][1].append(s)
    for mi, (block, members) in enumerate(modules):
        y0 = y
        for s in members:
            n = s['num']
            tl = wrap(s['title'], TS, wtit, True)
            dl = wrap(DELIVERABLE[n], DS, wdel)
            lines_h = max(len(tl) * TS, len(dl) * DS) * LEAD / 72
            rh = lines_h + 0.055
            red = n in MARK
            text(cx[1], y + 0.025, wnum, rh, str(n), TS, RED if red else INK, True, 'l')
            text(cx[2], y + 0.025, wtit, rh, s['title'], TS, INK, True)
            text(cx[3], y + 0.025, wdel, rh, DELIVERABLE[n], DS, BODY)
            if red:
                text(cx[4], y + 0.025, wmark, rh, MARK[n], DS, RED, True)
            y += rh
        letter, nm = block.replace('Module ', '').split(': ', 1)
        nums = f'Sessions {members[0]["num"]} to {members[-1]["num"]}'
        text(cx[0], y0 + 0.025, wmod, y - y0, [[(f'{letter}  {nm}', {'bold': True, 'color': INK, 'size': 9.5, 'after': 1})], [(nums, {'color': MUTE, 'size': 8.5})]], 9.5)
        line(MX, y, PW - MX, y, BLACK if mi == len(modules) - 1 else HAIR, 1.0 if mi == len(modules) - 1 else 0.5)

    # ---- bottom strip
    y += 0.12
    colw = (CW - 2 * 0.35) / 3
    xs = [MX + i * (colw + 0.35) for i in range(3)]
    blocks = [
        ('Every session', ['10 min recall and the question of the day', '45 min concepts, laptops closed', '10 min break',
                           '45 min lab: predict, run, read, change', '10 min exit check, keep and next']),
        ('Free tools, nothing to buy', ['Google Colab and Google Sheets (or Excel)', 'Python: pandas, NumPy, scikit-learn, matplotlib',
                                        'SciPy, statsmodels, seaborn, SQLite', 'GitHub, Streamlit Community Cloud', 'TensorFlow Playground, sentence-transformers']),
        ('At the end you can', ['Clean a raw export and prove its total', 'Query a database with SQL and test a difference',
                                'Build and judge a model against a baseline', 'Publish a small app and present to a manager']),
    ]
    heights = []
    for (head, items), x in zip(blocks, xs):
        hh = 0.2
        for it in items:
            hh += len(wrap(it, 8.5, colw - 0.14)) * 8.5 * LEAD / 72 + 0.025
        heights.append(hh)
    bh = max(heights)
    for (head, items), x in zip(blocks, xs):
        text(x, y, colw, 0.2, head, 9.5, INK, True)
        yy = y + 0.2
        for it in items:
            k = len(wrap(it, 8.5, colw - 0.14))
            text(x, yy, 0.12, 0.15, '-', 8.5, MUTE)
            text(x + 0.14, yy, colw - 0.14, k * 8.5 * LEAD / 72, it, 8.5, BODY)
            yy += k * 8.5 * LEAD / 72 + 0.025
    y += bh + 0.05
    cap = 'Question in 13, dataset in 14, tested model in 19, app in 23, talk in 24. No exams or marks. Finishing it earns a KLAi certificate of completion.'
    text(MX, y, CW, 0.2, [[('Course project. ', {'bold': True, 'color': INK}), (cap, {})]], 8.5, BODY)
    y += 0.17
    foot_y = PH - 0.3
    line(MX, foot_y - 0.06, PW - MX, foot_y - 0.06, HAIR, 0.5)
    text(MX, foot_y, CW, 0.2, 'KLAi Professional Learning  |  Tutor: Jotham Martin Wambi  |  Windows or Mac, in a browser  |  All course data is fictional', 8.5, MUTE)
    print('content ends at', round(y, 2), 'of', PH, 'footer at', round(foot_y, 2))
    assert y < foot_y - 0.06, 'roadmap content overflows the page'

    OUT.mkdir(exist_ok=True)
    pp = OUT / 'Student Roadmap (one page).pptx'
    prs.core_properties.title = 'AI and Data Science Professional: Student Roadmap'
    prs.core_properties.author = 'KLAi Professional Learning'
    prs.save(str(pp))
    subprocess.run(['soffice', f'-env:UserInstallation=file:///tmp/lo_roadmap{os.getpid()}', '--headless', '--convert-to', 'pdf', '--outdir', str(OUT), str(pp)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
    print('wrote', pp.name, 'and PDF')


if __name__ == '__main__':
    main()
