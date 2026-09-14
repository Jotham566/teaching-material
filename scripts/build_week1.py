# -*- coding: utf-8 -*-
"""Week 1 as full 3-hour teaching material, revisable. Three cohorts."""
import sys, os
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from pptxkit import *   # noqa

FIG = _ROOT + "/figs"
OUTDIR = _ROOT + "/IUEA_Teaching_Plan/decks"
os.makedirs(OUTDIR, exist_ok=True)
FOOT = "IUEA Faculty of Engineering · Semester 1, 2026/27"
NSEG = 11

# Per-cohort QR for the end-of-session quiz.
#
# quiz_links.json is the source of truth, NOT the presence of a PNG. A week
# absent from that file gets the labelled placeholder even if a stale image is
# still sitting in qr/, which is what stops a demo or a superseded link from
# reaching a deck.
QRDIR = _ROOT + "/qr"
QRLINKS = _ROOT + "/data/quiz_links.json"
_LINKS = None


def _links():
    global _LINKS
    if _LINKS is None:
        try:
            import json
            with open(QRLINKS, encoding="utf-8") as fh:
                _LINKS = json.load(fh)
        except Exception:
            _LINKS = {}
    return _LINKS


def qrp(code, wk):
    if not _links().get("%s|%d" % (code, wk)):
        return None
    p = os.path.join(QRDIR, "quiz_%s_W%02d.png" % (code, wk))
    return p if os.path.exists(p) else None


SLOT = {"CML3112": ("Tuesday 11:00–14:00 · Room 106", "Tue 8 September 2026"),
        "CML3113": ("Friday 08:00–11:00 · Room 105", "Fri 11 September 2026"),
        "CML3111": ("Friday 11:00–14:00 · Room 115", "Fri 11 September 2026")}

CO = {
 "CML3112": dict(short="Design_Infrastructure", progs="Architecture + Civil Engineering",
   title="Introduction to Machine Learning in Design & Infrastructure",
   q='Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?',
   dataset="Concrete Compressive Strength", unit="MPa", tgt="28-day compressive strength",
   feat="cement, water, aggregate and curing age",
   domain="construction, structures, materials and building performance",
   rule_eg="IF the crack is wider than 0.30 mm THEN flag it for repair",
   rule_why="A code of practice gives you the threshold. You do not need data to write that rule.",
   ml_eg="4,000 past inspections, each with the measurements taken and what the engineer decided",
   probes=["Concrete strength from a mix design, without waiting 28 days",
           "A building's energy use before it is built",
           "Which sections of road will deteriorate first",
           "Defect severity from inspection records, more consistently than three inspectors"],
   lim_nodata="Most site inspection records before about 2015 exist only on paper, in a box.",
   lim_nosignal="The colour of the site hoarding does not predict concrete strength. A model fed that column will still return a number.",
   lim_physics="For a simply supported beam under a uniform load, the bending moment has an exact formula. Use it.",
   lim_future="A model trained on one quarry's aggregate may quietly stop working when the supplier changes.",
   cls_eg="strength class: below 25 MPa, 25 to 40, above 40",
   tabfeat="cement content, water content and curing age",
   cause="A target is not the same as a cause. Cement content is associated with strength; the model learns the association and knows nothing about hydration chemistry.",
   num_tgt="28-day compressive strength", num_unit="MPa",
   unitid="SPAN_07", units_pl="bridge spans", arrq="crack widths",
   finding="strength rises with cement but flattens above 400 kg/m3",
   recname="inspection records", derivcol="water/cement ratio",
   proj="Building Energy Predictor · Concrete Strength Estimator · Pavement Deterioration Forecast"),

 "CML3113": dict(short="Mining_Petroleum", progs="Mining + Petroleum Engineering",
   title="Introduction to Machine Learning in Mining & Petroleum Engineering",
   q='The silica assay takes an hour to come back from the laboratory. Can we know it now, from the process variables we already measure?',
   dataset="froth flotation process data", unit="% silica", tgt="silica in the concentrate",
   feat="iron feed grade, reagent flows, pulp pH and column air flow",
   domain="exploration, ore and reservoir characterisation, production and equipment health",
   rule_eg="IF the pulp pH falls below 9.0 THEN alarm the operator",
   rule_why="Process engineering gives you that set point. No data is needed to write the rule.",
   ml_eg="six months of process readings every twenty seconds, each with the assay that came back later",
   probes=["Concentrate quality now, instead of in an hour",
           "Lithology from well logs already drilled",
           "Which haul truck fails next, from its own sensor history",
           "Ore or waste, with the cost of each mistake made explicit"],
   lim_nodata="Blast fragmentation was judged by eye for decades. There is no dataset of it.",
   lim_nosignal="The shift supervisor's name does not cause recovery to change. A model given that column will still find a pattern in it.",
   lim_physics="Contained metal is tonnage times grade. That is arithmetic; there is nothing to predict.",
   lim_future="A model trained on one ore body will not transfer to the next bench when the mineralogy changes.",
   cls_eg="ore or waste; or lithology: sandstone, shale, limestone",
   tabfeat="iron feed grade, starch flow and pulp pH",
   cause="A target is not the same as a cause. Starch flow is associated with concentrate quality; the model learns the association and knows nothing about surface chemistry.",
   num_tgt="silica in the concentrate", num_unit="percentage points",
   unitid="HOLE_114", units_pl="drill holes", arrq="assay grades",
   finding="concentrate silica falls as starch flow rises, but only while the pulp pH stays above 9",
   recname="assay records", derivcol="reagent-to-feed ratio",
   proj="Real-Time Concentrate Quality Predictor · Lithology Classifier · Equipment Failure Risk"),

 "CML3111": dict(short="Engineering", progs="Electrical, Mechatronics & Robotics, Communications",
   title="Introduction to Machine Learning in Engineering",
   q='This machine has three sensors on it. It failed last month. Could we have known?',
   dataset="AI4I 2020 Predictive Maintenance", unit="N·m", tgt="whether the machine fails",
   feat="air and process temperature, rotational speed, torque and tool wear",
   domain="sensors, signals, energy systems, fault detection and machine health",
   rule_eg="IF the winding temperature exceeds 130 °C THEN trip the motor",
   rule_why="The insulation class gives you that limit. It is a rule you can write from a datasheet.",
   ml_eg="10,000 machine-hours of sensor readings, each labelled with whether a failure followed",
   probes=["Failure before it happens, from sensor history alone",
           "Plant output from ambient conditions",
           "A real fault told apart from a start-up transient",
           "How many false alarms an operator will tolerate before disabling the alarm"],
   lim_nodata="Most motors in most plants have no sensor on them at all. There is nothing to learn from.",
   lim_nosignal="The cabinet's paint colour does not predict bearing failure. Feed it in and a model will still produce a number.",
   lim_physics="Power is voltage times current. Do not train a model to rediscover Ohm's law.",
   lim_future="A model trained before a rewind or a firmware change may silently stop being true afterwards.",
   cls_eg="failure or no failure; or fault type: bearing, winding, imbalance",
   tabfeat="rotational speed, torque and tool wear",
   cause="A target is not the same as a cause. Tool wear is associated with failure; the model learns the association and knows nothing about metal fatigue.",
   num_tgt="shaft torque", num_unit="N·m",
   unitid="MOTOR_07", units_pl="motors", arrq="winding temperatures",
   finding="torque climbs steadily with tool wear and drops back the moment the tool is changed",
   recname="sensor logs", derivcol="temperature rise",
   proj="Motor Anomaly Detector · Machine Failure Risk Model · Power Output Forecaster"),
}


def build(code):
    c = CO[code]
    prs = deck()
    seg_reset()
    notes_context(f"{code} Week 1")
    f = lambda n: os.path.join(FIG, n)

    # ============================================ FRONT MATTER
    slot, date1 = SLOT[code]
    s = s_title(prs, code, "AI, machine learning\nand the engineering problem",
                c["title"], "WEEK 1  ·  " + date1, slot + "  ·  " + FOOT)
    notes(s, "Today runs entirely on paper. You will not touch a computer, so nothing you do this session "
             "depends on owning a laptop or having a connection. By the end you will have answered a real "
             "engineering question from twelve rows of a real dataset with a pencil, and measured how wrong you "
             "were.\n\nTO TEACH: print the 12-row dataset extracts (one per team), the Problem Hunt board "
             "sheets, the paper laptop-access survey and the question card for the challenge. Open by saying "
             "how long you have been doing this and one thing you got wrong recently. A room of beginners needs "
             "to know the lecturer is fallible before it will risk being wrong out loud.")

    # ---- who is teaching this, and what they have actually built
    s = s_profile(
        prs,
        "Jotham Martin Wambi",
        "Data scientist and ML engineer · Founding engineer, Magentiq AI Labs",
        "JW",
        "Background",
        # Four lines, because the column is 4.7in wide and every line now sets
        # at about 18pt: seven rows could only fit by dropping the type back
        # to where a student in row twelve could not read it. The full version
        # is in the teaching guide and in the syllabus.
        ["PhD Informatics, UEC Tokyo — in progress",
         "MSc Data Science and ML, Yamaguchi, 2024 — valedictorian",
         "BSc IT, Makerere · BA Economics, IUIU",
         "Eight years at Citibank, EY and D'isum Inc, Tokyo"],
        "Some of what I have built",
        # Three, same reason. CARSA came off because it is the one furthest
        # from what this class will build.
        [("Law Lens",
          "Language models over Ugandan law, fully traceable."),
         ("Magentiq AssetGuard",
          "Machine failure predicted from vibration sensors."),
         ("Wearable ECG detection",
          "Eleven cardiac conditions from a live ECG.")],
        "linkedin.com/in/jothammartinwambi   ·   github.com/Jotham566   ·   "
        "jothammartin.wambi@gmail.com",
        "Every system on the right uses the pipeline you build from Week 8: split the data, "
        "fit a model, then score it.")
    notes(s, "A short introduction, and there is a reason for it beyond courtesy.\n\n"
             "First, so that you know what you can ask me for. The work on the right is where my "
             "experience actually is: sensor data and predictive maintenance, language models over "
             "documents, and getting models into something a colleague can use. If your project heads in "
             "one of those directions I can help you in detail. If it heads somewhere I know less well, I "
             "will tell you that rather than guess.\n\n"
             "Second, because of the route rather than the titles. I read economics and information "
             "technology as undergraduate degrees, and my first seven years of work were in banking, tax "
             "and product management, none of which involved building a model. Nobody starts where this "
             "field expects them to start, and the engineering degree you are already halfway through is a "
             "better foundation for machine learning than most computing degrees, for reasons we come to "
             "in the roadmap segment.\n\n"
             "Third, so the claims in this course are checkable. Where I tell you a technique behaves a "
             "certain way, it is usually because I have watched it fail somewhere first.\n\n"
             "The contact details are real. Use them.")

    s = s_objectives(prs, [
        "Say what artificial intelligence, machine learning and data science each mean, and how they differ.",
        "Explain the difference between writing a rule yourself and letting a computer infer one from examples.",
        "Point at a table of data and correctly identify the features and the target.",
        "Tell a regression problem from a classification problem, and give an example of each from your own field.",
        "Name three problems in " + c["domain"] + " where data could help, and two where it could not.",
        "State four things machine learning cannot do, with a reason for each.",
        "Describe how this course is assessed and what your project will look like."],
        1, "AI, machine learning and the engineering problem")
    notes(s, "Seven objectives, and they are the whole session. Nothing is hidden behind them and there is no "
             "reading list you are expected to have done. Mark yourself against each one at the end of the "
             "session; whatever you cannot claim is what to revise before Week 2.\n\nTO TEACH: read these out. "
             "Students at zero need to know the session has a bottom — that it is finite and achievable — or "
             "the volume of new words feels limitless. Come back to this slide at the end and ask them to "
             "self-assess against it: ninety seconds, and the cheapest way to make a three-hour session feel "
             "like progress.")

    s = s_figure(prs, "How every session this semester is shaped", f("clock_w1.png"),
                 "Three hours, eleven segments. No block of talking runs longer than 25 minutes, and roughly "
                 "half of every session is you doing something rather than me saying something.",
                 kicker="HOW TODAY RUNS")
    notes(s, "Every session this semester has the same shape: eleven segments across three hours, with no block "
             "of talking longer than 25 minutes and roughly half the time spent working rather than listening. "
             "That is why attendance matters more here than on a lecture course — the practical and challenge "
             "segments cannot be read off a deck afterwards. There is a 10-minute break at the midpoint.\n\nTO "
             "TEACH: put this up and leave it up while you explain. Say the break time out loud so nobody "
             "spends the first hour wondering.")

    s = s_figure(prs, "Where this semester goes", f("arc.png"),
                 "Fifteen weeks. Weeks 7 and 14 are practical tests: you are given data you have never seen and "
                 "asked what you make of it. The project runs from Week 9 to the last session.",
                 kicker="THE SEMESTER")
    notes(s, "Fifteen weeks. Weeks 7 and 14 are practical tests where you are given data you have never seen "
             "and asked what you make of it, and the project runs from Week 9 to the last session. There is "
             "nothing to memorise in this course, which surprises most students who arrive expecting to revise "
             "definitions.\n\nTO TEACH: say the no-memorisation point plainly. If you are teaching a Friday "
             "cohort, flag now that Friday 9 October is Independence Day and Week 5 will be delivered as a "
             "recorded package.")

    s = s_figure(prs, "What you will be able to say by December", f("ladder.png"),
                 "This is the promise of the course. Most of you cannot do step two today. All of you can get "
                 "to step six by December, and the students who do are the ones who do the weekly work.",
                 kicker="THE PROMISE")
    notes(s, "Six steps, from knowing what a dataset is to saying 'here is a model I built and here is how I "
             "know it works'. Most of you cannot do step two today and all of you can reach step six by "
             "December. The students who get there are the ones who do the weekly deliverable every week, and "
             "the difference is visible by about Week 6.\n\nTO TEACH: two minutes on this — it is the "
             "motivation slide of the session. Name the utterance you want to kill, 'Sir, what should I type?', "
             "and the one you want by December: 'we tried three approaches, the first two failed because of X, "
             "so we are testing the third.'")

    # ============================================ SEGMENT 1
    s = s_segment(prs, 1, NSEG, "Welcome, and how this course works", 15,
                  "The promise, the assessment, and what I expect from you. Then we start on the actual "
                  "engineering.")
    notes(s, "Fifteen minutes on how the course works: the promise, the assessment, and what is expected on "
             "both sides. Everything after this segment is engineering.\n\nTO TEACH: keep to time. The "
             "temptation is to spend forty minutes on admin; do not. The hands-on prediction exercise is what "
             "makes them come back next week.")

    s = s_figure(prs, "How you are assessed", f("assessment.png"),
                 "No written examination anywhere in this course. Everything is practical: work with data, "
                 "write and run code, build and evaluate a model, explain your reasoning. Sixty-five per cent "
                 "of the mark is individual, so you cannot be carried and you cannot be dragged down.",
                 kicker="ASSESSMENT")
    notes(s, "Two details the figure does not carry. Every teaching session ends with a five-minute quiz of "
             "five questions, taken on your phone by QR code, auto-marked, and you have your score before "
             "you leave the room. There are twelve of them and the best ten count, one per cent each, so "
             "missing two costs you nothing and there are no resits to arrange. The two practical tests run "
             "offline on lab machines with no internet and no AI assistants. AI tools are permitted and taught "
             "in the coursework provided you declare what you used, because the mark follows what you can "
             "explain.")

    s = s_prose(prs, "What I expect, and what you can expect back", [
        "**What I expect from you**",
        "Attend. There is one three-hour session a week and no lecture to catch up from — the value is in the "
        "practical and the challenge, which cannot be read later.",
        "Do the weekly deliverable every week. Eleven small pieces spread over twelve weeks is manageable; "
        "nine of them attempted in December is not.",
        "Ask, but ask well. Bring the error message, what you already tried, and what you expected to happen. "
        "That is not a hurdle in front of help — it is the actual professional skill.",
        "Struggle before you seek rescue. In the challenge segments you are supposed to be stuck for a while.",
        "**What you can expect from me**",
        "Every rubric published before the work is set. You will never meet a marking scheme for the first "
        "time in an assessment.",
        "Every dataset staged locally, so a slow connection is never your problem.",
        "Feedback on the weekly work within a week, and instant feedback on every quiz.",
        "A straight answer to 'why are we learning this?', every single time it is asked."],
        kicker="THE DEAL")
    notes(s, "The 'ask well' item is the one that changes how much you get out of the semester. Bring the error "
             "message, what you already tried, and what you expected to happen; assembling those three things "
             "solves the problem outright often enough to be worth the effort every time. If you are stuck for "
             "more than five minutes in a practical, put your hand up rather than sitting quietly.\n\nTO TEACH: "
             "read the 'ask well' item slowly. It is the single behaviour that most changes what a beginner "
             "gets from the semester.")

    # ============================================ SEGMENT: THE ROADMAP
    s = s_segment(prs, 2, NSEG, "The whole field, start to finish", 15,
                  "Before we teach you any of it, here is the entire territory — and exactly which parts of it "
                  "this course covers, which parts Semester 2 covers, and which parts we do not touch.")
    notes(s, "This segment hands you the map of the field before any of it is taught, so that every later week "
             "has somewhere to sit rather than arriving from nowhere. The structure follows the public "
             "roadmap.sh Machine Learning roadmap, which is the map the profession itself uses, so you can "
             "check this course against something written outside this room.\n\nTO TEACH: this segment is new "
             "and it is worth protecting. Tell them explicitly that the structure is not a syllabus you "
             "invented.")

    s = s_figure(prs, "The machine learning roadmap", f("roadmap_journey.png"),
                 "Fifteen stages, from Python to transformers. Orange is Semester 1. Green is Semester 2. Dark "
                 "blue is the stage you already have from your engineering degree. Grey is what this course "
                 "deliberately does not teach. Structure follows the public roadmap.sh Machine Learning "
                 "roadmap.",
                 kicker="THE TERRITORY")
    notes(s, "Fifteen stages, from Python to transformers. By December you will have covered stages 1 to 9. "
             "Most of the individual terms on the figure mean nothing to you today and that is expected — what "
             "to take from it is the shape of the field and where this course stops. The interactive version is "
             "at roadmap.sh/machine-learning, and it is worth an evening of clicking around.\n\nTO TEACH: walk "
             "it in order, about seventy seconds per column. Do not explain the individual terms. Say plainly "
             "that nobody expects them to know what a transformer is today.")

    s = s_prose(prs, "Stage 2 is the one that matters to you", [
        "**You already have the mathematics**",
        "The roadmap puts calculus, linear algebra, statistics and probability as a major stage — for most "
        "people entering this field from computing, it is the hardest one.",
        "You did it in Years 1 and 2. Derivatives, matrices, distributions, hypothesis tests. You are not "
        "starting from zero on the roadmap; you are starting from stage 3 with stage 2 already behind you.",
        "**What you are missing is the programming, and that is the easier half**",
        "Stages 1 and 3 — Python and the data libraries — are five weeks of work. The mathematics took "
        "you two years; Weeks 2 to 6 cover the five.",
        "**Which is why an engineer is well placed here**",
        "The people who struggle in this field are usually strong programmers with no domain knowledge and "
        "shaky mathematics. You are the reverse, and the reverse is more useful.",
        "An engineer who can do this in their own discipline is rarer, and harder to replace, than a "
        "generalist who can do it in none."],
        kicker="WHERE YOU ALREADY ARE")
    notes(s, "The mathematics stage — calculus, linear algebra, statistics, probability — is the one most "
             "people entering this field find hardest, and you did it in Years 1 and 2. What you are missing is "
             "stages 1 and 3, Python and the data libraries, which Weeks 2 to 6 cover in five weeks of work. "
             "The expensive prerequisite is already behind you.\n\nTO TEACH: this slide exists to counter the "
             "belief that machine learning belongs to computer scientists. Say directly that the hard "
             "prerequisite for the field is the mathematics and they have already done it. Watch the room "
             "change posture.")

    s = s_figure(prs, "Where this course sits, honestly", f("roadmap_coverage.png"),
                 "The grey is what we do not teach. Reinforcement learning, full MLOps and most of the "
                 "advanced language-model material are outside this course. I would rather you knew that now "
                 "than discovered it in December.",
                 kicker="COVERAGE")
    notes(s, "The grey stages sit outside this course: reinforcement learning, full MLOps and most of the "
             "advanced language-model material. If you want to go after them later, roadmap.sh publishes "
             "separate roadmaps for the AI engineer, the data scientist, MLOps and AI agents, and any of the "
             "four is a reasonable next step after December.")

    s = s_figure(prs, "Four jobs this field splits into", f("career_paths.png"),
                 "These are four different roadmaps and four different careers. This course points at the "
                 "first one, applied inside your own engineering discipline — which is a narrower and more "
                 "defensible position than competing with computer science graduates on general machine "
                 "learning.",
                 kicker="WHERE IT LEADS")
    notes(s, "Four different roadmaps and four different careers. This course points at the first one, applied "
             "inside your own engineering discipline. A computer science graduate will beat you at general "
             "machine learning, and that contest is avoidable: a civil engineer who can model concrete "
             "strength, or a mining engineer who can predict concentrate quality, is competing in a much "
             "smaller field.\n\nTO TEACH: expect the question 'what job does this get me?'. Answer it here "
             "rather than deflecting it to later in the semester.")

    # ============================================ SEGMENT 2
    s = s_segment(prs, 3, NSEG, "What this course is actually about", 15,
                  "Three words people use interchangeably and should not — and where engineering sits among "
                  "them.")
    notes(s, "Three words — artificial intelligence, machine learning, data science — get used interchangeably "
             "in job adverts, papers and vendor brochures. Fifteen minutes here is what lets you read those "
             "documents without being misled by them.\n\nTO TEACH: keep it tight and move to the real work in "
             "the block on rules and learning.")

    s = s_figure(prs, "The words, and how they nest", f("nested_ai.png"),
                 "Each is contained by the one before it. Data science is the odd one out: it overlaps all of "
                 "them and is contained by none, because it is the craft of getting an answer out of data at "
                 "all — finding it, cleaning it, questioning it, presenting it.",
                 kicker="LANGUAGE")
    notes(s, "Each term is contained by the one before it. Data science is the odd one out: it overlaps all of "
             "them and is contained by none, because it is the craft of getting an answer out of data at all — "
             "finding it, cleaning it, questioning it, presenting it. Most of your semester goes into the data "
             "science ring, and the modelling turns out to be the small part.\n\nTO TEACH: draw this on the "
             "board as well as showing it. Drawn beats projected for a nested diagram.")

    s = s_define(prs, "Artificial intelligence",
                 "Any machine doing something we would call intelligent. It names a goal. Many different "
                 "techniques aim at it.",
                 "A chess engine is AI. So is a spam filter. A thermostat is not — it follows one fixed rule "
                 "with no notion of doing better.",
                 "Machine learning, which is one particular way of achieving AI. All machine learning is AI; "
                 "most AI historically was not machine learning.")
    notes(s, "A thermostat follows one fixed rule and has no capacity to do better, which puts it outside the "
             "definition. A spam filter that improves as it sees more mail sits inside it. Whether any of this "
             "is 'really' intelligent is a genuine open question in the field; here the word is a label for an "
             "area of work.")

    s = s_define(prs, "Machine learning",
                 "Getting a computer to work out a rule from examples, instead of you writing the rule yourself.",
                 "You show it " + c["ml_eg"] + ". It infers a relationship. You then decide whether to trust it.",
                 "Automation. A script that emails a report every Monday is automation and there is no learning "
                 "in it at all.")
    notes(s, "This is the definition the rest of the course rests on. Note the last step of the example: the "
             "computer infers a relationship and you then decide whether to trust it. That step is the easy one "
             "to skip, and Weeks 10 to 14 are entirely about it.\n\nTO TEACH: write the definition on the board "
             "and leave it there for the whole session.")

    s = s_define(prs, "Data science",
                 "The craft of getting a trustworthy answer out of data — finding it, cleaning it, questioning "
                 "it, analysing it and presenting it so somebody can act.",
                 "Discovering that a third of your " + c["recname"] + " are missing, working out whether they are "
                 "missing at random, and deciding what that does to your conclusion. No model involved.",
                 "Machine learning. You will spend far more of this semester on data science than on machine "
                 "learning, and that ratio matches professional practice.")
    notes(s, "In industry the split is roughly eighty per cent getting data into a usable state and twenty per "
             "cent modelling. An engineer with clean data beats a better algorithm with dirty data. The "
             "missing-assay example on this slide is a real Week 6 exercise: you will be handed records with a "
             "large part of one column absent and asked whether they are missing at random and what that does "
             "to your conclusion.\n\nTO TEACH: expect pushback here — they want the models. Give the "
             "eighty-twenty split honestly and move on.")

    # ============================================ SEGMENT 3
    s = s_segment(prs, 4, NSEG, "Two ways to make a computer decide", 25,
                  "The actual idea of the course, and the vocabulary you need to talk about data.")
    notes(s, "The core teaching segment of the session: the difference between writing a rule and inferring one "
             "from examples, plus the vocabulary for talking about a table of data. Everything from Week 5 "
             "onwards assumes both.\n\nTO TEACH: if you are running out of time elsewhere, protect this "
             "segment.")

    s = s_question(prs, "THE QUESTION THIS COURSE STARTS FROM", '"' + c["q"] + '"',
                   "Hold onto that question. In twenty minutes you are going to answer a version of it "
                   "yourself, on paper, with no computer and no formula.")
    notes(s, "Sit with the question before any answer arrives. Two honest first reactions are 'you cannot' and "
             "'there must be a formula somewhere', and both are useful. The hands-on prediction exercise shows "
             "what a third answer looks like.\n\nTO TEACH: ask the room how they would answer it today, then do "
             "not resolve it. The paper exercise resolves it.")

    s = s_figure(prs, "Traditional programming, and machine learning", f("rules_vs_learning.png"),
                 "On the left, the way you already know: you work out the rule and write it down. On the "
                 "right, the new way: you do not know the rule, but you have examples of inputs and the "
                 "answers that followed, and the computer works out a rule from them.",
                 kicker="THE ACTUAL IDEA")
    notes(s, "A worked case from your own discipline: " + c["rule_eg"] + " — " + c["rule_why"] + " That "
             "belongs firmly in the left-hand column. The right-hand column earns its place when there is no "
             "threshold in any code of practice and no formula to look up, and you have examples of past cases "
             "instead. Neither column is better; the useful question is whether you already know the rule for "
             "the problem in front of you.\n\nTO TEACH: walk the two columns slowly, left then right, then give "
             "the domain example. If a student asks which is better, ask them for a problem where they know the "
             "rule and one where they do not.")

    s = s_prose(prs, "When to write the rule, and when to learn it from data", [
        "**Write the rule yourself when…**",
        "A code of practice, a datasheet or a validated equation already gives you the answer.",
        "The relationship is simple and well understood.",
        "You must be able to explain the decision to a client or a regulator line by line.",
        "You have little or no historical data.",
        "**Let the computer infer the rule when…**",
        "Nobody knows the rule, or it involves many variables interacting.",
        "You have a reasonable quantity of past examples where you know both the inputs and the outcome.",
        "An approximate answer now is worth more than an exact answer later — which is exactly the case in "
        "the question we opened with.",
        "You can test the inferred rule against cases it has never seen."],
        kicker="CHOOSING")
    notes(s, "Most of engineering stays in the left-hand column and that is the correct place for it. The third "
             "item on the left is the one that decides real projects: a model whose decision cannot be "
             "explained line by line often cannot be used at all, whatever its accuracy on test data. That "
             "constraint returns in Week 12.\n\nTO TEACH: say out loud that most of engineering stays in the "
             "left-hand column. It protects you from the charge of selling a technique.")

    s = s_figure(prs, "What we actually mean by 'data'", f("data_table_" + code + ".png"),
                 "This is the single most important picture in today's session. Every dataset you meet this "
                 "semester has this shape: one row per example, feature columns for what you know beforehand, "
                 "and one target column for the thing you want to predict.",
                 kicker="THE VOCABULARY")
    notes(s, "This is the picture to fix in your head, because every dataset you meet this semester has this "
             "shape. One row is one example. The feature columns hold what you know beforehand and the target "
             "column holds the thing you want to predict. Worth thinking about: the target of one problem can "
             "be a feature of another. Curing temperature is the target if you are studying an oven and a "
             "feature if you are predicting strength.\n\nTO TEACH: five minutes here at least. Point at the "
             "table and ask individual students 'feature or target?' four or five times until the answers come "
             "back quickly, then put the harder question about targets becoming features.")

    s = s_define(prs, "Feature, and target",
                 "A FEATURE is a column you know before the outcome — an input. The TARGET is the column you "
                 "want to predict. One row containing all of them is one EXAMPLE.",
                 "In the table you just saw, " + c["tabfeat"] + " are the features. " + c["tgt"].capitalize() +
                 " is the target.",
                 c["cause"])
    notes(s, "The 'association is not a cause' line is the seed of correlation versus causation, which arrives "
             "properly in Week 8. One error to start watching for now: including a column that is only known "
             "after the target is known. That is data leakage, it is the most destructive mistake in applied "
             "machine learning, and Week 10 is a full session on it.\n\nTO TEACH: plant the causation point in "
             "one sentence and do not develop it here.")

    s = s_check(prs, [
        "In a table of " + c["dataset"] + " records, is " + c["tgt"] + " a feature or the target?",
        "You want to predict how long a pump will run before it fails. You have a column recording the repair "
        "that was carried out afterwards. Should it be a feature? Why or why not?",
        "Give one example from your own discipline of a problem where you already know the rule, so machine "
        "learning would be the wrong tool."])
    notes(s, "Write something for each of the three before you turn to the answers. Question B is deliberately "
             "hard for Week 1 — noticing that the repair column can only be filled in after the failure has "
             "happened is enough at this stage, even if you cannot yet name what is wrong with using it.\n\nTO "
             "TEACH: ninety seconds in pairs before you reveal, and do not take an answer aloud immediately. "
             "Accept any answer to B that notices the timing problem.")

    s = s_answers(prs, [
        ("Feature or target?",
         "The target. It is the thing you want to predict. Everything measured beforehand is a feature."),
        ("The repair column?",
         "No. You only know what repair was done AFTER the failure, so it cannot help you predict the failure. "
         "Include it and your model will look brilliant in testing and be useless in service. This is called "
         "data leakage and we spend a whole session on it in Week 10."),
        ("A rule you already know?",
         "Anything with a formula or a code threshold: " + c["lim_physics"] + " If a validated equation "
         "exists, use the equation.")])
    notes(s, "Getting B wrong is normal; professional teams ship this bug regularly and only find it when the "
             "model reaches service. The name for it is data leakage. The timing test in answer B — could I "
             "know this column before the outcome? — is the one habit to carry out of this slide.\n\nTO TEACH: "
             "write 'data leakage' on the board and tell them it will come back in Week 10.")

    # ============================================ SEGMENT 4
    s = s_segment(prs, 5, NSEG, "Hands on: predict case 13", 25,
                  "You are going to do machine learning by hand, on paper, before anybody writes a line of "
                  "code. Teams of four or five — form them now.")
    notes(s, "Teams of four or five, formed now and kept for the rest of the semester. You are about to do "
             "machine learning by hand, on paper, before anybody writes a line of code.\n\nTO TEACH: form teams "
             "HERE and keep them all semester. Mix by ability rather than friendship — use the Week 1 survey if "
             "you have it, otherwise count off around the room. Hand out the printed 12-row extracts now, one "
             "per team, plus a blank sheet.")

    s = s_figure(prs, "Your task", f("hand_pred_before_" + code + ".png"),
                 "Twelve cases, each with its features and its known outcome. Case 13 has features but the "
                 "outcome is hidden. In your team: predict it, write the number down, and write one sentence "
                 "saying how you decided. Fifteen minutes.",
                 kicker="TEAM TASK · 15 MINUTES")
    notes(s, "The number your team predicts matters far less than the sentence saying how you got it, so write "
             "the reasoning down. The next three slides give names to whatever method you used, and that only "
             "works if you can still see what you did. If you are stuck, start with one question: which single "
             "column seems to move with the outcome, and why that one?\n\nTO TEACH: circulate and ask 'why that "
             "number?' Do not help. If a team is stuck, ask which column they think matters most. Some teams "
             "will average everything and some will spot the trend; you contrast the two afterwards.")

    s = s_worked(prs, "Reading the pattern from twelve cases",
                 "There is no single right method. This is one line of thinking that works, and it is close "
                 "to what most teams arrive at.",
                 ["Look down the columns and ask which one seems to move with the outcome. Ignore the others "
                  "for now.",
                  "Find the two cases whose value of that column sits either side of case 13's value.",
                  "Look at their outcomes. Case 13's answer is probably between them.",
                  "Adjust for anything else you noticed — a second column that also seems to matter.",
                  "Write the number down, and write why. Then ask: how confident am I, and what would change "
                  "my mind?"],
                 "That is genuinely the whole idea. You found a pattern in examples and used it on a case you "
                 "had never seen — which is exactly what every algorithm in this course does.")
    notes(s, "There is no single right method, and this is one line of thinking that works. Step five is what "
             "separates an engineer from a calculator: how confident am I, and what would change my mind? The "
             "two practical tests, in Weeks 7 and 14, assess that step far more heavily than the "
             "arithmetic.\n\nTO TEACH: show this AFTER they have tried, never before. Handing them the method "
             "first destroys the exercise.")

    s = s_figure(prs, "The answer, and your error", f("hand_pred_after_" + code + ".png"),
                 "The star is the true value. The distance between your guess and the star is your ERROR — and "
                 "measuring that distance honestly is what most of this course is about. The dashed line is "
                 "the pattern you were sensing without being able to write it down.",
                 kicker="THE REVEAL")
    notes(s, "The spread of team answers is the teaching point. Several different reasonable methods produced "
             "several different numbers, so being reasonable is not enough on its own — you need a way to "
             "measure which method is better. One case cannot tell you that, which is what Week 8 sets "
             "up.\n\nTO TEACH: collect every team's number on the board before revealing. Then reveal, ask the "
             "closest team to explain their method, and ask whether that method would still be best on a "
             "different case. Usually nobody knows, and that is the honest answer.")

    s = s_prose(prs, "You just did every step of a machine learning project", [
        "**What you called it**", "You looked at the table.",
        "You noticed which columns seemed to matter.",
        "You worked out a rough rule in your head.",
        "You applied it to a case you had not seen.",
        "You compared your answer with the truth.",
        "**What it is called**",
        "You explored the data. That is Weeks 5 and 6.",
        "You selected features. That is Week 11.",
        "You fitted a model. That is Week 8.",
        "You predicted on unseen data — the single most important idea in the course. Week 8 and Week 10.",
        "You evaluated the error. That is Week 10, and it is where engineers earn their keep."],
        kicker="NAMING IT")
    notes(s, "The syllabus for the rest of the semester is largely a set of names for what you just did with a "
             "pencil. The fourth pair is the one to dwell on: you predicted a case that was not in front of you "
             "when you formed the rule. That is generalisation, and everything in Week 10 follows from "
             "it.\n\nTO TEACH: go slowly here. This is the pedagogical payoff of the whole session.")

    s = s_break(prs, 10, after="Nothing after the break needs a computer.")
    notes(s, "Ten minutes. The challenge segment after the break is the longest single working block of the "
             "session, so use the time.\n\nTO TEACH: take the break. Do not skip it to catch up — attention at "
             "ninety minutes is genuinely gone and the challenge segment needs them fresh.")

    # ============================================ SEGMENT 6
    s = s_segment(prs, 7, NSEG, "Two kinds of question", 15,
                  "Predicting a number, and predicting a category. Almost everything in this course is one or "
                  "the other.")
    notes(s, "A short segment carrying one distinction that decides which method you reach for all semester. It "
             "needs to be automatic by Week 8, when you start fitting models to both kinds of problem.")

    s = s_figure(prs, "Regression and classification", f("reg_vs_class_" + code + ".png"),
                 "Left: the answer is a number on a continuous scale, so we fit a line through the cases. "
                 "Right: the answer is one of a small set of labels, so we look for a boundary that separates "
                 "them. The data can be the same; the question is what changes.",
                 kicker="THE TWO SHAPES")
    notes(s, "The point that is easy to miss: the SAME dataset can pose either question. Take the target on "
             "the left and band it — " + c["cls_eg"] + " — and the regression problem has become a "
             "classification problem. Banding is an engineering decision with consequences, because it throws "
             "away the distance between two values inside the same band, and it comes back in Week 9 when you "
             "start choosing how to measure performance.")

    s = s_define(prs, "Regression, and classification",
                 "REGRESSION predicts a number on a continuous scale. CLASSIFICATION predicts which of a "
                 "small number of categories a case belongs to.",
                 "Regression: how many " + c["unit"] + "? Classification: " + c["cls_eg"] + ".",
                 "Each other. Ask 'what would the answer look like written down?' A quantity with a unit means "
                 "regression. A word or a label means classification.")
    notes(s, "Carry the test as a habit: what would the answer look like written down? A quantity with a unit "
             "means regression. A word or a label means classification. That question resolves almost every "
             "case you will meet, and it is faster than trying to remember the definitions.\n\nTO TEACH: drill "
             "it. Call out five problems from their discipline and have the room answer 'number' or 'category' "
             "in unison. Thirty seconds, and it sticks far better than the definition.")

    s = s_check(prs, [
        "You want to predict how many days until a component needs replacing. Regression or classification?",
        "You want to predict whether a sample passes or fails specification. Which one?",
        "You want to predict which of five fault types a machine has. Which one — and what makes it different "
        "from the previous question?"])
    notes(s, "Question C is the interesting one. It is still classification, with five categories rather than "
             "two. Multi-class problems are harder to evaluate because one accuracy figure hides which classes "
             "you are getting wrong, and that is a Week 9 topic.")

    s = s_answers(prs, [
        ("Days until replacement?", "Regression. The answer is a number with a unit — days."),
        ("Pass or fail?", "Classification. Two categories, so it is called binary classification."),
        ("Which of five fault types?",
         "Still classification, but multi-class rather than binary. It is harder: with five classes there are "
         "far more ways to be wrong, and a single accuracy figure hides which ones you get wrong. Week 9.")])
    notes(s, "You now have vocabulary you can use immediately: binary classification for two categories, "
             "multi-class for three or more. The distinction starts to matter as soon as you begin measuring "
             "performance in Week 9, because the same accuracy figure means different things in the two cases.")

    # ============================================ SEGMENT 7
    s = s_segment(prs, 8, NSEG, "What machine learning cannot do", 15,
                  "Four honest limits. This segment is here to protect you from being sold something.")
    notes(s, "Four honest limits, so that you can recognise in advance when data will not help. This is also "
             "your protection against being sold a technique that cannot work on the problem you have.\n\nTO "
             "TEACH: this segment buys credibility for the whole semester. Engineering students are rightly "
             "sceptical of hype, and showing the limits early earns the right to teach the rest.")

    s = s_figure(prs, "Four limits, and none of them go away", f("four_limits.png"),
                 "A machine learning method will always give you an answer. It will never tell you that the "
                 "question was unanswerable. That is your job.",
                 kicker="THE LIMITS")
    notes(s, "The caption is the sentence to remember. A machine learning method will always return an answer "
             "and will never tell you that the question was unanswerable. Judging that is your job, and it is "
             "the reason a trained engineer is still needed after the code runs.\n\nTO TEACH: say the caption "
             "twice. Ask the room for a case from their own experience that hits limit one — somebody always "
             "has a story about records that were never kept.")

    s = s_prose(prs, "The same four limits, in your own discipline", [
        "**1 · No data**", c["lim_nodata"],
        "**2 · No signal**", c["lim_nosignal"],
        "**3 · Physics is better**", c["lim_physics"] + " Do not use a model where an equation will do.",
        "**4 · The future changed**", c["lim_future"],
        "**Why this matters for the rest of the course**",
        "Every project in Week 9 has to survive these four questions before it is approved. A team that "
        "cannot answer them has not defined an engineering problem yet — it has picked a technique and gone "
        "looking for somewhere to use it."],
        kicker="MADE CONCRETE")
    notes(s, "Every project in Week 9 has to survive these four questions before it is approved. A team that "
             "cannot answer them has picked a technique and gone looking for somewhere to use it, which is the "
             "most common way a student project fails.\n\nTO TEACH: read each of the four out and then ask for "
             "one more example from the room; their examples are better than yours because they own them. The "
             "closing paragraph is the project gate, so say it now and Week 9 will not be a surprise.")

    # ============================================ SEGMENT 8
    s = s_segment(prs, 9, NSEG, "Challenge: the Problem Hunt", 30,
                  "You get a problem and no method. I will ask you questions and answer none. This is how "
                  "roughly one segment of every session works.")
    notes(s, "In this segment you get a problem and no method, and the questions you are asked will not be "
             "answered for you. Proceeding without instructions is the skill being practised, and roughly one "
             "segment of every session this semester works this way.\n\nTO TEACH: say out loud that you will "
             "not answer questions in this segment, and why. Carry the printed question card — it is there to "
             "stop YOU giving answers, which is harder than it sounds.")

    s = s_challenge(prs, "Problem Hunt",
                    "In your team, list six problems from " + c["domain"] + " where data might help.\n"
                    "Then sort all six into: predict a NUMBER, predict a CATEGORY, or NOT a machine learning "
                    "problem — and justify every placement, including the rejections.\n"
                    "Thirty minutes. No template, no worked example, no help from me.",
                    ["What are you actually trying to find?",
                     "Who measures that, and how often?",
                     "Would a rule you already know do this better?",
                     "What would the answer let somebody DO?",
                     "How would you know if you were wrong?",
                     "What does a mistake cost here?"])
    notes(s, "The rejections carry more weight than the acceptances. A team that can say clearly why something "
             "is NOT a machine learning problem has understood the session, and the six questions on the slide "
             "are the ones to argue each placement against. Keep your sheet: the class list of problems built "
             "in this segment is what teams draw on when they choose projects in Week 9.\n\nTO TEACH: seed "
             "prompts, only if a team is genuinely stuck: " + " · ".join(c["probes"]) + ". Harvest every board "
             "onto a class list afterwards — students take their own idea far more seriously than one you hand "
             "them.")

    s = s_prose(prs, "How your team works, all semester", [
        "**Teams of four or five, formed today, kept to the end**",
        "You will do two projects together: a data analysis project due Week 8, and the Engineering ML Project "
        "from Week 9 to Week 15.",
        "**Roles rotate at every milestone**",
        "Data analyst · machine learning engineer · domain engineer · documentation lead · presenter. Nobody "
        "does the same job twice, so nobody hides in one role.",
        "**Individual accountability is built in**",
        "Sixty-five per cent of the mark is individual. Your team keeps a contribution log, and it is checked "
        "against the repository history.",
        "In Week 15 every student answers two unseen questions about their own team's work. That is how a team "
        "mark becomes an individual one — you cannot be carried, and you will not be dragged down.",
        "**Sign the team charter before you leave**",
        "Names, contact details, a weekly meeting slot, and what you will do if somebody stops contributing. "
        "Agreeing that now is much easier than agreeing it in November."],
        kicker="TEAMS")
    notes(s, "Sign the team charter before you leave: names, contact details, a weekly meeting slot, and what "
             "you will do if somebody stops contributing. Agreeing that in Week 1 is far easier than agreeing "
             "it in November, and the charter is the document your contribution log gets read against.\n\nTO "
             "TEACH: collect the charters — you need the team list for the Week 9 project registration anyway. "
             "The charter takes five minutes and prevents most of the free-riding complaints that otherwise "
             "arrive in Week 12.")

    # ============================================ SEGMENT 9-10
    s = s_segment(prs, 10, NSEG, "Gallery walk, and what you owe me", 10,
                  "Critique two other teams' boards, then the assignment and the pre-work for next week.")
    notes(s, "Gallery walk: your team visits two other teams' boards and writes one question on each sheet. "
             "Questions only, no verdicts. This is the first peer review of the semester, and in Week 13 peer "
             "review is graded.")

    s = s_split(prs, "Before Week 2", "Assignment A1 — one page, due at the start of Week 2",
                "Three candidate machine learning problems from your own discipline.\n\n"
                "For each one: what data it would need, and where that data might actually come from — who "
                "measures it, how often, and whether anyone has kept it.\n\n"
                "One of the three must be a problem you think is NOT solvable with the data that exists. Say "
                "why.\n\nMarked pass or redo. What is being checked is engagement.",
                "Also before next week",
                ["Create a GitHub account.",
                 "Create a Google account if you",
                 "do not have one — we work in",
                 "Google Colab from Week 2.",
                 "",
                 "Watch the video on the next slide.",
                 "",
                 "Do NOT install anything.",
                 "Week 2 needs a browser only.",
                 "",
                 "Sign and hand in your team charter."],
                kicker="ASSIGNMENT")
    notes(s, "The 'not solvable' item is the most valuable part of A1, because it forces you to use the four "
             "limits rather than remember them. Take the instruction not to install anything seriously: the "
             "course runs in Google Colab, and a Python installation you set up at home creates a problem that "
             "cannot be diagnosed in class.\n\nTO TEACH: collect the paper laptop-access survey before they "
             "leave. Paper gets a 100 per cent return; a form does not.")

    s = s_video(prs, "Watch this before Week 2", "IBM Technology",
                "AI, Machine Learning, Deep Learning and Generative AI Explained",
                "https://www.youtube.com/watch?v=qYNweeDHiyU", "under 10 minutes",
                "Watch for where he draws the boundaries between the four terms, and whether they match the "
                "nested diagram we drew today. If they differ, raise it next week — the field genuinely does "
                "not fully agree on this.",
                "PRE-WORK")
    notes(s, "Watch for where he draws the boundaries between the four terms, and whether they match the nested "
             "diagram from today. If they differ, raise it next week — the field genuinely does not fully agree "
             "on this. Two optional extras: StatQuest, 'A Gentle Introduction to Machine Learning', "
             "https://www.youtube.com/watch?v=Gv9_4yMHFhI, whose author Josh Starmer is the spine of Weeks 8 to "
             "12; and if you have ninety seconds only, Fireship, 'Machine Learning Explained in 100 Seconds', "
             "https://www.youtube.com/watch?v=PeMlggyqz0Y\n\nTO TEACH: link verified as existing on 7 September "
             "2026. The runtime was not stated in the source, so check it and write it on the slide before you "
             "issue the deck.")

    # ============================================ REVISION SECTION
    s = s_segment(prs, 11, NSEG, "Revision material", 5,
                  "Everything from here on is for you to study from. Summary, self-test with answers, "
                  "glossary and a one-page reference.")
    notes(s, "Everything from here on is revision material rather than presented content: a summary, a "
             "self-test with worked answers, an eighteen-term glossary and a one-page reference sheet. It is "
             "written to be studied from in your own time.\n\nTO TEACH: tell them explicitly that the deck "
             "continues past the end of the session. Students do not read past the last slide you present "
             "unless told to.")

    s = s_summary(prs, [
        "Artificial intelligence is a goal; machine learning is one way of reaching it; data science is the "
        "craft of getting a trustworthy answer out of data at all.",
        "In traditional programming you write the rule. In machine learning you supply examples and the "
        "computer infers the rule — and you then have to decide whether to trust it.",
        "Every dataset has the same shape: one row per example, feature columns known beforehand, one target "
        "column you want to predict.",
        "Regression predicts a number with a unit. Classification predicts which of a small set of categories "
        "a case belongs to. The same data can pose either question.",
        "A model learns association. It does not learn cause, and a good fit is no evidence of a "
        "mechanism.",
        "Four limits never go away: no data, no signal, physics is simply better, and the future stopped "
        "resembling the past.",
        "A method will always give you an answer. It will never tell you the question was unanswerable — "
        "that judgement is the engineer's job, and it is what this course is really training."])
    notes(s, "Seven statements covering the whole session. If any of them reads as new to you, go back to the "
             "slide it came from before Week 2 rather than after it.\n\nTO TEACH: come back to the learning "
             "objectives slide after this and ask for a show of hands against each. Ninety seconds, and it "
             "converts a long session into visible progress.")

    s = s_check(prs, [
        "A colleague says 'we should use AI for this'. What three questions would you ask before agreeing?",
        "You have a table of 500 past pump repairs. Which columns are features and which is the target — and "
        "what tells you?",
        "Give one problem from your discipline that is regression, and one that is classification.",
        "Why is a very good fit on data the model has already seen NOT evidence that the model is any good?",
        "Your model predicts " + c["num_tgt"] + " to within a few " + c["num_unit"] + ". Name one thing "
        "you would still need to know before acting on it."],
        title="Self-test — try these before you look",
        foot="Answers on the next slide. Do not look until you have written something for each.")
    notes(s, "Optional revision, best attempted with a pencil before you look at the next slide. Question D is "
             "a Week 10 idea planted early: anything that notices the circularity of testing a model on cases "
             "it has already seen is a good answer at this stage.")

    s = s_answers(prs, [
        ("Three questions before agreeing to 'use AI'?",
         "What exactly are we predicting? What data exists, who measured it, and is it kept? And would a rule "
         "or an equation we already have do this better? If any of those has no answer, stop."),
        ("Features and target in a repair table?",
         "The target is whatever you want to predict — say time to next failure. Features are everything known "
         "BEFORE that: operating hours, load, temperature. The test is timing: anything only known afterwards "
         "cannot be a feature."),
        ("One of each from your discipline?",
         "Regression: any quantity with a unit — " + c["num_tgt"] + " in " + c["num_unit"] + ". "
         "Classification: " + c["cls_eg"] + "."),
        ("Why is a good fit on seen data not evidence?",
         "Because the model could simply have memorised those cases. The only honest test is performance on "
         "examples it has never seen — exactly what you did with case 13. This is the whole subject of Week 10."),
        ("What else before acting?",
         "How large the error is in engineering terms and whether that is tolerable; what it costs when the "
         "model is wrong; and whether today's conditions still resemble the data it learned from.")])
    notes(s, "Answer D is the most important idea in the course. A model can simply memorise the cases it was "
             "shown, so good performance on those cases is no evidence of anything. The only honest test is "
             "data the model has never seen, which is exactly what case 13 was for you.")

    s = s_glossary(prs, [
        ("Artificial intelligence", "Any machine doing something we would call intelligent. A goal that "
                                     "many techniques aim at."),
        ("Machine learning", "Inferring a rule from examples instead of writing it yourself."),
        ("Deep learning", "Machine learning using large neural networks. Semester 2."),
        ("Data science", "The craft of getting a trustworthy answer out of data — finding, cleaning, "
                         "questioning, analysing, presenting."),
        ("Dataset", "A table of past cases you can learn from."),
        ("Example (or row, or observation)", "One case: all its features plus its known outcome."),
        ("Feature", "A column known before the outcome. An input to the prediction."),
        ("Target (or label)", "The column you are trying to predict."),
        ("Regression", "Predicting a number on a continuous scale."),
        ("Classification", "Predicting which of a small set of categories a case belongs to."),
        ("Binary classification", "Classification with exactly two categories, such as pass or fail."),
        ("Multi-class classification", "Classification with three or more categories."),
        ("Prediction", "The model's answer for a case."),
        ("Error", "The distance between the prediction and the truth. Measuring it honestly is most of this "
                  "course."),
        ("Unseen data", "Cases the model was not shown while it was learning. The only fair test."),
        ("Data leakage", "Accidentally giving the model information it would not have in real use — usually "
                         "something only known after the outcome. Week 10."),
        ("Generalisation", "Whether a rule learned from past cases still works on new ones."),
        ("Association vs cause", "A model learns which columns move together. It knows nothing about "
                                 "mechanism.")],
        page="1 of 1")
    notes(s, "Eighteen terms. If you can define all eighteen by Week 3 you are ahead of the schedule, and these "
             "exact words appear in the weekly quizzes. The last two entries, generalisation and association "
             "versus cause, are forward references; they are printed here so the words are familiar when they "
             "arrive properly in Weeks 8 and 10.\n\nTO TEACH: do not teach the last two entries today.")

    s = s_prose(prs, "Eight questions to ask about any data problem", [
        "**1 · What exactly am I predicting?**",
        "Name the target column and its unit. If you cannot, you do not have a problem yet.",
        "**2 · Is it a number or a category?**",
        "What would the answer look like written down? A quantity with a unit means regression; a word means "
        "classification.",
        "**3 · What do I know beforehand?**",
        "List the features. Check every one: would I really have this before the outcome?",
        "**4 · Where does the data come from?**",
        "Who measured it, how often, over what period, and is it actually kept anywhere?",
        "**5 · Would a rule or an equation do this better?**",
        "If a code of practice or a validated formula answers it, use that instead.",
        "**6 · How will I know if I am wrong?**",
        "You need cases the model has never seen. Decide now how you will hold some back.",
        "**7 · What does being wrong cost?**",
        "A false alarm and a missed failure are not equally bad. That asymmetry decides which model you pick.",
        "**8 · Do today's conditions still resemble the data?**",
        "If the process, material or plant has changed, the model may be quietly obsolete."],
        kicker="CHEAT SHEET — KEEP THIS SLIDE")
    notes(s, "These eight questions are the spine of the whole course. Every project milestone from Week 9 "
             "onwards is assessed against some subset of them, and this is the page worth having in front of "
             "you in the Week 14 practical test.\n\nTO TEACH: tell students to photograph this slide.")

    s = s_quiz(prs, 1,
               "Features and target read off a table, regression told from classification, and one of the four "
                        "limits applied to a case.", qr_path=qrp(code, 1))
    notes(s, "The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.\n\nNothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.\n\nTO TEACH: open the Form, project the QR, and give it exactly five minutes. Afterwards look at the responses-by-question view — any question most of the room got wrong is next week's five-minute reteach.")

    s = s_closing(prs, "You have already done\nmachine learning once.",
                  "You answered a real engineering question today with a pencil and twelve rows of data, and "
                  "you measured your own error. Everything else this semester is making that faster, more "
                  "reliable, and honest about what it does not know.",
                  "Next week: Colab, notebooks and version control — where the work actually happens. "
                  "Bring a browser; you will install nothing.")
    notes(s, "Before next week: A1 due at the start of the session, a GitHub account and a Google account "
             "created, the video watched, and nothing installed. Week 2 needs a browser and nothing else.\n\nTO "
             "TEACH: close on the promise you opened with, then repeat the four practical instructions. Stay "
             "behind for ten minutes — the students who need the most help will not ask in front of the room.")

    name = f"{code}_Week01_{c['short']}.pptx"
    prs.save(os.path.join(OUTDIR, name))
    return name, len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for code in CO:
        n, cnt = build(code)
        print(f"  {n}  ({cnt} slides)")

    import json
    from pptxkit import LECTURER
    path = _ROOT + "/data/lecturer_notes_" + __file__.split("/")[-1].replace(".py", ".json")
    json.dump(LECTURER, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  {len(LECTURER)} lecturer notes -> {path.split('/')[-1]}")
