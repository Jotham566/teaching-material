# -*- coding: utf-8 -*-
"""Slide primitives for the IUEA ML teaching decks (python-pptx)."""
import os

from pptx import Presentation
from pptx.util import Inches as In, Pt, Emu
from pptx.dml.color import RGBColor as C
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------- palette
INK    = C(0x1C, 0x31, 0x44)   # deep slate — dominant
INK2   = C(0x2A, 0x45, 0x5E)   # lighter slate
PAPER  = C(0xFF, 0xFF, 0xFF)
STEEL  = C(0xE8, 0xED, 0xF2)   # pale card fill
STEEL2 = C(0xF4, 0xF7, 0xFA)
ORANGE = C(0xE4, 0x57, 0x2E)   # safety orange — accent
TEAL   = C(0x2E, 0x7D, 0x6F)   # verified / correct
MUTED  = C(0x6B, 0x7A, 0x8A)
CODEBG = C(0x16, 0x24, 0x33)
CODEFG = C(0xD8, 0xE3, 0xEC)

HEAD = "Cambria"
BODY = "Calibri"
MONO = "Courier New"

W, H = 13.333, 7.5
M = 0.75          # margin

# ---------------------------------------------------------------- type scale
# Room 106 seats about a hundred and the back row is a long way from the
# screen. The decks were originally set at 10-13pt body, which reads fine on
# a laptop and is unreadable from row twelve.
#
# The ramp below lifts small text hard and leaves display text alone. A flat
# multiplier would have blown the headline slides apart: 44pt x 1.4 is 62pt,
# which does not fit the title box and would not be an improvement anyway,
# because the headlines were never the problem.
#
#   10pt -> 13.2    13pt -> 17.2    17pt -> 21.4    24pt -> 26.9
#   11pt -> 14.5    14pt -> 18.5    19pt -> 23.1    30pt and up unchanged
#   12pt -> 15.8    15pt -> 19.7    21pt -> 24.6
#
# It applies in exactly two places, tb() and theight(), which is what keeps
# the shrink-to-fit loops honest: they measure with the same ramp that draws,
# so a block that no longer fits shrinks or gets reported, instead of
# silently running off the bottom of the slide.
SMALL, LARGE = 13.0, 30.0     # ramp endpoints
LIFT = 1.32                   # multiplier at SMALL and below


# The shrink-to-fit loops stop here. These are AUTHORED points, so the floor
# renders at _scaled(11) = 14.5pt, which is about the smallest thing worth
# projecting to a hundred seats. A slide that cannot hold its content at the
# floor is named in TIGHT and counted by validation/overflow_scan.py, and the
# fix for those is fewer words: the old floors let a dense slide quietly drop
# to 9pt, which is how the decks ended up unreadable from the back.
FLOOR = 11.0
CODE_FLOOR = 10.0     # Courier is narrow and code lines are short
# A few slides genuinely cannot hold their content at the floor. Running off
# the bottom of the screen is worse than one size down, so those drop to the
# hard floor AND get named in TIGHT, which the deck builders print. The list
# is the to-do list for cutting words; it should not be treated as normal.
HARD_FLOOR = 9.5
TIGHT = []


def _tight(kind, fs, over):
    TIGHT.append((_CTX.get("deck", "?"), _CTX.get("slide", 0), kind,
                  round(_scaled(fs), 1), round(over, 2)))


def _shrink(fs, need_fn, avail, kind, step=0.5):
    """Shrink a block to fit, preferring the readable floor.

    need_fn(fs) returns the height the block wants at that authored size.
    Stops at FLOOR if it can; only goes below when the alternative is text
    off the slide, and reports every time it does.
    """
    while fs > FLOOR and need_fn(fs) > avail:
        fs -= step
    if need_fn(fs) > avail:
        while fs > HARD_FLOOR and need_fn(fs) > avail:
            fs -= step
        _tight(kind, fs, need_fn(fs) - avail)
    return fs


def _scaled(size):
    """Rendered point size for an authored point size."""
    s = float(size)
    if s >= LARGE:
        return s
    if s <= SMALL:
        return s * LIFT
    f = LIFT + (1.0 - LIFT) * (s - SMALL) / (LARGE - SMALL)
    return s * f


def deck():
    p = Presentation()
    p.slide_width = In(W)
    p.slide_height = In(H)
    return p


def _blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _bg(slide, prs, colour):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, In(W), In(H))
    r.fill.solid(); r.fill.fore_color.rgb = colour
    r.line.fill.background()
    r.shadow.inherit = False
    return r


def tb(slide, x, y, w, h, text, size=16, bold=False, colour=INK, font=BODY,
       align=PP_ALIGN.LEFT, italic=False, anchor=MSO_ANCHOR.TOP, space_after=6,
       line=None):
    box = slide.shapes.add_textbox(In(x), In(y), In(w), In(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    size = _scaled(size)
    lines = text.split("\n") if isinstance(text, str) else text
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space_after)
        if line:
            para.line_spacing = line
        run = para.add_run(); run.text = ln
        f = run.font
        f.name = font; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = colour
    return box


def nlines(text, w_in, size):
    """Estimated wrapped line count. Calibrated against LibreOffice renders:
    usable characters per inch is about 166/pt for Calibri."""
    if not text:
        return 1
    cpi = 166.0 / float(size)
    per = max(8.0, w_in * cpi)
    total = 0
    for seg in str(text).split("\n"):
        total += max(1, int(len(seg) / per + 0.999))
    return total


# A line-spacing MULTIPLE is not applied to the point size. It is applied to
# the font's line box, which for Calibri is ascender + descender + line gap =
# about 1.21 em. So a 20pt line at spacing 1.25 occupies 20 x 1.25 x 1.21 pt,
# not 20 x 1.25. The old theight ignored this and under-measured every block
# by a fifth. At 13pt that was 0.05in a line and the padding absorbed it; at
# 20pt it is 0.08in a line, and a four-line paragraph lands on top of the one
# below it. That is exactly what the first rendered check caught.
#
# Verified against LibreOffice renders at 90dpi: 19.5pt at 1.25 measured
# 0.41in a line (nominal 0.339, ratio 1.21) and 21.5pt at 1.24 measured
# 0.444in (nominal 0.370, ratio 1.20).
LINEBOX = {"Calibri": 1.21, "Cambria": 1.24, "Courier New": 1.13}


# Three per cent of slack on every measured block. The line-box model above
# is close but not exact, and it is least exact at tight leads: a row set at
# lead 1.14 rendered about 1.5em rather than the 1.38em predicted, which put
# the last row of a panel on the panel's own bottom edge. Rounding the wrong
# way costs nothing; rounding this way costs a clipped line.
SAFETY = 1.03


def theight(text, w_in, size, lead=1.20, font=BODY):
    """Estimated rendered height in inches for a wrapped text block.

    Takes the AUTHORED size and applies the same ramp tb() draws with, so
    callers keep passing the sizes they wrote and still measure the truth.
    Pass the same `lead` you pass tb() as `line`.
    """
    s = _scaled(size)
    return (nlines(text, w_in, s) * (s * lead * LINEBOX.get(font, 1.21) / 72.0)
            * SAFETY)


def card(slide, x, y, w, h, fill=STEEL, radius=True, shadow=True):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        In(x), In(y), In(w), In(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    if radius:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    if not shadow:
        shp.shadow.inherit = False
    return shp


def chip(slide, x, y, text, fill=ORANGE, fg=PAPER, w=None, size=11, dia=0.42):
    """Small pill or numbered circle."""
    size = _scaled(size)
    if w is None:
        shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, In(x), In(y), In(dia), In(dia))
    else:
        # widen to fit the label rather than clipping it. size is the scaled
        # one here, so a lifted chip label widens its pill with it.
        w = max(w, len(text) * size * 0.0080 + 0.40)
        shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, In(x), In(y), In(w), In(dia))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    if not text or text == "•":
        return shp                      # a solid dot reads better than a tiny glyph
    tf = shp.text_frame
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = BODY; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = fg
    return shp


# Lecturer material is collected here and written to a separate teaching guide.
# The deck itself carries ONLY the student-facing explanation, because the decks
# are shared with students after each session.
LECTURER = []
_CTX = {"deck": "", "slide": 0, "title": ""}


def notes_context(deck_name):
    _CTX["deck"] = deck_name
    _CTX["slide"] = 0


def notes(slide, text):
    """Split on the TO TEACH marker. Student explanation goes on the slide;
    lecturer stage directions are held for the teaching guide."""
    # Slides without notes (and repeated/out-of-order notes calls) must not
    # shift the lecturer guide away from the actual presentation position.
    slides = slide.part.package.main_document_part.presentation.slides
    _CTX["slide"] = next(i for i, candidate in enumerate(slides, 1)
                         if candidate.slide_id == slide.slide_id)
    student, lect = text, ""
    # Match ANY "TO TEACH" variant. A marker that fails to match publishes an
    # answer key to students, so this is deliberately permissive.
    import re as _re
    m = _re.search(r"TO\s+TEACH\b[^\n:]{0,40}?[::—–-]?\s*", text)
    if m:
        student = text[:m.start()].rstrip()
        lect = text[m.end():].strip()
    title = ""
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            t = sh.text_frame.text.strip()
            if 8 < len(t) < 90 and "\n" not in t:
                title = t
                break
    if lect:
        LECTURER.append({"deck": _CTX["deck"], "slide": _CTX["slide"],
                         "title": title, "text": lect})
    slide.notes_slide.notes_text_frame.text = student.strip()


# ---------------------------------------------------------------- slide types
def s_title(prs, code, title, subtitle, week_label, foot):
    s = _blank(prs); _bg(s, prs, INK)
    chip(s, M, 1.05, code, fill=ORANGE, w=1.35, size=12)
    tb(s, M, 1.75, W - 2 * M, 2.2, title, size=44, bold=True, colour=PAPER, font=HEAD, line=1.05)
    tb(s, M, 4.05, W - 2 * M, 0.6, subtitle, size=19, colour=C(0xA8, 0xBC, 0xCE))
    tb(s, M, 5.85, 6.0, 0.4, week_label, size=13, bold=True, colour=ORANGE)
    tb(s, M, 6.25, 9.0, 0.4, foot, size=11, colour=C(0x7E, 0x93, 0xA6))
    return s


def s_question(prs, kicker, question, under):
    s = _blank(prs); _bg(s, prs, INK2)
    tb(s, M, 1.15, W - 2 * M, 0.4, kicker, size=13, bold=True, colour=ORANGE)
    tb(s, M, 1.85, W - 2 * M, 3.0, question, size=34, italic=True, colour=PAPER,
       font=HEAD, line=1.15)
    tb(s, M, 5.35, W - 2 * M, 1.2, under, size=15, colour=C(0xB8, 0xC9, 0xD8), line=1.2)
    return s


def s_head(s, title, kicker=None):
    """Returns the y at which body content may start — wrap-aware."""
    y = 0.62
    if kicker:
        tb(s, M, y, W - 2 * M, 0.32, kicker, size=12, bold=True, colour=ORANGE)
        y += 0.42
    # ~56 characters of 32pt Cambria fit the usable width
    lines = max(1, int(len(title) / 56.0 + 0.999))
    tb(s, M, y, W - 2 * M, 0.55 * lines + 0.3, title, size=32, bold=True, colour=INK,
       font=HEAD, line=1.0)
    return y + 0.52 + lines * 0.53


def s_points(prs, title, items, kicker=None, numbered=True):
    """items: list of (header, body)"""
    s = _blank(prs)
    y = s_head(s, title, kicker)
    n = len(items)
    avail = H - y - 0.62
    bw = W - 2 * M - 1.3
    # Each card needs a header line plus its wrapped body. Give up the gap
    # first, then body size, then header room, until the whole stack fits the
    # slide; a fixed per-card floor would push the last card off the bottom.
    fs, gap, hdh, hsz = 13.0, 0.26, 0.72, 17

    def _need(fs, hdh):
        return [hdh + theight(bd, bw, fs, 1.16) for _, bd in items]

    while True:
        if sum(_need(fs, hdh)) + gap * (n - 1) <= avail:
            break
        if gap > 0.11:
            gap -= 0.05
        elif fs > FLOOR:
            fs -= 0.5
        elif hdh > 0.58:
            hdh, hsz = 0.58, 15
        else:
            break
    need = _need(fs, hdh)
    total_need = sum(need) + gap * (n - 1)
    if total_need <= avail:
        slack = (avail - total_need) / n
        heights = [x + slack for x in need]
    else:                                # still tight: shrink proportionally
        k = (avail - gap * (n - 1)) / sum(need)
        heights = [x * k for x in need]
    top = y
    for i, (hd, bd) in enumerate(items):
        ch = heights[i]
        card(s, M, top, W - 2 * M, ch, fill=STEEL2)
        if numbered:
            chip(s, M + 0.28, top + (ch - 0.42) / 2, str(i + 1), fill=ORANGE)
        else:
            # a small marker dot; a blank 0.42in circle reads as a missing glyph
            chip(s, M + 0.39, top + (ch - 0.20) / 2, "", fill=TEAL, dia=0.20)
        tb(s, M + 0.95, top + 0.13, W - 2 * M - 1.3, hdh - 0.20, hd,
           size=hsz, bold=True, colour=INK)
        tb(s, M + 0.95, top + hdh - 0.16, W - 2 * M - 1.3, ch - hdh + 0.06, bd,
           size=fs, colour=C(0x3C, 0x4E, 0x5E), line=1.16)
        top += ch + gap
    return s


def s_split(prs, title, left_head, left_body, right_head, right_rows, kicker=None):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    cw = (W - 2 * M - 0.45) / 2
    # Measure the head: a two-line heading in a fixed 0.4in box overlapped
    # the first body paragraph, which is pinned below it.
    lh_h = max(0.40, theight(left_head, cw, 17, 1.16))
    tb(s, M, y, cw, lh_h + 0.04, left_head, size=17, bold=True, colour=INK)

    # LEFT: shrink the body until its measured height fits the column, so a
    # trailing paragraph (typically the STRETCH task) can never fall off.
    lavail = H - (y + lh_h + 0.12) - 0.55
    paras = [q for q in str(left_body).split("\n") if q.strip() != ""]
    lfs, gap = 14.0, 0.11
    def lneed(fs, gap):
        return sum(theight(q, cw, fs, 1.25) + gap for q in paras)
    while lfs > FLOOR and lneed(lfs, gap) > lavail:
        lfs -= 0.5
        if lfs <= 12 and gap > 0.05:
            gap = 0.06
    if lneed(lfs, gap) > lavail:
        while lfs > HARD_FLOOR and lneed(lfs, gap) > lavail:
            lfs -= 0.5
        _tight('split left', lfs, lneed(lfs, gap) - lavail)
    lty = y + lh_h + 0.12
    for q in paras:
        h = theight(q, cw, lfs, 1.25)
        tb(s, M, lty, cw, h + 0.05, q, size=lfs, colour=C(0x3C, 0x4E, 0x5E), line=1.25)
        lty += h + gap

    # RIGHT: measure each row's wrapped height so a wrapped row does not eat
    # the gap below it and collide with the next one.
    # The right panels were authored one string per RENDERED LINE, with bare
    # "" strings as vertical spacers. That only ever matched one font size:
    # this layout wraps rows itself, so the manual breaks now fall in the
    # wrong places, and each spacer costs a whole row gap. Normalising here
    # rather than in fourteen call sites keeps the fix in one place.
    #
    # A row starting with two or more spaces continues the row above it. A
    # blank row becomes a little extra space before the row that follows.
    # Some panels indent their continuation lines and some do not, so the
    # test that actually works is punctuation: a row that does not end a
    # sentence is being continued by the row under it. The 200-character
    # ceiling stops a genuinely short unpunctuated row from swallowing the
    # rest of the panel.
    _rows, _extra = [], {}
    for _r in right_rows:
        _t = str(_r)
        if _t.strip() == "":
            if _rows:
                _extra[len(_rows)] = 0.14
            continue
        _t = " ".join(_t.split())
        _open = bool(_rows) and (
            not _rows[-1].rstrip().endswith((".", ":", "?", "!", ";"))
            and len(_rows[-1]) + len(_t) < 200)
        if _rows and (str(_r).startswith("  ") or _open):
            _rows[-1] = _rows[-1].rstrip() + " " + _t
        else:
            _rows.append(_t)
    right_rows = _rows
    _slack = sum(_extra.values())

    rx = M + cw + 0.45
    # The card used to stop at H-0.84 while the text was budgeted to H-0.78,
    # so the last row was allowed to sit just past the panel it belongs to.
    # The card now runs to H-0.55 and the text is budgeted to stop inside it,
    # which is also where the room for the bigger type came from.
    card(s, rx, y - 0.12, cw, H - y - 0.43, fill=STEEL)
    rhh = max(0.40, theight(right_head, cw - 0.6, 15, 1.16))
    tb(s, rx + 0.3, y + 0.08, cw - 0.6, rhh + 0.04, right_head, size=15,
       bold=True, colour=INK)
    tw = cw - 0.6
    rtop = y + 0.10 + rhh + 0.14
    ravail = (H - 0.82) - rtop     # clearance to the card's own bottom edge
    rfs, rgap = 13.0, 0.10
    def rneed(fs, g):
        return sum(theight(r, tw, fs, 1.14) + g for r in right_rows) + _slack
    while rfs > FLOOR and rneed(rfs, rgap) > ravail:
        rfs -= 0.5
        if rfs <= 11 and rgap > 0.05:
            rgap = 0.05
    if rneed(rfs, rgap) > ravail:
        while rfs > HARD_FLOOR and rneed(rfs, rgap) > ravail:
            rfs -= 0.5
        _tight('split right', rfs, rneed(rfs, rgap) - ravail)
    ty = rtop
    for i, r in enumerate(right_rows):
        ty += _extra.get(i, 0.0)
        h = theight(r, tw, rfs, 1.14)
        tb(s, rx + 0.3, ty, tw, h + 0.05, r, size=rfs, colour=C(0x33, 0x46, 0x57), line=1.14)
        ty += h + rgap
    return s


def s_video(prs, title, channel, vtitle, url, runtime, watch_for, when, kicker="VIDEO"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    card(s, M, y, W - 2 * M, 2.55, fill=INK)
    chip(s, M + 0.35, y + 0.3, when, fill=ORANGE, w=1.9, size=11)
    tb(s, M + 2.45, y + 0.34, 5.0, 0.34, channel, size=13, bold=True, colour=C(0xA8, 0xBC, 0xCE))
    tb(s, M + 0.35, y + 0.95, W - 2 * M - 0.7, 0.8, vtitle, size=21, bold=True,
       colour=PAPER, font=HEAD, line=1.05)
    tb(s, M + 0.35, y + 1.85, W - 2 * M - 0.7, 0.32, url, size=12, colour=C(0x8E, 0xB4, 0xCB),
       font=MONO)
    tb(s, M + 0.35, y + 2.18, W - 2 * M - 0.7, 0.3, "Runtime: " + runtime, size=11,
       colour=C(0x7E, 0x93, 0xA6))
    ty = y + 2.85
    chip(s, M, ty, "WATCH FOR", fill=TEAL, w=1.55, size=11)
    tb(s, M + 1.75, ty + 0.03, W - 2 * M - 1.9, 1.3, watch_for, size=15, colour=INK, line=1.22)
    return s


def s_livecode(prs, title, where, code, mistake, kicker="LIVE CODING"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    # The "open Colab" instruction rides on the kicker row, which is otherwise
    # empty to the right. Putting it on its own row below the title cost 0.6in
    # of the code block and forced the longest listings down to 9pt.
    # chip() widens itself to fit its label, so compute that width first and
    # right-align against it; otherwise a long label runs off the slide.
    # mirror chip()'s own width formula, in the size chip() will actually draw
    _cw = max(3.35, len(where) * _scaled(12) * 0.0080 + 0.40)
    chip(s, W - M - _cw, 0.56, where, fill=ORANGE, w=_cw, size=12)
    # size the code card from the code itself, and shrink the font if it is long
    # EXACT point line spacing, so the card height is deterministic. A spacing
    # multiple is not: LibreOffice derives it from the font's ascent+descent,
    # which for Courier New is well over the point size, and the block overflows.
    n = len(code.split("\n"))
    # Measure the break-it-on-purpose block rather than reserving a flat band
    # for it. Most are two lines, and a fixed reservation was pushing the code
    # font down to 8.5pt on the longest listings, which does not project.
    cw = 3.3
    mw = W - 2 * M - cw - 0.65
    mistake_block = max(0.42, theight(mistake, mw, 13, 1.18) + 0.06)
    avail = H - y - mistake_block - 0.40
    fs = 13.0
    lead = 1.36
    # The card height has to be measured in the size that will actually be
    # DRAWN, so the type ramp goes through this loop too. Courier at 18pt over
    # twelve lines is a tall block, and measuring it unscaled would put the
    # last two lines of code through the bottom of the card.
    while fs > CODE_FLOOR and (0.36 + n * (_scaled(fs) * lead / 72.0)) > avail:
        fs -= 0.5
    lh = _scaled(fs) * lead / 72.0
    ch = min(avail, 0.36 + n * lh)
    card(s, M, y, W - 2 * M, ch, fill=CODEBG, radius=False)
    tb(s, M + 0.32, y + 0.16, W - 2 * M - 0.64, ch - 0.32, code, size=fs, colour=CODEFG,
       font=MONO, line=Pt(_scaled(fs) * lead), space_after=0)
    ty = y + ch + 0.24
    chip(s, M, ty, "NOW BREAK IT ON PURPOSE", fill=TEAL, w=cw, size=11)
    tb(s, M + cw + 0.65, ty + 0.01, mw, mistake_block, mistake,
       size=13, colour=INK, line=1.18)
    return s


def s_challenge(prs, title, brief, questions, kicker="CHALLENGE"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    width = W - 2 * M
    bh = theight(brief, width - 0.64, 15, 1.25) + 0.52
    card(s, M, y, width, bh, fill=STEEL)
    tb(s, M + 0.32, y + 0.22, width - 0.64, bh - 0.40,
       brief, size=15, colour=INK, line=1.25)
    ty = y + bh + 0.30
    cw = (width - 0.4) / 2
    half = (len(questions) + 1) // 2
    groups = (questions[:half], questions[half:])
    needed = max(sum(theight(q, cw, 13, 1.15)+0.18 for q in qs) for qs in groups) if questions else 0
    if ty + needed + 0.52 > H - 0.25:
        # Keep the readable brief intact and put tasks on a continuation.
        s = _blank(prs)
        ty = s_head(s, title + " continued", kicker)
    tb(s, M, ty, width, 0.34, "Work these questions in order", size=14,
       bold=True, colour=ORANGE)
    ty += 0.52
    for col, qs in enumerate(groups):
        yy = ty
        for q in qs:
            h = theight(q, cw, 13, 1.15) + 0.08
            tb(s, M + col*(cw+0.4), yy, cw, h, q, size=13,
               colour=C(0x33, 0x46, 0x57), line=1.15)
            yy += h + 0.10
    return s


def s_closing(prs, headline, body, footer):
    s = _blank(prs); _bg(s, prs, INK)
    tb(s, M, 1.5, W - 2 * M, 0.4, "THE ONE THING TO REMEMBER", size=13, bold=True, colour=ORANGE)
    tb(s, M, 2.15, W - 2 * M, 2.4, headline, size=34, bold=True, colour=PAPER,
       font=HEAD, line=1.1)
    tb(s, M, 4.85, W - 2 * M, 1.3, body, size=16, colour=C(0xB8, 0xC9, 0xD8), line=1.25)
    tb(s, M, 6.5, W - 2 * M, 0.4, footer, size=11, colour=C(0x7E, 0x93, 0xA6))
    return s


# ================================================================
# TEACHING-MATERIAL SLIDE TYPES  (dense enough to revise from)
# ================================================================
def add_fig(slide, path, x, y, max_w, max_h, centre=True):
    """Place an image fitted inside a box, preserving aspect ratio."""
    pic = slide.shapes.add_picture(path, In(x), In(y), width=In(max_w))
    if pic.height > In(max_h):
        scale = In(max_h) / pic.height
        pic.height = In(max_h)
        pic.width = int(pic.width * scale)
    if centre:
        pic.left = In(x) + int((In(max_w) - pic.width) / 2)
        # Centre vertically too. A wide figure fitted by width is much shorter
        # than its box, and pinning it to the top left obvious dead space
        # underneath it.
        pic.top = In(y) + max(0, int((In(max_h) - pic.height) / 2))
    return pic


def s_objectives(prs, objs, week, topic):
    s = _blank(prs)
    tb(s, M, 0.62, W - 2 * M, 0.32, "LEARNING OBJECTIVES", size=12, bold=True, colour=ORANGE)
    tb(s, M, 1.04, W - 2 * M, 0.8, "By the end of today you can…", size=30, bold=True,
       colour=INK, font=HEAD)
    y = 2.05
    n = len(objs)
    rh = min(0.62, (H - y - 0.85) / n)
    for i, o in enumerate(objs):
        chip(s, M, y + 0.03, str(i + 1), fill=INK, dia=0.34, size=10)
        tb(s, M + 0.55, y, W - 2 * M - 0.7, rh, o, size=14.5, colour=C(0x2A, 0x3B, 0x4A), line=1.16)
        y += rh
    tb(s, M, H - 0.72, W - 2 * M, 0.4,
       f"Week {week} · {topic} · nothing here needs prior programming experience",
       size=11, italic=True, colour=MUTED)
    return s


_SEG = {"n": 0}


def seg_reset():
    _SEG["n"] = 0


def s_segment(prs, num, total, title, mins, what):
    """num/total are ignored: segments are numbered contiguously in the order
    they are added, so the label can never disagree with the deck."""
    s = _blank(prs); _bg(s, prs, INK2)
    _SEG["n"] += 1
    tb(s, M, 1.45, W - 2 * M, 0.4, f"SEGMENT {_SEG['n']}", size=13, bold=True, colour=ORANGE)
    tb(s, M, 2.05, W - 2 * M, 1.9, title, size=36, bold=True, colour=PAPER, font=HEAD, line=1.08)
    if mins:
        chip(s, M, 4.35, f"{mins} MINUTES", fill=ORANGE, w=2.0, size=12)
    tb(s, M, 5.15, W - 2 * M, 1.3, what, size=16, colour=C(0xB8, 0xC9, 0xD8), line=1.25)
    return s


def s_profile(prs, name, role, monogram, left_head, left_rows,
              right_head, right_rows, links, close):
    """Introduce the lecturer: credentials on the left, built work on the right.

    left_rows is a list of strings. right_rows is a list of (title, one-line
    description). Every block is measured — the role line wraps, the closing
    band grows with its text, and both columns share one scale so the two
    headings stay on the same line.
    """
    s = _blank(prs)
    y = s_head(s, name, "YOUR LECTURER")

    # monogram, top right, clear of the title
    d = 1.05
    mono = s.shapes.add_shape(MSO_SHAPE.OVAL, In(W - M - d), In(0.66), In(d), In(d))
    mono.fill.solid(); mono.fill.fore_color.rgb = ORANGE
    mono.line.fill.background(); mono.shadow.inherit = False
    mtf = mono.text_frame
    mtf.margin_left = 0; mtf.margin_right = 0
    mtf.margin_top = 0; mtf.margin_bottom = 0
    mp = mtf.paragraphs[0]; mp.alignment = PP_ALIGN.CENTER
    mr = mp.add_run(); mr.text = monogram
    mr.font.name = HEAD; mr.font.size = Pt(30); mr.font.bold = True
    mr.font.color.rgb = PAPER

    rolew = W - 2 * M - 1.45
    roleh = theight(role, rolew, 14, 1.2)
    tb(s, M, y - 0.10, rolew, roleh + 0.06, role, size=14,
       colour=C(0x3C, 0x4E, 0x5E), line=1.2)
    y += roleh + 0.26

    # closing band, sized to its own text so the links never sit under it
    bandw = W - 2 * M - 0.60
    closeh = theight(close, bandw, 11.5, 1.2)
    linkh = theight(links, bandw, 10.5, 1.2)
    band_h = closeh + linkh + 0.30
    band_y = H - band_h - 0.34

    avail = band_y - y - 0.30
    lw = 4.95
    rw = W - 2 * M - lw - 0.55
    rx = M + lw + 0.55

    # The two columns are scaled independently. Their headings are drawn above
    # the bodies, so nothing misaligns, and tying them together made the short
    # column shrink to match the long one for no reason.
    def left_need(k):
        return sum(theight(r, lw - 0.28, 12.5 * k, 1.22) + 0.11 * k for r in left_rows)

    def right_need(k):
        return sum(theight(ti, rw - 0.60, 13.5 * k, 1.16)
                   + theight(ds, rw - 0.60, 12.0 * k, 1.18) + 0.16 + 0.22 * k
                   for ti, ds in right_rows)

    body = avail - 0.40
    # The scale floor was 0.60, which took the body to 7.5pt authored and
    # rendered barely 10.6pt: the smallest text in the whole deck was on the
    # slide introducing the lecturer. 0.84 holds it at about 15pt. If the bio
    # no longer fits at that size the answer is a shorter bio, and TIGHT says
    # so by name.
    SFLOOR = 0.84
    lscale = rscale = 1.0
    while lscale > SFLOOR and left_need(lscale) > body:
        lscale -= 0.02
    while rscale > SFLOOR and right_need(rscale) > body:
        rscale -= 0.02
    if left_need(lscale) > body:
        _tight('profile left', 12.5 * lscale, left_need(lscale) - body)
    if right_need(rscale) > body:
        _tight('profile right', 12.0 * rscale, right_need(rscale) - body)

    tb(s, M, y, lw, 0.34, left_head, size=13.5, bold=True, colour=INK)
    tb(s, rx, y, rw, 0.34, right_head, size=13.5, bold=True, colour=INK)
    cy = y + 0.40

    ly = cy
    for r in left_rows:
        h = theight(r, lw - 0.28, 12.5 * lscale, 1.22)
        chip(s, M + 0.02, ly + 0.06, "", fill=TEAL, dia=0.11)
        tb(s, M + 0.28, ly, lw - 0.28, h + 0.05, r, size=12.5 * lscale,
           colour=C(0x3C, 0x4E, 0x5E), line=1.22)
        ly += h + 0.11 * lscale

    ry = cy
    for ti, ds in right_rows:
        th = theight(ti, rw - 0.60, 13.5 * rscale, 1.16)
        dh = theight(ds, rw - 0.60, 12.0 * rscale, 1.18)
        card(s, rx, ry, rw, th + dh + 0.16, fill=STEEL2)
        tb(s, rx + 0.30, ry + 0.06, rw - 0.60, th + 0.04, ti,
           size=13.5 * rscale, bold=True, colour=INK, line=1.16)
        tb(s, rx + 0.30, ry + 0.06 + th, rw - 0.60, dh + 0.04, ds,
           size=12.0 * rscale, colour=C(0x3C, 0x4E, 0x5E), line=1.18)
        ry += th + dh + 0.16 + 0.22 * rscale

    card(s, M, band_y, W - 2 * M, band_h, fill=STEEL, radius=False, shadow=False)
    tb(s, M + 0.30, band_y + 0.11, bandw, closeh + 0.04, close,
       size=11.5, colour=INK, line=1.2)
    tb(s, M + 0.30, band_y + 0.11 + closeh + 0.06, bandw, linkh + 0.04, links,
       size=10.5, colour=MUTED, line=1.2)
    return s


def s_quiz(prs, week, topic, integrative=False, qr_path=None):
    """End-of-session quiz slide: a QR placeholder and the standing rules.

    The QR image is pasted in on the day, once the Google Form for that week
    exists, so this leaves a labelled square for it rather than inventing a
    link that does not resolve.
    """
    s = _blank(prs); _bg(s, prs, INK2)
    tb(s, M, 0.95, W - 2 * M, 0.34, f"END-OF-SESSION QUIZ  ·  WEEK {week}", size=13,
       bold=True, colour=ORANGE)
    tb(s, M, 1.45, 7.4, 1.5, "Five questions,\nfive minutes",
       size=40, bold=True, colour=PAPER, font=HEAD, line=1.05)
    # The topic line was given a flat 0.9in. At 20.6pt a two-line topic runs
    # into the first bullet, which is what the render showed, so it is
    # measured and the bullets start below whatever it actually needs.
    toph = theight(topic, 7.4, 15, 1.25)
    tb(s, M, 3.15, 7.4, toph + 0.06, topic, size=15, colour=C(0xB8, 0xC9, 0xD8),
       line=1.25)

    # "Your score appears the moment you submit" was not quite true: Forms
    # releases the mark immediately and puts it behind a View score tap.
    # Students who do not know to tap it miss the feedback entirely, which
    # is the part worth five minutes of a three-hour session.
    # These were paragraphs. At projector sizes they no longer fit, and the
    # right fix is fewer words rather than smaller ones: the long version of
    # every rule is on the form itself, in the HOW THIS WORKS block, where a
    # student reads it at their own pace with the thing in front of them. The
    # slide only has to carry what has to be said out loud.
    rows = ['Enter your own Student Registration Number exactly as recorded.',
            "One attempt, from the Google account you are signed in to.",
            'Open for 24 hours from lecturer activation, then it closes.',
            "One per cent each. Tap View score and read the feedback.",
            "Twelve this semester, best ten count. No resits."]
    if integrative:
        rows.insert(1, "Two of the five come from earlier weeks.")
    rw = 7.1
    top = max(3.95, 3.15 + toph + 0.34)
    avail = (H - 0.30) - top
    rfs = _shrink(13.5, lambda f: sum(theight(r, rw, f, 1.22) + 0.12
                                      for r in rows), avail, "quiz rows")
    y = top
    for r in rows:
        h = theight(r, rw, rfs, 1.22)
        chip(s, M + 0.02, y + 0.08, "", fill=ORANGE, dia=0.12)
        tb(s, M + 0.30, y, rw, h + 0.05, r, size=rfs,
           colour=C(0xA8, 0xBC, 0xCE), line=1.22)
        y += h + 0.12

    # The QR itself, or a labelled square if this week's form does not exist
    # yet. A white card sits behind it either way, because a QR needs a light
    # quiet zone and this slide has a dark background.
    qs = 3.05
    qx = W - M - qs
    qy = 1.95
    card(s, qx, qy, qs, qs, fill=PAPER, radius=False, shadow=False)
    if qr_path and os.path.exists(qr_path):
        pad = 0.12
        add_fig(s, qr_path, qx + pad, qy + pad, qs - 2 * pad, qs - 2 * pad)
    else:
        tb(s, qx, qy + qs / 2 - 0.42, qs, 0.4, "QR CODE", size=15, bold=True,
           colour=C(0x8E, 0xA4, 0xB8), align=PP_ALIGN.CENTER)
        tb(s, qx, qy + qs / 2 + 0.02, qs, 0.7, "projected here\non the day",
           size=12, colour=C(0xAA, 0xB8, 0xC6), align=PP_ALIGN.CENTER, line=1.2)
    # The caption here used to offer "no phone? come and use mine". Removed:
    # one lecturer cannot lend a phone to a hundred students, so it was a
    # promise that could not be kept. The dropped-scores rule in the bullets
    # already covers a week somebody cannot get online.
    return s


def s_divider(prs, kicker, title, what):
    """A section divider that carries no segment number.

    Weeks whose session is a test rather than a taught sequence still need to
    break the deck into parts. Using s_segment for that printed "SEGMENT 1"
    against a clock whose first segment was something else entirely.
    """
    s = _blank(prs); _bg(s, prs, INK2)
    tb(s, M, 1.45, W - 2 * M, 0.4, kicker, size=13, bold=True, colour=ORANGE)
    tb(s, M, 2.05, W - 2 * M, 1.9, title, size=36, bold=True, colour=PAPER,
       font=HEAD, line=1.08)
    tb(s, M, 4.55, W - 2 * M, 1.3, what, size=16, colour=C(0xB8, 0xC9, 0xD8),
       line=1.25)
    return s


def s_figure(prs, title, img, caption, kicker=None):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    add_fig(s, img, M, y, W - 2 * M, H - y - 1.02)
    tb(s, M, H - 0.92, W - 2 * M, 0.6, caption, size=12, colour=MUTED, italic=True, line=1.2)
    return s


def s_fig_text(prs, title, img, paras, kicker=None, img_left=True, split=None):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    if split is None:
        # Give a wide figure more of the width. Fitted by width in a narrow
        # column, a two-panel figure ends up a fraction of the height
        # available to it and its labels stop being readable from the back.
        split = 0.55
        try:
            from PIL import Image as _Im
            with _Im.open(img) as _i:
                ar = _i.width / float(_i.height)
            if ar >= 2.6:
                split = 0.70
            elif ar >= 1.9:
                split = 0.63
        except Exception:
            pass
    iw = (W - 2 * M - 0.5) * split
    tw = (W - 2 * M - 0.5) * (1 - split)
    ix = M if img_left else M + tw + 0.5
    tx = M + iw + 0.5 if img_left else M
    add_fig(s, img, ix, y, iw, H - y - 0.75)

    # Measure the wrap with the calibrated helper. The old estimate assumed
    # 15.5 characters per inch against a real 12.3 at 13.5pt, so a paragraph
    # that wrapped to three lines was advanced as though it were two and the
    # next heading landed on top of it.
    sizes = [15.0 if p.startswith("**") else 13.5 for p in paras]
    texts = [p.strip("*") for p in paras]
    gap = 0.20
    avail = H - y - 0.80

    def need(scale, gap):
        return sum(theight(t, tw, sz * scale, 1.22) + gap
                   for t, sz in zip(texts, sizes))

    scale = 1.0
    while scale > 0.74 and need(scale, gap) > avail:
        if gap > 0.11:
            gap -= 0.03
        else:
            scale -= 0.04
    ty = y
    for txt, sz in zip(texts, sizes):
        fs = sz * scale
        h = theight(txt, tw, fs, 1.22)
        tb(s, tx, ty, tw, h + 0.06, txt, size=fs, bold=(sz == 15.0),
           colour=INK if sz == 15.0 else C(0x3C, 0x4E, 0x5E), line=1.22)
        ty += h + gap
    return s


def s_prose(prs, title, paras, kicker=None, cols=2):
    """Readable two-column text — this is what makes the deck revisable."""
    s = _blank(prs)
    y = s_head(s, title, kicker)
    cw = (W - 2 * M - 0.55) / cols
    per = (len(paras) + cols - 1) // cols
    # Never let a bold heading be separated from the body that belongs to it:
    # if column 2 would start on a body paragraph whose heading ended column 1,
    # move the heading across too.
    while 0 < per < len(paras) and not paras[per].startswith("**") and paras[per - 1].startswith("**"):
        per -= 1
    groups = [paras[c * per:(c + 1) * per] if c < cols - 1 else paras[c * per:]
              for c in range(cols)]

    # Measure and draw from ONE code path. This function had no fit loop at
    # all, which was invisible while the body was 13pt and put 125 blocks off
    # the bottom of the slide the moment the type scale went up. Two copies of
    # the stacking arithmetic would drift apart again, so there is only one.
    def boxes(bfs):
        hfs = bfs + 2.0                          # sub-headings ride above body
        out, bottom = [], y
        for c, g in enumerate(groups):
            x = M + c * (cw + 0.55)
            ty = y
            for p in g:
                bold = p.startswith("**")
                txt = p.strip("*")
                fs = hfs if bold else bfs
                if bold and ty > y + 0.01:
                    ty += 0.16                   # space BEFORE a sub-heading
                h = theight(txt, cw, fs, 1.24)
                out.append((x, ty, cw, h + 0.06, txt, bold, fs))
                ty += h + (0.07 if bold else 0.15)
            bottom = max(bottom, ty)
        return out, bottom - y

    avail = H - y - 0.20
    bfs = _shrink(13.0, lambda f: boxes(f)[1], avail, "prose")
    for x, ty, w, h, txt, bold, fs in boxes(bfs)[0]:
        tb(s, x, ty, w, h, txt, size=fs, bold=bold,
           colour=ORANGE if bold else C(0x33, 0x46, 0x57), line=1.24)
    return s


def s_define(prs, term, definition, example, confuse=None, kicker="DEFINITION"):
    """Term, definition, an example, and the thing it gets confused with.

    Every block here is measured. The definition card used to be a fixed
    1.28in, which was right for a two-line definition and spilled the third
    line out below the card. It looked fine to the bounds scanner, because
    the text box was still inside the slide, and it was only visible in a
    render. The term itself is measured too: a long term wrapped into the
    card underneath it.
    """
    s = _blank(prs)
    tb(s, M, 0.62, W - 2 * M, 0.32, kicker, size=12, bold=True, colour=ORANGE)
    th = max(0.62, theight(term, W - 2 * M, 38, 1.05, font=HEAD))
    tb(s, M, 1.02, W - 2 * M, th + 0.06, term, size=38, bold=True,
       colour=INK, font=HEAD)

    y = 1.02 + th + 0.30
    dh = theight(definition, W - 2 * M - 0.64, 16, 1.24)
    card(s, M, y, W - 2 * M, dh + 0.44, fill=STEEL)
    tb(s, M + 0.32, y + 0.22, W - 2 * M - 0.64, dh + 0.06, definition,
       size=16, colour=INK, line=1.24)

    y += dh + 0.44 + 0.30
    eh = theight(example, W - 2 * M - 2.2, 14, 1.2)
    chip(s, M, y, "FOR EXAMPLE", fill=TEAL, w=1.8, size=11)
    tb(s, M + 2.05, y - 0.02, W - 2 * M - 2.2, eh + 0.06, example, size=14,
       colour=C(0x33, 0x46, 0x57), line=1.2)

    if confuse:
        y += max(0.52, eh) + 0.30
        ch = theight(confuse, W - 2 * M - 3.1, 14, 1.2)
        chip(s, M, y, "DO NOT CONFUSE WITH", fill=ORANGE, w=2.7, size=11)
        tb(s, M + 2.95, y - 0.02, W - 2 * M - 3.1, ch + 0.06, confuse,
           size=14, colour=C(0x33, 0x46, 0x57), line=1.2)
    return s


def s_worked(prs, title, intro, steps, answer, kicker="WORKED EXAMPLE"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    # The intro reserve used to be a character count times a flat 0.24in,
    # calibrated by hand at 14.5pt. The type ramp invalidated both halves of
    # that at once, so it is measured now.
    ih = theight(intro, W - 2 * M, 14.5, 1.2)
    tb(s, M, y, W - 2 * M, ih + 0.06, intro, size=14.5, colour=C(0x33, 0x46, 0x57),
       line=1.2)
    y += ih + 0.12
    n = len(steps)
    tw = W - 2 * M - 1.1
    # Measure the answer band rather than reserving a flat 1.32in. A one-line
    # answer was being charged for two, and that reserve was most of the room
    # the steps needed.
    ah = max(0.70, theight(answer, W - 2 * M - 0.64, 16, 1.18) + 0.26)
    avail = H - y - (ah + 0.24)   # 0.16 put the answer card 0.02in past the margin
    fs = 13.5
    def budget(fs):
        hs = [max(0.44, theight(st, tw, fs, 1.16) + 0.16) for st in steps]
        return hs, sum(hs) + 0.06 * (n - 1)
    fs = _shrink(fs, lambda f: budget(f)[1], avail, 'worked steps')
    hs, need = budget(fs)
    # If it still does not fit, keep shrinking instead of squeezing the cards
    # proportionally. A squeezed card does not clip its text, it spills it over
    # the card below, and a bounds scan cannot see that happen: every shape is
    # still inside the slide while the slide itself is unreadable.
    while need > avail and fs > 8.0:
        fs -= 0.5
        hs, need = budget(fs)
    for i, st in enumerate(steps):
        ch = hs[i]
        card(s, M, y, W - 2 * M, ch, fill=STEEL2)
        chip(s, M + 0.24, y + 0.06, str(i + 1), fill=INK, dia=0.34, size=10)
        tb(s, M + 0.82, y + 0.05, tw, ch - 0.10, st, size=fs, colour=INK, line=1.16)
        y += ch + 0.06
    y += 0.06
    card(s, M, y, W - 2 * M, ah, fill=ORANGE)
    tb(s, M + 0.32, y + 0.15, W - 2 * M - 0.64, ah - 0.30, answer, size=16,
       bold=True, colour=PAPER, line=1.18)
    return s


def s_check(prs, qs, kicker="CHECK YOUR UNDERSTANDING", title="Can you answer these?",
            foot="Answers are on the next slide — try first, then look."):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    n = len(qs)
    avail = H - y - 0.86       # the foot line is 0.22in of the 0.86
    tw = W - 2 * M - 0.75
    fs = 14.5
    def budget(fs):
        hs = [theight(q, tw, fs, 1.20) + 0.20 for q in qs]
        return hs, sum(hs)
    fs = _shrink(fs, lambda f: budget(f)[1], avail, 'check questions')
    hs, need = budget(fs)
    for i, q in enumerate(qs):
        chip(s, M, y + 0.04, chr(65 + i), fill=TEAL, dia=0.36, size=11)
        tb(s, M + 0.58, y, tw, hs[i] - 0.06, q, size=fs,
           colour=C(0x2A, 0x3B, 0x4A), line=1.20)
        y += hs[i]
    tb(s, M, H - 0.82, W - 2 * M, 0.4, foot, size=12, italic=True, colour=MUTED)
    return s


def s_answers(prs, pairs, kicker="ANSWERS", title="How did you do?"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    n = len(pairs)
    avail = (H - 0.45) - y

    # An answers slide is a stack of short paragraphs, which is the one shape
    # that takes a second column well. Going two-up buys about twice the room
    # and costs nothing in reading order, so it happens before the font is
    # allowed below the floor.
    def plan(cols, fs):
        cw = (W - 2 * M - 0.5 * (cols - 1)) / cols
        tw = cw - 0.62
        hs = [0.32 + theight(a, tw, fs, 1.20) + 0.18 for _, a in pairs]
        per = (n + cols - 1) // cols
        tallest = max(sum(hs[c * per:(c + 1) * per]) for c in range(cols))
        return cw, tw, hs, per, tallest

    cols, fs = 1, 14.0
    while fs > FLOOR and plan(1, fs)[4] > avail:
        fs -= 0.5
    if plan(cols, fs)[4] > avail:
        cols = 2
        fs = _shrink(14.0, lambda f: plan(2, f)[4], avail, 'answers')
    cw, tw, hs, per, _ = plan(cols, fs)
    for i, (q, a) in enumerate(pairs):
        c = min(i // per, cols - 1)
        x = M + c * (cw + 0.5)
        ty = y + sum(hs[c * per:i])
        chip(s, x, ty + 0.04, chr(65 + i), fill=ORANGE, dia=0.36, size=11)
        tb(s, x + 0.58, ty, tw, 0.30, q, size=min(12.5, fs), bold=True, colour=MUTED)
        tb(s, x + 0.58, ty + 0.32, tw, hs[i] - 0.36, a, size=fs,
           colour=C(0x2A, 0x3B, 0x4A), line=1.20)
    return s


def s_glossary(prs, terms, page=None, kicker="GLOSSARY"):
    """Fill columns by measured height, adding pages before text reaches the footer."""
    cw = (W-2*M-0.5)/2
    top = (1.04 if kicker else 0.62) + 0.52 + 0.53
    available = H - 0.55 - top
    pages = [[[], []]]
    col, used = 0, 0.0
    for term, definition in terms:
        th = theight(term,cw,13,1.15)+0.06
        dh = theight(definition,cw,12,1.18)+0.10
        height = th+dh+0.14
        if height > available:
            raise ValueError("Glossary definition needs editing: " + term)
        if used+height > available:
            if col == 0: col = 1
            else: pages.append([[], []]); col = 0
            used = 0.0
        pages[-1][col].append((term,definition,th,dh))
        used += height
    for index, columns in enumerate(pages):
        s = _blank(prs)
        suffix = f" ({index+1} of {len(pages)})" if len(pages)>1 else (f" ({page})" if page else "")
        y = s_head(s, "Every word we used today"+suffix, kicker)
        for col, entries in enumerate(columns):
            ty = y
            for term, definition, th, dh in entries:
                tb(s,M+col*(cw+0.5),ty,cw,th,term,size=13,bold=True,colour=ORANGE,line=1.15)
                tb(s,M+col*(cw+0.5),ty+th,cw,dh,definition,size=12,colour=INK,line=1.18)
                ty += th+dh+0.14
    return s


def s_break(prs, mins=10, after=None):
    """`after` says what happens next.

    The default used to claim nothing after the break needed a computer, which
    is false in every week whose hands-on block follows the break — most of
    them. Callers that want the old line pass it explicitly.
    """
    s = _blank(prs); _bg(s, prs, INK)
    tb(s, M, 2.6, W - 2 * M, 1.4, "Break", size=54, bold=True, colour=PAPER, font=HEAD,
       align=PP_ALIGN.CENTER)
    tb(s, M, 4.1, W - 2 * M, 0.6, f"{mins} minutes", size=22, colour=ORANGE,
       align=PP_ALIGN.CENTER)
    tail = after or "Be back on time: the longest working block of the session is next."
    tb(s, M, 5.0, W - 2 * M, 0.6,
       "Stretch, and talk to someone you have not worked with. " + tail,
       size=14, colour=C(0x8E, 0xA4, 0xB8), align=PP_ALIGN.CENTER)
    return s


def s_summary(prs, points, kicker="MODULE SUMMARY", title="What you should take away"):
    s = _blank(prs)
    y = s_head(s, title, kicker)
    n = len(points)
    avail = H - y - 0.45
    tw = W - 2 * M - 0.6
    fs = 14.5
    def budget(fs):
        hs = [theight(p, tw, fs, 1.20) + 0.16 for p in points]
        return hs, sum(hs)
    fs = _shrink(fs, lambda f: budget(f)[1], avail, 'summary points')
    hs, need = budget(fs)
    for i, p in enumerate(points):
        chip(s, M, y + 0.06, "", fill=TEAL, dia=0.20)
        tb(s, M + 0.45, y, tw, hs[i] - 0.05, p, size=fs,
           colour=C(0x2A, 0x3B, 0x4A), line=1.20)
        y += hs[i]
    return s


def s_map(prs, current, weeks, kicker="WHERE WE ARE"):
    s = _blank(prs)
    y = s_head(s, "The fifteen weeks", kicker)
    cols = 5
    cw = (W - 2 * M - 0.3 * (cols - 1)) / cols
    chh = 0.78
    for i, (num, label) in enumerate(weeks):
        r, c = divmod(i, cols)
        x = M + c * (cw + 0.3)
        top = y + r * (chh + 0.26)
        is_now = (num == current)
        card(s, x, top, cw, chh, fill=ORANGE if is_now else STEEL2, shadow=is_now)
        tb(s, x + 0.14, top + 0.08, cw - 0.28, 0.28, "WEEK " + str(num), size=10, bold=True,
           colour=PAPER if is_now else MUTED)
        tb(s, x + 0.14, top + 0.34, cw - 0.28, chh - 0.42, label, size=11,
           bold=is_now, colour=PAPER if is_now else INK, line=1.1)
    return s
