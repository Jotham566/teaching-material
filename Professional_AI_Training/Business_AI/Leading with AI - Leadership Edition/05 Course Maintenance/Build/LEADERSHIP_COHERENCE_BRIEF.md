# Leadership Edition coherence and fact-check brief (12 November 2026)

All fifteen sessions of Leading with AI are written (seven writers in parallel). This pass makes them one course: coherent, understandable and relatable to senior leaders new to AI, flowing in order, each session building on the ones before, well illustrated, and TRUE.

Read first: `LEADERSHIP_BIBLE.md`, `LEADERSHIP_AUTHORING_BRIEF.md` (all of it), `kit/sessions_plan.py`, `kit/chain.py`, and the whole-course outline `$S/lead_outline.txt` (every slide title of every session). Then the content files of the session before yours and your sessions, and their rendered images.

## For each of your sessions, read every slide image and its notes as a newcomer leader, and fix
1. **Understandable.** Every term explained before use (plain words first, then the industry term) or recalled in one line naming the session where it was built. No maths, no jargon left unexplained.
2. **Relatable.** Everyday picture first; the industry tour gives the learner's industry a real example; the people slide is concrete.
3. **Order and bridges.** Each slide follows from the one before; every new part opens with a bridge. The first slide bridges from the previous session as it was actually written (read that session's last slides and keep note). The keep note names the next session as it was actually written.
4. **Build-up across sessions.** Where a case or idea appeared earlier, recall it ("as in Session 9") instead of re-telling it at length, and keep facts identical across sessions (the same figures, the same wording of a result). Known repeats to align: Telstra (Sessions 4 and 8), Commonwealth Bank of Australia (9 and 12), Klarna (12, maybe 5), the non-existent court case runs (5 and 9), URA (0, 11 and 14), Penda Health (0 and 5), the twelve-message rule versus AI run (0 and 11), hidden instructions (9 and 10), the "words" definitions repeated across sessions (Fine-tuning in 6 and 8, Hallucination in 5 and 9, Prompt injection in 9 and 10, Threshold in 2 and 3): same meaning, recalled.
5. **Recall slide.** The recall questions ask about what the previous session actually taught; their answers match it.
6. **Illustrated.** Every concept and case slide has a figure that teaches; text 14 pt or more; no overlap, clipping, empty boxes or stray symbols. Industry tour tiles that have no named case should still give a typical use and say "no published case yet" in a way that reads well.
7. **True.** Check EVERY case figure, date, name and claim on your slides and in your notes against its block in `research/*.md` (search by organisation). Fix any figure that differs, any claim stronger than the source, and any missing "company figures" caution. Check every demonstration number against its run record in `demo_runs/` or `Case Runs` (the Executive Edition's Case Runs folder is at `../../../Applied AI and Automation - Executive Edition/05 Course Maintenance/Case Runs`). Never invent.

## Known items from the writers (fix those in your sessions)
- S14: the demonstration slide says the script "read" the Busoga agreement copies and undated files; the run record does not show this. Reword truthfully. Check the zero-VAT rule wording; the EU deforestation rule status is for the facilitator note.
- S14: recall questions and portfolio columns must match Sessions 11 to 13 as written.
- S1: the banking tile has no named case; S3: the manufacturing tile has no named case. Make the tiles read well.
- S1: the live receipt demonstration has no recording; the fallback must be explicit.
- S13: the OrbitDesk price is in US dollars; leave it as written in the fictional proposal or explain.

## Rules
Edit only your sessions' `content/sNN.py` and `kit/diagrams_lNN.py`. If a fix belongs in a shared helper you do not own, draw a local version. Do not edit kit/deck.py, kit/lint_content.py, kit/chain.py (propose changes in your report), other sessions, or the research files. Setup: `. $S/env_lead.sh; cd "$B"` (S is /private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/d327a2a5-164d-49e1-94aa-14fa1a0cd931/scratchpad). Lint `python kit/lint_content.py N` to 0; render `$S/render_lead.sh N`; look at every changed slide again.

## Report (under 250 words per session)
What you fixed (slides named), facts corrected (old and new, with the source), cross-session alignments, anything left and why, proposed chain.py changes, lint result.
