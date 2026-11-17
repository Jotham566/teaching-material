# -*- coding: utf-8 -*-
"""Single source of truth for the S.5 / S.6 Machine Learning Track.

Eight weeks of the December holiday, three sessions a week, three hours a
session. The syllabus document, the roadmap figure and the verifier are all
generated from this file.

WHO THIS IS FOR
---------------
Senior 5 and Senior 6 students whose computing background is Subsidiary ICT:
Word, Excel and a browser. Nobody has programmed. They own the laptops they
bring, which are a mix of Windows and Mac of unknown age.

WHAT THEY ALREADY HAVE, AND IT IS MORE THAN THEY THINK
------------------------------------------------------
A-level mathematics gives them the mean, the median, standard deviation,
correlation, the line of best fit, probability, gradients and, for the
Principal Maths students, differentiation. Every one of those is used in this
track, and the syllabus says where. That is the single most useful thing to
tell a sixteen-year-old who thinks machine learning is out of reach.

FOUR PROMISES, BECAUSE ALL FOUR WERE ASKED FOR
----------------------------------------------
A finished project they can explain. A head start on A-level and first-year
university. A certificate with real marks. A public portfolio they can show
an admissions officer or an employer. Each one is costed into the timetable
below rather than added to the brochure.
"""

TRACK = "Machine Learning Track"
FOR_WHOM = "Senior 5 and Senior 6"
WHEN = "December holiday"
SUBTITLE = "Eight weeks - twenty-four sessions - seventy-two hours"

# ---------------------------------------------------------------- shape
WEEKS = 8
SESSIONS_PER_WEEK = 3
HOURS_PER_SESSION = 3
SESSIONS = WEEKS * SESSIONS_PER_WEEK          # 24
TOTAL_HOURS = SESSIONS * HOURS_PER_SESSION    # 72

# The three-hour session. Teenagers, and a holiday: the teaching blocks are
# shorter than an adult course would use and there is more time at the
# keyboard. Nothing is a lecture for longer than twenty-five minutes.
BLOCK = [
    (15, "Warm-up",
     "A short puzzle on the screen as they arrive, and last session's "
     "homework answered. Starts on time even if the room does not."),
    (25, "Teach one idea",
     "One idea, typed live on the projector while they follow on their own "
     "machines. Twenty-five minutes is the ceiling."),
    (35, "Do it yourself",
     "They build the same thing without being led, working in pairs. The "
     "instructor circulates rather than presents."),
    (15, "Break", "Off screens. Eat something."),
    (25, "Teach the second idea",
     "The half that only makes sense once the first half is in their "
     "fingers."),
    (45, "Build something that runs",
     "Every session ends with a file that does something. Nothing is left "
     "half-finished on the screen."),
    (20, "Show and tell",
     "Two or three students put their screen on the projector. This is the "
     "part they come back for."),
]
assert sum(m for m, _, _ in BLOCK) == HOURS_PER_SESSION * 60

# ---------------------------------------------------------------- the weeks
# stage: the roadmap card this week belongs to, so the figure and the text
#        cannot drift apart
# maths: the A-level topic it leans on, or None
# build: what exists on their laptop at the end of the week
WEEKS_PLAN = [
    dict(n=1, title="Your first programs",
         stages=[1, 3],
         sessions=[
             ("What machine learning actually is, and your first program",
              "Three live demonstrations: a model that reads handwriting, one "
              "that separates spam from real messages, one that guesses a "
              "price. Then how each of them is only arithmetic on a table of "
              "numbers. Everyone fills in the twelve-question class survey, "
              "which becomes the dataset used in Weeks 2, 3, 4 and 7. Set up "
              "Python on your own laptop, and write and run a program before "
              "you leave."),
             ("Variables, numbers and text",
              "Storing a value under a name and using it again. The four "
              "types you need: whole numbers, decimals, text and true/false. "
              "Reading input from the keyboard and printing an answer. Your "
              "first error message, on purpose, and how to read it."),
             ("Making decisions: if, else and comparison",
              "A program that behaves differently depending on its input. "
              "Comparison and the words and, or and not. By the end you have "
              "written a program that grades a mark out of 100 into a letter."),
         ],
         maths="Nothing new. You are using arithmetic you have had since P.7.",
         build="Four small programs that run, and Python working on your own "
               "laptop.",
         home="Rewrite the grading program from memory, without notes. Fifteen "
              "minutes, and it is worth more than an hour of reading."),

    dict(n=2, title="Lists, loops and functions",
         stages=[3],
         sessions=[
             ("Lists: holding many values at once",
              "One name holding thirty marks. Getting one item out, adding, "
              "removing, counting, sorting. Counting from zero, which is the "
              "one real surprise in this week."),
             ("Loops: doing the same thing to every item",
              "Repeating an instruction for every value in a list without "
              "writing it thirty times. Adding a list up, finding the "
              "largest, counting how many pass."),
             ("Functions, and your first real program",
              "Giving a name to a piece of work so you can use it again. "
              "Inputs, a result, and why this is the same idea as a formula "
              "in Excel. Then you build a marks program: it takes a class "
              "list, computes the mean and the highest, and says who passed."),
         ],
         maths="Mean and highest value. You are writing the formulas you "
               "already use in Excel, in a language that can also do the "
               "rest of this course.",
         build="A working marks program, and your code saved online where you "
               "can show it.",
         home="Add the median to your marks program. You know what a median "
              "is; the work is getting the computer to find it."),

    dict(n=3, title="Real data, real files",
         stages=[4],
         sessions=[
             ("From spreadsheet to pandas",
              "Opening a real data file in Python, starting with your own "
              "class survey so the rows are people you can ask. Rows, columns "
              "and the words the field uses for them. Six commands that tell "
              "you what any new file contains, in the same order every time; "
              "you will use those six on every dataset for the rest of the "
              "track."),
             ("Choosing rows and columns",
              "Filtering to the rows you care about and picking the columns "
              "you need. This is the autofilter you already use, written down "
              "so it runs again tomorrow on a bigger file."),
             ("Grouping and summarising",
              "One number per group: the average mark per subject, the total "
              "sales per month. This is a pivot table, written down."),
         ],
         maths="Mean, median, mode and range, applied to a file with "
               "thousands of rows rather than the twenty in a textbook "
               "exercise.",
         build="A notebook that opens a real dataset and answers five "
               "questions about it.",
         home="Find a dataset that interests you, from the list we give you, "
              "and write down three questions you would like it to answer."),

    dict(n=4, title="Cleaning, and drawing what you find",
         stages=[5, 6],
         sessions=[
             ("Data is never clean when it arrives",
              "Missing values, the same thing spelled three ways, numbers "
              "stored as text, and rows recorded twice. Each one found in two "
              "lines and fixed in two more. Writing down what you changed, so "
              "somebody else can get your number back."),
             ("Charts that answer a question",
              "Four charts and the question each one answers: a line for "
              "change over time, a bar to compare groups, a histogram for the "
              "shape of one column, a scatter for whether two things move "
              "together. Titles, axis labels and units."),
             ("Checkpoint 1: your first data investigation",
              "Take a dataset you have not seen, clean it, draw three charts "
              "and write five findings with a number attached to each. Marked, "
              "and it counts towards your certificate."),
         ],
         maths="Correlation and the scatter diagram, straight out of the "
               "statistics you are taught for A-level. You will draw one and "
               "then compute the correlation coefficient.",
         build="A cleaned dataset, three labelled charts and five written "
               "findings. The first thing in your portfolio.",
         home="Finish and submit the investigation."),

    dict(n=5, title="Teaching a computer to predict",
         stages=[7, 8, 9],
         sessions=[
             ("What learning from data means",
              "Features and a target. Showing a computer examples and letting "
              "it find the pattern instead of writing the rule yourself. "
              "Splitting your data into a part to learn from and a part to be "
              "tested on, and why that split is the whole game."),
             ("Predicting a number: the line of best fit, by machine",
              "You have drawn a line of best fit by eye. Today the computer "
              "finds the one that fits best, and you see that y = mx + c is "
              "exactly what a first machine learning model is. Then you use it "
              "to predict a value it has never seen."),
             ("Predicting a category: nearest neighbours",
              "Deciding which group something belongs to by looking at the "
              "examples it most resembles. No equations. Then the same idea "
              "made to fail on purpose, so you see what it cannot do."),
         ],
         maths="y = mx + c, gradient and intercept, and the line of best fit. "
               "This is the week where A-level algebra turns into a working "
               "model.",
         build="Two trained models on your laptop, one predicting a number "
               "and one predicting a category.",
         home="Retrain your line-of-best-fit model on a different pair of "
              "columns and write one sentence on whether it got better or "
              "worse."),

    dict(n=6, title="Is the model any good?",
         stages=[9, 10],
         sessions=[
             ("Decision trees, which you can read",
              "A model that makes a decision by asking a series of yes-or-no "
              "questions, drawn as a diagram you can follow with your finger. "
              "Then you print the tree your data produced and explain it out "
              "loud."),
             ("Accuracy lies: how to actually check a model",
              "Ninety-nine per cent accurate and completely useless. The "
              "confusion matrix, and what it costs to be wrong in each "
              "direction. Precision and recall, in plain words, on an example "
              "where the difference matters."),
             ("Checkpoint 2: build, test and defend a model",
              "Train two different models on the same data, compare them "
              "honestly, choose one and write down why. Marked, and it counts "
              "towards your certificate."),
         ],
         maths="Probability, percentages and rates: the difference between a "
               "count and a proportion, which is where most wrong claims "
               "about models come from.",
         build="Two compared models, a confusion matrix you can read, and a "
               "written justification for the one you chose.",
         home="Finish and submit the checkpoint."),

    dict(n=7, title="Grouping, neural networks, and the real world",
         stages=[11, 12, 13],
         sessions=[
             ("Finding groups nobody labelled",
              "Letting a computer sort things into groups when you have not "
              "told it what the groups are. Run first on the class survey "
              "from Week 1, where you can check the answer against people you "
              "know, and then on the penguin measurements, where the groups "
              "turn out to be the three species. Same six lines of code, two "
              "very different answers."),
             ("What a neural network is, and where ChatGPT fits",
              "One artificial neuron, worked by hand on paper, then the same "
              "thing with thirty of them in three lines of code. What deep "
              "learning is, what a large language model is doing when it "
              "answers you, and what it is not doing. The honest limits."),
             ("Machine learning in the world, and choosing your project",
              "Where these methods are already deciding things about people: "
              "loans, admissions, policing, medical triage. What bias in a "
              "model means and how it gets there. Then you choose your project "
              "dataset and question, and write the plan."),
         ],
         maths="Weighted sums and the gradient of a curve. For Principal "
               "Maths students, the derivative you learned last term is "
               "exactly how a neural network improves itself.",
         build="A clustering notebook, a small neural network that runs, and "
               "a one-page project plan.",
         home="Collect or download your project dataset and profile it with "
              "the six commands from Week 3."),

    dict(n=8, title="Your project, and showing it",
         stages=[14],
         sessions=[
             ("Build, with help at your elbow",
              "Three hours on your own project. The instructor moves between "
              "students; anything asked twice is answered to the whole room. "
              "By the end of the session your model trains and produces a "
              "number."),
             ("Finish it, write it up, publish it",
              "The last fixes, then the write-up: your question, your answer "
              "with its number, how you know, and what would change your "
              "answer. Push the whole thing to your public portfolio."),
             ("Showcase, and certificates",
              "Five minutes each, in front of the room, with parents invited. "
              "The question, the answer, one chart, and what you would do "
              "next. Then certificates."),
         ],
         maths="Everything above, used at once, on data you chose.",
         build="A finished project: a working model, a written page, a public "
               "portfolio link and a five-minute presentation.",
         home="None. Show somebody at home what you built."),
]
assert len(WEEKS_PLAN) == WEEKS
assert sum(len(w["sessions"]) for w in WEEKS_PLAN) == SESSIONS

# ---------------------------------------------------------------- roadmap
# The figure is a port of the approved roadmap figure in make_figures.py:
# same palette, same geometry, same type sizes. Only the content changes.
# Bands map a stage to when it happens, or to why it is not here.
B12, B34, B56, B78 = "WEEKS 1-2", "WEEKS 3-4", "WEEKS 5-6", "WEEKS 7-8"
HAVE = "YOU ALREADY HAVE THIS"
LATER = "NOT IN THIS TRACK"

STAGES = [
    ("1", "Getting started",
     "what machine learning is\nsetting up Python\nyour first program", B12,
     "Week 1"),
    ("2", "Maths foundations",
     "mean, median, spread\ncorrelation, probability\ngradients, y = mx + c",
     HAVE, "your A-level maths"),
    ("3", "Python fundamentals",
     "variables, types, input\nif and else, comparison\nlists, loops, functions",
     B12, "Weeks 1-2"),
    ("4", "Working with data",
     "opening a real dataset\nrows, columns, filtering\ngrouping, summarising",
     B34, "Week 3"),
    ("5", "Data cleaning",
     "missing values\nduplicates, wrong types\nrecording what changed",
     B34, "Week 4"),
    ("6", "Charts with a point",
     "line, bar, histogram\nscatter, axes, units\nwhat a chart hides",
     B34, "Week 4"),
    ("7", "How learning works",
     "features and target\ntrain and test split\nsupervised or not",
     B56, "Week 5"),
    ("8", "Predicting a number",
     "line of best fit, by machine\nregression\npredicting unseen values",
     B56, "Week 5"),
    ("9", "Predicting a category",
     "nearest neighbours\ndecision trees you read\nwhere each one fails",
     B56, "Weeks 5-6"),
    ("10", "Checking honestly",
     "why accuracy lies\nconfusion matrix\nprecision and recall",
     B56, "Week 6"),
    ("11", "Finding groups",
     "clustering\ngroups nobody labelled\none method, two answers",
     B78, "Week 7"),
    ("12", "Neural networks",
     "one neuron, by hand\na small network in code\nwhat deep learning is",
     B78, "Week 7"),
    ("13", "AI in the real world",
     "models deciding about people\nbias, and how it gets in\nwhat an LLM is not doing",
     B78, "Week 7"),
    ("14", "Your project",
     "your data, your question\nbuild, write up, publish\nfive minutes on your feet",
     B78, "Weeks 7-8"),
    ("15", "Where to go next",
     "computer vision, images\nlanguage models in depth\nreinforcement learning",
     LATER, "after this track"),
]
assert len(STAGES) == 15

# The figure and the week-by-week text must agree, so weeks claim roadmap
# CARD NUMBERS and the claim is checked exactly. A name-based check with a
# prefix fallback was the first version of this, and a fuzzy check on names
# is a check that cannot properly fail.
STAGE_NUMS = {s[0]: s[1] for s in STAGES}
_claimed = set()
for _w in WEEKS_PLAN:
    for _n in _w["stages"]:
        if str(_n) not in STAGE_NUMS:
            raise KeyError("week %d claims roadmap stage %r, which does not "
                           "exist" % (_w["n"], _n))
        _claimed.add(str(_n))

# Cards 2 and 15 are deliberately unclaimed: card 2 is the maths they arrive
# with and card 15 is what comes after this track. Everything else must be
# taught in some week, or the roadmap promises something the timetable does
# not deliver.
_expected_unclaimed = {"2", "15"}
_unclaimed = set(STAGE_NUMS) - _claimed
if _unclaimed != _expected_unclaimed:
    raise KeyError("roadmap cards taught by no week: %s; cards claimed that "
                   "should not be: %s"
                   % (sorted(_unclaimed - _expected_unclaimed),
                      sorted(_expected_unclaimed - _unclaimed)))

# ---------------------------------------------------------------- assessment
# A certificate with real marks was asked for, so the marks have to come from
# work rather than from attendance. Turning up is expected and is not a grade.
ASSESSMENT = [
    ("Weekly practical work", 20, "Weeks 1-7",
     "Seven short pieces, one a week, marked out of 10. These are the "
     "programs and notebooks built in the sessions themselves, so a student "
     "who attends and works collects most of this."),
    ("Checkpoint 1: a data investigation", 15, "Week 4",
     "Clean an unfamiliar dataset, draw three charts and write five findings "
     "with a number attached to each. Marked on the findings and the labels "
     "on the charts."),
    ("Checkpoint 2: build and defend a model", 20, "Week 6",
     "Train two models on the same data, compare them honestly and justify "
     "the one you chose. Marked on the reasoning as much as on the accuracy."),
    ("Final project", 30, "Week 8",
     "A working model on a dataset the student chose, with a written page: "
     "the question, the answer with its number, how they know, and what "
     "would change the answer."),
    ("Showcase presentation", 15, "Week 8",
     "Five minutes in front of the room with parents present. Marked on "
     "whether somebody outside the room could follow it."),
]
assert sum(w for _, w, _, _ in ASSESSMENT) == 100

# The questions a student asks the moment marks are mentioned, and which a
# syllabus that only publishes weights leaves unanswered.
MARK_NOTES = [
    ("When you get a mark back",
     "Within a week of handing it in, with written comments on the work "
     "itself rather than a number on its own. The two checkpoints are "
     "returned in the next session, because a mark that arrives after the "
     "topic has moved on teaches nothing."),
    ("If you hand something in late",
     "Practical work is accepted up to a week late at full marks, because "
     "this is a holiday and life happens. After that it is marked and "
     "capped at a pass. The final project cannot be late, because the "
     "showcase is a fixed day and the room is booked."),
    ("If you miss a checkpoint entirely",
     "You sit it in the following session from a different dataset. A "
     "student who misses both checkpoints and the project has no marked "
     "work, and the certificate then records attendance only."),
    ("If you want to improve a mark",
     "Practical work can be redone once, any time before Week 8, and the "
     "better mark stands. The checkpoints and the project are marked once. "
     "Redoing work you got wrong is the most useful thing a student on this "
     "track can do with an evening."),
]

BANDS = [
    ("Distinction", 70, "Can start a new dataset unaided and finish it."),
    ("Merit", 60, "Can do the whole workflow with the notes open."),
    ("Pass", 50, "Can follow the workflow and explain what each step does."),
    ("Certificate of attendance", 0,
     "Attended and took part. The certificate says exactly that and claims "
     "no skill beyond it."),
]

# ---------------------------------------------------------------- kit
KIT = [
    ("A laptop they bring themselves",
     "Windows 10 or newer, or any Mac from 2017 onward. 4 GB of memory is "
     "enough; 8 GB is comfortable. About 6 GB of free disk space. A student "
     "without a laptop should tell us before Week 1 so we can pair them and "
     "arrange lab access, rather than discovering it on the first morning."),
    ("Nothing installed beforehand, and this matters",
     "We install everything together in Session 1 from a USB stick, so a slow "
     "connection cannot stop the first morning. Please do not install Python "
     "at home first: the whole class runs one fixed version, and a laptop "
     "carrying a different one produces errors nobody else in the room can "
     "reproduce and that cannot be fixed during a session. Every piece of "
     "software we use is named in the next section."),
    ("Two free accounts, made in Session 1",
     "A Google account, for the browser fallback, and a GitHub account, for "
     "the portfolio. Both are free and both are set up in the room. A student "
     "under thirteen needs a parent to make the GitHub one."),
    ("A notebook and a pen",
     "Several things in this track are worked on paper first, including the "
     "neuron in Week 7. That is deliberate."),
    ("The data, on a USB stick",
     "Every dataset is handed out on the first day as well as being "
     "downloadable. The internet in the room is not a dependency for any "
     "session."),
]

# ------------------------------------------------------------------- stack
# Every tool named, with a version policy, because "we will use Python" is
# not something a parent can check and not something a student can prepare
# for. All of it is free, none of it expires, and none of it needs a
# subscription or a card.
#
# ONE fixed version for the whole class is the single most important line
# here. Compiled packages are tied to the Python minor version, so a student
# who installs a different one at home gets an error nobody else in the room
# can reproduce and there is no fix available during a session. The rule
# that follows from that is in the kit list: do not install anything before
# Week 1.
STACK = [
    ("Python", "The language. One version is fixed for the whole class and "
                "every laptop gets that one, so an error on your screen is "
                "an error the person next to you can also read."),
    ("Anaconda",
     "The installer that puts Python and everything below on a laptop in one "
     "go, with nothing left to configure. It runs from the USB stick we "
     "bring, so the room's internet cannot stop the first session. About 5 "
     "GB once installed."),
    ("Jupyter Notebook",
     "Where all the work happens: you type a few lines, run them, and see "
     "the answer or the chart underneath. A notebook is also the thing you "
     "submit, because it shows the working as well as the result."),
    ("pandas",
     "Tables in Python. Everything you can do to a spreadsheet, written down "
     "so it runs again tomorrow on a file ten times the size."),
    ("matplotlib",
     "The charts. Line, bar, histogram and scatter, with the titles and the "
     "axis labels that make a chart mean something."),
    ("scikit-learn",
     "The models. Regression, nearest neighbours, decision trees, clustering "
     "and the small neural network, all in the same three lines of code: fit, "
     "predict, score."),
    ("Google Colab",
     "The fallback. The same notebooks run in a browser with nothing "
     "installed, which covers a laptop that is too old or too locked down "
     "for the installer. Needs a free Google account."),
    ("GitHub",
     "The portfolio. A free account, and each finished piece of work is "
     "pushed there as a public link the student keeps and can put on an "
     "application."),
]

# ---------------------------------------------------------------- the data
# Named, because "relevant datasets" is the question every serious parent
# and every serious student asks next, and because the answer determines
# whether the room needs internet.
DATA = [
    ("Your own class, from Week 1",
     "Twelve questions everybody answers in the first session: hours of "
     "sleep, distance to school, subject combination, screen time, how you "
     "travel, and so on. About twenty-five rows, and every student is one of "
     "them, which is why this is the dataset the room argues about. Used in "
     "Weeks 2, 3, 4 and 7. No names on it, and it is never published to "
     "anybody's portfolio."),
    ("Data that arrives inside the software",
     "Handwritten digits, house prices, penguin body measurements and a few "
     "others are installed along with scikit-learn, so one line of code loads "
     "them and nothing is downloaded. These are the standard teaching "
     "datasets used in universities, which is deliberate: a student who meets "
     "them here will meet them again next year."),
    ("Ugandan open data, on the USB stick",
     "Health facility locations, population and school enrolment by district, "
     "and a rainfall series. All of it is published free by public bodies and "
     "humanitarian data services, downloaded before the track starts and "
     "handed out on day one. Working on data about places students know is "
     "worth more than a tidier dataset about somewhere they do not."),
    ("Data the student collects for the project",
     "Boda fares against distance, second-hand phone prices against their "
     "specifications, match results, a market's prices over three weeks. "
     "Forty rows gathered by hand in a notebook is plenty for Week 8, and a "
     "student defends their own data far better than anything handed to "
     "them."),
    ("Kaggle, for after the track",
     "Thousands of free public datasets and beginner competitions. Week 8 "
     "shows how to enter one, and it is where a student who wants to keep "
     "going finds their next dataset."),
]

# Project examples. Every one is (question, where the data comes from),
# because a project idea without a dataset behind it is a wish. These are
# examples to choose from or to argue with, not a fixed list.
PROJECTS = [
    ("Does more sleep go with better marks?",
     "The class survey, plus your own marks for the last three terms."),
    ("What is a second-hand phone worth, given its age, memory and screen?",
     "Forty listings you copy from an online marketplace into a spreadsheet."),
    ("Can you predict a boda fare from the distance and the time of day?",
     "Fares you record yourself for two weeks, with the distance from a maps "
     "app."),
    ("Which subject combinations go together in your school, and why?",
     "Subject choices for your year, with no names attached."),
    ("Can a computer read a handwritten digit?",
     "The handwritten digit images that arrive with scikit-learn."),
    ("Does rainfall predict the price of tomatoes in your market?",
     "The rainfall series on the USB stick, and prices you record weekly."),
    ("Which districts are furthest from a health facility?",
     "The health facility and population data on the USB stick."),
    ("Can you tell a real message from a scam message?",
     "A public collection of scam and ordinary text messages, on the stick."),
    ("Does a footballer's minutes played predict their goals?",
     "A season of public match data for a league you follow."),
]

# What a project has to satisfy to be approved in Week 7. Practical, because
# the commonest way a first project fails is a question that no number can
# answer, or data that turns out not to exist.
PROJECT_RULES = [
    "Your question must have a number or a category as its answer. "
    "“Is machine learning useful in farming” is an essay; "
    "“can I predict maize yield from rainfall” is a project.",
    "The data must exist before you commit to the question. You profile it "
    "in Week 7 with the six commands from Week 3, in front of the "
    "instructor.",
    "About two hundred rows if you download it, or forty if you collect it "
    "yourself. Below that, nothing you find will hold up.",
    "No personal information about anybody who has not agreed to be in it, "
    "and no names in anything you publish.",
    "You must be able to explain every line you submit, including any line "
    "an AI tool wrote for you.",
]

# ---------------------------------------------------------------- policies
# The questions parents actually ask, answered before they have to ask.
POLICIES = [
    ("Attendance",
     "Twenty-four sessions, and the work is cumulative: Week 5 assumes Week "
     "2. A student who misses a session gets the notes and the recording of "
     "the live coding, and should expect to spend an hour catching up before "
     "the next one. Missing more than four sessions makes the certificate "
     "marks difficult to award honestly."),
    ("Using AI tools such as ChatGPT",
     "Allowed, and taught, with one rule: a student must be able to explain "
     "every line they submit. We ask in the showcase and at the checkpoints. "
     "Code a student cannot explain scores nothing, which is the same rule "
     "any university will apply to them next year. Week 7 covers what these "
     "tools are actually doing and where they are wrong."),
    ("Safety online",
     "Students create a public portfolio, so the setup session covers what "
     "goes in it and what does not: no full date of birth, no home address, "
     "no school ID numbers, no photographs of other students without asking. "
     "Datasets are public and contain no personal information about anybody "
     "in the room."),
    ("How much work there is at home",
     "Fifteen to twenty minutes after most sessions, which is one small "
     "exercise and is listed in the week-by-week table. Three weeks are "
     "heavier because a marked piece is due: Week 4, Week 6 and Week 8 need "
     "about two hours each at home. Over the whole track that is roughly ten "
     "hours outside the room, and a student who does none of it will still "
     "pass and will get noticeably less out of it."),
    ("Screens and breaks",
     "Every session has a fifteen-minute break away from screens, and no "
     "teaching block runs longer than twenty-five minutes."),
    ("What parents are invited to",
     "The showcase on the final session, where each student presents for five "
     "minutes. Parents are welcome to the first fifteen minutes of Week 1 "
     "Session 1 as well, to see the room and meet the instructor."),
    ("Marks, and what the certificate says",
     "Marks come from work rather than attendance. The certificate states the "
     "band and the hours, and a student below 50 receives a certificate of "
     "attendance that does not claim a skill they do not have. We would "
     "rather a certificate meant something."),
]

# ---------------------------------------------------------------- honesty
# What this track does not do. In the syllabus because a parent reading a
# brochure deserves to know the edges, and because over-promising is how a
# holiday course loses a family's trust.
LIMITS = [
    ("It does not make your child a professional in eight weeks",
     "Seventy-two hours makes a confident beginner who can finish a small "
     "project without help. A working data scientist has years behind them. "
     "What this track does is remove the barrier: after it, the online "
     "courses and university modules are readable rather than baffling."),
    ("It is not a substitute for A-level revision",
     "It is a holiday track and it is scheduled three days a week for that "
     "reason. The maths it uses is A-level maths, so it reinforces "
     "statistics and algebra, and several students find their Paper 2 "
     "statistics easier afterwards. It does not teach the syllabus."),
    ("There is no deep learning beyond a first look",
     "Image recognition, language models and reinforcement learning need "
     "foundations this track is building. Week 7 shows what they are and "
     "Stage 15 of the roadmap says where to learn them. A track that "
     "promised them in eight weeks from zero would be selling something."),
    ("Nobody is promised a job or a scholarship",
     "Students leave with a public portfolio and a certificate with marks on "
     "it, which is a real thing to show an admissions officer. It is an "
     "advantage rather than a guarantee, and we will not describe it as more "
     "than that."),
]

# ---------------------------------------------------------------- next steps
NEXT = [
    ("If they want more machine learning",
     "Stage 15 of the roadmap: computer vision, language models, "
     "reinforcement learning. Kaggle Learn and Google's machine learning "
     "crash course both cover the next step for nothing, and both assume "
     "exactly what this track leaves a student with."),
    ("If they are heading for university computing",
     "This track covers roughly the practical half of a first-year "
     "introduction to programming and data. Keep the portfolio and keep "
     "adding to it."),
    ("If they are heading for engineering, medicine or economics",
     "Every one of those fields now uses these methods on its own data. The "
     "data handling in Weeks 3 and 4 is the part they will use first, "
     "whatever they study."),
    ("If they want to keep practising for free",
     "Kaggle has thousands of public datasets and beginner competitions. The "
     "final week shows them how to enter one."),
]

# ---------------------------------------------------------------- fill-ins
# Facts I do not have. Written as fields rather than invented, because a
# syllabus that goes to parents with a guessed date or fee is worse than one
# with a blank.
TO_CONFIRM = [
    "Start date and end date",
    "Which three days of the week, and the time of day",
    "Venue and room",
    "Fee, what it includes, and how to pay",
    "Instructor name and one line of background",
    "A phone number and an email for questions",
    "Maximum number of students in the group",
    "Registration deadline and how to register",
]

# ------------------------------------------------------- figures, and print
# How wide each figure is PLACED in the document, in inches. Declared here
# because the figure code needs it: a figure drawn 13in wide and placed at
# 6.7in has its type halved, and the first build of this syllabus put 7.7pt
# annotation on the page at under 4pt. The figure generator asserts against
# these numbers, so a figure cannot be drawn at a size the page will shrink
# into illegibility.
#
# The page is Letter with 1.9cm margins, which leaves 7.0in of measure.
# Everything is placed within that and the document stays portrait: a
# landscape page for the roadmap was tried and is awkward to print and
# worse to read on a phone, which is how most parents will open this.
FIG_PLACEMENT = {
    "timeline_schools": 6.70,
    "roadmap_schools": 7.00,
    "marks_schools": 6.70,
}

# The smallest type any figure may show ON PAPER, after placement scaling.
# Lower than the document's 9pt floor, because a figure annotation is not
# body text, and stated rather than left to judgement.
FIG_MIN_PT = 8.0

# The tallest a figure may be ONCE PLACED, in inches. Letter with 1.9cm
# margins gives about 9.5in of height; a section heading, an intro paragraph
# and a caption take about 1.5in of it. A figure taller than this is pushed
# onto the next page on its own, which is what happened to the roadmap on
# the first build: the heading and the intro printed on one page and the
# figure on the following one.
FIG_MAX_H = 7.7
