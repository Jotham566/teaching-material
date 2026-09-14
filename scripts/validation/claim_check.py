# -*- coding: utf-8 -*-
"""Check spelled-out counts in slide titles against what the slide contains.

A title that says "fourteen lines" and a code block with thirteen is the kind
of error nobody notices until a student counts them out loud in class.
"""
import glob
import re

from pptx import Presentation
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
       "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
       "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
       "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20}
WORDS = "|".join(NUM)
PAT = re.compile(rf"\b({WORDS})\s+(lines?|steps?|questions?|charts?|"
                 rf"rules?|features?|columns?|numbers?|checks?|models?)\b", re.I)

bad = 0
checked = 0
for f in sorted(glob.glob(_ROOT + "/"
                          "IUEA_Teaching_Plan/decks/CML*.pptx")):
    code = f.split("/")[-1].split("_")[0]
    wk = int(re.search(r"Week(\d+)", f).group(1))
    prs = Presentation(f)
    for i, s in enumerate(prs.slides, 1):
        title, mono, bullets = "", None, 0
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            t = sh.text_frame.text
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            is_mono = any(r.font.name == "Courier New" for r in runs)
            big = any(r.font.size and r.font.size.pt >= 26 for r in runs)
            if big and not title:
                title = t
            if is_mono and t.count("\n") > 2:
                mono = t
            if 0 < len(t) < 400 and not big and not is_mono:
                bullets += 1
        m = PAT.search(title)
        if not m or mono is None:
            continue
        checked += 1
        claim, noun = NUM[m.group(1).lower()], m.group(2).lower()
        if noun.startswith("line"):
            actual = len([l for l in mono.split("\n") if l.strip()])
            if actual != claim:
                bad += 1
                print(f"  MISMATCH {code} W{wk:02d} sl{i}: title claims {claim} "
                      f"{noun}, code block has {actual}   {title[:44]!r}")
print(f"checked {checked} numeric title claims against slide content; "
      f"mismatches: {bad}")
