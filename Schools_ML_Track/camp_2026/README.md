# Holiday Data and AI Camp

Two beginner tracks for S.4 to S.6 students and school leavers: **Machine Learning** and **Python for Data Analysis**. Eight weeks, three core sessions a week, 24 core sessions each. Machine Learning adds four foundation labs on a fourth day in weeks 1 to 4 and an optional extension. Every learner needs their own laptop. SQL is taught in the professional courses and is not part of this camp. Rebuilt on 31 October 2026 (revision 2); the reasons and evidence are in [the restructuring proposal](../docs/Camp_Restructuring_Proposal.docx).

## Where to find things

| I want to | Go to |
|---|---|
| Teach a session | [instructor_materials/](instructor_materials/README.md): one guide per session with the 180-minute clock, answers, misconceptions and questions to ask. Keep it private. |
| Hand out the course | [student_packs/](student_packs/README.md): one ZIP per track, ready to share. |
| See what each session teaches | [curriculum/](curriculum/README.md): the 24-session curriculum and eight-week plan for each track, glossaries and the foundation labs. |
| Check a rule (AI use, marking, completion, what to tell students) | [handbook/](handbook/README.md) |
| Prepare laptops and the room, or see the organiser's decisions | [programme/](programme/README.md): setup, preflight script, decisions, benchmarks. |
| Find or rebuild a dataset | [data/](data/README.md) |
| Edit a lesson, rebuild or verify the pack | [build/](build/README.md) |
| See the student sheets and notebooks | [student_materials/](student_materials/README.md) (the same files are inside the ZIPs) |
| Project a session | `slides/DA/` and `slides/ML/`: 53 KLAi-branded decks (one per session, lab and the extension) with a spoken script in the speaker notes. Instructor only, not in the student ZIPs. Install the Lato fonts from `brand/fonts/` on the teaching laptop first. |
| Brand files (logos, fonts, colours) | `brand/` |
| Send parents a short outline | `marketing/parent_outlines/KLAi_Camp_Parent_Outline_DA.pdf` and `_ML.pdf` (2 pages each, fee and venue included) |
| Teach from a printed guide | `instructor_materials/PDF/Instructor_Guide_DA.pdf` and `_ML.pdf` |
| Share flyers and posts | [marketing/](marketing/README.md) |

## One session in a sentence

One question for the day, at most six new words, two 50-minute blocks (predict, run, investigate, modify), a Make task, an error card and an exit ticket. Default clock: 10 recall, 50 block A, 15 break, 50 block B, 40 make, 15 exit.

## Before the first class

Run [programme/preflight_stack.py](programme/preflight_stack.py) on every laptop. Pilot one beginner through ML01, ML05, ML14, DA02, DA09, DA14 and DA17. Confirm the dates, venue, fees and booking terms in [programme/PROGRAMME_DECISIONS.md](programme/PROGRAMME_DECISIONS.md).

Students work from PDF session sheets and notebooks; the slides are the instructor's projection aid. A school submission platform, online registration and payment, automatic grading and issued certificates are not deployed by this pack. No beginner pilot has been run.

## Verify and rebuild

From the repository root:

```
python Schools_ML_Track/camp_2026/build/build_camp.py
python Schools_ML_Track/camp_2026/build/verify_camp.py
python Schools_ML_Track/camp_2026/build/package_camp.py
```

The verifier runs every worked example, Modify answer, Make reference and lab against the supplied data and writes `review/2026-10-31/schools-camp/verification.json`.

## Rebuild the slides

```
cd Schools_ML_Track/camp_2026/build/slides
PPTX_SKILL_SCRIPTS=<path to pptx skill scripts> python3 build_slides.py          # all decks (FORCE_FIGS=1 redraws every figure)
python3 lint_slides.py
```

Figures are cached in `figures/` and specs in `build/slides/_specs`; both can be regenerated.
