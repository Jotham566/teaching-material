# Coherence review brief (11 November 2026): the whole course, read as a complete newcomer

## The lecturer's request (verbatim, 11 November 2026)
"Now, let's review everything one more time to ensure they are coherent, understandable and relatable to totally new students to the industry, flowing logically and chronologically, concepts and slides and sessions build up each other sequentially, very well structured, well illustrated to aid visual learning...etc"

Context: the explain-before-use rework of Sessions 2 to 14 (`EXPLAIN_BEFORE_USE_BRIEF.md`) was finished and committed today. Sessions 0 and 1 are delivered and stay unchanged; read them to know what the learner already has. This pass is a final cold read, not a rewrite. Keep what works. Fix what a newcomer would stumble on.

## Who reads it
An executive in finance, operations, HR, legal or sales. No maths or technical background, and new to AI work. They sat Sessions 0 and 1. They will read each slide for about a minute while the lecturer speaks the notes.

## Read each session as that person, slide by slide, and ask
1. UNDERSTANDABLE. Could I follow this slide with only what came before it? Is every term, symbol and number explained on this slide, earlier in this session, or in an earlier session (with a one-line recall naming the session)? Is any sentence dense, abstract or jargon-heavy where a plain one would do?
2. RELATABLE. Does each new idea open with an everyday picture a newcomer knows (shopping, a phone, a kitchen, a school, a bank, a car), before the work example (Nile Valley Foods and the other running cases)? Is the "where you meet it at work" link clear?
3. LOGICAL AND CHRONOLOGICAL ORDER. Does each slide follow from the one before? Does each new topic open with a bridge (in the notes, or a `statement` slide) saying why we turn to it now? Is anything taught after it is used, or taught twice? Are any slides in an odd place (for example a teaching slide after the decision slide)? Reorder if needed.
4. SESSIONS BUILD ON EACH OTHER. Where a concept was built in an earlier session, the slide recalls it in one line ("as in Session 4") and does not re-teach it at length or contradict it. Where the same word means something different from an earlier session (for example "baseline"), say so plainly. The cover note says what we build on; the keep note says what comes next. Check that these match the slides and `kit/chain.py`.
5. STRUCTURE. The plan slide and clock match the order of the slides. Each session has a visible arc: hook, ideas built in order, demonstration, hands-on, decision, take-away. Slide titles read as a story when listed alone (run the outline below and read only the titles).
6. ILLUSTRATED. Every concept slide has a drawn picture that teaches (not decoration): the worked numbers, the steps, the comparison. Text in figures is at least 14 pt, nothing overlaps or is clipped, labels are readable, colours are consistent with the rest of the course. A slide that is a wall of text, or whose picture does not match its words or numbers, needs a better figure. Look at every rendered PNG with the Read tool.
7. TRUE. Never change a recorded number or fact. Recompute every number you touch in Python.

## Cross-session points the lead reviewer noticed (check them; fix the ones that hold)
- S2: slide 1 recalls the four ways of learning from Session 0 slide 5? Slides 25, 26, 28 and 29 run k-nearest neighbours on messages and words before Session 4 teaches turning words into numbers. Is the needed idea taught at the right level (one plain line: "count shared words; Session 4 shows how"), or does it confuse?
- S3: slide 24 re-teaches overfitting after Session 2 taught it in depth. Make it a short recall that adds what is new (the gap between training and test score, and the baseline as a check). Session 0 previewed the confusion matrix, precision, recall and ROC: acknowledge it once.
- S4: the bridge from Session 3 (measuring) to words as numbers.
- S5: log in the next-token loss recalls log from Session 2 (log₂) and Session 4 (idf), and e from slide 7.
- S6: slide 11 uses "open weights" before Session 7 defines it (one-line forward pointer). The order of slides 11 to 16 (kinds, mixture of experts, reasoning, multimodal, diffusion): is it a clear path?
- S7: slide 24 ("Four questions expose a loose use of the word open") sits after the decision slide; it belongs with slides 3 and 4 (open weights and licences), or as an explicit take-away.
- S8: constraints, the fifth part, first appears inside Demonstration 1 with no teaching slide of its own. Structured output (slides 9 and 10) is split from its demonstration (slide 15) by the system prompt and delimiters. Consider the order: five parts one by one (role, context, examples, format, constraints), the strong prompt taken apart, Demonstration 1, system prompt and delimiters, structured output and JSON, Demonstration 2, evaluation sets, chain-of-thought and reasoning models.
- S9: recall of Session 1 (a layer is a table of weights) and Session 4 (cosine).
- S10: expected cost = P(error) × cost; S11 risk = likelihood × impact; S13 risk score = likelihood × impact. Each later one should recall the earlier one and say what is the same and what differs (money versus scores 1 to 5).
- S11 and S13: S13 slides 4 and 5 re-teach likelihood × impact with a flat tyre; S11 slide 8 already built it. Recall and move on faster, or make S13 a clear extension (from one risk to a register).
- S12: "baseline" here means today's measured cost or time, which differs from the Session 3 baseline (the score to beat). Say so. Rules, AI step, agent: recall Session 0 slide 36 and Session 11.
- S14: five kinds of data and the readiness scorecard recall Session 0 slides 17 to 21; the evaluation set recalls Session 10; OCR, chunking, metadata and embeddings recall Sessions 4 and 9. The final slides close the whole course: does the one-picture summary show every session in order?

## What you may change
Your sessions' `content/sNN.py` (slides, notes, order, words, recall, keep, clock, plan, workbook, facilitator) and `kit/diagrams_tNN.py`. Authored slides up to 32 per session. Keep the clock at 120 minutes with the plan slide matching. Do NOT edit `kit/chain.py`, `kit/deck.py`, `kit/lint_content.py`, `kit/diagrams.py`, `kit/figkit.py`, other sessions, Sessions 0 and 1, or generated documents. Put proposed `kit/chain.py` changes in your report. Do not run `kit/make_docs.py`, or `kit/deck.py` without an argument.

## Workflow
Setup: `. /private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/d327a2a5-164d-49e1-94aa-14fa1a0cd931/scratchpad/env.sh; cd "$B"`.
1. Read this brief, `EXPLAIN_BEFORE_USE_BRIEF.md`, `V3_AUTHORING_BRIEF.md`, `FLOW_BRIEF.md`, `TERMS_AND_EXAMPLES_BRIEF.md`, and the course outline `$S/outline_all.txt` (every slide title of every session). Read `content/s00.py` and `content/s01.py`, the session before yours, and your sessions.
2. Render: `$S/render_one.sh N` (PNGs in `$S/review/NN/`). Look at every slide image and read its notes.
3. Write `$S/coherence_sNN.md`: slide by slide, every stumble under the seven questions above, plus a verdict on each cross-session point that concerns you.
4. Fix. Then `python kit/lint_content.py N` to 0 problems, `$S/render_one.sh N`, and look again at every changed slide. Repeat until clean.
5. Read the spoken script in order from `_specs/NN_-_*.json` as if aloud: no cold starts, every topic change bridged.

## Report (under 250 words per session)
Slide count before and after; what you reordered, rewrote, recalled or redrew (name the slides); cross-session points closed; anything left and why; proposed `kit/chain.py` changes; lint result; any claim you could not verify.
