# Demo re-run table (verified 6 November 2026)

Setup for every row: `. env.sh; cd "$B"` (the Build folder, shared venv). Re-run on this machine (Apple laptop, MPS) and compared with the saved record. "Internet" means needed only on the very first run, to download a model once; after that everything runs offline. Seeds are fixed, so output repeats exactly unless noted.

| Session | Script | Command (from Build/) | Runtime | Internet | What to look for |
|---|---|---|---|---|---|
| 1 | digits_run.py | `cd demo_runs/s01; python digits_run.py` | 3 s | no | Test accuracy 0.9689 (436 right, 14 wrong), 1,210 parameters, shifted images 0.9689 / 0.4578 / 0.1422, five starts 0.962 to 0.969 |
| 1 | rgb_image.py | `cd demo_runs/s01; python rgb_image.py` | under 1 s | no | Sunrise as RGB triples, count 192 |
| 2 | make_expenses.py | `cd demo_runs/s02; python make_expenses.py` | under 1 s | no | Rewrites expenses_fictional.csv (240 rows, 75 queried), identical each time |
| 2 | learn_run.py | `cd demo_runs/s02; python learn_run.py` | 4 s | no | Depth-3 tree 0.933 best; unlimited tree 100% on own claims, 33 leaves; scaling 0.690 vs 0.904; messages: keyword rule 23 of 40, learned models 0.54 to 0.58 |
| 3 | s03_threshold.py | `python demo_runs/s03/s03_threshold.py 0.50 0.30 0.20 0.15 0.10 0.05` (add `--miss 100000` or `--miss 600000`) | 1 s | no | 900 invoices, 83 late, lazy score 90.8%; cheapest row is 0.05 at UGX 12,020,000 (default); with --miss 100000 it is 0.20 (6,840,000); with 600000 it is 0.05 (13,520,000) |
| 3 | s03_measure.py | `python demo_runs/s03/s03_measure.py` | 1 s | no | Prints about 800 lines; scroll to always_no (0.908, recall 0), rule, deep_tree (train 1.0, test 0.852), small_tree |
| 4 | s04_search.py | `python demo_runs/s04/s04_search.py contracts "What happens if heavy rain floods the road and the delivery cannot get through?"` | 6 to 10 s | first run only (all-MiniLM-L6-v2) | Force majeure first, cosine 0.361; word search shares no word |
| 4 | s04_search.py | `... finance "Make sure our books match what the bank says."` (add `--raw` for step 4) | 6 to 10 s | no | Bad debt write-off 0.514, Bank reconciliation 0.461 (a miss); with --raw straight line and city blocks name Bank reconciliation |
| 4 | s04_search.py | `... hr "I saw a colleague stealing stock and I am afraid to say so."` | 6 to 10 s | no | Whistleblowing first, 0.402 |
| 4 | s04_run.py | `python demo_runs/s04/s04_run.py` (not live; rebuilds results.json) | 9 s | no | Output identical to output_s04_run.txt |
| 5 | live_s05.py | `cd demo_runs/s05; python live_s05.py "Nile Valley Foods delivers maize flour to Mbale."` | 6 to 8 s | first run only (gpt2) | 8 words, 11 tokens |
| 5 | live_s05.py | `python live_s05.py "Please pay the invoice within thirty"` | 6 s | no | "(" 69.3%, days 17.8%, "-" 10.2% |
| 5 | live_s05.py | `python live_s05.py "The customer was angry because the delivery was" 0.2 1.0 1.8` | 10 s | no | Calm at 0.2, odd at 1.0, nonsense at 1.8. Seeds 0 to 3, so differs from slide samples (seeds 100 to 105) |
| 5 | run_s05.py | `cd demo_runs/s05; python run_s05.py` (not live) | 12 s | first run only | Rebuilds results.json (attention map, 144 heads); identical |
| 6 | run_s06.py | `cd demo_runs/s06; python run_s06.py` (optional) | about 55 s | first run only (Qwen2.5-1.5B, about 3 GB) | Greedy reply repeats the record. Sampled replies also matched here; on another machine they may differ. PRE-RUN before class |
| 7 | measure_sizes.py | `cd demo_runs/s07; python measure_sizes.py` | 14 s | first run only (about 270 MB) | fp32 538.1, fp16 269.1, int8 135.0, int4 75.8 MB; int4 next word shifts to " the" 0.56. Writes about 1 GB into demo_runs/s07/work |
| 8 | (no script) | JSON check: `python -c "import json; d=json.load(open('demo_runs/s08/runs/R1_structured_run1.json')); print(len(d), [x['type'] for x in d])"` | 1 s | no | 4 records: order, payment, complaint, question |
| 9 | retrieve.py | `cd demo_runs/s09; python retrieve.py .` | 7 s | first run only | Q03 clause 3.2 at 0.73, Q08 0.40, Q09 wrongly 2.1 at 0.70 |
| 9 | chunking.py | `python chunking.py .` | 7 s | no | Clause chunks 8 of 8, 150 characters 5 of 8, 300 characters 8 of 8 |
| 9 | lora_style.py | `python lora_style.py .` | 25 s here (record says 42 s training) | first run only (gpt2) | Sign-off present before 0 of 6, after 6 of 6; invented facts in AFTER text. PRE-RUN once |
| 9 | make_prompts.py | `python make_prompts.py` (preparation only) | 1 s | no | Rebuilds the retrieved-passage prompts |
| 12 | business_case_check.py | `python demo_runs/s12/business_case_check.py` | 1 s | no | Hours saved 5.33; payback 3.02 months; 12-month net 1,428,000; after 30% haircut 333,600; break-even haircut 0.391 |
| 14 | nvf_file_check.py | `python demo_runs/s14/nvf_file_check.py "../../03 Learner Materials/Practice Files/01 Case Company"` | 1 s | no | 60 invoice rows, 8 faults (4 wrong totals, 2 missing PO, 1 zero VAT, 1 duplicate); 32 of 40 sender names with phone numbers |

Sessions 6, 8, 10, 11, 12 and 13 otherwise use recorded assistant runs (files named in the facilitator steps); nothing to execute. Only Sessions 6, 7 and 9 take more than 30 seconds or download models: run them once the day before.
