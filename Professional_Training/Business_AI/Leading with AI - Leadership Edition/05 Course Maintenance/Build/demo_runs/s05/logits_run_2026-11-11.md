# Session 5 recorded run, 11 November 2026: raw logits, a chain of probabilities, one embedding row

What: GPT-2 small (124M), the same Hugging Face `gpt2` weights as the 6 November run (`run_s05.py`, `results.json`), run again to record numbers the 6 November run did not keep: the raw scores (logits) before softmax, the probability chain of a short sentence, the first numbers of one embedding row and one position row, and the parameter count of one block.

How: `python logits_s05.py` in this folder (output `logits_run_2026-11-11.json`). The course venv on 11 November 2026 had numpy 2.2.6 and Python 3.12.14 but no torch, so the script runs the GPT-2 forward pass with numpy, reading `model.safetensors`, `vocab.json` and `merges.txt` from the downloaded model. One deterministic pass (no sampling). Laptop CPU, about 1 second.

Check against the 6 November record (printed by the script): the token ids of all five recorded sentences match; for "Please pay the invoice within thirty" and "The customer was angry because the delivery was" the top 10 next tokens are the same and every probability agrees within 0.00003.

## Raw logits (scores) for "Please pay the invoice within thirty"
| Next token | Logit | Probability after softmax |
|---|---|---|
| " (" | -20.702 | 69.33% |
| " days" | -22.061 | 17.81% |
| "-" | -22.620 | 10.18% |
| " minutes" | -25.791 | 0.43% |
| " business" | -25.908 | 0.38% |
Lowest of all 50,257 logits: -55.93. Highest: -20.70. Gaps from the top score: days 1.36 lower, "-" 1.92 lower.
Also recorded: "Thank you for your" (support -106.108, 30.35%) and "The customer was angry because the delivery was" (delayed -129.615, 11.43%); see the json.

## Chain of probabilities, "Thank you for your support" (first token "Thank" given)
P(" you" | "Thank") = 0.0221, loss 3.810; P(" for" | "Thank you") = 0.4271, loss 0.851; P(" your" | "Thank you for") = 0.2733, loss 1.297; P(" support" | "Thank you for your") = 0.3035, loss 1.192. Product 0.000785. Average loss 1.788.
(A second chain, "Please pay the invoice within thirty days", is in the json; it ends with P(" days" | ...) = 0.1781, loss 1.726.)

## Embedding row plus position row: " invoice" (id 45,458), 4th token of "Please pay the invoice"
First 4 of 768 numbers. Token row E: 0.0688, -0.3022, 0.1568, -0.2135. Position row P (4th position): -0.0003, -0.0738, 0.1055, 0.0007. Sum: 0.0685, -0.3760, 0.2623, -0.2129. Token table 50,257 rows; position table 1,024 rows.

## One transformer block (block 1)
7,087,872 parameters: self-attention 2,362,368; feed-forward network 4,722,432 (768 inputs, a hidden layer of 3,072 neurons, back to 768); layer normalisation 3,072.
