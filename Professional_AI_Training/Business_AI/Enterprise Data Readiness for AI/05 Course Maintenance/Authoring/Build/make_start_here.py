"""Write 00 Start Here.txt and 05 Course Maintenance/Verification Record.txt with counts read from docs_data.json.  python3 make_start_here.py"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
d = json.loads((HERE / 'docs_data.json').read_text(encoding='utf-8')); T = d['totals']; hrs = round(T['words'] / 130 / 60, 1)
tpl = ', '.join(d['templates'])
start = f"""ENTERPRISE DATA READINESS FOR AI
{d['course']['sessions']} sessions of 2 hours | {d['course']['total_hours']} hours | free tools only | for a decision maker and a data or IT colleague from the same organisation

{d['course']['start']} They finish with a scored baseline, a tested search over the organisation's own documents and a twelve-month plan presented as a board paper. Delivery is either a cohort of organisations or in house for one organisation. Pairing a decision maker with a data colleague is preferred. KLAi issues no certificate for the course.

STATUS: built. {T['slides']} slides, {d['course']['sessions']} team notebooks with solutions, the Kitara Group case data, the workpiece templates and the handouts exist. See 05 Course Maintenance/Verification Record.txt for what is and is not checked.

01 Course Overview
Course Roadmap (one page).pdf is the page to share with participants. The .pptx beside it is the editable version.

02 Class Slides
One PowerPoint per session, numbered in teaching order. {T['slides']} slides in all: {T['animated']} are animated ({T['clicks']} click reveals), and every slide has speaker notes written as a script to read aloud (about {hrs} hours in all). {T['code_slides']} slides carry code for the live demonstration. Play the animated slides in Slide Show mode.

03 Learner Materials
Setup Guide.docx: what to bring and do before Session 1. Send it before the course starts.
Participant Workbook.docx: how to use the course, the five dimensions and levels, the three workpieces, a task page for each session with ruled answer space, the decision questions, the vocabulary, and the pages Pipeline map, Data protection map, Search pilot report outline and Board presentation outline.
Glossary.docx: all {T['vocab']} vocabulary terms with their plain meaning and where they appear.
Workpiece Templates: {tpl}.
Practice Files/data: the Kitara Group files (see DATA DICTIONARY.txt). Practice Files/data.zip is the same set for participants to upload. Practice Files/notebooks: the student team notebook for each session. Open them in Google Colab.

04 Facilitator Materials
Course Plan and Tutor Guide.docx: course shape, how a pair attends, before the course, timetable, a page for each session with the workshop answer key and decision answer, workpiece checklists, room and confidentiality.
Benchmark and Design Report.docx: the evidence, frameworks, law, tool licences, East African context, comparator courses and the design.
Lab Solutions: the solution notebook for each session (tutor only).
run_all_labs.py: runs every solution notebook top to bottom. Use --allow-missing-libs on a machine without the heavy libraries.
Playback and Rehearsal Checklist.txt: every animated slide with its click count, the cells to run once in Colab and the workbook to open for each session.

05 Course Maintenance
Authoring: everything needed to rebuild the decks, notebooks, data, figures and documents. Read Authoring/README - Read First.txt.
Research/Research Notes.txt: every external fact with its source and what is unconfirmed.
Verification Record.txt: what was checked, what could not be, and what to do before the first class.

BEFORE THE FIRST CLASS
1 Upload data.zip where participants can reach it.
2 Send the Setup Guide and ask each participant to run the first notebook cell in Colab.
3 Run run_all_labs.py in 04 Facilitator Materials, then run the heavy-library cells once in Colab (the Playback and Rehearsal Checklist lists them).
4 Play every animated slide in PowerPoint.
5 Read the notes aloud once per session.
6 Collect from each participant the written approval that their 50 documents are non-confidential (needed by Session 5).
7 Read the primary sources listed in section 10 of the Benchmark and Design Report.
"""
(ROOT / '00 Start Here.txt').write_text(start, encoding='utf-8')
ver = f"""VERIFICATION RECORD, 29 OCTOBER 2026
Enterprise Data Readiness for AI: {d['course']['sessions']} sessions, {T['slides']} slides ({T['animated']} animated, {T['clicks']} click reveals), {T['vocab']} vocabulary terms, {T['workshop_tasks']} workshop tasks, {d['course']['sessions']} student and {d['course']['sessions']} solution notebooks. The counts were read from the built decks and content files by export_docs_data.py on the day of the final rebuild.

CHECKED, AND HOW
Builds. python3 build_course.py data was run once at the end, then build all. All {d['course']['sessions']} decks and notebooks build with 0 HARD problems and 0 warnings. The slide engine measures text and refuses a slide whose text does not fit at its minimum size.
Course check. python3 check_course.py reports no course-level problems: no duplicate vocabulary term, no repeated sentence beyond the limit, no unknown figure name, no title ending in a full stop.
Validator. The PowerPoint schema validator passes on all {d['course']['sessions']} decks and on the roadmap deck.
Code on slides and in notebooks. Every pandas, numpy, matplotlib and SQLite block was run on the Kitara data and the slide output compared with the real output. Blocks that need a heavy library were syntax-checked only.
Labs. run_all_labs.py with --allow-missing-libs ran all {d['course']['sessions']} solution notebooks to the end. Cells needing sentence-transformers (Session 6, Task 5 and its check) and presidio (Session 9) were skipped. The runner was corrected during this pass: a check cell that depends on a skipped download cell is now skipped as well. No notebook failed, so no content file needed a fix.
Documents. The Participant Workbook, Course Plan and Tutor Guide, Glossary, Setup Guide and Benchmark and Design Report were rendered to PDF with LibreOffice and their pages were viewed. Layout faults found (ruled answer lines merging into one line, a landscape map table running onto a second page, a numbered list continuing across sections, duplicated text) were fixed in make_docs.js. Totals in the documents are computed from the files.
Data. The Kitara folder holds 121 documents, 14 sources, 5,000 customers, 20,000 mobile money rows and 60 test questions, counted from the files.
Figures. The figures were reviewed when each session was written. 23 figures are in the catalogue.

CHECKED BY WEB SEARCH ONLY
Surveys, forecasts, framework details, laws, regulator actions, tool licences, hosting facts, course prices and dates quoted in the decks and the Benchmark and Design Report come from search results and third-party pages, with dates seen in Research Notes.txt. They were not read in the primary document.

NOT VERIFIED
1 Heavy-library code was never executed here: sentence-transformers, chromadb, pgvector with psycopg2, pandera, great_expectations, presidio, dagster, duckdb with pyarrow and docling. It was read against the documentation. Run each cell once in Colab.
2 Primary legal texts were not read: the Uganda Data Protection and Privacy Act, 2019 and its regulations, the Kenya, Rwanda and Tanzania laws and the Kenya cross-border guidance note. Session 9 is a teaching summary and not legal advice.
3 Licence files were not read. Open the LICENSE file or model card of each tool marked check before relying on it.
4 PowerPoint playback of the animations was not tested. LibreOffice shows the finished slide only.
5 Nothing was rehearsed aloud.
6 Google Colab was not used to run the notebooks, so the setup cell, the apt-get install of Tesseract and the file upload are untested there.
7 Spreadsheet formulas in the workpiece templates were not run in Excel or Google Sheets here.

OPEN VERIFICATION LIST (Benchmark and Design Report, section 10)
Open and read before teaching: the Gartner 60 percent wording; the MIT NANDA 95 percent wording; the Uganda Data Protection and Privacy Act sections 19 and 23 and its regulations; the Kenya cross-border guidance note; the Official Journal text of Regulation (EU) 2026/1744; the LICENSE file of every tool in section 5 of the report; the Oxford Insights ranks for Kenya and Rwanda; and the definitions of recall at k and mean reciprocal rank. The Colab and pgvector demonstrations are untested.

IF THE DATA GENERATOR CHANGES
Run python3 build_course.py check N for every session. A slide output that no longer matches the real output is an error, and the content file must then be updated. Do not run build_teaching_data.py on its own, because it overwrites the zip without kitara_search.py. Use build_course.py data.
"""
(ROOT / '05 Course Maintenance' / 'Verification Record.txt').write_text(ver, encoding='utf-8'); print('written')
