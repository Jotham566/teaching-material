# -*- coding: utf-8 -*-
"""Three cohort syllabi — one Word document per programme group."""
import sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border
from plan_content import COHORT_META

DIR = _ROOT + "/IUEA_Teaching_Plan/"

# ---------------------------------------------------------------- per-cohort text
SPEC = {
"A": dict(
  file="IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx",
  short="Design & Infrastructure",
  audience="Year 3 Civil Engineering and Architecture",
  hook="Every structure you will ever design generates data — mix designs and cylinder tests, survey and "
       "inspection records, energy meters, sensor arrays on bridges, cost histories from projects that came before "
       "yours. Most of that data is thrown away or filed and never read. This course teaches you to use it.",
  questions=[
    "Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?",
    "Can we predict a building's heating and cooling load from its geometry, orientation and glazing before it is built?",
    "Can we predict which sections of a road will deteriorate first, and inspect those first?",
    "Can we classify infrastructure defects from inspection records more consistently than three different inspectors do?",
  ],
  outcomes=[
    "Frame a problem in construction, structures, materials or building performance as a machine learning task, and "
    "recognise the problems for which machine learning is the wrong tool.",
    "Load, clean, analyse and visualise engineering datasets such as mix designs, building performance records and "
    "inspection logs, and state honestly what the data cannot tell you.",
    "Build, validate and interpret regression and classification models on infrastructure and building data, "
    "reporting error in engineering units such as megapascals or kilowatt-hours per square metre.",
    "Construct features from civil and architectural domain knowledge — the water-to-cement ratio, the "
    "window-to-wall ratio, degree-days — and demonstrate whether they improved the model.",
    "Judge whether a model is fit to inform a design or maintenance decision, and state the conditions under which "
    "it should not be used.",
    "Work in a team, in a version-controlled repository, and communicate a data-driven result to an engineer who is "
    "not a specialist.",
    "Use AI coding assistants productively, and explain and verify everything they produce.",
  ],
  projects=[
    "Building Energy Predictor — predict consumption from size, orientation, glazing, materials and occupancy",
    "Concrete Strength Estimator with a stated confidence range",
    "Pavement or road deterioration forecast",
    "Construction cost estimator from historical project data",
    "Infrastructure defect classifier from inspection records",
    "Design option screener — rank design variants on a predicted performance measure",
  ],
  datasets="Concrete Compressive Strength (UCI Machine Learning Repository, dataset 165, CC BY 4.0) and Energy "
           "Efficiency (UCI dataset 242, CC BY 4.0) are the anchor datasets and recur through the semester. "
           "Additional construction, building performance and predictive maintenance datasets are introduced for "
           "classification work and for projects.",
),
"B": dict(
  file="IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx",
  short="Mining & Petroleum",
  audience="Year 3 Petroleum Engineering and Mining Engineering",
  hook="Mining and petroleum operations are among the most heavily instrumented industrial systems in the world. "
       "Assay laboratories, well logs, flotation circuits, drill rigs and haulage fleets generate measurements "
       "continuously — and the decisions they inform are often made hours later, from a sample of that data, by "
       "hand. This course teaches you to use the rest of it.",
  questions=[
    "The silica assay takes an hour to come back from the laboratory. Can we know it now, from the process "
    "variables we already measure?",
    "Can we predict lithology from the well logs we already have, rather than drilling again?",
    "Can we tell which piece of mining equipment is about to fail, from its own sensor history?",
    "Can we decide ore from waste more cheaply, and quantify what each kind of mistake costs us?",
  ],
  outcomes=[
    "Frame a problem in exploration, ore or reservoir characterisation, production or equipment health as a machine "
    "learning task, and recognise the problems for which machine learning is the wrong tool.",
    "Load, clean, analyse and visualise geoscience and process datasets such as assay registers, well logs, "
    "flotation circuit data and drill logs, and state honestly what the data cannot tell you.",
    "Build, validate and interpret regression and classification models on mining and petroleum data, reporting "
    "error in operational units such as percentage points of silica or a lithology misclassification rate.",
    "Construct features from mining and petroleum domain knowledge — reagent-to-feed ratios, contained metal, "
    "specific energy, cumulative operating hours — and demonstrate whether they improved the model.",
    "Judge whether a model is fit to inform a set-point change, a drilling decision or a maintenance intervention, "
    "and state the conditions under which it should not be used.",
    "Work in a team, in a version-controlled repository, and communicate a data-driven result to an engineer who is "
    "not a specialist.",
    "Use AI coding assistants productively, and explain and verify everything they produce.",
  ],
  projects=[
    "Real-time concentrate quality predictor from process variables",
    "Lithology classifier from well logs",
    "Mining equipment failure risk model from sensor history",
    "Rate-of-penetration analysis and drilling parameter optimiser",
    "Ore or waste classifier with an explicit cost of error",
    "Production decline forecaster",
  ],
  datasets="A teaching subset of the froth flotation process dataset 'Quality Prediction in a Mining Process' "
           "(Kaggle) is the anchor dataset for the mining stream, and a three-well subset of the FORCE 2020 well "
           "log collection (labels CC BY 4.0, log data under the Norwegian Licence for Open Government Data 2.0) "
           "serves the petroleum stream. Additional equipment-health datasets are introduced for classification "
           "work and for projects.",
),
"C": dict(
  file="IUEA_ML_Syllabus_CohortC_Engineering.docx",
  short="Engineering",
  audience="Year 3 Communications, Electrical, Mechatronics and Robotics Engineering",
  hook="You already work with signals and sensors. Every motor, feeder, actuator, radio link and robot you build "
       "produces a stream of measurements, and the conventional response is a threshold alarm that either nuisance-"
       "trips or misses the fault entirely. This course teaches you what else can be done with that stream.",
  questions=[
    "This machine has four sensors on it. It failed last month. Could we have known?",
    "Can we predict a plant's power output from ambient conditions alone, well enough to schedule generation?",
    "Can we tell a real fault from a start-up transient, without a human looking at the trace?",
    "How many false alarms will an operator tolerate before they disable our alarm entirely — and what does that "
    "mean for how we choose a model?",
  ],
  outcomes=[
    "Frame a problem in sensing, energy systems, fault detection, machine health or robotics as a machine learning "
    "task, and recognise the problems for which machine learning is the wrong tool.",
    "Load, clean, analyse and visualise sensor and electrical datasets, including recognising sensor dropouts, "
    "stuck-at values and start-up transients, and state honestly what the data cannot tell you.",
    "Build, validate and interpret regression and classification models on sensor and machine data, reporting error "
    "in engineering units such as megawatts or a missed-failure rate.",
    "Construct features from electrical and mechanical domain knowledge — power from voltage and current, "
    "mechanical power from torque and speed, temperature rise above ambient, rolling statistics of a signal — and "
    "demonstrate whether they improved the model.",
    "Judge whether a model is fit to drive an alarm, a maintenance schedule or a control decision, weighing false "
    "alarms against missed failures, and state the conditions under which it should not be used.",
    "Work in a team, in a version-controlled repository, and communicate a data-driven result to an engineer who is "
    "not a specialist.",
    "Use AI coding assistants productively, and explain and verify everything they produce.",
  ],
  projects=[
    "Motor anomaly detector from vibration, temperature, current and speed",
    "Machine failure risk model with an explicit false-alarm budget",
    "Power output or electricity demand forecaster",
    "Electrical fault classifier",
    "Surface or component defect classifier",
    "Sensor health monitor — detecting the instrument rather than the process",
    "Robot state classifier from onboard sensors",
  ],
  datasets="Combined Cycle Power Plant (UCI Machine Learning Repository, dataset 294) and AI4I 2020 Predictive "
           "Maintenance (UCI dataset 601, CC BY 4.0) are the anchor datasets and recur through the semester. "
           "Steel Plates Faults (UCI dataset 198, CC BY 4.0) and real compressor sensor data are introduced for "
           "multi-class and anomaly work.",
),
}

WEEKS = [
 ("1", "Tue 8 / Fri 11 Sep", "The engineering problem that needs data", "Problem Hunt", "A1 · Three problems, one dataset"),
 ("2", "Tue 15 / Fri 18 Sep", "The development environment: Python, VS Code, Jupyter, Git, Kaggle", "Break and Fix", "A2 · Working repository and notebook"),
 ("3", "Tue 22 / Fri 25 Sep", "Python as an engineering calculator", "Wrong Answer Hunt", "A3 · Discipline function library"),
 ("4", "Tue 29 Sep / Fri 2 Oct", "Collections, loops, files and errors", "Investigation Lab 1", "A4 · Reading report and a finding"),
 ("5", "Tue 6 / Fri 9 Oct", "NumPy, pandas, and where data comes from", "Ten Questions, No Help", "A5 · Twelve Questions notebook"),
 ("6", "Tue 13 / Fri 16 Oct", "Dirty data, and seeing it: cleaning through visualisation", "The Outlier Argument", "A6 · Cleaning notebook and data quality statement"),
 ("7", "Tue 20 / Fri 23 Oct", "PRACTICAL TEST 1 — Data Investigation (individual, offline)", "The test itself", "None"),
 ("8", "Tue 27 / Fri 30 Oct", "Learning from data: the first model", "Beat the Baseline", "A7 · Regression with a baseline comparison"),
 ("9", "Tue 3 / Fri 6 Nov", "Classification: predicting a category", "The 97% Trap", "A8 · Classifier and cost table"),
 ("10", "Tue 10 / Fri 13 Nov", "Can I trust this model? Validation and data leakage", "Too Good To Be True", "A9 · Trust Lab and conditions of use"),
 ("11", "Tue 17 / Fri 20 Nov", "Features: where engineering knowledge enters the model", "Domain Advantage", "A10 · Feature dictionary and ablation table"),
 ("12", "Tue 24 / Fri 27 Nov", "Model comparison and engineering judgement", "Choose a Model and Defend It", "A11 · One-page recommendation (in session)"),
 ("13", "Tue 1 / Fri 4 Dec", "Reproducibility, communication and peer review", "Peer review", "Project work only"),
 ("14", "Tue 8 / Fri 11 Dec", "PRACTICAL TEST 2 — End-to-End Engineering ML (individual, offline)", "The test itself", "None"),
 ("15", "Tue 15 / Fri 18 Dec", "Engineering ML Demo Day, viva and reflection", "The viva", "Final submission"),
]

QUIZ_WEEKS = {"1": "Quiz 1", "2": "Quiz 2 · setup check", "3": "Quiz 3", "4": "Quiz 4", "5": "Quiz 5",
              "6": "Quiz 6", "8": "Quiz 7", "9": "Quiz 8", "10": "Quiz 9", "11": "Quiz 10",
              "12": "Quiz 11 · integrative", "13": "Quiz 12 · integrative"}

ASSESS = [
 ["Weekly quizzes", "End of every teaching session: Weeks 1–6 and 8–13", "Individual", "10%",
  "A five-minute quiz of five multiple-choice questions on your phone, reached by a QR code, in the last five "
  "minutes of the session. Auto-marked: you see your score and feedback immediately. Twelve quizzes, 1% each, and "
  "your best ten count. There are no resits; the two dropped scores cover a missed week."],
 ["Practical challenges and assignments", "Weekly, Weeks 1–12", "Individual", "10%",
  "Best 8 of 11. Notebooks and one-pagers pushed to your repository. Auto-marked — you can check your own work "
  "against the visible tests before you submit."],
 ["Data Analysis Project", "Set Week 5, due Week 8", "Team of 4–5", "10%",
  "Cleaned dataset, question-driven analysis, four or more charts, one page of findings. An individual "
  "contribution log is required."],
 ["Practical Test 1 — Data Investigation", "Week 7", "Individual, offline", "15%",
  "Two hours practical plus twenty-five minutes written. An unfamiliar dataset. 40 of the 100 marks are "
  "auto-marked from a structured answers cell; the other 60 are marked by your lecturer."],
 ["Practical Test 2 — End-to-End ML", "Week 14", "Individual, offline", "20%",
  "Two hours practical plus twenty-five minutes written. An unfamiliar dataset. 45 of the 100 marks are "
  "auto-marked; the other 55 are marked by your lecturer."],
 ["Engineering ML Project", "Set Week 9, due Week 15", "Team of 4–5", "25%",
  "Repository, two-page engineering brief, poster. Four graded milestones in Weeks 10, 11, 12 and 13."],
 ["Demonstration, viva and reflection", "Week 15", "Individual", "10%",
  "Six-minute demonstration, two unseen questions on your own work, 500-word reflection."],
]

PROJ_RUBRIC = [
 ["Problem definition", "15", "Is the engineering problem real, specific and bounded, and is the machine learning task correctly derived from it?"],
 ["Data understanding", "15", "Provenance and licence stated, defects found and handled with justification, limitations acknowledged."],
 ["Methodology", "20", "Appropriate models compared under one protocol, inside a pipeline, with choices explained."],
 ["Engineering reasoning", "20", "Does your own discipline visibly enter the work, and is the result discussed as engineering rather than as a score?"],
 ["Validation", "15", "Correct train and test discipline, cross-validation with a reported spread, leakage ruled out, metric justified."],
 ["Communication", "10", "Readable by a non-specialist engineer. Charts answer questions. Uncertainty stated honestly."],
 ["Reproducibility and documentation", "5", "Runs from a clean clone. README, requirements, seeds, AI declaration, contribution log."],
]


def build(key):
    m = COHORT_META[key]
    s = SPEC[key]
    d = new_doc(margin_cm=2.3)
    header_footer(d, f"IUEA Faculty of Engineering · {m['title']} · Semester 1 Syllabus")
    first_page_different(d)

    # ---------------- title
    spacer(d, 30)
    para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
         size=10, bold=True, colour=MID, align=AL.CENTER, after=18)
    para(d, m["title"], size=22, bold=True, colour=NAVY, align=AL.CENTER, after=6)
    p = para(d, f"{m['code']} · COURSE SYLLABUS · SEMESTER 1 · 2026/2027", size=12, bold=True, align=AL.CENTER,
             after=8, before=8)
    _border(p, "top", NAVY_H, 10)
    _border(p, "bottom", NAVY_H, 10)
    spacer(d, 10)

    table(d, ["", ""],
          [["Cohort", f"{m['name']} — {m['programmes']}"],
           ["Level", s["audience"]],
           ["Course code", m["code"]],
           ["Credit / contact hours", "45 contact hours · one 3-hour session per week · 15 study weeks"],
           ["Semester dates", "7 September – 18 December 2026"],
           ["Day, time and room", m["slot"]],
           ["Class size", m["size"]],
           ["Lecturer", "________________________"],
           ["Office hours", "________________________"],
           ["Class channel", "________________________"],
           ["Prerequisites", "None in computing or programming. You are assumed to have your Year 1 and Year 2 "
                             "engineering mathematics and your own discipline's core subjects, and no more."]],
          [24, 76], bold_first=True, band=True, hide_header=True)
    spacer(d, 8)
    para(d, "This syllabus is issued in Week 1 and is the reference document for the semester. Assessment weightings "
            "are subject to confirmation against IUEA regulations.", size=9, italic=True, colour=GREY)

    page_break(d)

    # ---------------- 1 course description
    h1(d, "1. What this course is")
    para(d, s["hook"])
    para(d, "This is a course in machine learning for engineers, not an introductory computing course. It assumes "
            "you have never written a line of code, and it teaches programming from zero — but it teaches it as the "
            "means to an end. Every technical idea in this course arrives as the answer to a question from your own "
            "discipline. Among the questions we will actually work on:")
    for q in s["questions"]:
        quote(d, "“" + q + "”")
    para(d, "By the end of the semester you should be able to say something specific and true: give me an "
            "engineering problem involving data, and I know how to start investigating it. Not “I know Python "
            "syntax” — that is a means, and a perishable one.")

    h2(d, "How the course is taught")
    para(d, "Each week is a single three-hour session, and it is not a three-hour lecture. A typical session runs "
            "roughly thirty to forty-five minutes on the concept, twenty to thirty minutes of live demonstration, "
            "sixty to ninety minutes of hands-on practical work, twenty to thirty minutes on a challenge or "
            "problem you have not been shown how to solve, and a short close on reflection and the week's "
            "deliverable. Some weeks are almost entirely practical. Some are almost entirely challenge.")
    para(d, "You should expect at least one segment every week in which you are given a problem and not given a "
            "method. This is deliberate. In those segments the lecturer will ask you questions rather than answer "
            "yours: what are you trying to find, why that variable, what does that chart actually tell you, how "
            "would you know if you were wrong. You will find this uncomfortable in September. It is the single most "
            "valuable thing the course does.")
    para(d, "Expect roughly three to five hours of work outside class each week — the weekly deliverable, and from "
            "Week 5 onward your project.")

    # ---------------- 2 outcomes
    h1(d, "2. Learning outcomes")
    para(d, "On successful completion of this course you will be able to:")
    table(d, ["#", "Outcome", "Mainly assessed by"],
          [[str(i + 1), o, a] for i, (o, a) in enumerate(zip(s["outcomes"], [
              "Weekly challenges; Project problem definition",
              "Practical Test 1; Data Analysis Project",
              "Practical Test 2; Project methodology and validation",
              "Week 11 assignment; Project engineering reasoning",
              "Practical Test 2 written section; Project validation",
              "Project; Demonstration and peer review",
              "AI-use declaration; viva"]))],
          [5, 66, 29], bold_first=True)

    # ---------------- 3 schedule
    page_break(d)
    h1(d, "3. Weekly schedule")
    para(d, "Dates are given for both the Tuesday and Friday slots; your session is one of the two, and will be "
            "confirmed in Week 1. Weeks 7 and 14 are the designated assessment weeks.")
    table(d, ["Wk", "Date", "Topic", "Challenge segment", "Quiz", "Your deliverable"],
          [list(w[:4]) + [QUIZ_WEEKS.get(w[0], "—"), w[4]] for w in WEEKS],
          [4, 14, 33, 17, 14, 22], bold_first=True,
          shade_fn=lambda i, r: RED_H if r[0] in ("7", "14") else (GREEN_H if r[0] == "15" else None))
    spacer(d, 10)
    callout(d, "Note on Week 5",
            "Friday 9 October 2026 is Uganda Independence Day. If your session falls on a Friday you will not meet "
            "in Week 5. The session will instead be provided as a recorded walkthrough and notebook released by "
            "Wednesday 7 October, with an online clinic that week and a consolidation at the start of Week 6 — "
            "unless a make-up session is timetabled, which will be confirmed by Week 2. Week 5 is important; do "
            "not skip the asynchronous package.", "C55A11", AMBER_H)

    # ---------------- 4 assessment
    h1(d, "4. Assessment")
    para(d, "This course has no traditional written examination. It is assessed entirely on what you can actually "
            "do: work with data, write and run code, build and evaluate a model, and explain your reasoning. It is "
            "also continuous: forty per cent of your mark accumulates week by week rather than landing in one or "
            "two large events.")
    table(d, ["Component", "When", "Mode", "Weight", "What you submit"],
          ASSESS, [23, 16, 12, 8, 41], bold_first=True)
    spacer(d, 10)
    para(d, "Sixty-five per cent of the mark is individual. Both practical tests use a dataset you have not seen "
            "before, drawn from your own discipline. There is nothing to memorise for them and no past paper to "
            "revise from. The way to prepare is to do the weekly work, because the weekly challenges and the weekly "
            "quizzes are the rehearsal.")

    h2(d, "The weekly quizzes, and why they exist")
    para(d, "Every teaching session ends with a five-minute quiz. A QR code goes up on the projector in the last "
            "five minutes, you scan it with your phone, you answer five multiple-choice questions, and you get "
            "your score and an explanation of anything you got wrong before you leave the room. There are twelve "
            "of them, one at the end of each teaching session in Weeks 1 to 6 and Weeks 8 to 13, and your best ten "
            "count at one per cent each. Weeks 7 and 14 are the practical tests and Week 15 is Demo Day, so those "
            "three weeks have no quiz. The Week 2 quiz includes one question that asks you to read the output of "
            "your own environment setup, which is how your lecturer finds out early who is not yet running.")
    para(d, "Three things about them are worth knowing in advance. First, they are not memory tests. Every question "
            "shows you code, an output, a chart or a table and asks you to work out what it means or what is wrong "
            "with it, so there is nothing to be gained from memorising definitions the night before. Second, there "
            "are no resits. Only your best ten of the twelve count, so two of them can go badly for any reason at "
            "all, and that is what covers illness, travel and a bad day. Third, if the room network fails, that "
            "week's quiz becomes a 48-hour asynchronous window and you will be told so before you leave the room.")
    para(d, "They exist for two reasons, and it is fair to state both. They give you feedback in minutes instead of "
            "weeks, which is the single biggest complaint students have about any course. And they let a class of "
            "this size be assessed continuously by one lecturer, which would otherwise be impossible — the "
            "alternative is fewer, larger, later assessments, and that is worse for you.")

    h2(d, "How the project is marked")
    para(d, "The project rubric is published here and applied without variation. Note where the marks are: method, "
            "reasoning and validation together carry fifty-five of the hundred marks, and communication and "
            "reproducibility carry fifteen. A model with a mediocre score that you have understood, validated and "
            "honestly reported will out-score a better score you cannot account for.")
    table(d, ["Criterion", "Marks", "What earns them"], PROJ_RUBRIC, [26, 8, 66], bold_first=True)
    spacer(d, 10)
    para(d, "The rubrics for the two practical tests, the Data Analysis Project and the Week 15 demonstration are "
            "published at least one week before each is used. You will never meet a rubric for the first time in "
            "an assessment.")

    h2(d, "Team work and individual accountability")
    para(d, "The two projects are done in teams of four to five, formed in Week 1 and kept for the semester. Roles "
            "— data analyst, machine learning engineer, domain engineer, documentation lead, presenter — rotate at "
            "every milestone, so you will not do the same job twice. Each team keeps a contribution log in its "
            "repository, and it is checked against the commit history.")
    para(d, "In Week 15 every student individually answers two unseen questions about their own team's repository. "
            "This is how a team mark becomes an individual one. If you have not engaged with a part of your team's "
            "work, that will be visible, and the reverse is also true: a strong contributor is not dragged down by "
            "a weak teammate.")

    # ---------------- 5 AI policy
    page_break(d)
    h1(d, "5. Policy on AI coding assistants")
    para(d, "AI coding assistants are permitted and actively taught in this course. You will use them for the rest "
            "of your career and pretending otherwise would be dishonest. What is assessed is not whether you used "
            "one, but whether you understand and can defend what came out.")
    para(d, "There is a quality gradient in how these tools are used, and we will work up it deliberately during "
            "the semester.")
    table(d, ["Level", "What it looks like", "Verdict"],
          [["Poor", "“Write my entire assignment.”",
            "You learn nothing, and you will be unable to answer a single viva question."],
           ["Better", "“Explain why this code is producing this error.”",
            "Legitimate, and where we start in Week 3."],
           ["Good", "“I need to remove missing values from these columns. Here is my code and the error. Explain "
                    "three possible approaches and their trade-offs.” — then you choose and justify.",
            "This is the target for coursework."],
           ["Advanced", "“Review my machine learning pipeline for data leakage and explain any problems you "
                        "identify.” — then you verify the answer yourself.",
            "Introduced in Week 10. The verification is what earns the marks."]],
          [10, 56, 34], bold_first=True)
    spacer(d, 10)
    para(d, "The rules are simple and they are applied consistently. In all coursework, AI assistance is permitted "
            "and must be declared: a short log of the tool, what you asked, and what you changed. In both practical "
            "tests, AI assistance is not available, because the tests run offline with no network access. And in all "
            "circumstances, you are marked on what you can explain. If your submission contains work you cannot "
            "account for, your mark is reduced to the part you can account for.")
    para(d, "The weekly quizzes are the one place where the rule is different, and it is worth being direct "
            "about why. They are taken on your own phone, so nothing stops you looking something up or asking a "
            "neighbour. Three versions are in circulation in the room and the questions require you to read a code "
            "snippet rather than recall a fact, so it is harder than it looks. The real answer is that each "
            "quiz is worth one per cent and it exists to tell you, and me, whether you have kept "
            "up. Thirty-five per cent of your mark sits in the two offline tests. If your quiz scores are "
            "strong and your test scores are not, the quizzes were not doing you any good, and we should talk "
            "before Week 14 rather than after it.")
    callout(d, "Why the tests are offline",
            "Coursework is where you learn to work with these tools and must defend the result. The tests certify "
            "what you can do unaided. Both are worth knowing about you, and they cannot be measured in the same "
            "room. Running the tests offline is also simply enforceable, which a rule against using an assistant on "
            "a networked machine is not.", MID_H, LIGHT_H)

    h2(d, "Academic integrity")
    para(d, "Copying another student's submission, or a public notebook, and presenting it as your own is plagiarism "
            "and is handled under IUEA regulations. Reading a public notebook to learn from it, then writing your "
            "own work and citing what you learned from, is good practice and is encouraged — we will do it together "
            "in Week 5. The distinction is attribution and understanding, and the viva makes the difference "
            "visible.")

    # ---------------- 6 tools & setup
    h1(d, "6. What you need, and what you will learn to use")
    para(d, "You need access to a computer that can run Python, and an internet connection for downloads and for "
            "GitHub. If you do not have a laptop, say so in Week 1: laboratory machines and Google Colab, which "
            "runs in a browser, are both supported, and nobody is excluded for lack of hardware. Bring your laptop "
            "to Week 2 if you have one, charged, with your administrator password known.")
    para(d, "Every tool in this course is introduced by the problem it solves, in this order:")
    table(d, ["Week", "Tool", "The problem it solves"],
          [["1", "GitHub, Kaggle (accounts only)", "Where will my work live, and where will I find data?"],
           ["2", "Python, VS Code, terminal, Jupyter, Git", "Where do I write, run, debug, version and share code?"],
           ["3", "VS Code debugger; AI assistant, first use", "How do I find out what my code is actually doing?"],
           ["4", "Standard-library file reading", "How do I read a data file at all?"],
           ["5", "NumPy, pandas, Kaggle, UCI repository", "How do I work with thousands of measurements — and where "
                                                          "do I find trustworthy data?"],
           ["6", "matplotlib, seaborn", "How do I see my data, and see what is wrong with it?"],
           ["8–12", "scikit-learn", "How do I build a model, check whether to trust it, and choose between models?"],
           ["13", "requirements.txt, repository structure", "How does someone else run my work next year?"]],
          [7, 34, 59], bold_first=True)
    spacer(d, 10)
    para(d, "Deep learning, computer vision, time series, generative AI and deployment are Semester 2. They are "
            "deliberately not in this course. Eight tools learned properly are worth more than twenty met once.")

    h2(d, "Datasets")
    para(d, s["datasets"])
    para(d, "All datasets used in class are staged on the course share, so you do not need to download them during "
            "a session. Every dataset we use is openly licensed, and part of what you will learn is to check that "
            "for yourself before using someone else's data.")

    # ---------------- 7 project
    h1(d, "7. The Engineering ML Project")
    para(d, "The project is set in Week 9 and runs to Week 15, with graded milestones in Weeks 10, 11, 12 and 13, "
            "so it is built continuously rather than in the last fortnight. Your team chooses its own problem, "
            "subject to approval, and finds or is given its own data. Examples of the scope expected:")
    table(d, ["Example project titles for this cohort"], [[p] for p in s["projects"]], [100],
          band=True, font=9)
    spacer(d, 10)
    para(d, "What is being assessed is engineering judgement, not novelty. A well-executed, well-validated, "
            "honestly reported concrete strength predictor is a better project than an ambitious deep learning "
            "attempt that nobody in the team can explain. In Week 15 there are prizes for Best Engineering "
            "Reasoning, Best Investigation and Most Honest Limitations. There is deliberately no prize for the "
            "highest accuracy.")

    # ---------------- 8 expectations
    h1(d, "8. What is expected of you")
    para(d, "Attend. This course is a single three-hour session per week and there is no lecture to catch up from — "
            "the value is in the practical and the challenge, which cannot be read later. If you must miss a "
            "session, tell the lecturer in advance and collect the week's materials from the share.")
    para(d, "Do the weekly deliverable, every week. Eleven small pieces of work spread across twelve weeks is a "
            "manageable load; nine of them attempted in December is not, and the two practical tests will find you "
            "out. The weekly work is the rehearsal for the tests, which is why the best eight of eleven count.")
    para(d, "Ask, but ask well. Bring the error message, what you have already tried, and what you expected to "
            "happen. This is not a hurdle placed in front of help; it is the actual skill, and it is what makes you "
            "employable.")
    para(d, "Struggle before you seek rescue. In the challenge segments you are supposed to be stuck for a while. "
            "Being stuck is not evidence that you cannot do this — it is what doing this feels like, for everyone, "
            "including your lecturer.")

    h2(d, "What you can expect in return")
    para(d, "Every rubric published before the work is set. Every dataset staged so that a slow connection is never "
            "your problem. Feedback on the weekly work within a week. A clear answer when something is genuinely "
            "outside the course's scope, rather than a vague one. And a straight answer to the question “why are we "
            "learning this?”, every time it is asked.")

    spacer(d, 14)
    callout(d, "The one-line version",
            "Problem first. Tools second. Theory when needed. Build continuously. Think for yourself.",
            NAVY_H, LIGHT_H)

    spacer(d, 10)
    para(d, "Syllabus version 1.0 · drafted 1 September 2026 · assessment weightings subject to confirmation "
            "against IUEA regulations.", size=9, italic=True, colour=GREY, align=AL.CENTER)

    out = DIR + s["file"]
    d.save(out)
    print("saved", out)


for k in ("A", "B", "C"):
    build(k)
