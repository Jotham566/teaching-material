# Week 3–15 teaching revision — 29 September 2026

This edition covers CML3111, CML3112 and CML3113. Teach from the PowerPoints in `decks/`; matching lecturer companions are in `decks/lecturer_notes/`. The older semester Word guides may retain historical slide numbers. Use the current slide companions for exact navigation.

## Starting the next class

- CML3112 resumes Week 3 at **slide 13**. See `CML3112_Week3_Continuation.md` for the suggested demonstration route.
- CML3111 and CML3113 begin their Week 3 decks at slide 1.
- CML3112 A3 remains due **29 September 2026, 11:00 Kampala**. Students were already told to read the final slides and complete it. This revision does not reopen forms or extend deadlines.
- Share the refreshed cohort student ZIP. `guided_practice.ipynb` contains worked examples for revision; the issued assignment notebook remains the graded submission.

## What changed

A second pass expands arithmetic operators, comparisons, branch paths, for/while loops and loop controls into definitions, runnable examples and trace tables. Later prerequisites cover dictionary fallback lookup, pandas chains, None, medians, array shapes, pipelines, paired errors and sorting keys. Lecturer notes now follow actual slide content rather than retaining unrelated keyword-matched explanations. See [Teaching prerequisite map](Teaching_Prerequisite_Map.md).

Week 3 introduces collections and their differences before indexing, searching or selecting errors. Conditions precede functions; each function example includes its call and expected result. Week 4 teaches dictionary operations, tuples, sets, unpacking and summaries before record processing. Later weeks explain matrices, library imports, model objects, thresholds, counters, hyperparameters and candidate records before the corresponding examples.

Live partner activities have been replaced by direct worked explanations and individual revision checks. Optional videos appear after taught content. Illustrations using separate example data now identify that change. Existing navy, orange and teal styling and illustrations are retained. Lecturer notes and guided notebooks follow the revised sequence.

Issued assignment files, function interfaces, grading logic, marks and quiz banks are unchanged. No extra manually marked work was introduced. Quiz availability remains 24 hours from activation.

## Verification

- 39 final PowerPoints, containing 1,739 slides, exported and rendered; finalizer checks completed.
- Published hashes, slide text, linked speaker notes and all 39 lecturer companions checked against the source.
- 27 guided notebooks executed successfully using the supplied CSVs where needed.
- 27 Week 3 onward student ZIPs checked against the current practice notebooks and issued assignment files; private grading files excluded.
- Eleven prerequisite/order/deadline/example-output tests and four submission-guidance tests passed.
- Rendered slide review included the common weekly sequence, corrected layouts and cohort-specific examples. This was not a native PowerPoint application test.
- The five-page lecturer quick guide was regenerated and rendered for layout review.

The pre-revision repository checkpoint was committed and pushed to main as `d388b0bc` before these changes. Review renders and temporary build files remain ignored. School-camp and independent-track materials were not changed by this revision.

## Rebuilding and checking

`data/iuea_deck_content.json` is the shared content consumed by the deck and practice builders. `scripts/prepare_beginner_ppt_content.py` reproduces it from the curriculum and reviewed notes, applying `scripts/iuea_foundations_revision.py`. Previously taught Week 2 content is preserved.

Use the configured Node runtime to run `scripts/build_beginner_decks.mjs`, selecting cohort/week identifiers and a new `PPT_EDITION`. Publication requires matching finalizer receipts and renders; update the edition selection in `scripts/publish_iuea_foundations.py` when intentionally publishing another build. Then rebuild the guided notebooks and student packages.

Run `python3 scripts/verify_iuea_foundations.py` for current deck/note/package verification. The September 15 and September 21 verification scripts are historical audits of their original editions.
