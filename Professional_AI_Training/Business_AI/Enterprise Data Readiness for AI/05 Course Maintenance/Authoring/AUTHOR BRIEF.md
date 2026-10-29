# Author brief: write one session of "Enterprise Data Readiness for AI"

You write the content for ONE two-hour session of a 12-session course, then prove it with the checker. You write one JSON file. A builder turns it into a PowerPoint deck, a team notebook and a solution notebook, and the workshop tasks go into the participant workbook.

## The course and the room

Participants come as pairs or trios from one East African organisation (bank, insurer, telco, manufacturer, government body): a decision maker (CIO, CTO, chief data officer, head of operations, business owner) and one or two colleagues from data, IT or information management. The tutor is one person, Jotham Wambi, who teaches live and READS YOUR NOTES ALOUD, so the notes must sound like a warm, experienced colleague talking to a mixed table, never like a document.

The leader does not write code. The data colleague runs the technical steps in the team notebook after seeing them demonstrated. Therefore:
- Every concept is explained in plain words first, with the business consequence, then the mechanism. A leader must be able to follow every slide and make a decision from it. Use the technical word only after the plain one, and define it.
- Every session ends with a decision question that only a leader can answer (who owns it, what level is acceptable, what to fund).
- Code slides are the demonstration. They are short, readable by a non-programmer when the tutor explains them, and they print real results from the case data.
- All data is fictional. The case is Kitara Group, a bank and insurer in Kampala with a subsidiary in Nairobi (about 1,800 staff). Currency UGX. Never use a real company, person or phone number as an example. Real laws, regulators and standards may be named.
- Tools are free for tutor and participants. Never ask for a paid account, a paid API, an API key, Docker Desktop, a GPU or hosted inference. Colab and a spreadsheet are enough for every lab.

## Where things are (host paths for Read and Write; the shell sees the same files under /sessions/nice-gallant-tesla/mnt/Business_AI/...)

Course root: `/Users/jothamwambi/Projects/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/Enterprise Data Readiness for AI/`

- `05 Course Maintenance/Authoring/Build/curriculum.py`: your session's entry (title, question, result, outcomes, topics, lab, min_code) and its neighbours. You must cover every topic and every outcome.
- `05 Course Maintenance/Research/Research Notes.txt`: every external fact with its source and what is UNCONFIRMED. Use only facts from it, from the case data, or that you verify yourself by WebSearch. State forecasts and surveys as what they are (a forecast, a survey of N people). Never quote a statistic you cannot trace. The notes were gathered from search summaries, so for any law, licence or date that you put on a slide, run a WebSearch to confirm and hedge it when sources disagree ("reported", "as of October 2026").
- `04 Facilitator Materials/Benchmark and Design Report.docx` (run `pandoc -t plain` on it): the design intent, the five dimensions, the five levels, the tool licence table, what the session must achieve.
- `03 Learner Materials/Practice Files/data/`: the Kitara case data. Read `DATA DICTIONARY.txt` first. Compute every number you put on a slide from the files with pandas, or take it from `answer_key.json`. Never estimate and never remember a number. `kitara_search.py` is the search toolkit (chunking, BM25, a stand-in for embeddings, fusion, scoring); sessions 5 to 7 import and quote it (`import kitara_search as ks`; see its docstring).
- `03 Learner Materials/Workpiece Templates/`: the workbooks participants use. Refer to them by file name in the workshop tasks.
- `05 Course Maintenance/Authoring/Build/figs_cache/catalog.json`: the figure catalog (name, description, alt text). Read the description and LOOK at any PNG you plan to use (Read the file) so your words match what is drawn. Do not invent figure names.
- `05 Course Maintenance/Authoring/Build/deckkit.py`: the slide engine.
- A finished example of the JSON format and of the note style from a sister course: `/Users/jothamwambi/Projects/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/AI and Data Science Professional/05 Course Maintenance/Authoring/Content/s07.json`. Copy its structure and the quality of its notes, and adapt the audience (leaders as well as data staff). Its slide types, schema and rules are the same, with the changes below.

Your output file: `05 Course Maintenance/Authoring/Content/sNN.json` (NN = two-digit session number).

## The checker. Run it until it reports 0 HARD problems and 0 warnings you can fix.

```
cd "/sessions/nice-gallant-tesla/mnt/Business_AI/Enterprise Data Readiness for AI/05 Course Maintenance/Authoring/Build" && python3 build_course.py check N
```
It builds your deck in memory (a slide whose text does not fit is a HARD problem: cut words, split the slide, or shorten code), lints every note, EXECUTES your Python and SQL code against the real data and compares your slide output with the real output, and checks the structure. This machine has pandas, numpy, matplotlib, pypdf, pdfplumber, pytesseract, sqlite and reportlab. It has NO sentence-transformers, chromadb, duckdb, pandera, great_expectations, presidio, dagster, docling, ragas, pyarrow, scikit-learn or internet. Code that imports them is only syntax-checked, so be extra careful with their APIs (use the simplest documented form), and never show an `output` you cannot reproduce here. The code runs with the data folder as the working directory, so use paths like `docs/policies/...`, `customers.csv`, and `import kitara_search as ks`.

SQL slides (`lang: sql`) run against an in-memory SQLite database holding customers, sources, docs_metadata, users, eval_questions, mobile_money_log, lineage_edges and readiness_evidence.

OCR in `ks.load_corpus` takes time. Cache results with `ocr_cache` (see the docstring) or load only what you need, so a single code block runs in well under a minute.

## Content schema

```
{
 "session": N,
 "notes_title": "...", "notes_outcomes": "...", "notes_words": "...",   // read-aloud notes for the three automatic slides
 "vocab": [[term, plain definition, where it appears at Kitara or null], ...],   // 4 to 8 terms, each defined in one session only
 "slides": [ ... 15 to 20 slides ... ],
 "lab": {"intro": "...", "workshop": [{"task": "...", "example": "..."}], "cells": [...]}
}
```
The builder adds the title slide, the outcomes and timetable slide ("By the end of today" plus how the two hours run) and the vocabulary slide. Your `slides` list follows them. The session shape is: Case and recall 10, Teaching 30, Live demonstration 25, Break 5, Workshop on your organisation 40, Decision and wrap-up 10.

Required spine (in this order, with your own slides between):
1. First slide: type `check`, a recall or warm-up with two questions on the previous session (for Session 1, a warm-up about the participants' own experience with data and AI). It is the "Case and recall" ten minutes. The second slide may show the Kitara case situation for today.
2. Concept slides, then demonstration slides, in a mix of types.
3. At least one `trap` slide (a mistake that looks fine, or a failure read aloud) and, where natural, a code slide that fails on purpose (`expect_error`).
4. A `steps` slide for the workshop (40 minutes): title starts "Workshop:", `tool` names the workbook and notebook (for example "Data Inventory workbook and team notebook"), `time` "40 minutes", `done` says what exists when finished.
5. A `check` exit slide with three questions, the third one a DECISION QUESTION for the leader ("Who in your organisation signs off ...").
6. Last slide: `summary` with `next` naming the next session as curriculum.py titles it (for Session 12, say what happens after the course).

Also required: at least 5 animated slides (flow, cycle, compare, code with says, check, trap, figure with look, matrix); at least one figure from the catalog; the number of code slides in `min_code`.

### Slide types
Same as the sister course: `concept` (title, lead, points [{h, t}], optional fig and alt), `flow`, `cycle`, `compare`, `table`, `code` (title, lang, code, output, says, expect_error), `figure` (title, fig, look, caption, alt), `stat`, `steps`, `trap` (title, looks, why, fix), `check`, `define` (title, definition, example, excel: here the `example` field is shown under "At Kitara Group" and the `excel` field under "In your organisation": write a question or prompt for the participant), `matrix`, `bar`, `erd`, `summary`. Every slide needs `notes`. Fit limits are real: body text is at least 15 to 16 points, so slides carry few words. If a slide says too much, split it.

### Outputs and numbers
- A `code` slide's `output` must be what the code really prints. Compute it by running the code, and show a subset of lines if long.
- A figure slide's `look` lines must describe what is really in the PNG.
- Use `ks` outputs (recall, ranks) exactly as the code produces them; the stand-in meaning scorer is not a real embedding model, so say so wherever its results are shown ("a stand-in so the numbers are reproducible; your embedding model will differ").
- External numbers: only from the research notes or verified by you, each with its source named in the notes in spoken form ("Gartner's February 2025 forecast", never a URL), and each described as a forecast or survey where it is one.
- Laws: teaching summary, not legal advice. Cite no section numbers. For Uganda use the Data Protection and Privacy Act, 2019 (see the box at the end). For Kenya, Rwanda and Tanzania, state only the points listed in the Benchmark and Design Report section 4 and hedge them ("reported", "check the current text").

### Notes: a script to read aloud, word for word
Every slide needs `notes`. They are what Jotham reads aloud. Rules:
- First person, plain speech, contractions, short and medium sentences, warm and unhurried, for a room of senior people and their technical colleagues. Address them as "you". "We" for what we do together. Respectful, never talking down, and never hype.
- No stage directions, labels, headings, bullets, brackets, timings. Never write: click, "this slide", "next slide", "on the screen", "I ask", "a good answer", "the learner", "facilitator", "Sources:", URLs, dashes (use full stops and commas), markdown.
- Do not read the slide word for word.
- Questions to the room: say the question, a short natural pause line, END THE PARAGRAPH, then give the answer in the next paragraph. Vary pause lines ("Take your time.", "Have a think.", "No rush.", "Think it over.", "Give that a moment.", "Sit with it for a second.", "Let's hear your answer first."). Do not use the same one twice in a session.
- Animated slides (flow, cycle, compare, code with says or output, figure with look, check, trap, matrix, bar with look): an opening paragraph, then exactly one paragraph per click in order (blank line between paragraphs), then optionally a wrap-up. The checker tells you the click count. Static slides: 1 to 4 paragraphs.
- Length: 60 to 160 words a slide, hard limits 40 to 300. Title, outcomes and words notes: 60 to 120 words.
- Style: state things plainly. No "X, not Y", "not just X but Y", "rather than" contrasts, no "no X, no Y" pairs for effect. No dashes. No aphoristic closers ("and that is the whole point"). No filler openers ("Here's the thing", "So,", "Now,", "Let's dive in"). None of: genuinely, honestly, straightforward, delve, crucial, pivotal, robust, leverage, journey, landscape, unlock, game-changer. No meta commentary about the course or about honesty. Specific beats general: name the Kitara file, the number, the department.
- Do NOT reuse the ritual openers of other sessions. The title notes, outcomes notes, exit check notes, summary notes and workshop notes of every session must open differently and be specific to the session's content. The checker fails when one sentence repeats across more than two sessions.
- Numbers are spoken the way you say them ("thirty thousand shillings", "twenty eight days").
- Mention laws, standards and surveys by name where natural; never read a URL.

### Slide titles
Say what the slide is about or what it shows. No trailing full stop. No hedged authorial titles ("A way to think about ..."), no method-in-the-heading, no stock titles ("Key takeaways", "Putting it together"). Use "Summary" for the final slide and "Questions to finish" for the exit check.

### The lab
`lab.intro`: one or two sentences about the workshop and the notebook.
`lab.workshop`: 3 to 7 items, each `{"task": "...", "example": "..."}`. These are the tasks participants do on their OWN organisation (or on Kitara first), with the named workbook from Workpiece Templates, in the 40-minute workshop. `example` is the worked Kitara answer, using real numbers from the case data (it goes into the tutor's answer book). The tasks must produce what curriculum.py names as the session `result`.
`lab.cells`: the team notebook, a list of `{"md": "..."}` and `{"code": "...", "starter": "..."}` items. A task is an `md` cell, a `code` cell whose `code` is the full SOLUTION and `starter` is what the team sees (comments and blanks, with `# Your turn:` lines, no solution leaked), then a `code` cell with no starter that is a CHECK asserting the answer with a helpful message and printing "Task N correct". 4 to 6 tasks, ending with an `md` cell that asks a question for the leader to answer from the results. The setup cell is added automatically (it extracts data.zip, so the files above, `docs/` and `kitara_search.py` are in the working folder). Compute expected values on the real data. Model-free tasks only; for heavy-library cells (sentence-transformers and so on) use the simplest documented API, put them last, and make the rest of the notebook work without them.

## Quality bar
- Each deck takes about 70 minutes to teach (teaching 30, demonstration 25, recall and wrap-up); the workshop is 40 minutes on top. Fifteen to twenty content slides.
- Teach with the real Kitara data and documents. One real finding per slide where possible.
- Vocabulary: define a term in plain words on first use. Do not use a term defined in a later session without a one-phrase explanation.
- Be accurate. Where unsure of a library function, use the simplest well-known form.
- Do not add a slide type or figure name that does not exist.
- The five dimensions (use cases and sponsorship; data: inventory, quality and metadata; platform and pipelines; protection and law; people and governance) and the five levels (ad hoc, developing, defined, managed, optimised) are used throughout. Tie each session to the dimension(s) it moves.
- Three workpieces: Session 2 baseline scorecard, Session 7 search pilot report, Session 12 roadmap and board presentation. Mention the next workpiece when it is near.

When the checker shows 0 HARD problems, reply with ONLY: the session number, the slide count, how many animated slides, any WARN you left and why, and any fact or API you could not verify. Do not paste the content.

## Uganda Data Protection and Privacy Act, 2019 (the summary slides may use, and nothing beyond it)
It applies to anyone who collects, processes, holds or uses personal data in Uganda, and to data about Ugandan citizens handled elsewhere. The regulator is the Personal Data Protection Office (PDPO), an independent office under NITA-U. Seven principles: accountability to the data subject; fair and lawful collection and processing; collecting data that is adequate, relevant and not excessive; keeping it only as long as needed; quality of information; transparency and participation of the data subject; safety and security of the data. Data subject rights: access, to prevent processing, to prevent processing for direct marketing, rights in relation to automated decision-taking, and rectification, blocking, erasure and destruction. Controllers register with the PDPO and report breaches to it promptly. Processing or storage outside Uganda is reported to need an equivalent level of protection or the person's consent. Always present it as a teaching summary and not legal advice. Cite no section numbers.
