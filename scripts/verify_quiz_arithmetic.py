# -*- coding: utf-8 -*-
"""Check the quiz banks against the things a structural test cannot see.

quiz_banks.py already asserts the shape of every question: four options, one
correct, feedback everywhere. That passes happily on a question whose code
block claims an output the code does not produce, or whose mix breaks the
design rule, or that could be answered without reading the snippet.

This script checks the rest:

  1. ARITHMETIC. Every buggy snippet in the banks is re-implemented here and
     executed. The value the question prints must be the value the code
     really produces, and the value the feedback calls correct must really
     be correct. A diagnosis question that lies about its own output teaches
     the wrong lesson.
  2. MIX. Weeks 3 onward must be 2 diagnosis, 1 traceback, 1 interpretation,
     1 judgement. Weeks 1 and 2 have their own documented mixes.
  3. STYLE. The house rules: no "X, not Y" antithesis, no em-dash asides.
  4. COHORT HYGIENE. A cohort must never see another cohort's domain terms.
  5. ANSWER POSITION. The correct option must not sit in the same slot every
     time, since the Apps Script shuffles per cohort but the bank order is
     what a printed paper fallback would use.
"""
import re
import sys
from collections import Counter

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

import quiz_banks as QB

FAILED = []


def ok(label, cond, detail=""):
    if cond:
        print(f"  pass  {label}")
    else:
        print(f"  FAIL  {label}" + (f"  ({detail})" if detail else ""))
        FAILED.append(label)


# ---------------------------------------------------------------------------
print("1. Arithmetic in the code blocks, executed")
# ---------------------------------------------------------------------------

# --- W3 Q1: unit errors
ok("W3 slab volume with mm passed as m == 6000.00",
   abs(6.0 * 4.0 * 250 - 6000.0) < 1e-9)
ok("W3 slab volume correct == 6.00", abs(6.0 * 4.0 * 0.25 - 6.0) < 1e-9)
ok("W3 contained metal with g/t as pct == 4,500,000",
   abs(250000.0 * 1800 / 100.0 - 4500000.0) < 1e-6)
ok("W3 contained metal correct == 450", abs(250000.0 * 0.18 / 100.0 - 450.0) < 1e-9)
_p_bad = 8.5 * 151.8 * 2 * 3.14159 / 60.0
_p_ok = 8.5 * 1450 * 2 * 3.14159 / 60.0
ok("W3 shaft power with rad/s == 135 W", round(_p_bad) == 135, f"{_p_bad:.1f}")
ok("W3 shaft power correct == 1291 W", round(_p_ok) == 1291, f"{_p_ok:.1f}")


# --- W3 Q2: if-chain order
def crack_bad(w, e):
    if w > 0.10:
        return "monitor"
    elif w > 0.30:
        return "flag for repair"
    elif e == "marine" and w > 0.20:
        return "seal now"
    return "no action"


def crack_ok(w, e):
    if e == "marine" and w > 0.20:
        return "seal now"
    elif w > 0.30:
        return "flag for repair"
    elif w > 0.10:
        return "monitor"
    return "no action"


ok("W3 crack_action mis-ordered returns 'monitor'",
   crack_bad(0.45, "marine") == "monitor")
ok("W3 crack_action correct returns 'seal now'",
   crack_ok(0.45, "marine") == "seal now")
ok("W3 Q4 crack_action(0.25, marine) == 'seal now'",
   crack_ok(0.25, "marine") == "seal now")


def grade_bad(g, c):
    if g >= c * 0.8:
        return "stockpile"
    elif g >= c * 1.5:
        return "mill now"
    elif g >= c:
        return "mill"
    return "waste"


def grade_ok(g, c):
    if g >= c * 1.5:
        return "mill now"
    elif g >= c:
        return "mill"
    elif g >= c * 0.8:
        return "stockpile"
    return "waste"


ok("W3 grade_action mis-ordered returns 'stockpile'",
   grade_bad(1.2, 0.5) == "stockpile")
ok("W3 grade_action correct returns 'mill now'",
   grade_ok(1.2, 0.5) == "mill now")
ok("W3 Q4 grade_action(0.45, 0.50) == 'stockpile'",
   grade_ok(0.45, 0.50) == "stockpile")


def temp_bad(w, a):
    if w - a > 80:
        return "investigate cooling"
    elif w > 155:
        return "trip"
    elif w > 130:
        return "alarm"
    return "normal"


def temp_ok(w, a):
    if w > 155:
        return "trip"
    elif w > 130:
        return "alarm"
    elif w - a > 80:
        return "investigate cooling"
    return "normal"


ok("W3 temp_action mis-ordered returns 'investigate cooling'",
   temp_bad(162.0, 25.0) == "investigate cooling")
ok("W3 temp_action correct returns 'trip'", temp_ok(162.0, 25.0) == "trip")
ok("W3 Q4 temp_action(120, 25) == 'investigate cooling'",
   temp_ok(120.0, 25.0) == "investigate cooling")
ok("W3 Q4 rise at 120/25 is 95 K", 120 - 25 == 95)


# --- W4 Q1: accumulator reset inside the loop
def acc_bad(vals):
    total = 0.0
    for v in vals:
        total = 0.0
        total = total + v
    return total / len(vals)


for _label, _vals, _bad, _good in [
    ("W4 widths", [0.12, 0.35, 0.41, 0.08], 0.020, 0.240),
    ("W4 rates", [7.2, 9.5, 8.1, 6.4], 1.600, 7.800),
    ("W4 temps", [118, 131, 126, 141], 35.25, 129.00),
]:
    ok(f"{_label} buggy mean == {_bad}", abs(acc_bad(_vals) - _bad) < 5e-4,
       f"{acc_bad(_vals):.4f}")
    _m = sum(_vals) / len(_vals)
    ok(f"{_label} true mean == {_good}", abs(_m - _good) < 5e-4, f"{_m:.4f}")

# --- W4 Q2: range starting at one
for _label, _vals, _lim, _bad, _good in [
    ("W4 widths >0.30", [0.44, 0.35, 0.41, 0.08], 0.30, 2, 3),
    ("W4 rates >8.0", [9.1, 8.6, 7.2, 8.3], 8.0, 2, 3),
    ("W4 temps >130", [134, 131, 128, 126], 130, 1, 2),
]:
    _b = sum(1 for i in range(1, len(_vals)) if _vals[i] > _lim)
    _g = sum(1 for v in _vals if v > _lim)
    ok(f"{_label} buggy count == {_bad}", _b == _bad, str(_b))
    ok(f"{_label} true count == {_good}", _g == _good, str(_g))
    ok(f"{_label} first element really is over the limit", _vals[0] > _lim)

# --- W5 Q2: text max is alphabetical
_vals = ["32.5", "41.2", "9.9", "28.0"]
ok("W5 text max == '9.9'", max(_vals) == "9.9")
ok("W5 numeric max == 41.2", max(float(v) for v in _vals) == 41.2)

# --- W6 Q1: sentinel averaged as data
for _label, _vals, _sent, _bad, _good in [
    ("W6 silica -999", [2.1, 2.4, -999, 2.8, 2.2], -999, -197.90, 2.375),
    ("W6 floor area 0", [120, 0, 95, 110], 0, 81.25, 108.3333),
    ("W6 vibration 0.0", [2.41, 0.0, 2.38, 2.44], 0.0, 1.8075, 2.4100),
]:
    _b = sum(_vals) / len(_vals)
    _real = [v for v in _vals if v != _sent]
    _g = sum(_real) / len(_real)
    ok(f"{_label} mean with sentinel == {_bad}", abs(_b - _bad) < 5e-3,
       f"{_b:.4f}")
    ok(f"{_label} mean of real values == {_good}", abs(_g - _good) < 5e-3,
       f"{_g:.4f}")

# --- W9: the confusion matrix, and every figure quoted about it
_tn, _fp, _fn, _tp = 9620, 36, 310, 34
_tot = _tn + _fp + _fn + _tp
_pos = _fn + _tp
ok("W9 matrix totals 10,000", _tot == 10000, str(_tot))
ok("W9 positives == 344", _pos == 344, str(_pos))
ok("W9 base rate == 3.44 in 100", abs(_pos / _tot * 100 - 3.44) < 0.005)
ok("W9 accuracy == 0.965", abs((_tn + _tp) / _tot - 0.9654) < 5e-4)
ok("W9 recall == 0.099", abs(_tp / _pos - 0.0988) < 5e-4)
ok("W9 misses stated as 310 of 344", _fn == 310 and _pos == 344)
ok("W9 'nine in ten missed' is fair", 0.85 < _fn / _pos < 0.95,
   f"{_fn / _pos:.3f}")
ok("W9 majority-class accuracy (0.966) beats the model's (0.965)",
   round(_tn + _fp, 0) / _tot > (_tn + _tp) / _tot)
ok("W9 false alarms (36) far fewer than misses (310)", _fp * 5 < _fn)
# threshold move
_tn2, _fp2, _fn2, _tp2 = 9366, 290, 193, 151
ok("W9 threshold-0.2 matrix also totals 10,000",
   _tn2 + _fp2 + _fn2 + _tp2 == 10000)
ok("W9 threshold-0.2 positives still 344", _fn2 + _tp2 == 344)
ok("W9 threshold-0.2 recall == 0.439", abs(_tp2 / (_tp2 + _fn2) - 0.439) < 5e-4)
ok("W9 false alarms grow about eightfold", 7 < _fp2 / _fp < 9,
   f"{_fp2 / _fp:.1f}")

# --- W10 Q4: fold spread
_folds = [0.71, 0.68, 0.74, 0.52, 0.70]
ok("W10 fold mean == 0.67", abs(sum(_folds) / len(_folds) - 0.67) < 5e-3)
ok("W10 one fold is a clear outlier",
   min(_folds) < sorted(_folds)[1] - 0.10)

# --- W11 Q2: one-hot width.
# get_dummies DROPS the source column and adds one per distinct value, so
# width = original - 1 + nunique. The earlier version of this check asserted
# 4 + 847 == 851, an arithmetic identity that was true while the claimed
# shapes were wrong, because it never referenced the real dataset widths.
# Assert against the shapes the question itself prints instead.
for _label, _rows, _cols, _nuniq, _claimed in [
    ("W11 CML3112 batch_id", 1030, 10, 240, 249),
    ("W11 CML3113 assay_batch_id", 20000, 24, 847, 870),
    ("W11 CML3111 product_id", 10000, 14, 847, 860),
]:
    _expect = _cols - 1 + _nuniq
    ok(f"{_label}: get_dummies width == {_claimed}", _expect == _claimed,
       f"computed {_expect}")
    # and the identifier must be plausible: several rows per unit, otherwise
    # the premise that the test score improves does not hold.
    ok(f"{_label}: at least 3 rows per identifier",
       _rows / _nuniq >= 3.0, f"{_rows / _nuniq:.1f} rows per id")

# --- W11 Q4: ablation. The table must list all FIVE removals, otherwise
# "which feature earned its place least" is not answerable from it and the
# "every feature earns its place" option is untestable.
for _label, _table, _worst in [
    ("W11 concrete", {"all five": 3.9, "minus water/cement ratio": 6.8,
                      "minus curing age": 7.4, "minus total binder": 4.0,
                      "minus superplasticiser": 4.1, "minus fly ash": 4.6},
     "minus total binder"),
    ("W11 flotation", {"all five": 0.31, "minus starch dose per tonne": 0.68,
                       "minus iron feed grade": 0.74,
                       "minus amina-to-starch ratio": 0.32,
                       "minus air flow": 0.39, "minus pulp density": 0.44},
     "minus amina-to-starch ratio"),
]:
    _base = _table["all five"]
    _degr = {k: v - _base for k, v in _table.items() if k != "all five"}
    ok(f"{_label}: all five removals tabulated", len(_degr) == 5,
       f"{len(_degr)} rows")
    _least = min(_degr, key=_degr.get)
    ok(f"{_label}: least useful feature is {_worst}", _least == _worst, _least)
    _second = sorted(_degr.values())[1]
    ok(f"{_label}: the answer is not a tie",
       _second - min(_degr.values()) >= 0.01,
       f"gap {_second - min(_degr.values()):.3f}")

# recall table: higher is better, so the least useful is the smallest DROP
_rt = {"all five": 0.78, "minus mechanical power": 0.51,
       "minus temperature rise": 0.46, "minus tool wear": 0.77,
       "minus rotational speed": 0.72, "minus torque": 0.68}
_drop = {k: _rt["all five"] - v for k, v in _rt.items() if k != "all five"}
ok("W11 machines: all five removals tabulated", len(_drop) == 5,
   f"{len(_drop)} rows")
ok("W11 machines: least useful feature is tool wear",
   min(_drop, key=_drop.get) == "minus tool wear")
ok("W11 machines: tool wear drop is ~1 point",
   abs(_drop["minus tool wear"] - 0.01) < 5e-3)
ok("W11 machines: the answer is not a tie",
   sorted(_drop.values())[1] - min(_drop.values()) >= 0.01)

# --- W12 Q1: the per-fold differences must genuinely change sign, which is
# what makes "cannot be separated" the right reading rather than a slogan.
for _label, _a, _b in [
    ("W12 F1/recall", [0.78, 0.70, 0.76, 0.71, 0.75],
     [0.75, 0.73, 0.72, 0.68, 0.72]),
    ("W12 MAE", [0.28, 0.36, 0.29, 0.34, 0.28],
     [0.31, 0.33, 0.36, 0.32, 0.33]),
]:
    _d = [round(x - y, 10) for x, y in zip(_a, _b)]
    ok(f"{_label}: differences change sign across folds",
       any(x > 0 for x in _d) and any(x < 0 for x in _d), str(_d))
    ok(f"{_label}: means are the quoted 0.02 apart",
       abs(abs(sum(_a) / 5 - sum(_b) / 5) - 0.02) < 5e-4,
       f"{abs(sum(_a) / 5 - sum(_b) / 5):.4f}")

# --- W5 Q1: mask.sum() must be well below the row count, so the "every row
# qualifies" option is ruled out by the block rather than by argument.
for _label, _rows, _hits in [("W5 CML3112", 1030, 289),
                             ("W5 CML3113", 20000, 4120),
                             ("W5 CML3111", 9568, 3702)]:
    ok(f"{_label}: mask.sum() is well below the row count",
       0.05 < _hits / _rows < 0.6, f"{_hits}/{_rows}")

# ---------------------------------------------------------------------------
print("\n2. Question mix per week")
# ---------------------------------------------------------------------------
EXPECTED = {
    1: {"interpretation": 3, "diagnosis": 1, "judgement": 1},
    2: {"traceback": 1, "interpretation": 3, "judgement": 1},
}
STANDARD = {"diagnosis": 2, "traceback": 1, "interpretation": 1,
            "judgement": 1}
# Weeks 6 and 8 to 12 were redesigned on 15 October 2026 (pandas_quiz_revision.py) around short reading questions
# on the taught pandas workflow: two interpretation, one diagnosis, one traceback, one judgement.
REVISED = {"interpretation": 2, "diagnosis": 1, "traceback": 1, "judgement": 1}
for _w in (6, 8, 9, 10, 11, 12):
    EXPECTED[_w] = REVISED

for wk in sorted(QB.QUIZ):
    got = Counter(q["kind"] for q in QB.QUIZ[wk]["q"])
    want = EXPECTED.get(wk, STANDARD)
    ok(f"Week {wk} mix is {dict(want)}", dict(got) == want, str(dict(got)))

# ---------------------------------------------------------------------------
print("\n3. House style")
# ---------------------------------------------------------------------------
# The banned antithesis: "..., not ..." used as a rhetorical construction.
ANTITHESIS = re.compile(r",\s+not\s+(a|an|the|its|his|her|their|because|"
                        r"about|by|from|in|on|to|with|what|how|why)\b", re.I)
EMDASH_ASIDE = re.compile(r"\s—\s")

style_hits = []
for wk in sorted(QB.QUIZ):
    for i, q in enumerate(QB.QUIZ[wk]["q"], 1):
        blobs = [("stem", QB.stem_for(q, c)) for c in QB.CODES]
        for c in QB.CODES:
            for oi, (text, _, fb) in enumerate(QB.options_for(q, c), 1):
                blobs.append((f"opt{oi} text", text))
                blobs.append((f"opt{oi} feedback", fb))
        for where, text in blobs:
            if ANTITHESIS.search(text or ""):
                style_hits.append(f"W{wk}Q{i} {where}: "
                                  f"{ANTITHESIS.search(text).group(0)!r}")

ok("no banned 'X, not Y' antithesis anywhere", not style_hits,
   "; ".join(style_hits[:4]))

# An em dash that separates a leading option label from its explanation
# ("column_name — it IS the answer") is structural and fine. An em dash in
# the middle of a sentence in feedback is the editorial aside to avoid.
dash_hits = []
for wk in sorted(QB.QUIZ):
    for i, q in enumerate(QB.QUIZ[wk]["q"], 1):
        for c in QB.CODES:
            for oi, (_text, _, fb) in enumerate(QB.options_for(q, c), 1):
                if EMDASH_ASIDE.search(fb or ""):
                    dash_hits.append(f"W{wk}Q{i} option {oi} ({c})")
ok("no em-dash asides in feedback prose", not dash_hits,
   "; ".join(dash_hits[:4]))

# ---------------------------------------------------------------------------
print("\n4. Cohort hygiene: no cohort sees another's domain")
# ---------------------------------------------------------------------------
# Whole words only. Substring matching gives false positives that waste more
# time than they save: "ore" matches inside "before", "moisture" and "more".
LEAK = {
    "CML3112": ["flotation", "silica", "borehole", "assay", "assays",
                "winding", "gearbox", "ore", "pulp"],
    "CML3113": ["concrete", "slab", "precast", "winding", "gearbox",
                "cylinder"],
    "CML3111": ["concrete", "slab", "precast", "flotation", "silica",
                "assay", "assays", "ore", "pulp"],
}
leaks = []
for wk in sorted(QB.QUIZ):
    for i, q in enumerate(QB.QUIZ[wk]["q"], 1):
        for code in QB.CODES:
            text = (QB.stem_for(q, code) + " " + (QB.pre_for(q, code) or ""))
            for _t, _c, _fb in QB.options_for(q, code):
                text += " " + _t + " " + _fb
            low = text.lower()
            for term in LEAK[code]:
                if re.search(rf"\b{re.escape(term)}\b", low):
                    leaks.append(f"W{wk}Q{i} {code}: {term!r}")
ok("no cohort-inappropriate domain terms", not leaks, "; ".join(leaks[:6]))

# ---------------------------------------------------------------------------
print("\n5. Correct-answer position as a STUDENT sees it")
# ---------------------------------------------------------------------------
# The banks are authored correct-answer-first because that is far easier to
# review. Position in the source is therefore meaningless, and the thing
# worth testing is the order that actually reaches a student, which
# build_quiz_forms_gs.py produces by shuffling with a per-cohort seed.
import build_quiz_forms_gs as GS                      # noqa: E402

payload = GS.build_payload()
pos = Counter()
for code, cohort in payload.items():
    for wkentry in cohort["weeks"]:
        for q in wkentry["questions"]:
            idx = [i for i, ch in enumerate(q["choices"]) if ch["correct"]]
            ok_one = len(idx) == 1
            if not ok_one:
                FAILED.append(f"{code} week {wkentry['week']} has "
                              f"{len(idx)} correct options")
            pos[idx[0]] += 1
total = sum(pos.values())
worst = max(pos.values()) / total
print(f"     shuffled positions: {dict(sorted(pos.items()))} of {total}")
ok("shuffled correct answer is spread across all four slots",
   len(pos) == 4 and worst < 0.40, f"{worst:.0%} in one slot")
ok("every shuffled question still has exactly one correct option",
   total == sum(pos.values()))

# ---------------------------------------------------------------------------
print("\n6. Every question shows something to read")
# ---------------------------------------------------------------------------
missing_pre = []
for wk in sorted(QB.QUIZ):
    for i, q in enumerate(QB.QUIZ[wk]["q"], 1):
        # Judgement questions pose a situation in prose by design. Week 1 is
        # also exempt for its interpretation questions: the class has not
        # written a line of code, so a scenario in prose is the only fair
        # form. From Week 2 onwards there is always something to show.
        kinds = ("diagnosis", "traceback")
        if wk >= 2:
            kinds += ("interpretation",)
        if q["kind"] in kinds:
            for code in QB.CODES:
                if not (QB.pre_for(q, code) or "").strip():
                    missing_pre.append(f"W{wk}Q{i} {q['kind']} {code}")
ok("every non-judgement question has a snippet or table to read",
   not missing_pre, "; ".join(sorted(set(missing_pre))[:6]))

# The correct option should not be padded relative to the distractors: on a
# printed paper the longest option is a free clue.
#
# Both conditions are needed. A pure ratio test flags Week 3's "investigate
# cooling" against "trip", "alarm" and "normal", where the gap is the domain
# vocabulary rather than padding and cannot be written away. The absolute
# floor restricts this to prose options, which is where padding happens.
LEN_FLOOR = 90
LEN_RATIO = 2.2
length_cues = []
for wk in sorted(QB.QUIZ):
    for i, q in enumerate(QB.QUIZ[wk]["q"], 1):
        for code in QB.CODES:
            opts = QB.options_for(q, code)
            right = [t for t, c, _ in opts if c][0]
            wrong = [len(t) for t, c, _ in opts if not c]
            mean_wrong = sum(wrong) / len(wrong)
            if len(right) > LEN_FLOOR and len(right) > LEN_RATIO * mean_wrong:
                length_cues.append(
                    f"W{wk}Q{i} {code} ({len(right)} vs mean "
                    f"{mean_wrong:.0f})")
ok(f"no prose key over {LEN_FLOOR} chars and {LEN_RATIO}x the distractors",
   not length_cues, "; ".join(sorted(set(length_cues))[:8]))

# ---------------------------------------------------------------------------
print("\n7. The incorrect-answer message must state the answer")
# ---------------------------------------------------------------------------
# Forms has one feedback message per question rather than per option, so a
# student who gets it wrong reads a single block. The first live test showed
# that block listing three refutations without ever naming the right answer,
# which is the one thing they needed. It must lead with it.
lead_bad, key_bad, stale = [], [], []
for code, cohort in payload.items():
    for wkentry in cohort["weeks"]:
        for q in wkentry["questions"]:
            fb = q["fbWrong"]
            key = [c["text"] for c in q["choices"] if c["correct"]][0]
            where = f"{code} W{wkentry['week']}Q{q['n']}"
            if not fb.startswith("THE ANSWER: "):
                lead_bad.append(where)
            if key not in fb:
                key_bad.append(where)
            first = fb.split("\n")[0]
            if "Correct." in first or "Correct," in first:
                stale.append(where)

ok("every wrong-answer message leads with the answer", not lead_bad,
   "; ".join(lead_bad[:5]))
ok("every wrong-answer message quotes the correct option text", not key_bad,
   "; ".join(key_bad[:5]))
ok("no leftover 'Correct.' inside a wrong-answer message", not stale,
   "; ".join(stale[:5]))

intro_bad = [f"{code} W{w['week']}" for code, c in payload.items()
             for w in c["weeks"] if w["week"] != 6 and "tap View score" not in w["intro"]]  # Quiz 6 is waived
ok("every form tells students to tap View score", not intro_bad,
   "; ".join(intro_bad[:5]))


# --- W13 (Quiz 12): the two tables are the Week 13 deck's reference numbers, and the scaling example is computed.
import numpy as _np
import week_reference_numpy as _R
for _code in ("CML3112", "CML3113", "CML3111"):
    _b = _R.bundle13(_code); _q = QB.QUIZ[13]["q"]
    _t1 = QB.pre_for(_q[0], _code); _t2 = QB.pre_for(_q[1], _code)
    for _r in _b["ridge_rows"]:
        ok(f"W13 {_code} ridge row {_r['name']} printed", f"{_r['train']:7.2f}  {_r['valid']:7.2f}" in _t1, _t1)
    _rr = _b["ridge_rows"]
    ok(f"W13 {_code} alpha 100 is worst on train and on validation",
       _rr[2]["train"] > max(_rr[0]["train"], _rr[1]["train"]) and _rr[2]["valid"] > max(_rr[0]["valid"], _rr[1]["valid"]))
    for _r in _b["knn"]:
        ok(f"W13 {_code} k={_r['k']} printed", f"{_r['valid']:8.2f}" in _t2, _t2)
    _kv = {r["k"]: r["valid"] for r in _b["knn"]}
    ok(f"W13 {_code} k=3 is the lowest and the others are far apart",
       _kv[3] < _kv[1] < _kv[20] and _kv[1] / _kv[3] > 1.4)
_qq, _A, _B, _sd = _np.array([60, 30.]), _np.array([63, 36.]), _np.array([67, 30.]), _np.array([25, 3.])
_raw = (_np.linalg.norm(_qq - _A), _np.linalg.norm(_qq - _B)); _sc = (_np.linalg.norm((_qq - _A) / _sd), _np.linalg.norm((_qq - _B) / _sd))
ok("W13 scaling example: raw says A (6.7 v 7.0)", round(_raw[0], 1) == 6.7 and round(_raw[1], 1) == 7.0 and _raw[0] < _raw[1], str(_raw))
ok("W13 scaling example: scaled says B (2.0 v 0.3)", round(_sc[0], 1) == 2.0 and round(_sc[1], 1) == 0.3 and _sc[1] < _sc[0], str(_sc))

print()
if FAILED:
    print(f"  {len(FAILED)} FAILED")
    for f in FAILED:
        print(f"    - {f}")
    sys.exit(1)
print("  all checks passed")
