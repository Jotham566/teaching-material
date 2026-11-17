# Leadership Edition authoring brief (11 November 2026)

You are writing one session of **Leading with AI** (Leadership Edition) for senior leaders who want industry application, not maths. The course map was approved on 11 November 2026. Pilots: Session 0 and Session 2, reviewed by the lecturer before the rest are built, so they set the standard and the pattern.

## Read first, in this order
1. `LEADERSHIP_BIBLE.md`: audience, the four phases, the three threads (industry, people, portfolio), the session pattern, the rules. Binding.
2. `kit/sessions_plan.py`: your session's title, question, idea, cases, demonstration, people angle, keep and links. Follow it; you may improve wording and swap a case for a better one from `research/` if you say why.
3. `kit/chain.py`: what your session builds on and feeds.
4. `V3_AUTHORING_BRIEF.md` (slide kinds, visual rules, writing rules), `FLOW_BRIEF.md` (spoken notes that flow), `TERMS_AND_EXAMPLES_BRIEF.md` (plain words first, then the industry term). Where they speak of formulas or "a calculation with three numbers", this edition replaces that with pictures, counts and shillings.
5. `content_exec_reference/s00.py` and `content_exec_reference/s02.py`: the Executive Edition sessions. Use them for the SESSION dict structure and every required field (see `kit/lint_content.py` REQ), and as a source of good pictures and recorded demonstrations, never for the maths.
6. `research/*.md`: the case bank. Use only what is there: organisation, what it does, result, source, caution. Read the full case block before you write it.
7. `kit/deck.py` (KINDS and their fields), `kit/figkit.py` and `kit/diagrams.py` (the figure API, icons), and existing figure modules for examples (`kit/diagrams_t02.py`, `kit/diagrams_t00.py`).

## The standard
- **No maths.** No formulas, symbols, Greek letters, logs or algebra, on slides, in figures or in notes. Counts, percentages and shillings only ("8 of 10", "2 false alarms for every real fraud", "UGX 4 million a month"). The lint enforces this.
- **Explain before use.** A newcomer to AI who sat the earlier sessions must follow every slide. Every term in plain words first, then the industry term in bold the first time. A term from an earlier session gets a one-line recall naming the session. A later session's idea is only a one-line pointer.
- **Flow.** Each slide follows from the previous one; each new part (the idea, the industry tour, the demonstration, your people, the hands-on) opens with a bridge saying why we turn to it. Titles listed alone read as a story.
- **Illustration rich.** Every concept slide and every case slide has a purpose-drawn figure that teaches: a process picture, an icon grid, before and after, a map of who does what, a timeline, a value grid. Text in figures at least 14 pt; nothing overlaps or clips. At most one text-only slide per deck.
- **Industry tour.** One slide with the six main industries (banking and microfinance, telecom and mobile money, agriculture and agribusiness, manufacturing and FMCG, healthcare and insurance, public sector) showing today's idea in each, with one named example per tile where the case bank has one. Then two or three case slides, one case each, told as a story: the problem, what the AI does, the result (exact figure from the case file), and the catch. A small source line on every case slide (publisher, date). Say "company figures" when they are.
- **People slide.** Which roles use it, which tasks change, skills needed, what employees fear or gain.
- **Portfolio hands-on.** The learner adds one or two entries to their **AI Opportunity Portfolio** (a one-page register in the Learner Workbook): the use, what goes in, what comes out, who uses it, how we would know it works, plus the session's own column.
- **Truth.** Never invent a case, a figure or an AI output. Demonstrations show recorded runs from `demo_runs/` (copied from the Executive Edition; read the run records), labelled with the model, the date and the number of runs, or are clearly marked as live with a fallback. Nile Valley Foods is fictional and always labelled so. No AI product prices. No product named as best.
- **Audience voice.** Calm, precise, respectful of senior people's time; Uganda and East Africa first. Spoken notes in first person, 45 to 150 words, each bridging from the previous slide.

## Files and figures
- Write `content/sNN.py` (SESSION dict). Draw figures in `kit/diagrams_lNN.py`, registered `@fig('x_lNN_name')` and used as `dict(kind='lNN_name')`. You may import helpers from existing modules but do not edit them, and do not edit `kit/deck.py`, `kit/lint_content.py`, `kit/chain.py`, `kit/diagrams.py`, `kit/figkit.py` or other sessions.
- Slide count: Session 0 up to 38 authored slides; Sessions 1 to 14 up to 32. Clock sums to 120 and matches the plan slide (see the bible for the pattern).
- Setup: `. /private/tmp/claude-501/-Users-jothamwambi-Projects-IUEA-Teaching-Resources/d327a2a5-164d-49e1-94aa-14fa1a0cd931/scratchpad/env_lead.sh; cd "$B"`. Lint: `python kit/lint_content.py N` to 0 problems. Render: `$S/render_lead.sh N` (PNGs in `$S/review_lead/NN/`). Look at every slide image with the Read tool, fix, re-render, until clean. Then read the spoken script in order from `_specs/` as if aloud.

## Report (under 300 words)
Slide count and the title list; the cases used (IDs) and any swaps; the figures you drew; demonstrations and which recorded runs they use; anything you could not source or show; lint result.

## Rollout (12 November 2026): Sessions 1 and 3 to 14
The pilots `content/s00.py` and `content/s02.py` (with `kit/diagrams_l00.py`, `kit/diagrams_l02.py`) were approved by the lecturer as the standard. Read both decks' slide images in `$S/review_lead/00/` and `$S/review_lead/02/` and their content files before you start, and match their quality, density, figure style and structure. You may import and reuse their figure functions (for example the four-panel case figure and the six-industry tour in `diagrams_l02.py`) but do not edit their files.
- Neighbours are being written at the same time. Keep to `kit/sessions_plan.py` and `kit/chain.py` for what the previous session taught and what the next one teaches; your recall questions ask about the previous session as planned there; your keep note names the next session.
- Practicals (11 to 14) use the Executive Edition practicals as their base (`content_exec_reference/s12.py`, `s13.py`, `s14.py`), stripped of maths and enriched with the industry and people threads and named cases. Template names to use: AI Opportunity Portfolio (in the Learner Workbook and as `Templates/AI Opportunity Portfolio.xlsx`), People and Skills Plan (`Templates/People and Skills Plan.docx`), plus the existing Executive templates in `03 Learner Materials/Templates/` (Business Case Workbook, Use-Case Scorecard, Task Card, AI Use Policy Template, Risk Register, Vendor Question List, Information Inventory, 90-Day Roadmap, Tool Boundary Sheet, Reusable Brief Template, Reliability Test Record) and the Follow-up Kit. Do not create templates; name them.
- Session 14 closes the course: the final AI Opportunity Portfolio, the 90-day plan, and a one-picture summary of all fifteen sessions.
