# December holiday camp materials

Two beginner tracks for S.4–S.6 students and vacists. Each is eight weeks with three core classes per week. ML adds a fourth-day foundation lab in weeks 1–4 (28 meetings); DA has 24 meetings. Every student must have their own laptop. Working programme name: Holiday Data and AI Camp. The proposed offering is one track per learner, with three groups of five learners total.

## Marketing files to review

- [Parent and student one pager PDF](marketing/Parent_Student_One_Pager.pdf)
- [Editable one pager DOCX](marketing/Parent_Student_One_Pager.docx)
- [Machine Learning flyer PDF](marketing/Machine_Learning_Flyer.pdf) and [WhatsApp image](marketing/Machine_Learning_Flyer.png)
- [Data Analysis flyer PDF](marketing/Data_Analysis_Flyer.pdf) and [WhatsApp image](marketing/Data_Analysis_Flyer.png)

The enquiry materials include main tutor Jotham Martin Wambi’s profile, phone, email and LinkedIn. Before advertising confirmed bookings, resolve the dates, venue, session lengths, booking terms and three/four-person price. [Programme decisions](operations/PROGRAMME_DECISIONS.md) distinguishes supplied details from working choices. December 2026 plus eight teaching weeks normally extends into January 2027.

## Teaching and student packs

- [Class-by-class delivery plan](teaching/CLASS_BY_CLASS_PLAN.md): objectives for all 48 classes, weekly practice and the ML lab sequence.
- [Final project rubric](teaching/PROJECT_RUBRIC.md): scoring anchors for the project and unaided demonstration.
- [Responsible AI policy](teaching/AI_USE_POLICY.md): independent foundations, limited supervised exposure in weeks 7–8 and unaided final assessment.
- [Coding-assistant critique](teaching/AI_CODING_ASSISTANTS_LAB.md): guided Session 21 practice with tests and disclosure.
- [Optional modern-AI orientation](teaching/MODERN_AI_ORIENTATION.md): 20 minutes inside Session 23, with an offline demonstration and lecturer prompts.
- [Foundation lab sequence](teaching/FOUNDATION_LABS.md): required ML bridge before modelling.
- [Curriculum](teaching/CURRICULUM.md): both 24-session pathways, definitions and practical outcomes.
- [Student start guide](teaching/START_HERE.md): extracting files, opening tools, saving and submitting work.
- [Assessment and showcase](teaching/ASSESSMENT_AND_SHOWCASE.md): observable evidence and proposed completion rules.
- [Machine Learning student ZIP](ML_Beginner_Student_Pack.zip): 24 core lesson sheets/notebooks plus four foundation lab sheets/notebooks, practice data and start instructions.
- [Data Analysis student ZIP](DA_Beginner_Student_Pack.zip): 24 lesson sheets and notebooks, Python/pandas practice CSV, SQLite database and five worked SQL files.
- [Instructor material](instructor_materials/): 48 core session guides plus four ML foundation lab guides, task references, exact data totals, reference SQL and ML checkpoint code. Keep this folder private.
- [Instructor setup](operations/INSTRUCTOR_SETUP.md): prepare and rehearse the tools before class.

The student ZIP is distributed before the first class once device instructions are agreed. Start at ML01 or DA01; the instructor teaches each example in order. Learners complete the matching task in class and practise it afterward. Do not tell learners to complete all files independently before class. Empty task cells are deliberate spaces for their work; worked examples and expected results are included.

These teaching materials are lesson sheets and notebooks, not a completed PowerPoint slide course. They need a beginner pilot and actual-device preflight. A school submission platform, online registration/payment flow, full automated grading service and issued certificates are not deployed by this pack.

## Review and verification

[Review rationale and sources](operations/REVIEW_AND_BENCHMARKS.md) records the corrections and external benchmarks without implying affiliation. The teaching data is supplied and synthetic; no learner survey or public profile is required. Privacy and equipment arrangements are explicit launch decisions.

`review/2026-09-26/schools-camp/verification.json` records example execution and notebook validation. Final PDF and DOCX layouts have been rendered and visually inspected. These checks do not establish beginner comprehension or compatibility with every laptop.

## Rebuild

Run from the repository root using a Python environment with the required libraries. Artifact creation uses the workspace's bundled Python with python-docx/reportlab; worked-code verification uses the tested teaching environment.

```
python scripts/build_schools_camp.py
python scripts/build_schools_camp_marketing.py
python scripts/verify_schools_camp.py
python scripts/package_schools_camp.py
```

After editing, render and inspect all marketing pages again and regenerate the two final PNG flyers from the current PDFs. `scripts/schools_camp_content.py` supplies lesson content and four-phase roadmaps. The eight-week comparison in the marketing builder must remain aligned with it. Do not use the old ML-only syllabus generators to publish this new two-track offer.
