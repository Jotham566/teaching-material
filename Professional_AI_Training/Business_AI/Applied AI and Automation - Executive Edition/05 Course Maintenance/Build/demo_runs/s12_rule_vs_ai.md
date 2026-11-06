# Session 12: the two recorded automations side by side (reused, not rerun)

Assembled 6 November 2026 from existing records. Nothing was rerun.

Sources
- AI sort: `04 Facilitator Materials/Twelve-Message AI Demonstration Results (4 Nov 2026).md`. Claude, three fresh sessions given only the prompt, 4 November 2026, answer key hidden; not ChatGPT or Gemini. All three runs gave the same category for every message.
- Rule router: computed in the v2 Session 6 (`Archive/v2_before_technical_2026-11-05/content/s06.py`): a payment rule (paid, payment, MoMo: Finance) placed before the complaint rule (late, delay: Customer Service), otherwise Sales desk. The words were chosen after reading the twelve messages, so 7 of 12 flatters the rule.
- Key: `04 Facilitator Materials/Answer Keys/customer_messages_key.csv`.

| Id | Rule (right queue?) | AI (all 3 runs) |
|---|---|---|
| M01 | right | exact |
| M02 | right | exact |
| M03 | wrong | exact |
| M07 | wrong (late in an order) | exact |
| M10 | wrong (polite complaint) | exact |
| M14 | right (Finance) | wrong: said Complaint, key says Payment first |
| M15 | right | exact |
| M21 | right | exact |
| M26 | right (Sales desk) | UNSURE, spotted both topics: acceptable |
| M28 | right (Sales desk) | UNSURE, agrees with the key's advice: acceptable |
| M32 | wrong (sarcastic thanks) | exact |
| M38 | wrong (4pm is a delivery time) | exact |

Counts: rule 7 of 12 in the right queue. AI 9 of 12 exact, 11 of 12 acceptable, 1 wrong with confidence (M14).
The two counts use different measures (a queue for the rule, a category for the AI), so read them side by side and do not subtract them.
Not measured: the time a person takes to check the AI, and the person alone on the same twelve (the class result from the Session 12 demonstration, if recorded in the Rehearsal Record).

Business case example: `demo_runs/s12/business_case_check.py` recomputes the grey NVF example in `Templates/Business Case Workbook.xlsx` with the workbook's own formulas (output in `business_case_output.txt`): 5.33 hours saved a month, benefit UGX 304,000, monthly cost UGX 145,000, net UGX 159,000, one-off UGX 480,000, payback 3.0 months, 12-month net UGX 1,428,000, UGX 333,600 after a 30% haircut, break-even haircut about 39%. These are PLAN figures with invented NVF inputs. Note: the Stop rules sheet of the template still says "Base 12-month net UGX 1,548,000; UGX 417,600 after a 30% haircut", which does not match its own Inputs (stale text; template owner to fix).
