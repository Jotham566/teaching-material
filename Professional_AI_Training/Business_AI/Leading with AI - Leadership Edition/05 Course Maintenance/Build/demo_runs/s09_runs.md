# Session 9 recorded runs (6 November 2026)

All code and data are in `Build/demo_runs/s09/`. Python 3.12.10 in the shared venv. Re-run any script from that folder.

## 1. Retrieval step (retrieve.py), run once, live on a laptop
- Tool: sentence-transformers 6.2.0, model `sentence-transformers/all-MiniLM-L6-v2`, cosine similarity on normalised vectors.
- Input: `staff_handbook_excerpt.txt` (copy of the Practice Files file), cut into 30 chunks, one per numbered clause; the ten questions in `handbook_questions_key.csv`.
- Output (exact, saved in `retrieval_output.txt` and `retrieval_results.json`, which also holds the top five): Q01 2.1 (0.88); Q02 2.2 (0.90); Q03 3.2 (0.73), then 3.1 (0.47), 3.5 (0.46); Q04 3.1 (0.80); Q05 1.3 (0.76); Q06 4.4 (0.75); Q07 5.3 (0.71); Q08 3.3 (0.40); Q09 (no answer in the handbook) 2.1 (0.70); Q10 (no answer) 4.3 (0.32).
- Runs: 1 (deterministic).

## 2. Chunking comparison (chunking.py), run once
- Same model and questions (the eight answerable ones). A question counts as answered when the top chunk contains every answer fragment listed in the script (a text check).
- Result (`chunking_output.txt`): one chunk per clause 8 of 8 (30 chunks); every 150 characters 5 of 8 (30 chunks; Q03, Q05, Q06 failed, for Q03 the answer sits in the chunk after the top hit); every 300 characters 8 of 8 (15 chunks).

## 3. Token counts (tokens_output.txt)
- tiktoken 0.14.0, cl100k_base: handbook excerpt 829 words, 1,074 tokens; supplier agreement 576 words, 747 tokens; meeting notes 753 words, 1,176 tokens; vendor proposal 606 words, 791 tokens. Other tokenisers differ.

## 4. Tiny LoRA (lora_style.py), run once
- Tool: transformers 5.22.1, torch 2.15.0, peft 0.21.2; base model GPT-2 (124,439,808 parameters); LoRA rank 8, alpha 16, target c_attn; 294,912 trainable parameters (0.24 percent). 48 invented NVF customer messages with replies in one house style (generated from templates in the script), 4 epochs, batch 8, learning rate 2e-3, about 42 seconds on a laptop CPU. Greedy decoding on 6 new customer messages.
- Result (`lora_output.txt`, `lora_results.json`): reply ends with the house sign-off before 0 of 6, after 6 of 6. The replies contain invented facts (for example "We will arrive on Monday"). A tiny model and invented data: the run shows the idea, not what a product would do.

## 5. Assistant runs with and without the document
Claude, fresh general-purpose subagent session for each run, given only the prompt file, 6 November 2026. Not ChatGPT or Gemini. Replies saved verbatim in `s09/runs/`. Prompts in `s09/prompts/` (A and B built by make_prompts.py).
- A_no_document_run1.md and run2.md: the ten questions, no handbook. Both answered "not stated" to all ten, saying no handbook text was provided. Against the key: 2 right (Q09, Q10), 8 missed, 0 invented.
- C_plain_question_run1.md: the same ten questions asked plainly, with no instruction to answer only from the handbook and no handbook. It declined to answer any of them and listed where to look. It is kept as a record and NOT scored or shown on the slides.
- B_retrieved_passages_run1.md and run2.md: the top three clauses per question from run 1 above. Both 10 of 10 against the key.
- Whole handbook: `Case Runs/runs/F2b_handbook_questions_run1.md` and `run2.md` (4 November 2026), both 10 of 10 against the key.

## 6. Added 11 November 2026 (explain-before-use rework)
- `s09/token_budget.py` (output `token_budget_output.txt`), tiktoken 0.14.0, cl100k_base, run once on 11 November 2026: instructions plus the Q03 question exactly as in the retrieved-passages prompt = 94 tokens; the three retrieved clauses for Q03 with their [clause] labels (3.2, 3.1, 3.5) = 104 tokens; whole handbook = 1,074 tokens; answer allowance 300 tokens (a chosen setting). Totals 498 and 1,468. This records where the 94 and 104 on the context-window slide come from (they were on the slide before but not in a run file).
- `s09/check_numbers.py` (output `check_numbers_output.txt`): plain arithmetic for the slides: cosine of (4, 3) and (3, 4) = 24 ÷ (5 × 5) = 0.96, about 16 degrees; cosine 0.6 is about 53 degrees, 0.73 about 43, 0.47 about 62, 0 is 90; the 4 × 4 LoRA picture (W, B = (1, 0, 2, 0) as a column, A = (1, 0, 0, 1) as a row, B A and W′ = W + B A); 4 × 4 = 16 numbers against 1 × (4 + 4) = 8 at rank 1; GPT-2: W 768 × 2,304 = 1,769,472; B 768 × 8 = 6,144; A 8 × 2,304 = 18,432; B + A = 24,576 = 8 × (768 + 2,304); × 12 blocks = 294,912; 294,912 ÷ 124,439,808 = 0.00237, about 0.24 percent (matches lora_output.txt: trainable 294,912).
