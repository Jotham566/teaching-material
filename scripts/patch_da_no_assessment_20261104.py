# -*- coding: utf-8 -*-
"""Remove assessment wording from the fifteen Data Analysis decks in place.

Why a patch and not build_da_decks.py: the decks on disk carry later
speaker-note layers (lecturer cues, checks, recovery notes) that
build_da_decks.py does not regenerate, so a clean rebuild would lose them.
This script applies the same wording changes as the sources (da_content.py,
da_deck_w2/w3/w5.py, build_da_decks.py) to the decks themselves.

Lecturer decision 4 Nov 2026: no exam, marks, grades, weights or graded
work. Run once from the repo root; running it again changes nothing.
"""
import glob
import os
import re
import sys
from pptx import Presentation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = os.path.join(ROOT, "DataAnalysis_Track", "decks")

PAIRS = [  # (regex or literal, replacement); applied in order
    ("CHECKPOINT 1 · 15% OF THE MARK", "PROJECT 1 · THE SQL REVENUE REPORT"),
    ("CHECKPOINT 2 · 15% OF THE MARK", "PROJECT 2 · CLEANED DATA AND LOG"),
    ("This is Checkpoint 1 and it is marked against the answer key tonight.",
     "This is Project 1. Check it against the answer sheet tonight and keep it."),
    ("Put your judgement in a SQL comment for class discussion. The automatic mark checks the query: 25 points each for grain, gross, returned and net amounts.",
     "Put your judgement in a SQL comment for class discussion."),
    ("Submit one .sql file. Amounts allow 1 UGX rounding tolerance; extra or missing rows reduce credit.",
     "Check your grain, gross, returned and net amounts against the answer sheet. Keep the .sql file. Nothing is marked."),
    ("Checkpoint 1", "Project 1"), ("Checkpoint 2", "Project 2"),
    ("What to hand in", "What to keep"),
    ("one is the deliverable, and it is marked.", "one is part of what you keep."),
    ("That is the pass mark.", "That is what a good result looks like."),
    ("The log is marked as heavily as the number.", "The log matters as much as the number."),
    ("Restart and Run All before you submit.", "Restart and Run All before you keep it."),
    ("How it is marked", "What good looks like"),
    ("explaining it scores higher than a clean match", "explaining it is a better result than a clean match"),
    ("Submit with the cleaning log from last session.", "Keep it with the cleaning log from last session."),
    ("and finding one is a pass.", "and finding one is a good result."),
    ("and the marking reflects that.", "and so will the people who read your write-up."),
    ("THE SECTOR ASSESSMENT", "PROJECT 4 · THE INVESTIGATION"),
    ("The capstone is worth more to you", "The final project is worth more to you"),
    (re.compile(r"This is the sector assessment, worth 30%\..*?not on the code\.", re.S),
     "This is Project 4, the investigation write-up. Six questions in order, then five findings. Peers read the findings and the limitations beside them and say which they would act on. Nothing is marked."),
    ("Finish and submit the investigation:", "Finish the investigation to show a neighbour:"),
    ("which is where the marks are", "which is where the value is"),
    ("CAPSTONE · 40% OF THE MARK", "FINAL PROJECT · PEER FEEDBACK"),
    ("And what is marked", "And what you get back"),
    ("What you hand in, and what you say", "What you show, and what you say"),
    ("Upload PPTX with narration notes and numerical evidence.",
     "Show the final project: the investigation and the dashboard, with narration in the speaker notes."),
    ("Add a DOCX/PDF appendix if needed. Keep PBIX as supporting material.",
     "Keep the PBIX and the notebook. They are yours."),
    ("Marks reward a supported decision and the required evidence.",
     "Peers say what they would act on and what they doubt. There are no marks."),
    (re.compile(r"Every learner submits a five-minute narrated presentation with the capstone for rubric assessment; selected live demonstrations provide discussion, not extra marks\."),
     "Every learner shows the final project (investigation and dashboard) in a five-minute presentation, with narration in the speaker notes. Peers give feedback; there are no marks."),
    ("40 selected demonstrations and 20 application planning", "40 for showing selected final projects with peer feedback and 20 application planning"),
    ("Submit a five-minute narrated presentation. Selected live demonstrations take 40 minutes, followed by 20 minutes on applying the work.",
     "Then prepare a five-minute presentation of the final project. Selected projects are shown for 40 minutes with peer feedback, followed by 20 minutes on applying the work."),
    ("Selected demonstrations follow; keep your submitted slides ready.",
     "Selected final projects are shown next; keep your slides ready."),
    ("Every learner submits the same presentation evidence for grading. Selected live demonstrations carry no extra marks.",
     "Everybody prepares the same five-minute presentation of the final project. Nothing is marked; peers give feedback on what they would act on and what they doubt."),
    ("DEMONSTRATIONS · 40 MINUTES", "FINAL PROJECTS · 40 MINUTES"),
    ("Eight short demonstrations", "Eight final projects, with peer feedback"),
    (re.compile(r"name one limitation\.(?! Peers say)"), "name one limitation. Peers say what they would act on."),
    ("It is a capstone candidate.", "It is a final project candidate."),
    ("they are capstone candidates.", "they are final project candidates."),
    ("These three are what tonight is marked against, in the sense that the lab checks them.",
     "These three are what tonight's lab practises, and the check and answers slide lets you test yourself on them."),
    ("Outside an assessment restriction, restart", "Restart"),
    ("That is a smaller claim than a certificate implies and a bigger one than it sounds. Most organisations",
     "The certificate of completion from KLAi Professional Learning says you finished the course and its project. This is the skill behind it, and most organisations"),
    ("Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.",
     "Does saving to GitHub mean someone else can run your project? Only if the README says how to run it."),
]
DROP_HEADS = {"ASSIGNMENT HANDOVER", "CAPSTONE FILES"}
changed = {"pairs": 0, "blocks": 0}


def fix_par(par):
    text = "".join(r.text for r in par.runs)
    if not text:
        return
    new = text
    for old, rep in PAIRS:
        if isinstance(old, str):
            new = new.replace(old, rep)
        else:
            new = old.sub(rep, new)
    if new == text:
        return
    changed["pairs"] += 1
    # keep the first run's formatting; the changed paragraphs are uniform
    par.runs[0].text = new
    for r in par.runs[1:]:
        r.text = ""


def frames(shape):
    if shape.has_text_frame:
        yield shape.text_frame
    if getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            for c in row.cells:
                yield c.text_frame
    if shape.shape_type == 6:
        for s in shape.shapes:
            yield from frames(s)


def drop_blocks(tf):
    pars = list(tf.paragraphs)
    i = 0
    while i < len(pars):
        if pars[i].text.strip() in DROP_HEADS:
            j = i
            while j < len(pars) and pars[j].text.strip() != "":
                j += 1
            for k in range(i, min(j + 1, len(pars))):
                el = pars[k]._p
                el.getparent().remove(el)
            changed["blocks"] += 1
            pars = list(tf.paragraphs)
            continue
        i += 1


for f in sorted(glob.glob(os.path.join(DECKS, "DA_S*.pptx"))):
    prs = Presentation(f)
    for s in prs.slides:
        for sh in s.shapes:
            for tf in frames(sh):
                for p in tf.paragraphs:
                    fix_par(p)
        if s.has_notes_slide:
            tf = s.notes_slide.notes_text_frame
            drop_blocks(tf)
            for p in tf.paragraphs:
                fix_par(p)
    prs.save(f)
print("paragraphs changed: %(pairs)d, note blocks removed: %(blocks)d" % changed)

# ---- the readable lecturer companions in decks/lecturer_notes/*.md
MD = sorted(glob.glob(os.path.join(DECKS, "lecturer_notes", "DA_S*.md")))
md_changed = 0
for f in MD:
    txt = open(f, encoding="utf-8").read()
    lines = txt.split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip() in DROP_HEADS:
            while i < len(lines) and lines[i].strip() != "":
                i += 1
            i += 1                       # the blank line after the block
            continue
        out.append(lines[i])
        i += 1
    new = "\n".join(out)
    for old, rep in PAIRS:
        new = old.replace if False else new
        new = (new.replace(old, rep) if isinstance(old, str)
               else old.sub(rep, new))
    if new != txt:
        open(f, "w", encoding="utf-8").write(new)
        md_changed += 1
print("lecturer companion files changed: %d of %d" % (md_changed, len(MD)))
