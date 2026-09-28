# -*- coding: utf-8 -*-
"""Week 3 slide content: sessions 7, 8 and 9. pandas on real files."""
import da_keys as D

DECKS = {}

# ============================================================== SESSION 7
DECKS[7] = dict(
    b1_title="Six commands, on any file you have never seen",
    b2_title="Selecting, filtering, and the type that lies",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Somebody sends you a file you have never seen.\n"
              "What are the first two minutes?",
              "The same six commands, in the same order, every time. It is "
              "the cheapest habit in this work."),

    concepts=[("Series",
               "One column of a DataFrame, on its own. Selecting a single "
               "column gives you one of these rather than a table.",
               "orders[\"status\"] is a Series. orders[[\"status\"]] with "
               "two sets of brackets is a DataFrame with one column. The "
               "difference matters when you chain something onto it.",
               "A single column selection. Excel does not distinguish the "
               "two, and pandas does."),

              ("dtype",
               "The type pandas decided a column has when it read the file. "
               "You did not choose it and it is not always right.",
               "object on a text column is normal. object on a column of "
               "NUMBERS means something in there is not a number: a comma, "
               "a currency symbol, a blank, or the word NULL.",
               "Cell format. The difference is that a wrong dtype changes "
               "the ANSWER: summing a text column concatenates instead of "
               "adding, and nothing raises an error."),

              ("Missing value",
               "A cell with nothing recorded. pandas shows it as NaN, which "
               "stands for not a number and appears in text columns too.",
               "orders.isna().sum() reports <<missing_cust>> missing "
               "customer ids. It is the same walk-in trade you met as NULL "
               "in SQL: the word changes, the fact does not.",
               "A blank cell. The trap is the same one: a blank is not a "
               "zero, and a count that ignores it is answering a different "
               "question.")],

    code=[("The six commands. Learn the order, not the words.",
           "JUPYTER OR COLAB",
           "import pandas as pd\n"
           "df = pd.read_csv(\"data/orders_raw.csv\")\n"
           "\n"
           "df.shape                  # 1. how big? rows, then columns\n"
           "df.head()                 # 2. what is one row?\n"
           "df.dtypes                 # 3. what type is each column?\n"
           "df.info()                 # 4. types and non-null counts at once\n"
           "df.isna().sum()           # 5. what is missing, per column?\n"
           "df[\"status\"].value_counts()   # 6. what values does this hold?",
           "Run df.describe() as well and look at customer_id: it has been "
           "given a mean and a standard deviation. Both are meaningless, "
           "because it is an identifier. describe() cannot tell the "
           "difference and will not warn you."),

          ("Selecting and filtering, which is autofilter written down",
           "JUPYTER OR COLAB",
           "# one column\n"
           "df[\"channel\"]\n"
           "\n"
           "# several columns: a LIST inside the brackets\n"
           "df[[\"order_id\", \"channel\", \"status\"]]\n"
           "\n"
           "# rows by condition\n"
           "delivered = df[df[\"status\"] == \"Delivered\"]\n"
           "delivered.shape                    # (<<delivered>>, 6)\n"
           "\n"
           "# two conditions: the inner brackets are NOT optional\n"
           "recent = df[(df[\"status\"] == \"Delivered\")\n"
           "            & (df[\"order_date\"] >= \"2025-01-01\")]",
           "Drop the inner brackets from the last one. It raises, because & "
           "binds more tightly than ==. The message is unhelpful and this "
           "costs people twenty minutes the first time, so meet it now."),

          ("The type that lies",
           "JUPYTER OR COLAB",
           "items = pd.read_csv(\"data/order_items_raw.csv\")\n"
           "items.dtypes\n"
           "\n"
           "# suppose unit_price had arrived as text. This is what happens:\n"
           "text_prices = items[\"unit_price\"].astype(str)\n"
           "print(text_prices.sum()[:60])    # it JOINS them, end to end\n"
           "print(len(text_prices.sum()))    # thousands of characters\n"
           "\n"
           "# the real column, as a number\n"
           "print(items[\"unit_price\"].sum())",
           "A text column summed does not fail. It concatenates, and you "
           "get a number-shaped answer that is nonsense. This is the "
           "commonest cause of a wrong pandas answer and the reason dtypes "
           "is command three of six."),
          ],

    worked=("Profiling a file you have never seen",
            "The routine in a fixed order. Two minutes, and afterwards you "
            "can say what the file can and cannot answer.",
            ["shape. Write the row count down; every later step is checked "
             "against it.",
             "head. Say out loud what one row is. If you cannot, stop and "
             "find out before doing anything else.",
             "dtypes. Is anything text that should be a number, or text "
             "that should be a date?",
             "isna().sum(). What is missing, and is it missing at random or "
             "for a reason? Here <<missing_cust>> orders have no customer "
             "because walk-in trade has none.",
             "describe(), on the columns where it means something and only "
             "those.",
             "value_counts() on every category column, looking for two "
             "spellings of one thing."],
            "Six commands. The two-minute version of this is what separates "
            "an analyst from somebody who trusts a file."),

    splits=[("A large workbook to inspect with pandas",
             "Online Retail II",
             "A real transactional file from the UCI repository. CC BY 4.0, "
             "no account needed.\n\n"
             "1,067,371 rows and 8 columns, December 2009 to December "
             "2011.\n\n"
             "A worksheet has a row limit. This workbook spans sheets; "
             "inspect all sheets before combining them. pandas makes "
             "the preparation repeatable.",
             "Produce the one-page profile",
             ["Shape, and one sentence on what one row is.",
              "",
              "dtypes, and name every column whose type is wrong.",
              "",
              "The date range. Does it match what the documentation "
              "claims?",
              "",
              "Missing values per column, as a count and as a percentage.",
              "",
              "The five countries with the most invoices."],
             "LAB · THE FIRST REAL FILE")],

    check=(["A price column has dtype object. What does that tell you, and "
            "what does it not tell you?",
            "describe() gives you a mean customer_id. Why is that "
            "meaningless?",
            "Why is df.isna().sum() one of the six and not an optional "
            "extra?"],
           [("A price column with dtype object",
             "Something in it is not a number: a comma, a currency symbol, "
             "a blank, or a word. It does not tell you which or how many, "
             "and value_counts() on the odd values is how you find out."),
            ("A mean customer_id",
             "It is an identifier that happens to be stored as a number. "
             "describe() computes statistics on anything numeric and cannot "
             "tell an identifier from a measurement. The judgement is "
             "yours."),
            ("Why the missing-value count is not optional",
             "Because a blank is not a zero, and every count, average and "
             "join downstream behaves differently depending on how many "
             "there are. Here it is <<missing_cust>> rows worth "
             "<<walkin_rev>>.")]),

    lab=("Profile Online Retail II",
         "Download it, open it in pandas, and produce the one-page profile. "
         "You are not cleaning it tonight. The goal is to be able to say, in "
         "three sentences, what the file is a record of and what it cannot "
         "tell you.",
         ["The six commands, in order.",
          "One sentence: what is one row?",
          "Every column whose dtype is wrong.",
          "Missing values, count and percentage.",
          "The five countries with the most invoices.",
          "Three sentences on what this file is a record of."]),

    closing=("Look before you compute",
             "Six commands, two minutes. Every hour lost in this work is "
             "lost to an assumption about a file that nobody checked, and "
             "the check is cheaper than the assumption every single time.",
             "Next session: the file is dirty, and cleaning it is a series "
             "of decisions rather than a series of commands."),
)

# ============================================================== SESSION 8
DECKS[8] = dict(
    b1_title="Seven defects, found and fixed",
    b2_title="The decision, the log, and the reconciliation",

    question=("THE QUESTION TONIGHT ANSWERS",
              "You cleaned the data and got a number.\n"
              "Could somebody else get the same number?",
              "Only if you wrote down what you changed. Cleaning is a "
              "series of decisions, and a decision nobody recorded is a "
              "number nobody can reproduce."),

    points=[("The seven defects in tonight's file, and what each one costs",
             [("<<dup_rows>> exact duplicate rows",
               "An export that ran twice. Revenue overstated by whatever "
               "those rows contained."),
              ("<<neg_lines>> negative quantities",
               "A returns convention rather than an error. Sum the column "
               "and you get a figure that is neither sales nor net of "
               "returns."),
              ("<<usd_lines>> lines priced in dollars",
               "One whole category, priced by a team that works in USD. "
               "Nothing in the file says so, and the error is a factor of "
               "3,780."),
              ("<<bad_discounts>> discounts above 1.0",
               "15 typed where 0.15 was meant, which makes revenue on those "
               "lines negative."),
              ("<<alt_dates>> dates in a second format",
               "Both 2025-03-14 and 14/03/2025 in one column. Parse it "
               "carelessly and March becomes February."),
              ("<<messy_names>> messy customer names",
               "Upper case, lower case and trailing spaces. Harmless until "
               "you group by name and get three groups for one customer."),
              ("<<missing_cust>> orders with no customer",
               "Walk-in trade. A decision rather than a defect: dropping "
               "them loses <<walkin_rev>> of real revenue.")],
             "WHAT IS WRONG WITH THE FILE")],

    concepts=[("A cleaning log",
               "A table recording rows in, rows out, what changed and why, "
               "written as you work rather than afterwards.",
               "Loaded <<raw>> rows. Dropped <<dup_rows>> exact duplicates "
               "because an export ran twice. Moved <<neg_lines>> negative "
               "lines to a returns frame because negative quantity is this "
               "system's return convention.",
               "The notes tab nobody fills in. The difference is that this "
               "one is the deliverable, and it is marked."),

              ("Reconciliation",
               "Getting the same number two different ways and chasing every "
               "difference until you can name it.",
               "Your cleaned CSVs should give <<rev_from_raw>>. The "
               "database says <<rev_delivered>>. The gap is <<residual>>, "
               "and tonight you find out why.",
               "Ticking a total against another total. You already do this; "
               "here it becomes the habit that catches the mistakes "
               "cleaning introduces."),

              ("Residual",
               "The difference left after you have explained everything you "
               "can. Naming it is part of the job.",
               "Tonight's residual is <<residual>> on <<rev_delivered>>, "
               "which is 0.0004%. It comes from the dollar-priced lines "
               "being recorded to the cent, and it cannot be cleaned away.",
               None)],

    code=[("Duplicates, and the returns convention",
           "JUPYTER OR COLAB",
           "items = pd.read_csv(\"data/order_items_raw.csv\")\n"
           "items.shape                       # (<<raw>>, 6)\n"
           "\n"
           "items.duplicated().sum()          # <<dup_rows>>\n"
           "items = items.drop_duplicates()\n"
           "\n"
           "# negative quantity is a RETURN here, not corruption\n"
           "items[\"quantity\"].describe()\n"
           "rets  = items[items[\"quantity\"] < 0].copy()   # <<neg_lines>>\n"
           "sales = items[items[\"quantity\"] > 0].copy()",
           "Run items[\"quantity\"].sum() BEFORE splitting them. The "
           "negative lines net off against the sales, so the total is "
           "neither gross sales nor net of returns. It is a number with no "
           "definition, and it looks entirely reasonable."),

          ("The defect nothing in the file tells you about",
           "JUPYTER OR COLAB",
           "prod = pd.read_csv(\"data/products.csv\")\n"
           "\n"
           "j = sales.merge(prod[[\"product_id\", \"category\"]],\n"
           "                on=\"product_id\", how=\"left\",\n"
           "                validate=\"many_to_one\")\n"
           "\n"
           "j.groupby(\"category\")[\"unit_price\"].describe()[[\"min\", \"max\"]]\n"
           "\n"
           "# one category's prices are a thousandth of the others:\n"
           "# <<usd_lines>> lines recorded in USD at 3,780 to the dollar\n"
           "usd = j[\"category\"] == \"Imported appliances\"\n"
           "j.loc[usd, \"unit_price\"] = j.loc[usd, \"unit_price\"] * 3780.0",
           "There is no error message for this one, ever. The only way to "
           "find it is to ask what a price SHOULD look like and then check. "
           "If the rate is wrong, every number downstream is wrong by the "
           "same factor and still looks plausible."),

          ("Two date formats in one column",
           "JUPYTER OR COLAB",
           "orders = pd.read_csv(\"data/orders_raw.csv\")\n"
           "orders[\"order_date\"].head(8)\n"
           "# both 2025-03-14 and 14/03/2025: <<alt_dates>> of the second\n"
           "\n"
           "orders[\"order_date\"] = pd.to_datetime(\n"
           "    orders[\"order_date\"], format=\"mixed\", dayfirst=True)\n"
           "\n"
           "orders[\"order_date\"].isna().sum()      # must be 0\n"
           "orders[\"order_date\"].min(), orders[\"order_date\"].max()\n"
           "# 2024-01-01 to 2025-12-31, the whole trading window",
           "Drop dayfirst=True and every date whose day is 12 or less gets "
           "silently read the American way: 14/03 stays March but 03/04 "
           "becomes the 4th of March. Checking min and max does NOT catch "
           "it, because both stay inside the window."),
          ],

    splits=[("The reconciliation does not come out exact, and that is the "
             "lesson",
             "What you will get",
             "A correct clean of these CSVs lands on <<rev_from_raw>>.\n\n"
             "The database says <<rev_delivered>>.\n\n"
             "You will be <<residual>> short, which is 0.0004%.",
             "Why, and what to do about it",
             ["The dollar-priced category was recorded TO THE CENT.",
              "",
              "Multiplying <<usd_delivered>> delivered lines back by 3,780 "
              "cannot recover the exact shilling price. Rounding to the "
              "cent threw a fraction away and it does not come back.",
              "",
              "So: land within a few thousand shillings, then WRITE THE "
              "RESIDUAL DOWN with its cause. That is the pass mark.",
              "",
              "An analyst who reports a reconciliation as exact when it is "
              "not has told you they did not look."],
             "PRECISION")],

    check=(["You dropped <<dup_rows>> duplicate rows. When is an exact "
            "duplicate NOT an error?",
            "One category's prices are a thousandth of the others. How "
            "would you have found that unaided?",
            "Why is a missing customer id a decision rather than a fix?"],
           [("When a duplicate is not an error",
             "When the grain allows it: two identical payments on one day "
             "are two real payments. On an order line it is an error, "
             "because the same product twice on one order would be one line "
             "with quantity 2. The grain decides, which is why session 1 "
             "spent an hour on it."),
            ("Finding a currency defect unaided",
             "Ask what a price should look like, then check min and max per "
             "category. A category whose prices are a thousandth of "
             "everything else is not a cheap category. Domain sense is the "
             "detector; there is no error message."),
            ("Why a missing customer id is a decision",
             "Because both answers are defensible and they give different "
             "numbers. Dropping those orders loses <<walkin_rev>>; keeping "
             "them means every per-customer analysis has a gap you must "
             "state. What is not defensible is doing either one "
             "silently.")]),

    lab=("Clean it, log it, reconcile it",
         "From the raw CSVs to a revenue figure you can defend, keeping the "
         "log as you go rather than writing it afterwards. The log is marked "
         "as heavily as the number.",
         ["Profile first. Rows in, and what you expect rows out to be.",
          "Work the seven defects. Two lines to find each, two to fix it.",
          "Keep the log: rows before, rows after, what changed, why.",
          "Reconcile against <<rev_from_raw>> and name your residual.",
          "State one decision you are not sure about, and why.",
          "Restart and Run All before you submit."]),

    closing=("A number nobody can reproduce is not a result",
             "In six months the person who cannot reproduce it will be you. "
             "The log costs five minutes while you work and saves an "
             "afternoon later, which is the best trade available in this "
             "course.",
             "Next session: the same answers in pandas as in SQL, and what "
             "to do when they disagree."),
)

# ============================================================== SESSION 9
DECKS[9] = dict(
    b1_title="groupby: split, apply, combine",
    b2_title="merge, and reconciling two tools",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Your SQL and your pandas give different answers.\n"
              "Which one is wrong?",
              "Usually neither. They are answering slightly different "
              "questions, and finding out which is the actual skill."),

    concepts=[("groupby",
               "Split the rows into groups, apply an aggregation to each, "
               "combine the results into a new table. It is SQL's GROUP BY "
               "and it is your pivot table.",
               "sales.groupby(\"region\")[\"revenue\"].sum() gives one "
               "number per region. Add .reset_index() and you get a proper "
               "table instead of something with a surprising index.",
               "A pivot table. Third time you have met this idea, and that "
               "is deliberate: pivot, then GROUP BY, then groupby."),

              ("Index",
               "The labels down the side of a DataFrame. After a groupby "
               "your grouping keys become the index rather than columns, "
               "which is the commonest confusion in pandas.",
               "by_region[\"region\"] raises KeyError because region is the "
               "index. .reset_index() moves it back into a column and "
               "everything downstream behaves as you expected.",
               "Row headers. In Excel they are just the leftmost column; in "
               "pandas they are a separate thing with its own rules."),

              ("merge, and validate",
               "merge is pandas' join. validate is the argument that makes "
               "it REFUSE a join that would multiply rows instead of "
               "silently doing it.",
               "validate=\"many_to_one\" raises MergeError if the right "
               "side has duplicate keys. There is no reason not to pass it, "
               "and SQL has no equivalent.",
               "VLOOKUP, with a safety catch VLOOKUP does not have.")],

    code=[("groupby, and the four characters that fix it",
           "JUPYTER OR COLAB",
           "sales[\"revenue\"] = (sales[\"quantity\"] * sales[\"unit_price\"]\n"
           "                     * (1 - sales[\"discount\"]))\n"
           "\n"
           "# one key\n"
           "sales.groupby(\"product_id\")[\"revenue\"].sum().head()\n"
           "\n"
           "# several aggregations at once, with readable output names\n"
           "by_cat = (sales.groupby(\"category\")\n"
           "          .agg(revenue_ugx=(\"revenue\", \"sum\"),\n"
           "               lines=(\"revenue\", \"size\"),\n"
           "               mean_line=(\"revenue\", \"mean\"))\n"
           "          .reset_index()\n"
           "          .sort_values(\"revenue_ugx\", ascending=False))\n"
           "by_cat",
           "Leave off .reset_index() and then ask for by_cat[\"category\"]. "
           "KeyError, because category is the index and not a column. Four "
           "characters, and it is the single most common pandas confusion."),

          ("merge, with the guard rails on",
           "JUPYTER OR COLAB",
           "orders = pd.read_csv(\"data/orders.csv\")\n"
           "cust   = pd.read_csv(\"data/customers.csv\")\n"
           "\n"
           "# how= is SQL's join type. validate= is the guard SQL lacks.\n"
           "j = orders.merge(cust, on=\"customer_id\", how=\"left\",\n"
           "                 validate=\"many_to_one\", indicator=True)\n"
           "\n"
           "len(orders), len(j)          # <<orders>>, <<orders>>\n"
           "j[\"_merge\"].value_counts()\n"
           "# left_only is the <<walkins>> walk-in orders, worth "
           "<<walkin_rev>>",
           "Change how=\"left\" to how=\"inner\" and the row count drops to "
           "<<joined>>. Same data, same merge, <<walkin_rev>> gone. Print "
           "the length before and after EVERY merge, exactly as you check "
           "the row count in SQL."),

          ("The same three tables meeting, so region and month exist",
           "JUPYTER OR COLAB",
           "# revenue is on the LINES, region on the customer, month on\n"
           "# the order. All three have to meet before you can group.\n"
           "lines = (sales\n"
           "         .merge(orders[[\"order_id\", \"order_date\", \"status\",\n"
           "                        \"customer_id\"]],\n"
           "                on=\"order_id\", how=\"left\")\n"
           "         .merge(cust[[\"customer_id\", \"region\"]],\n"
           "                on=\"customer_id\", how=\"left\"))\n"
           "\n"
           "lines[\"month\"] = (pd.to_datetime(lines[\"order_date\"])\n"
           "                   .dt.strftime(\"%Y-%m\"))\n"
           "\n"
           "out = (lines[lines[\"status\"] == \"Delivered\"]\n"
           "       .groupby([\"region\", \"month\"])[\"revenue\"]\n"
           "       .sum().reset_index())",
           "Check lines[\"region\"].isna().sum(). It is not zero: the "
           "walk-in lines have no region because the left merge kept them, "
           "which is what you wanted. Now you have to decide what a "
           "regional total means, and say so."),
          ],

    worked=("Reconciling two tools, properly",
            "Same question, same data, different tool. They have to agree, "
            "and where they do not you have found something.",
            ["Export the SQL answer to CSV and read both results into "
             "pandas.",
             "Merge them on rep and month with indicator=True. Any "
             "left_only or right_only row is a difference in WHICH ROWS, "
             "not in the arithmetic.",
             "For rows in both, subtract. A few shillings is rounding; "
             "thousands is a filter or a join.",
             "Check the three usual suspects in order: the status filter, "
             "the date window, and whether one side dropped the "
             "<<walkins>> rows with no customer.",
             "Name every difference. Then stop: a named difference is "
             "finished."],
            "The commonest cause, by a long way, is one side filtering on "
            "status and the other not."),

    splits=[("Checkpoint 2",
             "What to hand in",
             "The pandas rebuild of the session 5 report.\n\n"
             "A reconciliation against the SQL output, row by row.\n\n"
             "The cleaning log from session 8 that produced your starting "
             "numbers.",
             "How it is marked",
             ["Do the numbers agree, and where they do not, is every "
              "difference named?",
              "",
              "Could somebody else reproduce your starting figures from the "
              "log alone?",
              "",
              "Finding a genuine difference and explaining it scores higher "
              "than a clean match you cannot account for."],
             "CHECKPOINT 2 · 15% OF THE MARK")],

    check=(["Your groupby result will not let you select a column you can "
            "see. Why?",
            "A merge turned <<orders>> rows into <<items>>. What happened?",
            "SQL says one figure and pandas says a smaller one. Where do "
            "you look first?"],
           [("Cannot select a column you can see",
             "It is in the index, not the columns. .reset_index() moves the "
             "grouping keys back and everything downstream works."),
            ("A merge that multiplied the rows",
             "Fan-out: the right-hand side had several rows per key, so "
             "every left row was repeated once per match. Pass "
             "validate=\"one_to_many\" and pandas raises instead. Aggregate "
             "the many side first, then merge."),
            ("A gap between SQL and pandas",
             "The filters, first and always: status, the date window, and "
             "whether one side dropped the <<walkins>> rows with no "
             "customer. That last one alone is <<walkin_rev>>. Only look at "
             "the arithmetic once the row sets match.")]),

    lab=("Reconcile pandas against SQL",
         "Rebuild the rep revenue report in pandas and set it beside your "
         "SQL output. Any difference is a finding, and finding one is a "
         "pass. A clean match you cannot explain is not.",
         ["Rebuild the report with groupby and merge.",
          "Print the row count after every merge.",
          "Merge your result against the SQL output with indicator=True.",
          "List every difference and name the cause of each.",
          "Submit with the cleaning log from last session."]),

    closing=("Two tools, one answer",
             "Getting the same number twice, two different ways, is the only "
             "self-check available to somebody working alone. It is also the "
             "first thing you will be asked for when a number of yours is "
             "doubted.",
             "Next week: what the numbers mean, starting from what a "
             "statistic is."),
)

# Placeholders live in da_keys.FMT_BASE, in one place, because sessions
# move between these modules and a private copy goes stale.
FMT = {}
