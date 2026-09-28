# -*- coding: utf-8 -*-
"""Week 1 slide content: sessions 1, 2 and 3.

Two foundation sessions with no code at all, then the first SQL. The room is
confident in Excel and has never programmed, so every new idea arrives beside
the spreadsheet thing it replaces.

Placeholders use the angle-bracket form because slides carry Python dicts and
f-strings, both of which contain braces.
"""
import da_keys as D

DECKS = {}

# ============================================================== SESSION 1
DECKS[1] = dict(
    b1_title="What you were asked, and what you can answer",
    b2_title="The words, on a real table",

    question=("THE QUESTION TONIGHT ANSWERS",
              "What is the difference between what you were asked\n"
              "and what you can actually answer?",
              "Most bad analysis is not a technique failure. It is a "
              "correct answer to a question nobody asked."),

    points=[("Four requests, as they actually arrive",
             [("\"Can you look at the sales numbers?\"",
               "Which sales, over what period, compared with what? Three "
               "people asking this want three different things."),
              ("\"Why are sales down?\"",
               "Are they? Down against last month, last year, or budget? "
               "Down in shillings or in units? The question assumes its own "
               "answer."),
              ("\"Send me a dashboard.\"",
               "A dashboard is a delivery format. Nobody wants one. They "
               "want to stop asking somebody for a number every Monday."),
              ("\"How many customers do we have?\"",
               "The easiest-looking one and the worst. Customers on our "
               "books, customers who bought this year, or customers who owe "
               "us money? Three numbers from one table.")],
             "REQUESTS"),

            ("You are not starting from nothing",
             [("You already know what a row is",
               "You have sorted one, filtered one and deleted one by "
               "accident. Tonight it gets a second name, RECORD, and that "
               "is most of what changes."),
              ("You already write code",
               "=IF(B2>1000,\"large\",\"small\") is a function with three "
               "arguments: a condition and two possible results. Session 6 puts the "
               "brackets somewhere else."),
              ("You already do joins",
               "VLOOKUP is a join. It has one behaviour that differs from a "
               "real join, and in session 2 that difference is the whole "
               "lesson."),
              ("You already aggregate",
               "A pivot table is GROUP BY. Session 4 is your pivot table, "
               "written down so it runs again next month without you.")],
             "WHAT YOU BRING")],

    concepts=[("An answerable question",
               "A question with three things attached: a NUMBER you will "
               "produce, a POPULATION it covers, and a TIME WINDOW. Without "
               "all three, two people can agree on the answer and still "
               "disagree about what it meant.",
               "Not \"why are sales down\" but \"was delivered revenue in "
               "October to December 2025 lower than the same quarter a year "
               "earlier, across all four regions, in shillings?\" That has "
               "an answer, and you can be shown to be wrong.",
               "A KPI. A KPI is a number somebody watches. A question is "
               "something you can be wrong about, and this course is about "
               "the second kind."),

              ("Grain",
               "What one row of a table represents. It is the single most "
               "important fact about any table and the one nobody states "
               "out loud.",
               "In orders, one row is one order: <<orders>> rows. In "
               "order_items, one row is one product on one order: "
               "<<items>> rows. Same business, same two years, two "
               "different tables, and a number that is right in one and "
               "wrong in the other.",
               "Row count. Two tables about the same thing can have very "
               "different row counts and both be complete. What differs is "
               "the grain."),

              ("Data type",
               'A column’s intended type: integer, decimal, text, date or Boolean. Check imported values.',
               "order_date is a date, so the database can sort it, subtract "
               "one from another and pull the month out. If it were text, "
               "\"2025-03-10\" and \"10/03/2025\" would be two unrelated "
               "pieces of text and none of that would work.",
               "Cell formatting. Formatting changes how a value LOOKS. A "
               "type changes what the value IS, and the software will "
               "refuse to break it.")],

    b1_figs=[],
    b2_figs=[("fig_table_anatomy",
              "One table. Five words you will hear all term.",
              "The first five real rows of orders.csv. Everything you "
              "already know about a spreadsheet still applies; the words "
              "change and one new idea, the primary key, arrives.")],

    splits=[("What you are working with for five weeks",
             "Riverside Distributors",
             "A wholesale distributor. Six tables, two years of trading, "
             "and it behaves like a real system because it was built to.\n\n"
             "<<orders>> orders, <<items>> order lines, <<customers>> "
             "customers, <<products>> products, <<reps>> sales reps, "
             "<<returns>> returns.\n\n"
             "Small enough that you can check it by hand, which is why you "
             "will trust what you learn on it.",
             "By the end of tonight",
             ["The data open on your own machine, in a spreadsheet.",
              "",
              "Six sentences: what one row is, in each of the six files.",
              "",
              "Three requests rewritten as answerable questions.",
              "",
              "One question from your own work, written down. It is a "
              "capstone candidate."],
             "THE DATASET")],

    prose=[("How the five weeks go",
            ["**Week 1 — the words, and getting the data**",
             "Tonight and next session have no code at all. Then your first "
             "SQL, which is a written-down filter.",
             "**Week 2 — SQL, then your first program**",
             "Grouping, joining, and the report a sales manager would "
             "actually ask for. Then Python from the beginning.",
             "**Week 3 — Python on real files**",
             "Read a file too big for Excel, clean it without destroying "
             "it, and get the same answer as your SQL.",
             "**Week 4 — what the numbers mean**",
             "Statistics from what a statistic is. Then charts, from what "
             "an axis is.",
             "**Week 5 — shipping it**",
             "A full investigation, then Power BI, then five minutes in "
             "front of the room."],
            "THE SHAPE", 2)],

    check=(["Your manager says the Eastern region is underperforming. What "
            "three things are missing before that is answerable?",
            "Somebody asks how many customers we have. Name two defensible "
            "answers that differ.",
            "orders has <<orders>> rows and order_items has <<items>>. Is "
            "one of them incomplete?"],
           [("\"The Eastern region is underperforming\"",
             "A number, a population and a window. Underperforming on what "
             "measure, against which comparison, over what period. As it "
             "stands it is a conclusion with no question underneath it."),
            ("Two answers to \"how many customers\"",
             "Everyone in the customers table, which is <<customers>> here, "
             "or everyone who placed an order in a given window, which is "
             "smaller. Both are right. Which one was wanted is the question "
             "you have to go and ask."),
            ("Different row counts in two tables",
             "No. They have different GRAIN. One row of orders is one "
             "order; one row of order_items is one product on one order. "
             "Both tables are complete, and a total computed on the wrong "
             "one is wrong.")]),

    lab=("Say what one row is, six times",
         "Open the six course files in your spreadsheet. For each one, write "
         "down three things: what one row represents in a single sentence, "
         "how many rows there are, and which column could never repeat. "
         "Then take the three requests on your sheet and turn each into an "
         "answerable question.",
         ["One row of this file is ___ .",
          "How many rows? Write the number down.",
          "Which column never repeats? That is the primary key.",
          "Which column points at another table?",
          "Then: the three requests, rewritten with a number, a population "
          "and a window."]),

    closing=("You now have a question, and the words to describe the data",
             "Everything from here is technique, and technique is teachable "
             "in five weeks. Knowing what you are being asked, and what one "
             "row means, is the part that separates an analyst from somebody "
             "who produces charts.",
             "Next session: why the data is in six tables and not one. "
             "Still no code."),
)

# ============================================================== SESSION 2
DECKS[2] = dict(
    b1_title="Why not one big sheet",
    b2_title="Grain, keys, and what a join does",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Why is this data in six tables\n"
              "instead of one big sheet?",
              "Because one big sheet stores the same fact many times, and "
              "every copy is a chance to be wrong."),

    concepts=[("Primary key",
               "A column whose value is never repeated, so it identifies "
               "exactly one row. Every proper table has one.",
               "customer_id in the customers table. There is one row for "
               "customer 1007 and there will never be another.",
               "A row number. A row number changes when you sort. A primary "
               "key belongs to the thing itself and never moves."),

              ("Foreign key",
               "A column that holds another table's primary key. It is what "
               "connects the two tables.",
               "orders.customer_id holds a value from customers.customer_id. "
               "That one column is the whole connection, and <<walkins>> "
               "orders leave it empty because walk-in trade has no "
               "customer.",
               "The lookup value you type into VLOOKUP. Same idea, except "
               "the database can refuse a value that does not exist."),

              ("One-to-many",
               "One row on one side matches several rows on the other. It "
               "is the commonest relationship in business data and the "
               "reason totals go wrong.",
               "One order has several order lines. One customer has many "
               "orders. One rep has many customers. <<orders>> orders "
               "become <<items>> order lines.",
               None)],

    points=[("What goes wrong with one big sheet",
             [("The same fact, stored many times",
               "A customer's region appears on every one of their orders. "
               "One customer, dozens of copies of one fact."),
              ("Every copy is a chance to disagree",
               "The customer moves region. Now you edit dozens of rows, and "
               "the ones you miss are still there, still wrong, still being "
               "summed."),
              ("You cannot record something that has not happened",
               "A customer who has not ordered this year has no row at all, "
               "so they are invisible to every total. The thing you most "
               "want to know is the thing the sheet cannot hold."),
              ("Six tables fix all three",
               "Each fact is stored once, in the table it belongs to. A "
               "region change is one edit. A customer with no orders still "
               "exists.")],
             "THE PROBLEM")],

    b1_figs=[("fig_grain",
              "The same business, two different grains",
              "Left: one row is one order. Right: one row is one order "
              "line, so an order appears more than once. Both are real rows "
              "from the course data. The caption is the number to remember.")],

    b2_figs=[("fig_join",
              "What a join does, and what an INNER JOIN quietly throws away",
              "Real counts from the course data. The INNER JOIN loses the "
              "<<walkins>> walk-in orders because they have no customer to "
              "match, and nothing in the output says so."),
             ("fig_star_schema",
              "The six tables, and how they connect",
              "You will build exactly this in Power BI in session 14. "
              "Tonight you only need to see that the arrows all point the "
              "same way: many orders to one customer.")],

    splits=[("Tonight's lab has no SQL in it",
             "DB Browser, Browse Data tab",
             "You will click, not type. Open riverside.db, go to Browse "
             "Data, and use the dropdown to look at each of the six "
             "tables.\n\n"
             "The point is to get the SHAPE of this business into your head "
             "before any syntax arrives. Next session the typing starts, "
             "and it is much easier when you already know what is in "
             "there.",
             "For each of the six tables",
             ["What is the grain? One row is one what?",
              "",
              "What is the primary key?",
              "",
              "Which columns point at another table?",
              "",
              "Then find an order with no customer_id, and write down what "
              "you think that means about how this business trades."],
             "LAB · NO TYPING")],

    check=(["A customer moves from Central to Eastern. How many edits in "
            "one big sheet, and how many in six tables?",
            "orders.customer_id is empty on <<walkins>> rows. Is that a "
            "data error?",
            "You join orders to order_items. Will the result have more "
            "rows, fewer, or the same?"],
           [("One edit or many",
             "One edit in the customers table. In a flat sheet, one edit "
             "per order that customer ever placed, and the ones you miss "
             "stay wrong and keep being summed."),
            ("Empty customer_id on <<walkins>> orders",
             "No. It is walk-in trade: a real order with real revenue and "
             "no customer recorded. It becomes an error only if somebody "
             "joins to customers without noticing, which silently removes "
             "<<walkin_rev>> from the answer."),
            ("Row count after joining orders to lines",
             "More. It is one-to-many, so each order appears once per line: "
             "<<orders>> becomes <<items>>. That is correct, and summing an "
             "order-level figure on that result is not.")]),

    lab=("Map the six tables by clicking",
         "No SQL tonight. In DB Browser's Browse Data tab, work through all "
         "six tables and fill in the sheet: grain, primary key, foreign "
         "keys. Then draw the six boxes and the arrows between them on "
         "paper. Drawing it by hand is what makes it stick.",
         ["Grain of each table: one row is one what?",
          "Primary key of each table.",
          "Every column that points at another table.",
          "Draw the six boxes and the arrows, on paper.",
          "Find an order with no customer and say what it means."]),

    closing=("Say the grain out loud, every time",
             "Nearly every wrong total in the rest of this course comes from "
             "a grain nobody stated. Two sessions with no code buys you that "
             "habit, and it is the cheapest thing you will learn here.",
             "Next session: the same tables, and your first query."),
)

# ============================================================== SESSION 3
DECKS[3] = dict(
    b1_title="A query is a written-down filter",
    b2_title="Nothing, zero, and blank are three different things",

    question=("THE QUESTION TONIGHT ANSWERS",
              "How do you ask a database for exactly the rows you want,\n"
              "and know that you got them?",
              "Every clause you add changes the row count. The row count is "
              "how you check yourself."),

    concepts=[("A query",
               "A written description of the rows you want. You describe the "
               "result and the database works out how to fetch it, which is "
               "why SQL has outlived every tool built on top of it.",
               "SELECT region, city FROM customers WHERE region = 'Eastern' "
               "ORDER BY city LIMIT 10;",
               "Autofilter plus sort. Same result, except this one is "
               "written down, so it runs again next month and somebody else "
               "can check what you did."),

              ("NULL",
               "No value recorded. It is not zero and it is not an empty "
               "piece of text. Any comparison with NULL is neither true nor "
               "false, so a filter written with = NULL matches nothing at "
               "all.",
               "<<walkins>> of the <<orders>> orders have no customer_id. "
               "Find them with IS NULL. Written as = NULL you get zero rows, "
               "no error and no warning, and zero looks like a fact.",
               "Zero. A credit limit of 0 means we checked and they get "
               "nothing. A credit limit of NULL means nobody has looked "
               "yet. Summing them treats both as nothing, which is wrong "
               "about one of them.")],

    code=[("Build it one clause at a time, watching the row count",
           "DB BROWSER · EXECUTE SQL",
           "-- run each of these and note the row count\n"
           "SELECT * FROM orders;                     -- <<orders>> rows\n"
           "\n"
           "SELECT * FROM orders\n"
           "WHERE status = 'Delivered';               -- <<delivered>>\n"
           "\n"
           "SELECT order_id, order_date, channel\n"
           "FROM orders\n"
           "WHERE status = 'Delivered'\n"
           "  AND order_date >= '2025-01-01'\n"
           "ORDER BY order_date DESC\n"
           "LIMIT 10;                                 -- 10 rows",
           "Now change 'Delivered' to 'delivered', lower case. Zero rows. "
           "Text comparison is case sensitive here, and a filter that "
           "matches nothing looks exactly like a fact about the business."),

          ("The one that catches everybody",
           "DB BROWSER · EXECUTE SQL",
           "SELECT COUNT(*)           AS rows_in_table,\n"
           "       COUNT(customer_id) AS rows_with_a_customer\n"
           "FROM orders;\n"
           "\n"
           "-- <<count_star>> and <<count_col>>. The gap is <<walkins>>.\n"
           "-- COUNT(*) counts ROWS.\n"
           "-- COUNT(column) counts rows where that column is NOT NULL.\n"
           "\n"
           "SELECT COUNT(*) FROM orders WHERE customer_id IS NULL;",
           "Try the last line with = NULL instead of IS NULL. Zero rows, no "
           "error. In Excel you would have SEEN the blanks; here nothing "
           "shows you, which is why this is worth half an hour."),
          ],

    worked=("Your first real answer, in four steps",
            "How much revenue did we take on delivered orders? Revenue is "
            "not a column: it is quantity times price times one minus "
            "discount, and it lives on the order lines.",
            ["Count the order lines, so you have a number to check "
             "everything against: <<items>>.",
             "Total the line values with no filter at all: <<rev_all>>. "
             "This counts orders nobody paid for, so it is not the answer.",
             "Join to orders so you can see the status. Check the row count "
             "did not move: still <<items>>.",
             "Filter to delivered: <<rev_delivered>>. The difference, "
             "<<cancelled_gap>>, was sitting in pending and cancelled "
             "orders."],
            "From now on, every revenue figure in this course says which "
            "statuses it counts. \"Revenue\" on its own is not an answer."),

    check=(["What is the difference between COUNT(*) and COUNT(city)?",
            "Why does WHERE customer_id = NULL return nothing?",
            "Somebody gives you a revenue figure. What is the first "
            "question you ask?"],
           [("COUNT(*) against COUNT(city)",
             "COUNT(*) counts rows. COUNT(city) counts rows where city is "
             "not NULL. On orders that difference is <<walkins>> rows, "
             "worth <<walkin_rev>>."),
            ("Why = NULL matches nothing",
             "Because NULL means no value, and comparing anything with no "
             "value is neither true nor false. The filter is never "
             "satisfied. IS NULL is a different test and it works."),
            ("The first question about any revenue figure",
             "Which orders does it count? Delivered only is "
             "<<rev_delivered>>; everything is <<rev_all>>. The gap is "
             "<<cancelled_gap>>, and nobody can tell which you meant "
             "from the number alone.")]),

    lab=("Eight questions against the database",
         "Work them in order; they get harder. Every question has its "
         "answer on the sheet, so you know within seconds whether you are "
         "right. Write the query before you look at the answer: reading it "
         "first feels like learning and is not.",
         ["How many orders, and how many were delivered?",
          "Which sales channel is used most?",
          "Which customer segments have more than 80 customers?",
          "Total revenue, before any filtering.",
          "Revenue on delivered orders only.",
          "How many orders have no customer, and what are they worth?"]),

    closing=("Check the row count after every clause",
             "It is the cheapest habit in this course and it catches most "
             "wrong answers before they leave your screen. A number that "
             "moved when you did not expect it to is telling you something "
             "you need to know.",
             "Next session: your pivot table, written down."),
)

# --------------------------------------------------------------- formatting
# Placeholders live in da_keys.FMT_BASE, in one place, because sessions
# move between these modules and a private copy goes stale.
FMT = {}
