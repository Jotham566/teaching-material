# Assignment clarity review 29 September 2026

The student assignment notebook is now the main working document. It contains the short brief, exact required files, task prompts, marks and answer locations. Separate instruction files are labelled reference copies. Setup help is a reference for a specific difficulty, not compulsory extra reading.

## Changes

- Short guides for all 48 IUEA assessments; no independent Data Analysis or school camp content changed.
- Thirty weekly student ZIPs rebuilt with one start file and matching current instructions.
- All 48 live Google assignment form descriptions shortened to 142–168 words, plus their marks/deadline header. Existing form URLs, required fields, open/closed state and windows preserved.
- A3 formulas, units, signed error, efficiency guard and worst-error selection clarified beside the five existing answer cells. No new task or loop requirement.
- A3–A5 explicitly require one completed notebook, with no separate report or written-evidence section. A4's title “Reading report” is explained as a Python notebook task.
- Later weekly written criteria converted from assessor instructions into student questions, located beside the existing written-answer cell. Supplied scenarios are identified as supplied results. Grading rubrics and question marks remain unchanged.
- Long function instructions broken into steps; expected dictionary keys and return types clarified. Full chart requirements now appear beside the chart task instead of referring to an absent contract.
- Assignment copies in ZIPs have execution outputs cleared for sharing. The lecturer's local code, execution history and written answers remain intact.
- CML3112 marked as having completed Week 3; Week 4 is next. CML3111 and CML3113 start Week 3 at slide 1. Updated lecturer Word guidance rendered and all five pages inspected.

## Verification

Four instruction/package tests passed, along with 16 existing registration, submission-selection, offline-collection and presentation-guidance tests. A before/after check across 179 files confirmed executable notebook cells, saved execution state, existing written-answer cells, grading specifications, rubrics and calibration cases were preserved.

Each live form refresh verified its description, field IDs, acceptance state and stored window. No responses or grades were edited. Unreleased assessments remain unreleased. Live A4 was checked through its student view.

## Lecturer use

Use [the instruction index](Assignment_Instructions_Index.md) for refreshed ZIPs and cohort guides. Share the matching student ZIP. Students already working should keep their work and use the clearer instructions as a reference; no restart or resubmission is required solely for this wording change.

Before assigning work, state the exact notebook/document, expected outputs, upload count and live Kampala deadline. The current CML3112 reopening dates are recorded separately in [the student links](CML3112_Sept29_Student_Links.md). This clarity revision changes no deadline.

## Regeneration

Run these in order after changing the student wording:

```
python3 scripts/build_assignment_instructions.py --iuea-only
python3 scripts/build_submission_forms.py
python3 scripts/build_student_packages.py --iuea-only
python3 -m unittest discover -s tests -p test_concise_iuea_assignments.py
```

The builder updates markdown prompts only; it does not reset code cells or student evidence. After a separate full assessment-bank rebuild, rerun this sequence to apply the current student wording. Do not run a full bank rebuild over saved lecturer/student work.

For a new live description revision, use the generated concise_assignment_briefs.gs with concise_assignment_instructions.gs in the existing assignment controller. Give a new revision its own completion-property key; run the batch function until all 48 are complete. Never rebuild or reopen forms merely to refresh their descriptions.

## Subsequent approved deadline correction

After the wording review, the lecturer explicitly approved extending CML3113 A3 to 9 October 2026 at 08:00 and CML3111 A3 to 9 October at 11:00 Kampala. These are the only additional window changes. The registry, link index, guides and weekly ZIPs reflect them.
