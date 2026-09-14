# -*- coding: utf-8 -*-
"""Week 4 slide content: sessions 10, 11 and 12.

Statistics from what a statistic IS, then rates and time, then charts from
what an axis is. The figures carry most of the teaching here, because a
distribution cannot be explained in prose to somebody who has never seen one
drawn.
"""
import da_keys as D

DECKS = {}

# ============================================================== SESSION 10
DECKS[10] = dict(
    b1_title="What a statistic is, before any particular one",
    b2_title="The shape decides which statistic is honest",

    question=("THE QUESTION TONIGHT ANSWERS",
              "What is a typical order worth?",
              "There are three defensible answers and they differ by a "
              "factor of five. Choosing between them is tonight."),

    concepts=[("A statistic",
               "One number standing in for many. Every statistic throws "
               "information away, which is exactly what makes it useful and "
               "exactly what makes it dangerous.",
               "<<orders>> order values become one number. Whichever number "
               "you choose, <<orders>> minus one facts have been "
               "discarded, and which ones were discarded is the whole "
               "question.",
               "AVERAGE. You have used it for years; tonight is about when "
               "it is the wrong one."),

              ("Mean, median and mode",
               "The mean is the total divided by the count. The median is "
               "the middle value when you line them all up. The mode is the "
               "commonest value.",
               "Order value here: mean <<mean_order>>, median "
               "<<median_order>>. The mean is <<skew>> times the median. "
               "Both are arithmetically correct and they describe different "
               "things.",
               "AVERAGE, MEDIAN and MODE. The functions are the same; "
               "choosing between them is the part no spreadsheet helps "
               "with."),

              ("Distribution",
               "The shape you get when you count how many values fall in "
               "each band. It is the thing you should look at before "
               "choosing any statistic at all.",
               "The order-value distribution here has one tall bar at the "
               "left and a long thin tail to the right, which is what "
               "almost every business quantity looks like.",
               "A histogram, or a frequency table built with FREQUENCY. "
               "Most people have never drawn one, which is why the mean "
               "gets misused so often."),

              ("Percentile",
               "The value below which a given share of the data falls. The "
               "90th percentile is bigger than nine values in ten.",
               "p10 is <<p10_order>>, the median is <<median_order>>, p90 "
               "is <<p90_order>> and the largest single order is "
               "<<max_order>>. Four numbers, and now you have described "
               "the business honestly.",
               "PERCENTILE. Same function, and the reason to reach for it "
               "is that it survives a skewed distribution.")],

    b1_figs=[("fig_distribution_shapes",
              "Three shapes, and what each one allows you to say",
              "Simulated on purpose, so the shapes are clean. Symmetric: "
              "the mean is fine. Right-skewed: use the median. Bimodal: you "
              "have two populations mixed together and no single statistic "
              "describes them.")],

    b2_figs=[("fig_skew_real",
              "The real order values, with the mean and the median marked",
              "All <<orders>> orders from the course data. The mean sits "
              "above four orders in five, which is why it is a poor answer "
              "to \"what is typical\"."),
             ("fig_percentiles",
              "Four numbers that describe the business honestly",
              "p10, median, p90 and the largest order. Together these say "
              "more than any single statistic can, and none of them "
              "mislead.")],

    code=[("Compute all three by hand first, then trust the function",
           "JUPYTER OR COLAB",
           "# ten numbers, small enough to check on paper\n"
           "vals = [2, 3, 3, 4, 5, 6, 8, 9, 40, 120]\n"
           "\n"
           "print(sum(vals) / len(vals))       # the mean, by hand: 20.0\n"
           "print(sorted(vals)[4:6])           # the middle two: 5 and 6\n"
           "print((5 + 6) / 2)                 # the median, by hand: 5.5\n"
           "\n"
           "import pandas as pd\n"
           "s = pd.Series(vals)\n"
           "print(s.mean(), s.median(), s.mode()[0])\n"
           "\n"
           "# the mean is 20 and eight of the ten numbers are below it.",
           "Remove the 120. The mean drops from 20.0 to about 4.4 and the "
           "median barely moves. One value out of ten moved the mean by a "
           "factor of four, which is what a skewed distribution does to it "
           "every time."),

          ("The same three on the real order values",
           "JUPYTER OR COLAB",
           "order_value = (delivered.groupby(\"order_id\")[\"revenue\"]\n"
           "               .sum())\n"
           "\n"
           "order_value.describe()\n"
           "order_value.mean()                 # <<mean_order_raw>>\n"
           "order_value.median()               # <<median_order_raw>>\n"
           "order_value.quantile([0.1, 0.5, 0.9])\n"
           "\n"
           "# what share of orders are BELOW the mean?\n"
           "(order_value < order_value.mean()).mean()   # about 0.80",
           "That last line is the argument in one number: about 80% of "
           "orders are smaller than the mean. A statistic that is bigger "
           "than four fifths of the thing it describes is not describing it "
           "well."),

          ("Draw it before you choose",
           "JUPYTER OR COLAB",
           "import matplotlib.pyplot as plt\n"
           "\n"
           "fig, ax = plt.subplots(figsize=(9, 4))\n"
           "order_value.plot(kind=\"hist\", bins=60, ax=ax)\n"
           "ax.axvline(order_value.median(), color=\"teal\")\n"
           "ax.axvline(order_value.mean(), color=\"orangered\",\n"
           "           linestyle=\"--\")\n"
           "ax.set_xlabel(\"Order value, UGX\")\n"
           "ax.set_ylabel(\"Number of orders\")\n"
           "ax.set_title(\"Most orders are small; a few are very large\",\n"
           "             loc=\"left\")",
           "Now change bins=60 to bins=5. The skew disappears into one bar "
           "and the chart says the distribution is fine. The bin count is a "
           "choice you are making, and a careless one hides the finding."),
          ],

    check=(["When is the mean the right statistic?",
            "Is the largest order, <<max_order>>, an outlier you should "
            "delete?",
            "Why look at the distribution before choosing a statistic?"],
           [("When the mean is right",
             "When the distribution is roughly symmetric, or when you "
             "genuinely need the total divided by the count, which is what "
             "average order value is for pricing and capacity. As a "
             "description of typical, on a skewed distribution, it is "
             "wrong."),
            ("Is the largest order an outlier to delete?",
             "You cannot tell from the data alone, and deleting it is a "
             "decision about the business rather than about the file. It "
             "might be a typo and it might be your most important "
             "customer. Go and ask. Describe it either way."),
            ("Why look at the shape first",
             "Because the shape is what decides whether a statistic is "
             "honest. Choosing the statistic first and looking at the shape "
             "afterwards is how the mean ends up in board papers where the "
             "median belonged.")]),

    lab=("Describe three columns properly",
         "Pick three numeric columns from the course data. For each: draw "
         "the distribution, choose the right statistic, and write one "
         "sentence saying why the alternative would mislead.",
         ["Draw the histogram first, before choosing anything.",
          "Mean, median and the three percentiles.",
          "Which statistic describes this column honestly?",
          "One sentence: why would the other one mislead?",
          "Then find a column where the mean IS the right answer, and say "
          "why."]),

    closing=("Look at the shape, then pick the number",
             "The order is the whole lesson. A mean reported on a skewed "
             "distribution is the commonest misleading number in business, "
             "and it costs nothing to avoid once you have drawn the "
             "histogram.",
             "Next session: comparing groups of different sizes, and "
             "reading a number that changes over time.",
             ),
    figs_note=True,
)

# ============================================================== SESSION 11
DECKS[11] = dict(
    b1_title="Counts, rates, and the difference that changes the decision",
    b2_title="Growth, or just December?",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Which region has our worst returns problem?",
              "The region with the most returns and the region with the "
              "highest return rate are different regions. Only one of them "
              "is the answer."),

    concepts=[("A rate",
               "A count divided by the population it came from. What you "
               "need whenever the groups you are comparing are different "
               "sizes, which is nearly always.",
               "<<count_top_region>> has the most returns, "
               "<<count_top_n>>. <<rate_top_region>> has the highest RATE, "
               "<<rate_top_pct>> against <<rate_top_pct_east>> in "
               "<<count_top_region>>. Two regions, two different "
               "conversations.",
               "A count is COUNTIF. A rate is COUNTIF divided by COUNT, and "
               "the division is the part people skip."),

              ("Percentage point",
               "The unit for the DIFFERENCE between two percentages. Going "
               "from 2% to 3% is one percentage point and also a fifty per "
               "cent increase, and both statements are true.",
               "Return rates here run from <<rate_bottom_pct>> to "
               "<<rate_top_pct>>. That is a gap of about half a percentage "
               "point, and about a fifth in relative terms. Say which one "
               "you mean.",
               None),

              ("Seasonality",
               "A pattern that repeats on the calendar. It is not growth "
               "and it is not a trend, and confusing either with it "
               "produces a confident wrong headline every January.",
               "December 2025 was <<dec_over_feb>> times February 2024. "
               "December is also the biggest month in BOTH years, which is "
               "what tells you it is the calendar rather than the business.",
               None),

              ("Year on year",
               "Comparing a period against the same period a year earlier. "
               "It is the simplest honest way to see through seasonality.",
               "December against December removes the December effect. "
               "December against November does not, and will tell you the "
               "business is booming every single year.",
               None)],

    b1_figs=[("fig_rate_vs_count",
              "The most returns and the highest return rate are different "
              "regions",
              "Real counts and rates from the course data. Report the "
              "counts and somebody is sent to <<count_top_region>>, which "
              "simply has the most orders. The rate points at "
              "<<rate_top_region>>.")],

    b2_figs=[("fig_seasonality",
              "December is the biggest month in both years",
              "Real monthly revenue with a three-month rolling average. The "
              "December peaks are the calendar, not growth, and the rolling "
              "average is what lets you see the difference.")],

    code=[("Counts and rates, side by side",
           "JUPYTER OR COLAB",
           "# how many returns per region? A count.\n"
           "counts = (lines.groupby(\"region\")[\"returned\"]\n"
           "          .sum().sort_values(ascending=False))\n"
           "\n"
           "# what SHARE of each region's lines came back? A rate.\n"
           "totals = lines.groupby(\"region\")[\"returned\"].size()\n"
           "rates  = (counts / totals).sort_values(ascending=False)\n"
           "\n"
           "print(counts)      # <<count_top_region>> leads\n"
           "print(rates)       # <<rate_top_region>> leads\n"
           "\n"
           "# both are correct. They answer different questions.",
           "Compute the rate as counts / counts.sum() by mistake and every "
           "region's number changes, because you have divided by the total "
           "RETURNS rather than by each region's own lines. The result "
           "still adds to 100% and is still wrong."),

          ("Percentages against percentage points",
           "JUPYTER OR COLAB",
           "best  = rates.min()      # <<rate_bottom_pct>>\n"
           "worst = rates.max()      # <<rate_top_pct>>\n"
           "\n"
           "print((worst - best) * 100)        # percentage POINTS\n"
           "print((worst / best - 1) * 100)    # per cent, relative\n"
           "\n"
           "# the same gap, two units, two very different-sounding\n"
           "# sentences. Both true. Say which one you mean.",
           "Write the relative figure into a report as \"returns are up X "
           "per cent\" without saying what the base was, and somebody will "
           "read it as X percentage points. That is how a half-point gap "
           "becomes a crisis in a summary."),

          ("Trend, or the calendar?",
           "JUPYTER OR COLAB",
           "m = (delivered.set_index(\"order_date\")[\"revenue\"]\n"
           "     .resample(\"ME\").sum())\n"
           "\n"
           "m.plot()                       # the raw monthly series\n"
           "m.rolling(3).mean().plot()     # the trend, noise removed\n"
           "\n"
           "# December 2025 is <<dec_over_feb>>x February 2024.\n"
           "# Growth, or December?\n"
           "m.groupby(m.index.month).mean()    # answer: it is December\n"
           "m.pct_change(12)                   # year on year, honestly",
           "Quote month-on-month growth into January and you will report a "
           "collapse every year. Quote year-on-year and December stops "
           "being news. Both are correct arithmetic and they produce "
           "opposite headlines from identical data."),
          ],

    worked=("Five statements, five verdicts",
            "For each: supported, unsupported, or unanswerable from this "
            "data. Attach a number to every verdict.",
            ["\"A typical order is worth about <<mean_order>>.\" "
             "UNSUPPORTED. That is the mean of a distribution skewed "
             "<<skew>>x. The median, <<median_order>>, is the honest "
             "answer.",
             "\"<<count_top_region>> has our worst returns problem.\" "
             "UNSUPPORTED as stated. It has the most returns and the LOWEST "
             "rate, <<rate_top_pct_east>>. <<rate_top_region>> has the "
             "highest rate at <<rate_top_pct>>.",
             "\"Revenue is growing: December was <<dec_over_feb>>x "
             "February.\" UNSUPPORTED. December is the biggest month in "
             "both years, so that is the calendar. Year on year is the "
             "test.",
             "\"The largest order, <<max_order>>, must be an error.\" "
             "UNANSWERABLE here. Nothing in the data distinguishes a real "
             "bulk order from a typo. You go and ask.",
             "\"Half our orders are under <<median_order>>.\" SUPPORTED, "
             "and true by definition: that is what a median is."],
            "Three of the five were unsupported for the same reason: a "
            "statistic that does not fit the shape of the thing it "
            "describes."),

    check=(["When would you report a count rather than a rate?",
            "Returns went from 2% to 3%. Is that one per cent or fifty?",
            "One check that tells you whether December is growth."],
           [("When a count beats a rate",
             "When the work is proportional to the count: staffing a "
             "returns desk, printing labels, answering calls. "
             "<<count_top_region>> needs the people even though "
             "<<rate_top_region>> has the problem. Report both and say "
             "which question each answers."),
            ("2% to 3%: one or fifty?",
             "Both. One percentage POINT, and fifty per cent in relative "
             "terms. Neither is wrong and the unit has to be stated, "
             "because the two sound completely different to a reader."),
            ("One check for growth against seasonality",
             "Compare the same month a year apart. If December beats "
             "February in both years by a similar factor, it is the "
             "calendar rather than the business.")]),

    lab=("Five statements, five verdicts, with numbers",
         "On your sheet are five statements about this business. Decide "
         "which are supported, which are unsupported and which are "
         "unanswerable, and attach a number to every verdict. Unanswerable "
         "is a real answer and one of them is.",
         ["For each: supported, unsupported, or unanswerable?",
          "Which statistic would you have to compute to decide?",
          "Compute it. Write the number beside your verdict.",
          "For the unanswerable one: what would you have to go and ask?",
          "Then one of your own: a statement about your own work data that "
          "you now suspect is unsupported."]),

    closing=("Rates for how bad, counts for how much work",
             "Both are honest and they answer different questions. Almost "
             "every misleading comparison in business reporting is a count "
             "presented where the reader will hear a rate.",
             "Next session: charts. Starting from what an axis is."),
)

# ============================================================== SESSION 12
DECKS[12] = dict(
    b1_title="The parts of a chart, and the four that matter",
    b2_title="Honesty, and putting the finding in the title",

    question=("THE QUESTION TONIGHT ANSWERS",
              "Can somebody read your chart\n"
              "without you standing next to it?",
              "If it needs narrating, it is a chart for you rather than a "
              "chart for them."),

    b1_figs=[("fig_chart_anatomy",
              "Every part of a chart has a name",
              "You cannot be told to label an axis if nobody has said which "
              "part is the axis. Learn these eight words and every piece of "
              "chart advice you ever read becomes actionable."),
             ("fig_four_charts",
              "Four charts, and the question each one answers",
              "Drawn from the real course data. Pick the chart from the "
              "QUESTION, not from the menu: change over time, comparison "
              "across categories, the shape of one column, or whether two "
              "things move together.")],

    b2_figs=[("fig_axis_honesty",
              "The same real data, twice, telling two different stories",
              "Identical numbers. The left chart does not start at zero, "
              "which turns an ordinary month into a collapse. Neither chart "
              "contains a false number.")],

    concepts=[("Axis",
               "The scale down the side or along the bottom. Every axis "
               "needs a label and a unit, and a value axis usually needs to "
               "start at zero.",
               "\"Revenue, UGX billions\" is a labelled axis. \"Revenue\" "
               "is not, because the reader does not know whether the 2 "
               "means two shillings, two million or two billion.",
               "The same thing Excel calls an axis. The difference is that "
               "here you have to choose the scale deliberately."),

              ("Histogram",
               "A chart of a distribution: values in bands along the "
               "bottom, counts up the side. It is not a bar chart, and the "
               "difference matters.",
               "A bar chart compares named categories. A histogram shows "
               "the shape of ONE column of numbers. You met one in session "
               "10; this is the name for it.",
               "Excel will build you a bar chart if you ask for a "
               "histogram, and the result looks fine and answers a "
               "different question."),

              ("A chart title",
               "One line stating the FINDING. Not the variables, not the "
               "method: the thing you want the reader to leave with, in "
               "words, above the picture.",
               "\"<<region_top>> is our largest region, at "
               "<<region_top_bn>>\" rather than \"Revenue by region\". The "
               "second is the axis labels read aloud.",
               "The default title Excel gives you IS the variables. "
               "Changing it is the single highest-value thing in this "
               "session."),

              ("What a chart hides",
               "Every chart is a summary and every summary drops something. "
               "Naming what yours drops is the difference between a chart "
               "and a claim.",
               "A monthly revenue line hides the <<orders>> individual "
               "orders behind it, including whether one order made a month. "
               "A regional bar hides that <<walkins>> walk-in orders, worth "
               "<<walkin_rev>>, are in no region at all.",
               None)],

    code=[("A line chart nobody has to ask about",
           "JUPYTER OR COLAB",
           "import matplotlib.pyplot as plt\n"
           "\n"
           "fig, ax = plt.subplots(figsize=(10, 4.5))\n"
           "m.plot(ax=ax, linewidth=2)\n"
           "\n"
           "ax.set_title(\"December is the biggest month in both years\",\n"
           "             loc=\"left\", fontsize=14, weight=\"bold\")\n"
           "ax.set_ylabel(\"Revenue, UGX\")\n"
           "ax.set_xlabel(\"\")              # the dates say it already\n"
           "ax.set_ylim(0)                  # START AT ZERO\n"
           "ax.spines[[\"top\", \"right\"]].set_visible(False)",
           "Remove ax.set_ylim(0). matplotlib starts the axis wherever it "
           "likes, and on this series an ordinary month suddenly looks like "
           "a collapse. It is the commonest accidental lie in business "
           "charting and it is one line to prevent."),

          ("A bar chart, sorted by what it is about",
           "JUPYTER OR COLAB",
           "rev = (lines.groupby(\"region\")[\"revenue\"].sum()\n"
           "       .sort_values())            # ascending, for barh\n"
           "\n"
           "fig, ax = plt.subplots(figsize=(9, 4))\n"
           "ax.barh(rev.index, rev / 1e9)\n"
           "ax.set_title(\"<<region_top>> is our largest region\",\n"
           "             loc=\"left\", fontsize=14, weight=\"bold\")\n"
           "ax.set_xlabel(\"Revenue, UGX billions\")\n"
           "for i, v in enumerate(rev / 1e9):\n"
           "    ax.text(v, i, f\" {v:.2f}\", va=\"center\")",
           "Sort it alphabetically instead. The chart still looks "
           "professional, and the ranking, which is the entire point, now "
           "has to be worked out by the reader one bar at a time."),
          ],

    check=(["Your chart is titled \"Revenue by region\". What is wrong "
            "with that?",
            "When is a truncated y axis legitimate?",
            "Name something a monthly revenue line necessarily hides."],
           [("\"Revenue by region\" as a title",
             "It is the axes read aloud. It states the method rather than "
             "the finding, so the reader has to do the analysis themselves. "
             "\"<<region_top>> is our largest region, at "
             "<<region_top_bn>>\" is the same chart doing its job."),
            ("When truncation is legitimate",
             "When zero is not meaningful and the audience knows it: body "
             "temperature, an index, a share price over one day. For "
             "revenue, volumes or counts, start at zero."),
            ("What a monthly line hides",
             "The distribution inside each month. One large order can make "
             "a month, and the line cannot show you that. The largest "
             "single order here is <<max_order>>, which is visible in a "
             "histogram and invisible in a monthly total.")]),

    lab=("Three charts that answer three questions",
         "Take three of the questions from week one and answer each with one "
         "chart. Each gets a title that states its finding, labelled axes "
         "with units, and one sentence underneath naming what it hides.",
         ["Which of the four chart types does each question imply?",
          "Title: the finding, in words, not the variables.",
          "Axis labels with units. Y axis from zero unless you can justify "
          "otherwise.",
          "One annotation pointing at the thing you want seen.",
          "One sentence under each: what does this chart NOT show?"]),

    closing=("Put the finding in the title",
             "It is the cheapest improvement available to any chart you will "
             "ever make, and it forces you to decide what you actually "
             "found. A chart you cannot title has not finished being "
             "analysed.",
             "Next week: a whole investigation, then Power BI, then five "
             "minutes in front of the room."),
)

# Placeholders live in da_keys.FMT_BASE, in one place, because sessions
# move between these modules and a private copy goes stale.
FMT = {}
