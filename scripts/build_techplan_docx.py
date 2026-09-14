# -*- coding: utf-8 -*-
"""Assessment Technology Build Plan — Word document."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Assessment_Technology_Build_Plan.docx"

d = new_doc(margin_cm=2.3)
header_footer(d, "IUEA Faculty of Engineering · CML3111 / CML3112 / CML3113 · Assessment Technology Build Plan")
first_page_different(d)

# ---------------------------------------------------------------- title
spacer(d, 60)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=22)
para(d, "Assessment Technology", size=26, bold=True, colour=NAVY, align=AL.CENTER, after=2)
para(d, "Build Plan", size=26, bold=True, colour=NAVY, align=AL.CENTER, after=14)
p = para(d, "CONTINUOUS ASSESSMENT AND AUTO-GRADING FOR ~195 STUDENTS, ONE LECTURER",
         size=11, bold=True, align=AL.CENTER, after=8, before=8)
_border(p, "top", NAVY_H, 10)
_border(p, "bottom", NAVY_H, 10)
spacer(d, 16)
para(d, "CML3111 · CML3112 · CML3113   ·   Semester 1, 2026/2027", size=11.5, align=AL.CENTER, after=4)
para(d, "Free tools only   ·   No institutional LMS   ·   Offline-first by design",
     size=11.5, align=AL.CENTER, after=40)
para(d, "Companion to the Semester 1 Master Teaching Plan", size=9.5, bold=True, colour=GREY,
     align=AL.CENTER, after=3)
para(d, "Working code: the assessment-tools folder beside this document", size=9.5, colour=GREY,
     align=AL.CENTER, after=3)
para(d, "Operating detail, install steps and test-spec syntax: assessment-tools/README.md",
     size=9.5, colour=GREY, align=AL.CENTER, after=16)
para(d, "Version 1.0 · drafted 1 September 2026", size=9.5, italic=True, colour=GREY, align=AL.CENTER)
page_break(d)

h1(d, "Contents")
toc(d)
page_break(d)

# ================================================================
h1(d, "1. The problem this solves")
para(d, "The teaching design for these three courses is entirely practical: weekly notebook work, two offline "
        "practical tests, two team projects, and an individual viva. That is the right design for engineering "
        "students who need to be able to do something rather than recite it. Marked entirely by hand, it is also "
        "impossible for one person.")

table(d, ["Item", "Volume per semester", "Minutes each", "Hours"],
      [["Weekly practical challenges", "11 weeks × ~195 students = ~2,145 items", "3", "107"],
       ["Practical Test 1", "~195 scripts", "8", "26"],
       ["Practical Test 2", "~195 scripts", "8", "26"],
       ["Engineering ML Project and 4 milestones", "43 teams", "60", "43"],
       ["Data Analysis Project", "43 teams", "25", "18"],
       ["Demonstration, viva and reflection", "~195 students", "5", "15"],
       ["Gradebook reconciliation", "3 cohorts", "—", "10"],
       ["TOTAL", "", "", "246 h  ·  ≈16 h per week"]],
      [36, 33, 12, 19], bold_first=True,
      shade_fn=lambda i, r: RED_H if i == 7 else None)
spacer(d, 12)

para(d, "Sixteen hours of marking a week, on top of nine contact hours and the preparation of a course that does "
        "not yet exist, is not a workload that can be absorbed by working harder. Something in the design has to "
        "change. The three obvious options are all bad: cut the practical work and teach a theory course; mark "
        "less carefully and give feedback nobody can learn from; or move to a single written examination and "
        "abandon the point of the course.")

callout(d, "The fourth option, and the one taken here",
        "Automate the assessment that can be honestly automated — the high-volume, low-stakes, objectively "
        "checkable work — and spend the recovered time on the assessment that cannot be automated: engineering "
        "reasoning, validation, communication and judgement. The total falls from about 246 hours to about 120, "
        "roughly eight hours a week, for a one-off authoring cost of about thirty hours that is reusable in "
        "later years.", MID_H, LIGHT_H)

h2(d, "Where the saving actually comes from")
para(d, "This point is worth labouring, because it is counter-intuitive and it determines what gets built first. "
        "The QR-code weekly quizzes are the visible, appealing part of continuous assessment — and they are not where "
        "the saving comes from. They cost nothing to mark, but marking them was never the problem. The problem is "
        "the roughly 2,145 weekly practical submissions, and what removes about 97 hours of that is the notebook "
        "auto-grader, which is a different tool entirely and has no QR code anywhere near it.")
para(d, "The quizzes earn their place for other reasons, and they are good ones. A student gets feedback in "
        "minutes rather than a fortnight. The lecturer gets a weekly engagement signal across ~195 students that "
        "is otherwise completely invisible until the first test. And assessment weight can move away from the work "
        "that is expensive to mark, which is what makes the whole rebalancing possible. Both layers are worth "
        "having. Only one of them fixes the capacity problem.")

table(d, ["Item", "All human", "With the stack", "How"],
      [["Weekly practical challenges", "107 h", "10 h", "Layer B grades them; human time is spot checks only"],
       ["Weekly quizzes (new)", "—", "0 h", "Machine-scored on submission"],
       ["Practical Test 1", "26 h", "16 h", "Layer C marks 40 of the 100 marks; reasoning stays human"],
       ["Practical Test 2", "26 h", "16 h", "Layer C marks 45 of the 100 marks; reasoning stays human"],
       ["Projects, DAP, viva", "76 h", "76 h", "Irreducibly human — and the point of the course"],
       ["Gradebook", "10 h", "1 h", "Layer D"],
       ["TOTAL", "246 h", "120 h", "≈16 h/week becomes ≈8 h/week — 126 hours saved per semester"]],
      [30, 13, 16, 41], bold_first=True,
      shade_fn=lambda i, r: GREEN_H if i == 6 else None)

# ================================================================
page_break(d)
h1(d, "2. Architecture")
para(d, "Five layers, each doing one job, each independently replaceable. Nothing here is a bespoke application. "
        "Two layers are existing free products configured for this course; three are short scripts written for it "
        "and already tested.")

table(d, ["Layer", "Job", "Built on", "Status"],
      [["A · Weekly quizzes", "Deliver a five-minute, five-question diagnostic quiz by QR in the last five minutes "
        "of every teaching session; release the score and teaching feedback instantly",
        "Google Forms in quiz mode → Google Sheets",
        "Question banks for the first quizzes written; forms to build"],
       ["B · Notebook auto-grading", "Grade the weekly practical work; let students self-check before submitting",
        "assessment-tools/autograde.py — Python standard library only", "Written and tested"],
       ["C · Auto-marked test Part A", "Mark the objective portion of the two offline practical tests",
        "The same grader with a test-specific spec", "Grader ready; specs to write with the test variants"],
       ["D · Gradebook and reports", "Weighted totals, best-of rules, missing-submission flags, student standing "
        "emails", "assessment-tools/gradebook.gs — Apps Script on Google Sheets",
        "Written and unit-tested; needs installing"],
       ["E · Submission collection", "Pull every student's repository for a given week into one folder",
        "assessment-tools/pull_submissions.sh + Git and GitHub", "Written"]],
      [19, 33, 27, 21], bold_first=True)
spacer(d, 12)

h2(d, "Why the notebook grader was written rather than adopted")
para(d, "Two mature free autograders exist and both were considered. Otter-grader, from UC Berkeley, is excellent "
        "and generates the student notebook and the autograder from a single master file — but its containerised "
        "batch grading mode runs submissions in Docker, so it needs Docker installed and an image pulled. Its "
        "local mode avoids that. Nbgrader is equally respectable, needs no Docker, and can author and autograde "
        "without JupyterHub — but its collect-and-distribute exchange, which is the part that would actually save "
        "the file-handling time, does assume a JupyterHub deployment.")
para(d, "Neither assumption survives contact with this course. There is no JupyterHub, there is no institutional "
        "infrastructure at all, and asking a lecturer to depend on a Docker image pull on an unreliable connection "
        "in the week the marks are due is asking for the system to fail at the worst possible moment. The grader "
        "written for this course therefore uses nothing but the Python standard library: no Docker, no pip install, "
        "no server, no continuous-integration minutes, no network. A notebook is JSON, and executing it is a "
        "subprocess. It graded 195 notebooks in sixty-three seconds in testing.")
para(d, "The trade-off is honest and should be recorded. Student code runs unsandboxed on the lecturer's machine, "
        "which is exactly what nbgrader does too, but it is a real risk and the README says so. If Docker ever "
        "becomes easy to rely on here, otter-grader is the better long-term choice and the test specs would "
        "translate.")

h2(d, "The feature that changes student behaviour")
para(d, "The same test specification ships to students with the hidden tests withheld. A student runs one command "
        "on their own machine, offline, and finds out whether their notebook runs from a clean start and whether "
        "the basics are right — before the deadline, not a fortnight after it. The feedback is written to teach "
        "rather than to judge: not 'incorrect', but 'n_meters is 24, which is the number of rows; each meter "
        "appears once per month, so you want the distinct values in the meter_id column'.")
para(d, "This matters more than the marking saving. It removes the most common and most demoralising failure mode "
        "for a beginner — submitting work that does not run, and finding out too late to do anything about it.")

# ================================================================
page_break(d)
h1(d, "3. What is deliberately not being built")
para(d, "There is no custom web application here, no self-hosted quiz server, no mobile app and no student "
        "dashboard. That is a decision, not an omission.")
para(d, "Building software while teaching nine contact hours a week, authoring eighteen unseen test datasets and "
        "writing a course from scratch is a reliable way to lose the semester. Every hour spent debugging a web "
        "framework in October is an hour not spent on the Week 10 leakage notebooks, and the students will feel "
        "the second absence far more than the first. Everything in this plan is either an existing free product or "
        "a script short enough to read in one sitting.")
para(d, "One genuine gap should be stated rather than discovered in December: nothing in this stack detects "
        "plagiarism. With shared accommodation and shared wifi, near-identical notebooks will occur, and only the "
        "Week 15 viva and the two offline tests will catch it. If that becomes a visible problem, the cheapest "
        "response is not a tool but a policy already in the syllabus — a student is marked on what they can "
        "explain.")
callout(d, "A better use for the idea",
        "A student-facing progress dashboard, reading the gradebook and showing each student their standing and "
        "their weakest block, would make an excellent Semester 2 capstone project for a strong team. It is a real "
        "problem, the data already exists, the users are sitting in the room, and it is exactly the kind of "
        "'engineering problem involving data' the course promises to prepare them for. That is a far better use of "
        "the idea than lecturer time in Semester 1.", "2E5C8A", LIGHT_H)

# ================================================================
h1(d, "4. Build schedule")
para(d, "Ordered by when each piece is first needed. The total is about thirty-eight hours, of which roughly "
        "twenty-five is authoring question banks and test specs — content work that is reusable in later years, "
        "not throwaway configuration.")

table(d, ["When", "Task", "Hours", "Blocks what"],
      [["Before Week 1", "Run selftest.py on your own machine. Confirm 19 passed. Do this before trusting it with "
        "any real mark.", "0.5", "Everything downstream"],
       ["Before Week 1", "Author the Quiz 1 and Quiz 2 banks (five questions each), build both in Forms and "
        "generate their QR codes. Week 1 ends with a quiz, so this one cannot slip.", "3.5",
        "Weeks 1 and 2 quizzes"],
       ["Week 1", "Create the Google account structure and the three gradebook sheets. Install gradebook.gs, set "
        "the grade bands against IUEA regulations. Collect the roster.", "2", "Layer D"],
       ["Week 1", "Put the data-protection question to the Faculty in writing (see Section 7).", "0.5",
        "Nothing technically — but it gets harder to raise later"],
       ["Weeks 1–2", "Author the Quiz 3 and Quiz 4 banks and build them in Forms, three versions each, re-skinning "
        "two of the five questions per cohort. Print 20 paper copies of version A.", "4",
        "Weeks 3 and 4 quizzes"],
       ["Week 2", "Collect GitHub usernames with assignment A2; complete the roster CSV.", "0.5", "Layer E"],
       ["Weeks 2–3", "Write the test specs for Weeks 3, 4 and 5 practical work. The first one is the slow one.",
        "4", "Layer B going live"],
       ["Week 3", "First live grading run on real submissions. Expect to fix your own spec, not the students.",
        "1", "Trust in the whole system"],
       ["Weeks 3–4", "Author the Quiz 5 and Quiz 6 banks and build them in Forms.", "3.5",
        "Weeks 5 and 6 quizzes"],
       ["Weeks 5–6", "Write the Test 1 Part A structured-answer spec alongside the test variants.", "3",
        "Week 7 auto-marking"],
       ["Weeks 6–7", "Author the Quiz 7 and Quiz 8 banks and build them in Forms.", "3.5",
        "Weeks 8 and 9 quizzes"],
       ["Weeks 8–9", "Author the Quiz 9 bank. This is the highest-value one — leakage, metrics, trust.",
        "2.5", "Week 10 quiz"],
       ["Weeks 9–10", "Author the Quiz 10 bank.", "2", "Week 11 quiz"],
       ["Weeks 10–11", "Author the Quiz 11 and Quiz 12 integrative banks. Two of the five questions in each are "
        "drawn from the Week 1–10 banks, so they are cheaper to write.", "3", "Weeks 12 and 13 quizzes"],
       ["Weeks 12–13", "Write the Test 2 Part A spec alongside the test variants.", "3",
        "Week 14 auto-marking"],
       ["", "TOTAL", "≈38 h", ""]],
      [13, 47, 8, 26], bold_first=True,
      shade_fn=lambda i, r: LIGHT_H if i == 15 else None)
spacer(d, 12)
para(d, "The sequencing rule that matters: author the quiz banks in pairs, one or two weeks before they are "
        "needed, in the weeks where the teaching preparation is light. Quizzes 1 and 2 have to exist before the "
        "first session, because Week 1 ends with one. Weeks 2 and 13 require no cohort-specific teaching "
        "preparation at all, and Weeks 8 and 15 are low-divergence — those are the widest windows. Authoring a "
        "question bank in the week it is sat will produce recall questions, because good diagnostic questions take "
        "time to write and test.")

# ================================================================
page_break(d)
h1(d, "5. Designing quiz questions")
para(d, "This is the part of the system most likely to go wrong, and it will not go wrong technically. It will go "
        "wrong by the questions gradually becoming easier to write.")

callout(d, "The single rule",
        "Every question must show the student code, an output, a chart or a table, and ask them to diagnose or "
        "interpret it. If a question could be answered without reading the material shown, throw it away. "
        "'What is a for loop?' tells you the student read the slides. 'Here is a function and its output; the "
        "answer is wrong by a factor of a thousand — which line causes it?' tells you whether they can look at a "
        "broken thing and find out why.", "C00000", RED_H)

para(d, "The reason for the rule is not purity. It is that a recall question is trivially answerable by a phone "
        "search or a neighbour, and a diagnostic question is not — so the rule that protects the pedagogy also "
        "happens to protect the integrity. And it is aimed at a specific failure. In the Quiz 3 bank that "
        "has already been written, two of the five questions show code that runs cleanly and returns a wrong "
        "answer: a unit conversion wrong by a thousand, and a function that returns nothing because it prints "
        "instead. That is the hardest thing for a beginner to "
        "see, and it is precisely what will silently destroy their Week 10 model. One question shows a "
        "traceback and tests whether the student can read it, one supplies an output to interpret, and one "
        "sets a constraint and asks which choice follows from it. Five questions leave no room for a spare one, "
        "so every question in a bank has to carry a diagnosis.")

h2(d, "Structure of each bank")
table(d, ["Element", "Specification"],
      [["Length", "5 multiple-choice questions, 1 mark each, five minutes, sat in the last five minutes of the "
        "session"],
       ["Question mix", "Two questions on a silently wrong answer (40 of the marks), one traceback (20), one "
        "output to interpret (20), one judgement under a stated constraint (20)"],
       ["Delivery", "A QR code on the projector opens the Google Form; students answer on their own phones; "
        "auto-marked, with the score visible on submission"],
       ["Shared vs re-skinned", "3 questions shared across all three cohorts; 2 re-skinned per cohort with the "
        "discipline's own variables and units. Same logic, same distractors, different clothing."],
       ["Versions", "Three versions (A/B/C) per quiz, issued by seating column, with question and option "
        "order shuffled"],
       ["Distractors", "Every wrong option must be a diagnosis a real student would actually make. A distractor "
        "nobody would choose wastes a question."],
       ["Feedback", "Every wrong answer carries feedback that teaches the correct diagnosis, not the words "
        "'incorrect'. This is where the pedagogical value of the quiz actually lives."],
       ["Answer release", "Release the score and which questions were missed. Do NOT release correct answers — "
        "the other two cohorts have not sat it yet."],
       ["Integrative banks", "Quizzes 11 and 12, in Weeks 12 and 13, draw two of their five questions from the "
        "Week 1–10 banks. This is what keeps the set cumulative."],
       ["Week 2 does a second job", "One of the five questions in the Week 2 quiz asks the student to read the "
        "output of their own environment setup. That question carries the readiness signal, which is how you "
        "find out who is not yet running before Week 3 starts depending on it."],
       ["No resits", "A quiz is a single sitting. The two lowest of the twelve scores are dropped, and that is "
        "what covers illness, travel and a bad day."],
       ["Network failure", "The sitting converts to a 48-hour asynchronous window, and the class is told so "
        "before they leave the room."],
       ["Counting", "Best 10 of the 12 graded quizzes count, at 1% each."]],
      [20, 80], bold_first=True)
spacer(d, 12)

h2(d, "The ten minutes that are worth more than the marks")
para(d, "After each quiz, open the Responses-by-question view. A question that eighty per cent of the cohort "
        "got wrong is not a hard question; it is a topic you did not teach as well as you thought, and you have "
        "found out the same week rather than in Week 14. Reteach it in ten minutes at the start of the next "
        "session. Because there is a quiz every teaching week, this view refreshes weekly instead of five times "
        "a semester. This diagnostic use of the data is the strongest argument for the quizzes, stronger than "
        "either the marks or the workload, and it is the thing most likely to be skipped.")

# ================================================================
h1(d, "6. Integrity, honestly assessed")
para(d, "The quizzes are taken on personal phones, in one room, at one time. Collusion and lookup are possible "
        "and no free tool prevents them. The design accepts this rather than pretending otherwise, and compensates "
        "structurally.")
table(d, ["Measure", "What it does", "What it does not do"],
      [["1% per quiz", "Keeps the incentive to cheat small", "Does not stop a determined student"],
       ["Three shuffled versions by seating column", "Makes copying a neighbour's answer actively misleading",
        "Does not stop a group that coordinates"],
       ["Every question requires reading a snippet", "Much harder to shout across a room than a definition; "
        "resists a quick phone search", "Does not stop a student who understands it and helps a friend"],
       ["Correct answers never released", "Prevents an answer key circulating to the cohorts that sit it later",
        "Does not stop screenshots"],
       ["Five-minute window, form closed after", "Removes the option of finishing it later, in comfort", "—"],
       ["35% of the mark in two OFFLINE tests", "This is the real answer: unaided capability is certified where "
        "collusion is actually preventable", "—"],
       ["Divergence monitoring", "A student with strong quiz scores and weak tests is visible in the gradebook by "
        "Week 7, and should be spoken to before Week 14", "—"]],
      [26, 42, 32], bold_first=True)
spacer(d, 12)
callout(d, "The framing to give students",
        "The weekly quizzes reward keeping up. They do not certify competence. Say this out loud in Week 1, and "
        "say why: the two offline practical tests are where the course certifies what you can do unaided, and if "
        "your quiz scores are strong while your test scores are not, the quizzes were not doing you any good. "
        "Stated that way, most students stop treating them as something to beat.", MID_H, LIGHT_H)

# ================================================================
page_break(d)
h1(d, "7. Verified limits, and what to do about each")
para(d, "Every constraint below was checked rather than assumed. Each one shapes an operating decision, so none of "
        "them should be discovered in week eight.")

table(d, ["Limit", "Consequence", "Response"],
      [["Google Forms has no native timer",
        "You cannot set a five-minute limit inside the form",
        "Open the form, then switch off 'Accepting responses' after five minutes. Reliable, free, and it also gives "
        "you a hard stop you control."],
       ["Google Forms cannot work offline",
        "A network or power failure during a quiz costs that sitting for a whole cohort",
        "Three fallbacks: best 10 of 12 means two lost quizzes cost a student nothing; the sitting converts to a "
        "48-hour asynchronous window, and the class is told so before they leave; and 20 printed copies of version "
        "A live in the room. Never reschedule into the following week, because it collides with that week's own "
        "quiz."],
       ["A personal Google account cannot restrict one response per person",
        "A student could submit twice",
        "Make the student number a required first question and de-duplicate in Sheets, keeping the first response. "
        "The gradebook script does this."],
       ["A free Gmail account can email only ~100 recipients per day",
        "A standing-report mail-out to ~195 students cannot go in one run",
        "Run it over two days. The script checkpoints and resumes, so this is one extra click, not a rewrite."],
       ["Apps Script caps a single execution at ~6 minutes",
        "A long mail-out or a full recompute can time out",
        "Already handled by the checkpoint-and-resume design. Do not add long loops without the same pattern."],
       ["The grader's per-cell timeout is Unix-only",
        "On Windows, one hanging cell costs the whole notebook rather than one cell",
        "Grade on macOS or Linux. If Windows is unavoidable, the hard per-notebook timeout still protects the batch."],
       ["The grader cannot mark plots, prose or style",
        "Roughly a third of what the course values is invisible to it",
        "By design. That is what the 25% project, the 10% viva and the human halves of both tests are for. Do not "
        "try to close this gap with more auto-marking."],
       ["The grader depends on exact variable names",
        "A correct answer stored in the wrong variable name scores zero",
        "Every task sheet must state the required variable names in a box. Students self-check before submitting, "
        "so they find this out themselves rather than losing marks to it."],
       ["Student code runs unsandboxed on your machine",
        "A malicious or careless submission could damage files",
        "Grade in a dedicated folder, keep backups, and never grade as an administrator. Nbgrader has the same "
        "exposure; it is the accepted trade for not requiring Docker."],
       ["Nothing here detects plagiarism",
        "Near-identical submissions will occur and will not be flagged",
        "Accepted. The viva and the offline tests are the detection mechanism, and the 'marked on what you can "
        "explain' rule is the sanction."]],
      [24, 32, 44], bold_first=True)
spacer(d, 12)

h2(d, "The institutional question")
callout(d, "Raise this in Week 1, in writing",
        "IUEA has no institutional learning platform, so quiz responses and the gradebook for ~195 students' "
        "official marks will sit in a personal Google account belonging to one member of staff. That raises real "
        "questions of ownership, continuity and data protection, and they are much easier to raise in September "
        "than after the first test. Two interim measures are cheap and should happen regardless of the answer: "
        "export the Forms responses and the gradebook to the university's own course share as CSV at the end of "
        "every block, so the authoritative record is a file the institution holds; and collect student numbers "
        "rather than personal email addresses. State in the syllabus what is collected and where it goes. If an "
        "LMS arrives later, Layers A and D move onto it without touching Layers B, C or E.", "C55A11", AMBER_H)

# ================================================================
h1(d, "8. Weekly operating routine")
para(d, "The point of the whole system is that the recurring work is small and the same every week. Detailed "
        "commands are in assessment-tools/README.md; this is the shape of it.")
table(d, ["When", "What", "Time"],
      [["In the session", "Deliverable and required variable names on the last slide. In the last five minutes of "
        "every teaching week: QR up, form open five minutes, form closed, score distribution shown before they "
        "leave.", "2 min"],
       ["Monday morning", "Collect submissions with one command. Read the collection failures BEFORE grading — "
        "that is the step people skip. Grade with one command.", "3 min + ~1 min machine"],
       ["Monday", "Scan the results CSV. Hand-check only the rows the grader flags as unreadable or crashed. If "
        "the whole class failed one question, suspect your spec before you suspect 195 people.", "10 min"],
       ["Monday", "Return the per-student feedback files.", "2 min"],
       ["Every 2–3 weeks", "Compute totals, flag missing submissions, preview one email, send standing reports.",
        "5 min"],
       ["After each quiz", "Ten minutes on the responses-by-question view. Reteach whatever the cohort "
        "failed, at the start of the next session.", "10 min"],
       ["End of each block", "Export responses and gradebook to the course share as CSV.", "5 min"]],
      [17, 66, 17], bold_first=True)
spacer(d, 12)
para(d, "One habit is worth forming deliberately in Week 3: run the grader on the first real batch expecting to "
        "find a fault in your own test specification rather than in the students' work. It usually is your spec. "
        "Finding that out in Week 3, on work worth a fraction of a per cent, is how you come to trust the system "
        "by Week 7 when it is marking a test.")

# ================================================================
h1(d, "9. What this does and does not solve")
para(d, "It does solve the capacity problem. Marking falls from roughly sixteen hours a week to roughly eight, the "
        "recovered time goes to the assessment that needs a human, and students get feedback in minutes instead of "
        "weeks. It also makes forty per cent of the mark genuinely continuous, accumulated across eleven weekly "
        "submissions and twelve weekly quizzes, which is a much easier case to make to a faculty than two large "
        "events.")
para(d, "It does not make eight hours a week comfortable, on top of nine contact hours and the preparation of a "
        "course that does not yet exist. The residual should still be quantified in a written request in Week 1. "
        "It does not assess engineering reasoning — sixty-five per cent of the mark still depends on a human "
        "reading the work, and that proportion should be defended rather than eroded. It does not detect "
        "plagiarism. And it does not remove the authoring cost, which is real, front-loaded, and the thing most "
        "likely to slip.")
para(d, "The honest summary is that auto-grading buys back the time that repetitive marking was consuming, and "
        "buys nothing else. What that time is then spent on is the decision that will actually determine whether "
        "these three courses are any good.")

spacer(d, 14)
callout(d, "The rule to hold on to",
        "Automate the checking. Never automate the judgement.", NAVY_H, LIGHT_H)

spacer(d, 10)
para(d, "Build Plan version 1.0 · 1 September 2026 · tool limits verified at that date and worth re-checking "
        "before each semester.", size=9, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
