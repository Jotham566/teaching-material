# -*- coding: utf-8 -*-
"""Single source of truth for the Data Analysis track.

Audience: adults already in work who are confident in a spreadsheet and have
never written a line of code. FIVE weeks, three sessions a week, three hours
a session. Python-heavy, with SQL to get the data and Power BI to ship the
result.

Every document, lab and deck in DataAnalysis_Track/ is generated from this
file, so a change here reaches all of them.

WHY FIFTEEN SESSIONS AND NOT TWELVE
-----------------------------------
The first version of this track was twelve sessions and assumed the room
already knew what a row, a table, a mean and an axis were. It did not. Jotham
was explicit: they start from scratch. Teaching from scratch is worth six to
eight hours on its own, and it was funded two ways, both of which he chose:
three extra sessions, AND cutting the most advanced material. What came out
is listed in CUT below, so nobody puts it back by accident.

WHAT "FROM SCRATCH" MEANS HERE
------------------------------
Not "never used a computer". They can build a pivot table and write a
VLOOKUP. So every new idea arrives through something they already do in
Excel, and the vocabulary is defined out loud before it is used. That is what
the `vocab` field on each session is for, and it is what the glossary
handout is built from.
"""

TRACK = "Data Analysis with Python, SQL and Power BI"
SUBTITLE = "Five weeks, fifteen sessions, forty-five hours"
AUDIENCE = ("People already in work who have to answer questions from data. "
            "They are confident in a spreadsheet: a pivot table and a "
            "VLOOKUP hold no fear. They have never written code, and nobody "
            "has ever defined the words this field uses.")

# ---------------------------------------------------------------- shape
WEEKS = 5
SESSIONS_PER_WEEK = 3
HOURS_PER_SESSION = 3
TOTAL_HOURS = WEEKS * SESSIONS_PER_WEEK * HOURS_PER_SESSION      # 45

# The three-hour block. Unchanged from the twelve-session version because it
# worked: two teaching blocks of fifty, real breaks, and the last fifty
# minutes hands-on with the room's questions answered out loud.
BLOCK = [
    (10, "Recap, and the words for tonight",
     "What we settled last session, then the three or four terms this "
     "session will use. Beginners lose sessions to undefined vocabulary "
     "more than to difficult ideas."),
    (50, "Teach block 1",
     "Live, on the screen, typed out. Participants follow along on their "
     "own machines rather than watching."),
    (10, "Break", "Off screens. This one is not optional after a work day."),
    (45, "Teach block 2",
     "The second half of the technique, then the failure modes: what it "
     "looks like when this goes wrong, and how you notice."),
    (5, "Break", "Short. Stand up."),
    (50, "Lab",
     "Participants work the lab; the instructor circulates. Anything asked "
     "twice gets answered to the whole room."),
    (10, "Wrap",
     "One thing to practise before next time, the homework, and the single "
     "sentence you should be able to say about tonight."),
]
assert sum(m for m, _, _ in BLOCK) == HOURS_PER_SESSION * 60

# ---------------------------------------------------------------- datasets
DATASETS = [
    {"key": "core",
     "name": "Riverside Distributors (course dataset)",
     "url": "built by DataAnalysis_Track/data/build_teaching_data.py",
     "licence": "Course-owned. Generated, so it can be redistributed freely, "
                "including on a commercial course.",
     "shape": "6 tables, about 6,000 orders and 20,000 order lines over two "
              "years, plus returns and a daily FX series",
     "account": "none",
     "use": "The spine of the track, and small enough that a beginner can "
            "check it by hand. It is a wholesale distributor: customers, "
            "products, sales reps, orders, order lines, returns. Every lab "
            "answer is computed by the generator and stored in "
            "answer_key.json, so a participant knows within seconds whether "
            "they are right, and no number in any handout was estimated."},
    {"key": "retail",
     "name": "Online Retail II",
     "url": "https://archive.ics.uci.edu/dataset/502/online+retail+ii",
     "licence": "CC BY 4.0",
     "shape": "1,067,371 rows x 8 columns, .xlsx, Dec 2009 to Dec 2011",
     "account": "none",
     "use": "The first real file they meet, in week three. One flat table of "
            "invoices, which is the shape data actually arrives in. Also the "
            "first file too big for Excel to open comfortably, which is the "
            "moment the course justifies itself."},
    {"key": "bank",
     "name": "Bank Marketing (UCI 222)",
     "url": "https://archive.ics.uci.edu/dataset/222/bank+marketing",
     "licence": "CC BY 4.0",
     "shape": "bank-full.csv is 45,211 rows x 17; bank-additional-full.csv is "
              "41,188 rows x 21. They are different files: say which one.",
     "account": "none",
     "use": "Banking, finance and telecom capstone. Campaign contacts "
            "against an outcome, so it carries segmentation, rates and "
            "cross-tabs. The duration column leaks the outcome and must be "
            "dropped, which makes it a good lesson about leakage."},
    {"key": "machine",
     "name": "AI4I 2020 Predictive Maintenance (UCI 601)",
     "url": "https://archive.ics.uci.edu/dataset/601/"
            "ai4i+2020+predictive+maintenance+dataset",
     "licence": "CC BY 4.0",
     "shape": "10,000 rows x 14 columns, one CSV. Failures are about 3.4% of "
              "rows",
     "account": "none",
     "use": "Energy, mining and manufacturing capstone. Machine sensor "
            "readings against a failure flag. The imbalance is the point: a "
            "rule that predicts no failure is 96.6% accurate and useless."},
    {"key": "worldbank",
     "name": "World Bank Open Data indicators API",
     "url": "https://api.worldbank.org/v2/country/UG/indicator/"
            "NY.GDP.MKTP.CD?format=json",
     "licence": "CC BY 4.0, with additional terms on the portal",
     "shape": "About 16,000 indicators. JSON, 50 records a page by default",
     "account": "No key. Authentication was removed entirely.",
     "use": "Government, NGO and health capstone. The URL above works in a "
            "browser address bar, which is the cheapest possible way to show "
            "a beginner what an API actually is."},
    {"key": "healthsites",
     "name": "Uganda Healthsites",
     "url": "https://data.humdata.org/dataset/uganda-healthsites",
     "licence": "ODbL. Share-alike applies to a derived database, so say so "
                "if participants publish anything built on it.",
     "shape": "About 7,969 facilities. CSV, SHP and GeoJSON, with name, "
              "facility type, activities and coordinates",
     "account": "none",
     "use": "The local dataset. Real Ugandan records with categories and "
            "coordinates, which makes the Power BI map land on data the room "
            "recognises."},
]

REJECTED = [
    ("Sample - Superstore",
     "The best shape on offer and the worst licence: use is governed by the "
     "Tableau EULA, whose sample-code clause is internal use only and not "
     "sublicensable. Every Kaggle and GitHub copy lists the licence as "
     "unknown. It cannot be redistributed to a class."),
    ("Olist Brazilian E-Commerce",
     "Nine related tables and a genuine star schema, which is what the core "
     "dataset needed, but CC BY-NC-SA 4.0. The NonCommercial clause is a "
     "live problem the moment the course is paid for, so the course dataset "
     "is generated instead and the schema lesson is kept."),
    ("IBM Telco Customer Churn and IBM HR Analytics Attrition",
     "No licence could be found for either. There are open, unanswered "
     "forum threads from people asking for the Telco licence for exactly "
     "this purpose, and the HR set appears to have needed prior permission "
     "from its administrator."),
    ("WHO Global Health Observatory OData API",
     "Mechanically ideal, including a documented Power BI OData path. WHO's "
     "confirmed licence is CC BY-NC-SA 3.0 IGO and covers publications; no "
     "dataset-specific terms page could be retrieved. NonCommercial again."),
    ("DHIS2 play instance",
     "The database is wiped nightly, the version paths rotate, and there is "
     "a documented history of the default credentials breaking. Fine as a "
     "live look at what an HMIS is, unusable as something a lab depends on."),
]

# ---------------------------------------------------------------- sessions
# vocab: (term, plain definition, the Excel equivalent or None)
#   Every term a session uses is defined here BEFORE the session uses it, and
#   the glossary handout is generated from the union of these lists. If a
#   term appears on a slide and not here, that is a defect the verifier
#   reports.
SESSIONS = [
    dict(n=1, week=1, tool="Foundations",
         title="From a spreadsheet to data",
         roadmap="What is data analysis; the analyst's workflow",
         outcomes=[
             "Name the parts of a table using the words the rest of the "
             "field uses, and say what each one is called in Excel.",
             "Say what one row of a file represents, in one sentence, before "
             "doing anything else with it.",
             "Turn a vague request into a question with a number, a "
             "population and a time window attached.",
         ],
         vocab=[
             ("Data", "Recorded facts. Numbers, text and dates that "
                      "something or somebody wrote down.", None),
             ("Dataset", "One collection of data that belongs together. "
                         "Usually one or more files, or one database.",
              "A workbook"),
             ("Table", "Rows and columns where every row is the same kind of "
                       "thing and every column holds the same kind of "
                       "value.", "A sheet with a header row"),
             ("Row, or record", "One of the things the table is about: one "
                                "order, one customer, one machine reading.",
              "A row"),
             ("Column, or field", "One fact recorded about every row, with "
                                  "one name and one type.", "A column"),
             ("Cell, or value", "One column of one row. The smallest piece.",
              "A cell"),
             ("Data type", "What kind of value a column holds: whole "
                           "number, decimal, text, date, or true/false. A "
                           "column has ONE type, all the way down.",
              "Cell format, but enforced rather than cosmetic"),
             ("Grain", "What one row represents. The single most important "
                       "fact about any table, and the one nobody states.",
              None),
         ],
         b1="Requests against questions. Four real requests from a manager, "
            "each rewritten into a question you could actually answer, and "
            "one rewritten three different ways to show the original was "
            "ambiguous. The rule for the rest of the course: no analysis "
            "starts until the question has a number, a population and a "
            "window.",
         b2="The words, on a real table. The anatomy figure on the screen "
            "and the same five rows open in Excel: row, column, cell, "
            "header, primary key, and the Excel word beside each. Then data "
            "types, and grain, which is the one that matters: every table in "
            "this course gets its grain said out loud before it is used.",
         lab="Open the course data in Excel. Write down, for each of the six "
             "files: what one row is, how many rows there are, and which "
             "column could never repeat. Then take the three requests on "
             "your sheet and turn each into an answerable question.",
         home="Write down the last three things somebody asked you for at "
              "work. Rewrite each as a question with a number, a population "
              "and a window. Bring them: they are capstone candidates.",
         trap="Starting to compute before agreeing what was asked. It is "
              "the most expensive habit in the room and the cheapest to "
              "fix.",
         check="Setup checkpoint: the tools installed and the data open.",
         figs=["fig_table_anatomy"]),

    dict(n=2, week=1, tool="Foundations",
         title="Why data lives in several tables",
         roadmap="Data modelling basics; relational thinking",
         outcomes=[
             "Explain why a business keeps orders and customers in separate "
             "tables instead of one big sheet.",
             "Find the key that connects two tables, and predict what "
             "happens to the row count when they are joined.",
             "Say what one row means in each of the six course tables.",
         ],
         vocab=[
             ("Primary key", "A column whose value is never repeated, so it "
                             "identifies one row exactly.",
              "The column you would VLOOKUP on"),
             ("Foreign key", "A column that holds another table's primary "
                             "key, which is what links the two.",
              "The lookup value you type into VLOOKUP"),
             ("One-to-many", "One row on one side matches several rows on "
                             "the other. One order, several order lines.",
              None),
             ("Join", "Putting two tables side by side by matching a key, so "
                      "you can use columns from both.",
              "VLOOKUP, except it returns EVERY match rather than the first"),
             ("Database", "Several related tables kept together, with the "
                          "types and the keys enforced by the software.",
              "A workbook where the rules are not optional"),
             ("Duplication", "The same fact stored in more than one place. "
                             "It is why one big sheet goes wrong: change a "
                             "customer's region and you have to change it in "
                             "every row.", None),
         ],
         b1="Why not one big sheet. Start from the flat export everybody "
            "recognises and break it: a customer changes region, and the "
            "same fact now has to be edited in four hundred rows, some of "
            "which get missed. Then the same data as six tables, and the "
            "same change made once. Keys, primary and foreign, drawn on the "
            "screen.",
         b2="Grain, and what a join does to it. The grain figure: one row is "
            "one order against one row is one order line. Then the join "
            "figure: INNER against LEFT, and the walk-in orders that "
            "disappear from one and survive the other. No SQL yet. This is "
            "done by clicking through the tables in DB Browser so the idea "
            "lands before the syntax does.",
         lab="In DB Browser, on the Browse Data tab, with no SQL at all: "
             "find the six tables, write down the grain of each, find the "
             "primary key of each, and find which column in orders points at "
             "customers. Then find an order with no customer and say what "
             "you think that means.",
         home="Take one report you receive at work and work out how many "
              "tables it was probably built from. Name them and the key each "
              "would join on. You will be right more often than you expect.",
         trap="Assuming one row means what you assume it means. Every wrong "
              "total later in this course comes from a grain nobody said out "
              "loud.",
         figs=["fig_grain", "fig_join"]),

    dict(n=3, week=1, tool="SQL", title="Asking a database for rows",
         roadmap="SQL: SELECT, WHERE, ORDER BY, LIMIT, NULL",
         outcomes=[
             "Write a SELECT with a filter, a sort and a limit, and say what "
             "each part did to the number of rows.",
             "Count rows, and explain why two different counts of the same "
             "table can both be right.",
             "Recognise a NULL and handle it without getting a silently "
             "empty answer.",
         ],
         vocab=[
             ("Query", "A written description of the rows you want. You "
                       "describe the result; the database works out how to "
                       "fetch it.", "A filter, but written down and "
                                    "repeatable"),
             ("SELECT", "The clause that says which columns you want back.",
              None),
             ("WHERE", "The clause that says which rows you want, by "
                       "condition.", "Autofilter"),
             ("ORDER BY", "Sort the result.", "Sort"),
             ("LIMIT", "Return only the first so many rows, which is how you "
                       "look at something without printing 6,000 lines.",
              None),
             ("NULL", "No value recorded. It is not zero and not an empty "
                      "string, and any comparison with it is neither true "
                      "nor false.", "A genuinely blank cell"),
             ("COUNT", "How many rows. COUNT(*) counts rows; COUNT(column) "
                       "counts rows where that column is not NULL.",
              "COUNTA against COUNT"),
         ],
         b1="A table is rows and columns, and a query is a description of the "
            "rows you want. SELECT, FROM, WHERE, ORDER BY, LIMIT, typed live "
            "against the orders table, checking the row count after every "
            "clause. Each one is shown beside the Excel action it replaces, "
            "so nothing feels new for its own sake.",
         b2="NULL, and why it needs its own half hour. A missing value is not "
            "zero, so any comparison with it comes back neither true nor "
            "false, and a filter written with = NULL returns nothing at all "
            "with no error. Then COUNT(*) against COUNT(customer_id) on a "
            "table that has both, which is the session's one surprise.",
         lab="Eight questions of rising difficulty against the course "
             "database. Answers are on the sheet, so check yourself as you "
             "go rather than at the end. Write the query before you read the "
             "answer.",
         home="Five more questions on the sheet. Then: name one table at "
              "work you would like to query, and write down what its columns "
              "probably are.",
         trap="Writing = NULL instead of IS NULL. No error, no warning, zero "
              "rows, and the zero looks like a fact about the business."),

    dict(n=4, week=2, tool="SQL", title="Counting and grouping",
         roadmap="SQL: aggregates, GROUP BY, HAVING",
         outcomes=[
             "Aggregate with COUNT, SUM and AVG, and group by one or more "
             "columns.",
             "Filter groups with HAVING, and say why WHERE cannot do it.",
             "Spot an averaged average and correct it.",
         ],
         vocab=[
             ("Aggregate", "A calculation that collapses many rows into one "
                           "number: count, sum, average, minimum, maximum.",
              "What a pivot table does in its value area"),
             ("GROUP BY", "Says which rows belong together before the "
                          "aggregate runs.",
              "The Rows area of a pivot table"),
             ("HAVING", "A filter on the GROUPS, applied after the "
                        "aggregation.",
              "Filtering a pivot table by its totals"),
             ("Alias", "A name you give a computed column so the output is "
                       "readable.", "Typing a header over a formula"),
             ("Derived value", "A number the data does not store, computed "
                               "from columns that it does. Revenue here is "
                               "quantity times price times one minus "
                               "discount.", "A formula column"),
         ],
         b1="This session is a pivot table, written down. Say that first: the "
            "room already knows what they want, and GROUP BY is the "
            "vocabulary for it. COUNT, SUM, AVG, MIN, MAX, then GROUP BY on "
            "one column, then two, with the pivot table built beside it in "
            "Excel for the first example so the mapping is visible.",
         b2="HAVING, and the difference between filtering rows and filtering "
            "groups, demonstrated by getting it wrong first and reading the "
            "error out loud. Then revenue, which is not a column: the "
            "definition used for the rest of the course, and why every "
            "revenue question has to say which order statuses it counts.",
         lab="Revenue by channel, by segment and by month, delivered orders "
             "only. Then the same three figures as a pivot table in Excel "
             "from the exported CSV, and confirm they agree.",
         home="Two more groupings on the sheet, then one sentence: which "
              "grouping of your own work data would you most like to see, "
              "and which columns would it need?",
         trap="Averaging an average. The average of four regional averages "
              "is not the national average unless the regions are the same "
              "size. Sum the top, sum the bottom, then divide."),

    dict(n=5, week=2, tool="SQL", title="Joining tables, carefully",
         roadmap="SQL: INNER and LEFT JOIN, CTEs",
         outcomes=[
             "Join three tables and say what each join is for.",
             "Predict which rows an INNER JOIN will drop, then check that "
             "prediction against the row count.",
             "Break a query into named steps somebody else can read.",
         ],
         vocab=[
             ("INNER JOIN", "Keep only rows that matched on both sides.",
              "VLOOKUP where you delete the #N/A rows"),
             ("LEFT JOIN", "Keep every row on the left, and leave the right "
                           "side blank where nothing matched.",
              "VLOOKUP where you keep the #N/A rows"),
             ("Fan-out", "When one row matches several, its values are "
                         "repeated once per match. Sum them afterwards and "
                         "you have counted the same thing several times.",
              None),
             ("CTE", "A named step at the top of a query that you can then "
                     "use like a table. Short for common table expression.",
              "A helper sheet you build before the final calculation"),
         ],
         b1="The join, in SQL now that the idea is already familiar from "
            "session 2. INNER, then LEFT, with the row count checked each "
            "time, because the number of rows is the fastest way to find out "
            "you joined wrongly. The walk-in orders vanish from the inner "
            "join, and with them a visible amount of revenue.",
         b2="Fan-out, which is the dangerous one: joining orders to order "
            "lines and then summing an order-level column gives a number far "
            "too big, and nothing warns you except a row count that moved. "
            "Then CTEs: three short named steps instead of one nested query, "
            "and each step checked on its own before the next is written.",
         lab="Build the revenue report the sales manager wants: revenue by "
             "rep by month for 2025, net of returns. Three CTEs, checked "
             "step by step. This is Checkpoint 1 and it is marked against "
             "the key tonight.",
         home="Finish the report if it is not finished, then break it on "
              "purpose: change one LEFT JOIN to an INNER JOIN and write down "
              "what changed in the numbers and why.",
         check="Checkpoint 1: the rep revenue report, marked against the key.",
         trap="A join that multiplies rows. The total gets bigger and looks "
              "plausible, and the only tell is the row count."),

    dict(n=6, week=2, tool="Python", title="Your first program",
         roadmap="Python basics: variables, types, functions, errors",
         outcomes=[
             "Say what a variable, a function and a library are, in your own "
             "words.",
             "Read an error message and find the line that caused it.",
             "Load a file into pandas and print how many rows it has.",
         ],
         vocab=[
             ("Program", "A list of instructions, run in order, top to "
                         "bottom.", "A macro, or a formula that got long"),
             ("Variable", "A name that holds a value, so you can use it "
                          "again without retyping it.",
              "A named cell or a named range"),
             ("Type", "What kind of value: whole number, decimal, text, "
                      "true/false, date.", None),
             ("Function", "A named instruction that takes inputs and gives "
                          "back a result.", "SUM, VLOOKUP, IF"),
             ("Argument", "An input you hand to a function.",
              "What goes inside the brackets of a formula"),
             ("Library", "Somebody else's functions, loaded when you need "
                         "them.", "An add-in"),
             ("pandas", "The library that gives Python tables. Almost "
                        "everything in weeks three and four is pandas.",
              None),
             ("DataFrame", "A table in Python: named columns, each with one "
                           "type.", "A sheet, with the rules enforced"),
             ("Traceback", "The error message. It is long, and the LAST line "
                           "is the one that names the problem.",
              "#VALUE!, with an explanation attached"),
             ("Zero-based", "Counting from 0. The first row is row 0. It is "
                            "a real difference from Excel and it catches "
                            "everybody once.", None),
         ],
         b1="You already write code. Open a spreadsheet formula, =IF(B2>1000, "
            "\"large\", \"small\"), and name its parts: a function, its "
            "arguments, a condition, a result. Python is that with the "
            "brackets in different places. Then, live: a variable, four "
            "types, a list, a function you write yourself, and an error on "
            "purpose so the traceback is read out loud in the first half "
            "hour rather than feared for a week.",
         b2="import pandas as pd, and the first DataFrame. read_csv, then "
            "shape, then head. Three commands, and the room can see their "
            "own data in a new tool. Then the two things that catch every "
            "Excel user: counting from zero, and a column having one type "
            "all the way down.",
         lab="Type it yourself, from a blank notebook: load the orders file, "
             "print the shape, print the first five rows, print the column "
             "types, and make one deliberate error and read the traceback "
             "out loud to your neighbour.",
         home="Retype tonight's notebook from scratch without looking. It "
              "takes fifteen minutes and it is worth more than an hour of "
              "reading.",
         trap="Copying code you cannot read. It works, you learn nothing, "
              "and the first time it breaks you are stuck. Type it."),

    dict(n=7, week=3, tool="Python", title="Reading a file, and looking at it",
         roadmap="pandas: loading, inspecting, selecting, filtering",
         outcomes=[
             "Profile a file you have never seen in six commands.",
             "Select columns and filter rows by condition.",
             "Say what a dtype of object on a number column tells you.",
         ],
         vocab=[
             ("Series", "One column of a DataFrame, on its own.", None),
             ("dtype", "The type pandas decided a column has. object on a "
                       "column of numbers means something in there is not a "
                       "number.", None),
             ("Boolean filter", "Selecting rows by a true/false test applied "
                                "to every row.", "Autofilter, written down"),
             ("Missing value", "A cell with nothing recorded, shown as NaN.",
              "A blank cell"),
             ("Profile", "The fixed six-command routine you run on any new "
                         "file before you trust it.", None),
         ],
         b1="The profiling routine, in a fixed order, on the course data: "
            "shape, head, dtypes, info, isna, value_counts. Six commands, "
            "two minutes, and afterwards you can say what the file can and "
            "cannot answer. Each command is shown next to what you would "
            "have done in Excel and how long that would have taken.",
         b2="Selecting and filtering: one column, several columns, rows by "
            "condition, then two conditions and the brackets that are not "
            "optional. Then the failure everybody meets: a price column that "
            "arrived as text, and the sum that silently concatenates instead "
            "of adding.",
         lab="Online Retail II: a real file of 1,067,371 rows, which is more "
             "than a spreadsheet will open comfortably. Produce the "
             "six-command profile, then three sentences on what the file is "
             "a record of.",
         home="Profile a file from your own work, or a second sheet of the "
              "retail file, and write the three sentences. The sentences are "
              "harder than the code and they are the point.",
         trap="Reading a file and trusting the types. A column of numbers "
              "arriving as text is the commonest cause of a wrong answer in "
              "pandas, and nothing raises an error."),

    dict(n=8, week=3, tool="Python", title="Cleaning, and writing down what "
                                          "you did",
         roadmap="Data cleaning and preparation",
         outcomes=[
             "Find and handle duplicates, missing values, wrong types and "
             "mixed date formats.",
             "Justify each cleaning decision in writing, in a log somebody "
             "else could follow.",
             "Reconcile your cleaned total against a figure you already "
             "trust, and name the residual.",
         ],
         vocab=[
             ("Duplicate", "The same row recorded twice. Whether that is an "
                           "error depends entirely on the grain.", None),
             ("Cleaning log", "A table recording rows in, rows out, what "
                              "changed and why, written as you work.",
              None),
             ("Reconciliation", "Getting the same number two different ways "
                                "and chasing every difference until you can "
                                "name it.", None),
             ("Residual", "The difference that is left after you have "
                          "explained everything you can. Naming it is part "
                          "of the job.", None),
         ],
         b1="Seven defects, on data where the right answer is known: "
            "duplicate rows, returns recorded as negative quantities, one "
            "category priced in dollars, discounts typed as percentages, two "
            "date formats in one column, messy customer names, and missing "
            "customer ids. Each is found with two lines and fixed with two "
            "more.",
         b2="The decision, not the code, is the work. Dropping a row, "
            "filling a value and leaving it alone are three defensible "
            "choices with different consequences, and the choice belongs in "
            "writing beside the number. Then the log, and the reconciliation "
            "that catches the mistakes cleaning introduces.",
         lab="Clean the raw extract from rows-in to rows-out, keeping the log "
             "as you go. Your revenue total has a target. You will land just "
             "below it, and finding out why is the exercise.",
         home="Clean your own file, or the retail file, with a log. State "
              "one decision you are not sure about and why. Uncertainty "
              "written down is worth more than a confident wrong number.",
         trap="Cleaning until the number looks right. The log exists to make "
              "that visible, including to yourself."),

    dict(n=9, week=3, tool="Python", title="Grouping and joining in pandas",
         roadmap="pandas: groupby, merge; reconciling against SQL",
         outcomes=[
             "Reproduce any of your SQL aggregates in pandas and get the "
             "same number.",
             "Merge two frames and check the result rather than hoping.",
             "Explain a difference between two tools that should agree.",
         ],
         vocab=[
             ("groupby", "pandas' GROUP BY. Split the rows into groups, "
                         "apply an aggregation, combine the results.",
              "A pivot table"),
             ("Index", "The labels down the side of a DataFrame. After a "
                       "groupby your grouping keys are the index, not "
                       "columns, which is the commonest pandas confusion.",
              None),
             ("merge", "pandas' JOIN. The how argument is the join type.",
              "VLOOKUP"),
             ("validate", "An argument that makes pandas REFUSE a merge that "
                          "would multiply rows, instead of silently doing "
                          "it.", None),
         ],
         b1="groupby as split, apply, combine, said in those words and then "
            "shown. One key, several keys, several aggregations at once, "
            "named output columns, and reset_index, which is the four "
            "characters that turn a confusing result into a table.",
         b2="merge: the how argument against SQL's join types, indicator to "
            "see what matched, and validate to make pandas raise rather than "
            "fan out. Then the reconciliation: the same report from SQL and "
            "from pandas, set side by side, and every difference named.",
         lab="Rebuild session 5's rep revenue report in pandas and reconcile "
             "it against the SQL output row by row. This is Checkpoint 2. "
             "Finding a real difference and explaining it scores higher than "
             "a clean match you cannot account for.",
         home="Take one report somebody at work produces by hand every month "
              "and write the pandas that would produce it. It does not have "
              "to run yet.",
         check="Checkpoint 2: the reconciliation, and the cleaning log "
               "behind it.",
         trap="A merge that silently multiplies rows. validate turns that "
              "into an exception instead of a wrong number."),

    dict(n=10, week=4, tool="Statistics", title="Describing one column",
         roadmap="Descriptive statistics; distributions",
         outcomes=[
             "Say what a statistic is, and compute a mean, a median and a "
             "mode.",
             "Read a histogram and say which statistic the shape allows.",
             "Use percentiles to describe a business quantity honestly.",
         ],
         vocab=[
             ("Statistic", "One number that summarises many. Every statistic "
                           "throws information away, which is the point and "
                           "the danger.", None),
             ("Mean", "The total divided by the count.", "AVERAGE"),
             ("Median", "The middle value when you line them all up. Half "
                        "are smaller.", "MEDIAN"),
             ("Mode", "The commonest value. Useful on categories, where a "
                      "mean is meaningless.", "MODE"),
             ("Range", "Largest minus smallest.", "MAX minus MIN"),
             ("Distribution", "The shape you get when you count how many "
                              "values fall in each band.",
              "A histogram, or a frequency table"),
             ("Skew", "A distribution with a long tail on one side. Business "
                      "quantities nearly always have one.", None),
             ("Percentile", "The value below which a given share of the data "
                            "falls. The 90th percentile is bigger than nine "
                            "values in ten.", "PERCENTILE"),
             ("Outlier", "A value far from the rest. It may be an error and "
                         "it may be your biggest customer.", None),
         ],
         b1="What a statistic is, before any particular one: one number "
            "standing in for many, which always throws something away. Then "
            "mean, median and mode computed by hand on ten numbers on the "
            "board, so nobody is taking AVERAGE on faith, and then the same "
            "three in Excel and in pandas.",
         b2="Shape decides which statistic is honest. The distribution "
            "figure, then the real order values from the course data: mean "
            "well above median, a long tail, and a mean that is bigger than "
            "four orders in five. Percentiles as the fix, read off a number "
            "line.",
         lab="Describe three columns of the course data: pick the right "
             "statistic for each, draw the histogram, and write one sentence "
             "on why the mean would mislead on at least one of them.",
         home="Find a number quoted in your organisation and work out which "
              "statistic it is. If it is a mean, check whether the "
              "distribution justifies one.",
         trap="Reporting a mean on a skewed distribution. It is the single "
              "commonest misleading number in business reporting.",
         figs=["fig_distribution_shapes", "fig_skew_real",
               "fig_percentiles"]),

    dict(n=11, week=4, tool="Statistics",
         title="Comparing groups, and reading time",
         roadmap="Rates and proportions; time series basics",
         outcomes=[
             "Choose between a count and a rate, and say which question each "
             "answers.",
             "Use percentages and percentage points correctly.",
             "Separate a trend from a seasonal pattern.",
         ],
         vocab=[
             ("Rate", "A count divided by the population it came from. What "
                      "you need whenever the groups are different sizes.",
              None),
             ("Proportion and percentage", "A part of a whole. A percentage "
                                           "is a proportion times a "
                                           "hundred.", None),
             ("Percentage point", "The unit for the DIFFERENCE between two "
                                  "percentages. From 2% to 3% is one "
                                  "percentage point and a 50% increase, and "
                                  "both are true.", None),
             ("Time series", "Values recorded in time order.", None),
             ("Trend", "The direction over the long run, once the wobble is "
                       "taken out.", None),
             ("Seasonality", "A pattern that repeats on the calendar. "
                             "December here is not growth.", None),
             ("Moving average", "The average of the last few periods, used "
                                "to see the trend through the noise.",
              None),
             ("Year on year", "Comparing a period against the same period a "
                              "year earlier, which is the honest way to see "
                              "through seasonality.", None),
         ],
         b1="Counts against rates, on the returns data where the two "
            "disagree: one region has the most returns and another has the "
            "highest rate, and they call for different actions. Then "
            "percentages, and percentage points, which get confused in "
            "public by people who should know better.",
         b2="Time. Resample to a month, then a moving average, then the "
            "question that matters: is this growth or is it the calendar? "
            "December against February in both years, and year on year as "
            "the test. Same data, two arithmetics, opposite headlines.",
         lab="Five statements about this business, each of which sounds "
             "plausible. Decide which are supported, which are unsupported "
             "and which are unanswerable, and attach a number to every "
             "verdict.",
         home="Find a percentage quoted at work and decide whether it should "
              "have been a percentage point, a rate, or a count.",
         trap="Reporting a count where the audience will read a rate, and "
              "calling a seasonal peak growth.",
         figs=["fig_rate_vs_count", "fig_seasonality"]),

    dict(n=12, week=4, tool="Charts", title="Charts that answer the question",
         roadmap="Data visualisation; choosing the right chart",
         outcomes=[
             "Name the parts of a chart, and pick the chart a question "
             "implies.",
             "Label a chart so it can be read without you standing next to "
             "it.",
             "Name what your own chart hides.",
         ],
         vocab=[
             ("Axis", "The scale down the side or along the bottom. Every "
                      "axis needs a label and a unit.", None),
             ("Data series", "One set of values drawn together: one line, "
                             "one set of bars.", None),
             ("Categorical and continuous", "Categories are named groups; "
                                            "continuous values are measured "
                                            "numbers. They need different "
                                            "charts.", None),
             ("Histogram", "A chart of a distribution: values in bands along "
                           "the bottom, counts up the side. Not a bar "
                           "chart.", None),
             ("Truncated axis", "A value axis that does not start at zero, "
                                "which makes a small change look enormous.",
              None),
             ("Annotation", "A note on the chart itself, pointing at the "
                            "thing you want seen.", None),
         ],
         b1="The anatomy figure first: every part of a chart named, because "
            "you cannot be told to label an axis if nobody has said which "
            "part is the axis. Then the four charts and the question each "
            "answers: line for change over time, bar for comparison, "
            "histogram for a distribution, scatter for a relationship.",
         b2="Honesty and its opposite, each shown beside its corrected "
            "version: the truncated axis, the dual axis, the pie chart with "
            "eleven slices, the bar chart sorted alphabetically. Then the "
            "title rule, which is the whole session in one line: the title "
            "states the finding. And the question asked of every chart from "
            "here on, which is what it does not show.",
         lab="Three charts answering three of the questions from week one. "
             "Each titled with its finding, each with labelled axes and "
             "units, and each with one sentence underneath naming what it "
             "hides.",
         home="Take a chart from a report you receive and redraw it so the "
              "title states its finding. Bring both versions.",
         trap="Titling a chart 'Revenue by month'. That is the axes read "
              "aloud, and it leaves the reader to do the work you were paid "
              "to do.",
         figs=["fig_chart_anatomy", "fig_four_charts", "fig_axis_honesty"]),

    dict(n=13, week=5, tool="Investigation",
         title="A whole investigation, end to end",
         roadmap="Exploratory data analysis; the write-up",
         outcomes=[
             "Run a structured investigation on an unfamiliar dataset, in a "
             "fixed order.",
             "Produce five findings, each with a number and a stated "
             "limitation.",
             "Write the half page a decision maker reads instead of the "
             "notebook.",
         ],
         vocab=[
             ("Finding", "A sentence with a number in it that somebody could "
                         "act on or dispute.", None),
             ("Observation", "Something true about the data rather than "
                             "about the business. It belongs in the "
                             "notebook.", None),
             ("Limitation", "Where a finding stops being reliable, written "
                            "beside it rather than in a footnote.", None),
             ("Leakage", "When a column you would not have at decision time "
                         "is used to answer the question, making the answer "
                         "look far better than it is.", None),
         ],
         b1="The routine, written up and followed live on a dataset nobody "
            "has seen: what is this file a record of, what is one row, what "
            "is the window, what is missing, what does the main quantity "
            "look like, what moves with what, and what would change my mind.",
         b2="From notebook to finding. Eleven observations become five "
            "findings by striking anything about the data rather than the "
            "business, merging duplicates, and ranking what is left by what "
            "somebody could do about it. Then the limitation beside each one.",
         lab="Run the routine on the sector dataset you chose: banking and "
             "telecom, energy and manufacturing, or public sector and "
             "health. Five findings with numbers. This is the mid-track "
             "assessment and it is marked on the findings, not the code.",
         home="Finish and submit the investigation: half a page of findings "
              "plus the notebook behind it.",
         check="Mid-track assessment: five findings on a sector dataset.",
         trap="A notebook with forty cells and no conclusion. The routine "
              "exists to stop exactly that."),

    dict(n=14, week=5, tool="Power BI", title="Getting data in, and modelling "
                                              "it",
         roadmap="BI tools: loading, transformation, data modelling",
         outcomes=[
             "Load several tables and clean them in Power Query without "
             "touching the source.",
             "Build a star schema whose totals are correct.",
             "Check a dashboard total against a number you already trust.",
         ],
         vocab=[
             ("Power Query", "The part of Power BI that gets the data and "
                             "shapes it. Its Applied Steps list is a recipe "
                             "that runs again next month.", None),
             ("Data model", "The tables plus the relationships between them. "
                            "This is what decides whether a total is right.",
              None),
             ("Relationship", "A join defined once in the model rather than "
                              "written in every query.", None),
             ("Star schema", "One fact table in the middle, dimension tables "
                             "around it.", None),
             ("Fact and dimension", "The fact table holds the events; "
                                    "dimensions hold the descriptions you "
                                    "slice by.", None),
             ("Date table", "A separate table with one row per date. Without "
                            "one, your months sort alphabetically.", None),
         ],
         b1="Power BI is three products people confuse: Power Query gets and "
            "shapes, the model relates, the report shows. Get Data from CSV, "
            "then Power Query: promote headers, set types, trim, remove "
            "duplicates. The Applied Steps list as the same idea as the "
            "cleaning log from session 8.",
         b2="The model, which is where the marks are. The star schema figure, "
            "then five relationships built by hand after deleting every one "
            "Power BI guessed. A deliberately wrong relationship first, so "
            "the wrong total is seen before the rule is stated. Then the "
            "date table, and marking it.",
         lab="Load the course data, build the model, and produce three "
             "visuals whose totals match the numbers you already got in SQL "
             "and in pandas. Matching is the mark.",
         home="Add the Uganda Healthsites file and put a map visual on it. "
              "Notice what that file makes easy and what it makes "
              "impossible.",
         trap="Trusting the relationships Power BI detects for you. Check "
              "every direction, then check a total against a number you "
              "already trust.",
         note="Power BI Desktop is Windows only. Mac participants work in "
              "the browser Service throughout, loading CSVs they have "
              "already cleaned in pandas; the lab gives both paths and names "
              "the three things the browser cannot do.",
         figs=["fig_star_schema"]),

    dict(n=15, week=5, tool="Power BI",
         title="Measures, a dashboard, and presenting it",
         roadmap="BI tools: DAX basics, dashboards; reporting and "
                 "storytelling",
         outcomes=[
             "Write a measure, and say why it is not a column.",
             "Lay out a dashboard for somebody who will look at it for "
             "thirty seconds.",
             "Present an analysis in five minutes and take a hard question.",
         ],
         vocab=[
             ("Measure", "A calculation worked out when a visual asks for "
                         "it, inside that visual's filters.",
              "A pivot table value field"),
             ("Calculated column", "A calculation worked out once per row "
                                   "when the data loads, and then fixed.",
              "A formula column"),
             ("Filter context", "The filters in force where a measure is "
                                "evaluated: the row, the slicer, the chart "
                                "axis.", None),
             ("DAX", "The formula language Power BI measures are written in.",
              None),
             ("Slicer", "An on-page filter the reader can change.",
              "A pivot table filter"),
             ("Recommendation", "What somebody should do, with the number "
                                "that justifies it and the conditions under "
                                "which it stops being true.", None),
         ],
         b1="Three measures and one rule: a measure is evaluated in the "
            "filter context of whatever asked for it, which is why it is not "
            "a column. SUM, DIVIDE instead of the division operator, and "
            "CALCULATE to change the filter. Each checked against a figure "
            "from week two.",
         b2="Design for thirty seconds: the number they came for top left, "
            "no more than five visuals, one accent colour, one slicer, and a "
            "title that states the finding. Then the five-minute "
            "presentation structure: the question, the answer with its "
            "number, how you know, what you traded, and what would change "
            "your answer.",
         lab="Finish the dashboard, then present. Five minutes each plus "
             "questions from the room, and everybody asks at least one "
             "question of somebody else. Then twenty minutes on the one "
             "report you will replace at work this month.",
         home="None. Send the dashboard to the person who asked the question "
              "in week one.",
         check="Capstone: dashboard, one page, five-minute presentation.",
         trap="A dashboard with fourteen visuals and no answer, presented "
              "method first. Nobody outside the room cares which library you "
              "used.",
         note="With more than about fourteen participants, five minutes each "
              "will not fit alongside the dashboard clinic. Either run the "
              "presentations in two parallel groups with a second marker, or "
              "add a sixteenth session."),
]
assert len(SESSIONS) == 15
assert [s["n"] for s in SESSIONS] == list(range(1, 16))

# ---------------------------------------------------------------- assessment
ASSESSMENT = [
    ("Checkpoint 1 — the rep revenue report", 15, "Session 5",
     "One SQL query with three named steps, marked against the answer key. "
     "Either the numbers match or they do not, so feedback is immediate."),
    ("Checkpoint 2 — reconciliation and cleaning log", 15, "Session 9",
     "The same report in pandas, reconciled against the SQL, with the log "
     "that makes the starting numbers reproducible. Marked on the log as "
     "much as the answer."),
    ("Mid-track investigation", 30, "Session 13",
     "Five findings on a sector dataset, each with a number, a chart and a "
     "stated limitation. Marked on the findings, not the code."),
    ("Capstone", 40, "Session 15",
     "A dashboard whose totals reconcile, one page of recommendation, and "
     "five minutes in front of the room. Marked on whether a decision maker "
     "could act on it."),
]
assert sum(w for _, w, _, _ in ASSESSMENT) == 100

# ---------------------------------------------------------------- tool split
TOOL_HOURS = {"Foundations": 6, "SQL": 9, "Python": 12, "Statistics": 6,
              "Charts": 3, "Investigation": 3, "Power BI": 6}
assert sum(TOOL_HOURS.values()) == TOTAL_HOURS

# Statistics, charts and the investigation are all taught IN Python, so the
# Python total is 24 of the 45 hours. The verifier checks that against SQL
# and Power BI, because "Python-heavy" was a requirement rather than a
# preference.
PYTHON_FAMILY = ("Python", "Statistics", "Charts", "Investigation")
PYTHON_HOURS = sum(TOOL_HOURS[k] for k in PYTHON_FAMILY)
assert PYTHON_HOURS == 24

# --------------------------------------------------------------- what was cut
# Funded the foundations. Written down so it does not creep back in.
CUT = [
    ("SQL window functions",
     "RANK, running totals and PARTITION BY. They are the right tool for "
     "the rep report's ranking, and they are a session's worth of new ideas "
     "for somebody who met their first SELECT eight days earlier. The report "
     "now stops at revenue net of returns, and the ranking is done in the "
     "spreadsheet where the room is already fluent."),
    ("DAX time intelligence",
     "TOTALYTD and its relatives. They need a correctly marked date table "
     "and an understanding of filter context, and getting either wrong "
     "returns a plausible wrong number silently. Session 15 teaches SUM, "
     "DIVIDE and CALCULATE properly instead."),
    ("Reshaping: pivot_table and melt in pandas",
     "Wide against long is a genuinely useful idea and it is the third way "
     "of saying something the room has already met as a pivot table and as "
     "GROUP BY. Cut to make room, and named here because it is the first "
     "thing to add back if a cohort moves quickly."),
    ("Row-level security in Power BI",
     "Mentioned in one line in session 15 as a thing that exists, because a "
     "beginner who publishes a dashboard needs to know the concept is out "
     "there. Not taught."),
]

# ---------------------------------------------------------------- departures
DEPARTURES = [
    ("Excel is assumed, not taught",
     "The roadmap.sh path starts with spreadsheets. This room already has "
     "them: everybody arrives able to build a pivot table and write a "
     "VLOOKUP. So Excel is the ANCHOR rather than a topic. Every new idea "
     "arrives beside the spreadsheet equivalent, and sessions 4 and 9 "
     "deliberately produce the same answer both ways so the room can see "
     "that the new tool is doing something they already understand."),
    ("Two full sessions before any code",
     "Sessions 1 and 2 are vocabulary, grain and keys, with no SQL and no "
     "Python. It looks slow and it is the reason the rest is not. Nearly "
     "every wrong total later in the course comes from a grain nobody "
     "stated, and six hours spent on that at the start is cheaper than "
     "debugging it in week four."),
    ("Statistics gets two sessions, placed after cleaning",
     "The roadmap puts statistics early. Before any real data it does not "
     "stick, because nobody yet has a distribution they care about. "
     "Sessions 10 and 11 arrive when participants have cleaned their own "
     "file and have a skewed revenue column in front of them, and they "
     "start from what a statistic IS rather than from a formula."),
    ("No machine learning",
     "It is on the roadmap's later branches and it is not on this one. "
     "Forty-five hours buys either a competent analyst or a bad modeller. "
     "Session 15 says where to go next for the other thing."),
]

# ---------------------------------------------------------------- logistics
KIT = [
    ("Excel or any spreadsheet",
     "Already on their machines, and used in sessions 1, 4 and 9 as the "
     "thing everything else is explained against."),
    ("Python", "Anaconda, or Google Colab in a browser if the laptop is "
               "locked down by an employer. Colab needs no install and is "
               "the fallback for anybody who arrives blocked."),
    ("SQL", "DB Browser for SQLite. Free, Windows and Mac, no server, and it "
            "opens the course database by double-clicking it. Session 2 uses "
            "only its Browse Data tab, with no SQL at all."),
    ("Power BI", "Power BI Desktop on Windows, free. Mac participants use "
                 "the browser Service: it cannot give them the full Power "
                 "Query editor, local file refresh, or the SQLite "
                 "connector, so the week five labs give both paths."),
    ("The data", "One folder, handed out in session 1 on a USB stick as well "
                 "as a link. The room's network is not a dependency."),
]

ROOM = [
    ("Session length", "Three hours, evening or weekend. Two breaks, both "
                       "taken."),
    ("Group size", "Twelve to twenty. Above twenty the lab stops working, "
                   "because the instructor cannot reach everybody in fifty "
                   "minutes. Above fourteen, session 15 needs a second "
                   "marker or a sixteenth session for the presentations."),
    ("Between sessions", "One homework of 45 to 60 minutes, always with the "
                         "option to do it on the participant's own work "
                         "data, which is what makes it get done."),
    ("What is on the screen", "The instructor types everything live. Nothing "
                              "is pasted from a finished notebook, because "
                              "the errors are half the teaching."),
    ("Vocabulary", "Every session opens with its three to eight new terms, "
                   "defined in plain language with the Excel equivalent "
                   "where there is one. The glossary handout is the union of "
                   "those lists, and it is printed once and kept."),
]


# ------------------------------------------------------------------ glossary
def glossary():
    """Every term the track defines, in one alphabetical list.

    Built from the sessions rather than maintained separately, so a term
    cannot be taught without reaching the handout, and the handout cannot
    drift from what was taught. Returns (term, definition, excel, session).
    """
    out = {}
    for s in SESSIONS:
        for term, definition, excel in s.get("vocab", []):
            if term in out:
                raise KeyError("term %r defined twice, in sessions %d and %d"
                               % (term, out[term][3], s["n"]))
            out[term] = (term, definition, excel, s["n"])
    return [out[k] for k in sorted(out, key=lambda t: t.lower())]


GLOSSARY = glossary()
