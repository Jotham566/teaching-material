# -*- coding: utf-8 -*-
"""Week 2 slide content: sessions 4, 5 and 6.

Two more SQL sessions, then Python from the beginning. Session 4 is
deliberately framed as "your pivot table, written down", because the room can
already do it and only needs the vocabulary.
"""
import da_keys as D

DECKS = {}

# ============================================================== SESSION 4
DECKS[4] = dict(
    b1_title="Your pivot table, written down",
    b2_title="Filtering groups, and the trap in every average",

    question=("THE QUESTION TONIGHT ANSWERS",
              "You can already build a pivot table.\n"
              "What does writing it down buy you?",
              "It runs again next month without you, somebody else can "
              "check it, and it works on files a spreadsheet will not "
              "open."),

    concepts=[("Aggregate",
               "A calculation that collapses many rows into one number: "
               "count, sum, average, minimum, maximum.",
               "SUM over <<items>> order lines gives one revenue figure. "
               "COUNT over <<orders>> orders gives one number. The rows go "
               "in; one value comes out.",
               "The value area of a pivot table. Exactly the same thing, "
               "and you have been doing it for years."),

              ("GROUP BY",
               "Says which rows belong together before the aggregate runs. "
               "Group by region and you get one number per region.",
               "GROUP BY channel gives one row per channel. GROUP BY "
               "channel, status gives one row per combination, which is a "
               "two-level pivot.",
               "The Rows area of a pivot table. Drag region in there and "
               "you have written GROUP BY region."),

              ("HAVING",
               "A filter on the GROUPS, applied after the aggregation. "
               "WHERE filters rows before grouping; HAVING filters the "
               "results afterwards.",
               "WHERE status = 'Delivered' throws away rows. HAVING "
               "COUNT(*) > 80 throws away whole groups, and you cannot do "
               "it with WHERE because at that point no count exists yet.",
               "Filtering a pivot table on its totals rather than on the "
               "source rows."),

              ("Derived value",
               "A number the data does not store, computed from columns "
               "that it does.",
               "Revenue is derived: quantity x unit_price x (1 - discount). "
               "There is no revenue column anywhere in this database, and "
               "there should not be, because a stored total goes stale the "
               "moment a line changes.",
               "A formula column. The difference is that yours is computed "
               "fresh every time the query runs.")],

    code=[("The same answer, both ways",
           "DB BROWSER · EXECUTE SQL",
           "-- build this, then build the same thing as a pivot table\n"
           "-- from orders.csv, and check they agree\n"
           "SELECT channel,\n"
           "       COUNT(*)                AS orders,\n"
           "       COUNT(customer_id)      AS with_a_customer\n"
           "FROM orders\n"
           "WHERE status = 'Delivered'\n"
           "GROUP BY channel\n"
           "ORDER BY orders DESC;",
           "Add ORDER BY orders DESC and remove it again. Note that you can "
           "sort by a number you just computed and named, which a pivot "
           "table makes you click three times to do."),

          ("Revenue, which is not a column",
           "DB BROWSER · EXECUTE SQL",
           "SELECT c.segment,\n"
           "       ROUND(SUM(oi.quantity * oi.unit_price_ugx\n"
           "                 * (1 - oi.discount))) AS revenue_ugx,\n"
           "       COUNT(DISTINCT o.order_id)       AS orders\n"
           "FROM order_items oi\n"
           "JOIN orders    o ON o.order_id    = oi.order_id\n"
           "JOIN customers c ON c.customer_id = o.customer_id\n"
           "WHERE o.status = 'Delivered'\n"
           "GROUP BY c.segment\n"
           "ORDER BY revenue_ugx DESC;",
           "Change COUNT(DISTINCT o.order_id) to COUNT(*) and the order "
           "count jumps, because there is one row per LINE and not per "
           "order. Same query, same data, and now the average order value "
           "underneath it is wrong by a factor of three."),

          ("HAVING, after getting it wrong first",
           "DB BROWSER · EXECUTE SQL",
           "-- this one FAILS. Run it and read the message.\n"
           "SELECT segment, COUNT(*) AS customers\n"
           "FROM customers\n"
           "WHERE COUNT(*) > 80\n"
           "GROUP BY segment;\n"
           "\n"
           "-- this one works\n"
           "SELECT segment, COUNT(*) AS customers\n"
           "FROM customers\n"
           "GROUP BY segment\n"
           "HAVING COUNT(*) > 80\n"
           "ORDER BY customers DESC;",
           "The error is the lesson: WHERE runs before the rows are "
           "grouped, so there is no count to test yet. Read the message out "
           "loud. Most SQL errors say what is wrong if you read them."),
          ],

    worked=("Why you must never average an average",
            "Four regions, four average order values. The national average "
            "is not the average of those four, and the gap is not small.",
            ["Compute the average order value per region. Four numbers, all "
             "correct.",
             "Average those four numbers. Write the answer down.",
             "Now compute the national average properly: total revenue "
             "divided by total orders.",
             "They differ, because the regions have different numbers of "
             "orders. The simple average treats a region with 400 orders "
             "and one with 1,900 as equally important.",
             "The rule: sum the top, sum the bottom, then divide. Never "
             "average an average unless the groups are the same size."],
            "Delivered revenue is <<rev_delivered>> over <<delivered>> "
            "delivered orders, so the average delivered order is about "
            "<<aov>>."),

    check=(["Why does WHERE COUNT(*) > 80 fail?",
            "You grouped by region and the totals do not add up to the "
            "overall figure. Why?",
            "Your average order value came out three times too small. What "
            "did you do?"],
           [("Why WHERE COUNT(*) > 80 fails",
             "WHERE is evaluated before the rows are grouped, so no count "
             "exists yet. Filtering on an aggregate is what HAVING is for."),
            ("Regional totals not adding up",
             "Grouping by region needs a join to customers, and the "
             "<<walkins>> walk-in orders have no customer to join to. They "
             "drop out silently, taking <<walkin_rev>> with them."),
            ("Average order value three times too small",
             "You divided by the number of order LINES instead of the "
             "number of ORDERS. There are <<items>> lines and <<orders>> "
             "orders. COUNT(DISTINCT order_id) is the fix, and it is the "
             "grain lesson from session 1 arriving in arithmetic.")]),

    lab=("Three groupings, then check them in Excel",
         "Revenue by channel, by segment and by month, delivered orders "
         "only. Then export the order lines to CSV, build the same three "
         "figures as pivot tables, and confirm they agree. Where they "
         "disagree, the SQL is usually right and the pivot has quietly "
         "included something.",
         ["Revenue by channel, delivered only.",
          "Revenue by customer segment, delivered only.",
          "Revenue by month for 2025.",
          "The same three as pivot tables from the exported CSV.",
          "Any disagreement: which one is wrong, and why?"]),

    closing=("You have written your first pivot table down",
             "It now runs again next month without you, on a file too big "
             "for a spreadsheet, and somebody else can read what you did. "
             "That is the whole argument for SQL and you have just made it "
             "yourself.",
             "Next session: joining tables, carefully. This is the one that "
             "goes wrong in real reports."),
)

# ============================================================== SESSION 5
DECKS[5] = dict(
    b1_title="INNER and LEFT, and the row count that tells you",
    b2_title="Fan-out, and queries somebody else can read",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Your total went up when you joined a table.\n"
              "Is that possible?",
              "Yes, and it is wrong. A join can multiply rows, and nothing "
              "warns you except a row count you were not watching."),

    concepts=[("INNER JOIN",
               "Keep only the rows that matched on both sides. Anything "
               "without a match disappears, with no message.",
               "Joining orders to customers with an INNER JOIN gives "
               "<<joined>> rows instead of <<orders>>. The <<walkins>> "
               "walk-in orders are gone, and with them <<walkin_rev>>.",
               "A VLOOKUP where you then delete every #N/A row. Same "
               "effect, and at least in Excel you SAW the #N/A."),

              ("LEFT JOIN",
               "Keep every row on the left, and leave the right-hand "
               "columns empty where nothing matched.",
               "The same join written LEFT gives all <<orders>> rows back, "
               "with a blank region on the walk-in orders. Now you can "
               "decide what to do about them, which is the point.",
               "A VLOOKUP where you keep the #N/A rows and deal with them "
               "on purpose."),

              ("Fan-out",
               "When one row matches several rows, its values are repeated "
               "once per match. Sum them afterwards and you have counted "
               "the same thing several times.",
               "Join orders to order_items and you get <<items>> rows, not "
               "<<orders>>. Any order-level figure now appears several "
               "times, and summing it gives a number far too big that looks "
               "entirely plausible.",
               "Nothing in Excel does this to you, because VLOOKUP returns "
               "only the FIRST match. This is the one place a real join "
               "behaves differently from the thing you already know."),

              ("CTE",
               "A named step at the top of a query that you can then use "
               "like a table. Short for common table expression, and "
               "nobody says that out loud.",
               "WITH line_value AS ( ... ) SELECT ... FROM line_value. You "
               "can run the step on its own, check it, and only then write "
               "what comes after it.",
               "A helper sheet. You already build one when a formula gets "
               "too long to trust in a single cell.")],

    code=[("Watch the row count decide the answer",
           "DB BROWSER · EXECUTE SQL",
           "SELECT COUNT(*) FROM orders;                        -- <<orders>>\n"
           "\n"
           "SELECT COUNT(*) FROM orders o\n"
           "JOIN customers c ON c.customer_id = o.customer_id;  -- <<joined>>\n"
           "\n"
           "SELECT COUNT(*) FROM orders o\n"
           "LEFT JOIN customers c ON c.customer_id = o.customer_id;\n"
           "-- still <<orders>>: LEFT keeps every order\n"
           "\n"
           "-- The INNER JOIN dropped <<walkins>> orders worth <<walkin_rev>>.",
           "Nothing in the output says rows were dropped. The only tell is "
           "that <<orders>> became <<joined>>. Check the count after every "
           "join, every time, for the rest of your career."),

          ("Fan-out, made visible",
           "DB BROWSER · EXECUTE SQL",
           "-- one row per order\n"
           "SELECT COUNT(*) FROM orders;               -- <<orders>>\n"
           "\n"
           "-- one row per LINE, after the join\n"
           "SELECT COUNT(*)\n"
           "FROM orders o\n"
           "JOIN order_items oi ON oi.order_id = o.order_id;\n"
           "--                                            <<items>>\n"
           "\n"
           "-- so this is WRONG: it counts each order several times\n"
           "SELECT COUNT(o.order_id), COUNT(DISTINCT o.order_id)\n"
           "FROM orders o\n"
           "JOIN order_items oi ON oi.order_id = o.order_id;",
           "The last query shows both numbers side by side: <<items>> and "
           "<<orders>>. Whenever you join to a table with more rows, ask "
           "what the grain of the result is before you sum anything."),

          ("Three named steps instead of one long query",
           "DB BROWSER · EXECUTE SQL",
           "WITH line_value AS (\n"
           "    -- step 1: one row per line, with its value and its month\n"
           "    SELECT oi.order_id, oi.line_no,\n"
           "           o.rep_id,\n"
           "           substr(o.order_date, 1, 7) AS month,\n"
           "           oi.quantity * oi.unit_price_ugx\n"
           "               * (1 - oi.discount)    AS gross_ugx\n"
           "    FROM order_items oi\n"
           "    JOIN orders o ON o.order_id = oi.order_id\n"
           "    WHERE o.status = 'Delivered'\n"
           "      AND o.order_date >= '2025-01-01'\n"
           ")\n"
           "SELECT r.region, r.rep_name, lv.month,\n"
           "       ROUND(SUM(lv.gross_ugx)) AS gross_ugx\n"
           "FROM line_value lv\n"
           "JOIN reps r ON r.rep_id = lv.rep_id\n"
           "GROUP BY r.region, r.rep_name, lv.month\n"
           "ORDER BY r.region, r.rep_name, lv.month;",
           "Run just the CTE first: SELECT * FROM line_value LIMIT 10 with "
           "the WITH still in place. If step one is wrong, everything after "
           "it is wrong, and you want to find that out in step one."),
          ],

    worked=("The report the sales manager actually wants",
            "Revenue by rep by month for 2025, net of returns. Two CTEs and "
            "a final SELECT, built and checked one step at a time.",
            ["Step one, a CTE: one row per line, with its month and its "
             "rep. Filter to delivered and to 2025 here, once, so the rest "
             "of the query does not have to.",
             "Check step one on its own before writing step two.",
             "Step two, a CTE: subtract what came back. LEFT JOIN to "
             "returns, because an INNER JOIN would keep only the returned "
             "lines and your revenue would collapse.",
             "Final SELECT: join the rep names on and group.",
             "Check it. Top three reps for 2025 before returns are "
             "<<top_reps>>."],
            "Everything returned across both years is worth "
            "<<returns_value>>. A report that ignores returns overstates "
            "every rep, and the manager will find out from somebody else."),

    splits=[("Checkpoint 1",
             "What to hand in",
             "One query that runs from cold in DB Browser.\n\n"
             "Revenue by rep by month for 2025, net of returns, built as "
             "named steps.\n\n"
             "Your row count, and one sentence on why it is the number it "
             "is.",
             "And one sentence of judgement",
             ["Which rep would you talk to first, and why?",
              "",
              "That sentence is the assessed part. A query with no "
              "conclusion is not an analysis: somebody still has to do the "
              "thinking you were asked to do.",
              "",
              "Marked against the answer key tonight, so you leave knowing "
              "whether it was right."],
             "CHECKPOINT 1 · 15% OF THE MARK")],

    check=(["An INNER JOIN and a LEFT JOIN return the same row count. What "
            "does that tell you?",
            "You joined orders to order_items and summed a per-order "
            "figure. What went wrong?",
            "Why put each step in a CTE rather than nesting?"],
           [("Same count from INNER and LEFT",
             "Every row on the left found a match, so on today's data the "
             "two are equivalent. That is a fact about these rows rather "
             "than about the tables, so re-check it when the data changes."),
            ("Summing a per-order figure after joining to lines",
             "Fan-out. The order-level figure repeated once per line, so "
             "the total counted it several times: <<orders>> orders became "
             "<<items>> rows. Aggregate the lines first, in their own step, "
             "then join."),
            ("Why CTEs rather than nesting",
             "You can run a CTE on its own and check it. A nested subquery "
             "can only be checked as part of the whole thing, which means a "
             "mistake in the middle is the last one you find.")]),

    lab=("Build the rep revenue report",
         "This is Checkpoint 1 and it is marked against the answer key "
         "tonight. Build it as named steps and check the row count after "
         "each one.",
         ["Step one: line value, filtered to delivered and to 2025.",
          "Check step one on its own.",
          "Step two: net of returns, with a LEFT JOIN.",
          "Final select: rep names, grouped by rep and month.",
          "Then break it on purpose: make the returns join an INNER JOIN "
          "and write down what happened and why.",
          "One sentence: which rep do you talk to first?"]),

    closing=("The row count is the smoke alarm",
             "Every error in this session announced itself the same way: a "
             "count that changed when you did not expect it to. Nothing else "
             "warns you, so build the habit now while the data is still "
             "small enough to check by hand.",
             "Next session: Python, from the beginning. No SQL for a while."),
)

# ============================================================== SESSION 6
DECKS[6] = dict(
    b1_title="You already write code",
    b2_title="Your first DataFrame",

    question=("THE QUESTION TONIGHT ANSWERS",
              "You have never programmed.\n"
              "How long until Python is useful to you?",
              "About ninety minutes. Tonight you load a real file and print "
              "how many rows it has."),

    points=[("A spreadsheet formula, with the parts named",
             [("=IF(B2>1000, \"large\", \"small\")",
               "You have written this. Every part of it has a name in "
               "programming, and you already understand all of them."),
              ("IF is a FUNCTION",
               "A named instruction that takes inputs and gives back a "
               "result. SUM, VLOOKUP and AVERAGE are functions too."),
              ("B2>1000 and the two words are ARGUMENTS",
               "The inputs you hand the function, inside its brackets, "
               "separated by commas. Python is identical."),
              ("B2 is a REFERENCE; in Python it is a VARIABLE",
               "A name that stands for a value. The difference is that you "
               "choose the name, so it can say what it means."),
              ("The whole thing is an EXPRESSION",
               "Something that produces a value. A program is mostly "
               "expressions, run top to bottom.")],
             "WHAT YOU ALREADY KNOW")],

    concepts=[("Variable",
               "A name that holds a value, so you can use it again without "
               "retyping it. You choose the name.",
               "rate = 3780.0 then price_ugx = price_usd * rate. If the "
               "rate changes you edit one line, and everything that used it "
               "follows.",
               "A named cell or a named range. You have probably called a "
               "cell TaxRate and referred to it by name."),

              ("Function",
               "A named instruction that takes inputs, does something, and "
               "gives back a result. You use other people's and you write "
               "your own.",
               "round(8751705520 / 3780, 2) uses two built-in functions. "
               "Writing your own takes one line: def to_usd(ugx): return "
               "ugx / 3780.",
               "SUM, IF, VLOOKUP. Identical idea; the brackets sit in a "
               "different place and you can make new ones."),

              ("Library",
               "Somebody else's functions, loaded when you need them. You "
               "will use one library, pandas, for almost everything in "
               "weeks three and four.",
               "import pandas as pd loads it and gives it the short name pd. "
               "Every pandas command in this course starts with pd or with "
               "the name of a table.",
               "An add-in. The difference is that these are free, "
               "universal, and the one you are learning is the most widely "
               "used data tool in the world."),

              ("Traceback",
               "The error message Python prints when something goes wrong. "
               "It is long, it looks alarming, and the LAST line is the one "
               "that names the problem.",
               "KeyError: 'Western' means you asked for something that is "
               "not there. NameError means a name does not exist. "
               "FileNotFoundError means the path is wrong. Three messages "
               "cover most of your first month.",
               "#VALUE! or #REF!, with an explanation attached and the line "
               "number. It is genuinely more helpful than Excel here."),

              ("Zero-based counting",
               "Python counts from 0, so the first row is row 0 and the "
               "first item of a list is item 0.",
               "regions[0] is the first region. df.iloc[0] is the first "
               "row. It feels wrong for about a week and then it stops "
               "being noticeable.",
               "Excel counts from 1. This is a genuine difference and it "
               "catches everybody once, so it is worth being told rather "
               "than discovering.")],

    code=[("Everything in the left half, in fourteen lines",
           "JUPYTER OR COLAB",
           "# a variable: a name holding a value\n"
           "rate = 3780.0\n"
           "region = \"Eastern\"\n"
           "\n"
           "# a list: several values in order, counted from ZERO\n"
           "regions = [\"Central\", \"Eastern\", \"Northern\", \"Western\"]\n"
           "print(regions[0])            # Central, not Eastern\n"
           "print(len(regions))          # 4\n"
           "\n"
           "# a function you write yourself\n"
           "def to_usd(ugx):\n"
           "    return round(ugx / rate, 2)\n"
           "\n"
           "print(to_usd(8751705520))    # delivered revenue, in dollars\n"
           "\n"
           "# a condition, which is the IF you already know\n"
           "if to_usd(8751705520) > 1000000:\n"
           "    print(\"over a million dollars\")",
           "Now ask for regions[4]. IndexError: list index out of range, "
           "because there are four items numbered 0 to 3. Read the last "
           "line of the traceback first. That habit is worth more tonight "
           "than any of the syntax."),

          ("Make three errors on purpose",
           "JUPYTER OR COLAB",
           "# 1. a name that does not exist\n"
           "print(reigon)          # NameError: name 'reigon' is not defined\n"
           "\n"
           "# 2. a file that is not there\n"
           "pd.read_csv(\"orders.csv\")   # FileNotFoundError\n"
           "\n"
           "# 3. a key that is not in the dictionary\n"
           "target = {\"Central\": 2.0e9, \"Eastern\": 2.4e9}\n"
           "print(target[\"Western\"])    # KeyError: 'Western'\n"
           "\n"
           "# every one of those told you exactly what was wrong.",
           "Do this deliberately now, in a safe room, and the first real "
           "error next week is an inconvenience instead of a wall. Every "
           "message above names both the problem and the thing that caused "
           "it."),

          ("Your first DataFrame",
           "JUPYTER OR COLAB",
           "import pandas as pd\n"
           "\n"
           "orders = pd.read_csv(\"data/orders.csv\")\n"
           "\n"
           "orders.shape        # (<<orders>>, 6)  rows, then columns\n"
           "orders.head(5)      # the first five rows\n"
           "orders.dtypes       # what type each column is\n"
           "\n"
           "# one column, which pandas calls a Series\n"
           "orders[\"status\"].value_counts()\n"
           "\n"
           "# rows by condition: this is autofilter, written down\n"
           "delivered = orders[orders[\"status\"] == \"Delivered\"]\n"
           "delivered.shape     # (<<delivered>>, 6)",
           "shape says (<<orders>>, 6): always rows first, then columns. "
           "Then try orders[\"Status\"] with a capital S. KeyError, because "
           "column names are case sensitive. Excel would have found it; "
           "pandas will not."),
          ],

    check=(["What is a variable, in your own words?",
            "Python says NameError: name 'reigon' is not defined. What do "
            "you do?",
            "regions has four items. Why does regions[4] fail?"],
           [("A variable, in your own words",
             "A name that holds a value so you can use it again. Like "
             "naming a cell, except you pick the name and it can say what "
             "it means."),
            ("NameError on a name you thought you had",
             "Read it literally: that name does not exist. Nine times in "
             "ten it is a typo, or a cell you have not run yet. Scroll up, "
             "find where you meant to create it, and run that cell."),
            ("Why regions[4] fails",
             "Because counting starts at 0, so four items are numbered 0, "
             "1, 2 and 3. There is no item 4. This is the one real "
             "difference from Excel and it catches everybody once.")]),

    lab=("Type it yourself, from a blank notebook",
         "Nothing is pasted tonight. Open an empty notebook and type every "
         "line. It is slower and it is the only version that teaches you "
         "anything.",
         ["Three variables, of three different types.",
          "A list, and print its first item and its length.",
          "A function you write, and call twice with different inputs.",
          "Load data/orders.csv and print its shape and its first five "
          "rows.",
          "Make all three errors from the slide on purpose, and write down "
          "what the last line of each traceback said.",
          "Filter to delivered orders and check you get <<delivered>>."]),

    closing=("You wrote a program tonight",
             "It loaded a real file of <<orders>> rows and told you "
             "something true about it. The rest of this course is more of "
             "the same, in bigger steps.",
             "Next session: the six-command routine you run on any file you "
             "have never seen."),
)

# Placeholders live in da_keys.FMT_BASE, in one place, because sessions
# move between these modules and a private copy goes stale.
FMT = {}
