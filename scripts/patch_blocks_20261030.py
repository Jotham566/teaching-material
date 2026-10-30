"""Block assessment arrangement in the decks (data/assessment_blocks_20261030.json).
From Week 8 the weekly assignment and weekly quiz become one assignment pack and one quiz sitting per block of three
classes. This script rewrites the Week 1 assessment slide and the Week 8 to 13 assessment slides, with spoken notes.
Run after patch_weeks8b_12_20261030.py and before apply_spoken_notes_20261030.py. Idempotent.
Usage: python3 scripts/patch_blocks_20261030.py [--dir DIR]"""
import argparse, json, sys, io
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx import Presentation
from pptx.util import Pt
from deckkit_20261030 import *
import week_reference_numpy as R
from patch_weeks8b_12_20261030 import deck_name, first_title, DECKS, p8

ROOT = p8.ROOT
POL = json.loads((ROOT / "data" / "assessment_blocks_20261030.json").read_text())
SUB = json.loads((ROOT / "data" / "submission_links.json").read_text())
QZ = json.loads((ROOT / "data" / "quiz_links.json").read_text())
BLOCK_OF_WEEK = {w: b for b in POL["blocks"] for w in b["weeks"]}
TASKS = {8: "predict_regression and regression_errors", 9: "classification_metrics", 10: "group_split and predict_regression",
         11: "make_features and ablation_metrics", 12: "select_model and regression_errors"}
MARK = "BLOCK-PATCHED"


def when(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B %Y')}, {d.strftime('%H:%M')} Kampala time"


def spoken_when(iso):
    d = datetime.fromisoformat(iso); h = d.strftime("%H:%M")
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')} at {h} Kampala time"


def link_slide(prs, kicker, title, rows, foot, notes, label):
    """rows: list of (label, url_text, url). Each row shows a label and a hyperlink."""
    s = new_slide(prs); header(s, kicker, title)
    y = 132; step = min(88, 280 / max(len(rows), 1))
    for i, (lab, linktext, url) in enumerate(rows):
        textbox(s, f"{i + 1:02d}", 46, y, 60, 40, 30, ORANGE, True)
        textbox(s, lab, 112, y + 2, 800, 30, 21, INK, True)
        tb = s.shapes.add_textbox(Pt(112), Pt(y + 34), Pt(800), Pt(30)); p = tb.text_frame.paragraphs[0]; r = p.add_run()
        r.text = linktext; r.font.size = Pt(19); r.font.name = "Calibri"; r.font.underline = True; r.font.color.rgb = rgb(TEAL); r.hyperlink.address = url
        y += step
    shape_rect(s, 0, 430, 960, 74, PALE2)
    textbox(s, foot, 46, 438, 870, 62, 18, TEAL, True)
    footer(s, label); set_notes(s, notes); return s


def exists(prs, title): return find_slide(prs, title) is not None


def set_kicker(slide, text):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip().isupper() and sh.top < Pt(60):
            r = sh.text_frame.paragraphs[0].runs; r[0].text = text
            for x in r[1:]: x.text = ""
            return True
    return False


def patch_week(code, week, prs):
    b = BLOCK_OF_WEEK[week]; lab = lambda: f"{code}   Week {week}   0"
    close = b["assignment_closes"][code]; dl, dls = when(close), spoken_when(close)
    letters = {p["id"]: p["part"] for p in b["assignment_parts"]}; part = letters.get(f"W{week:02d}")
    w1, w2, w3 = b["weeks"]; weeks_txt = f"Weeks {w1}, {w2} and {w3}"; marks = b["assignment_marks"]
    n_parts = len(b["assignment_parts"])
    # --- task slides get a block kicker
    started = False
    for sl in list(prs.slides):
        t = first_title(sl)
        if t == "Your issued task": started = True
        if started and part:
            set_kicker(sl, f"{b['label'].upper()}, PART {part}")
        if t == "Written evidence": started = False
    anchor = find_slide(prs, "Your issued task")
    # --- the introduction or part slide
    if week == 13:
        new = None
    elif week in (8, 11):
        rest = ("Week 13 has no graded notebook. It is assessed in the Block 2 quiz and in your project." if week == 11 else "Part B follows in Week 9 and part C in Week 10.")
        body = [(f"Today's tasks are part {part} of the {b['label']} pack, worth 20 of its {marks} marks. {rest}", False),
                (f"Nothing is submitted and there is no quiz after today's class. You hand in all {n_parts} parts together by {dl}.", False),
                (f"The {b['label']} quiz has 15 questions, five from each of the three weeks. You sit it after the Week {w3} class.", False)]
        new = statement_slide(prs, "ASSESSMENT", f"{b['label']}: how {weeks_txt} are assessed", "One assignment pack and one quiz for every three classes.", body,
            spoken(f"From this week the weekly assignment and the weekly quiz stop. We now assess in blocks of three classes. {b['label']} covers {weeks_txt}: {b['topics']}.",
                   f"Today's tasks are part {part} of the {b['label']} assignment pack. It is worth 20 of the pack's {marks} marks. " + ("The next part arrives in Week 12. Week 13 has no graded notebook, so its content is assessed in the Block 2 quiz and in your project." if week == 11 else "Part B arrives next week and part C the week after."),
                   f"Nothing is submitted after today's class, and there is no quiz. We hand in all {n_parts} parts together by {dls}. The {b['label']} quiz has fifteen questions, five from each week. It opens after the Week {w3} class.",
                   "Weeks 1 to 6 stay as they were. The two lowest weekly scores are dropped, and the block marks count in full, so the blocks carry about 60 percent of the quiz and assignment marks."), lab())
    else:
        extra = ("This is the last part. The pack closes " + dl + ". Part A and part B are the earlier weeks' notebooks." if week == 10 else f"The pack closes {dl}.")
        body = [(f"Today's tasks are part {part} of the {b['label']} pack, worth 20 of its {marks} marks. They use {TASKS[week]}.", False),
                (extra if week in (10, 12) else f"Part {'C' if week == 9 else 'B'} follows next week. All parts are handed in together by {dl}.", False),
                (f"There is no quiz after today's class. The {b['label']} quiz comes after the Week {w3} class.", False) if week != w3 else ("The quiz opens after today's class.", False)]
        if week == 9: body[2] = (f"There is no quiz after today's class. The Block 1 quiz comes after the Week 10 class.", False)
        new = statement_slide(prs, "ASSESSMENT", f"{b['label']}, part {part}: this week's tasks", f"Part {part} of {n_parts}. 20 marks.", body,
            spoken(f"This week's tasks are part {part} of the {b['label']} assignment pack, worth twenty marks. They are built around {TASKS[week]}.",
                   (f"This is the last part, so the whole pack is due by {dls}. In a moment we show where each part is submitted." if week in (10, 12) else f"The earlier part is already in your folder, and the next part comes next week. All parts are handed in together by {dls}."),
                   (f"There is no quiz today. The {b['label']} quiz opens after the Week {w3} class." if week != w3 else f"The {b['label']} quiz opens after today's class.")), lab())
    if new is not None: move_slide(prs, new, anchor)
    # --- the old weekly submission and quiz slides
    titles = [first_title(s) for s in prs.slides]
    sub_t = [t for t in titles if t.endswith(" submission") and "Revision" not in t and "Data analysis" not in t]
    quiz_t = f"Week {week} quiz"
    exit_anchor = find_slide(prs, "Revision and submission checklist")
    links = lambda wk: SUB[f"{code}|W{wk:02d}"]["url"]
    if week in (10, 12):
        rows = [(f"Part {p['part']}: {p['title']} ({p['label']}, Week {int(p['id'][1:])})", f"Open the {p['label']} form", links(int(p['id'][1:]))) for p in b["assignment_parts"]]
        pack = link_slide(prs, "ASSIGNMENT SUBMISSION", f"Submit the {b['label']} assignment pack", rows,
            f"Closes {dl}. Submit each notebook to its own form, with your full Student Registration Number.",
            spoken(f"This slide is where the {b['label']} assignment pack goes in. It has {n_parts} parts, one notebook for each, and each part has its own form.",
                   f"Open the form for each part in turn, enter your full Student Registration Number, and upload that part's notebook. Do not wait for the last minute, because the pack closes {dls}, and all parts close together.",
                   "A part that is not submitted scores zero for that part. The block marks are never dropped, so each part counts."), lab())
        move_slide(prs, pack, exit_anchor)
    if week in (10, 13):
        rows = [(f"Week {wk} form ({'5 questions'})", f"Open the Week {wk} quiz form", QZ[f"{code}|{wk}"]) for wk in b["weeks"]]
        qs = link_slide(prs, "QUIZ ACCESS", f"{b['label']} quiz: three forms, 15 questions", rows,
            "Opens after today's class. Each form stays open for 24 hours. Use your Student Registration Number and registered account.",
            spoken(f"The {b['label']} quiz is three short forms, one for each week of the block, with five questions each. Together they are fifteen questions and fifteen marks.",
                   "The forms open after today's class, when the lecturer activates them, and each stays open for twenty-four hours. Open them one after the other and answer individually, using your Student Registration Number and your registered account.",
                   f"This quiz replaces the three weekly quizzes of {weeks_txt}. Like the assignment pack, it counts in full and is not dropped."), lab())
        move_slide(prs, qs, exit_anchor)
    for t in sub_t + [quiz_t]:
        s = find_slide(prs, t)
        if s is not None and (t != quiz_t or True):
            delete_slide(prs, s)
    # --- Week 13 wrap slide replaces the old 'Preparing for the assignment'
    if week == 13:
        old = find_slide(prs, "Preparing for the assignment")
        wrap = statement_slide(prs, "ASSESSMENT", "Block 2 closes after today", "No new weekly assignment.",
            [(f"The Block 2 pack, A10 and A11 for 40 marks, is due {dl}.", False),
             ("The Block 2 quiz covers Weeks 11, 12 and 13. It opens after today's class.", False),
             ("Next week is Practical Test 2. Rehearse saving and submitting your test notebook, and revise the published function interfaces.", False)],
            spoken("There is no new assignment this week. Block 2 closes with two things.",
                   f"The first is the Block 2 assignment pack, which is part A from Week 11 and part B from Week 12, forty marks in all, due {dls}. The second is the Block 2 quiz, fifteen questions across Weeks 11, 12 and 13, which opens after today's class.",
                   "Next week is Practical Test 2. Rehearse saving your test notebook and submitting it, and revise the function interfaces. An interface is the function name, its inputs and what it returns, and the test expects them exactly as published."), lab())
        move_slide(prs, wrap, old); delete_slide(prs, old)
    # --- exit slide wording
    ex = find_slide(prs, "Revision and submission checklist")
    if ex is not None and week != 13:
        replace_text(ex, "before submitting the required assignment notebook.", f"before you hand in your {b['label']} notebooks.")


def patch_week1(code, prs):
    img = ROOT / "figs" / "week8b_12_20261030" / "assessment_blocks.png"
    s8 = find_slide(prs, "How you are assessed")
    for sh in s8.shapes:
        if sh.shape_type == 13 and img.exists():
            rid = sh._element.blipFill.blip.rEmbed; s8.part.related_part(rid)._blob = img.read_bytes()
    s = statement_slide(prs, "ASSESSMENT", "Quizzes and assignments from Week 8", "Weekly in Weeks 1 to 6. Every three classes from Week 8.",
        [("Weeks 1 to 5: a quiz and an assignment each week, and the best 3 of the 5 count. Week 6 is waived.", False),
         ("Block 1 is Weeks 8 to 10 and Block 2 is Weeks 11 to 13. Each block has one assignment pack and one quiz.", False),
         ("A block counts in full and cannot be dropped. Together the two blocks carry about 60 percent of the quiz and assignment marks.", False)],
        spoken("Here is how the quizzes and assignments work over the whole semester. In Weeks 1 to 6 you have a short quiz and an assignment each week, and your best four of the six count, so two weak weeks do not hurt you.",
               "From Week 8 we assess every three classes. Block 1 covers Weeks 8 to 10 and Block 2 covers Weeks 11 to 13. Each block has one assignment pack and one quiz, and each is handed in or sat after the third class of the block.",
               "A block counts in full and cannot be dropped, because it holds three weeks of learning. Together the two blocks carry about sixty percent of the quiz and assignment marks. The two practical tests, the projects and the demonstration are unchanged."), f"{code}   Week 1   0")
    move_slide(prs, s, next(sl for i, sl in enumerate(prs.slides, 1) if i == 9))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=None); a = ap.parse_args(); d = Path(a.dir) if a.dir else DECKS
    for code in R.COHORT:
        for week in (1, 8, 9, 10, 11, 12, 13):
            path = d / deck_name(code, week); prs = Presentation(str(path))
            if prs.core_properties.keywords == MARK: print(f"{code} W{week}: already patched"); continue
            (patch_week1(code, prs) if week == 1 else patch_week(code, week, prs))
            prs.core_properties.keywords = MARK
            finalize(prs, code, week, path); print(f"{code} W{week}: {len(prs.slides)} slides")


if __name__ == "__main__":
    main()
