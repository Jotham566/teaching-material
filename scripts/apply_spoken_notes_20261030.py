"""Apply the spoken-script notes (data/spoken_notes_w8_12_20261030.json) to the Week 8 to 12 decks.

Each key is "<slide title>||<n>" (n counts repeated titles from 0). {short} and {unit} are replaced with the
cohort's target name and unit. Run after patch_weeks8b_12_20261030.py.
Usage: python3 scripts/apply_spoken_notes_20261030.py [--dir DECKS_DIR]
"""
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx import Presentation
import week_reference_numpy as R
from patch_weeks8b_12_20261030 import deck_name, first_title, DECKS, p8

_A = json.loads((p8.ROOT / "data" / "spoken_notes_w8_12_20261030.json").read_text())
_B = json.loads((p8.ROOT / "data" / "spoken_notes_w1_7_13_15_20261030.json").read_text())
norm = lambda k: k.replace(" \u2014 ", ": ")
SCRIPTS = {w: {norm(k): ({"all": v} if isinstance(v, str) else v) for k, v in d.items()} for w, d in {**_A, **_B}.items()}
# slides whose notes are written by the build, not from this file
KEEP_BUILD_NOTES = {"Today\u2019s learning||0"}


def apply(path, code, week):
    prs = Presentation(str(path)); c = R.COHORT[code]; seen = {}; applied = missing = 0
    scripts = SCRIPTS[str(week)]; used = set()
    for s in prs.slides:
        t = first_title(s); nth = seen.get(t, 0); seen[t] = nth + 1
        key = norm(f"{t}||{nth}")
        if week in (9, 10, 11, 12, 13) and key in KEEP_BUILD_NOTES: used.add(key); continue
        if key in scripts:
            entry = scripts[key]; text = entry.get(code, entry.get("all"))
            if text is None: continue
            text = text.replace("{short}", c["short"]).replace("{unit}", c["unit"])
            assert "{" not in text, f"unfilled placeholder in {key}"
            s.notes_slide.notes_text_frame.text = text; applied += 1; used.add(key)
    retired = lambda k: week >= 8 and (k.endswith(" submission||0") or k.endswith("quiz||0") or k.startswith("Preparing for the assignment"))
    unused = {k for k, e in scripts.items() if (code in e or "all" in e) and not retired(k)} - used
    prs.save(str(path))
    return applied, sorted(unused)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=None); ap.add_argument("--weeks", nargs="*", type=int, default=list(range(1, 16))); a = ap.parse_args()
    d = Path(a.dir) if a.dir else DECKS
    for week in a.weeks:
        for code in R.COHORT:
            n, unused = apply(d / deck_name(code, week), code, week)
            print(f"{code} W{week}: {n} scripts applied" + (f"; UNUSED KEYS {unused}" if unused else ""))


if __name__ == "__main__":
    main()
