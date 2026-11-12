# Session 2 recorded runs: Learning from examples

Date: 5 November 2026. Tool: Python 3.12.10, scikit-learn 1.9.1, numpy 2.5.4. No internet needed.
Scripts and outputs: `demo_runs/s02/` (`make_expenses.py`, `learn_run.py`, `run_output.txt`, `results_s02.json`, `expenses_fictional.csv`, copies of `customer_messages.csv` and `customer_messages_key.csv`). Re-run live with `python make_expenses.py` then `python learn_run.py` (about 40 seconds).

## Data
- FICTIONAL expense claims: 240 rows made by `make_expenses.py` with numpy seed 2026 (amount lognormal, receipt 72% yes, days to file exponential). Label rule written by the author (no receipt and over UGX 50,000, or over UGX 800,000, or filed over 30 days) with 8% of labels flipped at random. 75 queried, 165 paid. Labelled fictional wherever shown.
- Nile Valley Foods customer messages: the 40 messages in the Practice Files, with the Answer Keys labels: order 11, other 11, payment 9, complaint 9, of which 8 are marked tricky.

## Results (exact, from `run_output.txt`)
- Trees on the claims, cross-validated (5 folds x 20 repeats): depth 1 0.800, depth 2 0.930, depth 3 0.933, depth 4 0.927, unlimited 0.875. The unlimited tree has 33 leaves and 1.0 accuracy on the claims it trained on. The depth-3 tree is drawn on the slide (7 leaves; counts per leaf are in `results_s02.json`).
- Split on receipt: 163 with receipt, 23 queried; 77 without, 52 queried; all 240, 75 queried.
- Nearest neighbours on the 163 claims with a receipt (log10 amount and days, put on one scale): new claim UGX 450,000, 31 days; 5 nearest E040, E178, E010, E071, E012; vote 3 paid, 2 queried.
- Scaling lesson, all three measurements, k = 5: raw numbers 0.690; same scale 0.904. Always saying paid: 0.688.
- 40 messages, 5-fold stratified x 20 repeats (100 tests): always the commonest 0.275; keyword rule (written by the author before seeing results, untuned, no training) 23 of 40 = 0.575; decision tree on word presence 0.536 (worst test 0.00, best 0.88); depth-3 tree 0.579; TF-IDF cosine nearest neighbours k=1 0.578, k=3 0.546, k=5 0.565 (worst 0.12 to 0.25, best 0.88 to 1.00).
- Leave-one-out, 3 neighbours: 0.50 (20 wrong); tree on words 0.55.
- Precedent: M30 (pay in two parts) nearest M14, M08, M34, all payment (similarity 0.35, 0.25, 0.19). M03 (wet sugar) nearest M23 complaint 0.21, M11 order 0.13, M14 payment 0.13.
- Honest limits: 40 messages is far too few for text; single tests vary widely; the claims are made up and the tree recovers the rule written into them. A separate earlier recorded run (Claude, fresh session, 4 November 2026, 12 of these messages, 9 exact) is a different test and is not compared.
