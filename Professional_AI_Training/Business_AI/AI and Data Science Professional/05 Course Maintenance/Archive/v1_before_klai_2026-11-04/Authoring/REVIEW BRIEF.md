# Review brief: one more pass over four sessions of "AI and Data Science Professional"

You are reviewing four sessions that are already written, checked and built. Your job is to make them complete, consistent, accurate and human. Read `AUTHOR BRIEF.md` (same folder) first for the files, the schema and the note rules, then `Build/curriculum.py`, then your four `Content/sNN.json` files. Edit the Content JSON directly. After every edit run, from the Build folder:

    python3 build_course.py check N        (until 0 HARD problems and 0 warnings)
    python3 check_course.py                (look at the lines about your sessions)

Host paths for Read and Write: `/Users/jothamwambi/Projects/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/AI and Data Science Professional/05 Course Maintenance/Authoring/...`. In the shell the same files are under `/sessions/nice-gallant-tesla/mnt/Business_AI/AI and Data Science Professional/...`.

## The five jobs, in this order

### 1. Completeness against the curriculum
For each of your sessions, take its entry in `curriculum.py` (title, question, result, outcomes, topics, lab).
- Every topic in `topics` must be taught on at least one slide. Every outcome must be something a slide demonstrates and the lab practises. The lab slide steps must match the lab cells or sheet tasks. The `result` must be what the lab produces.
- The first slide must be a recall of the previous session's real content (read that session's slides to be sure the answers are right). The `summary.next` line must name the next session as `curriculum.py` titles it.
- If something is missing, fix it: edit a slide, or add a slide (keep 15 to 22 content slides; a new slide needs correct notes with the right paragraph count, and any number on it must come from the data). If a gap cannot be fixed cheaply, report it.

### 2. Consistency across the course
- Every mention of another session ("in Session 8 we...", "as you saw in Session 3") must be true: open that session's JSON and confirm the idea is taught there. Fix wrong ones.
- A term must be used the way the session that defined it defined it (look at the vocab arrays of all 24 sessions). Do not use a term before the session that defines it unless the notes define it in one phrase on the spot.
- Facts about the data must agree everywhere (for example 30,229 orders; 98,066 lines; 8,000 loans; 12.5 percent default; the 2,000-order workbook is a sample). If you find two different numbers for one fact, find the true value with pandas on `03 Learner Materials/Practice Files/data` and fix the wrong one.
- Capstone timeline, which must be stated the same way wherever it appears: Session 13 write and scope the question, Session 14 choose the dataset, Session 19 baseline and tested model (Checkpoint 3), Session 23 publish the app and model card, Session 24 present for ten minutes. Checkpoints: Session 8, Session 13 (analysis report), Session 19. Marks: weekly checks ungraded; three checkpoints 15 percent each; capstone 40; participation 15.
- Names: use "Lakeside Mart", "Nile Microfinance", "District Clinics" (the file is clinic_visits.csv), "order lines", "loyalty customers". Tools are named the way `curriculum.py` TOOLS names them.

### 3. Ritual repetition
`check_course.py` now fails when one sentence appears in the notes of more than 4 sessions. The course repeats the same ritual sentences in every session, which a listener hears as a script. Rewrite those passages for YOUR sessions so each is specific to that session and phrased differently from the other sessions (and from your other three). They are in:
- `notes_outcomes` ("Three things to take away." and "The two hours run as usual." and "We recall first, then I teach, then I show you live, then you work in the lab."): say what is distinctive about this session's two hours instead, for example where the live part sits or what the lab produces.
- the exit check notes ("Three questions to finish. Answer each in your head, then I'll show you mine."): open from the content of the questions.
- the summary notes ("Let's finish with three things to keep."): open from the content, or just start with the first point.
- the lab notes ("Forty minutes in Google Colab. Open the Session N notebook and run the setup cell. ... If you get an error, read the last line first, then ask me. Then work down the tasks."): say what the first task actually is.
- the warm-up notes ("Before anything new, two quick questions from last session."): open by naming the topic being recalled.
- the title notes ("Welcome to Session N."): vary the opening.
- recurring fillers: "Now it's your turn.", "The fix is a habit.".
Pause lines (Take your time, Have a think, and so on) are allowed once per session. Do not copy another session's ritual phrasing: write your own and keep them short and natural.

### 4. The slop sweep (slides and notes)
Read every slide's text and every note aloud in your head, and rewrite sentences with these tells while keeping the warm teacher voice:
- filler openers ("Here's the thing", "Let's dive in", "So, ...", "Now, ...") used as rhythm, repeated "Look at the ..." and "This is the ..." openers on consecutive slides;
- portentous closers and aphorisms ("That is the whole point", "and that is the lesson", "everything changes");
- "X, not Y" and "not just X but Y", "rather than" contrasts, "no X, no Y" pairs used for effect;
- triplets used purely for rhythm ("fast, simple and reliable"), stacked rhetorical questions;
- meta commentary about the slide, the course or the speaker; praise of the course or of honesty ("honest", "honestly", "real", "true" as filler);
- stock analogies repeated across sessions (a shop till, a recipe, a map) unless they carry the idea;
- slide text that is generic ("Key takeaways", "Putting it together"), spaced-caps style labels, or slogans.
A note should sound like a knowledgeable person talking to one student at a table. Specific beats general. Keep numbers and facts exactly right.

### 5. Re-check
Anything you changed must still be true. Recompute numbers with pandas if you touch them. Keep paragraph counts for animated slides (one opening paragraph plus one per click; the checker tells you the number of clicks).

## Limits
- Do not change slide types, figure names, code, outputs or lab cells unless a fact is wrong or a topic is missing.
- Do not rewrite for taste where nothing is wrong. Change what needs changing.
- Never use dashes, the word click, markdown or labels in notes (the checker enforces this).

## Reply (under 300 words)
Sessions reviewed; what you added or fixed for completeness; wrong cross-references or facts fixed (session and slide); how many ritual passages you rewrote; number of slop fixes by type; anything you could not resolve.
