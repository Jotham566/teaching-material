# Author brief: write one session of "AI and Data Science Professional"

You write the content for ONE two-hour session of a 24-session course, then prove it with the checker. You write one JSON file. A builder turns it into a PowerPoint deck, a student notebook and a solution notebook.

## The course and the students

Working professionals in Uganda, confident in Excel or Google Sheets, with no code and no statistics. They are adults after a work day. They need to feel clever, not lost. The tutor is one person, Jotham Wambi, who teaches live and READS YOUR NOTES ALOUD, so the notes must sound like a warm teacher speaking, never like a document.

Rules of the course design:
- Excel is the anchor. Every new idea arrives beside the spreadsheet thing it replaces. Say the spreadsheet word first, then the new word.
- Define every term in plain words before you use it. One idea per slide. Show the picture or the real data before the rule.
- Everything is free for the student and the tutor. Tools: Google Colab, Google Sheets (or Excel or LibreOffice), Python with pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib, seaborn, SQLite, GitHub, Streamlit Community Cloud, TensorFlow Playground, the sentence-transformers model all-MiniLM-L6-v2 run inside Colab. NEVER ask for a paid account, a paid API, an API key, Anaconda, Power BI, Docker, a GPU, or hosted inference. A free chat assistant may be mentioned as optional help, never required.
- Mixed Windows and Mac laptops, browser first. Notebooks run in Colab.
- All data is fictional and generated. Business setting: Uganda and East Africa. Currency UGX. Never invent a real company, person or patient.

## Where things are (host paths for Read and Write; the shell sees the same files under /sessions/nice-gallant-tesla/mnt/Business_AI/...)

Course root: `/Users/jothamwambi/Projects/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/AI and Data Science Professional/`

- `05 Course Maintenance/Authoring/Build/curriculum.py` the curriculum. Read your session's entry (title, question, result, outcomes, topics, lab, dataset) and the entries before and after it. You must cover the listed topics.
- `05 Course Maintenance/Authoring/Content/s07.json` THE EXEMPLAR. Read it first and copy its quality, structure and note style.
- `03 Learner Materials/Practice Files/data/` the generated data (CSV files, `lakeside.db` SQLite copy, `lakeside_for_sheets.xlsx`, `answer_key.json`, `DATA DICTIONARY.txt`, `policies/`). Open them with pandas. Compute every number you put on a slide. Never estimate and never remember a number.
- `05 Course Maintenance/Authoring/Build/figs_cache/catalog.json` the figure catalog (name, description, alt text). The PNGs are in the same folder. Look at any figure you plan to use (Read the PNG) so your bullets describe what is really drawn.
- `05 Course Maintenance/Authoring/Build/deckkit.py` the slide engine (read the slide types at the top if you need detail).

Your output file: `05 Course Maintenance/Authoring/Content/sNN.json` (NN = two-digit session number).

## The checker. Run it until it reports 0 HARD problems.

```
cd "/sessions/nice-gallant-tesla/mnt/Business_AI/AI and Data Science Professional/05 Course Maintenance/Authoring/Build" && python3 build_course.py check N
```
It builds your deck in memory (a slide whose text does not fit is a HARD problem: cut words, split the slide, or shorten code), lints every note, EXECUTES your pandas, numpy, matplotlib and SQL code against the real data and compares your slide output with the real output, and checks the structure. Also fix WARN lines where sensible. This machine has no scikit-learn, SciPy, statsmodels, torch or sentence-transformers and no internet. Code that uses them is only syntax-checked, so you must be extra careful with their APIs, and you must not show an output you cannot reproduce here (see "Outputs" below).

## Content schema

```
{
 "session": N,
 "notes_title": "...", "notes_outcomes": "...", "notes_words": "...",   // read-aloud notes for the three automatic slides
 "vocab": [[term, plain definition, spreadsheet equivalent or null], ...],   // 4 to 8 terms, no term used in another session
 "slides": [ ... 15 to 20 slides ... ],
 "lab": {"intro": "...", "cells": [...]}      // coding sessions
        // or {"intro": "...", "sheet_tasks": [{"task": "...", "answer": "..."}]}   // sessions 1 to 4
}
```
The builder adds the title slide, the outcomes and timetable slide, and the vocabulary slide for you. Your `slides` list follows them.

Required spine (in this order, with your own slides between):
1. First slide: type `check` as a recall or warm-up (two questions on the previous session; for Session 1 a warm-up about the students' own data experience).
2. Concept and demonstration slides: a mix of types (below).
3. At least one `trap` slide (a mistake that runs without error, or an error read aloud) and a code slide that shows the error where one is natural.
4. A `steps` slide for the lab (40 minutes).
5. A `check` exit slide (three questions, answers reveal one by one).
6. Last slide: `summary` with `next` naming the next session.

Also required: at least 5 animated slides (flow, cycle, compare, code with says, check, trap, figure with look, matrix); at least one figure from the catalog; coding sessions need at least 3 `code` slides.

### Slide types (fields; `notes` required on every slide)
- `concept`: title, lead (1 or 2 sentences), points [{h, t}] 2 to 4, optional `fig` (catalog name) and `alt`. With `fig` the points stack at left and the figure sits at right.
- `flow`: title, steps [{h, t}] 3 to 6, caption. Animated: one click per step.
- `cycle`: title, steps [{h, t}] 4 to 6, center. Animated.
- `compare`: title, left {h, points[]}, right {h, points[]}, verdict. Animated.
- `table`: title, header [], rows [[]], caption (optional), colw (optional widths), hl (optional highlighted row numbers). Static.
- `code`: title, lang ("python" or "sql"), code, output (optional real output), says [3 or fewer short explanations, optional], expect_error (true when the block must fail). Animated through the says. Keep lines under about 80 characters. Use `print()` for anything you want in the output; only the final bare expression of a block is displayed automatically. For SQL one SELECT per slide.
- `figure`: title, fig (catalog name), look [2 or 3 short observations, optional], caption (optional), alt. Animated through look.
- `stat`: title, stats [{n, label}] 2 to 4, caption. Static big numbers.
- `steps`: title, steps [4 to 7 short lines], tool, time, done. The lab slide.
- `trap`: title, looks, why, fix. Dark slide, animated.
- `check`: title, kicker, questions [{q, a}] 2 to 4. Answers reveal one at a time.
- `define`: title, definition, example, excel.
- `matrix`: title, cells {tp, fn, fp, tn} each (label, number), side, pos, neg. Confusion-matrix style, animated.
- `bar`: title, categories, series [[name, [values]]], look, caption. A native chart for one comparison.
- `erd`: title, tables [{name, cols ("*" prefix marks a key)}], layout [(col, row)] on a 3 by 2 grid, links, caption.
- `summary`: points [3], next.

Fit limits are real: body text is at least 15 to 16 points, so slides carry few words. Cards hold one or two short sentences. If a slide says too much, split it.

### Outputs and numbers
- A `code` slide's `output` must be what the code really prints (the checker compares line by line; you may show a subset of lines). Compute it by running the code.
- For code that needs scikit-learn, SciPy, statsmodels or any library missing here, do NOT write an `output` with numbers you cannot reproduce. Either omit `output`, or describe the result in the notes in approximate, safe terms using the facts below (for example "an AUC near 0.76"). Model facts you may quote are in `05 Course Maintenance/Authoring/Content/_facts.json` (a numpy logistic regression on a 75/25 split: AUC about 0.76 honest, 0.995 with the leaked column; confusion matrices at four thresholds; customer segments from k-means). They are stand-ins: scikit-learn will give close but not identical numbers, so say "about" or "close to" in the notes, and tell the student their own run will be near these but not the same. Other facts: 12.5 percent of loans default (87.5 percent repaid); OLS coefficients in `answer_key.json` (regression_weekly_orders) are exactly what statsmodels will print. Do not invent other model results.
- Every figure number on a slide (UGX values, counts, rates) must come from the data or answer_key.json. The checker lists large numbers it cannot trace in the code output; verify them yourself with pandas.

### Notes: a script to read aloud, word for word
Every slide needs `notes`. They are what Jotham reads aloud. Rules:
- First person, plain speech, contractions, short and medium sentences, warm and unhurried. Address the student as "you". "We" for what you do together.
- No stage directions, labels, headings, bullets, brackets, timings. Never write: click, "this slide", "next slide", "on the screen", "I ask", "a good answer", "the learner", "facilitator", "Sources:", URLs, dashes (use full stops and commas), markdown.
- Do not read the slide word for word. Refer to what is on it only where the student needs to find it.
- Questions to the student: say the question, then a short natural pause line, END THE PARAGRAPH, then give the answer in the next paragraph. Vary the pause lines across slides ("Take your time.", "Have a think.", "No rush.", "Think it over.", "Give that a moment.", "Sit with it for a second."). Do not use the same one twice in a session, and do not use "Take a moment with that" at all.
- Animated slides (flow, cycle, compare, code with says or output, figure with look, check, trap, matrix, bar with look): write an opening paragraph, then exactly one paragraph per click in order (blank line between paragraphs), then optionally a wrap-up paragraph. The checker tells you how many clicks a slide has. Static slides: 1 to 4 paragraphs.
- Length: 60 to 160 words a slide, hard limits 40 to 300. Title, outcomes and words notes: 60 to 120 words.
- Style: state things plainly. No "X, not Y" or "not just X but Y" or "rather than" contrasts. No dashes. No aphoristic closers. None of: genuinely, honestly, straightforward, delve, crucial, pivotal, robust, leverage. No hedged authorial voice. Do not praise the course.
- Say numbers the way you would speak them ("thirty thousand two hundred and twenty nine", "forty seven thousand shillings").
- Weave in sources or laws by name where natural (for example "the Data Protection and Privacy Act of 2019"); never read a URL.

### Slide titles
Say what the slide is about or what it shows. No trailing full stop. No "A way to think about" or other hedging. No method-in-the-heading boasting.

### The lab (coding sessions)
`lab.cells` is a list. Each item is `{"md": "..."}` or `{"code": "...", "starter": "..."}`.
- A task is: an `md` cell (the task in one or two sentences), then a `code` cell whose `code` is the full SOLUTION and whose `starter` is what the student sees (comments and blanks, with `# Your turn:` lines), then a `code` cell with no starter that is a CHECK: it asserts the answer, for example `assert len(jinja) == 3562, 'Use a double equals sign'` and prints `Task 1 correct`. Compute the expected values with pandas on the real data. The checker executes your solution cells and checks in order, so each notebook must run top to bottom with the solutions.
- 5 to 8 tasks. The setup cell is added automatically (it puts the CSV files in the working folder). Files in the working folder: branches.csv, products.csv, customers.csv, orders.csv, order_lines.csv, returns.csv, branch_weeks.csv, offer_test.csv, feedback.csv, orders_raw.csv, loans.csv, clinic_visits.csv, lakeside.db, and the policies folder.
- For model tasks (scikit-learn), check with tolerant ranges from the facts above (for example `assert 0.70 <= auc <= 0.85`) and fix random seeds (`random_state=42`).
- End with one `md` reflection or comparison task (for example check against Sheets, write one sentence).
- Sessions 1 to 4 (no code): `lab.sheet_tasks` is a list of {"task", "answer"} using `lakeside_for_sheets.xlsx` (a 2,000-order sample: answers differ from the full CSV, so compute the expected answers FROM THAT WORKBOOK with pandas read_excel). Session 1 may add `cells` for its single first Colab cell.

## Quality bar
- Each deck should take about 70 minutes to teach (concepts 30, live demonstration 25, plus recall and wrap-up); the lab is 40 minutes on top. Fifteen to twenty content slides.
- Teach with real Lakeside Mart, Nile Microfinance, clinic or feedback data from the files. Prefer one real finding per slide.
- Respect the vocabulary: use only words defined in this or earlier sessions. If you need a new term, define it on a slide first. Look at earlier sessions' topics in curriculum.py.
- Be accurate. Where you are unsure of a library function, use the simplest well-known form (pandas, scikit-learn and matplotlib documented basics).
- Do not add a slide type or a figure name that does not exist. If you need a diagram the catalog lacks, use a native slide type (flow, cycle, compare, table, erd, matrix).

When the checker shows 0 HARD problems, reply with ONLY: the session number, the slide count, how many animated slides, any WARN you left and why, and any fact you could not verify. Do not paste the content.


## Uganda Data Protection and Privacy Act, 2019 (the summary slides may use, and nothing beyond it)
It applies to anyone who collects, processes, holds or uses personal data in Uganda, and to data about Ugandan citizens handled elsewhere. The regulator is the Personal Data Protection Office (PDPO), an independent office under NITA. Seven principles: accountability to the data subject; fair and lawful collection and processing; collecting data that is adequate, relevant and not excessive; keeping it only as long as needed; quality of information; transparency and participation of the data subject; safety and security of the data. Data subject rights: access, to prevent processing, to prevent processing for direct marketing, rights in relation to automated decision-taking, and rectification, blocking, erasure and destruction. Always present it as a teaching summary and not legal advice. Cite no section numbers.
