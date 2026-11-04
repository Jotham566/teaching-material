# Instructor setup and first class checklist

Prepare the environment before learner arrival rather than spending the first lesson downloading many tools. No learner account is required for the local route. Do not promise public publishing or mandatory AI accounts. The venue is The National ICT Innovation Hub, Nakawa: visit it before the first class, check the room, power points, internet, projector or screen, and seating for five learners and the instructor.

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

Run programme/preflight_stack.py on every device type, including your own. It imports NumPy, pandas, matplotlib, seaborn, scikit-learn and Jupyter and exercises one real function from each; it must print READY. Then preflight ML01, ML07, ML11, ML15 and ML16 and DA01, DA07, DA11, DA14 and DA16 from a clean kernel. Confirm data is beside notebooks, plots render, CSV writes succeed and a saved notebook reopens. Pin a tested environment for the intake; do not blindly upgrade halfway through the course. After the first passing run on both a Windows laptop and a Mac, pin the installed versions of numpy and seaborn in requirements-tested.txt with pip freeze.

## Python for Data Analysis

Use the Python and Jupyter environment above for both tracks. The track uses NumPy, pandas, matplotlib and seaborn. No Excel, spreadsheet, database tool or SQL is used with teenagers; SQL belongs to the professional courses. The lessons start with the 60-row camp_shop.csv so every answer can be checked by hand, and move to the Sunrise Shops files from session 9. All data files sit flat beside the notebooks. The files are generated: run `python3 data/generators/build_sunrise_data.py` and `python3 data/generators/verify_sunrise_data.py` if you ever need to rebuild or check them.

Teach Python first. If students need more time with loops or indexing, use the next class's opening recall period and shorten the optional Modify steps. Keep the final project to three questions and a few clear charts. No interactive dashboard, web deployment or GitHub account is required.

## Machine Learning extension

TensorFlow and Keras are not installed on student laptops. The optional extension notebook ML25 uses scikit-learn's MLPClassifier. If you want to demonstrate Keras, install TensorFlow only on your own laptop after checking that its supported Python versions include the one in the camp environment, then run `python programme/preflight_stack.py --tf`. The demonstration script is instructor_materials/ML/ML25_keras_demo_instructor.py and is not run by the verifier.

## Online setup check (hybrid groups)

Some learners take part online for two of their three weekly classes (and for the ML foundation labs). Before the first online class, work through the instructor part of handbook/HYBRID_DELIVERY.md: confirm the platform, the written class times and link for each parent or guardian, the consent form for any recording, and the route for returning build tasks (the organiser sets it and you rehearse it). Test screen sharing and sound with one learner. Check that each learner has the camp notebook installed and tested, the PDF sheet and the notebook already on the laptop as the backup, a charger and headphones. Online classes have a 90-minute live clock, and every instructor guide has an Online version section with that session's clock and build task. Keep a private list of who returned each build task.

## Every class

Open the student sheet and corresponding private instructor guide. Run the example before learners arrive. Write the words for today and the expected output on the board. Have the previous session's repair task ready. Confirm each learner can save a file. During practice visit all five learners. Finish with a saved artifact and one explanation from each student. Track complete/needs repair/absent privately. Keep a backup of teaching files and student work only in the agreed location.

## Build log and showcase operations

References include numeric data summaries, SQL and an ML held-back-set implementation. They help you check that a learner's numbers are right. They are not an upload service and nothing is graded. The organiser must choose and rehearse the way learners share their project folders before it is promised to parents. Use SHOWCASE_GUIDE.md for friendly feedback, one strength and one next step for each learner. Do not copy university roster identifiers or gradebook rules into this camp.

## Added ML foundation labs

Follow curriculum/FOUNDATION_LABS.md. Teach F01 after ML03, F02 after ML06, F03 after ML09 and F04 after ML12 on the fourth day of each of weeks 1–4. Each lab proposes two hours including a break. Check the learner can explain and reproduce the evidence before advancing. No previous Python or advanced mathematics is an entry requirement. Every learner brings their own laptop and charger; check it before enrolment.

## Responsible AI literacy

Teach handbook/AI_USE_POLICY.md in Session 1. Disable generative suggestions for weeks 1–6 and all core independent exercises. Before Session 21, rehearse handbook/AI_CODING_ASSISTANTS_LAB.md and check learner readiness; use a tutor-controlled local assistant or the labelled teacher-written fallback. Never make an account a prerequisite. Keep the permitted-use log with the project folder. The showcase is presented without an AI assistant open. No automated AI detector is used for anything.
