# -*- coding: utf-8 -*-
"""
Per-cohort content for Weeks 2-13. One dict per (week, cohort-code).

Voice rules for everything in here:
  - Plain engineering register. No hype, no "leverage", no "delve", no "robust".
  - Every claim concrete and checkable. Units always stated.
  - Notes lead with the explanation a STUDENT can read unaided, then a
    "TO TEACH:" block for the lecturer. Never lecturer-only.
"""

# ---------------------------------------------------------------- Week 3 formulas
W3 = {
 "CML3112": dict(
   why="You already know how to work out a slab's concrete volume. Why write it as code?",
   noun="slab",
   fname="slab_volume",
   code=('def slab_volume(length_m, width_m, thickness_m):\n'
         '    """Volume of a rectangular slab in cubic metres."""\n'
         '    return length_m * width_m * thickness_m\n'
         '\n'
         'length = 6.0          # metres\n'
         'width = 4.0           # metres\n'
         'thickness = 0.25      # metres\n'
         'cement_per_m3 = 320.0 # kg/m3 - teaching figure; use your mix design\n'
         '\n'
         'volume = slab_volume(length, width, thickness)\n'
         'cement = volume * cement_per_m3\n'
         '\n'
         'print(f"{volume:.2f} m3 needs {cement:.0f} kg of cement")'),
   out="6.00 m3 needs 1920 kg of cement",
   mistake="Type thickness = 250 instead of 0.25 — millimetres instead of metres. The volume comes back as "
           "6000 m3 and the cement as 1.9 million kg. Python does not complain. Nothing in the computer "
           "catches this. You catch it, because you know a slab is not six thousand cubic metres.",
   formulas=["Maximum bending moment of a simply supported beam under a uniform load",
             "Concrete volume and reinforcement mass for a slab",
             "Mix quantities for a target volume at a stated water/cement ratio",
             "Wall U-value from the thermal resistance of each layer",
             "Cost per square metre of floor area",
             "Window-to-wall ratio for a facade"],
   decision=('def crack_action(width_mm, exposure):\n'
             '    """Return the action a crack of this width requires."""\n'
             '    if exposure == "marine" and width_mm > 0.20:\n'
             '        return "seal now"\n'
             '    elif width_mm > 0.30:\n'
             '        return "flag for repair"\n'
             '    elif width_mm > 0.10:\n'
             '        return "monitor"\n'
             '    else:\n'
             '        return "no action"'),
   dec_note="The thresholds come from a durability code. No data is needed to write this rule, which puts "
            "it in the left-hand column of the Week 1 diagram.",
   callex="slab_volume(6, 4, 0.25)",
   unit_trap="millimetres and metres"),

 "CML3113": dict(
   why="You already know contained metal is tonnage times grade. Why write it as code?",
   noun="batch",
   fname="contained_metal",
   code=('def contained_metal(tonnes, grade_pct):\n'
         '    """Tonnes of metal contained in an ore tonnage at a given grade."""\n'
         '    return tonnes * grade_pct / 100.0\n'
         '\n'
         'ore_tonnes = 250000.0\n'
         'copper_grade = 1.8      # per cent\n'
         'mill_recovery = 0.88    # fraction actually recovered\n'
         '\n'
         'in_ground = contained_metal(ore_tonnes, copper_grade)\n'
         'saleable = in_ground * mill_recovery\n'
         '\n'
         'print(f"{in_ground:,.0f} t contained, {saleable:,.0f} t saleable")'),
   out="4,500 t contained, 3,960 t saleable",
   mistake="Type copper_grade = 0.018 while leaving the /100 inside the function — the grade gets divided by a "
           "hundred twice. The answer comes back as 45 tonnes instead of 4,500. Silent, plausible if you are "
           "not paying attention, and wrong by two orders of magnitude.",
   formulas=["Ore tonnage from volume and bulk density",
             "Contained metal from tonnage and grade",
             "Mill recovery and dilution",
             "A two-stream mass balance across a plant",
             "Rate of penetration from weight on bit and rotary speed",
             "Volumetric original oil in place"],
   decision=('def grade_action(grade_pct, cutoff_pct):\n'
             '    """Route material to the mill, the stockpile or the waste dump."""\n'
             '    if grade_pct >= cutoff_pct * 1.5:\n'
             '        return "mill now"\n'
             '    elif grade_pct >= cutoff_pct:\n'
             '        return "mill"\n'
             '    elif grade_pct >= cutoff_pct * 0.8:\n'
             '        return "stockpile"\n'
             '    else:\n'
             '        return "waste"'),
   dec_note="The cut-off grade comes from an economic calculation. No data is needed to write this rule, "
            "which puts it in the left-hand column of the Week 1 diagram.",
   callex="contained_metal(250000, 1.8)",
   unit_trap="per cent and grams per tonne"),

 "CML3111": dict(
   why="You already know power is voltage times current. Why write it as code?",
   noun="motor",
   fname="mechanical_power",
   code=('def mechanical_power(torque_nm, rpm):\n'
         '    """Shaft power in watts from torque and rotational speed."""\n'
         '    return torque_nm * rpm * 2 * 3.14159 / 60.0\n'
         '\n'
         'voltage = 240.0     # volts\n'
         'current = 12.5      # amperes\n'
         'torque = 8.5        # newton metres\n'
         'speed = 1450.0      # revolutions per minute\n'
         '\n'
         'p_in = voltage * current\n'
         'p_out = mechanical_power(torque, speed)\n'
         '\n'
         'print(f"in {p_in:.0f} W, out {p_out:.0f} W, "\n'
         '      f"efficiency {100 * p_out / p_in:.1f} %")'),
   out="in 3000 W, out 1291 W, efficiency 43.0 %",
   mistake="Delete the / 60.0 from the function. Efficiency comes back as about 2,600 per cent. You spot "
           "that instantly because you know a motor cannot exceed a hundred per cent. Python knows nothing "
           "at all about motors.",
   formulas=["Ohm's law and electrical power",
             "Three-phase real power with a power factor",
             "Motor torque, and revolutions per minute converted to radians per second",
             "Gear ratio and output speed",
             "Decibel conversion for a power ratio",
             "RC time constant, and root-mean-square of a sampled signal"],
   decision=('def temp_action(winding_c, ambient_c):\n'
             '    """Return the protective action for this winding temperature."""\n'
             '    rise = winding_c - ambient_c\n'
             '    if winding_c > 155:\n'
             '        return "trip"\n'
             '    elif winding_c > 130:\n'
             '        return "alarm"\n'
             '    elif rise > 80:\n'
             '        return "investigate cooling"\n'
             '    else:\n'
             '        return "normal"'),
   dec_note="The 130 and 155 degree limits come from the insulation class on the motor's datasheet. No "
            "data is needed to write this rule, which puts it in the left-hand column of the Week 1 diagram.",
   callex="mechanical_power(8.5, 1450)",
   unit_trap="revolutions per minute and radians per second"),
}

# ---------------------------------------------------------------- Week 4 investigation files
W4 = {
 "CML3112": dict(
   file="site_inspection_log.csv",
   cols="structure_id, span_m, inspection_date, crack_width_mm, defect_rating, inspector_id",
   col="crack_width_mm", limit="0.30", unit="mm",
   rows=300,
   story="One inspector's defect ratings run systematically about one grade harsher than everyone else's, on "
         "the same structures. Nobody will ever tell them that.",
   herrings="Two red herrings: one structure has genuinely severe cracking for a real reason (it is the oldest "
            "span), and crack widths look worse in the wet-season months because they were measured after rain.",
   report="min, max and mean crack width per structure; the count of readings above the 0.30 mm action limit; "
          "and the number of rows that had to be skipped because a field was blank"),
 "CML3113": dict(
   file="drill_shift_log.csv",
   cols="hole_id, depth_m, rate_of_penetration, bit_type, operator_id, downtime_min, downtime_reason",
   col="rate_of_penetration", limit="8.0", unit="m/h",
   rows=300,
   story="One bit type performs clearly worse — but only on the night shift. Both facts are in the file and "
         "neither is in any single column.",
   herrings="Two red herrings: total downtime is highest for the deepest holes, which is expected rather than "
            "interesting, and one operator has very few rows because they only started last month.",
   report="mean rate of penetration per bit type; total downtime per reason code; and the number of rows "
          "skipped because a field was blank"),
 "CML3111": dict(
   file="motor_test_bench.csv",
   cols="motor_id, supply_v, current_a, rpm, winding_temp_c, vibration_rms, pass_fail",
   col="winding_temp_c", limit="130.0", unit="degrees C",
   rows=300,
   story="One motor runs hot, but only at low supply voltage — so at nominal voltage it passes every time and "
         "the pass/fail flag never caught it.",
   herrings="Two red herrings: vibration is higher across the board on one test day (the bench was not bolted "
            "down), and one motor has a single wild current reading that is a logging error.",
   report="mean winding temperature rise per motor; the count of readings above the 130 degree alarm limit; and "
          "the number of rows skipped because a field was blank"),
}

# ---------------------------------------------------------------- Week 5 twelve questions
W5 = {
 "CML3112": dict(
   anchor="Concrete Compressive Strength",
   file="concrete_strength.csv",
   source="UCI Machine Learning Repository, dataset 165, CC BY 4.0",
   shape="1,030 rows x 9 columns",
   cols="cement, blast furnace slag, fly ash, water, superplasticiser, coarse aggregate, fine aggregate, "
        "age in days, and compressive strength in MPa",
   qs=["How many mixes are in the file, and how many columns?",
       "What is the mean compressive strength, and the range?",
       "How many mixes were tested at 28 days rather than some other age?",
       "What is the mean strength of the 28-day mixes only?",
       "Which mix has the highest strength, and what was its cement content?",
       "How does mean strength differ between mixes with and without fly ash?",
       "Add a water-to-cement ratio column. What is its range?",
       "What is the mean strength for water/cement below 0.4, and above 0.6?",
       "How many mixes would fail a 25 MPa specification?",
       "Group by age band and report the mean strength of each.",
       "Which two columns are most strongly associated with strength?",
       "Save the 28-day mixes with their water/cement ratio to a new CSV."],
   derived="water-to-cement ratio", derived_code='df["w_c"] = df["water"] / df["cement"]',
   group="age band", agg="mean compressive strength",
   col="strength", thr="40", gcol="age_band",
   nrows="1030", ncols="9", rec="mixes", gname="age band"),
 "CML3113": dict(
   anchor="Quality Prediction in a Mining Process (froth flotation)",
   file="flotation_subset.csv",
   source="Kaggle, edumagalhaes — subset to 20,000 rows for teaching",
   shape="20,000 rows x 24 columns after subsetting",
   cols="iron and silica feed grades, starch and amina flow, ore pulp flow, pH and density, air flow and level "
        "for seven flotation columns, and the iron and silica concentrate assays",
   qs=["How many records are in the subset, and how many columns?",
       "What is the mean silica in the concentrate, and the range?",
       "What is the distribution of iron feed grade?",
       "How does mean concentrate silica differ between high and low iron feed?",
       "Which record has the worst concentrate silica, and what was the feed like?",
       "What is the mean starch flow, and how much does it vary?",
       "Add a reagent-to-feed ratio column. What is its range?",
       "Group by pulp pH band and report mean concentrate silica for each.",
       "How many records would fail a 3 per cent silica specification?",
       "Which flotation column shows the widest variation in air flow?",
       "Which two process columns are most strongly associated with concentrate silica?",
       "Save the records that failed specification, with the ratio column, to a new CSV."],
   derived="reagent-to-feed ratio", derived_code='df["reagent_ratio"] = df["starch_flow"] / df["ore_pulp_flow"]',
   group="pulp pH band", agg="mean concentrate silica",
   col="silica_concentrate", thr="3", gcol="ph_band",
   nrows="20000", ncols="24", rec="records", gname="pulp pH band"),
 "CML3111": dict(
   anchor="Combined Cycle Power Plant",
   file="power_plant.csv",
   source="UCI Machine Learning Repository, dataset 294",
   shape="9,568 rows x 5 columns",
   cols="ambient temperature, exhaust vacuum, ambient pressure, relative humidity, and net hourly electrical "
        "power output in megawatts",
   qs=["How many hours are in the file, and how many columns?",
       "What is the mean power output, and the range?",
       "What is the distribution of ambient temperature?",
       "How does mean power output differ between the coldest and hottest quarter of hours?",
       "Which hour had the lowest output, and what were the conditions?",
       "What is the mean output when humidity is above 80 per cent?",
       "Add a temperature-rise-above-minimum column. What is its range?",
       "Group by temperature band and report the mean output of each.",
       "How many hours fell below 430 MW?",
       "Which single variable varies most, relative to its own mean?",
       "Which two variables are most strongly associated with power output?",
       "Save the hours below 430 MW, with the derived column, to a new CSV."],
   derived="temperature rise above the minimum recorded",
   derived_code='df["t_rise"] = df["AT"] - df["AT"].min()',
   group="temperature band", agg="mean power output in MW",
   col="output", thr="450", gcol="temp_band",
   nrows="9568", ncols="5", rec="machine-hours", gname="temperature band"),
}

# ---------------------------------------------------------------- Week 6 defects & outliers
W6 = {
 "CML3112": dict(
   damaged="A damaged copy of the concrete dataset, plus building_performance_survey.csv",
   defects=["Eighteen floor areas recorded as 0 rather than left blank — a zero-coded missing value",
            "Forty-one duplicated rows from an export that was run twice",
            "One compressive strength entered as text: \"32.5 MPa\" instead of 32.5",
            "Three negative crack widths",
            "A slab thickness of 2.5 metres",
            "Curing age recorded in months for part of the file and days for the rest"],
   outliers=[("A 28-day strength of 91 MPa", "Real. High-performance mixes reach this. Keep it, and check the "
              "mix design confirms it."),
             ("A building using 4 kWh per square metre per year", "Arguable. A genuine passive house can "
              "approach this; so can a building that stood empty all year. You cannot tell from the data alone "
              "— and saying so is the correct answer."),
             ("A crack width of -0.4 mm", "Error. A width cannot be negative. Almost certainly a sign "
              "convention or a data-entry slip."),
             ("An inspection dated 14 months in the future", "Error. Someone typed the wrong year."),
             ("A slab 2.5 m thick", "Arguable. Wrong for a suspended floor slab, entirely normal for a raft "
              "foundation or a mass-concrete pour. Check what structure it belongs to before deleting it.")],
   qkey="Does mean strength differ between mixes with and without fly ash?"),
 "CML3113": dict(
   damaged="A damaged copy of the flotation subset, plus assay_register.csv",
   defects=["Missing assays coded as -999, which averages happily and destroys every mean",
            "Twenty-six duplicated laboratory entries",
            "One grade entered as text: \"1.8 %\" instead of 1.8",
            "Four negative flow rates",
            "A pulp pH of 14.0",
            "Grade recorded in per cent for part of the file and grams per tonne for the rest"],
   outliers=[("A gold assay of 45 grams per tonne", "Real, and important. High-grade intersections exist and "
              "deleting them destroys the thing you were looking for."),
             ("A production spike immediately after a shutdown", "Arguable. Could be a real catch-up run, could "
              "be a meter reset. The data alone will not tell you; the shift log would."),
             ("A negative reagent flow rate", "Error. Flow cannot be negative. A sensor fault or a sign error."),
             ("A pulp pH of 14.0", "Error in practice. Achievable in a beaker; a flotation circuit never runs there."),
             ("A bottom-hole pressure of exactly 0", "Arguable. Either the gauge failed, or the well really was "
              "shut in and vented. Both happen, and they need different handling.")],
   qkey="Does concentrate silica differ between high and low iron feed grade?"),
 "CML3111": dict(
   damaged="A damaged copy of the plant dataset, plus sensor_stream.csv",
   defects=["Sensor dropouts recorded as 0.0 rather than as missing",
            "A stuck-at value: vibration reads exactly 2.41 for six straight hours",
            "Thirty-three duplicated logger rows",
            "One current entered as text: \"12.5 A\" instead of 12.5",
            "A timestamp gap of four hours with no rows at all",
            "Winding temperature in Fahrenheit for part of the file and Celsius for the rest"],
   outliers=[("A current spike at motor start-up", "Real. Inrush current is six to eight times running "
              "current and it is physics. Deleting it hides normal behaviour."),
             ("A winding temperature of 200 degrees", "Arguable. Beyond every insulation class, so either the "
              "motor was destroyed or the sensor failed. Which one changes what you do."),
             ("Vibration of exactly 0.00 for six hours", "Error. A real sensor is never exactly zero. This is a "
              "dead channel reading as good news, which is the most dangerous defect on this list."),
             ("A negative power reading", "Arguable. An error on a motor; entirely correct on a regenerating "
              "drive or an inverter exporting to the grid."),
             ("30,000 rpm on a four-pole induction motor", "Error. The synchronous speed at 50 Hz is 1,500 rpm. "
              "A decimal point or a unit is wrong.")],
   qkey="Does power output differ between the coldest and hottest hours?"),
}

# ---------------------------------------------------------------- Week 11 features
W11 = {
 "CML3112": dict(
   metric="MAE in MPa",
   tgt="28-day compressive strength",
   domfeat="water/cement ratio",
   domraw="cement content in kg/m3",
   domwhy="Abrams' law: strength is governed by the water carried per unit of cement. Two mixes both batched "
          "at 380 kg/m3 of cement behave nothing alike if one of them is much wetter than the other.",
   domcode='df["w_c"] = df["water"] / df["cement"]',
   rawcol="cement", rawcol2="water", featcol="w_c", splitex="cement <= 320",
   catcol="exposure_class",
   catvals="XC1, XC3, XD2, XS1",
   catnote="These are three different exposure types - carbonation, chlorides and seawater - rather than "
           "one severity scale, so an ordered number cannot be defended across them. "
           "The gap between XC3 and XD2 has no measurable size, which is why one-hot encoding is the safer "
           "default.",
   ordinal_eg="fire resistance ratings REI 30, REI 60 and REI 120, where the label is itself a "
              "number of minutes, so the spacing between the classes is known rather than assumed, in "
              "minutes",
   standard="the 0.30 mm crack-width action limit, and the maximum water/cement ratio the durability code "
            "sets for each exposure class",
   five=[("water/cement ratio",
          "water divided by cement. Abrams' law. In the ablation table it is second only to curing "
          "age, and it is the strongest column you can build rather than measure."),
         ("total binder, kg/m3",
          "cement plus blast furnace slag plus fly ash. Hydration uses all three, so the cement column on its "
          "own understates the binder."),
         ("supplementary binder fraction",
          "slag plus fly ash, divided by total binder. It governs how much strength arrives after 28 days."),
         ("logarithm of curing age in days",
          "strength gain is roughly linear in the logarithm of age, so the logarithm gives a straight-line "
          "model something it can use."),
         ("aggregate-to-binder ratio",
          "coarse plus fine aggregate, divided by total binder. A stand-in for paste content, which drives "
          "workability and shrinkage.")],
   nohelp="water content on its own, once the water/cement ratio is in the model. The ratio has already taken "
          "almost everything the raw water column was carrying, so dropping it moves the MAE by under "
          "0.1 MPa, and slightly downwards.",
   adv_result="The feature teams normally win by 3 to 5 MPa of MAE using linear regression alone, while the "
              "raw-column teams reach for a random forest and still come second. Water/cement ratio is doing "
              "all of it."),

 "CML3113": dict(
   metric="MAE in percentage points of silica",
   tgt="silica in the concentrate",
   domfeat="reagent dose per tonne of feed",
   domraw="starch flow in g/min",
   domwhy="What a reagent does depends on how much ore it has to coat. 600 g/min into a heavy feed is a weak "
          "dose; the same 600 g/min into a light feed is a strong one.",
   domcode='df["starch_dose"] = df["starch_flow"] / df["ore_pulp_flow"]',
   rawcol="starch_flow", rawcol2="ore_pulp_flow", featcol="starch_dose",
   splitex="starch_flow <= 3200",
   catcol="ore_source",
   catvals="pit 1, pit 3, stockpile, blend",
   catnote="These four have no order at all. Numbering them 1 to 4 would tell a straight-line model that a "
           "blend sits twice as far from pit 1 as pit 3 does, which means nothing.",
   ordinal_eg="crushing stage — primary, secondary, tertiary — or sieve size classes, both of which are "
              "genuinely ordered",
   standard="the 3 per cent silica concentrate specification, and the pulp pH set point of 9.0 from the "
            "process manual",
   five=[("starch dose per tonne of feed",
          "starch flow divided by ore pulp flow. A dose is only meaningful against the tonnage it has to "
          "treat."),
         ("amina-to-starch ratio",
          "collector against depressant. The balance between the two matters more than either flow alone."),
         ("total air flow across the seven columns, m3/h",
          "the circuit is aerated as a whole, so the sum is closer to the physical quantity than any single "
          "column."),
         ("air flow per unit of froth level",
          "aeration intensity. The same air into a deep froth and a shallow froth are two different duties."),
         ("iron-to-silica feed ratio",
          "feed quality expressed as one number, which is what the metallurgist actually reasons about.")],
   nohelp="the record index. It rises steadily with time and appears associated with almost every column, and "
          "it is a row number. Dropping it changes the MAE by about 0.01 percentage points.",
   adv_result="The feature teams normally win by 0.3 to 0.5 percentage points of silica using linear "
              "regression, while the raw-column teams get most of the way there with a forest and cannot say "
              "which reading drove any prediction."),

 "CML3111": dict(
   metric="recall on the failure class",
   tgt="whether the machine fails",
   domfeat="mechanical power in kW",
   domraw="shaft torque in N·m",
   domwhy="Heating follows mechanical power, and power is torque times angular velocity. The same 45 N·m at "
          "1,300 rpm and at 2,800 rpm are two completely different duties for the motor.",
   domcode='df["power_kw"] = df["torque_nm"] * 2 * 3.14159 * df["rpm"] / 60.0 / 1000.0',
   rawcol="torque_nm", rawcol2="rpm", featcol="power_kw", splitex="torque_nm <= 47",
   catcol="product_type",
   catvals="L, M, H",
   catnote="These are quality grades and they are ordered by hardness, so one ordered column is defensible. "
           "Whether H sits as far above M as M sits above L is unknown, and one-hot encoding avoids having to "
           "claim it.",
   ordinal_eg="insulation classes A, E, B, F and H, which are ordered and carry a stated temperature limit "
              "each",
   standard="the 130 °C alarm and 155 °C trip limits that follow from the insulation class on the motor's "
            "datasheet",
   five=[("mechanical power, kW",
          "torque times 2 pi times rpm, divided by 60, then by a thousand. The quantity that actually "
          "heats the machine."),
         ("temperature rise, K",
          "process temperature minus air temperature. A rise is comparable between a cold morning and a hot "
          "afternoon; an absolute reading is not."),
         ("specific tool wear",
          "tool wear divided by mechanical power. How much wear the tool carries for the duty it is "
          "being worked at."),
         ("torque per unit speed",
          "a loading ratio. High torque at low speed is the duty that kills gearboxes."),
         ("power times tool wear",
          "an accumulated duty term. It rises when a hard-working machine also has a worn tool.")],
   nohelp="the machine identifier, one-hot encoded. It gives the model a way to memorise individual machines "
          "and tells you nothing about a machine you have not met. Recall on the failure class moves by about "
          "one percentage point when you drop it.",
   adv_result="The feature teams normally win 8 to 12 points of recall on the failure class using logistic "
              "regression, while the raw-column teams reach for a forest and come close on accuracy and well "
              "short on recall."),
}

# ---------------------------------------------------------------- Week 12 comparison challenge
W12 = {
 "CML3112": dict(
   client="the quality manager of a precast concrete yard",
   brief='"We reject about one panel in twelve at the 7-day cube test, and by then the panel is cast. Give us '
         'something that flags a mix as likely to miss 32 MPa at 28 days on the day it is batched. I sign '
         'every rejection and the client reads my reason for it."',
   constraint="Every rejection has to be explained in writing to a paying client.",
   dataset="a mix-and-strength dataset from a plant you have not seen, about 1,400 rows",
   target="whether a mix reaches 32 MPa at 28 days",
   metric_note="A weak panel that gets through goes into a building. A panel rejected for no reason costs one "
               "panel. The two mistakes have very different prices, so an accuracy figure will not settle "
               "this on its own.",
   models=["Logistic regression on the engineered features",
           "A decision tree with max_depth between 3 and 5",
           "A random forest with 300 trees",
           "k-nearest neighbours inside a scaling pipeline"],
   planted="The forest beats logistic regression by about 0.02 of F1, and the fold-to-fold spread on both is "
           "about 0.04 — so the two cannot be separated on this data. The tree at depth 3 reads as a mix "
           "rule the quality manager could sign. A team that reports the forest as the winner has ignored "
           "both the spread and the client's constraint.",
   attacks=["Your recall is 0.71. Which panels are the 29 per cent you miss, and where do they end up?",
            "You picked the forest. Read me the reason it rejected batch 812.",
            "Your water/cement ratio comes from a batching sheet. What happens on a wet day when the "
            "aggregate is already soaked?"]),

 "CML3113": dict(
   client="the metallurgist of a concentrator",
   brief='"The assay comes back an hour late, and by then we have run an hour of off-spec concentrate. '
         'Predict concentrate silica from the readings we already have on the panel. If the model tells the '
         'operator to move a set point, the operator will ask which reading drove it."',
   constraint="The operator has to be able to see which reading drove the call.",
   dataset="a flotation dataset from a circuit you have not seen, about 12,000 rows",
   target="concentrate silica in percentage points",
   metric_note="Being wrong by 0.2 percentage points is a rounding error. Being wrong by 1.5 percentage "
               "points ships off-spec material for an hour. Think about which errors your metric is willing "
               "to average away.",
   models=["Linear regression on the engineered features",
           "A decision tree with max_depth between 3 and 6",
           "A random forest with 300 trees",
           "k-nearest neighbours inside a scaling pipeline"],
   planted="The forest wins on MAE by about 0.15 percentage points and gives the operator nothing to act on. "
           "The linear model's coefficients read as set-point advice directly. There is also a lag in the "
           "data: the assay belongs to material that left the circuit twenty minutes earlier, and a team "
           "that spots the lag has found the real problem.",
   attacks=["Your model says lower the amina flow. By how much, and where does that number come from?",
            "You trained on twelve thousand rows twenty seconds apart. How many independent observations is "
            "that really?",
            "Which pit was the feed from during your test rows, and would the model still hold on the next "
            "bench?"]),

 "CML3111": dict(
   client="the maintenance planner of a production line",
   brief='"We stop the line once a month on a calendar schedule whether or not anything needs doing. Tell us '
         'when a machine actually needs attention. A false alarm costs us a four-hour stop. A missed failure '
         'costs a gearbox and a week of production."',
   constraint="A false alarm costs four hours. A missed failure costs a gearbox and a week.",
   dataset="a machine sensor dataset from a line you have not seen, about 10,000 machine-hours",
   target="whether a machine fails within the next shift",
   metric_note="Work out what one false alarm and one missed failure each cost, in hours, before you choose a "
               "metric. The cost ratio here is roughly one to forty, and that ratio is what picks your "
               "metric and your threshold.",
   models=["Logistic regression on the engineered features",
           "A decision tree with max_depth between 3 and 5",
           "A random forest with 300 trees",
           "k-nearest neighbours inside a scaling pipeline"],
   planted="Failures are about 3.4 per cent of the rows, so every model reports over 96 per cent accuracy and "
           "one of them predicts no failures at all. The decision threshold matters more than the choice of "
           "model here, and a team that moves the threshold and shows the trade-off has understood the "
           "session better than a team that found a slightly better model.",
   attacks=["You accept eleven false alarms a month. Have you asked what the operators do to an alarm that "
            "cries wolf?",
            "Your recall is 0.62 on the failure class. Which failure mode are you blind to?",
            "The line was rewound in March. Which side of that date is your training data on?"]),
}

# ---------------------------------------------------------------- Week 13 repository studio
W13 = {
 "CML3112": dict(
   repo="concrete-strength/",
   datafile="concrete_strength.csv",
   metric="MAE in MPa",
   smells=["A path that reads C:/Users/.../Desktop/concrete_final_v3.csv, so the notebook runs on one laptop "
           "in the world.",
           "Three separate cells that all assign df, run in an order nobody wrote down.",
           "The duplicate rows removed by hand in Excel before loading, with no record of which rows went.",
           "A chart titled 'output' with no units on either axis.",
           "random_state left unset, so the reported MAE moves by 0.4 MPa between runs.",
           "Forty commented-out lines kept in case they are needed again."],
   readme=["A precast yard wants 28-day strength estimated on the day a mix is batched.",
           "1,030 mixes from the UCI Concrete Compressive Strength dataset, CC BY 4.0.",
           "A file of nine columns, five engineered features, and a Pipeline with a scaler and a "
           "linear model.",
           "MAE 3.6 MPa on held-out mixes, 5-fold cross-validated at 3.8 plus or minus 0.4 MPa.",
           "The data is laboratory cylinders. Site-cured concrete is weaker and this model has never seen "
           "any."],
   cap_bad="Figure 3: strength against cement content.",
   cap_good="Figure 3: strength rises with cement content and flattens above 400 kg/m3, so the last 50 kg/m3 "
            "buys about 1 MPa."),

 "CML3113": dict(
   repo="flotation-silica/",
   datafile="flotation_subset.csv",
   metric="MAE in percentage points of silica",
   smells=["A path that reads C:/Users/.../Desktop/flotation_final_v3.csv, so the notebook runs on one laptop "
           "in the world.",
           "Three separate cells that all assign df, run in an order nobody wrote down.",
           "The -999 assays replaced by hand in Excel before loading, with no record of how many there were.",
           "A chart titled 'output' with no units on either axis.",
           "random_state left unset, so the reported MAE moves by 0.08 percentage points between runs.",
           "Forty commented-out lines kept in case they are needed again."],
   readme=["A concentrator wants concentrate silica now instead of an hour after the assay.",
           "20,000 rows of the Kaggle froth flotation process dataset, subset for teaching.",
           "A file of twenty-four columns, five engineered features, and a Pipeline with a scaler "
           "and a linear model.",
           "MAE 0.42 percentage points of silica on held-out rows, 5-fold cross-validated at 0.45 plus or "
           "minus 0.06.",
           "Readings twenty seconds apart are not independent, so the effective sample is far smaller than "
           "20,000."],
   cap_bad="Figure 3: silica against starch flow.",
   cap_good="Figure 3: concentrate silica falls as starch dose rises to about 900 g per tonne of feed and "
            "flattens after that."),

 "CML3111": dict(
   repo="machine-failure-risk/",
   datafile="ai4i2020.csv",
   metric="recall on the failure class",
   smells=["A path that reads C:/Users/.../Desktop/motor_log_FINAL.csv, so the notebook runs on one laptop in "
           "the world.",
           "Three separate cells that all assign df, run in an order nobody wrote down.",
           "The zero-coded sensor dropouts deleted by hand in Excel before loading, with no record of how "
           "many rows went.",
           "A chart titled 'output' with no units on either axis.",
           "random_state left unset, so the reported recall moves by three points between runs.",
           "Forty commented-out lines kept in case they are needed again."],
   readme=["A maintenance team wants to know which machine needs attention before the next shift.",
           "10,000 machine-hours from the AI4I 2020 Predictive Maintenance dataset.",
           "Five sensor columns, five engineered features, a Pipeline with a scaler and logistic regression.",
           "Recall 0.78 on the failure class at a threshold of 0.22, precision 0.31, 5-fold cross-validated.",
           "Failures are 3.4 per cent of the rows, so accuracy says nothing here and the threshold carries "
           "the decision."],
   cap_bad="Figure 3: failures against tool wear.",
   cap_good="Figure 3: the failure rate rises sharply above 200 minutes of tool wear, from 2 per cent to "
            "11 per cent."),
}


# ---------------------------------------------------------------- Weeks 8-10
W8 = {
 "CML3112": dict(
   tgt="28-day compressive strength", tgtcol="strength", unit="MPa", file="concrete_strength.csv",
   feats='["cement", "water", "age"]',
   good="A cylinder test is repeatable to roughly 2 MPa between specimens of the same mix. A model that "
        "predicts to plus or minus 5 MPa is therefore about two and a half times as uncertain as the "
        "test it replaces.",
   act="Would you pour on the strength of it? No. Would you use it to rank six candidate mixes before "
       "casting any of them? That is a much easier yes, and it is where a model like this earns its keep.",
   addfeat="the water-to-cement ratio", dropfeat="curing age"),
 "CML3113": dict(
   tgt="silica in the concentrate", tgtcol="silica_concentrate", unit="% silica", file="flotation_subset.csv",
   feats='["iron_feed", "starch_flow", "pulp_ph"]',
   good="The laboratory assay itself repeats to about 0.1 percentage points. A model predicting to plus or "
        "minus 0.4 points is four times looser than the measurement it stands in for.",
   act="Would a metallurgist change a reagent set point on it? Probably not on its own. Would they use it to "
       "see a drift an hour before the assay confirms it? Yes, and that hour is the whole value.",
   addfeat="the reagent-to-feed ratio", dropfeat="pulp pH"),
 "CML3111": dict(
   tgt="net hourly power output", tgtcol="output", unit="MW", file="power_plant.csv",
   feats='["AT", "V", "AP", "RH"]',
   good="Published work on this dataset reaches roughly 3 to 4 MW root-mean-square error, so you have an "
        "external yardstick: if your model is at 12 MW there is something to fix, and if it is at 3 MW you "
        "are where the literature is.",
   act="Would a control room schedule generation on it? Not alone. Would a planner use it to estimate output "
       "for tomorrow's forecast conditions? Yes, with the error stated.",
   addfeat="temperature rise above the minimum recorded", dropfeat="relative humidity"),
}

W9 = {
 "CML3112": dict(
   task="Predict whether a pour will meet its specification class",
   pos="fails specification", neg="meets specification",
   fp="You reject a pour that was actually sound: a demolition, a re-pour, a week of programme lost.",
   fn="You accept a pour that was substandard: it goes into the structure and somebody finds out later.",
   costs=["cost of rejecting a sound pour", "cost of accepting a substandard pour",
          "cost of an unnecessary core test", "delay cost of stopping the works"],
   which="Recall on the failing class. A missed substandard pour is structural; a false alarm is expensive.",
   imb="site defect records, where roughly 3 in 100 inspections find something serious"),
 "CML3113": dict(
   task="Classify material as ore or waste at the cut-off grade",
   pos="above cut-off", neg="below cut-off",
   fp="You send waste to the mill: you pay to process rock that yields nothing.",
   fn="You send ore to the dump: you throw away metal you already paid to mine, and you never find out.",
   costs=["cost of milling waste", "value of ore sent to the dump",
          "cost of an extra assay", "cost of a misrouted truck"],
   which="It depends on the grade. Near the cut-off the two errors cost about the same; well above it, "
          "missing ore is far worse.",
   imb="equipment failure records, where roughly 3 in 100 machine-hours end in a failure"),
 "CML3111": dict(
   task="Predict whether a machine will fail within the next operating hour",
   pos="fails", neg="runs normally",
   fp="A false alarm: you stop a healthy line, and the operator learns to distrust the alarm.",
   fn="A missed failure: the machine destroys itself, and possibly injures somebody.",
   costs=["cost of a false alarm and a stopped line", "cost of a destroyed machine and lost production",
          "cost of an unnecessary callout", "safety consequence of an undetected fault"],
   which="Recall, and by a long way. But watch the false-alarm rate: an alarm nobody believes is worse "
          "than no alarm.",
   imb="the AI4I 2020 set, where 3.4 in 100 machine-hours end in a failure"),
}

W10 = {
 "CML3112": dict(
   leak1="a 28-day strength column left among the features while predicting strength class",
   leak2="the missing slump values filled with the mean of the whole file before the split, so every " 
         "training row already carries information from the test rows",
   leak3="a specimen identifier that encodes the batch, and the batch determines the strength",
   grp="mix batch", grpwhy="specimens from one batch are near-copies of each other"),
 "CML3113": dict(
   leak1="the laboratory silica assay left among the features while predicting silica",
   leak2="the sensor columns standardised across the whole file before the split, so the mean and " 
         "spread the scaler used already included every test row",
   leak3="a hole identifier that encodes the lithology you are trying to predict",
   grp="drill hole", grpwhy="samples from one hole are far more alike than samples from different holes"),
 "CML3111": dict(
   leak1="a maintenance-action column left among the features while predicting failure",
   leak2="the vibration and temperature columns scaled across the whole file before the split, so the " 
         "scaler had already measured every test row",
   leak3="a machine identifier that encodes which units were already known to be failing",
   grp="machine", grpwhy="consecutive hours from one machine are almost the same reading twice"),
}
