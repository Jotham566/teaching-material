# Applied AI and Automation for Executives: course bible

Read this first. It fixes what the course is, who it is for, the twelve sessions, the case company, the file names and the writing rules, so that every part of the edition agrees with every other part. Session 1 (`content/s01.py`) is the worked model: copy its structure, its voice and its level of detail.

## 1. What the course is

- A private or small-group course (1 to 5 learners) for company executives and owners in any industry, taught by Jotham Martin Wambi (KLAi Professional Learning, Kampala). Not for teenagers and not only for lawyers.
- 12 sessions of 2 hours, 24 hours in all. Dates and frequency are agreed with the learners. Format: in person, online or at the learner's workplace.
- No tests, no marks, no grades, no homework required. Progress is shown by what each executive builds and keeps. A 30, 60 and 90 day follow-up checks what happened at work.
- Every learner brings ONE real recurring task from their own company in Session 1 (the "own task"). It runs through every session: choose and measure it (1), test it for mistakes (2), brief an AI tool for it (3), prepare its information (4), review its documents (5), automate it with Zapier (6), set its limits (7), build and measure it with Apps Script (8), write its risks and the company policy (9), question vendors for it (10), write its business case (11), show it and plan 90 days (12).
- Outcomes the executive keeps: a written AI-use policy, two or three working automations, a costed business case and a 90-day roadmap, and the confidence to question vendors and supervise a pilot.
- Never mention the course fee anywhere (slides, notes, guides, templates). Only mention a price if the owner asks for a flyer.
- Build tools: ZAPIER (Session 6) and GOOGLE APPS SCRIPT (Session 8) are the two tools the learners use. Power Automate, Make, n8n, Microsoft Copilot Studio and agent builders are discussed as options only (Session 7 and Session 10).
- Legal and tax material from the earlier edition is an optional lane, not part of this edition.

## 2. The twelve sessions

Each session: 120 minutes. Default clock (minutes): 10 recall and check-in (Session 1: welcome), 25 idea, 20 demonstration, 5 break, 45 the learner's own task, 10 decision, 5 close. Sessions 6 and 8 are build sessions and use a build clock (see below).

| No. | Title | Question | The learner keeps |
|---|---|---|---|
| 1 | Where AI fits in your business | Which tasks in my company should AI touch first? | Use-case scorecard and one-page task card with baseline |
| 2 | How AI works and where it fails | When can I trust what an AI tool tells me? | Reliability test record for the own task |
| 3 | Working with AI tools | How do I brief an AI tool and check what it returns? | A reusable brief and one checked result for the own task |
| 4 | Your information | What does the AI need to know, and who may see it? | Information inventory and three sample inputs, each marked by sensitivity |
| 5 | Reviewing documents | How can AI help me review documents without missing what matters? | A source-linked review table and a review prompt pack |
| 6 | Build 1: a no-code workflow | Can I build a workflow that drafts, waits for my approval and logs the result? | A working Zapier workflow with an approval step, a test log, an owner and an off switch |
| 7 | Agents and controlled actions | What may an automation do on its own, and what needs me? | A tool boundary sheet and stop conditions; a choice of tool family |
| 8 | Build 2: a script and its measurement | Does my automation really save time and cut errors? | A working Apps Script automation, a measured test, a time and error comparison with the baseline |
| 9 | Risk, security and the law | What could go wrong, and what rules should my company set? | Risk register for the own task and a first draft of the company AI-use policy |
| 10 | Buying and oversight | How do I question a vendor and decide build, buy or partner? | A vendor question list and a review of a sample proposal |
| 11 | The business case | Is it worth doing, and what would change my mind? | A costed business case workbook and a one-page summary |
| 12 | Demo day and your 90-day roadmap | What will I do in the next 90 days, and who will own it? | A presented result, a 90-day roadmap and the follow-up kit |

Session 6 build clock: 10 recall and setup check, 20 idea (trigger, action, approval), 15 instructor builds a small Zap step by step, 5 break, 60 the learner builds their own Zap with test messages, 10 test log and decision.
Session 8 build clock: 10 recall, 15 idea (what a script is, secrets, triggers), 20 instructor walk-through of the supplied script, 5 break, 60 learner adapts the script to their own sheet and measures it, 10 results and decision.
Session 12 clock: 10 setup, 70 presentations (8 minutes each plus questions; with one learner use a guest such as a colleague or the instructor's panel), 5 break, 25 roadmap, 10 follow-up plan and close. Adjust group size.

Authored slides per session: 11 to 13 (the builder adds a cover, outcome, plan, recall, words and keep slide automatically). Total deck about 17 to 19 slides, of which about 6 are practice, decision or demonstration.

## 3. The case company: Nile Valley Foods Ltd (NVF)

A fictional food distributor in Jinja, Uganda, founded 2014. About 85 staff. Distributes maize flour, cooking oil, rice, sugar and beans to about 320 shops and 14 supermarkets across Eastern Uganda from depots in Jinja and Mbale. 9 trucks. Uses Google Workspace (Gmail, Sheets, Drive), an accounting package, WhatsApp Business for orders and MTN MoMo and Airtel Money for payments. All names, firms and figures are fictional and labelled so.

People: Managing Director Sarah Namukasa; Sales Manager Peter Okello; Finance Manager Joseph Mugisha; Operations Manager Grace Akello; HR Officer Mary Nabirye; Customer Service Lead David Kato; Warehouse Supervisor Ibrahim Ssemwogerere. Suppliers: Busoga Oils Ltd (cooking oil), Elgon Millers Ltd (maize flour), Tororo Rice Growers Cooperative, Lakeside Logistics Ltd (transport), Pearl Packaging Ltd. Regions in sales data: Jinja, Mbale, Iganga, Tororo, Soroti, Kamuli.

Use NVF for examples where the learner's own task is not the point. Use the learner's own company for practice. Do not invent real companies, real people or real statistics.

## 4. Files that exist (use these exact names; do not reference others)

Practice Files are in `03 Learner Materials/Practice Files/`; keys and facilitator files are in `04 Facilitator Materials/`.

`01 Case Company/`: `Company Profile.pdf`; `customer_messages.csv` (40 messages: id, date, channel, sender, text); `supplier_invoices.csv` (60 rows: invoice_id, date, supplier, description, qty, unit_price_ugx, vat_pct, total_ugx, po_number; some totals wrong, one duplicate, one missing PO); `weekly_sales.csv` (12 weeks x 6 regions x 5 products: week_start, region, product, units, revenue_ugx); `supplier_agreement_busoga_oils.docx` and `.txt` (two-page oil supply agreement with auto-renewal, price adjustment, liability cap, data and confidentiality clauses); `review_playbook_supplier_agreements.txt` (what NVF will and will not accept); `cv_pack/` (8 synthetic CVs and `job_description_dispatch_clerk.txt`); `staff_handbook_excerpt.txt` (leave, expenses, data and IT use); `meeting_notes_raw.txt` (a board meeting transcript with decisions and actions); `vendor_proposal_orbitdesk.txt` (a fictional AI vendor proposal with red flags); `supplier_email_with_instruction.txt` (an email that contains a hidden instruction, for Session 7); `market_notes_1.txt` to `market_notes_4.txt` (four short fictional industry bulletins, labelled illustrative, for a briefing exercise).

`Templates/` (all KLAi branded): `Use-Case Scorecard.xlsx`, `Task Card.docx`, `Reliability Test Record.docx`, `Reusable Brief Template.docx`, `Information Inventory.xlsx`, `Document Review Table.xlsx`, `Automation Test Log.xlsx`, `Tool Boundary Sheet.docx`, `Risk Register.xlsx`, `AI Use Policy Template.docx`, `Vendor Question List.xlsx`, `Business Case Workbook.xlsx`, `90-Day Roadmap.xlsx`.

`Follow-up Kit/`: `30-60-90 Check-in Form.docx`, `Results Tracker.xlsx`, `Sponsor Briefing.docx`.

`02 Zapier Build/`: `Zapier Build Guide.docx` (step by step for the Session 6 workflow: new email or form row, AI classify and draft, human approval, log to Google Sheet, notify), `sample_enquiries.csv`, `Zapier Rehearsal Checklist.docx`.

`03 Apps Script Build/`: `weekly_digest.gs` (reads weekly_sales in a Google Sheet, computes totals and week-on-week change in plain code, optionally asks an AI model for a three-sentence commentary, writes a draft email to the user), `invoice_check.gs` (flags wrong totals, duplicates and missing PO numbers in a sheet), `ai_helper.gs` (a safe wrapper for one call to the Gemini API with the key in Script Properties), `tests/` (node tests with mocks), `Apps Script Build Guide.docx`, `Apps Script Rehearsal Checklist.docx`.

Facilitator: `Facilitator Guide.docx` (generated), `Answer Keys/` (customer_messages_key.csv, invoice_errors_key.csv, handbook_questions_key.csv, agreement_review_key.txt, vendor_proposal_red_flags.txt), `Rehearsal Record.docx` (a form the instructor fills in during rehearsal; observed runs go here, never invented).

## 5. Facts that are safe to teach (all from research of 1 Nov 2026; checked against search summaries, to be re-checked in a real account before teaching)

- McKinsey, The State of AI 2025: 88% of companies use AI in at least one function; about 39% report any effect on profit (large global firms).
- Zapier: free plan allows two-step Zaps and 100 tasks a month, so the Session 6 workflow needs the free trial of the paid plan (multi-step Zaps, premium apps including Human in the Loop). Human in the Loop pauses a Zap until a person approves or edits. Zapier is SOC 2 Type II and hosts data in the US. Verify in a real account: what the trial allows, whether AI by Zapier runs on the trial without your own key, whether an external approver needs a Zapier login.
- Google Apps Script: JavaScript on Google's servers, free with a Google account. Quotas: consumer Gmail 100 recipients a day and Workspace 1,500; script runtime 6 minutes per run; URL fetch 20,000 a day (consumer). Secrets belong in Script Properties, never in the code. A new script asks for permission once ("Google hasn't verified this app": Advanced, then Go to the project, then Allow); permissions can be revoked at myaccount.google.com/permissions.
- Gemini API: key created in Google AI Studio; a free tier exists for some models; free-tier content may be used to improve Google products, paid-tier content is not, so use only fake or sample data on a free key. Rate limits change: check the console.
- Other tools (talk, do not teach): Microsoft Power Automate and Copilot Studio (licensed per user or by credits, best if the company already uses Microsoft 365); Make (billed per operation, visual canvas); n8n (billed per execution on cloud, can be self-hosted, most technical); agent builders in ChatGPT, Gemini and Claude. Never put prices on slides.
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

Copy the shape of `content/s01.py`. Required keys: num, title, question, outcomes (3), keep, next, clock (list of (minutes, label) summing to 120), plan_caption, words (3 to 5 pairs), cover_note, outcome_note, plan_note, words_note, keep_note, recall (2 or 3 pairs of (question, expected answer) about the PREVIOUS session; empty list for Session 1), slides (11 to 13), workbook (question, steps, fields, reflect, decision), facilitator (prep, landmarks, misconceptions, questions, rescue, demo_steps), needs_files (optional list of any extra file you want created).

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
- Session fields NEW: `keep_title`, `next_label` (default 'Next session'), `plan_title`, `keep_returns` (False only for Session 12). Every close returns to the cover question automatically (the builder adds it).
- Recall slides, words slides, plan slides and the close are partly generated by the builder; do not repeat their text in your notes. Plan notes: write one short paragraph that names the three or four biggest parts of the clock in words (the builder adds the full clock only if you do not).
- Voice: no stock filler ('Nobody is being tested', 'That moment is gold', 'This is the most important', 'Here is how I would answer it'); no homework (anything the learner does between sessions is called 'optional'); one meaning per word: 'task' means the learner's own work task (the Zapier billing unit is always 'Zapier task'); 'prompt' is anything you type, 'brief' is a prompt written once in seven parts and reused, 'assistant' is the product, 'model' is the engine inside it; 'trigger' in a Zap is the event that starts it and in Apps Script it is a timer or event that starts a script (say which); 'log' (Zap or script record), 'test log' (the Automation Test Log template).
- Do not over-claim. Say 'can' and 'often' for AI behaviour; say 'cut down' not 'remove'; never say a tool 'does not look up facts' without 'unless search, files or memory are switched on'; never say a control 'works every time'; never imply one named product is the one that trains on your data: the same five account questions apply to every product and the answers depend on the plan.
- Every learner-facing slide carries one idea. Every session has one place before the break where each learner speaks or decides.
- Numbers: the NVF Monday sales email: 90 minutes by hand; planned with automation 25 minutes (5 to start, 20 to review), so 65 saved per run, and 85 saved before review (the workbook counts the 20 review minutes as a cost). In Session 12 the measured result is 35 minutes a run, so 55 saved a run and 11.0 hours over twelve runs: teach plan against measurement. Loaded hourly cost worked example: UGX 4,500,000 a month plus UGX 500,000 employer contributions and benefits, over 160 hours, is about UGX 31,250 an hour.
- Dates: the 90-day plan starts on 1 February 2027: day 30 is 3 March 2027, day 60 is 2 April 2027, day 90 is 2 May 2027.
- New files created for this pass (reference these exact names): `03 Learner Materials/Practice Files/03 Apps Script Build/last_month_summary_by_hand.csv` (the Sales Manager's hand-made weekly totals with exactly two errors, for Session 8 measurement; key in Answer Keys/hand_summary_errors_key.txt), `03 Learner Materials/Practice Files/01 Case Company/supplier_quote_pearl_packaging.txt` (the quote used in Session 5), and the guides now describe an instructor-prepared 'Make a copy' sheet for Session 6 ('Zapier Practice') and Session 8 ('NVF Apps Script Practice').
