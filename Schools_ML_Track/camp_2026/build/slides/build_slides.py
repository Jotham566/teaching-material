"""Build the camp slide decks (one PPTX per session, per lab and for the extension).

    python Schools_ML_Track/camp_2026/build/slides/build_slides.py [DA09 ML01 F02 ...] [--spec-only]

For each session this script assembles a spec of slides from the lesson file (the automatic slides: title, question,
plan, words, predict, run, investigate, modify, break, make, errors, exit) and the authored concept slides and
illustrations (concepts_da.py, concepts_ml.py, figs_*.py), writes the spec as JSON and calls render_deck.js.

Slide order for a session with two blocks:
  title, question, plan, words, concept slides (at=0), Block A (predict, run, investigate, modify), break,
  concept slides (at=1), Block B (predict, run, investigate, modify), concept slides (at=2), make, errors, exit.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD))

import brand as B
import slidekit as K
import figkit
import notes_auto as N
from common import ROOT, TRACK_NAMES, DEFAULT_CLOCK, DATA_DA, DATA_ML
from content import ML, DA, LABS, EXTENSION

PPTX_SKILL_SCRIPTS = os.environ.get('PPTX_SKILL_SCRIPTS', '/sessions/focused-youthful-einstein/mnt/.claude/skills/pptx/scripts')
SPEC_DIR = HERE / '_specs'
OUT_DIR = ROOT / 'slides'
AUTO = B.FIG_DIR / 'auto'
VENUE = 'The National ICT Innovation Hub, Nakawa'
WEEK_THEMES = {
    'DA': ['Meet the data', 'Python you need', 'Tables in pandas', 'Clean and chart', 'Explore with NumPy and seaborn', 'Messy data and two tables', 'Show it', 'Hand over'],
    'ML': ['Python and a first prediction', 'Python you need', 'Tables and statistics', 'Clean, chart, question', 'Baselines and a line', 'Trees and fair tests', 'Your project', 'Hand over'],
}
try:
    import figs_common  # noqa: F401
except ImportError:
    pass
for _m in ('figs_da', 'figs_da_r1', 'figs_da_r2', 'figs_ml', 'figs_ml_r3', 'figs_ml_r4', 'figs_example'):  # figs_common is imported above
    try:
        __import__(_m)
    except ImportError:
        pass
def _load(prefix):
    merged = {}
    for suffix in ('1', '2', '3'):
        try:
            m = __import__(f'concepts_{prefix}_{suffix}')
            merged.update(m.CONCEPTS)
        except ImportError:
            pass
    return merged


CONCEPTS_DA = _load('da')
CONCEPTS_ML = _load('ml')

LOGO = {'on_white': str(B.LOGO_ON_WHITE), 'on_black': str(B.LOGO_ON_BLACK)}


def _logo_dims():
    from PIL import Image
    with Image.open(B.LOGO_ON_WHITE) as im:
        ar = im.width / im.height
    return {'on_white': str(B.LOGO_ON_WHITE), 'on_black': str(B.LOGO_ON_BLACK), 'h_small': 0.27, 'w_small': round(0.27 * ar, 3), 'h_large': 0.62,
            'w_large': round(0.62 * ar, 3)}


# ---------------------------------------------------------------- automatic figures
def auto_fig(name, w, h, draw):
    path = AUTO / f'{name}_{w:.2f}x{h:.2f}.png'
    if not path.exists():
        s = figkit.Scene(w, h)
        draw(s)
        s.save(path)
    return path


def fig_paper_pen(w=2.6, h=2.6):
    def d(s):
        s.icon('notebook', w * 0.42, h * 0.5, 1.9)
        s.icon('pen', w * 0.8, h * 0.42, 1.5)
        s.text(w * 0.45, h * 0.52, '?', size=46, weight='bold', color=figkit.RED)
    return auto_fig('paper_pen', w, h, d)


def fig_save(w=2.6, h=2.6):
    def d(s):
        s.icon('notebook', w * 0.45, h * 0.5, 1.9)
        s.icon('check', w * 0.72, h * 0.28, 1.0)
    return auto_fig('save_check', w, h, d)


def fig_icon(name, w, h, scale=1.6):
    return auto_fig('icon_' + name, w, h, lambda s: s.icon(name, w / 2, h / 2, scale))


def fig_clock_dark(w=2.4, h=2.4):
    def d(s):
        s.ax.add_patch(figkit.Rectangle((0, 0), w, h, fc='#000000', ec='none', zorder=0))
        s.circle(w / 2, h / 2, 0.85, fill='#000000', edge='#FFFFFF', lw=4)
        s.line(w / 2, h / 2, w / 2, h / 2 + 0.55, color='#FFFFFF', lw=5, z=4)
        s.line(w / 2, h / 2, w / 2 + 0.38, h / 2, color=figkit.GOLD, lw=5, z=4)
    p = AUTO / f'clock_dark_{w:.2f}x{h:.2f}.png'
    if not p.exists():
        s = figkit.Scene(w, h)
        d(s)
        s.f.savefig(p, dpi=figkit.DPI, facecolor='#000000')
        figkit.plt.close(s.f)
    return p


FRIENDLY = {'Recall: retrieve yesterday, three questions on paper': 'Recall: three questions on paper',
            'Block A: predict, run, investigate, modify': 'First idea: predict, run, investigate, modify',
            'Break away from screens': 'Break away from screens',
            'Block B: predict, run, investigate, modify': 'Second idea: predict, run, investigate, modify',
            'Make: the independent task and the project journal': 'Make: your own task and project journal',
            'Exit ticket, save, and an individual check with each learner': 'Exit ticket, save, and a check with each of you'}
PLAN_CAPTION = {}
for _i in ('12', '18'):
    for _t in ('DA', 'ML'):
        PLAN_CAPTION[_t + _i] = 'Today is your own work. I visit each of you and answer questions on the brief.'
for _i in ('19', '20', '21', '22'):
    for _t in ('DA', 'ML'):
        PLAN_CAPTION[_t + _i] = 'Most of the time is your own build, with a check and a partner.'
for _t in ('DA', 'ML'):
    PLAN_CAPTION[_t + '23'] = 'You build five slides, then rehearse in turn with a timer.'
    PLAN_CAPTION[_t + '24'] = 'Your families come to see what you built. You show it and answer questions.'


def parse_clock(l):
    if l.get('pacing'):
        import re
        out = []
        for part in [x.strip() for x in l['pacing'].split(';') if x.strip()]:
            m = re.match(r'(\d+)\s*minutes?\s*(.*)', part)
            lab = m.group(2).strip()
            out.append((lab[:1].upper() + lab[1:], int(m.group(1))))
        return out
    return [(lab, m) for lab, m in DEFAULT_CLOCK]


def plan_label(label):
    return FRIENDLY.get(label, label)


def fig_plan(ident, parts, w=11.9, h=4.55):
    """The session as rows: start time, a bar as long as the minutes, and the full name of the part."""
    path = AUTO / f'plan2_{ident}_{w:.2f}x{h:.2f}.png'
    if path.exists():
        return path
    s = figkit.Scene(w, h)
    n = len(parts)
    row_h = h / n
    maxm = max(m for _, m in parts)
    bar_x, bar_w = 1.1, 2.6
    t = 0
    for i, (label, m) in enumerate(parts):
        y = h - (i + 1) * row_h
        cy = y + row_h / 2
        sl = label.lower()
        is_break = 'break' in sl
        is_make = sl.startswith('make') or 'your own' in sl or ('build' in sl and 'idea' not in sl and 'block' not in sl)
        is_idea = 'idea' in sl or 'block' in sl or 'teach' in sl or 'work' in sl
        fill = '#FFFFFF' if is_break else (figkit.GOLD if is_make else ('#111111' if is_idea else '#FFFFFF'))
        col = '#FFFFFF' if fill == '#111111' else '#111111'
        s.text(bar_x - 0.15, cy, f'{t // 60}:{t % 60:02d}', size=18, color='#666666', ha='right')
        bw = max(0.55, bar_w * m / maxm)
        s.box(bar_x, cy - row_h * 0.3, bw, row_h * 0.6, f'{m}', size=20, fill=fill, edge='#111111', lw=1.6, r=0.03, color=col, weight='bold')
        txt = plan_label(label)
        tx = bar_x + bar_w + 0.35
        avail = w - tx - 0.1
        size = 20
        lines = K.wrap(txt, size, 'regular', avail)
        if len(lines) > 2 or len(lines) * size * 1.2 / 72 > row_h * 0.95:
            size = 17
            lines = K.wrap(txt, size, 'regular', avail)
        s.text(tx, cy, '\n'.join(lines), size=size, color='#222222', ha='left')
        t += m
    s.text(bar_x + bar_w / 2, 0.0, '', size=1)
    s.save(path)
    return path


# ---------------------------------------------------------------- capture program output and charts
def capture_block(track, ident, l, bi):
    cache = AUTO / f'{ident}_b{bi}_v3.json'
    if cache.exists():
        return json.loads(cache.read_text())
    blocks = l['blocks']
    if not blocks[bi].get('code'):
        return {'ok': False}
    files = DATA_DA if track == 'DA' else DATA_ML
    tmp = tempfile.mkdtemp()
    for f in files:
        src = ROOT / 'student_materials' / track / f
        if src.exists():
            shutil.copy2(src, tmp)
    prev = os.getcwd()
    os.chdir(tmp)
    import matplotlib.pyplot as plt
    charts = []
    counter = [0]

    def _show(*a, **k):
        for num in list(plt.get_fignums()):
            counter[0] += 1
            p = AUTO / f'{ident}_b{bi}_{counter[0]}.png'
            figkit.save_chart(plt.figure(num), p)
            charts.append(str(p))

    ns = {'__name__': '__main__'}
    try:
        orig_show = plt.show
        plt.show = lambda *a, **k: None
        for j in range(bi):
            if blocks[j].get('code'):
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(blocks[j]['code'], f'{ident}:b{j}', 'exec'), ns)
                plt.close('all')
        plt.show = _show
        out = io.StringIO()
        figkit.use_style()
        try:
            import seaborn as _sns
            if not getattr(_sns.heatmap, '_klai', False):
                _orig = _sns.heatmap
                def _heat(*a, **k):
                    k.setdefault('cmap', 'Greys')
                    return _orig(*a, **k)
                _heat._klai = True
                _sns.heatmap = _heat
        except ImportError:
            pass
        with contextlib.redirect_stdout(out):
            exec(compile(blocks[bi]['code'], f'{ident}:b{bi}', 'exec'), ns)
        plt.show = orig_show
        plt.close('all')
        res = {'ok': True, 'stdout': out.getvalue().rstrip('\n').split('\n') if out.getvalue().strip() else [], 'charts': charts}
        AUTO.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(res))
        return res
    except Exception:
        return {'ok': False}
    finally:
        os.chdir(prev)
        plt.close('all')
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- slide builders
class Deck:
    def __init__(self, ident, track, kind, title, objective, question, footer):
        self.ident, self.track, self.kind = ident, track, kind
        self.title, self.objective, self.question, self.footer = title, objective, question, footer
        self.slides = []
        self.section = 'Opening'
        self.seed = sum(ord(c) for c in ident)

    def add(self, layout='light', title=None, objects=None, notes='', section=None):
        self.slides.append({'layout': layout, 'section': section or self.section, 'title': K.title_obj(title) if title and layout == 'light' else None,
                            'title_raw': title if layout == 'dark' else None, 'objects': objects or [], 'notes': notes})


def fig_path(spec, w, h):
    if isinstance(spec, (list, tuple)):
        return figkit.render_figure(spec[0], w, h, spec[1] if len(spec) > 1 else None)
    return figkit.render_figure(spec, w, h)


def add_title(d, l, num, lesson_title, week):
    ts, tlines = K.fit_lines(lesson_title, 'bold', 11.6, 2.5, 56, 34, lead=1.1)
    qy = 2.3 + len(tlines) * ts * 1.1 / 72 + 0.55
    q, _ = K.fitted_text(0.7, qy, 11.2, 1.3, d.question, kind='italic', size_max=30, size_min=22, color=B.GOLD, italic=True)
    info = f'{TRACK_NAMES[d.track] if d.track in TRACK_NAMES else "Machine Learning"}  |  {d.sub}'
    sub = K.text_obj(0.7, 6.55, 11.8, 0.5, text=f'{info}\nHoliday Data and AI Camp  |  {VENUE}', size=16, color='B5B5B5', lead=1.45)
    s, lines = K.fit_lines(lesson_title, 'bold', 11.6, 2.5, 56, 34, lead=1.1)
    sl = {'layout': 'dark', 'section': 'Opening', 'title': {'text': lesson_title, 'size': s, 'lead': round(s * 1.1, 1)}, 'objects': [q, sub],
          'notes': N.title_note(d.ident, lesson_title, d.objective, d.question, d.seed)}
    d.slides.append(sl)


def add_question(d, concepts):
    w, h = 11.9, 4.75
    objs = []
    spec = concepts.get('question')
    if spec:
        objs.append(K.image_obj(fig_path(spec['fig'], w, h), 0.7, 1.85, w, h, alt=spec.get('alt', d.question)))
    notes = N.question_note(d.question, d.seed)
    if spec and spec.get('say'):
        notes = spec['say']
    d.add('light', d.question, objs, notes)


def add_plan(d, l):
    parts = parse_clock(l)
    n = len(parts)
    p = fig_plan(d.ident, parts, 11.9, min(4.55, 0.72 * n + 0.2))
    objs = [K.image_obj(p, 0.7, 1.75, 11.9, min(4.55, 0.72 * n + 0.2), alt='The plan for the session: start time, minutes and what we do')]
    if l['mode'] == 'python':
        cap, title = 'Most of our time is spent doing, in small steps, with a guess before every run.', 'Three hours, mostly doing'
    else:
        cap, title = PLAN_CAPTION.get(d.ident, 'The numbers in the bars are minutes.'), "Today's plan in minutes"
    objs.append(K.text_obj(0.7, 6.4, 11.9, 0.5, text=cap, size=22, color=B.BODY))
    d.add('light', title, objs, N.plan_note(parts, d.seed, l['mode'], cap))


def add_words(d, l, concepts):
    words = l['words']
    if not words:
        return
    icons = concepts.get('word_icons', {})
    n = len(words)
    pages = [words] if n <= 3 else [words[:(n + 1) // 2], words[(n + 1) // 2:]]
    for pi, grp in enumerate(pages):
        objs = []
        row_h = 1.62 if len(grp) == 3 else 1.9
        y = 1.85
        any_icon = any(icons.get(t[0]) for t in grp)
        for i, (term, plain, like) in enumerate(grp):
            yy = y + i * row_h
            icon = icons.get(term)
            tx = 0.7
            if any_icon:
                if icon:
                    ip = fig_icon(icon, 1.3, 1.3, 1.0) if isinstance(icon, str) else fig_path(icon, 1.3, 1.3)
                    objs.append(K.image_obj(ip, 0.7, yy + 0.1, 1.3, 1.3, alt=term))
                tx = 2.2
            tsize = int(min(34, max(24, 34 - max(0, len(term) - 10) * 1.2)))
            objs.append(K.text_obj(tx, yy + 0.05, 3.2, row_h - 0.2, text=term, size=tsize, bold=True, valign='middle'))
            bx = tx + 3.4
            body_w = 12.6 - bx
            po, ps = K.fitted_text(bx, yy + 0.1, body_w, 0.95, plain, size_max=22, size_min=18, lead=1.2)
            nl = len(K.wrap(plain, ps, 'regular', body_w))
            ph = nl * ps * 1.2 / 72
            objs.append(po)
            lo, _ = K.fitted_text(bx, yy + 0.1 + ph + 0.1, body_w, 0.62, like, kind='italic', size_max=19, size_min=16, color=B.MUTE, italic=True)
            objs.append(lo)
            if i < len(grp) - 1:
                objs.append(K.line_obj(0.7, yy + row_h - 0.04, 12.6, yy + row_h - 0.04))
        title = 'Words for today' if len(pages) == 1 else f'Words for today ({pi + 1} of {len(pages)})'
        d.add('light', title, objs, N.words_note(grp, pi, len(pages), d.seed))


def add_concepts(d, concepts, at):
    for c in concepts.get('slides', []):
        if c.get('at', 0) != at:
            continue
        kind = c.get('kind', 'concept')
        objs = []
        if kind == 'concept':
            fw, fh = 7.7, 4.95
            objs.append(K.image_obj(fig_path(c['fig'], fw, fh), 0.7, 1.75, fw, fh, alt=c.get('alt', c['title'])))
            pts = c.get('points', [])
            if pts:
                o, _ = K.fitted_paras(8.7, 1.95, 3.9, 4.7, pts, size_max=24, size_min=19, lead=1.2, gap=0.28)
                objs.append(o)
        elif kind == 'wide':
            fw, fh = 11.9, 4.45
            objs.append(K.image_obj(fig_path(c['fig'], fw, fh), 0.7, 1.7, fw, fh, alt=c.get('alt', c['title'])))
            pts = c.get('points', [])
            if pts:
                o, _ = K.fitted_text(0.7, 6.2, 11.9, 0.7, ' '.join(pts), size_max=22, size_min=18, color=B.BODY)
                objs.append(o)
        elif kind == 'pair':
            fw, fh = 5.85, 3.75
            for i, f in enumerate(c['figs']):
                x = 0.7 + i * 6.05
                objs.append(K.image_obj(fig_path(f, fw, fh), x, 1.7, fw, fh, alt=c['captions'][i]))
                o, _ = K.fitted_paras(x, 5.55, fw, 1.3, [c['captions'][i]], size_max=22, size_min=18, lead=1.2)
                objs.append(o)
        d.add('light', c['title'], objs, c['say'], section=c.get('section'))


CODE_SMALL = []     # (deck, slide, size): code panels below 16 pt because a lesson line is long


def pick_sentences(text, max_words=46):
    import re
    sents = [x for x in re.split(r'(?<=[.!?])\s+', text.strip()) if x]
    out, n = [], 0
    for x in sents:
        w = len(x.split())
        if out and n + w > max_words:
            break
        out.append(x)
        n += w
    return out


def split_code(code):
    """Split long code into two parts at a top-level line near the middle; None if it cannot be split sensibly."""
    lines = code.splitlines()
    if len(lines) < 8:
        return None
    mid = len(lines) // 2
    cands = [i for i in range(3, len(lines) - 2) if lines[i] and not lines[i][0].isspace() and lines[i][0] not in ')]}' and not lines[i - 1].rstrip().endswith(('\\', ',', '(', '[', '{'))]
    if not cands:
        return None
    after_show = [c for c in cands if lines[c - 1].startswith('plt.show')]
    i = min(after_show or cands, key=lambda c: abs(c - mid))
    return '\n'.join(lines[:i]), '\n'.join(lines[i:])


def add_block(d, l, bi, letter, concepts):
    blk = l['blocks'][bi]
    idea = blk['idea']
    d.section = f'Block {letter}'
    seed = d.seed + bi * 7
    run_code = blk.get('code')
    code = run_code or blk.get('display_code')
    # ---- predict
    objs = []
    prompt = blk['predict']
    placed = False
    if code:
        try:
            o, s, ph = K.code_panel(code, 0.7, 1.8, 6.6, 4.9, size_max=22, size_min=16)
            objs += o
            placed = True
            tx, tw = 7.7, 4.9
        except K.FitError:
            try:
                o, s, ph = K.code_panel(K.wrap_code(code, 62), 0.7, 1.8, 11.9, 3.7, size_max=22, size_min=16)
                objs += o
                placed = 'wide'
            except K.FitError:
                try:
                    o, s, ph = K.code_panel(K.wrap_code(code, 50), 0.7, 1.8, 7.9, 4.95, size_max=18, size_min=16)
                    objs += o
                    placed = True
                    tx, tw = 8.9, 3.7
                except K.FitError:
                    pass
            if placed is False:
                halves = split_code(code)
                parts = []
                try:
                    for k, hc in enumerate(halves or ()):
                        o2, s2, ph2 = K.code_panel(K.wrap_code(hc, 78), 0.7, 1.8, 11.9, 3.5, size_max=22, size_min=16)
                        parts.append((o2, ph2))
                except K.FitError:
                    parts = []
                if halves and len(parts) == 2:
                    placed = 'split'
                else:
                    try:
                        o, s, ph = K.code_panel(K.wrap_code(code, 70), 0.7, 1.8, 11.9, 3.7, size_max=16, size_min=12)
                        objs += o
                        placed = 'wide'
                        CODE_SMALL.append((d.ident, f'Predict block {letter}', s))
                    except K.FitError:
                        placed = False
    if placed == 'split':
        for k, (o2, ph2) in enumerate(parts):
            ob = list(o2)
            bottom = 1.8 + ph2 + 0.2
            if k == 0:
                msg = [f'Read the first part of the code. {len(halves[0].splitlines())} lines. Say what each one does.', 'The second part comes next.']
            else:
                msg = [prompt, 'Write your guess on paper before we run it.']
            po, _ = K.fitted_paras(0.7, bottom, 8.8, 6.85 - bottom, msg, size_max=24, size_min=19, lead=1.2, gap=0.14)
            ob.append(po)
            ob.append(K.image_obj(fig_paper_pen(1.5, 1.3), 11.1, max(bottom, 5.45), 1.5, 1.3, alt='A page and a pen'))
            d.add('light', f'Predict: {idea} ({k + 1} of 2)', ob, N.predict_note(blk['intro'], prompt, seed) if k == 1 else
                  f'Read this first part of the code with me before we run anything. {pick_sentences(blk["intro"])}', section=f'Block {letter}')
        placed = 'done'
    if placed == 'done':
        pass
    elif placed is True:
        po, _ = K.fitted_paras(tx, 1.9, tw, 2.8, [prompt, 'Write your guess on paper before we run it.'], size_max=30, size_min=18, lead=1.2, gap=0.3)
        objs.append(po)
        objs.append(K.image_obj(fig_paper_pen(2.4, 2.1), tx + 0.9, 4.75, 2.4, 2.0, alt='A page and a pen: write your guess first'))
    elif placed == 'wide':
        ph_bottom = 1.8 + ph + 0.2
        po, _ = K.fitted_paras(0.7, ph_bottom, 8.8, 6.85 - ph_bottom, [prompt, 'Write your guess on paper before we run it.'], size_max=26, size_min=19, lead=1.2, gap=0.14)
        objs.append(po)
        objs.append(K.image_obj(fig_paper_pen(1.3, 1.15), 11.2, min(max(ph_bottom, 5.5), 5.7), 1.3, 1.15, alt='A page and a pen'))
    else:
        po, _ = K.fitted_paras(0.7, 1.9, 7.4, 4.5, [prompt, 'Write your guess on paper before we run it.'], size_max=32, size_min=22, lead=1.2, gap=0.3)
        objs.append(po)
        objs.append(K.image_obj(fig_paper_pen(3.6, 3.4), 8.9, 2.0, 3.6, 3.4, alt='A page and a pen'))
    if placed != 'done':
        d.add('light', f'Predict: {idea}', objs, N.predict_note(blk['intro'], prompt, seed), section=f'Block {letter}')
    # ---- run
    cap = capture_block(d.track, d.ident, l, bi) if run_code else {'ok': False}
    objs = []
    shown = pick_sentences(blk['shows'])
    charts = cap.get('charts') or []
    if cap.get('ok') and len(charts) >= 2:
        for i, c in enumerate(charts[:2]):
            objs.append(K.image_obj(c, 0.7 + i * 6.05, 1.75, 5.85, 3.3, alt='A chart the code draws'))
        so, _ = K.fitted_paras(0.7, 5.25, 11.9, 1.6, [' '.join(shown)], size_max=24, size_min=18, lead=1.2)
        objs.append(so)
    else:
        lay = None
        if cap.get('ok') and len(charts) == 1:
            objs.append(K.image_obj(charts[0], 0.7, 1.75, 6.6, 4.95, alt='The chart the code draws'))
            lay = 'chart'
        elif cap.get('ok') and cap.get('stdout'):
            lines = cap['stdout'][:12] + (['...'] if len(cap['stdout']) > 12 else [])
            try:
                o, s, ph = K.output_panel(lines, 0.7, 1.8, 6.6, 4.8, size_max=22, size_min=15)
                objs += o
                lay = 'output'
            except K.FitError:
                lay = None
        if lay:
            so, _ = K.fitted_paras(7.7, 1.9, 4.9, 4.8, shown, size_max=26, size_min=18, lead=1.2, gap=0.22)
            objs.append(so)
        else:
            so, _ = K.fitted_paras(0.7, 1.9, 8.2, 4.8, shown, size_max=30, size_min=20, lead=1.2, gap=0.25)
            objs.append(so)
            objs.append(K.image_obj(fig_icon('check', 2.6, 2.6, 1.6), 9.6, 2.4, 2.6, 2.6, alt='Compare with your guess'))
    d.add('light', f'Run it: {idea}', objs, N.run_note(blk['shows'], seed), section=f'Block {letter}')
    # ---- investigate
    objs = []
    qs = [f'{i + 1}.  {q}' for i, (q, a) in enumerate(blk['investigate'])]
    if code:
        try:
            o, s, ph = K.code_panel(K.wrap_code(code, 36), 8.2, 1.9, 4.4, 4.7, size_max=18, size_min=14)
            objs += o
            qw = 7.0
        except K.FitError:
            objs.append(K.image_obj(fig_icon('magnifier', 1.8, 1.8, 1.4), 10.8, 4.9, 1.8, 1.8, alt='Look closely'))
            qw = 9.8
    else:
        qw = 9.4
        objs.append(K.image_obj(fig_icon('magnifier', 2.4, 2.4, 1.6), 10.2, 2.4, 2.4, 2.4, alt='Look closely'))
    qo, _ = K.fitted_paras(0.7, 1.9, qw, 4.8, qs, size_max=36, size_min=22, lead=1.2, gap=0.55)
    objs.append(qo)
    d.add('light', f'Investigate: {idea}', objs, N.investigate_note(idea, blk['investigate'], seed), section=f'Block {letter}')
    # ---- modify
    objs = []
    mod = blk['modify']
    mo, _ = K.fitted_paras(0.7, 1.9, 6.6 if code else 8.2, 4.6, [mod['instruction'], 'Then tell your neighbour what changed and how you know.'], size_max=36, size_min=22, lead=1.2, gap=0.45)
    objs.append(mo)
    if code:
        try:
            o, s, ph = K.code_panel(K.wrap_code(code, 38), 7.9, 1.9, 4.7, 4.6, size_max=18, size_min=14)
            objs += o
        except K.FitError:
            objs.append(K.image_obj(fig_icon('pen', 2.0, 2.0, 1.5), 10.3, 2.3, 2.0, 2.0, alt='Change one thing'))
    else:
        objs.append(K.image_obj(fig_icon('pen', 2.6, 2.6, 1.7), 9.6, 2.4, 2.6, 2.6, alt='Change one thing'))
    d.add('light', 'Modify: change one thing', objs, N.modify_note(mod['instruction'], mod['answer'], seed), section=f'Block {letter}')


def add_break(d, l):
    mins = 15
    for lab, m in parse_clock(l):
        if 'break' in lab.lower():
            mins = m
    objs = [K.text_obj(0.7, 3.45, 7.5, 1.0, text=f'{mins} minutes away from your screen', size=34, color='FFFFFF', bold=True),
            K.text_obj(0.7, 4.6, 7.0, 1.6, text='Stand up. Drink some water. Tell someone what you guessed in the first half.', size=24, color='D8D8D8', lead=1.25),
            K.image_obj(fig_clock_dark(3.2, 3.2), 9.1, 3.0, 3.2, 3.2, alt='A clock')]
    sl = {'layout': 'dark', 'section': 'Break', 'title': {'text': 'Break', 'size': 54, 'lead': 60.0}, 'objects': objs,
          'notes': N.break_note(mins, 'the second idea', d.seed)}
    sl['title_pos'] = 'break'
    d.slides.append(sl)


def add_make(d, l):
    import re
    mk = l['make']
    d.section = 'Make and close'
    sents = [x for x in re.split(r'(?<=[.!?])\s+', mk['task'].strip()) if x]
    save = f'Save it as {d.ident}. Write two sentences: what you changed and how you checked it.'
    words = len(mk['task'].split())
    if words > 70 and len(sents) > 3:
        half = 0
        acc = 0
        for i, x in enumerate(sents):
            acc += len(x.split())
            if acc >= words / 2:
                half = i + 1
                break
        groups = [sents[:half], sents[half:]]
    else:
        groups = [sents]
    for gi, g in enumerate(groups):
        objs = []
        paras = [' '.join(g)] + ([save] if gi == len(groups) - 1 else [])
        mo, _ = K.fitted_paras(0.7, 1.9, 7.6, 4.9, paras, size_max=30, size_min=21, lead=1.2, gap=0.35)
        objs.append(mo)
        objs.append(K.image_obj(fig_save(3.8, 3.6), 8.9, 2.1, 3.8, 3.6, alt='A notebook saved with a tick'))
        title = 'Make: your own version' if len(groups) == 1 else f'Make: your own version ({gi + 1} of {len(groups)})'
        d.add('light', title, objs, N.make_note(d.ident, mk['task'], d.seed, gi, len(groups)), section='Make and close')


def add_errors(d, l):
    objs = []
    rows = l['errors']
    for i, (see, means, fix) in enumerate(rows):
        y = 1.8 + i * 2.55
        objs.append(K.image_obj(fig_icon('cross', 0.9, 0.9, 1.6), 0.7, y + 0.05, 0.9, 0.9, alt='Error'))
        size = 18
        try:
            s, lines = K.fit_lines(see, 'regular', 4.1, 1.9, 20, 15, lead=1.25)
        except K.FitError:
            s, lines = K.fit_lines(see[:90] + '...', 'regular', 4.1, 1.9, 15, 13, lead=1.25)
        objs.append(K.rect_obj(1.8, y + 0.2, 4.4, 1.8, fill='FFFFFF', line=B.RED, line_w=2.0, radius=0.06))
        objs.append(K.text_obj(1.95, y + 0.3, 4.1, 1.6, text=see, size=s, font=B.MONO_FONT, color=B.RED, lead=1.25, valign='middle'))
        mo, _ = K.fitted_paras(6.6, y + 0.02, 6.0, 2.15, [f'It means: {means}', f'Fix: {fix}'], size_max=22, size_min=17, lead=1.2, gap=0.18)
        objs.append(mo)
        if i < len(rows) - 1:
            objs.append(K.line_obj(0.7, y + 2.37, 12.6, y + 2.37))
    d.add('light', 'Two errors you may meet today', objs, N.errors_note(rows, d.seed), section='Make and close')


def add_exit(d, l):
    objs = []
    eo, _ = K.fitted_paras(0.7, 1.9, 7.6, 3.2, [l['exit_ticket']], size_max=40, size_min=26, lead=1.2)
    objs.append(eo)
    objs.append(K.text_obj(0.7, 5.3, 7.6, 1.2, text='Then save your notebook, close it and open it again to check it saved.', size=22, color=B.BODY, lead=1.25))
    objs.append(K.image_obj(fig_icon('check', 3.6, 3.6, 2.2), 9.0, 2.1, 3.6, 3.6, alt='Finished'))
    d.add('light', 'Finish this sentence in your notebook', objs, N.exit_note(l['exit_ticket'], d.question, d.seed), section='Make and close')


# ---------------------------------------------------------------- adapters for labs and the extension
LAB_IDEA = {'F01': 'names and totals', 'F02': 'lists as vectors', 'F03': 'spread and chance', 'F04': 'weighted sums'}


def lab_as_lesson(i, lab):
    ident = f'F{i:02d}'
    reps = [s.strip() for s in lab['repair'].replace('\n', ' ').split('. ') if s.strip()]
    errs = lab.get('errors') or [('Your printed numbers differ from your paper work', (reps[0].rstrip('.') + '.') if reps else 'A step was changed or skipped.', (reps[1].rstrip('.') + '.') if len(reps) > 1 else 'Ask the instructor to look at it with you.'),
            ('The code stops with an error message', 'Python could not run one of the lines.', 'Read the last line of the message first, then find the line number it names.')]
    return {'title': lab['title'], 'objective': 'By the end: you can explain the idea in your own words and run the worked example.', 'question': lab['question'],
            'words': lab['words'], 'blocks': [dict(idea=LAB_IDEA.get(ident, lab['title']), intro=lab['explain'], predict='Work the paper example first: ' + lab['hand'].split('.')[0] + '. Then predict every line the code will print.',
                                                  code=lab['code'], shows=lab['output'], investigate=[('What does each line of the code do?', 'Read each line aloud and say what it stores or prints.'), ('Which number surprised you?', 'Say which printed value differed from your paper work, and why.')],
                                                  modify=dict(instruction=lab['task'].split('. ')[0] + '.', answer=lab['answer'].split('.')[0] + '.'))],
            'make': dict(task=lab['task'], reference=lab['answer'], evidence=ident + '.ipynb'), 'errors': errs,
            'exit_ticket': 'I can explain ' + lab['title'][0].lower() + lab['title'][1:] + ' in my own words.', 'mode': 'python', 'pacing': None}, ident


def ext_as_lesson():
    e = EXTENSION
    return {'title': e['title'], 'objective': 'By the end: you can compare a small neural network with a decision tree and a baseline, and say why a bigger model is not automatically better.',
            'question': 'Does a neural network beat a small tree on 150 flowers?', 'words': [],
            'blocks': [dict(idea='A network, a tree and a baseline', intro=e['intro'], predict='Predict whether the network will score higher than the depth 3 tree.', code=e['code'],
                            shows=e['honest_note'], investigate=[('Why scale the inputs first?', 'Networks learn badly from numbers on very different scales.'), ('What would convince you a network is worth using?', 'A clear gain on data it has not seen, after the baseline and the tree are beaten.')],
                            modify=dict(instruction='Change hidden_layer_sizes from (8,) to (16,) and run it again.', answer='The score changes a little. A bigger network is not automatically better.'))],
            'make': dict(task='Write two sentences: which model scored best and whether the difference is big enough to matter.', reference='', evidence='ML25.ipynb'),
            'errors': [('ConvergenceWarning', 'The network stopped before it finished learning.', 'Raise max_iter and run it again.'), ('Scores change every run', 'The random_state is missing.', 'Set random_state=7 so the run repeats.')],
            'exit_ticket': 'A bigger model is not automatically a better one, and I check it against a baseline.', 'mode': 'python', 'pacing': None}, 'ML25'


# ---------------------------------------------------------------- driver
def build_one(track, idx, lesson, ident, concepts, kind='session'):
    num = f'{idx}' if kind == 'session' else ident
    week = (idx - 1) // 3 + 1 if kind == 'session' else None
    d = Deck(ident, track, kind, lesson['title'], lesson['objective'], lesson['question'], f'{ident}  |  {lesson["title"]}'[:84])
    if kind == 'session':
        d.sub = f'Session {idx} of 24  |  Week {week}, {WEEK_THEMES[track][week - 1]}'
    elif kind == 'lab':
        d.sub = f'Foundation lab {ident}'
    else:
        d.sub = 'Optional extension after session 24'
    add_title(d, lesson, idx, lesson['title'], week)
    add_question(d, concepts)
    add_plan(d, lesson) if kind == 'session' else None
    add_words(d, lesson, concepts)
    add_concepts(d, concepts, 0)
    blocks = lesson['blocks']
    if blocks:
        add_block(d, lesson, 0, 'A', concepts)
    if len(blocks) > 1:
        add_break(d, lesson)
        add_concepts(d, concepts, 1)
        add_block(d, lesson, 1, 'B', concepts)
    add_concepts(d, concepts, 2)
    add_make(d, lesson)
    add_errors(d, lesson)
    add_exit(d, lesson)
    spec = {'out': str(OUT_DIR / track / f'{ident}.pptx'), 'title': f'{ident} {lesson["title"]}', 'subject': TRACK_NAMES.get(track, 'Machine Learning'),
            'footer': d.footer, 'fonts': {'head': B.HEAD_FONT, 'body': B.BODY_FONT, 'mono': B.MONO_FONT}, 'brand': {}, 'logo': _logo_dims(),
            'slides': d.slides}
    # dark-slide title sizing for the break slide is fixed; the placeholder sits at y 2.3, so move it up for the break
    return spec


def write_and_render(spec, render=True):
    SPEC_DIR.mkdir(parents=True, exist_ok=True)
    p = SPEC_DIR / (Path(spec['out']).stem + '.json')
    # resolve dark-slide titles
    for s in spec['slides']:
        if s.get('title_raw') is not None and s['title'] is None:
            s['title'] = {'text': s['title_raw'], 'size': 48, 'lead': 53.0}
    p.write_text(json.dumps(spec))
    if not render:
        return None
    env = dict(os.environ, PPTX_SKILL_SCRIPTS=PPTX_SKILL_SCRIPTS)
    r = subprocess.run(['node', str(HERE / 'render_deck.js'), str(p)], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return r.stdout.strip()


def sessions(selected):
    items = []
    for i, l in enumerate(DA, 1):
        items.append(('DA', i, l, f'DA{i:02d}', CONCEPTS_DA.get(i, {}), 'session'))
    for i, l in enumerate(ML, 1):
        items.append(('ML', i, l, f'ML{i:02d}', CONCEPTS_ML.get(i, {}), 'session'))
    for i, lab in enumerate(LABS, 1):
        lesson, ident = lab_as_lesson(i, lab)
        items.append(('ML', i, lesson, ident, CONCEPTS_ML.get(ident, {}), 'lab'))
    lesson, ident = ext_as_lesson()
    items.append(('ML', 25, lesson, ident, CONCEPTS_ML.get(ident, {}), 'extension'))
    if selected:
        items = [x for x in items if x[3] in selected]
    return items


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    spec_only = '--spec-only' in sys.argv
    AUTO.mkdir(parents=True, exist_ok=True)
    problems = []
    for track, idx, lesson, ident, concepts, kind in sessions(set(args)):
        try:
            spec = build_one(track, idx, lesson, ident, concepts, kind)
            msg = write_and_render(spec, render=not spec_only)
            print(ident, len(spec['slides']), 'slides', msg or '')
        except Exception as e:
            problems.append((ident, repr(e)))
            print('FAILED', ident, repr(e)[:300])
            traceback.print_exc(limit=2)
    if CODE_SMALL:
        print('\nCode panels below 16 pt (shorten the lesson code lines):')
        for ident, where, size in CODE_SMALL:
            print('  ', ident, where, size)
    if figkit.SMALL_TEXT:
        by = {}
        for name, txt, size in figkit.SMALL_TEXT:
            by.setdefault(name, []).append(size)
        print('\nFigures with text under 14 pt: %d figures' % len(by))
        for name, sizes in sorted(by.items()):
            print('  ', name, 'min', min(sizes), 'count', len(sizes))
    if problems:
        print('\n%d decks failed' % len(problems))
        sys.exit(1)


if __name__ == '__main__':
    main()
