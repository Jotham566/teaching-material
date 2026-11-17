"""AI and Data Science Professional deck builder: a session dict (content/sNN.py -> build()) -> a JSON spec -> render_deck.js -> .pptx.

Run from Build/:   python3 kit/deck.py [1 2 ...]   (session numbers; none = all)
Env: PPTX_SKILL_SCRIPTS must point at the pptx skill's scripts folder (apply_theme.js).

Slide kinds (every slide needs a `title` that states the point and `notes`, the spoken script):
  idea       title, lead, points[<=3], visual{...}        a diagram on the left, the point on the right
  wide       title, visual{...}, caption                   a full-width diagram
  statement  title, lead, points[<=4], icon                text only, with one pictogram
  compare    title, left{head, points[]}, right{head, points[]}, verdict
  table      title, headers[], rows[][], widths[], note, hl_col
  steps      title, steps[{head,text,icon}], caption, highlight   a flow of 3 to 5 steps
  example    title, scenario, blocks[{label, text, mono}]
  demo       title, show[], watch[]                         what the instructor does and what to look for
  practice   title, minutes, task, steps[], output          the learner works on their own company task
  decision   title, question, options[{head,text}], record
  stat       title, big, text, source
  list       title, items[], icon
Auto slides: cover, outcome, plan, recall, words, keep.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'content'))
import brand as B  # noqa: E402
import figkit  # noqa: E402
import slidekit as K  # noqa: E402
import diagrams as DG  # noqa: E402

BUILD = HERE.parent
EDITION = BUILD.parent.parent
SPEC_DIR = BUILD / '_specs'
OUT_DIR = EDITION / '02 Class Slides'
PPTX_SKILL_SCRIPTS = os.environ.get('PPTX_SKILL_SCRIPTS', '/sessions/focused-youthful-einstein/mnt/.claude/skills/pptx/scripts')
COURSE = 'AI and Data Science Professional'
X0, XW = 0.7, 11.9
Y0, YB = 1.95, 6.85



# ------------------------------------------------------------------ speaker notes: spoken script, paragraphs, pauses
import re as _re

PAUSES = ['Take a moment.', 'Say it to yourself first.', 'Think about your own task as you answer.']
ANSWERS = ['Here is how I would answer it.', 'The answer is this.', 'Let me say it plainly.', 'This is the answer I am looking for.', 'Here is the short version.', 'What I would say is this.']
ORDINALS = ['One', 'Two', 'Three', 'Four']


def _sentences(text):
    return [x for x in _re.split(r'(?<=[.!?])\s+', text.strip()) if x]


def paragraphs(text, target=48):
    """Break a note into short paragraphs a presenter can read without losing the place: after a question, and after about `target` words."""
    if '\n' in text:
        return text.strip()
    out, cur, n = [], [], 0
    for s in _sentences(text):
        cur.append(s)
        n += len(s.split())
        if s.endswith('?') or n >= target:
            out.append(' '.join(cur))
            cur, n = [], 0
    if cur:
        if out and n < 12:
            out[-1] += ' ' + ' '.join(cur)
        else:
            out.append(' '.join(cur))
    return '\n\n'.join(out)


def recall_script(s):
    """Read each question, pause, then give the expected answer in the next paragraph."""
    n = len(s['recall'])
    lead = {1: 'One quick question', 2: 'Two quick questions', 3: 'Three quick questions'}.get(n, f'{n} quick questions')
    paras = [f'{lead} from {s.get("recall_from", "last class")}. Answer aloud first, and then we check together. It is a warm-up to bring last time back.']
    for i, (q, a) in enumerate(s['recall']):
        paras.append(f'Question {ORDINALS[i].lower()}. {q}')
        paras.append(f'A good answer is this. {a}')
    paras.append('If you missed one, check your notes from last session tonight. Now to today.')
    return '\n\n'.join(paras)


def words_script(s):
    words = s['words']
    k = {3: 'three', 4: 'four', 5: 'five'}.get(len(words), str(len(words)))
    paras = [f'{k.capitalize()} words for today. I give the plain meaning of each, and we use every one of them before the end of the session.']
    for term, meaning in words:
        paras.append(f'{term}. {meaning}')
    return '\n\n'.join(paras)


_NUM = {5: 'five', 10: 'ten', 15: 'fifteen', 20: 'twenty', 25: 'twenty-five', 30: 'thirty', 35: 'thirty-five', 40: 'forty', 45: 'forty-five', 50: 'fifty', 60: 'sixty', 70: 'seventy'}


def plan_script(s):
    base = s['plan_note']
    if len(_re.findall(r'minutes', base)) >= 3 or len(base.split()) >= 70:
        return paragraphs(base)
    order = ['First', 'Then', 'After that', 'Next', 'Then', 'Then', 'Last']
    parts = []
    for i, (m, label) in enumerate(s['clock']):
        parts.append(f'{order[min(i, len(order) - 1)]}, {_NUM.get(m, str(m))} minutes. {label[:1].upper() + label[1:]}.')
    return paragraphs(base) + '\n\nHere is how the two hours run. ' + ' '.join(parts)


def cover_script(s):
    base = s['cover_note']
    if len(base.split()) >= 60:
        return paragraphs(base)
    return paragraphs(base) + f'\n\nThe question for today is this: {s["question"]} Keep it in mind. At the end of the session we come back to it and see how much more you can say.'


class Deck:
    def __init__(self, sess):
        self.s = sess
        self.slides = []
        self.section = 'Opening'

    def add(self, title, objs, notes, layout='light', section=None, raw_title=None):
        self.slides.append({'layout': layout, 'section': section or self.section, 'title': K.title_obj(title) if (title and layout == 'light') else None,
                            'title_raw': raw_title, 'objects': objs, 'notes': paragraphs(notes)})


def _logo():
    from PIL import Image
    with Image.open(B.LOGO_ON_WHITE) as im:
        ar = im.width / im.height
    return {'on_white': str(B.LOGO_ON_WHITE), 'on_black': str(B.LOGO_ON_BLACK), 'h_small': 0.27, 'w_small': round(0.27 * ar, 3), 'h_large': 0.62, 'w_large': round(0.62 * ar, 3)}


def img(data_or_name, x, y, w, h, alt=''):
    path = DG.render(data_or_name, w, h) if isinstance(data_or_name, dict) else data_or_name
    return K.image_obj(str(path), x, y, w, h, alt=alt)


def paras(x, y, w, h, items, smax=24, smin=18, color=B.INK, gap=0.16, bold=False):
    o, s = K.fitted_paras(x, y, w, h, items, size_max=smax, size_min=smin, color=color, gap=gap, bold=bold)
    return o


def text(x, y, w, h, t, smax=24, smin=18, color=B.INK, bold=False, align='left', valign='top', italic=False):
    o, s = K.fitted_text(x, y, w, h, t, size_max=smax, size_min=smin, color=color, bold=bold, align=align, valign=valign, italic=italic)
    return o


def icon_img(name, size, x, y, alt=''):
    def d(sc):
        sc.icon(name, size / 2, size / 2, size * 0.95, **({'text': ''} if name == 'coin' else {}))
    p = figkit.FIG_DIR / f'icon_{name}_{size:.2f}.png'
    if not p.exists():
        sc = figkit.Scene(size, size)
        d(sc)
        sc.save(p)
    return K.image_obj(str(p), x, y, size, size, alt=alt or name)


# ------------------------------------------------------------------ tables (native, editable)
def table_obj(x, y, w, headers, rows, widths=None, size_max=20, size_min=15, hl_col=None, max_h=None, header=True):
    n = len(rows[0]) if rows else len(headers)
    tot = sum(widths) if widths else n
    colw = [w * (c / tot) for c in widths] if widths else [w / n] * n
    max_h = max_h or (YB - y)
    for size in [x_ for x_ in range(int(size_max), int(size_min) - 1, -1)]:
        pad = 0.16
        heights = []
        allrows = ([headers] if header else []) + rows
        for ri, r in enumerate(allrows):
            lines = 1
            for ci, c in enumerate(r):
                kind = 'bold' if (header and ri == 0) or ci == 0 else 'regular'
                lines = max(lines, len(K.wrap(str(c), size, kind, colw[ci] - 0.24)))
            heights.append(lines * size * 1.2 / 72 + pad)
        if sum(heights) <= max_h:
            break
    else:
        raise K.FitError(f'table does not fit {max_h:.2f} in at {size_min} pt: {allrows[0]}')
    none_b = {'type': 'none'}
    line = {'type': 'solid', 'pt': 0.75, 'color': 'CFCFCF'}
    head_line = {'type': 'solid', 'pt': 2.0, 'color': '111111'}
    out = []
    for ri, r in enumerate(allrows):
        is_head = header and ri == 0
        row = []
        for ci, c in enumerate(r):
            row.append({'text': str(c), 'bold': is_head or ci == 0, 'size': size, 'color': '111111' if (is_head or ci == 0) else '333333',
                        'fill': 'E0BE36' if (hl_col is not None and ci == hl_col and not is_head) else None,
                        'border': [none_b, none_b, head_line if is_head else line, none_b]})
        out.append(row)
    return {'type': 'table', 'x': x, 'y': y, 'w': w, 'colW': colw, 'rowH': heights, 'rows': out, 'size': size}, sum(heights)



_ICON_WORDS = [(('write', 'record', 'list', 'note', 'name', 'fill'), 'notebook'), (('score', 'measure', 'time', 'minutes', 'count', 'hours'), 'clock'),
               (('check', 'test', 'verify', 'approve', 'confirm', 'compare'), 'check'), (('plot', 'chart', 'trend', 'result', 'payback', 'saving'), 'chart'),
               (('choose', 'decide', 'pick', 'select', 'decision'), 'pin'), (('build', 'run', 'set up', 'install', 'trigger', 'script'), 'gear'),
               (('email', 'message', 'send', 'notify', 'reply', 'enquiry', 'enquiries'), 'mail'), (('data', 'file', 'document', 'source', 'sheet', 'inventory', 'folder'), 'folder'),
               (('staff', 'team', 'owner', 'people', 'train', 'adoption', 'tell'), 'people'), (('risk', 'safe', 'protect', 'permission', 'policy', 'private', 'confidential', 'least privilege'), 'shield'),
               (('key', 'secret', 'password', 'login'), 'key'), (('cost', 'money', 'price', 'ugx', 'budget', 'licence'), 'coin'), (('search', 'find', 'read', 'look', 'review'), 'magnifier')]
_ICON_CYCLE = ['pin', 'notebook', 'check', 'gear', 'chart', 'folder', 'people']


def auto_icons(items):
    """One pictogram per item, chosen by keyword (the author can override with an `icons` list); no icon repeats twice in a row."""
    out = []
    for i, it in enumerate(items):
        s = (it if isinstance(it, str) else ' '.join(str(v) for v in it.values() if isinstance(v, str))).lower()
        pick = None
        for words, ic in _ICON_WORDS:
            if any(w in s for w in words):
                pick = ic
                break
        pick = pick or _ICON_CYCLE[i % len(_ICON_CYCLE)]
        if out and out[-1] == pick:
            pick = _ICON_CYCLE[(i + 3) % len(_ICON_CYCLE)]
        out.append(pick)
    return out


def icon_rows(x, y, w, h, items, icons=None, smax=24, smin=18, bold_first=False):
    """Rows with a pictogram on the left and one item of text each, separated by hairlines. Row heights follow the text. Returns objects."""
    n = len(items)
    icons = icons or auto_icons(items)
    tw = w - 1.0
    chosen = None
    for sz in range(int(smax), int(smin) - 1, -1):
        hs = [max(0.72 if n < 6 else 0.6, len(K.wrap(str(it), sz, 'regular', tw)) * sz * 1.2 / 72 + (0.2 if n < 6 else 0.12)) for it in items]
        if sum(hs) <= h:
            chosen = (sz, hs)
            break
    if chosen is None:
        raise K.FitError(f'rows do not fit {h:.2f} in at {smin} pt: {items[0]}')
    sz, hs = chosen
    extra = min(0.25, (h - sum(hs)) / max(1, n))
    objs = []
    yy = y
    for i, it in enumerate(items):
        rh = hs[i] + extra
        isz = min(0.7, rh - 0.1)
        objs.append(icon_img(icons[i], round(isz, 2), x + 0.05, yy + (rh - isz) / 2))
        o = K.text_obj(x + 1.0, yy + 0.04, tw, rh - 0.08, text=str(it), size=sz, color=B.INK, valign='middle')
        objs.append(o)
        if i < n - 1:
            objs.append(K.line_obj(x, yy + rh, x + w, yy + rh, color='CFCFCF', w=0.75))
        yy += rh
    return objs


def table_with_icons(x, y, w, headers, rows, widths, icons=None, size_max=20, size_min=15, hl_col=None, max_h=None, header=True):
    """A native table with a pictogram column on its left."""
    isz = 0.5
    t, th = table_obj(x + 0.8, y, w - 0.8, headers, rows, widths, size_max, size_min, hl_col, max_h, header)
    objs = [t]
    icons = icons or auto_icons([r[0] + ' ' + (r[1] if len(r) > 1 else '') for r in rows])
    yy = y + (t['rowH'][0] if header else 0)
    for i, ic in enumerate(icons[:len(rows)]):
        rh = t['rowH'][i + (1 if header else 0)]
        s_ = min(isz, rh - 0.1)
        objs.append(icon_img(ic, round(s_, 2), x + 0.1, yy + (rh - s_) / 2))
        yy += rh
    return objs, th


# ------------------------------------------------------------------ slide kinds
def k_idea(d, sl):
    objs = [img(sl['visual'], X0, Y0, 7.7, 4.8, sl.get('alt', sl['title']))]
    lo = text(8.8, Y0 + 0.05, 3.8, 1.9, sl['lead'], 26, 20, bold=True)
    objs.append(lo)
    pts = sl.get('points', [])
    if pts:
        objs.append(paras(8.8, Y0 + 2.1, 3.8, 2.8, pts, 22, 18, color=B.BODY, gap=0.2))
    return objs


def k_wide(d, sl):
    objs = [img(sl['visual'], X0, Y0 - 0.05, XW, 4.25, sl.get('alt', sl['title']))]
    if sl.get('caption'):
        objs.append(text(X0, 6.25, XW, 0.6, sl['caption'], 22, 18, color=B.BODY))
    return objs


def k_statement(d, sl):
    objs = [text(X0, Y0 + 0.05, XW, 1.2, sl['lead'], 30, 24, bold=True)]
    pts = sl.get('points', [])
    if pts:
        objs += icon_rows(X0, Y0 + 1.4, XW, 3.5, pts, sl.get('icons'), 24, 18)
    elif sl.get('icon'):
        objs.append(icon_img(sl['icon'], 3.2, 9.4, 2.3, sl['icon']))
    return objs


def k_compare(d, sl):
    objs = []
    colw = 5.6
    for i, side in enumerate((sl['left'], sl['right'])):
        x = X0 + i * (colw + 0.7)
        hx = x
        if side.get('icon'):
            objs.append(icon_img(side['icon'], 0.75, x, Y0 + 0.02))
            hx = x + 0.9
        objs.append(text(hx, Y0 + 0.05, colw - (hx - x), 0.7, side['head'], 30, 24, bold=True, valign='middle'))
        objs.append(K.line_obj(x, Y0 + 0.85, x + colw, Y0 + 0.85, color='111111', w=2.0))
        objs.append(paras(x, Y0 + 1.0, colw, 2.95, side['points'], 22, 18, color=B.BODY, gap=0.2))
    objs.append(K.line_obj(X0 + colw + 0.35, Y0 + 0.1, X0 + colw + 0.35, Y0 + 4.2, color='CFCFCF', w=1.0))
    if sl.get('verdict'):
        objs.append(text(X0, 6.1, XW, 0.7, sl['verdict'], 24, 19, bold=True, color=B.RED))
    return objs


def k_table(d, sl):
    note = sl.get('note')
    if sl.get('split'):
        rows = sl['rows']
        half = (len(rows) + 1) // 2
        objs = []
        for i, part in enumerate((rows[:half], rows[half:])):
            x = X0 + i * (XW / 2 + 0.1)
            t, th = table_obj(x, Y0, XW / 2 - 0.1, sl['headers'], part, sl.get('widths'), 18, 14, None, YB - Y0 - 0.1)
            objs.append(t)
        return objs

    maxh = (YB - Y0 - 0.1) - (0.7 if note else 0)
    if sl.get('icons') is not False:
        objs, th = table_with_icons(X0, Y0, XW, sl['headers'], sl['rows'], sl.get('widths'), sl.get('icons'), 20, 15, sl.get('hl_col'), maxh)
    else:
        t, th = table_obj(X0, Y0, XW, sl['headers'], sl['rows'], sl.get('widths'), 20, 15, sl.get('hl_col'), maxh)
        objs = [t]
    if note:
        objs.append(text(X0, min(Y0 + th + 0.2, 6.2), XW, 0.6, note, 20, 16, color=B.MUTE))
    return objs


def k_steps(d, sl):
    n = len(sl['steps'])
    h = 3.9 if sl.get('caption') else 4.6
    objs = [img({'kind': 'flow', 'steps': sl['steps'], 'highlight': sl.get('highlight')}, X0, Y0, XW, h, sl.get('alt', sl['title']))]
    if sl.get('caption'):
        objs.append(text(X0, Y0 + h + 0.15, XW, 0.9, sl['caption'], 24, 18, color=B.BODY))
    return objs


def k_example(d, sl):
    objs = []
    y = Y0
    if sl.get('scenario'):
        o = text(X0, y, XW, 0.85, sl['scenario'], 22, 17, color=B.BODY, italic=True)
        objs.append(o)
        y += 0.95
    blocks = sl['blocks']
    avail = YB - y - 0.15
    gap = 0.18
    bh = (avail - gap * (len(blocks) - 1)) / len(blocks)
    for b in blocks:
        objs.append(K.rect_obj(X0, y, XW, bh, fill=None, line='111111' if not b.get('red') else 'AE2525', line_w=1.5, radius=0.05))
        objs.append(text(X0 + 0.2, y + 0.08, 2.0, bh - 0.16, b['label'], 18, 14, bold=True, color=B.RED if b.get('red') else B.INK, valign='middle'))
        if b.get('mono'):
            sz = 18
            lines = K.wrap_code(b['text'], 80) if hasattr(K, 'wrap_code') else b['text']
            o, s_ = K.fitted_text(X0 + 2.3, y + 0.08, XW - 2.5, bh - 0.16, b['text'], 'regular', 20, 15, valign='middle')
            o['font'] = B.MONO_FONT
            objs.append(o)
        else:
            objs.append(text(X0 + 2.3, y + 0.08, XW - 2.5, bh - 0.16, b['text'], 22, 16, valign='middle', color=B.BODY))
        y += bh + gap
    return objs


def k_demo(d, sl):
    objs = []
    if sl.get('visual'):
        objs.append(text(X0, Y0 + 0.05, 7.3, 0.6, 'I will show', 28, 22, bold=True))
        objs.append(K.line_obj(X0, Y0 + 0.75, X0 + 7.3, Y0 + 0.75, color='111111', w=2.0))
        objs.append(img(sl['visual'], X0, Y0 + 0.9, 7.3, 3.9, sl.get('alt', sl['title'])))
        objs.append(text(8.4, Y0 + 0.05, 4.2, 0.6, 'Watch for', 28, 22, bold=True, color=B.RED))
        objs.append(K.line_obj(8.4, Y0 + 0.75, 12.6, Y0 + 0.75, color='111111', w=2.0))
        objs.append(paras(8.4, Y0 + 0.9, 4.2, 3.9, sl['watch'], 22, 18, color=B.BODY, gap=0.2))
        return objs
    colw = 5.6
    for i, (head, items) in enumerate((('I will show', sl['show']), ('Watch for', sl['watch']))):
        x = X0 + i * (colw + 0.7)
        objs.append(text(x, Y0 + 0.05, colw, 0.6, head, 28, 22, bold=True, color=B.RED if i else B.INK))
        objs.append(K.line_obj(x, Y0 + 0.75, x + colw, Y0 + 0.75, color='111111', w=2.0))
        objs.append(paras(x, Y0 + 0.9, colw, 3.9, items, 22, 18, color=B.BODY, gap=0.2))
    return objs


def k_practice(d, sl):
    objs = []
    objs.append(K.rect_obj(X0, Y0 - 0.02, 2.0, 0.46, fill='E0BE36', radius=0.08))
    objs.append(K.text_obj(X0, Y0 - 0.02, 2.0, 0.46, text=f"{sl['minutes']} minutes", size=18, bold=True, align='center', valign='middle'))
    objs.append(K.text_obj(X0 + 2.2, Y0 - 0.02, 6, 0.46, text=sl.get('label', 'Your own company task'), size=18, bold=True, color=B.RED, valign='middle'))
    if sl.get('example'):
        objs.append(text(X0, Y0 + 0.6, 6.0, 1.2, sl['task'], 26, 20, bold=True))
        objs.append(paras(X0, Y0 + 1.85, 6.0, 3.0, sl['steps'], 21, 17, color=B.BODY, gap=0.14))
        objs.append(img(sl['example'], 7.1, Y0 + 0.5, 5.5, 3.55, sl.get('example_alt', 'What your finished page looks like')))
        objs.append(text(7.1, Y0 + 4.15, 5.5, 0.8, 'You keep: ' + sl['output'], 18, 14, bold=True))
        return objs
    objs.append(text(X0, Y0 + 0.6, 7.4, 1.1, sl['task'], 28, 21, bold=True))
    objs.append(paras(X0, Y0 + 1.8, 7.4, 3.0, sl['steps'], 22, 17, color=B.BODY, gap=0.14))
    objs.append(K.rect_obj(8.5, Y0 + 0.6, 4.1, 3.0, fill=None, line='111111', line_w=1.5, radius=0.05))
    objs.append(text(8.75, Y0 + 0.75, 3.6, 0.5, 'You keep', 22, 18, bold=True, color=B.RED))
    objs.append(text(8.75, Y0 + 1.35, 3.6, 2.1, sl['output'], 22, 17))
    return objs


def k_decision(d, sl):
    objs = [text(X0, Y0 + 0.05, XW, 1.3, sl['question'], 32, 24, bold=True)]
    opts = sl['options']
    n = len(opts)
    gap = 0.3
    bw = (XW - gap * (n - 1)) / n
    icons = [o.get('icon') or ic for o, ic in zip(opts, ['check', 'chart', 'pin', 'shield'])]
    for i, o in enumerate(opts):
        x = X0 + i * (bw + gap)
        objs.append(K.rect_obj(x, Y0 + 1.5, bw, 2.6, fill=None, line='111111', line_w=1.5, radius=0.05))
        objs.append(icon_img(icons[i], 0.8, x + 0.15, Y0 + 1.62))
        objs.append(text(x + 1.05, Y0 + 1.62, bw - 1.2, 0.8, o['head'], 24, 14, bold=True, valign='middle'))
        objs.append(text(x + 0.2, Y0 + 2.55, bw - 0.4, 1.5, o['text'], 20, 16, color=B.BODY))
    objs.append(text(X0, 6.5, XW, 0.4, sl.get('record', 'Write your decision and the reason in your notebook or sheet.'), 22, 18, color=B.MUTE))
    return objs


def k_stat(d, sl):
    objs = [K.text_obj(X0, Y0 + 0.1, 6.8, 1.9, text=sl['big'], size=96, bold=True, color=B.INK, valign='middle')]
    objs.append(text(X0, Y0 + 2.2, 6.8, 2.0, sl['text'], 28, 21, bold=True))
    vis = sl.get('visual')
    if vis is None and sl['big'].strip().endswith('%'):
        vis = {'kind': 'waffle', 'filled': int(float(sl['big'].strip().rstrip('%'))), 'label': sl.get('waffle_label', 'out of every 100')}
    if vis:
        objs.append(img(vis, 8.2, Y0 + 0.05, 4.4, 4.3, sl.get('alt', sl['title'])))
    if sl.get('source'):
        objs.append(text(X0, 6.45, XW, 0.4, 'Source: ' + sl['source'], 16, 14, color=B.MUTE))
    return objs


def k_list(d, sl):
    items = sl['items']
    return icon_rows(X0, Y0 + 0.05, XW, 4.75, items, sl.get('icons'), 26, 19)


def k_code(d, sl):
    """Code on the left (black panel), what it means in plain words on the right, optional output under the code."""
    objs = []
    cobjs, cs, ph = K.code_panel(sl['code'], X0, Y0, 7.2, 3.6, size_max=20, size_min=14)
    objs += cobjs
    y = Y0 + ph + 0.15
    if sl.get('output'):
        oo, os_, oh = K.output_panel(sl['output'], X0, y, 7.2, YB - y - 0.05, size_max=18, size_min=14)
        objs += oo
    objs.append(text(8.2, Y0, 4.4, 0.5, 'In plain words', 24, 20, bold=True, color=B.RED))
    objs.append(K.line_obj(8.2, Y0 + 0.55, 12.6, Y0 + 0.55, color='111111', w=2.0))
    objs.append(paras(8.2, Y0 + 0.7, 4.4, 4.1, sl['reads'], 21, 16, color=B.BODY, gap=0.2))
    return objs


def k_divider(d, sl):
    return []


def k_formula(d, sl):
    """Formulas drawn as maths on top; under them a table that names every symbol: symbol, what it means, and where it is in our data."""
    fl = sl['formulas']
    import diagrams_ml as _dm
    fh = sum(_dm.math_heights(fl, sl.get('size', 28))) + 0.1
    objs = [img({'kind': 'math', 'lines': fl, 'size': sl.get('size', 28)}, X0, Y0, XW, fh, sl.get('alt', sl['title']))]
    y = Y0 + fh + 0.1
    t, th = table_obj(X0, y, XW, ['Symbol', 'What it means', 'In our data'], sl['symbols'], sl.get('widths', [2.0, 5.6, 4.3]), 18, 14, None, YB - y - (0.55 if sl.get('note') else 0.05))
    objs.append(t)
    if sl.get('note'):
        objs.append(text(X0, min(y + th + 0.12, 6.35), XW, 0.5, sl['note'], 18, 15, color=B.MUTE))
    return objs


KINDS = {'formula': k_formula, 'code': k_code, 'divider': k_divider, 'idea': k_idea, 'wide': k_wide, 'statement': k_statement, 'compare': k_compare, 'table': k_table, 'steps': k_steps, 'example': k_example,
         'demo': k_demo, 'practice': k_practice, 'decision': k_decision, 'stat': k_stat, 'list': k_list}


# ------------------------------------------------------------------ automatic slides
def add_cover(d):
    s = d.s
    ts, tl = K.fit_lines(s['title'], 'bold', 11.0, 2.6, 56, 34, lead=1.1)
    qy = 2.3 + len(tl) * ts * 1.1 / 72 + 0.5
    q = text(X0, qy, 10.8, 1.4, s['question'], 30, 22, color=B.GOLD, italic=True)
    meta = K.text_obj(X0, 6.55, 11.8, 0.5, text=f'AI and Data Science Professional  |  Session {s["num"]} of 24  |  {s["block"]}' + '\nKLAi Professional Learning  |  Jotham Martin Wambi', size=16, color='B5B5B5', lead=1.45)
    sl = {'layout': 'dark', 'section': 'Opening', 'title': {'text': K.balance(s['title'], ts, 'bold', 11.0), 'size': ts, 'lead': round(ts * 1.1, 1)}, 'title_raw': None, 'objects': [q, meta],
          'notes': cover_script(s)}
    d.slides.append(sl)


def add_outcome(d):
    s = d.s
    objs = [text(X0, Y0 + 0.05, XW, 0.7, s.get('outcome_head', 'By the end of today you can'), 30, 24, bold=True)]
    objs.append(K.line_obj(X0, Y0 + 0.85, X0 + XW, Y0 + 0.85, color='111111', w=2.0))
    objs += icon_rows(X0, Y0 + 1.05, XW, 3.6, s['outcomes'], s.get('outcome_icons') or ['check', 'doc', 'chart'][:len(s['outcomes'])], 26, 19)
    d.add('Today in one view: what you will leave with', objs, s['outcome_note'])


def add_plan(d):
    s = d.s
    parts = s['clock']
    h = min(3.95, 0.55 * len(parts) + 0.2)
    objs = [img({'kind': 'plan', 'parts': [[lab, m] for m, lab in parts]}, X0, Y0, XW, h, 'The two hours in parts, in minutes')]
    objs.append(text(X0, Y0 + h + 0.15, XW, 0.6, s.get('plan_caption', 'Ideas first. Then the lab. Then the checks and what to keep.'), 24, 18, color=B.BODY))
    d.add(s.get('plan_title', 'Your two hours: ideas, lab, then AI'), objs, plan_script(s))


def add_recall(d):
    s = d.s
    qs = [f'{i + 1}.  {q}' for i, (q, a) in enumerate(s['recall'])]
    objs = [paras(X0, Y0 + 0.2, 8.6, 3.9, qs, 30, 22, gap=0.45)]
    objs.append(icon_img('question', 2.8, 9.9, Y0 + 0.5, 'Three questions'))
    objs.append(text(X0, 6.2, XW, 0.6, 'Answer aloud first. Then we check together.', 22, 18, color=B.MUTE))
    d.add({1: 'A question from last time', 2: 'Two questions from last time', 3: 'Three questions from last time'}.get(len(s['recall']), 'Questions from last time'), objs, recall_script(s))


def add_words(d):
    s = d.s
    words = s.get('words')
    if not words:
        return
    icons = s.get('word_icons') or auto_icons([a + ' ' + b for a, b in words])
    t, th = table_obj(X0 + 1.0, Y0, XW - 1.0, ['Word', 'What it means'], [[a, b] for a, b in words], [2.4, 7.0], 24, 17)
    objs = [t]
    yy = Y0 + t['rowH'][0]
    for i, ic in enumerate(icons[:len(words)]):
        rh = t['rowH'][i + 1]
        sz = min(0.7, rh - 0.1)
        objs.append(icon_img(ic, round(sz, 2), X0 + 0.1, yy + (rh - sz) / 2))
        yy += rh
    d.add('Words we use today', objs, words_script(s))


def keep_script(s):
    base = paragraphs(s['keep_note'])
    if s.get('keep_returns') is False:
        return base
    return base + f'\n\nWe began with this question: {s["question"]} Before you go, say in one sentence what you can now say about it.'


def add_keep(d):
    s = d.s
    objs = [text(X0, Y0 + 0.05, 7.4, 0.7, 'What you keep from today', 30, 24, bold=True)]
    objs.append(K.line_obj(X0, Y0 + 0.85, X0 + 7.4, Y0 + 0.85, color='111111', w=2.0))
    objs.append(paras(X0, Y0 + 1.0, 7.4, 1.6, [s['keep']], 24, 18, gap=0.2))
    if s.get('keep_returns') is not False:
        objs.append(text(X0, Y0 + 2.65, 7.4, 0.4, 'Our question today', 20, 16, bold=True, color=B.RED))
        objs.append(text(X0, Y0 + 3.05, 7.4, 0.75, s['question'], 22, 16, italic=True, color=B.BODY))
    objs.append(text(X0, Y0 + 3.9, 7.4, 0.4, s.get('next_label', 'Next session'), 20, 16, bold=True, color=B.RED))
    objs.append(text(X0, Y0 + 4.3, 7.4, 0.65, s['next'], 20, 15, color=B.BODY))
    if s.get('keep_visual'):
        objs.append(img(s['keep_visual'], 8.5, Y0 + 0.1, 4.1, 4.5, 'What you keep from today'))
    else:
        objs.append(icon_img('folder', 3.0, 9.4, 2.5, 'folder'))
    d.add(s.get('keep_title', 'Save it, and bring one question to the next session'), objs, keep_script(s), section='Close')



# ------------------------------------------------------------------ build
def build_spec(sess):
    d = Deck(sess)
    add_cover(d)
    add_outcome(d)
    add_plan(d)
    answers = [x for x in sess['slides'] if x['title'].startswith('Answers to')]
    if sess.get('recall'):
        add_recall(d)
        for a in answers:   # the model answers go straight after the questions
            d.add(a['title'], KINDS[a['kind']](d, a), a['notes'])
    add_words(d)
    d.section = 'Concepts'
    for sl in sess['slides']:
        if sl in answers and sess.get('recall'):
            continue
        kind = sl['kind']
        if kind not in KINDS:
            raise ValueError(f'unknown slide kind {kind}')
        if sl.get('section'):
            d.section = sl['section']
        objs = KINDS[kind](d, sl)
        if kind == 'divider':
            d.slides.append({'layout': 'dark', 'section': sl.get('section', d.section), 'title': {'text': K.balance(sl['title'], 44, 'bold', 11.0), 'size': 44, 'lead': 48.0},
                             'title_raw': None, 'objects': [text(X0, 4.3, 11.6, 1.6, sl['lead'], 26, 20, color=B.GOLD)], 'notes': paragraphs(sl['notes'])})
            continue
        d.add(sl['title'], objs, sl['notes'])
    add_keep(d)
    import re as _re
    out = OUT_DIR / (f'{sess["num"]:02d} - ' + _re.sub(r'[:/\\?*"<>|]', '', sess['short_title']) + '.pptx')
    return {'out': str(out), 'title': f'Session {sess["num"]}: {sess["title"]}', 'subject': COURSE,
            'footer': f'KLAi  |  AI and Data Science  |  Session {sess["num"]}: {sess["short_title"]}'[:90],
            'fonts': {'head': B.HEAD_FONT, 'body': B.BODY_FONT, 'mono': B.MONO_FONT}, 'brand': {}, 'logo': _logo(), 'slides': d.slides}


def load(num):
    p = BUILD / 'content' / f's{num:02d}.py'
    spec = importlib.util.spec_from_file_location(f's{num:02d}', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.build()


def render(spec):
    SPEC_DIR.mkdir(parents=True, exist_ok=True)
    p = SPEC_DIR / (Path(spec['out']).stem.replace(' ', '_') + '.json')
    for s in spec['slides']:
        if s.get('title_raw') is not None and s['title'] is None:
            s['title'] = {'text': s['title_raw'], 'size': 48, 'lead': 53.0}
    p.write_text(json.dumps(spec))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PPTX_SKILL_SCRIPTS=PPTX_SKILL_SCRIPTS)
    r = subprocess.run(['node', str(HERE / 'render_deck.js'), str(p)], capture_output=True, text=True, env=env, cwd=str(HERE))
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return r.stdout.strip()


def main(argv):
    nums = [int(a) for a in argv if a.isdigit()] or sorted(int(p.stem[1:]) for p in (BUILD / 'content').glob('s[0-9][0-9].py'))
    bad = 0
    for n in nums:
        try:
            sess = load(n)
            spec = build_spec(sess)
            print(n, len(spec['slides']), 'slides', render(spec))
        except Exception as e:  # keep going so every deck reports
            bad += 1
            print('FAILED', n, type(e).__name__, str(e)[:600])
    if figkit.SMALL_TEXT:
        by = {}
        for name, txt, size in figkit.SMALL_TEXT:
            by.setdefault(name, []).append(size)
        print('Figures with text under 14 pt:', {k: min(v) for k, v in by.items()})
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
