# -*- coding: utf-8 -*-
"""IUEA Semester 1 Master Teaching Plan — narrative Word document."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.shared import Pt
from docxkit import *   # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Semester1_Master_Teaching_Plan.docx"

d = new_doc()
header_footer(d, "IUEA Faculty of Engineering · Machine Learning for Engineers · Semester 1 Master Teaching Plan")
first_page_different(d)

# ---------------------------------------------------------------- title page
spacer(d, 70)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA", size=11.5, bold=True, colour=MID, align=AL.CENTER, after=4)
para(d, "Faculty of Engineering", size=11.5, colour=GREY, align=AL.CENTER, after=30)
para(d, "Machine Learning for Engineers", size=27, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "Year 3 Undergraduate Programme", size=15, colour=MID, align=AL.CENTER, after=26)
p = para(d, "SEMESTER 1 MASTER TEACHING PLAN", size=17, bold=True, align=AL.CENTER, after=6, before=6)
_border(p, "top", NAVY_H, 12)
_border(p, "bottom", NAVY_H, 12)
spacer(d, 18)
para(d, "7 September – 18 December 2026   ·   15 study weeks", size=11.5, align=AL.CENTER, after=3)
para(d, "Three cohorts   ·   3 contact hours per cohort per week   ·   45 contact hours each", size=11.5, align=AL.CENTER, after=3)
para(d, "Approximately 190–200 students in total", size=11.5, align=AL.CENTER, after=50)
para(d, "Companion documents", size=9.5, bold=True, colour=GREY, align=AL.CENTER, after=3)
para(d, "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx — the week-by-week master grid", size=9.5, colour=GREY, align=AL.CENTER, after=2)
para(d, "IUEA_ML_Assessment_Technology_Build_Plan.docx — the auto-grading system", size=9.5, colour=GREY, align=AL.CENTER, after=2)
para(d, "IUEA_ML_Student_Setup_Guide.docx  ·  IUEA_ML_Week2_Lecturer_Runsheet.docx", size=9.5, colour=GREY, align=AL.CENTER, after=2)
para(d, "grader/ and setup/ — implementation and student practicals", size=9.5, colour=GREY, align=AL.CENTER, after=2)
para(d, "Three cohort syllabi — CML3111, CML3112, CML3113", size=9.5, colour=GREY, align=AL.CENTER, after=14)
para(d, "Version 1.0  ·  drafted 1 September 2026  ·  for Faculty review",
     size=9.5, italic=True, colour=GREY, align=AL.CENTER)
page_break(d)

# ---------------------------------------------------------------- contents
h1(d, "Contents")
para(d, '1. Purpose and status', size=11, after=9)
para(d, '2. The teaching assignment', size=11, after=9)
para(d, '3. The Semester 1 calendar', size=11, after=9)
para(d, '4. The pedagogical model', size=11, after=9)
para(d, '5. The 70/30 architecture', size=11, after=9)
para(d, '6. The shape of the semester', size=11, after=9)
para(d, '7. Assessment design', size=11, after=9)
para(d, '8. Making it markable: the auto-grading stack', size=11, after=9)
para(d, '9. Managing a hundred-student cohort', size=11, after=9)
para(d, '10. Tooling, and why each tool appears when it does', size=11, after=9)
para(d, '11. Dataset strategy', size=11, after=9)
para(d, '12. Risk register', size=11, after=9)
para(d, '13. What to build next, and in what order', size=11, after=9)
para(d, '14. The bridge to Semester 2', size=11, after=9)
para(d, 'Appendix A · The fifteen weeks at a glance', size=11, after=9)
para(d, 'Appendix B · The graduate profile ladder', size=11, after=9)
page_break(d)

# ================================================================ 1
h1(d, "1. Purpose and status")
para(d, "This document is the pedagogical architecture for Semester 1 of the Year 3 machine learning programme in "
        "the Faculty of Engineering. It sits deliberately between the curriculum concept and the teaching "
        "materials. The concept — three cohorts, a shared machine learning core, a problem-first pedagogy and "
        "entirely practical assessment — has already been agreed. The materials, meaning slide decks, notebooks, "
        "datasets and labs, have not yet been built. This plan is the layer that must be settled first, because "
        "every one of those materials inherits its shape from decisions made here.")
para(d, "It fixes six things. It fixes the calendar against the real academic dates and the real public holidays. "
        "It fixes the architecture of the thirteen teaching weeks and the two assessment weeks. It fixes what is "
        "shared across the three cohorts and what must be prepared three times over. It fixes the assessment "
        "design, including weights, formats and rubrics. It fixes the policy on artificial intelligence "
        "assistants, which cannot be left vague in a course of this kind. And it names, honestly, the delivery "
        "risks that will determine whether the semester works.")
para(d, "What it deliberately does not do is produce content. There are no slides here and no notebooks. That "
        "restraint is the point: producing three hundred slides against an unagreed architecture would waste most "
        "of the effort. Section 13 sets out what should be built next, in what order, and by when each piece is "
        "needed.")
callout(d, "Status of the numbers in this plan",
        "The assessment weightings, the course codes and the cohort-to-slot allocation are proposals, not "
        "confirmed IUEA policy. Section 7 provides an alternative weighting model that satisfies a mandated "
        "coursework-versus-final split without altering any teaching. Four items require a Faculty decision "
        "inside the first fortnight and are listed immediately below.", "C55A11", AMBER_H)

h2(d, "Four decisions needed in the first fortnight")
para(d, "The first is test capacity. Cohort A is approximately one hundred students, and the two practical tests "
        "in Weeks 7 and 14 are computer-based. If one laboratory cannot seat and equip a hundred students "
        "simultaneously, the tests require either two sittings with different datasets or a hybrid of personal "
        "laptops and laboratory machines. That is a timetabling and estates question, and it needs to be asked in "
        "Week 1 rather than Week 6.")
para(d, "The second is the Week 5 public holiday, discussed in Section 3. The third is marking capacity: "
        "one lecturer cannot manually assess every submission. Deterministic checks handle code and numerical "
        "work; a calibrated local model is intended to handle supported reasoning evidence. Real grading time "
        "and exception rates must be measured in a pilot; no reduction in workload is yet a verified result. "
        "The fourth is Faculty confirmation of the assessment model before the first test in Week 7.")

# ================================================================ 2
h1(d, "2. The teaching assignment")
para(d, "Three cohorts are taught, each grouping related programmes, and each receiving one three-hour session "
        "per week. The total lecturer contact load is nine hours per week: three hours in the Tuesday slot and six "
        "hours on Friday, the Friday block being two separate three-hour sessions for two different cohorts. No "
        "cohort receives more than three hours per week, which is the single most important constraint in this "
        "plan and the reason the design is as compressed as it is.")
table(d, ["Code", "Cohort", "Programmes", "Size", "Course title"],
      [["CML3112", "A", "Architecture + Civil Engineering", "~100\n(≈22 teams)",
        "Introduction to Machine Learning in Design & Infrastructure"],
       ["CML3113", "B", "Mining Engineering + Petroleum Engineering", "~40–50\n(≈10 teams)",
        "Introduction to Machine Learning in Mining & Petroleum Engineering"],
       ["CML3111", "C", "Electrical, Mechatronics & Robotics, Communications Engineering", "~50\n(≈11 teams)",
        "Introduction to Machine Learning in Engineering"]],
      [11, 7, 31, 13, 38], bold_first=True)
spacer(d, 12)
para(d, "Which cohort occupies which slot was not confirmed when this plan was drafted, so the plan is written to "
        "be slot-agnostic. The workbook carries a mapping table on its first sheet; filling in three cells "
        "resolves every date in every cohort sheet. There is one substantive consideration in making that choice. "
        "Cohort A is the largest, and the Tuesday slot is the only one that does not share a day with another "
        "three-hour session. Placing the hundred-student cohort on Tuesday gives a full day's recovery either side "
        "of it and avoids a six-hour Friday that begins with the most demanding class. Set against that, the two "
        "Friday cohorts will always run one session behind if a Friday is lost to a holiday — which, as Section 3 "
        "shows, is exactly what happens in Week 5.")
para(d, "The students have essentially no background in programming, computer science or machine learning. "
        "Everything technical is built from zero. This is not, however, an introductory computing course wearing "
        "an engineering label. The framing throughout is machine learning for engineers: the motivating question "
        "always comes from the students' own discipline, and the programming is introduced as the means of "
        "answering it.")

# ================================================================ 3
h1(d, "3. The Semester 1 calendar")
para(d, "The semester runs for fifteen study weeks from Monday 7 September 2026, inclusive of the two designated "
        "assessment weeks. That gives thirteen teaching weeks and two assessment weeks per cohort, and forty-five "
        "contact hours in total. The assessment weeks are placed at Weeks 7 and 14.")

cal_rows = [
    ["1", "7 Sep", "Tue 8 Sep", "Fri 11 Sep", "Teaching", ""],
    ["2", "14 Sep", "Tue 15 Sep", "Fri 18 Sep", "Teaching", ""],
    ["3", "21 Sep", "Tue 22 Sep", "Fri 25 Sep", "Teaching", ""],
    ["4", "28 Sep", "Tue 29 Sep", "Fri 2 Oct", "Teaching", ""],
    ["5", "5 Oct", "Tue 6 Oct", "Fri 9 Oct", "Teaching", "PUBLIC HOLIDAY on the Friday — Independence Day"],
    ["6", "12 Oct", "Tue 13 Oct", "Fri 16 Oct", "Teaching", ""],
    ["7", "19 Oct", "Tue 20 Oct", "Fri 23 Oct", "ASSESSMENT", "Practical Test 1 — Data Investigation"],
    ["8", "26 Oct", "Tue 27 Oct", "Fri 30 Oct", "Teaching", ""],
    ["9", "2 Nov", "Tue 3 Nov", "Fri 6 Nov", "Teaching", ""],
    ["10", "9 Nov", "Tue 10 Nov", "Fri 13 Nov", "Teaching", ""],
    ["11", "16 Nov", "Tue 17 Nov", "Fri 20 Nov", "Teaching", ""],
    ["12", "23 Nov", "Tue 24 Nov", "Fri 27 Nov", "Teaching", ""],
    ["13", "30 Nov", "Tue 1 Dec", "Fri 4 Dec", "Teaching", ""],
    ["14", "7 Dec", "Tue 8 Dec", "Fri 11 Dec", "ASSESSMENT", "Practical Test 2 — End-to-End ML"],
    ["15", "14 Dec", "Tue 15 Dec", "Fri 18 Dec", "Demo", "Engineering ML Demo Day and viva"],
]
table(d, ["Wk", "Commencing", "Tuesday slot", "Friday slots", "Type", "Note"], cal_rows,
      [5, 12, 14, 14, 13, 42], bold_first=True,
      shade_fn=lambda i, r: RED_H if r[4] == "ASSESSMENT" else (AMBER_H if r[5] and r[4] == "Teaching" else (GREEN_H if r[4] == "Demo" else None)))
spacer(d, 14)
callout(d, "The Week 5 collision — decide this in Week 2",
        "Friday 9 October 2026 is Uganda Independence Day. It falls in Week 5, and Week 5 is the pandas session — "
        "arguably the single most load-bearing three hours of the semester, since everything from Week 6 onward "
        "assumes it. Both Friday cohorts lose it, while the Tuesday cohort is unaffected. The mitigation must be "
        "decided in Week 2, not discovered in Week 4. Either secure a Faculty-approved make-up slot, or publish "
        "the session asynchronously: a recorded walkthrough and the practical notebook released by Wednesday 7 "
        "October, a forty-five-minute online clinic that week, and a thirty-minute consolidation opening Week 6 "
        "with that week's demonstration shortened to compensate. The asynchronous route is workable but it is "
        "second-best, and it means the two Friday cohorts carry a small deficit into the Week 7 test.",
        "C00000", RED_H)
para(d, "No other public holiday falls inside a class slot in this window. Christmas and Boxing Day fall after the "
        "semester ends. Islamic holidays in 2026 fall in March and May and are therefore a Semester 2 concern; "
        "because their dates depend on lunar observation they should be checked again when the Semester 2 calendar "
        "is built.")

# ================================================================ 4
h1(d, "4. The pedagogical model")
h2(d, "The problem creates the need for the concept")
para(d, "The organising principle of the whole programme is that no session opens with a definition. The "
        "conventional sequence — define machine learning, teach three weeks of syntax, eventually arrive at an "
        "application — fails with this audience for a specific reason: it asks students with no programming "
        "background to invest weeks of effort before they see why any of it matters. A third of them will "
        "disengage before the payoff arrives.")
para(d, "The inverted sequence looks like this in practice. Week 8 does not begin by defining linear regression. "
        "It begins with a question the students can already feel the weight of:")
quote(d, "“Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?”")
para(d, "The class then works out what data would be needed, which variables might matter, and how one might tell "
        "whether an estimate could be trusted. Only at that point is a technique introduced, and it is introduced "
        "as the answer to a question the students have already asked. Every week in Section 6 is built this way, "
        "and the framing question for each cohort is recorded in the workbook.")

h2(d, "The learning cycle")
para(d, "The cycle is problem, explore, learn, build, test, reflect, improve — not lecture, notes, assignment, "
        "examination. Concretely, that means roughly half of every three-hour session is hands-on, every week "
        "produces an artefact in a repository, and every week contains at least one segment in which the students "
        "are given a problem and not given a method.")

h2(d, "Productive struggle, and the refusal to spoon-feed")
para(d, "One segment of every session is deliberately under-guided, and four sessions are almost entirely so: the "
        "Investigation Lab in Week 4, the Ten Questions round in Week 5, the 97% Trap in Week 9 and the "
        "Engineering AI Challenge in Week 12. In these segments the lecturer's role narrows to asking questions. "
        "The question bank is printed on a card and carried around the room, because the hardest part of running "
        "these sessions is not designing them but resisting the urge to answer.")
para(d, "The questions are: what are you trying to find; why did you choose that variable; what does this chart "
        "actually tell you; is that relationship meaningful or coincidental; what would happen if this data were "
        "missing; how do you know your model is any good; could there be leakage here; and what else could you "
        "try. Nothing on that list supplies an answer, and every item on it models the internal monologue of a "
        "working engineer.")
para(d, "The target is a measurable shift in how students speak. In September the characteristic utterance is "
        "“Sir, what should I type?” By December it should be “We tried three approaches; the first two failed "
        "because of X, so we are now testing the third.” That shift is worth more than any particular technique, "
        "and the assessment design in Section 7 is built to reward it.")

h2(d, "Learning to learn")
para(d, "The tooling in this field will have changed substantially by the time these students graduate, so a "
        "course that teaches only current tools is depreciating from the day it is delivered. Reading "
        "documentation, interpreting an error message, searching effectively, reading unfamiliar code, decomposing "
        "a large problem, finding and evaluating a dataset, and using an AI assistant without surrendering "
        "judgement are therefore treated as examinable content rather than incidental skills. They appear "
        "explicitly in Weeks 2, 3, 4, 5, 6, 10 and 13, and they carry marks.")
quote(d, "“I am not here to teach you everything you will ever need. I am here to teach you how to learn what you need.”")

# ================================================================ 5
h1(d, "5. The 70/30 architecture")
para(d, "Three cohorts share approximately seventy per cent of their content — the machine learning core — and "
        "diverge in approximately thirty per cent, being the examples, datasets, projects and case studies. The "
        "core progression is identical for all three: engineering problems, computational thinking, Python, data "
        "handling, data analysis, statistics, machine learning, model evaluation, engineering application, project.")
para(d, "The practical consequence is that one preparation serves three sessions, provided the divergence is "
        "handled deliberately rather than accidentally. The workbook's 'Shared vs Divergent' sheet states, for "
        "each of the fifteen weeks, exactly what is common and exactly what must be re-skinned, with an effort "
        "estimate. Reading that sheet yields a clear and slightly uncomfortable finding: the triplicated effort is "
        "concentrated almost entirely in Weeks 4 through 7 and in the two assessment weeks, because that is where "
        "teaching datasets must be authored from scratch. Weeks 2 and 13 require no divergent preparation "
        "whatsoever.")
para(d, "The implication for planning is that the unseen test datasets are the largest single item of work in the "
        "semester. Three matched variants per cohort means nine per test, and eighteen across the two assessment "
        "weeks, each with a model answer and a mark scheme. They should be built during the low-divergence weeks — "
        "Weeks 2 to 5 for the first test and Weeks 8 to 12 for the second — rather than in the fortnight before "
        "each test, when there will be no time.")
table(d, ["Layer", "Content", "Preparation"],
      [["Shared core (≈70%)",
        "Concepts, session structure, challenge designs, tool introductions, assessment formats, rubrics, "
        "reproducibility standards, peer review", "Once"],
       ["Cohort overlay (≈30%)",
        "Framing questions, anchor datasets, engineering formulas, engineered features, cost categories, planted "
        "leakage causes, client briefs, project titles, test variants", "Three times"]],
      [16, 62, 15], bold_first=True)

# ================================================================ 6
page_break(d)
h1(d, "6. The shape of the semester")
para(d, "The thirteen teaching weeks fall into five blocks. Each is described below in terms of what the students "
        "can do at the end of it that they could not do at the start. The workbook carries the full detail for "
        "every week: learning objectives, a minute-by-minute session structure, concepts, tools, practical, "
        "dataset, challenge, assignment, project milestone, assessment relevance, lecturer preparation and "
        "required resources.")

h2(d, "Block 1 · Weeks 1–4 · Orientation and computational thinking")
para(d, "The semester opens without a computer. Week 1 is a paper-based session in which teams predict a withheld "
        "value from a printed twelve-row extract of their cohort's anchor dataset, discover that they have just "
        "done inductive inference from examples, and produce the words feature, target and error themselves. They "
        "also see a finished student-level project, so the destination is concrete from the first hour, and they "
        "form the teams they will keep all semester. Nobody is blocked by a laptop on day one, which matters more "
        "than it sounds when a hundred students arrive with unknown hardware.")
para(d, "Week 2 teaches Colab notebooks and GitHub version control through a small cohort-specific CSV practical. Students upload the supplied notebook and CSV, explore execution order, repair four faults and save a fresh-run notebook. A prepared local lab provides the connection fallback. A2 requires the notebook, README and repository URL; its form closes at the start of Week 3.")
para(d, "Weeks 3 and 4 build Python on engineering formulas the students already know, so the syntax is carried "
        "by familiar content rather than by abstract exercises. Week 3 ends with the Wrong Answer Hunt: six "
        "functions that run cleanly and return wrong answers, through integer division, operator precedence, a "
        "degrees-and-radians confusion, a misplaced conditional boundary, a mutated input and a unit mismatch. The "
        "belief that code which runs is code which is correct is the most dangerous thing a beginner can carry "
        "forward, and it is fatal later in model evaluation, so it is attacked early and explicitly.")
para(d, "Week 4 introduces collections, loops and file reading using only the standard library — deliberately the "
        "hard way, so that pandas is earned rather than merely presented — and closes with Investigation Lab 1, "
        "the first fully unguided session. Teams receive an unfamiliar three-hundred-row file with no column "
        "dictionary, no suggested method and the instruction to find something interesting. The file must be "
        "authored so that it contains one genuine, findable, discipline-relevant story plus two red herrings; a "
        "file with nothing in it teaches cynicism instead of investigation.")

h2(d, "Block 2 · Weeks 5–6 · Engineering data")
para(d, "Week 5 opens by rewriting the previous week's sixty-line reading report in four lines of pandas, side by "
        "side on the projector. The argument for the tool is made by the tool. The session then runs a guided "
        "interrogation of the cohort's anchor dataset through twelve real engineering questions, each answerable "
        "in a few lines, with answers required in physical units rather than as raw output. It also covers where "
        "data comes from: Kaggle, the UCI repository, and how to read a dataset card for provenance, licence, "
        "collection method and — the question students never think to ask — whether the data can actually answer "
        "the question being posed.")
para(d, "Week 6 pairs data cleaning with visualisation, and pairs them for a reason. Charts are taught as "
        "instruments of detection rather than decoration: a box plot to find outliers, a missingness map to find "
        "gaps, a scatter plot to find physically impossible relationships, a correlation heatmap to find "
        "redundancy. The standing rule, which later becomes a marking criterion, is that every chart answers a "
        "stated question. The session closes with the Outlier Argument: five flagged extreme values, of which two "
        "are genuinely arguable either way, on which teams must commit to a position and defend it. There is no "
        "lookup answer, which is precisely the point.")

h2(d, "Week 7 · Practical Test 1 · Data Investigation")
para(d, "The first assessment week certifies data literacy, not modelling. Individually and offline, over two "
        "hours plus a twenty-five-minute written section, each student investigates an unfamiliar dataset from "
        "their own domain: profile it, find and handle its defects with a written justification for each, answer "
        "three stated engineering questions with evidence, produce three charts each captioned with the question "
        "it answers, list five findings, and make one recommendation. The written section then asks them about "
        "their own submission, typed offline without code execution: why that cleaning decision, what the chart does not show, what "
        "would change the conclusion, what data is missing.")
para(d, "Three matched dataset variants are issued in a checkerboard seating pattern. The room runs offline, which "
        "removes both internet search and AI assistance, and — this matters — is actually enforceable, unlike a "
        "rule against using an assistant on a networked machine.")

h2(d, "Block 3 · Weeks 8–10 · The machine learning core")
para(d, "Week 8 is the first model, and its central demonstration — a complete regression in about fifteen lines, "
        "with every line justified aloud — is the most important fifteen minutes of the semester and should be "
        "rehearsed until it cannot fail. Two devices do the pedagogical work. The first is the train-and-test "
        "argument delivered as an analogy rather than a rule: revising with the exam paper in front of you tells "
        "you nothing about what you know. The second is the trivial baseline. Comparing against a "
        "predict-the-mean baseline is what makes a number like R-squared of 0.62 mean anything, and it makes an "
        "unimpressive model an interesting result to diagnose rather than a failure to hide. Error is reported in "
        "physical units throughout — plus or minus so many megapascals, megawatts or percentage points of silica — "
        "followed by the question that actually matters: is that good enough to act on? The answer is usually no, "
        "and that is the most valuable thing the week teaches.")
para(d, "Week 9 moves to classification, framed from the outset around the asymmetry of the two mistakes. A false "
        "alarm stops production; a missed failure destroys a machine or hurts someone. Everything else — the "
        "confusion matrix, the choice between precision and recall, the threshold as an engineering decision "
        "rather than a constant — follows from that asymmetry. Students complete a cost table in their own "
        "domain's terms before they are allowed to recommend a metric. The session closes with the 97% Trap: a "
        "model reporting ninety-seven per cent accuracy on an imbalanced dataset, an unhappy fictional plant "
        "manager, and no hints. Teams must discover the imbalance, prove the model useless and propose a better "
        "metric. This single exercise inoculates against the most common failure in applied machine learning.")
para(d, "Week 10 asks whether the model can be trusted, and it is the highest-value week in the semester. Students "
        "see training accuracy climb to one while test accuracy falls, discover that a single train-test split was "
        "itself a noisy measurement, and then deliberately introduce two leaks — scaling before the split, and a "
        "column that is only known after the outcome — in order to watch the score become impossibly good. The "
        "Pipeline is introduced at this moment, not as tidy code but as the structural fix for leakage. The "
        "closing challenge hands teams a notebook reporting an R-squared of 0.998 with three different planted "
        "causes across the room, so no diagnosis can be copied. Leakage is the defect most likely to appear in "
        "student projects and in professional practice, and this is where it is confronted.")

h2(d, "Block 4 · Weeks 11–12 · Practical judgement")
para(d, "Week 11 is where domain knowledge formally enters the model. A feature is engineering knowledge written "
        "in a form the model can use, connecting domain understanding with programming. "
        "Each cohort tests a proposed feature against raw inputs under the same validation protocol: the "
        "water-to-cement ratio for the civil and architecture cohort, a century-old piece of concrete technology; "
        "the reagent-to-feed ratio for mining and petroleum; and mechanical power from torque and angular velocity "
        "for the electrical, mechatronic and robotics cohort, which has the strongest physics-to-feature story of "
        "the three. Contributions are measured by ablation, and a feature that did not help must be reported "
        "rather than quietly deleted. The closing challenge splits the room: half of each pair of teams may use "
        "only raw columns, the other half must invent features and may not change the model. They generate the "
        "evidence for the week's argument themselves.")
para(d, "Week 12 is the least guided session before the test and the closest rehearsal for professional practice. "
        "After twenty minutes on what a fair comparison protocol requires and a single worked hyperparameter "
        "search, teams receive an unfamiliar dataset and a brief from a fictional client that contains a real "
        "constraint — a cost, a safety consequence, or a requirement that the decision be explainable to a "
        "regulator. They run at least four candidate models under one identical protocol and produce a one-page "
        "recommendation. The lecturer circulates for a full hour and three quarters and gives no answers. Each "
        "team then defends its recommendation to another team whose job is to attack it, and the quality of the "
        "challenges is marked alongside the quality of the defences. Gradient boosting is demonstrated for sixty "
        "seconds and then explicitly deferred to Semester 2, with the students told why: the tool is not the lesson.")

h2(d, "Block 5 · Weeks 13–15 · Project, test and demonstration")
para(d, "Week 13 treats reproducibility as a professional obligation. A messy exploratory notebook is refactored "
        "live into a clean repository with a README, requirements file and passing restart-and-run-all. Teams then "
        "build, with the lecturer running timed clinic slots on a booked rotation, and review one another's "
        "repositories against the project rubric. The peer review is where most teams find their own defects, in "
        "someone else's work. For a cohort of twenty-two teams the clinic rotation must be built and published in "
        "advance; without a booking sheet this session degrades into a queue.")
para(d, "Week 14 is the second practical test, this time end-to-end: frame the task, prepare the data, build at "
        "least two models inside a leak-proof pipeline, evaluate with a justified metric, report in operational "
        "units and state three limitations. Again individual, again offline, again three matched variants.")
para(d, "Week 15 is Demo Day. Every cohort uses a two-round fair with laptops and posters, followed by three "
        "selected demonstrations of at most six minutes each and two minutes for recognition. "
        "Every student submits individual typed answers to two repository-specific questions with their "
        "reflection. These provide evidence for local rubric assessment; brief live questioning is formative "
        "sampling, since one lecturer cannot conduct a three-minute viva for every student during the fair. Recognition is awarded for Best Engineering Reasoning, Best Investigation and Most Honest "
        "Limitations. There is deliberately no prize for highest accuracy. The session closes by putting the Week "
        "1 promise back on the screen and asking the cohort whether it was kept.")

# ================================================================ 7
h1(d, "7. Assessment design")
para(d, "Assessment is entirely practical and project-based. There is no traditional written machine learning "
        "examination, on the straightforward grounds that a written paper cannot distinguish a student who can "
        "investigate a dataset from one who has memorised a definition. What is assessed instead is the full "
        "chain: engineering problem, data, analysis, model, evaluation, engineering interpretation, solution.")

h2(d, "Recommended weighting")
table(d, ["Component", "When", "Mode", "Weight"],
      [["Weekly quizzes (12 graded, best 10 of 12)", "End of every teaching session: W1–W6, W8–W13",
        "Individual, auto-graded", "10%"],
       ["Practical challenges and assignments (best 8 of 11)", "Weeks 1–12", "Individual, auto-graded", "10%"],
       ["Data Analysis Project", "Launched W5, due W8", "Team, individual log", "10%"],
       ["Practical Test 1 — Data Investigation", "Week 7", "Individual, offline", "15%"],
       ["Practical Test 2 — End-to-End Engineering ML", "Week 14", "Individual, offline", "20%"],
       ["Engineering ML Project", "Launched W9, due W15", "Team + individual evidence", "25%"],
       ["Demonstration, viva and individual reflection", "Week 15", "Individual", "10%"],
       ["Individual share of the total mark", "", "", "65%"],
       ["Team share of the total mark", "", "", "35%"],
       ["Automated assessment coverage", "", "", "Pilot pending"]],
      [44, 23, 20, 11], bold_first=True,
      shade_fn=lambda i, r: GREEN_H if i >= 7 else None)
spacer(d, 12)
para(d, "Two tests rather than one is a change from the original curriculum sketch, and it follows from the "
        "assessment weeks being fixed at Weeks 7 and 14. Since two slots exist, they should examine different "
        "things. Week 7 certifies data literacy; Week 14 certifies end-to-end capability. Splitting them also "
        "means a student who struggles in October is not sunk, and it gives the lecturer a mid-semester signal "
        "that arrives in time to act on.")
para(d, "Sixty-five per cent of the mark is individual. With teams of four to five and up to twenty-two teams in "
        "the largest cohort, a team-heavy scheme would allow a weak student to pass on a strong teammate's work. "
        "Two individual tests, individually marked weekly work, twelve individual weekly quizzes and an individual viva "
        "make the team component safe to award — and they make the rotating team roles and contribution logs "
        "meaningful rather than decorative.")

h2(d, "Continuous assessment: the twelve weekly quizzes")
para(d, "Every teaching session closes with a five-minute quiz of five multiple-choice questions, delivered by a "
        "QR code on the projector, taken on the students' own phones in the last five minutes, auto-marked, with "
        "the score and a teaching comment released the moment they submit. Twelve are graded, the best ten "
        "counting, at one per cent each: Weeks 1 to 6 and Weeks 8 to 13. Weeks 7 and 14 are the practical tests "
        "and Week 15 is Demo Day, so those three weeks carry no quiz. The Week 2 proof-of-life submission separately verifies that each student can run and save the supplied notebook.")
para(d, "The design constraint that matters is what the questions are allowed to be. A multiple-choice question "
        "cannot assess engineering reasoning, and a course that lets auto-marking spread unchecked ends up "
        "testing recall. So every quiz question shows the student code, an output, a chart or a table, and asks "
        "them to diagnose or interpret it. None asks for a definition. Two of the five questions in each quiz "
        "show code that runs cleanly and returns a wrong answer, because that is the failure a beginner "
        "cannot see and the one that will quietly destroy their Week 10 model. One shows a traceback, one "
        "supplies an output to interpret, and one sets a constraint. A question that could be answered "
        "without reading the code is thrown away. The quizzes in Weeks 12 and 13 draw two of their five questions "
        "from the Week 1 to Week 10 banks, which is what keeps the set cumulative.")
para(d, "Two features are worth noting because they follow from auto-marking rather than merely surviving it. "
        "Because marking is free, the quiz can run every week rather than five times a semester, which turns it "
        "from an occasional gate into a weekly signal for the student and the lecturer alike. And there are no "
        "resits: only the best ten of the twelve count, so a student who misses two sessions, or a cohort that "
        "loses one to a network failure, is not penalised at all. A sitting lost to the network converts to a "
        "24-hour asynchronous window, and the class is told so before they leave the room.")
para(d, "On integrity, the honest position is that a quiz taken on personal phones in one room can be colluded on, "
        "and no free tool prevents it. The design accepts this rather than pretending otherwise: each quiz "
        "is worth one per cent, three parallel versions are issued by seating column with question and "
        "option order shuffled, every question requires reading a supplied snippet rather than recalling a fact, "
        "and correct answers are never released — only which questions were missed, with the feedback. The "
        "quizzes reward keeping up. They do not certify competence. Thirty-five per cent of the mark sits in "
        "the two offline tests, and that is where unaided capability is certified. A student whose quiz "
        "scores and test scores diverge sharply is visible in the gradebook and should be spoken to.")

h2(d, "If IUEA mandates a coursework and final split")
para(d, "Many programmes require a fixed division between continuous assessment and final assessment. The "
        "following mapping produces a forty–sixty split without altering a single teaching session; only the "
        "recorded category changes.")
table(d, ["Category", "Components", "Weight"],
      [["Continuous assessment (40%)",
        "Weekly quizzes 10% · Practical challenges 10% · Data Analysis Project 10% · Practical Test 1 10%",
        "40%"],
       ["Final assessment (60%)",
        "Practical Test 2 20% · Engineering ML Project 30% · Demonstration, viva and reflection 10%", "60%"]],
      [24, 60, 14], bold_first=True)
spacer(d, 12)
para(d, "This mapping is worth having ready, because the weekly quizzes make the continuous-assessment case "
        "much easier to argue: forty per cent of the mark is now genuinely continuous, accumulated across eleven "
        "weekly submissions and twelve weekly quizzes rather than concentrated in one or two events.")

h2(d, "Rubrics")
para(d, "Six rubrics are published in full in the workbook and issued to students before the relevant work is "
        "set. Across all of them, method, reasoning, validation and interpretation carry considerably more weight "
        "than the score achieved. A student whose model performs poorly but who correctly diagnoses why, and says "
        "so, should out-score a student who copies a public notebook to a better number. The project rubric "
        "allocates fifteen marks to problem definition, fifteen to data understanding, twenty to methodology, "
        "twenty to engineering reasoning, fifteen to validation, ten to communication and five to reproducibility.")
callout(d, "Apply the published criteria",
        "Execution, evidence and explanation earn their specified marks. Missing justification affects the "
        "relevant criterion; there is no unpublished whole-submission penalty based on a live answer. "
        "Individual typed defence and reflection are separate from shared project marks. Live questioning "
        "and peer comments are formative.", MID_H, LIGHT_H)

h2(d, "The policy on AI coding assistants")
para(d, "Banning these tools would be both unenforceable and professionally dishonest, since the students will use "
        "them throughout their careers. The policy is therefore to teach their use as a skill with a quality "
        "gradient, and to assess the students' capacity to explain and verify what the assistant produced. Four "
        "rungs are published in Week 1 and referenced all semester. Asking the assistant to write the whole "
        "assignment is poor use. Asking it to explain why an error is occurring is better. Asking it for three "
        "approaches to a cleaning problem with their trade-offs, and then choosing and defending one, is good. "
        "Asking it to review a pipeline for data leakage and then verifying the answer independently is advanced.")
para(d, "The rungs are introduced in sequence rather than all at once: error explanation in Week 3, comparing "
        "approaches in Week 6, and auditing a pipeline for leakage in Week 10, at which point the verification "
        "itself carries the marks. Use is permitted in all coursework, subject to a declaration logging the tool, "
        "the request and what the student changed. Use is prohibited in both practical tests, which run offline. "
        "The reasoning for the asymmetry is explained to students in Week 6 rather than announced on the day: "
        "coursework is where you learn to work with the tool and must defend the result; the tests certify what "
        "you can do unaided.")

# ================================================================ 8 (NEW)
page_break(d)
h1(d, "8. Making it markable: the auto-grading stack")

para(d, "The assessment workflow uses complete-cohort notebook execution, timed file uploads, local rubric assessment and ID-based grade imports. The operational implementation is in grader/. The companion Assessment Operations Plan gives setup and failure handling.")
h2(d, "Workload evidence")
from plan_content import MARKING_LOAD, TECH_STACK
table(d, ["Item","Volume","Illustrative human hours","Automated workflow hours"],
      [[r[0],r[1],str(r[3]),"Pilot pending" if r[4] is None else str(r[4])] for r in MARKING_LOAD],
      [32,28,20,20],bold_first=True)
para(d, "Before values are illustrative estimates. Measure model calibration, file retries and exception handling during the pilot; earlier fixed savings claims were unverified. The lecturer should not routinely read every submission.")
h2(d, "Implemented components")
for name,purpose,tool,cost,saving,limit in TECH_STACK:
    h3(d,name)
    para(d,purpose+" "+tool+". "+limit)
callout(d,"Record ownership and continuity",
        "Keep the roster and gradebook private. Export audit records and grades to an institution-controlled location after each block. Google sign-in email supports roster matching; local model input removes routine identifiers. No grading content is sent to an external AI provider.",MID_H,LIGHT_H)

# ================================================================ 9
h1(d, "9. Managing a hundred-student cohort")
para(d, "Cohort A is too large for sustained individual attention, and pretending otherwise is the fastest route "
        "to a failed semester. Four structural devices carry the load.")
para(d, "The first is teams of four to five, giving roughly twenty-two teams in Cohort A and ten to eleven in the "
        "others. Teams form in Week 1, are deliberately mixed by ability rather than by friendship, and persist "
        "all semester. Roles rotate at every project milestone — data analyst, machine learning engineer, domain "
        "engineer, documentation lead, presenter — so that no student occupies the same position twice.")
para(d, "The second is two-tier practicals. Every lab has a core tier that everyone must complete and a stretch "
        "tier for those who finish early, which means the fast students are extended rather than idle and the "
        "slower ones are not left behind by a single pace. The third is the floor-helper system: six to eight "
        "students identified early and recruited to help, briefed to ask questions rather than fix code. This is "
        "scaffolding and recognition at the same time, and it is what makes the Week 2 practical survivable.")
para(d, "The fourth is individual accountability inside team work, which rests on the sixty-five per cent "
        "individual mark, the contribution log with repository evidence, and two individual typed defence "
        "answers in Week 15. Shared project and individual marks remain separate; a live response does not "
        "silently rescale a team mark. The repository-history evidence route still requires validation.")
para(d, "Two sessions need explicit crowd logistics rather than good intentions. The Week 13 studio requires a "
        "published clinic booking sheet, because ninety-five minutes across twenty-two teams is about four "
        "minutes each and an unmanaged queue wastes the session. The Week 15 demonstration requires a fair "
        "format with two rounds and a plenary shortlist, because the fair itself is a hundred and thirty "
        "minutes with formative questioning running inside it: twenty-two consecutive six-minute demonstrations "
        "is a hundred and thirty-two minutes before a single question is asked, which leaves nothing for "
        "the plenary shortlist or the close. Running it as a fair also means every team "
        "presents four or five times to small groups rather than once to a room that has stopped listening.")

# ================================================================ 9
h1(d, "10. Tooling, and why each tool appears when it does")
para(d, "Students start from zero and must be taught the actual tools of the field, not merely the algorithms. The "
        "governing rule is that no tool is named before the problem it solves has been felt. This is what prevents "
        "the tool fatigue that afflicts introductory data science courses, where a beginner meets ten libraries in "
        "three weeks and retains none of them.")
table(d, ["Tool", "Week", "The problem it solves"],
      [["GitHub and Kaggle accounts", "1", "Where will my work live, and where will I find data?"],
       ["Python, VS Code, terminal, Jupyter, Git", "2", "Where do I write, run, debug, version and share code?"],
       ["VS Code debugger", "3", "How do I find out what my code is actually doing?"],
       ["Standard-library file reading", "4", "How do I read a data file at all? (Deliberately the hard way.)"],
       ["NumPy and pandas", "5", "How do I work with thousands of engineering measurements at once?"],
       ["Kaggle and the UCI repository", "5", "Where do I find data, and how do I judge whether to trust it?"],
       ["matplotlib and seaborn", "6", "How do I see my data — and see what is wrong with it?"],
       ["scikit-learn, core", "8", "How do I build a model that learns from examples?"],
       ["scikit-learn, classifiers", "9", "How do I get the machine to choose between categories?"],
       ["scikit-learn, validation and Pipeline", "10", "How do I know whether to trust my own model?"],
       ["scikit-learn, preprocessing", "11", "How do I feed the model what it can actually use?"],
       ["Hyperparameter search", "12", "How do I choose between models fairly?"],
       ["Environment capture and repository structure", "13", "How does someone else run my work next year?"],
       ["AI coding assistant", "3, 6, 10", "How do I get unstuck without outsourcing my thinking?"]],
      [40, 8, 52], bold_first=True)
spacer(d, 12)
para(d, "Deliberately absent from Semester 1: deep learning, PyTorch, OpenCV, transfer learning, time-series "
        "forecasting, retrieval-augmented generation, agents, MLOps, FastAPI and cloud deployment. Gradient "
        "boosting is shown for one minute in Week 12 and then explicitly deferred. All of it belongs to Semester "
        "2, and the students are told so, and told why.")

# ================================================================ 10
h1(d, "11. Dataset strategy")
para(d, "Each cohort has one anchor dataset that recurs across Weeks 1, 5, 6, 8 and 11, so that students meet the "
        "same data repeatedly at increasing depth rather than a fresh dataset every week. Familiarity with one "
        "dataset is what allows the conceptual difficulty to rise without the cognitive load rising with it.")
table(d, ["Cohort", "Anchor dataset", "Task", "Licence"],
      [["A", "Concrete Compressive Strength (UCI 165); Energy Efficiency (UCI 242) for the architecture stream",
        "Regression — strength in MPa; heating and cooling load", "CC BY 4.0"],
       ["B", "Quality Prediction in a Mining Process, froth flotation (Kaggle); FORCE 2020 well logs for the "
             "petroleum stream", "Regression — % silica in concentrate; lithology classification",
        "Kaggle page; CC BY 4.0 / NLOD 2.0"],
       ["C", "Combined Cycle Power Plant (UCI 294); AI4I 2020 Predictive Maintenance (UCI 601)",
        "Regression — power output in MW; machine failure classification", "CC BY 4.0"]],
      [7, 40, 32, 21], bold_first=True)
spacer(d, 12)
para(d, "All of these were confirmed to exist and to be openly licensed on 1 September 2026, and the workbook's "
        "dataset register records that status for every entry, flagging those named from knowledge but not "
        "verified. Two operational points matter more than the choice of dataset. First, every dataset is "
        "downloaded and staged on the local share at the start of the semester; nothing is fetched live in a "
        "classroom. Second, two of the anchors must be reduced before use — the flotation data runs to roughly "
        "seven hundred thousand rows sampled every twenty seconds, and the FORCE 2020 collection covers more than "
        "a hundred wells. Handing either to a five-week-old programmer guarantees failure, so subsetting to about "
        "twenty thousand rows and three wells respectively is preparation work, not an optional refinement.")
para(d, "Public datasets cannot do all of the teaching, however, and the register is explicit about what must be "
        "written from scratch. The Week 4 Investigation Lab file needs one genuine planted finding and two red "
        "herrings. The Week 6 damaged dataset needs six planted defects and two genuinely arguable extreme values. "
        "The Week 10 leakage notebooks need three different planted causes per cohort. And each practical test "
        "needs three matched unseen variants per cohort — nine per test, eighteen in total, each with a model "
        "answer and a mark scheme. These authored artefacts are the real preparation workload of the semester and "
        "should be scheduled now.")

# ================================================================ 11
page_break(d)
h1(d, "12. Risk register")
para(d, "The risks are recorded in full in the workbook with owners and mitigations. The seven that will most "
        "likely determine whether the semester runs as designed are summarised here, and the first three require "
        "action inside the first fortnight.")
table(d, ["ID", "Risk", "Mitigation"],
      [["R1", "Friday 9 October is Independence Day; both Friday cohorts lose the Week 5 pandas session.",
        "Secure a make-up slot, or publish a recorded walkthrough plus notebook by 7 October, run a 45-minute "
        "clinic, and open Week 6 with a 30-minute consolidation. Decide in Week 2."],
       ["R2", "Cohort A (~100) exceeds one lab's capacity, making the Week 7 and 14 tests unrunnable in a single "
              "sitting.",
        "Run the laptop-access survey in Week 1. Submit a written capacity request in Week 1. Plan two sittings "
        "with different variants. Confirm by Week 5."],
       ["R3", "Unreliable connectivity during Colab access and notebook uploads in Week 2.",
        "Use the small Colab kit and retain cohort ZIPs on USB/local share. "
        "Pre-provision lab machines. Recruit 6–8 floor helpers."],
       ["R6", "Free-riding in team projects.",
        "Retain individual marks and rotating roles. Require contribution evidence and submitted individual typed "
        "defence answers in Week 15. Live questioning is formative; repository evidence checks remain a release requirement."],
       ["R8", "Manual marking could exceed one lecturer's capacity; the workbook estimates are planning assumptions.",
        "Use the stack in Section 8 and measure calibration and exception handling during the pilot. Earlier fixed "
        "savings and authoring-cost estimates were unverified. Request support for measured access and exception-handling needs."],
       ["R13", "Google Forms cannot work offline. A network or power failure during a quiz costs that sitting "
               "for a whole cohort.",
        "Best 10 of 12 does not replace a fair attempt opportunity. Announce and configure an equivalent "
        "replacement window after an outage; retain the change reason and do not silently assign a zero. "
        "Printed questions support practice while verified collection is restored."],
       ["R15", "The current records are in a lecturer-owned Google account; confirm Faculty-approved arrangements.",
        "Confirm restricted records access and continuity with the Faculty. Collect registration numbers, verified "
        "email and required files. Uploads are in Google Drive; AI grading is local after download. Export records "
        "only to an approved restricted records location."]],
      [5, 40, 55], bold_first=True)

# ================================================================ 12
h1(d, "13. What to build next, and in what order")
para(d, "With the architecture agreed, materials can be produced against it. The sequencing below is ordered by "
        "when each item is first needed, not by how interesting it is to build, and it front-loads the items that "
        "block teaching. It assumes the 70/30 design is exploited — one preparation re-skinned three times.")
table(d, ["#", "Deliverable", "Needed by", "Note"],
      [["1", "Student Setup Guide, Week 2 Lecturer Runsheet and the setup/ toolkit — DONE", "Before Week 2",
        "Use the generated cohort ZIPs. Rehearse sign-in, CSV upload, saving and timed submission. Check the prepared lab fallback."],
       ["2", "Three cohort syllabi (drafted — see companion documents)", "Week 1",
        "Issued to students in the first session."],
       ["2b", "Gradebook installed; the Quiz 1 and Quiz 2 banks authored and built in Forms with their QR codes",
        "Week 1",
        "Code is written and tested. About 2 hours of gradebook setup plus 3.5 hours for the first two banks. "
        "Week 1 ends with a quiz, so this one cannot slip."],
       ["2c", "The remaining ten quiz banks, five questions each, built in Forms in three versions", "Weeks 3–13",
        "Author them in pairs, one or two weeks before each is sat. The Build Plan gives the schedule."],
       ["3", "Lesson plans and slides, Weeks 1–4", "Week 1", "Four sessions is enough of a lead to start teaching."],
       ["4", "Week 4 Investigation Lab files (three, one per cohort)", "Week 4",
        "Generated fictional cohort logs, four deterministic summaries and a formative interpretation task."],
       ["5", "Weeks 5–6 notebooks and the damaged datasets", "Week 5",
        "Includes subsetting the flotation and well-log data."],
       ["6", "Practical Test 1: nine dataset variants (three per cohort), mark schemes, offline bundle, "
             "auto-check script", "Week 6", "Build during Weeks 2–5. Do not leave to the week before."],
       ["7", "Lesson plans, slides and notebooks, Weeks 8–10", "Week 8",
        "Includes the three leakage notebooks per cohort."],
       ["8", "Project briefs, milestone checklists and the contribution log template", "Week 9",
        "The project launches in Week 9."],
       ["9", "Lesson plans and notebooks, Weeks 11–13, plus the Week 12 client briefs", "Week 11", ""],
       ["10", "Practical Test 2: nine dataset variants (three per cohort), mark schemes, offline bundle",
        "Week 13", "Build during Weeks 8–12."],
       ["11", "Week 15 viva question bank, peer assessment form, assessor packs", "Week 14", ""],
       ["12", "Semester 2 master plan", "Week 12",
        "Needed before the Week 15 preview, and while Semester 1 evidence is fresh."]],
      [5, 44, 14, 37], bold_first=True)
spacer(d, 12)
para(d, "One sequencing point is worth stating plainly, because it is the most common way a plan like this fails. "
        "The nine dataset variants for each assessment week — eighteen across the semester — are the largest "
        "single item of work and the easiest to defer. They must be built in the quiet weeks, Weeks 2 to 5 for the "
        "first test and Weeks 8 to 12 for the second, because the fortnight before an assessment week is precisely "
        "when there is no capacity to author nine datasets of matched difficulty and nine mark schemes.")

# ================================================================ 13
h1(d, "14. The bridge to Semester 2")
para(d, "Semester 1 answers one question: can I take an engineering dataset, analyse it, build a basic model, "
        "evaluate it and explain the result? Semester 2 answers a different one: how do I build more useful "
        "engineering solutions with this? It should extend rather than repeat, moving through advanced data "
        "preparation and pipelines, gradient boosting with tuning and explainability, time series and anomaly "
        "detection on sensor data, computer vision including transfer learning, and a properly bounded treatment "
        "of generative AI for engineering work. The capstone then runs across the final weeks.")
para(d, "Three design commitments should carry across. Tools continue to be introduced only in service of a "
        "problem, which is why gradient boosting is deferred out of Semester 1 despite being easy to demonstrate. "
        "The generative AI block must not become a course on how to use a chatbot; its value lies in retrieval "
        "over engineering documentation, verification, and the professional limits of the technology. And the "
        "cross-disciplinary challenge — an intelligent factory or campus monitoring system, with each cohort "
        "contributing the data its own discipline owns — belongs in Semester 2, because real engineering systems "
        "are multidisciplinary and a single cohort cannot experience that alone.")
para(d, "The Semester 2 calendar should be built from the university schedule once published, and the Week 15 "
        "reflection, which requires each student to name two goals for the second semester, is the natural input "
        "to its detailed design.")

# ================================================================ Appendices
h1(d, "Appendix A · The fifteen weeks at a glance")
table(d, ["Wk", "Block", "Topic", "Under-guided segment", "Quiz", "Milestone"],
      [["1", "Orientation", "The engineering problem that needs data", "Problem Hunt", "Quiz 1", "Teams formed"],
       ["2", "Orientation", "The development environment", "Break and Fix", "Quiz 2 · A2 proof",
        "Team repo created"],
       ["3", "Orientation", "Python as an engineering calculator", "Wrong Answer Hunt", "Quiz 3",
        "Function library"],
       ["4", "Orientation", "Collections, loops and files", "Investigation Lab 1", "Quiz 4",
        "Problem area chosen"],
       ["5", "Data", "NumPy, pandas, and where data comes from", "Ten Questions, No Help", "Quiz 5",
        "Data Analysis Project launched"],
       ["6", "Data", "Dirty data, and seeing it", "The Outlier Argument", "Quiz 6",
        "Cleaned data and charts"],
       ["7", "ASSESSMENT", "Practical Test 1 — Data Investigation", "The whole test", "—", "—"],
       ["8", "ML core", "Learning from data: the first model", "Beat the Baseline", "Quiz 7",
        "Data Analysis Project due"],
       ["9", "ML core", "Classification: predicting a category", "The 97% Trap", "Quiz 8",
        "ML Project launched"],
       ["10", "ML core", "Can I trust this model?", "Too Good To Be True", "Quiz 9",
        "PM1 — problem, data, baseline"],
       ["11", "Judgement", "Features: where engineering enters", "Domain Advantage", "Quiz 10",
        "PM2 — features and first model"],
       ["12", "Judgement", "Model comparison and judgement", "Choose a Model and Defend It",
        "Quiz 11 · integrative", "PM3 — comparison table"],
       ["13", "Project", "Reproducibility and peer review", "Peer review", "Quiz 12 · integrative",
        "PM4 — repo freeze"],
       ["14", "ASSESSMENT", "Practical Test 2 — End-to-End ML", "The whole test", "—", "—"],
       ["15", "Project", "Demo Day, viva and reflection", "The viva", "—", "Final submission"]],
      [4, 11, 29, 21, 15, 20], bold_first=True,
      shade_fn=lambda i, r: RED_H if r[1] == "ASSESSMENT" else None)

spacer(d, 20)
h1(d, "Appendix B · The graduate profile ladder")
para(d, "The ladder below is the outcome this plan is built to produce. It is worth putting on a slide in Week 1 "
        "and again in Week 15, because students find it far easier to see how far they have come when they were "
        "told at the outset where they were going.")
table(d, ["Stage", "The student can say", "Reached by"],
      [["Start", "“I have never programmed.”", "Week 1"],
       ["Foundation", "“I can write and run Python, and read an error message.”", "Week 4"],
       ["Data", "“I can load, clean, analyse and visualise engineering data.”",
        "Week 7 — certified by Practical Test 1"],
       ["Modelling", "“I can train a model and tell you honestly whether to trust it.”", "Week 10"],
       ["Judgement", "“I can choose an approach for an engineering problem and defend the choice.”", "Week 12"],
       ["End of semester",
        "“Give me an engineering problem involving data and I know how to start investigating it.”",
        "Week 15 — certified by Practical Test 2 and the project"]],
      [16, 60, 24], bold_first=True)

spacer(d, 18)
callout(d, "The philosophy, in one line",
        "Problem first. Tools second. Theory when needed. Build continuously. Challenge students to think "
        "independently.", NAVY_H, LIGHT_H)

d.save(OUT)
print("saved", OUT)
