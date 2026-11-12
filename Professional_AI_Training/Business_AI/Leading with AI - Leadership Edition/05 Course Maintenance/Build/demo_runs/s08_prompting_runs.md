# Session 8 recorded runs (6 November 2026)

All runs: Claude, fresh general-purpose subagent session, 6 November 2026; not ChatGPT or Gemini. Each subagent was given only the prompt text (with one line telling it to answer as a chat assistant and use no tools), no key, no hint of the lesson. Replies are saved verbatim in `demo_runs/s08/runs/`; prompts in `demo_runs/s08/prompts/`. The model behind a fresh subagent is a standard Claude model; we cannot switch its thinking mode on or off from here, so these runs compare PROMPTS, not reasoning against standard models (see below).

## Reused runs (Case Runs, 4 November 2026): weak and strong brief
`Case Runs/runs/F1a_weak_brief_run1.md` ("Write the Monday sales email" + data) and `F1b_strong_brief_run1.md` (role, reader, format, limits, "do not invent"). One run each. Check against the data: both weekly totals and product figures are right in both. Weak run: no table instruction, so it chose its own layout; it invented a closing instruction to keep stock of beans and sugar high ("demand is rising") and signed "[Your name]". Strong run: followed the format (subject, two-sentence summary, table, three sentences, one thing to check), addressed Sarah, said the data does not show why volumes rose, and gave one thing to check. Note: its table "Units change" and "Revenue change" columns show the same percentages because prices did not change.

## New run 1: structured output (P1)
Prompt: `prompts/P1_structured.txt` (four invented NVF customer messages; JSON array with fixed fields). One run. Reply: `runs/R1_structured_run1.json`.
Check (Python json.load, field names compared with the list): valid JSON, 4 objects, every object has exactly the seven fields, types in the allowed list. Content vs my reading of the messages: ids 1 to 4 correct; types order, payment, complaint, question correct; item quantities correct (40 and 20; 6; null); amount 4350000 correct; urgency high for the third (correct), low for the fourth (correct), normal for the first (reasonable: "by Friday"). Points a person must still check: customer for message 1 came back as "Mary, Kamuli Fresh Mart" (name and business in one text field); reference for message 2 came back as one text "INV-2291, MM88231" (the invoice number and the payment reference joined; the schema asked for one reference); message 3 customer null (none given; correct) and its product "cooking oil jerrycans" without the 20L size (the message gave none); product names vary in wording ("maize flour 25kg bags").
Lesson: a fixed format makes the output checkable by a program, and shows where the schema was too loose (one reference field for two references).

## New runs 2 to 5: a multi-step payroll calculation, four prompt variants (controlled comparison)
Task (invented NVF payroll case): salary UGX 1,800,000 for 160 hours, 12 weekday overtime hours at 1.5, 6 Sunday hours at 2, one unpaid leave day at salary/22, 5 percent employee and 10 percent employer pension on gross, a UGX 150,000 advance repaid after pension. Key, worked in Python and re-verified on 6 November 2026 (second computation): hourly 11,250; overtime 202,500; Sunday 135,000; leave 81,818.18; gross 2,055,681.82; employee pension 102,784.09; net 1,802,897.73 (UGX 1,802,898); employer pension 205,568.18; total cost 2,261,250.

Why four variants: the first comparison (plain against framed) changed more than one thing, because the framed prompt also ended with "Check your answer by re-adding the lines before you reply". Two controlled variants were made, each changing ONE thing (checked with diff):
- P2 plain: facts and the question. (Original.)
- P3 framed + re-add: goal, facts, rules listed, what to send back, "say which rule is unclear", re-add sentence. (Original.)
- P4 framed, no re-add: P3 with only the final sentence ("Check your answer by re-adding the lines before you reply.") removed. It still asks for the working so that each line can be checked.
- P5 plain + re-add: P2 with only that same sentence added at the end.

Each run: Claude, fresh general-purpose subagent session, 6 November 2026, given only the prompt text (plus one line: answer as a chat assistant, use no tools), no key. Replies saved verbatim in `runs/`.

| Variant | Prompt file | Run | Reply file | Net pay | Total cost | Result |
|---|---|---|---|---|---|---|
| Plain | P2_plain.txt | 1 | R2_plain_run1.md | 1,802,898 | 2,261,250 | right |
| Plain | P2_plain.txt | 2 | R2_plain_run2.md | 1,612,898 | 2,041,250 | WRONG (gross 1,855,681.82, 200,000 slip in the addition) |
| Plain + re-add | P5_plain_plus_readd.txt | 1 | R5_plain_plus_readd_run1.md | 1,802,898 | 2,261,250 | right |
| Plain + re-add | P5_plain_plus_readd.txt | 2 | R5_plain_plus_readd_run2.md | 1,802,898 | 2,261,250 | right |
| Plain + re-add | P5_plain_plus_readd.txt | 3 | R5_plain_plus_readd_run3.md | 1,802,898 | 2,261,250 | right |
| Framed, no re-add | P4_framed_no_readd.txt | 1 | R4_framed_no_readd_run1.md | 1,802,898 | 2,261,250 | right |
| Framed, no re-add | P4_framed_no_readd.txt | 2 | R4_framed_no_readd_run2.md | 1,802,898 | 2,261,250 | right |
| Framed, no re-add | P4_framed_no_readd.txt | 3 | R4_framed_no_readd_run3.md | 1,802,898 | 2,261,250 | right |
| Framed + re-add | P3_framed.txt | 1 | R3_framed_run1.md | 1,802,898 | 2,261,250 | right |
| Framed + re-add | P3_framed.txt | 2 | R3_framed_run2.md | 1,802,898 | 2,261,250 | right |

Totals: plain 1 of 2; plain + re-add 3 of 3; framed, no re-add 3 of 3; framed + re-add 2 of 2. Overall 9 of 10 right; the one wrong run is the only one with neither framing nor a re-add sentence. Net pay in the P5 runs was given to the cent (1,802,897.73), which rounds to the key.
Observations: all three P5 runs wrote out a re-add check section; none of the P4 runs did (they listed assumptions instead, as the framed prompt asks, and noted that PAYE and NSSF-type items were not included).
Reading, stated plainly: with framing alone (P4) 3 of 3 were right, against 1 of 2 for the plain prompt; with the re-add sentence alone (P5) 3 of 3 were right. Each change is consistent with helping, but the numbers are far too small to say which helps, whether they help equally, or whether either helps at all: a single plain error in two runs could be chance, and the plain prompt was right once. We cannot say that framing alone fixed the error, and we cannot say that the re-add sentence alone did. This is a pattern in a small set of runs, not proof. The framed prompt does not tell the model how to think; it states the goal, the rules and the output.
Not recorded: a reasoning model against a standard model. We could not switch a model's thinking on and off in a fresh subagent. The slide says so and tells the lecturer how to run it live on the assistant the learner has (switch thinking or "reasoning" mode on and off, same prompt).

## New runs of 11 November 2026: one technique at a time, before and after (T1 to T5)
Purpose: a before and after for each prompt technique taught in Session 8 (role, context, examples or few-shot, output format, structured JSON output). Everyday tasks, so no domain knowledge is needed.
Method: ten Claude fresh general-purpose subagent sessions, 11 November 2026 (not ChatGPT or Gemini), one run per prompt. Each subagent was given only: "Answer the message below as a chat assistant would. Use no tools. Reply with your answer only." followed by the prompt text. No key, no hint of the lesson. Prompts in `s08/prompts/T*.txt`; replies saved verbatim in `s08/runs/T*_run1.*`. Word counts with `wc -w`.

| Technique | Before prompt | After prompt (the one change) | Before reply (run 1) | After reply (run 1) |
|---|---|---|---|---|
| Role | T1_role_before.txt: "Explain what inflation is. Answer in at most 60 words." | T1_role_after.txt: adds "You are a primary school teacher talking to a class of ten-year-olds." | 56 words; "general rise in prices across an economy", "Consumer Price Index", "money supply" | 53 words; a chocolate bar at 1,000 shillings costing 1,200 next year; no technical terms |
| Context | T2_context_before.txt: "Suggest a dinner I can cook tonight. Answer in at most 60 words." | T2_context_after.txt: adds four people, one vegetarian, beans, rice, tomatoes and onions at home, 45 minutes | Lemon-garlic chicken stir-fry with peppers, broccoli, snap peas, soy sauce, honey (none of it known to be at home) | Bean and tomato stew over rice, about 35 minutes; it still added garlic, cumin, paprika and an optional fried egg, which the prompt did not list |
| Examples (few-shot) | T3_fewshot_before.txt: label three SMS, no examples (zero-shot) | T3_fewshot_after.txt: two labelled examples first (IN, OUT) | Its own labels and layout: "Money In (Received)", "Money Out (Bill Payment)", plus totals nobody asked for; 73 words | "1. IN  2. OUT  3. IN": exactly the labels and layout of the examples |
| Output format | T4_format_before.txt: "Compare renting and buying a house." | T4_format_after.txt: a table, two columns, three rows, at most eight words a cell, nothing else | 529 words, seven headings, rules of thumb and advice | A three-row table, as asked |
| Structured output (JSON) | T5_json_before.txt: "Write down this order for the kitchen." | T5_json_after.txt: JSON only, fields table (number), items (dish, quantity), note (text or null) | Free text: "KITCHEN ORDER - TABLE 4 / 2 x Chapati / 1 x Tea (NO SUGAR)" | {"table": 4, "items": [{"dish": "chapati", "quantity": 2}, {"dish": "tea", "quantity": 1}], "note": "no sugar"}; json.load accepts it |

All answers are right in substance; the change is in level, fit, labels, length and shape. One run per prompt: the comparison illustrates what each part of a prompt does and proves nothing about rates. The context "after" run shows a further point used on the slide: the model still added ingredients the prompt did not mention, so a constraint ("use only what we have") would be the next change.

## Run of 11 November 2026 (coherence review): constraints, before and after (T6)
Purpose: a before and after for the fifth part of a prompt, constraints, so that it is taught on its own slide like the other four parts.
Method: one Claude fresh general-purpose subagent session, 11 November 2026 (not ChatGPT or Gemini), same wrapper as T1 to T5: "Answer the message below as a chat assistant would. Use no tools. Reply with your answer only." followed by the prompt text. No key, no hint of the lesson. One run.
Before: the T2 context "after" prompt and its recorded reply (copied as `s08/prompts/T6_constraints_before.txt` and `s08/runs/T6_constraints_before_run1.md`), which added garlic, cumin, paprika and an optional fried egg.
After prompt (`s08/prompts/T6_constraints_after.txt`): the same text plus "Use only the ingredients I listed, plus salt, oil and water. If a good dish needs anything else, say so instead of adding it."
After reply (`s08/runs/T6_constraints_after_run1.md`, verbatim, 63 words by `wc -w`): beans and rice with an onion and tomato sauce, using only oil and salt beyond the list; it named garlic, chili or cumin as improvements "but you didn't list them", and said the 45 minutes holds only if the beans are canned or precooked. One run: it illustrates the effect and proves no rate.

## Check of the bracket token, 11 November 2026
Slide "Your prompt is the start of that text" says the bracket " (" leads after "Please pay the invoice within thirty" because invoices often write the number twice. Checked with `demo_runs/s05/bracket_check.py` (numpy GPT-2 small, same weights as `logits_s05.py`; output `demo_runs/s05/bracket_check_2026-11-11.txt`): after "Please pay the invoice within thirty (" the top next token is "30" at 99.42% (then "31" 0.19%, "35" 0.06%, "60" 0.06%, "29" 0.05%). The model has learned the "thirty (30)" pattern.
