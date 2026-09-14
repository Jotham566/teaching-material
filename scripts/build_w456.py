# -*- coding: utf-8 -*-
"""Weeks 4, 5 and 6 as full 3-hour teaching material. Three cohorts."""
import sys, os
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from pptxkit import *   # noqa
from build_week1 import CO, FIG, OUTDIR, FOOT, qrp
from week_content import W4, W5, W6

F = lambda n: os.path.join(FIG, n)
DATE = {4: {"CML3112": "Tue 29 September 2026", "CML3113": "Fri 2 October 2026",
            "CML3111": "Fri 2 October 2026"},
        5: {"CML3112": "Tue 6 October 2026", "CML3113": "Fri 9 October — PUBLIC HOLIDAY",
            "CML3111": "Fri 9 October — PUBLIC HOLIDAY"},
        6: {"CML3112": "Tue 13 October 2026", "CML3113": "Fri 16 October 2026",
            "CML3111": "Fri 16 October 2026"}}
SLOTS = {"CML3112": "Tuesday 11:00–14:00 · Room 106",
         "CML3113": "Friday 08:00–11:00 · Room 105",
         "CML3111": "Friday 11:00–14:00 · Room 115"}
FRIDAY = ("CML3113", "CML3111")


# =====================================================================
def week4(code):
    c, w = CO[code], W4[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 4")
    N = 10

    s = s_title(prs, code, "Many measurements\nat once",
                "Collections, loops, files — and your first unguided investigation",
                "WEEK 4  ·  " + DATE[4][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Two halves today. The first teaches loops and file reading the hard way, using nothing but "
             "standard Python. The second is the first session where you are given a problem and no method.\n\n"
             "The hard way is deliberate: sixty lines today become three lines next week, and you will "
             "appreciate next week's tool because you earned it.\n\n"
             "TO TEACH: this session closes with the weekly quiz, as every session does. Have the QR ready "
             "and 20 paper copies of version A in the room in case the network is down.")

    s = s_objectives(prs, [
        "Choose between a list and a dictionary for a given engineering record, and justify the choice.",
        "Write a loop that does the same thing to every measurement in a collection.",
        "Use the accumulator pattern to total, count and average without pandas.",
        "Read a CSV file with standard Python and explain why every value arrives as text.",
        "Catch an error so a bad row does not stop the whole run — and say when you should NOT catch it.",
        "Break an open-ended data question into an ordered sequence of steps before writing any code.",
        "Report a finding from a file nobody explained to you, and defend it with evidence."],
        4, "Collections, loops and files")
    notes(s, "Objective 7 is the one that matters most and it is the one Practical Test 1 in three weeks' time "
             "actually assesses.\n\nTO TEACH: read them out, return at the end.")

    s = s_figure(prs, "How today runs", F("clock_w4.png"),
                 "The same shape. Today the second half is almost entirely you working, with me asking "
                 "questions and answering none.",
                 kicker="HOW TODAY RUNS")
    notes(s, "The same eleven-segment shape, with the second half given over almost entirely to your own work. "
             "Investigation Lab 1, which follows the break, is unguided on purpose: a file, a question and no method, "
             "which is the format Practical Test 1 uses in three weeks.\n\nTO TEACH: warn them now that the "
             "Investigation Lab is unguided and that this is on purpose. Students who are told to expect it "
             "cope far better than students who discover it.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can write a function that calculates one thing. Today: four thousand things.")
    notes(s, "Ten minutes of recall. You can already write a function that calculates one thing; today the same "
             "work happens to several hundred values at once.\n\nTO TEACH: collect A3. Two minutes of recall, "
             "then move.")

    s = s_check(prs, [
        "What is the difference between return and print, and why does it matter from next week?",
        "Your if-chain checks width > 0.30 before width > 0.50. What goes wrong and will Python tell you?",
        "You get a beam moment of 4.2 out of your function. What is the first question to ask?"],
        title="Two minutes: what stuck from Week 3?", foot="Answers next slide.")
    notes(s, "Three questions from Week 3, all of which get used within the hour. If the third one gives you "
             "trouble, the units habit is the one to fix before the practical, because the Investigation Lab "
             "will punish it.\n\nTO TEACH: thirty seconds in pairs. Take answers from people who have not "
             "spoken yet.")

    s = s_answers(prs, [
        ("return versus print?",
         "Return hands a value back so it can be used; print puts characters on screen and hands back nothing. "
         "From next week you apply functions to whole columns, and a printing function produces no column."),
        ("if-chain in the wrong order?",
         "The 0.30 branch catches everything above 0.50 as well, so the strict branch never runs. Python will "
         "not warn you — it is valid code returning the wrong action."),
        ("A moment of 4.2?",
         "In what unit? Newton-metres and kilonewton-metres are a factor of a thousand apart and only one is "
         "plausible.")])
    notes(s, "The return-versus-print answer matters most of the three. From next week you feed functions whole "
             "columns of data, and a function that only prints hands back nothing you can work with.")

    # -------- 2
    s = s_segment(prs, 2, N, "The question you cannot answer by hand", 10,
                  "Your functions work on one value at a time. Here is a file with several hundred.")
    notes(s, "Ten minutes to establish the problem before any solution appears. Your five functions from Week 3 "
             "each take one value and the file in front of you has several hundred rows; a loop is what closes "
             "that gap.\n\nTO TEACH: put a real file on screen and scroll it. Let the length do the arguing — "
             "the need for a loop should feel obvious before you name the word.")

    s = s_question(prs, "TODAY'S QUESTION",
                   '"There are several hundred readings in this file. What is the average, and how many are '
                   'outside the limit?"',
                   "You cannot do this by hand, and the five functions you wrote last week do not help — they "
                   "each take one value. You need a way to say: do this same thing to every single one.")
    notes(s, "Work out roughly how long that file would take by hand before you read on. Then note that you "
             "will do this every week for the rest of the course, on files a thousand times bigger than this "
             "one.\n\nTO TEACH: ask how long it would take by hand and let someone estimate. Then make the "
             "point about scale.")

    # -------- 3
    s = s_segment(prs, 3, N, "Two ways to hold many values", 20,
                  "A list keeps them in order. A dictionary keeps them by name. Almost every engineering "
                  "record is one or the other.")
    notes(s, "Twenty minutes on lists and dictionaries. Almost every engineering record you meet is naturally "
             "one or the other, and choosing correctly saves you from a class of bug that is very hard to see "
             "later.\n\nTO TEACH: twenty minutes. Keep it concrete — use real record types from their "
             "discipline.")

    s = s_figure(prs, "Lists and dictionaries", F("list_vs_dict.png"),
                 "A list is accessed by position, counting from zero. A dictionary is accessed by a label you "
                 "chose. Use a list when order is the meaningful thing; use a dictionary when the label is.",
                 kicker="COLLECTIONS")
    notes(s, "Counting from zero surprises everyone once: the first item is [0] and the last item of a "
             "twelve-item list is [11]. Ask for [12] and you get an IndexError.\n\nMost engineering records are "
             "naturally dictionaries — a reading belongs to " + c["unitid"] + ", and position 43 means "
             "nothing to anybody reading your code. "
             "Next week's DataFrame is essentially a table of both: rows in order, columns by name.\n\n"
             "TO TEACH: ask the room for one example of each from their own field before you show the answers. "
             "Their examples are better than yours because they own them.")

    s = s_define(prs, "List, dictionary, and index",
                 "A LIST is an ordered sequence, written in square brackets. A DICTIONARY maps labels to "
                 "values, written in curly braces. An INDEX is the position or the label you use to get one "
                 "item out.",
                 'readings = [12.4, 13.1, 11.8] is a list; readings[0] is 12.4. '
                 'readings = {"' + c["unitid"] + '": 78.2} is a dictionary; '
                 'readings["' + c["unitid"] + '"] is 78.2.',
                 "Each other. If you find yourself remembering that position 3 means the pH reading, you "
                 "wanted a dictionary.")
    notes(s, "The 'do not confuse with' line is the practical test for choosing between them. Any time you are "
             "keeping a mental note of what a position means, the label belongs in the code instead.\n\n"
             "TO TEACH: a KeyError from asking a dictionary for a label it does not have is one of the bugs "
             "in this week's quiz. Mention it now.")

    # -------- 4
    s = s_segment(prs, 4, N, "The accumulator", 25,
                  "One pattern, and it is most of what you will write today.")
    notes(s, "Twenty-five minutes on one pattern, and it is most of what you write today. The file reading in "
             "the file-reading block becomes mechanical once the accumulator is clear, so this is the block to concentrate "
             "on.\n\nTO TEACH: this is the conceptual core of the session. Do not rush it — the file reading is "
             "mechanical once this is understood.")

    s = s_figure(prs, "A loop, traced step by step", F("accumulator_trace.png"),
                 "There is no magic in a loop. It takes each value in turn and updates a running total and a "
                 "running count. The table shows exactly what is in each variable after every step.",
                 kicker="THE ACCUMULATOR")
    notes(s, "The accumulator pattern is: start a variable at zero BEFORE the loop, add to it INSIDE the loop, "
             "use it AFTER the loop. Three positions, and getting them wrong is the classic bug.\n\n"
             "total = total + value reads right to left, exactly as in Week 3: take what is in total, add "
             "value, put it back.\n\nTO TEACH: draw the trace table on the board and fill it in one row at a "
             "time, asking the room for each value. It makes the loop mechanical rather than mysterious, and "
             "it takes four minutes.")

    s = s_figure(prs, "The bug that gets everybody once", F("accumulator_bug.png"),
                 "The same loop, with total = 0 in the right place and in the wrong place. On the right it is "
                 "reset every time round, so at the end it holds only the last value — and the mean is wrong by "
                 "a factor of the number of rows. No error appears.",
                 kicker="A SILENT WRONG ANSWER")
    notes(s, "This is a Week 3 lesson in a new costume: it runs, and the answer is wrong. The only defence is "
             "knowing roughly what the answer should be.\n\nThe tell is that the 'total' comes out suspiciously "
             "close to a single reading rather than to hundreds of them. If your total of three hundred "
             "readings looks like one reading, you have this bug.\n\nTO TEACH: make the mistake live and let "
             "them spot it from the magnitude. This exact bug appears in the quiz at the end of the session.")

    s = s_define(prs, "Loop, iteration, and the three positions",
                 "A LOOP runs the same block once for every item in a collection. One pass is an ITERATION. "
                 "An accumulator needs three positions: started BEFORE the loop, updated INSIDE it, used "
                 "AFTER it.",
                 "total = 0 sits before. total = total + value sits inside, indented. print(total) sits after, "
                 "un-indented. The indentation is what tells Python which lines are inside.",
                 "Repeating code by copying it. A loop written for twelve readings works unchanged for twelve "
                 "thousand; twelve copied lines do not.")
    notes(s, "Indentation in Python is syntax. The lines indented under the for statement run inside the loop "
             "and the lines left un-indented run outside it, so shifting one line by four spaces changes what "
             "the program does. That single shift is exactly the accumulator bug on the previous slide.\n\nTO "
             "TEACH: this is the moment to make the indentation point explicitly, because IndentationError is "
             "the traceback question in this week's quiz.")

    s = s_check(prs, [
        "readings = [12.4, 13.1, 11.8]. What is readings[0], and what happens if you ask for readings[3]?",
        "You have one reading for each of forty named " + c["units_pl"] + ". List or dictionary, "
        "and why?",
        "In an accumulator loop, where must total = 0 go, and what happens if it goes one line lower?"],
        title="Two minutes: check the foundations",
        foot="Answers next slide. Write something for each first.")
    notes(s, "Three questions on the foundations before the file reading starts. Question C is the accumulator "
             "bug again; if it is not solid, go back to the previous figure, because everything after the break "
             "depends on it.\n\nTO TEACH: pulse check before the file reading. If question C is weak, re-show "
             "the accumulator_bug figure — everything after the break depends on it.")

    s = s_answers(prs, [
        ("readings[0], and readings[3]?",
         "readings[0] is 12.4 — counting starts at zero, so the first item is [0]. readings[3] raises an "
         "IndexError, because a three-item list only has positions 0, 1 and 2."),
        ("Forty named " + c["units_pl"] + "?",
         "A dictionary, keyed by name. With a list you would have to remember that position 17 means "
         + c["unitid"] + ", which is exactly the situation a dictionary exists to prevent."),
        ("Where does total = 0 go?",
         "Before the loop, un-indented. One line lower — indented, inside the loop — it resets on every "
         "iteration, so at the end it holds only the last value. No error appears, and the mean comes out "
         "wrong by a factor of the number of rows.")])
    notes(s, "Answer C is worth reading twice. Moving total = 0 one line lower puts it inside the loop, so it "
             "resets on every iteration and the mean comes out wrong by a factor of the number of rows, with no "
             "error message anywhere. This exact bug appears in the quiz at the end of the session.\n\nTO "
             "TEACH: say that the bug in answer C is in the quiz.")

    # -------- 5
    s = s_segment(prs, 5, N, "Reading a real file", 25,
                  "Everybody types. And yes, this is deliberately more work than it needs to be.")
    notes(s, "Twenty-five minutes with everyone typing, and it is deliberately more work than it needs to be. "
             "Next week the same job takes three lines of pandas. Doing it the long way once is what lets you "
             "diagnose those three lines when they misbehave.\n\nTO TEACH: lockstep. Say out loud that next "
             "week this becomes three lines — then say they will understand what those three lines do, which is "
             "why it is worth doing the long way once.")

    s = s_figure(prs, "What happens when you read a file", F("file_pipeline.png"),
                 "A file on disk is characters. Reading it gives you text, one line at a time. Splitting gives "
                 "you fields — still text. Only float() turns a field into a number you can do arithmetic with.",
                 kicker="THE PIPELINE")
    notes(s, "This is the single most useful thing to understand about data files, and it is the cause of the "
             "TypeError you met in Week 3. A file has no idea what a number is. Everything arrives as text "
             "until you convert it.\n\nNext week pandas does the conversion for you, and it will sometimes get "
             "it wrong — usually when one row has a stray unit in it. You will only be able to diagnose that "
             "because you did it by hand today.\n\nTO TEACH: this is the forward reference that makes Week 6's "
             "'a number stored as text' defect make sense.")

    s = s_livecode(prs, "Reading " + w["file"], "OPEN COLAB — UPLOAD THE FILE FIRST",
                   ('import csv\n'
                    '\n'
                    'total = 0.0        # BEFORE the loop\n'
                    'count = 0\n'
                    'over_limit = 0\n'
                    '\n'
                    'with open("' + w["file"] + '") as f:\n'
                    '    for row in csv.DictReader(f):\n'
                    '        value = float(row["' + w["col"] + '"])   # text -> number\n'
                    '        total = total + value          # INSIDE the loop\n'
                    '        count = count + 1\n'
                    '        if value > ' + w["limit"] + ':\n'
                    '            over_limit = over_limit + 1\n'
                    '\n'
                    'print(f"mean {total / count:.2f} over {count} rows")   # AFTER\n'
                    'print(f"{over_limit} above ' + w["limit"] + ' ' + w["unit"] + '")'),
                   "Delete the float() and run it. You get a TypeError about adding a string to a float — the "
                   "same error as Week 3, now with a reason: everything read from a file is text. Then move "
                   "total = 0.0 inside the loop and watch the mean collapse to the last value, with no error "
                   "at all.")
    notes(s, "csv.DictReader gives you each row as a dictionary keyed by the column headings, which is why "
             "row[\"value\"] works. That is also why a typo in a column name gives a KeyError rather than "
             "silently returning nothing.\n\nThe with block closes the file for you when it finishes, even if "
             "something goes wrong inside it. Use it every time.\n\nTO TEACH: make BOTH mistakes. The first "
             "crashes and is a gift; the second is silent and is the dangerous one. Contrast them explicitly.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. The Investigation Lab after the break is unguided and it needs you fresh.\n\nTO "
             "TEACH: take it. The Investigation Lab needs them fresh.")

    # -------- 7
    s = s_segment(prs, 7, N, "When a row is broken", 10,
                  "Real files have bad rows. You have two choices and they are not equally good.")
    notes(s, "Ten minutes on what to do with a row that cannot be read. There are two choices, and the part "
             "usually skipped is knowing when catching the error is the wrong answer.\n\nTO TEACH: short "
             "segment, but the 'when NOT to catch' point is important and usually skipped.")

    s = s_livecode(prs, "Catching an error, and counting it", "ADD THIS TO YOUR LOOP",
                   ('        try:\n'
                    '            value = float(row["' + w["col"] + '"])\n'
                    '        except ValueError:\n'
                    '            skipped = skipped + 1     # count it, do not hide it\n'
                    '            continue                  # move to the next row\n'
                    '\n'
                    '# ... and at the end, always report it:\n'
                    'print(f"skipped {skipped} rows that could not be read")'),
                   "Replace the except body with just 'pass'. It runs, no error, and you have silently thrown "
                   "away an unknown number of rows. Your mean is now computed on a subset you cannot describe. "
                   "This is worse than crashing.")
    notes(s, "try and except let you carry on past a bad row instead of stopping, which is often the right call "
             "— one malformed row in three hundred should not end the run.\n\nCatching an error silently is a "
             "serious mistake. Skip forty rows without counting them and your answer describes 260 readings out "
             "of 300, and you can say nothing about the forty you dropped; they may all be the extreme ones. "
             "Count what you skip and report the count every time.\n\nWhen should you leave it uncaught? When "
             "the failure means your assumption about the data is wrong. If every row fails you have the wrong "
             "file or the wrong column name, and a crash tells you that in one second.\n\nTO TEACH: 'except: "
             "pass' is the single worst line a data engineer can write. Say so plainly.")

    # -------- 8
    s = s_split(prs, "Practical: build a reading report", "What to build",
                "A script that reads " + w["file"] + " and reports:\n\n"
                + w["report"] + "\n\n"
                "CORE: it runs, and the numbers are right.\n"
                "STRETCH: survive a file with a blank line, a stray unit in a numeric column, and a duplicated "
                "header row — which is exactly what Week 6 formalises.",
                "The file you are given",
                [w["file"], "", str(w["rows"]) + " rows.", "", "Columns:"] +
                ["  " + x.strip() for x in w["cols"].split(",")],
                kicker="PRACTICAL — 30 MINUTES")
    notes(s, "The skipped-row count is part of the deliverable. A report that does not say how "
             "much data it ignored leaves the reader unable to judge it.\n\nTO TEACH: circulate and ask for the expected magnitude "
             "before looking at anyone's code. Then ask 'how many rows did you skip?' — the students who have "
             "not counted will realise why it matters.")

    s = s_worked(prs, "Decomposing a question before you write any code",
                 "You are about to be handed a file and told to find something interesting. That is not a "
                 "coding problem, it is a thinking problem, and this is the routine.",
                 ["Read the column names and say out loud what each one probably is, and in what unit. If you "
                  "cannot guess, that column is your first question.",
                  "Ask what this file is a record OF. Somebody collected it for a reason — what decision was "
                  "it collected to support?",
                  "Pick one column you could imagine an engineer caring about, and say why you picked it.",
                  "Ask the smallest possible question about it: what is its range, and does anything look "
                  "impossible? Answer that before anything ambitious.",
                  "Now ask a comparison question: does that column differ between groups — between machines, "
                  "operators, dates, materials? Comparisons are where findings live.",
                  "Before you believe the answer: could something else explain it? Name one alternative, and "
                  "say what evidence would rule it out."],
                 "Steps 1 to 4 take five minutes and will stop you from spending twenty minutes on the wrong "
                 "column. Step 6 is the difference between a finding and a coincidence.")
    notes(s, "This routine is what Practical Test 1 assesses in three weeks. The subject of that test is what "
             "to do when nobody has told you what to do; the pandas syntax carries a small part of the "
             "marks.\n\nStep 2 is the one beginners skip and the one that most often produces the interesting "
             "question. Data is never collected by accident, so asking what decision it was collected to "
             "support tells you what it can answer.\n\nTO TEACH: walk this on the board with the actual column "
             "names from the file before you release them to work. Five minutes here saves the whole activity "
             "from becoming aimless clicking.")

    # -------- 9
    s = s_challenge(prs, "Investigation Lab 1 — find something interesting",
                    "Your team gets " + w["file"] + " — " + str(w["rows"]) + " rows, and no column "
                    "dictionary.\n"
                    "No suggested method. No worked example. No help from me.\n"
                    "Twenty-five minutes and one instruction: find something interesting, and be ready to "
                    "defend it with evidence from the data.",
                    ["What are you trying to find?",
                     "Why did you choose that column?",
                     "What does that number mean physically?",
                     "Is that a real pattern or a coincidence?",
                     "What would change your mind?",
                     "What is the engineer supposed to DO about it?"])
    notes(s, "This is the first fully unguided activity of the semester and it sets the pattern for the rest of "
             "them: a file, a question and no method. Marks go to the evidence you can show, so a team that "
             "finds nothing and can say what it ruled out and how has done real work. Most real investigations "
             "end that way.\n\nWork the six questions on the slide in order, and expect to give a "
             "sixty-second findings pitch at the end.\n\nTO TEACH: what is actually in the file: " + w["story"] +
             "\n\n" + w["herrings"] + "\n\nYour only permitted moves are the six questions — carry the printed "
             "card and do not touch a keyboard. Sixty-second findings pitch per team at the end. Some teams "
             "will be frustrated: say plainly that most real investigations end without a finding, and that "
             "this is why the marks are on method.")

    # -------- 10
    s = s_points(prs, "Before you leave the room",
                 [("This week's quiz — five minutes, and it counts",
                   "Five questions on this session. QR code on the screen, answers on your phone, score and "
                   "an explanation immediately. Worth one per cent. There are twelve across the semester and "
                   "the best ten count, so a missed session costs you nothing and there are no resits to "
                   "arrange."),
                  ("Assignment A4 — due at the start of Week 5",
                   "Your reading report script, including the skipped-row count, plus 150 words on the most "
                   "interesting thing you found in the Investigation Lab and why an engineer should care about "
                   "it.")],
                 kicker="QUIZ AND ASSIGNMENT", numbered=False)
    notes(s, "The quiz format matters more than its content: two of the five questions show code that "
             "runs cleanly and returns a wrong answer and ask for the cause, one shows a traceback, one "
             "gives you an output to interpret, and one sets a constraint. There is nothing to memorise and "
             "revising definitions will not help — doing A3 properly was the preparation. A4 is due at the "
             "start of Week 5, and the skipped-row count is part of the deliverable.\n\nTO TEACH: afterwards "
             "spend five minutes on the responses-by-question view. Any question most of the room got wrong is a "
             "five-minute reteach at the start of Week 5, not a hard question. Bank: "
             "assessment-tools/quiz_04_questions.md")

    # -------- revision
    s = s_summary(prs, [
        "A list holds values in order and is accessed by position, counting from zero. A dictionary holds them "
        "by label. Most engineering records are dictionaries.",
        "The accumulator pattern has three positions: start at zero before the loop, add inside it, use the "
        "result after it. Getting the first one wrong is silent.",
        "Everything read from a file arrives as text. float() or int() converts it, and forgetting to is the "
        "TypeError you met in Week 3.",
        "csv.DictReader gives each row as a dictionary keyed by the column headings.",
        "try and except let you survive a bad row — but count what you skipped and report the count. "
        "'except: pass' throws away data you cannot describe.",
        "Crash rather than catch when the error means your assumption about the file is wrong.",
        "Given a file and no instructions, the method is: decide what you are looking for, choose a column and "
        "say why, check whether the pattern is real, and say what would change your mind."])
    notes(s, "Seven statements covering the session. The second and the fifth carry the most weight later: the "
             "three positions of an accumulator, and counting what you skipped.\n\nTO TEACH: return to the "
             "objectives slide and ask for hands against each.")

    s = s_check(prs, [
        "You total 300 readings and the total comes out at 41.7, while a single typical reading is about 40. "
        "What has almost certainly happened?",
        "Your loop crashes on row 84 with a ValueError. Give one good reason to catch it and one good reason "
        "not to.",
        "Why does row[\"value\"] give you text rather than a number, when the file clearly contains numbers?",
        "You skipped 40 of 300 rows and reported a mean. What is wrong with the sentence 'the mean reading is "
        "41.2'?",
        "In the Investigation Lab you found a pattern. What is the minimum you must be able to say before you "
        "call it a finding?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question A is the accumulator bug seen from the magnitude alone, which is how you will actually "
             "catch it.")

    s = s_answers(prs, [
        ("Total of 41.7 for 300 readings?",
         "total = 0 is inside the loop instead of before it, so it resets every time round and holds only the "
         "last value. The tell is that a total of hundreds of readings looks like one reading."),
        ("Catch it, or not?",
         "Catch it if one malformed row in three hundred should not stop the run — count it and report it. Do "
         "NOT catch it if the failure means your assumption is wrong: if every row fails you have the wrong "
         "file or the wrong column name, and crashing tells you that immediately."),
        ('Why is row["value"] text?',
         "Because a file stores characters. It has no type information at all. Python hands you "
         "exactly what is written there and leaves the conversion to you."),
        ("Skipped 40 of 300?",
         "It is the mean of 260 readings, not 300, and you cannot describe the 40 you dropped — they may all "
         "be the extreme ones. State the count and the proportion every time: 'mean 41.2 over 260 of 300 rows; "
         "40 rows could not be read.'"),
        ("Minimum before calling it a finding?",
         "What you looked at, what the pattern is in physical terms, what else could explain it, and what "
         "would change your mind. Without the last two you have a coincidence.")])
    notes(s, "Answer E is the standard Practical Test 1 marks against in three weeks: what you looked at, what "
             "the pattern is in physical terms, what else could explain it, and what would change your mind. "
             "Without the last two you have a coincidence.")

    s = s_glossary(prs, [
        ("List", "An ordered sequence in square brackets. Accessed by position, counting from zero."),
        ("Dictionary (dict)", "Labels mapped to values, in curly braces. Accessed by label."),
        ("Index", "The position or label used to get one item out."),
        ("IndexError", "You asked a list for a position it does not have."),
        ("KeyError", "You asked a dictionary for a label it does not have. Usually a typo in a column name."),
        ("Loop (for)", "Do the same thing to every item in a collection."),
        ("Accumulator", "A variable that builds up a result across a loop. Start it BEFORE the loop."),
        ("Iteration", "One pass through the loop body."),
        ("open() and with", "Open a file. The with block closes it for you, even if something fails inside."),
        ("csv.DictReader", "Reads a CSV, giving each row as a dictionary keyed by the column headings."),
        ("float() / int()", "Convert text to a number. Everything read from a file needs this."),
        ("ValueError", "The right type of operation on a value it cannot handle — float(\"abc\")."),
        ("TypeError", "An operation the type does not allow — \"12\" + 3."),
        ("try / except", "Attempt something; if it raises a named error, handle it instead of stopping."),
        ("continue", "Skip the rest of this pass and move to the next item."),
        ("except: pass", "Catching an error and doing nothing. Throws away data you cannot describe. Do not."),
        ("Decomposition", "Breaking a question into an ordered sequence of steps before writing code."),
        ("Evidence", "The numbers from the data that support your claim. A finding without it is a guess."),
    ], page="1 of 1")
    notes(s, "Eighteen terms. Five of them are error names, and being able to recognise an error by name is "
             "most of what makes a beginner faster.")

    s = s_prose(prs, "One-page reference — reading a file without pandas", [
        "**The three positions of an accumulator**",
        "total = 0 before the loop. total = total + value inside it. print(total) after it.",
        "**Every value from a file is text**",
        "float(row[\"" + w["col"] + "\"]). Forget it and you get a TypeError.",
        "**Always count what you skipped**",
        "And always report it, as a count and a proportion. A mean without that is a mean of something you "
        "cannot describe.",
        "**Never write except: pass**",
        "Count it, or let it crash. Silence is the one option that is always wrong.",
        "**Sanity-check by magnitude**",
        "Does the total look like hundreds of readings or like one? Does the mean look like a typical value? "
        "That single check catches the accumulator bug every time.",
        "**Given a file and no instructions**",
        "What am I looking for · which column and why · is the pattern real · what would change my mind · what "
        "should an engineer do about it.",
        "**Before you submit**",
        "Restart and Run All. Report the skipped count. State the units."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide. The magnitude check is the line that will save you most often — a total of "
             "three hundred readings that looks like a single reading is the accumulator bug every time.")

    s = s_quiz(prs, 4,
               "An accumulator reset inside the loop, a range off by one, and a skipped-row count nobody "
                        "reported.", qr_path=qrp(code, 4))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You just investigated a file\nnobody explained to you.",
                  "Four weeks ago most of you had never written a line of code. Next week the same work takes "
                  "three lines instead of sixty, and the datasets stop being teaching files and start being "
                  "real.",
                  "Next week: pandas, and how to find data you can actually trust.")
    notes(s, "Four weeks ago most of you had never written a line of code, and you have just investigated a "
             "file that nobody explained to you. Next week is a real step up in pace: the same work takes "
             "three lines instead of sixty, and the datasets stop being teaching files.\n\n"
             + ("This cohort does NOT meet next week — Friday 9 October is Independence Day. The Week 5 "
                "material reaches you as a recording of the Tuesday session plus the notebook, published by "
                "Wednesday 7 October, with a 45-minute online clinic that week, and Week 6 opens with a "
                "30-minute consolidation of it.\n\n"
                "TO TEACH — THIS COHORT: you will NOT meet next week. Friday 9 October is Independence Day. "
                "The Week 5 material comes to you as a recording of the Tuesday session plus the notebook, "
                "published by Wednesday 7 October, with a 45-minute online clinic that week. Week 6 opens with "
                "a 30-minute consolidation. Say this now, clearly, and put the dates on the board — do not let "
                "them find out by turning up to a locked room."
                if code in FRIDAY else
                "TO TEACH — THIS COHORT: you teach Week 5 as normal on Tuesday 6 October. RECORD IT. The two "
                "Friday cohorts lose their Week 5 session to Independence Day and your recording is what they "
                "get instead, so set the recording up before you start."))

    prs.save(os.path.join(OUTDIR, f"{code}_Week04_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week5(code):
    c, w = CO[code], W5[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 5")
    N = 10

    s = s_title(prs, code, "pandas: the engineer's\ndata table",
                "And how to find data you can actually trust",
                "WEEK 5  ·  " + DATE[5][code],
                ("NO CLASS — issued as a recording plus notebook by Wed 7 Oct, with an online clinic"
                 if code in FRIDAY else SLOTS[code]) + "  ·  " + FOOT)
    notes(s, ("THIS COHORT DOES NOT MEET IN WEEK 5 — Friday 9 October is Uganda Independence Day.\n\n"
              "This deck is issued as an asynchronous package alongside a recording of the Tuesday session and "
              "the Twelve Questions notebook, by Wednesday 7 October. Work through it, attempt the practical, "
              "and bring your questions to the 45-minute online clinic. Week 6 opens with a 30-minute "
              "consolidation of this material.\n\nDo not skip it. Everything from Week 6 onwards assumes it, "
              "and it is the single most load-bearing session of the semester.\n\n"
              "TO TEACH: publish by Wed 7 Oct. Hold the clinic. Open Week 6 with the consolidation."
              if code in FRIDAY else
              "This is the most load-bearing session of the semester — everything from Week 6 onwards assumes "
              "it.\n\nTO TEACH: RECORD THIS SESSION. Both Friday cohorts lose their Week 5 to Independence Day "
              "and this recording is what they receive instead. Set up the recording before you start, and "
              "check it captured the screen as well as the audio."))

    s = s_objectives(prs, [
        "Load a CSV into a DataFrame and describe what you have: rows, columns, types and missing values.",
        "Select a column, select rows, and filter with a condition.",
        "Group by a category and compute a summary for each group.",
        "Create a new column that encodes something you know as an engineer.",
        "Explain why one line of pandas replaces the sixty lines you wrote last week.",
        "Find a dataset on Kaggle or the UCI repository and state its provenance, licence and limitations.",
        "Judge whether a dataset can actually answer a stated engineering question — before using it."],
        5, "NumPy, pandas, and finding data")
    notes(s, "Objective 7 is the one nobody expects and the one that separates a useful analysis from a wasted "
             "fortnight.\n\nTO TEACH: read them out, return at the end.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "Sixty lines of loop last week. Three lines this week — and now you know what they do.")
    notes(s, "Ten minutes of recall. Last week's sixty lines of loop become three lines this week, and you now "
             "know what those three lines do underneath.\n\nTO TEACH: collect A4. Reteach anything last week's quiz "
             "showed the room got wrong — that is what the responses-by-question view is for.")

    s = s_segment(prs, 2, N, "Sixty lines becomes three", 20,
                  "The case for the tool, made by the tool.")
    notes(s, "Twenty minutes making the case for the tool before any of its syntax appears. The comparison on "
             "the next slide is the whole argument.\n\nTO TEACH: this is the motivating comparison. Show it "
             "before teaching any syntax.")

    s = s_figure(prs, "The same job, two ways", F("loops_vs_vectorised.png"),
                 "The same answer, agreeing to nine decimal places. Ten statements of standard Python against "
                 "three of pandas. The timings shown were measured on this machine on a million rows — yours "
                 "will differ, but the direction will not.",
                 kicker="WHY PANDAS")
    notes(s, "Two honest points about the speed. pandas is faster because the loop happens in compiled code "
             "rather than in Python, and the algorithm is the same one you wrote last week. The stronger reason "
             "to use it is that three lines leave far less room for the accumulator bug than sixty lines "
             "do.\n\nThe two answers differ in the last few bits because the additions happen in a different "
             "order. That is floating-point arithmetic, exactly as in Week 3, and it is why you compare with a "
             "tolerance.\n\nTO TEACH: do not overclaim the speed figure. It was measured on one machine and the "
             "slide says so.")

    s = s_segment(prs, 3, N, "NumPy: arithmetic on many numbers at once", 20,
                  "One idea: do the operation to the whole column at once.")
    notes(s, "Twenty minutes on one idea: do the operation to the whole column at once. Arrays and elementwise "
             "arithmetic are all you need from NumPy this semester.\n\nTO TEACH: keep NumPy light. Arrays and "
             "elementwise arithmetic. Broadcasting is a footnote and should stay one.")

    s = s_define(prs, "Array, and vectorisation",
                 "An ARRAY is a column of numbers of the same type. VECTORISATION means writing the operation "
                 "once for the whole array instead of looping over it.",
                 "If readings is an array of " + c["arrq"] + ", readings - 25 gives you a whole new array of "
                 "temperature rises. No loop, one line.",
                 "A list. A list can hold anything and has no arithmetic; an array holds one type and "
                 "arithmetic applies to all of it at once.")
    notes(s, "This is the idea the rest of the course rests on. Every pandas operation you meet is really "
             "'do this to the whole column'.\n\nWhy it matters practically: a loop with an accumulator has "
             "three places to go wrong. temps - 25 has none.\n\nTO TEACH: demonstrate it against last week's "
             "loop for the same task. The contrast is the lesson.")

    s = s_segment(prs, 4, N, "The DataFrame", 25,
                  "A table with named columns and a numbered index. From here to the end of the year, this is "
                  "where your data lives.")
    notes(s, "Twenty-five minutes on the DataFrame, and it is the most load-bearing block of the semester. "
             "Every week from here to the end of the year keeps its data in one.\n\nTO TEACH: budget "
             "generously. This is the most important twenty-five minutes of the semester.")

    s = s_figure(prs, "The anatomy of a DataFrame", F("dataframe_anatomy.png"),
                 "Rows down the side with an index, columns across the top with names, and every column has a "
                 "type. One column on its own is called a Series. The shape tells you how many rows and "
                 "columns you have.",
                 kicker="ANATOMY")
    notes(s, "Compare this directly with the Week 1 data-table figure: the same picture, now with the names "
             "pandas uses. Features are columns, the target is a column, one row is one example.\n\nThe dtype "
             "row is the one to watch. A column that should be numbers but shows 'object' contains text "
             "somewhere — usually one row with a stray unit in it — and that is a Week 6 defect you can now "
             "diagnose.\n\nTO TEACH: run .info() on the anchor dataset live and read the dtypes out loud. It "
             "takes ninety seconds and it prevents a great deal of confusion later.")

    s = s_livecode(prs, "Loading and describing " + w["anchor"], "OPEN COLAB — RUN EACH LINE SEPARATELY",
                   ('import pandas as pd\n'
                    '\n'
                    'df = pd.read_csv("' + w["file"] + '")\n'
                    '\n'
                    'df.shape          # (rows, columns)\n'
                    'df.head()         # the first five rows\n'
                    'df.info()         # column names, types, non-null counts\n'
                    'df.describe()     # count, mean, std, min, quartiles, max\n'
                    '\n'
                    '' + w["derived_code"] + '\n'
                    'df.head()'),
                   "Type df.shape without the brackets and run it. You get something about a 'bound method' "
                   "instead of the numbers — because you asked for the function itself rather than calling it. "
                   "It is the Week 3 define-versus-call distinction, in a new place.")
    notes(s, "Four commands to run on every dataset you ever open, in this order: shape, head, info, describe. "
             "They answer how big, what does it look like, what types are there, and what are the "
             "ranges.\n\ndescribe() is where you first see something wrong. A minimum of -999 in a column that "
             "cannot be negative is a sentinel value standing in for missing data, and it will destroy every "
             "mean you compute. That is Week 6.\n\nNote that shape has no brackets and head() does. Attributes "
             "describe the object; methods do something to it.\n\nTO TEACH: run all four on the real anchor "
             "dataset and narrate what each tells you.")

    s = s_define(prs, "Attribute and method",
                 "An ATTRIBUTE is a fact about the object, written without brackets. A METHOD does something "
                 "to the object and is written with brackets, even when they are empty.",
                 "df.shape is an attribute — it just is (rows, columns). df.head() is a method — it goes and "
                 "gets the first rows for you. df.dtypes attribute; df.describe() method.",
                 "Each other, and getting it wrong is a confusing error rather than a helpful one. Ask for "
                 "df.shape() and you get 'tuple object is not callable'; ask for df.head and you get a "
                 "description of the method instead of your data.")
    notes(s, "This distinction explains an error message that otherwise looks like nonsense. 'Not callable' "
             "means you put brackets after something that is not a function.\n\nThere is no rule you can "
             "derive — you learn which is which by use. The four you need constantly: shape and dtypes have no "
             "brackets; head() and describe() do.\n\nTO TEACH: make both mistakes live. Thirty seconds, and it "
             "removes a recurring source of confusion for the rest of the semester.")

    s = s_worked(prs, "Answering one of the twelve questions, properly",
                 "Question: " + w["qs"][3] + "  Here is the whole routine, including the part that is not code.",
                 ["Decide what the answer will look like before you write anything. A single number with a "
                  "unit? A small table? That tells you which operation you need.",
                  "Check the column exists and is numeric. df.info() — if the dtype is 'object' you must fix "
                  "that first, because no arithmetic will work.",
                  "Write the smallest expression that answers it. One line if possible.",
                  "Look at the answer and ask whether the magnitude is plausible for this quantity. This is "
                  "the Week 3 habit, applied to a table.",
                  "State it as a sentence with its unit. Not a printed Series — a sentence an engineer could "
                  "put in a report.",
                  "Say what it does NOT tell you. One clause is enough, and it is what turns an answer into "
                  "an analysis."],
                 "Steps 1, 4 and 6 involve no code at all, and they are where the marks are in this course.")
    notes(s, "The temptation is to start typing at step 3. Doing steps 1 and 2 first is faster overall, "
             "because it stops you computing a mean of a column that is secretly text.\n\nStep 6 is what "
             "distinguishes a pass from a merit in the Data Analysis Project. 'The mean 28-day strength is "
             "35.8 MPa — but that is across all mixes and all ages, so it does not tell us anything about any "
             "particular mix design' is a far better answer than the number alone.\n\nTO TEACH: work this "
             "example live, out loud, including the two non-code steps. Then release them onto the other "
             "eleven.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. The segment after the break is dense — selecting, filtering and grouping in one "
             "go.\n\nTO TEACH: take it. The next segment is dense.")

    s = s_segment(prs, 6, N, "Selecting, filtering, grouping", 30,
                  "Three operations that answer most engineering questions you will ask of a table.")
    notes(s, "Thirty minutes, all hands on keyboards. Three operations, select, filter and group, answer most "
             "engineering questions you will ask of a table, and the twelve questions on the practical slide "
             "are how to practise them.\n\nTO TEACH: thirty minutes, all hands-on. Give them the twelve "
             "questions to work through as you go rather than teaching all three operations first.")

    s = s_figure(prs, "Filtering with a condition", F("boolean_mask.png"),
                 "A condition applied to a column gives you a column of True and False. Put that inside square "
                 "brackets and you get only the rows where it was True. This is how every filter in pandas "
                 "works.",
                 kicker="FILTERING")
    notes(s, "The intermediate step is the part worth seeing. df[\"strength\"] > 40 gives you a column of True "
             "and False the same length as the data, and wrapping it as df[that] is what selects the rows. "
             "Print the condition on its own once and the two steps will stay separate in your head "
             "afterwards.\n\nOnce you see it as two steps, combining conditions makes sense: & for and, | for "
             "or, with brackets round each condition, because & binds more tightly than > does.\n\nTO TEACH: "
             "print the mask on its own before using it. Students who have seen the True/False column never get "
             "confused by compound conditions.")

    s = s_figure(prs, "Grouping: split, apply, combine", F("split_apply_combine.png"),
                 "Split the table into groups by a category column, apply a summary to each group, and combine "
                 "the answers into a smaller table. One line of pandas does all three.",
                 kicker="GROUPING")
    notes(s, "This is the operation that answers most comparison questions: does this differ between groups? "
             "df.groupby(\"" + w["group"] + "\")[\"target\"].mean() gives you " + w["agg"] +
             " for each group.\n\nThe result is a smaller table. Your original is unchanged. pandas almost never "
             "changes your data in place, which is deliberate — it means you cannot accidentally destroy the "
             "thing you loaded.\n\nTO TEACH: the three-stage figure is worth walking slowly. Beginners "
             "otherwise treat groupby as an incantation.")

    s = s_define(prs, "Series, mask, and groupby",
                 "A SERIES is one column. A MASK is a column of True and False produced by a condition. "
                 "GROUPBY splits the table by a category, applies a summary to each part, and combines the "
                 "results.",
                 'df["' + w["col"] + '"] is a Series. df["' + w["col"] + '"] > ' + w["thr"] + ' is a mask. '
                 'df.groupby("' + w["gcol"] + '")["' + w["col"] + '"].mean() is '
                 'split-apply-combine.',
                 "A filtered DataFrame. The mask is the True/False column; the filtered DataFrame is what you "
                 "get after applying it.")
    notes(s, "These three words cover most of what you will read in pandas documentation and in Kaggle "
             "notebooks. Having the vocabulary is what makes other people's work readable, which is the point "
             "of the second half of this session.")

    s = s_check(prs, [
        "df.shape gives (" + w["nrows"] + ", " + w["ncols"] + "). How many " + w["rec"] + " and how "
        "many columns, and which number is which?",
        "You write df['" + w["col"] + "'] > " + w["thr"] + " and print it. Describe what you see, "
        "rather than what you wanted.",
        "You want the mean of " + w["col"] + " for each " + w["gname"] + ". Write the line."],
        title="Two minutes: check you can drive it",
        foot="Answers next slide.")
    notes(s, "Three questions to confirm you can drive the tool. Question B catches the commonest confusion: a "
             "condition on a column is the question you are asking, and the filter is what you get after "
             "putting it inside df[...].\n\nTO TEACH: quick pulse check before the sourcing segment. Question B "
             "catches anyone still thinking a condition is a filter.")

    s = s_answers(prs, [
        ("(1030, 9)?",
         "1,030 rows and 9 columns — rows first, always. So 1,030 mixes, each described by 9 columns."),
        ("Printing the condition?",
         "A column of True and False, 1,030 entries long, with the same index as the data. It is not the rows "
         "you wanted — it is the question. Put it inside df[...] to get the rows."),
        ("Mean per age band?",
         'df.groupby("' + w["gcol"] + '")["' + w["col"] + '"].mean() — group by the category, '
         'pick the column, apply the '
         "summary. The result is one row per band.")])
    notes(s, "If question C gave you trouble, go back to the split-apply-combine figure before you go on. "
             "groupby appears in every week from here to the end of the year, and it answers most comparison "
             "questions you will be asked.")

    s = s_prose(prs, "Reading somebody else's notebook without being misled", [
        "**Kaggle notebooks are the best free resource you have**",
        "Thousands of people have analysed these exact datasets and published their working. Reading them is "
        "how you learn what is possible.",
        "**And they are not peer reviewed**",
        "Many are wrong, and the popular ones are not the correct ones — they are the well-presented ones. "
        "Treat them as a colleague's rough working.",
        "**Three things to check before you copy an idea**",
        "Did they look at the data before modelling it, or dive straight in? Did they hold anything back to "
        "test on? Do the numbers in the conclusion actually follow from the output shown?",
        "**The specific thing to watch for**",
        "A notebook reporting near-perfect accuracy has almost always leaked information it should not have "
        "had. You will learn to spot exactly how in Week 10 — for now, treat a suspiciously good result as a "
        "reason for suspicion.",
        "**How to use them honestly in this course**",
        "Read them, learn from them, then write your own and say in your README what you learned from where. "
        "Citing a notebook you learned from is good practice. Copying one and presenting it as yours is "
        "plagiarism, and the Week 15 viva will find it."],
        kicker="USING PUBLIC WORK")
    notes(s, "Kaggle notebooks are the best free resource available on these datasets, and they carry no "
             "quality guarantee whatsoever, so read them the way you would read a colleague's rough working. "
             "The popularity of a notebook tracks how well it is presented. The leakage warning is the part to "
             "hold onto: a notebook reporting near-perfect accuracy has almost always been given information it "
             "should not have had, and Week 10 shows you exactly how that happens. Until then, treat a "
             "suspiciously good result as a reason for suspicion.\n\nTO TEACH: open one real Kaggle notebook on "
             "the anchor dataset and walk the three checks live. Five minutes, and it makes the whole segment "
             "concrete.")

    s = s_segment(prs, 7, N, "Where data comes from, and whether to trust it", 20,
                  "Finding a dataset is easy. Judging whether it can answer your question is the skill.")
    notes(s, "Twenty minutes on judging a dataset before you commit to it. Finding data is easy; deciding "
             "whether it can answer your question is the part that saves you a fortnight, and it is the gate "
             "the Week 9 projects have to pass.\n\nTO TEACH: this segment is often cut for time and should not "
             "be. It is what stops the Week 9 projects being built on unusable data.")

    s = s_prose(prs, "Six questions to ask before you use anyone's data", [
        "**1 · Who measured it, and how?**",
        "An instrument reading, a laboratory analysis and somebody's estimate are not the same kind of "
        "number, "
        "and the dataset card should say which you have.",
        "**2 · Over what period, and is that period still relevant?**",
        "Process data from before a plant upgrade may describe a plant that no longer exists.",
        "**3 · What is the licence?**",
        "You must be allowed to use it, and you must attribute it. CC BY 4.0 means use it and cite it. No "
        "stated licence means assume you may not.",
        "**4 · What is missing, and is it missing at random?**",
        "A column that is blank for the first two years because the sensor was installed later is not missing "
        "at random, and averaging it will mislead you.",
        "**5 · Can it actually answer my question?**",
        "The question nobody asks. If you want to predict failures and the file contains no failures, no "
        "amount of technique will help.",
        "**6 · What would I need that is not here?**",
        "Saying this clearly is a real result. 'This data cannot answer the question, and here is what would' "
        "is a legitimate and often valuable conclusion."],
        kicker="JUDGING A DATASET")
    notes(s, "Question 5 is the one that wastes fortnights. Ask it while walking away is still cheap, before "
             "you download anything and long before you start cleaning.\n\nQuestion 6 takes some getting used "
             "to if you were trained to treat a negative result as a failure. 'This data cannot answer the "
             "question, and here is what would' is often the most useful thing an analyst produces, and it is "
             "an acceptable conclusion for the Data Analysis Project.\n\nTO TEACH: walk them through the actual "
             "dataset card for " + w["anchor"] +
             " on screen, answering all six questions from it. Ten minutes, and it makes the abstract "
             "concrete.")

    s = s_split(prs, "Practical: the Twelve Questions", "Work through these on " + w["anchor"],
                "\n".join(f"{i+1}. {q}" for i, q in enumerate(w["qs"][:6])),
                "Continued",
                [f"{i+7}. {q}" for i, q in enumerate(w["qs"][6:])],
                kicker="PRACTICAL — 30 MINUTES")
    notes(s, "Answer every question in physical units. A printed Series is not an answer. '38.4 MPa' is an answer; a "
             "Series printed to the screen is not.\n\nThe dataset: " + w["shape"] + ". Source: " + w["source"] +
             ". Columns: " + w["cols"] + ".\n\nCORE: answer all twelve. STRETCH: add two questions of your own "
             "and answer them.\n\nTO TEACH: circulate and ask 'what does that number mean?' rather than "
             "checking syntax. Have the marked-up solution to hand with the expected units.")

    s = s_challenge(prs, "Ten Questions, No Help",
                    "A different dataset you have not seen, and ten questions about it.\n"
                    "Twenty-five minutes. No help from me, and no searching for the answers.\n"
                    "This is deliberately the same format as Practical Test 1 in two weeks — treat it as a "
                    "calibration.",
                    ["What is the shape, and what are the types?",
                     "What does describe() tell you that head() does not?",
                     "Which column is the one you would predict?",
                     "Is anything obviously wrong with this data?",
                     "What does that number mean in engineering terms?",
                     "What would you need that is not in this file?"])
    notes(s, "This challenge uses the same format as Practical Test 1 in two weeks, so treat it as a "
             "calibration. Part of what you are finding out is whether you can work at this pace on a dataset "
             "you have never seen. Answer in physical units, and say plainly what you could not determine from "
             "the file.\n\nTO TEACH: this is the Week 7 rehearsal and you should say so. Students who take it "
             "seriously arrive at the test knowing the format and the pace, which removes most of the anxiety. "
             "Time it strictly — part of what is being calibrated is whether they can work at this pace.")

    s = s_split(prs, "Before Week 6", "The Data Analysis Project — set today, due Week 8",
                "In your team: choose a dataset from the approved list, or propose one for approval.\n\n"
                "Register the engineering question you will answer with it.\n\n"
                "Deliverable in Week 8: a cleaned dataset, a question-driven analysis notebook, four or more "
                "charts each answering a stated question, and one page of findings.\n\n"
                "Worth 10 per cent. An individual contribution log is required.",
                "Assignment A5 — due Week 6",
                ["Your Twelve Questions notebook,",
                 "with every answer stated in",
                 "physical units.",
                 "",
                 "Plus a README section giving",
                 "the dataset's source and licence.",
                 "",
                 "Restart and Run All before",
                 "you submit.",
                 "",
                 "Next week: why real data is",
                 "broken, and how to see it."],
                kicker="PROJECT AND ASSIGNMENT")
    notes(s, "The six judging questions from earlier in the session are the gate for a proposed dataset. If "
             "your team wants to bring its own, answer all six before you register your question, because a "
             "dataset that cannot answer it will cost you the whole of Weeks 6 to 8.\n\nTO TEACH: hand out the "
             "approved dataset list with licences stated. A team that proposes its own dataset must answer the "
             "six judging questions before approval — that requirement is what prevents a Week 9 disaster.")

    s = s_summary(prs, [
        "A DataFrame is a table: rows with an index, columns with names, and a type per column.",
        "Four commands on every new dataset, in this order: shape, head, info, describe. They tell you how "
        "big, what it looks like, what types, and what ranges.",
        "A column that should be numeric but shows dtype 'object' contains text somewhere. That is a defect, "
        "and Week 6 is about finding it.",
        "A condition on a column gives a mask of True and False. The mask inside square brackets is the filter.",
        "groupby splits by a category, applies a summary, and combines the results into a smaller table.",
        "Vectorisation means writing the operation once for the whole column. It is not just faster — it has "
        "far less room for the accumulator bug.",
        "Before using anyone's data, ask six questions. The one people skip is whether it can answer the "
        "question at all."])
    notes(s, "Seven statements covering the session. The second one — shape, head, info, describe, in that "
             "order — is the habit to build first, because it is the fastest way to find out whether a dataset "
             "is usable at all.\n\nTO TEACH: return to objectives.")

    s = s_check(prs, [
        "df.info() shows a column called " + w["col"] + " with dtype 'object'. What does that mean "
        "and what caused it?",
        "df.describe() shows a minimum of -999 in a column that cannot be negative. What is going on?",
        "What is the difference between df[\"x\"] > 40 and df[df[\"x\"] > 40]?",
        "You want the mean target for each category. Which operation, and what shape is the result?",
        "You find a dataset that perfectly matches your question but has no stated licence. What do you do?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question B is the sentinel-value trap and it is the most destructive defect in Week 6.")

    s = s_answers(prs, [
        ("dtype 'object' on a numeric column?",
         "At least one value in it is text. Usually a stray unit ('32.5 MPa'), a comma as a decimal separator, "
         "or a note typed into a data cell. Until it is fixed, no arithmetic on that column will work."),
        ("A minimum of -999?",
         "It is a sentinel value standing in for 'missing' — someone chose an impossible number instead of "
         "leaving the cell blank. It looks like data to pandas, so it will be included in every mean and will "
         "drag them all down. Find it with describe(), then convert it to a proper missing value."),
        ("The mask versus the filtered frame?",
         'df["x"] > 40 is a column of True and False, the same length as the data. df[df["x"] > 40] is the '
         "rows where that was True. The first is the question, the second is the answer."),
        ("Mean target per category?",
         'df.groupby("category")["target"].mean(). The result is a smaller table — one row per category — not '
         "a modified version of the original."),
        ("No stated licence?",
         "Assume you may not use it. Look for the same data from a source that does state a licence, or contact "
         "the publisher. For assessed work in this course, an unlicensed dataset is not acceptable — and being "
         "able to say why is part of the mark.")])
    notes(s, "Answer B describes the defect most likely to turn up in your own Data Analysis Project. A "
             "sentinel value such as -999 looks like a measurement to pandas, so it is included in every mean "
             "you compute and drags all of them down. describe() exposes it in one second.")

    s = s_glossary(prs, [
        ("pandas", "The library for working with tables of data. Imported as pd by convention."),
        ("NumPy", "The library underneath pandas, providing arrays and fast elementwise arithmetic."),
        ("DataFrame", "A table: indexed rows, named columns, one type per column."),
        ("Series", "One column of a DataFrame."),
        ("Index", "The row labels down the side of a DataFrame."),
        ("dtype", "The type of a column. 'object' on a numeric column means text has got in."),
        ("shape", "(rows, columns). An attribute, so no brackets."),
        ("head() / tail()", "The first or last few rows."),
        ("info()", "Column names, types and non-null counts. Run it on everything."),
        ("describe()", "Count, mean, standard deviation, min, quartiles and max per numeric column."),
        ("Vectorisation", "Applying an operation to a whole column at once instead of looping."),
        ("Mask", "A column of True and False produced by a condition."),
        ("Filtering", "Selecting rows using a mask: df[mask]."),
        ("groupby", "Split by a category, apply a summary, combine the results."),
        ("Derived column", "A new column computed from existing ones — where your engineering knowledge enters."),
        ("Sentinel value", "An impossible number used to mean 'missing', such as -999. Destroys means silently."),
        ("Provenance", "Who measured the data, how, and when."),
        ("Licence", "What you are permitted to do with someone else's data. No licence means assume not."),
    ], page="1 of 1")
    notes(s, "Eighteen terms, and every one of them appears in a weekly quiz or in Practical Test 1.")

    s = s_prose(prs, "One-page reference — the pandas you need this semester", [
        "**Open and describe**",
        "pd.read_csv(path) · df.shape · df.head() · df.info() · df.describe()",
        "**One column, and a new column**",
        'df["name"] · df["new"] = df["a"] / df["b"]',
        "**Filter**",
        'df[df["' + w["col"] + '"] > ' + w["thr"] + ']  ·  combine with & and | and brackets '
        'round each condition',
        "**Summarise**",
        'df["x"].mean() · .min() · .max() · .std() · .count() · df["cat"].value_counts()',
        "**Group**",
        'df.groupby("cat")["x"].mean()',
        "**Sort and save**",
        'df.sort_values("x", ascending=False) · df.to_csv("out.csv", index=False)',
        "**Before you trust anything**",
        "Look at info() for dtypes and describe() for impossible minimums and maximums. Both take one second "
        "and both catch defects that would otherwise survive into your conclusions.",
        "**Answer in units**",
        "Never hand in a printed Series. State the number, its unit, and what it means."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "These commands cover the great majority of what Weeks 6 to 15 require, which is why the list is "
             "deliberately short. Keep it to hand during the Data Analysis Project.")

    s = s_quiz(prs, 5,
               "A mask confused with a filtered frame, a groupby result misread, and a numeric column with dtype "
                        "'object'.", qr_path=qrp(code, 5))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "Three lines, and you know\nwhat all three of them do.",
                  "Last week you wrote sixty lines to answer one question. The reason this week feels easy is "
                  "that you did it the hard way first — and when pandas gets something wrong, which it will, "
                  "you will be able to tell.",
                  "Next week: why real data is broken, and how to see it before it misleads you.")
    notes(s, "The order of the last two weeks was deliberate. Sixty lines of loop first and three lines of "
             "pandas second means you can tell when pandas gets something wrong, and it will — usually on a "
             "column where one row has a stray unit in it.\n\nTO TEACH: the closing point matters. Students who "
             "start with pandas cannot diagnose it. Students who started with loops can.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week05_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week6(code):
    c, w = CO[code], W6[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 6")
    N = 9

    s = s_title(prs, code, "Dirty data,\nand seeing it",
                "Data quality through visualisation", "WEEK 6  ·  " + DATE[6][code],
                SLOTS[code] + "  ·  " + FOOT)
    notes(s, "Today pairs cleaning with charts, and the pairing is deliberate: a chart is how you FIND a "
             "defect, in time to stop it reaching your conclusion. Practical Test 1 is next week, and its "
             "format and rubric are published today so that you can prepare against them.\n\n"
             + ("TO TEACH — THIS COHORT: open with the 30-minute Week 5 consolidation, because this cohort "
                "lost Week 5 to Independence Day. Budget it in and cut the chart demonstration "
                "accordingly. Check who actually worked through the asynchronous package before you go on. "
                "Publish the Test 1 format and rubric today."
                if code in FRIDAY else
                "TO TEACH — THIS COHORT: no consolidation needed for this cohort — you taught Week 5 normally. "
                "Publish the Test 1 format and rubric today."))

    s = s_objectives(prs, [
        "Profile a dataset for missing values, duplicates, impossible values, wrong types and outliers.",
        "Recognise a sentinel value standing in for missing data, and say why it is worse than a blank.",
        "Choose a handling strategy for each defect and justify it in one sentence.",
        "Say whether data is missing at random, and what difference that makes.",
        "Produce histograms, box plots, scatter plots, line charts and a correlation heatmap, correctly "
        "labelled with units.",
        "Use a chart to find a defect rather than to present a result.",
        "Argue whether an extreme value is a measurement error or real behaviour — and commit to a position."],
        6, "Data quality through visualisation")
    notes(s, "Objective 7 has no lookup answer, and that is the point. Two of the five cases in today's "
             "challenge are genuinely arguable.\n\nTO TEACH: read them out, return at the end.")

    s = s_segment(prs, 1, N, "Where we got to", 15,
                  "You can load a table and interrogate it. Today: what to do when the table is wrong.")
    notes(s, "Fifteen minutes of recall. You can load a table and interrogate it; today is about what to do "
             "when the table itself is wrong.\n\nTO TEACH: for the Friday cohorts this segment is the Week 5 "
             "consolidation and needs the full fifteen minutes. Run the four commands — shape, head, info, "
             "describe — live on the anchor dataset and take questions.")

    s = s_segment(prs, 2, N, "Real data is broken, and the break is informative", 15,
                  "Not a warning — a description. Every dataset you will ever be handed has defects in it.")
    notes(s, "Fifteen minutes. Every dataset you will ever be handed has defects in it, and each defect has a "
             "physical cause: a sensor fitted late, an export run twice, a note typed into a numeric cell. The "
             "cause is what tells you how to handle it.\n\nTO TEACH: lead with the physical story behind each "
             "defect rather than the taxonomy. Defects have causes, and the cause tells you how to handle them.")

    s = s_question(prs, "TODAY'S QUESTION",
                   '"' + w["qkey"] + '"',
                   "You could answer that in one line of pandas today. The problem is that the answer would "
                   "be wrong, and nothing on your screen would tell you so.")
    notes(s, "You could answer today's question in one line of pandas, and the answer would be wrong with "
             "nothing on the screen to say so. That is why this session exists. By the end you will answer the "
             "same question again on cleaned data and see how far it moved.\n\nTO TEACH: run the one-liner live "
             "on the damaged dataset and get a confident, wrong answer. Then spend the session finding out why. "
             "This framing is far more effective than starting with a list of defect types.")

    s = s_segment(prs, 3, N, "Six ways data goes wrong", 25,
                  "Each with a physical cause, because the cause determines the fix.")
    notes(s, "Twenty-five minutes on six defect classes, each with the physical cause that produced it. The "
             "cause determines the fix, which is why a taxonomy on its own is not much use to you.\n\nTO TEACH: "
             "twenty-five minutes. Use the figure, then the cohort-specific list.")

    s = s_figure(prs, "Six defects in one small table", F("defect_types.png"),
                 "A missing value, a zero-coded missing value, a duplicated row, an impossible value, a number "
                 "stored as text, and an outlier. All six are in this table, and all six are in the file you "
                 "are about to be given.",
                 kicker="THE SIX DEFECTS")
    notes(s, "The zero-coded missing value is the dangerous one. A blank is visibly absent and pandas will "
             "exclude it from a mean. A zero, or a -999, looks like data and will be included — so it silently "
             "moves every number you compute.\n\nA number stored as text is what makes a column show dtype "
             "'object' in info(), which you met last week.\n\nTO TEACH: point at each one and ask the room what "
             "could have caused it physically. Their answers are usually better than a prepared list, because "
             "they have seen site records.")

    s = s_prose(prs, "The same six, in your own data", [
        "**What is in the file you are about to clean**"] +
        [f"{i+1} · {x}" for i, x in enumerate(w["defects"])] +
        ["**And one thing that is not a defect**",
         "An extreme value is not automatically an error. Some of them are the most important rows in the "
         "file. Telling the difference is the last segment of today, and it is a judgement call."],
        kicker="MADE CONCRETE")
    notes(s, "Every one of these is drawn from something that genuinely happens in this industry. The unit "
             "inconsistency is the one that most often survives into a published result.\n\nTO TEACH: read them "
             "out and ask which they have personally seen on placement or in a laboratory. Several will have.")

    s = s_define(prs, "Missing, and missing at random",
                 "A value is MISSING when it was never recorded. It is MISSING AT RANDOM when whether it is "
                 "absent has nothing to do with what its value would have been — and NOT at random when it does.",
                 "A sensor added two years into a five-year record leaves the first two years blank. That is "
                 "not random: the blanks correspond exactly to a period with different instrumentation.",
                 "Zero. A blank means we do not know; a zero means we measured nothing. Treating one as the "
                 "other is the most common way to corrupt an analysis.")
    notes(s, "This distinction decides what you are allowed to do. If values are missing at random you can "
             "often drop or impute them without much harm. If they are not, dropping them removes a specific "
             "part of your data and biases everything that follows.\n\nThe honest position is frequently 'I "
             "cannot tell from the data alone, and here is what I would need to know'. That is a real answer "
             "and it earns marks in this course.\n\nTO TEACH: the missingness map in the next segment makes "
             "this visible rather than theoretical.")

    s = s_worked(prs, "Profiling a dataset in four commands",
                 "The routine to run on every dataset you are ever handed, before you answer a single "
                 "question about it. It takes about a minute.",
                 ["df.shape — how much data is there? A file with 40 rows and a file with 40,000 support very "
                  "different claims.",
                  "df.info() — what type is every column, and how many non-null values does each have? A "
                  "numeric column showing dtype 'object' has text in it. A column with far fewer non-nulls "
                  "than the others has a missingness problem.",
                  "df.describe() — look ONLY at the minimum and maximum rows first. This is where impossible "
                  "values and sentinels announce themselves: a negative width, a pH of 14, a -999.",
                  "df.duplicated().sum() — how many rows are exact copies of another row? Anything above zero "
                  "needs explaining before you go on."],
                 "Four commands, about a minute, and they catch four of the six defect classes. Skipping this "
                 "is how a confident wrong answer gets into a report.")
    notes(s, "The order matters. shape tells you whether the dataset is worth the effort. info() tells you "
             "whether the columns are even usable. describe() is where defects surface. duplicated() catches "
             "the export-run-twice problem that nothing else will show you.\n\nOn describe(): read the min and "
             "max rows before the mean. A mean tells you nothing if the column contains a sentinel; the "
             "minimum tells you immediately that it does.\n\nTO TEACH: run all four live on the damaged "
             "dataset and let the room spot the defects from the output. They will find most of them "
             "unprompted, which is far better than being told.")

    s = s_define(prs, "Duplicate, and impossible value",
                 "A DUPLICATE is a row that is an exact copy of another — almost always an export run twice, "
                 "or two people entering the same record. An IMPOSSIBLE VALUE is one that physics or the "
                 "instrument does not allow.",
                 "Forty-one identical rows in a 1,000-row file means your means are weighted towards whatever "
                 "those rows say. A negative crack width or an efficiency above 100 per cent cannot be a real "
                 "measurement.",
                 "An outlier. An outlier is extreme but possible, and may be the most valuable row in the "
                 "file. An impossible value is definitely wrong, and it is the only defect class you can be "
                 "certain about without domain knowledge.")
    notes(s, "The distinction matters because the actions differ. An impossible value gets removed or "
             "corrected without much debate. An outlier gets investigated, and often kept.\n\nDuplicates are "
             "easy to miss because nothing about a single row looks wrong — you only see it by comparing rows, "
             "which is what duplicated() does.\n\nOne caution: two rows can legitimately be identical if the "
             "data has no unique identifier and two genuinely separate events happened to produce the same "
             "readings. Check before you delete.\n\nTO TEACH: the last caution is worth saying. Blindly "
             "dropping duplicates is itself a defect.")

    s = s_segment(prs, 4, N, "Charts that find problems", 25,
                  "Every chart today answers a question about whether the data can be trusted.")
    notes(s, "Twenty-five minutes of charts, and every one of them answers a question about whether the data "
             "can be trusted. The standing rule from here on: a chart exists to answer a stated question. It "
             "becomes a marking criterion in the Data Analysis Project and in both practical tests.\n\nTO "
             "TEACH: state the rule and then enforce it all semester.")

    s = s_figure(prs, "Seeing what is missing", F("missingness_map.png"),
                 "Rows down, fields across, blanks where data is absent. The pattern is the finding: this is "
                 "not scattered randomly, it is structured — which tells you something happened to the "
                 "instrumentation partway through.",
                 kicker="FINDING DEFECTS")
    notes(s, "A missingness map takes one line and answers the question that describe() cannot: is the "
             "missingness structured? Scattered blanks are usually harmless. A block of blanks is a story.\n\n"
             "This is exactly the 'missing at random' distinction from the previous slide, made visible.\n\n"
             "TO TEACH: run it on the damaged dataset live. The pattern will be obvious and the room will see "
             "it before you explain it, which is the ideal.")

    s = s_figure(prs, "What a box plot shows, and what it hides", F("boxplot_annotated.png"),
                 "The box is the middle half of the data, the line inside it is the median, and the whiskers "
                 "reach the last real point within 1.5 times the interquartile range — not to 1.5 IQR itself. "
                 "Points beyond that are flagged. But the box cannot show shape, which is why the histogram "
                 "beside it matters.",
                 kicker="TWO VIEWS OF THE SAME DATA")
    notes(s, "Precision matters here, because the sloppy version of this sticks. The fence sits at Q1 minus 1.5 "
             "times the IQR and at Q3 plus 1.5 times the IQR. The whisker reaches the last actual data point "
             "inside that fence, so where it ends depends on your data rather than on the quartiles alone. "
             "Points beyond the fence are flagged for inspection, and flagged means worth a look.\n\nThe "
             "pairing of the two charts is the lesson. A box plot tells you where the data sits and marks the "
             "extremes; a histogram tells you what shape it has. A distribution with two peaks looks perfectly "
             "ordinary in a box plot, and two peaks in an engineering dataset usually means two populations "
             "have been mixed together — two materials, two machines, two shifts.\n\nTO TEACH: this figure's "
             "caption names the planted data-entry errors. Point that out — it is the same honesty you expect "
             "from them.")

    s = s_figure(prs, "Which chart answers which question", F("chart_chooser.png"),
                 "Five questions, five charts. Choose the chart from the question you are asking, never from "
                 "what looks impressive.",
                 kicker="CHART GRAMMAR")
    notes(s, "The standing rule for the rest of the course: every chart must answer a stated question, and the "
             "caption should say what the answer was rather than describing the axes.\n\n'Figure 3: strength "
             "against cement content' is a description. 'Figure 3: strength rises with cement content but the "
             "relationship weakens above 400 kg/m3' is a finding. The second earns marks; the first does "
             "not.\n\nTO TEACH: show one good and one bad caption for the same chart. Thirty seconds, and it "
             "visibly changes what gets submitted.")

    s = s_check(prs, [
        "A pressure column has dtype 'object'. Can you compute its mean, and what must you do first?",
        "describe() shows a maximum of 9999 in a temperature column. Data or defect, and how would you decide?",
        "Two rows are identical in every column. Is that definitely a duplicate to delete?"],
        title="Two minutes: check the profiling",
        foot="Answers next slide.")
    notes(s, "Three questions on profiling before the Data Clinic. Question C is the one that catches "
             "over-confident cleaning: identical rows are not automatically duplicates to delete.\n\nTO TEACH: "
             "pulse check before the Data Clinic. Question C is the one that catches over-confident cleaning.")

    s = s_answers(prs, [
        ("dtype 'object' on pressures?",
         "No — pandas will refuse, or worse, concatenate the values as text. Find the offending rows, see what "
         "is in them (usually a stray unit or a comma), fix or remove those, then convert the column with "
         "pd.to_numeric before computing anything."),
        ("A maximum of 9999?",
         "Almost certainly a sentinel meaning missing, because 9999 is a suspiciously round impossible number. "
         "Decide by asking what the instrument's range actually is, and by counting how many 9999s there are — "
         "a sentinel usually appears many times, a real extreme usually once."),
        ("Two identical rows?",
         "Not necessarily. If the table has no unique identifier, two genuinely separate events can produce "
         "identical readings — two periods with the same conditions, two samples with the same measured "
         "value. Check "
         "whether a timestamp or an ID distinguishes them before deleting. Blindly dropping duplicates is "
         "itself a defect.")])
    notes(s, "Answer C is where cleaning stops being a checklist and becomes judgement. Two identical rows can "
             "record two genuinely separate events when the table has no unique identifier, so look for a "
             "timestamp or an ID that distinguishes them before deleting anything.")

    s = s_prose(prs, "The defect register — what you hand in", [
        "**One row per defect, and five columns**",
        "What you found · where (which column, how many rows) · what you think caused it · what you did · why.",
        "**Why it is a table and not prose**",
        "Because a reader needs to check your decisions one at a time, and because you will find eight to "
        "twelve defects and prose about twelve things is unreadable.",
        "**The 'why' column is the marked one**",
        "'Dropped 41 duplicate rows because they were an exact re-export and keeping them would weight the "
        "mean towards one day's readings' earns full marks. 'Dropped duplicates' earns about half.",
        "**Then a five-line data quality statement**",
        "How much data you started with, how much you used, what you removed and why, and one sentence on how "
        "much confidence the conclusion deserves as a result.",
        "**Why this matters beyond the marks**",
        "If a result of yours is ever questioned — in a viva, in a review, in practice — the defect register is "
        "the document that defends it. Without one you are relying on memory, and memory is not evidence."],
        kicker="THE DELIVERABLE")
    notes(s, "The defect register is the same artefact professional analysts produce, usually called a data "
             "preparation log. The contrast in the third point is the one to study: 'Dropped 41 duplicate rows "
             "because they were an exact re-export and keeping them would weight the mean towards one day's "
             "readings' earns full marks, and 'Dropped duplicates' earns about half. The difference is one "
             "clause of causal reasoning.\n\nTO TEACH: put a blank register template on the board or hand it "
             "out. Students fill in a structure far more readily than they invent one.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. The Data Clinic after the break is the long practical, at 35 minutes.\n\nTO TEACH: "
             "take it. The Data Clinic is the long practical.")

    s = s_split(prs, "Practical: the Data Clinic", "What to do",
                "You are given a damaged version of a dataset you already know.\n\n"
                "Find every defect. Decide how to handle each one. Write ONE sentence justifying each decision.\n\n"
                "Then answer the question from the start of the session — properly this time — and say how much "
                "your answer moved.\n\n"
                "CORE: find and handle the six planted defects, with justifications.\n"
                "STRETCH: quantify how much the headline answer changes under two different cleaning "
                "strategies.",
                "What is marked",
                ["The justification carries the marks.",
                 "",
                 "An unjustified correct fix scores",
                 "about half. A justified decision",
                 "you can defend scores full marks",
                 "even where another engineer would",
                 "have chosen differently.",
                 "",
                 "Deliverables:",
                 "  a cleaning notebook",
                 "  a defect register table",
                 "  a five-line data quality",
                 "  statement"],
                kicker="PRACTICAL — 35 MINUTES")
    notes(s, "The marking emphasis here is deliberate. There is often no single right way to handle a defect, "
             "so a decision you can defend earns full marks even where another engineer would have chosen "
             "differently, and a correct fix with no justification earns about half. The stretch tier is the "
             "most valuable part if you get that far: showing that the conclusion depends on which cleaning "
             "strategy you chose is a genuinely mature result.\n\nTO TEACH: state the marking emphasis out "
             "loud. Circulate and ask 'why did you choose that?' and nothing else.")

    s = s_segment(prs, 7, N, "Error, or reality?", 15,
                  "The judgement that cannot be automated, and the reason a trained engineer is still needed.")
    notes(s, "Fifteen minutes of framing before the challenge. This judgement cannot be automated, and it is "
             "the reason a trained engineer is still needed once the profiling code has run.\n\nTO TEACH: "
             "fifteen minutes of framing before the challenge. Do not give them the answers to the five cases "
             "here.")

    s = s_prose(prs, "How to decide whether an extreme value is real", [
        "**Is it physically possible?**",
        "A negative width, a pH of 14 in a plant, an efficiency above 100 per cent. Impossible means error, "
        "and this is the only test that gives a definite answer.",
        "**Is it possible but implausible for THIS system?**",
        "Achievable in principle, wrong for this plant, this material or this machine. Now you need domain "
        "knowledge, and this is where you are more use than any algorithm.",
        "**Is there a mechanism that would produce it?**",
        "A start-up transient, a high-grade intersection, a shutdown, a calibration run. If you can name the "
        "mechanism, it is probably real and probably important.",
        "**Does it come with company?**",
        "One isolated extreme is more likely to be an error. A cluster of them at a particular time or on a "
        "particular unit is a signal.",
        "**What does keeping or dropping it do to your answer?**",
        "If the conclusion changes, the decision matters and must be reported. If it does not, say so and move "
        "on.",
        "**And the answer that is always available**",
        "'I cannot tell from the data alone. I would need the shift log, the calibration record, or the "
        "instrument specification.' That is a correct answer."],
        kicker="OUTLIER JUDGEMENT")
    notes(s, "The last point on the slide is the one that takes longest to accept. Saying precisely what you "
             "would need in order to know — the shift log, the calibration record, the instrument specification "
             "— is one of the most valuable things a data analyst produces, and it earns marks in this "
             "course.\n\nTO TEACH: this framework is what the challenge is assessed against. Hand it out or "
             "leave it on screen during the challenge.")

    s = s_challenge(prs, "The Outlier Argument",
                    "Five flagged extreme values from your own discipline's data.\n"
                    "For each one your team must COMMIT to a position — measurement error to be removed, or "
                    "real behaviour to be kept — and defend it.\n"
                    "Twenty minutes. Two of the five have no single right answer, and finding out which two is "
                    "part of the exercise.",
                    ["Is it physically possible at all?",
                     "Is it plausible for THIS system?",
                     "Can you name a mechanism that produces it?",
                     "Is it alone, or are there others like it?",
                     "Does your conclusion change either way?",
                     "What would you need in order to be sure?"])
    notes(s, "Two of the five cases are genuinely arguable, and a team that identifies which two has done "
             "better than a team that answers confidently on all five. The reasoning carries the marks. Commit "
             "to a position before you hear anyone else's, and work the six questions in order — the third "
             "one, naming a mechanism that would produce the value, settles most of the cases on its own.\n\n"
             "TO TEACH: the five cases and the intended reading:\n\n" +
             "\n\n".join(f"• {case} — {verdict}" for case, verdict in w["outliers"]) +
             "\n\nMark the reasoning. Make each team commit publicly before you reveal anything.")

    s = s_points(prs, "Before you leave the room",
                 [("Practical Test 1 is next week — here is exactly what it is",
                   "Individual, offline, on a laboratory machine with no internet and no AI assistance. Two "
                   "hours of practical plus twenty-five minutes of written reasoning. You get a dataset you "
                   "have never seen from your own discipline. You profile it, find and handle its defects with "
                   "a written justification for each, answer three stated questions with evidence, produce "
                   "three charts each captioned with the question it answers, list five findings and make one "
                   "recommendation. Worth 15 per cent. The rubric is published today."),
                  ("This week's quiz — five minutes, and it counts",
                   "Five questions on this session: a zero-coded missing value, a chart that does not answer "
                   "its question, and an extreme value to judge. Worth one per cent, best ten of twelve "
                   "count.")],
                 kicker="TEST 1 AND THIS WEEK'S QUIZ", numbered=False)
    notes(s, "The Test 1 rubric is published today, so you will not meet the marking scheme for the first time "
             "in the assessment. The weighting is the part to note: the written justification for each cleaning "
             "decision carries more marks than the fix itself. There is nothing to memorise, and the way to "
             "prepare is to redo the Data Clinic on a different dataset.\n\nTO TEACH: publish the Test 1 rubric "
             "TODAY. Confirm the room and machine allocation now — CML3112 is ~100 students and will very "
             "likely need two sittings, which must be settled this week, not next.")

    s = s_summary(prs, [
        "Every real dataset has defects. The defect usually has a physical cause, and the cause tells you how "
        "to handle it.",
        "A zero or a -999 standing in for missing data is worse than a blank, because pandas will include it "
        "in every calculation.",
        "Whether data is missing at random decides what you are allowed to do about it. A missingness map "
        "makes that visible in one line.",
        "A column that should be numeric but shows dtype 'object' has text in it somewhere.",
        "A box plot tells you where the data is and flags extremes. A histogram tells you what shape it has. "
        "You need both.",
        "Whiskers reach the last real data point inside 1.5 times the IQR. They do not sit at 1.5 IQR.",
        "An extreme value is not automatically an error. Physically impossible means error; implausible needs "
        "domain knowledge; and 'I cannot tell without the shift log' is a legitimate answer.",
        "Every chart answers a stated question, and the caption says what the answer was."])
    notes(s, "Eight statements covering the session, and the last summary before Practical Test 1. The sixth is "
             "the one most often got wrong, including in textbooks: whiskers reach the last real data point "
             "inside 1.5 times the IQR.\n\nTO TEACH: return to objectives. This is the last summary before "
             "Practical Test 1, so it is worth the full two minutes.")

    s = s_check(prs, [
        "A column of pressures has a mean of 340 kPa and a minimum of -999. What has happened, and what does "
        "it do to the mean?",
        "You drop every row with a missing value and your dataset shrinks by 30 per cent. What is the question "
        "you must ask before proceeding?",
        "Your box plot shows no outliers but your histogram has two clear peaks. What might that mean "
        "physically?",
        "Give one extreme value from your own discipline that is definitely an error, and one that is probably "
        "real. Say how you can tell.",
        "You clean a dataset two different defensible ways and get two different answers to your question. "
        "What do you report?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide. This is good Test 1 preparation.")
    notes(s, "Question E is the mature answer and it is what separates a merit from a pass in the Data Analysis "
             "Project.")

    s = s_answers(prs, [
        ("Mean 340, minimum -999?",
         "-999 is a sentinel value meaning 'missing'. pandas treats it as a real measurement, so it is dragging "
         "the mean down — and the more of them there are, the further wrong you are. Convert them to proper "
         "missing values, then recompute and compare."),
        ("Dropping 30 per cent of rows?",
         "Are they missing at random? If the blanks correspond to a period, a unit or a condition, you have "
         "just deleted a specific part of your data and everything downstream is biased. Check the missingness "
         "pattern before you drop anything."),
        ("No outliers but two peaks?",
         "Two populations have probably been mixed — two materials, two machines, two operating regimes, or "
         "two shifts. That is often the most interesting finding in the file, and a box plot would never have "
         "shown it."),
        ("One definite error, one probably real?",
         "Definite: anything physically impossible — a negative width, an efficiency above 100 per cent. "
         "Probably real: an extreme with a nameable mechanism, such as inrush current at start-up or a "
         "high-grade intersection. The test is whether you can name the mechanism."),
        ("Two defensible cleanings, two answers?",
         "Report both, and say which decision drove the difference. That is not indecision — it is the honest "
         "result, and it tells the reader how much confidence the conclusion deserves. Hiding it would be the "
         "error.")])
    notes(s, "Answer E is the mature position, and it is what separates a merit from a pass in the Data "
             "Analysis Project. Two defensible cleanings that produce two different answers is an honest "
             "result: report both, and say which decision drove the difference.")

    s = s_glossary(prs, [
        ("Data quality", "Whether a dataset is fit to answer the question you are asking of it."),
        ("Missing value (NaN)", "A value that was never recorded. pandas excludes NaN from most calculations."),
        ("Sentinel value", "An impossible number used to mean missing, such as -999 or 0. Included in "
                           "calculations, so silently corrupting."),
        ("Missing at random", "Whether a value is absent has nothing to do with what it would have been."),
        ("Missing not at random", "The absence is structured — a period, a unit, a condition. Dropping these "
                                  "rows biases everything."),
        ("Imputation", "Filling a missing value with an estimate — the mean, the median, the previous value. "
                       "Every method assumes something."),
        ("Duplicate", "The same record recorded twice, usually from an export run twice."),
        ("Impossible value", "A value outside what physics or the instrument allows. Always an error."),
        ("Outlier", "An extreme value. NOT automatically an error."),
        ("IQR", "Interquartile range: the spread of the middle half of the data, Q3 minus Q1."),
        ("Fence", "Q1 - 1.5 x IQR and Q3 + 1.5 x IQR. Points beyond are flagged for inspection."),
        ("Whisker", "Reaches the last real data point inside the fence — not to the fence itself."),
        ("Histogram", "Shows the shape of one variable's distribution."),
        ("Box plot", "Shows where the data is and flags extremes. Cannot show shape."),
        ("Scatter plot", "Shows whether two variables move together."),
        ("Correlation heatmap", "Shows which pairs of variables are associated. Association only."),
        ("Defect register", "A table of every defect found, what you did about it, and why."),
        ("Data quality statement", "A short honest note on what is wrong with the data and what that means for "
                                   "the conclusion."),
    ], page="1 of 1")
    notes(s, "Nineteen terms. The distinction between fence and whisker is the one most often got wrong, "
             "including in textbooks.")

    s = s_prose(prs, "One-page reference — profiling and cleaning", [
        "**Profile first, every time**",
        "df.info() for dtypes and non-null counts · df.describe() for impossible minimums and maximums · "
        "df.duplicated().sum() · df.isna().sum()",
        "**Find the sentinels**",
        "Look at the minimum and maximum of every column. -999, 0, 9999 in a column that cannot hold them are "
        "missing values in disguise.",
        "**See the missingness pattern**",
        "Plot it. Scattered is usually harmless; a block is a story.",
        "**Handle, then justify**",
        "One sentence per decision. What you did, and why. The justification is what is marked.",
        "**Charts that find problems**",
        "Histogram for shape · box plot for extremes · scatter for impossible pairs · heatmap for redundancy.",
        "**Caption with the finding**",
        "A caption that states the finding: '" + c["finding"] + "'.",
        "**Report what you dropped**",
        "How many rows, what proportion, and whether they were missing at random.",
        "**When you cannot tell**",
        "Say so, and say exactly what you would need in order to know. That is a result."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "This is the page to have open while you prepare for Practical Test 1. The profiling line at the "
             "top is the one-minute routine that catches four of the six defect classes.")

    s = s_quiz(prs, 6,
               "A zero-coded missing value, a chart that does not answer its question, and an extreme value to "
                        "judge.", qr_path=qrp(code, 6))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You answered the same question twice\nand got two different numbers.",
                  "You answered today's question twice — once on the broken data and once on the cleaned data "
                  "— and got two different numbers. Nothing on your screen told you the first one was wrong. "
                  "Only the profiling did.",
                  "Next week: Practical Test 1. An unfamiliar dataset, two hours, offline, and marks for your "
                  "reasoning rather than your result.")
    notes(s, "You answered the same question twice today and got two different numbers, and nothing on the "
             "screen distinguished them. Only the profiling did. Practical Test 1 next week works the same way: "
             "an unfamiliar dataset, two hours, offline, with the marks weighted towards your reasoning. "
             "Redoing the Data Clinic on a different dataset is better preparation than rereading notes.\n\nTO "
             "TEACH: end by restating the test format and the rubric weighting one final time.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week06_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for code in CO:
        print(f"  {code}  W4: {week4(code)}   W5: {week5(code)}   W6: {week6(code)}")

    import json
    from pptxkit import LECTURER
    path = _ROOT + "/data/lecturer_notes_" + __file__.split("/")[-1].replace(".py", ".json")
    json.dump(LECTURER, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  {len(LECTURER)} lecturer notes -> {path.split('/')[-1]}")
