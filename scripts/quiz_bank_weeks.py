# -*- coding: utf-8 -*-
"""Question banks for Weeks 2 to 13. Merged into QUIZ by quiz_banks.py.

Kept in its own module because the eleven banks together run to a few
thousand lines and quiz_banks.py stays readable as the schema, the Week 1
reference bank and the helpers.

EVERY NUMBER IN A CODE BLOCK HERE WAS EXECUTED BEFORE IT WAS WRITTEN DOWN.
A diagnosis question whose "silently wrong" output is not actually what the
code produces teaches the wrong lesson and cannot be defended in front of a
class. Re-run scripts/verify_quiz_arithmetic.py after editing any snippet.

MIX
  Week 2   1 traceback, 3 interpretation, 1 judgement — their first
           notebook, so no silent-wrong-answer question yet.
  Weeks 3+ 2 diagnosis of a silently wrong answer, 1 traceback,
           1 interpretation, 1 judgement.

PER-COHORT DATA
  CML3112  concrete, structures, site inspection
  CML3113  froth flotation, drilling, ore grade
  CML3111  motors, machine failure, power output
Where the concept is the same for everyone the stem and options are shared;
only the data changes. Where the domain changes the reasoning, the options
are branched too.
"""

BANKS = {}

# ==========================================================================
# QUIZ 2 — Week 2. Notebooks and version control. Their first notebook.
# Mix: 1 traceback, 3 interpretation, 1 judgement.
# ==========================================================================
BANKS[2] = [
    # ---- 1. out-of-order execution read off the cell numbering
    {
        "kind": "interpretation",
        "stem": ("The numbers in the square brackets are the order the cells "
                 "were actually run. The notebook now reads as shown. Why "
                 "does it print 10?"),
        "pre_by": {
            "CML3112":
                "In [1]:  readings = 40\n"
                "In [2]:  limit = 30\n"
                "In [5]:  readings = 55\n"
                "In [3]:  over = readings - limit\n"
                "In [4]:  print(over)\n"
                "         10",
            "CML3113":
                "In [1]:  holes_logged = 40\n"
                "In [2]:  target = 30\n"
                "In [5]:  holes_logged = 55\n"
                "In [3]:  ahead = holes_logged - target\n"
                "In [4]:  print(ahead)\n"
                "         10",
            "CML3111":
                "In [1]:  motors_tested = 40\n"
                "In [2]:  quota = 30\n"
                "In [5]:  motors_tested = 55\n"
                "In [3]:  spare = motors_tested - quota\n"
                "In [4]:  print(spare)\n"
                "         10",
        },
        "options": [
            ("The subtraction ran while the first value was still in memory, "
             "and the cell that replaced it ran afterwards", True,
             "Correct. Read the bracket numbers as a timeline: 1, 2, 3, 4, "
             "then 5. The subtraction happened at step 3 on the old value, "
             "and the replacement only happened at step 5. What you see on "
             "screen is the code; what produced the 10 is the order it ran."),
            ("The notebook cached the printed output and did not refresh it",
             False,
             "Notebooks do keep an old output on screen after you edit a "
             "cell, but the value here was genuinely computed from the "
             "earlier number. Nothing is stale about the 10 itself."),
            ("Python read the cells from the top of the page downwards",
             False,
             "That is the assumption this question exists to break. A "
             "notebook runs cells in whatever order you click them, and the "
             "bracket numbers are the record of that order."),
            ("The variable was never given the second value at all", False,
             "It was, at step 5. That is precisely why the code on screen "
             "and the number underneath it disagree."),
        ],
    },
    # ---- 2. what Restart and Run All actually proves
    {
        "kind": "interpretation",
        "stem": ("Read the two states below. What has Restart and Run All "
                 "established?"),
        "pre": "before:  In [7]  In [3]  In [12]  In [4]  In [9]\n"
               "         (outputs on screen, run in some past order)\n"
               "\n"
               "after:   In [1]  In [2]  In [3]   In [4]  In [5]\n"
               "         (no errors, and the same outputs as before)",
        "options": [
            ("That it produces those outputs from an empty memory, in page "
             "order", True,
             "Correct, and that is a narrow claim worth having. The counts "
             "now run 1 to 5 in page order, which rules out the "
             "out-of-order trap and any variable that only survived because "
             "of a cell you later deleted."),
            ("That the code is correct", False,
             "It establishes that the code runs and reproduces its own "
             "outputs. Code can run cleanly from top to bottom and still "
             "compute the wrong quantity, which is what the diagnosis "
             "questions from Week 3 onwards are about."),
            ("That the notebook will run on a classmate's machine", False,
             "That needs the same packages, the same Python version and the "
             "data file reachable at the same relative path. Week 13 is "
             "about exactly this gap."),
            ("That the results are statistically reliable", False,
             "Reproducing an output says nothing about whether the number "
             "was worth computing. A notebook can faithfully reproduce a "
             "meaningless average every time you run it."),
        ],
    },
    # ---- 3. traceback: NameError
    {
        "kind": "traceback",
        "stem": ("You have been working for an hour, the variable is plainly "
                 "assigned in a cell further up the page, and running the "
                 "cell at the bottom gives this. What is the most likely "
                 "cause?"),
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n"
                "    print(mean_width)\n"
                "NameError: name 'mean_width' is not defined",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n"
                "    print(mean_rop)\n"
                "NameError: name 'mean_rop' is not defined",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-2-a1b2c3>\", line 1, in <module>\n"
                "    print(mean_temp)\n"
                "NameError: name 'mean_temp' is not defined",
        },
        "options": [
            ("The cell that creates it has not actually been run in this "
             "session, whatever the page shows", True,
             "Correct. Being written on the page and having been executed "
             "are different things: the kernel only knows what it has run. "
             "Either that cell was never run, or the kernel was restarted "
             "since. Restart and Run All settles it in one step."),
            ("The variable holds nothing, so printing it fails", False,
             "A variable holding nothing still exists and prints happily as "
             "None. This error says the name itself is unknown to Python."),
            ("The name is a reserved word in Python", False,
             "It is an ordinary name. A reserved word would be reported as a "
             "SyntaxError while the cell was being read, before it ran."),
            ("The notebook needs a library imported before it can print",
             False,
             "print is built in and needs no import. A missing library "
             "reports itself as ModuleNotFoundError."),
        ],
    },
    # ---- 4. reading git status
    {
        "kind": "interpretation",
        "stem": "Read this output. Which statement is true?",
        "pre_by": {
            "CML3112":
                "$ git status\n"
                "On branch main\n"
                "Changes not staged for commit:\n"
                "        modified:   analysis.ipynb\n"
                "Untracked files:\n"
                "        data/site_inspection_log.csv",
            "CML3113":
                "$ git status\n"
                "On branch main\n"
                "Changes not staged for commit:\n"
                "        modified:   analysis.ipynb\n"
                "Untracked files:\n"
                "        data/drill_shift_log.csv",
            "CML3111":
                "$ git status\n"
                "On branch main\n"
                "Changes not staged for commit:\n"
                "        modified:   analysis.ipynb\n"
                "Untracked files:\n"
                "        data/motor_test_bench.csv",
        },
        "options": [
            ("The notebook is tracked and edited; the CSV was never added",
             True,
             "Correct. Git reports a tracked file as modified and a file it "
             "has never seen as untracked. Committing now would save the "
             "notebook edit and leave the data file behind entirely."),
            ("Both files will be saved by the next commit", False,
             "Neither will. The notebook change is unstaged and the CSV is "
             "untracked, so a bare commit captures nothing from this list."),
            ("The notebook has been committed and the CSV has been deleted",
             False,
             "A committed file with no further edits does not appear in this "
             "output at all, and a deletion is reported as deleted."),
            ("The repository is broken and needs to be created again", False,
             "This is the ordinary output of a healthy repository with work "
             "in progress. It is the state you should expect to see most of "
             "the time."),
        ],
    },
    # ---- 5. judgement: setup readiness
    {
        "kind": "judgement",
        "stem": ("It is twenty minutes before the session. The Python "
                 "install on your laptop fails with an error you have not "
                 "seen before. What is the right move?"),
        "options": [
            ("Open Colab in the browser and work there for the session",
             True,
             "Correct. Colab needs a browser and nothing else, which is why "
             "this course is built on it. Your install can be repaired at a "
             "time when it is not costing you a three-hour session."),
            ("Spend the session fixing the install so the rest of the "
             "semester is smooth", False,
             "This trades a guaranteed three hours of teaching for a repair "
             "of unknown length. Install problems are often version "
             "mismatches with no quick fix, which is why the browser route "
             "exists."),
            ("Copy a classmate's notebook afterwards and read through it",
             False,
             "Reading someone else's finished notebook skips the part that "
             "does the teaching. You would arrive at Week 3 without having "
             "run a single cell yourself."),
            ("Ask for the session to be repeated later in the week", False,
             "There is no second slot: each cohort meets once a week. A "
             "working browser removes the problem in under a minute."),
        ],
    },
]

# ==========================================================================
# QUIZ 3 — Week 3. Python as an engineering calculator.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[3] = [
    # ---- 1. diagnosis: a unit error that returns a plausible number
    {
        "kind": "diagnosis",
        "stem": ("This runs without any error and prints the number shown. "
                 "What is wrong?"),
        "pre_by": {
            "CML3112":
                "def slab_volume(length_m, width_m, thickness_m):\n"
                "    return length_m * width_m * thickness_m\n"
                "\n"
                "volume = slab_volume(6.0, 4.0, 250)\n"
                "print(f\"{volume:.2f} m3 of concrete\")\n"
                "\n"
                "6000.00 m3 of concrete",
            "CML3113":
                "def contained_metal(tonnes, grade_pct):\n"
                "    return tonnes * grade_pct / 100.0\n"
                "\n"
                "metal = contained_metal(250000.0, 1800)\n"
                "print(f\"{metal:,.0f} t of contained metal\")\n"
                "\n"
                "4,500,000 t of contained metal",
            "CML3111":
                "def mechanical_power(torque_nm, rpm):\n"
                "    return torque_nm * rpm * 2 * 3.14159 / 60.0\n"
                "\n"
                "p_out = mechanical_power(8.5, 151.8)\n"
                "print(f\"shaft power {p_out:.0f} W\")\n"
                "\n"
                "shaft power 135 W",
        },
        "options_by": {
            "CML3112": [
                ("The thickness was passed in millimetres to a parameter "
                 "measured in metres", True,
                 "Correct. 250 mm is 0.25 m, and the right answer is 6.00 m3. "
                 "The parameter name says thickness_m and nothing in Python "
                 "enforces that. A slab 250 metres thick would be absurd on "
                 "site, and that absurdity is the only thing protecting you "
                 "here."),
                ("The multiplication should have been a division somewhere",
                 False,
                 "Volume is length times width times thickness, and that is "
                 "what the function computes. The formula is right and the "
                 "input is wrong."),
                ("The result needs rounding to two decimal places", False,
                 "It is already formatted to two decimals. Presentation is "
                 "not the problem; the magnitude is."),
                ("Nothing is wrong; 6000 m3 is a reasonable slab", False,
                 "A transit mixer carries six to eight cubic metres, so "
                 "6000 m3 is around eight hundred truck loads for one slab "
                 "of six metres by four. Always sanity-check the size of an "
                 "answer against something physical you know."),
            ],
            "CML3113": [
                ("The grade was passed in grams per tonne to a parameter "
                 "measured in per cent", True,
                 "Correct. 1800 g/t is 0.18 per cent, and the right answer is "
                 "450 t. The output claims more metal than the ore tonnage "
                 "that contains it, which is impossible and is the tell."),
                ("The division by 100 should not be there", False,
                 "The division by 100 is what converts a percentage into a "
                 "fraction, and it belongs there. The value handed in was "
                 "never a percentage."),
                ("The thousands separator in the format string is wrong",
                 False,
                 "The formatting is fine. A correctly formatted impossible "
                 "number is still impossible."),
                ("Nothing is wrong; high-grade ore gives large tonnages",
                 False,
                 "You cannot recover 4.5 million tonnes of metal from "
                 "250,000 tonnes of rock. Compare the answer with the input "
                 "before believing it."),
            ],
            "CML3111": [
                ("The speed was passed in radians per second to a parameter "
                 "measured in revolutions per minute", True,
                 "Correct. 1450 rpm is 151.8 rad/s, so the value handed in "
                 "had already been converted once. Passing 1450 gives 1291 W, "
                 "which is the right answer for this motor."),
                ("The constant should be 3.14159 divided by two", False,
                 "The 2 pi over 60 converts revolutions per minute into "
                 "radians per second inside the function. That algebra is "
                 "correct."),
                ("Torque and speed were given in the wrong order", False,
                 "Multiplication gives the same product either way, so a "
                 "swap of these two would not change the number. Check the "
                 "units instead."),
                ("Nothing is wrong; 135 W is normal for a small motor",
                 False,
                 "It is a plausible-looking figure, which is what makes this "
                 "dangerous. Check it against the inputs on the line above: "
                 "8.5 N·m at 1450 rpm is about 1.3 kW, so 135 W means the "
                 "torque or the speed is out by roughly a factor of ten."),
            ],
        },
    },
    # ---- 2. diagnosis: if-chain branches in the wrong order
    {
        "kind": "diagnosis",
        "stem": ("This function runs without error. The printed answer is "
                 "wrong and dangerous. Why?"),
        "pre_by": {
            "CML3112":
                "def crack_action(width_mm, exposure):\n"
                "    if width_mm > 0.10:\n"
                "        return \"monitor\"\n"
                "    elif width_mm > 0.30:\n"
                "        return \"flag for repair\"\n"
                "    elif exposure == \"marine\" and width_mm > 0.20:\n"
                "        return \"seal now\"\n"
                "    else:\n"
                "        return \"no action\"\n"
                "\n"
                "print(crack_action(0.45, \"marine\"))\n"
                "monitor",
            "CML3113":
                "def grade_action(grade_pct, cutoff_pct):\n"
                "    if grade_pct >= cutoff_pct * 0.8:\n"
                "        return \"stockpile\"\n"
                "    elif grade_pct >= cutoff_pct * 1.5:\n"
                "        return \"mill now\"\n"
                "    elif grade_pct >= cutoff_pct:\n"
                "        return \"mill\"\n"
                "    else:\n"
                "        return \"waste\"\n"
                "\n"
                "print(grade_action(1.2, 0.5))\n"
                "stockpile",
            "CML3111":
                "def temp_action(winding_c, ambient_c):\n"
                "    rise = winding_c - ambient_c\n"
                "    if rise > 80:\n"
                "        return \"investigate cooling\"\n"
                "    elif winding_c > 155:\n"
                "        return \"trip\"\n"
                "    elif winding_c > 130:\n"
                "        return \"alarm\"\n"
                "    else:\n"
                "        return \"normal\"\n"
                "\n"
                "print(temp_action(162.0, 25.0))\n"
                "investigate cooling",
        },
        "options_by": {
            "CML3112": [
                ("The loosest test is first, so it catches the crack and the "
                 "rest never run", True,
                 "Correct. 0.45 is above 0.10, so the first branch returns "
                 "and nothing below it is ever consulted. A 0.45 mm crack in "
                 "a marine exposure should return seal now. Order the "
                 "branches from the most severe condition downwards."),
                ("The marine condition needs to use or rather than and",
                 False,
                 "The marine rule genuinely requires both a marine exposure "
                 "and a width above 0.20, so and is right. The branch is "
                 "correct and simply never reached."),
                ("The comparisons should be greater-than-or-equal", False,
                 "At 0.45 mm none of these boundaries is touched exactly, so "
                 "that change would not alter this answer. The ordering is "
                 "what decides it."),
                ("The function should not take exposure as an argument",
                 False,
                 "Exposure is exactly what makes 0.45 mm urgent rather than "
                 "routine. Removing it would lose the most important part of "
                 "the rule."),
            ],
            "CML3113": [
                ("The lowest threshold is tested first, so high-grade ore "
                 "matches the stockpile branch and never reaches mill now",
                 True,
                 "Correct. 1.2 is above 0.4, so the first branch returns and "
                 "ore worth milling immediately gets sent to a stockpile. At "
                 "a cut-off of 0.5 this material is above 1.5 times cut-off "
                 "and should return mill now."),
                ("The multipliers 0.8 and 1.5 are the wrong way round",
                 False,
                 "Those multipliers describe the intended bands correctly: "
                 "0.8 of cut-off for marginal material, 1.5 for high grade. "
                 "The sequence of the tests is the fault."),
                ("Cut-off grade should be a fixed number in the function",
                 False,
                 "Passing it in is the better design, because cut-off moves "
                 "with the metal price. That is unrelated to this wrong "
                 "answer."),
                ("The comparisons should be strictly greater than", False,
                 "At 1.2 against a cut-off of 0.5 no boundary is hit exactly, "
                 "so this would change nothing here."),
            ],
            "CML3111": [
                ("The temperature rise is tested first, so a winding hot "
                 "enough to trip only returns the cooling message", True,
                 "Correct. The rise of 137 K clears the 80 K test, so the "
                 "function returns before it can look at 155. A winding at "
                 "162 °C should trip. Order the branches with the most "
                 "severe outcome first."),
                ("The rise should be compared against the winding "
                 "temperature", False,
                 "A temperature rise is the winding temperature minus "
                 "ambient, which is what the code computes. That line is "
                 "right."),
                ("The trip and alarm limits have been swapped", False,
                 "155 for trip and 130 for alarm is the correct way round "
                 "for this insulation class. Both branches are correct and "
                 "neither is reached."),
                ("Ambient temperature should not affect the decision", False,
                 "A rise test catches a cooling fault that an absolute limit "
                 "misses, so it earns its place. It simply must not be "
                 "consulted before the trip limit."),
            ],
        },
    },
    # ---- 3. traceback: string where a number was expected
    {
        "kind": "traceback",
        "stem": "What does this tell you about the variable?",
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n"
                "    total_span = span + 2.5\n"
                "TypeError: can only concatenate str (not \"float\") to str",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n"
                "    total_depth = depth + 2.5\n"
                "TypeError: can only concatenate str (not \"float\") to str",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-5-9f8e7d>\", line 2, in <module>\n"
                "    total_load = load + 2.5\n"
                "TypeError: can only concatenate str (not \"float\") to str",
        },
        "options": [
            ("It holds text, so the plus sign was read as joining strings "
             "and a number cannot be joined to text", True,
             "Correct. The word concatenate is the clue: Python was trying to "
             "stick things together rather than add them. Values typed in or "
             "read from a file arrive as text, and float() converts them."),
            ("It holds a number that is too large for the addition", False,
             "Python integers grow as large as memory allows, and floats "
             "would report an overflow differently. The message names the "
             "type as str."),
            ("The 2.5 should have been written as an integer", False,
             "Adding an integer to text fails in exactly the same way. The "
             "type of the variable is what has to change."),
            ("The variable was never assigned a value", False,
             "That reports itself as a NameError. This variable exists and "
             "holds something; the something is text."),
        ],
    },
    # ---- 4. interpretation: read the corrected decision function
    {
        "kind": "interpretation",
        "stem": "Reading this function as written, what does the call return?",
        "pre_by": {
            "CML3112":
                "def crack_action(width_mm, exposure):\n"
                "    if exposure == \"marine\" and width_mm > 0.20:\n"
                "        return \"seal now\"\n"
                "    elif width_mm > 0.30:\n"
                "        return \"flag for repair\"\n"
                "    elif width_mm > 0.10:\n"
                "        return \"monitor\"\n"
                "    else:\n"
                "        return \"no action\"\n"
                "\n"
                "crack_action(0.25, \"marine\")",
            "CML3113":
                "def grade_action(grade_pct, cutoff_pct):\n"
                "    if grade_pct >= cutoff_pct * 1.5:\n"
                "        return \"mill now\"\n"
                "    elif grade_pct >= cutoff_pct:\n"
                "        return \"mill\"\n"
                "    elif grade_pct >= cutoff_pct * 0.8:\n"
                "        return \"stockpile\"\n"
                "    else:\n"
                "        return \"waste\"\n"
                "\n"
                "grade_action(0.45, 0.50)",
            "CML3111":
                "def temp_action(winding_c, ambient_c):\n"
                "    rise = winding_c - ambient_c\n"
                "    if winding_c > 155:\n"
                "        return \"trip\"\n"
                "    elif winding_c > 130:\n"
                "        return \"alarm\"\n"
                "    elif rise > 80:\n"
                "        return \"investigate cooling\"\n"
                "    else:\n"
                "        return \"normal\"\n"
                "\n"
                "temp_action(120.0, 25.0)",
        },
        "options_by": {
            "CML3112": [
                ("seal now", True,
                 "Correct. The exposure is marine and 0.25 is above 0.20, so "
                 "the first branch matches and returns immediately. The "
                 "0.30 mm limit is never consulted."),
                ("monitor", False,
                 "That is what you get by reading only the width and "
                 "skipping the marine branch above it. In a marine exposure "
                 "the threshold that matters is 0.20."),
                ("flag for repair", False,
                 "That branch needs a width above 0.30. This crack is "
                 "0.25 mm."),
                ("no action", False,
                 "The final branch is only reached when every test above it "
                 "fails. Two of them match here."),
            ],
            "CML3113": [
                ("stockpile", True,
                 "Correct. 0.45 is below the 0.50 cut-off so it is not ore, "
                 "and it is above 0.8 of cut-off which is 0.40, so it is "
                 "marginal material worth keeping rather than dumping."),
                ("mill", False,
                 "That branch needs the grade to reach the cut-off of 0.50. "
                 "This grade is 0.45."),
                ("waste", False,
                 "Waste is what falls below 0.8 of cut-off, which is 0.40. "
                 "At 0.45 this material clears that test."),
                ("mill now", False,
                 "That branch needs 1.5 times cut-off, which is 0.75."),
            ],
            "CML3111": [
                ("investigate cooling", True,
                 "Correct. 120 °C is under both the trip and alarm limits, "
                 "and the rise of 95 K is above 80, so the third branch "
                 "matches. This is the case an absolute limit alone would "
                 "miss."),
                ("normal", False,
                 "That is what you get by checking only the two absolute "
                 "limits. The rise of 95 K says this machine is not "
                 "shedding heat properly."),
                ("alarm", False,
                 "The alarm branch needs a winding above 130 °C. This one is "
                 "at 120 °C."),
                ("trip", False,
                 "The trip branch needs a winding above 155 °C."),
            ],
        },
    },
    # ---- 5. judgement: the limit written in three places
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "A teammate has written the 0.30 mm action limit "
                       "directly into three different cells. The code works. "
                       "What should you do?",
            "CML3113": "A teammate has written the 3 per cent silica "
                       "specification directly into three different cells. "
                       "The code works. What should you do?",
            "CML3111": "A teammate has written the 130 °C alarm limit "
                       "directly into three different cells. The code works. "
                       "What should you do?",
        },
        "options": [
            ("Put it in one named constant and refer to that everywhere",
             True,
             "Correct. When the standard is revised you change one line and "
             "can point to it. Three copies means three chances to update "
             "two of them and ship a notebook that applies two different "
             "limits in the same analysis."),
            ("Leave it, because the code produces the right answers today",
             False,
             "It does work today. The cost arrives on the day the figure "
             "changes, and it arrives as an inconsistency nobody notices "
             "because every cell still runs."),
            ("Write a function that looks the limit up online each time",
             False,
             "That makes the notebook depend on a network and on somebody "
             "else's page layout. A named constant with a comment citing the "
             "clause is auditable and works offline."),
            ("Ask each teammate to remember which cells contain it", False,
             "Relying on memory across a fifteen-week project with several "
             "people is how the two-out-of-three update happens."),
        ],
    },
]

# ==========================================================================
# QUIZ 4 — Week 4. Collections, loops and files.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[4] = [
    # ---- 1. diagnosis: accumulator reset inside the loop
    {
        "kind": "diagnosis",
        "stem": ("This runs cleanly and prints the mean shown. The mean is "
                 "wrong. What causes it?"),
        "pre_by": {
            "CML3112":
                "widths = [0.12, 0.35, 0.41, 0.08]\n"
                "total = 0.0\n"
                "for w in widths:\n"
                "    total = 0.0\n"
                "    total = total + w\n"
                "\n"
                "print(f\"mean width {total / len(widths):.3f} mm\")\n"
                "mean width 0.020 mm",
            "CML3113":
                "rates = [7.2, 9.5, 8.1, 6.4]\n"
                "total = 0.0\n"
                "for r in rates:\n"
                "    total = 0.0\n"
                "    total = total + r\n"
                "\n"
                "print(f\"mean rate {total / len(rates):.3f} m/h\")\n"
                "mean rate 1.600 m/h",
            "CML3111":
                "temps = [118, 131, 126, 141]\n"
                "total = 0.0\n"
                "for t in temps:\n"
                "    total = 0.0\n"
                "    total = total + t\n"
                "\n"
                "print(f\"mean temp {total / len(temps):.2f} C\")\n"
                "mean temp 35.25 C",
        },
        "options_by": {
            "CML3112": [
                ("The reset to zero sits inside the loop, so only the last "
                 "value survives", True,
                 "Correct. Every pass throws away the running total, so the "
                 "loop leaves 0.08 behind and 0.08 divided by 4 is 0.020. "
                 "The true mean is 0.240 mm. Move the reset above the loop."),
                ("The division should use the number of readings above the "
                 "limit", False,
                 "A mean over all readings divides by all of them, so "
                 "len(widths) is right. The numerator is what has been "
                 "destroyed."),
                ("Adding floats accumulates rounding error", False,
                 "Float rounding here would show up somewhere past the third "
                 "decimal. This answer is out by a factor of twelve."),
                ("The list should have been a dictionary", False,
                 "A list of readings is the right structure for a mean. The "
                 "fault is one misplaced line."),
            ],
            "CML3113": [
                ("The reset to zero sits inside the loop, so only the last "
                 "value survives", True,
                 "Correct. The running total is wiped on every pass, leaving "
                 "6.4, and 6.4 divided by 4 is 1.600. The true mean is "
                 "7.800 m/h. Move the reset above the loop."),
                ("The loop variable has the same name as one of the rates",
                 False,
                 "The loop variable is r and the list is rates, so nothing "
                 "is shadowed. Even if it were, that would not empty the "
                 "running total on every pass."),
                ("Adding floats accumulates rounding error", False,
                 "Float rounding would appear in the far decimals. This "
                 "answer is out by a factor of nearly five."),
                ("The list should have been a dictionary", False,
                 "A list is the right structure for a sequence of readings."),
            ],
            "CML3111": [
                ("The reset to zero sits inside the loop, so only the last "
                 "value survives", True,
                 "Correct. Each pass discards the total, leaving 141, and 141 "
                 "divided by 4 is 35.25. The true mean is 129.00 °C. Move "
                 "the reset above the loop."),
                ("The temperatures are integers and the total is a float",
                 False,
                 "Python handles that mixture without trouble and the "
                 "division is correct. The numerator is the problem."),
                ("Adding floats accumulates rounding error", False,
                 "Rounding error at this scale is invisible. A mean of 35 °C "
                 "for readings between 118 and 141 is a structural error."),
                ("The list should have been a dictionary", False,
                 "A list is the right structure here."),
            ],
        },
    },
    # ---- 2. diagnosis: range starting at one
    {
        "kind": "diagnosis",
        "stem": ("This prints a count that is one too low on this file. "
                 "Why?"),
        "pre_by": {
            "CML3112":
                "widths = [0.44, 0.35, 0.41, 0.08]\n"
                "LIMIT = 0.30\n"
                "over = 0\n"
                "for i in range(1, len(widths)):\n"
                "    if widths[i] > LIMIT:\n"
                "        over = over + 1\n"
                "\n"
                "print(f\"{over} readings above the limit\")\n"
                "2 readings above the limit",
            "CML3113":
                "rates = [9.1, 8.6, 7.2, 8.3]\n"
                "TARGET = 8.0\n"
                "over = 0\n"
                "for i in range(1, len(rates)):\n"
                "    if rates[i] > TARGET:\n"
                "        over = over + 1\n"
                "\n"
                "print(f\"{over} holes above target rate\")\n"
                "2 holes above target rate",
            "CML3111":
                "temps = [134, 131, 128, 126]\n"
                "ALARM = 130\n"
                "over = 0\n"
                "for i in range(1, len(temps)):\n"
                "    if temps[i] > ALARM:\n"
                "        over = over + 1\n"
                "\n"
                "print(f\"{over} readings above the alarm limit\")\n"
                "1 readings above the alarm limit",
        },
        "options_by": {
            "CML3112": [
                ("The range starts at 1, so the first reading is never "
                 "tested", True,
                 "Correct. Python indexes from 0, so range(1, 4) visits "
                 "positions 1, 2 and 3 and skips 0.44 entirely. Three "
                 "readings exceed 0.30. Use range(len(widths)), or better, "
                 "loop over the values directly."),
                ("The range stops one short of the end of the list", False,
                 "range(1, 4) does reach position 3, which is the last of "
                 "four. The miss is at the start."),
                ("The comparison should be greater-than-or-equal", False,
                 "No reading here sits exactly on 0.30, so that change would "
                 "not alter the count."),
                ("The counter should start at 1", False,
                 "A count of things starts at nothing. Starting at 1 would "
                 "hide this bug behind a second one and give the right "
                 "answer for the wrong reason."),
            ],
            "CML3113": [
                ("The range starts at 1, so the first hole is never tested",
                 True,
                 "Correct. range(1, 4) skips position 0, which holds 9.1. "
                 "Three holes beat the 8.0 m/h target. Loop over the values "
                 "directly and the question of where to start disappears."),
                ("The range stops one short of the end of the list", False,
                 "It reaches position 3, the last of four. The skipped "
                 "element is the first one."),
                ("The comparison should be greater-than-or-equal", False,
                 "No rate here equals 8.0 exactly, so that would change "
                 "nothing."),
                ("The counter should start at 1", False,
                 "A count starts at nothing. Pre-loading it to 1 would mask "
                 "this bug rather than fix it."),
            ],
            "CML3111": [
                ("The range starts at 1, so the first reading is never "
                 "tested", True,
                 "Correct. range(1, 4) skips position 0, which holds 134. "
                 "Two readings exceed 130. Loop over the values themselves "
                 "and the off-by-one cannot happen."),
                ("The range stops one short of the end of the list", False,
                 "It reaches position 3, the last of four. The problem is at "
                 "the beginning."),
                ("The comparison should be greater-than-or-equal", False,
                 "No reading equals 130 exactly here, so that change would "
                 "not affect the count."),
                ("The counter should start at 1", False,
                 "That would give the right total here by accident, while "
                 "leaving the real fault in place and breaking every other "
                 "file."),
            ],
        },
    },
    # ---- 3. traceback: blank field in a CSV
    {
        "kind": "traceback",
        "stem": ("You are reading a 300-row file and it stops partway "
                 "through with this. What has happened, and what should the "
                 "loop do about it?"),
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n"
                "    if float(row[\"crack_width_mm\"]) > LIMIT:\n"
                "ValueError: could not convert string to float: ''",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n"
                "    if float(row[\"rate_of_penetration\"]) > TARGET:\n"
                "ValueError: could not convert string to float: ''",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-7-4c5d6e>\", line 4, in <module>\n"
                "    if float(row[\"winding_temp_c\"]) > ALARM:\n"
                "ValueError: could not convert string to float: ''",
        },
        "options": [
            ("That field is empty in one row, so the loop should skip that "
             "row and count how many it skipped", True,
             "Correct. The two quote marks with nothing between them are an "
             "empty string. Skipping is the right response and the count of "
             "skips belongs in your report, because it tells the reader how "
             "much of the file the answer actually covers."),
            ("The column name is spelled wrongly", False,
             "A wrong column name raises a KeyError before any conversion is "
             "attempted. The column was found; its content was empty."),
            ("The whole file is corrupted and cannot be used", False,
             "One blank field in one row says nothing about the other 299. "
             "Handle the gap and carry on."),
            ("The empty value should be replaced with zero so the loop can "
             "continue", False,
             "This is the trap. Zero is a real measurement, so substituting "
             "it silently drags every average downwards. Week 6 is largely "
             "about the damage this does."),
        ],
    },
    # ---- 4. interpretation: what the skipped-row count means
    {
        "kind": "interpretation",
        "stem": ("Your script prints this summary. Which statement does it "
                 "support?"),
        "pre_by": {
            "CML3112":
                "rows in file      300\n"
                "rows used         287\n"
                "rows skipped       13\n"
                "mean crack width 0.21 mm",
            "CML3113":
                "rows in file      300\n"
                "rows used         287\n"
                "rows skipped       13\n"
                "mean rate         8.40 m/h",
            "CML3111":
                "rows in file      300\n"
                "rows used         287\n"
                "rows skipped       13\n"
                "mean temp rise   62.5 K",
        },
        "options": [
            ("The mean describes the 287 usable rows, and the other 13 "
             "need explaining", True,
             "Correct. A mean is only ever a mean of what went into it. If "
             "the 13 gaps are scattered at random the figure is probably "
             "fine; if they share a cause the figure is biased and the count "
             "is your only warning."),
            ("The mean describes all 300 rows in the file", False,
             "Thirteen rows contributed nothing to it. Reporting it as a "
             "figure for the file overstates what you measured."),
            ("The 13 skipped rows were duplicates", False,
             "The summary says they were skipped and does not say why. "
             "Duplicates are a separate problem, and one you meet in "
             "Week 6."),
            ("Losing 13 rows out of 300 is too small to mention", False,
             "The size of the loss is not what matters; the reason is. "
             "Thirteen gaps from one source can move a mean further than "
             "fifty scattered at random."),
        ],
    },
    # ---- 5. judgement: the skips share a source
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "You look at the 13 skipped rows and every one of "
                       "them comes from the same inspector. What should you "
                       "do before reporting the mean?",
            "CML3113": "You look at the 13 skipped rows and every one of "
                       "them comes from the same shift. What should you do "
                       "before reporting the mean?",
            "CML3111": "You look at the 13 skipped rows and every one of "
                       "them comes from the same test day. What should you "
                       "do before reporting the mean?",
        },
        "options": [
            ("Investigate the shared cause first, because gaps that cluster "
             "in one source point at how the data was collected", True,
             "Correct. Thirteen blanks spread across the file is untidiness. "
             "Thirteen blanks from one source is a finding, and it may "
             "matter more than the mean you were asked for."),
            ("Report the mean and mention the 13 skips in a footnote", False,
             "Reporting the count is necessary and it is not sufficient "
             "here. A footnote presents a systematic gap as though it were "
             "random noise."),
            ("Fill the gaps with that source's own average so no rows are "
             "lost", False,
             "That invents readings from the one source you have reason to "
             "distrust, and it hides the pattern you just found."),
            ("Drop that source entirely and report the rest", False,
             "That might end up being right, and it is a decision to take "
             "after you understand the cause. Removing a source before "
             "knowing why it failed can delete the very thing under "
             "investigation."),
        ],
    },
]

# ==========================================================================
# QUIZ 5 — Week 5. pandas, and judging a dataset.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[5] = [
    # ---- 1. diagnosis: a mask is not a filtered frame
    {
        "kind": "diagnosis",
        "stem": ("You wanted the number of records above the threshold. This "
                 "prints the whole row count instead. Why?"),
        "pre_by": {
            # mask.sum() is shown so the "every row qualifies" option can be
            # ruled out from the block rather than argued about.
            "CML3112":
                "mask = df[\"strength\"] > 40\n"
                "print(len(mask))\n"
                "1030\n"
                "print(mask.sum())\n"
                "289",
            "CML3113":
                "mask = df[\"silica_concentrate\"] > 3\n"
                "print(len(mask))\n"
                "20000\n"
                "print(mask.sum())\n"
                "4120",
            "CML3111":
                "mask = df[\"output\"] > 450\n"
                "print(len(mask))\n"
                "9568\n"
                "print(mask.sum())\n"
                "3702",
        },
        "options": [
            ("The mask holds one True or False per row, so its length is "
             "the row count", True,
             "Correct. A comparison on a column answers the question for "
             "every row and hands back all the answers, so it is always as "
             "long as the frame. mask.sum() counts the True entries, as the "
             "second line shows, and len(df[mask]) counts the rows you keep."),
            ("The comparison was written the wrong way round", False,
             "Reversing it would produce a different set of True entries and "
             "the same length. Length is the wrong measurement to be "
             "taking."),
            ("The threshold is too low, so every row qualifies", False,
             "The second line rules this out: the sum is well below the row "
             "count, so most rows do not qualify. Notice also that the "
             "length would have been the row count either way, which is what "
             "makes it the wrong thing to measure."),
            ("len() does not work on pandas objects", False,
             "It works and it reported the truth. The truth it reported "
             "answers a different question from the one you asked."),
        ],
    },
    # ---- 2. diagnosis: object dtype makes max compare text
    {
        "kind": "diagnosis",
        "stem": ("The maximum below is far too small and no error was "
                 "raised. What has happened?"),
        "pre_by": {
            "CML3112":
                "print(df[\"strength\"].dtype)\n"
                "object\n"
                "\n"
                "print(df[\"strength\"].max())\n"
                "9.9\n"
                "\n"
                "# the file contains values such as 32.5, 41.2, 9.9, 28.0",
            "CML3113":
                "print(df[\"iron_feed\"].dtype)\n"
                "object\n"
                "\n"
                "print(df[\"iron_feed\"].max())\n"
                "9.9\n"
                "\n"
                "# the file contains values such as 56.3, 41.2, 9.9, 28.0",
            "CML3111":
                "print(df[\"output\"].dtype)\n"
                "object\n"
                "\n"
                "print(df[\"output\"].max())\n"
                "9.9\n"
                "\n"
                "# the file contains values such as 32.5, 41.2, 9.9, 28.0",
        },
        "options": [
            ("The column holds text, so the maximum was decided "
             "alphabetically and a value starting with 9 wins", True,
             "Correct. object dtype means the column is text. Compared as "
             "text, \"9.9\" beats \"41.2\" because the character 9 comes "
             "after 4. Convert with pd.to_numeric and the real maximum "
             "appears. One stray value with a unit or a stray space is "
             "usually what forced the whole column to text."),
            ("The column contains missing values that max() skipped", False,
             "max() does skip missing values, and skipping them cannot "
             "produce a maximum below most of the data. The ordering itself "
             "is what has gone wrong."),
            ("The largest values are stored in a different column", False,
             "The comment shows the values are in this column. The problem "
             "is how they are being compared."),
            ("max() needs the column sorted first", False,
             "max() never needs sorting. It compared correctly by the rules "
             "for text, which are the wrong rules for measurements."),
        ],
    },
    # ---- 3. traceback: KeyError on a column name
    {
        "kind": "traceback",
        "stem": "What is the first thing to check?",
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n"
                "    df[\"strength_mpa\"].mean()\n"
                "KeyError: 'strength_mpa'",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n"
                "    df[\"silica_pct\"].mean()\n"
                "KeyError: 'silica_pct'",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-4-7a8b9c>\", line 1, in <module>\n"
                "    df[\"power_output\"].mean()\n"
                "KeyError: 'power_output'",
        },
        "options": [
            ("Print df.columns and compare the exact spelling, case and any "
             "stray spaces", True,
             "Correct. A KeyError on a frame means no column carries that "
             "exact label. Trailing spaces from a spreadsheet export are a "
             "common cause and they are invisible until you print the list."),
            ("Whether the column contains missing values", False,
             "Missing values inside a column never stop you selecting it. "
             "This error happened before any value was read."),
            ("Whether the file loaded at all", False,
             "That is worth confirming, and a frame that failed to load "
             "would raise on the read or on len(df) first. The message names "
             "one specific label."),
            ("Whether mean() works on that data type", False,
             "The error came from the selection, before mean() was reached. "
             "A type problem would name the type."),
        ],
    },
    # ---- 4. interpretation: the shape of a groupby result
    {
        "kind": "interpretation",
        "stem": "What does this shape tell you?",
        "pre_by": {
            "CML3112":
                "g = df.groupby(\"age_band\")[\"strength\"].mean()\n"
                "print(g.shape)\n"
                "(4,)",
            "CML3113":
                "g = df.groupby(\"ph_band\")[\"silica_concentrate\"].mean()\n"
                "print(g.shape)\n"
                "(4,)",
            "CML3111":
                "g = df.groupby(\"temp_band\")[\"output\"].mean()\n"
                "print(g.shape)\n"
                "(4,)",
        },
        "options": [
            ("There are four groups, and the result holds one mean for each "
             "of them", True,
             "Correct. Grouping collapses the frame to one row per group, so "
             "the length of the result is the number of distinct values in "
             "the grouping column. The original frame is untouched."),
            ("Four rows of the original data survived the operation", False,
             "Grouping summarises rows rather than removing them. Every row "
             "contributed to one of the four means."),
            ("The result has four columns", False,
             "A shape written with one number describes one dimension. Four "
             "columns would appear as a second number."),
            ("Four rows had a missing value in the grouping column", False,
             "Rows with a missing group label are left out of the result "
             "rather than counted into it, and that would not set the "
             "length to four."),
        ],
    },
    # ---- 5. judgement: provenance before publication
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "A colleague sends you concrete_strength.csv as an "
                       "email attachment with no other information, and you "
                       "are asked to quote the mean strength in a report. "
                       "What do you do first?",
            "CML3113": "A colleague sends you flotation_subset.csv as an "
                       "email attachment with no other information, and you "
                       "are asked to quote the mean concentrate silica in a "
                       "report. What do you do first?",
            "CML3111": "A colleague sends you power_plant.csv as an email "
                       "attachment with no other information, and you are "
                       "asked to quote the mean power output in a report. "
                       "What do you do first?",
        },
        "options": [
            ("Establish where the file came from, what licence it carries "
             "and how many rows it holds, and record all three alongside the "
             "figure", True,
             "Correct. A number in a report is only as defensible as the "
             "file behind it. Source, licence, date and row count are the "
             "minimum you need to be able to answer the question every "
             "reader eventually asks, which is where this came from."),
            ("Compute the mean and quote it, since the file is the data you "
             "were given", False,
             "The arithmetic is the easy part and the least of your "
             "obligations. A figure whose origin you cannot state is one you "
             "cannot defend when it is challenged."),
            ("Ask for the file in a different format to be safe", False,
             "The format is not the risk. An unsourced spreadsheet is "
             "exactly as unsourced after conversion."),
            ("Compare it against a published dataset and use whichever looks "
             "cleaner", False,
             "Choosing data by how tidy it looks selects for convenience "
             "over relevance. Find out what this file is before reaching for "
             "another one."),
        ],
    },
]

# ==========================================================================
# QUIZ 6 — Week 6. Dirty data, and seeing it.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[6] = [
    # ---- 1. diagnosis: a sentinel value averaged as though real
    {
        "kind": "diagnosis",
        "stem_by": {
            # Only the -999 case is literally impossible. Saying "impossible"
            # to the other two cohorts would ask them to spot something that
            # is not there, and would hand this cohort the answer.
            "CML3113": "The mean below is impossible. Read the values and say "
                       "what went wrong.",
            "CML3112": "The mean below is lower than every real reading in "
                       "the list. What went wrong?",
            "CML3111": "The mean below is lower than every real reading in "
                       "the list. What went wrong?",
        },
        "pre_by": {
            "CML3113":
                "# the laboratory system writes -999 when no result came back\n"
                "silica = [2.1, 2.4, -999, 2.8, 2.2]\n"
                "print(f\"mean {sum(silica) / len(silica):.2f} % silica\")\n"
                "mean -197.90 % silica",
            "CML3112":
                "# the survey tool writes 0 when the area field is left blank\n"
                "floor_area = [120, 0, 95, 110]\n"
                "print(f\"mean {sum(floor_area) / len(floor_area):.2f} m2\")\n"
                "mean 81.25 m2",
            "CML3111":
                "# the logger writes 0.0 when the accelerometer drops out\n"
                "vibration = [2.41, 0.0, 2.38, 2.44]\n"
                "print(f\"mean {sum(vibration) / len(vibration):.4f} mm/s\")\n"
                "mean 1.8075 mm/s",
        },
        "options_by": {
            "CML3113": [
                ("One entry is a code standing in for a missing assay", True,
                 "Correct. -999 is a marker meaning no result, and arithmetic "
                 "has no way to know that. The mean of the four real assays "
                 "is 2.38 per cent. Replace the code with a proper missing "
                 "value before any arithmetic touches the column."),
                ("The list is too short for a mean to be meaningful", False,
                 "Four real values give a perfectly usable mean. The "
                 "arithmetic was poisoned by a fifth entry that is not a "
                 "measurement at all."),
                ("Silica cannot be negative, so the sensor is faulty", False,
                 "Silica certainly cannot be negative, and no sensor "
                 "produced -999. It is a convention for absent data, which "
                 "is why it is such a reliable trap."),
                ("The division should exclude the last value", False,
                 "The problem is not which position is excluded. It is that "
                 "a placeholder is being treated as data."),
            ],
            "CML3112": [
                ("One entry is a zero standing in for a missing area", True,
                 "Correct. A zero-coded gap is the most dangerous kind, "
                 "because zero is a legal number and nothing looks wrong. "
                 "The mean of the three real areas is 108.33 m2. Convert "
                 "these zeros to missing values first."),
                ("The list is too short for a mean to be meaningful", False,
                 "Three real values give a usable mean. A fourth entry that "
                 "is not a measurement is what moved it."),
                ("A floor area of zero is possible for an unbuilt unit",
                 False,
                 "The comment settles it: this tool writes 0 for a blank "
                 "field, so this zero records an absence of data rather than "
                 "an absence of floor. Without that comment the option would "
                 "be arguable, which is why a column like this needs its "
                 "coding documented before you touch it."),
                ("The division should exclude the last value", False,
                 "The position of the offending entry is incidental. Treating "
                 "a placeholder as data is the fault."),
            ],
            "CML3111": [
                ("One entry is a sensor dropout recorded as zero", True,
                 "Correct. A dropout written as 0.0 is indistinguishable from "
                 "a real reading by arithmetic alone. The mean of the three "
                 "real readings is 2.4100 mm/s. Convert dropouts to missing "
                 "values before averaging."),
                ("The list is too short for a mean to be meaningful", False,
                 "Three real readings give a usable mean. The fourth entry "
                 "is not a reading."),
                ("Zero vibration is possible when the machine is stopped",
                 False,
                 "The comment settles it: this logger writes 0.0 for a "
                 "dropout, so this reading records a lost signal rather than "
                 "a still machine. Without that comment the option would be "
                 "arguable, and a genuine zero from a stopped machine still "
                 "has no place in an average of running vibration."),
                ("The division should exclude the last value", False,
                 "Which position is dropped is beside the point. A "
                 "placeholder is being counted as a measurement."),
            ],
        },
    },
    # ---- 2. diagnosis: coerce silently discards values
    {
        "kind": "diagnosis",
        "stem": ("This runs with no error and no warning. What has it done "
                 "to your data?"),
        "pre_by": {
            "CML3112":
                "# one strength was typed as \"32.5 MPa\" instead of 32.5\n"
                "df[\"strength\"] = pd.to_numeric(df[\"strength\"],\n"
                "                                 errors=\"coerce\")\n"
                "print(df[\"strength\"].mean())",
            "CML3113":
                "# one grade was typed as \"1.8 %\" instead of 1.8\n"
                "df[\"iron_feed\"] = pd.to_numeric(df[\"iron_feed\"],\n"
                "                                  errors=\"coerce\")\n"
                "print(df[\"iron_feed\"].mean())",
            "CML3111":
                "# one current was typed as \"12.5 A\" instead of 12.5\n"
                "df[\"current_a\"] = pd.to_numeric(df[\"current_a\"],\n"
                "                                  errors=\"coerce\")\n"
                "print(df[\"current_a\"].mean())",
        },
        "options": [
            ("It turned every unreadable value into a missing value, and the "
             "mean then quietly skipped those rows", True,
             "Correct. Coercing is often the right move and it is never "
             "free: it converts a loud failure into a silent one. Count the "
             "missing values it created and report that count, otherwise "
             "your mean covers fewer rows than you believe."),
            ("It stripped the unit and kept the number", False,
             "Nothing here parses units. A value with a unit attached is "
             "unreadable as a number and becomes missing."),
            ("It raised the error but carried on to the next row", False,
             "That is what errors=\"raise\" would do, minus the carrying on. "
             "Coercing suppresses the error entirely."),
            ("It replaced the unreadable value with the column mean", False,
             "No substitution happens. Filling gaps is a separate decision "
             "you have to make deliberately, and doing it before a split "
             "leaks information, as Week 10 shows."),
        ],
    },
    # ---- 3. traceback: to_numeric without coerce
    {
        "kind": "traceback",
        "stem": ("You convert the column without coercing and get this. What "
                 "is the useful thing about this message?"),
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n"
                "    df[\"strength\"] = pd.to_numeric(df[\"strength\"])\n"
                "ValueError: Unable to parse string \"32.5 MPa\" at "
                "position 417",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n"
                "    df[\"iron_feed\"] = pd.to_numeric(df[\"iron_feed\"])\n"
                "ValueError: Unable to parse string \"1.8 %\" at "
                "position 417",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-6-2b3c4d>\", line 1, in <module>\n"
                "    df[\"current_a\"] = pd.to_numeric(df[\"current_a\"])\n"
                "ValueError: Unable to parse string \"12.5 A\" at "
                "position 417",
        },
        "options": [
            ("It names the offending value and the row it sits in, so you "
             "can look at it and decide what it should be", True,
             "Correct. This is more useful than a silent conversion, because "
             "it hands you the exact value and position. Look at row 417, "
             "decide whether to repair the entry or drop it, and write down "
             "which you chose."),
            ("It proves the column cannot be converted", False,
             "It proves one value cannot. Fix or remove that value and the "
             "column converts."),
            ("It means the column is the wrong data type for pandas", False,
             "The column is text because of this value. Conversion is the "
             "cure and the message is telling you what stands in the way."),
            ("It should be suppressed so the analysis can continue", False,
             "Suppressing it is available and it costs you the position and "
             "the value. Read the message first, then decide."),
        ],
    },
    # ---- 4. interpretation: a chart that does not answer its question
    {
        "kind": "interpretation",
        "stem": ("Read the question you set yourself against the chart you "
                 "produced. Does the chart answer it?"),
        "pre_by": {
            "CML3112":
                "question:  Does mean strength differ between mixes\n"
                "           with and without fly ash?\n"
                "\n"
                "chart:     one histogram\n"
                "           x = compressive strength (MPa)\n"
                "           y = number of mixes\n"
                "           all 1,030 mixes, no grouping applied",
            "CML3113":
                "question:  Does concentrate silica differ between\n"
                "           high and low iron feed grade?\n"
                "\n"
                "chart:     one histogram\n"
                "           x = concentrate silica (%)\n"
                "           y = number of records\n"
                "           all 20,000 records, no grouping applied",
            "CML3111":
                "question:  Does power output differ between the\n"
                "           coldest and the hottest hours?\n"
                "\n"
                "chart:     one histogram\n"
                "           x = net power output (MW)\n"
                "           y = number of hours\n"
                "           all 9,568 hours, no grouping applied",
        },
        "options": [
            ("No, because the two groups are mixed together in one "
             "distribution and cannot be compared", True,
             "Correct. The question asks for a comparison, so the chart has "
             "to separate the groups: two distributions side by side, or a "
             "mean for each with its spread. A single pooled histogram "
             "cannot show a difference between halves it never divided."),
            ("Yes, because the shape of the distribution reveals the two "
             "groups", False,
             "Two clear humps would hint at something and would not tell you "
             "which group each hump belongs to. A distribution with one hump "
             "can still hide a real difference between the groups."),
            ("Yes, provided the sample is large enough", False,
             "Sample size cannot rescue a chart that never made the "
             "comparison. Twenty thousand pooled records answer the question "
             "no better than two hundred."),
            ("No, because a histogram is never the right chart", False,
             "A histogram is a good way to show one distribution. The fault "
             "is the missing split rather than the choice of chart type."),
        ],
    },
    # ---- 5. judgement: an extreme value that is real
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "You find a 28-day compressive strength of 91 MPa in "
                       "a file where most mixes sit between 20 and 50 MPa. "
                       "What do you do with it?",
            "CML3113": "You find a gold assay of 45 grams per tonne in a "
                       "file where most assays sit between 0.5 and 3 grams "
                       "per tonne. What do you do with it?",
            "CML3111": "You find a current reading six times the running "
                       "current, lasting a fraction of a second at the "
                       "moment a motor starts. What do you do with it?",
        },
        "options_by": {
            "CML3112": [
                ("Keep it and check the mix design", True,
                 "Correct. 91 MPa is unusual and entirely possible for a "
                 "high-performance mix. Verify it against the mix design and "
                 "the test record, and keep it. An extreme value is a "
                 "question to answer rather than a row to delete."),
                ("Delete it, because it is far outside the normal range",
                 False,
                 "Distance from the mean is not evidence of error. Deleting "
                 "real high-strength mixes teaches your model that such "
                 "mixes do not exist."),
                ("Cap it at the highest ordinary value so it stops "
                 "distorting the mean", False,
                 "Capping fabricates a measurement that was never taken and "
                 "hides the very behaviour you might be trying to predict."),
                ("Replace it with the mean of the column", False,
                 "That substitutes an invented average for a real result and "
                 "makes the data look tidier than the world it came from."),
            ],
            "CML3113": [
                ("Keep it and verify it against the assay record", True,
                 "Correct. A 45 g/t intersection is exactly what a drilling "
                 "programme exists to find. Confirm it in the laboratory "
                 "register and keep it. Deleting it removes the discovery."),
                ("Delete it, because it is far outside the normal range",
                 False,
                 "This is the single most expensive mistake available in "
                 "this dataset. The outlier is the ore body."),
                ("Cap it at the highest ordinary value so it stops "
                 "distorting the mean", False,
                 "Capping a high-grade result understates the resource and "
                 "would be indefensible in a technical report."),
                ("Replace it with the mean of the column", False,
                 "That erases a genuine high-grade result and replaces it "
                 "with a number nobody measured."),
            ],
            "CML3111": [
                ("Keep it and label it as a start-up sample", True,
                 "Correct. Starting current runs six to eight times the "
                 "running value and it is expected behaviour. Keep it, mark "
                 "it as a start-up sample, and decide separately whether "
                 "start-up hours belong in the analysis you are doing."),
                ("Delete it, because it is far outside the normal range",
                 False,
                 "Deleting inrush hides a normal operating state. A model "
                 "that has never seen a start-up will treat every start-up "
                 "as a fault."),
                ("Cap it at the highest running value so it stops distorting "
                 "the mean", False,
                 "Capping invents a reading and removes the signature of an "
                 "ordinary event."),
                ("Replace it with the mean of the column", False,
                 "That substitutes an invented value for a correct "
                 "measurement of a real phenomenon."),
            ],
        },
    },
]

# ==========================================================================
# QUIZ 7 — Week 8. Learning from data: the first model.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[8] = [
    # ---- 1. diagnosis: score quoted on the training rows
    {
        "kind": "diagnosis",
        "stem": ("A teammate reports this as the accuracy of the model. What "
                 "does the number actually describe?"),
        "pre_by": {
            "CML3112":
                "model.fit(X, y)\n"
                "print(model.score(X, y))\n"
                "0.91",
            "CML3113":
                "model.fit(X, y)\n"
                "print(model.score(X, y))\n"
                "0.91",
            "CML3111":
                "model.fit(X, y)\n"
                "print(model.score(X, y))\n"
                "0.91",
        },
        "options": [
            ("How well the model reproduces the rows it was fitted on, which "
             "tells you nothing about a new case", True,
             "Correct. The same rows appear in fit and in score, so the "
             "model is being marked on the answers it was shown. Hold rows "
             "back with train_test_split and score on those."),
            ("How well the model will do on new data, give or take a little",
             False,
             "There is no basis for that reading. A model with enough "
             "freedom can score near one on its training rows and fail "
             "completely on anything new, which is the whole subject of "
             "Week 10."),
            ("The proportion of the data used for training", False,
             "score() returns a measure of fit. The train and test "
             "proportions are whatever you chose when you split, and here "
             "nothing was split."),
            ("Nothing useful, because score() is the wrong function", False,
             "score() is the right function used on the wrong rows. Give it "
             "held-out data and the number becomes meaningful."),
        ],
    },
    # ---- 2. diagnosis: features passed in the wrong order
    {
        "kind": "diagnosis",
        "stem": ("This predicts a plausible-looking value and raises no "
                 "error, and the value is wrong. Why?"),
        "pre_by": {
            "CML3112":
                "feats = [\"cement\", \"water\", \"age\"]\n"
                "model.fit(df[feats], df[\"strength\"])\n"
                "\n"
                "# a new mix: 380 kg/m3 cement, 190 kg/m3 water, 28 days\n"
                "print(model.predict([[190, 380, 28]]))",
            "CML3113":
                "feats = [\"iron_feed\", \"starch_flow\", \"pulp_ph\"]\n"
                "model.fit(df[feats], df[\"silica_concentrate\"])\n"
                "\n"
                "# a new record: 56.3 % iron feed, 3180 g/min starch, pH 9.4\n"
                "print(model.predict([[3180, 56.3, 9.4]]))",
            "CML3111":
                "feats = [\"AT\", \"V\", \"AP\", \"RH\"]\n"
                "model.fit(df[feats], df[\"output\"])\n"
                "\n"
                "# a new hour: 14.6 C, 41.7 cm Hg, 1019 mbar, 76 % humidity\n"
                "print(model.predict([[41.7, 14.6, 1019, 76]]))",
        },
        "options": [
            ("The values were supplied in a different order from the fitted "
             "columns", True,
             "Correct. A fitted model knows only that its first input is "
             "whatever its first training column was. Swap two and it "
             "happily applies the wrong coefficient to each. Build the row "
             "as a frame with named columns and this class of error "
             "disappears."),
            ("The new values should have been scaled first", False,
             "Scaling would matter for some model types and it would not "
             "repair a swap. Scaled or raw, the values are in the wrong "
             "positions."),
            ("predict() needs a two-dimensional input", False,
             "It does, and it was given one. The doubled brackets are "
             "correct here."),
            ("The model was fitted on too few features to predict anything",
             False,
             "Three or four features is enough to produce a prediction. The "
             "count is fine and the order is not."),
        ],
    },
    # ---- 3. traceback: inconsistent sample counts
    {
        "kind": "traceback",
        "stem": "What is the most likely cause?",
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n"
                "    model.fit(X, y)\n"
                "ValueError: Found input variables with inconsistent numbers\n"
                "of samples: [824, 1030]",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n"
                "    model.fit(X, y)\n"
                "ValueError: Found input variables with inconsistent numbers\n"
                "of samples: [16000, 20000]",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-9-5e6f7a>\", line 1, in <module>\n"
                "    model.fit(X, y)\n"
                "ValueError: Found input variables with inconsistent numbers\n"
                "of samples: [7654, 9568]",
        },
        "options": [
            ("The features were filtered or had rows dropped and the target "
             "was not, so the two no longer line up", True,
             "Correct. Dropping missing values from the feature frame "
             "without applying the same selection to the target is the usual "
             "cause. Filter the frame first and take X and y from the "
             "filtered frame so they can never drift apart."),
            ("The target column contains missing values", False,
             "Missing values in the target give a different complaint about "
             "NaN. This message is purely about the row counts disagreeing."),
            ("The features and the target need to be the same data type",
             False,
             "They routinely differ, and that is fine. The error counts rows "
             "and says nothing about types."),
            ("There are too few rows to fit a model", False,
             "Both counts here are ample. The problem is that they are not "
             "equal."),
        ],
    },
    # ---- 4. interpretation: residuals plotted against the actual value
    {
        "kind": "interpretation",
        "stem": ("A teammate shows you this plot and this conclusion. How "
                 "should you read it?"),
        "pre_by": {
            "CML3112":
                "plot:        y = residual (actual - predicted), MPa\n"
                "             x = ACTUAL 28-day strength, MPa\n"
                "             a clear upward slope, left to right\n"
                "\n"
                "conclusion:  \"the model under-predicts strong mixes\"",
            "CML3113":
                "plot:        y = residual (actual - predicted), % silica\n"
                "             x = ACTUAL concentrate silica, %\n"
                "             a clear upward slope, left to right\n"
                "\n"
                "conclusion:  \"the model under-predicts high-silica\n"
                "             records\"",
            "CML3111":
                "plot:        y = residual (actual - predicted), MW\n"
                "             x = ACTUAL power output, MW\n"
                "             a clear upward slope, left to right\n"
                "\n"
                "conclusion:  \"the model under-predicts high-output\n"
                "             hours\"",
        },
        "options": [
            ("The slope appears by construction; plot residuals against "
             "the predicted value", True,
             "Correct, and this catches almost everybody once. The actual "
             "value equals the prediction plus the residual, so the residual "
             "is built into the quantity on the horizontal axis and rises "
             "with it. Against the predicted value the slope disappears and "
             "any real pattern becomes visible."),
            ("The conclusion is right, and the model needs an extra feature "
             "to fix it", False,
             "The conclusion may happen to be true and this plot cannot "
             "establish it. Redraw against the predicted value before "
             "changing the model."),
            ("The residuals should have been squared before plotting", False,
             "Squaring throws away the sign, which is the most useful part "
             "of a residual. The pairing of axes is what is wrong here."),
            ("A slope in the residuals always means the model is broken",
             False,
             "A slope against the predicted value would be worth "
             "investigating. A slope against the actual value is arithmetic "
             "rather than a finding."),
        ],
    },
    # ---- 5. judgement: no baseline
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "Your model reaches a mean absolute error of 4.2 MPa. "
                       "The client asks whether that is good. What do you "
                       "need before you can answer?",
            "CML3113": "Your model reaches a mean absolute error of 0.4 "
                       "percentage points of silica. The client asks whether "
                       "that is good. What do you need before you can "
                       "answer?",
            "CML3111": "Your model reaches a root-mean-square error of "
                       "4.1 MW. The client asks whether that is good. What "
                       "do you need before you can answer?",
        },
        "options_by": {
            "CML3112": [
                ("The error of predicting the mean, and the cylinder test's "
                 "own repeatability", True,
                 "Correct. Both comparisons are needed. Predicting the mean "
                 "is the score to beat, and a cylinder test repeats to about "
                 "2 MPa between specimens, so 4.2 MPa is roughly twice as "
                 "uncertain as the measurement it stands in for. That is the "
                 "sentence the client actually needs."),
                ("A second model to compare it against", False,
                 "Two models with no baseline tell you which is better and "
                 "leave you unable to say whether either is worth having."),
                ("A larger dataset", False,
                 "More data may lower the error and does not tell you "
                 "whether the current figure is useful. That judgement needs "
                 "a reference point."),
                ("Nothing further; 4.2 MPa is a small number", False,
                 "Small against what? A number with no reference is not yet "
                 "a result."),
            ],
            "CML3113": [
                ("The error of predicting the mean, and the assay's own "
                 "repeatability", True,
                 "Correct. Both are needed. The assay repeats to about 0.1 "
                 "percentage points, so 0.4 is around four times looser than "
                 "the measurement it replaces, and predicting the mean gives "
                 "you the floor. Those two numbers turn a metric into an "
                 "answer."),
                ("A second model to compare it against", False,
                 "That ranks two options without telling you whether either "
                 "beats doing nothing."),
                ("A larger dataset", False,
                 "More rows might help and cannot answer the question of "
                 "whether 0.4 points is useful to a metallurgist."),
                ("Nothing further; 0.4 percentage points is a small number",
                 False,
                 "Small compared with what? Against a specification of 3 per "
                 "cent it may matter a great deal."),
            ],
            "CML3111": [
                ("The error of predicting the mean, and the published "
                 "figures", True,
                 "Correct. Published work on this dataset reaches roughly 3 "
                 "to 4 MW, so 4.1 MW puts you at the edge of the literature "
                 "rather than adrift. Predicting the mean gives you the "
                 "floor. Together they let you say what the number means."),
                ("A second model to compare it against", False,
                 "That tells you which of two is better and not whether "
                 "either is worth deploying."),
                ("A larger dataset", False,
                 "The dataset is already nearly ten thousand hours. Size is "
                 "not what is missing."),
                ("Nothing further; 4.1 MW is a small number", False,
                 "On a plant output of several hundred megawatts it sounds "
                 "small, and the judgement still needs a stated reference."),
            ],
        },
    },
]

# ==========================================================================
# QUIZ 8 — Week 9. Classification.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[9] = [
    # ---- 1. diagnosis: accuracy under imbalance
    {
        "kind": "diagnosis",
        "stem": ("A teammate is pleased with this result. What has the model "
                 "actually learned?"),
        "pre_by": {
            "CML3112":
                "accuracy                     0.966\n"
                "pours predicted to fail          0\n"
                "\n"
                "# in this register 3.4 in 100 pours fail specification",
            "CML3113":
                "accuracy                     0.966\n"
                "samples predicted as ore         0\n"
                "\n"
                "# in this register 3.4 in 100 samples are above cut-off",
            "CML3111":
                "accuracy                     0.966\n"
                "hours predicted to fail          0\n"
                "\n"
                "# in this log 3.4 in 100 machine-hours end in a failure",
        },
        "options": [
            ("To answer with the majority class every time, which scores the "
             "majority-class share and finds nothing", True,
             "Correct. Since 96.6 in 100 cases are negative, always saying "
             "negative scores 0.966. The model has found the base rate and "
             "no signal. Recall on the class you care about is zero, and "
             "that is the number to report."),
            ("A genuinely strong rule, since 96.6 per cent is a high score",
             False,
             "The score is exactly what you get for free by ignoring the "
             "data. A rule that never fires cannot be strong at the job it "
             "was built for."),
            ("That the two classes are equally easy to separate", False,
             "It never attempted the separation. It predicted one class "
             "throughout."),
            ("That more features are needed to raise accuracy", False,
             "Accuracy is already near its ceiling and is the wrong "
             "instrument. Change the metric before changing the model."),
        ],
    },
    # ---- 2. diagnosis: reading a confusion matrix for the expensive error
    {
        "kind": "diagnosis",
        "stem_by": {
            # A ten-thousand-row register from the industry, deliberately
            # larger than this cohort's 1,030-row teaching file, so nobody
            # tries to reconcile the two.
            "CML3112": "This model was tested against a precast yard's "
                       "quality register of ten thousand pours. Read the "
                       "confusion matrix. Which statement does it support?",
            "CML3113": "This model was tested against a grade-control "
                       "register of ten thousand samples. Read the confusion "
                       "matrix. Which statement does it support?",
            "CML3111": "This model was tested against a maintenance log of "
                       "ten thousand machine-hours. Read the confusion "
                       "matrix. Which statement does it support?",
        },
        "pre_by": {
            "CML3112":
                "                      pred: meets    pred: fails\n"
                "actual: meets                9620             36\n"
                "actual: fails                 310             34\n"
                "\n"
                "10,000 pours in total; accuracy 0.965",
            "CML3113":
                "                      pred: waste    pred: ore\n"
                "actual: waste                9620             36\n"
                "actual: ore                   310             34\n"
                "\n"
                "10,000 samples in total; accuracy 0.965",
            "CML3111":
                "                      pred: runs     pred: fails\n"
                "actual: runs                 9620             36\n"
                "actual: fails                 310             34\n"
                "\n"
                "10,000 machine-hours in total; accuracy 0.965",
        },
        "options": [
            ("It misses about nine in ten of the cases it exists to catch",
             True,
             "Correct. Recall on the class of interest is 34 out of 344, "
             "which is 0.099. The high accuracy comes almost entirely from "
             "the 9,620 easy negatives. This is the number the matrix exists "
             "to expose."),
            ("Its main weakness is false alarms", False,
             "There are only 36 false alarms against 310 misses. The costly "
             "error here is the one being made nearly ten times as often."),
            ("It is well balanced between the two kinds of error", False,
             "310 against 36 is close to a nine-to-one imbalance in the "
             "errors."),
            ("Accuracy of 0.965 shows it is fit for use", False,
             "Predicting the majority class throughout would score 0.966, "
             "which is higher. Accuracy cannot see this failure."),
        ],
    },
    # ---- 3. traceback: binary metric on a multiclass target
    {
        "kind": "traceback",
        "stem": "What does this tell you to change?",
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n"
                "    print(recall_score(y_test, pred))\n"
                "ValueError: Target is multiclass but average='binary'.\n"
                "Please choose another average setting, one of "
                "[None, 'micro', 'macro', 'weighted'].",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n"
                "    print(recall_score(y_test, pred))\n"
                "ValueError: Target is multiclass but average='binary'.\n"
                "Please choose another average setting, one of "
                "[None, 'micro', 'macro', 'weighted'].",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-11-8b9c0d>\", line 1, in <module>\n"
                "    print(recall_score(y_test, pred))\n"
                "ValueError: Target is multiclass but average='binary'.\n"
                "Please choose another average setting, one of "
                "[None, 'micro', 'macro', 'weighted'].",
        },
        "options": [
            ("The target has more than two classes, so you must say how "
             "recall should be combined across them", True,
             "Correct, and the choice matters. average=None gives you recall "
             "per class, which is usually what you want, because a single "
             "combined figure can hide a class the model never predicts."),
            ("The predictions are the wrong data type", False,
             "The types are acceptable. The message is about the number of "
             "classes in the target."),
            ("Recall cannot be computed for more than two classes", False,
             "It can, once you state how to aggregate it. The error offers "
             "you the options."),
            ("The test set is too small for recall to be defined", False,
             "Size is not mentioned and is not the issue. The class count "
             "is."),
        ],
    },
    # ---- 4. interpretation: moving the threshold
    {
        "kind": "interpretation",
        "stem": ("You lower the decision threshold from 0.5 to 0.2 and "
                 "re-score the same model on the same test set. What has "
                 "changed?"),
        "pre_by": {
            "CML3112":
                "threshold 0.5   recall 0.099   false alarms  36\n"
                "threshold 0.2   recall 0.439   false alarms 290",
            "CML3113":
                "threshold 0.5   recall 0.099   false alarms  36\n"
                "threshold 0.2   recall 0.439   false alarms 290",
            "CML3111":
                "threshold 0.5   recall 0.099   false alarms  36\n"
                "threshold 0.2   recall 0.439   false alarms 290",
        },
        "options": [
            ("Nothing about the model; you moved along its trade-off, buying "
             "recall by accepting eight times as many false alarms", True,
             "Correct. The model and its scores are untouched: only the "
             "cut-off you apply to them changed. Which threshold is right "
             "depends on what a false alarm costs against a miss, and that "
             "is a question about the work rather than the model."),
            ("The model has been improved by better tuning", False,
             "No retraining took place. The same probabilities are being cut "
             "in a different place."),
            ("The model now overfits, because recall rose sharply", False,
             "Overfitting is about the gap between training and unseen data. "
             "This is one model on one test set at two thresholds."),
            ("The result is invalid because the threshold should stay at "
             "0.5", False,
             "0.5 is a default rather than a rule. On a problem where a miss "
             "costs far more than a false alarm, moving it is exactly the "
             "right thing to do."),
        ],
    },
    # ---- 5. judgement: which metric, given the cost ratio
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "Accepting a substandard pour means it goes into the "
                       "structure and somebody finds out later. Rejecting a "
                       "sound pour costs one panel and some programme. Which "
                       "metric should govern your model, and why?",
            "CML3113": "Sending ore to the waste dump throws away metal you "
                       "have already paid to mine, and you never find out. "
                       "Sending waste to the mill costs the processing of "
                       "worthless rock. Which metric should govern your "
                       "model, and why?",
            "CML3111": "A false alarm costs a four-hour stop. A missed "
                       "failure costs a gearbox and a week of production. "
                       "Which metric should govern your model, and why?",
        },
        "options": [
            ("Recall on the class you cannot afford to miss, with the "
             "false-alarm rate beside it", True,
             "Correct. The expensive error is the miss, so recall is the "
             "quantity to drive up. Quoting the false-alarm rate beside it "
             "keeps you honest, because recall can always be bought and "
             "somebody has to pay for it."),
            ("Accuracy, because it summarises overall performance", False,
             "At a base rate near 3 per cent, accuracy is dominated by easy "
             "negatives and a useless model scores 0.966. It cannot see the "
             "error that matters here."),
            ("Precision, because false alarms annoy the operators", False,
             "Precision alone rewards a model that fires only when certain, "
             "which is a model that misses most of the cases. It belongs in "
             "the report next to recall rather than in charge of it."),
            ("Whichever metric gives the highest number, so the result reads "
             "well", False,
             "Choosing a metric to flatter the model is how a system that "
             "misses nine failures in ten gets signed off."),
        ],
    },
]

# ==========================================================================
# QUIZ 9 — Week 10. Can I trust this model?
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[10] = [
    # ---- 1. diagnosis: preprocessing fitted before the split
    {
        "kind": "diagnosis",
        "stem": ("This reports a good test score. Why can that score not be "
                 "trusted?"),
        "pre_by": {
            "CML3112":
                "scaler = StandardScaler()\n"
                "X_scaled = scaler.fit_transform(X)     # whole file\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\n"
                "model.fit(X_tr, y_tr)\n"
                "print(model.score(X_te, y_te))",
            "CML3113":
                "scaler = StandardScaler()\n"
                "X_scaled = scaler.fit_transform(X)     # whole file\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\n"
                "model.fit(X_tr, y_tr)\n"
                "print(model.score(X_te, y_te))",
            "CML3111":
                "scaler = StandardScaler()\n"
                "X_scaled = scaler.fit_transform(X)     # whole file\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y)\n"
                "model.fit(X_tr, y_tr)\n"
                "print(model.score(X_te, y_te))",
        },
        "options": [
            ("The scaler was fitted on the whole file, so the test rows "
             "helped set the scaling", True,
             "Correct. The test rows are supposed to stand in for cases you "
             "have never seen, and here they helped set the scaling. Put the "
             "scaler in a Pipeline and fit it after the split, so it only "
             "ever sees training rows."),
            ("StandardScaler is the wrong scaler for this data", False,
             "The choice of scaler is a separate question. Any scaler fitted "
             "before the split leaks in the same way."),
            ("The split should come before the features are selected", False,
             "Selecting which columns to use is fine either side. Measuring "
             "something from the data is what has to wait until after the "
             "split."),
            ("Nothing is wrong; scaling does not use the target", False,
             "Leakage does not require the target. Borrowing the test rows' "
             "mean and spread means the test set is no longer a clean "
             "estimate, and how far the number is distorted is not something "
             "you can work out from the outside, which is the real cost."),
        ],
    },
    # ---- 2. diagnosis: the train and test gap
    {
        "kind": "diagnosis",
        "stem": ("Which of the three error stories does this pattern match?"),
        "pre_by": {
            "CML3112":
                "training score   0.98\n"
                "test score       0.61",
            "CML3113":
                "training score   0.98\n"
                "test score       0.61",
            "CML3111":
                "training score   0.98\n"
                "test score       0.61",
        },
        "options": [
            ("The model has memorised its training rows and does not "
             "generalise", True,
             "Correct. A high training score with a much lower test score is "
             "the signature of a model with too much freedom for the data. "
             "Simplify it, constrain it, or get more rows."),
            ("The model is too simple to capture the pattern", False,
             "A model that is too simple scores poorly on both, because it "
             "cannot even fit the rows it was given. Here it fits them "
             "almost perfectly."),
            ("Information has leaked from the test set into training", False,
             "Leakage usually makes both scores look good, since the model "
             "has effectively seen the answers. A large gap points the other "
             "way."),
            ("The two scores are measuring different quantities", False,
             "Both are the same measure on different rows. That is what "
             "makes the comparison meaningful."),
        ],
    },
    # ---- 3. traceback: NaN reaching the model
    {
        "kind": "traceback",
        "stem": ("A teammate has already tried to deal with the gaps, in the "
                 "cell shown above the traceback. Read both, then say what "
                 "you would change."),
        "pre_by": {
            "CML3112":
                "imp = SimpleImputer(strategy=\"mean\")\n"
                "X[[\"slump\"]] = imp.fit_transform(X[[\"slump\"]])\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y)\n"
                "pipe = Pipeline([(\"model\", Ridge())])\n"
                "pipe.fit(X_tr, y_tr)\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n"
                "    pipe.fit(X_tr, y_tr)\n"
                "ValueError: Input X contains NaN.",
            "CML3113":
                "imp = SimpleImputer(strategy=\"mean\")\n"
                "X[[\"pulp_ph\"]] = imp.fit_transform(X[[\"pulp_ph\"]])\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y)\n"
                "pipe = Pipeline([(\"model\", Ridge())])\n"
                "pipe.fit(X_tr, y_tr)\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n"
                "    pipe.fit(X_tr, y_tr)\n"
                "ValueError: Input X contains NaN.",
            "CML3111":
                "imp = SimpleImputer(strategy=\"mean\")\n"
                "X[[\"RH\"]] = imp.fit_transform(X[[\"RH\"]])\n"
                "\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y)\n"
                "pipe = Pipeline([(\"model\", Ridge())])\n"
                "pipe.fit(X_tr, y_tr)\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-13-1a2b3c>\", line 6, in <module>\n"
                "    pipe.fit(X_tr, y_tr)\n"
                "ValueError: Input X contains NaN.",
        },
        "options": [
            ("Move the imputer inside the Pipeline, and cover every column",
             True,
             "Correct on both counts. Only one column was imputed, so the "
             "gaps in the others are still there, which is why the error "
             "still fires. And fitting it on the whole frame before the "
             "split measures the test rows, which is the leak from question "
             "one wearing different clothes. Inside the pipeline both "
             "problems go away at once."),
            ("Impute the remaining columns the same way, before the split",
             False,
             "That silences the error and keeps the leak. Every value the "
             "imputer learns before the split has been measured partly from "
             "the test rows."),
            ("Drop the rows that still contain gaps", False,
             "It would run, and it discards data and can bias what is left "
             "if the gaps cluster in one source, which Week 4 showed they "
             "often do."),
            ("Replace the remaining gaps with zero so the model can fit",
             False,
             "Zero is a real value on these columns, so this quietly invents "
             "low readings. Week 6 covers the damage that does."),
        ],
    },
    # ---- 4. interpretation: cross-validated score with one odd fold
    {
        "kind": "interpretation",
        "stem": ("You run five-fold cross-validation and get these scores. "
                 "What should you report, and what should you look at?"),
        "pre_by": {
            "CML3112":
                "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\n"
                "mean 0.67",
            "CML3113":
                "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\n"
                "mean 0.67",
            "CML3111":
                "fold scores: 0.71, 0.68, 0.74, 0.52, 0.70\n"
                "mean 0.67",
        },
        "options": [
            ("The mean with its spread, and look into the 0.52 fold", True,
             "Correct. Four folds sit close together and one sits well "
             "below, which suggests that fold contains something the others "
             "do not. Group structure in the rows is the usual explanation, "
             "and it is the subject of the next question."),
            ("The mean alone, since averaging is the purpose of "
             "cross-validation", False,
             "A bare mean hides the thing worth knowing. Reporting 0.67 with "
             "no spread conceals a fold that scored 0.52 and the reason "
             "behind it."),
            ("The best fold, since it shows what the model can achieve",
             False,
             "Quoting the best fold is selecting the most flattering result "
             "from your own experiment."),
            ("Nothing yet; five folds is too few to report", False,
             "Five folds is a standard choice and perfectly reportable. The "
             "spread is part of the report rather than a reason to withhold "
             "it."),
        ],
    },
    # ---- 5. judgement: group structure in the split
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "You discover that several specimens from the same "
                       "mix batch are split across your training and test "
                       "sets. Specimens from one batch are near-copies of "
                       "each other. What should you do?",
            "CML3113": "Working with the well-log dataset, you discover that "
                       "samples from the same drill hole are split across "
                       "your training and test sets. Samples from one hole "
                       "are far more alike than samples from different "
                       "holes. What should you do?",
            "CML3111": "You discover that consecutive hours are split at "
                       "random across your training and test sets, and that "
                       "one hour is almost the same reading as the hour "
                       "before it. What should you do?",
        },
        "options_by": {
            "CML3112": [
                ("Split by batch, so every specimen from one batch sits "
                 "entirely in training or entirely in test", True,
                 "Correct. Otherwise the model can recognise a batch it has "
                 "already been trained on, and your test score measures "
                 "recall of batches rather than prediction of strength. "
                 "GroupShuffleSplit and GroupKFold exist for this."),
                ("Leave it, because a random split is unbiased by "
                 "definition", False,
                 "Random assignment of rows is unbiased about rows and blind "
                 "to the fact that these rows come in near-identical "
                 "families."),
                ("Remove the duplicate-looking specimens", False,
                 "They are genuine separate tests rather than duplicates, "
                 "and discarding them throws away real information about "
                 "within-batch variation."),
                ("Increase the size of the test set", False,
                 "A larger test set built the same way carries the same "
                 "flaw at greater scale."),
            ],
            "CML3113": [
                ("Split by hole, so every sample from one hole sits entirely "
                 "in training or entirely in test", True,
                 "Correct. A random split lets the model learn a hole and "
                 "then be tested on the same hole, which flatters it badly. "
                 "The question you actually face is prediction in a hole you "
                 "have not drilled."),
                ("Leave it, because a random split is unbiased by "
                 "definition", False,
                 "It is unbiased with respect to rows and takes no account "
                 "of the strong similarity within a hole."),
                ("Remove the samples that look most similar", False,
                 "Those samples are real observations, and downhole "
                 "similarity is a property of the ore body rather than an "
                 "error."),
                ("Increase the size of the test set", False,
                 "The same flaw simply appears in a bigger test set."),
            ],
            "CML3111": [
                ("Split on time: train on an earlier stretch, test on a "
                 "later one", True,
                 "Correct. The structure here is time, so the split has to "
                 "respect time. A random split puts the hour before and the "
                 "hour after into training while testing on the hour "
                 "between, which is close to handing over the answer. It "
                 "also matches the real task, which is predicting forward "
                 "rather than filling in gaps. TimeSeriesSplit does this."),
                ("Leave it, because a random split is unbiased by "
                 "definition", False,
                 "Random over rows takes no account of the fact that "
                 "consecutive hours are nearly the same reading. Unbiased "
                 "selection of rows is not the same as an honest test."),
                ("Remove the near-identical consecutive rows", False,
                 "They are genuine samples of a continuing state, and "
                 "thinning them changes what the model sees without fixing "
                 "the fact that neighbouring hours straddle the split."),
                ("Increase the size of the test set", False,
                 "A bigger test set assembled the same way is optimistic in "
                 "the same way."),
            ],
        },
    },
]

# ==========================================================================
# QUIZ 10 — Week 11. Features.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# ==========================================================================
BANKS[11] = [
    # ---- 1. diagnosis: scaling in front of a tree changes nothing
    {
        "kind": "diagnosis",
        "stem": ("A teammate adds a scaler expecting an improvement and the "
                 "score does not budge. Why not?"),
        "pre_by": {
            # random_state is shown, otherwise two fits of an unseeded tree
            # would not be expected to agree to the last digit anyway.
            "CML3112":
                "before:  DecisionTreeRegressor(random_state=0)\n"
                "                                                MAE 5.1\n"
                "after:   Pipeline([(\"scale\", StandardScaler()),\n"
                "                   (\"model\", DecisionTreeRegressor(\n"
                "                                 random_state=0))])\n"
                "                                                MAE 5.1",
            "CML3113":
                "before:  DecisionTreeRegressor(random_state=0)\n"
                "                                               MAE 0.42\n"
                "after:   Pipeline([(\"scale\", StandardScaler()),\n"
                "                   (\"model\", DecisionTreeRegressor(\n"
                "                                 random_state=0))])\n"
                "                                               MAE 0.42",
            "CML3111":
                "before:  DecisionTreeClassifier(random_state=0)\n"
                "                                             recall 0.61\n"
                "after:   Pipeline([(\"scale\", StandardScaler()),\n"
                "                   (\"model\", DecisionTreeClassifier(\n"
                "                                 random_state=0))])\n"
                "                                             recall 0.61",
        },
        "options": [
            ("A tree splits on the order of the values, and scaling "
             "preserves that order", True,
             "Correct. Rescaling moves the numbers and leaves their ranking "
             "untouched, and a threshold split only cares about ranking. "
             "Scaling earns its keep for models that measure distances or "
             "fit coefficients."),
            ("The scaler was placed after the model in the pipeline", False,
             "It is first, which is the correct position. The order in the "
             "pipeline is not the issue."),
            ("The features were already on the same scale", False,
             "Even if they were, that would not be the reason. A tree is "
             "unaffected by this kind of rescaling whatever the starting "
             "scales happen to be."),
            ("The tree needs a greater depth before scaling helps", False,
             "Depth changes how the tree fits and never makes it sensitive "
             "to a monotonic rescaling."),
        ],
    },
    # ---- 2. diagnosis: one-hot encoding a high-cardinality identifier
    {
        "kind": "diagnosis",
        "stem": ("The score on your own test split improves after this "
                 "change, and the model is worse. What has happened?"),
        "pre_by": {
            # get_dummies drops the source column and adds one per distinct
            # value, so the width is (original - 1 + nunique). Every number
            # below is that arithmetic against the real dataset shape.
            "CML3112":
                "print(df.shape)\n"
                "(1030, 10)\n"
                "\n"
                "print(df[\"batch_id\"].nunique())\n"
                "240\n"
                "\n"
                "X = pd.get_dummies(df, columns=[\"batch_id\"])\n"
                "print(X.shape)\n"
                "(1030, 249)",
            "CML3113":
                "print(df.shape)\n"
                "(20000, 24)\n"
                "\n"
                "print(df[\"assay_batch_id\"].nunique())\n"
                "847\n"
                "\n"
                "X = pd.get_dummies(df, columns=[\"assay_batch_id\"])\n"
                "print(X.shape)\n"
                "(20000, 870)",
            "CML3111":
                "print(df.shape)\n"
                "(10000, 14)\n"
                "\n"
                "print(df[\"product_id\"].nunique())\n"
                "847\n"
                "\n"
                "X = pd.get_dummies(df, columns=[\"product_id\"])\n"
                "print(X.shape)\n"
                "(10000, 860)",
        },
        "options": [
            ("It added one column per identifier, so the model can now "
             "recognise individual units", True,
             "Correct. An identifier expanded this way hands the model a "
             "lookup table for the units in your file. It scores well "
             "wherever the same units appear on both sides of the split and "
             "carries nothing to a new one. Drop the identifier and keep the "
             "columns that describe the thing."),
            ("It made the frame too wide for the model to fit", False,
             "A few hundred columns is unremarkable and fits without "
             "complaint. The problem is what those columns mean."),
            ("get_dummies should have been given the whole frame", False,
             "It was given the whole frame with one column named for "
             "expansion, which is the normal usage. The choice of column is "
             "the fault."),
            ("The identifiers should have been numbered 1 to 847 instead",
             False,
             "That is worse: it tells a straight-line model that unit 800 "
             "is a hundred times unit 8. Neither encoding rescues a column "
             "that is only a label."),
        ],
    },
    # ---- 3. traceback: unseen category at prediction time
    {
        "kind": "traceback",
        "stem": ("What has happened, and what is the catch in the obvious "
                 "fix?"),
        "pre_by": {
            "CML3112":
                "enc = OneHotEncoder(drop=\"first\")\n"
                "# ... fitted on exposure_class values XC1, XC3, XD2, XS1\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n"
                "    pipe.predict(new_rows)\n"
                "ValueError: Found unknown categories ['XS3'] in column 0\n"
                "during transform",
            "CML3113":
                "enc = OneHotEncoder(drop=\"first\")\n"
                "# ... fitted on ore_source values pit 1, pit 3,\n"
                "#     stockpile, blend\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n"
                "    pipe.predict(new_rows)\n"
                "ValueError: Found unknown categories ['pit 7'] in column 0\n"
                "during transform",
            "CML3111":
                "enc = OneHotEncoder(drop=\"first\")\n"
                "# ... fitted on product_type values L, M, H\n"
                "\n"
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-15-6d7e8f>\", line 1, in <module>\n"
                "    pipe.predict(new_rows)\n"
                "ValueError: Found unknown categories ['X'] in column 0\n"
                "during transform",
        },
        "options": [
            ("handle_unknown=\"ignore\" clears it, and with drop=\"first\" "
             "an unseen category then encodes as the dropped one", True,
             "Correct, and the second half is the part almost nobody is "
             "told. An ignored unknown category is encoded as all zeros, "
             "which is exactly how the dropped reference category is "
             "encoded, so every new category silently becomes the baseline. "
             "Choose one of the two options deliberately and count how often "
             "an unknown value arrives."),
            ("Adding handle_unknown=\"ignore\" solves it cleanly, with no "
             "side effect worth worrying about", False,
             "It does clear the error. The side effect is that the unknown "
             "category is encoded as all zeros, and because drop=\"first\" "
             "is set, that is the same encoding as the dropped category."),
            ("Refitting the encoder on the new rows as well will fix it "
             "properly", False,
             "Fitting anything on rows you are about to predict is the "
             "leakage pattern from Week 10. It also cannot work in service, "
             "where the new value arrives after the model is deployed."),
            ("The category column should be dropped from the model", False,
             "It may be carrying real signal. The task is to encode it so it "
             "survives a value you have not seen before."),
        ],
    },
    # ---- 4. interpretation: reading an ablation table
    {
        "kind": "interpretation",
        "stem": ("Each row removes one feature and refits. Which feature has "
                 "earned its place least?"),
        "pre_by": {
            "CML3112":
                "features                        MAE (MPa)\n"
                "all five                              3.9\n"
                "minus water/cement ratio              6.8\n"
                "minus curing age                      7.4\n"
                "minus total binder                    4.0\n"
                "minus superplasticiser                4.1\n"
                "minus fly ash                         4.6",
            "CML3113":
                "features                    MAE (pts silica)\n"
                "all five                                0.31\n"
                "minus starch dose per tonne             0.68\n"
                "minus iron feed grade                   0.74\n"
                "minus amina-to-starch ratio             0.32\n"
                "minus air flow                         0.39\n"
                "minus pulp density                     0.44",
            "CML3111":
                "features                   recall (failures)\n"
                "all five                                0.78\n"
                "minus mechanical power                  0.51\n"
                "minus temperature rise                  0.46\n"
                "minus tool wear                         0.77\n"
                "minus rotational speed                  0.72\n"
                "minus torque                            0.68",
        },
        "options_by": {
            "CML3112": [
                ("Total binder, because removing it moves the error by "
                 "0.1 MPa", True,
                 "Correct. Curing age and the water/cement ratio each cost "
                 "you around 3 MPa when removed, and total binder costs "
                 "0.1 MPa. It is very likely saying the same thing as the "
                 "cement column already in the model."),
                ("Curing age, because it has the largest error when removed",
                 False,
                 "That reading is inverted. A large error without a feature "
                 "means the model badly needs it."),
                ("Water/cement ratio, because 6.8 is a poor result", False,
                 "6.8 is the error you suffer without it, which is why it "
                 "belongs in the model."),
                ("None of them; every feature earns its place", False,
                 "A feature whose removal changes the error by 0.1 MPa is "
                 "carrying almost nothing the others do not already carry."),
            ],
            "CML3113": [
                ("The amina-to-starch ratio, because removing it moves the "
                 "error by 0.01 percentage points", True,
                 "Correct. Iron feed grade and starch dose each cost you "
                 "around 0.4 points when removed, and this one costs 0.01. "
                 "It is close to redundant given the dose feature."),
                ("Iron feed grade, because it has the largest error when "
                 "removed", False,
                 "That is the reading reversed. The largest degradation "
                 "marks the most valuable feature."),
                ("Starch dose per tonne, because 0.68 is a poor result",
                 False,
                 "0.68 is the error without it. That is the case for keeping "
                 "it."),
                ("None of them; every feature earns its place", False,
                 "A change of 0.01 percentage points is well inside the "
                 "noise you would see between folds."),
            ],
            "CML3111": [
                ("Tool wear, because removing it moves recall by one "
                 "percentage point", True,
                 "Correct. Mechanical power and temperature rise each cost "
                 "you around 30 points of recall when removed, and tool wear "
                 "costs one. On this evidence it is nearly redundant."),
                ("Temperature rise, because it has the lowest recall when "
                 "removed", False,
                 "Lowest recall without a feature means the model depends on "
                 "it most. The reading is inverted."),
                ("Mechanical power, because 0.51 is a poor result", False,
                 "0.51 is the recall you are left with when it is gone, "
                 "which is the argument for keeping it."),
                ("None of them; every feature earns its place", False,
                 "One point of recall is within the fold-to-fold spread you "
                 "would expect."),
            ],
        },
    },
    # ---- 5. judgement: engineered feature against raw columns
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "Two teams reach almost the same error. One uses a "
                       "random forest on the raw columns; the other uses "
                       "linear regression on the water/cement ratio and four "
                       "other engineered features. Every rejection has to be "
                       "explained in writing to a paying client. Which do "
                       "you recommend?",
            "CML3113": "Two teams reach almost the same error. One uses a "
                       "random forest on the raw columns; the other uses "
                       "linear regression on reagent dose per tonne and four "
                       "other engineered features. The operator has to see "
                       "which reading drove the call. Which do you "
                       "recommend?",
            "CML3111": "Two teams reach almost the same recall. One uses a "
                       "random forest on the raw columns; the other uses "
                       "logistic regression on mechanical power and four "
                       "other engineered features. The maintenance planner "
                       "has to justify every four-hour stop. Which do you "
                       "recommend?",
        },
        "options": [
            ("The engineered features with the simpler model, whose "
             "reasoning can be read off and defended", True,
             "Correct. On equal performance the stated constraint decides "
             "it, and a coefficient on a quantity with physical meaning is "
             "something you can put in front of the person who has to sign. "
             "The engineering went into the features rather than the "
             "algorithm."),
            ("The random forest, because ensembles generalise better in "
             "general", False,
             "It may well generalise better on some problems, and here the "
             "two are level while only one of them satisfies the constraint "
             "you were given."),
            ("Either, since the error is what matters", False,
             "The error was stated as a condition to meet rather than the "
             "only criterion. Explainability was given as a requirement."),
            ("The random forest, and add an importance chart to explain it",
             False,
             "Feature importance tells you which columns the model leaned on "
             "overall. It does not tell the client why this particular case "
             "was rejected, which is the question they will ask."),
        ],
    },
]

# ==========================================================================
# QUIZ 11 — Week 12. Model comparison. Integrative.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# Two of the five deliberately revisit Weeks 1-10.
# ==========================================================================
BANKS[12] = [
    # ---- 1. diagnosis: a difference inside the noise
    {
        "kind": "diagnosis",
        "stem": ("A teammate concludes the forest is the better model. What "
                 "does this table actually support?"),
        "pre_by": {
            # Per-fold figures, so the paired differences can be read off
            # rather than inferred from a summary spread. The forest wins
            # three folds, loses two, and the differences change sign.
            "CML3112":
                "fold                  1      2      3      4      5   mean\n"
                "random forest      0.78   0.70   0.76   0.71   0.75   0.74\n"
                "logistic reg.      0.75   0.73   0.72   0.68   0.72   0.72\n"
                "difference        +0.03  -0.03  +0.04  +0.03  +0.03",
            "CML3113":
                "fold                  1      2      3      4      5   mean\n"
                "random forest      0.28   0.36   0.29   0.34   0.28   0.31\n"
                "linear reg.        0.31   0.33   0.36   0.32   0.33   0.33\n"
                "difference        -0.03  +0.03  -0.07  +0.02  -0.05",
            "CML3111":
                "fold                  1      2      3      4      5   mean\n"
                "random forest      0.78   0.70   0.76   0.71   0.75   0.74\n"
                "logistic reg.      0.75   0.73   0.72   0.68   0.72   0.72\n"
                "difference        +0.03  -0.03  +0.04  +0.03  +0.03",
        },
        "options": [
            ("Very little: the difference changes sign between folds, so on "
             "this evidence the two cannot be separated", True,
             "Correct, and reading the per-fold differences is what settles "
             "it. The sign of the difference flips from fold to fold, so the "
             "mean gap of 0.02 is not a consistent advantage. Report them as "
             "level on this data and let the stated constraints decide. Note "
             "what makes this readable at all: both models were scored on "
             "the SAME five folds, so the differences can be paired up."),
            ("The forest is better, since it has the stronger mean", False,
             "A mean hides the fold-by-fold picture. Here the sign of the "
             "difference flips, which is the pattern of two models that are "
             "level rather than one that is ahead."),
            ("The forest is better, because it wins the majority of folds",
             False,
             "Winning more folds than it loses is worth noticing and is weak "
             "evidence at this margin, because the fold it loses it loses by "
             "as much as the others are won. With only five folds this "
             "pattern arises easily between two models of equal ability."),
            ("The comparison is invalid because the models share folds",
             False,
             "Sharing folds is what makes the comparison valid. Scoring each "
             "model on its own random split is the mistake, and it is the "
             "subject of the next question."),
        ],
    },
    # ---- 2. diagnosis: models compared on different splits
    {
        "kind": "diagnosis",
        "stem": ("Two models, two scores, no error anywhere. Why can these "
                 "numbers not be compared?"),
        "pre_by": {
            "CML3112":
                "# model A\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=1)\n"
                "# ... fit A ...      score 0.78\n"
                "\n"
                "# model B\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=7)\n"
                "# ... fit B ...      score 0.81",
            "CML3113":
                "# model A\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=1)\n"
                "# ... fit A ...      score 0.78\n"
                "\n"
                "# model B\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=7)\n"
                "# ... fit B ...      score 0.81",
            "CML3111":
                "# model A\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=1)\n"
                "# ... fit A ...      score 0.78\n"
                "\n"
                "# model B\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y,\n"
                "                              random_state=7)\n"
                "# ... fit B ...      score 0.81",
        },
        "options": [
            ("They were scored on different test sets, so the gap may be "
             "the split rather than the model", True,
             "Correct. Changing the seed changes the split, and split-to-"
             "split variation on this kind of data is often larger than the "
             "gap you are trying to measure. Score every model on identical "
             "folds, which is what cross_val_score with a fixed splitter "
             "gives you."),
            ("Model B had the advantage of a later random state", False,
             "The number in random_state is a label for a shuffle and "
             "carries no ordering. Seed 7 is not later or better than "
             "seed 1."),
            ("The scores need to be averaged together", False,
             "Averaging two figures measured on different test sets produces "
             "a number that describes neither model."),
            ("Nothing is wrong, since both used the same data file", False,
             "The same file cut two different ways gives two different test "
             "sets. The comparison needs the cuts to match."),
        ],
    },
    # ---- 3. traceback: predict before fit
    {
        "kind": "traceback",
        "stem": ("You have run this notebook for an hour and now get this. "
                 "What is the most likely history behind it?"),
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n"
                "    print(forest.predict(X_te)[:5])\n"
                "NotFittedError: This RandomForestClassifier instance is not\n"
                "fitted yet. Call 'fit' with appropriate arguments before\n"
                "using this estimator.",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n"
                "    print(forest.predict(X_te)[:5])\n"
                "NotFittedError: This RandomForestRegressor instance is not\n"
                "fitted yet. Call 'fit' with appropriate arguments before\n"
                "using this estimator.",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-31-9a8b7c>\", line 1, in <module>\n"
                "    print(forest.predict(X_te)[:5])\n"
                "NotFittedError: This RandomForestClassifier instance is not\n"
                "fitted yet. Call 'fit' with appropriate arguments before\n"
                "using this estimator.",
        },
        "options": [
            ("The cell that creates the model was re-run after the one that "
             "fitted it", True,
             "Correct, and this is the Week 2 out-of-order trap arriving in "
             "a much more expensive place. Re-running the constructor throws "
             "away an hour of fitting. Restart and Run All is how you find "
             "out whether your notebook still tells a straight story."),
            ("The model does not support predict on a test set", False,
             "It does. The message is specifically that this instance has "
             "never been fitted."),
            ("The test features contain missing values", False,
             "That reports itself as an error about NaN, and it would only "
             "arise once the model was fitted."),
            ("The forest needs more trees before it can predict", False,
             "The number of trees is set at construction and any number can "
             "be fitted and used. This one was never fitted."),
        ],
    },
    # ---- 4. interpretation: a global chart cannot answer a per-case question
    {
        "kind": "interpretation",
        "stem_by": {
            "CML3112": "Two outputs from the same forest. The quality "
                       "manager needs to know why THIS batch was rejected. "
                       "Which output answers that, and what does the other "
                       "one tell you?",
            "CML3113": "Two outputs from the same forest. The operator needs "
                       "to know which reading drove THIS call. Which output "
                       "answers that, and what does the other one tell you?",
            "CML3111": "Two outputs from the same forest. The planner needs "
                       "to know why THIS machine was flagged today. Which "
                       "output answers that, and what does the other one "
                       "tell you?",
        },
        "pre_by": {
            "CML3112":
                "A   feature_importances_ over the whole training set\n"
                "      w_c ratio        0.41\n"
                "      curing age       0.29\n"
                "      total binder     0.18\n"
                "      superplasticiser 0.12\n"
                "\n"
                "B   contribution to the prediction for batch 812\n"
                "      w_c ratio 0.61   pushed toward reject  +0.22\n"
                "      curing age 3 d   pushed toward reject  +0.15\n"
                "      total binder     pushed toward accept  -0.04",
            "CML3113":
                "A   feature_importances_ over the whole training set\n"
                "      starch dose      0.41\n"
                "      iron feed grade  0.29\n"
                "      pulp pH          0.18\n"
                "      air flow         0.12\n"
                "\n"
                "B   contribution to the prediction for record 14:20\n"
                "      starch dose low  pushed silica up      +0.22\n"
                "      iron feed 52 %   pushed silica up      +0.15\n"
                "      pulp pH 9.4      pushed silica down    -0.04",
            "CML3111":
                "A   feature_importances_ over the whole training set\n"
                "      mechanical power 0.41\n"
                "      temp rise        0.29\n"
                "      tool wear        0.18\n"
                "      rot speed        0.12\n"
                "\n"
                "B   contribution to the prediction for machine 14\n"
                "      temp rise 96 K   pushed toward fail    +0.22\n"
                "      power 4.8 kW     pushed toward fail    +0.15\n"
                "      tool wear 40 min pushed toward normal  -0.04",
        },
        "options": [
            ("B answers it, because it is specific to this case; A describes "
             "the model's average behaviour across all cases", True,
             "Correct, and the distinction is worth holding on to. A global "
             "importance chart says what the model relies on in general and "
             "can never say why one case came out as it did. A per-case "
             "breakdown is what a client's question actually needs."),
            ("A answers it, because the highest-importance feature is the "
             "reason for any given decision", False,
             "That does not follow. The most important feature overall can "
             "be unremarkable in this particular case, and here B shows a "
             "different feature leading for batch-level reasons."),
            ("Both answer it equally well, since they rank the same "
             "features", False,
             "They do not even rank them the same way, and more importantly "
             "they answer different questions. One is about the model, the "
             "other about a case."),
            ("Neither answers it, because a forest can never be explained "
             "at all", False,
             "Too pessimistic. Per-case attributions like B are exactly how "
             "you interrogate one prediction from an ensemble. The honest "
             "caveat is that they are estimates of the contribution rather "
             "than a rule you can read off."),
        ],
    },
    # ---- 5. judgement: answering the client's question
    {
        "kind": "judgement",
        "stem_by": {
            "CML3112": "The quality manager points at one batch and asks: "
                       "read me the reason your model rejected batch 812. "
                       "You chose the forest. What is the honest position?",
            "CML3113": "The metallurgist asks: your model says lower the "
                       "amina flow, by how much, and where does that number "
                       "come from? You chose the forest. What is the honest "
                       "position?",
            "CML3111": "The planner asks: your model called a stop on "
                       "machine 14 this morning, why that machine and why "
                       "today? You chose the forest. What is the honest "
                       "position?",
        },
        "options": [
            ("Say plainly that this model cannot give a per-case reason, and "
             "that the constraint therefore rules it out despite the score",
             True,
             "Correct. The professional answer is to name the limitation and "
             "change the recommendation. A stated condition of acceptance "
             "that your chosen model cannot meet is a reason to change the "
             "model rather than to talk around it."),
            ("Show the feature importance chart as the explanation", False,
             "Importance describes the model's behaviour across the whole "
             "dataset. It cannot say why one case was decided as it was, "
             "which is the question you were asked."),
            ("Explain that the model is accurate and ask them to trust the "
             "result", False,
             "They told you at the outset that they cannot act on an "
             "unexplained call. Asking for trust instead is not an answer."),
            ("Offer to retrain the forest with fewer trees so it is simpler",
             False,
             "A smaller forest is still an ensemble of trees and remains "
             "unreadable case by case. This concedes accuracy without "
             "gaining explainability."),
        ],
    },
]

# ==========================================================================
# QUIZ 12 — Week 13. Reproducibility. Integrative.
# Mix: 2 diagnosis, 1 traceback, 1 interpretation, 1 judgement.
# Two of the five deliberately revisit earlier weeks.
# ==========================================================================
BANKS[13] = [
    # ---- 1. diagnosis: a path that exists on one machine
    {
        "kind": "diagnosis",
        "stem": ("This runs perfectly on the machine it was written on. What "
                 "is wrong with it?"),
        "pre_by": {
            "CML3112":
                "df = pd.read_csv(\n"
                "    \"C:/Users/Jotham/Desktop/concrete_final_v3.csv\")",
            "CML3113":
                "df = pd.read_csv(\n"
                "    \"C:/Users/Jotham/Desktop/flotation_final_v3.csv\")",
            "CML3111":
                "df = pd.read_csv(\n"
                "    \"C:/Users/Jotham/Desktop/motor_log_FINAL.csv\")",
        },
        "options": [
            ("It names a location that exists on exactly one computer, so "
             "the notebook cannot run anywhere else", True,
             "Correct. Keep the data inside the project and read it by a "
             "relative path such as data/… so the notebook works for anyone "
             "who has the folder. The version marker in the file name is a "
             "second warning: it suggests there are other copies and no "
             "record of which is current."),
            ("The file should be read with a different pandas function",
             False,
             "read_csv is the right function for a CSV. The path is the "
             "problem."),
            ("Backslashes should have been used for a Windows path", False,
             "Forward slashes work on Windows in Python and avoid the escape "
             "problems backslashes cause. This is the better of the two "
             "styles and the location is still wrong."),
            ("Nothing, as long as you send the file with the notebook",
             False,
             "The recipient would have to recreate your user name and your "
             "desktop for the path to resolve. A relative path inside the "
             "project removes the problem entirely."),
        ],
    },
    # ---- 2. diagnosis: an unseeded result that moves
    {
        "kind": "diagnosis",
        "stem": ("You run the same notebook twice, changing nothing, and get "
                 "these two numbers. What is going on, and what should you "
                 "do?"),
        "pre_by": {
            "CML3112":
                "run 1:   MAE 4.1 MPa\n"
                "run 2:   MAE 4.6 MPa",
            "CML3113":
                "run 1:   MAE 0.31 pts\n"
                "run 2:   MAE 0.36 pts",
            "CML3111":
                "run 1:   recall 0.74\n"
                "run 2:   recall 0.69",
        },
        "options": [
            ("The split and the model involve randomness that was never "
             "pinned down", True,
             "Correct. Without a seed, the rows that land in the test set "
             "and the internal choices a forest makes change every run. Set "
             "random_state on the split and on the model, and write the "
             "number in the notebook so a reader can reproduce your figure "
             "exactly."),
            ("The data file is being modified between runs", False,
             "Nothing here writes to the file. Unseeded randomness explains "
             "this without needing the data to change."),
            ("The second run is the more trustworthy of the two", False,
             "Neither is more trustworthy. That two runs differ by this much "
             "is itself the finding, and it says your single reported figure "
             "carries this much uncertainty."),
            ("Report the average of the two runs", False,
             "An average of two arbitrary draws is still arbitrary. Seed the "
             "randomness, and if you want a figure with a spread, "
             "cross-validate deliberately."),
        ],
    },
    # ---- 3. traceback: the file is not where the notebook expects
    {
        "kind": "traceback",
        "stem": ("A classmate clones your repository and gets this on the "
                 "first cell. What is the cause?"),
        "pre_by": {
            "CML3112":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n"
                "    df = pd.read_csv(\"concrete_strength.csv\")\n"
                "FileNotFoundError: [Errno 2] No such file or directory:\n"
                "'concrete_strength.csv'",
            "CML3113":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n"
                "    df = pd.read_csv(\"flotation_subset.csv\")\n"
                "FileNotFoundError: [Errno 2] No such file or directory:\n"
                "'flotation_subset.csv'",
            "CML3111":
                "Traceback (most recent call last):\n"
                "  File \"<ipython-input-1-3e4f5a>\", line 1, in <module>\n"
                "    df = pd.read_csv(\"ai4i2020.csv\")\n"
                "FileNotFoundError: [Errno 2] No such file or directory:\n"
                "'ai4i2020.csv'",
        },
        "options": [
            ("The data file was never committed, or sits elsewhere", True,
             "Correct, and both halves are worth checking. Data is often "
             "left out of a repository deliberately because of size or "
             "licence, in which case the README has to say where to get it "
             "and where to put it. Otherwise the path needs to match the "
             "folder layout."),
            ("The classmate is missing a package", False,
             "A missing package reports itself as ModuleNotFoundError. This "
             "message is about a file."),
            ("The file name has the wrong extension", False,
             "The extension matches a CSV read. The file is simply not at "
             "that location."),
            ("The repository was cloned incorrectly", False,
             "A clone that failed would leave you with no notebook to run. "
             "The notebook arrived and its data did not."),
        ],
    },
    # ---- 4. interpretation: which figure caption does its job
    {
        "kind": "interpretation",
        "stem": ("Two captions for the same chart. Which one does the job a "
                 "caption exists to do, and why?"),
        "pre_by": {
            "CML3112":
                "A:  Figure 3: strength against cement content.\n"
                "\n"
                "B:  Figure 3: strength rises with cement content and\n"
                "    flattens above 400 kg/m3, so going from 450 to\n"
                "    500 kg/m3 buys about 1 MPa.",
            "CML3113":
                "A:  Figure 3: silica against starch flow.\n"
                "\n"
                "B:  Figure 3: concentrate silica falls as starch dose\n"
                "    rises to about 900 g per tonne of feed and flattens\n"
                "    after that.",
            "CML3111":
                "A:  Figure 3: failures against tool wear.\n"
                "\n"
                "B:  Figure 3: the failure rate rises sharply above 200\n"
                "    minutes of tool wear, from 2 per cent to 11 per cent.",
        },
        "options": [
            ("B, because it states the finding and its size, so a reader who "
             "only reads the captions still learns the result", True,
             "Correct. A caption is often the only part of your work that "
             "gets read. B carries the conclusion and the magnitude, which "
             "is what makes it useful and also what makes it checkable "
             "against the chart."),
            ("A, because a caption should describe the chart and let the "
             "reader draw the conclusion", False,
             "A describes the axes, which the axis labels already do. It "
             "leaves the reader to rediscover something you already know."),
            ("A, because B might be wrong and the caption would then be "
             "misleading", False,
             "A claim you can check is a feature. If B is wrong the chart "
             "will show it, whereas A cannot be wrong because it says "
             "nothing."),
            ("Neither; captions should give the data source instead", False,
             "The source belongs in the caption or nearby and does not "
             "replace the finding. B plus a source is the target."),
        ],
    },
    # ---- 5. judgement: three cells that all assign df
    {
        "kind": "judgement",
        "stem": ("Your notebook has three separate cells that each assign "
                 "df, and nobody wrote down the order they should run in. "
                 "Submission is tomorrow. What do you do?"),
        "options": [
            ("Restart and Run All, then fix whatever breaks until it runs "
             "clean from top to bottom", True,
             "Correct, and do it before you are tired. That single action "
             "converts a notebook that works on your screen into one that "
             "works from an empty memory, which is the only version anyone "
             "else can use. Consolidating the three assignments into one "
             "clear sequence is usually the fix."),
            ("Add a comment above each cell saying what order to run them "
             "in", False,
             "Instructions to run cells out of order are a description of "
             "the problem. Anyone who follows them slightly differently gets "
             "a different answer."),
            ("Leave it, since you know the right order", False,
             "That knowledge is not in the file, so it does not survive you. "
             "It also will not survive next week for you either."),
            ("Delete two of the three cells and hope the notebook still "
             "runs", False,
             "Each of them may be doing something needed. Running from a "
             "clean state tells you what is required rather than leaving you "
             "to guess."),
        ],
    },
]

