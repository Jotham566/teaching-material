APPLIED AI AND AUTOMATION FOR EXECUTIVES: MAINTENANCE NOTES

Everything in 02 Class Slides, 01 Course Overview, 03 Learner Materials (Workbook) and 04 Facilitator Materials (Guide, Rehearsal Record) is generated from Build/content/s01.py to s12.py. Edit those files, then rebuild. Do not edit generated files by hand.

From Build/ (set PPTX_SKILL_SCRIPTS to the pptx skill scripts folder; Lato fonts are in Build/brand/fonts):
  python3 kit/lint_content.py            house style and schema of the session files
  python3 kit/deck.py [n ...]            the decks in 02 Class Slides
  python3 kit/make_docs.py               Course Overview, Learner Workbook, Facilitator Guide, Rehearsal Record, Start Here (Word and PDF)
  python3 kit/audit_specs.py             geometry audit of the decks (look for low, edge, small text, title collision)
  python3 kit/scan_edition.py            banned content scan across the edition
  python3 data_gen/make_case_data.py     regenerate the case-company CSV files (fixed seed)
  python3 data_gen/verify_case_data.py   722 checks of every planted fact against the keys
  python3 templates_gen/gen_docx.py and gen_xlsx.py   regenerate the templates; verify_templates.py checks them
  node "03 Learner Materials/Practice Files/03 Apps Script Build/tests/run_tests.js" and integration_case_data.js

COURSE_BIBLE.md holds the decisions: the twelve sessions, the case company, file names, writing and honesty rules.
Keep Archive/ and the Build folder out of anything a client receives.
