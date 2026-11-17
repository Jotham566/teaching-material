APPLIED AI AND AUTOMATION FOR EXECUTIVES: MAINTENANCE NOTES (version 3, November 2026)

The course has 14 sessions of 2 hours (28 hours), with no coding. Session 0 is the introduction. Sessions 1 to 11 teach how AI works, with demonstrations the lecturer runs. Sessions 12 to 14 are practicals with the learner.

Everything in 02 Class Slides, 01 Course Overview, 03 Learner Materials (Workbook, Take-away Sheets, Course Handbook), and 04 Facilitator Materials (Guide, Presenter Script, Rehearsal Record) is generated from Build/content/s00.py to s14.py. Edit those files, then rebuild. Do not edit generated files by hand.

From Build/ (set PPTX_SKILL_SCRIPTS to the pptx skill scripts folder; Lato fonts are in Build/brand/fonts):
  python3 kit/lint_content.py [n]        house style and schema of the session files (0 problems expected)
  python3 kit/deck.py n [n ...]          the decks in 02 Class Slides (name the sessions; do not run it with no number while someone else is building)
  python3 kit/make_docs.py               Course Overview, Learner Workbook, Take-away Sheets, Facilitator Guide, Presenter Script, Rehearsal Record, Start Here (Word and PDF)
  python3 kit/make_handbook.py           the Course Handbook in 03 Learner Materials
  python3 kit/audit_specs.py             geometry audit of the decks
  python3 kit/scan_edition.py            banned content scan across the edition
  python3 data_gen/make_case_data.py     regenerate the case-company CSV files (fixed seed)
  python3 data_gen/verify_case_data.py   checks of every planted fact against the keys
  python3 templates_gen/gen_docx.py and gen_xlsx.py   regenerate the Templates and Follow-up Kit; python3 templates_gen/verify_templates.py checks them

Other folders in Build/:
  V3_AUTHORING_BRIEF.md   the design of the 14-session course and the rules every session writer followed
  COURSE_BIBLE.md         the decisions: course, sessions, case company, facts, honesty and writing rules
  demo_runs/              every recorded run and its scripts and inputs (demo_runs/sNN_*.md and demo_runs/sNN/), plus sources_sNN.md for the external facts. Slides quote only these runs. The Session 11 mailbox run is not recorded yet (see demo_runs/s11_mailbox_agent.md).
  figures/, kit/diagrams_tNN.py   the drawn figures (one module per session)
  Case Runs/ (next to Build)      the earlier recorded runs F1 to F7 used by Sessions 10 to 13

Optional archived material (not part of the taught course): Archive/v2_before_technical_2026-11-05/practice_files (the Zapier and Apps Script builds). The course no longer teaches these builds. Keep them for a learner who wants a hands-on automation after the course.
Archive/ holds the earlier versions (v1, v2 twelve-session course, including the old Session 1 Preparation Pack and the 4 November course map). Keep Archive/ and the Build folder out of anything a client receives.
