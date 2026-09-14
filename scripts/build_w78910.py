# -*- coding: utf-8 -*-
"""Week 7 (Practical Test 1 briefing) and Weeks 8-10 (the machine learning core)."""
import sys, os
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from pptxkit import *   # noqa
from build_week1 import CO, FIG, OUTDIR, FOOT, qrp
from week_content import W8, W9, W10

F = lambda n: os.path.join(FIG, n)
DATE = {7:  {"CML3112": "Tue 20 October 2026", "CML3113": "Fri 23 October 2026",
             "CML3111": "Fri 23 October 2026"},
        8:  {"CML3112": "Tue 27 October 2026", "CML3113": "Fri 30 October 2026",
             "CML3111": "Fri 30 October 2026"},
        9:  {"CML3112": "Tue 3 November 2026", "CML3113": "Fri 6 November 2026",
             "CML3111": "Fri 6 November 2026"},
        10: {"CML3112": "Tue 10 November 2026", "CML3113": "Fri 13 November 2026",
             "CML3111": "Fri 13 November 2026"}}
SLOTS = {"CML3112": "Tuesday 11:00–14:00 · Room 106",
         "CML3113": "Friday 08:00–11:00 · Room 105",
         "CML3111": "Friday 11:00–14:00 · Room 115"}


# =====================================================================
def week7(code):
    c = CO[code]
    prs = deck(); seg_reset(); notes_context(f"{code} Week 7")

    s = s_title(prs, code, "Practical Test 1\nData Investigation",
                "Individual · offline · two hours plus twenty-five minutes",
                "WEEK 7  ·  " + DATE[7][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "This deck is the briefing you see at the start of the test, and it is also the reference to "
             "revise from beforehand. Nothing in it is a surprise: the format, the tasks and the marking scheme "
             "were all published in Week 6.\n\nThe test is worth 15 per cent of the course. It is individual "
             "and it is sat offline.\n\nTO TEACH: read the rules aloud from slide 4 rather than paraphrasing. "
             "Have the three dataset variants distributed in a checkerboard pattern before anyone sits down, "
             "and confirm the machines have no network before you start the clock.")

    s = s_points(prs, "What this test is",
                 [("An unfamiliar dataset from your own discipline",
                   "You have not seen it. There is no past paper and nothing to memorise. It is a real "
                   "engineering dataset with real defects in it."),
                  ("Two hours at a computer, then twenty-five minutes on paper",
                   "The practical part produces a notebook. The written part asks you about your own "
                   "submission, with the computer closed."),
                  ("Offline, with no AI assistance",
                   "No internet, no assistant. You have Python, pandas, matplotlib, seaborn and an offline "
                   "copy of their documentation."),
                  ("Marked on your reasoning more than your result",
                   "Thirty-five of the hundred marks are for justifying decisions. A defensible choice you can "
                   "explain beats a lucky one you cannot.")],
                 kicker="AT A GLANCE", numbered=False)
    notes(s, "The fourth point is the one to take seriously when you prepare. Two students can clean the same "
             "column differently and both score full marks, provided each says why. A student who fixes it "
             "correctly and writes nothing scores about half.\n\nThe offline condition is why the AI rule is "
             "enforceable rather than a request. Coursework is where you learn to work with an assistant; this "
             "test certifies what you can do unaided.")

    s = s_figure(prs, "How the three hours are spent", F("clock_w7.png"),
                 "Fifteen minutes of setup, two hours of practical work, twenty-five minutes of written "
                 "reasoning, then collection. The clock starts when the rules have been read and everyone has "
                 "their dataset.",
                 kicker="TIMING")
    notes(s, "Two hours is enough for the six tasks and not much more, so the plan on the next slide matters. "
             "Students who spend an hour perfecting one chart routinely lose the twenty marks attached to the "
             "findings.\n\nTO TEACH: put a visible countdown on the projector. Call the time at 1:00, 1:30, "
             "1:50 and 2:10.")

    s = s_prose(prs, "The rules", [
        "**What you may use**",
        "The machine in front of you, Python with pandas, matplotlib and seaborn, and the offline "
        "documentation bundle on the desktop. Your own printed notes and the cheat-sheet slides from any week.",
        "**What you may not use**",
        "The internet. Any AI assistant. Any messaging. Any shared drive. Another student's screen.",
        "**Why the room is offline**",
        "It makes the rule enforceable without anybody watching over your shoulder, and it means the mark "
        "certifies what you can do on your own. In coursework the assistant is permitted and taught.",
        "**Three dataset variants**",
        "Your neighbours have different data. Copying an answer will produce something that does not match "
        "your own file.",
        "**If you finish early**",
        "Reread your justifications. The marks are there, and most students under-write them.",
        "**Absence**",
        "If you miss the test with cause, tell the Faculty office the same day and follow the standard "
        "procedure. Do not simply arrange it with me."],
        kicker="RULES")
    notes(s, "The printed-notes allowance is deliberate: this course has never asked you to memorise anything, "
             "so bringing the cheat sheets changes nothing about the difficulty. What is being tested is "
             "whether you can investigate a dataset you have never seen.\n\nTO TEACH: state the variant "
             "distribution out loud so nobody wastes time attempting to collude. Have the absence procedure "
             "confirmed with the Faculty before the day.")

    s = s_split(prs, "Part A — the practical, two hours", "The six tasks, in this order",
                "1. Load the file and profile it. Report its shape, the type of every column, and what it "
                "appears to be a record of.\n\n"
                "2. Find its defects. Handle each one, and write ONE sentence justifying each decision.\n\n"
                "3. Answer the three stated engineering questions, with evidence and correct units.\n\n"
                "4. Produce three charts. Caption each with the question it answers.\n\n"
                "5. List five findings, each supported by a number from the data.\n\n"
                "6. Make one engineering recommendation, and state what further data you would need.",
                "What you hand in",
                ["One notebook.", "",
                 "It must run top to bottom",
                 "from a clean start.",
                 "",
                 "Restart and Run All before",
                 "you submit. A notebook that",
                 "only works in the order you",
                 "clicked does not work.",
                 "",
                 "Save it with the outputs",
                 "visible.", "",
                 "Then the Part B booklet."],
                kicker="PART A")
    notes(s, "Do the tasks in this order. Task 2 has to precede tasks 3 to 5, because answers computed on "
             "uncleaned data are wrong and you will have to redo them.\n\nTask 6 is where most of the "
             "engineering interpretation marks sit and it is the one most often left blank because time ran "
             "out. Two sentences written at 1:50 are worth more than a fourth chart.")

    s = s_worked(prs, "A plan for the two hours",
                 "Time is the binding constraint. This allocation matches where the marks are.",
                 ["0:00 to 0:15 — load, profile, and write two sentences saying what the file is a record of. "
                  "Do not clean anything yet.",
                  "0:15 to 0:45 — find and handle the defects, writing the justification as you go rather "
                  "than afterwards. Afterwards never happens.",
                  "0:45 to 1:15 — answer the three stated questions. State every answer with its unit.",
                  "1:15 to 1:40 — three charts, each captioned with its question and its finding.",
                  "1:40 to 1:55 — the five findings, each with a number attached.",
                  "1:55 to 2:00 — Restart and Run All, confirm it is clean, save with outputs, submit."],
                 "Twenty marks sit in the findings and fifteen in the recommendation. Reaching them is worth "
                 "more than a fourth chart.",
                 kicker="PLANNING THE TIME")
    notes(s, "The last five minutes are not optional. A notebook that fails Restart and Run All loses the ten "
             "clarity and reproducibility marks outright, and it also casts doubt on numbers the marker cannot "
             "reproduce.\n\nIf you are behind at 1:40, write the findings anyway with whatever evidence you "
             "have. Twenty marks for findings beats a third chart worth part of twenty.")

    s = s_split(prs, "Part B — written reasoning, twenty-five minutes", "Four questions about YOUR submission",
                "The computer is closed. You have your own notebook printed or on screen, read-only, and a "
                "paper booklet.\n\n"
                "1. Why did you handle that defect the way you did, and what would the alternative have "
                "changed?\n\n"
                "2. What does one of your charts NOT show?\n\n"
                "3. What would change your recommendation?\n\n"
                "4. What data is missing that you would want before acting on this?",
                "Why Part B exists",
                ["It is very hard to write",
                 "a good answer about work",
                 "you did not do yourself.",
                 "",
                 "It also captures the",
                 "reasoning that never made",
                 "it into the notebook —",
                 "which in a real report",
                 "would be the discussion",
                 "section.",
                 "",
                 "Write in sentences.",
                 "Bullet points score less",
                 "because they hide the",
                 "reasoning."],
                kicker="PART B")
    notes(s, "Part B is worth a substantial share of the interpretation marks and it is where the difference "
             "between a pass and a merit usually shows. Question 2 is the one students find hardest: every "
             "chart hides something, and naming what yours hides is a mark of understanding rather than a "
             "confession.\n\nAcceptable answers to question 4 include 'the shift log', 'the calibration "
             "record', 'the instrument specification' — anything specific. 'More data' scores nothing.")

    s = s_points(prs, "The marking scheme, restated",
                 [("Loading and profiling — 15",
                   "Correct shape, types and summary, and an accurate description of the dataset in your own "
                   "words."),
                  ("Cleaning decisions and justification — 20",
                   "Defects found AND each decision justified. An unjustified correct fix scores about half."),
                  ("Visualisation — 20",
                   "Three charts, correct types, axes labelled with units, each captioned with the question it "
                   "answers."),
                  ("Findings — 20",
                   "Five findings supported by numbers, with correct magnitudes and units. A wrong number "
                   "loses the mark even where the method was right."),
                  ("Engineering interpretation — 15",
                   "One actionable recommendation, plus what further data you would need."),
                  ("Clarity and reproducibility — 10",
                   "Runs top to bottom. Logical order. Markdown explaining intent. No dead code.")],
                 kicker="RUBRIC — PUBLISHED IN WEEK 6", numbered=False)
    notes(s, "Add up where the marks actually are: 20 for justification and 15 for interpretation is 35 of the "
             "100 for writing about your own decisions. Only 20 are for the findings themselves.\n\nThat "
             "distribution is deliberate and it is the same shape as the project rubric you will meet from "
             "Week 9.")

    s = s_prose(prs, "What earns marks, and what students lose them on", [
        "**Earns marks**",
        "A justification that names the alternative: 'dropped the 41 duplicate rows because they were an exact "
        "re-export and keeping them would weight the mean towards one day's readings.'",
        "A caption that states a finding: '" + c["finding"] + "'.",
        "A number with its unit, every time.",
        "An honest limitation. 'I cannot tell whether this extreme is real without the calibration record' is "
        "a correct answer.",
        "**Loses marks**",
        "Cleaning something correctly and saying nothing about why.",
        "A chart with no caption, or a caption that describes the axes.",
        "A printed pandas Series offered as an answer to an engineering question.",
        "Computing the three answers before cleaning, then not recomputing them.",
        "A notebook that fails Restart and Run All.",
        "Leaving task 6 blank because time ran out."],
        kicker="WHERE THE MARKS GO")
    notes(s, "Every item in the second column is drawn from what actually happens. The last one is the most "
             "common and the most expensive.\n\nThe honest-limitation point is worth repeating: this course "
             "marks 'I cannot tell from the data alone, and here is what I would need' as a correct answer. It "
             "is what a professional would write.")

    s = s_prose(prs, "If something goes wrong", [
        "**Your machine fails**",
        "Raise your hand immediately. Do not try to fix it. Time lost to a machine fault is given back.",
        "**You cannot open the file**",
        "Raise your hand. Check first that you are in the right folder — that is the commonest cause and it is "
        "not a fault.",
        "**Your code crashes and you cannot fix it**",
        "Comment out the failing cell, write in markdown what you were attempting and why you think it failed, "
        "and move on. That earns partial credit. A blank section earns none.",
        "**You run out of time**",
        "Submit what you have, having run Restart and Run All. An incomplete notebook that runs beats a "
        "complete one that does not.",
        "**Power goes out**",
        "Save often — every ten minutes. If the session is lost, the Faculty rescheduling rule applies and "
        "nobody is penalised."],
        kicker="CONTINGENCY")
    notes(s, "The comment-out-and-explain strategy is genuinely worth marks and almost nobody uses it. A "
             "marker can see what you were trying to do and give credit for the reasoning even where the code "
             "failed.\n\nTO TEACH: agree the rescheduling rule with the Faculty before the day, and keep two "
             "spare machines powered on at the back.")

    s = s_points(prs, "After the test",
                 [("Marks and feedback within a fortnight",
                   "You get your script back with the rubric annotated, plus a short note on the three most "
                   "common failures across the cohort."),
                  ("Week 8 opens with the debrief",
                   "Fifteen minutes on what went wrong most often, shown anonymously, with the fix. That "
                   "debrief is more useful than the mark."),
                  ("Then the course changes character",
                   "From Week 8 you stop describing data and start predicting from it. Everything you did "
                   "today is the input to that.")],
                 kicker="WHAT HAPPENS NEXT", numbered=False)
    notes(s, "The debrief matters more than the mark. Practical Test 1 exists partly to find out what the "
             "cohort cannot yet do, while there is still half a semester to fix it.")

    # ---- revision section
    s = s_divider(prs, "REVISION", "Revision material for this test",
                  "Everything from here is what the test draws on: Weeks 1 to 6, condensed.")
    notes(s, "Use these slides to prepare. The most effective preparation is to redo the Week 6 Data Clinic on "
             "a different dataset, timing yourself.")

    s = s_summary(prs, [
        "Every dataset has the same shape: one row per example, feature columns known beforehand, one target "
        "column you want to predict.",
        "Four commands on every new dataset, in this order: shape, head, info, describe. They answer how big, "
        "what it looks like, what types, and what ranges.",
        "A numeric column showing dtype 'object' has text in it. A minimum of -999 is a sentinel standing in "
        "for missing data and it will corrupt every mean.",
        "Whether data is missing at random decides what you may do about it. Plot the missingness before you "
        "drop anything.",
        "An extreme value is not automatically an error. Physically impossible means error; implausible needs "
        "domain knowledge.",
        "Every chart answers a stated question, and its caption says what the answer was.",
        "Report what you removed: how many rows, what proportion, and whether they were missing at random.",
        "State every answer with its unit. A printed Series is not an answer."])
    notes(s, "Eight statements, and the test is built on all eight. If you can act on each of them without "
             "looking anything up, you are prepared.")

    s = s_check(prs, [
        "A column of " + c["unit"] + " values has a mean that looks plausible and a minimum of -999. What has "
        "happened, and what does it do to every number you have computed from that column?",
        "You drop every row with a missing value and lose 30 per cent of the file. What must you check before "
        "going any further?",
        "Your box plot flags no outliers but your histogram has two clear peaks. What might that mean about "
        "the data?",
        "Give one defect you could be certain about without knowing anything about " + c["domain"] + ", and one "
        "you could not.",
        "You clean a file two defensible ways and get two different answers to the same question. What do you "
        "report?"],
        title="Self-test — the five things this test rewards",
        foot="Answers on the next slide. Write something for each first.")
    notes(s, "These five map directly onto the rubric's cleaning and interpretation marks, which together are "
             "35 of the 100.")

    s = s_answers(prs, [
        ("A minimum of -999?",
         "It is a sentinel value meaning 'missing'. pandas treats it as a real measurement, so it is included "
         "in every mean, standard deviation and correlation you have computed from that column. Convert it to "
         "a proper missing value, recompute, and report how much the answer moved."),
        ("Losing 30 per cent of the file?",
         "Whether those rows were missing at random. If the blanks correspond to a period, a unit or a "
         "condition, you have deleted a specific part of the data and everything downstream is biased. Plot "
         "the missingness pattern before you drop anything."),
        ("No outliers but two peaks?",
         "Two populations have probably been mixed — two materials, two machines, two operating regimes or "
         "two shifts. That is frequently the most interesting finding in a file, and a box plot would never "
         "have shown it."),
        ("Certain versus uncertain defects?",
         "Certain without domain knowledge: anything physically impossible — a negative width, an efficiency "
         "above 100 per cent, a duplicated row. Uncertain: any extreme that is possible but implausible, "
         "which needs someone who knows the process."),
        ("Two defensible cleanings, two answers?",
         "Report both, and say which decision drove the difference. That is the honest result and it tells "
         "the reader how much confidence the conclusion deserves. Hiding it would be the error.")])
    notes(s, "Answer E is the one that most improves a script. Reporting that your conclusion depends on a "
             "cleaning decision is a mature result, and it earns interpretation marks rather than losing them.")

    s = s_closing(prs, "Nothing in this test\nis a surprise.",
                  "You have the format, the six tasks, the timing plan and the marking scheme. The dataset is "
                  "new; the work is exactly what you did in the Week 6 Data Clinic.",
                  "Week 8: you stop describing data and start predicting from it.")
    notes(s, "The most effective preparation is one timed run at the Week 6 Data Clinic on a dataset you have "
             "not used, writing the justifications as you go. Two hours, once, is worth more than rereading "
             "notes.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week07_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week8(code):
    c, w = CO[code], W8[code]
    prs = deck(); seg_reset(); notes_context(f"{code} Week 8")
    N = 10

    s = s_title(prs, code, "Learning from data:\nyour first model",
                "Fitting, testing, and error in units you can act on",
                "WEEK 8  ·  " + DATE[8][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Until now you have described data. From today you predict from it.\n\nThe whole session rests on "
             "one honest idea: a model is only worth anything if it works on cases it has never seen. "
             "Everything about how we fit, test and report follows from that.\n\nTO TEACH: open with the "
             "fifteen-minute Test 1 debrief — the three commonest failures, shown anonymously, with the fix. "
             "That debrief is worth more than returning the marks.")

    s = s_objectives(prs, [
        "Express an engineering question as a supervised learning task, naming the features and the target.",
        "Explain why data is split into training and test sets, in terms a non-specialist would accept.",
        "Fit a linear regression, predict, and read the coefficients with appropriate caution.",
        "Compute MAE, RMSE and R-squared, and say what each one measures.",
        "State the error in " + w["unit"] + " and answer whether that is good enough to act on.",
        "Compare a model against a predict-the-mean baseline and interpret either outcome correctly.",
        "Read a residual plot and say where the model is worst."],
        8, "Learning from data")
    notes(s, "Objective 5 is the one that separates an engineer from a person running library calls. An "
             "R-squared of 0.68 means nothing on a construction site; 'plus or minus 5 " + w["unit"] + "' means "
             "something to everybody.")

    s = s_figure(prs, "How today runs", F("clock_w8.png"),
                 "Ten segments. The hands-on block in the middle is where you build a working model for the "
                 "first time.", kicker="HOW TODAY RUNS")
    notes(s, "Ten blocks across three hours. The first four build up what a model is and how it gets "
             "scored, the hands-on block is where you type a working model end to end, and the last four "
             "take that model apart to see whether its score means anything.\n\nThe fourteen lines you type "
             "in the hands-on block are the "
             "ones to keep. Everything after this week reuses them with one line changed.\n\n"
             "TO TEACH: the fourteen-line demonstration in the hands-on block is the most important half-hour of the "
             "semester. Rehearse it until it cannot fail.")

    s = s_segment(prs, 1, N, "Where we got to, and the debrief", 10,
                  "Test 1 in brief, then the three things it showed the cohort needs.")
    notes(s, "Whatever came up most often in the test is worth more of your attention than the mark itself. "
             "The pattern across a cohort is usually one of: not justifying decisions, not stating units, or "
             "computing answers before cleaning.")

    s = s_segment(prs, 2, N, "Today's question", 10,
                  "You can describe a dataset. Can you use it to say something about a case that is not in it?")
    notes(s, "This is the Week 1 hand-prediction exercise again, done properly and by machine.")

    s = s_question(prs, "TODAY'S QUESTION", '"' + c["q"] + '"',
                   "In Week 1 you answered a version of this with a pencil and twelve rows. Today you answer "
                   "it with a thousand rows and a method that can state its own error.")
    notes(s, "Hold onto the connection to Week 1. You already did every step of this by hand: you looked at "
             "the columns, worked out which mattered, formed a rough rule, applied it to a case you had not "
             "seen, and measured how wrong you were. Today each of those steps gets a name and a line of code.")

    s = s_segment(prs, 3, N, "From a line by eye to least squares", 25,
                  "Three engineers draw three different lines through the same data. Which is right, and how "
                  "would you know?")
    notes(s, "The answer is that 'by eye' is not wrong, it is just unmeasured. Least squares replaces judgement "
             "with a stated criterion.")

    s = s_figure(prs, "Three plausible lines, and the one we choose", F("fit_by_eye.png"),
                 "On the left, three lines that all look reasonable and disagree about every prediction. On the "
                 "right, the vertical distance from each point to the line is its residual, and least squares "
                 "picks the line that makes the sum of the squared residuals smallest.",
                 kicker="FITTING")
    notes(s, "A residual is the gap between what the model said and what actually happened, measured "
             "vertically because the vertical axis is what you are predicting.\n\nWhy squared rather than "
             "absolute? Squaring makes large misses count disproportionately, which matches most engineering "
             "situations — being 20 " + w["unit"] + " out once is usually worse than being 2 out ten times. It "
             "also has a single exact solution, which absolute error does not.\n\nThe important shift is that "
             "'best' now has a definition you can check, so two engineers with the same data get the same "
             "line.")

    s = s_define(prs, "Model, fitting, and prediction",
                 "A MODEL is a rule with adjustable numbers in it. FITTING means choosing those numbers so the "
                 "rule matches the examples you have. PREDICTION means applying the fitted rule to a case it "
                 "has never seen.",
                 "A straight line has two adjustable numbers, a slope and an intercept. Fitting chooses them "
                 "from your " + w["file"] + " rows. Prediction then estimates " + w["tgt"] + " for a new case.",
                 "A formula from a textbook. A formula's numbers come from physics and hold everywhere; a "
                 "model's numbers come from your data and hold where your data holds.")
    notes(s, "The last line is the whole difference between the two columns of the Week 1 diagram. A fitted "
             "coefficient describes the dataset it came from. Take the model to a different plant, a different "
             "supplier or a different operating range and there is no guarantee it still applies.\n\nThis is "
             "also why reporting the range your data covered is part of reporting a model.")

    s = s_segment(prs, 4, N, "Train and test", 25,
                  "The single most important idea in the course, and it takes one line of code.")
    notes(s, "Protect this segment. Everything in Week 10 is a consequence of it.")

    s = s_figure(prs, "Why the data is split", F("train_test_split.png"),
                 "The model is fitted on the training rows and scored on the test rows, which it never saw. "
                 "Scoring on rows it was fitted on tells you how well it memorised, and nothing about whether "
                 "it learned.",
                 kicker="TRAIN AND TEST")
    notes(s, "The honest analogy: revising with the exam paper open in front of you tells you nothing about "
             "what you know. A model scored on its own training data is doing exactly that.\n\nThe usual split "
             "is 80 per cent to train and 20 per cent to test. The exact ratio matters less than the "
             "discipline: the test rows are spent once, at the end, and never used to make a choice.\n\nIn "
             "Week 1 you did this without being told: case 13 was not among the twelve you formed your rule "
             "from, which is why measuring your error against it meant something.")

    s = s_define(prs, "Training set, test set, and generalisation",
                 "The TRAINING SET is the rows used to fit. The TEST SET is rows held back and used once, to "
                 "score. GENERALISATION is whether a rule learned from the training rows still works on rows "
                 "it has never seen.",
                 "1,030 rows split 80/20 gives 824 rows to fit on and 206 to score on. The 206 are not looked "
                 "at until the model is final.",
                 "Validation. A validation set is a third slice used to make choices during development, so "
                 "that the test set stays untouched. That distinction arrives in Week 10.")
    notes(s, "The rule about spending the test set once is easy to break by accident. If you try five models, "
             "look at the test score each time, and keep the best, you have used the test set to make a choice "
             "and its score is now optimistic. Week 10 gives you the proper tool for that situation.\n\n"
             "random_state fixes which rows land in which set, so that your split is reproducible. Without it "
             "your score changes every time you run the notebook and you cannot tell improvement from noise.")

    s = s_break(prs, 10, after="The hands-on block is next, so have Colab open when you come back.")
    notes(s, "The hands-on block after the break is the longest of the session.")

    s = s_segment(prs, 6, N, "Your first model", 30,
                  "Everybody types. Fourteen lines, and every one of them explained.")
    notes(s, "Thirty minutes with everybody typing. Fourteen lines take you from a CSV file to a scored "
             "model, and each line is explained as it goes in.\n\nThe order matters: the picture of "
             "predicted against actual comes before any metric, because a single number cannot show you "
             "the shape of a mistake. A model can have a respectable average error and still be wrong in "
             "one systematic direction over the range you care about.\n\n"
             "TO TEACH: type it live, do not paste. Justify each line aloud as you go. Plot predicted against "
             "actual BEFORE quoting any metric — the picture should come first.")

    s = s_livecode(prs, "Fourteen lines, end to end", "OPEN COLAB — TYPE THIS WITH ME",
                   ('import pandas as pd\n'
                    'from sklearn.model_selection import train_test_split\n'
                    'from sklearn.linear_model import LinearRegression\n'
                    'from sklearn.metrics import mean_absolute_error, r2_score\n'
                    '\n'
                    'df = pd.read_csv("' + w["file"] + '")\n'
                    '\n'
                    'X = df[' + w["feats"] + ']      # the features\n'
                    'y = df["' + w["tgtcol"] + '"]' + " " * max(1, 22 - len(w["tgtcol"])) + '# the target\n'
                    '\n'
                    'X_tr, X_te, y_tr, y_te = train_test_split(\n'
                    '        X, y, test_size=0.2, random_state=42)\n'
                    '\n'
                    'model = LinearRegression()\n'
                    'model.fit(X_tr, y_tr)              # fit on TRAIN only\n'
                    'pred = model.predict(X_te)         # predict on TEST\n'
                    '\n'
                    'print(f"MAE {mean_absolute_error(y_te, pred):.2f} ' + w["unit"] + '")\n'
                    'print(f"R2  {r2_score(y_te, pred):.3f}")'),
                   "Fit on the whole dataset instead of X_tr, then score on X_te. The numbers improve, and "
                   "they are now meaningless — the model has already seen every row you are testing it on. "
                   "This is the mistake Week 10 is entirely about.")
    notes(s, "Four imports, and then the same fit / predict / score pattern that every model in this course "
             "will use. Once you have this shape, swapping LinearRegression for a decision tree next week is "
             "a one-line change.\n\nNote the order: split, then fit on the training part only, then predict on "
             "the test part. Any preparation you do — scaling, filling gaps — must also happen after the "
             "split, and Week 10 shows you the tool that enforces that.\n\nrandom_state=42 is an arbitrary "
             "number that makes the split repeatable. Any fixed value does.")

    s = s_segment(prs, 7, N, "Reading the error in units you can act on", 25,
                  "Three numbers describe how wrong a model is. Only one of them means anything to a client.")
    notes(s, "This segment is where the course's engineering character shows most clearly.")

    s = s_figure(prs, "What MAE, RMSE and R-squared each measure", F("error_metrics.png"),
                 "MAE is the average size of the miss, in the units of the thing you are predicting. RMSE "
                 "squares the misses first, so one large error moves it far more than several small ones. "
                 "R-squared says how much of the variation the model explains, compared with just predicting "
                 "the mean.",
                 kicker="THREE METRICS")
    notes(s, "Which to quote depends on who is asking. To another engineer, MAE in " + w["unit"] + " is the "
             "honest answer, because it is the number they can compare against their tolerance. R-squared is "
             "useful for comparing two models on the same data and useless as a statement about the world — "
             "it has no units and it changes if you change the spread of your data.\n\nRMSE is worth quoting "
             "when large errors are disproportionately costly, which in engineering they usually are.\n\nOne "
             "caution about R-squared: it can be high while the model is unusable, and low while the model is "
             "still the best available. It is a comparison tool.")

    s = s_fig_text(prs, "Predicted against actual", F("pred_vs_actual.png"),
                   ["**Read this plot before any metric**",
                    "Each point is one test case. The diagonal is where a perfect prediction would sit. "
                    "Distance from the diagonal is the error on that case.",
                    "**What to look for**",
                    "A cloud tilted away from the diagonal means the model is systematically over- or "
                    "under-predicting across the range.",
                    "A cloud that fans out means the model is reliable for small values and unreliable for "
                    "large ones, which matters a great deal if the large ones are the ones you care about.",
                    "A few points far from the diagonal are worth naming individually. They are often the "
                    "most interesting cases in the file."],
                   kicker="THE FIRST PLOT TO DRAW", img_left=True)
    notes(s, "Draw this before you quote a single metric. A metric collapses every case into one number; this "
             "plot shows you which cases the model gets wrong, and that is what you can act on.\n\nThe "
             "fanning-out pattern is common in engineering data and it is the reason a single average error "
             "can be misleading. If your model is accurate at low " + w["tgt"] + " and poor at high values, "
             "and it is the high values that trigger a decision, then the average error is flattering you.")

    s = s_question(prs, "THE QUESTION THAT ACTUALLY MATTERS",
                   '"Plus or minus a few ' + w["unit"] + '. Is that good enough to act on?"',
                   w["act"])
    notes(s, w["good"] + "\n\nThis is the question that turns a score into engineering. A number without a "
             "tolerance to compare it against is not yet an answer.\n\nAsking it also tells you whether the "
             "project was worth doing. If the model's error is larger than the decision's tolerance, the "
             "honest report says so — and that is a result, arrived at properly.")

    s = s_segment(prs, 8, N, "Residuals: where is it worst?", 20,
                  "The average error hides the pattern. The residual plot shows it.")
    notes(s, "A model with a good average can still be systematically wrong somewhere specific.")

    s = s_figure(prs, "Reading a residual plot", F("residuals.png"),
                 "Residual against predicted value, with zero marked. Scattered evenly about zero means the "
                 "straight-line model has captured the shape. A visible curve means the relationship is not "
                 "straight and a straight line is the wrong model.",
                 kicker="RESIDUALS")
    notes(s, "Plot the residual against the PREDICTED value, not against the actual value. Against the "
             "predicted value a correct model gives no slope at all. Against the actual value the same "
             "residuals slope upwards, because the actual value is the prediction plus the residual, so the "
             "residual is part of what you are plotting it against. That upward slope appears even when "
             "nothing is wrong, and you would diagnose a fault that is not there.\n\n"
             "Structure in a residual plot is a message. A curve says fit something curved. A funnel says the "
             "error grows with the value. A cluster of large residuals in one region says something is "
             "different about that region, and it is worth finding out what.")

    s = s_segment(prs, 9, N, "Challenge: beat the baseline", 20,
                  "Before you can say a model is good, you need something to compare it against.")
    notes(s, "A baseline is what makes a score interpretable.")

    s = s_figure(prs, "The model against a predict-the-mean baseline", F("baseline_vs_model.png"),
                 "The baseline ignores every feature and predicts the training mean for every case. Any model "
                 "that cannot beat that has learned nothing from the features.",
                 kicker="THE BASELINE")
    notes(s, "The baseline must be computed from the TRAINING mean, not the test mean, or you have leaked the "
             "answer into your comparison.\n\nThis is what makes a number like MAE interpretable. On its own, "
             "an MAE of 5 " + w["unit"] + " means nothing. Against a baseline of 10, it means the features "
             "have halved your uncertainty, and that is a claim you can defend.\n\nA model that fails to beat "
             "the baseline is a real and reportable result. It usually means the features do not carry the "
             "signal — which is limit two from Week 1.")

    s = s_challenge(prs, "Beat the baseline",
                    "In your team: compute the predict-the-mean baseline on the training rows, then build a "
                    "regression and compare on MAE in " + w["unit"] + ".\n"
                    "Then change the features. Add " + w["addfeat"] + ". Remove " + w["dropfeat"] + ". Record "
                    "what happens to the error each time.\n"
                    "Twenty minutes. Report your error in " + w["unit"] + ", never as a bare score.",
                    ["What is the baseline error, in real units?",
                     "By how much did the features improve on it?",
                     "Which feature mattered most, and how do you know?",
                     "Where is the model worst?",
                     "Is this error small enough to act on?",
                     "What would you need to do better?"])
    notes(s, "Both outcomes are valid results and both are marked the same way. A team that beats the "
             "baseline must explain why; a team that does not must diagnose why not.\n\nRemoving a feature and "
             "watching the error rise is the crudest form of the ablation method you will use properly in "
             "Week 11.\n\nTO TEACH: run a visible leaderboard on MAE in " + w["unit"] + ". Pre-compute the "
             "baseline so nobody spends the segment on it.")

    s = s_split(prs, "Before Week 9", "Assignment A7 — due at the start of Week 9",
                "A regression notebook on " + w["file"] + " containing:\n\n"
                "the train/test split with a fixed random_state · the fitted model · MAE and R-squared on the "
                "test rows · a predicted-against-actual plot · a residual plot\n\n"
                "Plus the baseline comparison, the error stated in " + w["unit"] + ", and three sentences on "
                "whether an engineer should act on this model.\n\n"
                "Restart and Run All before you submit.",
                "Also this week",
                ["The Data Analysis Project",
                 "is due today. Repository,",
                 "cleaned data, four charts,",
                 "one page of findings.",
                 "",
                 "Worth 10 per cent.",
                 "",
                 "Next week the Engineering",
                 "ML Project is set — the",
                 "25 per cent one that runs",
                 "to Week 15."],
                kicker="ASSIGNMENT")
    notes(s, "The three sentences about acting on the model carry as much weight as the notebook. A student "
             "who reports 'MAE 4.8 " + w["unit"] + ", which is larger than the tolerance this decision needs, "
             "so I would not act on it' has understood the week.")

    s = s_summary(prs, [
        "A model is a rule with adjustable numbers. Fitting chooses those numbers from examples; prediction "
        "applies the rule to a case it has never seen.",
        "Least squares picks the line that makes the sum of the squared residuals smallest, which gives 'best "
        "fit' a definition two engineers can both check.",
        "Fit on the training rows and score on the test rows. A score on data the model was fitted to only "
        "tells you how well it memorised those rows.",
        "Split first, then do everything else. Any preparation done before the split leaks information.",
        "MAE is the average miss in real units. RMSE punishes large misses. R-squared compares against "
        "predicting the mean and has no units.",
        "Quote the error in " + w["unit"] + " and then ask whether it is inside the tolerance the decision "
        "needs. That question turns a score into engineering.",
        "Plot predicted against actual and residual against predicted before quoting any metric. Structure in "
        "the residuals is a message about the model.",
        "A model that cannot beat a predict-the-mean baseline has learned nothing from the features, and that "
        "is a reportable result."])
    notes(s, "Statement 6 is the one this course will keep coming back to, and it is what Practical Test 2 in "
             "Week 14 actually assesses.")

    s = s_check(prs, [
        "You fit on all 1,030 rows and score on the same 1,030 rows. Your R-squared is 0.94. What is wrong "
        "with quoting that?",
        "Your model has an MAE of 4.8 " + w["unit"] + " and an R-squared of 0.31. Is it useful?",
        "Your residual plot shows a clear curve. What does that tell you, and what would you do?",
        "Your model beats the baseline by 2 per cent. Should you deploy it?",
        "The coefficient on " + w["addfeat"].replace("the ", "") + " is large and positive. Can you tell a "
        "client that increasing it will increase " + w["tgt"] + "?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question E is the correlation-and-cause point from Week 1, arriving now with a real coefficient "
             "attached to it.")

    s = s_answers(prs, [
        ("Fitting and scoring on the same rows?",
         "The score measures how well the model memorised those rows, and says nothing about a case it has "
         "not seen. It will always look better than the honest number. Split the data and score on the held-"
         "back part."),
        ("MAE 4.8 with R-squared 0.31?",
         "Possibly, and the two numbers are answering different questions. R-squared says the model explains "
         "little of the variation, which is often because the target genuinely varies for reasons your columns "
         "do not capture. Whether it is useful depends entirely on whether 4.8 " + w["unit"] + " is inside the "
         "tolerance of the decision it would inform."),
        ("A curve in the residuals?",
         "A straight line is the wrong shape for this relationship. The model is systematically over-"
         "predicting in one part of the range and under-predicting in another. Either fit something curved, or "
         "engineer a feature that straightens the relationship — which is Week 11."),
        ("Beating the baseline by 2 per cent?",
         "No, on that evidence alone. A 2 per cent gap could easily be the noise in one particular train/test "
         "split rather than a real improvement. You need to know how much the score moves when the split "
         "changes, and that is cross-validation in Week 10."),
        ("A large positive coefficient?",
         "No. The model has learned that the two move together in this dataset. It knows nothing about "
         "mechanism, and the coefficient also depends on which other features are in the model. Say "
         "'associated with' and leave causation to the physics.")])
    notes(s, "Answer D plants Week 10. A single split is one noisy measurement, and comparing two models on "
             "one split is how people convince themselves of improvements that are not there.")

    s = s_glossary(prs, [
        ("Supervised learning", "Learning a rule from examples where the answer is known."),
        ("Regression", "Predicting a number on a continuous scale."),
        ("Model", "A rule with adjustable numbers in it."),
        ("Fitting (training)", "Choosing those numbers so the rule matches the training examples."),
        ("Coefficient", "One of the fitted numbers. It describes an association inside your data and "
                        "carries no claim about mechanism."),
        ("Intercept", "The model's prediction when every feature is zero. Often physically meaningless."),
        ("Prediction", "Applying the fitted rule to a case it has not seen."),
        ("Residual", "Actual minus predicted, for one case. The vertical gap to the fitted line."),
        ("Least squares", "Choosing the fit that makes the sum of the squared residuals smallest."),
        ("Training set", "The rows used to fit the model."),
        ("Test set", "Rows held back and used once, at the end, to score."),
        ("train_test_split", "The scikit-learn function that separates them. Use random_state to make it "
                             "repeatable."),
        ("Generalisation", "Whether the fitted rule still works on rows it never saw."),
        ("MAE", "Mean absolute error. The average size of the miss, in the target's own units."),
        ("RMSE", "Root mean squared error. Squares the misses first, so large ones dominate."),
        ("R-squared", "The share of variation explained, compared with predicting the mean. No units."),
        ("Baseline", "A deliberately trivial model. Predicting the training mean every time is the usual one."),
        ("fit / predict / score", "The pattern every scikit-learn model follows. Learn it once, reuse it all "
                                  "year."),
    ], page="1 of 1")
    notes(s, "Eighteen terms, and all of them appear in Practical Test 2. The three metrics and the "
             "train/test pair are the ones to be fluent in.")

    s = s_prose(prs, "One-page reference — fitting and reporting a model", [
        "**The five lines that matter**",
        "split · fit on train · predict on test · metric on test · plot predicted against actual",
        "**Split first, always**",
        "Anything you do to the data before the split leaks information from the test rows into the model.",
        "**Fix the random_state**",
        "Otherwise your score changes every run and you cannot tell improvement from noise.",
        "**Report the error in real units**",
        "MAE in " + w["unit"] + ". Then say whether that is inside the tolerance the decision needs.",
        "**Always compare against a baseline**",
        "Predict the training mean. Without that comparison a score is uninterpretable.",
        "**Look at two plots before any number**",
        "Predicted against actual, and residual against predicted. Structure in either one is a message.",
        "**Describe the range you covered**",
        "A model is only evidence about the conditions your data spanned. Say what those were.",
        "**Say 'associated with'**",
        "A coefficient is not a mechanism. Leave causation to the physics."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "These eight are the marking criteria for every modelling task from here to Week 15.")

    s = s_quiz(prs, 8,
               "A score quoted on the training rows, a residual plot read the wrong way round, and a baseline "
                        "nobody computed.", qr_path=qrp(code, 8))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You built a model, and you\ncan say how wrong it is.",
                  "The second half of that sentence is the part that matters. Anyone can fit a line. Reporting "
                  "its error in " + w["unit"] + " and saying whether that is good enough is the engineering.",
                  "Next week: predicting a category, and the cost of getting it wrong in each direction.")
    notes(s, "Next week the two kinds of mistake stop being symmetrical. A false alarm and a missed failure "
             "cost very different amounts, and that asymmetry decides which model you choose.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week08_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week9(code):
    c, w = CO[code], W9[code]
    prs = deck(); seg_reset(); notes_context(f"{code} Week 9")
    N = 10

    s = s_title(prs, code, "Classification:\ndeciding, and the cost of\nbeing wrong",
                "Boundaries, trees, forests, and the two mistakes",
                "WEEK 9  ·  " + DATE[9][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Last week the answer was a number. This week it is a decision, and a decision has two ways of "
             "being wrong that almost never cost the same.\n\nThat asymmetry is the whole session. Everything "
             "about which model to choose, which metric to quote and where to put the threshold follows from "
             "it.\n\nTO TEACH: the Engineering ML Project is released today and runs to Week 15. Have the "
             "brief, the rubric and the milestone schedule printed.")

    s = s_objectives(prs, [
        "Recognise when a problem is classification, and when a continuous target should be banded.",
        "Fit and compare logistic regression, a decision tree and a random forest.",
        "Read a confusion matrix and name each of the four cells in the language of " + c["domain"] + ".",
        "Explain why accuracy is misleading when one class is rare, with a worked case.",
        "Choose between precision and recall by reasoning about the cost of each mistake.",
        "Move the decision threshold and say what that does operationally.",
        "Read a feature importance ranking with appropriate scepticism."],
        9, "Classification")
    notes(s, "Objective 5 is the one an engineer is uniquely placed to do well. Choosing a metric is not a "
             "statistical question; it is a question about what a mistake costs, and you know that better "
             "than any algorithm does.")

    s = s_figure(prs, "How today runs", F("clock_w9.png"),
                 "Ten segments. The challenge at the end is the most important twenty minutes of the week.",
                 kicker="HOW TODAY RUNS")
    notes(s, "Ten segments. The first half introduces classification and three models that do it; the "
             "second half is about reading the four numbers that tell you whether a classifier is any "
             "use.\n\nThe last twenty minutes carry the most weight. A classifier scoring 97 per cent "
             "accuracy can be worth nothing at all, and the challenge at the end is where that becomes "
             "obvious rather than something you have been told.\n\n"
             "TO TEACH: protect the last two segments. If time is short, shorten the trees-and-forests block "
             "rather than the confusion matrix or the imbalance challenge.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can predict a number and state its error. Today the answer becomes a decision.")
    notes(s, "Everything from last week carries over: the split, the fit / predict / score pattern, and the "
             "habit of asking whether the error is small enough to act on. Only the metrics change.")

    s = s_segment(prs, 2, N, "The two mistakes", 15,
                  "Before any model, the arithmetic of being wrong in each direction.")
    notes(s, "This framing has to come first. A student who learns the metrics before the costs will reach "
             "for accuracy every time.")

    s = s_question(prs, "TODAY STARTS WITH THE COSTS",
                   '"' + w["task"] + '. What does each kind of mistake cost?"',
                   "There are exactly two ways to be wrong, and in engineering they are almost never equally "
                   "expensive.")
    notes(s, "Write both costs down before you write any code. It sounds like an administrative step and it "
             "is the step that determines which model you end up recommending.")

    s = s_prose(prs, "Two ways to be wrong", [
        "**A false alarm — you predicted " + w["pos"] + ", it was " + w["neg"] + "**",
        w["fp"],
        "**A miss — you predicted " + w["neg"] + ", it was " + w["pos"] + "**",
        w["fn"],
        "**Why this decides everything that follows**",
        "A model can be tuned to make fewer of one at the price of more of the other. You cannot reduce both "
        "at once, so somebody has to decide which is worse. That somebody is the engineer.",
        "**The cost table you will fill in today**",
        " · ".join(w["costs"]),
        "**And the honest complication**",
        "A false alarm is not free even when nobody is hurt. An alarm that cries wolf gets disabled, and a "
        "disabled alarm catches nothing at all."],
        kicker="THE ASYMMETRY")
    notes(s, "The last point is the one practitioners learn the hard way. A model with excellent recall and a "
             "poor false-alarm rate looks good on paper and gets switched off within a month. Recall you "
             "cannot sustain operationally is not recall.\n\nFor this cohort: " + w["which"])

    s = s_segment(prs, 3, N, "A boundary, and where to put it", 25,
                  "Logistic regression, and why its output is a probability rather than a verdict.")
    notes(s, "The probability output is the part that matters, because it is what lets you move the threshold "
             "later.")

    s = s_figure(prs, "The decision boundary", F("decision_boundary.png"),
                 "The model learns a line separating the two classes, and its position depends on where you "
                 "set the cut-off. Move the cut-off and the boundary moves with it.",
                 kicker="THE BOUNDARY")
    notes(s, "Logistic regression does not output a class. It outputs a probability between 0 and 1, and "
             "something else has to turn that into a decision by comparing it with a threshold.\n\nThe "
             "default threshold is 0.5, and there is nothing special about 0.5. It is a convention. Choosing "
             "it is an engineering decision, and the figure shows what changing it does.\n\nAt a threshold of "
             "0.5 this model gets 86 per cent right; at 0.2 it gets 81 per cent right but catches many more "
             "of the positive cases. Which is better depends entirely on the cost table.")

    s = s_define(prs, "Classification, probability and threshold",
                 "CLASSIFICATION predicts which category a case belongs to. Most classifiers first produce a "
                 "PROBABILITY, and a THRESHOLD turns that probability into a decision.",
                 'model.predict_proba(X)[:, 1] gives the probability of ' + w["pos"] + '. Comparing it with '
                 '0.5 gives the same answer as model.predict(X). Comparing it with 0.2 gives a more cautious '
                 'model that raises more alarms.',
                 "The probability being a statement of confidence. It is the model's estimate of how often "
                 "cases like this one turn out positive, calibrated on the data it saw.")
    notes(s, "Keeping the probability rather than only the class is what gives you a dial to turn. It is also "
             "far more useful in a report: 'a 78 per cent chance of " + w["pos"] + "' says more to a decision-"
             "maker than a bare label.\n\nThe 'do not confuse with' point matters. A model that says 0.9 is "
             "not 90 per cent confident in the everyday sense; it is saying that among training cases that "
             "looked like this, about 90 per cent were positive.")

    s = s_segment(prs, 4, N, "Trees and forests", 25,
                  "A model you can read as an engineering rule, and what you give up by averaging many of "
                  "them.")
    notes(s, "The readability of a shallow tree is a genuine engineering advantage rather than a teaching "
             "convenience.")

    s = s_figure(prs, "A decision tree you can read", F("decision_tree.png"),
                 "Each split is a condition on one feature. Follow the branches and you arrive at a leaf with "
                 "a class and a count. A tree this shallow is a rule a person could apply by hand.",
                 kicker="DECISION TREES")
    notes(s, "This is the only model in the course you can hand to a colleague as a written procedure, and "
             "that is worth a great deal in any setting where a decision has to be explained to a client or "
             "a regulator.\n\nRead the leaf counts, not just the labels. A leaf saying 'expect fine' with a "
             "20 per cent failure rate behind it is doing something quite different from one with a 2 per "
             "cent rate, and the label alone hides that.\n\nDepth is the control. A deeper tree fits the "
             "training data better and generalises worse, which is exactly the subject of next week.")

    s = s_figure(prs, "Many trees, voting", F("forest_vote.png"),
                 "A random forest fits many trees on different samples of the data and lets them vote. The "
                 "individual trees vary; the vote is steadier than any single one of them.",
                 kicker="RANDOM FORESTS")
    notes(s, "Why averaging helps: each tree makes its own mistakes, and the mistakes are not the same ones. "
             "Averaging cancels a good deal of that individual error.\n\nWhat you give up is readability. "
             "There is no rule to write down any more — the model is a hundred trees and a vote. In a setting "
             "where the decision must be explained, that cost is real and sometimes decisive.\n\nDo not take "
             "away the idea that a forest always beats the best single tree. On any one dataset the best tree "
             "may win; you simply have no way of knowing in advance which tree that would have been.")

    s = s_break(prs, 10)
    notes(s, "The hands-on block after the break builds all three models.")

    s = s_segment(prs, 6, N, "Three classifiers", 30,
                  "The same fit / predict / score pattern, three times, with one line changed.")
    notes(s, "Thirty minutes fitting three different classifiers to the same data. Logistic regression, a "
             "decision tree and a random forest are three genuinely different ideas about how to draw a "
             "boundary, and all three are used through exactly the same four steps you learned in Week 8: "
             "split, fit, predict, score.\n\nOnly the line that creates the model changes. That is the "
             "return on having learned the pattern properly — swapping in a new algorithm is a one-line "
             "edit, so the hard part of your project is never going to be the modelling.\n\n"
             "TO TEACH: point out explicitly that only the constructor line changes. That is the payoff of "
             "learning the pattern in Week 8.")

    s = s_livecode(prs, "Three models, one pattern", "OPEN COLAB — TYPE THIS WITH ME",
                   ('from sklearn.linear_model import LogisticRegression\n'
                    'from sklearn.tree import DecisionTreeClassifier\n'
                    'from sklearn.ensemble import RandomForestClassifier\n'
                    'from sklearn.metrics import confusion_matrix, classification_report\n'
                    '\n'
                    'models = {\n'
                    '    "logistic": LogisticRegression(max_iter=1000),\n'
                    '    "tree":     DecisionTreeClassifier(max_depth=3, random_state=42),\n'
                    '    "forest":   RandomForestClassifier(n_estimators=100, random_state=42),\n'
                    '}\n'
                    '\n'
                    'for name, m in models.items():\n'
                    '    m.fit(X_tr, y_tr)\n'
                    '    pred = m.predict(X_te)\n'
                    '    print(name)\n'
                    '    print(confusion_matrix(y_te, pred))\n'
                    '    print(classification_report(y_te, pred, digits=3))'),
                   "Drop max_depth from the tree and run it again. Its training score goes up and its test "
                   "score goes down, because an unlimited tree can memorise every training row. That gap is "
                   "the subject of next week.")
    notes(s, "Three models, one loop, and the only thing that differs between them is the constructor. "
             "Everything you learned in Week 8 transfers unchanged.\n\nmax_iter=1000 on logistic regression "
             "stops a convergence warning, which is housekeeping rather than a modelling choice. "
             "max_depth=3 on the "
             "tree is a modelling choice and a deliberate one — it keeps the tree readable.\n\nclassification"
             "_report gives precision, recall and F1 for each class. Read the row for the class you care "
             "about, which is usually the rare one.")

    s = s_segment(prs, 7, N, "The confusion matrix", 20,
                  "Four numbers that say everything a single score hides.")
    notes(s, "Once a student can read this table in their own domain's language, the metrics stop being "
             "arbitrary.")

    s = s_figure(prs, "Four cells, in your own language", F("confusion_matrix_" + code + ".png"),
                 "Every prediction lands in one of four cells. Two are correct and two are the mistakes you "
                 "costed at the start of the session. Every metric in this course is arithmetic on these four "
                 "numbers.",
                 kicker="THE CONFUSION MATRIX")
    notes(s, "Read the table before any metric. Accuracy is the two correct cells divided by all four, which "
             "is why it can look excellent while one of the correct cells is empty.\n\nPrecision answers: of "
             "the cases I flagged, how many really were " + w["pos"] + "? Recall answers: of the cases that "
             "really were " + w["pos"] + ", how many did I catch? They are different questions and improving "
             "one usually worsens the other.\n\nF1 combines them into one number. It is convenient for "
             "comparing models and it hides the trade-off, so quote the two separately when the costs differ.")

    s = s_worked(prs, "Reading a confusion matrix in four steps",
                 "The routine to use every time, before you look at a single metric.",
                 ["Find the rare class and check it is not empty. A column of zeros means the model never "
                  "predicts it, and no metric will tell you that as plainly as the table does.",
                  "Name each of the four cells out loud in your own domain's language. If you cannot, you do "
                  "not yet know what the model is doing.",
                  "Count the misses — the cases that were " + w["pos"] + " and were not caught. Multiply by "
                  "what one costs.",
                  "Count the false alarms and multiply by what one of those costs.",
                  "Compare the two totals. The larger one tells you which metric to optimise, and therefore "
                  "which model to prefer.",
                  "Only now quote a number, and quote the one that matches the cost you just computed."],
                 "Steps 3 to 5 are arithmetic an engineer can do and an algorithm cannot, because the costs "
                 "are not in the data.",
                 kicker="THE ROUTINE")
    notes(s, "This routine is what the project rubric means by engineering reasoning. Two teams with "
             "identical models and different cost tables should reach different recommendations, and both can "
             "be right.\n\nStep 1 catches the failure in the last segment of today before it catches you.")

    s = s_segment(prs, 8, N, "Precision, recall and the threshold", 20,
                  "One dial, and what turning it does to each kind of mistake.")
    notes(s, "The threshold is the most useful and least used control a beginner has.")

    s = s_figure(prs, "Turning the dial", F("threshold_tradeoff.png"),
                 "As the threshold falls, the model flags more cases: recall rises and precision falls. As it "
                 "rises, the model becomes more selective: precision rises and recall falls. There is no "
                 "setting that improves both.",
                 kicker="THE TRADE-OFF")
    notes(s, "Two operating points are marked, and choosing between them is not a statistical decision. It "
             "is a decision about how many false alarms the people using this system will tolerate before "
             "they stop believing it.\n\nA practical way to set it: ask how many alarms per week are "
             "acceptable, find the threshold that produces that many, and report the recall you get at that "
             "threshold. That is a far more useful conversation than quoting an F1 score.\n\nFor this cohort: "
             + w["which"])

    s = s_segment(prs, 9, N, "Challenge: the 97 per cent trap", 20,
                  "A model with an excellent score and no value whatsoever.")
    notes(s, "Twenty minutes on a notebook that reports an excellent accuracy score and is of no practical "
             "use whatsoever. Your job is to work out why, using the tools from the previous two "
             "segments.\n\nThe answer is in the confusion matrix rather than in the accuracy figure, and "
             "the reason is in how often the thing being predicted actually happens. Work the four numbers "
             "before you form an opinion.\n\n"
             "TO TEACH: hand out the notebook and the fictional complaint. Give no hints for the full twenty "
             "minutes.")

    s = s_figure(prs, "The most dangerous score in machine learning", F("imbalance_trap.png"),
                 "A model that predicts " + w["neg"] + " for every single case, on data where the positive "
                 "class is about three in a hundred. It has no features and no parameters. It scores about 97 "
                 "per cent accurate and it has never once predicted " + w["pos"] + ".",
                 kicker="CLASS IMBALANCE")
    notes(s, "This is the most important figure in Week 9. Accuracy is the wrong instrument whenever one "
             "class is rare, and rare classes are exactly the interesting ones in engineering — failures, "
             "defects, incidents.\n\nWhat to quote instead: recall on the rare class, or the confusion matrix "
             "itself. Both make the empty column impossible to hide.\n\nThe practical lesson is a reflex. "
             "When somebody reports a high accuracy, ask what the class balance was. If they do not know, "
             "the number means nothing yet.")

    s = s_challenge(prs, "The 97 per cent trap",
                    "You are given a notebook and a dataset from " + w["imb"] + ". The notebook reports 97 per "
                    "cent accuracy. The plant manager is unhappy with the system and cannot say why.\n"
                    "In your team: work out what is wrong, prove it with evidence from the data, and propose "
                    "what should be reported instead. Twenty minutes, no hints.",
                    ["What is the class balance in this file?",
                     "What does the confusion matrix look like?",
                     "How many of the " + w["pos"] + " cases did it catch?",
                     "What would a model that always says " + w["neg"] + " score?",
                     "Which metric would have exposed this immediately?",
                     "What should the report have said?"])
    notes(s, "Question 4 is the one that cracks it: computing the score of the do-nothing model shows that "
             "the 97 per cent contains no information at all.\n\nThe deliverable is one sentence naming the "
             "problem and one naming the metric that should replace accuracy. Teams that get there in ten "
             "minutes should go on to find the threshold that gives a usable recall.\n\nTO TEACH: the planted "
             "notebook must genuinely report high accuracy and a confusion matrix with an empty positive "
             "column. Prepare it beforehand; the marking key is that the positive class is ~3 per cent and "
             "recall is zero.")

    s = s_split(prs, "The Engineering ML Project — set today", "25 per cent, from now to Week 15",
                "Your team chooses an engineering problem from your own discipline, finds or is given data, "
                "and builds something you can defend.\n\n"
                "Four graded milestones, each briefed in one session and due at the start of the next: PM1 "
                "in Week 10 (problem, data, baseline), PM2 at the start of Week 12 (cleaned data, feature "
                "dictionary, first evaluated model), PM3 at the start of Week 13 (model comparison "
                "table), PM4 in Week 13 (repository freeze and peer review).\n\n"
                "Final submission in Week 15: repository, two-page engineering brief, poster, AI-use "
                "declaration and an individual contribution log.\n\n"
                "Example titles for this cohort: " + c["proj"] + ".",
                "How it is marked",
                ["Problem definition        15",
                 "Data understanding        15",
                 "Methodology               20",
                 "Engineering reasoning     20",
                 "Validation                15",
                 "Communication             10",
                 "Reproducibility            5",
                 "",
                 "Method, reasoning and",
                 "validation are 55 of the",
                 "100. A mediocre score you",
                 "understand and report",
                 "honestly beats a better one",
                 "you cannot account for."],
                kicker="PROJECT LAUNCH")
    notes(s, "Register your problem statement, dataset and named target by Week 10. Before it is approved it "
             "has to survive the four limits from Week 1: is there data, is there signal, would physics do "
             "this better, and have the conditions changed.\n\nThe rubric is published now and does not "
             "change. Note where the marks are: 55 of the 100 are for method, reasoning and validation, and "
             "only the communication and reproducibility marks are about presentation.")

    s = s_summary(prs, [
        "Classification predicts a category. Most classifiers produce a probability first, and a threshold "
        "turns it into a decision.",
        "There is nothing special about a threshold of 0.5. Choosing it is an engineering decision.",
        "There are two ways to be wrong and they almost never cost the same. Write both costs down before "
        "you build anything.",
        "A shallow decision tree is a rule a person can read and apply, which is a real advantage wherever a "
        "decision must be explained.",
        "A random forest averages many trees and is steadier than any one of them. You give up readability "
        "to get that.",
        "Read the confusion matrix before any metric. Precision asks how many of your flags were right; "
        "recall asks how many of the real cases you caught.",
        "Accuracy is the wrong instrument whenever one class is rare, and in engineering the rare class is "
        "usually the one you care about.",
        "When somebody quotes a high accuracy, ask what the class balance was. If they do not know, the "
        "number means nothing."])
    notes(s, "Statement 8 is a reflex worth acquiring. It will serve you in reading papers, vendor claims and "
             "your own work.")

    s = s_check(prs, [
        "A model reports 97 per cent accuracy on " + w["imb"] + ". What is the first thing you ask?",
        "Your model has precision 0.9 and recall 0.3. Describe in plain words what it is doing.",
        "You lower the threshold from 0.5 to 0.25. What happens to each of the four confusion matrix cells?",
        "Why might you prefer a decision tree over a random forest that scores two points higher?",
        "Feature importance says " + c["tabfeat"].split(",")[0] + " is the most important feature. What can "
        "you and can you not conclude?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question C is worth working through cell by cell. Being able to predict the direction each cell "
             "moves is what shows you understand the threshold.")

    s = s_answers(prs, [
        ("97 per cent accuracy?",
         "What is the class balance? On these records the rare class is roughly three in a hundred, so a "
         "model that never predicts it at all scores about 97 per cent while detecting nothing. Ask for "
         "the confusion matrix and the recall on the rare class before believing any accuracy figure."),
        ("Precision 0.9, recall 0.3?",
         "When it raises an alarm it is almost always right, and it misses about seven in ten of the real "
         "cases. A cautious model. Whether that is acceptable depends on whether a miss costs more than a "
         "false alarm."),
        ("Lowering the threshold to 0.25?",
         "The model flags more cases, so true positives rise and false negatives fall — recall improves. At "
         "the same time false positives rise and true negatives fall — precision worsens. You have traded "
         "misses for false alarms."),
        ("A tree over a better forest?",
         "Because you can write the tree down and hand it to somebody. Where a decision has to be explained "
         "to a client, a regulator or an operator, two points of accuracy is often a poor trade for losing "
         "the explanation. Week 12 treats this properly."),
        ("Feature importance?",
         "You can conclude that the model relied on it heavily for these data. You cannot conclude that it "
         "causes the outcome, nor that it would still rank first with a different set of features — "
         "importances shift when correlated features are added or removed. Treat the ranking as a hint "
         "about your fitted model, and look for physical evidence before you report it as a finding.")])
    notes(s, "Answer E matters for the project. Teams routinely present a feature-importance chart as though "
             "it were a physical finding. It is a property of the fitted model.")

    s = s_glossary(prs, [
        ("Classification", "Predicting which of a small set of categories a case belongs to."),
        ("Binary classification", "Two categories, such as " + w["pos"] + " and " + w["neg"] + "."),
        ("Class", "One of the categories."),
        ("Class imbalance", "One class much rarer than the other. Makes accuracy misleading."),
        ("Probability output", "The model's estimated chance that a case is positive. predict_proba."),
        ("Threshold", "The cut-off that turns a probability into a decision. 0.5 by convention only."),
        ("Decision boundary", "The surface separating the classes, at the chosen threshold."),
        ("Logistic regression", "A linear model producing a probability. Fast and interpretable."),
        ("Decision tree", "Nested if-conditions on features. Readable at shallow depth."),
        ("max_depth", "How deep a tree may grow. Deeper fits training data better and generalises worse."),
        ("Random forest", "Many trees fitted on different samples, combined by voting."),
        ("Ensemble", "Any model built by combining several models."),
        ("Confusion matrix", "The four counts: true and false positives, true and false negatives."),
        ("False positive", "A false alarm. " + w["fp"].split(":")[0] + "."),
        ("False negative", "A miss. " + w["fn"].split(":")[0] + "."),
        ("Accuracy", "Correct predictions over all predictions. Misleading under imbalance."),
        ("Precision", "Of the cases you flagged, the share that really were positive."),
        ("Recall (sensitivity)", "Of the cases that really were positive, the share you caught."),
        ("F1", "One number combining precision and recall. Convenient, and it hides the trade-off."),
        ("Feature importance", "How much the fitted model relied on each feature. Not a causal claim."),
    ], page="1 of 1")
    notes(s, "Twenty terms. Precision and recall are the two to be able to state from memory, in the domain's "
             "own language, without hesitating.")

    s = s_prose(prs, "One-page reference — building and reporting a classifier", [
        "**Write the cost table first**",
        "What does a false alarm cost? What does a miss cost? Everything else follows from those two numbers.",
        "**Check the class balance before anything**",
        "df['target'].value_counts(). If one class is rare, accuracy is already useless to you.",
        "**Same pattern as Week 8**",
        "split · fit on train · predict on test · confusion matrix · then metrics.",
        "**Read the table before the metrics**",
        "Four cells, named in your own domain's language. An empty column is invisible in a score.",
        "**Quote precision and recall separately**",
        "F1 is convenient for ranking models and hides the trade-off you are being paid to make.",
        "**The threshold is yours to set**",
        "Ask how many false alarms are tolerable per week, set the threshold to deliver that, report the "
        "recall you achieved at it.",
        "**Keep a tree if the decision must be explained**",
        "Two points of accuracy is often a poor trade for losing the written rule.",
        "**Treat feature importance as a hint**",
        "It describes your fitted model. Confirm it against the physics before reporting it."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "The first line is the one that makes the rest work. A classifier reported without its cost "
             "table is a score without a decision attached to it.")

    s = s_quiz(prs, 9,
               "A confusion matrix read for what the model does badly, and an accuracy figure quoted without the "
                        "class balance.", qr_path=qrp(code, 9))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "A model with a 97 per cent score\ncaught nothing at all.",
                  "Four numbers in a confusion matrix told you that. The score on its own hid it. The cost "
                  "of each mistake, and the confusion matrix, are what tell you whether a classifier is "
                  "worth anything.",
                  "Next week: how a model can look excellent and be worthless, and how to catch it.")
    notes(s, "Next week is the highest-value session of the semester. Everything you were told to trust this "
             "week gets tested properly, including the possibility that your own model has been cheating "
             "without your knowledge.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week09_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week10(code):
    c, w = CO[code], W10[code]
    prs = deck(); seg_reset(); notes_context(f"{code} Week 10")
    N = 9

    s = s_title(prs, code, "Can I trust\nthis model?",
                "Overfitting, cross-validation and data leakage",
                "WEEK 10  ·  " + DATE[10][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "This is the most valuable session of the semester. Everything before it was about getting a "
             "model. This is about whether the model deserves to be believed.\n\nThe uncomfortable part is "
             "that the most common failure produces a model that looks better than the honest one. A very "
             "good score is a reason for suspicion before it is a reason for satisfaction.\n\nTO TEACH: "
             "Project Milestone 1 is reviewed today. Have the checklist and the booking sheet ready.")

    s = s_objectives(prs, [
        "Diagnose overfitting and underfitting from the gap between training and test performance.",
        "Explain why a single train/test split is itself a noisy measurement.",
        "Run k-fold cross-validation and report a mean with a spread.",
        "Name the four kinds of data leakage and identify each in a pipeline.",
        "Rebuild a leaking workflow correctly using a Pipeline.",
        "Explain why a near-perfect score is grounds for suspicion.",
        "State the conditions under which your own model should not be used."],
        10, "Validation and leakage")
    notes(s, "Objective 6 is the reflex this week exists to install. In four years of professional work it "
             "will save you more embarrassment than any other habit in this course.")

    s = s_figure(prs, "How today runs", F("clock_w10.png"),
                 "Nine segments, and the last two are the ones that matter most.",
                 kicker="HOW TODAY RUNS")
    notes(s, "Nine segments. The first five cover the three ways a model goes wrong and the two techniques "
             "that catch them; the last two are about data leakage, which is the failure that produces "
             "excellent scores and worthless models.\n\nThis is the session that decides whether your "
             "project result can be believed. Every number you have quoted since Week 8 rests on the "
             "assumption that the test set was genuinely unseen, and today you find out how easily that "
             "assumption breaks without anybody noticing.\n\n"
             "TO TEACH: the leakage segment and the challenge are the core. If the session runs late, cut the "
             "cross-validation demonstration rather than either of those.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can fit a regression and a classifier and report their scores. Today: whether those "
                  "scores mean anything.")
    notes(s, "Both of the last two weeks ended with a number. This week asks what would have to be true for "
             "that number to be honest.")

    s = s_segment(prs, 2, N, "Three error stories", 15,
                  "A model can fail in three quite different ways, and they need different fixes.")
    notes(s, "Being able to tell these three apart from evidence is the diagnostic skill of the week.")

    s = s_prose(prs, "Three ways a model goes wrong", [
        "**It never learned — underfitting**",
        "Poor on the training data and poor on the test data. The model is too simple for the relationship, "
        "or the features do not carry the signal. Both scores are bad and they are close together.",
        "**It memorised — overfitting**",
        "Excellent on the training data and much worse on the test data. The model has learned the particular "
        "rows it saw, including their noise. The gap between the two scores is the tell.",
        "**It cheated — leakage**",
        "Excellent on both, and useless in service. The model was given information it will not have when it "
        "matters. This one is the hardest to spot because nothing looks wrong.",
        "**How to tell them apart**",
        "Compare the training score with the test score. Both poor means underfitting. A large gap means "
        "overfitting. Both suspiciously good means look for leakage.",
        "**And the reason this ordering matters**",
        "Underfitting and overfitting are honest failures that show up in your numbers. Leakage flatters you, "
        "so you have to go looking for it deliberately."],
        kicker="DIAGNOSIS")
    notes(s, "Write down both the training score and the test score for every model you build, every time. "
             "Most beginners record only the test score, which throws away the information needed to tell the "
             "first two stories apart.\n\nThe third story is the subject of the second half of today, and it "
             "is the one that ends up in published papers and shipped products.")

    s = s_segment(prs, 3, N, "Overfitting, and the curve", 25,
                  "Watch a model get better and better at the training data while getting worse at its job.")
    notes(s, "The curve is the single most useful picture in machine learning.")

    s = s_figure(prs, "The same data, fitted three ways", F("fit_three_panel.png"),
                 "Too simple, about right, and far too flexible. The third fit bends to chase individual "
                 "training points and is much worse on data it has not seen. Both errors are shown under each "
                 "panel.",
                 kicker="THREE FITS")
    notes(s, "Look at the third panel and ask what it would predict slightly outside the range of the data. "
             "It swings wildly, because it has fitted the noise rather than the relationship.\n\nThe numbers "
             "underneath are the honest summary: the flexible model's training error is the lowest of the "
             "three and its test error is by far the worst. A model can be made to fit any dataset perfectly "
             "and that tells you nothing.")

    s = s_figure(prs, "Training error and test error against complexity", F("overfit_curve.png"),
                 "Training error falls the whole way. Test error falls, reaches a minimum, and then rises. "
                 "The minimum is the model you want, and it is not the one with the best training score.",
                 kicker="THE CURVE")
    notes(s, "Three regions. On the left the model is too simple and both errors are high. In the middle it "
             "has captured the relationship. On the right it is fitting noise, and every extra bit of "
             "flexibility makes it worse at the only job that matters.\n\nThe practical consequence: you "
             "cannot choose model complexity by looking at the training score, because the training score "
             "always prefers the most complex model available. You need held-back data to make that choice, "
             "and choosing on the test set spends it.")

    s = s_define(prs, "Overfitting, underfitting and generalisation gap",
                 "OVERFITTING means the model has learned the particular training rows rather than the "
                 "relationship. UNDERFITTING means it is too simple to capture the relationship. The "
                 "GENERALISATION GAP is the difference between the training and the test score.",
                 "A tree with unlimited depth scores 1.00 on training and 0.62 on test — a gap of 0.38, and a "
                 "clear case of overfitting. A tree of depth 1 scores 0.55 and 0.54: honest, and too simple.",
                 "A bad model. An overfitted model is often extremely good at the data it saw. The problem is "
                 "that this is not the job.")
    notes(s, "The word 'overfitting' sounds like a synonym for 'inaccurate' and it is not. An overfitted "
             "model is the most accurate one available on the data it was fitted to. That is exactly why it "
             "is dangerous — it looks like success.\n\nThe control differs by model: max_depth on a tree, "
             "polynomial degree on a curve, the amount of regularisation on a linear model. The pattern is "
             "always the same.")

    s = s_segment(prs, 4, N, "Cross-validation", 25,
                  "One split gives you one noisy number. Five splits give you a number and an uncertainty.")
    notes(s, "This is the fix for the Week 8 problem of not knowing whether a 2 per cent improvement is real.")

    s = s_figure(prs, "Five folds, five scores", F("kfold.png"),
                 "The data is divided into five parts. Each part is held out in turn while the model is fitted "
                 "on the other four. You get five scores, and their mean and spread tell you far more than any "
                 "single one.",
                 kicker="CROSS-VALIDATION")
    notes(s, "The five scores in this figure are 4.80, 3.78, 4.67, 3.95 and 4.30, giving a mean of 4.30 with a "
             "standard deviation of 0.39. That spread is the thing a single split hides.\n\nWhich means the "
             "Week 8 question now has an answer. If model A scores 4.30 plus or minus 0.39 and model B "
             "scores 4.20 plus or minus 0.39, the difference between them is well inside the noise and you "
             "have no evidence that B is better.\n\nAlways report a mean and a spread. A single "
             "cross-validated number quoted on its own throws away the more useful half of the result.")

    s = s_define(prs, "k-fold cross-validation",
                 "Divide the data into k parts. Fit k times, each time holding out a different part for "
                 "scoring. Report the mean of the k scores and their spread.",
                 "cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error') gives five numbers. "
                 "Take the mean for the estimate and the standard deviation for the uncertainty.",
                 "The test set. Cross-validation is done on the training data to make choices. The test set "
                 "is still held back and spent once, at the very end, after every choice is final.")
    notes(s, "The 'do not confuse with' point is the one that gets broken most often. If you cross-validate "
             "to choose between models and then also report the cross-validated score as your final result, "
             "that number is optimistic — the data helped you choose.\n\nThe clean discipline: "
             "cross-validate on the training data to choose, then score the chosen model once on the test "
             "set, and report that.\n\nStratified folds keep the class balance the same in every fold, which "
             "matters whenever a class is rare. Use StratifiedKFold for classification.")

    s = s_break(prs, 10, after="The Trust Lab is next, so have Colab open when you come back.")
    notes(s, "The second half of today is leakage, which is the part worth being awake for.")

    s = s_segment(prs, 6, N, "The Trust Lab", 30,
                  "Build the curve, run the cross-validation, then break your own model on purpose.")
    notes(s, "Thirty minutes in three parts. You plot the overfitting curve so you can see the gap between "
             "training and test error open up, you replace a single split with k-fold cross-validation so "
             "your score comes with an uncertainty attached, and then you break your own model on "
             "purpose.\n\nThe third part is the one to concentrate on. Introducing a leak deliberately and "
             "watching the score jump is what makes the same pattern recognisable later, when it appears "
             "in your own work by accident.\n\n"
             "TO TEACH: the deliberate-leak exercise is the point of the block. Make sure everyone reaches it.")

    s = s_livecode(prs, "Validation, and then a deliberate leak", "OPEN COLAB — TYPE THIS WITH ME",
                   ('from sklearn.model_selection import cross_val_score\n'
                    'from sklearn.pipeline import Pipeline\n'
                    'from sklearn.preprocessing import StandardScaler\n'
                    'from sklearn.linear_model import LinearRegression\n'
                                        '\n'
                    '# CORRECT: scaling happens inside the pipeline, so it is\n'
                    '# fitted on each training fold only.\n'
                    'pipe = Pipeline([("scale", StandardScaler()),\n'
                    '                 ("model", LinearRegression())])\n'
                    '\n'
                    'scores = -cross_val_score(pipe, X_tr, y_tr, cv=5,\n'
                    '                          scoring="neg_mean_absolute_error")\n'
                    'print(f"MAE {scores.mean():.2f} +/- {scores.std():.2f}")\n'
                    '\n'
                    '# NOW THE LEAK: scale everything BEFORE splitting.\n'
                    'X_all = StandardScaler().fit_transform(X)   # sees the test rows\n'
                    '# ... refit and rescore, and watch the number improve dishonestly.'),
                   "Run the leaking version and compare. The score improves, and it is now a lie: the scaler "
                   "learned the mean and spread of the test rows, so information crossed the split. Then add "
                   "a column that is only known after the outcome and watch the score become impossible.")
    notes(s, "A Pipeline is not tidiness. It is the mechanism that makes leakage structurally difficult: "
             "everything inside it is fitted on the training part of each fold and applied to the held-out "
             "part, in the right order, automatically.\n\nOnce you have seen how small the leak in the second "
             "half of that code is — one scaler, fitted a few lines too early — you will understand why this "
             "happens in real projects. Nobody sets out to cheat. The split simply happens after something "
             "that should have come first.")

    s = s_segment(prs, 7, N, "Data leakage: four kinds", 25,
                  "The failure that produces a model which looks excellent and is worthless.")
    notes(s, "The highest-value twenty-five minutes in the semester.")

    s = s_figure(prs, "Four kinds of leakage", F("leakage_types.png"),
                 "Information reaching the model that it will not have in service. Contamination across the "
                 "split, a target that hides in a feature, using the future to predict the past, and the same "
                 "physical unit appearing on both sides of the split.",
                 kicker="LEAKAGE")
    notes(s, "All four have the same signature: a score that is better than the problem allows.\n\nTarget "
             "leakage is the one to fear most, because it survives every validation scheme you can throw at "
             "it. Cross-validation will not save you: if a feature contains the answer, every fold contains "
             "the answer.\n\nThe only defence against target leakage is the timing question, asked of every "
             "single feature: would I actually have this value at the moment I need the prediction? Anything "
             "recorded afterwards is disqualified however predictive it looks.")

    s = s_prose(prs, "The four kinds, in your own data", [
        "**Target leakage — a feature that contains the answer**",
        # The leakN strings do not end in a full stop, so supply one here
        # rather than running two sentences together on the slide.
        w["leak1"] + ". The model reports a near-perfect score and cannot predict anything in service.",
        "**Contamination across the split — preparation done too early**",
        w["leak2"] + ". Fit every transformation inside a Pipeline so it only ever sees the training part.",
        "**Group leakage — the same physical thing on both sides**",
        w["leak3"] + ". Rows from one " + w["grp"] + " are near-copies, because " + w["grpwhy"] + ". Split by "
        + w["grp"] + " rather than by row.",
        "**Temporal leakage — using the future to predict the past**",
        "Any time-ordered data split at random puts later rows in the training set and earlier rows in the "
        "test set. Split by time instead: train on the earlier period, test on the later one.",
        "**The one question that catches most of it**",
        "For every feature: would I have this value, at this moment, before the outcome is known? If not, it "
        "cannot be a feature."],
        kicker="MADE CONCRETE")
    notes(s, "Group leakage is the one that catches careful people. A random split looks scrupulous and is "
             "wrong whenever your rows come in clusters that resemble each other, which in engineering data "
             "they nearly always do.\n\nTemporal leakage is equally common in sensor data. If your data has a "
             "timestamp, a random split is almost certainly the wrong split.")

    s = s_figure(prs, "What a leak does to your score", F("leakage_score.png"),
                 "The same model and the same data, split two ways. Splitting by row gives an R-squared of "
                 "0.987. Splitting by group gives 0.557. The first number is the one you would have reported.",
                 kicker="THE SIZE OF THE EFFECT")
    notes(s, "A gap of 0.43 in R-squared, from nothing but the choice of how to split. Neither run is a "
             "mistake in the code; the difference is entirely in whether related rows were allowed to sit on "
             "both sides.\n\nThis is the figure to remember when a result looks too good. The reflex to build "
             "is: an unexpectedly excellent score is evidence of a leak until you have ruled one out.")

    s = s_segment(prs, 8, N, "Challenge: too good to be true", 30,
                  "A notebook reporting an R-squared of 0.998. Find out why.")
    notes(s, "Thirty minutes on a notebook whose model reports an R-squared of 0.998 on data it has never "
             "seen. Something in it is wrong, and your task is to name the mechanism and prove it by "
             "producing an honest score.\n\nTeams around the room have been given different faults, so a "
             "diagnosis borrowed from the next table will not fit your notebook. Work through the four "
             "kinds of leakage in order and check each one against your own code.\n\n"
             "TO TEACH: three different planted causes across the room so no diagnosis can be copied. Give "
             "no hints.")

    s = s_challenge(prs, "Too good to be true",
                    "Your team is given a notebook that reports an R-squared of 0.998 on " + c["dataset"] +
                    ".\nThe code runs. There is no error. The score is impossible.\n"
                    "Find out why, prove it with evidence, and rebuild the workflow so it reports an honest "
                    "number. Thirty minutes, no hints from me.",
                    ["Is this score plausible for this problem at all?",
                     "Which columns went into the model?",
                     "For each one: would you have it before the outcome?",
                     "When was the split made, relative to everything else?",
                     "Are any rows near-copies of each other?",
                     "What does the honest score turn out to be?"])
    notes(s, "Question 3 catches target leakage and question 4 catches contamination. Question 5 catches "
             "group leakage, and it is the one teams reach last.\n\nThe deliverable is one sentence naming "
             "the leak, the evidence for it, and the honest score after the fix. A team that finds the leak "
             "and cannot state the honest score has done half the work.\n\nTO TEACH: the three planted "
             "causes for this cohort are — (1) " + w["leak1"] + " (2) " + w["leak2"] + " (3) " + w["leak3"] +
             " Distribute them so adjacent teams have different ones, and keep the marking key to hand.")

    s = s_split(prs, "Project Milestone 1 — reviewed today", "What you bring to the review",
                "A problem statement: the engineering problem, the ML task derived from it, and the named "
                "target column.\n\n"
                "Your dataset, with its provenance and licence stated.\n\n"
                "A baseline notebook: the split, a trivial baseline, and one simple model, with the score "
                "reported as a mean and a spread.\n\n"
                "An individual contribution log in the repository, consistent with the commit history.",
                "And one new requirement",
                ["A conditions-of-use paragraph.",
                 "",
                 "State the range your data",
                 "covers, the assumptions your",
                 "model makes, and the",
                 "circumstances in which it",
                 "should not be relied on.",
                 "",
                 "That paragraph is what turns",
                 "a score into a piece of",
                 "engineering, and it carries",
                 "marks under validation.",
                 "",
                 "PM2 is due in Week 12."],
                kicker="MILESTONE 1")
    notes(s, "The conditions-of-use paragraph is new and it is the most professionally realistic thing in the "
             "project. Every model has a domain of validity, and stating yours is what a reviewer will look "
             "for first.\n\nTO TEACH: run PM1 as a four-minute stand-up per team against a printed checklist "
             "rather than a conversation. With 22 teams in CML3112 anything longer will not fit.")

    s = s_summary(prs, [
        "Record the training score and the test score for every model. Both poor means underfitting; a large "
        "gap means overfitting; both suspiciously good means look for leakage.",
        "Training error always prefers the most complex model, so you cannot choose complexity with it.",
        "A single train/test split is one noisy measurement. Cross-validation gives you a mean and a spread.",
        "Report the spread. Two models whose scores differ by less than the spread are not distinguishable.",
        "Cross-validate on the training data to make choices. Spend the test set once, at the end.",
        "Four kinds of leakage: target, contamination across the split, group, and temporal. All four produce "
        "a score better than the problem allows.",
        "For every feature ask: would I have this value before the outcome is known? If not, it is not a "
        "feature.",
        "A Pipeline prevents contamination structurally, by fitting every step on the training part only.",
        "An unexpectedly excellent score is evidence of a leak until you have ruled one out."])
    notes(s, "Statement 9 is the reflex. Install it now and it will serve you for the rest of your career.")

    s = s_check(prs, [
        "Training R-squared 0.99, test R-squared 0.62. Name the problem and one fix.",
        "Training MAE 8.4, test MAE 8.6, both poor. Name the problem and one fix.",
        "Cross-validated MAE 4.30 plus or minus 0.39 for model A, 4.20 plus or minus 0.39 for model B. Which "
        "do you choose?",
        "You have sensor data with a timestamp and you split it at random. What have you done wrong?",
        "Your model reports 0.998 and the code has no error. What is your first hypothesis, and what is the "
        "single most useful question to ask next?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide. Question E is the one that matters most.")
    notes(s, "These five are the diagnostic patterns of the week, and Practical Test 2 in Week 14 will "
             "present you with one of them.")

    s = s_answers(prs, [
        ("0.99 training, 0.62 test?",
         "Overfitting — a generalisation gap of 0.37. The model has learned these particular rows. Reduce the "
         "flexibility: cap the tree depth, lower the polynomial degree, or add regularisation. Then check the "
         "gap again."),
        ("8.4 and 8.6, both poor?",
         "Underfitting. The two scores agree, so nothing is being memorised — the model is simply too simple, "
         "or the features do not carry the signal. Try a more flexible model, and engineer better features, "
         "which is next week. If neither helps, you may have Week 1's limit two."),
        ("4.30 ± 0.39 against 4.20 ± 0.39?",
         "You have no evidence that B is better. The 0.10 difference is well inside the spread of either "
         "estimate. Choose on another ground — interpretability, cost, data requirements — and say that is "
         "what you did."),
        ("Random split on timestamped data?",
         "Temporal leakage. Later rows are in the training set and earlier rows in the test set, so the model "
         "is using the future to predict the past. In service it will never have that. Split by time: train "
         "on the earlier period, test on the later one."),
        ("0.998 with no error?",
         "First hypothesis: leakage, because the score is better than the problem allows. The most useful "
         "next question is the timing question, asked of every feature — would I have this value before the "
         "outcome is known? That single question finds target leakage, which is the commonest and the most "
         "destructive of the four.")])
    notes(s, "Answer E is the routine. Suspicion first, then the timing question, then the split, then the "
             "group structure.")

    s = s_glossary(prs, [
        ("Generalisation", "Whether a model works on data it never saw. The only thing that matters."),
        ("Underfitting", "Too simple to capture the relationship. Both scores poor and close together."),
        ("Overfitting", "Learned the training rows including their noise. Large gap between the scores."),
        ("Generalisation gap", "Training score minus test score. The size of the memorisation."),
        ("Model complexity", "How flexible a model is. Tree depth, polynomial degree, number of parameters."),
        ("Validation curve", "Training and test error plotted against complexity. Shows where the minimum is."),
        ("Cross-validation", "Fit k times, holding out a different part each time. Gives a mean and a spread."),
        ("k-fold", "The usual scheme. k=5 or k=10."),
        ("StratifiedKFold", "Folds that preserve the class balance. Use it for classification."),
        ("Fold", "One of the k parts."),
        ("Validation set", "Data used to make choices during development, keeping the test set untouched."),
        ("Spread (standard deviation)", "How much the score moves between folds. Report it always."),
        ("Data leakage", "Information reaching the model that it will not have in service."),
        ("Target leakage", "A feature that contains, or is derived from, the answer."),
        ("Contamination", "Preparation fitted before the split, so it saw the test rows."),
        ("Group leakage", "Near-copy rows from one physical unit on both sides of the split."),
        ("Temporal leakage", "Training on later data and testing on earlier data."),
        ("Pipeline", "A container that fits every step on the training part only. The structural fix."),
        ("Conditions of use", "The range and assumptions under which your model may be relied on."),
    ], page="1 of 1")
    notes(s, "Nineteen terms. The four leakage names and the timing question are the ones to carry into the "
             "project and into Practical Test 2.")

    s = s_prose(prs, "One-page reference — validating a model honestly", [
        "**Record both scores, always**",
        "Training and test. Without both you cannot tell underfitting from overfitting.",
        "**Read the gap**",
        "Both poor: underfitting. Large gap: overfitting. Both excellent: look for a leak.",
        "**Never choose complexity on the training score**",
        "It always prefers the most flexible model available.",
        "**Cross-validate to choose, test once to report**",
        "cross_val_score on the training data. The test set is spent at the very end, after every choice.",
        "**Report a mean and a spread**",
        "A difference smaller than the spread is not a difference.",
        "**Put every transformation inside a Pipeline**",
        "It makes contamination structurally difficult rather than a matter of remembering.",
        "**Ask the timing question of every feature**",
        "Would I have this value, at this moment, before the outcome is known?",
        "**Check the split matches the structure of the data**",
        "Timestamps mean split by time. Repeated units mean split by unit.",
        "**Treat a brilliant score as a symptom**",
        "Rule out a leak before you celebrate."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "These nine are the validation criteria in the project rubric and in the Test 2 rubric, where "
             "leakage control alone carries 20 of the 100 marks.")

    s = s_quiz(prs, 10,
               "Train and test scores matched to one of the three error stories, and four pipelines with one "
                        "that leaks.", qr_path=qrp(code, 10))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "The best-looking model\nin the room was cheating.",
                  "You found the leak from four numbers and one question about timing. A score that is better "
                  "than the problem allows is the most reliable warning sign in this field.",
                  "Next week: where your engineering knowledge enters the model, and how to prove it helped.")
    notes(s, "Next week is the one where a domain engineer beats a better programmer, and you get to measure "
             "that rather than assert it.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week10_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for code in CO:
        print(f"  {code}  W7: {week7(code)}  W8: {week8(code)}  "
              f"W9: {week9(code)}  W10: {week10(code)}")
    import json
    from pptxkit import LECTURER
    p = _ROOT + "/data/lecturer_notes_build_w78910.json"
    json.dump(LECTURER, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  {len(LECTURER)} lecturer notes -> {p.split('/')[-1]}")
