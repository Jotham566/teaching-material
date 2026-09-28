# Instructor setup and first class checklist

Prepare the environment before learner arrival rather than spending the first lesson downloading many tools. No learner account is required for the local route. Do not promise public publishing or mandatory AI accounts.

## Python environment for both tracks

Use a supported Python version with the tested dependencies recorded in requirements-tested.txt. Create a dedicated virtual environment; do not modify a learner's unrelated Python installation. The following commands are for the instructor, who explains each action and adapts the Python executable to the machine.

Windows PowerShell, in the extracted student folder:

```
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-tested.txt
.venv\Scripts\python -m notebook
```

macOS Terminal, in the extracted student folder:

```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-tested.txt
.venv/bin/python -m notebook
```

If Python is not present, install it from https://www.python.org/downloads/ using the device owner's permission and the correct operating-system build. The command line is not assumed learner knowledge: show the app, folder, command and result separately. Explain that pip installs dependencies, a virtual environment keeps them separate, and Jupyter opens a local notebook interface. Official Jupyter guidance: https://jupyter.org/install . Prepare the dependencies while internet is available. The supplied data and notebooks then run locally.

Preflight ML01, ML07, ML11, ML15 and ML16 from a clean kernel on every device type. Confirm data is beside notebooks, plots render, CSV writes succeed and a saved notebook reopens. Pin a tested environment for the intake; do not blindly upgrade halfway through the course.

## Data Analysis

Use the Python/Jupyter environment above for DA as well as ML. Test DA01, DA07, DA11 and DA12 from a fresh kernel. pandas handles tables; matplotlib handles charts. No Excel or pivot-table setup is required. The shared tested environment includes scikit-learn for ML; explain that DA does not need to use it.

Install DB Browser for SQLite from https://sqlitebrowser.org/dl/ before DA13. Demonstrate Open Database, Execute SQL, saving a query as .sql and exporting its result as CSV using the installed version. DA13–DA17 SQL examples run in DB Browser, not a Python code cell. DA18 uses pandas to read the exported results.csv and compare by-item totals; category totals are checked against the overall revenue because camp_shop.csv has no category column. Do not require an untaught pandas merge. Keep the existing row labels and money units visible during comparison.

Teach Python first. If students need more time with loops or indexing, use the next class’s opening repair period and reduce optional chart variations. Keep the final project to three taught questions and a few clear charts. No interactive dashboard, web deployment or GitHub account is required.

## Every class

Open the student sheet and corresponding private instructor guide. Run the example before learners arrive. Write the three new terms and the expected output on the board. Have the previous session's repair task ready. Confirm each learner can save a file. During practice visit all five learners. Finish with a saved artifact and one explanation from each student. Track complete/needs repair/absent privately. Keep a backup of teaching files and student work only in the agreed location.

## Assessment operations

References include numeric data summaries, SQL and an ML checkpoint implementation. They are not an upload service or a complete autograder. The organiser must choose and rehearse the collection and grading workflow before it is promised to parents. Use the short common rubrics for explanations and demonstrations; do not copy university roster identifiers or gradebook rules into this camp.

## Added ML foundation labs

Follow teaching/FOUNDATION_LABS.md. Teach F01 after ML03, F02 after ML06, F03 after ML09 and F04 after ML12 on the fourth day of each of weeks 1–4. Each lab proposes two hours including a break. Check the learner can explain and reproduce the evidence before advancing. No previous Python or advanced mathematics is an entry requirement. Every learner brings their own laptop and charger; check it before enrolment.

## Responsible AI literacy

Teach teaching/AI_USE_POLICY.md in Session 1. Disable generative suggestions for weeks 1–6 and all core independent exercises. Before Session 21, rehearse teaching/AI_CODING_ASSISTANTS_LAB.md and check learner readiness; use a tutor-controlled local assistant or the labelled teacher-written fallback. Never make an account a prerequisite. Collect the permitted-use log with project evidence. Final explanations and demonstrations must be unaided. No automated AI detector is a grading criterion.
