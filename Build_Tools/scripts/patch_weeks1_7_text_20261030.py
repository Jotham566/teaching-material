"""Small text repairs found by review in the Week 1 to 7 decks (notes are applied by apply_spoken_notes_20261030.py).
Usage: python3 scripts/patch_weeks1_7_text_20261030.py   (idempotent; originals are in decks/_backup_2026-10-30)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx import Presentation
from deckkit_20261030 import replace_text
from patch_weeks8b_12_20261030 import DECKS, deck_name
import week_reference_numpy as R

FIXES = {
    4: [("import loads a library. from selects a tool from it.", "with open(...) as source opens the file. as gives the open file the name source.")],
    6: [("Store three summary values for crusher energy demand in target_summary.", "Store three summary values for the target in target_summary."),
        ("Load and power demand demand", "Load and power demand")],
}


def main():
    for week, fixes in FIXES.items():
        for code in R.COHORT:
            path = DECKS / deck_name(code, week); prs = Presentation(str(path)); n = 0
            for sl in prs.slides:
                for old, new in fixes: n += replace_text(sl, old, new)
            prs.save(str(path)); print(f"{code} W{week}: {n} text repairs")


if __name__ == "__main__":
    main()
