"""Slide geometry, text measurement and code highlighting for the camp decks.

Every text box is measured with the real Lato and DejaVu Sans Mono files, with about 6 per cent slack, so the
renderer does not rely on PowerPoint's shrink-to-fit. A box that cannot hold its text at the minimum size raises
FitError, and the content is shortened instead of shrunk.
"""
import re
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageFont

import brand as B

FONTS = {
    'regular': str(B.FONT_DIR / 'Lato-Regular.ttf'),
    'bold': str(B.FONT_DIR / 'Lato-Bold.ttf'),
    'black': str(B.FONT_DIR / 'Lato-Black.ttf'),
    'italic': str(B.FONT_DIR / 'Lato-Italic.ttf'),
    'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
}
SLACK = 0.94          # text may fill 94 % of the box width
MONO_EM = 0.602       # DejaVu Sans Mono advance; Consolas is narrower, so this is conservative


class FitError(Exception):
    pass


@lru_cache(maxsize=None)
def _font(kind, px):
    return ImageFont.truetype(FONTS[kind], px)


def width_in(text, size, kind='regular'):
    """Width of one line of text in inches at `size` pt."""
    f = _font(kind, 200)
    return f.getlength(text) / 200.0 * size / 72.0


def wrap(text, size, kind, max_w):
    """Word-wrap text to max_w inches; honours explicit newlines. Returns a list of lines."""
    out = []
    lim = max_w * SLACK
    for para in str(text).split('\n'):
        words = para.split(' ')
        cur = ''
        for w in words:
            t = (cur + ' ' + w) if cur else w
            if width_in(t, size, kind) <= lim or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def fit_lines(text, kind, max_w, max_h, size_max, size_min, lead=1.2, step=1.0):
    """Largest size in [size_min, size_max] such that wrapped text fits the box. Returns (size, lines)."""
    s = size_max
    while s >= size_min - 1e-6:
        lines = wrap(text, s, kind, max_w)
        if len(lines) * s * lead / 72.0 <= max_h * 0.98 and all(width_in(l, s, kind) <= max_w for l in lines):
            return s, lines
        s -= step
    raise FitError(f'text does not fit {max_w:.2f}x{max_h:.2f} in at {size_min} pt: {str(text)[:70]!r}')


def fit_paragraphs(paras, kind, max_w, max_h, size_max, size_min, lead=1.2, gap=0.14, step=1.0):
    """Several paragraphs with a gap (inches) between them. Returns (size, [lines per paragraph])."""
    s = size_max
    while s >= size_min - 1e-6:
        blocks = [wrap(p, s, kind, max_w) for p in paras]
        h = sum(len(b) for b in blocks) * s * lead / 72.0 + gap * (len(paras) - 1)
        if h <= max_h * 0.98:
            return s, blocks
        s -= step
    raise FitError(f'paragraphs do not fit {max_w:.2f}x{max_h:.2f} in at {size_min} pt: {str(paras[0])[:60]!r}')


# ---------------------------------------------------------------- spec objects
def balance(text, size, kind, w):
    """Insert one line break so a two-line text has two similar lines (spaces only, never at a hyphen)."""
    if '\n' in text or len(wrap(text, size, kind, w)) != 2:
        return text
    ws = text.split(' ')
    best = min(range(1, len(ws)), key=lambda i: max(width_in(' '.join(ws[:i]), size, kind), width_in(' '.join(ws[i:]), size, kind)))
    return ' '.join(ws[:best]) + '\n' + ' '.join(ws[best:])


def title_obj(text, w=11.9, h=1.15, size_max=38, size_min=28):
    s, lines = fit_lines(text, 'bold', w, h, size_max, size_min, lead=1.12)
    if len(lines) == 2 and '\n' not in text:
        ws = text.split(' ')
        best = min(range(1, len(ws)), key=lambda i: max(width_in(' '.join(ws[:i]), s, 'bold'), width_in(' '.join(ws[i:]), s, 'bold')))
        text = ' '.join(ws[:best]) + '\n' + ' '.join(ws[best:])
    return {'text': text, 'size': s, 'lead': round(s * 1.12, 1)}


def text_obj(x, y, w, h, text=None, runs=None, size=20, bold=False, italic=False, color=B.INK, font=None, align='left', valign='top',
             lead=1.2, para=0):
    o = {'type': 'text', 'x': x, 'y': y, 'w': w, 'h': h, 'size': size, 'bold': bold, 'italic': italic, 'color': color.lstrip('#'), 'align': align,
         'valign': valign, 'lead': round(size * lead, 1)}
    if font:
        o['font'] = font
    if para:
        o['para'] = para
    if runs is not None:
        o['runs'] = runs
    else:
        o['text'] = text
    return o


def fitted_text(x, y, w, h, text, kind='regular', size_max=24, size_min=18, color=B.INK, bold=False, italic=False, lead=1.2, align='left',
                valign='top'):
    s, lines = fit_lines(text, 'bold' if bold else ('italic' if italic else kind), w, h, size_max, size_min, lead=lead)
    # the box wraps the text itself; the size was chosen so that the measured wrap fits
    return text_obj(x, y, w, h, text=str(text), size=s, bold=bold, italic=italic, color=color, lead=lead, align=align, valign=valign), s


def fitted_paras(x, y, w, h, paras, kind='regular', size_max=24, size_min=18, color=B.INK, lead=1.2, gap=0.14, bold=False):
    s, blocks = fit_paragraphs(paras, 'bold' if bold else kind, w, h, size_max, size_min, lead=lead, gap=gap)
    runs = []
    for i, p in enumerate(paras):
        runs.append({'text': str(p), 'o': {'breakLine': i < len(paras) - 1, 'color': color.lstrip('#'), 'bold': bold}})
    o = text_obj(x, y, w, h, runs=runs, size=s, color=color, lead=lead, para=round(gap * 72, 1))
    return o, s


def rect_obj(x, y, w, h, fill=None, line=None, line_w=1.0, radius=0):
    o = {'type': 'rect', 'x': x, 'y': y, 'w': w, 'h': h}
    if fill:
        o['fill'] = fill.lstrip('#')
    if line:
        o['line'] = line.lstrip('#')
        o['lineW'] = line_w
    if radius:
        o['radius'] = radius
    return o


def line_obj(x1, y1, x2, y2, color=B.HAIR, w=1.0, dash=False):
    return {'type': 'line', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color.lstrip('#'), 'w': w, 'dash': dash}


def image_obj(path, x, y, w, h, alt='', fit=True, align='center'):
    """Place an image inside the box, keeping its proportions."""
    path = str(path)
    if fit:
        with Image.open(path) as im:
            iw, ih = im.size
        sc = min(w / iw, h / ih)
        pw, ph = iw * sc, ih * sc
        px = x + (w - pw) / 2 if align == 'center' else (x if align == 'left' else x + w - pw)
        py = y + (h - ph) / 2
        return {'type': 'image', 'path': path, 'x': px, 'y': py, 'w': pw, 'h': ph, 'alt': alt}
    return {'type': 'image', 'path': path, 'x': x, 'y': y, 'w': w, 'h': h, 'alt': alt}


# ---------------------------------------------------------------- code
KEYWORDS = {'def', 'if', 'else', 'elif', 'for', 'in', 'return', 'import', 'from', 'as', 'and', 'or', 'not', 'while', 'assert', 'try', 'except',
            'with', 'True', 'False', 'None', 'class', 'lambda', 'pass', 'break', 'continue'}
_TOK = re.compile(r'(#.*$)|("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|(\b[A-Za-z_][A-Za-z0-9_]*\b)|(\s+)|(.)')


def code_runs(code, color='FFFFFF'):
    """Syntax-coloured runs for a black panel: keywords bold, strings gold, comments grey italic."""
    runs = []
    lines = code.rstrip('\n').split('\n')
    for li, line in enumerate(lines):
        parts = []
        for m in _TOK.finditer(line):
            com, st, word, ws, other = m.groups()
            if com:
                parts.append((com, {'color': '9A9A9A', 'italic': True}))
            elif st:
                parts.append((st, {'color': 'E0BE36'}))
            elif word:
                parts.append((word, {'color': color, 'bold': True} if word in KEYWORDS else {'color': color}))
            else:
                parts.append((m.group(0), {'color': color}))
        # merge neighbours with identical options
        merged = []
        for t, o in parts:
            if merged and merged[-1][1] == o:
                merged[-1] = (merged[-1][0] + t, o)
            else:
                merged.append((t, o))
        if not merged:
            merged = [(' ', {'color': color})]
        for ri, (t, o) in enumerate(merged):
            oo = dict(o)
            if ri == len(merged) - 1 and li < len(lines) - 1:
                oo['breakLine'] = True
            runs.append({'text': t, 'o': oo})
    return runs


def code_extent(code, size):
    lines = code.rstrip('\n').split('\n')
    longest = max(len(l) for l in lines)
    return longest * MONO_EM * size / 72.0, len(lines) * size * 1.3 / 72.0


def code_panel(code, x, y, w, h, size_max=22, size_min=16, pad=0.22):
    """A black panel with syntax-coloured code, sized to fit. Returns (objects, size) or raises FitError."""
    s = size_max
    while s >= size_min - 1e-6:
        cw, ch = code_extent(code, s)
        if cw <= (w - 2 * pad) * SLACK and ch <= (h - 2 * pad):
            panel_h = min(h, ch + 2 * pad + 0.04)
            objs = [rect_obj(x, y, w, panel_h, fill='111111', radius=0.08),
                    text_obj(x + pad, y + pad, w - 2 * pad, panel_h - 2 * pad, runs=code_runs(code), size=s, font=B.MONO_FONT, color='FFFFFF', lead=1.3)]
            return objs, s, panel_h
        s -= 1
    raise FitError(f'code does not fit {w:.2f}x{h:.2f} at {size_min} pt')


def output_panel(lines, x, y, w, h, size_max=20, size_min=15, pad=0.2):
    """A white panel with a hairline border for program output (monospaced)."""
    text = '\n'.join(lines)
    s = size_max
    while s >= size_min - 1e-6:
        cw, ch = code_extent(text, s)
        if cw <= (w - 2 * pad) * SLACK and ch <= (h - 2 * pad):
            ph = min(h, ch + 2 * pad + 0.04)
            return [rect_obj(x, y, w, ph, fill='FFFFFF', line=B.INK, line_w=1.25, radius=0.08),
                    text_obj(x + pad, y + pad, w - 2 * pad, ph - 2 * pad, text=text, size=s, font=B.MONO_FONT, color=B.INK, lead=1.3)], s, ph
        s -= 1
    raise FitError('output does not fit')


# ---------------------------------------------------------------- wrapping long code lines for display
def _bracket_pairs(line):
    """Matching bracket pairs outside string literals: list of (open_index, close_index, depth)."""
    pairs, stack, quote, i = [], [], None, 0
    while i < len(line):
        c = line[i]
        if quote:
            if c == '\\':
                i += 1
            elif c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c == '#':
            break
        elif c in '([{':
            stack.append((i, len(stack)))
        elif c in ')]}' and stack:
            o, d = stack.pop()
            pairs.append((o, i, d))
        i += 1
    return pairs


def _split_commas(inner):
    """Split on top-level commas outside strings and nested brackets."""
    items, depth, quote, cur, i = [], 0, None, '', 0
    while i < len(inner):
        c = inner[i]
        cur += c
        if quote:
            if c == '\\' and i + 1 < len(inner):
                i += 1
                cur += inner[i]
            elif c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == ',' and depth == 0:
            items.append(cur.strip().rstrip(',').strip())
            cur = ''
        i += 1
    if cur.strip():
        items.append(cur.strip())
    return items


def _chain_split(line, width):
    """name = a.b().c() becomes name = ( a.b() / .c() ) with the chain broken before each method call."""
    indent = len(line) - len(line.lstrip())
    eq = None
    depth, quote = 0, None
    for i, c in enumerate(line):
        if quote:
            if c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == '=' and depth == 0 and line[i - 1:i + 2].strip() == '=' and line[i + 1:i + 2] != '=':
            eq = i
            break
    if eq is None:
        return None
    lhs, rhs = line[:eq + 1], line[eq + 1:].strip()
    cuts, depth, quote = [], 0, None
    for i, c in enumerate(rhs):
        if quote:
            if c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == '.' and depth == 0 and i > 0 and rhs[i - 1] in ')]':
            cuts.append(i)
    if len(cuts) < 2:
        return None
    segs = [rhs[:cuts[0]]] + [rhs[cuts[k]:cuts[k + 1] if k + 1 < len(cuts) else len(rhs)] for k in range(len(cuts))]
    pad = ' ' * (indent + 4)
    out = [lhs + ' ('] + [pad + sg for sg in segs] + [' ' * indent + ')']
    return out if max(len(x) for x in out) <= width else None


def wrap_line(line, width):
    """Break a long line inside its last top-level bracket pair, black style, or as a method chain. Still valid Python."""
    if len(line) <= width or line.lstrip().startswith('#'):
        return [line]
    indent = len(line) - len(line.lstrip())
    chain = _chain_split(line, width)
    if chain:
        return chain
    cands = [(o, c) for o, c, d in _bracket_pairs(line) if d == 0 and o < width - 2 and c - o > 1]
    result = None
    if cands:
        o, c = cands[-1]
        head, inner, tail = line[:o + 1], line[o + 1:c], line[c:]
        pad = ' ' * (indent + 4)
        items = _split_commas(inner)
        chunks, cur = [], ''
        for k, it in enumerate(items):
            piece = it + (',' if k < len(items) - 1 else '')
            if cur and len(pad) + len(cur) + 1 + len(piece) > width:
                chunks.append(cur)
                cur = piece
            else:
                cur = (cur + ' ' + piece) if cur else piece
        chunks.append(cur)
        result = [head]
        for ch in chunks:
            result.extend(wrap_line(pad + ch, width))
        result.append(' ' * indent + tail)
    return result or [line]


def wrap_code(code, width=62):
    out = []
    for ln in code.rstrip('\n').split('\n'):
        out.extend(wrap_line(ln, width))
    return '\n'.join(out)
