AUTHORING SOURCES: WHAT PRODUCES THE TEACHING EDITION

The teaching edition is reproduced in two layers. Edit the layer named below, build into a staging folder, compare, verify and only then replace the live files.

1. Builder layer (needs the author's Mac runtime; not run in the October 2026 maintenance sessions)
   Documents/*.py, course.json and PowerPoint/build_course.mjs produced the original decks and Word documents. A copy of that output is kept in Baseline/ and is the BASE for the next layer. The text in these builder sources still describes the earlier fictional agreement and the generated notes. Do not teach from them and do not copy their output over the live edition.

2. Edition layer (runs on any machine with Python, python-pptx, python-docx and Pillow)
   Baseline/                          the builder's output, versioned and hash-checked (Baseline Manifest.json). The builder cannot be rerun from maintained sources.
   Edition/patch/slide_patch.json     slide text and picture corrections to the baseline decks
   Documents/lesson_notes.json        speaker notes for all 285 slides, written as a script to read aloud (previous guide-style notes: Documents/archive)
   Documents/lesson_notes_sources.json  source links and click counts, written to Teaching Resources/Presenter Notes Backup.txt
   Illustrations/                     the drawing code, the placement plan, the placement script and approved/ (the PNGs the decks embed; builds never draw)
   Edition/patch/docx_patch.json      paragraph text corrections to the builder's Word documents
   Edition/files/                     the practice files, teaching resources and other hand-written files

How to change something
   Slide notes:         edit Documents/lesson_notes.json (keep the read-aloud form; an animated slide needs at least one paragraph per click plus an opening paragraph)
   Pictures:            edit Illustrations/illustrations.py or illustration_plan.json, then run Illustrations/approve_illustrations.py render, inspect the result and commit approved/ with Approved Assets.json
   Practice files and teaching resources: edit the live file, then run Edition/snapshot_files.py
   Slide text or Word text: edit the live file, then regenerate the patch with Edition/edition_patch.py make or Edition/docx_patch.py make (see their headers)
How to release
   python3 Edition/build_edition.py /tmp/staging        builds a complete staging edition
   python3 Edition/compare_edition.py /tmp/staging      lists every difference from the live edition
   python3 Edition/verify_edition.py --rebuild --write-records
                                                        checks the live edition, rebuilds it from these sources, requires a match and refreshes File Integrity.json and Validation/Edition Verification.json
Validation/Session 01.json to Session 12.json, Content Verification.json and Manual Inspection.json describe the earlier builder output and are kept as history.

28 October correction: Documents/session_delivery.json drives the concrete 120-minute activities recorded in Classroom Run Sheets.txt and the Guide. The repaired retrieval route and its observed results are in the edition snapshot. Run verify_edition.py --rebuild after changing sources; its correction checks bind the results to Tested Sources.json. Re-run the actual experiment before refreshing that record.

Demonstration instructions: Documents/demonstrations.json is the maintained source. Documents/add_demonstration_instructions.py appends its linked sections after docx_patch.py emits the core Guide. Do not make a paragraph patch from the assembled Guide. Edit the JSON and rebuild. Documents/make_demo_materials.py regenerates Demo Materials in staging on every build; live prompt files must match the source IDs. facilitator_demo.py and its .command launcher are copied in Edition/files with the practice assets.

Experienced-user delivery: demonstrations.json holds each session’s executive_task and executive_check. The Guide presents these before the procedure. The session_delivery.json timetable and core Guide/Workbook paragraph patch carry the adjusted repeat-comparison and briefing activities. Keep routine interface instructions as facilitator preparation. Source and executable tests stay separate from instruction reviews in Demonstration Delivery.json.

Repository size: .build render/staging outputs are disposable and ignored. The hash-checked Baseline, approved illustrations, source patches, current deliverables and observed-run evidence are required. Synthetic rehearsal audio is optional: transcripts and historical timing measurements stay tracked, while generated M4A/AIFF files are omitted from snapshots and comparisons. See Teaching Resources/Rehearsal Audio/Read First.txt to regenerate one outside the repository.
