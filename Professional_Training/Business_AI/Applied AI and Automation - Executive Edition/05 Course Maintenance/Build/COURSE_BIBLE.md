# Applied AI and Automation for Executives, Executive Edition: course bible (version 3, 5 to 6 November 2026)

Read this first, then `V3_AUTHORING_BRIEF.md`. It fixes what the course is, who it is for, the 14 sessions, the case company, the file names and the writing rules, so that every part of the edition agrees with every other part. `content/s00.py` (Session 0) and the other `content/sNN.py` files are the sources for the slides and the documents.

## 1. What the course is

- A private or small-group course (1 to 5 learners) for company executives and owners in any industry, including financial managers, taught by Jotham Martin Wambi (KLAi Professional Learning, Kampala). It is not a law course: examples spread across finance, operations, customer service, HR, sales, compliance and legal.
- 14 sessions of 2 hours, 28 hours in all, plus Session 0 (the introduction, delivered first, which hands out the Course Handbook). Dates and frequency are agreed with the learners. Format: in person, online or at the learner's workplace. Works for one learner or a group.
- No coding labs. Sessions 1 to 11 teach how AI works (a touch of the maths, machine learning, foundation models, open weights, prompting, retrieval and fine-tuning, failures, agents). The lecturer runs the demonstrations while the learner watches and may join in on a laptop with an AI account. Each of these sessions has a paper exercise (no computer) and ends with a one-page take-away sheet. Sessions 12 to 14 are practicals where the learner works on their own organisation and the documents and templates are created.
- Nothing to prepare before Session 1: read the Course Handbook, bring a laptop and an AI account to join the demonstrations.
- No tests, no marks, no grades, no required homework (anything between sessions is optional). The Handbook phrase is "There are no tests and no required homework". A 30, 60 and 90 day follow-up checks what happened at work.
- Outcomes the executive keeps: a take-away sheet from every session; from the practicals a mapped workflow with an hours-saved estimate and a costed business case, a first AI use policy, a risk register and vendor question list, a readiness scorecard, a data roadmap and a 90-day plan; and the confidence to question vendors and supervise a pilot.
- Never mention the course fee anywhere (slides, notes, guides, templates). Only mention a price if the owner asks for a flyer.
- Automation tools (Zapier, Make, n8n, Power Automate, Copilot Studio, agent builders) are discussed as options only. The course shows two recorded automations on the same twelve customer messages (rule-based and AI with a person checking) in Session 12 and teaches no tool build.
- Legal and tax material from the earlier edition is an optional lane, not part of this edition.

## 2. The 14 sessions

Each session: 120 minutes. Technical clock (Sessions 1 to 11): 10 recall, 35 the ideas (picture, analogy, calculation of at most three numbers, real term), 25 demonstration by the lecturer, 5 break, 25 paper exercise, 15 what this means for your work (decision slide), 5 close. Practical clock (Sessions 12 to 14): 10 recall, 20 idea, 15 demonstration, 5 break, 55 the learner works, 10 decision, 5 close. Session 14 closes the course (`keep_returns` True, `next_label` 'After the course', one-learner variant in the facilitator notes).

| No. | Title | The learner keeps |
|---|---|---|
| 0 | AI and machine learning: the map before the route | The Course Handbook, with today’s ideas, a glossary and what to prepare. Read it before Session 1, which begins with how a machine sees. |
| 1 | Seeing: pixels, features and neurons | A one-page sheet: how a picture becomes numbers, the payment-risk neuron worked by hand, and the digit results. |
| 2 | Learning from examples: types of machine learning, decision trees, nearest neighbours | A one-page sheet: the four types of learning, a tree read as rules, nearest neighbours, and the honest scores from today’s run. |
| 3 | Measuring a model: accuracy, precision, recall, F1, ROC and AUC, thresholds, baselines, overfitting | The vendor question sheet: ten questions about the numbers behind any AI claim. Keep it next to every proposal you read. |
| 4 | Words as numbers: bag of words, TF-IDF, embeddings and distance | The distance cheat sheet: four ways to say how close two things are, each with its picture, its rule and when to use it. |
| 5 | Language models: tokens, attention and next-word probability | A one-page sheet: the next-word loop, the softmax recipe, what temperature does and five questions to ask about any language-model answer. |
| 6 | Foundation models: pretraining, post-training, model families, reasoning and multimodal models, benchmarks | A one-page model comparison grid for your own tasks, with the questions to ask of a model card and a benchmark claim. |
| 7 | Open weights, file formats, size and running cost | A one-page rent, host or own decision sheet, with the memory sum and the licence questions to ask. |
| 8 | Prompting and reasoning models | A reusable prompt template and a prompt log, so that every prompt you keep has been tested. |
| 9 | Giving a model your knowledge: retrieval-augmented generation, long context and fine-tuning | A one-page decision tree: prompt first, then retrieve, then fine-tune, and the test that tells you when to climb. |
| 10 | When models fail, and how to check them | A five-step check routine and a test-set template, each on one page. |
| 11 | Agentic AI: tools, loops, MCP, autonomy and guardrails | Your Tool Boundary Sheet: what an agent may read, write, send and spend, who approves, the log and the off switch. |
| 12 | Workflow mapping (practical) | Your mapped workflow, the choice for each step, your assistant sketch and the hours-saved estimate in the Business Case Workbook. |
| 13 | Governance and buying (practical) | Your Risk Register, your AI Use Policy draft, your Vendor Question List with five questions, and your page of questions for the lawyer. |
| 14 | Data readiness assessment, roadmap and 90-day plan (practical) | Your inventory and scorecard, your roadmap with its risks and decisions, and the Follow-up Kit: Check-in Form, Results Tracker and Sponsor Briefing. |

Every number or output shown from a demonstration is a recorded run in `demo_runs/`. Authored slides per technical session: 14 to 20 (lint limit 22), at most one text-only slide, at least 10 with a purpose-drawn diagram. The take-away content is also stored in `facilitator['takeaway']` and written to `03 Learner Materials/Take-away Sheets.docx` by `kit/make_docs.py`.

## 3. The case company: Nile Valley Foods Ltd (NVF)

A fictional food distributor in Jinja, Uganda, founded 2014. About 85 staff. Distributes maize flour, cooking oil, rice, sugar and beans to about 320 shops and 14 supermarkets across Eastern Uganda from depots in Jinja and Mbale. 9 trucks. Uses Google Workspace (Gmail, Sheets, Drive), an accounting package, WhatsApp Business for orders and MTN MoMo and Airtel Money for payments. All names, firms and figures are fictional and labelled so.

People: Managing Director Sarah Namukasa; Sales Manager Peter Okello; Finance Manager Joseph Mugisha; Operations Manager Grace Akello; HR Officer Mary Nabirye; Customer Service Lead David Kato; Warehouse Supervisor Ibrahim Ssemwogerere. Suppliers: Busoga Oils Ltd (cooking oil), Elgon Millers Ltd (maize flour), Tororo Rice Growers Cooperative, Lakeside Logistics Ltd (transport), Pearl Packaging Ltd. Regions in sales data: Jinja, Mbale, Iganga, Tororo, Soroti, Kamuli.

Use NVF for examples where the learner's own task is not the point. Use the learner's own company for practice. Do not invent real companies, real people or real statistics.

## 4. Files that exist (use these exact names; do not reference others)

Generated from Build: `02 Class Slides/NN - Title.pptx` (15 decks, Session 0 to 14), `01 Course Overview/Course Overview` and `Course Map for Approval (5 Nov 2026)`, `00 Start Here/Start Here`, `03 Learner Materials/` (`Learner Workbook`, `Take-away Sheets`, `Course Handbook`), `04 Facilitator Materials/` (`Facilitator Guide`, `Presenter Script`, `Rehearsal Record`, `Answer Keys/`, `Twelve-Message AI Demonstration Results (4 Nov 2026).md`, which Session 12 uses).

Practice Files are in `03 Learner Materials/Practice Files/`; keys and facilitator files are in `04 Facilitator Materials/`.

`01 Case Company/`: `Company Profile.pdf`; `customer_messages.csv` (40 messages); `supplier_invoices.csv` (60 rows); `weekly_sales.csv`; `supplier_agreement_busoga_oils.docx` and `.txt`; `review_playbook_supplier_agreements.txt`; `cv_pack/`; `staff_handbook_excerpt.txt`; `meeting_notes_raw.txt`; `vendor_proposal_orbitdesk.txt` (fictional proposal with red flags, Session 13); `supplier_email_with_instruction.txt` (hidden instruction, Sessions 10 and 11); `market_notes_1.txt` to `market_notes_4.txt`; `supplier_quote_pearl_packaging.txt`.

`Templates/` (all KLAi branded), with the session that uses each: Reusable Brief Template (8), Reliability Test Record (10), Tool Boundary Sheet (11), Business Case Workbook, Use-Case Scorecard and Task Card (12), AI Use Policy Template, Risk Register and Vendor Question List (13), Information Inventory, 90-Day Roadmap (14). Document Review Table and Automation Test Log remain as optional templates. Generated by `templates_gen/`; checked by `verify_templates.py`.

`Follow-up Kit/` (Session 14): `30-60-90 Check-in Form.docx`, `Results Tracker.xlsx`, `Sponsor Briefing.docx`.

Optional archived material, not part of the taught course: `Archive/v2_before_technical_2026-11-05/practice_files/02 Zapier Build` and `03 Apps Script Build` (guides, scripts, tests and rehearsal checklists from the earlier twelve-session edition). The earlier versions of the sessions, decks and documents are in `05 Course Maintenance/Archive/`.

Build folder: `V3_AUTHORING_BRIEF.md`, `demo_runs/` (recorded runs, scripts, inputs and `sources_sNN.md`), `kit/` (builders; `diagrams_tNN.py` per session), `Case Runs/` (the earlier recorded runs F1 to F7).

## 5. Facts that are safe to teach (all from research of 1 Nov 2026; checked against search summaries, to be re-checked in a real account before teaching)

- McKinsey, The State of AI 2025: 88% of companies use AI in at least one function; about 39% report any effect on profit (large global firms).
- Zapier, Google Apps Script and the Gemini API are no longer taught. Their facts are kept only in the optional archived practice folders and must be re-checked in a real account before anyone uses them.
- Other tools (options only, never taught as a build): Microsoft Power Automate and Copilot Studio (licensed per user or by credits, best if the company already uses Microsoft 365); Make (billed per operation, visual canvas); n8n (billed per execution on cloud, can be self-hosted, most technical); agent builders in ChatGPT, Gemini and Claude. Never put prices on slides.
- Risks: over-broad account permissions; vendor and AI provider process the data; prompt injection through incoming emails or documents (OWASP LLM Top 10 2025 ranks it first); cost runaway from loops; ownership when staff leave.
- Governance vocabulary: NIST AI RMF 1.0 (Govern, Map, Measure, Manage) and its Generative AI Profile; ISO/IEC 42001 (certifiable AI management system); OECD AI Principles; African Union Continental AI Strategy (2024); EU AI Act applies only if the company serves the EU (AI literacy duty already applies there). Uganda has no AI statute: the Data Protection and Privacy Act 2019 applies in full to personal data in AI use; the national AI strategy status must be re-checked the week of teaching.
- Evidence that pilots stall: Deloitte 2026 (only about one in five has a mature governance model for agents); MIT NANDA 2025 (most pilots show no measurable return; not peer reviewed); Gartner (forecast: over 40% of agent projects cancelled by 2027). These are large-firm global figures; say so.
- Customer-service study (Brynjolfsson and others, NBER 2023): about 14% more issues resolved per hour, most for novices. Use only if a slide needs a sourced benefit.
- Do not quote any other statistic. Do not quote prices. Do not name a product as best.

## 6. Honesty rules for demonstrations

- Never write an AI output as if it was observed. Use "illustrative" or "typical" or "you will check the live result". The instructor records real runs in `Rehearsal Record.docx`.
- Label simulations and saved runs apart from live runs.
- A demonstration may fail live. Every demonstration has a fallback (a saved run or a paper walk-through) written in the facilitator section.
- Never assume the learner has a paid AI account or enterprise access. Name no tool as required. The course works with any one assistant the learner already has (for example ChatGPT, Claude, Gemini or Copilot) plus the two build tools.

## 7. Writing rules

- Audience: busy executives. Plain words. Short sentences. Explain every new word the first time.
- Slide titles state the point. One idea per slide. At most about 45 words on a slide (the lint limits are per slide kind). Body text is 18 pt or larger.
- Notes are a spoken script in the first person ("I show", "Take fifteen minutes"). Address the learner as "you". No stage directions, no brackets, no "click". 60 to 130 words per slide.
- No "X, not Y" constructions (for example "it is a tool, not a person"). State the fact directly. No em dashes. Never use "honestly", "genuinely", "straightforward", "dive into", "unlock", "journey", "embark", "game-changer", "leverage".
- No exam, marks or grading language. The word "test" is fine for testing an automation or a prompt.
- Gender: the learner's gender is unknown. Use "the learner" or "you". Do not use he or she for the learner.
- Examples: NVF for illustration, the learner's own company for practice. Money in UGX with the abbreviation UGX and a space before the number (UGX 500,000).
- Do not invent statistics, company claims or quotes. Use only the facts in section 5.

## 8. Session file format (content/sNN.py defines SESSION)

Copy the shape of `content/s00.py` for voice and slide kinds and of a technical session (for example `content/s03.py`) for structure. Required keys: num, title, question, outcomes (3), keep, next, clock (list of (minutes, label) summing to 120), plan_caption, words (3 to 5 pairs), cover_note, outcome_note, plan_note, words_note, keep_note, recall (2 or 3 pairs of (question, expected answer) about the PREVIOUS session; Session 1 recalls Session 0), slides (14 to 20, lint limit 22), workbook (question, steps, fields, reflect, decision), facilitator (prep, demo_steps, fallback, probes, misconceptions, questions, rescue, takeaway; one_learner in Session 14), needs_files (optional); keep_visual, keep_title and takeaway (the one-page sheet).

Slide kinds and fields: see the docstring of `kit/deck.py`. Diagram kinds (the `visual` or `steps` data) are listed in `kit/diagrams.py`: flow (steps with head, text, icon), stack (layers), matrix (x_label, y_label, quadrants, points), cycle (items), bars (items with label and value), timeline (items with when and what), icons (items with icon, head, text), ladder. Icons available: person, shop, laptop, notebook, folder, tag, bag, cloud, magnifier, calculator, clock, coin, bars, receipt, check, cross, phone, calendar, home, gear, lock, pin, mail, shield, people, doc, chart, key, robot.

Slide limits: statement up to 4 points; list up to 7 items; steps 3 to 5; table up to 8 rows; decision 3 or 4 options; practice 3 to 5 steps. Use a variety of kinds; about a third of the slides should carry a diagram. Include at least: one demonstration, two or three practice slides on the learner's own task (minutes sum to about 45), one decision slide, and one slide that shows a finished example from NVF.

Build and check: `python3 kit/lint_content.py N` then `python3 kit/deck.py N` (set PPTX_SKILL_SCRIPTS=/sessions/focused-youthful-einstein/mnt/.claude/skills/pptx/scripts). Render with soffice and look at every slide; fix overlaps and long titles (titles over two lines are shortened). Do not edit files in `kit/`; if you need a new diagram kind or slide kind, say so in your report.

## 9. Branding

KLAi: black, white, red #AE2525 (attention) and gold #E0BE36 (the thing to look at; as a fill behind black text). Lato. No stock clip-art. Hairline outlines, almost no tinted fills, no accent stripes under titles. The cover is black with the KLAi logo. The builder applies all of this; do not fight it.

## 10. Visual standard (added 1 Nov 2026, after the visual audit)

The first build was too text-heavy: only 21 percent of slides carried a real diagram. The standard now: at most ONE text-only slide in a deck; at least 7 slides with a real diagram (images named x_*); every other slide uses pictogram rows or a drawn example. Check with `python3 kit/visual_report.py` after `kit/deck.py`.

New fields (all optional unless marked):
- practice: `example` (REQUIRED) is a diagram dict drawn on the right: what the finished page looks like with NVF example values. Use kind `sheet` ({headers, rows, hl:[row, col]}; 3 to 5 columns of short text, 2 to 4 rows; the columns must match the real template in Templates/), `card` ({title, fields:[{label, value}]}, 3 to 5 fields), `bubbles`, `versus`, `bars`, `flow`. Size on the slide is 5.0 x 3.5 inches, so keep text short. `example_alt` is optional.
- demo: `visual` (REQUIRED) is a diagram dict drawn on the left (7.3 x 3.9 inches): a `flow` of what the instructor does, `bubbles` for messages, `stack`, `versus`, `icons`. `show` may then be omitted; `watch` stays on the right.
- decision: each option may carry `icon` (default check, chart, pin, shield).
- list, statement: `icons` list, one pictogram name per item (default is chosen by keyword and is often wrong: set it). statement points are now drawn as icon rows.
- table: `icons` list, one per row (or False to switch off). The first column gets a pictogram.
- stat: draws a `waffle` automatically when `big` ends in %; or give `visual`.
- compare: `icon` in left and right dicts.
- session level: `word_icons` (list, one per word), `outcome_icons` (list of 3), `keep_visual` (a diagram dict, 4.1 x 4.5 inches, usually a `card` or `sheet` of the artefact the learner keeps).
- New diagram kinds: `sheet`, `card`, `waffle` ({filled, label}), `bubbles` ({items:[{who, text, tag, red, hl}]}), `versus` ({left:{head,big,unit,icon}, right:{...}, middle}).
- Icons: person, shop, laptop, notebook, folder, tag, bag, cloud, magnifier, calculator, clock, coin, bars, receipt, check, cross, phone, calendar, home, gear, lock, pin, mail, shield, people, doc, chart, key, robot.

## 11. Teachability standard (added 1 Nov 2026, after the coherence and flow review)

The instructor must be able to teach from the slides, the Presenter Script and the Facilitator Guide alone, in a calm expert voice.
- Facilitator fields now used by the Guide: `prep`, `demo_steps` (complete and numbered: name the exact files, ids and wording to use), `fallback` or `fallbacks`, `misconceptions`, `questions`, `rescue`, and NEW `probes` (list of (a question a learner may ask, a safe accurate answer); 4 to 6 per session; hedge legal and technical claims honestly: 'my understanding is X; confirm with your lawyer'), and for Session 12 NEW `one_learner` (list of steps for a one-learner group). `landmarks` is no longer used: the Guide prints a slide map automatically from the deck, so never write slide numbers by hand anywhere.
- Session fields NEW: `keep_title`, `next_label` (default 'Next session'), `plan_title`, `keep_returns` (True only for Session 14, with next_label "After the course"). Every close returns to the cover question automatically (the builder adds it).
- Recall slides, words slides, plan slides and the close are partly generated by the builder; do not repeat their text in your notes. Plan notes: write one short paragraph that names the three or four biggest parts of the clock in words (the builder adds the full clock only if you do not).
- Voice: no stock filler ('Nobody is being tested', 'That moment is gold', 'This is the most important', 'Here is how I would answer it'); no homework (anything the learner does between sessions is called 'optional'); one meaning per word: 'task' means the learner's own work task; 'prompt' is anything you type, 'brief' is a prompt written once in seven parts and reused, 'assistant' is the product, 'model' is the engine inside it; 'trigger' is the event that starts an automation.
- Do not over-claim. Say 'can' and 'often' for AI behaviour; say 'cut down' not 'remove'; never say a tool 'does not look up facts' without 'unless search, files or memory are switched on'; never say a control 'works every time'; never imply one named product is the one that trains on your data: the same five account questions apply to every product and the answers depend on the plan.
- Every learner-facing slide carries one idea. Every session has one place before the break where each learner speaks or decides.
- Numbers (Session 12 business case, from `demo_runs/s12/business_case_output.txt` and the Business Case Workbook): inputs 4 runs a month, 90 minutes by hand, 10 minutes own time and 20 minutes review with the routine, share of runs with an error 0.4, share of errors removed 0.6, cost of one error UGX 150,000, hourly cost UGX 30,000; hours saved a month 5.33; monthly benefit UGX 304,000, monthly cost UGX 145,000, one-off cost UGX 480,000; payback 3.02 months; 12-month net UGX 1,428,000; after a 30% haircut UGX 333,600; break-even haircut 0.391. Teach plan against measurement. The Template text must agree with these figures.
- Dates: the 90-day plan starts on 1 February 2027: day 30 is 3 March 2027, day 60 is 2 April 2027, day 90 is 2 May 2027.
- Files added in the v2 pass and still used: `Practice Files/01 Case Company/supplier_quote_pearl_packaging.txt`. The Apps Script file `last_month_summary_by_hand.csv` belongs to the archived optional folder.
