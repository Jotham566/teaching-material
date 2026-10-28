# Applied AI and Automation: independent evaluation

Prepared 26 October 2026 for discussion. No course file was edited. Part 1 was written from the teaching materials alone. Part 2, at the end, compares it with the Benchmark Review, which I opened only after Part 1 was complete.

## How I evaluated it, and what I could not inspect

I read `00 Start Here.txt`, the Course Overview, all 12 decks (slide text and speaker notes, 286 slides), the Animation Guide, the Learner Workbook, all 43 Practice Files, the Facilitator Guide, the Implementation Playbook and the three Teaching Resources files.

I rendered all 286 slides to images through LibreOffice and looked at contact sheets of every deck, then at eight slides at full size (Session 2 slides 10 and 18, Session 4 slides 10 and 12, plus the embedded URA and Copilot Studio screenshots extracted from Sessions 10 and 8). I also checked the arithmetic, compared the clause 3 wording across every file, counted repeated note text, and compared the animation XML with the Animation Guide.

Limits that affect the conclusions:

- **Animation playback.** I did not play any animation. I confirmed from the slide XML that the click counts in the Animation Guide match on all 34 listed slides and that no other slide has animation. The Animation Guide itself records that only Session 8 slide 13 was played in desktop PowerPoint. Whether the builds look right on screen remains untested by me.
- **Live tools.** I did not run any AI assistant, agent builder or the Session 10 page against the files. Statements about what the tools will do are inferences from the scripts.
- **Web sources.** My fetch tool was blocked for every external site (`cowork-egress-blocked`). I could not open ULII, URA, any provider's programme page or any vendor page. Everything in the benchmark section comes from web-search result summaries, which paraphrase the provider pages and in places third-party reviews. I give the provider URL for each item and mark every price and hour figure as unverified until opened. I did not access any paid course content.
- **Fonts.** Slide text is set in Calibri. LibreOffice substitutes a metric-compatible font, so text fit in PowerPoint should match my renders.

---

# Part 1: independent assessment

## 1. Verdict

The course is a sound, internally consistent design for teaching a lawyer how to supervise AI output. Its best idea is the single matter in which a plausible answer loses an exception, a search returns an old version, a draft invents a fee, and an action reaches the wrong recipient. Each failure has a control, an owner and a test. The arithmetic checks out, clause 3 is word-for-word identical wherever it is quoted in full, simulated material is labelled as simulated almost everywhere, and the decision at the end of each session builds towards the Session 12 pilot proposal. A learner who completes it will check sources, preserve exceptions, ask for owners and tests, and distinguish retrieval errors from generation errors. Most free paths do not teach those habits.

As written, it is not yet ready to deliver as 24 hours of teaching, for five reasons.

1. **The outcome "explain AI/ML mechanisms accurately" is only half met.** The course explains training, embeddings, tokens and retrieval well. It never explains how a language model produces an answer. The words "probability", "temperature" and "context window" appear nowhere in the slides or notes. Next-token prediction appears as one row in a table (S2 slide 6, "Predict masked or next tokens") and one phrase in the S2 slide 22 notes ("Pretraining often learns from token prediction"), and is never explained as the way answers are generated. "Hallucinate" appears once, in a Session 6 note, on no slide, and is never defined. Variation between runs appears once, as an instruction to "repeat one run to observe variation" in a Session 3 note. This is the mechanism behind the failures the whole course is about. A learner who "has encountered the terminology" will leave still unable to say why a fluent answer can be wrong.
2. **The learner is shown the failures and never finds them.** The contract is 1.4 KB of eight short clauses. The invoice file has four rows. The retrieval "trace" is a hand-written description labelled as not a live run. The damaged OCR extract is typed text. Any current assistant will pass most of these tasks on the first attempt, which leaves the learner with the impression that the checking routine is a ceremony. Her evidence that AI errs on real documents will come from a prepared slide.
3. **The timing is not credible as written.** Every session uses the same block plan (10 / 25 / 25 / 5 / 35 / 15 / 5). The sessions carry 15 to 21 concept slides each (214 across the course), each with a question and an expected answer, inside a 25-minute block. That is 1.0 to 1.6 minutes per slide.
4. **The speaker notes give less support than the Facilitator Guide claims.** The same "If unclear" line appears on all 286 slides. Five questions ("What would a useful result look like?" and four others) fill 60 slides. The expected answer on every opening slide is an instruction ("Use the answer to emphasise relevant examples"). Slide-specific note content averages about 64 words.
5. **A few set-piece exercises have unresolved facts.** The changed-fact exercise ("the provider transfers to a buyer outside its wholly owned group") has no definitive expected answer and is reused four times. The matter's fact pattern shifts between an internal reorganisation and a sale to a buyer. The tax session contains no tax analysis. Session 10 repeats Session 8's control logic on a page that hard-codes the answer.

Everything above can be fixed inside 12 sessions and 24 hours. The corrections are mostly in notes, one new block of content, one merge, and a handful of exercises.

### Criterion summary

| Criterion | Assessment | Principal evidence |
|---|---|---|
| 1. Relevance and depth | Right level overall. Some material is too thin, some is too detailed. | Missing: generation mechanism, evaluation method, vendor due diligence, enterprise data terms. Excess: data analysis and data science definitions (S1 slides 6–7), CNN/RNN slide (S2 20), Akoma Ntoso (S4 16), NER taxonomy (S7 5–6), CAG (S5 17), agent taxonomies (S8 11–12). |
| 2. Accuracy | Sound where checked. A small number of defects. | Arithmetic verified (S9, S12). Clause 3 identical in every full quotation. Defects listed in section 5. |
| 3. Structure and flow | Logical build with good recaps. One missing block, one redundancy. | Information → retrieval → research → contract → agents is a strong spine. Session 10 repeats Session 8. Generation mechanism missing before Session 3. |
| 4. Teachability | Format is good, content is thin. | Notes carry Ask, Expected, Transition on every slide, but 60 questions are templates and the key live exercises have one-sentence answers. |
| 5. Timing | Needs redesign. | 214 concept slides in 12 × 25 minutes. Identical block plan for sessions as different as 6 and 8. |
| 6. Visual communication | Clean, consistent, legible. Weak on mechanism diagrams. | Only 4 pictures and 1 native chart in 286 slides. 26 slides are built from the same numbered-box-and-arrow template. The attention slide shows no attention. |
| 7. Applicability | Strong. | Each session ends in a firm decision. Playbook, risk register, adoption plan and proposal fields connect. |
| 8. Consistency | Good on content, weaker on cues and facts. | Findings count (2 vs 3), fact-pattern drift, animation cues that do not match animations. |
| 9. Learning evidence | Weakest dimension. | Checks repeat what the previous two slides show. One changed fact reused four times. No baseline, no misconception probes. |
| 10. Value | Real, concentrated in Sessions 4–12. | See section 8. |

## 2. What to preserve

- The fluent-versus-supported answer pair (S1 slides 16–17). It is the best opening exercise in the course.
- The retrieval versus generation failure split (S5 slide 14) and the five assistant tests (S5 slide 18).
- The "model change is an operational change" slide (S2 slide 23) and the stress-case arithmetic (S12 slides 10–11).
- Honest labelling of prepared material, and the rule "record connected execution as unverified" (Agent Build Guide, Session 8 notes).
- The three flawed documents (contract review, research note, tax report). The Flawed Tax Report is the best of them: four unsupported inferences, each traceable to a source.
- The single-matter spine, and the restraint on transfer examples (one slide, S3 slide 8). That restraint fits your brief.
- The refusal to hard-code tax rates or deadlines (S9 slide 15).

## 3. Findings by criterion

### 3.1 Relevance and depth

The conceptual register is right for this learner. Definitions are accurate, no mathematics is required, and each is tied to a task in the matter. Three adjustments follow.

**Add.** The generation mechanism (next-token prediction, sampling, why variation occurs, context window, why fluent errors occur, what reasoning modes and tool use add). Enterprise versus consumer data terms (she already uses AI tools, so the question "what happens to what I paste?" is live now, and the course defers it to Session 11 and a single line on S1 slide 19). Evaluation method (how many test cases, who scores, what counts as a pass). Vendor due diligence beyond "ask for coverage". A named Ugandan legal frame in the governance session.

**Trim.** S1 slides 6–7 (data analysis and data science) do not change any decision she will make. S2 slide 20 (CNN, RNN; the notes also mention GRUs, which the slide does not). S4 slide 16 (Akoma Ntoso). S5 slide 17 (CAG). S7 slides 5–6 (three NER slides). S8 slides 11–12.

**Keep at current depth.** Tokens, embeddings, training versus inference, chunking, hybrid retrieval, access-aware retrieval, the agent loop, prompt injection and human-in-the-loop. These are the concepts her firm's vendors will use.

### 3.2 Accuracy

Verified correct: the reconciliation (125 − 25 = 100; 100 − 2 = 98; 98 − 80 = 18; 125 − 98 = 27 = 25 + 2), the capacity example (30 versus 20 minutes; 40 × 10 = 400 minutes; stress case 33 minutes, 120 extra minutes), the INV-001/002/003 amounts (40 + 35 + 25 = 100), and the consistency of clause 3 across slides, workbook, guide and practice files.

Defects are listed with proposed wording in section 5. The ones that matter most:

- The Session 6 judgment pinpoint and the statute section number cannot be confirmed from the course files (details in 5, item C8).
- S1 slide 5 attributes its AI definition to the OECD page. The slide's wording describes a field. OECD's published text defines an *AI system*, which is the formulation a lawyer will meet in regulation.
- S7 asks for repair of "two" flawed findings while the practice file contains three.
- S2 slide 18 (attention) shows no relationships. The slide XML contains only word boxes and a caption.
- The Session 10 screenshot shows a logged-in user's name.

### 3.3 Structure and flow

The sequence is mostly right: orient (1), mechanism (2), tools (3), information (4), retrieval (5), research (6), contract (7), agents (8), tax (9–10), risk (11), leadership (12). Recaps at slide 2 of each deck name the previous result, which suits flexible scheduling.

Four structural issues:

1. The generation mechanism is missing between Sessions 2 and 3.
2. Session 10's new content is one idea (an uncertain response needs a status check before a retry) plus a concrete process boundary. The rest repeats Session 8: the human-in-the-loop diagram is the same on S8 slide 13 and S10 slide 12, and the API-versus-browser contrast appears on both S8 slides 5–7 and S10 slide 10.
3. Confidentiality and data terms arrive late. She is likely to use tools between sessions, and the course contains one line about it before Session 11.
4. The same changed fact is reused (see 3.9).

### 3.4 Teachability

The notes structure is good: explain, ask, expected answer, transition. Its content is thinner than it looks.

- 286 of 286 slides carry the identical line "If unclear: return to the source in our matter, change one fact and ask which part of the result changes."
- Every slide carries one of two "Visual cue" lines. 243 say "Pause for the question before revealing or discussing the answer", including slides with nothing to reveal.
- Five template questions repeat in every deck (60 slides): "Which part of today's work would matter most in the firm?", "What would a useful result look like?", "What would you change before using this result?", "What does this example still leave unproven?" and "What is the next sensible step for the firm?". The first has the expected answer "Use the answer to emphasise relevant examples while retaining the conceptual sequence", which is an instruction.
- On definition slides, the "I will explain" note restates the slide ("X is Y. In plain language: [the slide's matter example]. Connect this explanation to the matter example and ask the question before showing the expected answer.") on 17 slides. There is no analogy, no worked step, no common misconception.
- The facilitator has no model output. The Teaching Resources hold one-sentence expected findings per session. For each live task the file does not say what a good assistant answer looks like, what a typical wrong answer looks like, or how to score either.

The Facilitator Guide's "Questions and answers" give two questions per session, and the closing check has three. Fine for recall, but they do not tell you what to do when the learner's answer is half right.

### 3.5 Timing

Content slides per session (excluding the title, the recap and the four closing slides): S1 19, S2 21, S3 19, S4 18, S5 18, S6 16, S7 17, S8 19, S9 16, S10 15, S11 18, S12 18. In the 25-minute concept block that is 1.0 to 1.6 minutes per slide. A definition slide with a real question needs about 2.5 minutes, an animated four-click diagram about 3.5. My estimate of the concept block is 40 to 55 minutes in most sessions, against 25 planned.

Two other timing problems:

- "Worked demonstration" (25 min) and "Joint application and tests" (35 min) are 60 minutes for the same four-bullet "in-class review" slide, with no split of tasks between blocks. For Session 8 (configure a builder, trigger a model-selected lookup, test an unknown ID, test an injection, approve and reject) 60 minutes is tight even if the account works first time. For Session 10 it is more than the content needs.
- The "Firm decision" block (15 min) recurs 12 times. It is the right idea (it builds the Session 12 proposal) but several decisions are near-identical ("evaluate one tool", "pilot a bounded collection", "pilot one bounded workflow"). Reducing it to 8–10 minutes in Sessions 1–10 and keeping the full block in 11–12 would give time back.

A workable plan for a two-hour session with one learner: 10 recap and retrieval practice, 40–45 explain-and-ask on 12–14 core slides, 40 guided practice, 15 decision and check, 10 buffer. Section 9 turns this into a recommendation.

### 3.6 Visual communication

What works: consistent colour system, calm hierarchy, titles at the same position on every slide, legible type (table text 18.75 pt, body 17–25 pt, footers, captions and diagram-box detail at 12–13.5 pt), few words per slide (about 36–42 on average per deck, maximum 87), no clutter, no decorative stock imagery. The native chart on S9 slide 8 and the labelled "illustrative" captions on the embedding map, token IDs and neural diagram are honest.

What does not work:

- **The mechanism diagrams do not carry the mechanism.** S2 slide 10 is a 2-3-3-1 node network with very faint grey lines and no indication of what goes in or out. S2 slide 14 (embedding map) shows six unrelated words and does not place a query beside candidate passages, which is the use the course needs in Session 5. S2 slide 18 (attention) shows seven word boxes with two words coloured; the XML contains no connector or weight. The notes say "Show illustrative relationships among provider, its and obligations", and nothing on the slide can show them. S5 slide 6 is a four-box flow. There is no RAG architecture picture (documents → chunks → vectors → index; question → vector → closest chunks → prompt → answer).
- **One template covers too many ideas.** 26 slides are built from the same numbered-box-and-arrow template. Most are four boxes left to right, used for a calculation (S9 slide 7), a pipeline (S4 slide 8), a retrieval system (S5 slide 6) and three categories joined by arrows as if they were steps (S1 slide 3 firm, client and matter; S4 slide 3 paper, digital files, systems). Only a few slides (S8 slides 10 and 13) change shape to fit the idea.
- **S9 slide 8** puts 125, 100, 98 and 80 in separate bars. The relationship (two deductions bridging 125 to 98, then 98 split into 80 received and 18 outstanding) is what the slide should show. A waterfall does that. The notes admit "the chart supports comparison but the source table explains why they differ".
- **S9 slide 7** shows the deductions (25, 2) and the end value (98) but not the intermediate 100.
- **Third-party images are small or cropped.** The Microsoft Document Intelligence image on S4 slide 10 is cut off mid-sentence at the bottom. The Copilot Studio activity map on S8 slide 15 is a weather agent. Both teach where to look, and neither shows a legal task.
- **S10 slide 5** embeds a URA portal screenshot that includes "Logged In As, GRACE NANSUKUSA". The slide is titled "A genuine URA guidance screen" and its notes say "No account is accessed in this demonstration." The origin of the image should be confirmed and the name cropped.
- **S4 slide 5** has notes saying "Show two representations of the same fictional clause" but the slide has two text blocks. A scanned page image beside its text layer is the picture that session needs.
- **Animation.** Static inspection (final state) is complete and readable. Playback quality is unverified. The notes' cue lines do not match the animations: "Reveal the diagram stages in order" appears on slide 2 of all 12 decks and on S2 slide 12 and S7 slide 5, none of which animate. Five animated slides (S1 3, S4 3, S5 6, S11 4, S11 8) carry the "Pause for the question" cue.

### 3.7 Applicability

Strong, and the best reason to teach it. The Session 12 proposal is assembled from earlier decisions, the Playbook mirrors the proposal fields, and the risk register, roles file and pilot decision record are blank templates that line up with the slides. Two gaps limit usefulness after the course:

- Every adoption artefact is blank. There is no completed example (a filled pilot proposal, a three-row risk register, a one-page AI use rule). A partner leaving the course with templates only has to recreate the thinking.
- The 90-day plan has no dates, owners or check-in. The course ends at Session 12 without a scheduled follow-up.

### 3.8 Consistency across materials

Items are listed in section 6. Content consistency is good. Cue, count and fact-pattern consistency is weaker.

### 3.9 Learning evidence

The activities generate evidence of recall and, in places, of application. They do not yet generate reliable evidence of understanding.

- **Closing checks repeat visible text.** For example, S9 slide 20 states "UGX 125 million becomes UGX 100 million ... UGX 18 million" and slide 22 asks for the same explanation two slides later. S1 slide 12 already maps total invoices to calculation, contract type to classification and amendment to generation, which is the expected answer to S1 slide 25 question 1.
- **The changed fact is reused.** "The provider transfers to a buyer outside its wholly owned group" appears in the Client Instruction, S3 slides 17 and 25, S7 slide 23 and Fresh Discussion Test 1. By Session 7 it is no longer fresh.
- **Expected answers are hedged.** "Reassess the exception against the changed fact and ask about remaining transaction conditions" (S3 17) tells the facilitator nothing about whether the learner's answer is right.
- **No baseline.** There is no diagnostic on entry. The brief says not to equate chatbot familiarity with technical understanding, and the course has no way to find out what she understands on day one.
- **No misconception probes.** Common confusions are not listed: that uploading a file trains the model; that a citation is evidence; that RAG "makes the model know" the firm's documents; that more agents are more reliable; that a second model agreeing is verification (Fresh Test 6 touches the last).
- **The workbook shows the answers.** Each session's "Worked reference" and "professional limitation" repeat the expected findings. If she holds the workbook before the session, the check is already answered.
- **The progress record is ambiguous.** The status column holds all three options as one string ("Discussed / explain independently / revisit in class"), so no status is recorded.

### 3.10 Value for money

No fee was supplied, so this separates what the course adds from what it costs.

**Educational value that free and cheap paths do not supply (from their public syllabi, which I read only in summary):** a continuous legal and tax matter; correction of her own misconceptions in real time; hands-on use of the tools she will buy; Ugandan sources (ULII, URA, PDPO); and a pilot proposal. None of the comparators I found lists any of these.

**Where the course overlaps what is free:** Sessions 1–2 teach vocabulary that several free paths cover in under 10 hours (DeepLearning.AI "AI for Everyone" about 7 hours, "Generative AI for Everyone" about 5–6 hours, IBM SkillsBuild fundamentals about 10 hours, Anthropic "AI Fluency" about 3 hours). If the live hours in those sessions go to definitions, the course is weakest on value for money there. If they go to live experiments with her own tools (section 9), they stay worth having.

Price reference points appear in section 7.

## 4. Session-by-session table

"Slides" counts all slides in the deck. "Concept" counts slides between the recap and the closing four. Time estimates assume the concept slides are taught with their questions.

| # | Purpose and prerequisite | Strengths | Weaknesses (evidence) | Timing | Recommended change |
|---|---|---|---|---|---|
| 1 | Map AI, analysis, ML, DL, generative AI onto the matter and choose a candidate use case. No prerequisite. 25 slides, 19 concept. | Fluent-versus-supported answer (16–17). Model inside a system (13–14). Rule versus learned prediction (15). Error list (18). | Six text-only definition slides (5–10). Data analysis and data science (6–7) do not change a decision. AI definition (5) misattributed. Venn (11) does not nest generative AI or show the data science overlap. Opening expected answer is an instruction. S1 notes (3) say "the client plans an internal group reorganisation", which conflicts with the Matter Brief. | 19 slides in 25 min is 1.3 min each. Realistic 40–45. | Start with a 10-minute live test: ask her own assistant the clause 3 question and find what it dropped. Merge 5–10 into one build. Cut 6–7 to a line. Move the consumer-versus-enterprise terms (see S3) forward. |
| 2 | How models learn and represent language. Needs S1. 27 slides, 21 concept (heaviest). | Learning loop (5). Leakage (8). "Charge" in two contexts (16). Training versus inference (21). Model change as operational change (23). | No generation mechanism although the title question is "why can it still misunderstand". CNN/RNN slide (20) is detail the notes inflate (GRU). Neural diagram (10) faint and unlabelled. Attention (18) has no relations drawn. S2 22 cites a Coursera landing page as a source. | 21 slides in 25 min. Realistic 55–60. Overloaded. | Cut 7, 20, merge 9–10 and 21–22. Move attention and generation to the new Session 3. Replace 10, 14 and 18 with diagrams that show the mechanism. Replace the Coursera source with Ouyang et al. 2022 (instruction following) or the Google crash course. |
| 3 | Tools and instructions. Needs S2 to know why context matters. 25 slides, 19 concept. | Constant-task comparison (3). Source-and-location table (14–15). Changed-fact loop (17). Four-line evaluation (20). One transfer slide (8). | Market tour spread over four slides (4–7) from vendor help pages. No content on model tiers, web search, file limits, memory, retention, enterprise terms. Non-determinism appears only in a note. Expected answers on 17 and 23 are hedged or mismatched. | Fine once tour is cut to one slide. | One slide for the tour. Add 15 minutes on data terms and plan types. Run the same prompt three times and compare. Give the changed-fact question a definitive answer (section 5, C6). |
| 4 | Preparing information. Needs S3. 24 slides, 18 concept. | Inventory (6–7). Damaged extract (11–12) is memorable. Quality record (13). Missing-value question (17). | No OCR run on a degraded scan. Slide 5 notes promise two representations, slide shows text. Slide 10 image is cropped. Four formats on three slides; Akoma Ntoso (16) is detail. "Map the firm's systems verbally" is open-ended with no output spec. | 18 slides in 25 min. Realistic 40. | Run a live OCR on a skewed low-resolution scan of the one-page agreement. Fold 14–16 into one slide. Keep JSON (needed in S9). Define the inventory output (a filled CSV row per system). |
| 5 | Retrieval. Needs S4. 24 slides, 18 concept. | Strongest session. Bad chunk split (8). Retrieval versus answer failure (14). Access-aware flow (16). Five tests (18). | No picture of RAG. Embedding model versus language model never distinguished. Trace is hand-written. Corpus is three documents, so retrieval cannot fail. CAG (17) is niche. No scoring rule for the five tests. | 18 slides in 25 min. Realistic 40. | Replace slide 6 with a mechanism diagram. Add one sentence on the two models. Test on a 30–50 document synthetic set where a wrong-version retrieval can occur. Move CAG to the notes. |
| 6 | Legal research. Needs S5. 22 slides, 16 concept. | Submission versus finding (8). Legislation at the relevant time (9). Failure modes (14). Confidential query (15). | Exercised proposition (appeal scope) is peripheral. The judgment's substantive issue is unused. Statute renumbering in the 2023 Revised Edition is unaddressed. No scripted live deep-research run. No real incident or quantified error rate. | 16 slides fine. | Choose a research question that bears on the matter, run one deep-research report live, and audit every citation. Use the renumbering as the "right edition, right date" lesson (C8). |
| 7 | Contract review and drafting. Needs S6. 23 slides, 17 concept. | Rule, exception, condition decomposition (8). Flawed review repair (11). Redline needs a reason (15). Responsibility table (18). | Contract is eight short clauses; no defined terms, cross-references or schedules. Three NER slides. "Two" versus three flawed findings. Changed fact is ambiguous (shares or assets) and reused. Client side is not stated. | Fine. | Add a real-length agreement for one extraction test. State the client side. Align the findings count. Replace the hedged expected answer (C6). |
| 8 | Automation and agents. Needs S7 (tool lookup uses the clause). 25 slides, 19 concept. | Ladder from rules to agent (5). Fixed workflow versus agent (18). Injection test (19). Rejection stops the dependent action. "Record unverified" rule. | Highest delivery risk. 60 minutes for a build that depends on account and model behaviour. No function-calling or MCP vocabulary. Slides 11–12 are taxonomies. No cost or spend test though slide 21 says "limit spending". | Overloaded. | Drop 11–12 to notes. Rehearse the build once with the exact account and save the real trace as the fallback. Split into 30 minutes concept, 60 build, 30 decision. |
| 9 | Tax health check. Needs S8 (human review). 22 slides, 16 concept. | Arithmetic correct. Flawed tax report. False positive cost (17). Refusal to invent an identifier (12). | No tax analysis, so the brief's "tax analysis" outcome is untested. Bar chart hides the reconciliation. Slide 7 omits the interim total. Slide 6 expected answer is circular ("the teaching fixture documents it"). Data is four rows. | Fine. | Merge with S10. Add one verified Ugandan tax question, answered from URA and legislation, as the analysis step (for example the EFRIS FDN requirement that the URA returns page states for input and output tax). |
| 10 | Filing assistance and controlled actions. Needs S9. 21 slides, 15 concept. | Preparation, submission and payment distinguished (4). Uncertain status and retry (13–14). Audit record (15). | Duplicates S8's human-in-the-loop and API/RPA content. The mock page hard-codes 98,000,000 so the AI step cannot fail. Screenshot with a named user. Real route (return template, PRN for payment) is not shown. | 15 concept slides, only 3 new. | Merge into Session 9. Keep slides 4, 5 (cropped), 13–15. |
| 11 | Risk and governance. Needs S8 and S10. 24 slides, 18 concept. | NIST functions (4). No-training setting is not confidentiality (7). Cross-matter access (8). Incident exercise (16–17). Proportionate governance (19). | No Ugandan instrument named. No consumer-versus-enterprise terms. Bias slide is generic. Register template blank. This is the session a law firm will rely on and it has the same time as the others. | 18 slides in 25 min. Realistic 45–50. | Give it fewer slides and more time. Pre-fill a three-row register. Add a one-page AI use rule as an exercise. Name the Data Protection and Privacy Act 2019 and the PDPO position (C21). |
| 12 | Leading adoption. Needs all. 24 slides, 18 concept. | Capacity example and stress case (10–11). Staged route (16). Proposal fields (18). | Proposal template is nine blank prompts. No exemplar. Sources on slide 15 are two training-course landing pages. 90-day plan has no dates. Final transition text is lower-case fragment. | Fine if the proposal is built over the whole session. | Provide a filled exemplar. Schedule a 30-60-90 follow-up. Add one optional transfer exercise per interest area (fintech, telecom, agents) at the end. |

## 5. Specific corrections

Type: **F** factual or reference error; **P** pedagogical judgment; **D** design preference.

| ID | Location | Issue | Type | Proposed fix or wording |
|---|---|---|---|---|
| C1 | S1 slide 5 and notes | The definition is described as OECD-sourced. The OECD page defines an AI system. | F | Replace with: "An AI system is a machine-based system that, for a given objective, infers from the input it receives how to produce outputs such as predictions, content, recommendations or decisions." Check the wording against the OECD page named on the slide. Then add: "AI is also the field that builds such systems." |
| C2 | Slide 1 of all 12 decks, notes | The expected answer is an instruction to the facilitator. | P | Replace with a concrete prompt. For example S1: "Which of your own tasks would you most want a tool to do reliably? Expected: any named task. Record it as a candidate for Session 12." S2: "What did your assistant get wrong this week? Expected: any real error, to be classified later as extraction, retrieval, generation or action." |
| C3 | S2 slide 18 and notes | The slide has no relation lines, so "Show illustrative relationships" cannot be done. Question tests the wrong thing. | F/P | Draw arcs from "its" to "provider" and "obligations", with invented weights labelled as such. Notes: "When the model reads 'its', it weighs the other words in the sentence to decide what 'its' refers to. The weights come from training. These are made up for the picture." Ask: "When the model reads 'its', which earlier word does it need?" Expected: "provider, because the provider's obligations are in question." |
| C4 | S2 slide 20 and notes | Architecture detail; notes mention GRUs absent from the slide. | P | Delete the slide. Add one sentence to S2 slide 19 notes: "Most current language tools use an architecture called a transformer. Image and audio tools often use others." |
| C5 | S2 slide 22 sources | A Coursera landing page cited as a source for training stages. | F | Cite the primary paper: Ouyang et al., "Training language models to follow instructions with human feedback" (2022), or the Google crash-course page already in Public Sources. |
| C6 | S3 slides 17 and 25; S7 slide 23; Fresh Test 1; Client Instruction | "Transfer to a buyer outside the group" is ambiguous (shares or assets) and the expected answer ("reassess the exception") is hedged. | F/P | Split into two variants with definitive answers. **Variant A, buyer acquires control of the provider (share sale):** "The group exception does not apply, because the change is not a reorganisation within a wholly owned group. Clause 3 requires the customer's prior written consent." **Variant B, buyer takes over the contract or business by assignment:** "Clause 3 does not address assignment. The extract has no assignment clause, so check the signed schedule and the general law before advising." Use A in Session 3 and B in Session 7. |
| C7 | S1 slide 3 notes; Matter Brief; Client Instruction; S5 slide 15; Knowledge Assistant Tests row "unknown fact" | The reorganised party is described three ways: the client, its service provider, and a "planned buyer" that the base facts do not contain. The client is the customer, and the playbook's "retain a workable exception" reads as a provider's preference. | F | State once: "Victoria Services Ltd (customer) has been told that Equator Systems Ltd (provider) plans an internal reorganisation. Victoria asks whether its consent is required." Remove "planned buyer" from the base case and keep it for Variant A. State the firm's side and whether the playbook is customer-side. |
| C8 | S6 slide 10; Verified Authority Example; Workbook S6 | Pinpoint ("printed page 3, lines 24 to 27") was taken from a SheriaHub copy, and line numbering is edition-specific. The statute citation "section 27(2)" may be superseded: a search summary of the 2023 Revised Edition on ULII places the High Court appeal provision at section 28. I could not open either source. | F (to verify) | Verify against the ULII PDF of the judgment and the 2023 Revised Edition. If confirmed, add: "The judgment cites section 27(2) of the Tax Appeals Tribunals Act. The 2023 Revised Edition numbers the provision differently, so quote the edition and date with the section." Use it as the lesson on S6 slide 9. |
| C9 | S6 slides 6, 10, 19 | The chosen proposition is about appeal scope. A search listing of the same judgment describes the substantive issue as withholding tax on management fees paid to a foreign affiliate. That issue bears directly on intra-group reorganisations and on a tax partner's practice. | P | After reading the judgment, add one substantive claim about the withholding tax holding to the evidence register, alongside the appeal-scope example. Run the deep-research task on that issue. |
| C10 | S7 slide 11, Facilitator Guide S7, Workbook S7 | Guide and workbook say "repair two flawed findings"; `Flawed Contract Review.txt` has three (the third invents "UGX 50 million" fees). | F | "Repair the three flawed findings", or remove finding 3 from the file and use slide 23 question 3 as the fee test. |
| C11 | S3 slide 23 | Expected answer to "What does this example still leave unproven?" is the data-use limitation, which does not answer the question. | P | "One tool, one clause and one afternoon. We have not measured accuracy on the firm's documents and we have not confirmed that this account may take client data." |
| C12 | S9 slide 6 | Expected answer ("The teaching fixture documents it as a duplicate import") is circular. | P | "The same invoice number, amount and supporting reference appear twice, and the ledger carries the invoice once. A second sale would carry its own number." |
| C13 | S9 slide 7 | Interim totals not shown. | F | Box 2: "Unique invoices: 100 (125 less duplicate 25)". Box 3: "Net sales: 98 (100 less credit note 2)". |
| C14 | S9 slide 8 | A bar chart of four values hides the relationship. | P | Waterfall: 125, −25 duplicate, −2 credit note, = 98 ledger; then a stacked bar splitting 98 into 80 received and 18 outstanding. |
| C15 | S10 slide 5 | Screenshot includes "Logged In As, GRACE NANSUKUSA". | F | Confirm where the image came from. Crop out the name or replace it with a screenshot of the public page. Change the notes line "No account is accessed" to describe the image accurately. |
| C16 | S4 slide 5; S4 slide 10 | Notes describe a scan beside a text layer that the slide does not show. Slide 10 image is truncated at the bottom. | F | Add a rendered scan and its extracted text, or edit the notes. Use the full image or a different crop. |
| C17 | All decks slide 2; S2 slide 12; S7 slide 5; S1 3, S4 3, S5 6, S11 4 and 8 | Visual cue lines contradict the actual animations. | F | Remove the "Reveal the diagram stages" cue from slides without animation. Add it to the animated slides. |
| C18 | S7 slide 5 notes | Notes say "highlight ... the effective date and amount." The slide has no amount. | F | Delete "and amount". |
| C19 | S12 slide 15 sources; S12 slide 24 transition | Training-course landing pages cited as sources. The transition is a lower-case fragment. | F | Remove the two Reforge and Coursera URLs. Transition: "Thank you. Keep the proposal and the decision record." |
| C20 | S5 slide 7 and slide 6 notes | Search uses one model to create embeddings and a different model to write the answer. The notes say only "an existing model can compute the representation." | P | Add: "Search uses an embedding model to turn text into vectors. A separate language model writes the answer from the passages it is given. They are different models and can be bought separately." |
| C21 | S11 slides 5–6 and 7 | No Ugandan instrument named. | P (verify) | Add to notes, after you confirm each on ULII or PDPO: Data Protection and Privacy Act 2019; the PDPO's position on registration and cross-border transfers (a July 2025 decision against a major foreign provider is reported in law-firm alerts, and the reports disagree on whether failure to register is itself a breach); the professional-communications provision of the Evidence Act (the 2023 edition places it at section 125 per a search summary). |
| C22 | Facilitator Guide time table | One identical plan for all 12 sessions. | P | Replace with a per-session plan naming the core slides, the optional slides and the minute allocation. Section 9 gives the model. |
| C23 | Notes boilerplate | "If unclear ..." on 286 slides. | P | Replace with slide-specific rescue: for example S5 slide 8: "If she does not see the problem, show Chunk B alone and ask what it says about consent." |

## 6. Cross-material inconsistencies and missing resources

### Inconsistencies

1. Findings count: two (S7 slide 11, Guide, Workbook) versus three (`Flawed Contract Review.txt`).
2. Fact pattern: customer or provider reorganisation, and a "planned buyer" that the base facts lack (C7).
3. The changed fact is reused four times (3.9).
4. Cue lines do not match animations (C17). Notes on S7 slide 5 and S2 slide 20 refer to content not on the slide.
5. Template questions have expected answers that do not answer them (C2, C11).
6. The workbook's "Worked reference" repeats the expected findings, so the workbook cannot be given out in advance.
7. Public Sources lists the case copy from SheriaHub while the slides cite ULII. The pinpoint belongs to one edition (C8).
8. The Facilitator Guide says the notes "contain an explanation, question, expected answer and transition for every slide". Formally true, substantively thin (3.4).
9. The In-Class Progress Record's status column lists the options as one string.
10. The Course Overview and Start Here do not list learning outcomes, prerequisites, required accounts or the way understanding is checked. They do state that live tools depend on account access.

### Missing resources

- Real run outputs. The fallback for every live task is a hand-written description. Save actual outputs of the intended tools for each task: S3 review table, S4 OCR comparison, S5 retrieval, S6 research report, S7 extraction, S8 agent trace, S9 reconciliation draft, S10 field map.
- A model answer and a scoring note for each live task: what a good answer contains, three typical wrong answers, what to say.
- A real-length document set: one 25–40 page public agreement, a 30–50 document synthetic knowledge set, and a larger ledger with noise.
- A plain-language glossary. The workbook's 18 definitions are formal ("a numerical representation learned or constructed so that relationships between items can be compared computationally").
- A diagnostic and a repeat of it in Session 12.
- Worked exemplars: a filled risk register, pilot proposal, one-page AI use rule, a cost and effort sheet.
- A facilitator run-sheet per session with minutes, core versus optional slides, and a rehearsal checklist for accounts. The Demonstration Preflight is one paragraph.
- A one-page Ugandan legal frame for the facilitator (C21).

## 7. Benchmarking

### Source limits

The fetch tool was blocked for every provider domain, so no primary page was opened. The facts below are from web-search result summaries that name the provider's page. Prices and hours need confirmation on the linked page before they are used in any document. No paid course content was accessed.

### Comparators

Provider is the institution that designs and teaches. Platform is where it is sold or hosted.

| Programme | Provider / platform | Paid or free | Audience and type | Format and hours (as reported) | Price (as reported) | Practice, assessment, implementation | Relevance to this learner |
|---|---|---|---|---|---|---|---|
| [GenAI for the Legal Profession: Power User Edition](https://executive.law.berkeley.edu/programs/generative-ai-for-the-legal-profession/) | Berkeley Law Executive Education / provider's own site | Paid | Lawyers; executive education | Self-paced, nine modules, four-week suggested schedule. Page figure about 6 hours (2–3 per week); third-party reviews say about 8. Optional live "jam" sessions | USD 950 general; reported discounts to USD 800–855; 6.5 California MCLE hours | Prompt practice in optional sessions. No assessment or implementation output found | Closest on subject. A quarter to a third of the hours. No tax, no organisational information, no pilot. |
| [AI: Implications for Business Strategy](https://executive.mit.edu/course/artificial-intelligence/a056g00000URaa3AAD.html) | MIT Sloan Executive Education with MIT CSAIL / delivered by GetSmarter | Paid | Business leaders; executive education | Six weeks plus orientation, 6–8 hours per week (36–48 hours), online cohort; next start 18 Nov 2026 | USD 3,850 (two instalments of 1,925 for the Nov 2026 cohort) | Weekly modules. Assessment details not found | Strategy-level. No legal, tax or jurisdiction content. |
| [Oxford Artificial Intelligence Programme](https://www.sbs.ox.ac.uk/programmes/online-learning/oxford-artificial-intelligence-programme) | Saïd Business School, University of Oxford / GetSmarter (a 2U brand) | Paid | Business leaders; executive education | Six weeks, 7–10 hours per week (about 42–60 hours); next start 11 Nov 2026 | USD 3,280 on GetSmarter; other listings differ | Weekly assignments, no formal exam (reported) | Broad AI-for-leaders. No legal anchor. |
| [AI Essentials for Business](https://pll.harvard.edu/course/ai-essentials-business) | Harvard Business School Online | Paid | Business professionals; online executive education | Four weeks, 5–7 hours per week (about 20–28 hours), start anytime | USD 1,949 per the Harvard page (older listings USD 1,850) | Cohort-style activities; details not captured | Comparable hours. General business. |
| [AI Strategy and Governance](https://www.coursera.org/learn/wharton-ai-strategy-governance) | Wharton, University of Pennsylvania / Coursera (course 4 of the Wharton AI for Business specialisation) | Paid or audit; sources conflict | Beginners; business | Self-paced, about 12 hours | Price not confirmed (a third-party figure is USD 49 per month) | Not found | Strong on governance and fairness. No practice with documents. |
| [AI Strategy](https://www.reforge.com/courses/ai-strategy/) | Reforge / own platform | Paid, membership only | Product, growth and marketing professionals | Self-paced, 26 lessons, about 2 hours per week | USD 1,995 per year, individual membership, no single-course option (search summary of the pricing page) | Not found | Weak comparator. Aimed at product teams. |
| [Transformational Leadership in Artificial Intelligence](https://www.lbs.edu.ng/executive-education/open-seminar-prog/transformational-leadership-in-artificial-intelligence/) | Lagos Business School, Pan-Atlantic University | Paid | C-suite, board, senior public sector; executive education | Three days, hybrid, campus. The 1–3 Sept 2026 run is over; next intake not found | NGN 1,200,000 excluding VAT (NGN 1,290,000 including VAT on the registration page) | African case studies reported; assessment not found | The only African executive comparator found. Short and high-level. |
| [AI for Everyone](https://www.coursera.org/learn/ai-for-everyone) and [Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone) | DeepLearning.AI (Andrew Ng) / Coursera and deeplearning.ai | Free access or low-cost certificate; conditions changed in 2025 and sources conflict | Non-technical; business | About 7 hours and about 5–6 hours; self-paced | Certificate about USD 49 per month on Coursera, or a DeepLearning.AI Pro plan at USD 25 per month (third-party figures) | Quizzes. Project lifecycle and an introduction to RAG in the second course | Covers Session 1 and part of Session 2 vocabulary at near-zero cost. |
| [AI Fluency: Framework and Foundations](https://www.coursera.org/learn/ai-fluency-framework-foundations) (also on Anthropic's Skilljar site) | Anthropic with academic authors / Anthropic's Skilljar site and Coursera | Free | General learners | About 3 hours, self-paced | Free. Certificate via Skilljar only | Four-competency framework (Delegation, Description, Discernment, Diligence) | Names the supervisory competencies this course teaches. |
| [Google Cloud Generative AI Leader](https://cloud.google.com/learn/certification/generative-ai-leader) | Google Cloud | Exam fee | Managers and directors | 90-minute exam, 50–60 questions, no prerequisites | USD 99 plus tax (the launch announcement and the certification page, per a search summary) | Multiple-choice only | A credential for leadership vocabulary. No applied work. |
| [Microsoft Certified: AI Transformation Leader (AB-731)](https://learn.microsoft.com/en-us/training/courses/ab-731t00) | Microsoft / Microsoft Learn | Free learning; exam fee | Business leaders | One-day course; exam | Exam USD 99 reported by third parties | Exam | Vendor-specific (Copilot and Foundry). |
| [OpenAI Academy](https://academy.openai.com/) | OpenAI | Free | General practitioners | Short courses (AI Foundations about 70 minutes) | Free with a ChatGPT account | A badge on an assessment | Teaches one product family. |
| [IBM SkillsBuild: AI Fundamentals](https://www.ibm.com/training/badge/artificial-intelligence-fundamentals) | IBM / SkillsBuild and Credly | Free | General | About 10 hours | Free | Quizzes | Foundations; one reviewer calls it "a mile wide, an inch deep". |
| Generative AI Explained (free) and Building RAG Agents with LLMs (paid) | NVIDIA Deep Learning Institute | Free and paid | The first is non-technical; the second is developer training | About 2 hours; about 8 hours | Free; USD 90 for the RAG course (third-party page summary) | Developer labs | Developer comparator. Not suitable for this learner. |

Executive education, in this table, is the MIT, Oxford, Berkeley and Lagos programmes. Harvard Business School Online and the Wharton course are online professional education. Developer training is the NVIDIA RAG course. Platforms are Coursera, GetSmarter (2U) and Skilljar.

### Price reference points

You gave no fee, so these are reference points and not a recommendation. They use the hours reported above, and they are self-paced or cohort programmes, so a one-to-one live course is a different product.

| Comparator | Reported price | Reported hours | USD per hour | Equivalent for 24 hours |
|---|---|---|---|---|
| Berkeley Law | 950 | 6–8 | 119–158 | 2,850–3,800 |
| HBS Online | 1,949 | 20–28 | 70–97 | 1,670–2,340 |
| MIT Sloan / CSAIL | 3,850 | 36–48 | 80–107 | 1,925–2,570 |
| Oxford Saïd | 3,280 | 42–60 | 55–78 | 1,310–1,870 |

### What to take from the benchmarking

- Add the generation, reliability and responsible-use basics that every free path includes. They are cheap to teach and the learner will otherwise meet them elsewhere.
- Add a baseline and a repeat measure. Several programmes use weekly assignments or quizzes (Oxford, DeepLearning.AI, IBM). The course has none that discriminate.
- Consider asking the Uganda Law Society whether it recognises continuing-development hours for a course of this kind. Berkeley sells 6.5 MCLE hours, which lawyers value. I could not verify whether such recognition exists locally.
- Keep the one-to-one, document-based work. None of the comparators lists legal and tax documents from the learner's jurisdiction, work on her own tools or a pilot proposal. That claim rests on public pages I did not open, so it needs checking against full syllabi before it is made in marketing.

### What not to take

Programming, MLOps, model-fine-tuning labs, certification exam preparation, a catalogue of vendor tools, and every provider's ethics module. The brief asks for decisions about adoption and none of those change a decision she will make.

## 8. Priorities

### Must fix before teaching

1. **M1 Matter and exercise facts.** Resolve C6 and C7 and write definitive expected answers for the changed-fact tasks.
2. **M2 Notes.** Replace the five template questions and their expected answers, correct C2, C11, C12, C17, C18, C19, and remove the 286 identical "If unclear" lines in favour of slide-specific rescue lines for at least the 60 core slides.
3. **M3 Generation mechanism.** Add the missing content (section 9). Without it the first outcome is not met.
4. **M4 Timing.** Replace the single time table with a per-session plan and mark core and optional slides. Cut Session 2 and Session 8 load first.
5. **M5 Rehearse and record.** Run each live task with the actual tools and accounts. Save the real outputs as the fallback. Rehearse the Session 8 build end to end.
6. **M6 Verify Session 6.** Check the judgment pinpoint, the statute edition and numbering, and decide on the proposition (C8, C9).
7. **M7 Session 10 screenshot.** Confirm origin and crop the name (C15).
8. **M8 Count mismatch.** Align the flawed findings (C10).
9. **M9 Facilitator readiness for Uganda.** Verify and add the instruments in C21.
10. **M10 Workbook answers.** Withhold the "Worked reference" text until after each session, or remove it.

### Useful improvements

- Replace three mechanism diagrams (S2 10, 14, 18) and add a RAG architecture diagram (S5 6). Replace the S9 bar chart with a waterfall.
- Add a real-length agreement and a 30–50 document set so a failure can occur.
- Merge Sessions 9 and 10 (section 9).
- Add a diagnostic on entry and a teach-back check each session: "Explain it to a partner who has not seen the slide."
- Vary the changed facts: one per session, never reused.
- Provide filled exemplars for the register, one-page use rule and pilot proposal.
- Add a plain-language glossary of 25–30 terms.
- Add a 15-minute data-terms segment in the tools session.
- Tie S10 to the real route and PRN step, after verifying on the URA page.
- Name real incidents of lawyers filing AI-invented citations, after verifying each, as one slide in Session 6 or 11, and give the Stanford figure with its date.

### Optional extensions

- One optional transfer exercise per interest area at the end of Session 12 (a mobile-money regulatory change brief, a telecom contract-obligation extraction, an investment claim check).
- A 30-60-90-day follow-up call.
- A short follow-on on evaluation and agent building for when she wants more technical depth (Session 12 slide 20 already offers it).
- CPD recognition, if available.
- A recorded 10-minute recap for each session for flexible scheduling.

## 9. Structure recommendation: keep 12 sessions, reorder lightly, reduce, and add one block

**Retain** 12 sessions of two hours. Your brief fixes 24 hours, the sequence is logical, and the single-matter design works.

**Reduce.** Merge Sessions 9 and 10 into "Tax evidence workflow and controlled actions". They share data and the control logic of Session 8. Keep from Session 10 the process boundaries (slide 4), the uncertain-status and retry rule (slides 13–14), the audit record (slide 15) and a shortened mock-page test. Trim definition-level slides to notes: S1 6–7, S2 7 and 20, S4 16, S5 17, S7 5–6, S8 11–12. Target 12–14 core slides per session.

**Add.** Use the freed session for **"How a language model produces an answer"**, placed after Session 2. Content: next-token prediction in words, sampling and why the same prompt gives different answers (run it three times live), the context window and what happens when a clause falls outside it, why fluent errors occur, what "reasoning" modes, web search and tool calls add, multimodal input, cost per token as a planning figure. Live work: the clause 3 question run three times; a long document with the exception buried in the middle; a deliberate question the sources cannot answer.

**Reorder.** Move the data-terms question (consumer versus enterprise plans, training opt-out, retention) to the tools session. Move the explanation of how information is used by tools (Session 2 slide 21) next to it.

**Proposed sequence**

| New # | Title | Source |
|---|---|---|
| 1 | Understanding AI in the firm | Old 1, trimmed, live opener |
| 2 | How AI learns and represents language | Old 2, trimmed |
| 3 | How a language model produces an answer | New |
| 4 | AI tools, instructions and safe use | Old 3 plus data terms |
| 5 | Preparing the firm's information | Old 4 |
| 6 | Internal knowledge search and retrieval | Old 5 |
| 7 | Legal research and deep research | Old 6 |
| 8 | Contract review and drafting | Old 7 |
| 9 | Automation and agentic AI | Old 8 |
| 10 | Tax evidence workflow and controlled actions | Old 9 and 10 |
| 11 | AI risk and organisational governance | Old 11, given more time |
| 12 | Leading an AI-native organisation | Old 12 |

**Time model per session:** 10 recap and retrieval practice; 40–45 explain and ask on core slides; 40 guided practice with real tools; 15 decision and check (8–10 in Sessions 1–10); 10 buffer and break. Because dates are flexible, a session that overruns by agreement does not break the sequence.

---

# Part 2: comparison with the existing Benchmark Review

I opened `05 Course Maintenance/Benchmark Review.txt` after Part 1 was complete. Part 1 changed afterwards only to correct my own counts and wording (the term counts in the verdict, the 26-slide template description, one example in 3.9, and some table labels). No conclusion changed as a result of reading the review. I did not read the other maintenance records or the authoring files.

## What the review is

A nine-provider coverage comparison dated 26 October 2026: DeepLearning.AI, Wharton on Coursera, Reforge, IBM, NVIDIA, Microsoft, Google Cloud, Anthropic and OpenAI. For each provider it states what the public outline covers, where the course covers the same ground, and which change followed. It closes with a design and delivery check and a pre-class rehearsal note.

## Where I agree

1. **The sequence is suitable.** The review's opening sentence, and my section 1, reach the same view of the order: foundations, language models, tools, information, retrieval, research, contract, automation, tax, governance, adoption.
2. **The limits on the benchmarking are stated honestly.** It says it compares published coverage and not qualifications, that paid course interiors were not reviewed, that IBM's badge page was not fully readable, that NVIDIA's catalogue is historical, and that Coursera is a platform. These match the access limits I report.
3. **Animation claims are modest.** It says only Session 8 slide 13 was played in PowerPoint. My XML check supports the click counts, and I add that playback remains unverified.
4. **The counts are right.** 286 slides, 12 decks, four course documents and four attributed images match what I found.
5. **The changes it lists exist in the files.** Slide 2 recaps, three closing questions per session, the In-Class Progress Record, the Session 2 slide 22 training sequence, the Session 3 slide 17 cycle, the RPA expansion on Session 8 slide 6, the Session 5 slide 17 comparison and the Session 12 slide 15 table are all present as described.
6. **Rehearse before teaching.** Its final section and my must-fix M5 say the same.
7. **Keep the course out of the technical-engineering lane.** It leaves programming, network mathematics and large-model training to later study. I agree, and I extend this to an explicit "what not to take" list.

## Where I disagree, and why

| # | Review position | My assessment | Evidence |
|---|---|---|---|
| 1 | Sessions 1–5 "establish these distinctions" that the DeepLearning.AI outlines cover, including limitations. | Coverage of limitations is overstated. The course never explains how a model produces an answer, why the same prompt can give different answers, what a context window is, or what a hallucination is. | Term search across all slides and notes: "probability", "temperature", "context window" absent; "hallucinate" once, in a Session 6 note; next-token prediction only as a table row (S2 slide 6) and a note phrase (S2 slide 22). The review's own comparator material is described as progressing "from terminology and limitations". |
| 2 | The most useful refinements, including stronger recall between classes and explicit checks of understanding, "are implemented". | They exist on paper and are weak in operation. The recap on slide 2 is the facilitator stating the last result, which gives her nothing to retrieve. The closing checks restate sentences from the preceding two slides. The same changed fact is reused four times. There is no baseline. | S2 slide 2 notes ("I will recall the earlier result with the learner" plus the generic question "What would a useful result look like?" on all 12 decks). S9 slide 20 versus slide 22. Client Instruction, S3 17 and 25, S7 23, Fresh Test 1. |
| 3 | "Specific closing questions now check understanding in every session." | The closing questions are specific. Sixty other questions are templates, and the expected answers to the check questions are one-sentence summaries with no scoring guidance. | 231 unique Ask lines across 286 slides; five template Asks account for 60 slides. Teaching Resources hold one sentence per session. |
| 4 | "All slides had a full visual review ... Package/layout checks found no unresolved findings." | I found unresolved findings in the shipped decks. | S2 slide 18 has no relation lines although the notes say to show them. S4 slide 10 image truncated. S10 slide 5 screenshot shows a named logged-in user. Cue lines say "Reveal the diagram stages" on slide 2 of every deck, which has no animation. S4 slide 5 notes describe an image the slide lacks. |
| 5 | Session 12 slide 15 "distinguishes doing an existing task faster from proposing a different client service." | The distinction is sound. Its sources are two training-course marketing pages (Reforge and a Coursera landing page). A partner reading the notes sees two course landing pages as the evidence for a service-design idea. | S12 slide 15 sources line. I recommend removing both URLs (C19). |
| 6 | CAG added on Session 5 slide 17 to compare direct context, RAG and CAG. | The direct-context versus RAG comparison is useful. CAG adds a term she will rarely meet in vendor conversations, while the embedding-model versus language-model distinction, which she will meet in every retrieval product, is missing. | S5 slide 7 notes and slide 6 (no two-model statement; no diagram of the pipeline). |
| 7 | The comparator set is nine provider outlines, mostly free or low-cost vendor learning paths plus Reforge. | The set omits the comparators closest to this learner, although the course's own `Public Sources.txt` lists two of them. It has no executive-education programme for lawyers and no cohort executive programme. | `Public Sources.txt` lists `berkeley:` (Berkeley Law Executive Education) and `mit:` (MIT Professional Education) URLs. The review discusses neither. It also gives no price, hours, format, audience type, assessment or implementation component. |
| 8 | The benchmark supports the existing progression. | The benchmark here is used mainly to confirm. It does not test where the course is thin. | The review's changes are additions to slide text; none reallocates time, adds a missing topic or removes material that the free paths already cover. |
| 9 | Several providers are developer tracks (OpenAI building-agents track, NVIDIA catalogue). | The review marks NVIDIA as a later technical extension. It does not label the OpenAI track as developer training, and it uses evaluation guidance written for engineers as support for a non-coding session. | Review items 5 and 9. The point for the course is sound (task-specific tests, edge cases, a baseline). The label should say developer. |
| 10 | Governance coverage is aligned with Wharton's outline (privacy, bias, governance). | Aligned in topic list. Thin in treatment. The bias slide is generic, no Ugandan instrument is named, and Session 11 has the same 25-minute concept block as every other session. | S11 slides 5–6, 11; Facilitator Guide time table. |

## What the review does not address, and I do

- **Timing.** It does not examine whether 214 concept slides fit in 12 × 25 minutes.
- **Teaching support.** It does not examine the notes, the boilerplate, or the absence of model answers and saved runs.
- **Exercise design.** It does not examine the scripted nature of the failures, the toy-size documents, or the ambiguous changed fact.
- **Factual checks.** It does not mention the OECD attribution, the findings count, the judgment pinpoint and statute edition, or the fact-pattern drift.
- **Value for money.** It does not separate educational value from price.
- **Reference points.** It gives no price or hours for any comparator.

## Net effect on my conclusions

The review supports the course's broad shape and supplies useful provenance for several slides. It does not change my verdict. It reinforces two recommendations: keep the course out of developer territory, and keep the rehearsal-first rule for live tools. It leads me to soften one point: the course already contains more explicit evaluation and approval material than a typical executive path, which is a real strength and is why I rate applicability highly.

## Questions for discussion

1. Do you agree that a new "How a language model produces an answer" block belongs in the course, funded by merging Sessions 9 and 10?
2. Which side does Kampala Legal and Tax act for in the matter, customer or provider? C7 depends on it.
3. Will she hold the workbook before each session? If yes, the "Worked reference" text should be removed from her copy.
4. Can I be given access to the judgment text and the statute editions, or can you confirm C8 and C9 yourself? I could not open ULII.
5. Do you want a full per-session run-sheet drafted once these decisions are made? That would be a new document, so I have not started it.

---

# Part 3: re-review of the revised edition (26 October 2026, afternoon)

You revised the course after Parts 1 and 2. I re-extracted every slide, note, document and practice file, rendered all 285 slides, ran the code and recalculated the data. I did not open `05 Course Maintenance/Review Response.txt` until my own findings were complete; section 8 compares them. Part 1 above describes the earlier edition and is kept for the record.

## 1. What changed, verified

- The course has 285 slides: 233 essential and 52 optional, which matches the stated counts. Optional slides sit after each session's closing check and carry an "OPTIONAL EXPLORATION" footer.
- Session 3 is new ("How language models generate answers and fail", 18 slides). Former Sessions 9 and 10 are merged into Session 10. Sessions 4 to 9 and 11 to 12 moved accordingly.
- Each session now has its own 120-minute plan in the Facilitator Guide. Concept blocks run 20 to 45 minutes and practice blocks 25 to 40 minutes. The blocks sum to 120 in every session (I checked all 12).
- The matter is now customer-side. Victoria is the customer, Equator the provider, with base facts and three variants (A share sale, B assignment, C responsibility fails) in `Transaction Variants.txt`.
- New material: a local copy of the Goal Relief judgment (24-page PDF), a 28-section "Long Agreement", a 40-record library, a 123-row ledger challenge, a local workflow demo with an engine in JavaScript, a read-only agent script, 12 saved observed runs, an entry and exit diagnostic with an answer key, a worked risk register, use rule, pilot proposal, cost sheet, vendor and investment due diligence lists, and a Ugandan legal source map.

## 2. Status of my earlier findings

"Fixed" means I checked the revised file. "Partly" and "Open" are explained in section 3.

| Earlier item | Status | Evidence |
|---|---|---|
| Generation mechanism missing (verdict point 1) | Fixed | New Session 3: next-token distribution (slide 4), growth by token (5), decoding and temperature (6), context window (7), fit versus use (8), attention (9), hallucination defined (10), reasoning, search and tools (11), modalities (12), cost (14). Three experiments with a run record. |
| Toy documents, scripted failures | Partly | Larger fixtures exist, but they are padded or too easy (N4, N5, N7). |
| Timing | Fixed, with exceptions | Per-session plans, 3.5 to 7.5 minutes per concept slide. Session 11 practice and Session 12 practice are tight (N8). |
| Notes boilerplate | Partly | The 286 identical "If unclear" lines are gone. Two identical lines still sit on all 285 slides, and a rotating three-misconception line replaced them (N1). |
| Weak checks, no baseline | Fixed, with exceptions | Entry and exit diagnostic, unique recall question per session, variant per session (A in 4, B in 8). The diagnostic omits the new Session 3 content (N10). |
| Fact pattern (C7) | Fixed | Matter Brief, Client Instruction, slide 3 of Session 1, playbook v2. "Planned buyer" no longer appears anywhere. |
| Changed fact (C6) | Fixed | Variant A answer is definitive and correct on the clause. Variant B answer ("clause 3 alone does not settle assignment") is correct, and the Long Agreement contains no assignment clause. |
| C1 OECD definition | Fixed | Session 1 slide 5 is now an "AI system" paraphrase with the OECD memorandum as source and a note that it is a paraphrase. |
| C2 vacuous opening answers | Fixed | Every slide 1 and 2 carries a substantive recall question and answer. |
| C3 attention slide | Fixed | Session 3 slide 9 draws weighted arcs from "provider", "responsible" and "other context" to "its", labelled invented. |
| C4 CNN/RNN | Fixed by demotion | Now optional (Session 2 slide 24). The note still mentions GRUs. |
| C5 Coursera source | Fixed | Session 2 slide 15 cites arXiv 2203.02155 and the Google crash course. |
| C8 judgment pinpoint | Verified | In the PDF, printed page 3 line 25 reads "Section 27(2) of the Tax Appeals Tribunal Act Cap. 341 (7th Revised Edition)", and the quotation sits at lines 27 to 28 ("An appeal to the High Court may be made on questions of law only, and the Notice of Appeal shall state ..."). The course's "lines 24–27" is accurate for the heading through the opening of the quotation. The K-Files citation (section 28(2), 2023 Revised Edition, printed page 6) I could not open. A search could not confirm its neutral citation. The course treats the discrepancy as something to resolve, which is the right stance. |
| C9 substantive research | Fixed | Ground 5 (pp 22 to 24) concerns VAT on the 10% programme delivery fee as an imported service, and the court dismisses the appeal (p 24). The slide's expected answer ("rejects the appellant's treatment") is vague; see N11. |
| C10 two versus three findings | Fixed | Slide, file, guide and workbook all say three. One stale note remains (N3). |
| C12, C13, C14 | Fixed | Interim totals shown (Session 10 slide 5). Waterfall-style chart with 80 received and 18 outstanding (slide 6). |
| C15 named URA user | Fixed by removal | No URA screenshot remains. |
| C16 images | Partly | Session 5 slide 5 now shows the synthetic scan. Session 5 slide 10 is uncropped but too small to read. The scan is barely degraded (N5). |
| C17 cue mismatches | Fixed | Each animated slide's notes state the click count. The counts in the notes, the Animation Guide and the slide XML agree on all 34 slides (126 clicks). One claim is wrong (N12). |
| C18, C19 | Fixed | |
| C20 two models | Fixed | Session 6 slide 6 is a two-path architecture diagram with a separate embedding model and language model. It renders cleanly. |
| C21 Ugandan frame | Fixed, mostly verified | Session 11 slide 5 and `Uganda Legal Frame.txt` name the Data Protection and Privacy Act 2019 (sections 19 and 29), the 2021 Regulations and Evidence Act section 125. A search summary corroborates sections 19 (processing outside Uganda) and 29 (register). |
| C22 timing table | Fixed | |
| C23 notes | Partly | See N1 and N2. |
| M5 rehearse and record | Partly | Real outputs saved for general-assistant tasks and a local agent route. Portal builder, enterprise search and live deep research remain unrehearsed, which the course states. |
| M10 workbook answers | Fixed | The workbook now holds working prompts and blank record tables. Answers sit in Teaching Resources. |
| Data terms in tools session | Fixed | Session 4 slide 5 and slide 15 (vendor questions). |
| Exemplars | Fixed | Worked risk register, use rule, pilot proposal, cost sheet. The cost sheet has no labour rate (N14). |
| Merge of Sessions 9 and 10 | Done | |

## 3. Remaining and new findings

Severity: **A** fix before teaching, **B** worth fixing, **C** minor.

**N1 (A). The "If partly correct" lines are assigned by position and often do not fit the slide.** Each deck has exactly three "Likely confusion" lines, and they rotate across all slides (36 distinct lines in the whole course, 285 slides). Session 1 examples: slide 4 (which source has authority) carries "AI means ChatGPT"; slide 5 (the AI definition) carries "A fluent answer is sufficient"; slide 14 (information boundary) carries the same. The Facilitator Guide's misconception lists are good. The slide-level lines are not. Fix: keep a rescue line only where a real confusion attaches (about 60 core slides) and delete the rest.

**N2 (A). Forty-eight slides carry a non-question or a template in the "Ask" field.**
- Twelve "Our in-class work" slides: "Ask: Before we begin: Sort six short document descriptions ..." is an instruction.
- Twelve "Check understanding" slides: "Ask: Variant A: share sale", "A changed extraction", "A pilot that fails its test" are labels.
- Twelve "What we can conclude" slides all ask "Which part of today's result remains unverified?", and twelve "firm decision" slides ask "What evidence would change this proposed decision?". The expected answers restate slide text.
- Slides 1 and 2 of every deck ask the identical question twice.
Fix: turn the check labels into the actual three questions already on the slide; give conclusion slides a question the learner can fail; drop the duplicate on slide 1.

**N3 (B). Stale or mismatched notes.**
- Session 2 slide 11 notes describe the old map ("contract, agreement and clause near one another, with tax and invoice in another region"); the slide now plots a query, clause 3, a support clause, an invoice term and a photograph consent.
- Session 8 slide 9 notes say "repair both findings"; the slide lists three.
- Session 5 slide 5 notes describe "two representations of the same clause. Search for responsible"; the slide shows a synthetic scan and refers to an observed OCR run.
- Session 2 slide 15 (training stages) asks "What should the system do when the source does not answer?"; Session 3 slide 9 (attention) asks about "charge".
- Session 10 slide 6 notes still say "show the four values 125, 100, 98 and 80".

**N4 (A). The "Long Agreement" is not a long agreement.** Sections 1 to 11 are the short contract expanded. Sections 12 to 28 describe the course itself: "The execution host enforces permitted tools, destinations and budgets" (20), "The local class simulation has no taxpayer identity and no URA connection" (23), "The local demonstrator illustrates an uncertain acknowledgement" (24), "A model may propose a request for the schedule but must not supply a fee" (26). Every section ends with the same two filler lines (56 repeated sentences). The file is about 20 KB (roughly 4 to 5 thousand tokens), so a current model will read it whole. A lawyer will see within a minute that it is a teaching artefact, and the model-addressed sentences hand the assistant the answers and behave like injected instructions. The Session 3 "fits in the window does not mean used correctly" lesson cannot appear with this file. Fix: use a genuine long agreement (a real public template with defined terms, cross-references and schedules, 15 to 30 thousand tokens or more), or drop sections 12 to 28 and the experiment's promise.

**N5 (A). The course promises failure ("and fail") and the saved evidence shows almost none.** The seven saved general-assistant outputs include three consent runs that agree in substance, a correct missing-fee answer, a correct share-sale answer with unnecessary caveats, one confounded reconciliation error and its fix. The Apple Vision OCR run preserved the negation, and the "synthetic scan" is barely degraded (clean sans-serif text, slight blur). The injection trace shows the model ignoring the note. The Guide's rule "do not force a failure" is honest, and the run review is candid. The result is a session titled "how language models fail" in which the learner may see no failure. Add checkable tasks where failure is likely: (a) ask without sources for the authority on appeals to the High Court in tax matters and check each citation on ULII; (b) the first reconciliation prompt as saved (it produced an invented "educational exemption" and a "declared tax basis"); (c) a genuinely degraded scan with a small-print negation; (d) a question that spans two of the 40 records.

**N6 (B). The agent demonstrations cannot show a defence working.** The unknown-ID trace is a request the user made, the budget trace configures a limit of zero (not exhaustion), and the injection trace shows the model not following the note while the host offers only a lookup. Add a scripted host test that feeds the host a proposed `send` request and a second lookup against a limit of one, so that the learner sees DENIED and HELD from the host itself. The route also needs the instructor's Claude CLI at `/opt/homebrew/bin/claude`, so the live model-selected demonstration is single-vendor and single-machine. The saved traces are the fallback.

**N7 (B). The retrieval library gives the answer away.** The 40 records are three-line stubs (about 330 bytes each) on six subjects. Most say "does not amend CONTRACT-01 v2" and some say "This is not the change-of-control clause" (record 07). The local search ranks by word overlap including common words, ties at a score of 1, and returns five results even when nothing answers ("What is the signed fee?" returns five tied records). It is labelled as not embeddings, which is honest, and the guide says use a connected product if available. Result: the session's central mechanism (vectors) is never run unless a product is available. Fix: write 40 records with real content, remove the self-describing sentences, and add a small embedding-based search the facilitator can run offline, or schedule one product demonstration.

**N8 (A). Session 11 practice is overloaded and one task has no data.** Practice time is 40 minutes (10 demonstration, 30 guided) for four tasks, one of which is a 20-minute incident. The other three tasks (adapt a register, compare unequal errors, draft a use rule) get about 20 minutes. The "compare error rates for difficult scans and clean text" task, and slide 9's "clear typed English and degraded mixed-language scans", have no data in any practice file (no file mentions mixed-language or degraded text; the extraction run record is blank). Fix: supply a small table of observed extraction errors per collection, or cut the task.

**N9 (B). Definitions sit on optional slides while essential slides use the terms.** "Neural network" (Session 2 slide 21, optional) is used on essential slide 8. "Model" (Session 1 slide 20) is used from Session 1 slide 10. "Automation" and "API" (Session 9 slides 20 and 21) are used on slides 4 and 5. "Token IDs" (Session 2 slide 22) and "foundation model" (Session 2 slide 23) are optional. Fix: add a one-line definition to the essential slide's note, or promote the definition slide.

**N10 (B). The diagnostic omits the largest addition.** The five entry and five exit items cover arithmetic versus generation, upload versus training, citation checks, rejection and cross-matter access. None tests next-token generation, variation, the context window, hallucination, retrieval versus answer failure or data terms. Add two items, for example: "The same prompt gives two different answers. What does that tell you?" and "The document fits in the window. Why can the answer still omit the exception?"

**N11 (C). Imprecise expected answer on Goal Relief.** "Goal Relief rejects the appellant's treatment of the programme delivery fee and dismisses the appeal" does not say what the court held. From pp 22 to 24: the court found that Goal Ireland provided fundraising services to the appellant, that the service was imported, and that VAT was correctly assessed. Replace with that sentence and add the relevant provision named in the judgment (VAT Act section 5(1)(c), recipient liability, as cited by the court).

**N12 (C). Animation Guide claim.** It says "A slide footer states its actual click count". No footer does; the count appears in the notes only. The click counts themselves are correct. Playback was sampled only for Session 3 slide 4.

**N13 (C). Typos in the Facilitator Guide:** "clause2’s", "VariantB", "clause4", "Ground5", "Day90"; workbook: "for discussion; We will".

**N14 (C). Cost sheet.** The guide asks for "total cost and review effort", but the sheet has no hourly cost, so review minutes cannot become money. The token arithmetic (10,000 in, 1,000 out per task at invented rates, about USD 0.014 per task) shows token cost is negligible beside the UGX 240,000 monthly fees, which is itself a useful point to teach. Add one labour-rate line.

**N15 (B). Visual gaps.**
- Session 3 slide 10 (hallucination, the session's central term) is two lines of text with no visual.
- Session 3 slide 7 (context window) draws four equal boxes, so it cannot show the capacity limit that is the slide's point. A bar with a fixed length filled by the four parts would.
- Session 5 slide 10 (Microsoft layout image) is uncropped but its labels are unreadable at slide size.
- The 4-box template remains the default for 20 or more slides; the new Session 6 slide 6, Session 3 slide 9, Session 10 slide 6 and Session 2 slides 8 and 11 show what purpose-built diagrams add.
- Static render (final state) checked on all 285 slides. Animation playback remains unverified by me.

**N16 (B). Tax analysis is still thin in Session 10 itself.** The essential path teaches evidence checks (FDN validation guidance, missing reference is not fraud) and the controlled action. The statutory question (VAT on imported services, withholding on payments abroad) lives in Session 7 through Goal Relief. The two are linked in the Matter Brief ("Victoria may procure overseas software/support"), but Session 10's reconciliation contains no payment to an overseas supplier. Adding one such line to the Ledger Challenge would let the learner test whether the reconciliation raises the Session 7 question. This is a design suggestion.

**N17 (C). Session 1 sequencing.** The Guide asks for the oral diagnostic before the explanatory slides, but slide 16 of the deck repeats that instruction after the concepts, and the 10-minute opening block must hold the diagnostic (five questions with reasons) as well as slides 1 and 2. Two minutes per item uses the whole block.

## 4. Timing, re-assessed

Essential slides per session are 18 to 20. Concept slides per block (Guide): S1 9 in 35 minutes, S2 13 in 45, S3 10 in 35, S4 8 in 30, S5 8 in 30, S6 8 in 35, S7 5 in 30, S8 6 in 30, S9 7 in 35, S10 4 in 30, S11 6 in 40, S12 4 in 20. That is 3.5 to 7.5 minutes per slide, which supports a question and discussion on each. The earlier concern is resolved. Remaining pressure points: Session 11 practice (N8), Session 12 guided block (diagnostic repeat, proposal adaptation, cost and stress calculation and owners in 40 minutes), Session 9 guided block (agent route, injection, budget, approval, stale approval and decline in 35 plus 15), and Session 1 opening (N17). The block ranges printed in each Guide table do not always match the slide order (for example, Session 5 lists slides 14 to 16, which are concept slides, under guided application).

## 5. What I verified by running or recalculating

- Ledger Challenge: raw 60,800,000; unique 59,400,000; duplicate difference 1,400,000 (INV-C013, C048, C094); credits 750,000; net 58,650,000; September receipts 30,000,000; outstanding 28,650,000; one October receipt of 1,500,000 excluded; seven blank references (C017, C034, C051, C068, C085, C102, C119). All match the answer key.
- Workflow engine: prepare gives 98,000,000; run without approval is held; a changed field after approval is held; a repeated approved run returns DUPLICATE PREVENTED; a timeout gives UNCERTAIN and blocks retry until status inspection; a third run is held at the illustrative budget of 2.5 credits; a new recipient and a conflicting duplicate are held. All as the Guide states.
- Playbook arithmetic: 600,000 + 3 × 240,000 = 1,320,000; 40 × (30 − 20) = 400; 40 × (30 − 33) = −120.
- Clause 3 text is identical in every slide, record and fixture that quotes it.
- Animation: 34 animated slides, 126 clicks; notes, Animation Guide and XML agree.

## 6. Updated verdict

The revised course now meets the brief far better. The generation mechanism is taught; the matter is coherent and customer-side; the research session reads a real judgment I could check line by line; timing is plausible; the notes expose observed results; and the entry and exit comparison gives a measure of learning. I would teach it once the five items rated A are fixed (N1, N2, N4, N5, N8), together with the stale notes in N3. N6 and N7 come next. The remaining problems sit in the support material and the notes; the core design is sound.

Priorities:

1. **Before teaching:** N1, N2, N3, N4, N5, N8, and the typos in N13.
2. **Next:** N6, N7, N9, N10, N15 and the cost line in N14.
3. **Optional:** N11, N12, N16, N17; a second product demonstration for retrieval; a recorded recap per session.

Limits of this re-review: I could not open ULII, the K-Files judgment, URA or any provider page (the fetch tool is blocked), so the K-Files citation, the Session 4 vendor-terms sources and the benchmark prices in Part 1 section 7 remain unverified by me. I did not run any live assistant, builder or the Claude CLI route. Section 8 compares my findings with the maintainers' response.

## 7. Questions for you

1. Is the long, padded agreement meant as a placeholder? If you can supply a genuine long agreement, N4 and part of N5 go away.
2. Do you want the facilitator notes rewritten as a spoken script with a separate backup file for answers, as in your pitch decks? The current labelled format (Ask, Expected answer, Transition) can stay if you prefer it for teaching.
3. Which AI account will she use in class? N5, N6 and N7 depend on it.

## 8. Comparison with Review Response.txt

I read `Review Response.txt` after finishing sections 1 to 7. It lists the 23 corrections (C1 to C23) as implemented. My checks agree with most, and I disagree with the response on these points:

- **C23 "slide-specific questions/responses and separate answer keys".** Answer keys are separate and the Guide has slide-relevant misconception lists. The slide-level rescue lines are position-rotated (N1) and 48 slides have template or label Asks (N2). The claim is partly true.
- **C11 "session-specific limits and task evidence replace generic expected answers".** True for the opening and closing check questions. Twelve conclusion slides and twelve decision slides still use one generic question each (N2).
- **C16 "uncropped documentation/source images".** Uncropped, yes. The Microsoft image is too small to read (N15), and the scan is barely degraded (N5).
- **C17 "renderer derives cues from actual reveal groups".** True; counts agree. The Animation Guide's footer claim is wrong (N12).
- **"A larger synthetic source is not a guarantee of failure."** Agreed. The larger source is also padded with course text (N4), which is a separate fault.
- **"Portal builders, enterprise connected search and live deep research need account-specific rehearsal."** Agreed, and it is the right disclosure. The agent route on the instructor's Claude CLI is real and saved.
- **"Architecture/data-science/XML/CAG topics remain optional because the user asked for those distinctions."** Agreed on keeping them out of the two-hour plan. N9 lists terms that essential slides use before the optional slides define them.
- **Statement that RAG inference does not train weights while components can be trained separately; attention weights depend on inputs.** Both are accurate. Session 3 slide 9 is worded carefully.

Where the response is stronger than my first review: it changed the substance (new session, saved runs, exemplars, legal frame, diagnostic), not only wording. Where Benchmark Review is concerned, its revised text now states that the first review "was too reassuring about readiness", which matches my Part 2 view, and it reports opening primary pages that I could not open. I cannot check those claims.


---

# Part 4. Implementation record (26–27 October 2026)

Part 3 was approved as the current assessment. This part records what was changed in response, what evidence now exists and what remains open. The detailed file-level record is in `05 Course Maintenance/Maintenance Record - October 2026 Fixes.txt`.

## What was done, by finding

| Finding | Action | State |
|---|---|---|
| N1, N2, N3 (rotated and generic notes, stale notes) | All 285 slide notes rewritten in the teacher's first-person voice: concept in plain words, worked step, a specific question, what a good answer contains, a misconception with a follow-up, a transition. Applied with `apply_lesson_notes.py`; Sources and Playback lines kept. Automated sweep found no template strings, banned words or old clause names. | Done. One note contradicted its slide (Session 6, slide 12) and was corrected. A read-through of all notes by the teacher is still advisable. |
| N4 (padded long agreement) | Replaced by Common Paper Cloud Service Agreement Standard Terms v3.0 with SLA v2.0 (CC BY 4.0). Original file kept unmodified with its hash. Two labelled teaching adaptations (Key Terms replacing Section 12.6, and a supplement to Section 1.5). The signed Fee Schedule is deliberately absent. Every dependent file, slide, answer and the Guide and Workbook were updated. | Done |
| N5 (no observed failure, barely degraded scan) | Reliability is taught with realistic tasks and with all outputs retained. Nine new model runs are saved with their prompts. They are mostly correct, and that is kept as a result. One run given only the Standard Terms reaches the opposite answer, which is a real consequence of missing evidence. A four-step OCR experiment produces measured word accuracy and lost negations. | Done. The runs are single runs by one model family. |
| N6 (agent traces cannot show a defence working) | `agent_host.py` enforces the operation, arguments, matter and call budget. Seven scripted host tests are labelled as such. Four model-selected traces are saved separately. In the traces the model stayed inside the offered clauses and ignored an injected note, so the denial is shown only by the scripted tests. The call budget did stop a model that asked for a second lookup. | Done |
| N7 (library stubs gave the answers away) | 38 realistic records plus the agreement and a draft. Lexical, LSA (vector) and an optional embedding backend. Seven tests with expected phrases. Observed results are saved: lexical passes six of seven, LSA and hybrid fail three or four. | Done. The embedding backend was not run (no download access). |
| N8 (Session 11 overloaded, no data for error rates) | One complete exercise per session. Session 11 uses the observed OCR results. | Done |
| N10 (diagnostic omits Session 3) | 7 entry and 7 exit items with an answer key in Teaching Resources. | Done |
| Accounts and tools | `Run Demonstrations.txt` lists five routes (needs an account, local, needs a command-line tool, needs the real account and rehearsal, saved). No account type is assumed. | Done |
| Smaller findings | Definitions before optional slides, typos, Animation Guide footer, cost sheet with labour rate and calculated rows, Goal Relief wording checked against the judgment PDF. | Done |

## Findings from the new evidence

1. The three repeats of one consent prompt agreed on the substance and differed in wording and length. Length limits in prompts were exceeded in several runs.
2. The Standard-Terms-only run concluded that consent is probably not needed, because it did not have the Key Terms. This is the clearest example in the course of what a model cannot know.
3. In the OCR experiment the moderate condition keeps 54 percent of words, and the key negation ("not required") is lost in the saved moderate scan.
4. Vector search did not beat lexical search on these seven tests. The tests include exact-phrase retrievals that favour lexical search, so the result should be read as a demonstration of different behaviour and not as a ranking.

## Still open

1. Run the embedding backend and save its output.
2. Rehearse any connected retrieval, portal-builder or live research demonstration in the learner's own account before using it.
3. Check the K-Files citation for the Goal Relief appeal-scope point.
4. Re-run the saved runs with the tools the learner will actually use.
5. The builder sources in the maintenance folder are out of date. Do not rebuild without following the Maintenance Record.


---

# Part 5. Consolidation pass (27 October 2026)

The full verification record is `Applied AI and Automation/05 Course Maintenance/Edition Verification Record.txt`. In short:

- **One edition, reproducible.** The live folders 00 to 04 are the teaching edition. A staging build from the authoring sources (`Authoring/Edition`) matches it part for part, and `verify_edition.py --rebuild` passes 24 of 24 checks. The deck builder itself was not run, because its runtime exists only on the author's Mac.
- **Notes.** All 285 were read against their slides. They now address the learner as "you", state whether each cited provision is the Key Terms replacement or the unmodified Standard Terms, and no longer contain a slide label, quotation or date that the slide or matter does not support.
- **Retrieval.** The search script keeps "not" and "no" by default. The earlier removal was a choice of that script's stop list. Dropping the words changed no result. A statement and its opposite return the same chunks under lexical search either way. LSA is described as a classical vector method. The neural embedding route (self-test, run sheet, `sbert` method) is written and not run, because the sandbox has no network or model files.
- **K-Files.** Not verifiable from here, so nothing relies on it any longer.
- **Illustrations.** 176 drawn illustrations (164 content slides, 12 title scenes). No photographs were available offline.
- **Open.** Neural embedding run, rehearsal of connected demos in the learner's account, builder run on the Mac, repeat of the model runs in the learner's tools, PowerPoint playback check, opening the Sources URLs.
