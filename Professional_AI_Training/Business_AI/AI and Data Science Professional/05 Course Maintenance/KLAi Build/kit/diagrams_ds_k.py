"""Figure kinds for Sessions 21 and 22 (text as data, language models, retrieval), author letter k. Each is registered as x_<kind> and used as visual=dict(kind='<kind>', ...).

Session 21
  k_msgtable       real rows of feedback.csv with the text variable highlighted
  k_preprocess     one message through the text preprocessing steps (text boxes and token boxes)
  k_regex          a small table of regular expression patterns (pattern in monospace, meaning, example)
  k_topwords       two bar panels of the most common words (document frequency)
  k_dtm            a document-term matrix (bag of words) for three short messages
  k_word_weights   the largest learned weights for each label (horizontal bars, one column per label)
  k_confusion3     a three-class confusion matrix with the diagonal in gold
  k_embed_map      an illustrative two-axis map of messages (made-up positions)
  k_cosine         three illustrative vector pairs with their angle and cosine
Session 22 kinds follow below in this file (k_tokens, k_nextword, k_context, k_temperature, k_chunks, k_rank, k_ctable).
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
import math

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K
from matplotlib.patches import Arc, Ellipse


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def mono_w(t, size):
    return 0.602 * size / 72 * len(t)


def wrapped(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', mono=False):
    """Wrapped text in a column of width w. Returns (number of lines, height in inches). y is the vertical centre (va centre) or the top (va top)."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, mono=mono)
    return len(lines), len(lines) * size * 1.15 / 72


def nlines(text, size, w, weight='normal'):
    return len(K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w))


def lineh(size, n=1):
    return n * size * 1.15 / 72


# ------------------------------------------------------------------ real rows of the feedback file
@fig('x_k_msgtable')
def k_msgtable(w, h, headers=(), rows=(), **_):
    s = Scene(w, h)
    size = 15
    cw = [0.95, 1.35, 1.3]
    mw = w - 0.1 - sum(cw) - 0.1
    x0 = 0.05
    s.text(x0, h - 0.22, 'feedback.csv: each record is one customer message', size=16, weight='bold', ha='left')
    ytop = h - 0.55
    hh = 0.46
    x = x0
    for i, hd in enumerate(headers):
        wd = cw[i] if i < 3 else mw
        s.rect(x, ytop - hh, wd, hh, fill=PALE, edge=INK, lw=1.2, z=2)
        s.text(x + 0.1, ytop - hh / 2, hd, size=size, weight='bold', ha='left')
        x += wd
    y = ytop - hh
    rhs = []
    for r in rows:
        k = nlines(r[3], size, mw - 0.2)
        rhs.append(max(0.6, lineh(size, k) + 0.2))
    for r, rh in zip(rows, rhs):
        x = x0
        for i, v in enumerate(r):
            wd = cw[i] if i < 3 else mw
            s.rect(x, y - rh, wd, rh, fill=GOLD if i == 3 else PAPER, edge=INK, lw=1.2, z=2)
            if i < 3:
                s.text(x + 0.1, y - rh / 2, v, size=size, ha='left')
            else:
                wrapped(s, x + 0.1, y - rh / 2, mw - 0.2, v, size)
            x += wd
        y -= rh
    s.text(x0, y - 0.32, 'The message is a text variable: a string with no fixed columns', size=15, weight='bold', color=RED, ha='left')
    return s


# ------------------------------------------------------------------ preprocessing steps on one message
@fig('x_k_preprocess')
def k_preprocess(w, h, stages=(), **_):
    s = Scene(w, h)
    n = len(stages)
    rh = (h - 0.05) / n
    lab_w = 4.7
    cx0 = lab_w + 0.35
    cw = w - cx0 - 0.05
    prev_tokens = []
    for i, (label, kind, content) in enumerate(stages):
        yc = h - 0.05 - (i + 0.5) * rh
        s.box(0.05, yc - rh / 2 + 0.06, lab_w, rh - 0.12, '', fill=GOLD if i in (0,) else PAPER, edge=INK, lw=1.6, r=0.05)
        wrapped(s, 0.2, yc, lab_w - 0.3, label, 16, 'bold', ha='left')
        s.arrow(lab_w + 0.1, yc, cx0 - 0.06, yc, color=INK, lw=2.0, head=14)
        if kind == 'text':
            size = 17
            while tw(content, size) > cw - 0.3 and size > 14:
                size -= 1
            s.box(cx0, yc - rh / 2 + 0.06, cw, rh - 0.12, '', fill=PAPER, edge=INK, lw=1.4, r=0.05)
            s.text(cx0 + 0.15, yc, content, size=size, ha='left')
        else:
            x = cx0
            kept = list(content)
            show = prev_tokens if (prev_tokens and len(prev_tokens) > len(kept)) else kept
            removed = [t for t in show if t not in kept] if show is not kept else []
            seq = []
            ki = 0
            for t in show:
                if ki < len(kept) and t == kept[ki]:
                    seq.append((t, False))
                    ki += 1
                else:
                    seq.append((t, True))
            for t, gone in seq:
                bw = tw(t, 17) + 0.34
                s.box(x, yc - 0.27, bw, 0.54, t, size=17, fill=PAPER if gone else GOLD, edge=MUTE if gone else INK, color=MUTE if gone else INK, lw=1.4, r=0.05, dash=gone)
                x += bw + 0.1
            if removed:
                s.text(x + 0.1, yc, 'removed: ' + ', '.join(removed), size=16, color=RED, weight='bold', ha='left')
            prev_tokens = list(content)
            if not removed:
                prev_tokens = list(content)
    return s


# ------------------------------------------------------------------ regex patterns
@fig('x_k_regex')
def k_regex(w, h, headers=(), rows=(), **_):
    s = Scene(w, h)
    size = 15
    cw = [2.0, 3.0, w - 5.0 - 0.1]
    x0 = 0.05
    ytop = h - 0.05
    hh = 0.46
    x = x0
    for i, hd in enumerate(headers):
        s.rect(x, ytop - hh, cw[i], hh, fill=PALE, edge=INK, lw=1.2, z=2)
        s.text(x + 0.1, ytop - hh / 2, hd, size=size, weight='bold', ha='left')
        x += cw[i]
    y = ytop - hh
    rh = (h - 0.05 - hh) / len(rows)
    for r in rows:
        x = x0
        for i, v in enumerate(r):
            s.rect(x, y - rh, cw[i], rh, fill=INK if i == 0 else PAPER, edge=INK, lw=1.2, z=2)
            if i == 0:
                s.text(x + 0.1, y - rh / 2, v, size=15, color=PAPER, mono=True, ha='left')
            else:
                wrapped(s, x + 0.1, y - rh / 2, cw[i] - 0.2, v, size)
            x += cw[i]
        y -= rh
    return s


# ------------------------------------------------------------------ two bar panels of the most common words
@fig('x_k_topwords')
def k_topwords(w, h, left=(), right=(), left_title='', right_title='', total=800, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    mx = max(max(v for _, v in left), max(v for _, v in right))
    for k, (title, data) in enumerate(((left_title, left), (right_title, right))):
        px = 0.05 + k * (pw + 0.3)
        s.text(px, h - 0.25, title, size=17, weight='bold', ha='left')
        row = (h - 0.7) / len(data)
        lab = 1.45
        bw_max = pw - lab - 0.2 - 0.7
        for i, (wd, v) in enumerate(data):
            yc = h - 0.6 - (i + 0.5) * row
            s.text(px + lab, yc, wd, size=16, ha='right')
            bw = max(0.05, bw_max * v / mx)
            s.rect(px + lab + 0.15, yc - row * 0.3, bw, row * 0.6, fill=GOLD if k else INK, edge=INK, lw=1.6)
            s.text(px + lab + 0.15 + bw + 0.12, yc, str(v), size=16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ document-term matrix
@fig('x_k_dtm')
def k_dtm(w, h, rows=(), vocab=(), msgs=(), **_):
    s = Scene(w, h)
    size = 15
    y = h - 0.05
    for m in msgs:
        s.text(0.05, y - 0.16, m, size=size, ha='left')
        y -= 0.34
    y -= 0.12
    lab_w = 1.5
    n = len(vocab)
    cw = (w - 0.1 - lab_w) / n
    head_h = max(tw(v, size) for v in vocab) + 0.3
    s.rect(0.05, y - head_h, lab_w, head_h, fill=PALE, edge=INK, lw=1.2, z=2)
    s.text(0.15, y - head_h / 2, 'Message', size=size, weight='bold', ha='left')
    for j, v in enumerate(vocab):
        x = 0.05 + lab_w + j * cw
        s.rect(x, y - head_h, cw, head_h, fill=PALE, edge=INK, lw=1.2, z=2)
        s.text(x + cw / 2, y - head_h / 2, v, size=size, weight='bold', rot=90)
    y -= head_h
    rh = 0.46
    for lab, counts in rows:
        s.rect(0.05, y - rh, lab_w, rh, fill=PAPER, edge=INK, lw=1.2, z=2)
        s.text(0.15, y - rh / 2, lab, size=size, weight='bold', ha='left')
        for j, c in enumerate(counts):
            x = 0.05 + lab_w + j * cw
            s.rect(x, y - rh, cw, rh, fill=GOLD if c else PAPER, edge=INK, lw=1.2, z=2)
            s.text(x + cw / 2, y - rh / 2, str(c), size=17, weight='bold' if c else 'normal', color=INK if c else MUTE)
        y -= rh
    s.text(0.05, max(y - 0.3, 0.2), 'Gold cell: the word appears. The number is how many times. Order is lost.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ learned weights per label
@fig('x_k_word_weights')
def k_word_weights(w, h, columns=(), **_):
    s = Scene(w, h)
    n = len(columns)
    gap = 0.2
    cw = (w - 0.1 - gap * (n - 1)) / n
    mx = max(v for _, ws in columns for _, v in ws)
    colors = {'negative': RED, 'neutral': GREY, 'positive': GOLD}
    for k, (title, ws) in enumerate(columns):
        x = 0.05 + k * (cw + gap)
        s.box(x, h - 0.55, cw, 0.5, title, size=17, weight='bold', fill=INK, edge=INK, color=PAPER, r=0.05)
        row = (h - 0.75) / len(ws)
        for i, (wd, v) in enumerate(ws):
            yt = h - 0.7 - i * row
            s.text(x + 0.05, yt - 0.2, wd, size=16, ha='left', weight='bold')
            bl = max(0.05, (cw - 0.65) * v / mx)
            s.rect(x + 0.05, yt - row + 0.1, bl, 0.28, fill=colors.get(title, GREY), edge=INK, lw=1.5)
            s.text(x + 0.05 + bl + 0.1, yt - row + 0.24, f'{v:.1f}', size=15, ha='left')
    return s


# ------------------------------------------------------------------ three-class confusion matrix
@fig('x_k_confusion3')
def k_confusion3(w, h, labels=(), cm=(), **_):
    s = Scene(w, h)
    lw_, top = 1.7, 0.95
    n = len(labels)
    cw = (w - lw_ - 0.1) / n
    ch = (h - top - 0.1) / n
    s.text(lw_ + cw * n / 2, h - 0.2, 'What the model said', size=16, weight='bold')
    for j, lab in enumerate(labels):
        s.text(lw_ + (j + 0.5) * cw, h - 0.65, lab, size=16)
    for i, lab in enumerate(labels):
        yc = h - top - (i + 0.5) * ch
        s.text(lw_ - 0.15, yc + 0.18, 'True', size=14, color=MUTE, ha='right')
        s.text(lw_ - 0.15, yc - 0.12, lab, size=16, ha='right')
        for j in range(n):
            x = lw_ + j * cw
            s.box(x + 0.04, yc - ch / 2 + 0.04, cw - 0.08, ch - 0.08, str(cm[i][j]), size=30, weight='bold' if i == j else 'normal', fill=GOLD if i == j else PAPER, edge=INK, lw=1.8, r=0.05,
                  color=INK if cm[i][j] else MUTE)
    return s


# ------------------------------------------------------------------ illustrative map of meaning
@fig('x_k_embed_map')
def k_embed_map(w, h, points=(), x_label='', y_label='', **_):
    s = Scene(w, h)
    ox, oy = 0.55, 0.65
    pw, ph = w - ox - 0.1, h - oy - 0.1
    s.rect(ox, oy, pw, ph, fill=PAPER, edge=INK, lw=1.8)
    s.text(ox + pw / 2, 0.3, x_label, size=15, color=MUTE)
    s.text(0.22, oy + ph / 2, y_label, size=15, color=MUTE, rot=90)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_lo, x_hi, y_lo, y_hi = 0.0, 6.0, 0.8, 5.0

    def px(v):
        return ox + 0.15 + (v - x_lo) / (x_hi - x_lo) * (pw - 0.3)

    def py(v):
        return oy + 0.15 + (v - y_lo) / (y_hi - y_lo) * (ph - 0.3)
    cols = {0: RED, 1: GOLD, 2: INK}
    groups = {}
    for x, y, lab, g in points:
        groups.setdefault(g, []).append((x, y))
    for g, pts in groups.items():
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        r = max(math.hypot(px(p[0]) - px(cx), py(p[1]) - py(cy)) for p in pts) + 0.3
        s.ax.add_patch(Ellipse((px(cx), py(cy)), 2 * r + 0.2, 2 * r, fc='none', ec=cols[g], lw=2.0, ls='--', zorder=1))
    for x, y, lab, g in points:
        s.circle(px(x), py(y), 0.11, fill=cols[g], edge=INK, lw=1.6, z=4)
        right = px(x) + 0.2 + tw(lab, 15) < ox + pw - 0.05
        if right:
            s.text(px(x) + 0.2, py(y), lab, size=15, ha='left')
        else:
            s.text(px(x) - 0.2, py(y), lab, size=15, ha='right')
    return s


# ------------------------------------------------------------------ cosine similarity pictures
@fig('x_k_cosine')
def k_cosine(w, h, pairs=(), **_):
    s = Scene(w, h)
    n = len(pairs)
    gap = 0.15
    pw = (w - 0.1 - gap * (n - 1)) / n
    side = min(pw, 2.4)
    top = h - 0.1
    unit = side / 9.4
    for k, (a, b, lab, c) in enumerate(pairs):
        x0 = 0.05 + k * (pw + gap)
        cx, cy = x0 + pw / 2, top - side / 2
        s.rect(cx - side / 2, cy - side / 2, side, side, fill=PAPER, edge=GREY, lw=1.4)
        s.line(cx - side / 2, cy, cx + side / 2, cy, color=HAIR, lw=1.2, z=1)
        s.line(cx, cy - side / 2, cx, cy + side / 2, color=HAIR, lw=1.2, z=1)
        s.arrow(cx, cy, cx + a[0] * unit, cy + a[1] * unit, color=INK, lw=3.2, head=18)
        s.arrow(cx, cy, cx + b[0] * unit, cy + b[1] * unit, color=RED, lw=3.2, head=18)
        ang = math.degrees(math.acos(max(-1, min(1, (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))))))
        a0 = math.degrees(math.atan2(a[1], a[0]))
        b0 = math.degrees(math.atan2(b[1], b[0]))
        t1, t2 = (a0, b0) if (b0 - a0) % 360 <= 180 else (b0, a0)
        r = side * 0.2
        if ang < 175:
            s.ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=t1, theta2=t2 if t2 > t1 else t2 + 360, color=GOLD, lw=4, zorder=5))
        y = top - side - 0.3
        s.text(cx, y, lab, size=16, weight='bold')
        s.text(cx, y - 0.4, f'angle {ang:.0f} degrees', size=15, color=BODY)
        s.text(cx, y - 0.85, f'cosine {c:.3f}', size=20, weight='bold', color=RED if c < 0.5 else INK)
    return s


# ================================================================== Session 22
# ------------------------------------------------------------------ tokens
@fig('x_k_tokens')
def k_tokens(w, h, tokens=(), ids=(), words=0, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.3, 'Text:  ' + ' '.join(tokens).replace(' .', '.').replace('Lake side', 'Lakeside'), size=18, ha='left', weight='bold')
    gap = 0.12
    bws = [tw(t, 20) + 0.5 for t in tokens]
    scale = min(1.0, (w - 0.1 - gap * (len(tokens) - 1)) / sum(bws))
    x = 0.05
    ytop = h - 1.25
    for t, i, bw in zip(tokens, ids, bws):
        bw *= scale
        s.box(x, ytop - 0.7, bw, 0.7, t, size=20, fill=GOLD, edge=INK, lw=1.8, r=0.06)
        s.text(x + bw / 2, ytop - 1.05, str(i), size=16, color=BODY)
        x += bw + gap
    s.box(0.05, 0.15, w - 0.1, 0.65, f'{words} words became {len(tokens)} tokens', size=22, weight='bold', fill=PALE, edge=INK, lw=1.6, r=0.06)
    return s


# ------------------------------------------------------------------ next word probabilities
@fig('x_k_nextword')
def k_nextword(w, h, context='', items=(), other=0.0, note='', **_):
    s = Scene(w, h)
    s.box(0.05, h - 0.75, w - 0.1, 0.6, context, size=22, weight='bold', fill=PALE, edge=INK, lw=1.6, r=0.06)
    allitems = [(a, b) for a, b in items] + [('all other words', other)]
    row = (h - 1.0 - 0.9) / len(allitems)
    lab = 2.3
    bmax = w - lab - 1.5
    mx = max(p for _, p in allitems)
    for i, (wd, p) in enumerate(allitems):
        yc = h - 1.0 - (i + 0.5) * row
        s.text(lab, yc, wd, size=17, ha='right')
        bw = max(0.05, bmax * p / mx)
        s.rect(lab + 0.15, yc - row * 0.3, bw, row * 0.6, fill=GREY if wd == 'all other words' else GOLD, edge=INK, lw=1.6)
        s.text(lab + 0.15 + bw + 0.12, yc, f'{p:.0%}', size=17, weight='bold', ha='left')
    wrapped(s, 0.1, 0.4, w - 0.2, note, 15, color=BODY)
    return s


# ------------------------------------------------------------------ context window
@fig('x_k_context')
def k_context(w, h, big_label='', small=(), small_label='', window_label='', **_):
    s = Scene(w, h)
    wx0, wx1 = 0.4, 7.4
    wy0, wy1 = 0.55, h - 0.55
    s.rect(wx0, wy0, wx1 - wx0, wy1 - wy0, fill=PAPER, edge=RED, lw=3.0)
    s.ax.patches[-1].set_linestyle('--')
    s.text(wx0, h - 0.28, window_label, size=16, weight='bold', color=RED, ha='left')
    # big bar overflowing the window
    by = wy1 - 1.0
    s.rect(wx0 + 0.2, by, w - wx0 - 0.4, 0.7, fill=INK, edge=INK, lw=1.5)
    s.text(wx0 + 0.35, by + 0.35, big_label, size=16, color=PAPER, ha='left', weight='bold')
    s.arrow(wx1 + 0.2, by + 0.35, w - 0.3, by + 0.35, color=GOLD, lw=3, head=16, z=8)
    s.text(wx1 + 0.3, by - 0.3, 'does not fit', size=16, weight='bold', color=RED, ha='left')
    # small bar fits
    sy = wy0 + 0.55
    tot = sum(v for _, v in small)
    avail = 5.4
    x = wx0 + 0.2
    cols = [PALE, GOLD, PAPER]
    for (lab, v), c in zip(small, cols):
        bw = 1.5 + 2.6 * v / tot
        s.box(x, sy, bw - 0.08, 0.7, f'{lab}: {v}', size=15, weight='bold', fill=c, edge=INK, lw=1.6, r=0.04)
        x += bw
    s.text(wx0 + 0.2, sy - 0.28, small_label, size=16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ temperature
@fig('x_k_temperature')
def k_temperature(w, h, words=(), groups=(), **_):
    s = Scene(w, h)
    n = len(groups)
    ph = (h - 0.1) / n
    lab = 1.2
    bmax = w - lab - 1.4
    for g, (t, ps) in enumerate(groups):
        y0 = h - 0.05 - g * ph
        s.text(0.05, y0 - 0.22, f'Temperature {t:g}', size=16, weight='bold', ha='left')
        row = (ph - 0.4) / len(words)
        for i, (wd, p) in enumerate(zip(words, ps)):
            yc = y0 - 0.45 - (i + 0.5) * row
            s.text(lab + 0.6, yc, wd, size=14, ha='right')
            bw = max(0.04, bmax * p)
            s.rect(lab + 0.75, yc - row * 0.32, bw, row * 0.64, fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.4)
            s.text(lab + 0.75 + bw + 0.1, yc, f'{p:.0%}', size=14, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ chunks of one document
@fig('x_k_chunks')
def k_chunks(w, h, title='', chunks=(), total='', **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.2, title, size=17, weight='bold', ha='left', mono=False)
    n = len(chunks)
    row = (h - 0.45 - 0.55) / n
    size = 15
    for i, c in enumerate(chunks):
        yb = h - 0.45 - (i + 1) * row
        s.box(0.05, yb + 0.03, 1.15, row - 0.06, f'chunk {i + 1}', size=14, weight='bold', fill=INK, edge=INK, color=PAPER, r=0.04)
        s.box(1.25, yb + 0.03, w - 1.3, row - 0.06, '', fill=GOLD if i % 2 == 0 else PALE, edge=INK, lw=1.3, r=0.04)
        s.text(1.4, yb + row / 2, c, size=size, ha='left')
    s.text(0.05, 0.25, total, size=16, weight='bold', color=RED, ha='left')
    return s


# ------------------------------------------------------------------ a ranked list with the relevant chunks in gold
@fig('x_k_rank')
def k_rank(w, h, items=(), total_rel=3, k=5, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'Search results, best first (illustrative)', size=17, weight='bold', ha='left')
    row = (h - 2.1) / len(items)
    for i, (r, name, rel) in enumerate(items):
        yb = h - 0.55 - (i + 1) * row
        s.box(0.05, yb + 0.04, 0.6, row - 0.08, str(r), size=17, weight='bold', fill=INK, edge=INK, color=PAPER, r=0.04)
        s.box(0.75, yb + 0.04, 3.2, row - 0.08, name, size=17, fill=GOLD if rel else PAPER, edge=INK, lw=1.6, r=0.04)
        s.text(4.1, yb + row / 2, 'right' if rel else 'wrong', size=16, weight='bold' if rel else 'normal', color=INK if rel else MUTE, ha='left')
    hits = sum(1 for _, _, r in items if r)
    s.text(0.05, 0.85, f'Right chunks in the top {k}: {hits}', size=17, ha='left')
    s.text(0.05, 0.45, f'Right chunks in the whole library: {total_rel}', size=17, ha='left')
    return s


# ------------------------------------------------------------------ precision and recall at k for k = 1, 3, 5
@fig('x_k_prk')
def k_prk(w, h, groups=(), **_):
    s = Scene(w, h)
    n = len(groups)
    gw = (w - 0.4) / n
    base = 0.9
    top = h - 0.8
    s.line(0.2, base, w - 0.2, base, color=INK, lw=2)
    s.box(0.2, h - 0.5, 0.3, 0.3, '', fill=INK, edge=INK, r=0.03)
    s.text(0.6, h - 0.35, 'Precision at k', size=15, ha='left')
    s.box(2.9, h - 0.5, 0.3, 0.3, '', fill=GOLD, edge=INK, r=0.03)
    s.text(3.3, h - 0.35, 'Recall at k', size=15, ha='left')
    for i, (k, p, r) in enumerate(groups):
        x0 = 0.2 + i * gw
        bw = gw * 0.32
        for j, (v, col) in enumerate(((p, INK), (r, GOLD))):
            bh = (top - base - 0.35) * v
            xb = x0 + gw * 0.12 + j * (bw + 0.08)
            s.rect(xb, base, bw, max(0.03, bh), fill=col, edge=INK, lw=1.6)
            s.text(xb + bw / 2, base + bh + 0.22, f'{v:.2f}', size=15, weight='bold')
        s.text(x0 + gw * 0.12 + bw + 0.04, base - 0.35, f'k = {k}', size=17, weight='bold')
    return s
