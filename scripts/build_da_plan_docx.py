# -*- coding: utf-8 -*-
"""The Data Analysis track plan: everything an instructor needs to run it.

Content comes from da_content.py and numbers from the generated answer key,
Keep the published plan consistent with the session source and verified delivery evidence.
"""
import json
import os
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docxkit import *          # noqa
import da_content as C         # noqa: E402

TRACK = _os.path.join(_ROOT, "DataAnalysis_Track")
OUT = _os.path.join(TRACK, "DataAnalysis_Track_Plan.docx")
with open(_os.path.join(TRACK, "data", "answer_key.json"),
          encoding="utf-8") as fh:
    K = json.load(fh)

def h1_page(doc, text):
    """A part heading that starts a new page WITHOUT risking a blank one.

    An explicit page-break paragraph after a page that happens to be exactly
    full lands on the next page and pushes the heading to the one after,
    which is how page 3 of the first build came out empty. page_break_before
    on the heading itself moves the heading and nothing else.
    """
    h = h1(doc, text)
    h.paragraph_format.page_break_before = True
    return h


def tidy_page_breaks(doc):
    """Delete empty paragraphs that sit immediately before a page break.

    docxkit's callout() and table() both end with a spacer paragraph, which
    is right in the middle of a section and wrong at the end of one: the
    spacer stays on the old page, and if the old page was already full it
    starts a new page by itself. That is what left page 3 holding nothing but
    a header and a footer. Strip them and the break lands where it should.
    """
    removed = 0
    changed = True
    while changed:
        changed = False
        body = list(doc.element.body)
        for i, el in enumerate(body):
            if el.tag != qn("w:p") or i == 0:
                continue
            pPr = el.find(qn("w:pPr"))
            if pPr is None or pPr.find(qn("w:pageBreakBefore")) is None:
                continue
            prev = body[i - 1]
            if prev.tag != qn("w:p"):
                continue
            if "".join(prev.itertext()).strip() == "":
                prev.getparent().remove(prev)
                removed += 1
                changed = True
                break
    return removed


d = new_doc(margin_cm=2.0)
header_footer(d, "Data Analysis with Python, SQL and Power BI · "
                 "instructor plan")
first_page_different(d)

# ------------------------------------------------------------------ cover
spacer(d, 24)
para(d, "PROFESSIONAL TRAINING · FIVE WEEKS", size=10, bold=True, colour=MID,
     align=AL.CENTER, after=14)
para(d, C.TRACK, size=23, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, C.SUBTITLE, size=12, colour=MID, align=AL.CENTER, after=20)

callout(d, "What this track is for, and who it assumes you are",
        C.AUDIENCE + "\n\n"
        "They leave able to get their own data out of a database, clean it "
        "without destroying it, answer a question with a number attached, and "
        "put the answer in front of somebody who will look at it for thirty "
        "seconds. That is the whole scope. It is deliberately narrower than "
        "the roadmap it is built from, and section 9 says what was left out "
        "and why.\n\n"
        "THE STARTING POINT IS A SPREADSHEET. Sessions 1 and 2 contain no "
        "code at all: they are the vocabulary of data, grain, and keys, "
        "taught against the pivot tables and VLOOKUPs the room already "
        "uses. Every session after that opens with its new words defined in "
        "plain language, and the glossary handout is the union of those "
        "lists. Section 5 is that glossary.\n\n"
        "The generated Riverside data and reference calculations have automated "
        "checks. This does not establish that every teaching activity or "
        "student account has been rehearsed. The assessment readiness report "
        "separately records current calibration and complete-packet evidence.",
        MID_H, LIGHT_H)

tool_rows = [[k, str(v) + " hours",
              "{:.0f}%".format(100.0 * v / C.TOTAL_HOURS)]
             for k, v in C.TOOL_HOURS.items()]
spacer(d, 8)
table(d, ["Where the forty-five hours go", "Hours", "Share"],
      tool_rows, [56, 22, 22], font=9.5, hdr_font=9.5)

spacer(d, 10)
para(d, "Python underpins 24 of the 45 hours, including statistics, charts and "
        "the investigation. Foundations take 6 hours, SQL 9 and Power BI 6. "
        "The timetable and tool totals are checked against the fifteen-session source.",
     size=9.5, colour=MID)

# ------------------------------------------------------------------ part 1
h1_page(d, "1 · The shape of the five weeks")

para(d, "Fifteen sessions of three hours, three a week. Week 1 introduces "
        "data, tables and the first SQL query. Week 2 develops SQL joins and "
        "introduces Python. Week 3 reads, cleans and reconciles files in pandas. "
        "Week 4 develops statistical descriptions and charts. Week 5 completes "
        "the investigation, Power BI model and capstone presentation.")

wk_titles = {1: "Week 1 — data foundations and first SQL",
             2: "Week 2 — SQL joins and first Python",
             3: "Week 3 — pandas, cleaning and reconciliation",
             4: "Week 4 — statistics and charts",
             5: "Week 5 — investigation, Power BI and presentation"}
rows = []
for w in range(1, C.WEEKS + 1):
    ss = [s for s in C.SESSIONS if s["week"] == w]
    rows.append([wk_titles[w],
                 "\n".join("{}. {} ({})".format(s["n"], s["title"], s["tool"])
                           for s in ss)])
table(d, ["Week", "Sessions"], rows, [30, 70], font=9, hdr_font=9)

spacer(d, 10)
h2(d, "The three-hour block")
para(d, "The same shape every session, so nobody has to wonder what happens "
        "next. These are people who have already worked a full day, and the "
        "breaks are load-bearing.")
table(d, ["Minutes", "What", "Why"],
      [[str(m), t, w] for m, t, w in C.BLOCK], [12, 30, 58],
      font=8.8, hdr_font=8.8)

para(d, "Demonstrate short examples live, including how to read an error and "
        "recover. Keep the prepared notebook as a fallback so debugging does "
        "not consume the practical period.", size=9, after=4)

# ------------------------------------------------------------------ part 2
h1_page(d, "2 · The fifteen sessions")

for s in C.SESSIONS:
    heading = h2(d, "Session {} · {}".format(s["n"], s["title"]))
    if s["n"] > 1: heading.paragraph_format.page_break_before = True
    para(d, "Week {} · {} · roadmap.sh: {}".format(
        s["week"], s["tool"], s["roadmap"]), size=9, bold=True, colour=MID,
        after=6)

    if s.get("vocab"):
        para(d, "New words, defined before they are used:", size=9.5,
             bold=True, after=3)
        table(d, ["Term", "What it means", "In a spreadsheet"],
              [[t, dfn, (xl or "no direct equivalent")]
               for t, dfn, xl in s["vocab"]],
              [18, 54, 28], font=8.2, hdr_font=8.2)
        spacer(d, 6)

    para(d, "By the end they can:", size=9.5, bold=True, after=3)
    for o in s["outcomes"]:
        para(d, "— " + o, size=9.5, after=2)
    spacer(d, 4)

    body = [["Teach block 1", s["b1"]],
            ["Teach block 2", s["b2"]],
            ["Practical work", s["lab"]],
            ["Before next session", s["home"]]]
    table(d, ["", ""], body, [20, 80], font=9, hide_header=True)

    spacer(d, 4)
    para(d, "Common mistake: " + s["trap"], size=9, colour=MID, after=3)
    if s.get("check"):
        spacer(d, 4)
        para(d, "Assessed here: " + s["check"], size=9, bold=True,
             colour=MID)
    if s.get("note"):
        spacer(d, 4)
        para(d, "Note: " + s["note"], size=9, italic=True, colour=MID)
    spacer(d, 4)

# ------------------------------------------------------------------ part 3
h1_page(d, "3 · Assessment")
para(d, "Light, because these are working adults, and real, because without "
        "it the practice does not happen. Everything is marked on whether "
        "somebody could act on the result.")
table(d, ["What", "Weight", "When", "How it is marked"],
      [[a, "{}%".format(w), when, how] for a, w, when, how in C.ASSESSMENT],
      [26, 10, 12, 52], font=9, hdr_font=9)

spacer(d, 10)
callout(d, "Automatic assessment has explicit release checks",
        "S05 SQL is checked against a reference in an isolated container. "
        "S09 combines 50 executed marks with 50 local-model cleaning-log marks. "
        "Local reasoning requires a passing current calibration, and unresolved "
        "results remain blank. It is not an instant guarantee of correctness.\n\n"
        "S13 has draft numerical checks for 40 Analysis marks; S15 has draft "
        "checks for 20 reported-measure marks. Their remaining criteria and "
        "complete evidence workflows must be validated before release. Actual "
        "session dates are still required for the timed forms. The independent "
        "track retains weights 15%, 15%, 30% and 40% and its own learner roster.",
        MID_H, LIGHT_H)

# ------------------------------------------------------------------ part 4
h1_page(d, "4 · The data")
para(d, "The generated Riverside dataset carries the core teaching. "
        "Fixed local snapshots now cover Bank Marketing, synthetic AI4I and "
        "Uganda GDP for 2000–2023. Their README records provenance, transformations "
        "and interpretation limits; their manifest records hashes. Other sources "
        "below remain optional and must be staged before use. See section 6 for "
        "sources considered and rejected.")

for ds in C.DATASETS:
    h3(d, ds["name"])
    table(d, ["", ""],
          [["Where", ds["url"]],
           ["Licence", ds["licence"]],
           ["Shape", ds["shape"]],
           ["Account", ds["account"]],
           ["What it is for", ds["use"]]],
          [16, 84], font=8.8, hide_header=True)
    spacer(d, 8)

h2(d, "Why the course dataset is generated")
para(d, "The obvious core datasets for a course like this fail on licence. "
        "Tableau's Superstore, which has exactly the right shape, is "
        "governed by an end-user agreement whose sample-code clause is "
        "internal use only and not sublicensable. The Olist e-commerce set, "
        "which has a genuine nine-table star schema, is CC BY-NC-SA 4.0, and "
        "the NonCommercial clause is a live problem the moment anybody pays "
        "for the course.")
para(d, "Generating it solved that and bought three things a real file could "
        "not. The defects are deliberate, so each one teaches a named skill "
        "instead of whatever mess the file happened to contain. Every lab "
        "answer is computed from the same data at generation time, so no "
        "number in any handout was estimated. And it is properly normalised, "
        "so the SQL joins in week one are real joins.")

spacer(d, 6)
defect_rows = [
    ["Exact duplicate rows", str(K["seeded_defects"]["duplicate_rows"]),
     "An export that ran twice"],
    ["Returns as negative quantities",
     str(K["seeded_defects"]["negative_quantity_lines"]),
     "A real convention rather than an error, until somebody sums the column"],
    ["Lines priced in dollars",
     str(K["seeded_defects"]["lines_priced_in_usd"]),
     "One category was priced by a team that works in USD. Nothing in the "
     "file says so"],
    ["Discounts recorded above 1.0",
     str(K["seeded_defects"]["discounts_over_one"]),
     "15 typed where 0.15 was meant, which makes revenue negative"],
    ["Dates in a second format",
     str(K["seeded_defects"]["dates_in_dd_mm_yyyy"]),
     "Both 2025-03-14 and 14/03/2025 in one column"],
    ["Customer names with case and space problems",
     str(K["seeded_defects"]["customer_names_messy"]),
     "Three groups for one customer when you group by name"],
    ["Orders with no customer id",
     str(K["seeded_defects"]["orders_missing_customer_id"]),
     "Walk-in trade. A decision, not a defect: an inner join to customers "
     "silently loses UGX {:,.0f} of revenue".format(
         K["s3"]["revenue_lost_to_inner_join_ugx"])],
    ["One customer under two ids", "1",
     "Same name, same city, both with orders against them"],
]
table(d, ["Seeded defect", "Rows", "What it teaches"], defect_rows,
      [30, 8, 62], font=8.6, hdr_font=8.6)

spacer(d, 8)
callout(d, "The reconciliation does not come out exact, on purpose",
        "Revenue on delivered orders is UGX {:,.0f} in the database. A "
        "participant who cleans the raw CSVs correctly lands on UGX {:,.0f}, "
        "which is UGX {:,.2f} lower.\n\n"
        "That gap is real and it cannot be cleaned away: the dollar-priced "
        "category was recorded to the cent, so converting {:,} delivered "
        "lines back at 3,780 cannot recover the exact shilling price. It is "
        "0.0004% of revenue.\n\n"
        "It is in the design because reporting a reconciliation as exact when "
        "it is not is the habit this course is trying to break. Naming the "
        "residual and its cause is part of the pass mark.".format(
            K["s3"]["revenue_delivered_ugx"],
            K["s3"]["revenue_delivered_from_raw_ugx"],
            K["s3"]["usd_rounding_residual_ugx"],
            K["s3"]["usd_lines_delivered"]),
        "C55A11", AMBER_H)

# ------------------------------------------------------------------ part 5
h1_page(d, "5 · The glossary, which is a handout in its own right")
para(d, "{} terms, defined in plain language, {} of which have a direct "
        "spreadsheet equivalent. It is printed once in session 1 and kept on "
        "the desk for five weeks, and nothing in this course is explained "
        "using a word that is not on it.".format(
            len(C.GLOSSARY),
            sum(1 for _, _, x, _ in C.GLOSSARY if x)))
para(d, "It is generated from the sessions themselves, so a term cannot be "
        "taught without reaching the handout and the handout cannot drift "
        "from what was taught. The full version is "
        "DataAnalysis_Glossary.docx; the terms with no spreadsheet "
        "equivalent are listed below, because those are the genuinely new "
        "ideas and there are fewer of them than anybody expects.")
spacer(d, 6)
_new_only = [t for t, _, x, _ in C.GLOSSARY if not x]
table(d, ["The {} ideas with no spreadsheet equivalent".format(
    len(_new_only))],
      [[", ".join(_new_only)]], [100], font=9, hdr_font=9)

h1_page(d, "6 · Datasets that were considered and rejected")
para(d, "Recorded so they do not get proposed again, and so that anybody "
        "asking why an obvious choice is missing gets an answer.")
table(d, ["Dataset", "Why it is not in the track"],
      [[a, b] for a, b in C.REJECTED], [24, 76], font=8.8, hdr_font=8.8)

spacer(d, 10)
callout(d, "Keep source terms with distributed data",
        "Use the source attribution and licence recorded for each dataset; "
        "the listed sources do not all have the same licence. The staged UCI "
        "snapshots use CC BY 4.0; World Bank data also have additional terms, "
        "and Healthsites uses ODbL. Keep original snapshots and identify changes "
        "in derived files. A course being university-based does not by itself "
        "establish permission for every proposed reuse. Confirm the applicable "
        "source terms before adding a new dataset or publishing derived work. "
        "Reference: https://creativecommons.org/faq/",
        MID_H, LIGHT_H)

# ------------------------------------------------------------------ part 6
h1_page(d, "7 · What the instructor does before session 1")
table(d, ["#", "Do this", "Why it matters"],
      [["1", "Run data/build_teaching_data.py once. It needs nothing "
             "installed beyond Python 3.8.",
        "Produces riverside.db, the raw CSVs, the clean CSVs and "
        "answer_key.json. Takes a few seconds."],
       ["2", "Run scripts/verify_da_track.py.",
        "Executes every SQL block in the labs, re-derives every asserted "
        "answer a second way, and runs the pandas pipeline end to end. If "
        "this is not green, do not teach from the pack."],
       ["3", "Work the SQL lab yourself, in DB Browser, from cold.",
        "It is fifty minutes. You will find the one question your room will "
        "get stuck on, and it is usually question 3."],
       ["4", "Build the Power BI model yourself, on the machine you will "
             "teach from.",
        "Sessions 14–15 require a rehearsed account and machine setup, and the "
        "difference is whether the instructor has already hit the date-table "
        "problem."],
       ["5", "Put the data folder on USB sticks as well as a link.",
        "The room's network is not a dependency. Twenty people downloading "
        "a database at 18:05 is twenty minutes gone."],
       ["6", "Ask, in writing, how many participants are on a Mac.",
        "It affects Week 5. Power BI Desktop requires Windows. Rehearse the "
        "browser model editor with the actual account and its workspace/tenant "
        "permissions, or arrange a Windows lab machine."],
       ["7", "Ask each participant for one question from their own work.",
        "Collected in session 1 and used as capstone candidates. A capstone "
        "on the participant's own data is the difference between a course "
        "they finish and a course they use."]],
      [4, 40, 56], font=8.8, hdr_font=8.8)

# ------------------------------------------------------------------ part 7
h1_page(d, "8 · Kit, room and logistics")
h2(d, "What has to be installed")
table(d, ["Tool", "What to install, and the fallback"],
      [[a, b] for a, b in C.KIT], [18, 82], font=9, hdr_font=9)

spacer(d, 8)
callout(d, "Rehearse the Power BI route before Week 5",
        "Desktop requires Windows. The browser semantic-model editor now "
        "includes Power Query, subject to model ownership, workspace permissions "
        "and tenant settings. A local CSV upload remains a snapshot; refreshing "
        "data needs a supported source. Use the CSV lab path and test it with "
        "the actual learner account. If editing is unavailable, pre-provision a "
        "Windows lab machine. Reference: "
        "https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models",
        "C55A11", AMBER_H)

spacer(d, 8)
h2(d, "The room")
table(d, ["", ""], [[a, b] for a, b in C.ROOM], [20, 80], font=9,
      hide_header=True)

# ------------------------------------------------------------------ part 8
h1_page(d, "9 · What was cut, and why")
para(d, "Teaching from a standing start is worth six to eight hours on its "
        "own. It was funded two ways: three extra sessions, taking the track "
        "from twelve to fifteen, and cutting the most advanced material. "
        "What came out is here so that nobody puts it back by accident, and "
        "so that a cohort which moves quickly has a list of what to add.")
table(d, ["What came out", "Why, and what replaced it"],
      [[a, b] for a, b in C.CUT], [26, 74], font=8.8, hdr_font=8.8)

spacer(d, 10)
callout(d, "The first thing to add back",
        "Reshaping, pivot_table and melt in pandas. It is a genuinely "
        "useful idea and it was cut because it is the third way of saying "
        "something the room has already met twice, as a pivot table and as "
        "GROUP BY. A cohort that reaches session 9 comfortably has room for "
        "it in the second half of that session.",
        "1F6F8B", "DDEAF0")

h1_page(d, "10 · Where this departs from the roadmap.sh path")
para(d, "The track is built on the roadmap.sh data-analyst path and every "
        "session names the part of it being taught. The deliberate "
        "departures, each with a reason.")
for t, why in C.DEPARTURES:
    h3(d, t)
    para(d, why, size=9.5)
    spacer(d, 4)

spacer(d, 8)
h2(d, "What to do next, which session 15 introduces")
para(d, "Forty-five hours provides a foundation for guided analysis; "
        "competence must be demonstrated in the submitted work. Further practice "
        "can develop statistics and experiment design for causal questions, "
        "machine learning for prediction, or data engineering for reliable "
        "collection and refresh. Choose the next step from the work the learner "
        "needs to do, rather than treating course attendance as proof of mastery.")

_gone = tidy_page_breaks(d)
d.save(OUT)
print("saved " + OUT)
print("  removed {} empty paragraph(s) stranded before a page break"
      .format(_gone))
print("  sessions: {}, hours: {}, datasets: {}, rejected: {}".format(
    len(C.SESSIONS), C.TOTAL_HOURS, len(C.DATASETS), len(C.REJECTED)))
