# -*- coding: utf-8 -*-
"""Week 5 slide content: sessions 13, 14 and 15.

A whole investigation, then Power BI, then the capstone. DAX time
intelligence and row-level security were cut to pay for the foundations; see
da_content.CUT.
"""
import da_keys as D

DECKS = {}

# ============================================================== SESSION 13
DECKS[13] = dict(
    b1_title="The routine, in a fixed order",
    b2_title="From eleven observations to five findings",

    question=("THE QUESTION TONIGHT ANSWERS",
              "You have a file you have never seen and three hours.\n"
              "Where do you start?",
              "In the same place every time. The routine is what stops an "
              "investigation becoming forty cells and no conclusion."),

    points=[("The routine. Same order, every dataset, every time.",
             [("What is this file a record of, and what is one row?",
               "One sentence each, written down. You have been doing this "
               "since session 1. If you cannot write them, stop and find "
               "out."),
              ("What is the time window, and is it complete?",
               "Earliest, latest, and whether any period in between is "
               "missing. A missing month is a finding on its own."),
              ("What is missing, and is it missing for a reason?",
               "Per column, count and percentage. Missing at random and "
               "missing by design need different handling."),
              ("What does the thing that matters look like?",
               "The distribution of your main quantity, drawn, then a "
               "decision about mean or median. Sessions 10 and 11."),
              ("What moves with what?",
               "Two or three comparisons the domain suggests. Not every "
               "pair: a correlation matrix of forty columns is not "
               "analysis."),
              ("What would change my mind?",
               "Written down before you present. It is the question you "
               "will be asked, and having the answer ready is the whole "
               "difference in a defence.")],
             "SIX QUESTIONS, IN THIS ORDER")],

    concepts=[("A finding",
               "A sentence with a number in it that somebody could act on "
               "or dispute. It is about the business, not about the data.",
               "\"Returns are highest in <<rate_top_region>> at "
               "<<rate_top_pct>>, against <<rate_bottom_pct>> in "
               "<<rate_bottom_region>>.\" That can be acted on and it can "
               "be argued with.",
               "The sentence you would put in an email, rather than the "
               "pivot table you would attach."),

              ("An observation",
               "Something true about the data rather than about the "
               "business. It belongs in your notebook and not in your "
               "findings.",
               "\"The returns table has <<returns>> rows\" is an "
               "observation. \"Two and a half per cent of order lines come "
               "back, and it is worse in one region\" is a finding.",
               None),

              ("A stated limitation",
               "The sentence beside a finding saying where it stops being "
               "reliable. Beside it, not in a footnote, because that is "
               "where the person acting on it will read.",
               "\"This excludes the <<walkins>> walk-in orders, worth "
               "<<walkin_rev>>, because they carry no customer and "
               "therefore no region.\"",
               "A disclaimer protects you. A limitation tells the reader "
               "how far they can push the number, which is useful to "
               "them."),

              ("Leakage",
               "Using a column you would not have had at decision time, "
               "which makes the answer look far better than it is.",
               "In the Bank Marketing dataset, the duration column records "
               "how long the sales call lasted. You only know it AFTER the "
               "call, so using it to predict the call's outcome is "
               "cheating, and it is the commonest beginner mistake on that "
               "file.",
               None)],

    splits=[("Choose your sector dataset tonight",
             "Three fixed course snapshots",
             "BANKING, FINANCE, TELECOM\n"
             "Bank Marketing, UCI 222. 45,211 rows x 17. Campaign contacts "
             "against an outcome. Duration is post-call; exclude it from pre-call decisions.\n\n"
             "ENERGY, MINING, MANUFACTURING\n"
             "AI4I 2020, UCI 601. 10,000 rows x 14. Synthetic observations against "
             "a failure flag, only 3.4% of which are failures.\n\n"
             "PUBLIC SECTOR AND DEVELOPMENT\n"
             "Uganda GDP in current USD, World Bank. One row per year, 2000–2023. "
             "Nominal dollar changes are not real growth or health outcomes.",
             "Use the supplied files and source notes",
             ["Read data/sector_snapshots/README.md for attribution, source terms and interpretation limits.",
              "",
              "Pick the one closest to your own work. The capstone is worth "
              "more to you if the data looks like your data.",
              "",
              "Whichever you pick, the routine is the same. That is the "
              "point of having a routine."],
             "THE SECTOR ASSESSMENT")],

    worked=("Turning eleven observations into five findings",
            "An investigation produces far more observations than findings. "
            "Choosing between them is part of the work.",
            ["Write every observation down as you go, without judging it. "
             "Eleven or twelve is normal for three hours.",
             "Strike anything about the DATA rather than the BUSINESS. Null "
             "counts and dtypes are not findings.",
             "Merge the ones that are the same finding seen twice. Two "
             "charts of one fact is one finding.",
             "Rank what is left by what somebody could DO about it. The top "
             "five are your findings.",
             "Write each as one sentence with a number, and put the "
             "limitation beside it."],
            "Five findings with numbers beat eleven observations without "
            "them, and the marking reflects that."),

    check=(["What makes a sentence a finding rather than an observation?",
            "Your investigation produced no surprises. Is that a failure?",
            "Why does the limitation belong beside the finding?"],
           [("Finding against observation",
             "A finding is about the business, has a number in it, and "
             "somebody could act on it or dispute it. An observation is "
             "about the data. Both belong in the notebook; only findings "
             "belong in the summary."),
            ("An investigation with no surprises",
             "No. Confirming what the room believed, with numbers attached, "
             "converts an assumption into something checkable. What IS a "
             "failure is not knowing which of the two you produced."),
            ("Why the limitation sits beside the finding",
             "Because that is where the person acting on it reads. A "
             "limitation at the end of a document is a limitation nobody "
             "saw, and you will still be the one defending the number.")]),

    lab=("Run the routine on your sector dataset",
         "This is the sector assessment, worth 30%. Six questions in "
         "order, then five findings. Marked on the findings and the "
         "limitations beside them, not on the code.",
         ["What is the file a record of? What is one row?",
          "Time window, and is it complete?",
          "What is missing, and is it missing for a reason?",
          "The distribution of the thing that matters, with a chart.",
          "Two or three comparisons the domain suggests.",
          "Five findings, each one sentence with a number and a limitation.",
          "What would change your mind?"]),

    closing=("A routine beats talent under time pressure",
             "Every analyst you would want to hire has one. It is what lets "
             "them open an unfamiliar file at nine and say something "
             "defensible by eleven, which is the actual job.",
             "Next session: Power BI, and the model that decides whether "
             "your totals are true."),
)

# ============================================================== SESSION 14
DECKS[14] = dict(
    b1_title="Power Query: get it in, shape it, keep the recipe",
    b2_title="The model, which is where the marks are",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Why does a Power BI total come out wrong\n"
              "when every number behind it is right?",
              "Almost always the model: one relationship pointing the wrong "
              "way, or no date table."),

    points=[("Power BI is three products, and people confuse them",
             [("Power Query gets the data and shapes it",
               "Promote headers, set types, trim, remove duplicates. The "
               "Applied Steps list is a recipe that runs again next month "
               "on new data. It is your cleaning log from session 8, built "
               "by clicking."),
              ("The model relates the tables",
               "One fact table, dimensions around it, relationships with a "
               "direction. This is the part that decides whether your "
               "totals are right, and it is the part beginners skip."),
              ("The report shows the answer",
               "Visuals. This is where everybody starts, and starting here "
               "is why the first dashboard most people build has wrong "
               "totals."),
              ("The browser route needs a readiness check",
               "Power BI Desktop is Windows only. The browser Service can "
               "edit models and use Power Query when permissions and tenant settings allow it. Test the supplied CSV workflow with the actual student account before class.")],
             "THREE PARTS")],

    concepts=[("A data model",
               "The tables plus the relationships between them, defined "
               "once, so you do not write a join in every query.",
               "Five relationships for the course data. Define them once "
               "and every visual you build afterwards inherits them.",
               "Doing your VLOOKUPs once, at the start, instead of in every "
               "sheet."),

              ("A star schema",
               "One fact table in the middle holding the events, with "
               "dimension tables around it holding the descriptions you "
               "slice by. Every dimension points INTO the fact, "
               "one-to-many.",
               "order_items is the fact: <<items>> rows, one per product "
               "per order. orders, customers, products and reps are "
               "dimensions.",
               "A well-organised workbook: one big transaction sheet and "
               "several small lookup sheets. You have probably built one "
               "without knowing it had a name."),

              ("A date table",
               "A separate table with one row per date, marked as the date "
               "table and related to your fact's date column.",
               "731 days, 1 January 2024 to 31 December 2025. Sort the Month "
               "names by MonthNo so that January comes first.",
               "The helper column of month names you add by hand every "
               "time. This one is built once and reused.")],

    b2_figs=[("fig_star_schema",
              "What you are building tonight",
              "The same six tables you mapped by hand in session 2, now as "
              "a model. The arrows all point the same way: many orders to "
              "one customer. Row counts are the real ones.")],

    code=[("The date table, and the step everybody skips",
           "POWER BI · MODELLING · NEW TABLE",
           "Dates =\n"
           "ADDCOLUMNS(\n"
           "    CALENDAR(DATE(2024, 1, 1), DATE(2025, 12, 31)),\n"
           "    \"Year\",      YEAR([Date]),\n"
           "    \"Month\",     FORMAT([Date], \"mmm\"),\n"
           "    \"MonthNo\",   MONTH([Date]),\n"
           "    \"YearMonth\", FORMAT([Date], \"yyyy-mm\")\n"
           ")\n"
           "\n"
           "-- then, and this is the step people miss:\n"
           "--   1. Table tools > Mark as date table > Date\n"
           "--   2. relate Dates[Date] to orders[order_date]\n"
           "--   3. Column tools > Month > Sort by column > MonthNo",
           "Skip step 3 and your months read April, August, December, "
           "February. It looks like a bug in Power BI and it is "
           "alphabetical sorting doing exactly what it was told."),
          ],

    splits=[("Build these five relationships by hand",
             "The five, all many-to-one",
             "order_items to orders on order_id\n\n"
             "orders to customers on customer_id\n\n"
             "orders to reps on rep_id\n\n"
             "order_items to products on product_id\n\n"
             "orders[order_date] to Dates[Date]",
             "Delete the auto-detected ones first",
             ["Power BI guesses relationships on load. It is right about "
              "most of them and wrong in a way you will not notice until a "
              "total is wrong.",
              "",
              "Delete all of them, build these five yourself, and check "
              "every arrow direction.",
              "",
              "Then check a total against a number you already trust. "
              "Delivered revenue is <<rev_delivered>>. If your card says "
              "something else, the model is wrong and the visuals cannot "
              "save it."],
             "THE MODEL")],

    prose=[("Reconcile against numbers you already have",
            ["**Why this matters more here than anywhere else**",
             "A dashboard is believed. A wrong number in a notebook gets "
             "questioned; the same number in a dashboard with a logo on it "
             "gets acted on.",
             "**The three you already know**",
             "Revenue over everything: <<rev_all>>. Delivered only: "
             "<<rev_delivered>>. Average delivered order: about <<aov>>.",
             "**If they do not match**",
             "The gap usually names the fault. Far too high means fan-out "
             "from a relationship pointing the wrong way. Low by about "
             "<<walkin_rev>> means the <<walkins>> walk-in orders have been "
             "dropped by a join to customers.",
             "**The rule**",
             "Reconcile before you make it look good. A dashboard whose "
             "totals do not reconcile is worth less than no dashboard."],
            "CHECKING YOUR MODEL", 2)],

    check=(["Why is a single flat table the wrong shape for a report?",
            "Your months sort April, August, December. What is wrong?",
            "Your revenue total is about three times too big. Where do you "
            "look?"],
           [("Why a flat table is wrong",
             "It cannot represent something that did not happen. A customer "
             "who bought nothing this quarter and a month with no orders "
             "both vanish, because the only rows that exist are rows where "
             "something occurred. This is session 2, arriving again."),
            ("Months sorting alphabetically",
             "The Month column is text and has not been told to sort by "
             "MonthNo. Column tools, Sort by column, MonthNo. It is not a "
             "bug."),
            ("Revenue three times too big",
             "Fan-out from a relationship, which is session 5's trap in a "
             "new tool. Check the direction and cardinality of every one, "
             "especially any you did not build yourself.")]),

    lab=("Load it, model it, reconcile it",
         "Five tables in, five relationships built by hand, a date table "
         "marked and sorted, and three visuals whose totals match the "
         "numbers you already got from SQL and pandas. Reconciliation is your "
         "practice check.",
         ["Get Data: the five CSVs, loaded separately.",
          "Power Query: headers, types, trim. Check the date range.",
          "Delete every auto-detected relationship.",
          "Build the four source-table relationships and check each direction.",
          "Add the date table and fifth relationship. Mark it; sort Month by MonthNo.",
          "Three visuals, each total reconciled against your own earlier "
          "answer."]),

    closing=("The model decides whether the report is true",
             "Visuals are half an hour of work. The model is the difference "
             "between a dashboard and a liability. Get the arrows right, "
             "then make it look good.",
             "Next session: three measures, a dashboard, and five minutes "
             "in front of the room."),
)

# ============================================================== SESSION 15
DECKS[15] = dict(
    b1_title="Three measures, and why a measure is not a column",
    b2_title="Thirty seconds of attention, and five minutes of yours",

    question=("THE QUESTION TONIGHT ANSWERS",
              "What does somebody take away\n"
              "in the thirty seconds they will give you?",
              "One number, one comparison, and a title that says what you "
              "found. Everything else on the page is competing with those."),

    concepts=[("A measure",
               "A calculation worked out when a visual asks for it, inside "
               "that visual's filters. The same measure gives a different "
               "number in every cell of a table, which is the point of it.",
               "Revenue UGX in a card with no filter gives <<rev_all>>. The "
               "same measure on a bar chart by region gives each region's "
               "share, with no extra work.",
               "A pivot table value field. You drop Revenue into Values "
               "once and it recalculates for every row and column "
               "combination. Identical idea."),

              ("A calculated column",
               "A calculation worked out once per row when the data loads, "
               "and then fixed. It cannot respond to a slicer.",
               "Line value, quantity times price times one minus discount, "
               "is reasonable as a column: it depends only on that row. "
               "Average order value is not, because it depends on which "
               "rows the user is looking at.",
               "A formula column in the sheet. Confusing these two is the "
               "commonest Power BI mistake there is."),

              ("A recommendation",
               "What somebody should do, with the number that justifies it "
               "and the conditions under which it stops being true. One "
               "page.",
               "\"Move one rep from <<region_low>> to <<region_top>> for "
               "the December peak. <<region_top>> did <<region_top_bn>> "
               "against <<region_low_bn>>, and December is the biggest "
               "month in both years. If December 2026 is flat by week two, "
               "revert it.\"",
               "A finding says what is true. A recommendation says what to "
               "do, and carries the risk of being acted on.")],

    code=[("Revenue: sum the value of each order line",
           "POWER BI · MODELLING · NEW MEASURE",
           "Revenue UGX =\n"
           "SUMX(\n"
           "    order_items,\n"
           "    order_items[quantity] * order_items[unit_price_ugx]\n"
           "        * (1 - order_items[discount])\n"
           ")\n"
           "-- expected: <<rev_all>>",
           "Check that discount is a fraction, and multiply at the order-line grain before summing."),
          ("Delivered revenue: change the filter context",
           "POWER BI · MODELLING · NEW MEASURE",
           "Delivered Revenue UGX =\n"
           "CALCULATE(\n"
           "    [Revenue UGX],\n"
           "    orders[status] = \"Delivered\"\n"
           ")\n"
           "-- expected: <<rev_delivered>>",
           "Compare the two revenue cards. The status filter must propagate through the relationship to order_items."),
          ("Average order value: match both populations",
           "POWER BI · MODELLING · NEW MEASURE",
           "Avg Order Value UGX =\n"
           "DIVIDE(\n"
           "    [Delivered Revenue UGX],\n"
           "    CALCULATE(DISTINCTCOUNT(orders[order_id]),\n"
           "              orders[status] = \"Delivered\")\n"
           ")\n"
           "-- expected: about <<aov>>",
           "Without CALCULATE in the denominator, delivered revenue is divided by all <<orders>> orders instead of <<delivered>> delivered orders. The plausible result <<aov_wrong>> is about 19% low."),

          ("DISTINCTCOUNT, which is session 5 again",
           "POWER BI · MODELLING · NEW MEASURE",
           "-- WRONG: counts order LINES, because that is the fact table\n"
           "Orders Wrong = COUNTROWS(order_items)      -- <<items>>\n"
           "\n"
           "-- RIGHT: counts distinct orders\n"
           "Orders = DISTINCTCOUNT(orders[order_id])   -- <<orders>>\n"
           "\n"
           "-- so average order value with the wrong one is about a third\n"
           "-- of the truth, and looks entirely plausible on a card.",
           "Build both cards side by side and put them on the page next to "
           "each other. The grain problem from session 1 has now bitten you "
           "in a spreadsheet, in SQL, in pandas and in Power BI. That is "
           "why it was the first thing taught."),
          ],

    points=[("A dashboard for somebody with thirty seconds",
             [("The number they came for, top left",
               "One card. Readers start top left, and the number in that "
               "position is the one that gets remembered."),
              ("Five visuals, maximum. Four is better.",
               "Every extra visual reduces the chance that any of them is "
               "read."),
              ("A title that states the finding",
               "Not \"Sales Dashboard\". The same rule as a chart title, "
               "applied to the page."),
              ("One slicer, not five",
               "Every slicer is a way for a reader to produce a view you "
               "have never seen and cannot defend."),
              ("One accent colour",
               "Colour should mean something. If everything is coloured, "
               "nothing is emphasised.")],
             "LAYOUT"),

            ("Five minutes, in the order they listen",
             [("The question, in one sentence",
               "The one you were actually asked. Fifteen seconds."),
              ("The answer, with its number",
               "Immediately. Not the method, not the journey. Attention is "
               "highest at the start and you cannot control when it ends."),
              ("How you know",
               "The data, the window, and the one chart that carries it. "
               "Ninety seconds, one chart."),
              ("What you accepted in exchange for what",
               "The trade you made: a narrower window, a dropped segment, "
               "a simpler measure. Naming it is what makes the rest "
               "credible."),
              ("What would change your answer",
               "The sentence that separates an analyst from an advocate.")],
             "THE PRESENTATION")],

    splits=[("What you hand in, and what you say",
             "Five minutes",
             "The question, in one sentence.\n\n"
             "The answer, with its number, immediately after.\n\n"
             "One chart. One.\n\n"
             "What you traded away.\n\n"
             "What would change your answer.",
             "And what is marked",
             ["Upload PPTX with narration notes and numerical evidence.",
              "",
              "Add a DOCX/PDF appendix if needed. Keep PBIX as supporting material.",
              "",
              'Marks reward a supported decision and the required evidence.',
              "",
              "Everybody asks at least one question of somebody else. That "
              "is how you learn what a weak answer sounds like."],
             "CAPSTONE · 40% OF THE MARK")],

    prose=[("Monday morning, and what to learn next",
            ["**Pick one report and replace it**",
             "One report somebody produces by hand every month. Not the "
             "biggest: the most repetitive. Automate that one and the "
             "second is easier.",
             "**Expect the bottleneck to be access, not skill**",
             "Most people leaving this course find the hard part is getting "
             "to the data rather than analysing it. That is a conversation "
             "with whoever owns the database, and it goes better when you "
             "can name the tables you need and the grain you want them at.",
             "**Where to go next, honestly**",
             "Statistics and experiment design if your questions are about "
             "causes. Machine learning if they are about prediction. Data "
             "engineering if the bottleneck turned out to be access. "
             "Forty-five hours buys a competent analyst; it does not buy "
             "the other three.",
             "**Keep the habits, if nothing else**",
             "The question before the query. The grain said out loud. The "
             "row count after every join. The cleaning log. The finding in "
             "the title. Those five are most of the value here and none of "
             "them need a tool."],
            "WHAT TO DO NEXT", 2)],

    check=(["When does something have to be a measure rather than a column?",
            "Somebody asks a question you cannot answer. What do you say?",
            "Why does the answer come second rather than last?"],
           [("Measure against column",
             "If the answer depends on what the reader filtered, it must be "
             "a measure. A column is fixed when the data loads and cannot "
             "respond to a slicer."),
            ("A question you cannot answer",
             "\"I do not know, and here is what I would need to find out.\" "
             "It costs you nothing and it protects every other number you "
             "gave them. Guessing costs you all of them."),
            ("Why the answer comes second",
             "Attention is highest at the start and you cannot control when "
             "it ends. Build to a conclusion and you may never reach it: "
             "somebody interrupts at minute three and the room leaves with "
             "your method.")]),

    lab=("Finish the dashboard, then present",
         "Use the 50-minute clinic to finish and reconcile the dashboard. Submit a five-minute narrated presentation. Selected live demonstrations take 40 minutes, followed by 20 minutes on applying the work.",
         ["Four visuals, three measures, one slicer.",
          "Every total reconciled against a number you already trust.",
          "A title that states your finding.",
          "Five minutes: question, answer, how you know, the trade, what "
          "would change it.",
          "Ask at least one question of somebody else.",
          "Write down: the report you will replace, the first step, and who "
          "you need to ask."]),

    closing=("You can answer a question with a number attached",
             "That is a smaller claim than a certificate implies and a "
             "bigger one than it sounds. Most organisations have very few "
             "people who will say what they found, what it cost, and what "
             "would change their mind.",
             "Send it to the person who asked in week one. That is the last "
             "step and it is the one people skip."),
)

# Placeholders live in da_keys.FMT_BASE, in one place, because sessions
# move between these modules and a private copy goes stale.
FMT = {}
