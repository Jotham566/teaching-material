"""Week 8 patch, 30 October 2026.

Applies to the three built Week 8 decks (CML3111, CML3112, CML3113):
  1. removes the six-slide Data Analysis Project block that followed the Week 8 form;
  2. repairs words that an automated renaming pass replaced with variable names;
  3. rewrites "Today's learning" with outcomes for this week;
  4. inserts ten plain-language concept slides (kinds of ML, vocabulary, why rows are
     held back, the scatter of the student's own data, loss and gradient descent,
     NumPy shape, and the error measures MAE / MSE / RMSE);
  5. renumbers the footers.

It edits the finished .pptx files, so run it again after any rebuild with build_decks.py.
Every number printed on a new slide is computed here from the cohort CSV or from the
toy code that is shown on the slide.

Usage:  python3 scripts/patch_week8_20261030.py [--out DIR]
Needs:  python-pptx, numpy, pandas, matplotlib.
"""
import argparse, copy, io, re, shutil, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
DECKS = BASE / "decks"
FIGS = ROOT / "figs" / "week8_20261030"
INK, ORANGE, TEAL, MUTED = "1C3144", "E4572E", "2E7D6F", "6B7A8A"
PALE1, PALE2, CODEFG, KEYWORD = "EEF3F6", "E5F1EE", "F4F7FA", "FFB080"

COHORTS = {
    "CML3111": dict(file="CML3111_Week08_Engineering.pptx",
                    short="motor temperature", unit="deg C", discipline="motor winding"),
    "CML3112": dict(file="CML3112_Week08_Design_Infrastructure.pptx",
                    short="cooling load", unit="kW", discipline="building cooling"),
    "CML3113": dict(file="CML3113_Week08_Mining_Petroleum.pptx",
                    short="crusher energy demand", unit="kWh/t", discipline="crusher energy"),
}

# ---------------------------------------------------------------- figures
ink, orange, teal, muted = "#" + INK, "#" + ORANGE, "#" + TEAL, "#" + MUTED
plt.rcParams.update({"font.family": ["Carlito", "Calibri", "DejaVu Sans"], "font.size": 16,
                     "axes.edgecolor": muted, "axes.labelcolor": ink, "text.color": ink,
                     "xtick.color": ink, "ytick.color": ink})


def box(ax, x, y, w, h, text, fc, ec=None, fs=17, color=ink, bold=False, sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.025",
                                fc=fc, ec=ec or fc, lw=2))
    if sub:
        ax.text(x + w / 2, y + h * 0.64, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal")
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=fs - 3, color=color)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal")


def arrow(ax, p, q, color=muted):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, lw=2.2, color=color))


def fig_map(path):
    fig, ax = plt.subplots(figsize=(12.5, 5.0)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    box(ax, 0.36, 0.80, 0.28, 0.15, "Machine learning", "#" + INK, fs=20, color="white", bold=True)
    box(ax, 0.04, 0.46, 0.34, 0.20, "Supervised learning", "#EEF3F6", "#" + INK, fs=19, bold=True,
        sub="examples come with answers")
    box(ax, 0.42, 0.46, 0.26, 0.20, "Unsupervised", "#F6F6F6", muted, fs=19, bold=True,
        sub="no answers; find groups")
    box(ax, 0.72, 0.46, 0.25, 0.20, "Reinforcement", "#F6F6F6", muted, fs=19, bold=True,
        sub="trial and reward")
    box(ax, 0.02, 0.14, 0.20, 0.24, "Regression", "#E4572E", fs=20, color="white", bold=True,
        sub="predict a number")
    box(ax, 0.25, 0.14, 0.20, 0.24, "Classification", "#E5F1EE", teal, fs=20, bold=True,
        sub="predict a category")
    for tx in (0.5,):
        arrow(ax, (0.50, 0.80), (0.21, 0.67)); arrow(ax, (0.50, 0.80), (0.55, 0.67)); arrow(ax, (0.50, 0.80), (0.84, 0.67))
    arrow(ax, (0.17, 0.46), (0.12, 0.40)); arrow(ax, (0.25, 0.46), (0.35, 0.40))
    ax.text(0.12, 0.04, "TODAY", ha="center", fontsize=15, color=orange, fontweight="bold")
    ax.text(0.35, 0.04, "WEEK 9", ha="center", fontsize=15, color=teal, fontweight="bold")
    ax.text(0.55, 0.36, "SEMESTER 2", ha="center", fontsize=15, color=teal, fontweight="bold")
    ax.text(0.55, 0.28, "clustering, PCA", ha="center", fontsize=15, color=muted)
    ax.text(0.845, 0.36, "NOT IN THIS COURSE", ha="center", fontsize=15, color=muted, fontweight="bold")
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)


def fig_holdback(path):
    fig, ax = plt.subplots(figsize=(12.5, 5.0)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    cols = [("Training rows", "E1 to E4", "The model learns from these.", "Practice questions\nyou study from", "#EEF3F6", ink),
            ("Validation rows", "E5", "We compare models on these.", "A mock exam\nto check progress", "#E5F1EE", teal),
            ("Test rows", "E6", "Opened once, at the very end.", "The real exam,\nunseen until the day", "#" + ORANGE, "white")]
    for i, (t, g, job, analogy, fc, fg) in enumerate(cols):
        x = 0.01 + i * 0.325
        ax.add_patch(FancyBboxPatch((x, 0.30), 0.30, 0.62, boxstyle="round,pad=0.02,rounding_size=0.03", fc=fc, ec=fc))
        ax.text(x + 0.15, 0.83, t, ha="center", fontsize=22, fontweight="bold", color=fg)
        ax.text(x + 0.15, 0.72, g, ha="center", fontsize=19, color=fg)
        ax.text(x + 0.15, 0.55, job, ha="center", fontsize=16, color=fg, wrap=True)
        ax.text(x + 0.15, 0.37, analogy, ha="center", va="center", fontsize=16, color=fg, style="italic")
    ax.text(0.5, 0.12, "Each group of equipment sits in exactly one box.", ha="center", fontsize=17, color=ink)
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)


def clean_groups(code):
    raw = pd.read_csv(BASE / "assessment_banks" / "W08" / code / "A" / "engineering_data.csv")
    d = raw.drop_duplicates("record_id").copy()
    d = d[d.target.notna() & d.load_pct.between(0, 100)].copy()
    tr = d[d.equipment_id.isin(["E1", "E2", "E3", "E4"])]
    va = d[d.equipment_id == "E5"]
    return raw, d, tr, va


def fig_scatter(path, code, unit, short):
    raw, d, tr, va = clean_groups(code)
    slope, intercept = np.polyfit(tr.load_pct, tr.target, 1)
    mean_t = tr.target.mean()
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    ax.scatter(tr.load_pct, tr.target, s=62, color=ink, label="Training rows (E1 to E4)", zorder=3)
    ax.scatter(va.load_pct, va.target, s=70, color=orange, marker="D", label="Validation rows (E5)", zorder=3)
    xs = np.linspace(d.load_pct.min() - 2, d.load_pct.max() + 2, 50)
    ax.plot(xs, slope * xs + intercept, color=teal, lw=3, label="Line fitted on the training rows")
    ax.axhline(mean_t, color=muted, lw=2.5, ls="--", label="Average of the training rows")
    ax.set_xlabel("load_pct  (equipment load, %)"); ax.set_ylabel(f"target  ({short}, {unit})")
    ax.grid(alpha=0.25); ax.legend(loc="upper left", fontsize=14, frameon=False)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)
    return dict(r=float(tr.load_pct.corr(tr.target)), n=len(tr), slope=float(slope), mean=float(mean_t))


def gd_run(steps=5, lr=0.05):
    x = np.array([1, 2, 3]); y = np.array([2, 4, 6]); w = 0.0; rows = []
    for step in range(1, steps + 1):
        gradient = 2 * np.mean(x * (w * x - y))
        w = w - lr * gradient
        loss = np.mean((w * x - y) ** 2)
        rows.append((step, round(float(w), 3), round(float(loss), 3)))
    return rows


def fig_loss(path):
    x = np.array([1, 2, 3]); y = np.array([2, 4, 6])
    loss = lambda w: np.mean((w * x - y) ** 2)
    ws = np.linspace(-0.4, 4.4, 200)
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot(ws, [loss(w) for w in ws], color=ink, lw=3)
    w = 0.0; pts = [w]
    for _ in range(5):
        w = w - 0.05 * 2 * np.mean(x * (w * x - y)); pts.append(w)
    for i, p in enumerate(pts):
        ax.scatter([p], [loss(p)], s=110, color=orange, zorder=4)
        if i < 3: ax.annotate(f"try {i}", (p, loss(p)), textcoords="offset points", xytext=(12, 6), fontsize=14, color=orange)
    for a, b in zip(pts[:-1], pts[1:]):
        ax.annotate("", xy=(b, loss(b)), xytext=(a, loss(a)),
                    arrowprops=dict(arrowstyle="-|>", color=orange, lw=2))
    ax.scatter([2], [0], s=170, color=teal, marker="*", zorder=5)
    ax.annotate("best slope = 2\nloss = 0", (2, 0.3), xytext=(2, 9), textcoords="data", ha="center", fontsize=15, color=teal, arrowprops=dict(arrowstyle="-|>", color=teal))
    ax.set_xlabel("slope w  (the number the model can change)"); ax.set_ylabel("loss  (mean squared error)")
    ax.set_ylim(-1, 20); ax.grid(alpha=0.25)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)


def fig_shape(path, code, short):
    raw = pd.read_csv(BASE / "assessment_banks" / "W08" / code / "A" / "engineering_data.csv").head(3)
    fig, ax = plt.subplots(figsize=(12.5, 5.0)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.25, 0.93, "The pandas table", ha="center", fontsize=19, fontweight="bold")
    ax.text(0.78, 0.93, "What scikit-learn receives", ha="center", fontsize=19, fontweight="bold")
    heads = ["record_id", "load_pct", "ambient_c", "target"]; xs = [0.00, 0.12, 0.24, 0.37]
    ax.add_patch(plt.Rectangle((0.0, 0.58), 0.50, 0.08, fc=ink)); ax.add_patch(plt.Rectangle((0.0, 0.34), 0.50, 0.24, fc="#EEF3F6"))
    for x, h in zip(xs, heads): ax.text(x + 0.05, 0.62, h, ha="center", va="center", color="white", fontsize=14)
    for r in range(3):
        row = raw.iloc[r]; vals = [int(row.record_id), f"{row.load_pct:g}", f"{row.ambient_c:g}", f"{row.target:g}"]
        for x, v in zip(xs, vals): ax.text(x + 0.05, 0.52 - r * 0.075, str(v), ha="center", va="center", fontsize=15)
    ax.add_patch(plt.Rectangle((0.125, 0.34), 0.23, 0.32, fc="none", ec=teal, lw=3)); ax.text(0.24, 0.28, "features", ha="center", color=teal, fontsize=17, fontweight="bold")
    ax.add_patch(plt.Rectangle((0.365, 0.34), 0.125, 0.32, fc="none", ec=orange, lw=3)); ax.text(0.43, 0.28, "target", ha="center", color=orange, fontsize=17, fontweight="bold")
    arrow(ax, (0.52, 0.55), (0.60, 0.62), teal); arrow(ax, (0.52, 0.45), (0.60, 0.33), orange)
    ax.add_patch(plt.Rectangle((0.62, 0.50), 0.20, 0.30, fc="#E5F1EE", ec=teal, lw=3))
    for r in range(3):
        row = raw.iloc[r]; ax.text(0.72, 0.74 - r * 0.075, f"[{row.load_pct:g}, {row.ambient_c:g}]", ha="center", fontsize=15)
    ax.text(0.72, 0.44, "X", ha="center", fontsize=26, fontweight="bold", color=teal)
    ax.text(0.72, 0.36, "shape (3, 2)", ha="center", fontsize=17, color=teal)
    ax.text(0.72, 0.29, "3 rows, 2 columns", ha="center", fontsize=15, color=muted)
    ax.add_patch(plt.Rectangle((0.86, 0.50), 0.11, 0.30, fc="#FCE9E3", ec=orange, lw=3))
    for r in range(3):
        row = raw.iloc[r]; ax.text(0.915, 0.74 - r * 0.075, f"{row.target:g}", ha="center", fontsize=15)
    ax.text(0.915, 0.44, "y", ha="center", fontsize=26, fontweight="bold", color=orange)
    ax.text(0.915, 0.36, "shape (3,)", ha="center", fontsize=17, color=orange)
    ax.text(0.915, 0.29, "3 answers", ha="center", fontsize=15, color=muted)
    ax.text(0.5, 0.08, "One row of X and the matching entry of y describe the same observation, in the same order.", ha="center", fontsize=17)
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.08); plt.close(fig)


# ---------------------------------------------------------------- pptx helpers
rgb = lambda h: RGBColor.from_string(h)


def shape_rect(slide, l, t, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(l), Pt(t), Pt(w), Pt(h))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill); s.line.fill.background(); s.shadow.inherit = False
    return s


def textbox(slide, text, l, t, w, h, size, color=INK, bold=False, font="Calibri", align=None, space_after=0, anchor=None):
    tb = slide.shapes.add_textbox(Pt(l), Pt(t), Pt(w), Pt(h)); tf = tb.text_frame; tf.word_wrap = True
    if anchor: tf.vertical_anchor = anchor
    paras = text if isinstance(text, list) else [text]
    for i, ptxt in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        bold_p = bold
        if isinstance(ptxt, tuple): ptxt, bold_p = ptxt
        r = p.add_run(); r.text = ptxt; f = r.font
        f.size = Pt(size); f.bold = bold_p; f.name = font; f.color.rgb = rgb(color)
        if align: p.alignment = align
        p.space_after = Pt(space_after)
    return tb


def header(slide, kicker, title, band=110, tsize=31.5):
    shape_rect(slide, 0, 0, 960, band, INK)
    if kicker: textbox(slide, kicker, 46, 14, 870, 22, 15, ORANGE, True)
    textbox(slide, title, 46, 41 if kicker else 15, 870, 64, tsize, "FFFFFF", True)


def footer(slide, label):
    textbox(slide, label, 46, 513.75, 851, 17, 12, MUTED)


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_slide(prs):
    blank = next(l for l in prs.slide_layouts if l.name == "Blank")
    return prs.slides.add_slide(blank)


def move_slide(prs, slide, before_slide=None):
    lst = prs.slides._sldIdLst
    ids = list(lst)
    el = next(e for e in ids if prs.part.related_part(e.rId) is slide.part)
    lst.remove(el)
    if before_slide is None:
        lst.append(el)
    else:
        tgt = next(e for e in lst if prs.part.related_part(e.rId) is before_slide.part)
        tgt.addprevious(el)


def slide_title_texts(slide):
    return [sh.text_frame.text.strip() for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()]


def find_slide(prs, title, nth=0, pos=None):
    hits = [s for s in prs.slides if title in slide_title_texts(s)[:3]]
    return hits[nth] if len(hits) > nth else None


def delete_slide(prs, slide):
    lst = prs.slides._sldIdLst
    el = next(e for e in lst if prs.part.related_part(e.rId) is slide.part)
    prs.part.drop_rel(el.rId); lst.remove(el)


def figure_slide(prs, title, img, caption, notes, label):
    s = new_slide(prs)
    shape_rect(s, 0, 0, 960, 75, INK)
    textbox(s, title, 38, 15, 885, 51, 29.25, "FFFFFF", True)
    from PIL import Image
    iw, ih = Image.open(img).size
    box_w, box_h = 900, 362
    sc = min(box_w / iw, box_h / ih); w, h = iw * sc, ih * sc
    s.shapes.add_picture(str(img), Pt(30 + (box_w - w) / 2), Pt(88 + (box_h - h) / 2), Pt(w), Pt(h))
    shape_rect(s, 0, 458, 960, 46, PALE2)
    textbox(s, caption, 44, 464, 872, 38, 18, TEAL, True)
    footer(s, label); set_notes(s, notes); return s


def table_slide(prs, kicker, title, header_row, rows, widths, notes, label, size=17, below=None, below_size=20, row_h=None):
    s = new_slide(prs); header(s, kicker, title)
    n = len(rows) + 1; left, top = 46, 128; tw = sum(widths)
    rh = row_h or (62 if n <= 6 else 52)
    gt = s.shapes.add_table(n, len(header_row), Pt(left), Pt(top), Pt(tw), Pt(rh * n))
    tbl = gt.table
    tblPr = tbl._tbl.tblPr
    for attr in ("bandRow", "firstRow"): tblPr.set(attr, "0")
    for j, w in enumerate(widths): tbl.columns[j].width = Pt(w)
    for i in range(n):
        tbl.rows[i].height = Pt(rh)
        for j in range(len(header_row)):
            c = tbl.cell(i, j); txt = header_row[j] if i == 0 else rows[i - 1][j]
            c.fill.solid(); c.fill.fore_color.rgb = rgb(TEAL if i == 0 else (PALE1 if i % 2 else "FFFFFF"))
            c.margin_left = c.margin_right = Pt(8); c.margin_top = c.margin_bottom = Pt(3)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; r = p.add_run(); r.text = str(txt)
            r.font.size = Pt(size); r.font.name = "Calibri"
            r.font.bold = (i == 0) or (j == 0)
            r.font.color.rgb = rgb("FFFFFF" if i == 0 else INK)
    if below:
        textbox(s, below, 46, top + rh * n + 14, 868, 540 - (top + rh * n + 14) - 34, below_size, INK, False, space_after=4)
    footer(s, label); set_notes(s, notes); return s


def code_runs(tf, code, size):
    kws = {"import", "as", "for", "in", "def", "return", "if", "else", "print"}
    first = True
    for line in code.split("\n"):
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.line_spacing = Pt(size * 1.25)
        for tok in re.split(r"(\b\w+\b)", line):
            if not tok: continue
            r = p.add_run(); r.text = tok
            r.font.name = "Courier New"; r.font.size = Pt(size)
            r.font.color.rgb = rgb(KEYWORD if tok in kws else CODEFG)


def code_slide(prs, kicker, title, code, output, cues, caption, notes, label, code_size=17, code_h=None, out_size=16):
    s = new_slide(prs); header(s, kicker, title)
    nl = len(code.split("\n")); ch = code_h or (nl * code_size * 1.25 + 28)
    shape_rect(s, 41, 126, 560, ch, INK)
    tb = s.shapes.add_textbox(Pt(52), Pt(136), Pt(540), Pt(ch - 18)); tb.text_frame.word_wrap = True
    code_runs(tb.text_frame, code, code_size)
    oy = 126 + ch + 10; on = len(output.split("\n")); oh = on * out_size * 1.35 + 16
    shape_rect(s, 41, oy, 560, oh, PALE1)
    tb2 = s.shapes.add_textbox(Pt(52), Pt(oy + 8), Pt(540), Pt(oh - 12)); tb2.text_frame.word_wrap = True
    for i, line in enumerate(output.split("\n")):
        p = tb2.text_frame.paragraphs[0] if i == 0 else tb2.text_frame.add_paragraph()
        r = p.add_run(); r.text = line; r.font.name = "Courier New"; r.font.size = Pt(out_size); r.font.color.rgb = rgb(INK)
    textbox(s, "WHAT IT PRINTS", 52, oy - 1, 200, 10, 1, PALE1)  # spacer-free placeholder removed below
    s.shapes._spTree.remove(s.shapes[-1]._element)
    textbox(s, "HOW TO READ IT", 625, 126, 300, 26, 15, TEAL, True)
    textbox(s, cues, 625, 156, 300, 300, 17.5, INK, False, space_after=9)
    textbox(s, caption, 46, 462, 868, 40, 17.5, TEAL, True)
    footer(s, label); set_notes(s, notes); return s


# ---------------------------------------------------------------- content per cohort
def build_content(code, c, figdir):
    short, unit = c["short"], c["unit"]
    figdir.mkdir(parents=True, exist_ok=True)
    fig_map(figdir / "kinds_of_ml.png"); fig_holdback(figdir / "hold_back.png"); fig_loss(figdir / "loss_walk.png")
    sc = fig_scatter(figdir / f"scatter_{code}.png", code, unit, short)
    fig_shape(figdir / f"shape_{code}.png", code, short)
    raw = pd.read_csv(BASE / "assessment_banks" / "W08" / code / "A" / "engineering_data.csv").head(3)
    y3 = [f"{v:g}" for v in raw.target]; x3 = [[f"{a:g}", f"{b:g}"] for a, b in zip(raw.load_pct, raw.ambient_c)]
    xcode = "X = np.array([[%s, %s],\n              [%s, %s],\n              [%s, %s]])" % tuple(v for r in x3 for v in r)
    shape_code = "import numpy as np\n" + xcode + "\ny = np.array([%s])\nprint(X.shape)\nprint(y.shape)\nprint(round(y.mean(), 3))" % ", ".join(y3)
    ymean = np.array([float(v) for v in y3]).mean()
    shape_out = "(3, 2)\n(3,)\n%s" % round(float(ymean), 3)
    gd = gd_run()
    gd_code = ("import numpy as np\nx = np.array([1, 2, 3])\ny = np.array([2, 4, 6])\nw, learning_rate = 0.0, 0.05\nprint(\"step w loss\")\n"
               "for step in range(1, 6):\n    gradient = 2 * np.mean(x * (w * x - y))\n    w = w - learning_rate * gradient\n"
               "    loss = np.mean((w * x - y) ** 2)\n    print(step, round(w, 3), round(loss, 3))")
    gd_out = "\n".join(f"{a} {b} {l}" for a, b, l in gd)
    # error table, four invented readings
    act = [70, 80, 90, 60]; pred = [72, 77, 90, 66]
    err = [a - p for a, p in zip(act, pred)]; ab = [abs(e) for e in err]; sq = [e * e for e in err]
    mae, mse = np.mean(ab), np.mean(sq); rmse = mse ** 0.5
    assert (mae, mse, rmse) == (2.75, 12.25, 3.5)
    return dict(sc=sc, shape_code=shape_code, shape_out=shape_out, ymean=ymean, gd=gd, gd_code=gd_code, gd_out=gd_out,
                act=act, pred=pred, err=err, ab=ab, sq=sq, mae=mae, mse=mse, rmse=rmse)


def patch_deck(code, c, src, dst, figdir):
    prs = Presentation(str(src))
    label0 = f"{code}   Week 8   "
    if any("Words for the whole field" in slide_title_texts(s)[:3] for s in prs.slides):
        print(f"{code}: already patched, skipping"); return
    short, unit = c["short"], c["unit"]
    K = build_content(code, c, figdir)

    # 1. remove the Data Analysis Project block
    removed = 0
    for t in ("Data analysis project", "Data analysis project continued", "Data analysis project submission"):
        while True:
            s = find_slide(prs, t)
            if s is None: break
            delete_slide(prs, s); removed += 1
    assert removed == 6, f"{code}: expected to remove 6 slides, removed {removed}"

    # 2. repair renaming damage in prose (skip code runs)
    fixes = [("baseline_errors", "errors"), ("as a equipment_data", "as a table"),
             ("maps group labels to validation_results", "maps group labels to their values"),
             ("its modelling_data", "its data")]
    count = 0
    def fix_tf(tf):
        nonlocal count
        for p in tf.paragraphs:
            if any(r.font.name == "Courier New" for r in p.runs): continue
            full = "".join(r.text for r in p.runs)
            new = full
            for a, b in fixes: new = new.replace(a, b)
            if new != full and p.runs:
                p.runs[0].text = new
                for r in p.runs[1:]: r.text = ""
                count += 1
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame: fix_tf(sh.text_frame)
        if s.has_notes_slide: fix_tf(s.notes_slide.notes_text_frame)

    # 3. Today's learning
    s2 = find_slide(prs, "Today’s learning")
    bodies = [sh for sh in s2.shapes if sh.has_text_frame and sh.text_frame.text.startswith(("Use pandas", "Complete the issued"))]
    assert len(bodies) == 2
    def set_two(sh, head, body):
        tf = sh.text_frame
        for r in list(tf.paragraphs[0].runs)[1:]: r.text = ""
        for extra in tf.paragraphs[1:]: extra._p.getparent().remove(extra._p)
        p = tf.paragraphs[0]; ref = p.runs[0]
        size = ref.font.size
        ref.text = head; ref.font.bold = True; ref.font.size = Pt(19); ref.font.color.rgb = rgb(TEAL)
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = body
        r2.font.size = Pt(22); r2.font.name = "Calibri"; r2.font.bold = False; r2.font.color.rgb = rgb(INK)
        p2.space_before = Pt(8)
    set_two(bodies[0], "WHAT WE WILL DO",
            f"Predict {short} from load and ambient temperature in three ways: the average, a straight line and a decision tree. Learn the words that go with them: feature, target, training, error and loss.")
    set_two(bodies[1], "HOW YOU WILL SHOW IT",
            f"You can say in plain words what each method learned and read its error in {unit.replace(chr(32), chr(160))}. You can explain why some rows stay hidden while a model learns.")
    set_notes(s2, f"Today we build our first prediction models. We will predict {short} from two inputs, using three methods. The first is the plain average. The second is a straight line. The third is a decision tree. Along the way we will name every idea we use, so that the words feature, target, training, error and loss all have a clear meaning by the end of the session. By the end you will be able to say what each method learned and read its error in {unit}.")

    # 4. new slides
    anchor_8 = find_slide(prs, "Rows used for modelling")
    anchor_18 = find_slide(prs, "Fitting a line to observations")
    anchor_24 = find_slide(prs, "Standard names for model inputs")
    anchor_35 = find_slide(prs, "Matching actual values and predictions")
    after2 = anchor_8  # slides A-C go just before "The supplied file"
    anchor_file = find_slide(prs, "The supplied file")
    lab = lambda: label0 + "0"

    A = figure_slide(prs, "Today’s model is supervised regression", figdir / "kinds_of_ml.png",
        "Supervised learning learns from examples that come with answers. Regression predicts a number.",
        f"Machine learning is a large field, so let us place today on a map. In supervised learning, every training example comes with its answer. Here an example is a past load reading together with the {short} that was recorded. The model studies many of those pairs. When the answer is a number, the job is called regression. That is today. When the answer is a category, such as fault or no fault, the job is called classification, and that is next week. In unsupervised learning there are no answers, and the computer looks for groups by itself. We meet that in Semester 2. It includes grouping similar rows, called clustering, and squeezing many columns into fewer ones, called PCA. In reinforcement learning, a program learns by trial and reward. The Week 1 roadmap showed that this topic sits outside our course.", lab())
    B = table_slide(prs, "WORDS WE USE", "Words for the whole field",
        ["Word", "Plain meaning", "Example from today"],
        [["Machine learning", "A computer finds a rule from examples, so nobody has to write the rule by hand.", f"Learn how {short} follows load"],
         ["Algorithm", "A step-by-step recipe for learning from data.", "LinearRegression, DecisionTreeRegressor"],
         ["Model", "What the algorithm produces after it has learned from your data. It turns inputs into a prediction.", "A fitted line from load to " + short],
         ["Training", "Showing the algorithm the examples so it can set the numbers inside the model.", "model.fit(X_train, y_train)"],
         ["Prediction", "The model’s answer for a row it is given.", "model.predict(X_valid)"]],
        [170, 440, 258],
        "Five words for the whole field. Machine learning means a computer finds the rule from examples. An algorithm is the recipe it follows, for example linear regression or a decision tree. A model is what you get after the recipe has studied your data. Same recipe, different data, different model. Training means showing the algorithm the examples so that it can set the numbers inside the model, and in scikit-learn that is one call, fit. A prediction is the model's answer for a row, and that is the call predict. Keep this table in mind. Every later slide uses these five words.", lab(), size=17)
    C = table_slide(prs, "WORDS WE USE", "Words for the data and the task",
        ["Word", "Plain meaning", "Example from today"],
        [["Feature", "An input column the model uses to predict.", "load_pct, ambient_c"],
         ["Target", "The column we want to predict. Some books call it the label.", f"target ({short}, {unit})"],
         ["Regression", "Predicting a number.", f"{short.capitalize()} in {unit}"],
         ["Classification", "Predicting a category.", "Fault or no fault (Week 9)"],
         ["Feature engineering", "Building a new input column from the columns you already have.", "load_pct / 100 (Week 11)"]],
        [170, 440, 258],
        f"Now five words for the data. A feature is an input column, here the load percentage and the ambient temperature. The target is the column we want to predict, here {short}. Regression is the job of predicting a number, so today is regression. Classification is predicting a category, and we meet it next week. Feature engineering means building a new input column from the ones you have, for example dividing the load by one hundred. We come to that in Week 11, and it is worth knowing the name today.", lab(), size=17)
    D = figure_slide(prs, "Some rows stay hidden while the model learns", figdir / "hold_back.png",
        "Training rows teach. Validation rows compare models. Test rows are opened once, at the end.",
        "Think about studying for an exam. The practice questions you study from play the part of the training rows. A mock exam that you sit to check your progress plays the part of the validation rows, and you may change how you study after it. The real exam plays the part of the test rows, and nobody sees its questions beforehand. If a model were scored on rows it had already studied, its score would look better than it deserves, in the same way that a student who has memorised the answers does well on the practice paper. In our data, equipment E1 to E4 train the model, E5 is the validation group, and E6 is the final test.", lab())
    sc = K["sc"]
    E = figure_slide(prs, "A line through the points beats the average", figdir / f"scatter_{code}.png",
        f"Higher load goes with higher {short}. The line follows the dots; the dashed average ignores load.",
        f"Here is our own data. Each dot is one observation. Load runs along the bottom, and the {short} runs up the side. The dots rise from left to right, and across the {sc['n']} training rows the correlation between load and target is {sc['r']:.2f}, which is strong. Correlation is a number between minus one and one that says how closely the dots follow a straight path. The dashed grey line is the training average. It predicts the same value for every row, whatever the load. The green line follows the dots, so it gives a different prediction for each load. The orange diamonds are the validation rows. The model never sees them while it learns, and we will check how far they sit from each prediction. The test rows are not drawn, because they stay sealed.", lab())
    F = new_slide(prs); header(F, "ONE IDEA AT A TIME", "Training walks downhill on the loss", band=75, tsize=29.25)
    # restore compact band for this slide
    for sh in list(F.shapes)[:2]: pass
    F.shapes._spTree.remove(F.shapes[0]._element); F.shapes._spTree.remove(F.shapes[0]._element)
    shape_rect(F, 0, 0, 960, 75, INK); textbox(F, "Training walks downhill on the loss", 38, 15, 885, 51, 29.25, "FFFFFF", True)
    from PIL import Image
    iw, ih = Image.open(figdir / "loss_walk.png").size; sc_ = min(520 / iw, 372 / ih)
    F.shapes.add_picture(str(figdir / "loss_walk.png"), Pt(24), Pt(88), Pt(iw * sc_), Pt(ih * sc_))
    shape_rect(F, 568, 88, 368, 362, PALE2)
    textbox(F, [("Loss", True), "One number for how wrong the model is. We use the mean squared error.",
                ("Gradient", True), "Which way is downhill, and how steeply.",
                ("Learning rate", True), "The size of each step. Too big overshoots; too small takes too long.",
                ("Gradient descent", True), "Guess, measure the loss, step downhill, repeat."],
            582, 98, 340, 345, 17, INK, False, space_after=3)
    shape_rect(F, 0, 458, 960, 46, PALE2)
    textbox(F, "Each orange dot is one try at the slope. The loss falls as the slope approaches the best value.", 44, 464, 872, 38, 18, TEAL, True)
    footer(F, lab())
    set_notes(F, "So far we said that a model learns from examples. Here is how the learning works. Imagine a model with one adjustable number, a slope. For every slope, we can measure how wrong the model is, and we call that number the loss. We use the mean squared error that we met a few slides ago. If we plot the loss against the slope we get a bowl. The bottom of the bowl is the best slope. We start from a poor guess, here a slope of zero, and we ask which way is uphill and how steep it is. That answer is called the gradient. We step the opposite way, downhill. The size of the step is the learning rate. Then we measure again and repeat. This repeated stepping is called gradient descent. The curve on the left comes from a tiny example where the best slope is exactly two, so you can see each try land closer to the bottom.")
    G = code_slide(prs, "WORKED EXAMPLE", "Gradient descent in a few lines of NumPy", K["gd_code"], "step w loss\n" + K["gd_out"],
        ["The best slope is 2, because y is always twice x.", "w starts at 0. Each step moves it a little toward 2.",
         "learning_rate sets the size of each step. np.mean averages an array. ** is the power from Week 3.", "The loss falls on every step."],
        "LinearRegression finds its line with a direct formula. Gradient descent is the walk behind neural networks, which we train in Semester 2.",
        f"Here is the same walk as code. We have three points where y is always twice x, so the best slope is two. We start with a slope w of zero and a learning rate of zero point zero five. Inside the loop, the first line works out the gradient. For this loss it equals two times the average of x times the miss, and np dot mean is the NumPy tool that averages an array. You do not need to derive the formula now, because your calculus course shows where it comes from. The next line updates w by taking a step against the gradient, and the third line measures the loss, using the power symbol you met in Week 3. Look at the output. After one step w is {K['gd'][0][1]}, after two steps {K['gd'][1][1]}, and after five steps {K['gd'][4][1]}. The loss falls from {K['gd'][0][2]} to {K['gd'][4][2]}. The model has learned the slope from the data, with nobody typing the number two. LinearRegression in scikit-learn finds its line with a direct formula, so it does not loop like this. We show the loop because neural networks learn by this kind of repeated downhill step, and in Semester 2 you will train one. The calculus you already know is what makes the gradient work.", lab(), code_size=13, out_size=13)
    H = figure_slide(prs, "scikit-learn reads X as a table and y as a column", figdir / f"shape_{code}.png",
        "X has one row per observation and one column per feature. y holds one answer per row.",
        f"Before we call fit, we must hand scikit-learn the data in the shape it expects. On the left is our pandas table. The load and ambient columns are the features. They go into X, which is a grid with one row for each observation and one column for each feature. Here that is three rows and two columns, so we say its shape is three comma two. The target column goes into y. It is a single column of answers, one per row, so its shape is three with a comma and nothing after it. Underneath, pandas and scikit-learn both use a library called NumPy. NumPy stores numbers in arrays like these, and its shape tells you the rows and columns. When a model predicts, the answer it returns is also a NumPy array.", lab())
    I = code_slide(prs, "WORKED EXAMPLE", "NumPy arrays and their shape", K["shape_code"], K["shape_out"],
        ["np.array turns a list of numbers into an array.", "A list inside a list gives rows and columns.",
         "shape gives (rows, columns). One-dimensional y shows (rows,).", "predict returns an array. Call .tolist() to get a plain Python list."],
        "X has shape (3, 2) and y has shape (3,). Every row of X lines up with one entry of y.",
        f"Let us build the same arrays by hand. We import NumPy with the short name np. np.array turns a list of numbers into an array. A list of lists gives a grid, so X has three rows and two columns. y is a one-dimensional array of three numbers. The shape of X prints as three comma two. The shape of y prints as three with a comma and nothing after it, which means three entries and no second dimension. The mean of y is {round(float(K['ymean']), 3)}, in {unit}. Later, when we call predict, we will get an array back. If we want a plain Python list, for example to return from a function, we call dot tolist on it.", lab(), code_size=14.5, out_size=15)
    J = table_slide(prs, "ONE IDEA AT A TIME", "Four misses, measured three ways",
        ["Reading", "Actual", "Predicted", "Error (actual − predicted)", "Absolute error", "Squared error"],
        [[i + 1, K["act"][i], K["pred"][i], f"{K['err'][i]:+d}", K["ab"][i], K["sq"][i]] for i in range(4)],
        [92, 110, 130, 226, 160, 150],
        f"Here are four invented readings, so that we can do the arithmetic by eye. For each reading, the error is the actual value minus the predicted value. Sometimes it is negative. The absolute error drops the sign. The squared error multiplies the error by itself, so a big miss counts a lot more than a small one. Now average. The mean of the absolute errors is the MAE, two point seven five. It is in the same unit as the target, so it reads as: on average we miss by two point seven five {unit}. The mean of the squared errors is the MSE, twelve point two five. Its unit is the target unit squared, which is awkward to read. Take its square root and we get the RMSE, three point five, back in {unit}. Because of the squaring, RMSE is bigger than MAE whenever some misses are larger than others. The squared version, the MSE, returns a little later as the loss that training tries to lower.", lab(), size=19, row_h=46,
        below=[("MAE  = mean of the absolute errors = 2.75 " + unit, True),
               ("MSE  = mean of the squared errors = 12.25 (" + unit + " squared)", True),
               ("RMSE = square root of the MSE = 3.5 " + unit, True),
               "These four readings are invented to show the arithmetic."], below_size=19)

    # ordering: A,B,C before 'The supplied file'; D before 'Rows used for modelling'; E,F,G before 'Fitting a line'... see below
    for s_ in (A, B, C): move_slide(prs, s_, anchor_file)
    move_slide(prs, D, anchor_8)
    move_slide(prs, E, anchor_18)
    # F and G go after the existing 'Fitting a line' slide, so before the slide that follows it
    nxt = find_slide(prs, "Training a model with missing inputs")
    for s_ in (F, G): move_slide(prs, s_, nxt)
    for s_ in (H, I): move_slide(prs, s_, anchor_24)
    move_slide(prs, J, anchor_35)

    # 5. footers
    pat = re.compile(r"^" + re.escape(code) + r"\s+Week 8\s+\d+$")
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and pat.match(sh.text_frame.text.strip()):
                r = sh.text_frame.paragraphs[0].runs
                r[0].text = f"{code}   Week 8   {i}"
                for x in r[1:]: x.text = ""
    # python-pptx names new parts from the slide count, which collides with parts left
    # over from deleted slides. Give every slide and notes part a unique sequential name.
    from pptx.opc.packuri import PackURI
    for i, s in enumerate(prs.slides, 1):
        s.part.partname = PackURI(f"/ppt/slides/slide{i}.xml")
        if s.has_notes_slide:
            s.notes_slide.part.partname = PackURI(f"/ppt/notesSlides/notesSlide{i}.xml")
    dst.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(dst))
    import zipfile
    names = zipfile.ZipFile(dst).namelist()
    assert len(names) == len(set(names)), "duplicate parts in saved package"
    print(f"{code}: {len(prs.slides)} slides; removed {removed}; text repairs {count}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=None); a = ap.parse_args()
    out = Path(a.out) if a.out else DECKS
    backup = DECKS / "_backup_2026-10-30"
    for code, c in COHORTS.items():
        src = DECKS / c["file"]
        if a.out is None:
            backup.mkdir(exist_ok=True)
            if not (backup / c["file"]).exists(): shutil.copy2(src, backup / c["file"])
            src_for_patch = backup / c["file"]
        else:
            src_for_patch = (backup / c["file"]) if (backup / c["file"]).exists() else src
        patch_deck(code, c, src_for_patch, out / c["file"], FIGS)


if __name__ == "__main__":
    main()
