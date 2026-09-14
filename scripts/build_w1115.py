# -*- coding: utf-8 -*-
"""Weeks 11 to 15. Weeks 11-13 are full 3-hour teaching sessions, Week 14 is the
Practical Test 2 briefing, Week 15 is Demo Day. Three cohorts."""
import sys, os
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from pptxkit import *   # noqa
from build_week1 import CO, FIG, OUTDIR, FOOT, qrp
from week_content import W11, W12, W13

F = lambda n: os.path.join(FIG, n)
DATE = {11: {"CML3112": "Tue 17 November 2026", "CML3113": "Fri 20 November 2026",
             "CML3111": "Fri 20 November 2026"},
        12: {"CML3112": "Tue 24 November 2026", "CML3113": "Fri 27 November 2026",
             "CML3111": "Fri 27 November 2026"},
        13: {"CML3112": "Tue 1 December 2026", "CML3113": "Fri 4 December 2026",
             "CML3111": "Fri 4 December 2026"},
        14: {"CML3112": "Tue 8 December 2026", "CML3113": "Fri 11 December 2026",
             "CML3111": "Fri 11 December 2026"},
        15: {"CML3112": "Tue 15 December 2026", "CML3113": "Fri 18 December 2026",
             "CML3111": "Fri 18 December 2026"}}
SLOTS = {"CML3112": "Tuesday 11:00–14:00 · Room 106",
         "CML3113": "Friday 08:00–11:00 · Room 105",
         "CML3111": "Friday 11:00–14:00 · Room 115"}

# Team counts drive the Week 13 clinic rotation and the Week 15 fair format.
# ~100 students in CML3112 gives about 22 teams of four or five; the two smaller
# cohorts give ten or eleven.
TEAMS = {"CML3112": 22, "CML3113": 10, "CML3111": 11}
BIG = "CML3112"

MAP15 = [(1, "AI, ML and the engineering problem"), (2, "Where the work happens"),
         (3, "Python as a calculator"), (4, "Collections, loops, files"),
         (5, "pandas and finding data"), (6, "Dirty data, and seeing it"),
         (7, "TEST 1 — Data Investigation"), (8, "The first model"),
         (9, "Classification"), (10, "Can I trust this model?"),
         (11, "Features"), (12, "Model comparison"),
         (13, "Reproducibility"), (14, "TEST 2 — End-to-end ML"),
         (15, "Demo Day and viva")]


# =====================================================================
def week11(code):
    c, w = CO[code], W11[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 11")
    N = 9

    s = s_title(prs, code, "Features: where your\nengineering knowledge enters",
                "Encoding, scaling, and building a column out of physics",
                "WEEK 11  ·  " + DATE[11][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "This is the session where your degree starts to pay. Everything in Weeks 8 to 10 was about "
             "measuring a model honestly; today you change what the model is fed, and a single column built "
             "from a relationship you learned in Year 2 will beat every raw column in the file put together. "
             "The Practical Test 2 specification and rubric are published this week, so you can prepare "
             "against them for three weeks.\n\nTO TEACH: verify the domain feature empirically BEFORE the "
             "session. If the domain-feature demonstration fails, the argument of the week fails with it. Print "
             "the feature dictionary template, the ablation table template and the cohort reference sheet of "
             "standards. Publish the Test 2 specification today.")

    s = s_objectives(prs, [
        "Encode a categorical column, and say what each encoding forces the model to believe.",
        "Scale features, and name which models are sensitive to scale and which ignore it entirely.",
        "Build a feature from a physical relationship in your own discipline.",
        "Measure what a feature was worth by ablation, and report the ones that were worth nothing.",
        "Assemble a ColumnTransformer inside a Pipeline that handles mixed column types without leaking.",
        "Write a feature dictionary another engineer could work from without asking you anything.",
        "Show, with your own evidence, where a domain engineer beats a better programmer."],
        11, "Features and feature engineering")
    notes(s, "Objective 4 is the one that separates this course from a tutorial. A feature you invented that "
             "turns out to be worthless goes in the table with its measured effect beside it. Deleting it "
             "quietly is the thing that costs marks.\n\nTO TEACH: read them out, return at the end.")

    s = s_figure(prs, "How today runs", F("clock_w11.png"),
                 "Nine segments. The Feature Workshop and the Domain Advantage challenge take an hour between "
                 "them, and both of them are you working.",
                 kicker="HOW TODAY RUNS")
    notes(s, "Two long working blocks today: thirty minutes of Feature Workshop and thirty minutes of "
             "Domain Advantage. The teaching in the first half is what you need to get through both of "
             "them.\n\nTO TEACH: keep the two concept blocks to time. The two working blocks are where the learning "
             "happens and they cannot be compressed.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can tell an honest model from a flattering one. Today you change what it is fed.")
    notes(s, "Ten minutes of recall. You can now measure whether a model generalises and you can find a leak. "
             "Today the model stays the same and the columns change.\n\nTO TEACH: collect A9. Reteach anything "
             "the Week 10 challenge showed the room got wrong, especially scaling before the split.")

    s = s_check(prs, [
        "Your training R² is 0.99 and your test R² is 0.61. What is that called, and what would you try first?",
        "Why is a single train/test split a noisy measurement, and what replaces it?",
        "You fitted the scaler on the whole table before splitting it. Which kind of leakage is that, and how "
        "much does it usually inflate the score?"],
        title="Two minutes: what stuck from Week 10?", foot="Answers next slide.")
    notes(s, "Three questions from Week 10, and all three get used within the hour. Question C is the one "
             "today's Pipeline exists to prevent, so if it gives you trouble, go back to your Trust Lab "
             "notebook before the practical.\n\nTO TEACH: thirty seconds in pairs. Take answers from people "
             "who have not spoken yet.")

    s = s_answers(prs, [
        ("Training 0.99, test 0.61?",
         "Overfitting. The model has memorised the training rows. First moves: reduce the model's freedom — a "
         "shallower tree, fewer features — and check with cross-validation that the gap is real rather than "
         "one unlucky split."),
        ("Why is one split noisy?",
         "Because which rows landed in the test set is itself a random draw, and on a few hundred rows that "
         "draw moves the score by several per cent. k-fold cross-validation replaces it: every row gets a "
         "turn in the test fold, and you report a mean with a spread."),
        ("Scaling before the split?",
         "Train-test contamination. The scaler's mean and standard deviation were computed using the test "
         "rows, so the model has seen a summary of data it was going to be judged on. It usually inflates the "
         "score by a small amount — one or two per cent — which is exactly why it survives review.")])
    notes(s, "Answer C is worth reading twice. A leak that inflates a score by fifty per cent gets caught in "
             "five minutes. A leak that inflates it by one per cent gets published, and the Pipeline you "
             "build today is the structural fix for it.")

    # -------- 2
    s = s_segment(prs, 2, N, "A feature is knowledge encoded", 15,
                  "The model knows only what you put in front of it. Today you decide what that is.")
    notes(s, "Fifteen minutes to establish the idea before any syntax. A model has no physics in it, no code "
             "of practice and no site experience; it has the columns you gave it and nothing else.\n\nTO "
             "TEACH: resist showing any encoder until the encoding block. This block is the argument and it is worth "
             "the full fifteen minutes.")

    s = s_question(prs, "TODAY'S QUESTION",
                   '"Your model already has ' + w["domraw"] + '. It is still wrong. What column is missing?"',
                   "The quantity you actually need has already been measured. It is spread across two columns "
                   "of the file you already have, and nobody has combined them yet.")
    notes(s, "Sit with the question before the answer arrives. The quantity that governs " + w["tgt"] + " is "
             "already in your file, split across two columns. " + w["domwhy"] + "\n\nBy the end of the domain-feature block "
             "you will have built that column and measured what it was worth.\n\nTO TEACH: ask the room what "
             "they would measure next if they could measure anything. Then point out that the answer needs no "
             "new measurement at all.")

    s = s_prose(prs, "What a model can and cannot work out for itself", [
        "**It can find a relationship between the columns you gave it**",
        "If the pattern is in the columns, a good model will find it. That is what fitting means.",
        "**It cannot invent a column**",
        "A model given the raw columns will never form " + w["domfeat"] + " on its own unless you ask "
        "it to. A linear model in particular can only add its columns up.",
        "**It has no physics, no code of practice and no site experience**",
        "Every constraint you know from your degree has to arrive as a column, a threshold or a band.",
        "**Which is why the encoding is a modelling decision**",
        "Writing L = 1, M = 2, H = 3 tells the model that H is three times L. If that is untrue, you have "
        "just fed it a false statement about your own plant.",
        "**And why an engineer beats a better programmer here**",
        "A computer scientist can tune the model further. Only you know that " + w["domfeat"] + " is the "
        "quantity that matters.",
        "**This is also where your marks are**",
        "Engineering reasoning carries 20 of the 100 marks in the project rubric, and feature construction is "
        "where a marker can see it."])
    notes(s, "The fourth point is the practical one for today. An encoding is a statement about your system: "
             "one-hot says only 'this row is H', while an ordered number says 'H is three times L and sits "
             "twice as far from L as M does'. Choose the one that is true.\n\nThe last point matters for the "
             "project. A marker cannot see judgement in a score; they can see it in a feature you built with "
             "a stated physical reason beside it.\n\nTO TEACH: ask for one relationship from their own "
             "discipline that a model could never work out from raw columns. Their examples land better than "
             "yours.")

    s = s_define(prs, "Feature engineering",
                 "Building a new column out of the columns you already have, using something you know about "
                 "the physical system, so that the relationship is in a form the model can use.",
                 "From " + w["domraw"] + " and the other columns already in the file you build " +
                 w["domfeat"] + ". " + w["domwhy"],
                 "Collecting more data. Feature engineering takes no new measurements at all. It rearranges "
                 "measurements you already have into the shape the physics is in.")
    notes(s, "The 'do not confuse with' line is the reason this session is worth three hours. Every one of "
             "the five features you build today costs nothing to collect, because the underlying numbers are "
             "already in the file.\n\nOne warning that arrives properly in the ablation segment: a feature "
             "built from a column you would not have at prediction time is a leak wearing a new hat. Ask the "
             "Week 1 timing question of every feature you build — would I really have this before the "
             "outcome?")

    # -------- 3
    s = s_segment(prs, 3, N, "Encoding and scaling", 25,
                  "Two mechanical jobs that both carry a modelling decision inside them.")
    notes(s, "Twenty-five minutes on the two jobs you will do to almost every dataset for the rest of your "
             "career. Both look mechanical and both contain a decision.\n\nTO TEACH: twenty-five minutes. Use "
             "the two figures, then the live Pipeline. Do not teach every encoder scikit-learn offers — two "
             "is enough.")

    s = s_figure(prs, "Text into columns a model can use", F("onehot.png"),
                 "A model does arithmetic, and there is no arithmetic to do on the letter H. One-hot encoding "
                 "gives every value its own column, with a 1 in the rows where it applies and a 0 everywhere "
                 "else.",
                 kicker="ENCODING")
    notes(s, "The lower half of the figure is the part to study. Writing L = 1, M = 2, H = 3 forces a "
             "straight-line model to believe three separate things: that the levels have an order at all, "
             "that the step from L to M is the same size as the step from M to H, and that H is three times "
             "L in whatever the column is measuring. For a product grade none of those is true.\n\nWhere an order really does exist and the "
             "spacing means something, one ordered column is the better feature and it costs you fewer "
             "columns. In your discipline the honest example is " + w["ordinal_eg"] + ".\n\nTO TEACH: put the "
             "cohort's own categorical column on the board and ask the room whether the spacing between its "
             "levels means anything. That question decides the encoding every time.")

    s = s_define(prs, "One-hot and ordinal encoding",
                 "ONE-HOT ENCODING gives each value of a category its own 0/1 column. ORDINAL ENCODING "
                 "replaces the category with a single number that carries an order. CARDINALITY is how many "
                 "distinct values the column has.",
                 "Your " + w["catcol"] + " column holds " + w["catvals"] + ". " + w["catnote"],
                 "The dummy variable trap. With one column per value, the last column is fully determined by "
                 "the others, which makes a linear model's coefficients unstable. Drop one column and the "
                 "problem goes away.")
    notes(s, "On cardinality: one-hot encoding a column with eight values costs you eight columns, and one "
             "with four hundred values costs four hundred. Above about twenty distinct values one-hot "
             "encoding stops being sensible, and the usual moves are to group the rare values into 'other' or "
             "to replace the category with a number that means something physically.\n\nOn the dummy variable "
             "trap: pass drop='first' to OneHotEncoder and it is handled. Tree models do not care about it at "
             "all.\n\nTO TEACH: keep the trap to thirty seconds. It matters for interpreting coefficients and "
             "for very little else at this level.")

    s = s_prose(prs, "Choosing the encoding for a column", [
        "**Ask first whether the spacing between the levels means anything**",
        "If the step from one level to the next is a measurable amount, an ordered number is the better "
        "feature. If it is not, use one-hot.",
        "**Genuinely ordered, in your discipline**",
        w["ordinal_eg"] + ". Here an ordered column is defensible and cheaper.",
        "**Genuinely unordered**",
        "Machine identifiers, pit names, supplier names, operator names. These get one-hot encoding, or they "
        "get replaced by something physical.",
        "**Watch the cardinality**",
        "One-hot encoding a column with 400 values gives you 400 columns, most of them almost all zeros. "
        "Group the rare values or find a physical replacement.",
        "**And watch for identifiers pretending to be features**",
        "A machine ID or a batch number lets a model memorise individual units. It will look good in testing "
        "and tell you nothing about a unit it has never met.",
        "**Encode inside the Pipeline, every time**",
        "Fit the encoder on the training fold only. An encoder fitted on the whole table has already seen "
        "which categories appear in your test rows."])
    notes(s, "The last two points are the ones that cost marks in projects. An identifier column is the "
             "commonest accidental leak in student work: it correlates with the target because particular "
             "units happen to fail, and it generalises to nothing.\n\nOn the last point: a category that "
             "appears only in your test rows will make a naively fitted encoder fail at prediction time. "
             "handle_unknown='ignore' inside the Pipeline is the practical answer.")

    s = s_figure(prs, "Why the units of a column change the answer", F("scaling_effect.png"),
                 "The same sixty machine-hours on two axes. Distance-based methods measure straight-line "
                 "distance in whatever units the columns arrived in, so a column that spans 1,700 units "
                 "drowns out a column that spans 50. Standardisation gives both a vote.",
                 kicker="SCALING")
    notes(s, "The star's nearest neighbour changes when the columns are put on a common scale, and nothing "
             "about the machines changed. Only the units did.\n\nThe list at the bottom of the figure is "
             "worth memorising. k-nearest neighbours, k-means, support vector machines, principal component "
             "analysis, neural networks and any regression with a ridge or lasso penalty all care about "
             "scale. Trees, forests and gradient boosting do not, because a tree splits one column at a time "
             "and '" + w["splitex"] + "' means the same thing whatever the other columns are doing.\n\nTO TEACH: this "
             "is the slide that explains why a Pipeline containing a scaler helps one model and does nothing "
             "for another. Say it plainly, because students otherwise scale everything as a ritual.")

    s = s_define(prs, "Standardisation and min-max scaling",
                 "STANDARDISATION subtracts each column's mean and divides by its standard deviation, so the "
                 "column is centred on zero and measured in standard deviations. MIN-MAX SCALING maps the "
                 "column onto 0 to 1 using its smallest and largest values.",
                 "StandardScaler is the default and it copes with extreme values. MinMaxScaler is the choice "
                 "when a bounded range is required, and one extreme value squashes everything else into a "
                 "narrow band.",
                 "Normalisation of a distribution's shape. Neither of these changes the shape of anything. A "
                 "skewed column is still skewed after scaling, and a logarithm is what changes shape.")
    notes(s, "Practical rule: standardise by default, and use min-max only when something downstream needs a "
             "bounded range.\n\nThe 'do not confuse with' line catches a real misunderstanding. Scaling is a "
             "change of units. If your column has a long tail, a logarithm is the transform that helps, and "
             "you can apply both.\n\nBoth of these must be fitted on the training fold only, which is why "
             "they live inside a Pipeline rather than in a cell of their own.")

    s = s_livecode(prs, "Mixed column types, one Pipeline",
                   "OPEN COLAB — TYPE THIS, THEN CHANGE ONE THING",
                   ('from sklearn.compose import ColumnTransformer\n'
                    'from sklearn.pipeline import Pipeline\n'
                    'from sklearn.preprocessing import StandardScaler, OneHotEncoder\n'
                    'from sklearn.linear_model import ' +
                    ("LogisticRegression" if "recall" in w["metric"]
                     else "LinearRegression") + '\n'
                    '\n'
                    'num = ["' + w["rawcol"] + '", "' + w["rawcol2"] + '", "' + w["featcol"] + '"]\n'
                    'cat = ["' + w["catcol"] + '"]\n'
                    '\n'
                    'prep = ColumnTransformer([\n'
                    '    ("n", StandardScaler(), num),\n'
                    '    ("c", OneHotEncoder(drop="first", handle_unknown="ignore"), cat),\n'
                    '])\n'
                    '\n'
                    'model = Pipeline([("prep", prep), ("fit", ' +
                    ("LogisticRegression(max_iter=1000)" if "recall" in w["metric"]
                     else "LinearRegression()") + ')])\n'
                    'model.fit(X_train, y_train)      # fitted on training rows ONLY\n'
                    'model.score(X_test, y_test)'),
                   "Take the scaler out of the Pipeline, fit it on the whole table, and re-run. The score "
                   "improves a little. That improvement is the test rows leaking into the scaler's mean, and "
                   "it is the leak from Week 10 in a new place.")
    notes(s, "A ColumnTransformer routes each group of columns to its own treatment: numeric columns to the "
             "scaler, categorical columns to the encoder, all in one object. A Pipeline then chains that "
             "object to the model, so when you call fit, both steps are fitted on the training rows and "
             "nothing else.\n\nThis is the structural fix for leakage rather than a tidiness habit. Once your "
             "preprocessing is inside the Pipeline, cross_val_score refits it inside every fold "
             "automatically, and there is no version of the code where you can forget.\n\nhandle_unknown="
             "'ignore' matters in service: a category the encoder never saw during training returns all "
             "zeros instead of stopping with an error. Note what that costs you here. With drop='first' the "
             "dropped baseline category is also encoded as all zeros, so an unknown category is silently "
             "treated as the baseline instead of being flagged. If you need to know when an unseen category "
             "arrives, check the incoming values yourself before they reach the model.\n\n"
             "TO TEACH: make the leak live and show the small "
             "improvement. Small is the teaching point — a one per cent gain is what makes this leak survive "
             "review.")

    # -------- 4
    s = s_segment(prs, 4, N, "Building a domain feature", 25,
                  "One column, built out of a relationship you learned in Year 2.")
    notes(s, "Twenty-five minutes and the centre of the session. One column built from a physical "
             "relationship, against every raw column in the file.\n\nTO TEACH: this demonstration must be "
             "pre-verified. Show the figure, then build the column live on the cohort dataset and read the "
             "two scores out loud.")

    s = s_figure(prs, "One column, built from the physics", F("domain_feature_" + code + ".png"),
                 "The same rows, the same target and the same straight-line fit on both sides. The "
                 "right-hand panel uses " + w["domfeat"] + " in place of the raw column, and no new "
                 "measurement was taken to build it.",
                 kicker="THE DOMAIN FEATURE")
    notes(s, w["domwhy"] + "\n\nThat is why the right-hand panel fits better. The raw column carries part of "
             "the signal, because the other quantity in the expression is varying at the same time and "
             "blurring it. Combine the two and the relationship straightens out.\n\nThe honest caveat, "
             "printed on the figure: this is illustrative data shaped like the real dataset, built so that "
             "the engineered column really is the stronger predictor. Both R² values are computed when the "
             "figure is drawn. You will do the same thing on the real file in the practical and get a "
             "smaller gain.\n\nTO TEACH: state the caveat out loud. Then run it on the real dataset so the "
             "claim is not resting on a synthetic figure.")

    s = s_worked(prs, "Turning a physical relationship into a column",
                 "The routine, using " + w["domfeat"] + " as the example. It works for any relationship you "
                 "can write down.",
                 # Six steps at projector size only fit as one line each. The
                 # reasoning behind steps 4 and 6 is in the notes.
                 ["Write it in symbols first, with units. " + w["domwhy"],
                  "Check every quantity is a column you already have BEFORE the "
                  "outcome is known. Otherwise it is a leak.",
                  "Write the one line: " + w["domcode"] + "  Then name the column "
                  "after its unit.",
                  "Check describe(). An infinity means you divided by zero; an "
                  "impossible range means mismatched units.",
                  "Fit with the column and without it, on the same split. Record "
                  "both numbers in " + w["metric"] + ".",
                  "Write one line in the feature dictionary: what it is, its unit, "
                  "and why you expected it to help."],
                 "Step 6 is what turns a lucky column into engineering. Step 2 is what stops a leak.")
    notes(s, "Step 4 is the one people skip and it catches two real defects. A division that produces "
             "infinity means the denominator was zero in some rows, which pandas will hand you without "
             "complaint and scikit-learn will refuse to fit. An impossible range usually means two columns "
             "were recorded in different units, which is the Week 6 defect arriving in a new place.\n\nStep 6 "
             "is the deliverable. A feature with no stated physical reason is a guess that happened to work, "
             "and it will not survive a viva question.\n\nTO TEACH: work this live on the cohort dataset, "
             "including the describe() check. Deliberately divide by a column containing a zero once so they "
             "see the infinity.")

    s = s_prose(prs, "Five features you could build from your own discipline", [
        "**Build these in the workshop, and measure each one**"] +
        [x for name, why in w["five"] for x in ("**" + name + "**", why)] +
        ["**And one that will not help**",
         w["nohelp"]],
        kicker="MADE CONCRETE", cols=2)
    notes(s, "These five are the core deliverable of the workshop. Each one needs a physical reason written "
             "beside it before you build it, because a reason invented afterwards is not a reason.\n\nThe "
             "last entry is on the slide on purpose. You are expected to find features that do nothing, and "
             "reporting one with its measured effect beside it is worth more than five features that all "
             "happened to help.\n\nTO TEACH: hand out the cohort reference sheet of standards and codes now. "
             "The stretch tier is a feature that encodes a design code or an empirical relation with the "
             "reference cited, and students need the sheet in front of them to attempt it.")

    s = s_define(prs, "Ratio, interaction, and dimensionless group",
                 "A RATIO divides one column by another. An INTERACTION multiplies two columns, so the effect "
                 "of one depends on the level of the other. A DIMENSIONLESS GROUP is a combination whose "
                 "units cancel, which makes it comparable across different plants and scales.",
                 w["domfeat"] + " is the example you will build today. " + w["domwhy"],
                 "A column you built because it improved the score. If you cannot say why you expected it to "
                 "help before you measured it, you have found a coincidence in your training rows.")
    notes(s, "Dimensionless groups are the most portable features you can build, and you already know "
             "several: Reynolds number, water/cement ratio, power factor, factor of safety. A dimensionless "
             "feature has a fair chance of holding on a plant the model has never seen, because it does not "
             "depend on the scale of that plant.\n\nInteractions are worth trying when you know that one "
             "variable's effect depends on another. A linear model cannot discover an interaction on its own; "
             "a tree can approximate one, which is part of why trees often do well on raw columns.")

    s = s_break(prs, 10, after="The Feature Workshop is next, so have Colab open when you come back.")
    notes(s, "Ten minutes. The Feature Workshop after the break runs for thirty minutes and the challenge "
             "follows it, so this is the last break of the session.\n\nTO TEACH: take it. Get the templates "
             "distributed during the break so the Feature Workshop starts on time.")

    # -------- 5
    s = s_segment(prs, 5, N, "The Feature Workshop", 30,
                  "Five features, five stated reasons, and a measured effect for each one.")
    notes(s, "Thirty minutes, all hands on keyboards. Build the five features, then measure each one. The "
             "measuring is the part that carries the marks.\n\nTO TEACH: circulate and ask 'why did you "
             "expect that to help?' before looking at any code. Do not fix syntax — pair students who are "
             "stuck with students who are not.")

    s = s_split(prs, "Practical: the Feature Workshop", "What to build",
                "Five features from your own discipline, each with a stated physical reason written BEFORE "
                "you build it.\n\n"
                "All of it inside a ColumnTransformer in a Pipeline, so nothing is fitted outside the "
                "training fold.\n\n"
                "Then an ablation table: refit the same model with each feature removed in turn, and record "
                "the change in " + w["metric"] + ".\n\n"
                "CORE: five features and a complete ablation table.\n"
                "STRETCH: a feature that encodes a design code, standard or empirical relation from your own "
                "discipline, with the reference cited.",
                "What is marked",
                ["The reason carries the marks.",
                 "",
                 "A feature with a measured",
                 "effect and no stated reason",
                 "scores about half. A feature",
                 "with a good reason that turned",
                 "out to be worthless scores full",
                 "marks when you report it.",
                 "",
                 "Deliverables:",
                 "  the Pipeline notebook",
                 "  a feature dictionary",
                 "  an ablation table"],
                kicker="PRACTICAL — 30 MINUTES")
    notes(s, "The marking emphasis is deliberate. A feature that helped for a reason you can state is "
             "engineering; a feature that helped for no reason you can name is a coincidence you have not "
             "found yet. Write the reason down before you measure, so you cannot invent one afterwards.\n\n"
             "For the stretch tier: " + w["standard"] + " are legitimate sources. Cite the clause.\n\nTO "
             "TEACH: use the reference sheet to unstick teams on the stretch tier. Keep the ablation table "
             "template visible — teams that build five features and never measure them have done half the "
             "work.")

    # -------- 6
    s = s_segment(prs, 6, N, "Measuring what helped", 25,
                  "Take one column away at a time and watch what happens to the error.")
    notes(s, "Twenty-five minutes on the honest method for feature selection. Correlation screening and "
             "importance rankings both mislead; taking a column away and refitting tells you what that "
             "column was worth to this model on this data.\n\nTO TEACH: twenty-five minutes. Figure, "
             "definition, then the loop typed live.")

    s = s_figure(prs, "Ablation: drop one column and refit", F("ablation.png"),
                 "One model per bar, all fitted on the same training rows and scored on the same test rows. "
                 "The dashed line is the full model. A bar to the right of it means the error rose when that "
                 "column was removed, so the column was carrying something.",
                 kicker="ABLATION")
    notes(s, "Read the figure's own note carefully, because it contains the subtlety. In the "
             "civil-engineering worked example above, water and cement look "
             "useless only because the water/cement ratio is already in the model and has "
             "taken what both of them were carrying. A column can be essential to the physics and still be "
             "droppable from the model.\n\nThat is why an ablation table is about this model with these other "
             "columns, rather than about the column in general. Say so when you report it.\n\nBatch number is "
             "on the chart as a reminder: an identifier is not a measurement and it never could have "
             "helped.\n\nTO TEACH: point at the two apparently useless columns and ask why. The answer, that "
             "the ratio has absorbed them, is the whole subtlety of feature selection, and they can reach it "
             "themselves.")

    s = s_define(prs, "Ablation, and a null result",
                 "ABLATION means removing one feature, refitting the same model on the same split, and "
                 "recording how much the chosen metric changed. A NULL RESULT is a feature whose removal "
                 "changes the metric by less than the fold-to-fold spread.",
                 "Drop " + w["five"][0][0] + " from your model and the " + w["metric"] + " gets clearly "
                 "worse, so that column is carrying the model. Drop " + w["nohelp"].split(",")[0] + " and "
                 "nothing measurable happens.",
                 "A feature importance ranking. An importance number tells you how much one fitted model "
                 "used a column. Ablation tells you what happens to the error when the column is gone, which "
                 "is the question you actually asked.")
    notes(s, "The definition of a null result matters. If your five folds give scores spread over 0.4 units "
             "and removing a feature moves the mean by 0.1, you have measured nothing, and the honest entry "
             "in the table is 'no measurable effect' with both numbers shown.\n\nFeature importance from a "
             "random forest is unstable: refit with a different seed and the ranking moves, and correlated "
             "columns split their importance between them so both look weak. Read importance as a hint and "
             "ablate what you intend to claim.")

    s = s_livecode(prs, "Two helpers, so the loop stays short",
                   "OPEN COLAB — TYPE BOTH HELPERS",
                   ('from sklearn.model_selection import cross_val_score\n'
                    '\n'
                    '# The preprocessor names its columns, so it has to be\n'
                    '# rebuilt for each reduced set of columns.\n'
                    'def build(cols):\n'
                    '    prep = ColumnTransformer([\n'
                    '        ("n", StandardScaler(), [c for c in cols if c in num]),\n'
                    '        ("c", OneHotEncoder(drop="first", handle_unknown="ignore"),\n'
                    '              [c for c in cols if c in cat]),\n'
                    '    ])\n'
                    '    return Pipeline([("prep", prep), ("fit", ' +
                    ("LogisticRegression(max_iter=1000)" if "recall" in w["metric"]
                     else "LinearRegression()") + ')])\n'
                    '\n'
                    'def score(cols):\n'
                    '    s = cross_val_score(build(cols), X[cols], y, cv=5,\n'
                    '                        scoring="' +
                    ("recall" if "recall" in w["metric"] else "neg_mean_absolute_error") +
                    '")\n'
                    '    return ' +
                    ("s" if "recall" in w["metric"] else "-s") +
                    '            # ' +
                    ("recall: higher is better" if "recall" in w["metric"]
                     else "flip the sign to get MAE") + '\n'),
                   "Call score() with one column left out, but pass the original model instead of "
                   "build(cols). scikit-learn stops with \"A given column is not a column of the "
                   "dataframe\", because the preprocessor is still asking for the column you removed. That "
                   "error is the reason build() exists.")
    notes(s, "Two short functions, and they exist for one reason each.\n\nbuild() rebuilds the "
             "preprocessor for whichever columns you are keeping. A ColumnTransformer holds the names of "
             "the columns it was given, so handing it a table with one of those columns missing stops the "
             "run.\n\nscore() puts the sign in one place. scikit-learn maximises whatever you give it, so "
             "an error metric arrives negated; flipping it once inside the helper means every number you "
             "read afterwards is the quantity you actually named.")

    s = s_livecode(prs, "The ablation loop", "OPEN COLAB — ONE LOOP, ONE TABLE",
                   ('import pandas as pd\n'
                    '# build() and score() are the two helpers from the last slide\n'
                    '\n'
                    'feats = list(X.columns)\n'
                    'base = score(feats)\n'
                    'rows = [("all features", base.mean(), base.std(), 0.0)]\n'
                    '\n'
                    'for f in feats:\n'
                    '    s = score([k for k in feats if k != f])\n'
                    '    rows.append((f"drop {f}", s.mean(), s.std(),\n'
                    '                 ' +
                    ("base.mean() - s.mean()" if "recall" in w["metric"]
                     else "s.mean() - base.mean()") + '))\n'
                    '\n'
                    '# "worse by" is positive when dropping that column ' +
                    ("lowered\n# recall" if "recall" in w["metric"]
                     else "raised\n# the error") + '. Compare it against the spread column.\n'
                    'pd.DataFrame(rows, columns=["run", "mean", "spread", "worse by"])'),
                   "Change cv=5 to a single train/test split and re-run twice with different seeds. The order "
                   "of your table changes between runs, and you can no longer tell a real contribution from a "
                   "reshuffle of the rows.")
    notes(s, "Three details make this table trustworthy. The spread column is what tells you whether a change "
             "is real: a change smaller than the spread is a null result. cross_val_score refits the "
             "whole Pipeline inside every fold, so the encoder and the scaler are refitted too, and the "
             "ablation is not quietly leaking. And the preprocessor is rebuilt for each reduced column set, "
             "because a ColumnTransformer that names a column you have just dropped raises an error.\n\n"
             "The last column is signed so that positive always means worse. For an error metric that is a "
             "rise in the error; for recall it is a fall in recall. Reading a signed column correctly is "
             "worth doing deliberately, because a sign error here reverses your conclusion about every "
             "feature.\n\nOne cost to know about: this loop fits the model once per "
             "feature per fold. Six features at 5 folds is 35 fits. On a large dataset, cut to cv=3 while you "
             "are developing and run cv=5 for the version you report.\n\nTO TEACH: run it live on the cohort "
             "dataset. The table it produces is the workshop deliverable, so they need to have seen it "
             "built.")

    # -------- 7
    s = s_segment(prs, 7, N, "Challenge: Domain Advantage", 30,
                  "A controlled experiment, and you are both the experimenters and the subjects.")
    notes(s, "Thirty minutes, and the design of the exercise is the lesson. Half the room may use only the "
             "raw columns and may use any model they like. The other half must invent features and may not "
             "change the model.\n\nTO TEACH: pair teams so both conditions are genuinely competitive. Assign "
             "the conditions rather than letting teams choose. Carry the question card and give no answers "
             "for the full thirty minutes.")

    s = s_challenge(prs, "Domain Advantage",
                    "Your team is assigned one of two conditions on the same dataset and the same metric.\n"
                    "RAW COLUMNS: use the columns as they came, and any model you like.\n"
                    "FEATURES: build features from your own discipline, and keep the simple model you were "
                    "given.\n"
                    "Thirty minutes. Then both teams report their score and explain the difference.",
                    ["What physical quantity is missing from the raw columns?",
                     "Which relationship from your degree connects two of them?",
                     "What are the units of your new column?",
                     "Would you have that column before the outcome is known?",
                     "How much did it move " + w["metric"] + "?",
                     "Is that change bigger than your fold-to-fold spread?"])
    notes(s, "The design of this challenge is what makes the point stick. One side may change the model and "
             "not the columns; the other may change the columns and not the model. Whichever side you are on, "
             "the number you report is evidence you generated yourselves.\n\nQuestion 6 is the one that keeps "
             "you honest. A win of less than your fold-to-fold spread is not a win, and saying so out loud "
             "when you are the winning team is worth more marks than the score.\n\nTO TEACH: expected "
             "outcome — " + w["adv_result"] + "\n\nMake both sides report before you comment. If the raw-"
             "column side wins, that is a real result and worth discussing honestly; ask what feature would "
             "have been needed. Do not rig it.")

    # -------- 8
    s = s_segment(prs, 8, N, "Milestone 2, and what to do this week", 10,
                  "What is due, how it is marked, and the Test 2 specification.")
    notes(s, "Ten minutes on Project Milestone 2 and the Practical Test 2 specification, which is published "
             "this week.\n\nTO TEACH: hand out the Test 2 specification and rubric on paper. Three weeks' "
             "notice is the point of publishing it now.")

    s = s_points(prs, "Before you leave the room",
                 [("Project Milestone 2 — due at the start of Week 12",
                   "A cleaned dataset, a feature dictionary covering every column you built, and a first "
                   "properly evaluated model inside a Pipeline. Graded milestone within the project's 25 per "
                   "cent. Your individual contribution log has to be in the repository, and it is read "
                   "against the commit history."),
                  ("Assignment A10 — the feature dictionary and ablation table for your own project",
                   "Five features minimum, each with a physical reason and a measured effect in your own "
                   "metric. Include at least one feature that did not help, with the number that shows it."),
                  ("Practical Test 2 specification is published today",
                   "Individual, offline, on a laboratory machine with no internet and no AI assistants. Two "
                   "hours of practical plus twenty-five minutes of written reasoning, worth 20 per cent. "
                   "Week 14. The rubric is in the specification, and 45 of the 100 marks come from a "
                   "structured answers cell.")],
                 kicker="MILESTONE, ASSIGNMENT AND TEST 2", numbered=False)
    notes(s, "Read the Test 2 specification this week rather than in Week 13. The part worth noticing now is "
             "that 45 of the 100 marks come from a structured answers cell you fill in during the test, so "
             "the marks for framing, metric choice and limits are collected from a form rather than from your "
             "prose. Practise filling one in during the Week 13 studio.\n\nOn A10: a feature dictionary is "
             "one row per column with its name, what it is made of, its unit, and the physical reason. "
             "Another engineer should be able to rebuild your feature set from it without asking you "
             "anything.\n\nTO TEACH: put the PM2 slot times on the board now.")

    # -------- revision
    s = s_summary(prs, [
        "A model knows only the columns you gave it. It has no physics, no code of practice and no site "
        "experience.",
        "One-hot encoding gives each category its own 0/1 column. An ordered number is defensible only when "
        "the spacing between the levels means something.",
        "Identifier columns let a model memorise individual units. They look good in testing and generalise "
        "to nothing.",
        "Distance-based and penalised methods care about scale. Trees, forests and boosting do not, because a "
        "split on one column is unaffected by the units of another.",
        "Every encoder and scaler belongs inside a Pipeline, so it is fitted on the training fold only.",
        "A feature built from a physical relationship needs no new measurement, and " + w["domfeat"] +
        " is the example from your own discipline.",
        "Ablation is the honest measure of what a feature was worth: drop it, refit on the same split, and "
        "record the change with its spread.",
        "A change smaller than the fold-to-fold spread is a null result, and reporting it is part of the "
        "work."])
    notes(s, "Eight statements covering the session. The fourth and the seventh carry the most weight in "
             "Practical Test 2: which models care about scale, and how to show that a feature earned its "
             "place.\n\nTO TEACH: return to the objectives slide and ask for hands against each.")

    s = s_check(prs, [
        "You one-hot encode a supplier column with 340 distinct values. What have you just done to your "
        "model, and what would you do instead?",
        "You add StandardScaler to a random forest and the score does not move. Explain why in one sentence.",
        "Your ablation table says dropping " + w["nohelp"].split(".")[0] + " changes " + w["metric"] + "by 0.05, and "
        "your five folds are spread over 0.30. What do you report?",
        "A team removes a feature because its importance score was low, without ablating. What could they "
        "have got wrong?",
        "You build a feature from a column that is only filled in after the outcome is known. What is the "
        "name for that, and when will you find out?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question C is the one Practical Test 2 will ask in some form. A change smaller than the spread "
             "is not a finding, and knowing that is what stops you defending a feature that did nothing.")

    s = s_answers(prs, [
        ("One-hot on 340 suppliers?",
         "You have added 340 columns, almost all of them zeros, and given the model a way to memorise "
         "individual suppliers. Group the rare ones into 'other', or replace the supplier with something "
         "physical — a delivery distance, a certified grade, a mean historical quality."),
        ("Scaler makes no difference to a forest?",
         "A tree splits one column at a time. The split '" + w["splitex"] + "' selects exactly the same "
         "rows whether " + w["rawcol"] + " is in its own units or in standard deviations, so rescaling a "
         "column cannot change any split."),
        ("0.05 change against a 0.30 spread?",
         "A null result. Report it as 'no measurable effect', with both the change and the spread shown. Then "
         "keep or drop the feature on other grounds — simplicity, cost of collecting it, or whether it is "
         "physically meaningful."),
        ("Dropping a feature on importance alone?",
         "Two things. Importance is unstable, so a different seed gives a different ranking. And two "
         "correlated columns split their importance between them, so both can look weak while the pair is "
         "doing real work. Ablate before you drop."),
        ("A feature built from a column known only afterwards?",
         "Target leakage. Your cross-validated score will look excellent, because the answer is inside the "
         "feature. You will find out when the model reaches service and predicts nothing useful, unless "
         "someone asks the timing question first.")])
    notes(s, "Answer E is the Week 10 lesson arriving inside a feature. Feature engineering is the easiest "
             "place in a project to create a leak, because you are combining columns and it is easy to lose "
             "track of when each one becomes available. Ask the timing question of every feature you build.")

    s = s_glossary(prs, [
        ("Feature engineering", "Building a new column from existing ones using knowledge of the system."),
        ("Categorical column", "A column whose values are labels rather than quantities."),
        ("Ordinal column", "A categorical column whose values have a genuine order."),
        ("Cardinality", "How many distinct values a column has. High cardinality makes one-hot expensive."),
        ("One-hot encoding", "One 0/1 column per category value."),
        ("Ordinal encoding", "One numeric column carrying the order of the categories."),
        ("Dummy variable trap", "With one column per value, the last is determined by the others. Drop one."),
        ("Standardisation", "Subtract the mean, divide by the standard deviation. StandardScaler."),
        ("Min-max scaling", "Map onto 0 to 1 using the smallest and largest values. MinMaxScaler."),
        ("Scale sensitivity", "kNN, k-means, SVM, PCA, neural networks and penalised regression care. Trees "
                              "do not."),
        ("ColumnTransformer", "Routes each group of columns to its own preprocessing step."),
        ("Pipeline", "Chains preprocessing to the model, so everything is fitted on the training fold only."),
        ("handle_unknown", "Tells an encoder what to do with a category it never saw in training."),
        ("Ratio feature", "One column divided by another. Often dimensionless and often portable."),
        ("Interaction", "Two columns multiplied, so one's effect depends on the other's level."),
        ("Dimensionless group", "A combination whose units cancel. Comparable across plants and scales."),
        ("Binning", "Turning a quantity into bands, usually at thresholds from a code or standard."),
        ("Ablation", "Drop one feature, refit on the same split, record the change in the metric."),
        ("Null result", "A change smaller than the fold-to-fold spread. Report it."),
        ("Feature dictionary", "One row per feature: name, inputs, unit, and the physical reason."),
    ], page="1 of 1")
    notes(s, "Twenty terms, and the last two are the ones that appear in the project rubric. A feature "
             "dictionary is a required project artefact, and a null result honestly reported is evidence of "
             "engineering judgement.")

    s = s_prose(prs, "One-page reference — features", [
        "**Encode**",
        "OneHotEncoder(drop=\"first\", handle_unknown=\"ignore\") for unordered categories · one ordered "
        "column where the spacing means something.",
        "**Scale**",
        "StandardScaler by default. Needed by kNN, k-means, SVM, PCA, neural networks and penalised "
        "regression. Ignored by trees, forests and boosting.",
        "**Route and chain**",
        "ColumnTransformer([(\"n\", StandardScaler(), num), (\"c\", OneHotEncoder(), cat)]) inside "
        "Pipeline([(\"prep\", prep), (\"fit\", model)]).",
        "**Build**",
        w["domcode"] + "   " + w["domfeat"] + ", from " + w["domwhy"].split(".")[0] + ".",
        "**Check the new column**",
        "describe() on it. An infinity means you divided by zero. An impossible range means two columns are "
        "in different units.",
        "**Measure**",
        "cross_val_score with the feature and without it, same split, and report the mean with its spread.",
        "**Write it down**",
        "One dictionary row per feature: name, inputs, unit, physical reason. Another engineer should be able "
        "to rebuild your feature set from it.",
        "**Ask the timing question every time**",
        "Would I really have this column before the outcome is known? If not, it is a leak."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide. The timing question at the bottom is the one that will save you most "
             "often, because feature engineering is the easiest place in a project to build a leak without "
             "noticing.")

    s = s_quiz(prs, 11,
               "An ablation table read for which feature earned its place, and a scaler that made no difference "
                        "to a tree.", qr_path=qrp(code, 11))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You built a column out of physics\nand measured what it was worth.",
                  "No new measurements were taken today. " + w["domfeat"] + " was already in your file, "
                  "spread across two columns, and combining them moved the error more than any change of "
                  "model would have. You also have a number for every feature that did nothing.",
                  "Next week: four models under one protocol, and a client who wants a reason.")
    notes(s, "The thing to take from today is that the largest single improvement available to you came from "
             "a relationship you learned in Year 2, applied to columns you already had. Next week you compare "
             "models under a fixed protocol and defend the choice to another team.\n\nTO TEACH: close on the "
             "domain advantage result the room generated, using their own numbers rather than the figure's.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week11_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week12(code):
    c, w = CO[code], W12[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 12")
    N = 7

    s = s_title(prs, code, "Choosing a model,\nand defending the choice",
                "A fair comparison protocol, tuning inside cross-validation, and a client with a constraint",
                "WEEK 12  ·  " + DATE[12][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "The least guided session of the semester. Thirty-five minutes of teaching, then one hundred and "
             "five minutes in which you receive an unfamiliar dataset and a brief from a client, run four "
             "models under one protocol, and write a recommendation. Then another team attacks it. This is "
             "the closest rehearsal you get for Practical Test 2 in two weeks.\n\nTO TEACH: pre-run the four "
             "candidate models on the challenge dataset and confirm that no single model trivially dominates "
             "and that the work fits 90 minutes. Print the client briefs, the question-bank cards, the "
             "recommendation template and the protocol poster. Brief any assistants: questions only, no "
             "answers, for the whole challenge.")

    s = s_objectives(prs, [
        "Design a comparison in which only the model changes, and say what you held constant.",
        "Tune one or two hyperparameters with a search that runs inside cross-validation.",
        "Say when a difference between two scores is too small to be a difference.",
        "Weigh accuracy against interpretability, cost, data hunger and failure behaviour.",
        "Write a one-page recommendation a supervising engineer could act on.",
        "Defend a modelling choice under hostile questioning.",
        "Concede a challenge when the challenge is correct, and say what you would change."],
        12, "Model comparison and engineering judgement")
    notes(s, "Objective 7 is marked today. Conceding a valid criticism and saying what you would change is a "
             "professional strength, and in the defence round it earns marks for both teams.\n\nTO TEACH: "
             "read them out, return at the end.")

    s = s_figure(prs, "How today runs", F("clock_w12.png"),
                 "Eight blocks, and the shape is different this week. Thirty-five minutes of teaching, then "
                 "ninety minutes of your own work with no answers from me, a defence round, and the "
                 "weekly quiz at the end.",
                 kicker="HOW TODAY RUNS")
    notes(s, "Notice the shape. The teaching is compressed into the first thirty-five minutes because you "
             "have already met everything you need; what you have not done is run four models under a single "
             "protocol against a real constraint and had to justify the result.\n\nTO TEACH: say out loud "
             "that you will not answer questions during the challenge, and why. Students who are told to "
             "expect it cope far better.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can build features and measure what they were worth. Today you choose between models.")
    notes(s, "Ten minutes of recall. You can evaluate a model honestly and you can improve what it is fed. "
             "The remaining question is which model, and why that one.\n\nTO TEACH: collect A10. The quiz "
             "closes this session, so say when it will run.")

    s = s_check(prs, [
        "You compare two models and each one got its own random train/test split. What have you learned about "
        "the two models?",
        "Your ablation table says a feature changed the metric by less than the fold-to-fold spread. What is "
        "the honest entry in the table?",
        "Name one model that needs its features scaled and one that does not care at all."],
        title="Two minutes: what stuck from Week 11?", foot="Answers next slide.")
    notes(s, "Question A is this week's whole subject in one line. If the split changed as well as the model, "
             "you cannot say which change moved the number.\n\nTO TEACH: thirty seconds in pairs, then move. "
             "Question A leads straight into the comparison protocol.")

    s = s_answers(prs, [
        ("Two models, two different splits?",
         "Nothing about the two models. Two things changed at once, so you cannot attribute the difference to "
         "either of them. A few per cent of score difference is easily produced by the split alone."),
        ("A change smaller than the spread?",
         "'No measurable effect', with both the change and the spread printed beside it. Then decide whether "
         "to keep the feature on other grounds, such as simplicity or the cost of collecting it."),
        ("Scaled, and indifferent?",
         "k-nearest neighbours needs scaling, because it measures straight-line distance in whatever units "
         "the columns arrived in. A decision tree does not care: a split on one column is unaffected by the "
         "units of any other.")])
    notes(s, "Answer A is the reason the protocol exists. Any comparison in which two things changed at once "
             "is uninterpretable, and this is the commonest way a student leaderboard becomes meaningless.")

    # -------- 2
    s = s_segment(prs, 2, N, "A fair comparison protocol", 20,
                  "What must be held constant, what may vary, and what a leaderboard is worth without one.")
    notes(s, "Twenty minutes on the protocol and the five selection criteria. A table of scores produced "
             "without a protocol carries no information at all, and this is the part people skip.\n\nTO "
             "TEACH: put the protocol poster up and leave it up for the rest of the session.")

    s = s_figure(prs, "Change one thing, hold everything else still", F("comparison_protocol.png"),
                 "The same split from one shuffle with one fixed seed, the same preprocessing fitted inside "
                 "each fold, the same metric chosen before you looked at any result, and the same folds in "
                 "the same order. Only the model on the right changes.",
                 kicker="THE PROTOCOL")
    notes(s, "Four things held constant, one thing varying. That is the whole of fair model comparison.\n\n"
             "The 'same metric chosen before you looked' item is the one that takes discipline. Choosing the "
             "metric after seeing the results means choosing the metric that flatters the model you already "
             "liked, and you will not notice yourself doing it.\n\nThe Pipeline is what makes 'fitted inside "
             "each fold' the default rather than something you have to remember. That is a second reason to "
             "use one, on top of the leakage argument from Week 10.\n\nTO TEACH: write the four constants on "
             "the board and leave them there through the challenge. Teams will refer to them.")

    s = s_define(prs, "Comparison protocol, and a real difference",
                 "A COMPARISON PROTOCOL fixes the split, the folds, the preprocessing and the metric, so the "
                 "only thing varying between runs is the model. A difference between two scores is REAL when "
                 "it is larger than the spread across folds.",
                 "Model A scores 0.82 and model B scores 0.84, and each model's five folds are spread over "
                 "0.06. The two cannot be separated on this data, and the honest report says so.",
                 "A leaderboard. A leaderboard ranks numbers. Without a protocol it ranks the accidents of "
                 "the splits as well as the models, and there is no way to tell the two apart.")
    notes(s, "This definition of a real difference is the most useful thing in the session. Report every "
             "score as a mean with its standard deviation across folds, and when two intervals overlap "
             "heavily, say the two models cannot be separated.\n\nWhat you do then is an engineering "
             "decision, and it is where the other four criteria come in. If two models are equally accurate "
             "and one of them can be read aloud to a client, the choice is already made.\n\nTO TEACH: this "
             "slide is what stops the challenge becoming a score chase. Emphasise it before you release them.")

    s = s_prose(prs, "Five things that decide the choice besides accuracy", [
        "**1 · How much of it you can explain**",
        "A decision you cannot explain line by line often cannot be used at all, whatever it scores. " +
        w["constraint"],
        "**2 · What it costs to train and to run**",
        "A model retrained nightly on a plant server has a budget. A forest of 300 trees answering in "
        "milliseconds is usually fine; something that takes an hour is usually not.",
        "**3 · How much data it needs**",
        "Some methods need thousands of rows to beat a straight line. On four hundred rows the simpler model "
        "frequently wins outright.",
        "**4 · How it behaves when it is wrong**",
        "A model that fails gradually as conditions drift is safer than one that fails suddenly and "
        "confidently. Ask what happens outside the range it was trained on.",
        "**5 · Who has to maintain it**",
        "A model nobody on site understands stops being used within a year. That is a real engineering "
        "constraint and it belongs in your recommendation.",
        "**And the metric itself is a decision**",
        w["metric_note"]],
        kicker="SELECTION CRITERIA")
    notes(s, "Criterion 1 is the one that governs today's challenge. " + w["constraint"] + " A model that "
             "wins on score and loses on that constraint has lost.\n\nCriterion 4 is the one that is easiest "
             "to check and most often skipped. Feed your model an input outside the range it was trained on "
             "and see what it returns. A linear model extrapolates a straight line, which is wrong in a "
             "predictable direction. A tree returns the value of the nearest leaf and gives no sign that it "
             "is out of its depth.\n\nTO TEACH: make criterion 5 concrete with a local example if you have "
             "one. Students find the maintenance argument surprising and remember it.")

    s = s_figure(prs, "Accuracy against explainability, measured", F("tradeoff_map.png"),
                 "Four models on the same rows and the same held-out test set. The vertical axis is measured. "
                 "The horizontal axis is a teaching judgement about how much of the model you could explain, "
                 "and it carries no units.",
                 kicker="THE TRADE-OFF")
    notes(s, "Read the two notes under the chart carefully. On this data the single decision tree is beaten "
             "on both axes: linear regression is more accurate AND easier to explain. A depth-3 tree is not a "
             "safe middle choice by default, and you have to measure.\n\nThe boosting result is the honest "
             "one. Boosting buys a real improvement in R², and if a client has to sign off on why one case "
             "was rejected, that improvement may not be worth having.\n\nThe horizontal axis carries no "
             "units, so do not read distances along it as quantities. It is a way of ordering four models by "
             "how much of them you could put in a report.\n\nTO TEACH: the figure's own caption says the "
             "horizontal axis is a judgement. Point that out — the same honesty you are asking of them.")

    s = s_check(prs, [
        "Name the four things a comparison protocol holds constant.",
        "Your best model scores 0.86 and your second scores 0.85, with folds spread over 0.05. Which do you "
        "recommend, and on what grounds?",
        "Your client has to explain every decision to a regulator. Which two of the five criteria have just "
        "become the deciding ones?"],
        title="Two minutes: check the protocol before you use it",
        foot="Answers next slide. You need all three during the challenge.")
    notes(s, "Three questions to confirm you can run a fair comparison before you are given 90 minutes to do "
             "it unsupervised. Question A is the one to be able to recite.\n\nTO TEACH: pulse check before "
             "the tuning demonstration. If question A is weak, put the four constants back on the board.")

    s = s_answers(prs, [
        ("The four constants?",
         "The split, from one shuffle with one fixed seed. The preprocessing, fitted inside each fold. The "
         "metric, chosen before you looked at any result. And the folds themselves, the same ones in the same "
         "order for every candidate."),
        ("0.86 against 0.85, spread 0.05?",
         "The gap is a fifth of the spread, so the two cannot be separated on this data. Say that, then "
         "recommend on the other criteria: explainability, cost, data hunger, failure behaviour, or "
         "maintenance. Whichever you choose, the reason is what earns the mark."),
        ("A regulator has to be satisfied?",
         "Explainability and failure behaviour. A regulator needs to be told why a particular decision was "
         "made and what happens when the model is wrong, and neither question can be answered from an "
         "accuracy figure.")])
    notes(s, "Answer A is worth memorising word for word, because writing those four lines at the top of your "
             "notebook secures a large part of the modelling protocol marks in Practical Test 2 before you "
             "fit anything.")

    # -------- 3
    s = s_segment(prs, 3, N, "Tuning inside cross-validation", 15,
                  "One worked search, and the reason it has to happen inside the folds.")
    notes(s, "Fifteen minutes and one worked example, deliberately short. This week you do the work.\n\nTO "
             "TEACH: one GridSearchCV, typed live, and stop. Do not demonstrate a second search method.")

    s = s_figure(prs, "A grid search is a table you fill in, then read", F("gridsearch.png"),
                 "Seven depths by four leaf sizes by five folds is 140 models fitted to produce one table. "
                 "Darker is lower error. The ringed cell is the best mean across the same five folds.",
                 kicker="TUNING")
    notes(s, "Read the shape of the table rather than only the winner. In this example depth is doing almost "
             "all of the work and a leaf size of 16 or 50 cripples the tree at every depth, which tells you "
             "which knob matters and which you can leave alone next time.\n\nThe line under the table is the "
             "important one. The search happens inside cross-validation, and the test set takes no part in "
             "choosing the cell. If you pick the winner using the rows you were going to check it with, the "
             "score you report is the score of a lucky guess.\n\nOne consequence worth knowing: the "
             "cross-validated score of the winning cell is slightly optimistic, because you chose it by "
             "looking at those folds. The honest final number comes from the test set you have not touched.\n"
             "\nTO TEACH: say the 140-fits number out loud. Grid search is expensive and students should feel "
             "that before they write a grid with 400 cells.")

    s = s_define(prs, "Parameter and hyperparameter",
                 "A PARAMETER is a number the fitting procedure works out from the data — the coefficients of "
                 "a regression, the thresholds in a tree. A HYPERPARAMETER is a number you choose before "
                 "fitting begins — the depth of the tree, the number of neighbours, the strength of a "
                 "penalty.",
                 "In a depth-4 tree, 4 is a hyperparameter you set. The 15 split thresholds inside it are "
                 "parameters the fit found. A grid search searches hyperparameters, and fitting finds "
                 "parameters.",
                 "Each other, and it matters for what you can search. You cannot grid-search the "
                 "coefficients of a regression: fitting is what produces them.")
    notes(s, "The distinction decides where the search goes. Fitting finds parameters; you choose "
             "hyperparameters and can only find good values by trying them and scoring the result.\n\nA "
             "practical warning: every hyperparameter you add multiplies the size of the grid. Two "
             "hyperparameters with five values each is 25 combinations, which is 125 fits at five folds. "
             "Four hyperparameters with five values each is 3,125 fits. RandomizedSearchCV samples the space "
             "instead of covering it and gets you most of the way for a fraction of the cost.")

    s = s_livecode(prs, "One search, inside the folds", "OPEN COLAB — ONE SEARCH, THEN BREAK IT",
                   ('from sklearn.model_selection import GridSearchCV, train_test_split\n'
                    'from sklearn.pipeline import Pipeline\n'
                    'from sklearn.impute import SimpleImputer\n'
                    'from sklearn.tree import DecisionTreeRegressor\n'
                    '\n'
                    'X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,\n'
                    '                                          random_state=42)\n'
                    '\n'
                    'pipe = Pipeline([("prep", SimpleImputer(strategy="median")),\n'
                    '                 ("fit", DecisionTreeRegressor(random_state=42))])\n'
                    '\n'
                    'grid = {"fit__max_depth": [2, 3, 4, 5, 6, 8, 10],\n'
                    '        "fit__min_samples_leaf": [1, 4, 16, 50]}\n'
                    '\n'
                    'search = GridSearchCV(pipe, grid, cv=5,\n'
                    '                      scoring="neg_mean_absolute_error")\n'
                    'search.fit(X_tr, y_tr)           # the test set is untouched\n'
                    '\n'
                    'print(search.best_params_, -search.best_score_)\n'
                    'print("held-out:", -search.score(X_te, y_te))'),
                   "Change search.fit(X_tr, y_tr) to search.fit(X, y) and re-run. The held-out number "
                   "improves, and it now means nothing: the winning cell was chosen using the very rows you "
                   "then check it against.")
    notes(s, "Three details to carry away. The double underscore in \"fit__max_depth\" names the step and "
             "then the argument, which is how you reach inside a Pipeline. The search is fitted on the "
             "training rows only, so the held-out score on the last line is the one you report. And the "
             "difference between the two printed numbers is worth looking at: the cross-validated best score "
             "is usually a little better than the held-out score, because the cell was chosen by looking at "
             "those folds.\n\nscoring=\"neg_mean_absolute_error\" is negative because scikit-learn maximises "
             "its scores. Flip the sign when you report it.\n\nTO TEACH: run it, then run the broken version. "
             "The improvement is small, which is exactly why this leak survives review.")

    s = s_prose(prs, "Gradient boosting, named and then set aside", [
        "**What it is, in one sentence**",
        "It fits a small tree, looks at what that tree got wrong, fits a second tree to the errors, and keeps "
        "going. XGBoost and LightGBM are the two implementations you will see.",
        "**Why it comes up**",
        "On tabular engineering data it is usually the most accurate thing available, and it wins most public "
        "competitions on data of this shape.",
        "**Why it is not in this course**",
        "It has a dozen hyperparameters that interact, and tuning it well is a skill of its own. Semester 2 "
        "gives it the time it needs.",
        "**What to do with that this week**",
        "You may name it in your recommendation as an option you did not take, with a reason. You may not "
        "submit it as one of your four candidates.",
        "**And the reason the tool is not the lesson**",
        "A boosted model you cannot explain, validated with a protocol you did not fix, is worth less than a "
        "straight line you can defend. The protocol is what this week examines.",
        "**If you want to read ahead**",
        "The XGBoost documentation's own introduction to boosted trees is short and honest, and it will make "
        "more sense after Week 13's work on reproducibility."],
        kicker="DEFERRED TO SEMESTER 2")
    notes(s, "You are told about boosting rather than taught it because you will meet the name immediately in "
             "any Kaggle notebook on data like yours, and a name you have never heard is worse than a name "
             "you have been told is coming.\n\nThe fourth point is the rule for today. Naming boosting as an "
             "option you considered and set aside, with a reason, is a good sentence in a recommendation.\n\n"
             "TO TEACH: sixty seconds of demonstration at most, then the explicit deferral. Say why: the tool "
             "is not the lesson this week.")

    s = s_break(prs, 10)
    notes(s, "Ten minutes. The challenge after the break runs for ninety minutes without a "
             "second break, so use this one.\n\nTO TEACH: take it. Distribute the client briefs and the "
             "recommendation template during the break so the challenge starts on time.")

    # -------- 4
    s = s_segment(prs, 4, N, "Engineering AI Challenge: choose a model and defend it", 90,
                  "An unfamiliar dataset, a client with a real constraint, and no answers from me for the "
                  "next hour and three quarters.")
    notes(s, "Ninety minutes. You get an unfamiliar dataset and a brief from a client, and you "
             "produce a results table for at least four models under one protocol plus a one-page "
             "recommendation. No help, no worked example, and no method suggested.\n\nTO TEACH: circulate with "
             "the question-bank cards and answer nothing for the full 90 minutes. Give time calls at 60, 30 "
             "and 10 minutes remaining. Teams that have not fixed a protocol by minute 20 should be asked "
             "which four things they are holding constant, and nothing else.")

    s = s_question(prs, "YOUR CLIENT, AND WHAT THEY ASKED FOR", w["brief"],
                   "From " + w["client"] + ". Your target is " + w["target"] + ". The constraint is the part "
                   "to read twice: " + w["constraint"])
    notes(s, "Read the brief twice before you touch the keyboard. The constraint is doing more work than the "
             "request. " + w["constraint"] + "\n\nA recommendation that ignores the constraint has answered a "
             "different question from the one you were asked, however good its score is.\n\nTO TEACH: hand "
             "out the printed brief. Do not paraphrase it or explain the constraint — reading a brief "
             "carefully is part of what is being assessed.")

    s = s_challenge(prs, "Choose a Model and Defend It",
                    "Dataset: " + w["dataset"] + ". Target: " + w["target"] + ".\n"
                    "Run at least four candidate models under one protocol you fix and write down first.\n"
                    "Produce a results table and a one-page recommendation.\n"
                    "Ninety minutes. AI assistants are permitted and every use must be logged.",
                    ["What four things are you holding constant?",
                     "Which metric, and what consequence chose it?",
                     "Is your best score really better than your second?",
                     "Does your choice satisfy the client's constraint?",
                     "What did you accept in exchange for what?",
                     "What would change this recommendation?"])
    notes(s, "The six questions on the slide are the ones you will be marked against, so work them in order. "
             "Question 1 comes before any modelling: write the protocol down, then run the four candidates "
             "through it.\n\nQuestion 3 is where most teams lose marks. Report every score as a mean with its "
             "spread across folds, and if the top two overlap, say they cannot be separated and let the "
             "constraint decide.\n\nAI assistants are permitted here and every use goes in the log. Your "
             "recommendation gets defended out loud in the next segment, which is what makes the logging "
             "honest.\n\nTO TEACH: what is in the challenge dataset and the intended reading — " +
             w["planted"] + "\n\nDo not reveal any of that. Mark the protocol and the reasoning. The score "
             "carries nothing on its own.")

    s = s_split(prs, "What to hand in at the end of the challenge", "The results table",
                "One row per candidate model. Columns: the model and its settings, the "
                "cross-validated mean of your metric, the spread across folds, and the held-out score.\n\n"
                "At least four models. All four through the same protocol.\n\n"
                "A line at the top of the table stating the four things you held constant, and the seed you "
                "used.",
                "The one-page recommendation",
                ["1  The model you chose.",
                 "",
                 "2  The metric, and the",
                 "   consequence that chose it.",
                 "",
                 "3  What you accepted in",
                 "   exchange for what.",
                 "",
                 "4  The conditions under which",
                 "   this recommendation would",
                 "   change.",
                 "",
                 "5  Your AI-use log.",
                 "",
                 "One page. Graded in session."],
                kicker="DELIVERABLE — A11")
    notes(s, "One page means one page. A supervising engineer reads the first paragraph and the table, and "
             "everything else has to earn its space.\n\nItem 4 is the one that separates a merit from a pass. "
             "'This recommendation holds while the feed comes from the same source; if the source changes, "
             "refit and recheck the metric' is a sentence a real engineer writes and a student usually "
             "leaves out.\n\nA11 is graded in session and it is the last of the eleven practical challenges."
             "\n\nTO TEACH: collect the pages at the end of the defence round, after teams have had the "
             "chance to annotate them with what they conceded.")

    s = s_worked(prs, "Writing the recommendation",
                 "Five paragraphs and one attachment, in the order a supervising engineer reads them. About "
                 "350 words in total.",
                 # Six paragraphs, one line each on the slide. The worked
                 # example sentences are in the notes, where they can be read
                 # out rather than squinted at.
                 ["State the decision in one sentence, with the number attached.",
                  "Name the metric, and what each kind of mistake costs the client "
                  "in hours, money or safety.",
                  "Show the table. Say whether the top two can be separated at all.",
                  "Say what you accepted in exchange for what.",
                  "State the conditions of use: the input range, and what change "
                  "would require a refit.",
                  "Attach the AI-use log: what you asked, and what you checked."],
                 "The first sentence and the fifth paragraph are the two a supervising engineer will actually "
                 "read. Write those two first.")
    notes(s, "Read these two out as the model answers. Opening: 'We recommend the depth-4 decision tree: "
             "it is within the fold-to-fold spread of the forest, and every decision it makes can be "
             "explained.' Paragraph 4: 'We gave up about 0.02 of F1 against the forest to get a model that "
             "can be read aloud in a rejection notice.'\n\nParagraph 4 is the one that reads as engineering. A trade you can name and quantify shows you "
             "understood the decision; a recommendation that claims the chosen model is best on every axis "
             "shows you did not look.\n\nParagraph 5 is what makes the recommendation usable. A model has a "
             "range of inputs it was trained on, and outside that range its output is a guess. Say where the "
             "boundary is.\n\nTO TEACH: put a good and a bad opening sentence on the board for thirty "
             "seconds. It visibly changes what gets handed in.")

    s = s_prose(prs, "The protocol you must run, written out", [
        "**Fix the split once, and write down the seed**",
        "One shuffle, one seed, one train/test split. Every candidate sees the same rows.",
        "**Put the preprocessing inside the Pipeline**",
        "The scaler and the encoder are fitted inside each fold. Nothing is fitted on the whole table.",
        "**Choose the metric before you look at any result**",
        "Write it at the top of the notebook with the consequence that chose it. Then do not change it.",
        "**Use the same folds, in the same order, for every candidate**",
        "cv=5 with a fixed seed. The same five folds for all four models.",
        "**Report the mean and the spread, every time**",
        "A single number hides whether the difference between two models is real.",
        "**Spend the test set once, at the end**",
        "Choose your model using cross-validation on the training rows. Score the chosen model on the test "
        "rows once and report that number."],
        kicker="NON-NEGOTIABLE")
    notes(s, "This slide is the marking scheme for the protocol part of the challenge. Six items, and a team "
             "that can point at all six in its notebook has secured those marks whatever its scores turn out "
             "to be.\n\nThe last item is the one that gets broken under time pressure. Every time you look at "
             "the test score and then change something, the test set becomes part of your training procedure "
             "and stops being an honest check.\n\nTO TEACH: this is the protocol poster. Print it A3 and put "
             "it on the wall.")

    # -------- 5
    s = s_segment(prs, 5, N, "Defence round", 15,
                  "You present your recommendation to another team, whose job is to attack it.")
    notes(s, "Fifteen minutes. Each team presents its recommendation to another team, which must raise at "
             "least two challenges and hear them answered. The quality of the challenges is marked as well "
             "as the quality of the defences.\n\nTO TEACH: pair teams that took different approaches wherever "
             "you can. Time it strictly: five minutes each way, five minutes to write down what each side "
             "conceded.")

    s = s_prose(prs, "How the defence round runs", [
        "**Five minutes each way**",
        "You present for two minutes and take challenges for three. Then you swap and do the other side.",
        "**The attacking team must raise two challenges**",
        "Aimed at the protocol, the metric, the constraint or the conditions of use. A challenge about the "
        "score alone is the weakest kind.",
        "**A good challenge names the evidence it wants**",
        "'Your top two overlap — show me the fold spreads' can be answered from the notebook. 'I do not "
        "believe you' cannot.",
        "**A good defence answers with the notebook open**",
        "Point at the number. If the challenge is right and you have no answer, say so.",
        "**Conceding earns marks**",
        "Write down what you conceded and what you would change. A team that concedes a correct challenge and "
        "says what it would do differently scores above a team that argues.",
        "**Both sides are marked**",
        "The quality of the challenges you raise counts as much as the quality of your own defence."],
        kicker="THE DEFENCE ROUND")
    notes(s, "The reason conceding is marked is that it is the professional behaviour. In a design review the "
             "engineer who says 'you are right, I checked the wrong thing, here is what I will do' is worth "
             "more than the one who defends a mistake fluently.\n\nWrite the concession down before you leave "
             "the room. It goes on your recommendation as an annotation, and it is read as part of A11.\n\nTO "
             "TEACH: mark the challenges as you circulate. Naming one team's challenge as the best of the "
             "session raises the standard immediately.")

    s = s_worked(prs, "Attacking a recommendation",
                 "Six lines of attack that work on any recommendation, including your own. Try them on "
                 "yourself before the other team does.",
                 ["Ask what was held constant. If the split moved, the table means nothing.",
                  "Ask for the spread. If the top two overlap, what decided between them?",
                  "Ask what the metric costs. " + w["attacks"][0],
                  "Ask them to explain one prediction. " + w["attacks"][1],
                  "Ask about the edge of the data: what comes back for an input "
                  "outside the training range, and does it warn you?",
                  "Ask what would break it. " + w["attacks"][2]],
                 "Every one of these six can be answered from a notebook. That is what makes them fair "
                 "challenges rather than opinions.")
    notes(s, "Run these six on your own recommendation before the defence round. Twenty minutes of attacking "
             "your own work is the cheapest way to find the hole someone else would have found.\n\nThe third "
             "and sixth lines are the ones that turn a modelling exercise into engineering, because they ask "
             "what happens to a real person when the model is wrong.\n\nTO TEACH: these six are the "
             "question-bank cards. Print one card per team.")

    # -------- 6
    s = s_segment(prs, 6, N, "Milestone 3, and what to do this week", 5,
                  "What is due next week, before the quiz closes the session.")
    notes(s, "Five minutes. Project Milestone 3 is due at the start of Week 13.\n\nTO TEACH: keep this to "
             "five minutes, then run the quiz.")

    s = s_points(prs, "Before you leave the room",
                 [("Project Milestone 3 — due at the start of Week 13",
                   "A model comparison table for your own project dataset, with at least three candidates "
                   "under one protocol, and a justified selection. Graded milestone within the project's 25 "
                   "per cent. State the four things you held constant and the seed you used."),
                  ("This week's quiz — five minutes, and two questions come from earlier weeks",
                   "Whether a difference between two models is real given the fold spread, and which model "
                   "a stated constraint selects. From this week on, two of the five are drawn from Weeks 1 "
                   "to 10, so nothing is ever finished with."),
                  ("A11 is graded in session and it is the last practical challenge",
                   "Your one-page recommendation, annotated with what you conceded in the defence round. "
                   "Hand it in before you leave.")],
                 kicker="MILESTONE AND QUIZ", numbered=False)
    notes(s, "The quiz has nothing to memorise. The questions show a comparison table or a snippet of a "
             "pipeline and ask what is wrong with it, so working through today's protocol carefully was the "
             "preparation.\n\nFrom this week the quizzes turn integrative: two of the five come from earlier "
             "weeks. There are two quizzes left after this one and your best ten of twelve count.\n\nTO TEACH: "
             "run the quiz now. Afterwards, look at the responses-by-question view and plan a five-minute "
             "reteach for the start of Week 13 for anything the room got wrong.")

    # -------- revision
    s = s_summary(prs, [
        "A comparison is fair when the split, the folds, the preprocessing and the metric are all held "
        "constant and only the model changes.",
        "A leaderboard without a protocol ranks the accidents of the splits alongside the models, and you "
        "cannot tell them apart.",
        "A difference between two scores is real only when it is larger than the spread across folds. Report "
        "the mean and the spread every time.",
        "A parameter is found by fitting. A hyperparameter is chosen before fitting, and a search is how you "
        "choose it.",
        "The search runs inside cross-validation, and the test set takes no part in choosing anything.",
        "Five criteria decide the choice besides accuracy: explainability, cost, data hunger, failure "
        "behaviour, and who has to maintain it.",
        "A recommendation names the trade you accepted and the conditions under which it would change.",
        "Conceding a correct challenge and saying what you would do differently is a professional strength, "
        "and it is marked."])
    notes(s, "Eight statements covering the session. The third is the one Practical Test 2 will examine, and "
             "the seventh is what the project rubric's engineering reasoning criterion is looking for.\n\nTO "
             "TEACH: return to objectives.")

    s = s_check(prs, [
        "Two models score 0.84 and 0.82, and each one's five folds are spread over 0.06. What do you report?",
        "You tuned max_depth by trying values and checking the test score each time. What have you spent, and "
        "what should you have done?",
        "Your forest beats your linear model by 0.03 of R². The client has to justify every decision in "
        "writing. Which do you recommend, and what is the sentence?",
        "Give one hyperparameter and one parameter for a decision tree, and say which one a grid search can "
        "reach.",
        "A team reports 'random forest, R² = 0.91' and nothing else. Name three things you cannot tell from "
        "that."],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide. Good Practical Test 2 preparation.")
    notes(s, "Question B is the one that costs marks in Practical Test 2. Every time you look at the test "
             "score and then change something, the test set has become part of how you chose the model.")

    s = s_answers(prs, [
        ("0.84 and 0.82, spread 0.06?",
         "That the two cannot be separated on this data. Report both means with their spreads, say the "
         "difference is smaller than the fold-to-fold variation, and then say which of the other five "
         "criteria decided between them."),
        ("Tuning against the test score?",
         "You have spent the test set. It is now part of how you chose the model, so it can no longer tell "
         "you how the model behaves on unseen data. Tune with cross-validation on the training rows, then "
         "score the chosen model on the test rows once."),
        ("Forest by 0.03, client needs a written reason?",
         "Recommend the model you can explain, and say what you gave up: 'we accepted about 0.03 of R² to "
         "get a model whose reasoning can be put in a rejection notice.' A decision that cannot be justified "
         "in writing cannot be used here, whatever it scores."),
        ("Hyperparameter and parameter for a tree?",
         "max_depth is a hyperparameter you set before fitting, and a grid search can reach it. The split "
         "thresholds inside the tree are parameters that fitting produces, and no search touches them."),
        ("'Random forest, R² = 0.91'?",
         "You cannot tell what it was compared against, what protocol produced the number, or how much it "
         "moves between folds. You also cannot tell which metric mattered to the client or what the model "
         "does when it is wrong.")])
    notes(s, "Answer E is the standard your own reporting is held to from here on. A score with no protocol, "
             "no spread and no comparison carries almost no information, and a reviewer's first question will "
             "be one of the three.")

    s = s_glossary(prs, [
        ("Comparison protocol", "The split, folds, preprocessing and metric held constant across candidates."),
        ("Candidate model", "One of the models being compared under the protocol."),
        ("Parameter", "A number the fitting procedure works out from the data."),
        ("Hyperparameter", "A number you choose before fitting begins."),
        ("Grid search", "Try every combination in a table of hyperparameter values."),
        ("Random search", "Sample combinations instead of covering them. Cheaper on large grids."),
        ("Nested search", "The hyperparameter search running inside cross-validation."),
        ("GridSearchCV", "scikit-learn's grid search with cross-validation built in."),
        ("step__argument", "The double-underscore naming that reaches an argument inside a Pipeline step."),
        ("Fold-to-fold spread", "The standard deviation of the score across folds. It sets the resolution."),
        ("Real difference", "A gap larger than the fold-to-fold spread."),
        ("Interpretability", "How much of the model's decision you can explain. Often a requirement."),
        ("Inference cost", "What it costs to produce one prediction in service."),
        ("Data hunger", "How many rows a method needs before it beats a simpler one."),
        ("Failure mode", "How the model behaves when it is wrong, and whether it warns you."),
        ("Conditions of use", "The input range and plant conditions under which the model holds."),
        ("Decision memo", "A one-page recommendation naming the choice, the metric and the trade accepted."),
        ("Gradient boosting", "Trees fitted in sequence to each other's errors. Semester 2."),
        ("Spending the test set", "Using the test score to make a choice. After that it is no longer a check."),
        ("Maintenance burden", "Who retrains it, how often, and what happens when that person leaves."),
    ], page="1 of 1")
    notes(s, "Twenty terms, and five of them are the selection criteria from the comparison-protocol block. The last entry is "
             "the one to keep in mind during Practical Test 2.")

    s = s_prose(prs, "One-page reference — comparing models", [
        "**Fix the protocol first, in writing**",
        "One seed · one split · same folds · preprocessing inside the Pipeline · metric chosen before you "
        "look.",
        "**Search inside the folds**",
        "GridSearchCV(pipe, grid, cv=5, scoring=...).fit(X_train, y_train). The test set takes no part.",
        "**Reach inside a Pipeline**",
        "\"fit__max_depth\" names the step, then the argument. Two underscores.",
        "**Report like this**",
        "model · settings · cross-validated mean · spread across folds · held-out score. Every row, same "
        "protocol.",
        "**Then ask whether the difference is real**",
        "Gap larger than the spread means a difference. Otherwise the two cannot be separated, and something "
        "else has to decide.",
        "**Five criteria besides accuracy**",
        "Explainability · training and inference cost · data hunger · failure behaviour · who maintains it.",
        "**The recommendation**",
        "The choice · the metric and its consequence · the trade you accepted · the conditions of use · the "
        "AI-use log.",
        "**Spend the test set once**",
        "Look at it at the end. Every look that changes a decision turns it into training data."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide and have it open during Practical Test 2. The modelling protocol criterion "
             "carries 20 of the 100 marks and the first two lines of this sheet are most of it.")

    s = s_quiz(prs, 12,
               "Whether a difference between two models is real given the fold spread, and which model a stated "
                        "constraint selects.", integrative=True, qr_path=qrp(code, 12))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You ran four models under one protocol\nand another team attacked the result.",
                  "You fixed a protocol, produced a table that means something, chose a model against a "
                  "constraint rather than a score, and answered two challenges you had not seen. That is what "
                  "a design review feels like.",
                  "Next week: making the whole thing reproducible, and reviewing another team's repository.")
    notes(s, "The part worth keeping from today is that the score was rarely what decided the choice. Once "
             "two models cannot be separated, the constraint decides, and stating that clearly is the "
             "recommendation.\n\nNext week is the studio: repository structure, README, requirements.txt and "
             "peer review, plus the Practical Test 2 briefing.\n\nTO TEACH: name the best challenge raised in "
             "the defence round and say why it was good. Thirty seconds, and it sets the standard for Week 15.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week12_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week13(code):
    c, w = CO[code], W13[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 13")
    N = 7
    teams = TEAMS[code]
    slot = max(4, 85 // teams)

    s = s_title(prs, code, "Work somebody else\ncan actually run",
                "Repository structure, README, environment capture and peer review",
                "WEEK 13  ·  " + DATE[13][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "A studio session. Forty minutes of teaching on what makes work reproducible, then one hundred "
             "minutes in which you build while I run clinic slots, then a peer review round in which you "
             "review another team's repository against the project rubric. Practical Test 2 is briefed at the "
             "end.\n\nTO TEACH: BUILD THE CLINIC BOOKING SHEET BEFORE THE SESSION. This cohort has about " +
             str(teams) + " teams, so 100 minutes gives roughly " + str(slot) + " minutes each. Publish the "
             "slot times before you start and use a printed checklist so each slot is diagnostic rather than "
             "conversational. Prepare the messy-to-clean refactor using a real anonymised student notebook, "
             "with permission. Print the peer review forms and the repository checklist.")

    s = s_objectives(prs, [
        "Structure a repository a stranger could clone and run without asking you anything.",
        "Write a README that states the problem, the data, the method, the result and the limitations.",
        "Capture the environment so the analysis can be rebuilt in a year.",
        "Use relative paths and fixed seeds, and say what each of them prevents.",
        "Report a result with its uncertainty and its conditions of use.",
        "Review another team's repository against the published rubric and give feedback they can act on.",
        "Declare and account for your use of AI assistance."],
        13, "Reproducibility, communication and peer review")
    notes(s, "Objective 6 is the one students find hardest, and it is the one that most improves their own "
             "work. Reviewing somebody else's repository is where you discover the defects in your "
             "own.\n\nTO TEACH: read them out, return at the end.")

    s = s_figure(prs, "How today runs", F("clock_w13.png"),
                 "Eight blocks. The studio is eighty-five minutes of your own build with clinic slots "
                 "running alongside, so check when your slot is before the break.",
                 kicker="HOW TODAY RUNS")
    notes(s, "The studio runs for eighty-five minutes and your clinic slot is about " + str(slot) + " "
             "minutes of it. Teams not in a slot are building or peer-reviewing, so nobody is waiting.\n\n"
             "Come to your slot with the repository checklist already filled in. A slot spent finding out "
             "what is missing is a slot wasted; a slot spent on the two things you could not fix yourself is "
             "worth having.\n\nTO TEACH: put the booking sheet on the wall and the slot times on the board "
             "before the break.")

    s = s_segment(prs, 1, N, "Where we got to", 10,
                  "You can choose a model and defend the choice. Today: making the work checkable.")
    notes(s, "Ten minutes of recall. You have a model you can defend. What you may not have is work anybody "
             "else could run.\n\nTO TEACH: collect A11 annotations if they were not handed in last week. "
             "Reteach anything last week's quiz showed the room got wrong — five minutes, from the "
             "responses-by-question view.")

    s = s_check(prs, [
        "You send your notebook to a colleague and it fails on the first cell. Name the two most likely "
        "causes.",
        "You report an MAE of 3.6 and your colleague reruns your notebook and gets 4.1. What single line "
        "would have prevented that?",
        "Your notebook runs perfectly for you and you have restarted the kernel twice this month. Why is that "
        "not evidence that it works?"],
        title="Two minutes: what stuck from Week 12?", foot="Answers next slide.")
    notes(s, "All three questions are about the gap between 'it works for me' and 'it works'. Question C is "
             "today's subject in one line.\n\nTO TEACH: thirty seconds in pairs. Question C leads straight "
             "into the block on reproducibility.")

    s = s_answers(prs, [
        ("Fails on the first cell?",
         "An absolute path that only exists on your machine, or a package your colleague does not have "
         "installed. A relative path and a requirements.txt fix both, and between them they account for most "
         "first-cell failures."),
        ("3.6 against 4.1?",
         "random_state=42, or any fixed seed, on the split and on the model. Without it, every run draws "
         "different rows into the test set and the number you reported was one sample from a distribution "
         "you never described."),
        ("It works for you?",
         "Because your kernel holds variables from cells you have since edited or deleted, so the notebook "
         "you have on screen and the state it is running in are two different things. Restart and Run All is "
         "the only test that settles it, and it is the acceptance test for today.")])
    notes(s, "Answer C is the Week 2 execution trap arriving at the moment it costs you marks. A notebook "
             "that works only because of variables left in memory from deleted cells will fail on a "
             "reviewer's machine, and Restart and Run All is a ten-second check that finds it.")

    # -------- 2
    s = s_segment(prs, 2, N, "Reproducibility as an obligation", 20,
                  "A result nobody else can reproduce is a claim, and a claim is not evidence.")
    notes(s, "Twenty minutes on why this matters beyond the marks. If a result of yours is questioned in a "
             "review, in a viva or in practice, the repository is what defends it.\n\nTO TEACH: lead with the "
             "professional argument rather than the tidiness argument. Engineering students respond to "
             "'defend your number', and they do not respond to 'keep your files neat'.")

    s = s_question(prs, "THE QUESTION SOMEBODY WILL ASK YOU",
                   '"You reported this number eight months ago. Where did it come from, and would you get it '
                   'again today?"',
                   "You will be asked this in the Week 15 viva, and you will be asked it again in practice. "
                   "The only answer that works is a repository somebody can clone and run.")
    notes(s, "This question arrives in every engineering career, usually at the least convenient moment. "
             "Memory is not evidence and a notebook on your laptop is not evidence either, because you "
             "cannot show that the version you have now is the version that produced the number.\n\nWhat "
             "works is a repository with a fixed environment, fixed seeds and a commit history, because it "
             "lets you rerun the exact analysis and get the exact number.\n\nTO TEACH: if you have a real "
             "story of being asked to defend an old number, tell it here. It carries the segment.")

    s = s_figure(prs, "What a reviewer opens, and in what order", F("repo_structure.png"),
                 "Five things at the top level and two folders inside data/. The numbered items are the order "
                 "a marker actually reads in, and none of them is your model.",
                 kicker="REPOSITORY ANATOMY")
    notes(s, "The order in the figure is the real one. A reviewer reads the README first to find out what the "
             "project is, then requirements.txt to find out whether they can run it, then src/ to see the "
             "code you would defend. The notebooks come after all three.\n\nThe data/raw and data/processed "
             "split is the part students most often skip and most often regret. A raw folder that is never "
             "edited is what lets you answer 'where did this number come from?' a month later. It is also "
             "the only defence against cleaning the same file twice in two different ways, which produces two "
             "different answers and no way to tell which is yours.\n\nYour project folder for this cohort is "
             + w["repo"] + " and your raw file is " + w["datafile"] + ".\n\nTO TEACH: walk the figure in the "
             "numbered order. Then show a real repository, ideally one of your own, and open the files in "
             "that order.")

    s = s_define(prs, "Reproducible, and repeatable",
                 "Work is REPEATABLE when you can run it again yourself and get the same numbers. It is "
                 "REPRODUCIBLE when somebody else can, on a different machine, from what you gave them.",
                 "Restart and Run All on your own machine tests repeatability. Cloning onto a machine that "
                 "has never seen the project, installing requirements.txt and running the notebooks in order "
                 "tests reproducibility.",
                 "Getting the same answer as somebody else who did their own analysis. That is replication, "
                 "and it is a much stronger and much rarer thing.")
    notes(s, "Repeatable is the easy half and it still catches most students, because a notebook depending on "
             "variables from deleted cells is not even repeatable.\n\nReproducible is the standard the project "
             "rubric uses, and it is worth 5 of the 100 marks directly plus a great deal indirectly, because "
             "a marker who cannot run your work cannot award marks for what it does.\n\nA practical note on "
             "seeds: a fixed seed makes the run repeatable and it does not make the result correct. If your "
             "conclusion changes when the seed changes, the honest report says so and gives the spread.")

    s = s_prose(prs, "Capturing the environment, and pinning the randomness", [
        "**requirements.txt is the list of packages and their versions**",
        "pip freeze > requirements.txt writes it. Then pip install -r requirements.txt rebuilds it on any "
        "machine.",
        "**Pin every version with a double equals**",
        "pandas==2.2.1 will still install in two years. 'pandas' installs whatever is current, and an API "
        "that changed in between will break your notebook.",
        "**Set a seed everywhere randomness enters**",
        "The train/test split, the cross-validation folds, and any model with a random component. "
        "random_state=42 in all of them.",
        "**Use relative paths only**",
        "pd.read_csv(\"data/raw/" + w["datafile"] + "\") works on any machine. A path starting C:/Users/ "
        "works on exactly one.",
        "**Never edit data/raw**",
        "Everything in data/processed is rebuilt from raw by code in src/, so it can be deleted and remade at "
        "any time.",
        "**And record the versions of what you cannot pin**",
        "The Python version, and the date you ran it. A line at the top of the README is enough."],
        kicker="ENVIRONMENT AND SEEDS")
    notes(s, "The pinning point is the one that bites later. A requirements.txt listing bare package names is "
             "a list of what you happened to have, and it will install something different next year. Pin the "
             "versions with double equals.\n\nOne practical caution about pip freeze: run it in a clean "
             "virtual environment if you can, because in Colab it will list several hundred packages that "
             "have nothing to do with your project. Listing the six you actually import, with versions, is "
             "better than listing four hundred.\n\nOn seeds: put the seed in one variable at the top of the "
             "notebook and pass that variable everywhere, so there is one place to change it.")

    # -------- 3
    s = s_segment(prs, 3, N, "From a messy notebook to a clean repository", 20,
                  "A real exploratory notebook, refactored live into something a stranger could run.")
    notes(s, "Twenty minutes of live refactoring. The starting notebook is a real one, used with permission, "
             "and it looks like the work most of you have on your machines right now.\n\nTO TEACH: use an "
             "anonymised real student notebook with permission. A synthetic mess does not land, because "
             "students recognise a real one as their own.")

    s = s_prose(prs, "Six things a reviewer sees immediately", [
        "**And every one of them costs marks**"] +
        [x for i, sm in enumerate(w["smells"]) for x in ("**" + str(i + 1) + " ·**", sm)],
        kicker="WHAT TO FIX FIRST", cols=2)
    notes(s, "The third one is the most damaging. Cleaning a file by hand outside the code means the cleaned "
             "file cannot be rebuilt, so nobody can check what you removed and nobody can redo the analysis "
             "with a different cleaning decision. Every cleaning step belongs in code.\n\nThe fifth is the "
             "one that quietly undermines a report. If your headline number moves between runs, the number "
             "you wrote in the brief was one draw from a distribution you never described. Fix the seed, then "
             "report the spread across folds as well.\n\nTO TEACH: put the real notebook on screen and let "
             "the room find these six before you name them. They will find four or five, which is more "
             "effective than being shown all six.")

    s = s_livecode(prs, "The acceptance test, and the environment file",
                   "RUN THIS ON YOUR OWN REPOSITORY NOW",
                   ('# 1 · the acceptance test, in the notebook menu:\n'
                    '#      Kernel  ->  Restart and Run All\n'
                    '#    It either runs top to bottom, or it does not. Nothing in between.\n'
                    '\n'
                    '# 2 · one seed, one place, passed everywhere\n'
                    'SEED = 42\n'
                    'X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,\n'
                    '                                          random_state=SEED)\n'
                    'model = RandomForestRegressor(n_estimators=300, random_state=SEED)\n'
                    '\n'
                    '# 3 · relative paths only\n'
                    'df = pd.read_csv("data/raw/' + w["datafile"] + '")\n'
                    '\n'
                    '# 4 · capture the environment, then read the file and cut it down\n'
                    '#      to the packages you actually import\n'
                    '!pip freeze > requirements.txt'),
                   "Run Restart and Run All right now and watch which cell fails first. Nearly every "
                   "repository in this room will fail on a name that was defined in a cell somebody has since "
                   "deleted.")
    notes(s, "Restart and Run All is the acceptance test for this week and for the project. It clears every "
             "variable from memory and runs the notebook as written, which is the only way to find out "
             "whether the notebook you have on screen is the one that produced your numbers.\n\nThe SEED "
             "variable in one place is a small habit with a large payoff. When a reviewer asks how much your "
             "result moves with the seed, you change one line and rerun.\n\nOn pip freeze in Colab: it will "
             "list several hundred packages. Open the file and keep the ones you import, with their "
             "versions.\n\nTO TEACH: make everyone run Restart and Run All at this point. Two minutes, and a "
             "visible number of hands go up, which makes the rest of the segment sell itself.")

    s = s_prose(prs, "README anatomy — five questions, half a page", [
        "**1 · What problem is this, and who has it?**",
        w["readme"][0],
        "**2 · What data, from where, under what licence?**",
        w["readme"][1],
        "**3 · What method, in three lines?**",
        w["readme"][2],
        "**4 · What is the result, with its unit and its spread?**",
        w["readme"][3],
        "**5 · What are the limitations and the conditions of use?**",
        w["readme"][4],
        "**Then how to run it**",
        "Clone, pip install -r requirements.txt, run the notebooks in numbered order. Four lines, and the "
        "reviewer stops guessing."],
        kicker="THE README")
    notes(s, "Half a page answering five questions. A reviewer who reads this knows whether to keep reading, "
             "which is the whole job of a README.\n\nQuestion 5 is the one that earns the most and gets "
             "written the least. Stating what your model cannot do, and under what conditions it should not "
             "be used, reads as competence rather than weakness, and the project rubric rewards it "
             "directly.\n\nThe two-page engineering brief due in Week 15 is a different document. The README "
             "tells a reviewer how to run your work; the brief tells an engineer what you found and what to "
             "do about it.\n\nTO TEACH: put a good README and a bad one side by side for a minute. Then show "
             "that the good one is shorter.")

    s = s_prose(prs, "Captions that state a finding", [
        "**A caption that describes the axes**",
        w["cap_bad"] + " A reader learns nothing they could not get from the axis labels.",
        "**A caption that states the finding**",
        w["cap_good"],
        "**Why the second one earns marks**",
        "Because it commits to a claim with a number attached, which a reader can check against the chart and "
        "argue with.",
        "**The rule from Week 6, still standing**",
        "Every chart answers a stated question, and the caption says what the answer was.",
        "**In the two-page brief this matters most**",
        "Two pages will hold four or five charts. If each caption states a finding, the brief can be read "
        "from the captions alone.",
        "**One test before you submit**",
        "Read only your captions, in order. Do they tell the story? If they do not, the charts are decoration."],
        kicker="COMMUNICATION")
    notes(s, "The last test is worth doing on every report you ever write. Read the captions in order and "
             "nothing else. If that sequence tells the story, your figures are doing work; if it does not, "
             "you have charts a reader has to interpret for themselves.\n\nCommunication carries 10 of the "
             "100 project marks, and captions are the cheapest place to earn them.")

    s = s_worked(prs, "Moving one cell out of the notebook and into src/",
                 "The refactor that makes a notebook readable. Do this to your cleaning code first, because "
                 "it is the code a reviewer most wants to check.",
                 ["Find a cell that does one job and does it in more than five lines. Cleaning code is almost "
                  "always the first candidate.",
                  "Give the job a name, and write it as a function with named arguments and a docstring "
                  "saying what goes in, what comes out, and in what units.",
                  "Move the function into src/prepare.py. Nothing else moves with it.",
                  "In the notebook, replace the cell with two lines: an import, and one call. The notebook "
                  "now reads as the sequence of steps you took.",
                  "Restart and Run All. If it fails, the function was depending on a variable that was "
                  "sitting in memory, which is exactly the defect you were removing.",
                  "Commit with a message that says what changed and why: 'move duplicate removal into "
                  "src/prepare.py so it can be tested and rerun'."],
                 "A notebook that reads as a sequence of named steps is one a reviewer can follow in two "
                 "minutes. A notebook of forty anonymous cells takes twenty.")
    notes(s, "Step 5 is the one that teaches you something. A function that fails after a restart was reading "
             "a variable from the global state instead of taking it as an argument, and it would have failed "
             "on anyone else's machine.\n\nStep 6 matters for the contribution log. Commit messages are what "
             "your log gets checked against, so 'move duplicate removal into src/prepare.py so it can be "
             "tested' is worth writing and 'update' is not.\n\nTO TEACH: do this live on one cell of the real "
             "notebook. Include the restart, and let it fail if it does.")

    s = s_define(prs, "Relative path, and a fixed seed",
                 "A RELATIVE PATH is written from the repository folder rather than from the root of a disk, "
                 "so it resolves on any machine. A FIXED SEED sets the starting point of every random "
                 "operation, so the same code produces the same numbers every time it runs.",
                 'pd.read_csv("data/raw/' + w["datafile"] + '") is relative and it works everywhere. '
                 "random_state=SEED on the split, the folds and the model pins the randomness.",
                 "A seed making your result correct. A seed makes it repeatable. If the conclusion changes "
                 "when you change the seed, the honest report gives the spread across several seeds.")
    notes(s, "The confusion warning is worth taking seriously, because a fixed seed can hide instability. Try "
             "three or four seeds while you are developing. If your headline number moves by more than you "
             "would be comfortable reporting, that movement is the real result and it belongs in the "
             "brief.\n\nOne more path habit: keep the notebook in notebooks/ and write paths as "
             "\"../data/raw/...\" from there, or set the working directory once at the top. Pick one and be "
             "consistent, because half a repository using each is worse than either.")

    s = s_break(prs, 10, after="Studio time is next: have your repository open.")
    notes(s, "Ten minutes. The studio afterwards runs for eighty-five minutes, so check your clinic slot time "
             "before you go.\n\nTO TEACH: take it. Put the booking sheet and the slot times up during the "
             "break.")

    # -------- 4
    s = s_segment(prs, 4, N, "Studio", 100,
                  "You build. I run clinic slots. Nobody waits, because teams outside a slot are building or "
                  "reviewing.")
    notes(s, "Eighty-five minutes of build time with clinic slots running alongside. Your slot is about " +
             str(slot) + " minutes, so come with the checklist filled in and two specific questions.\n\nTO "
             "TEACH: keep to the booking sheet and use the printed checklist in every slot. With " +
             str(teams) + " teams and " + str(slot) + " minutes each, a slot that becomes a conversation "
             "costs another team its slot. Set a timer.")

    s = s_split(prs, "Studio: what to build in the next hundred minutes", "The target",
                "A repository at " + w["repo"] + " that passes Restart and Run All on a machine that has "
                "never seen it.\n\n"
                "A README answering the five questions, in half a page.\n\n"
                "A requirements.txt with pinned versions of the packages you actually import.\n\n"
                "A contribution log per member, checkable against the commit history.\n\n"
                "An AI-use declaration.\n\n"
                "This is Project Milestone 4: the repository freeze candidate.",
                "Your clinic slot",
                ["About " + str(slot) + " minutes per team.",
                 "",
                 "Bring the checklist already",
                 "filled in, and two specific",
                 "questions.",
                 "",
                 "Slots are on the wall.",
                 "",
                 "Outside your slot: build, or",
                 "start your peer review.",
                 "",
                 "Teams whose repository already",
                 "passes Restart and Run All",
                 "should use the slot on the",
                 "brief and the poster instead."],
                kicker="STUDIO — 85 MINUTES")
    notes(s, "Project Milestone 4 is a repository freeze candidate rather than a final submission. What is "
             "checked is that it runs, that the README answers the five questions, and that the contribution "
             "log matches the commit history.\n\nThe last item on the right is worth reading. If your "
             "repository already passes, the highest-value use of your slot is the two-page brief and the "
             "poster, because those are what Week 15 is assessed on and they are the least practised things "
             "you will hand in.\n\nTO TEACH: circulate between slots. The commonest finding will be an "
             "absolute path and an unpinned requirements file, and both take a minute to fix.")

    s = s_points(prs, "The repository checklist — fill this in before your slot",
                 [("It runs",
                   "Restart and Run All passes from a clean kernel. Every path is relative. requirements.txt "
                   "pins versions of the packages you import. One SEED variable, passed to the split, the "
                   "folds and the model."),
                  ("It explains itself",
                   "README answers the five questions in half a page. data/raw is untouched and "
                   "data/processed is rebuilt by code. Notebooks numbered in reading order. Every chart "
                   "captioned with its finding."),
                  ("It accounts for itself",
                   "A contribution log per member that matches the commit history. An AI-use declaration "
                   "naming what you asked, what came back and what you checked. A conditions-of-use paragraph "
                   "for your model.")],
                 kicker="SELF-ASSESS FIRST", numbered=False)
    notes(s, "Work down this list before your clinic slot and fix everything you can fix yourself. Then bring "
             "the two things you could not.\n\nThe third group is the one teams leave to the last day and it "
             "is worth 5 of the 100 marks on its own, plus it is what makes your individual mark defensible "
             "in the Week 15 viva.\n\nTO TEACH: this is the printed checklist. Hand it out at the start of "
             "the studio and require it filled in as the price of a slot.")

    s = s_prose(prs, "The AI-use declaration", [
        "**What it is**",
        "A short section in the README listing where you used an AI assistant, what you asked it, and what "
        "you did to check the answer.",
        "**Why this course requires it**",
        "Because you are marked on what you can explain. A declaration makes that rule enforceable without "
        "anybody policing your keyboard.",
        "**What a good entry looks like**",
        "'Asked Claude to review our pipeline for leakage. It flagged the scaler outside the split, which we "
        "confirmed by comparing scores before and after the fix.'",
        "**What a weak entry looks like**",
        "'Used AI for help with code.' It says nothing a marker can check and it earns nothing.",
        "**Where it is checked**",
        "The Week 15 viva asks two unseen questions about your own repository. Anything in your repository "
        "that nobody on the team can explain is where the marks go.",
        "**The professional point**",
        "Declaring your tools is normal engineering practice. You cite a standard, a datasheet and a "
        "reference; an assistant belongs in the same list."],
        kicker="DECLARING YOUR TOOLS")
    notes(s, "The third and fourth points are the whole difference. A good entry says what you asked, what "
             "came back and what you did to verify it, and the verification is what is marked.\n\nAI tools "
             "are permitted and taught in the coursework of this course, and they are excluded from both "
             "practical tests by running those offline. The rule is consistent: you are marked on what you "
             "can explain.\n\nTO TEACH: show one strong and one weak declaration. Say plainly that a declared "
             "and verified use costs no marks at all.")

    # -------- 5
    s = s_segment(prs, 5, N, "Peer review round", 15,
                  "You review another team's repository against the rubric, in writing.")
    notes(s, "Fifteen minutes. You review another team's repository against the published project rubric and "
             "return a written review naming two strengths and two specific fixes. Reviewing is harder than "
             "building, and you will find defects in your own work while looking at theirs.\n\nTO TEACH: use "
             "the pairing you prepared. Collect the review forms — they are marked, and the reviewed team "
             "must submit a written response to them.")

    s = s_prose(prs, "Reviewing another team's repository", [
        "**Start by trying to run it**",
        "Clone it, install requirements.txt, Restart and Run All. Ten minutes of your fifteen, and it finds "
        "more than reading ever will.",
        "**Then read the README against the five questions**",
        "Problem, data and licence, method, result with its unit, limitations. Note which are missing rather "
        "than rewriting them.",
        "**Check one number end to end**",
        "Pick the headline result and trace it back through the notebook to the raw file. If you cannot, that "
        "is your most useful finding.",
        "**Mark against the rubric they were given**",
        "A team that made a different defensible choice has not made an error. Say what the rubric asks and "
        "where their work sits against it.",
        "**Name two strengths and two specific fixes**",
        "Specific means a file and a line. 'Improve the documentation' is unusable; 'README has no licence "
        "for the dataset' can be fixed in a minute.",
        "**And expect to fix your own repository afterwards**",
        "Most teams find one of their own defects while reviewing somebody else's. That is the intended "
        "outcome of the round."],
        kicker="PEER REVIEW")
    notes(s, "The 'mark against the rubric' point is where inexperienced reviewers go wrong. There is often "
             "more than one defensible choice, and a team that scaled with MinMaxScaler where you used "
             "StandardScaler has not made a mistake. Review against the published criteria.\n\nThe third "
             "point is the highest-value ten minutes you can spend. Tracing one headline number back to the "
             "raw file tests the whole chain at once, and when it cannot be done, the reason is always "
             "something worth reporting.\n\nTO TEACH: the review forms are keyed to the rubric. Mark the "
             "quality of the reviews as well as the repositories.")

    s = s_worked(prs, "A review comment somebody can act on",
                 "Four parts, and then two rules for the set. A comment missing any of the four wastes the "
                 "reviewer's time and the author's.",
                 ["Where it is. The file and, where you can, the line or the cell number.",
                  "What you observed. Something checkable: 'cell 12 reads C:/Users/amina/Desktop/data.csv'.",
                  "What it means for the reader. 'The notebook cannot run on any other machine, so I could "
                  "not verify any of your numbers.'",
                  "What would fix it. 'Move the file into data/raw/ and read it with a relative path.'",
                  "Then rank your findings, and lead with the one that blocked you. A reviewer who lists nine "
                  "small things and buries the blocker has not helped.",
                  "And write one genuine strength with the same specificity. 'Your ablation table reports two "
                  "features that did nothing, with the numbers' is a real compliment; 'good work' is not."],
                 "A comment with all four parts takes ninety seconds to write and saves the other team an "
                 "hour of guessing.")
    notes(s, "Part 3 is the one that changes how a comment is received. Saying what the defect meant for you "
             "as a reader turns a criticism into information, and it also tells the author how much it "
             "matters.\n\nThe last step matters more than it looks. Specific praise tells a team which of "
             "their choices to keep, and it is the part of a review most likely to be acted on.\n\nTO TEACH: "
             "put one good and one useless comment on the board. Thirty seconds, and the quality of the "
             "written reviews visibly improves.")

    # -------- 6
    s = s_segment(prs, 6, N, "Practical Test 2 briefing", 5,
                  "The format, the rules and the rubric, restated with a week to go.")
    notes(s, "Five minutes restating the Test 2 format you were given in Week 11. The last quiz of the "
             "semester closes the session.\n\nTO TEACH: hand out the Test 2 information sheet again. "
             "Confirm the room, machine allocation and sitting times now — for a cohort of this size that "
             "must already be timetabled.")

    s = s_points(prs, "Before you leave the room",
                 [("Practical Test 2 is next week",
                   "Individual and offline, on a laboratory machine with no internet and no AI assistants. "
                   "Two hours of practical plus twenty-five minutes of written reasoning, worth 20 per cent. "
                   "You get an unfamiliar dataset from your own discipline. The full briefing deck is issued "
                   "with this one, and 45 of the 100 marks come from a structured answers cell."),
                  ("The last quiz of the semester — five minutes, and it closes today",
                   "Reproducibility, with two of the five drawn from earlier weeks. Worth one per cent, and "
                   "your best ten of twelve count, so this is the last score you can bank."),
                  ("Project Milestone 4 and Week 15",
                   "PM4 is today's repository freeze candidate plus the peer review you received and your "
                   "written response to it. Due at the Week 15 session: the repository, a two-page "
                   "engineering brief, a one-page poster, the AI-use declaration, your individual "
                   "contribution log and a 500-word reflection.")],
                 kicker="TEST 2, THE LAST QUIZ AND WEEK 15", numbered=False)
    notes(s, "The most useful preparation for Test 2 next week is the studio you just ran. Practise "
             "Restart and Run All, practise writing a five-question README quickly, and practise filling in "
             "a structured answers cell, because 45 of the 100 marks come from one.\n\nOn Week 15: the "
             "two-page brief and the one-page poster are the least practised things you will hand in all "
             "semester, and there is no session between the test and Demo Day. Draft both this week.\n\nTO "
             "TEACH: run the quiz now. Say clearly that it is the last of the twelve and that the best ten "
             "count.")

    # -------- revision
    s = s_summary(prs, [
        "Work is repeatable when you can rerun it. It is reproducible when somebody else can, on another "
        "machine, from what you gave them.",
        "Restart and Run All from a clean kernel is the acceptance test. A notebook that only works because "
        "of variables in memory will fail on a reviewer's machine.",
        "Relative paths and pinned package versions between them prevent most first-cell failures.",
        "One SEED variable, passed to the split, the folds and the model. A seed makes a run repeatable and "
        "says nothing about whether the result is right.",
        "data/raw is never edited. Everything in data/processed is rebuilt from raw by code, so it can be "
        "deleted and remade.",
        "A README answers five questions in half a page: problem, data and licence, method, result with its "
        "unit, limitations and conditions of use.",
        "Every caption states a finding with a number in it. Read your captions in order and they should tell "
        "the story.",
        "A review comment names the file, what you observed, what it meant for the reader, and what would fix "
        "it.",
        "An AI-use declaration says what you asked, what came back, and what you did to check it. The "
        "checking is what is marked."])
    notes(s, "Nine statements. The second is the one to act on before you leave the room, and the fourth is "
             "the one that will come up in your viva.\n\nTO TEACH: return to objectives.")

    s = s_check(prs, [
        "A reviewer clones your repository and the first cell fails. Name the two most likely causes and the "
        "fix for each.",
        "Your requirements.txt lists 'pandas' and 'scikit-learn' with no versions. What will go wrong, and "
        "when?",
        "You fixed the seed and your reported MAE is now stable. A reviewer asks how much it moves with the "
        "seed. What should you have measured?",
        "Your notebook cleans the raw file in place and overwrites it. Name two things you can no longer do.",
        "You are reviewing a team that made a different but defensible modelling choice from yours. What do "
        "you write?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide.")
    notes(s, "Question D is the one that ends projects. Overwriting your raw file removes the only record of "
             "what you started with, and no amount of care afterwards gets it back.")

    s = s_answers(prs, [
        ("First cell fails on a clone?",
         "An absolute path, fixed by moving the file into data/raw and reading it with a relative path. Or a "
         "missing package, fixed by a requirements.txt with pinned versions. Those two account for most "
         "first-cell failures."),
        ("Unpinned versions?",
         "You have recorded which packages you used and not which versions, so a later install gets whatever "
         "is current. It will break when an API changes, which usually happens months later when you have "
         "forgotten the analysis. Write pandas==2.2.1."),
        ("How much does it move with the seed?",
         "Run three or four seeds and report the spread, or report the cross-validated mean with its standard "
         "deviation across folds. A single number from a fixed seed describes one draw, and the spread is "
         "what tells a reader how much confidence it deserves."),
        ("Cleaning the raw file in place?",
         "You can no longer say what the data looked like when it arrived, and you can no longer redo the "
         "analysis with a different cleaning decision. You have also made a second run of the same notebook "
         "clean an already-cleaned file, which may quietly change the numbers again."),
        ("A different defensible choice?",
         "Say that it is defensible, and review it against the rubric instead of against your approach. Then "
         "ask the question that tests it: what did that choice cost, and did they measure it? A reviewer's "
         "job is to check the reasoning rather than to impose their own method.")])
    notes(s, "Answer C is the standard your project brief is held to. A result reported without a spread "
             "gives a reader no way to judge how much of it is signal, and adding the spread costs you one "
             "line.")

    s = s_glossary(prs, [
        ("Repeatable", "You can run it again yourself and get the same numbers."),
        ("Reproducible", "Somebody else can, on another machine, from what you gave them."),
        ("Repository", "The project folder, with its history. The unit of work you hand in."),
        ("README.md", "Half a page answering five questions. The first thing a reviewer opens."),
        ("requirements.txt", "The packages and their pinned versions. pip install -r rebuilds them."),
        ("pip freeze", "Writes the installed packages and versions. In Colab, cut the output down."),
        ("Pinned version", "pandas==2.2.1 rather than pandas. What makes an install reproducible."),
        ("Relative path", "Written from the repository folder, so it resolves on any machine."),
        ("Absolute path", "Written from the root of a disk. Works on exactly one machine."),
        ("Seed (random_state)", "Pins every random operation so a run is repeatable."),
        ("Restart and Run All", "Clears memory and runs the notebook as written. The acceptance test."),
        ("data/raw", "Exactly as it arrived. Never edited, never overwritten."),
        ("data/processed", "Rebuilt from raw by code in src/, so it can be deleted and remade."),
        (".gitignore", "Keeps large data files and secrets out of the commit history."),
        ("src/", "The functions the notebooks call. Code you would defend lives here."),
        ("Commit message", "What changed and why. This is what your contribution log is checked against."),
        ("Contribution log", "Who did what, with commit evidence. Required per member."),
        ("AI-use declaration", "What you asked, what came back, what you checked. The checking is marked."),
        ("Conditions of use", "The input range and plant conditions under which your model holds."),
        ("Peer review", "Reviewing another team's work against the published rubric, in writing."),
    ], page="1 of 1")
    notes(s, "Twenty terms, and the practical five are Restart and Run All, relative path, pinned version, "
             "seed and data/raw. Between them they cover most of what makes work checkable.")

    s = s_prose(prs, "One-page reference — a repository somebody can run", [
        "**The folder**",
        w["repo"] + " with README.md · requirements.txt · data/raw · data/processed · notebooks/ · src/ · "
        ".gitignore",
        "**The acceptance test**",
        "Restart and Run All from a clean kernel. Then clone onto another machine, install, and run it again.",
        "**Paths**",
        'pd.read_csv("data/raw/' + w["datafile"] + '") — relative, always. Never C:/Users/.',
        "**Randomness**",
        "SEED = 42 at the top, passed to the split, the folds and the model. Then report the spread as well.",
        "**Environment**",
        "pip freeze > requirements.txt, then cut it down to what you import and pin every version with ==.",
        "**README, five questions, half a page**",
        "Problem · data and licence · method · result with its unit and spread · limitations and conditions "
        "of use.",
        "**Captions**",
        "State the finding with a number. Read your captions in order and they should tell the story.",
        "**Review comment**",
        "File and line · what you observed · what it meant for the reader · what would fix it."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "Photograph this slide. Reproducibility and documentation carries 5 of the 100 project marks "
             "directly, and it gates the rest, because a marker who cannot run your work cannot award marks "
             "for what it does.")

    s = s_quiz(prs, 13,
               "A notebook that will not run elsewhere, a hard-coded path, and a seed that was never set.", integrative=True, qr_path=qrp(code, 13))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "Your repository now runs on a machine\nthat has never seen it.",
                  "You cloned somebody else's work, tried to run it, and found out what was missing. Then "
                  "somebody did the same to yours. Everything you hand in from here on can be checked by a "
                  "stranger, which is what makes your numbers defensible.",
                  "Next week: Practical Test 2. Two hours, offline, an unfamiliar dataset from your own "
                  "discipline.")
    notes(s, "The peer review round is what makes today stick. Trying to run somebody else's repository "
             "teaches you more about your own than any checklist, and most teams find one of their own "
             "defects while looking at another team's.\n\nPractical Test 2 is next week. The best preparation "
             "is redoing today's studio work on a different dataset, and practising the structured answers "
             "cell.\n\nTO TEACH: end by confirming the test room, the sitting time and what to bring. Do not "
             "let anyone leave uncertain about where to be.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week13_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week14(code):
    """A briefing deck. Week 14 is Practical Test 2, so there is no teaching."""
    c = CO[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 14")

    s = s_title(prs, code, "Practical Test 2",
                "End-to-end engineering machine learning · what it is, how it runs, how it is marked",
                "WEEK 14  ·  " + DATE[14][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "This deck is the briefing for Practical Test 2 and it is issued with the Week 13 material, a "
             "week before the test. Read all of it. Everything about the format, the rules, the timing, the "
             "tasks and the rubric is here, so nothing in the room should surprise you.\n\nThe last section "
             "is revision covering Weeks 8 to 13.\n\nTO TEACH: issue this deck in Week 13. On the day, read "
             "the rules slide aloud from the screen and confirm the offline state of every machine before "
             "distributing task sheets. Author three parallel dataset variants of matched difficulty with a "
             "model answer and mark scheme each, and seat them in a checkerboard pattern.")

    s = s_points(prs, "What this test is",
                 [("Individual, offline, on a laboratory machine",
                   "No internet, no AI assistants, no messaging. The offline documentation bundle is on every "
                   "machine and it includes the scikit-learn API reference, because this test examines your "
                   "judgement rather than your memory of parameter names."),
                  ("Two hours of practical, then twenty-five minutes of writing",
                   "Part A is an end-to-end piece of work on a dataset from your own discipline that you have "
                   "never seen. Part B is four written questions with no computer, and it is collected "
                   "separately."),
                  ("Worth 20 per cent of the semester mark",
                   "Only the ML project carries more. Weeks 8 to 13 are what is examined, and there are no "
                   "new concepts in it.")],
                 kicker="THE FORMAT", numbered=False)
    notes(s, "The offline bundle including the scikit-learn documentation is deliberate. You are not being "
             "tested on whether you remember that the argument is called min_samples_leaf; you are being "
             "tested on whether you know why you would change it.\n\nThe two parts are collected separately "
             "and marked separately. Part B carries the reasoning marks and it has no computer, so a strong "
             "Part A with an empty Part B loses a large amount.")

    s = s_figure(prs, "How the session runs", F("clock_w14.png"),
                 "Fifteen minutes of setup, two hours of practical, twenty-five minutes of written reasoning, "
                 "twenty minutes to collect and check. The clock is on the wall and the time calls are read "
                 "out.",
                 kicker="THE THREE HOURS")
    notes(s, "Setup takes the full fifteen minutes and it is not part of your working time. Machine "
             "allocation, variant distribution and the rules being read out all happen before the clock "
             "starts on Part A.\n\nTime calls are read out at 60, 30 and 10 minutes remaining in Part A. "
             "There is no break between Part A and Part B, so eat before you come.\n\nTO TEACH: confirm the "
             "sitting plan and the second invigilator for any sitting above 40 students. A cohort of about "
             "100 will need two sittings, which must already be timetabled.")

    s = s_prose(prs, "The rules", [
        "**Bring**",
        "Your student card, a pen, and the one-page cheat sheets from Weeks 8 to 13 if you printed them. "
        "Paper notes are permitted.",
        "**The machine is offline and stays offline**",
        "The network is physically disconnected. Attempting to reconnect it is treated as academic "
        "misconduct.",
        "**Permitted on the machine**",
        "Python, Jupyter or VS Code, pandas, NumPy, matplotlib, seaborn, scikit-learn, and the offline "
        "documentation bundle.",
        "**Prohibited**",
        "Internet, AI assistants, phones, messaging, and any file brought in on a drive. Phones go in your "
        "bag at the front of the room.",
        "**Your work is individual**",
        "This is not a team assessment. Two scripts that share a distinctive error are both investigated.",
        "**Submission**",
        "Save into the drop folder named for your seat, with your student number in the filename. Part B is "
        "handed in on paper."],
        kicker="READ THIS BEFORE THE DAY")
    notes(s, "Paper notes are permitted deliberately. The cheat-sheet slides from Weeks 8 to 13 were written "
             "to be printed and used, and bringing them is the intended behaviour rather than a "
             "loophole.\n\nOn submission: save early and save often into the drop folder. A file saved at "
             "minute 40 and again at minute 90 protects you against losing the last stretch of work.\n\nTO "
             "TEACH: read this slide aloud from the screen at the start. Then confirm every machine's offline "
             "state before you distribute the task sheets.")

    s = s_prose(prs, "Part A — the six things you are asked to do", [
        "**1 · State the task and name the target**",
        "Regression or classification, the target column and its unit, and one sentence on what decision the "
        "prediction would support.",
        "**2 · Prepare the data, with a justified decision for every defect**",
        "Profile it first. One sentence per cleaning decision. Report how many rows you dropped and what "
        "proportion that was.",
        "**3 · Build at least two models inside a leak-proof pipeline**",
        "Preprocessing inside the Pipeline. State the four things you held constant and the seed you used.",
        "**4 · Evaluate with a justified metric, and validate properly**",
        "Name the metric before you look at any result, and say what consequence chose it. Report the mean "
        "and the spread across folds.",
        "**5 · Report the result in physical or operational units**",
        "A number with a unit and a sentence an engineer could act on. " + c["num_unit"] + " for a " +
        c["num_tgt"] + ", or a rate with the cost of each kind of mistake beside it.",
        "**6 · State three limitations**",
        "What the data cannot support, what conditions the model holds under, and what you would need in "
        "order to do better."],
        kicker="THE PRACTICAL — 2 HOURS")
    notes(s, "Notice that only two of the six tasks are modelling. Tasks 1, 2, 5 and 6 are framing, "
             "preparation, interpretation and limits, and together they carry more marks than the modelling "
             "does.\n\nTask 3 says at least two models. Two models compared honestly under one protocol score "
             "far better than five models compared carelessly, and a third model is worth adding only when "
             "the first two are properly done.\n\nTask 6 is the one candidates run out of time for, which is "
             "why the suggested plan later in this deck puts it before the last of the modelling.")

    s = s_prose(prs, "Part B — the four written questions", [
        "**No computer, twenty-five minutes, on paper**",
        "You answer about the work you have just done. The questions are the same for every variant.",
        "**1 · Why this metric?**",
        "Name the metric you used and the engineering consequence that chose it. Say what a different metric "
        "would have optimised instead.",
        "**2 · Where could this pipeline leak?**",
        "Name the most likely leak in your own workflow, say which of the four kinds it is, and say how you "
        "ruled it out.",
        "**3 · What would change your recommendation?**",
        "A change in the data, the plant or the conditions of use. Be specific about the change and about "
        "what you would do.",
        "**4 · Would you deploy this, and what would you require first?**",
        "A clear position, with the conditions attached. 'No, and here is what I would need' is a full-mark "
        "answer when the reasons are right.",
        "**How long each answer should be**",
        "Five or six sentences. Twenty-five minutes across four questions is about six minutes each, so write "
        "in short declarative sentences."],
        kicker="THE WRITTEN REASONING — 25 MINUTES")
    notes(s, "Part B is answered about your own work, so it cannot be prepared in advance in any detail. What "
             "you can do is practise the four questions on your project model this week, because the shape of "
             "the answer is the same.\n\nQuestion 4 has no expected answer. A well-reasoned refusal to deploy "
             "scores as highly as a well-reasoned deployment, and a position with no conditions attached "
             "scores poorly either way.\n\nWrite Part B even if Part A went badly. The marks are separate, "
             "and a candidate who can explain what went wrong recovers a large part of them.")

    s = s_prose(prs, "The rubric, out of 100", [
        "**Task framing — 10**",
        "The task named correctly, the target named with its unit, and the decision the prediction would "
        "support.",
        "**Data preparation and leakage control — 20**",
        "Profiling done, each decision justified, preprocessing inside the Pipeline, and the timing question "
        "asked of every column.",
        "**Modelling protocol — 20**",
        "At least two models, one protocol, the constants and the seed stated, and the test set spent once.",
        "**Evaluation and metric justification — 20**",
        "The metric chosen before the results and justified by a consequence, with the mean and the spread "
        "reported.",
        "**Engineering interpretation and limits — 20**",
        "The result stated in physical or operational units, and three limitations that follow from your own "
        "data.",
        "**Code clarity — 10**",
        "It runs top to bottom from a clean kernel. Relative paths, a named seed, and cells in a readable "
        "order."],
        kicker="PUBLISHED IN WEEK 11")
    notes(s, "Add up evaluation and interpretation: they carry 40 "
             "marks between them, and the accuracy your model achieves carries none of them on its own. A "
             "candidate whose model scores modestly and who explains honestly what it can and cannot do will "
             "beat a candidate with a better score and no interpretation.\n\nCode clarity is 10 marks that "
             "cost you nothing if you did Week 13 properly: relative paths, a named seed, and Restart and Run "
             "All before you submit.")

    s = s_prose(prs, "Where the marks come from", [
        "**45 of the 100 marks are read from a structured answers cell**",
        "One cell at the bottom of your notebook, filled in as you go. It is read by a script, so the keys "
        "have to be exactly as given.",
        "**Which marks those are**",
        "Task framing, the metric you named, your reported scores and spreads, the seed, the row counts you "
        "dropped, and your three limitations as short strings.",
        "**Why it works this way**",
        "So that your framing, your metric choice and your limits are collected from a form rather than "
        "hunted for in forty cells. It also means they are marked the same way for everybody.",
        "**The other 55 marks are marked by me**",
        "Your justifications, your pipeline, your charts, your interpretation, and Part B. Those need reading "
        "and they get read.",
        "**Fill the cell in as you go, never at the end**",
        "A candidate who leaves it until the last ten minutes loses marks they had already earned. Put the "
        "cell in place at minute five and add to it.",
        "**A structural check runs first**",
        "It confirms the notebook runs top to bottom, that the required sections are present and that nothing "
        "tried to reach the network. Failing it costs code clarity marks."],
        kicker="HOW IT IS MARKED")
    notes(s, "The single most valuable habit for this test is filling in the answers cell as you go. Those 45 "
             "marks are the easiest in the paper and they are the ones most often lost, because candidates "
             "leave the cell blank while they chase a better score and then run out of time.\n\nThe keys have "
             "to be exactly as given, because a script reads them. A misspelled key returns nothing for that "
             "line.\n\nTO TEACH: put the answers cell in the task sheet as copyable text, and say at the "
             "30-minute call that the cell should already have entries in it.")

    s = s_split(prs, "The structured answers cell", "How it works",
                "It is a Python dictionary in the last cell of your notebook. You fill it in as you go.\n\n"
                "Keep the keys exactly as printed on your task sheet. A script reads them, so a misspelled "
                "key scores nothing for that line.\n\n"
                "Values are numbers or short strings. No prose, no explanation — your explanations belong in "
                "the markdown cells and in Part B.\n\n"
                "Put the cell in place in the first five minutes, then add to it as each part is done.",
                "The keys",
                # Sixteen one-key rows needed 12.5pt to fit the panel, which is
                # the smallest text in the deck for the least subtle content on
                # the slide. Grouped four to a row it sets at a readable size and
                # still names all fourteen keys. The exact dict, with its ... and
                # its commas, is printed on the task sheet.
                ['ANSWERS = {',
                 '  task, target, target_unit',
                 '  metric, metric_reason, seed',
                 '  rows_in, rows_used, rows_dropped',
                 '  models, cv_mean, cv_spread',
                 '  holdout, limitations',
                 '}',
                 'Fourteen keys. Strings and numbers only.'],
                kicker="45 OF THE 100 MARKS")
    notes(s, "The exact keys are printed on your task sheet on the day, and they will match this list. "
             "Practise filling one in on your project notebook this week, because the habit of writing to it "
             "while you work is what protects those marks.\n\nOn 'metric_reason': a short string is enough. "
             "'false negative costs a gearbox' scores; 'best metric' does not.\n\nOn 'limitations': three "
             "short strings, each naming something specific about your own data. Generic statements about "
             "machine learning score nothing.\n\nTO TEACH: publish the exact key list with the specification "
             "so nobody meets it for the first time in the room.")

    s = s_prose(prs, "How to spend the two hours", [
        "**0:00 to 0:15 · read, profile, and write the framing**",
        "Read the brief twice. shape, head, info, describe, duplicated. Fill in task, target, target_unit and "
        "rows_in.",
        "**0:15 to 0:40 · clean, with a sentence per decision**",
        "One markdown line per defect: what, where, cause, action, why. Fill in rows_used and rows_dropped.",
        "**0:40 to 0:50 · fix the protocol and name the metric**",
        "Split with a named seed, write the four constants down, and write metric and metric_reason before "
        "you fit anything.",
        "**0:50 to 1:25 · build two models inside a Pipeline**",
        "The simple one first, and get it fully working before you add the second. Fill in models, cv_mean "
        "and cv_spread.",
        "**1:25 to 1:45 · write the limitations and the interpretation**",
        "Do this before any further modelling. It carries 20 marks and it is what candidates run out of time "
        "for.",
        "**1:45 to 2:00 · charts, captions, Restart and Run All, submit**",
        "Two or three charts, each captioned with its finding. Then restart, run all, check the answers cell, "
        "and save."],
        kicker="A SUGGESTED PLAN")
    notes(s, "This plan is a suggestion and it is the one that has worked. The important feature is that the "
             "limitations are written at 1:25 rather than at 1:55, because they carry 20 marks and a third "
             "model carries almost none.\n\nThe other important feature is that the metric is named at 0:40, "
             "before any model is fitted. Choosing the metric after seeing the scores means choosing the one "
             "that flatters the model you already liked, and the rubric asks for the consequence that chose "
             "it.\n\nLeave the last fifteen minutes alone. Restart and Run All will find something, and you "
             "want time to fix it.")

    s = s_prose(prs, "If something goes wrong", [
        "**The machine crashes or the kernel dies**",
        "Put your hand up immediately. Time lost to a machine fault is added back, and the invigilator "
        "records it. Save into the drop folder every twenty minutes so the loss is small.",
        "**A cell has been running for five minutes**",
        "Interrupt it. Something is fitting a grid far larger than you meant, or reading the file in a loop. "
        "Cut the grid or the fold count and move on.",
        "**You cannot get the second model to work**",
        "Submit one model that works, properly evaluated, and say in your notebook what the second was and "
        "why it failed. Partial marks for the protocol are available; a broken second model earns none.",
        "**You realise at 1:30 that your target was wrong**",
        "Say so in a markdown cell, state what the correct target is, and carry on with what you have. "
        "Diagnosing your own error in writing recovers a real part of the framing marks.",
        "**You run out of time on Part A**",
        "Stop, save, and go to Part B. Part B is marked separately and it is the cheapest 25 minutes in the "
        "paper.",
        "**You are ill on the day**",
        "Tell the Faculty office before the sitting. There is a documented deferral route and it has to be "
        "opened in advance, so a message afterwards is much harder to act on."],
        kicker="CONTINGENCY")
    notes(s, "The third and fourth items are the ones worth remembering, because they turn a bad run into a "
             "mediocre one instead of a failure. A written diagnosis of your own mistake is worth real marks; "
             "silence about it is worth none.\n\nThe fifth is the most common error in test technique. "
             "Candidates spend the Part B time trying to rescue Part A and lose the easier marks.\n\nTO "
             "TEACH: read the machine-fault item aloud and mean it. Candidates who lose ten minutes and say "
             "nothing until the end cannot be compensated fairly.")

    s = s_question(prs, "REVISION — WEEKS 8 TO 13",
                   '"Everything from here on is revision. Six weeks in two slides, then a self-test with '
                   'worked answers."',
                   "Nothing in this test is new. If you can answer the self-test at the end of this deck "
                   "without looking, you are prepared.")
    notes(s, "The rest of this deck is written to be studied from. Two summary slides covering Weeks 8 to 13, "
             "a five-question self-test with worked answers, a glossary of the terms the test uses, and a "
             "one-page reference.\n\nThe most effective preparation is redoing a past practical on a "
             "different dataset under the clock. Rereading these slides is the least effective.\n\nTO TEACH: "
             "tell them the deck continues past the briefing. Students do not read past the last slide you "
             "present unless told to.")

    s = s_summary(prs, [
        "A model is fitted by minimising an error on training data, and the only honest test of it is data it "
        "has never seen.",
        "Report regression error in the units of the target. MAE is the average size of the error; RMSE "
        "punishes large errors more heavily.",
        "Residuals tell you where the model is worst. A pattern in the residuals means something systematic "
        "is missing.",
        "A confusion matrix has four cells and each one has a cost in your discipline. Name the cost before "
        "you choose the metric.",
        "Accuracy is misleading under class imbalance. With 3 per cent positives, predicting nothing scores "
        "97 per cent and is worthless.",
        "Precision and recall trade against each other through the decision threshold, and the threshold is "
        "an engineering choice.",
        "Overfitting shows as a gap between training and test performance. Cross-validation tells you whether "
        "the gap is real.",
        "There are four kinds of leakage: train-test contamination, target leakage, temporal leakage and "
        "group leakage. A Pipeline is the structural fix for the first.",
        "Ask the timing question of every column: would I really have this before the outcome is known?"],
        kicker="REVISION 1 OF 2", title="Weeks 8, 9 and 10 — models, metrics and trust")
    notes(s, "Nine statements covering the machine learning core. The fifth and the eighth are the two most "
             "likely to appear in Part B, because both of them ask you to notice something that a score alone "
             "will not tell you.")

    s = s_summary(prs, [
        "A model knows only the columns you gave it. Encoding a category as 1, 2, 3 tells the model those "
        "levels are evenly spaced.",
        "Distance-based and penalised methods need their features scaled. Trees, forests and boosting do not.",
        "A feature built from a physical relationship needs no new measurement, and it is where your degree "
        "beats a better programmer.",
        "Ablation is the honest measure of a feature: drop it, refit on the same split, and report the change "
        "with its spread.",
        "A comparison is fair when the split, the folds, the preprocessing and the metric are held constant "
        "and only the model changes.",
        "A difference smaller than the fold-to-fold spread is not a difference. Report the mean and the "
        "spread every time.",
        "The hyperparameter search runs inside cross-validation, and the test set takes no part in choosing "
        "anything.",
        "Five criteria decide the choice besides accuracy: explainability, cost, data hunger, failure "
        "behaviour and maintenance.",
        "Relative paths, pinned versions, a named seed and Restart and Run All. Those four make your work "
        "checkable."],
        kicker="REVISION 2 OF 2", title="Weeks 11, 12 and 13 — features, comparison, reproducibility")
    notes(s, "Nine statements covering Block 4 and the studio week. The fifth and the sixth are worth writing "
             "out at the top of your notebook on the day, because between them they secure a large part of "
             "the modelling protocol marks before you fit anything.")

    s = s_check(prs, [
        "You have 10,000 rows and 340 of them are the positive class. Your model reports 96.6 per cent "
        "accuracy. What has it probably done, and what would you report instead?",
        "You standardised the whole table, then split it, then cross-validated. Name the defect and say "
        "roughly how much it inflates the score.",
        "Your two models score 0.81 and 0.79, with folds spread over 0.05. What do you write in the "
        "recommendation?",
        "Give one limitation of a model trained on " + c["dataset"] + " that follows from the data rather "
        "than from machine learning in general.",
        "You are asked whether you would deploy your model. What does a full-mark answer contain?"],
        title="Self-test — write something for each before you look",
        foot="Answers on the next slide. Do this without notes, then check.")
    notes(s, "Question D is the one candidates answer generically and lose marks on. A limitation has to come "
             "from your own data: the range it covers, the period it was collected in, the conditions it was "
             "measured under. 'Machine learning cannot extrapolate' is a statement about the field rather "
             "than about your dataset.")

    s = s_answers(prs, [
        ("96.6 per cent on a 3.4 per cent positive class?",
         "It has probably predicted the negative class every time, which scores 96.6 per cent and catches "
         "nothing. Report recall on the positive class, precision, and the confusion matrix with the cost of "
         "each cell in your own units."),
        ("Scaled before the split?",
         "Train-test contamination. The scaler's mean and standard deviation were computed using rows the "
         "model was going to be judged on. It typically inflates the score by one or two per cent, which is "
         "small enough to survive review, and the fix is to put the scaler inside the Pipeline."),
        ("0.81 and 0.79, spread 0.05?",
         "That the two cannot be separated on this data. Write both means with their spreads, say the "
         "difference is smaller than the fold-to-fold variation, and then choose on explainability, cost, "
         "data hunger, failure behaviour or maintenance — and name which one decided it."),
        ("A limitation from the data?",
         "Something specific: the range of conditions the file actually covers, the period it was collected "
         "over, the single plant or laboratory it came from, or a column that is missing for a structured "
         "reason. " + c["lim_future"]),
        ("Would you deploy it?",
         "A clear position, the conditions attached to it, and what you would require first. For example: "
         "'Not as an automatic decision. I would run it in advisory mode for three months, compare its calls "
         "against the existing procedure, and require a monthly check that the input range still matches the "
         "training data.' A position with no conditions scores poorly either way.")])
    notes(s, "Answer E is the shape of a full-mark Part B answer, and the shape matters more than the "
             "position. A confident 'yes' with no conditions and a confident 'no' with no reasons both score "
             "poorly; either position with the conditions attached scores well.")

    s = s_glossary(prs, [
        ("Target", "The column you are predicting. Name it with its unit."),
        ("Feature", "A column known before the outcome. Ask the timing question of every one."),
        ("Pipeline", "Preprocessing chained to the model, fitted on the training fold only."),
        ("Train/test split", "Rows held back so the model can be judged on data it has not seen."),
        ("Cross-validation", "Every row gets a turn in the test fold. Report the mean and the spread."),
        ("Overfitting", "Good on training data, poor on unseen data. Seen as a gap."),
        ("MAE", "Mean absolute error. The average size of the error, in the target's units."),
        ("RMSE", "Root mean squared error. Larger errors count for more."),
        ("R²", "The share of the variation the model accounts for. Unitless."),
        ("Confusion matrix", "TP, FP, FN, TN. Give each cell a cost in your own discipline."),
        ("Precision", "Of the cases you flagged, how many were real."),
        ("Recall", "Of the real cases, how many you caught."),
        ("Class imbalance", "One class is rare, so accuracy stops carrying information."),
        ("Decision threshold", "The probability above which you act. An engineering choice."),
        ("Data leakage", "Information the model would not have in service. Four kinds."),
        ("Timing question", "Would I really have this column before the outcome is known?"),
        ("Ablation", "Drop a feature, refit on the same split, record the change with its spread."),
        ("Comparison protocol", "Split, folds, preprocessing and metric held constant across candidates."),
        ("Hyperparameter", "A number you choose before fitting. Searched inside cross-validation."),
        ("Conditions of use", "The input range and plant conditions under which your model holds."),
    ], page="1 of 1")
    notes(s, "Twenty terms and all of them appear in the rubric or in Part B. If any of them is unfamiliar, "
             "go back to the week it came from rather than rereading this list.")

    s = s_prose(prs, "One-page reference — take this into the room", [
        "**Profile first, one minute**",
        "shape · head · info · describe (read min and max first) · duplicated().sum() · isna().sum()",
        "**Write the framing before you model**",
        "Task · target and its unit · the decision it supports · rows_in. Straight into the answers cell.",
        "**Clean, one sentence per decision**",
        "What · where · likely cause · action · why. Then rows_used and rows_dropped, as a count and a "
        "proportion.",
        "**Fix the protocol, in writing**",
        "One seed · one split · same folds for every candidate · preprocessing inside the Pipeline · metric "
        "chosen now.",
        "**Two models, properly**",
        "The simple one first and fully working. Report cross-validated mean and spread, then the held-out "
        "score once.",
        "**Interpret in units, at 1:25**",
        "A number with a unit and a sentence an engineer could act on. Then three limitations from your own "
        "data.",
        "**Captions state findings**",
        "Not the axes. A number in every caption.",
        "**Last fifteen minutes**",
        "Restart and Run All · check the answers cell · save into the drop folder · then Part B."],
        kicker="CHEAT SHEET — PRINT THIS")
    notes(s, "Print this slide and bring it. Paper notes are permitted, and the two lines that will earn you "
             "the most are the protocol line and the 1:25 line.")

    s = s_closing(prs, "You know the format, the rules and the rubric\na week before you sit down.",
                  "There is nothing to memorise. You will be given a dataset from your own discipline that "
                  "you have never seen, and asked what you make of it. Forty of the hundred marks are for "
                  "evaluating and interpreting honestly, and none of them are for the score your model "
                  "reaches.",
                  "Then Week 15: Demo Day, the individual viva, and your reflection.")
    notes(s, "The best preparation available to you is to redo a past practical on a different dataset, under "
             "the clock, with the answers cell open beside you. Two hours of that is worth more than a week "
             "of rereading.\n\nAfter the test, Week 15 is Demo Day. Your repository, two-page brief, poster, "
             "AI-use declaration, contribution log and 500-word reflection are all due at the start of that "
             "session, and there is no teaching session in between, so draft the brief and the poster this "
             "week.\n\nTO TEACH: on the day, confirm the Week 15 demo running order before dismissal.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week14_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


# =====================================================================
def week15(code):
    """Demo Day. Not a teaching session: a fair, a viva and a reflection."""
    c = CO[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 15")
    teams = TEAMS[code]
    big = (code == BIG)

    s = s_title(prs, code, "Demo Day",
                "The demo fair, the individual viva, and what you can say now that you could not in September",
                "WEEK 15  ·  " + DATE[15][code], SLOTS[code] + "  ·  " + FOOT)
    notes(s, "The last session. Your deliverables are due at the start of it, the demo fair runs for one "
             "hundred minutes, every student answers two unseen questions about their own repository, and the "
             "session closes with the three recognitions and your reflection.\n\nInvited Faculty staff and, "
             "where possible, a practising engineer from outside will be circulating as assessors.\n\nTO "
             "TEACH: invite Faculty staff and one external practising engineer — it raises the standard of "
             "every submission more than any amount of exhortation. Book a fair layout with tables round the "
             "perimeter and power at every station. Print the assessor packs, the peer assessment forms, the "
             "viva tally sheets and the three certificates.")

    s = s_points(prs, "How today runs",
                 [("First ten minutes — running order and rules",
                   "Station allocation, the two rounds of the fair, and how the marking works. Then the fair "
                   "starts and does not stop for a hundred and thirty minutes."),
                  ("The demo fair — two rounds, a hundred and thirty minutes",
                   "You present at your station with a laptop and your one-page poster. Assessors circulate. "
                   "Every team presents to at least four peer assessors across the two rounds." +
                   (" With about " + str(teams) + " teams, this cohort runs as a fair plus a plenary "
                    "shortlist of six rather than " + str(teams) + " presentations in a row." if big else
                    " With about " + str(teams) + " teams, every team also gets a plenary slot.")),
                  ("Then the viva, the shortlist and the reflection",
                   "Thirty minutes of individual viva sampling runs alongside the fair. Twenty minutes of "
                   "shortlisted demos and the recognitions. Twenty minutes of feedback, the Semester 2 "
                   "preview, and your reflection handed in.")],
                 kicker="THE RUNNING ORDER", numbered=False)
    notes(s, "The fair format exists because " + str(teams) + " consecutive presentations would take longer "
             "than the session and hold everybody's attention for none of it. At a station you present four "
             "or five times to small groups, which is better practice and a great deal less "
             "frightening.\n\nThe viva runs alongside the fair rather than after it, so you may be asked your "
             "two questions at any point during the hundred minutes.\n\nTO TEACH: allocate stations before "
             "the room fills. Post the running order on the wall.")

    s = s_figure(prs, "How today runs", F("clock_w15.png"),
                 "Four blocks and no break. The fair runs for a hundred and thirty minutes and the viva "
                 "sampling happens inside it, so keep your station staffed while your teammates circulate.",
                 kicker="THE THREE HOURS")
    notes(s, "There is no break in this session, so bring water. Your team needs at least one person at the "
             "station at all times, which means rotating through the two rounds so everybody gets to see "
             "other teams' work.\n\nDeciding that rotation before you arrive saves you ten "
             "minutes.\n\nTO TEACH: give time calls at the halfway point of each round so teams rotate. "
             "Without a call, one student presents for the whole hundred minutes.")

    s = s_prose(prs, "Due at the start of this session", [
        "**1 · The repository URL**",
        "It must pass Restart and Run All from a clean clone. This is the submission surface, so a "
        "repository nobody can run cannot be marked for what it does.",
        "**2 · A two-page engineering brief**",
        "What problem, what data, what you did, what you found, what you recommend, and what the limitations "
        "are. Written for an engineer rather than for a marker.",
        "**3 · A one-page poster**",
        "For the station. Three or four charts, each captioned with its finding, and the recommendation in "
        "one sentence at the top.",
        "**4 · An AI-use declaration**",
        "What you asked, what came back, and what you did to check it. In the README as well as in the "
        "submission.",
        "**5 · Your individual contribution log**",
        "Per member, checkable against the commit history. This is how a team mark becomes an individual one.",
        "**6 · A 500-word individual reflection**",
        "Handed in at the end of the session. The prompt is later in this deck."],
        kicker="SIX DELIVERABLES")
    notes(s, "Item 1 is the gate. A repository that fails on a clean clone cannot be marked for its "
             "methodology, its validation or its reasoning, which is 55 of the 100 project marks. Test it on "
             "a machine that is not yours before you come.\n\nItem 2 is a different document from your "
             "README. The README tells a reviewer how to run your work; the brief tells an engineer what you "
             "found and what to do about it. Two pages means two pages.\n\nItem 5 is what protects you. If "
             "your teammates did less than you, the log and the commit history are the evidence.\n\nTO TEACH: "
             "collect items 1 to 5 at the door. Item 6 comes in at the end.")

    s = s_prose(prs, "The demo fair, two rounds", [
        "**Your station**",
        "A table, power, a laptop showing your repository, and your poster. Assessors and peer assessors "
        "arrive in small groups.",
        "**Six minutes, four or five times**",
        "You will give roughly the same six minutes to each group that arrives. It gets better each time, "
        "which is part of why the format is a fair.",
        "**Rotate your team between the two rounds**",
        "One person on the station at all times. Everybody else circulates and peer-assesses. Decide the "
        "rotation before you arrive.",
        "**Your audience is mixed**",
        "Faculty staff from other disciplines, an external engineer, and students from the other programmes "
        "in your cohort. Nobody knows your dataset.",
        "**Which means you have thirty seconds to land the problem**",
        "Say what problem you took on and who has it, before any method. If the problem does not land, "
        "nothing after it will.",
        "**Have the notebook open, at the result**",
        "Every serious question gets answered by pointing at a number. Hunting through cells while somebody "
        "waits costs you the room."],
        kicker="THE FAIR — 130 MINUTES")
    notes(s, "The mixed audience is the point of the exercise. Explaining " + c["num_tgt"] + " to a Faculty "
             "member from a different discipline is harder and more useful than explaining it to somebody who "
             "already knows your dataset, and it is the skill you will need in every review meeting of your "
             "career.\n\nThe last point is practical. Open the notebook at your result before the first "
             "group arrives, and keep a second tab on your ablation table or your comparison table.")

    s = s_worked(prs, "Your six minutes at the station",
                 "The order that works with a mixed audience. Rehearse it once with a stopwatch before you "
                 "arrive.",
                 ["Thirty seconds: the problem and who has it. 'A precast yard rejects one panel in twelve "
                  "at the 7-day test, and by then the panel is cast.' No method yet.",
                  "Thirty seconds: the data. Where it came from, how many rows, and one honest sentence "
                  "about what is wrong with it.",
                  "Ninety seconds: what you did, at the level of decisions rather than code. The features "
                  "you built and why, the models you compared, and the protocol you held constant.",
                  "Ninety seconds: the result, in units, with its spread. Point at the number on the screen "
                  "as you say it.",
                  "Sixty seconds: the limitations and the conditions of use. What your model cannot do, and "
                  "what change would require a refit.",
                  "Sixty seconds: the recommendation, in one sentence, and then stop talking and take "
                  "questions."],
                 "Steps 1 and 5 are the two that distinguish the demos people remember. Rehearse those two "
                 "sentences until they are exact.")
    notes(s, "Step 5 is counter-intuitive and it works. A team that states clearly what its model cannot do "
             "reads as competent, and it is the single most reliable way to raise an assessor's opinion of "
             "your work. It is also one of the three recognition categories.\n\nStep 3 is where teams "
             "overrun. Nobody at a fair wants to see your code; they want to know which decisions you took "
             "and why. Say 'we built five features from the mix chemistry and measured each one by ablation' "
             "rather than opening the cell.\n\nTO TEACH: run one team through this at the start as a "
             "demonstration if the room is nervous.")

    s = s_prose(prs, "What the assessors are looking for", [
        "**Problem definition — 15 marks**",
        "A real engineering problem, named clearly, with the decision it supports.",
        "**Data understanding — 15**",
        "You know what is wrong with your data and you say so before being asked.",
        "**Methodology — 20**",
        "A protocol somebody could repeat, and choices that follow from the problem.",
        "**Engineering reasoning — 20**",
        "Features built from physics, trades named and quantified, and limits that come from your own data.",
        "**Validation — 15**",
        "Honest evaluation, a metric justified by a consequence, and no leakage.",
        "**Communication — 10 · Reproducibility — 5**",
        "The brief, the poster and the captions. And a repository a stranger can clone and run."],
        kicker="THE PROJECT RUBRIC, OUT OF 100")
    notes(s, "Engineering reasoning and data understanding carry 35 marks between them and neither is about "
             "your model. They are about whether you understood the problem and the data you had.\n\nNotice "
             "what is absent from the rubric: there is no criterion for the accuracy your model achieved. A "
             "team whose model performs modestly and who can say precisely why, and what would be needed to "
             "do better, scores above a team with a better number and no account of it.\n\nTO TEACH: the "
             "assessor packs carry this rubric. Brief invited staff to ask about reasoning and limits rather "
             "than about scores.")

    s = s_prose(prs, "Peer assessment — how to mark another team", [
        "**You assess at least four teams**",
        "One form each, filled in at their station. Your marks are advisory and I moderate them, so they are "
        "never used raw.",
        "**Mark against the rubric on the form**",
        "The same seven criteria the assessors use. A team that made a different defensible choice from yours "
        "has not made an error.",
        "**Justify every mark you award**",
        "One line per criterion, naming what you saw. A mark with no justification is discarded.",
        "**Ask one question before you mark**",
        "'What would change your recommendation?' is the most useful single question, and the answer tells "
        "you most of what you need for the reasoning criterion.",
        "**Marking generously helps nobody**",
        "A form where every team scores 95 carries no information and is dropped. Use the range.",
        "**And expect to learn from it**",
        "Most students find a defect in their own project while assessing somebody else's. That is the "
        "intended outcome, the same as in Week 13."],
        kicker="PEER ASSESSMENT")
    notes(s, "Peer assessment is advisory and moderated, which means your marks inform the decision and do "
             "not set it. What is marked is the quality of your justifications, so one specific line per "
             "criterion is worth more than a number.\n\nThe suggested question is worth using every time. A "
             "team that cannot say what would change its recommendation has usually not thought about the "
             "conditions of use, and that is visible in one answer.\n\nTO TEACH: collect the forms. Moderate "
             "before combining, and never use peer marks raw.")

    s = s_prose(prs, "The individual viva", [
        "**Two questions, ninety seconds each, about your own repository**",
        "Asked at your station at some point during the fair. You will not know in advance which two you "
        "get.",
        "**Every student is asked, and it is recorded on a tally sheet**",
        "This is the mechanism that turns a team mark into an individual one. Sixty-five per cent of your "
        "semester mark is individual, and this is part of it.",
        "**The questions are about your repository rather than about the topic**",
        "Nobody will ask you to define cross-validation. You will be asked what your own notebook does at a "
        "particular point, and why.",
        "**No tools, no notes, no help from your team**",
        "You may open your own repository and point at it. That is encouraged.",
        "**Which is why the AI-use declaration matters**",
        "Anything in your repository that nobody on the team can explain is exactly where these questions "
        "land.",
        "**And why the contribution log matters**",
        "You are asked about the part you did. A log that matches the commit history means the questions you "
        "get are the ones you can answer."],
        kicker="THE MECHANISM THAT MAKES IT INDIVIDUAL")
    notes(s, "Read your own repository the night before. Not to memorise it — to be able to find things in it "
             "and say why each decision was taken. The two questions you get will be about the work you "
             "logged as yours.\n\nA useful preparation: sit with your teammates and ask each other the ten "
             "questions on the next slide. Twenty minutes of that is the whole preparation.\n\nOne honest "
             "note: 'we tried that and it did not work, so we did this instead' is a good answer. Vagueness "
             "is what costs marks, and a clear account of something that failed is not vague.")

    s = s_check(prs, [
        "Point at the line in your notebook where the train/test split happens. Why is it there and not "
        "earlier?",
        "Which feature in your model did the most work, and how do you know?",
        "Name one feature your team built that turned out not to help. What was the number?",
        "What metric did you report, and what consequence chose it?",
        "How much does your headline number move between cross-validation folds?",
        "Where could your pipeline leak, and how did you rule it out?",
        "What does your model return for an input outside the range it was trained on?",
        "Which part of this repository did you write, and which part did you review?",
        "Name one thing your team disagreed about and how you settled it.",
        "What would you do differently if you started this project again on Monday?"],
        kicker="THE VIVA BANK", title="Ten of the twenty questions you could be asked",
        foot="You get two of these, or two like them, at your station. Practise them on each other.")
    notes(s, "These ten are published so that you can practise, and the bank has twenty in it. Every one of "
             "them is answerable from your own repository with the notebook open, and none of them requires "
             "you to remember a definition.\n\nQuestions C, I and J are the ones students expect least and "
             "find easiest once they think about it. A feature that did nothing, a disagreement you settled, "
             "and something you would change are all evidence that real work happened.\n\nTO TEACH: the "
             "shape of a full-mark answer to each:\n\nA · After any exploration and before any fitting or "
             "scaling; earlier and the preprocessing sees the test rows.\nB · Names a feature and cites the "
             "ablation table, with the change and the spread.\nC · Names a feature, gives the measured "
             "change, and says it was smaller than the fold spread.\nD · Names the metric AND a cost or "
             "consequence in the discipline's own units.\nE · Quotes the standard deviation across folds, or "
             "admits it was not measured.\nF · Names one of the four kinds and the specific check made — "
             "usually the Pipeline, or the timing question on a column.\nG · Linear models extrapolate a "
             "straight line; trees return the nearest leaf and give no warning. Credit any answer that "
             "notices there is no warning.\nH · Must match the contribution log and the commit history.\n"
             "I · Any specific disagreement with a resolution. Vagueness scores poorly.\nJ · A specific "
             "change with a reason. 'Work harder' scores nothing.\n\nTally two per student. Do not let "
             "teammates answer for each other.")

    s = s_prose(prs, "When you do not know the answer", [
        "**Say so, and say what you would need**",
        "'I did not measure that. I would run it across three seeds and report the spread.' That is a good "
        "answer and it scores.",
        "**Point at the notebook**",
        "You are allowed to open your own repository. Finding the cell and reading it is better than "
        "guessing from memory.",
        "**Do not invent a reason**",
        "An invented justification is the one thing that scores worse than 'I do not know', because the next "
        "question exposes it.",
        "**Distinguish what you did from what your team did**",
        "'I did not write that part — Sarah did, and it does X' is a complete and honest answer to a question "
        "about somebody else's work.",
        "**And a failure honestly described is worth marks**",
        "'We tried a forest, it beat the linear model by less than the fold spread, so we kept the model we "
        "could explain.' That is the course in one sentence.",
        "**Ninety seconds is short**",
        "Answer the question that was asked, in three or four sentences, and stop."],
        kicker="THE VIVA")
    notes(s, "The third point is the one to take seriously. Assessors ask follow-up questions, and an "
             "invented reason collapses immediately, which costs more than the original gap would have.\n\n"
             "The fifth point describes exactly what this course has been training. If you can say that "
             "sentence about your own project and mean it, you have got what the semester was for.")

    s = s_points(prs, "Three recognitions",
                 [("Best Engineering Reasoning",
                   "For the team whose choices most clearly followed from the engineering problem. Features "
                   "built from physics, trades named and quantified, and a recommendation that answers the "
                   "brief that was given."),
                  ("Best Investigation",
                   "For the team that found the most from the data, including teams whose conclusion was that "
                   "the data could not answer the question. A well-evidenced negative result wins this."),
                  ("Most Honest Limitations",
                   "For the team that was clearest about what their work does not support. Specific limits "
                   "drawn from their own data, and conditions of use somebody could check.")],
                 kicker="AWARDED IN THE PLENARY", numbered=False)
    notes(s, "There is no prize for the highest accuracy figure, and that has been true since Week 1. The "
             "three categories are the three things this course has been training, and Most Honest "
             "Limitations exists because being clear about what your work does not support is a professional "
             "skill that almost nothing else rewards.\n\nBest Investigation is open to a team whose answer "
             "was 'this data cannot answer the question, and here is what would'. That has been an acceptable "
             "conclusion since Week 5.\n\nTO TEACH: award all three and say why each one won, naming the "
             "specific thing the team did. Thirty seconds each, and it is the most-remembered part of the "
             "session.")

    s = s_figure(prs, "What you can say now", F("ladder.png"),
                 "This was the promise in Week 1. Most of you could not do step two in September. Look at "
                 "step six and then look at your own repository.",
                 kicker="THE WEEK 1 PROMISE")
    notes(s, "This figure was shown in the first hour of Week 1 as a promise. Step six was 'here is a model I "
             "built and here is how I know it works', and the second half of that sentence is what took "
             "fifteen weeks.\n\nIn September most of this room could not have said what a dataset was in "
             "precise terms. You have now cleaned one, argued about its defects, built features from your own "
             "discipline, compared models under a protocol you fixed, and defended the result to somebody "
             "trying to break it.\n\nTO TEACH: put this up next to the Week 1 slide if you can. The "
             "comparison is what makes fifteen weeks feel like progress.")

    s = s_figure(prs, "Where the marks came from", F("assessment.png"),
                 "No written examination anywhere in this course. Sixty-five per cent of your mark was "
                 "individual, so you could not be carried and you could not be dragged down.",
                 kicker="ASSESSMENT")
    notes(s, "Worth seeing at the end. Every mark in this course came from work with data: eleven weekly "
             "challenges, twelve weekly quizzes, a data analysis project, two offline practical tests, a team "
             "project and today's viva and reflection.\n\nThe individual share was 65 per cent, which is why "
             "the viva and the contribution log exist. A team mark on its own cannot tell anybody what you "
             "personally can do.")

    s = s_map(prs, 15, MAP15)
    notes(s, "Fifteen weeks. Two of them were practical tests where you were handed data you had never seen, "
             "and the project ran from Week 9 to today.\n\nThere was nothing to memorise in any of it, which "
             "surprised most of you in September.\n\nTO TEACH: ninety seconds. Walk it and name one thing "
             "from each block.")

    s = s_figure(prs, "Where you got to on the roadmap", F("roadmap_journey.png"),
                 "The same figure from Week 1. Orange is what this semester covered: stage 1 and stages 3 to "
                 "9. Stage 2 was already behind you in September. "
                 "In September most of the words on it meant nothing to you.",
                 kicker="THE TERRITORY, REVISITED")
    notes(s, "You have covered stage 1 and stages 3 to 9 of the public roadmap.sh Machine Learning "
             "roadmap, and stage 2 was behind you before the semester started. In Week 1 "
             "you were told that most of the individual terms on this figure would mean nothing yet and that "
             "this was expected. Read it again now.\n\nThe interactive version is at "
             "roadmap.sh/machine-learning and it is worth an evening over the holiday.\n\nTO TEACH: ask the "
             "room how many of the stage names they could now explain. The change since Week 1 is large and "
             "they will not have noticed it.")

    s = s_figure(prs, "What Semester 2 covers", F("roadmap_coverage.png"),
                 "Green is Semester 2. Grey is what neither semester teaches, and knowing where the course "
                 "stops is part of what you were given.",
                 kicker="COVERAGE")
    notes(s, "Semester 2 takes the green stages: neural networks and deep learning, gradient boosting "
             "properly, time series, and turning a model into something a colleague can use. The three-minute "
             "Streamlit teaser in Week 13 was pointing at that last one.\n\nThe grey stages sit outside both "
             "semesters. If you want them, roadmap.sh publishes separate roadmaps for the AI engineer, the "
             "data scientist, MLOps and AI agents, and any of the four is a reasonable next step.")

    s = s_prose(prs, "The 500-word reflection", [
        "**Handed in at the end of this session**",
        "Individual, 500 words, and it counts within the demo, viva and reflection component.",
        "**1 · What you could not do in September, and can do now**",
        "Be specific and name the thing. One paragraph.",
        "**2 · The hardest thing, and what got you past it**",
        "A week, a concept or a bug. Say what actually worked, because it is usually not what you expected.",
        "**3 · What you contributed to your team, and what you learned from someone else in it**",
        "Both halves. The second is the one people leave out.",
        "**4 · One thing you got wrong and would do differently**",
        "A specific mistake with a specific correction. This paragraph is read closely.",
        "**5 · Two named goals for Semester 2**",
        "Named, and yours. 'Get better at Python' is not a goal; 'build a time-series model of our own plant "
        "data' is."],
        kicker="THE LAST DELIVERABLE")
    notes(s, "Write it today rather than later. The reflection written in the room after the fair is "
             "consistently more useful than one written at home a week afterwards, because the session is "
             "still in front of you.\n\nParagraph 4 is read closely and it is not a trap. A specific mistake "
             "with a specific correction is evidence that you were paying attention to your own work, which "
             "is most of what reflective practice means.\n\nParagraph 5 is used. The two goals you write "
             "shape the Semester 2 opening weeks, which are designed as review through application rather "
             "than as re-teaching.\n\nTO TEACH: hand out the prompt on paper and collect the reflections "
             "before anybody leaves. Paper gets a full return; a form does not.")

    s = s_prose(prs, "Semester 2, and the holiday", [
        "**Semester 2 opens with review through application**",
        "The first two weeks apply what you already have to new problems. There is no re-teaching of Semester "
        "1, so the goals you write today matter.",
        "**What it adds**",
        "Neural networks and deep learning, gradient boosting given the time it needs, time series, and "
        "putting a model somewhere a colleague can use it.",
        "**The optional holiday challenge**",
        "One dataset, one question, and a repository that passes a clean clone. Nothing is marked and I will "
        "review anything you send me.",
        "**The most useful thing you can do over the break**",
        "Find data from your own discipline, ideally from a placement or a laboratory you have access to, and "
        "ask one question of it end to end.",
        "**Keep your repository**",
        "It is the most useful thing you own for an internship application, and it took you six weeks to "
        "build. Do not delete it in January.",
        "**And the claim you can make now**",
        "'Give me an engineering problem involving data and I know how to start investigating it.' That was "
        "the promise in Week 1."],
        kicker="WHAT COMES NEXT")
    notes(s, "The fifth point is practical advice about employment. A repository with a README, pinned "
             "requirements, a clean history and a two-page brief is a stronger thing to show an employer than "
             "a transcript, and you already have one.\n\nThe holiday challenge is genuinely optional and "
             "genuinely reviewed. Send it and you will get a reply.\n\nTO TEACH: issue the Semester 2 "
             "pre-reading and the holiday challenge sheet with the certificates.")

    s = s_summary(prs, [
        "You can take a dataset nobody has explained to you and say what it is, what is wrong with it, and "
        "what it can support.",
        "You can profile and clean data, justify every decision, and report how much you dropped and why.",
        "You can build features from your own discipline and measure what each one was worth.",
        "You can fit and compare models under a protocol you fixed, and say when two results cannot be "
        "separated.",
        "You can choose a metric from a consequence, and read a confusion matrix in the language of your own "
        "field.",
        "You can find data leakage, name which of the four kinds it is, and fix it structurally.",
        "You can state what your model cannot do and under what conditions it should not be used.",
        "You can hand somebody a repository they can clone and run, and defend the numbers in it.",
        "And you can say 'the data cannot answer this question, and here is what would', which is a real "
        "engineering result."],
        kicker="WHAT THE COHORT ACHIEVED", title="What you can do that you could not in September")
    notes(s, "Nine statements, and every one of them is something this cohort did in an assessed piece of "
             "work rather than something that was described to you. Mark yourself against each one.\n\nThe "
             "last is the one that takes longest to accept and it has been true since Week 5. Saying "
             "precisely what data would be needed to answer a question is frequently the most valuable thing "
             "an analyst produces.\n\nTO TEACH: read the last one aloud and mean it.")

    s = s_closing(prs, "You can take an engineering problem\ninvolving data and start investigating it.",
                  "In September most of this room had never written a line of code. Today you presented a "
                  "model you built, on data you cleaned, with features from your own discipline, evaluated "
                  "under a protocol you fixed, in a repository somebody else can run. You also said what it "
                  "cannot do.",
                  "Semester 2 starts with your own goals, applied to new problems. Keep the repository.")
    notes(s, "That sentence was the promise made in the first hour of Week 1, and it is the claim you can now "
             "make. It is worth noticing what it does not say: it does not claim you can build any model, and "
             "it says you know how to start, which is what an employer is actually asking about.\n\nKeep the "
             "repository, write the two Semester 2 goals down somewhere you will see them, and send me the "
             "holiday challenge if you do it.\n\nTO TEACH: close by naming two or three specific things "
             "individual students did well this semester. Then stay behind — the last ten minutes of the last "
             "session is when students ask the questions that matter to them.")

    prs.save(os.path.join(OUTDIR, f"{code}_Week15_{c['short']}.pptx"))
    return len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for code in CO:
        print(f"  {code}  W11: {week11(code)}   W12: {week12(code)}   "
              f"W13: {week13(code)}   W14: {week14(code)}   W15: {week15(code)}")

    import json
    from pptxkit import LECTURER
    path = _ROOT + "/data/lecturer_notes_" + __file__.split("/")[-1].replace(".py", ".json")
    json.dump(LECTURER, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  {len(LECTURER)} lecturer notes -> {path.split('/')[-1]}")
