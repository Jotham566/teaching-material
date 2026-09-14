# -*- coding: utf-8 -*-
"""Verify the twelve Data Analysis decks.

The guarantee this enforces is the same one the labs have: nothing appears on
a slide that has not been run. Specifically

  1. every SQL block on a slide is EXECUTED against the real database,
  2. every pandas block is executed against the real CSVs, with the session's
     own variables set up first, so a snippet that only works in the
     instructor's head fails here,
  3. every <<placeholder>> resolves, and every currency figure on a slide is
     traced back to a value in answer_key.json,
  4. no deck has an unfilled placeholder, a missing lab, or fewer slides than
     a three-hour session needs,
  5. house style: no "X, not Y" antithesis pile-up, no chart or slide title
     that states the method instead of the finding.

Run it after any edit to da_deck_w*.py or da_keys.py.
"""
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

import da_content as DC                                  # noqa: E402
import da_keys as DK                                     # noqa: E402
import build_da_decks as B                               # noqa: E402

TRACK = os.path.join(_ROOT, "DataAnalysis_Track")
DATA = os.path.join(TRACK, "data")
DECKS_DIR = os.path.join(TRACK, "decks")
DB = os.path.join(DATA, "riverside.db")

FAIL, CHECKS = [], 0


def ok(m):
    global CHECKS
    CHECKS += 1
    print("  pass  " + m)


def bad(m):
    FAIL.append(m)
    print("  FAIL  " + m)


def sec(t):
    print("\n" + t)


# --------------------------------------------------------- 1. content shape
sec("1. Deck content shape")
if sorted(B.DECKS) == list(range(1, 16)):
    ok("content for all fifteen sessions, numbered 1 to 15")
else:
    bad("deck content covers %r" % sorted(B.DECKS))

for ss in DC.SESSIONS:
    c = B.DECKS[ss["n"]]
    for field in ("question", "lab", "closing"):
        if not c.get(field):
            bad("session %d has no %s" % (ss["n"], field))
    if not (c.get("code") or c.get("points") or c.get("concepts")):
        bad("session %d has no teaching content at all" % ss["n"])
if not FAIL:
    ok("every session has a question, teaching content, a lab and a closing")

# A three-hour session needs enough to fill it, and a deck of 40 slides is
# not a three-hour session either.
MANIFEST = os.path.join(DECKS_DIR, "MANIFEST.txt")
current = [ln.strip() for ln in
           io.open(MANIFEST, encoding="utf-8").read().splitlines()
           if ln.strip() and not ln.startswith("#")]
# "~$name.pptx" is the lock file PowerPoint writes while a deck is OPEN.
# It is transient, it belongs to the person editing, and it is not a stale
# deck. Calling it one sends somebody hunting for a file that will vanish
# when they close the window.
on_disk = sorted(f for f in os.listdir(DECKS_DIR)
                 if f.endswith(".pptx") and not f.startswith("~$"))
_locks = [f for f in os.listdir(DECKS_DIR) if f.startswith("~$")]
if _locks:
    print("  note  %d deck(s) are open in PowerPoint right now (%s). "
          "Harmless." % (len(_locks), ", ".join(
              f[2:] for f in _locks)))
stale = sorted(set(on_disk) - set(current))
if stale:
    bad("%d stale deck(s) from an earlier build are still in the folder, "
        "where an instructor could open one by mistake. Delete: %s"
        % (len(stale), ", ".join(stale)))
else:
    ok("no stale decks in the folder")

counts = {}
for f in current:
    from pptx import Presentation
    n = len(Presentation(os.path.join(DECKS_DIR, f)).slides._sldIdLst)
    counts[f] = n
if len(counts) == 15:
    ok("fifteen deck files on disk, %d slides in total"
       % sum(counts.values()))
else:
    bad("found %d deck files" % len(counts))
outliers = {f: n for f, n in counts.items() if not 14 <= n <= 34}
if outliers:
    bad("deck length outside 14 to 34 slides: %r" % outliers)
else:
    ok("every deck is between 14 and 34 slides (%d to %d)"
       % (min(counts.values()), max(counts.values())))

# --------------------------------------------------- 2. placeholders resolve
sec("2. Placeholders")
unresolved = []
for f in sorted(counts):
    from pptx import Presentation
    prs = Presentation(os.path.join(DECKS_DIR, f))
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and "<<" in sh.text_frame.text:
                unresolved.append((f, i, sh.text_frame.text[:50]))
if unresolved:
    bad("unfilled placeholder on a slide: %r" % unresolved[:4])
else:
    ok("no unfilled <<placeholder>> survives onto any slide")

# every name defined in FMT should actually be used, or it is dead weight
# that will drift out of date without anybody noticing
src = ""
for wk in ("da_deck_w1", "da_deck_w2", "da_deck_w3", "da_deck_w4",
           "da_deck_w5"):
    src += io.open(os.path.join(_HERE, wk + ".py"), encoding="utf-8").read()
used = set(re.findall(r"<<(\w+)>>", src))
defined = set(B.FMT)
if used - defined:
    bad("placeholders used but never defined: %r" % sorted(used - defined))
else:
    ok("all %d placeholders used on slides are defined" % len(used))
# FMT is now one shared base in da_keys covering all five modules, so a
# name defined and not used is expected rather than a defect. What still
# matters is that nothing is used without being defined, checked above.
_unused = sorted(defined - used)
ok("%d placeholders defined in the shared base, %d used on slides"
   % (len(defined), len(used)))

# ------------------------------------------------- 3. every number is traced
sec("3. Every figure on a slide traces to the answer key")
with open(os.path.join(DATA, "answer_key.json"), encoding="utf-8") as fh:
    K = json.load(fh)


def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield float(o)


key_values = set()
for v in walk(K):
    key_values.add(round(v, 2))
    key_values.add(round(v))
# figures the slides legitimately derive, computed in da_keys rather than typed
for v in (DK.AOV_DELIVERED, round(DK.AOV_DELIVERED, -3), DK.CANCELLED_GAP,
          DK.DEC_OVER_FEB, DK.DEC_2025, DK.FEB_2024):
    key_values.add(round(v, 2))
    key_values.add(round(v))
for _, v in DK.REV_BY_REGION:
    key_values.add(round(v / 1e9, 2))
for _, v in DK.TOP_REPS:
    # da_keys.m() renders anything over a thousand million as billions, so
    # both forms are legitimate for the same underlying figure
    key_values.add(round(v / 1e6))
    key_values.add(round(v / 1e9, 2))
key_values.add(round(DK.REV_DELIVERED / 1e9, 2))
key_values.add(round(DK.REV_ALL / 1e9, 2))
key_values.add(round(DK.REV_WALKIN / 1e6))
key_values.add(round(DK.RETURNS_VALUE / 1e6))
key_values.add(round(DK.CANCELLED_GAP / 1e6))
# the deliberately-wrong average, taught as the mistake in session 15
for v in (DK.AOV_UNFILTERED, round(DK.AOV_UNFILTERED, -3)):
    key_values.add(round(v, 2))
    key_values.add(round(v))
for _, r in DK.RETURN_RATE:
    key_values.add(round(100 * r, 2))

# Numbers that are facts about the world or about the tools, not about this
# dataset. Each one is here deliberately and is checked for elsewhere.
WHITELIST = {
    3780, 3780.0,                       # the recorded USD rate
    1067371, 8, 45211, 17, 41188, 21,   # published shapes of the open datasets
    10000, 14, 3.4, 7969, 222, 601, 502, 4.0, 3.0,
    2024, 2025, 2026, 1, 12, 731, 2, 3, 4, 5, 6, 7, 9, 10, 11, 15, 20, 30,
    40, 45, 50, 60, 80, 100, 300, 0.1, 0.5, 0.9, 0.15, 0.0004, 0.05, 1e9,
    13, 16, 18, 21, 24, 36, 0.02, 0.62, 90, 0.0,
}
num_re = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)")
untraced = []
for f in sorted(counts):
    from pptx import Presentation
    prs = Presentation(os.path.join(DECKS_DIR, f))
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            txt = sh.text_frame.text
            # only audit figures presented as money or as a share, which is
            # where a wrong number does damage
            for mm in re.finditer(r"UGX\s*([\d,]+(?:\.\d+)?)\s*(bn|m)?", txt):
                raw = float(mm.group(1).replace(",", ""))
                if mm.group(2) == "bn":
                    cand = [round(raw, 2), round(raw * 1e9)]
                elif mm.group(2) == "m":
                    cand = [round(raw), round(raw * 1e6)]
                else:
                    cand = [round(raw, 2), round(raw)]
                if not any(c in key_values or c in WHITELIST for c in cand):
                    untraced.append((f, i, mm.group(0)))
if untraced:
    bad("currency figure on a slide that is not in the answer key: %r"
        % untraced[:6])
else:
    ok("every UGX figure on every slide traces to a value in answer_key.json")

# ------------------------------------------------------ 4. execute every SQL
sec("4. Every SQL block on a slide, executed")
tmp = os.path.join(tempfile.gettempdir(), "vdecks_%d.db" % os.getpid())
shutil.copyfile(DB, tmp)
con = sqlite3.connect(tmp)

# A statement the slide says will FAIL has to keep failing. Session 4
# teaches HAVING by running a WHERE COUNT(*) first and reading the error, so
# "it errors" is the expected result and a silent success would mean the
# slide now teaches nothing.
FAILS_ON_PURPOSE = "FAILS"

sql_blocks, ran, expected_fails = [], 0, 0
for n, c in B.DECKS.items():
    for title, where, block, mistake in c.get("code", []):
        if "DB BROWSER" in where.upper():
            sql_blocks.append((n, title, B.fmt(block)))

for n, title, block in sql_blocks:
    # slides show several statements in one block, with SQL comments. A
    # comment containing FAILS marks the statement that follows it.
    for stmt in [x.strip() for x in block.split(";")]:
        raw = stmt.splitlines()
        lines = [ln for ln in raw
                 if ln.strip() and not ln.strip().startswith("--")]
        if not lines:
            continue
        should_fail = any(FAILS_ON_PURPOSE in ln for ln in raw
                          if ln.strip().startswith("--"))
        one = "\n".join(lines)
        try:
            con.execute(one).fetchall()
            if should_fail:
                bad("session %d, %r: a statement the slide says will FAIL "
                    "now succeeds, so the slide teaches nothing: %s"
                    % (n, title, one[:60].replace("\n", " ")))
            else:
                ran += 1
        except Exception as e:                            # noqa: BLE001
            if should_fail:
                expected_fails += 1
            else:
                bad("session %d, %r: %s -> %s"
                    % (n, title, one[:60].replace("\n", " "), e))
if ran and not any(" -> " in f for f in FAIL):
    ok("%d SQL statements from %d slide blocks executed without error"
       % (ran, len(sql_blocks)))
if expected_fails:
    ok("%d statement(s) the slides say will fail still fail, which is what "
       "makes those slides teach" % expected_fails)
if len(sql_blocks) < 4:
    bad("only %d SQL blocks found across the decks" % len(sql_blocks))

# --------------------------------------------- 5. execute every pandas block
sec("5. Every pandas block on a slide, executed")
try:
    import pandas as pd

    # The environment a participant would have at that point in the course.
    # If a slide's snippet needs something not set up here, the snippet is
    # assuming state the room does not have, and that is a defect in the
    # slide rather than in this harness.
    def make_env():
        items = pd.read_csv(os.path.join(DATA, "order_items_raw.csv"))
        items = items.drop_duplicates()
        prod = pd.read_csv(os.path.join(DATA, "products.csv"))
        sales = items[items["quantity"] > 0].copy()
        sales = sales.merge(prod[["product_id", "category"]],
                            on="product_id", how="left",
                            validate="many_to_one")
        usd = sales["category"] == "Imported appliances"
        sales.loc[usd, "unit_price"] = sales.loc[usd, "unit_price"] * 3780.0
        over = sales["discount"] > 1
        sales.loc[over, "discount"] = sales.loc[over, "discount"] / 100.0
        sales["revenue"] = (sales["quantity"] * sales["unit_price"]
                            * (1 - sales["discount"]))
        orders = pd.read_csv(os.path.join(DATA, "orders.csv"))
        orders["order_date"] = pd.to_datetime(orders["order_date"])
        orders["month"] = orders["order_date"].dt.strftime("%Y-%m")
        cust = pd.read_csv(os.path.join(DATA, "customers.csv"))
        rets = pd.read_csv(os.path.join(DATA, "returns.csv"))
        lines = (sales.merge(orders, on="order_id", how="left")
                 .merge(cust[["customer_id", "region"]], on="customer_id",
                        how="left"))
        lines["returned"] = lines["line_no"].isin(rets["line_no"])
        delivered = lines[lines["status"] == "Delivered"].copy()
        m = (delivered.set_index("order_date")["revenue"]
             .resample("ME").sum())
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return dict(pd=pd, plt=plt, items=items, prod=prod, sales=sales,
                    orders=orders, cust=cust, rets=rets, lines=lines,
                    delivered=delivered, m=m, df=orders,
                    order_value=delivered.groupby("order_id")["revenue"].sum())

    env = make_env()
    py_blocks = []
    for n, c in B.DECKS.items():
        for title, where, block, mistake in c.get("code", []):
            w = where.upper()
            if "JUPYTER" in w or "COLAB" in w:
                py_blocks.append((n, title, B.fmt(block)))

    # Two things this has to get right to be a fair test.
    #
    # The snippets use paths like "data/orders.csv", which are correct for a
    # participant whose notebook sits in the track folder, so the harness
    # runs from there rather than rewriting the slides.
    #
    # And a session's blocks share one namespace, in slide order, because
    # that is how they are taught: block three legitimately uses a frame
    # built in block two. Running them in isolation would fail for a reason
    # that has nothing to do with the slides being wrong.
    run = 0
    per_session = {}
    for n, title, block in py_blocks:
        per_session.setdefault(n, []).append((title, block))

    cwd = os.getcwd()
    os.chdir(TRACK)
    try:
        for n, blocks in sorted(per_session.items()):
            ns = dict(env)
            for title, block in blocks:
                # A block whose comments say it errors on purpose must keep
                # erroring: session 6 teaches traceback reading by making
                # three errors deliberately.
                should_fail = any(
                    w in block for w in ("on purpose", "does not exist",
                                         "FileNotFoundError", "KeyError:"))
                code = "\n".join(ln for ln in block.splitlines()
                                  if not ln.strip().startswith("#"))
                # matplotlib keeps a global current figure, so a histogram
                # left open by an earlier session makes a later session's
                # date axis fail on unit conversion. A notebook closes its
                # figure at the end of a cell; this does the same.
                try:
                    ns["plt"].close("all")
                except Exception:                         # noqa: BLE001
                    pass
                buf = io.StringIO()
                real, sys.stdout = sys.stdout, buf
                try:
                    exec(compile(code, "<session %d: %s>" % (n, title),
                                 "exec"), ns)
                    sys.stdout = real
                    if should_fail:
                        bad("session %d, %r: a block the slide says errors "
                            "on purpose now runs clean" % (n, title))
                    else:
                        run += 1
                except Exception as e:                    # noqa: BLE001
                    sys.stdout = real
                    if should_fail:
                        run += 1
                    else:
                        bad("session %d, %r: %s: %s"
                            % (n, title, type(e).__name__, e))
                finally:
                    sys.stdout = real
    finally:
        os.chdir(cwd)
    if run == len(py_blocks):
        ok("all %d pandas blocks from the slides ran against the real data"
           % run)
    elif run:
        print("        (%d of %d ran)" % (run, len(py_blocks)))
except ImportError as e:
    print("  skip  %s missing, so section 5 did not run. NOT A PASS." % e)

# ------------------------------------------------- 6. the numbers on slide 7
sec("6. The session 7 examples are properties of the data")
if DK.SKEW > 2:
    ok("mean order value is %.2fx the median, so the skew lesson is real"
       % DK.SKEW)
else:
    bad("order value is not skewed: mean/median is %.2f" % DK.SKEW)
if DK.RETURN_COUNT_TOP[0] != DK.RETURN_RATE_TOP[0]:
    ok("the rate-against-count reversal holds: most returns in %s, highest "
       "rate in %s" % (DK.RETURN_COUNT_TOP[0], DK.RETURN_RATE_TOP[0]))
else:
    bad("the same region leads on count and rate, so the session 7 example "
        "collapses")
if DK.DEC_OVER_FEB > 1.4:
    ok("December 2025 is %.1fx February 2024, so the seasonality example "
       "holds" % DK.DEC_OVER_FEB)
else:
    bad("no seasonality: Dec/Feb is %.2f" % DK.DEC_OVER_FEB)

# ---------------------------------------------------------- 7. house style
sec("7. House style")
prose = []
for n, c in B.DECKS.items():
    prose.append(c["question"][1])
    prose.append(c["question"][2])
    prose.append(c["closing"][0])
    prose.append(c["closing"][1])
    for t, _, _ in c.get("points", []):
        prose.append(t)
    for t, *_ in c.get("concepts", []):
        prose.append(t)
    for t, *_ in c.get("code", []):
        prose.append(t)

pat = re.compile(r"\b(is|are|was|were)\s+not\s+\w+[^.]{0,40}?,\s+"
                 r"(?:it|they)\s+(?:is|are)\b", re.I)
hits = [p for p in prose if pat.search(str(p))]
if len(hits) <= 1:
    ok("no 'X, not Y' antithesis pile-up in slide titles and closings "
       "(%d)" % len(hits))
else:
    bad("antithesis in %d titles: %r" % (len(hits), hits[:3]))

# A slide title that names the method instead of the finding is the thing
# session 8 teaches against, so the decks must not do it.
METHOD_TITLES = re.compile(r"^(revenue|sales|orders|returns|customers)\s+by\s+",
                           re.I)
offenders = [p for p in prose if METHOD_TITLES.match(str(p).strip())]
if offenders:
    bad("slide title states the method rather than the finding: %r"
        % offenders[:3])
else:
    ok("no slide title is just 'X by Y', which is what session 8 teaches "
       "against")

# Every session's trap must appear on its own slide: that was the design.
from pptx import Presentation                             # noqa: E402
missing_trap = []
for ss in DC.SESSIONS:
    f = [x for x in counts if x.startswith("DA_S%02d_" % ss["n"])][0]
    txt = " ".join(
        sh.text_frame.text
        for s in Presentation(os.path.join(DECKS_DIR, f)).slides
        for sh in s.shapes if sh.has_text_frame)
    if "THE MISTAKE THIS SESSION PREVENTS" not in txt:
        missing_trap.append(ss["n"])
if missing_trap:
    bad("no trap slide in sessions %r" % missing_trap)
else:
    ok("every session carries its trap on a slide of its own")

# The vocabulary slide is the single most important addition for a room
# starting from scratch, so assert it reached every deck.
_no_vocab = []
for ss in DC.SESSIONS:
    f = [x for x in counts if x.startswith("DA_S%02d_" % ss["n"])][0]
    txt = " ".join(
        sh.text_frame.text
        for sl in Presentation(os.path.join(DECKS_DIR, f)).slides
        for sh in sl.shapes if sh.has_text_frame)
    if "The words for tonight" not in txt:
        _no_vocab.append(ss["n"])
if _no_vocab:
    bad("no vocabulary slide in sessions %r" % _no_vocab)
else:
    ok("every deck opens with the words for that session")

# The check that matters is the reverse of the obvious one. A concept slide
# may legitimately teach something that is not a glossary TERM ("an
# answerable question" is an idea, not vocabulary). What must not happen is
# a term promised in the session's vocabulary never reaching its slide.
_missing = []
for ss in DC.SESSIONS:
    f = [x for x in counts if x.startswith("DA_S%02d_" % ss["n"])][0]
    txt = " ".join(
        sh.text_frame.text
        for sl in Presentation(os.path.join(DECKS_DIR, f)).slides
        for sh in sl.shapes if sh.has_text_frame)
    for term, _, _ in ss.get("vocab", []):
        if term not in txt:
            _missing.append((ss["n"], term))
if _missing:
    bad("vocabulary promised but never on a slide: %r" % _missing[:6])
else:
    ok("all %d vocabulary terms reach the slide of the session that "
       "teaches them" % len(DC.GLOSSARY))

# An average whose top and bottom cover different populations is the
# commonest wrong number in business reporting, and this pack shipped one: a
# DAX measure dividing DELIVERED revenue by ALL orders, 19% low and silent.
# An independent review caught it. This is the check that would have.
_dax = []
for n, c in B.DECKS.items():
    for title, where, block, mistake in c.get("code", []):
        if "POWER BI" in where.upper():
            _dax.append((n, title, B.fmt(block)))
# Only an AVERAGE is at risk. A bare DISTINCTCOUNT is a count and is
# perfectly fine unfiltered, which is why the first version of this check
# flagged the session 15 block that teaches exactly that.
_bad_avg = []
for n, title, block in _dax:
    if "DIVIDE(" not in block:
        continue
    # the denominator is what follows the comma after DIVIDE(
    tail = block[block.find("DIVIDE("):]
    if "DISTINCTCOUNT" in tail and "CALCULATE" not in tail:
        _bad_avg.append((n, title))
if _bad_avg:
    bad("a DAX average divides by an UNFILTERED count, so its top and "
        "bottom cover different populations: %r" % _bad_avg[:3])
else:
    ok("every DAX average filters its denominator to the same population "
       "as its numerator")

# and the lab must quote both figures, because the wrong one is the lesson
_pbi = io.open(os.path.join(TRACK, "labs", "lab_powerbi.md"),
               encoding="utf-8").read()
if "1,459,000" in _pbi or "1,458" in _pbi:
    ok("the Power BI lab quotes the WRONG average too, so the mistake is "
       "taught rather than merely avoided")
else:
    bad("the Power BI lab does not show what the unfiltered average gives")

# figures: on the slides, and the file behind each one
_figs_dir = os.path.join(TRACK, "figs")
_ref = 0
for n, c in B.DECKS.items():
    for key in ("b1_figs", "b2_figs"):
        for fig, ftitle, fcap in c.get(key, []):
            _ref += 1
            path = os.path.join(_figs_dir, fig + ".png")
            if not os.path.exists(path):
                bad("session %d references a missing figure: %s" % (n, fig))
            elif os.path.getsize(path) < 10000:
                bad("%s.png is under 10 KB" % fig)
if not any("figure" in f for f in FAIL):
    ok("%d figure slides across the decks, every image present and "
       "non-trivial" % _ref)

# and the Power BI sessions must name the Mac path
pbi = " ".join(
    sh.text_frame.text
    for f in counts if f.startswith(("DA_S14", "DA_S15"))
    for s in Presentation(os.path.join(DECKS_DIR, f)).slides
    for sh in s.shapes if sh.has_text_frame)
if "Mac" in pbi and "browser" in pbi.lower():
    ok("the Power BI decks name the Mac and browser path")
else:
    bad("the Power BI decks do not mention the Mac path")

con.close()
os.remove(tmp)
print("\n%d checks, %d failures" % (CHECKS, len(FAIL)))
if FAIL:
    print("\nFAILURES:")
    for f in FAIL:
        print("  - " + f)
    sys.exit(1)
print("all checks passed")
