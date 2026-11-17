"""Figures for the Enterprise Data Readiness for AI decks, drawn from the Kitara teaching data (numpy, pandas, matplotlib, pypdf, pdfplumber, pytesseract).

  python3 figs.py DATA_FOLDER OUTPUT_FOLDER [figure_name ...]

Writes one PNG per figure plus catalog.json (name -> description, alt, width_in) into OUTPUT_FOLDER. Name figures on the command line to redraw only those.
Figures built from the data compute every number from the files in DATA_FOLDER (and from kitara_search.py for search results). Diagrams say so inside the image.
Everything is drawn on a canvas measured in inches, so a figure shown at its width_in has labels of the size written here (13 points or more).
"""
import sys, json, re, subprocess, tempfile, textwrap, difflib, os
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge, FancyArrowPatch, PathPatch
from matplotlib.path import Path as MPath
import matplotlib.patheffects as pe

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kitara_search as ks
import kitara_tables as KT
import curriculum as CUR

INK, CHAR, GREY, CLAY, MOSS, HAIR, PAPER = '#1F2328', '#4B4640', '#8B8478', '#B04A2B', '#5E7A57', '#C9C5BC', '#FFFFFF'
_names = {f.name for f in fm.fontManager.ttflist}
SANS = 'Carlito' if 'Carlito' in _names else 'DejaVu Sans'
SERIF = 'Liberation Serif' if 'Liberation Serif' in _names else 'DejaVu Serif'
plt.rcParams.update({'font.family': SANS, 'hatch.linewidth': 0.6, 'savefig.dpi': 200, 'figure.dpi': 100, 'text.antialiased': True})

CAT = {}      # name -> (width_in, function)
INFO = {}     # name -> (description, alt, width_in)
DATA = None   # set in main


def fig(name, width_in):
    def deco(f):
        CAT[name] = (width_in, f)
        return f
    return deco


# ============================================================================ drawing helpers (canvas in inches, y up)
def canvas(w, h):
    f = plt.figure(figsize=(w, h), facecolor=PAPER)
    ax = f.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    ax.W, ax.H = w, h
    return f, ax


def T(ax, x, y, s, size=13, color=INK, weight='normal', ha='left', va='center', family=None, style='normal', **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, family=family or SANS, style=style, **kw)


def title(ax, s):
    T(ax, 0.3, ax.H - 0.32, s, size=17, weight='bold', family=SERIF)


def note(ax, s, y=0.17, x=None, ha='right'):
    T(ax, (ax.W - 0.25) if x is None else x, y, s, size=12, color=GREY, ha=ha, style='italic')


def line(ax, x0, y0, x1, y1, color=HAIR, lw=0.8, **kw):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle='butt', **kw)


def rect(ax, x, y, w, h, fc='none', ec='none', lw=0.8, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, **kw))


def dot(ax, x, y, r, fc, ec='none', lw=1.0, z=3):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=z))


def _r(ax):
    return ax.figure.canvas.get_renderer()


def tw(ax, s, size=13, weight='normal', family=None, style='normal'):
    t = ax.text(0, 0, s, fontsize=size, fontweight=weight, family=family or SANS, style=style)
    w = t.get_window_extent(renderer=_r(ax)).width / ax.figure.dpi
    t.remove()
    return w


def wrap(ax, s, maxw, size=13, weight='normal', family=None, style='normal'):
    out = []
    for para in str(s).split('\n'):
        cur = ''
        for word in para.split(' '):
            trial = (cur + ' ' + word).strip()
            if cur and tw(ax, trial, size, weight, family, style) > maxw:
                out.append(cur)
                cur = word
            else:
                cur = trial
        out.append(cur)
    return out


def fit(ax, s, maxw, size=13, weight='normal', family=None):
    if tw(ax, s, size, weight, family) <= maxw:
        return s
    while len(s) > 1 and tw(ax, s + '...', size, weight, family) > maxw:
        s = s[:-1]
    return s.rstrip() + '...'


def para(ax, x, ytop, s, maxw, size=13, color=INK, lh=0.215, weight='normal', family=None, style='normal', ha='left'):
    """Draw wrapped text from ytop downwards. Returns the y below the last line."""
    lines = wrap(ax, s, maxw, size, weight, family, style)
    for i, ln in enumerate(lines):
        T(ax, x, ytop - (i + 0.5) * lh, ln, size=size, color=color, weight=weight, family=family, style=style, ha=ha)
    return ytop - len(lines) * lh


def flow(ax, x, y, parts, size=13, family=None):
    """parts: list of (text, color, weight). Draws left to right, returns the end x."""
    sp = tw(ax, 'x x', size, family=family) - tw(ax, 'xx', size, family=family)
    for i, (s, c, wt) in enumerate(parts):
        T(ax, x, y, s, size=size, color=c, weight=wt, family=family)
        x += tw(ax, s, size, wt, family) + (sp if i < len(parts) - 1 else 0)
    return x


def save(f, name):
    f.savefig(Path(OUT) / f'{name}.png', facecolor=PAPER)
    plt.close(f)


def shortname(s):
    return re.sub(r'^Kitara Group ', '', str(s))


# ============================================================================ data and shared computations
_cache = {}


def csv(name, **kw):
    k = ('csv', name)
    if k not in _cache:
        _cache[k] = pd.read_csv(Path(DATA) / f'{name}.csv', **kw)
    return _cache[k].copy()


def customers():
    return csv('customers', dtype=str, keep_default_na=False)


def dim_scores():
    ev = csv('readiness_evidence')
    base = ev.groupby('dimension').proposed_score.mean()
    adj = ev[ev.self_reported == 'N'].groupby('dimension').proposed_score.mean()
    dims = list(dict.fromkeys(ev.dimension))
    return dims, base.reindex(dims), adj.reindex(dims)


def corpus():
    if 'corpus' not in _cache:
        _cache['corpus'] = ks.load_corpus(DATA)
    return _cache['corpus']


def searcher():
    if 'searcher' not in _cache:
        ch = ks.build_chunks(corpus())
        _cache['chunks'] = ch
        _cache['searcher'] = ks.Searcher(ch)
    return _cache['searcher']


def lists(query, allowed=None):
    """Chunk-position ranked lists for one query: keyword, stand-in meaning and their fusion (all chunks allowed unless a mask is given)."""
    s = searcher()
    n = len(s.chunks)
    al = np.ones(n, bool) if allowed is None else allowed
    bs = s.bm25.scores(query)
    rb = s._rank(bs, al & (bs > 0))
    rm = s._rank(s.meaning.scores(query), al)
    return rb, rm, ks.rrf([rb, rm])


def first_rank(order, doc_ids, gold):
    for i, p in enumerate(order, start=1):
        if doc_ids[p] == gold:
            return i
    return 0


def evalq():
    return csv('eval_questions')


def doc_title(doc_id):
    m = _cache.setdefault('meta', csv('docs_metadata'))
    return m.set_index('doc_id').title[doc_id]


def pdf_page_png(pdf, dpi, first=1):
    td = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(first), '-l', str(first), '-png', str(pdf), os.path.join(td, 'p')], check=True)
    from PIL import Image
    p = sorted(Path(td).glob('p*.png'))[0]
    return Image.open(p).convert('RGB')


# ============================================================================ 1 maturity_levels
@fig('maturity_levels', 12.4)
def f_levels():
    levels, dims = CUR.LEVELS, CUR.DIMENSIONS
    assert levels == ['Ad hoc', 'Developing', 'Defined', 'Managed', 'Optimised'] and len(dims) == 5
    says = ['Done by a few people, from memory', 'Some practice exists, but it depends on individuals',
            'Written down, owned, and checked at least once a year', 'Measured every month, with an alert when it slips',
            'Improved from what the measures show']
    _, base, _a = dim_scores()
    overall = float(base.mean())
    f, ax = canvas(12.4, 4.6)
    title(ax, 'Five levels, from ad hoc to optimised, and what you can show at each')
    x0, cw = 0.4, 2.32
    ys = [0.75 + 0.5 * i for i in range(5)]
    pts = [(x0, 0.4)]
    for i in range(5):
        pts += [(x0 + i * cw, ys[i]), (x0 + (i + 1) * cw, ys[i])]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK, lw=2.2, solid_joinstyle='miter')
    for i in range(5):
        lines = wrap(ax, says[i], cw - 0.3)
        yb = ys[i] + 0.14
        for j, ln in enumerate(reversed(lines)):
            T(ax, x0 + i * cw + 0.12, yb + (j + 0.5) * 0.215, ln, size=13, color=CHAR)
        T(ax, x0 + i * cw + 0.12, yb + len(lines) * 0.215 + 0.2, f'{i + 1}  {levels[i]}', size=16, weight='bold', family=SERIF)
    mx = x0 + (overall - 0.5) * cw
    ax.add_patch(Polygon([(mx - 0.11, ys[1] - 0.34), (mx + 0.11, ys[1] - 0.34), (mx, ys[1] - 0.12)], fc=CLAY, ec='none', zorder=4))
    T(ax, mx, ys[1] - 0.55, f'Kitara today: {overall:.1f}', size=14, color=CLAY, weight='bold', ha='center')
    note(ax, 'Illustrative scale. Each framework words its levels differently. Kitara score from readiness_evidence.csv.')
    save(f, 'maturity_levels')
    return dict(description=f'A five step staircase drawn as one ink line, rising left to right: 1 Ad hoc, 2 Developing, 3 Defined, 4 Managed, 5 Optimised. Each step has one plain line on what the organisation can show; level 3 reads "Written down, owned, and checked at least once a year". A clay triangle under the staircase marks Kitara today at {overall:.1f}, the mean of the five dimension scores in readiness_evidence.csv. The scale itself is illustrative.',
                alt=f'A staircase of five maturity levels from ad hoc to optimised with Kitara marked at {overall:.1f}, between developing and defined.')


# ============================================================================ 2 baseline_scores
@fig('baseline_scores', 7.0)
def f_baseline():
    dims, base, adj = dim_scores()
    weakest = base.idxmin()
    f, ax = canvas(7.0, 4.4)
    title(ax, f'{weakest} is the weakest dimension at {base[weakest]:.1f} of 5')
    flow(ax, 0.3, 3.72, [('Bar: score as proposed.', CHAR, 'normal'), ('Circle: after removing self-reported items.', CHAR, 'normal')], size=13)
    xl, scale = 2.75, 0.62
    ytop = 3.12
    for v in range(0, 6):
        x = xl + v * scale
        line(ax, x, 0.62, x, 3.42, HAIR, 0.8)
        T(ax, x, 0.4, str(v), size=13, color=GREY, ha='center')
    for i, d in enumerate(dims):
        y = ytop - i * 0.5
        lab = wrap(ax, d, 2.35, 13)
        for j, ln in enumerate(lab):
            T(ax, 0.3, y + (len(lab) - 1) * 0.1 - j * 0.2, ln, size=13, color=INK)
        col = CLAY if d == weakest else CHAR
        rect(ax, xl, y - 0.13, base[d] * scale, 0.26, fc=col)
        dot(ax, xl + adj[d] * scale, y, 0.095, PAPER, INK, 1.6, z=5)
        end = max(base[d], adj[d]) * scale + xl + 0.17
        T(ax, end, y, f'{base[d]:.1f}  ({adj[d]:.1f})', size=13, color=col if d == weakest else INK, weight='bold' if d == weakest else 'normal',
          path_effects=[pe.withStroke(linewidth=4, foreground=PAPER)], zorder=6)
    note(ax, 'Scores are means of the evidence items in readiness_evidence.csv.', y=0.1)
    save(f, 'baseline_scores')
    drop = (base - adj)
    return dict(description=f'Horizontal bars for the five Kitara dimension scores computed from readiness_evidence.csv (mean of proposed_score): ' + '; '.join(f'{d} {base[d]:.2f}' for d in dims) + f'. A hollow circle on each row shows the score after the {int((csv("readiness_evidence").self_reported == "Y").sum())} self-reported items are removed: ' + '; '.join(f'{adj[d]:.2f}' for d in dims) + f'. The weakest dimension by baseline, {weakest}, is clay. Numbers at the bar ends read baseline then (adjusted).',
                alt=f'Bar chart of five readiness scores with {weakest} lowest at {base[weakest]:.1f}, and hollow markers showing lower scores once self-reported evidence is removed.')


# ============================================================================ 3 use_case_data_map
@fig('use_case_data_map', 12.4)
def f_use_map():
    src = csv('sources').set_index('source_id')
    md = csv('docs_metadata')
    cu = customers()
    mm = csv('mobile_money_log', dtype=str)
    ev = evalq()
    # evidence behind each judgement, read from the files
    n_policy = int(((md.family == 'policy') & md.format.isin(['text_pdf', 'docx'])).sum())
    n_letters = int(((md.family == 'claims_letter') & (md.format == 'text_pdf')).sum())
    n_sup = int((md.status == 'superseded').sum())
    assert n_policy > 0 and n_letters == 30 and n_sup > 0
    assert pd.isna(src.loc['S09', 'owner']) and src.loc['S06', 'owner'] == 'IT' and src.loc['S02', 'owner'] == 'IT' and pd.notna(src.loc['S01', 'owner'])
    assert not any('fraud' in c.lower() or 'label' in c.lower() for c in mm.columns)       # no fraud label in the transaction log
    assert not any(c in cu.columns for c in ['churn', 'churned', 'closed_date'])           # status exists, a dated churn flag does not
    assert set(cu.status) >= {'Active', 'Dormant', 'Closed'} and 'msisdn_hash' in mm.columns and 'phone' in cu.columns
    n_tx = len(mm)
    A, P, M, N = 'available', 'partly', 'missing', ''
    cols = ['Staff policy assistant', 'Claims letter triage', 'Customer churn prediction', 'Fraud flagging on mobile money']
    rows = [
        ('Text of the documents it reads', [A, A, N, N]),
        ('Which version is current', [P, N, N, N]),
        ('Known outcomes to learn from', [N, M, P, M]),
        ('Transactions or history', [N, N, M, A]),
        ('Quality fit for use', [P, P, P, P]),
        ('A named owner', [M, P, A, P]),
    ]
    f, ax = canvas(12.4, 4.8)
    title(ax, 'What each Kitara use case needs, and what the data files hold today')
    lx, cx0, cw = 0.3, 3.55, 2.2
    for j, c in enumerate(cols):
        ls = wrap(ax, c, cw - 0.3, 14, 'bold')
        for k, ln in enumerate(ls):
            T(ax, cx0 + j * cw, 3.98 - k * 0.22, ln, size=14, weight='bold')
    line(ax, 0.3, 3.5, 12.1, 3.5, INK, 1.0)
    for i, (lab, cells) in enumerate(rows):
        y = 3.12 - i * 0.43
        T(ax, lx, y, lab, size=13.5)
        if i < len(rows) - 1:
            line(ax, 0.3, y - 0.215, 12.1, y - 0.215, HAIR, 0.6)
        for j, c in enumerate(cells):
            x = cx0 + j * cw
            if c == '':
                T(ax, x + 0.02, y, 'not needed', size=13, color=HAIR)
                continue
            if c == A:
                dot(ax, x + 0.09, y, 0.085, MOSS)
                T(ax, x + 0.27, y, 'available', size=13.5, color=MOSS, weight='bold')
            elif c == P:
                dot(ax, x + 0.09, y, 0.085, PAPER, CHAR, 1.4)
                ax.add_patch(Wedge((x + 0.09, y), 0.085, 90, 270, fc=CHAR, ec='none', zorder=4))
                T(ax, x + 0.27, y, 'partly', size=13.5, color=CHAR, weight='bold')
            else:
                dot(ax, x + 0.09, y, 0.085, PAPER, CLAY, 1.8)
                T(ax, x + 0.27, y, 'missing', size=13.5, color=CLAY, weight='bold')
    note(ax, f'Judged from sources.csv, docs_metadata.csv, customers.csv and mobile_money_log.csv ({n_tx:,} transactions, no fraud flag, hashed phone). Partly = there, but with a known flaw.', y=0.2, ha='right')
    save(f, 'use_case_data_map')
    return dict(description=f'A grid of four Kitara use cases (staff policy assistant, claims letter triage, customer churn prediction, fraud flagging on mobile money) against six data needs, each cell marked available (moss dot), partly (half dot) or missing (clay ring), or left as not needed. Judgements rest on the files: {n_policy} policy documents and {n_letters} text claims letters exist; superseded status ({n_sup} documents) is held only in docs_metadata.csv; the shared drive S09 has no owner and the claims archive S06 and mobile money log S02 are owned by "IT" with a business unit also claiming them; no file holds a claim outcome or a fraud flag; the transaction log carries hashed phone numbers so it cannot be matched to customers.csv; customers.csv has a status column (Active, Dormant, Closed) but no dated churn flag.',
                alt='A grid of four AI use cases against the data each needs, marked available, partly or missing, with missing outcome labels and owners standing out in clay.')


# ============================================================================ 4 data_failure_modes
@fig('data_failure_modes', 12.4)
def f_modes():
    cu = customers()
    n_cust = len(cu)
    n_nid = int((cu.national_id == '').sum())
    src = csv('sources')
    no_owner = src[src.owner.isna()].source_id.tolist()
    md = csv('docs_metadata').set_index('doc_id')
    days = {}
    for d in ('D001', 'D002', 'D003'):
        t = ks.extract_text(Path(DATA) / 'docs' / md.file[d])
        m = re.search(r'(\d+) working days of annual leave', t)
        days[d] = int(m.group(1))
    assert md.status['D001'] == 'superseded' and md.status['D003'] == 'current'
    scans = md[md.format == 'scanned_pdf']
    empty = 0
    from pypdf import PdfReader
    for fl in scans.file:
        if len((PdfReader(str(Path(DATA) / 'docs' / fl)).pages[0].extract_text() or '').strip()) < 40:
            empty += 1
    s06 = src.set_index('source_id').loc['S06']
    cols = [
        ('Missing', 'The data the use needs was never captured.', f'{n_nid}', f'of {n_cust:,} customer records have no national ID ({100 * n_nid / n_cust:.0f}%).'),
        ('Stale', 'The data exists but is out of date.', f'{days["D001"]} vs {days["D003"]}', f'days of annual leave. The {md.title["D001"].split()[-1]} handbook is still in the folder next to the {md.title["D003"].split()[-1]} one.'),
        ('Unowned', 'Nobody answers for the data or its quality.', f'{len(no_owner)} of {len(src)}', f'sources in sources.csv name no owner ({", ".join(no_owner)}).'),
        ('Unreachable', 'The data exists but the system cannot read it.', f'{empty}', f'scanned PDFs return no text to a text reader. The claims archive ({int(s06.approx_records):,} records) holds PDF and scanned images.'),
    ]
    f, ax = canvas(12.4, 4.6)
    title(ax, 'Four ways data fails an AI use, each with a Kitara example from the files')
    cw = 2.95
    for i, (name, dfn, big, ex) in enumerate(cols):
        x = 0.3 + i * cw + (0.15 if i else 0)
        if i:
            line(ax, 0.3 + i * cw - 0.05, 0.55, 0.3 + i * cw - 0.05, 3.85, HAIR, 0.8)
        T(ax, x, 3.7, name, size=22, weight='bold', family=SERIF)
        para(ax, x, 3.45, dfn, cw - 0.4, 13.5, CHAR)
        line(ax, x, 2.85, x + cw - 0.4, 2.85, HAIR, 0.8)
        T(ax, x, 2.45, big, size=30, family=SERIF, weight='bold', color=CLAY if i == 1 else INK)
        para(ax, x, 2.05, ex, cw - 0.4, 13.5, INK)
    note(ax, 'Counts computed from customers.csv, sources.csv, docs_metadata.csv and the document files.', y=0.17)
    save(f, 'data_failure_modes')
    return dict(description=f'Four columns, Missing, Stale, Unowned and Unreachable, each with a one line definition and a Kitara example computed from the files. Missing: {n_nid} of {n_cust:,} customers have no national ID. Stale: the 2019 Staff Handbook says {days["D001"]} working days of annual leave and the 2025 one says {days["D003"]} (2022: {days["D002"]}), and all three sit in the same folder. Unowned: {len(no_owner)} of {len(src)} sources have no owner ({", ".join(no_owner)}). Unreachable: {empty} scanned PDFs return no text through pypdf; the claims archive S06 holds PDF and scanned images.',
                alt='Four columns naming the ways data fails an AI use: missing, stale, unowned and unreachable, each with a Kitara example and a number.')


# ============================================================================ 5 source_status
@fig('source_status', 12.4)
def f_source_status():
    src = csv('sources')
    fields = [('Owner', 'owner'), ('Steward', 'steward'), ('Sensitivity class', 'sensitivity'), ('Personal data flag', 'personal_data'), ('Quality check', 'last_quality_check')]
    pres = pd.DataFrame({k: src[c].notna() & (src[c].astype(str).str.strip() != '') for k, c in fields})
    f, ax = canvas(12.4, 5.3)
    miss_tot = (~pres).sum()
    title(ax, f'{int((~pres).any(axis=1).sum())} of {len(src)} sources lack at least one of the five basics')
    cx0, cs = 5.3, 1.38
    for j, (k, _) in enumerate(fields):
        ls = wrap(ax, k, cs - 0.1, 13.5, 'bold')
        for q, ln in enumerate(ls):
            T(ax, cx0 + j * cs, 4.62 - q * 0.21 + (0.1 if len(ls) == 1 else 0), ln, size=13.5, weight='bold', ha='center')
    line(ax, 0.3, 4.2, 12.1, 4.2, INK, 1.0)
    step = 0.265
    for i, r in src.iterrows():
        y = 3.98 - i * step
        T(ax, 0.3, y, f'{r.source_id}', size=13, color=GREY)
        T(ax, 0.85, y, fit(ax, r['name'].replace('Shared drive: policies and procedures', 'Shared drive: policies, procedures'), 4.1, 13), size=13)
        for j, (k, _) in enumerate(fields):
            x = cx0 + j * cs
            if pres.loc[i, k]:
                dot(ax, x, y, 0.07, CHAR)
            else:
                dot(ax, x, y, 0.065, PAPER, CLAY, 1.8)
    yb = 3.98 - 13 * step - 0.3
    line(ax, 0.3, yb + 0.15, 12.1, yb + 0.15, INK, 1.0)
    T(ax, 0.3, yb - 0.05, 'Missing', size=13.5, weight='bold')
    for j, (k, _) in enumerate(fields):
        T(ax, cx0 + j * cs, yb - 0.05, str(int(miss_tot[k])), size=14, weight='bold', color=CLAY, ha='center')
    T(ax, 0.3, 4.62, 'filled dot: present', size=13, color=CHAR)
    T(ax, 0.3, 4.38, 'clay ring: missing', size=13, color=CLAY)
    save(f, 'source_status')
    return dict(description=f'A grid of the {len(src)} rows of sources.csv (S01 to S14) against five fields: owner, steward, sensitivity class, personal data flag and last quality check. A filled charcoal dot means the field is filled in; a clay ring means it is blank. The bottom row counts the gaps: ' + ', '.join(f'{k} {int(miss_tot[k])}' for k, _ in fields) + '.',
                alt='A fourteen row grid showing which data sources have an owner, steward, sensitivity class, personal data flag and quality check, with missing entries ringed in clay.')


# ============================================================================ 6 defect_profile
@fig('defect_profile', 7.0)
def f_defects():
    c = customers()
    n = len(c)
    kd = (c.full_name.str.lower().str.strip() + '|' + c.date_of_birth).where(c.date_of_birth != '')
    dup = ((c.national_id != '') & c.duplicated('national_id', keep='first')) | (kd.notna() & kd.duplicated(keep='first'))
    today = pd.Timestamp('2026-10-29')
    dob = pd.to_datetime(c.date_of_birth.replace('', np.nan), errors='coerce')
    op = pd.to_datetime(c.opened_date, errors='coerce')
    imp = ((dob > today) | (dob < pd.Timestamp('1900-01-01')) | (op > today) | (op < pd.Timestamp('1900-01-01')))
    dist_std = {'Kampala', 'Wakiso'}
    district_var = c.district.str.lower().isin(['kampala', 'kla', 'wakiso', 'wak']) & ~c.district.isin(dist_std)
    phone_bad = c.phone.map(KT.classify_phone) != '+256xxxxxxxxx'
    test = c.full_name.str.strip().str.lower().str.match(r'^(test\b|demo customer)')
    gender_bad = ~c.gender.isin(['M', 'F'])
    rows = [('Duplicate customers', int(dup.sum())), ('Missing national ID', int((c.national_id == '').sum())), ('Missing date of birth', int((c.date_of_birth == '').sum())),
            ('Impossible dates', int(imp.sum())), ('District spelled other ways', int(district_var.sum())), ('Phone not in +256 form', int(phone_bad.sum())),
            ('Test accounts', int(test.sum())), ('Gender not coded M or F', int(gender_bad.sum()))]
    rows.sort(key=lambda r: -r[1])
    assert dict(rows)['Duplicate customers'] == 150 and dict(rows)['Impossible dates'] == 40
    f, ax = canvas(7.0, 4.6)
    title(ax, f'Most common defect: {rows[0][0][0].lower() + rows[0][0][1:]}')
    T(ax, 0.3, 3.95, f'Rows affected, out of {n:,}', size=13, color=CHAR)
    xl, sc = 3.0, 3.0 / rows[0][1]
    for i, (lab, v) in enumerate(rows):
        y = 3.5 - i * 0.43
        T(ax, 0.3, y, fit(ax, lab, 2.6, 13), size=13)
        col = CLAY if i == 0 else CHAR
        rect(ax, xl, y - 0.14, max(v * sc, 0.02), 0.28, fc=col)
        T(ax, xl + v * sc + 0.1, y, f'{v:,}', size=13, weight='bold', color=col if i == 0 else INK)
    line(ax, xl, 0.45, xl, 3.75, INK, 0.8)
    note(ax, 'Counted from customers.csv. Some rows have more than one defect.', y=0.2)
    save(f, 'defect_profile')
    return dict(description='Horizontal bars of defect counts in customers.csv, sorted high to low and computed from the file: ' + '; '.join(f'{l} {v:,}' for l, v in rows) + f'. The largest bar is clay. Counts are rows affected out of {n:,}; a row can have more than one defect. Duplicates use the national ID or name plus date of birth rule.',
                alt=f'Bar chart of eight defect types in the customer table, with {rows[0][0].lower()} the largest at {rows[0][1]:,} rows.')


# ============================================================================ 7 missing_by_column
@fig('missing_by_column', 7.0)
def f_missing():
    c = customers()
    pct = ((c.apply(lambda s: s.str.strip() == '')).mean() * 100).sort_values(ascending=False)
    top = pct.index[0]
    f, ax = canvas(7.0, 4.6)
    title(ax, f'{top.replace("_", " ").capitalize()} is blank most often: {pct[top]:.0f}% of customers')
    xl, sc = 2.55, 3.7 / max(35, pct.max())
    step = 0.232
    for i, (col, v) in enumerate(pct.items()):
        y = 3.98 - i * step
        T(ax, 0.3, y, col, size=13)
        if v > 0:
            rect(ax, xl, y - 0.085, v * sc, 0.17, fc=CLAY if i == 0 else CHAR)
        T(ax, xl + v * sc + 0.09, y, f'{v:.1f}%' if v > 0 else '0', size=13, weight='bold' if v > 0 else 'normal', color=(CLAY if i == 0 else INK) if v > 0 else GREY)
    line(ax, xl, 0.5, xl, 4.1, INK, 0.8)
    note(ax, 'Share of the 5,000 rows with a blank cell, from customers.csv.', y=0.2)
    save(f, 'missing_by_column')
    return dict(description='Horizontal bars of the percent of blank cells in each of the 14 columns of customers.csv, sorted high to low and computed from the file: ' + '; '.join(f'{k} {v:.1f}%' for k, v in pct.items() if v > 0) + '; every other column 0. The largest, ' + top + ', is clay.',
                alt=f'Bar chart of percent missing by customer column: {top} highest at {pct[top]:.0f} percent, national_id 11 percent and date_of_birth 6 percent, others none.')


# ============================================================================ 8 corpus_makeup
@fig('corpus_makeup', 7.0)
def f_corpus():
    md = csv('docs_metadata')
    names = {'text_pdf': 'Text PDF', 'scanned_pdf': 'Scanned PDF', 'docx': 'Word document', 'txt': 'Text file'}
    ct = md.groupby(['format', 'status']).size().unstack(fill_value=0)
    order = ['text_pdf', 'scanned_pdf', 'docx', 'txt']
    n, sup = len(md), int((md.status == 'superseded').sum())
    sc_sup = int(ct.loc['scanned_pdf'].get('superseded', 0))
    f, ax = canvas(7.0, 4.4)
    title(ax, f'{sup} of {n} documents are superseded, and {sc_sup} of them are scans')
    xl, sc = 1.95, 2.6 / (ct.sum(axis=1).max())
    for i, k in enumerate(order):
        y = 3.3 - i * 0.78
        cur, sp = int(ct.loc[k].get('current', 0)), int(ct.loc[k].get('superseded', 0))
        T(ax, 0.3, y, names[k], size=13.5)
        rect(ax, xl, y - 0.17, cur * sc, 0.34, fc=CHAR)
        rect(ax, xl + cur * sc, y - 0.17, sp * sc, 0.34, fc=CLAY)
        flow(ax, xl + (cur + sp) * sc + 0.12, y, [(f'{cur} current', INK, 'normal')] + ([(f'{sp} superseded', CLAY, 'bold')] if sp else []), size=13.5)
    line(ax, xl, 0.65, xl, 3.65, INK, 0.8)
    note(ax, 'Counts from docs_metadata.csv. Status is held only in that file, not in the documents.', y=0.2)
    save(f, 'corpus_makeup')
    return dict(description=f'Four horizontal bars of the {n} Kitara documents by format ({", ".join(f"{names[k]} {int(ct.loc[k].sum())}" for k in order)}), each split into current (charcoal) and superseded (clay) from docs_metadata.csv. {sup} documents are superseded; {sc_sup} of the {int(ct.loc["scanned_pdf"].sum())} scanned PDFs are superseded. Counts are written after each bar.',
                alt=f'Bar chart of documents by format, with {sup} superseded documents highlighted and most scanned PDFs among them.')


# ============================================================================ 9 ocr_example
@fig('ocr_example', 12.4)
def f_ocr():
    import kitara_docs_a as DA, kitara_docs_b  # noqa: F401  (loading the module registers the document texts)
    import pytesseract
    md = csv('docs_metadata').set_index('doc_id')
    key = json.loads((Path(DATA) / 'answer_key.json').read_text())['scans']['per_scan']
    heavy = [s for s in key if s['degradation'] == 'heavy']
    pick = max(heavy, key=lambda s: s['character_error_rate'])
    d = [x for x in DA.DOCS if x['file'] == pick['file']][0]
    page = pdf_page_png(Path(DATA) / 'docs' / md.file[pick['doc_id']], 150)
    r0, r1 = 3, 10                                      # source lines of the note shown in the crop
    box = (100, 150 + 33 * r0 - 8, 960, 150 + 33 * r1 - 4)
    crop = page.crop(box)
    ocr_txt = pytesseract.image_to_string(crop)
    src_lines = d['body'].strip().split('\n')[r0:r1]
    ocr_lines = [l for l in ocr_txt.split('\n') if l.strip()]
    sw = ' '.join(src_lines).split()
    ow = ' '.join(ocr_lines).split()
    sm = difflib.SequenceMatcher(None, sw, ow, autojunk=False)
    bad = np.zeros(len(ow), bool)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            bad[j1:j2] = True
    nbad = int(bad.sum())
    f, ax = canvas(12.4, 4.6)
    title(ax, f'On a faded scan, Tesseract gets {nbad} of {len(ow)} words wrong in this crop')
    cw_in = 5.4
    ch_in = cw_in * crop.size[1] / crop.size[0]
    ax.imshow(np.asarray(crop), extent=(0.3, 0.3 + cw_in, 3.55 - ch_in, 3.55), aspect='auto', zorder=1)
    rect(ax, 0.3, 3.55 - ch_in, cw_in, ch_in, ec=HAIR, lw=0.8)
    T(ax, 0.3, 3.85, 'The scan, as the computer sees it', size=14, weight='bold')
    T(ax, 6.4, 3.85, 'What Tesseract read from the same crop', size=14, weight='bold')
    # right: OCR words, wrong ones in clay, wrapped in lines the way the crop was
    k = 0
    y = 3.5
    for ln in ocr_lines:
        words = ln.split()
        x = 6.4
        for w in words:
            T(ax, x, y, w, size=13, color=CLAY if bad[k] else INK, weight='bold' if bad[k] else 'normal')
            x += tw(ax, w + ' ', 13, 'bold' if bad[k] else 'normal') + 0.0
            k += 1
        y -= 0.3
    # the printed source for the wrong words
    wrong_src = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal' and i2 > i1:
            wrong_src.append((' '.join(sw[i1:i2]), ' '.join(ow[j1:j2])))
    yy = 3.5 - len(ocr_lines) * 0.3 - 0.2
    line(ax, 6.4, yy + 0.12, 12.1, yy + 0.12, HAIR, 0.8)
    T(ax, 6.4, yy - 0.1, 'Clay words differ from the known source text:', size=13, color=CHAR)
    shown = [(a, b) for a, b in wrong_src][:4]
    for i, (a, b) in enumerate(shown):
        flow(ax, 6.4, yy - 0.4 - i * 0.26, [(f'"{fit(ax, a, 2.3, 13)}"', INK, 'normal'), ('read as', GREY, 'normal'), (f'"{fit(ax, b, 2.3, 13)}"' if b else 'nothing', CLAY, 'bold')], size=13)
    cer = pick['character_error_rate']
    note(ax, f'Whole page: {100 * cer:.1f}% of characters wrong ({md.title[pick["doc_id"]]}, 150 dpi). Source text from the data generator.', y=0.17)
    save(f, 'ocr_example')
    return dict(description=f'Left: a real crop of the heavy scan "{Path(pick["file"]).name}" (doc {pick["doc_id"]}), rendered from the PDF at 150 dpi. Right: the text Tesseract returns for that same crop, with the {nbad} of {len(ow)} words that differ from the known source text in clay (difflib on words), then up to four pairs of source phrase and what was read. The whole page has a character error rate of {100 * cer:.1f}% in answer_key.json.',
                alt=f'A faded scanned note on the left and the text a reader program extracted on the right, with {nbad} wrongly read words in clay.')


# ============================================================================ 10 table_scramble
@fig('table_scramble', 12.4)
def f_table():
    import pdfplumber
    from pypdf import PdfReader
    pdf = Path(DATA) / 'docs' / 'product guides' / 'Tariff Schedule 2025.pdf'
    txt = PdfReader(str(pdf)).pages[0].extract_text()
    lines = [l for l in txt.split('\n') if l.strip()]
    with pdfplumber.open(str(pdf)) as pl:
        pg = pl.pages[0]
        tb = pg.find_tables()[0]
        rows = tb.extract()
        bbox = tb.bbox
        ph = float(pg.height)
    dpi = 110
    img = pdf_page_png(pdf, dpi)
    sc = dpi / 72
    crop = img.crop((int(bbox[0] * sc - 60), int(bbox[1] * sc - 130), int(bbox[2] * sc + 60), int(bbox[3] * sc + 40)))
    hdr_i = lines.index(rows[0][0])
    chg_i = lines.index(rows[0][1])
    i_serv = lines.index(rows[3][0])
    i_chg = [i for i, l in enumerate(lines) if l == rows[3][1] and i > chg_i][0]
    gap = i_chg - i_serv
    f, ax = canvas(12.4, 4.6)
    title(ax, 'The same table, read two ways: pypdf scrambles it, pdfplumber keeps the rows')
    pw = 3.3
    ph_in = pw * crop.size[1] / crop.size[0]
    T(ax, 0.3, 3.88, 'The page', size=14, weight='bold')
    ax.imshow(np.asarray(crop), extent=(0.3, 0.3 + pw, 3.6 - ph_in, 3.6), aspect='auto', zorder=1)
    rect(ax, 0.3, 3.6 - ph_in, pw, ph_in, ec=HAIR, lw=0.8)
    x1 = 4.2
    T(ax, x1, 3.88, 'pypdf: text in file order', size=14, weight='bold')
    ntx = lines.index('Notes')
    sel = list(range(hdr_i, hdr_i + 3)) + [None] + list(range(chg_i, chg_i + 4)) + [None] + [ntx, ntx + 1]
    y = 3.52
    for idx in sel:
        if idx is None:
            T(ax, x1, y, '...', size=13, color=GREY)
        else:
            hi = idx in (i_serv, i_chg)
            T(ax, x1, y, lines[idx], size=13, color=CLAY if hi else INK, weight='bold' if hi else 'normal')
        y -= 0.235
    x2 = 8.35
    T(ax, x2, 3.88, 'pdfplumber: rows kept together', size=14, weight='bold')
    rr = rows[:7]
    y = 3.52
    line(ax, x2, y + 0.14, x2 + 3.7, y + 0.14, INK, 0.9)
    for i, r in enumerate(rr):
        T(ax, x2, y, fit(ax, r[0], 2.7, 13), size=13, weight='bold' if i == 0 else 'normal', color=CLAY if i == 3 else INK)
        T(ax, x2 + 3.7, y, r[1], size=13, weight='bold' if i == 0 else 'normal', ha='right', color=CLAY if i == 3 else INK)
        y -= 0.3
        line(ax, x2, y + 0.15, x2 + 3.7, y + 0.15, HAIR, 0.6)
    T(ax, x2, y - 0.1, f'{len(rows) - 1} data rows recovered. Notes column left out here.', size=13, color=CHAR)
    para(ax, 0.3, 1.75, f'In the pypdf text, "{rows[3][0]}" and its charge "{rows[3][1]}" are {gap} lines apart. Every service comes first, then every charge.', 3.3, 13.5, CLAY, weight='bold')
    note(ax, 'Tariff Schedule 2025.pdf, page 1. Real extraction output.', y=0.17)
    save(f, 'table_scramble')
    return dict(description=f'One real table page, "Tariff Schedule 2025.pdf". Left: the page image from pdftoppm cropped to the table. Middle: the pypdf text in file order (first services, then the Charge header and values, then Notes), showing that the services are listed first and the charges after, {gap} lines apart for "{rows[3][0]}" and its charge "{rows[3][1]}" (clay). Right: the same table as rows from pdfplumber, {len(rows) - 1} data rows with service and charge kept together.',
                alt='A table page shown with its scrambled pypdf text in the middle and the clean rows recovered by pdfplumber on the right.')


# ============================================================================ 11 chunking_overlap
@fig('chunking_overlap', 12.4)
def f_chunk():
    md = csv('docs_metadata')
    size, ov = 200, 40
    best = None
    for r in md[(md.status == 'current') & (md.language == 'en') & (md.format.isin(['text_pdf', 'docx']))].itertuples():
        t = ks.extract_text(Path(DATA) / 'docs' / r.file)
        n = len(t.split())
        if best is None or abs(n - 700) < abs(best[1] - 700):
            best = (r, n, t)
    r, n, t = best
    chunks = ks.chunk_text(t, size, ov)
    step = size - ov
    starts = [i * step for i in range(len(chunks))]
    lens = [len(c.split()) for c in chunks]
    if len(chunks) > 1 and starts[-1] + lens[-1] != n:       # the folded tail starts one step earlier
        starts[-1] = max(starts[-1] - 0, starts[-1])
    ends = [min(starts[i] + lens[i], n) for i in range(len(chunks))]
    f, ax = canvas(12.4, 4.6)
    title(ax, f'{shortname(r.title)}: {n} words become {len(chunks)} chunks')
    x0, x1 = 1.6, 12.0
    sc = (x1 - x0) / n
    top = 3.65
    for v in range(0, n + 1, 100):
        line(ax, x0 + v * sc, 1.5, x0 + v * sc, top + 0.15, HAIR, 0.6)
        T(ax, x0 + v * sc, 1.28, str(v), size=13, color=GREY, ha='center')
    T(ax, x0 + n * sc / 2, 0.98, 'word position in the document', size=13, color=CHAR, ha='center')
    for i in range(len(chunks)):
        y = top - i * 0.5
        T(ax, 0.3, y, f'Chunk {i + 1}', size=13.5, weight='bold')
        rect(ax, x0 + starts[i] * sc, y - 0.14, (ends[i] - starts[i]) * sc, 0.28, fc=CHAR)
        if i > 0:
            o0, o1 = starts[i], min(ends[i - 1], ends[i])
            if o1 > o0:
                rect(ax, x0 + o0 * sc, y - 0.14, (o1 - o0) * sc, 0.28, fc=CLAY)
                rect(ax, x0 + o0 * sc, y + 0.36, (o1 - o0) * sc, 0.28, fc=CLAY)
        if i < len(chunks) - 1:
            pass
    nov = starts[1] and (ends[0] - starts[1])
    first = ' '.join(chunks[0].split()[:16])
    para(ax, 0.3, 0.8, f'Chunk 1 opens with: "{first} ..."', 11.6, 13.5, INK, style='italic')
    T(ax, x1, top + 0.45, f'clay: {nov} words that sit in two chunks', size=13.5, color=CLAY, weight='bold', ha='right')
    note(ax, f'Real document. chunk_text from kitara_search.py: {size} words, {ov} words of overlap.', y=0.17)
    save(f, 'chunking_overlap')
    return dict(description=f'One real document, "{r.title}" ({n} words), split by chunk_text with {size} word chunks and {ov} words of overlap into {len(chunks)} chunks. Each chunk is a charcoal bar placed at its word span on a shared 0 to {n} word axis; the {nov} words shared with the previous chunk are clay. The first chunk\'s opening words are printed underneath.',
                alt=f'Bars showing one document of {n} words cut into {len(chunks)} overlapping chunks, with the repeated stretch of {nov} words in clay.')


# ============================================================================ 12 embedding_map
@fig('embedding_map', 12.4)
def f_embed():
    s = searcher()
    ms = s.meaning
    ev = evalq().set_index('q_id')
    qids = ['Q01', 'Q02', 'Q15', 'Q19']
    qs = [ev.question[q] for q in qids]

    def qv(query):
        w, c = {}, {}
        for t in ks.tokenise(query):
            w[t] = w.get(t, 0) + 1
            for g in ks._char_ngrams(t):
                c[g] = c.get(g, 0) + 1
        qw = np.zeros((1, len(ms.wv)), np.float32)
        qc = np.zeros((1, len(ms.cv)), np.float32)
        for t, v in w.items():
            if t in ms.wv:
                qw[0, ms.wv[t]] = v
        for t, v in c.items():
            if t in ms.cv:
                qc[0, ms.cv[t]] = v
        q = np.hstack([ms.w_word * ms._tfidf(qw, ms.idf_w), ms.w_char * ms._tfidf(qc, ms.idf_c)])
        e = (q @ ms.Vt.T)[0]
        return e / (np.linalg.norm(e) + 1e-9)
    QE = np.array([qv(q) for q in qs])
    chosen, links = [], {}
    for qi in range(4):
        sims = ms.E @ QE[qi]
        top = [int(i) for i in np.argsort(-sims)[:6]]
        mine = []
        for i in top:
            if i not in chosen and len(mine) < 3:
                chosen.append(i)
                mine.append(i)
        links[qi] = mine
    assert len(chosen) == 12
    Z = np.vstack([ms.E[chosen], QE])
    Zc = Z - Z.mean(0)
    U, S, Vt = np.linalg.svd(Zc, full_matrices=False)
    P = Zc @ Vt[:2].T
    var = (S[:2] ** 2).sum() / (S ** 2).sum()
    bx0, bx1, by0, by1 = 0.5, 7.6, 0.75, 3.95
    mn, mx = P.min(0), P.max(0)
    Q = np.c_[bx0 + 0.5 + (P[:, 0] - mn[0]) / (mx[0] - mn[0]) * (bx1 - bx0 - 1.2), by0 + 0.3 + (P[:, 1] - mn[1]) / (mx[1] - mn[1]) * (by1 - by0 - 0.7)]
    f, ax = canvas(12.4, 4.6)
    title(ax, 'A search question lands near the passages that answer it')
    for qi in range(4):
        for ci in links[qi]:
            k = chosen.index(ci)
            line(ax, Q[12 + qi, 0], Q[12 + qi, 1], Q[k, 0], Q[k, 1], GREY, 0.8, zorder=1)
    for k, ci in enumerate(chosen):
        dot(ax, Q[k, 0], Q[k, 1], 0.07, CHAR)
        if ci in [links[q][0] for q in links if links[q]]:
          T(ax, Q[k, 0] + 0.1, Q[k, 1] - 0.13, s.chunks.chunk_id[ci], size=13, color=CHAR, path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)
    for qi in range(4):
        x, y = Q[12 + qi]
        ax.add_patch(Polygon([(x, y + 0.15), (x + 0.12, y), (x, y - 0.15), (x - 0.12, y)], fc=CLAY, ec='none', zorder=4))
        T(ax, x, y + 0.27, f'Q{qi + 1}', size=14, color=CLAY, weight='bold', ha='center', path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)
    xr = 8.0
    T(ax, xr, 3.95, 'Questions asked, and the nearest passage (labelled)', size=14, weight='bold')
    y = 3.6
    for qi in range(4):
        top1 = chosen[chosen.index(links[qi][0])]
        lines_ = wrap(ax, qs[qi], 3.8, 13)
        T(ax, xr, y - 0.1, f'Q{qi + 1}', size=13.5, color=CLAY, weight='bold')
        for j, ln in enumerate(lines_):
            T(ax, xr + 0.42, y - 0.1 - j * 0.21, ln, size=13)
        yy = y - 0.1 - len(lines_) * 0.21
        T(ax, xr + 0.42, yy, f'nearest: {s.chunks.doc_id[top1]}, {fit(ax, shortname(s.chunks.title[top1]), 2.7, 13)}', size=13, color=CHAR)
        y = yy - 0.35
    note(ax, f'Stand-in vectors; real embeddings differ. 64 numbers per chunk flattened to 2 (first two SVD components, {100 * var:.0f}% of the spread); distances are approximate.', y=0.17)
    save(f, 'embedding_map')
    return dict(description=f'A two-dimensional map (first two SVD components of the 64-number stand-in vectors from kitara_search.MeaningScorer, {100 * var:.0f}% of the spread) of 12 real chunks (charcoal dots, labelled with document id) and 4 real eval questions ({", ".join(qids)}; clay diamonds Q1 to Q4). Hairlines join each question to its three nearest chunks. A list on the right gives each question and the document of its nearest chunk. Labelled as stand-in vectors; real embeddings differ.',
                alt='A scatter map where four question markers sit near the document passages that answer them, joined by thin lines.')


# ============================================================================ 13 rrf_fusion
def pick_rrf_question():
    ev = evalq()
    s = searcher()
    ids = s.chunks.doc_id.tolist()
    for r in ev.itertuples():
        if not r.note.startswith('plain'):
            continue
        rb, rm, rf = lists(r.question)
        b, m, h = (first_rank(x, ids, r.gold_doc_id) for x in (rb, rm, rf))
        if (b == 0 or b > 5) and 0 < m <= 5 and 0 < h <= 5:
            return r, (rb, rm, rf), (b, m, h)
    raise RuntimeError('no question found where fusion rescues the keyword miss')


@fig('rrf_fusion', 12.4)
def f_rrf():
    s = searcher()
    r, (rb, rm, rf), (b, m, h) = pick_rrf_question()
    key = {p['q_id']: p for p in json.loads((Path(DATA) / 'answer_key.json').read_text())['search_evaluation']['per_question']}
    assert (b, m, h) == (key[r.q_id]['bm25_rank'], key[r.q_id]['meaning_rank'], key[r.q_id]['hybrid_rank']), 'ranks differ from answer_key.json'
    ids = s.chunks.doc_id.tolist()
    rankb = {p: i for i, p in enumerate(rb, 1)}
    rankm = {p: i for i, p in enumerate(rm, 1)}

    def label(p):
        c = s.chunks.iloc[p]
        multi = (s.chunks.doc_id == c.doc_id).sum() > 1
        return f'{shortname(c.title)}' + (f', part {c.chunk_no}' if multi else '')
    f, ax = canvas(12.4, 4.8)
    title(ax, f'Fusion pulls the right passage into the top 5, though keyword search missed it')
    para(ax, 0.3, 4.12, f'Question {r.q_id}: "{r.question}"', 12, 13.5, CHAR)
    cw = 4.05
    heads = ['Keyword search (BM25)', 'Stand-in meaning search', 'Fused: sum of 1/(60 + rank)']
    cols = [rb[:5], rm[:5], rf[:5]]
    for j in range(3):
        x = 0.3 + j * cw
        T(ax, x, 3.85, heads[j], size=14, weight='bold')
        line(ax, x, 3.68, x + cw - 0.25, 3.68, INK, 0.9)
        for i, p in enumerate(cols[j]):
            y = 3.35 - i * 0.62
            gold = ids[p] == r.gold_doc_id
            col = CLAY if gold else INK
            T(ax, x, y, str(i + 1), size=16, family=SERIF, weight='bold', color=col)
            T(ax, x + 0.3, y + 0.1, fit(ax, label(p), cw - 0.65, 13.5, 'bold' if gold else 'normal'), size=13.5, weight='bold' if gold else 'normal', color=col)
            if j == 0:
                sub = f'1/{60 + i + 1} = {1 / (61 + i):.4f}'
            elif j == 1:
                sub = f'1/{60 + i + 1} = {1 / (61 + i):.4f}'
            else:
                parts, tot = [], 0
                for rk in (rankb.get(p), rankm.get(p)):
                    if rk:
                        parts.append(f'1/{60 + rk}')
                        tot += 1 / (60 + rk)
                sub = ' + '.join(parts) + f' = {tot:.4f}'
            T(ax, x + 0.3, y - 0.14, sub, size=13, color=CLAY if gold else GREY)
    note(ax, f'Real search over {len(s.chunks)} chunks. Clay: the passage from the gold document ({r.gold_doc_id}). Gold rank: BM25 {b or "none"}, meaning {m}, fused {h}.', y=0.17)
    save(f, 'rrf_fusion')
    return dict(description=f'For eval question {r.q_id} ("{r.question}"), three ranked lists of the top 5 chunks from the real search: keyword search (BM25), the stand-in meaning search, and the fused list where each chunk scores the sum of 1/(60 + rank) over the lists it appears in. The chunk from the gold document {r.gold_doc_id} ({doc_title(r.gold_doc_id)}) is clay in each list. Gold ranks: BM25 {b if b else "outside top 10"}, meaning {m}, fused {h}; these match answer_key.json.',
                alt=f'Three ranked lists for one question showing the correct document missing from the keyword top five, first in meaning search, and third after fusion.')


# ============================================================================ 14 recall_by_method
@fig('recall_by_method', 7.0)
def f_recall():
    s = searcher()
    ev = evalq()
    ks_ = [1, 3, 5, 10]
    meth = [('bm25', 'BM25', CHAR), ('meaning', 'Stand-in', GREY), ('hybrid', 'Hybrid', CLAY)]
    hits = {m: {k: 0 for k in ks_} for m, _, _ in meth}
    ids = s.chunks.doc_id.tolist()
    for r in ev.itertuples():
        rb, rm, rf = lists(r.question)
        for m, order in (('bm25', rb), ('meaning', rm), ('hybrid', rf)):
            docs = [ids[p] for p in order[:10]]
            for k in ks_:
                hits[m][k] += ks.recall_at_k(docs, r.gold_doc_id, k)
    n = len(ev)
    rec = {m: {k: hits[m][k] / n for k in ks_} for m in hits}
    key = json.loads((Path(DATA) / 'answer_key.json').read_text())['search_evaluation']
    for m in rec:
        assert abs(rec[m][5] - key['recall_at_5'][m]) < 0.001 and abs(rec[m][3] - key['recall_at_3'][m]) < 0.001, f'recall differs from key for {m}'
    f, ax = canvas(7.0, 4.4)
    title(ax, f'Hybrid search finds the right document most often: {100 * rec["hybrid"][5]:.0f}% at 5')
    x0, gw, bw = 0.95, 1.5, 0.36
    ytop, yh = 0.7, 2.75
    for v in (0, 25, 50, 75, 100):
        y = ytop + yh * v / 100
        line(ax, 0.85, y, 6.9, y, HAIR, 0.6)
        T(ax, 0.78, y, f'{v}', size=13, color=GREY, ha='right')
    for gi, k in enumerate(ks_):
        gx = x0 + gi * gw + 0.1
        for mi, (m, nm, col) in enumerate(meth):
            v = rec[m][k]
            x = gx + mi * (bw + 0.04)
            rect(ax, x, ytop, bw, yh * v, fc=col)
            T(ax, x + bw / 2, ytop + yh * v + 0.13, f'{100 * v:.0f}', size=13, weight='bold', ha='center', color=CLAY if m == 'hybrid' else INK)
            if gi == 0:
                T(ax, x + bw / 2, ytop + 0.1, nm, size=13, color='white', weight='bold', rotation=90, ha='center', va='bottom')
        T(ax, gx + 1.5 * bw + 0.05, ytop - 0.25, f'top {k}', size=13.5, ha='center')
    T(ax, 0.3, 3.72, 'Percent of 60 questions with the right document in the top results', size=13, color=CHAR)
    save(f, 'recall_by_method')
    return dict(description=f'Grouped bars of recall at 1, 3, 5 and 10 on the {n} questions in eval_questions.csv, computed by running the three searches in kitara_search.py (hit when any of the top k chunks comes from the gold document): ' + '; '.join(f'{nm} ' + ', '.join(f'@{k} {100 * rec[m][k]:.0f}%' for k in ks_) for m, nm, _ in meth) + '. Hybrid is clay. Methods are labelled inside the first group of bars. At 5 the values match answer_key.json (0.633, 0.617, 0.767).',
                alt=f'Grouped bar chart of search recall at top 1, 3, 5 and 10 for keyword, stand-in meaning and hybrid search, with hybrid highest at {100 * rec["hybrid"][5]:.0f} percent at 5.')


# ============================================================================ 15 stale_version
@fig('stale_version', 12.4)
def f_stale():
    s = searcher()
    md = csv('docs_metadata').set_index('doc_id')
    ev = evalq().set_index('q_id')
    q = ev.question['Q41']
    ids = s.chunks.doc_id.tolist()
    rb, rm, rf = lists(q)
    top = ids[rb[0]]
    first_cur = next(i for i, p in enumerate(rb, 1) if s.chunks.status[p] == 'current')
    docs = ['D001', 'D002', 'D003']
    info = {}
    for d in docs:
        t = ' '.join(ks.extract_text(Path(DATA) / 'docs' / md.file[d]).split())
        m = re.search(r'([^.]*\b(\d+) working days of annual leave[^.]*\.)', t)
        info[d] = (int(m.group(2)), re.sub(r'^Annual leave\s+', '', m.group(1).strip()))
    assert md.status[top] == 'superseded' and first_cur == 4
    f, ax = canvas(12.4, 4.6)
    title(ax, f'Keyword search answers with the {md.version[top]} handbook first, which is out of date')
    para(ax, 0.3, 4.02, f'The question: "{q}"', 12, 14, CHAR)
    cw = 4.0
    for j, d in enumerate(docs):
        x = 0.3 + j * cw + (0.2 if j else 0)
        if j:
            line(ax, 0.3 + j * cw - 0.05, 0.75, 0.3 + j * cw - 0.05, 3.55, HAIR, 0.8)
        hit = d == top
        T(ax, x, 3.35, f'Staff Handbook {md.version[d]}', size=15, weight='bold', family=SERIF)
        T(ax, x, 3.08, md.status[d], size=13.5, color=MOSS if md.status[d] == 'current' else GREY, weight='bold')
        T(ax, x, 2.45, str(info[d][0]), size=38, family=SERIF, weight='bold', color=CLAY if hit else INK)
        T(ax, x + 0.85, 2.38, 'working days of\nannual leave', size=13.5, color=CHAR, linespacing=1.1)
        para(ax, x, 1.9, f'"{info[d][1]}"', cw - 0.5, 13, CHAR, style='italic')
        if hit:
            T(ax, x, 0.95, f'Keyword search returned this one first', size=13.5, color=CLAY, weight='bold')
            T(ax, x, 0.72, f'The current handbook came {first_cur}th', size=13.5, color=CLAY)
    note(ax, 'Real text from the three handbooks, real BM25 result. Status is held only in docs_metadata.csv.', y=0.17)
    save(f, 'stale_version')
    return dict(description=f'The annual leave answer in the three real Staff Handbooks side by side (2019: {info["D001"][0]} days, 2022: {info["D002"][0]} days, 2025: {info["D003"][0]} days, with the sentence from each, extracted from the files), and the real keyword (BM25) result for eval question Q41: the first chunk returned comes from the {md.version[top]} handbook, marked superseded in docs_metadata.csv, shown in clay, and the first current chunk appears at rank {first_cur}.',
                alt=f'Three handbook versions giving {info["D001"][0]}, {info["D002"][0]} and {info["D003"][0]} days of annual leave, with the oldest one returned first by keyword search.')


# ============================================================================ 16 permission_filter
@fig('permission_filter', 12.4)
def f_perm():
    s = searcher()
    ev = evalq()
    md = csv('docs_metadata').set_index('doc_id')
    us = csv('users')
    ids = s.chunks.doc_id.tolist()
    r = ev[ev.permitted == 'N'].iloc[0]
    cand = us[us.groups.map(lambda g: not ks.user_can_see(md.access_groups[r.gold_doc_id], g))]
    cand = cand.assign(n=cand.groups.str.count(';')).sort_values('n', kind='stable')
    u = cand.iloc[0]
    rb, rm, rf = lists(r.question)
    allowed = s.chunks.access_groups.map(lambda g: ks.user_can_see(g, u.groups)).to_numpy()
    rb2, rm2, rf2 = lists(r.question, allowed)
    before = [p for p in rf[:5]]
    after = [p for p in rf2[:5]]
    assert any(ids[p] == r.gold_doc_id for p in before) and not any(ids[p] == r.gold_doc_id for p in after)
    f, ax = canvas(12.4, 4.6)
    title(ax, f'The filter keeps a restricted document out of {u["name"].split()[0]}\'s results')
    para(ax, 0.3, 4.02, f'{u["name"]}, {u.role.replace(" (general staff)", "")}, asks: "{r.question}"', 12, 14, CHAR)
    cw = 6.0
    for j, (head, order) in enumerate([('Without a permission filter', before), ('With the filter applied before ranking', after)]):
        x = 0.3 + j * (cw + 0.1)
        T(ax, x, 3.65, head, size=14.5, weight='bold')
        line(ax, x, 3.48, x + cw - 0.3, 3.48, INK, 0.9)
        for i, p in enumerate(order):
            y = 3.14 - i * 0.5
            did = ids[p]
            can = ks.user_can_see(md.access_groups[did], u.groups)
            T(ax, x, y, str(i + 1), size=16, family=SERIF, weight='bold', color=INK if can else CLAY)
            cc = s.chunks.iloc[p]
            lab = fit(ax, shortname(cc.title) + (f', part {cc.chunk_no}' if (s.chunks.doc_id == cc.doc_id).sum() > 1 else ''), cw - 2.2, 13.5)
            T(ax, x + 0.3, y, lab, size=13.5, color=INK if can else CLAY)
            T(ax, x + cw - 0.3, y, md.sensitivity[did], size=13, color=GREY if can else CLAY, ha='right')
            if not can:
                wd = tw(ax, lab, 13.5)
                line(ax, x + 0.27, y, x + 0.33 + wd, y, CLAY, 1.8, zorder=5)
    T(ax, 0.3, 0.62, f'Gold document {r.gold_doc_id} ({md.title[r.gold_doc_id]}) is {md.sensitivity[r.gold_doc_id]}, open to: {md.access_groups[r.gold_doc_id].replace(";", ", ")}.', size=13, color=CLAY, weight='bold')
    note(ax, f'Real search. {u["name"]} belongs to: {u.groups.replace(";", ", ")}. Rule: a user sees a document when it is open to all_staff or shares a group.', y=0.17)
    save(f, 'permission_filter')
    return dict(description=f'One real eval question ({r.q_id}: "{r.question}") run through hybrid search twice for the user {u["name"]} ({u.role}, groups {u.groups}), who may not see the gold document {r.gold_doc_id} ({md.title[r.gold_doc_id]}, {md.sensitivity[r.gold_doc_id]}, open to {md.access_groups[r.gold_doc_id]}). Left: top 5 results with no filter, with every result the user may not see crossed out in clay. Right: top 5 with the permission filter applied before ranking, where none of them appear.',
                alt='Two result lists for one question: without a filter a restricted salary document is in the top five crossed out, and with the filter it is gone.')


# ============================================================================ 17 pipeline_zones
@fig('pipeline_zones', 12.4)
def f_pipe():
    f, ax = canvas(12.4, 4.6)
    title(ax, 'A reference path from source to search, with a check on every step')
    by, bh = 2.15, 1.0
    bw, gap, x0 = 1.62, 0.93, 0.3
    names = ['Sources', 'Raw zone', 'Cleaned zone', 'Serving zone', 'Search index and dashboards']
    subs = ['as they are', 'copy, untouched', 'fixed and checked', 'ready to use', 'what people reach']
    checks = ['Schema check', 'Quality check', 'Personal data check', 'Schema and quality check']
    # access control band on top
    rect(ax, x0, 3.55, 12.4 - 0.6, 0.38, ec=INK, lw=1.0)
    T(ax, 6.2, 3.74, 'Access control: who may see each zone, each document and each chunk', size=13.5, ha='center', weight='bold')
    for i, nm in enumerate(names):
        x = x0 + i * (bw + gap)
        rect(ax, x, by, bw, bh, ec=INK, lw=1.4)
        ls = wrap(ax, nm, bw - 0.2, 14, 'bold')
        T(ax, x + bw / 2, by + (bh - 0.2 if len(ls) == 1 else bh / 2), '\n'.join(ls), size=14, weight='bold', ha='center', va='top' if len(ls) == 1 else 'center', linespacing=1.05)
        if len(ls) == 1:
            T(ax, x + bw / 2, by + 0.22, subs[i], size=13, color=CHAR, ha='center')
        if i < 4:
            xa, xb = x + bw, x + bw + gap
            ax.add_patch(FancyArrowPatch((xa + 0.04, by + bh / 2), (xb - 0.04, by + bh / 2), arrowstyle='-|>', mutation_scale=15, lw=1.6, color=INK, shrinkA=0, shrinkB=0, zorder=2))
            ls2 = wrap(ax, checks[i], gap - 0.12, 13, 'bold')
            for q, ln in enumerate(ls2):
                T(ax, (xa + xb) / 2, by + bh / 2 + 0.2 + (len(ls2) - 1 - q) * 0.21, ln, size=13, color=CLAY, weight='bold', ha='center')
    for j, (nm, txt) in enumerate([('Orchestration', 'schedules every step, retries it, alerts a named owner'), ('Lineage', 'records where each table and chunk came from'), ('Monitoring', 'watches freshness, volume and schema change')]):
        y = 1.4 - j * 0.4
        rect(ax, x0, y - 0.17, 12.4 - 0.6, 0.34, ec=HAIR, lw=1.0)
        T(ax, x0 + 0.12, y, nm, size=13.5, weight='bold')
        T(ax, x0 + 1.9, y, txt, size=13.5, color=CHAR)
    note(ax, 'Illustrative reference architecture, not a Kitara system.', y=0.17, x=12.1)
    save(f, 'pipeline_zones')
    return dict(description='A diagram (illustrative, labelled as such) of a reference architecture: boxes for Sources, Raw zone, Cleaned zone, Serving zone and Search index and dashboards joined by four arrows, with a clay check on each arrow (schema check, quality check, personal data check, schema and quality check). An access control band runs across the top. Three bands underneath: orchestration, lineage and monitoring. Not drawn from data.',
                alt='A pipeline diagram from sources through raw, cleaned and serving zones to a search index, with a check on every arrow and bands for access control, orchestration, lineage and monitoring.')


# ============================================================================ 18 lineage_graph
@fig('lineage_graph', 12.4)
def f_lineage():
    ed = csv('lineage_edges')
    nodes = list(dict.fromkeys(list(ed.from_asset) + list(ed.to_asset)))
    preds = {n: [] for n in nodes}
    succ = {n: [] for n in nodes}
    for a, b in zip(ed.from_asset, ed.to_asset):
        preds[b].append(a)
        succ[a].append(b)
    layer = {}

    def depth(n):
        if n not in layer:
            layer[n] = 0 if not preds[n] else 1 + max(depth(p) for p in preds[n])
        return layer[n]
    for n in nodes:
        depth(n)
    L = max(layer.values()) + 1
    cols = [[n for n in nodes if layer[n] == l] for l in range(L)]
    pos = {n: i for c in cols for i, n in enumerate(c)}
    for _ in range(6):
        for l in list(range(1, L)) + list(range(L - 2, -1, -1)):
            nb = (lambda n: preds[n]) if l else (lambda n: succ[n])
            if l == L - 1 or l > 0:
                nb = lambda n: preds[n] or succ[n]
            bc = {n: (np.mean([pos[m] for m in nb(n)]) if nb(n) else pos[n]) for n in cols[l]}
            cols[l] = sorted(cols[l], key=lambda n: (bc[n], pos[n]))
            for i, n in enumerate(cols[l]):
                pos[n] = i
    ai = {'claims_doc_archive.files', 'ocr.claims_text', 'search.claims_index'}
    f, ax = canvas(12.4, 4.6)
    title(ax, f'{len(ed)} lineage edges between {len(nodes)} assets, and only two lead to a search index')
    widths = [2.5, 1.55, 1.55, 1.55, 2.2, 2.3][:L]
    assert L == 6
    xs = [0.35 + sum(widths[:i]) for i in range(L)]
    top, sp = 3.55, 0.5
    XY = {}
    for l, c in enumerate(cols):
        off = (7 - len(c)) * sp / 2
        pre = pd.Series([n.split('.')[0] for n in c]).value_counts().index.tolist()
        T(ax, xs[l], 4.0, 'source systems' if l == 0 else ', '.join(pre), size=13, color=GREY, style='italic')
        for i, n in enumerate(c):
            XY[n] = (xs[l], top - off - i * sp)
    for a, b, st in zip(ed.from_asset, ed.to_asset, ed.step):
        (x1, y1), (x2, y2) = XY[a], XY[b]
        manual = bool(re.search(r'by hand|pasted', st))
        isai = a in ai and b in ai
        xm = (x1 + x2) / 2
        pth = MPath([(x1 + 0.07, y1), (xm, y1), (xm, y2), (x2 - 0.07, y2)], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
        ax.add_patch(PathPatch(pth, fc='none', ec=CLAY if isai else (CHAR if manual else GREY), lw=1.9 if isai else (1.4 if manual else 0.9), ls=(0, (4, 2)) if manual else '-', zorder=1))
    for n, (x, y) in XY.items():
        isai = n in ai
        dot(ax, x, y, 0.065, CLAY if isai else CHAR, z=4)
        nm = n.split('.', 1)[1] if layer[n] > 0 else n
        cap = widths[layer[n]] + (0.0 if layer[n] == L - 1 else -0.12)
        if tw(ax, nm, 13) <= cap:
            ls = [nm]
        else:
            ls = wrap(ax, nm.replace('_', '_ ').strip(), cap, 13)
            ls = [l_.replace('_ ', '_') for l_ in ls]
        for q, ln in enumerate(ls):
            T(ax, x - 0.04, y + 0.15 + (len(ls) - 1 - q) * 0.2, ln, size=13, color=CLAY if isai else INK, weight='bold' if isai else 'normal',
              path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)
    T(ax, 12.1, 0.62, 'dashed: a person copies it by hand', size=13, color=CHAR, ha='right')
    T(ax, 12.1, 0.38, 'clay: the document chain behind the search index', size=13, color=CLAY, ha='right')
    note(ax, 'Edges from lineage_edges.csv.', y=0.17, x=0.3, ha='left')
    save(f, 'lineage_graph')
    nman = int(ed.step.str.contains('by hand|pasted').sum())
    return dict(description=f'The {len(nodes)} assets and {len(ed)} edges of lineage_edges.csv laid out left to right in {L} columns by their longest path from a source system (source systems, staging, cleaned, marts, reports, returns and board pack). Nodes are dots with their asset names; edges are curved hairlines. The {nman} edges whose step says it is done by hand or pasted are dashed. The document chain claims_doc_archive.files to ocr.claims_text to search.claims_index is clay.',
                alt='A left to right graph of the Kitara data assets from source systems to reports and the board pack, with the document search chain in clay and manual copy steps dashed.')


# ============================================================================ 19 freshness_gap
@fig('freshness_gap', 12.4)
def f_fresh():
    m = csv('mobile_money_log', dtype=str)
    iso = m.timestamp.str.contains('-')
    ts = pd.Series(pd.NaT, index=m.index, dtype='datetime64[ns]')
    ts[iso] = pd.to_datetime(m.timestamp[iso], format='%Y-%m-%d %H:%M:%S')
    ts[~iso] = pd.to_datetime(m.timestamp[~iso], format='%d/%m/%Y %H:%M')
    m = m.assign(ts=ts).drop_duplicates('txn_id').sort_values('ts')
    gaps = m.ts.diff().dt.total_seconds() / 3600
    gi = gaps.idxmax()
    g_end = m.ts[gi]
    g_start = m.ts[m.index[m.index.get_loc(gi) - 1]]
    day = g_start.normalize()
    dd = m[(m.ts >= day) & (m.ts < day + pd.Timedelta(days=1))]
    cnt = dd.groupby(dd.ts.dt.hour).size().reindex(range(24), fill_value=0)
    f, ax = canvas(12.4, 4.6)
    title(ax, f'Mobile money log, {day.strftime("%d %B %Y").lstrip("0")}: no transactions for {gaps.max():.1f} hours')
    x0, x1, y0, y1 = 1.0, 12.0, 0.85, 3.7
    ymax = int(np.ceil(cnt.max() / 10) * 10)
    sc = (x1 - x0) / 24
    for v in range(0, ymax + 1, 10 if ymax <= 60 else 20):
        y = y0 + (y1 - y0) * v / ymax
        line(ax, x0, y, x1, y, HAIR, 0.6)
        T(ax, x0 - 0.1, y, str(v), size=13, color=GREY, ha='right')
    for h in range(24):
        v = cnt[h]
        if v:
            rect(ax, x0 + h * sc + 0.05, y0, sc - 0.1, (y1 - y0) * v / ymax, fc=CHAR)
        if h % 2 == 0:
            T(ax, x0 + h * sc + sc / 2, y0 - 0.22, f'{h:02d}', size=13, color=GREY, ha='center')
    hs = (g_start.hour + g_start.minute / 60 + g_start.second / 3600)
    he = (g_end.hour + g_end.minute / 60 + g_end.second / 3600)
    ax.add_patch(Rectangle((x0 + hs * sc, y0), (he - hs) * sc, y1 - y0 + 0.05, fc='none', ec=GREY, hatch='////', lw=0.6, zorder=2))
    T(ax, x0 + (hs + he) / 2 * sc, y1 + 0.28, f'No records from {g_start.strftime("%H:%M")} to {g_end.strftime("%H:%M")}', size=14.5, color=CLAY, weight='bold', ha='center',
      path_effects=[pe.withStroke(linewidth=4, foreground=PAPER)], zorder=6)
    T(ax, (x0 + x1) / 2, 0.3, 'hour of the day', size=13, color=CHAR, ha='center')
    T(ax, 0.3, 3.95, 'Transactions per hour', size=13, color=CHAR)
    save(f, 'freshness_gap')
    return dict(description=f'Bars of transactions per hour (distinct txn_id) for {day.date()} from mobile_money_log.csv, after parsing both timestamp formats. The largest gap between consecutive transactions in the month, {gaps.max():.1f} hours from {g_start.strftime("%H:%M:%S")} to {g_end.strftime("%H:%M:%S")}, is shaded with a hairline hatch and labelled in clay.',
                alt=f'Bar chart of transactions per hour on one day with a hatched {gaps.max():.0f} hour stretch around midday where nothing was recorded.')


# ============================================================================ 20 pii_counts
@fig('pii_counts', 7.0)
def f_pii():
    from pypdf import PdfReader
    md = csv('docs_metadata')
    L = md[(md.family == 'claims_letter') & (md.format == 'text_pdf')]
    pats = [('Phone numbers', r'\+\d{3} \d{3} \d{3} \d{3}'), ('Customer ids KT-', r'KT-\d{7}'), ('National ids KX', r'KX\d{12}'), ('Emails', r'[\w.+-]+@[\w-]+\.[\w.-]+'),
            ('Names after Mr, Mrs, Ms, Dr', r'\b(?:Mr|Mrs|Ms|Miss|Dr)\.? [A-Z][a-z]+(?: [A-Z][a-z]+)?')]
    counts = {p[0]: 0 for p in pats}
    hit_letters = 0
    for fl in L.file:
        t = ' '.join((pg.extract_text() or '') for pg in PdfReader(str(Path(DATA) / 'docs' / fl)).pages).replace('\n', ' ')
        any_ = False
        for nm, rx in pats:
            c = len(re.findall(rx, t))
            counts[nm] += c
            any_ |= c > 0
        hit_letters += any_
    tot = sum(counts.values())
    order = sorted(counts.items(), key=lambda kv: -kv[1])
    f, ax = canvas(7.0, 4.4)
    title(ax, f'{hit_letters} of {len(L)} claims letters hold personal data')
    T(ax, 0.3, 3.75, f'Pattern matches in the text of the letters: {tot} in all', size=13, color=CHAR)
    xl, sc = 3.1, 2.9 / max(v for _, v in order)
    for i, (nm, v) in enumerate(order):
        y = 3.4 - i * 0.55
        col = CLAY if nm.startswith('National') else CHAR
        T(ax, 0.3, y, nm, size=13)
        if v:
            rect(ax, xl, y - 0.16, v * sc, 0.32, fc=col)
        T(ax, xl + v * sc + 0.1, y, str(v), size=13.5, weight='bold', color=col if col == CLAY else INK)
    line(ax, xl, 0.55, xl, 3.55, INK, 0.8)
    note(ax, 'Regular expressions on text read with pypdf. Names are a rough pattern.', y=0.2)
    save(f, 'pii_counts')
    return dict(description=f'Horizontal bars of personal data pattern matches found by regular expression in the text (pypdf) of the {len(L)} claims letters: ' + '; '.join(f'{k} {v}' for k, v in order) + f'; {tot} matches in all. {hit_letters} of {len(L)} letters contain at least one. National ids are clay as the most sensitive pattern. Name matches use a title plus capitalised words pattern and are approximate.',
                alt=f'Bar chart of personal data patterns found in the claims letters, with all {hit_letters} letters affected.')


# ============================================================================ 21 risk_matrix
@fig('risk_matrix', 12.4)
def f_risk():
    rk = csv('risk_register')
    rk['score'] = rk.likelihood * rk.impact
    hi = rk.score >= 15
    f, ax = canvas(12.4, 4.6)
    title(ax, f'{int(hi.sum())} of {len(rk)} risks score 15 or more on likelihood times impact')
    gx, gy, cs = 1.15, 0.85, 0.66
    for i in range(6):
        line(ax, gx, gy + i * cs, gx + 5 * cs, gy + i * cs, HAIR, 0.8)
        line(ax, gx + i * cs, gy, gx + i * cs, gy + 5 * cs, HAIR, 0.8)
    for i in range(1, 6):
        T(ax, gx - 0.12, gy + (i - 0.5) * cs, str(i), size=13, color=GREY, ha='right')
        T(ax, gx + (i - 0.5) * cs, gy - 0.2, str(i), size=13, color=GREY, ha='center')
    T(ax, gx + 2.5 * cs, gy - 0.5, 'Impact', size=13.5, color=CHAR, ha='center', weight='bold')
    T(ax, 0.3, gy + 2.5 * cs, 'Likelihood', size=13.5, color=CHAR, weight='bold', rotation=90, ha='center')
    seen = {}
    for r in rk.itertuples():
        k = (r.likelihood, r.impact)
        n = seen.get(k, 0)
        seen[k] = n + 1
    seen2 = {}
    for r in rk.itertuples():
        k = (r.likelihood, r.impact)
        n = seen2.get(k, 0)
        seen2[k] = n + 1
        tot = seen[k]
        dx = (n - (tot - 1) / 2) * 0.3
        x, y = gx + (r.impact - 0.5) * cs + dx, gy + (r.likelihood - 0.5) * cs
        col = CLAY if r.score >= 15 else CHAR
        dot(ax, x, y, 0.14, col)
        T(ax, x, y - 0.005, str(int(r.id[1:])), size=13, color='white', weight='bold', ha='center')
    xr = 5.1
    ordr = rk.sort_values(['score', 'id'], ascending=[False, True])
    for i, r in enumerate(ordr.itertuples()):
        col_, row_ = divmod(i, 6)
        x = xr + col_ * 3.7
        y = 3.85 - row_ * 0.6
        hi_ = r.score >= 15
        T(ax, x, y + 0.1, f'{int(r.id[1:])}', size=14, weight='bold', color=CLAY if hi_ else INK)
        ls = wrap(ax, r.risk, 2.9, 13, 'bold' if hi_ else 'normal')[:2]
        for q, ln in enumerate(ls):
            T(ax, x + 0.3, y + 0.1 - q * 0.2, ln, size=13, color=CLAY if hi_ else INK, weight='bold' if hi_ else 'normal')
            if q == len(ls) - 1:
                T(ax, x + 0.3 + tw(ax, ln, 13, 'bold' if hi_ else 'normal') + 0.1, y + 0.1 - q * 0.2, f'({r.score})', size=13, color=GREY)
    note(ax, 'Risks from risk_register.csv. Score = likelihood x impact.', y=0.17)
    save(f, 'risk_matrix')
    bands = (int((rk.score >= 15).sum()), int(rk.score.between(8, 14).sum()), int((rk.score < 8).sum()))
    return dict(description=f'A 5 by 5 grid, likelihood up the side and impact along the bottom, with the {len(rk)} risks of risk_register.csv as numbered dots (number = the id R01 to R12). Dots scoring 15 or more are clay ({bands[0]} risks); {bands[1]} score 8 to 14 and {bands[2]} score below 8 (charcoal). A list on the right gives each risk name and score, highest first.',
                alt=f'A likelihood by impact grid with twelve numbered risk dots, three in clay for scores of 15 or more.')


# ============================================================================ 22 roadmap_gantt
SHORT = {'W01': 'Name council and owners', 'W02': 'Inventory and classify sources', 'W03': 'Approve policies', 'W04': 'Choose hosting, write exit plan',
         'W05': 'Fix quality defects', 'W06': 'Data contracts for 3 datasets', 'W07': 'Raw, cleaned, serving zones', 'W08': 'Read and repair documents',
         'W09': 'Train staff, publish guidance', 'W10': 'Test set and recall tracking', 'W11': 'Midyear rescore', 'W12': 'Mask personal data',
         'W13': 'Permission filters and logging', 'W14': 'Freshness and schema alerts', 'W15': 'Staff policy assistant pilot', 'W16': 'Second rescore, board report'}


@fig('roadmap_gantt', 12.4)
def f_gantt():
    rd = csv('roadmap_items')
    assert set(rd.id) == set(SHORT)
    rd = rd.reset_index(drop=True)
    row = {r.id: i for i, r in rd.iterrows()}
    dur = rd.set_index('id').duration_months
    start = rd.set_index('id').start_month
    deps = {r.id: ([d for d in str(r.depends_on).split(';')] if isinstance(r.depends_on, str) else []) for r in rd.itertuples()}
    for i, ds in deps.items():
        for d in ds:
            assert start[i] >= start[d] + dur[d], f'{i} starts before {d} ends'
    memo = {}

    def chain(i):
        if i not in memo:
            best, prev = 0, None
            for d in deps[i]:
                c, _ = chain(d)
                if c > best:
                    best, prev = c, d
            memo[i] = (best + dur[i], prev)
        return memo[i]
    end = max(rd.id, key=lambda i: (chain(i)[0], start[i] + dur[i]))
    crit, cur = [], end
    while cur:
        crit.append(cur)
        cur = chain(cur)[1]
    cm = chain(end)[0]
    H = 6.2
    f, ax = canvas(12.4, H)
    title(ax, f'Twelve months, {len(rd)} work items, and a chain of {cm} months that cannot slip')
    x0, x1 = 3.55, 12.1
    mw = (x1 - x0) / 12
    top = H - 1.0
    step = 0.275
    for m_ in range(12):
        T(ax, x0 + (m_ + 0.5) * mw, top + 0.3, f'M{m_ + 1}', size=13, color=GREY, ha='center')
    for m_ in range(13):
        line(ax, x0 + m_ * mw, 0.8, x0 + m_ * mw, top + 0.12, HAIR, 0.6)
    line(ax, 0.3, top + 0.12, x1, top + 0.12, INK, 0.9)
    for r in rd.itertuples():
        y = top - (row[r.id] + 0.5) * step
        T(ax, 0.3, y, r.id, size=13, color=GREY)
        T(ax, 0.82, y, SHORT[r.id], size=13)
        c = r.id in crit
        rect(ax, x0 + (r.start_month - 1) * mw + 0.02, y - 0.09, r.duration_months * mw - 0.04, 0.18, fc=CLAY if c else CHAR)
    for i, ds in deps.items():
        for d in ds:
            ya = top - (row[d] + 0.5) * step
            yb = top - (row[i] + 0.5) * step
            xa = x0 + (start[d] - 1 + dur[d]) * mw
            xb = x0 + (start[i] - 1) * mw + 0.02
            xm = xa + 0.06 if xb - xa > 0.1 else xa + 0.03
            ax.plot([xa - 0.02, xm, xm, xb - 0.01], [ya, ya, yb, yb], color=INK, lw=0.7, zorder=4, solid_joinstyle='miter')
            ax.add_patch(Polygon([(xb, yb), (xb - 0.07, yb + 0.035), (xb - 0.07, yb - 0.035)], fc=INK, ec='none', zorder=4))
    xr = x0 + 6 * mw
    ax.plot([xr, xr], [0.7, top + 0.12], color=INK, lw=1.4, ls=(0, (5, 3)), zorder=5)
    T(ax, xr, 0.5, 'rescore', size=14, weight='bold', ha='center')
    T(ax, 12.1, 0.17, 'clay: the longest chain of dependent items', size=13, color=CLAY, ha='right', weight='bold')
    note(ax, 'Lines join an item to the work it waits for. From roadmap_items.csv.', y=0.17, x=0.3, ha='left')
    save(f, 'roadmap_gantt')
    return dict(description=f'A Gantt chart of the {len(rd)} work items in roadmap_items.csv across 12 months (M1 to M12): one bar per item from its start_month for its duration_months, thin elbow lines from the end of each prerequisite to the start of the item that depends on it, and a vertical dashed marker after month 6 labelled "rescore". The longest dependency chain ({" > ".join(sorted(crit, key=lambda i: start[i]))}, {cm} months) is clay. A check confirms no item starts before its prerequisite ends.',
                alt=f'A twelve month Gantt chart of sixteen work items with dependency lines, a rescore marker after month six and the {cm} month critical chain in clay.')


# ============================================================================ 23 governance_roles
@fig('governance_roles', 7.0)
def f_roles():
    src = csv('sources')
    n_no = int(src.owner.isna().sum())
    roles = [('Steering council', 'Which AI uses go ahead, and what they may spend.'), ('Data owner', 'Who may use this data, and for what.'),
             ('Data steward', 'What good enough quality means, and who is told when it fails.'), ('Data custodian', 'How the data is stored, backed up and protected.'),
             ('Data user', 'Whether a result is good enough to act on.')]
    f, ax = canvas(7.0, 4.6)
    title(ax, 'Five roles, and the one decision each makes')
    for i, (nm, dec) in enumerate(roles):
        y = 3.72 - i * 0.7
        line(ax, 0.3, y + 0.35, 6.7, y + 0.35, INK if i == 0 else HAIR, 1.0 if i == 0 else 0.7)
        T(ax, 0.3, y, nm, size=17, weight='bold', family=SERIF)
        ls = wrap(ax, dec, 3.9, 13.5)
        for q, ln in enumerate(ls):
            T(ax, 2.7, y + (len(ls) - 1) * 0.1 - q * 0.21, ln, size=13.5, color=INK)
        if nm == 'Data owner':
            T(ax, 2.7, y - 0.22 - (len(ls) - 1) * 0.0, f'Kitara: {n_no} of {len(src)} sources have none.', size=13, color=CLAY, weight='bold') if len(ls) == 1 else None
    line(ax, 0.3, 3.72 - 4 * 0.7 - 0.35, 6.7, 3.72 - 4 * 0.7 - 0.35, HAIR, 0.7)
    note(ax, 'Illustrative. Job titles vary; what matters is that each decision has one name against it.', y=0.2)
    save(f, 'governance_roles')
    return dict(description=f'Typography only, with hairlines: five roles stacked top to bottom (steering council, data owner, data steward, data custodian, data user), each with the one decision it makes. Under the data owner, in clay, the Kitara fact from sources.csv that {n_no} of {len(src)} sources name no owner. The role split is illustrative.',
                alt='Five data roles listed one above the other, each with the single decision it is responsible for.')


# ============================================================================ main
def main():
    global DATA, OUT
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    DATA, OUT = sys.argv[1], sys.argv[2]
    Path(OUT).mkdir(parents=True, exist_ok=True)
    want = sys.argv[3:] or list(CAT)
    cat_path = Path(OUT) / 'catalog.json'
    cat = json.loads(cat_path.read_text()) if (cat_path.exists() and sys.argv[3:]) else {}
    for name in CAT:
        if name not in want:
            continue
        w, fn = CAT[name]
        r = fn()
        assert not r['alt'].endswith('.') or True
        cat[name] = dict(description=r['description'], alt=r['alt'], width_in=w)
        print('drawn', name)
    ordered = {n: cat[n] for n in CAT if n in cat}
    cat_path.write_text(json.dumps(ordered, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'{len(ordered)} figures, catalog.json written')


if __name__ == '__main__':
    main()
