# Review brief: one independent pass over three sessions of "Enterprise Data Readiness for AI"

You review three sessions that are already written, checked and built. Make them complete, consistent, accurate and human. Read `AUTHOR BRIEF.md` (same folder) first for the files, the schema and the note rules, then `Build/curriculum.py`, then your three `Content/sNN.json` files, then the sessions before and after yours. Edit the Content JSON directly. After every edit run, from the Build folder:

    python3 build_course.py check N        (until 0 HARD problems and 0 warnings)
    python3 check_course.py                (look at the lines about your sessions)

Host paths for Read and Write: `/Users/jothamwambi/Projects/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/Enterprise Data Readiness for AI/05 Course Maintenance/Authoring/...`. In the shell the same files are under `/sessions/nice-gallant-tesla/mnt/Business_AI/Enterprise Data Readiness for AI/...`.

## The six jobs, in this order

### 1. Completeness against the curriculum
Take each session's entry in `curriculum.py`. Every topic must be taught on at least one slide; every outcome must be demonstrated by a slide and practised in the workshop; the workshop steps slide must match `lab.workshop` and the notebook; the session `result` must be what the workshop produces. The first slide is a recall of the previous session's REAL content (open that session's JSON: some sessions were written in parallel, so earlier recall slides were written from curriculum.py and may not match what the previous session actually teaches). `summary.next` must name the next session as curriculum.py titles it. Fix gaps: edit or add a slide (keep 15 to 22 content slides; a new slide needs correct notes and numbers computed from the data).

### 2. Consistency across the course
- Every mention of another session must be true (open that session's JSON). Fix wrong ones.
- A term must be used as the session that defined it defined it (see the `vocab` of all 12 sessions); no vocabulary term may be defined in two sessions (the checker reports it). Do not use a term before its session without a one-phrase explanation.
- Facts about the case must agree everywhere and match the data: 121 documents; 14 sources; 5,000 customers; 20,000 mobile money rows; 60 eval questions; the baseline scores 3.0 / 2.0 / 2.5 / 3.0 / 1.5; recall values; the retrieval ranks. If two numbers disagree, recompute from the files in `03 Learner Materials/Practice Files/data` and fix the wrong one.
- Names: "Kitara Group", "Kitara Bank", "Kitara Assurance", "Kitara Kenya". Workbook names exactly as in `03 Learner Materials/Workpiece Templates/`. Participant Workbook pages that slides mention must be listed in your reply (the tutor documents will contain them).
- The three workpieces: Session 2 baseline scorecard, Session 7 search pilot report, Session 12 roadmap and board presentation.
- The stand-in meaning scorer is always called a stand-in.

### 3. Ritual repetition
`check_course.py` fails when one sentence appears in the notes of more than 2 sessions. Rewrite the repeated sentences in YOUR sessions so each is specific to that session and phrased differently from the other sessions. Sentences to watch: "Three questions to finish.", "I will come round the tables.", "Three things to take home.", the trap slide labels read aloud ("What it looks like.", "Why it goes wrong.", "The fix has three parts."), and any opener of the title, outcomes, words, workshop, exit-check and summary notes. Pause lines (Take your time, Have a think, ...) are allowed once per session.

### 4. The slop sweep (slides and notes)
Read every slide's text and every note aloud in your head and rewrite sentences with these tells while keeping the warm, direct voice:
- filler openers ("Here's the thing", "So,", "Now,"), repeated "Look at the ..." or "This is the ..." openers on consecutive slides;
- portentous closers and aphorisms ("That is the whole point", "everything changes");
- "X, not Y", "not just X but Y", "rather than" contrasts, "no X, no Y" pairs for effect;
- triplets used only for rhythm; stacked rhetorical questions;
- meta commentary about the slide, the course, the speaker; praise of the course or of honesty ("honest", "real", "true" as filler);
- stock analogies reused across sessions (a library, a recipe, a map) unless they carry the idea;
- generic or spaced-caps labels, slogans, hedged authorial titles.
A note should sound like a knowledgeable colleague talking to a mixed table of leaders and technical staff. Specific beats general. Keep numbers and facts exactly right. Check also that a leader who never codes can follow every concept slide (plain word first, technical word second) and that each session ends with a decision question only a leader can answer.

### 5. Accuracy of external claims
For every external fact, law, standard, licence, date, price or API on your slides or in your notes: confirm it by WebSearch (and `mcp__workspace__web_fetch` for primary pages where the host allows it). Accept it only if two sources agree or one primary source states it. Correct what is wrong, hedge ("reported", "as of October 2026", "check the current text") what sources disagree on, and delete what you cannot confirm. Laws are a teaching summary and not legal advice, with no section numbers. Do not invent statistics, prices or quotes. Library calls for heavy packages (sentence-transformers, Chroma, pandera, great_expectations, presidio, dagster, duckdb, docling, ragas) are syntax-checked only: confirm each call against the project's current documentation by search and use the simplest documented form.

### 6. Re-check
Anything you changed must still be true and still pass the checker. Recompute numbers with pandas if you touch them. Keep paragraph counts for animated slides (one opening paragraph plus one per click). Never use dashes, the word click, markdown or labels in notes.

## Limits
- Do not change slide types, figure names, code, outputs or lab cells unless a fact is wrong or a topic is missing.
- Do not rewrite for taste where nothing is wrong.

## Reply (under 300 words)
Sessions reviewed; what you added or fixed for completeness; wrong cross-references or facts fixed (session and slide); external claims changed or deleted and why; ritual passages rewritten; slop fixes by type; Participant Workbook pages the slides mention; anything unresolved.
