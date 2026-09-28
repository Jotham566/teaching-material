# -*- coding: utf-8 -*-
"""Weeks 2 and 3 as full 3-hour teaching material. Three cohorts."""
import sys, os
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from pptxkit import *   # noqa
from build_week1 import CO, FIG, OUTDIR, FOOT, qrp
from week_content import W3

F = lambda n: os.path.join(FIG, n)
NSEG2, NSEG3 = 11, 10
DATE = {2: {"CML3112": "Tue 15 September 2026", "CML3113": "Fri 18 September 2026",
            "CML3111": "Fri 18 September 2026"},
        3: {"CML3112": "Tue 22 September 2026", "CML3113": "Fri 25 September 2026",
            "CML3111": "Fri 25 September 2026"}}
SLOTS = {"CML3112": "Tuesday 11:00–14:00 · Room 106",
         "CML3113": "Friday 08:00–11:00 · Room 105",
         "CML3111": "Friday 11:00–14:00 · Room 115"}


# =====================================================================
def week2(code):
    c = CO[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 2")

    s = s_title(prs, code, "Where the work\nactually happens",
                "Colab, notebooks and version control", "WEEK 2  ·  " + DATE[2][code],
                SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Today you stop reading about this and start doing it. By the end of the session you will have run "
             "your own code, seen its output, and put it somewhere a marker can find it.\n\n"
             "You need three things: a browser, a Google account and a GitHub account. You do not need to "
             "install anything at all — that is deliberate.\n\n"
             "TO TEACH: read the Week 2 Lecturer Runsheet first. Confirm Room wifi before the session; with "
             "~100 students on Colab in Room 106 that is the single biggest risk. If Colab is unreachable, fall "
             "back to the offline bundle and lab machines — the runsheet has the contingency tree. Have the four "
             "Break and Fix notebooks ready to share.")

    s = s_objectives(prs, [
        "Open a notebook in Google Colab and run code in it without installing anything.",
        "Explain what a cell is, what the execution counter means, and what the kernel holds.",
        "Predict what happens when a cell is run twice, and say why that matters.",
        "Use Restart and Run All, and say what problem it solves.",
        "Explain what Git records that a backup does not.",
        "Create a repository, commit your work and push it, ending with a live URL.",
        "Read four different error messages and name the cause of each in one sentence."],
        2, "Colab, notebooks and version control")
    notes(s, "Seven objectives, and the fourth is the one that will save you the most time all semester.\n\n"
             "TO TEACH: read them out. Come back to this slide in the last five minutes and ask for a show of "
             "hands on each. It converts a busy practical session into visible progress.")

    s = s_figure(prs, "How today runs", F("clock_w2.png"),
                 "The same eleven-segment shape as last week. Today is heavier on practical work than any "
                 "session so far. Keep the cohort kit open for the practical activities.",
                 kicker="HOW TODAY RUNS")
    notes(s, "The same eleven-segment shape as Week 1, with more keyboard time than any session so far. The "
             "break falls at the midpoint, straight after the execution-trap segment.\n\nTO TEACH: say the "
             "break time out loud. In a practical session students will not ask, and they will start drifting "
             "out if they do not know when it is.")

    # -------- SEGMENT 1
    s = s_segment(prs, 1, NSEG2, "Where we got to, and where we are going", 10,
                  "A2 is due at the start of next week, and by the end of today you will already have most of "
                  "it.")
    notes(s, "Ten minutes of recall before any new material. A2 is due at the start of Week 3, and by the end "
             "of today most of it is already built.\n\nTO TEACH: collect A1 at the door. Then two minutes of "
             "recall — do not re-teach it.")

    s = s_check(prs, [
        "Last week you predicted case 13 from twelve examples. What was the name for the input columns you "
        "were given, and what was the name for the value you predicted?",
        "You want to predict how many days until a pump needs servicing. Regression or classification?",
        "Name one of the four limits — one thing machine learning cannot do."],
        title="Two minutes: what stuck from Week 1?",
        foot="Answers next slide. Ask a neighbour first — that is faster than waiting for me.")
    notes(s, "These three answers are the vocabulary the rest of the semester assumes. If you cannot answer "
             "them, the Week 1 deck's glossary slide has all of it in one place.\n\n"
             "TO TEACH: thirty seconds in pairs, then take answers from three different people rather than the "
             "first hand up.")

    s = s_answers(prs, [
        ("The input columns, and the value?",
         "The columns you were given are the FEATURES. The value you predicted is the TARGET. One row with "
         "both is one EXAMPLE."),
        ("Days until servicing?",
         "Regression — the answer is a number with a unit. If it were 'service due or not' it would be "
         "classification."),
        ("One of the four limits?",
         "No data · no signal · physics is simply better · the future stopped resembling the past. Any one of "
         "those.")])
    notes(s, "Features, target, example: those three words are the vocabulary every later week assumes. If the "
             "first question was hard, the Week 1 deck's data-table figure and glossary slide have all of it in "
             "one place, and half an hour on them this evening is worth more than anything else you could "
             "revise.\n\nTO TEACH: if more than a third of the room struggles with the first one, spend three "
             "minutes re-showing the Week 1 data-table figure. Everything from Week 5 assumes it and it is "
             "cheaper to fix now.")

    # -------- SEGMENT 2
    s = s_segment(prs, 2, NSEG2, "Four questions, four tools", 20,
                  "Nobody memorises tools. You need to know which one answers which question — and each of "
                  "today's four answers a different one.")
    notes(s, "Each of today's four tools answers a different question, and the question is the part to "
             "remember. Meeting ten libraries in three weeks and retaining none is the standard way an "
             "introductory data course fails; knowing which question each tool answers is what stops it "
             "happening to you.\n\nTO TEACH: introduce every tool by its question, never by its name.")

    s = s_figure(prs, "The four questions", F("tool_map.png"),
                 "Four separate problems, four separate tools. You will use all four every week for the rest of "
                 "the year, and you will not need a fifth this semester.",
                 kicker="THE TOOL MAP")
    notes(s, "Read it as four questions rather than four products. The question is the durable part — the tool "
             "that answers it will change during your career, and the question will not.\n\n"
             "TO TEACH: if asked about VS Code — it is the professional local editor and the Student Setup "
             "Guide covers it. Anyone who wants a local setup is welcome. Note that the Week 7 and Week 14 "
             "tests run offline on lab machines, so everyone meets a local environment at least once.")

    s = s_define(prs, "Google Colab",
                 "A notebook that runs in your browser, on Google's computers. Python and every library this "
                 "course needs are already installed on it.",
                 "You open colab.research.google.com, sign in with a Google account, and you are running Python "
                 "about fifteen seconds later. Nothing is installed on your own machine.",
                 "A website that teaches Python. Colab is not a tutorial — it is the real tool, and "
                 "professional engineers use it for exactly this kind of work.")
    notes(s, "The reason this course uses Colab is bandwidth and time. A hundred students installing Python, "
             "an editor and five libraries over one campus connection does not work; it has to be attempted to "
             "be believed.\n\nThe honest limitation: Colab needs an internet connection. That is why the two "
             "practical tests in Weeks 7 and 14 are sat offline on lab machines instead, and why the Setup "
             "Guide still exists for anyone who wants a local installation.\n\n"
             "TO TEACH: say the limitation out loud now rather than letting them discover it in Week 7.")

    # -------- SEGMENT 3
    s = s_segment(prs, 3, NSEG2, "Your first notebook", 30,
                  "Everybody types. This is not a demonstration you watch — open a browser now.")
    notes(s, "Thirty minutes with your hands on the keyboard. Open a browser now — this segment does not work "
             "as something you watch.\n\nTO TEACH: lockstep, projected, everyone typing along. Do NOT hand out "
             "a finished notebook at this stage; the typing is where the structure is learned. Circulate "
             "constantly and watch for students who have not got Colab open at all.")

    s = s_livecode(prs, "Three cells", "OPEN COLAB — NEW NOTEBOOK — TYPE THIS",
                   ('# Cell 1 - press Shift and Enter together to run it\n'
                    'print("Hello from ' + code + '")\n'
                    'print(2 + 2)\n'
                    '\n'
                    '# Cell 2 - a variable is a name for a value\n'
                    'readings = 12\n'
                    'print(f"I have {readings} readings")\n'
                    '\n'
                    '# Cell 3 - run THIS one three times and watch both numbers\n'
                    'readings = readings + 5\n'
                    'print(f"readings is now {readings}")'),
                   "Run cell 3 three times and watch the number it prints. You have not changed a single "
                   "character, so an unchanging cell giving a changing answer is worth explaining. Hold that "
                   "thought — it is the whole of the block on execution order.")
    notes(s, "Three cells, and each teaches one thing. Cell 1: code runs and produces output underneath it. "
             "Cell 2: a name can hold a value, and that value survives into the next cell. Cell 3: running the "
             "same cell twice is not the same as running it once.\n\n"
             "The f in front of a string is what lets you put a variable inside the text — anything in "
             "{curly braces} is replaced by that variable's value.\n\n"
             "TO TEACH: type it yourself on the projector, do not paste. Narrate as you go. When someone's "
             "cell 3 gives a different number from their neighbour's, that is the moment the execution-order block pays off — "
             "note who noticed.")

    s = s_prose(prs, "The three things that go wrong in the first ten minutes", [
        "**You pressed Enter instead of Shift and Enter**",
        "Enter gives you a new line inside the cell. Shift and Enter runs it. This catches almost everybody once.",
        "**Nothing appears underneath the cell**",
        "Either the cell has no print in it, or it has not finished running. A cell that is still running shows "
        "a spinning circle to its left instead of a number.",
        "**Colab asks you to sign in, or to connect**",
        "Sign in with your Google account. 'Connect' means Colab is allocating you a machine and takes a few "
        "seconds — it is normal and it is not an error.",
        "**And one thing that is not a problem**",
        "A warning in yellow is not an error. Errors are red and they stop the cell. Yellow means Python is "
        "telling you something and carrying on regardless.",
        "**If you are stuck for more than five minutes**",
        "Put your hand up. Do not sit quietly and do not restart your laptop hoping. Say three things: what you "
        "were trying to do, what you typed, and what it said back."],
        kicker="TROUBLESHOOTING")
    notes(s, "Every item on this slide came from a real beginner making that mistake in a real first session. "
             "Shift-and-Enter alone accounts for a large share of the first ten minutes. Keep the slide in view "
             "while you work rather than reading it once, because it answers most of what goes wrong before you "
             "have to ask anybody.\n\nTO TEACH: put this slide up and leave it up during the practical rather "
             "than reading it aloud. It answers most questions before they are asked, which frees you to help "
             "the students who have a real problem.")

    s = s_define(prs, "Markdown cell",
                 "A cell holding text rather than code. It is where you write down what you are doing and why, "
                 "in among the code that does it.",
                 "A heading saying 'Question 3: does fly ash change strength?', then the code that answers it, "
                 "then a sentence saying what the answer was. Anyone reading it — including you in November — "
                 "can follow the reasoning.",
                 "A comment. A comment explains one line to someone reading the code; a markdown cell explains "
                 "the reasoning to someone reading the document.")
    notes(s, "This is what makes a notebook better than a script for data work: the reasoning lives beside the "
             "calculation instead of in a separate report nobody updates.\n\nIn Colab, press the + Text button "
             "instead of + Code. A # at the start of a line makes it a heading; ** around words makes them "
             "bold.\n\nFrom Week 5 your submitted notebooks are marked partly on whether a reader can follow "
             "them, so this is not optional polish.\n\nTO TEACH: two minutes. Have them add one text cell "
             "above each code cell in the notebook they just built, saying what it does.")

    s = s_check(prs, [
        "You press Enter at the end of a line in a code cell and nothing runs. Why?",
        "You wrote print(\"hello\") in a cell and ran it. Where does the word hello appear?",
        "Your neighbour's cell 3 says 27 and yours says 17. Neither of you has changed the code. Who is wrong?"],
        title="Thirty seconds: check you are with me",
        foot="Answers next slide. Do not look yet.")
    notes(s, "Three quick questions to confirm you are still with the session. Question C is the interesting "
             "one: two people running identical code and getting different numbers is a real property of "
             "notebooks, and the execution-order block explains why.\n\nTO TEACH: this is a pulse check, not an assessment. "
             "Take it verbally and quickly — the point is to catch anyone who has been quietly lost for twenty "
             "minutes.")

    s = s_answers(prs, [
        ("Enter did nothing?",
         "Enter adds a new line inside the cell. Shift and Enter together runs it. This catches almost "
         "everybody once."),
        ("Where does 'hello' appear?",
         "Directly underneath that cell, in the output area. Not in a separate window — a notebook keeps the "
         "code and its output together, which is the whole point of it."),
        ("27 versus 17 — who is wrong?",
         "Neither. They have run the cell a different number of times. That is not a difference of opinion, it "
         "is a property of how notebooks work — and it is the subject of the execution-order block.")])
    notes(s, "Answer C sets up the next segment. Two notebooks holding identical code can hold different "
             "values, because the kernel remembers how many times each cell has been run and the screen does "
             "not show you that history. Neither person is wrong; the notebook is simply not telling you "
             "everything it knows.\n\nTO TEACH: if someone in the room has already noticed this discrepancy in "
             "their own work, name them when you reach the execution-order block. It lands far better coming from a student.")

    # -------- SEGMENT 4
    s = s_segment(prs, 4, NSEG2, "What a notebook actually is", 20,
                  "You have used one for half an hour. Now here is what is underneath it, because the next "
                  "segment depends on understanding this.")
    notes(s, "Twenty minutes away from the keyboard, and the only concept block in the session. The execution-order block "
             "depends on it, because the execution trap only makes sense once you know what the kernel is "
             "holding on your behalf.\n\nTO TEACH: keep it to twenty minutes and get them back on keyboards.")

    s = s_figure(prs, "The anatomy of a notebook", F("notebook_anatomy.png"),
                 "Cells hold either text or code. Code cells produce output directly beneath them. The number "
                 "in brackets counts how many pieces of code you have run since the notebook started. All the "
                 "cells share one memory, called the kernel.",
                 kicker="ANATOMY")
    notes(s, "The kernel is the part worth understanding properly. It is a single Python session sitting behind "
             "the whole notebook, so a variable made in cell 2 is available in cell 7 because both cells are "
             "talking to that one session. The cells themselves have no connection to each other.\n\nThis is "
             "also why a notebook can lie to you. The kernel remembers everything you have run in the order you "
             "ran it, and that order need not match the order the cells appear on screen.\n\nTO TEACH: draw the "
             "kernel on the board as a box that all the cells write into. Drawn beats projected for this one.")

    s = s_define(prs, "Cell, kernel, and the execution counter",
                 "A CELL is one block of text or code. The KERNEL is the single Python session that all cells "
                 "share. The EXECUTION COUNTER is the number in brackets beside a code cell, showing the order "
                 "in which things were actually run.",
                 "If the cell at the top of your notebook shows [7] and the one below it shows [3], you ran "
                 "them out of order — and any answer that depends on both is suspect.",
                 "The order the cells appear on screen. That is a layout; the counter is the truth.")
    notes(s, "Watch the execution counter. It is the single most useful diagnostic in a notebook and almost no "
             "beginner looks at it.\n\nA notebook where the counters run 1, 2, 3, 4 top to bottom is a notebook "
             "you can trust. Anything else needs checking.\n\nTO TEACH: have them look at their own counters "
             "right now. Several will already be out of order from experimenting, which makes the point better "
             "than any explanation.")

    # -------- SEGMENT 5
    s = s_segment(prs, 5, NSEG2, "The trap, and the habit that saves you", 20,
                  "The most common way a notebook gives a confident wrong answer — and the one keystroke that "
                  "prevents it.")
    notes(s, "Twenty minutes on the most common way a notebook produces a confident wrong answer, and on the "
             "one menu item that prevents it. If you take a single habit out of Week 2, take this one.\n\nTO "
             "TEACH: this is the highest-value twenty minutes of the session. If you are running late, take the "
             "time from the repository walkthrough rather than from here.")

    s = s_figure(prs, "The same cell, run three times", F("execution_trap.png"),
                 "The code never changed. Not one character. The answer went 17, then 22, then 27, because the "
                 "cell adds five to whatever is already in the box and puts it back. Restart and Run All takes "
                 "it back to 17.",
                 kicker="THE EXECUTION TRAP")
    notes(s, "This is why `readings = readings + 5` behaves the way it does: the right-hand side is worked out "
             "first, using whatever is currently in readings, and the result is then put back into readings. Run "
             "it three times and you have added fifteen.\n\nThe habit: **Restart and Run All** before you "
             "believe any answer. It clears the kernel and runs every cell from the top in order, which is "
             "exactly what your marker's machine will do.\n\nFrom Week 5 your submitted work is graded by a "
             "program that does precisely this from a clean start. If your notebook only works in the order you "
             "happened to click, it does not work.\n\nTO TEACH: let the room discover it before you explain. "
             "Ask 'is the notebook broken?' and wait. Someone will get there.")

    s = s_check(prs, [
        "A notebook's cells show, top to bottom, the counters [4], [1], [5], [2]. What does that tell you, and "
        "would you trust its final answer?",
        "You run Restart and Run All and the notebook now fails on cell 6 with an error, though it 'worked' "
        "five minutes ago. What was almost certainly true before you restarted?",
        "Why is Restart and Run All a better test than just re-running the one cell you changed?"])
    notes(s, "Question B is the one to take slowly. It is the realisation that 'it worked' can be an illusion "
             "produced by execution order, and that restarting is what turns the claim into evidence.\n\nTO "
             "TEACH: ninety seconds in pairs, then take B properly.")

    s = s_answers(prs, [
        ("Counters [4], [1], [5], [2]?",
         "They were run out of order, so the kernel's memory does not match what the notebook looks like. Do "
         "not trust the final answer until you have restarted and run all."),
        ("It fails after restarting?",
         "Cell 6 was depending on something created by a cell that has since been changed or deleted — or on a "
         "cell further down that you happened to run earlier. It never actually worked from a clean start; the "
         "kernel was just still holding the leftovers."),
        ("Why restart rather than re-run one cell?",
         "Because re-running one cell keeps everything else the kernel is holding, including things that no "
         "longer exist anywhere in your code. Only a restart proves the notebook can produce its results from "
         "nothing but itself — which is what reproducibility means.")])
    notes(s, "Answer B describes the most common way submitted work loses marks: the notebook ran for you and "
             "then failed for the marker. Every automated grader and every colleague runs code from a clean "
             "start, which is the whole reason the restart habit is asked for here.\n\nTO TEACH: say plainly "
             "that this is not a rule you invented to be difficult. It is how every automated grader and every "
             "colleague will run their code.")

    s = s_worked(prs, "Diagnosing a notebook from its counters",
                 "The reasoning, step by step. A classmate says their notebook 'stopped working' and "
                 "shows you this: the cells read, top to bottom, [2], [7], [3], and cell 4 is blank.",
                 # One line each. The longer version of every step is in the
                 # teaching-guide notes below, which is where it belongs: at
                 # projector size these five ran to 11pt on the slide.
                 ["Read the counters: 2, then 7, then 3. Not run top to bottom.",
                  "Cell 4 is blank, so it never ran. Anything needing it will fail.",
                  "[7] before [3] means they jumped down and came back up. The kernel "
                  "keeps the last write to each name.",
                  "The only useful question: does this notebook produce its results "
                  "from nothing but itself?",
                  "Restart and Run All. Whatever breaks now is a real problem you can fix."],
                 "The diagnosis is almost never 'the notebook is broken'. It is 'the notebook was never run in "
                 "the order it is written in', and the fix is one menu item.")
    notes(s, "This is the diagnostic routine to use for the rest of your degree. Counters out of order, or a "
             "blank counter, mean the notebook and the kernel disagree, and the kernel is what actually "
             "ran.\n\nStep 4 is the question that matters. A result you cannot reproduce from a clean start is "
             "indistinguishable from a coincidence, which is why reproducibility gets treated as an engineering "
             "requirement in this course.\n\nTO TEACH: walk it slowly. Then ask a student to read out their own "
             "counters and diagnose their own notebook, which makes it real.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. Git comes after the break and it needs you awake.\n\nTO TEACH: take it. Ninety "
             "minutes in, attention is genuinely gone, and Git needs them awake.")

    # -------- SEGMENT 7
    s = s_segment(prs, 7, NSEG2, "What version control gives you", 25,
                  "What Git records that a copy of a folder does not — and why this course submits everything "
                  "through it.")
    notes(s, "Twenty-five minutes on what Git records that a copied folder does not. The commands come later; "
             "this segment is about the problem they solve, because Git treated as ceremony never gets used "
             "voluntarily.\n\nTO TEACH: lead with the problem, not the commands. Students who do not understand "
             "what Git is FOR treat it as ceremony and never use it voluntarily.")

    s = s_prose(prs, "The problem Git actually solves", [
        "**What a backup gives you**",
        "Yesterday's version of the file. One version, and only if you remembered.",
        "**What you actually need, repeatedly**",
        "Which lines changed between Tuesday and Thursday. Who changed them. Why — because a good message says "
        "why. And the ability to go back to the version that worked, without having kept a folder called "
        "'final_v3_REAL_final'.",
        "**What it gives a team of five**",
        "Five people editing the same project without overwriting each other, and a record of who did which "
        "part.",
        "**Which is why it is in this course at all**",
        "Sixty-five per cent of your mark is individual, and two of your assessments are team projects. The "
        "commit history is how a team mark becomes an individual one. It is not administrative — it is the "
        "evidence that you did your share.",
        "**And it is what industry uses**",
        "Many engineering software teams use version control. Today you practise the basic workflow."],
        kicker="VERSION CONTROL")
    notes(s, "The 'final_v3_REAL_final' folder is a problem everybody recognises, and Git is the tool built for "
             "it. The assessment consequence is the part to take seriously: your commit history is the evidence "
             "of which part of a team project you did, and sixty-five per cent of your mark is "
             "individual.\n\nTO TEACH: that line usually gets a laugh because everyone has done it — use it, "
             "the problem is familiar even though the solution is not. Be explicit about the assessment "
             "consequence; students engage with Git far more readily once they understand it is how their "
             "individual contribution is seen.")

    s = s_figure(prs, "The four places your work can be", F("git_states.png"),
                 "Your files move left to right through four states, and one command moves them between each. "
                 "git status tells you where things currently are — run it constantly until it becomes "
                 "automatic.",
                 kicker="THE FOUR STATES")
    notes(s, "Most Git confusion comes from not knowing which of these four places a file is in. The diagram is "
             "worth photographing.\n\nThe staging area feels like a pointless extra step until the first time "
             "you want to commit two of the five files you changed. That is what it is for.\n\n"
             "TO TEACH: 'git status' is the single most useful command in the list. Tell them to run it before "
             "and after everything for the first fortnight.")

    s = s_define(prs, "Repository, commit, and push",
                 "A REPOSITORY is a project folder whose entire history Git is tracking. A COMMIT is one "
                 "recorded snapshot with a message saying what changed. To PUSH is to send your commits to "
                 "GitHub so they exist somewhere other than your laptop.",
                 'git commit -m "Add ' + c["derivcol"] + ' column" records a snapshot with that message. Six weeks '
                 'later that message is the only thing that tells you what you did.',
                 "Saving. Saving overwrites; committing adds a version and keeps every earlier one.")
    notes(s, "Commit messages matter more than beginners expect. 'update', 'fix' and 'stuff' are worthless in "
             "November. A message should say what changed and, where it is not obvious, why.\n\n"
             "TO TEACH: show one good and one useless commit message side by side on the board. It takes thirty "
             "seconds and it changes their habits for the semester.")

    # -------- SEGMENT 8
    s = s_segment(prs, 8, NSEG2, "Doing it: repository, commit, push", 25,
                  "Whole room in lockstep. Everyone finishes with a live repository URL and keeps a downloaded notebook and README for A2.")
    notes(s, "Twenty-five minutes with the whole room in step. You leave this segment with a live GitHub URL, "
             "and submit that URL together with the notebook and README.md for A2.\n\nTO TEACH: lockstep on the projector, line by line, "
             "everyone at the same step. Individually this takes three times as long and half the room ends up "
             "lost. Do not let the fast students run ahead.")

    s = s_livecode(prs, "From Colab to GitHub", 'GITHUB: UPLOAD AND COMMIT',
                   ('# Browser route used today:\n#   Colab: download your completed .ipynb\n#   GitHub: create a private repo with README\n#   Add file -> Upload files: notebook and CSV\n#   Commit changes, then edit your README\n\n# The command route, for when you work locally later:\ngit status                     # what have I changed?\ngit add .                      # mark it all ready\ngit commit -m "First commit"   # record it, with a message\ngit push                       # send it to GitHub'),
                   'Use GitHub in the browser today: upload your files and commit the changes. The commands above are optional local-terminal reference, not Python cells.')
    notes(s, "Colab can save straight to GitHub from the File menu, which is why today needs no command line at "
             "all. The four commands are shown because you will need them from Week 13, when the project has to "
             "be reproducible, and because every job you apply for expects them.\n\n"
             "TO TEACH: do the menu route with the whole room first so everyone has a URL. Then demonstrate the "
             "four commands once on the projector. Do not make them use the command line today — it doubles the "
             "failure surface for no gain.")

    s = s_split(prs, "Assignment A2 — Proof of Life", "Due at the start of Week 3",
                'Submit the notebook, README.md and repository URL through the A2 form.\n\nKeep the CSV in your repository. Upload only your notebook and README.md.\n\nExplain what changed when you repeated a cell, and what Restart and Run All does. Record one error you repaired.',
                "Before you submit",
                ["Restart and Run All.",
                 "It must finish with no errors.",
                 "",
                 "Save with the outputs showing.",
                 "",
                 "Repository name:",
                 "  " + code.lower() + "-yourstudentnumber",
                 "",
                 "Paste the repository URL into the A2 form.",
                 "",
                 "20 marks using the published rubric."],
                kicker="WHAT YOU OWE ME")
    notes(s, 'The honesty sentence is the part that is actually useful. A new reader should be able to open your files and reproduce the result. Test your README instructions before submitting.\n\nRedo is not a penalty. It means come to office hours this week, because Week 3 assumes a working setup.\n\nTO TEACH: the exact repository name matters — the grading tools pull repositories by name from a roster. State it and put it on the board.')

    s = s_prose(prs, "What makes a README worth reading", [
        "**It is the front door of your repository**",
        "It is the first thing a marker, a colleague or a future employer sees. An empty one says the work was "
        "not finished even when it was.",
        "**Four things, for A2**",
        "Your course code and program; keep personal identifiers in the submission form.",
        'The exact notebook and CSV filenames in your repository.',
        'How to open the notebook, upload the CSV and run cells from the top.',
        'How to restart, Run all, save and download the finished notebook.',
        "**Keep the README practical**",
        'Keep it short, but include the file list and run instructions. A new reader should be able to repeat your steps.',
        '**Why the run instructions matter**',
        'A new reader should be able to open your files and reproduce the result. Test your README instructions before submitting.'],
        kicker="THE README")
    notes(s, "README files are written in markdown — the same format as the text cells you just used. A # makes "
             "a heading and ** makes bold.\n\nTO TEACH: show one good and one empty README on the projector. "
             "Thirty seconds, and it visibly changes what gets submitted.")

    # -------- SEGMENT 9
    s = s_challenge(prs, "Break and Fix",
                    "Four notebooks are shared with you. Every one is broken. In your team, diagnose each and "
                    "write the cause in ONE sentence.\n"
                    "Three of them throw an error. One does not — it runs cleanly and gives a wrong answer. "
                    "That fourth one is the one that matters.",
                    ["What does the LAST line of the error say?",
                     "What was it looking for?",
                     "Where did it look?",
                     "Which cells ran, and in what order?",
                     "Is the answer even plausible?",
                     "How would you have caught this yourself?"])
    notes(s, "Three of the four notebooks throw an error and one does not. The fourth runs cleanly and returns "
             "a wrong answer, and it deserves your last three minutes. An error tells you something is wrong "
             "and roughly where; a clean wrong answer tells you nothing at all, and it is the failure that "
             "costs a model in Week 10 and marks in the Week 14 test. Work the six questions in order rather "
             "than guessing, and pay attention to which cells ran and in what order.\n\nTO TEACH: the four "
             "planted faults: (1) an import of a package that is not installed; (2) a notebook reading a file "
             "by a path that is only correct from a different folder; (3) a cell that uses a variable created "
             "in a cell further down, so it only works if you run them out of order; (4) cells saved after "
             "being run out of order, so it produces a confident wrong number with no error at all. Fault four "
             "is the one to spend the last three minutes on. Circulate and ask only the six questions. Do not "
             "diagnose for them. Build the notebooks before the session; the runsheet has the specification.")

    # -------- SEGMENT 10
    s = s_points(prs, "Before you leave the room",
                 [("This week's quiz — five minutes, and it counts for one per cent",
                   "A QR code goes up, you answer five questions on your phone, and you see your score "
                   "after submission. The questions check notebook state, version control and error diagnosis."),
                  ("Assignment A2 — due at the start of Week 3",
                   "Upload the notebook and README, and provide the repository URL. Restart and Run All first.")],
                 kicker="QUIZ AND ASSIGNMENT", numbered=False)
    notes(s, "Answer the setup question honestly. 'I could not get that far' is worth more to me than a "
             "guess, and it is not the question that carries the mark.\n\nTO TEACH: read the setup question's "
             "responses first. Anyone answering 'I do not know what is wrong' or 'I could not get that far' "
             "is your office-hours list this week, and that list is the highest-return thirty minutes of the "
             "semester. Question bank: scripts/quiz_bank_weeks.py, Week 2.")

    # -------- REVISION
    s = s_segment(prs, 11, NSEG2, "Revision material", 5,
                  "Everything from here is for you to study from — summary, self-test with answers, glossary "
                  "and a one-page reference.")
    notes(s, "Everything past this slide is revision material: a summary, a self-test with worked answers, an "
             "eighteen-term glossary and a one-page command reference. It is written to be studied from during "
             "the week.\n\nTO TEACH: say that the deck continues past the end of the session. Students do not "
             "read past the last slide you present unless told to.")

    s = s_summary(prs, [
        "Google Colab runs Python in your browser on Google's computers. Nothing is installed on your machine, "
        "and it needs an internet connection.",
        "A notebook is made of cells. Code cells produce output beneath them; the number in brackets shows the "
        "order things were actually run.",
        "All cells share one kernel — a single Python session. That is why a variable made in one cell exists in "
        "another, and why order matters.",
        "Running the same cell twice is not the same as running it once. Restart and Run All is the only honest "
        "test of a notebook.",
        "Git records every version, what changed, and who changed it. A backup gives you yesterday's file; Git "
        "gives you the history.",
        "Four states, four commands: working directory, git add, staging, git commit, local repository, git "
        "push, GitHub. git status tells you where you are.",
        "Three of today's four broken notebooks announced their problem. The fourth did not, and that is the "
        "kind you have to catch yourself."])
    notes(s, "Seven statements covering the whole session. The fourth and the seventh are the two that carry "
             "into every later week: Restart and Run All as the only honest test, and the broken notebook that "
             "never announces itself.\n\nTO TEACH: return to the objectives slide after this and ask for a show "
             "of hands against each.")

    s = s_check(prs, [
        "A classmate says their notebook 'worked yesterday' but fails today. What is the first thing you would "
        "ask them to do, and why?",
        "What does the number in brackets beside a code cell tell you that the cell's position on the page does "
        "not?",
        "You changed five files but only want to record two of them. Which Git command lets you choose, and "
        "which state do the two files move into?",
        "Why does this course submit work through GitHub rather than by email?",
        "Colab needs an internet connection. Given that, how are the Week 7 and Week 14 practical tests run, "
        "and why?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question E is worth thinking about properly. It is the trade-off at the centre of how this course "
             "is set up.")

    s = s_answers(prs, [
        ("'It worked yesterday'?",
         "Restart and Run All. Almost always the kernel was holding something from a cell that has since "
         "changed or been deleted, so it never really worked from a clean start."),
        ("What the counter tells you?",
         "The order in which cells were actually executed. Position on the page is only a layout — the counter "
         "is what the kernel actually did, and the two can disagree."),
        ("Recording two of five files?",
         "git add, naming just those two files rather than using a dot. They move into the staging area, and "
         "only staged files go into the next commit."),
        ("Why GitHub rather than email?",
         "Because it records who did what and when, which is how a team mark becomes an individual one; because "
         "the grading tools collect work from repositories automatically; and because it is what every "
         "engineering employer expects you to have used."),
        ("Colab needs internet — so how are the tests run?",
         "Offline, on laboratory machines with a local Python installation and no network. That is deliberate: "
         "it makes the no-AI-assistance rule actually enforceable rather than a request, and it certifies what "
         "you can do unaided. It is also why the Student Setup Guide still exists.")])
    notes(s, "Answer E is the trade-off at the centre of how this course is set up. Colab removes every "
             "installation problem and needs a connection to work; the offline lab machines make the no-AI rule "
             "in the two tests enforceable rather than a request. Both compromises are deliberate, and they are "
             "why the Student Setup Guide still exists for anyone who wants a local installation.\n\nTO TEACH: "
             "answer E is the one to read aloud. Students respect being told the reasoning behind a rule rather "
             "than just the rule.")

    s = s_glossary(prs, [
        ("Google Colab", "A notebook environment that runs in a browser on Google's computers, with Python and "
                         "the course libraries already installed."),
        ("Notebook (.ipynb)", "A document made of cells, mixing text, code and the code's output."),
        ("Cell", "One block of a notebook. Either markdown (text) or code."),
        ("Markdown", "The simple text format used for the text cells."),
        ("Kernel", "The single Python session that all the cells in a notebook share."),
        ("Execution counter", "The number in brackets beside a code cell, showing the order cells were run in."),
        ("Restart and Run All", "Clear the kernel and run every cell from the top. The only honest test of a "
                                "notebook."),
        ("Output", "Whatever a code cell produced, shown directly beneath it."),
        ("f-string", 'Text with holes in it: f"I have {n} readings". Anything in braces is replaced by that '
                     'variable\'s value.'),
        ("Git", "A tool that records every version of a project, what changed and who changed it."),
        ("GitHub", "A website that stores Git repositories so your work exists somewhere other than your laptop."),
        ("Repository (repo)", "A project folder whose whole history Git is tracking."),
        ("Working directory", "Your files as they are right now, changes included."),
        ("Staging area", "The set of changes you have marked as ready to go into the next commit."),
        ("Commit", "One recorded snapshot, with a message saying what changed."),
        ("Push", "Send your commits up to GitHub."),
        ("git status", "Ask Git what has changed and where it currently is. The most useful command on the list."),
        ("README", "The file that explains a repository to whoever opens it. Yours is marked."),
    ], page="1 of 1")
    notes(s, "Eighteen terms, and all of them are used every week from now on. If you can define them all by "
             "Week 4 you are in good shape — several appear in the weekly quizzes.")

    s = s_prose(prs, "One-page reference — the commands and the habits", [
        "**Running code**",
        "Shift and Enter runs a cell. Enter alone just adds a line inside it.",
        "**Before you believe any answer**",
        "Restart and Run All. If it fails, it was never working — the kernel was covering for you.",
        "**Before you submit anything**",
        "Restart and Run All, confirm no errors, then save with outputs visible.",
        "**The four Git commands**",
        "git status — what changed, and where is it?\ngit add . — mark it all ready\n"
        'git commit -m "message" — record it\ngit push — send it to GitHub',
        "**Writing a commit message**",
        "Say what changed, and why if it is not obvious. 'Add " + c["derivcol"] + " column' is useful in "
        "November. "
        "'update' is not.",
        "**Reading an error**",
        "Last line first. It names the error type and what Python actually wanted. Then look at the line number.",
        "**Asking for help**",
        "What you were trying to do, what you typed, what it said back. Those three things, in that order."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide. It answers most of what comes up in Weeks 3 to 6, and the four Git "
             "commands on it are the same four you will still be using on the project in Week 13.")

    s = s_quiz(prs, 2,
               "Out-of-order execution, what Restart and Run All proves, and reading one git status output.", qr_path=qrp(code, 2))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "Every error today told you\nexactly what it needed.",
                  "Everything you saw go wrong today has gone wrong for every engineer in this building, "
                  "including me, this week. The skill is not avoiding errors — it is reading them and carrying "
                  "on.",
                  "Next week: Python as an engineering calculator, using formulas you already know.")
    notes(s, "Everything you saw go wrong today has gone wrong for every engineer in this building, and it will "
             "keep happening for the rest of your career. What changes is how long it takes you to read the "
             "message and carry on. Next week is Python as an engineering calculator, built on formulas from "
             "your own programme.\n\nTO TEACH: say the body text out loud and mean it. For a room of beginners "
             "this is the most useful thing they hear all week. Then stay behind for ten minutes — the students "
             "who need the most help will not ask in front of everyone.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week02_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week3(code):
    c = CO[code]
    w = W3[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 3")

    s = s_title(prs, code, "Python as an\nengineering calculator",
                "Variables, decisions, functions — and reading errors",
                "WEEK 3  ·  " + DATE[3][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Everything today runs on formulas you already know from your own programme. The syntax rides "
             "along on familiar content, which is why this week works even though it is your first real "
             "programming session.\n\nTO TEACH: check A2 at the door — repository URL, notebook runs, README "
             "present. Anyone without a working setup goes on the office-hours list now, not in Week 5.")

    s = s_objectives(prs, [
        "Explain what the equals sign actually does in Python, and why it is not equality.",
        "Use integers, floats, strings and booleans, and say what goes wrong when they are mixed.",
        "Write a function with parameters, a docstring, stated units and a return value.",
        "Turn a formula from your own discipline into a function, and test it against a value you already know.",
        "Write conditional logic that encodes an engineering decision rule.",
        "Read a Python traceback and name the line and the cause.",
        "Recognise a wrong answer that produced no error at all — and say how you would have caught it."],
        3, "Python as an engineering calculator")
    notes(s, "The last objective is the one this whole week is built around. It matters more than any piece of "
             "syntax, and it comes back in Week 10 when a leaking model reports a beautiful score.\n\n"
             "TO TEACH: read them out, and return to this slide at the end.")

    # -------- SEGMENT 1
    s = s_segment(prs, 1, NSEG3, "Where we got to", 10,
                  "You can run code and put it on GitHub. Today you make it calculate something you care about.")
    notes(s, "Ten minutes of recall, then the new material. You can already run code and push it to GitHub; "
             "today it starts calculating something from your own discipline.\n\nTO TEACH: two minutes of "
             "recall, then move. Do not re-teach Week 2.")

    s = s_check(prs, [
        "What does Restart and Run All do, and why would you bother?",
        "A cell shows [7] and the cell above it shows [3]. Should you trust the notebook's final answer?",
        "Which Git command tells you what has changed and where it currently is?"],
        title="Two minutes: what stuck from Week 2?",
        foot="Answers next slide.")
    notes(s, "If the first question feels shaky, the Week 2 deck has a cheat-sheet slide with Restart and Run "
             "All on it. Get that habit settled before Week 5, when submitted notebooks start being run from a "
             "clean start by a program rather than by you.\n\nTO TEACH: thirty seconds in pairs. If the first "
             "question is shaky, the Week 2 deck's cheat-sheet slide has it.")

    s = s_answers(prs, [
        ("Restart and Run All?",
         "Clears the kernel and runs every cell from the top in order. It is the only honest test that your "
         "notebook produces its results from nothing but itself."),
        ("[7] above [3]?",
         "No. They were run out of order, so the kernel's memory does not match what the notebook looks like."),
        ("Which command?", "git status. Run it constantly until it is automatic.")])
    notes(s, "All three of these are Week 2 material and all three get used today. git status especially: run "
             "it before and after everything for the first fortnight, until you stop having to think about it.")

    # -------- SEGMENT 2
    s = s_segment(prs, 2, NSEG3, "Why write down a formula you already know?", 15,
                  "A fair question, and it deserves a real answer before you spend three hours on it.")
    notes(s, "The objection in this segment is a fair one and it gets a real answer. For a single calculation a "
             "calculator is faster, and the case for writing the formula down begins as soon as there is more "
             "than one calculation to do.\n\nTO TEACH: take the question seriously. A calculator IS faster for "
             "one calculation, and pretending otherwise loses you the sceptics in the room — who are usually "
             "the best students.")

    s = s_question(prs, "TODAY STARTS WITH AN OBJECTION", '"' + w["why"] + '"',
                   "For one " + w["noun"] + ", a calculator is faster. The answer is what happens when it is not one " + w["noun"] + ".")
    notes(s, "Try answering the objection yourself before you turn the page. The commonest answer, 'because you "
             "can do it lots of times', is exactly right, and the four reasons on the next slide expand it into "
             "something you can use in an argument with a colleague.\n\nTO TEACH: ask the room for the answer "
             "before you give it. Someone usually says 'because you can do it lots of times', which is exactly "
             "right and better received from a student.")

    s = s_prose(prs, "Four honest reasons, and one that matters more than the others", [
        "**1 · You will do it four hundred times**",
        "Not once. Once per " + c["unitid"].split("_")[0].lower() + ", per hour of data. From Week 5 the same formula is applied "
        "to a column of ten thousand rows in one line.",
        "**2 · It is inspectable**",
        "A number on a calculator screen carries no record of how it was produced. A function states its "
        "inputs, its units and its logic, and anyone can check it — including you, in six months.",
        "**3 · It is testable**",
        "You can feed it a case where you already know the answer and confirm it agrees. You cannot test a "
        "calculation you did in your head.",
        "**4 · When the standard changes, you fix one line**",
        "Not forty spreadsheets, of which you will find thirty-eight.",
        "**And the one that matters most**",
        "From Week 8 the computer starts working out relationships you did not give it. You will not be able to "
        "check that work unless you are already fluent at expressing relationships yourself. This week is the "
        "foundation for trusting — or refusing to trust — a model later."],
        kicker="WHY BOTHER")
    notes(s, "Reason three is the habit that matters most: feed the function a case whose answer you already "
             "know and confirm it agrees. Every practical from here on is marked partly on that, so it is worth "
             "building now. The last reason is why this week exists at all — from Week 8 the computer starts "
             "working out relationships you never supplied, and you cannot check that work without being fluent "
             "at expressing relationships yourself.\n\nTO TEACH: labour reason three. Make the Week 10 "
             "connection explicitly; students engage far better with syntax when they can see what it is for.")

    # -------- SEGMENT 3
    s = s_segment(prs, 3, NSEG3, "Variables and types", 25,
                  "Two ideas, and the second one causes more beginner bugs than anything else in this course.")
    notes(s, "Twenty-five minutes on two ideas. The second one, types, causes more beginner bugs than anything "
             "else in this course, and it is learned by writing code rather than by reading about it.\n\nTO "
             "TEACH: twenty-five minutes is enough. They learn this by writing it, not by hearing it.")

    s = s_figure(prs, "What the equals sign actually does", F("variable_box.png"),
                 "It is not equality. It means: work out the value on the right, then put it into the box named "
                 "on the left. Assign to the same name again and the old value is simply gone.",
                 kicker="VARIABLES")
    notes(s, "This is the single most common early misunderstanding, and it matters because "
             "`readings = readings + 5` is nonsense as an equation and perfectly sensible as an instruction.\n\n"
             "Read it right to left: take what is in readings, add five, put the result back.\n\n"
             "TO TEACH: draw the box on the board and physically write a value into it, then rub it out and "
             "write another. Thirty seconds, and it lands better than any slide.")

    s = s_define(prs, "The four types you need this week",
                 "An INT is a whole number. A FLOAT has a decimal point. A STR is text, in quotes. A BOOL is "
                 "True or False. Python decides which you have from how you wrote it.",
                 "thickness = 0.25 is a float. count = 12 is an int. name = \"Bridge 4\" is a string. "
                 "passed = True is a boolean.",
                 "What the value looks like on screen. \"12\" with quotes is text and you cannot do arithmetic "
                 "with it — which is exactly the error you will hit in Week 4 when you read a file.")
    notes(s, "The last line is a forward reference on purpose. Everything read from a file arrives as text "
             "until you convert it, and meeting that idea now makes Week 4's crash make sense rather than feel "
             "arbitrary.\n\nTO TEACH: demonstrate \"12\" + 3 live and let them read the error. It is the same "
             "TypeError they will see next week.")

    s = s_prose(prs, "Three arithmetic traps, and how to see them coming", [
        "**Integer division**",
        "In Python 3, 7 / 2 is 3.5 — a float, as you would expect. But 7 // 2 is 3, because the double slash "
        "throws the remainder away. Use it deliberately or not at all.",
        "**Operator precedence**",
        "Python follows the same rules you already use: brackets, then powers, then multiply and divide, then "
        "add and subtract. a + b / 2 is not (a + b) / 2. When in doubt, put the brackets in — they cost "
        "nothing and they document your intent.",
        "**Floats are approximations**",
        "0.1 + 0.2 prints 0.30000000000000004. That is not a bug; it is what binary fractions do, in every "
        "language, and it is why you compare with a tolerance rather than with equals when it matters.",
        "**And the trap that is not arithmetic at all**",
        "Units. Python has no idea whether 0.25 is metres or millimetres. It will multiply " + w["unit_trap"] +
        " together without a murmur and hand you a confident wrong answer. Write the unit in a comment beside "
        "every value you define — every single one — and you will catch most of these before they happen."],
        kicker="WHAT GOES WRONG")
    notes(s, "The float behaviour is worth being precise about. 0.1 + 0.2 printing 0.30000000000000004 is the "
             "same phenomenon as a third having no exact decimal form, and it happens in every language that "
             "stores numbers in binary. The units point is the one that will actually cost you marks: Python "
             "has no idea what unit your number is in and it will never ask.\n\nTO TEACH: demonstrate 0.1 + 0.2 "
             "live. It reliably produces an audible reaction and it makes the point permanently.")

    # -------- SEGMENT 4
    s = s_segment(prs, 4, NSEG3, "Turning your formula into a function", 25,
                  "Everybody types. We build " + w["fname"] + " together, line by line.")
    notes(s, "Twenty-five minutes with everyone typing. The function is built one line at a time, with the unit "
             "of every value written down as it is defined. That ordering is the habit being taught, and it is "
             "what the function-library practical is marked against.\n\nTO TEACH: type it live, do not paste. "
             "Narrate the units as you go. The typing is where the structure is learned.")

    s = s_figure(prs, "The parts of a function", F("function_anatomy.png"),
                 "Six parts, and one thing worth noticing: nothing happens when Python reads the definition. "
                 "The recipe is only written down. It runs when you call it.",
                 kicker="ANATOMY")
    notes(s, "The definition-versus-call distinction accounts for a large share of 'my code does nothing' "
             "reports. A beginner writes a perfect function, never calls it, and concludes Python is broken.\n\n"
             "The docstring — the text in triple quotes — is not decoration. It is where you state what the "
             "function does and what units it expects, and it is marked in this course.\n\n"
             "TO TEACH: ask 'what will this print?' after typing only the definition. Answer: nothing. Let that "
             "land before you add the call.")

    s = s_worked(prs, "Turning a formula into a function, step by step",
                 "The reasoning, before we type anything. This is the routine to use for every formula you "
                 "convert for the rest of the course.",
                 ["Write the formula down in words first, with its units. What goes in, what comes out, and in "
                  "what unit is the answer?",
                  "Decide what varies and what does not. The things that vary become parameters; the things "
                  "that do not can stay as values you define once.",
                  "Name it for what it does. " + w["fname"] + " tells a reader what comes back; calc does not.",
                  "Write the docstring before the body. If you cannot say in one line what it returns and in "
                  "what unit, you are not ready to write it.",
                  "Write the body as a single return statement wherever you can. One formula, one line.",
                  "Test it against a value you already know — from your notes, a worked example, or by hand. "
                  "If you cannot state the expected answer, you cannot tell whether the function is right."],
                 "Step 6 is the one that gets skipped, and it is the one that catches every bug in the Wrong "
                 "Answer Hunt later today.")
    notes(s, "Step 1 sounds trivial and is not. Most beginner function bugs come from starting to type before "
             "deciding what the function is for, and they surface as wrong answers rather than as syntax "
             "errors. Step 4, writing the docstring first, works the way a specification does: a requirement "
             "you cannot state clearly produces a confused implementation.\n\nTO TEACH: do steps 1 to 4 on the "
             "board, out loud, before opening Colab. It takes three minutes and it makes the live-coding "
             "segment much faster because the thinking is already done.")

    s = s_livecode(prs, w["fname"] + " — type this with me", "OPEN COLAB — NEW NOTEBOOK", w["code"],
                   w["mistake"])
    notes(s, "Expected output:\n    " + w["out"] + "\n\nEvery value has its unit in a comment beside it. That "
             "comment is the only defence you have against the trap in the box below the code.\n\n"
             "TO TEACH: type it, run it, confirm the output matches. THEN make the deliberate mistake and let "
             "the wrong number sit on screen for a few seconds before anyone speaks. Ask: what would have told "
             "you this was wrong? Physical intuition. The computer had no opinion about it.")

    s = s_define(prs, "return and print",
                 "RETURN hands a value back to whoever called the function, so it can be used. PRINT puts "
                 "characters on the screen and hands back nothing.",
                 "result = " + w["callex"] + " only works because the function returns. If it printed "
                 "instead, volume would hold None and the next line would fail.",
                 "Each other — and this is the commonest structural mistake in beginner code. A function that "
                 "prints gives you something to look at. A function that returns gives you something to work "
                 "with.")
    notes(s, "From Week 5 you will apply your functions to a whole column of data at once. A printing function "
             "is useless for that: it would print ten thousand lines and produce no column.\n\nA function may "
             "of course do both, but if it only prints, it is a dead end.\n\nTO TEACH: demonstrate it. Change "
             "the return to a print, run the same script, and show the TypeError two lines later when it tries "
             "to multiply None. That error is worth meeting on purpose.")

    s = s_check(prs, [
        "thickness = 0.25, then thickness = 0.30. What is in thickness now, and what happened to 0.25?",
        "You need to work out whether 7 divided by 2 should be 3.5 or 3 in your calculation. Which operator "
        "gives which?",
        "Why write the unit in a comment beside every value, when Python ignores comments entirely?"],
        title="Two minutes: check the foundations",
        foot="Answers next slide. Write something for each first.")
    notes(s, "Three questions on the foundations before the break. Question C is the one to dwell on, because "
             "it is the theme of the whole week and the answer is on the next slide.\n\nTO TEACH: quick pulse "
             "check before the break. Question C is the one to dwell on if the answers are weak.")

    s = s_answers(prs, [
        ("thickness after two assignments?",
         "0.30. The 0.25 is gone entirely — assignment replaces, it does not accumulate. There is no history "
         "in a variable."),
        ("7 / 2 versus 7 // 2?",
         "A single slash gives 3.5, a float. A double slash gives 3, throwing the remainder away. Use // only "
         "when you actually want whole units — a number of bags, a number of bars — and never by accident."),
        ("Why comment the units?",
         "Because Python ignores them and you do not. The computer will happily multiply millimetres by metres "
         "and hand you a confident answer that is wrong by a factor of a thousand. The comment is for the only "
         "part of the system that can catch that: you.")])
    notes(s, "Answer C is the sentence to carry for the rest of the semester. Python ignores your unit comments "
             "and you do not, and the comment exists for the only part of the system able to catch a "
             "factor-of-a-thousand error, which is you.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. The practical after the break is the long one, at 35 minutes.\n\nTO TEACH: take it. "
             "The practical after the break is the long one.")

    # -------- SEGMENT 6
    s = s_segment(prs, 6, NSEG3, "Encoding a decision rule", 15,
                  "You already write engineering decision rules. An 'if' statement is just notation for them.")
    notes(s, "Fifteen minutes. You already write engineering decision rules — thresholds out of a code of "
             "practice, pass and fail bands, alarm set points — and an if-statement is notation for what you "
             "already do. This is the left-hand column from Week 1: the rule you write yourself.\n\nTO TEACH: "
             "keep this short. The concept is easy; the value is in connecting it to Week 1.")

    s = s_livecode(prs, "A rule you already know, written down", "READ IT BEFORE YOU RUN IT",
                   w["decision"],
                   "Change the first threshold to be larger than the second and run it. Nothing errors, and "
                   "some inputs now return the wrong action because the first branch catches them. Order "
                   "matters in an if-chain, and getting it wrong is silent.")
    notes(s, w["dec_note"] + "\n\nAn if-chain is checked top to bottom and stops at the first match. That is "
             "why the strictest condition goes first — reverse them and the strict branch becomes "
             "unreachable.\n\nelse is the catch-all. Leave it out and a case that matches nothing returns None, "
             "which will confuse you later.\n\nTO TEACH: make the ordering mistake live. It is the same class "
             "of failure as the unit error — no crash, wrong answer.")

    # -------- SEGMENT 7
    s = s_segment(prs, 7, NSEG3, "Reading an error", 15,
                  "Errors are the most useful output Python produces. Most beginners do not read them at all.")
    notes(s, "Fifteen minutes on reading tracebacks. Most beginners do not read them at all, which is "
             "expensive, because the message usually names both the type of problem and the line it happened "
             "on.\n\nTO TEACH: this fifteen minutes saves more student time than any other in the semester.")

    s = s_figure(prs, "The anatomy of a traceback", F("traceback_anatomy.png"),
                 "Read the last line first. It names the error type and what Python actually wanted. Then look "
                 "up one line for the code that failed, and at the line number for where it is.",
                 kicker="TRACEBACKS")
    notes(s, "The word 'traceback' means it is tracing back through the calls that led to the problem. For your "
             "code this week it will usually be two or three lines long.\n\nThis exact error — adding text to a "
             "number — is the one you will hit in Week 4 when you read a file, because everything read from a "
             "file arrives as text.\n\nTO TEACH: the format shown is Python 3.10. If Colab is on 3.11 or later "
             "there is one extra line with a ~~~^~~ marker pointing at the failing part of the expression, "
             "which is helpful rather than confusing. Say so if a student's output differs.")

    s = s_prose(prs, "The five errors you will actually meet this week", [
        "**NameError**",
        "You used a name Python has never seen. Usually a typo, or a cell you did not run.",
        "**TypeError**",
        "You did something to a value its type does not allow — most often arithmetic on text.",
        "**SyntaxError**",
        "Python could not even read the line. Look for a missing bracket, quote or colon, and check the line "
        "ABOVE the one it blames.",
        "**IndentationError**",
        "The spacing at the start of a line is wrong. Python uses indentation to decide what is inside what.",
        "**ZeroDivisionError**",
        "Exactly what it says. Usually a variable you expected to have a value and which is zero.",
        "**And the one with no name**",
        "No error at all, and the answer is wrong. Python cannot help you here. This is what the next segment "
        "is about, and it is the whole point of the week."],
        kicker="FIVE NAMES, AND ONE WITHOUT")
    notes(s, "One trap in that list: a SyntaxError often points at the line after the real problem. An unclosed "
             "bracket is reported on the next line down, so when Python blames a line that looks perfect, check "
             "the line above it. The last entry on the slide has no name and no error message, and the next "
             "segment is about it.\n\nTO TEACH: produce each of the five live if you have time; at minimum "
             "produce NameError and TypeError. Seeing them made on purpose removes most of their power to "
             "frighten.")

    s = s_worked(prs, "Working through an error you have never seen before",
                 "You will meet errors this course never mentioned. This is the routine, and it works on all "
                 "of them.",
                 ["Read the LAST line. It names the error type and what Python actually wanted. Everything "
                  "above it is context.",
                  "Read the line of your code that it quotes. Not the line you think is wrong — the line "
                  "Python says failed.",
                  "Say out loud what you expected that line to be working with. 'I expected width to be a "
                  "number.' Often the error is already obvious at this point.",
                  "Check that assumption. Print the thing just before the failing line: print(width), "
                  "print(type(width)). Most bugs die here.",
                  "If it is still unclear, search the exact error message — the last line, in quotes, without "
                  "your variable names. Somebody has had it before.",
                  "If you use an AI assistant, paste the error AND your code and ask it to explain the cause. "
                  "Do not ask it to rewrite your function — you will learn nothing and you have to be able to "
                  "explain what you submit."],
                 "Step 4 is where most bugs are actually found: print the thing, look at it, and check it is "
                 "what you assumed.")
    notes(s, "print(type(x)) is the most underused diagnostic available to a beginner. It answers 'is this a "
             "number or is it text?', which is the cause of a large share of first-year errors.\n\nOn step 6 — "
             "the course policy is that AI assistants are permitted and taught in coursework, with a short "
             "declaration of what you asked and what you changed, and prohibited in the two practical tests, "
             "which run offline. You are marked on what you can explain.\n\nTO TEACH: this is the first formal "
             "introduction of the AI ladder from the syllabus. 'Explain why this error is happening' is the "
             "level for Week 3; asking for whole functions is not.")

    # -------- SEGMENT 8
    s = s_segment(prs, 8, NSEG3, "Practical: a function library for your own discipline", 35,
                  "Five functions from your own field, each with units stated and each tested against a value "
                  "you already know.")
    notes(s, "Thirty-five minutes building five functions from your own field. The expected value comes first: "
             "work out by hand what each function should return before you run it. A formula you cannot state "
             "an expected answer for is a formula you have not understood yet, and syntax help will not repair "
             "that.\n\nTO TEACH: circulate and ask for the EXPECTED value before you look at anyone's code. A "
             "student who cannot state it has not understood the formula.")

    s = s_split(prs, "What to build", "Five functions, and what each one needs",
                "A name that says what it does.\n\n"
                "A docstring stating what it returns and in what unit.\n\n"
                "The unit of every parameter, in a comment.\n\n"
                "A return value — not a print.\n\n"
                "Two test values with the answer you expect, worked out by hand or from your notes.\n\n"
                "CORE: five working functions.\n"
                "STRETCH: make one refuse a physically impossible input with a clear message.",
                "Suggested formulas",
                [("• " + x) for x in w["formulas"]],
                kicker="PRACTICAL — 35 MINUTES")
    notes(s, "Return rather than print. A function that returns hands back a value you can go on to use, and a "
             "printing function only gives you something to read. From Week 5 you will feed these into columns of data, and a "
             "printing function is useless for that.\n\nThe two test values are the marked part. If you cannot "
             "say what answer to expect, you cannot tell whether you got it.\n\nTO TEACH: commit per working "
             "function so the repository history shows the build. This is the week where git commit starts to "
             "feel useful rather than ceremonial.")

    # -------- SEGMENT 9
    s = s_figure(prs, "Two kinds of wrong", F("silent_wrong.png"),
                 "On the left, Python stops and tells you. On the right, it says nothing and the answer is "
                 "wrong by a factor of a thousand. Only one of these is dangerous.",
                 kicker="THE POINT OF THIS WEEK")
    notes(s, "An error is a gift. It is Python refusing to guess, and telling you exactly where it "
             "stopped.\n\nA silent wrong answer is the real hazard, and it is the one you will meet again in "
             "Week 10 when a model with a data leak reports a near-perfect score. The habit that protects you "
             "is the same in both cases: know roughly what the answer should be BEFORE you compute it, and "
             "check the one you got against the one you expected.\n\nTO TEACH: this figure is the thesis of the "
             "week. Do not rush it, even though the challenge is waiting.")

    s = s_challenge(prs, "Wrong Answer Hunt",
                    "Six functions. All six run without any error. All six return the wrong answer.\n"
                    "Find every one, name the cause, and fix it. Twenty-five minutes, in teams, no hints "
                    "from me.",
                    ["Is that answer even the right size?",
                     "What unit is that in?",
                     "What happens at the boundary value?",
                     "Did the order of operations do what you meant?",
                     "Has something been divided twice?",
                     "Would you sign your name under this number?"])
    notes(s, "All six functions run cleanly and all six are wrong, which is the entire point. The belief that "
             "code which runs is code which is correct is the most dangerous thing to carry out of a first "
             "month of programming, and it is fatal in Week 10 when a leaking model reports a near-perfect "
             "score. Work the six questions on the slide in order — the first two, right size and right unit, "
             "catch most of them.\n\nTO TEACH: the six planted bugs: integer division with //, operator "
             "precedence with a missing bracket, degrees where radians were needed, an if-chain whose branches "
             "are in the wrong order, a unit mismatch, and a parameter used in the wrong position in the call. "
             "Have the marking key ready naming each bug; you will need it when a team insists their diagnosis "
             "is right. Circulate with the question card and answer nothing.")

    # -------- SEGMENT 10 + revision
    s = s_split(prs, "Before Week 4", "Assignment A3 — due at the start of Week 4",
                "Your function library: five documented, tested functions, in a notebook in your repository.\n\n"
                "Each one needs its docstring, its units, and its two test values with the expected answers "
                "shown in the output.\n\n"
                "Plus one short paragraph: which of the six Wrong Answer Hunt bugs would you have been most "
                "likely to write yourself, and what will you do differently?\n\n"
                "Restart and Run All before you submit.",
                "Looking ahead",
                ["Next week you stop calculating",
                 "one thing at a time.",
                 "",
                 "You get a file with a few",
                 "hundred rows in it and a",
                 "question you cannot answer",
                 "by hand.",
                 "",
                 "Every session ends with a",
                 "five-question quiz worth one",
                 "per cent. Two of the five show",
                 "code that runs and returns a",
                 "wrong answer."],
                kicker="ASSIGNMENT")
    notes(s, "The reflection paragraph carries real weight. Naming the bug you would most likely have written "
             "yourself makes you measurably less likely to write it. It is also the best preparation there is "
             "for the weekly quiz, where two of the five questions show code that runs and returns a "
             "wrong answer, so there is "
             "nothing to memorise for it and doing A3 honestly is the preparation.\n\nTO TEACH: warn them "
             "properly about the quiz format so nobody sits down to revise definitions.")

    s = s_segment(prs, 10, NSEG3, "Revision material", 5,
                  "Summary, self-test with answers, glossary and a one-page reference.")
    notes(s, "Everything past this slide is revision material: a summary, a self-test with worked answers, a "
             "twenty-term glossary and a one-page reference on writing a function you can defend.\n\nTO TEACH: "
             "tell them the deck continues past the end of the session.")

    s = s_summary(prs, [
        "The equals sign is an instruction: work out the right-hand side and put the result "
        "in the box named on the left.",
        "Values have types. Text that looks like a number is still text, and arithmetic on it raises a "
        "TypeError — which is exactly what happens when you read a file.",
        "A function is a named recipe. Nothing happens when Python reads the definition; it runs when you call "
        "it.",
        "A docstring and a unit comment on every parameter are part of the function. Python does not know "
         "what unit your number is in.",
        "An if-chain is checked top to bottom and stops at the first match, so the strictest condition goes "
        "first.",
        "Read a traceback from the last line up. It names the error type and what Python wanted.",
        "The dangerous failure is the one with no error message. Know roughly what the answer should be before "
        "you compute it — that is the only defence, and it is the habit this week exists to build."])
    notes(s, "Seven statements covering the session. The last one is what this week exists for, and knowing the "
             "rough size of the answer before you compute it is the only defence against a wrong result that "
             "produces no error.\n\nTO TEACH: return to the objectives slide and ask for hands against each.")

    s = s_check(prs, [
        "What does  x = x + 1  mean, given that it is nonsense as an equation?",
        "Why does  \"12\" + 3  fail, and what would you write instead?",
        "You wrote a function and ran the cell. Nothing printed and no error appeared. What is the most likely "
        "explanation?",
        "Your if-chain tests  width > 0.30  before  width > 0.50 . What goes wrong, and will Python "
        "warn you?",
        "You compute a beam moment and get 4.2. What is the first question you should ask, before anything "
        "else?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question E has one intended answer and it is the theme of the week. Anything that notices the "
             "missing unit is right.")

    s = s_answers(prs, [
        ("What does  x = x + 1  mean?",
         "Take whatever is currently in x, add one, and put the result back into x. Read it right to left. As "
         "an instruction it is entirely sensible; as an equation it would be false."),
        ('Why does  "12" + 3  fail?',
         'Because "12" is text. Python will not guess a conversion, so it raises a TypeError. Write int("12") + 3 or '
         'float("12") + 3 to convert it first — which is exactly what you will do to every value you read from '
         'a file next week.'),
        ("Nothing printed, no error?",
         "You defined the function but never called it. Defining writes the recipe down; calling runs it. Add a "
         "line that calls it and prints or uses the result."),
        ("if-chain in the wrong order?",
         "The 0.30 branch catches everything above 0.30, including everything above 0.50, so the 0.50 branch "
         "can never run. Python will not warn you — it is valid code that returns the wrong action. Put the "
         "strictest condition first."),
        ("Beam moment of 4.2?",
         "In what unit? 4.2 newton-metres and 4.2 kilonewton-metres are a factor of a thousand apart, and only "
         "one of them is plausible. Always ask for the unit before you ask whether the number is right.")])
    notes(s, "Answer E is the sentence to carry all semester: ask for the unit before you ask whether the "
             "number is right. It comes back in Week 8, when model errors have to be reported in physical units "
             "rather than as a bare score.")

    s = s_glossary(prs, [
        ("Variable", "A name that holds a value. Assigning to it again replaces what was there."),
        ("Assignment (=)", "Work out the right-hand side, put the result in the name on the left."),
        ("int", "A whole number: 12."),
        ("float", "A number with a decimal point: 0.25. Stored approximately, which is why 0.1 + 0.2 is not "
                  "exactly 0.3."),
        ("str (string)", 'Text, in quotes: "Bridge 4". Arithmetic on it raises a TypeError.'),
        ("bool", "True or False."),
        ("Type conversion", 'Turning one type into another: int("12"), float("0.25"), str(12).'),
        ("Operator precedence", "The order operations happen in. Brackets first. When in doubt, add brackets."),
        ("// (floor division)", "Divide and throw the remainder away. 7 // 2 is 3."),
        ("Function", "A named recipe. Defined with def, run when called."),
        ("Parameter / argument", "The name in the definition is the parameter; the value you pass in is the "
                                 "argument."),
        ("return", "Hands a value back to whoever called the function. Not the same as print."),
        ("Docstring", "The text in triple quotes just inside a function, saying what it does and in what units."),
        ("Conditional (if / elif / else)", "Checked top to bottom, stops at the first match. else is the "
                                           "catch-all."),
        ("Boolean expression", "Something that evaluates to True or False: width > 0.30."),
        ("Traceback", "The error report. Read the last line first."),
        ("NameError", "A name Python has not seen. Usually a typo or an unrun cell."),
        ("TypeError", "An operation the value's type does not allow. Most often arithmetic on text."),
        ("SyntaxError", "Python could not read the line. Check the line above too."),
        ("Silent wrong answer", "No error, wrong result. The dangerous one. Know the expected magnitude first."),
    ], page="1 of 1")
    notes(s, "Twenty terms. The last one has no Python keyword attached to it and is the most important on the "
             "list.")

    s = s_prose(prs, "One-page reference — writing a function you can defend", [
        "**Name it for what it does**",
        w["fname"] + " tells a reader what comes back.",
        "**State the units, always**",
        "In the docstring for what comes out, in a comment for everything that goes in. Python does not know "
        "and will not warn you.",
        "**Return, do not print**",
        "A returned value can be used. A printed one can only be looked at.",
        "**Test it against something you already know**",
        "Two values, worked out by hand or taken from your notes. If you cannot say what to expect, you cannot "
        "tell whether you got it.",
        "**Put the strictest condition first**",
        "An if-chain stops at the first match. Reverse them and a branch becomes unreachable, silently.",
        "**Before you believe a number**",
        "Ask its unit. Ask its rough magnitude. Ask whether you would sign your name under it.",
        "**When it breaks**",
        "Last line of the traceback first. Then the line number. Then what you actually typed."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide. Every practical from here on is marked against some subset of these seven "
             "habits, and the units line accounts for more lost marks than the rest put together.")

    s = s_quiz(prs, 3,
               "A unit error that returns a plausible number, a function that prints instead of returning, and "
                        "one traceback.", qr_path=qrp(code, 3))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "Six functions ran cleanly\nand returned wrong answers.",
                  "Six functions today produced confident, plausible, wrong answers and Python raised no "
                  "objection at all. Your engineering judgement caught what the computer could not — and that "
                  "is the thing this course is really training.",
                  "Next week: a few hundred rows, a question you cannot answer by hand, and your first "
                  "unguided investigation.")
    notes(s, "Six functions today produced confident, plausible, wrong answers and Python raised no objection "
             "to any of them. Your own engineering judgement caught what the computer could not. Watch for the "
             "same pattern in Week 8, when a model reports a good score, and in Week 10, when one reports an "
             "impossible one.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week03_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for code in CO:
        print(f"  {code} W2: {week2(code)} slides   W3: {week3(code)} slides")

    import json
    from pptxkit import LECTURER
    path = _ROOT + "/data/lecturer_notes_" + __file__.split("/")[-1].replace(".py", ".json")
    json.dump(LECTURER, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  {len(LECTURER)} lecturer notes -> {path.split('/')[-1]}")
