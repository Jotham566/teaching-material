# Session 3 demonstration runs: measuring a model (recorded 6 November 2026)

**What was run.** `demo_runs/s03/s03_measure.py` and `demo_runs/s03/s03_threshold.py` (both kept in `demo_runs/s03/`, re-run them live). Tool: Python 3.12.10, scikit-learn 1.9.1, numpy 2.5.4. Run date: 6 November 2026. Number of runs: 3 trial runs of `s03_measure.py` while the generator constant (the base late rate) was tuned, because the first gave only 2.4 percent late invoices and the second 10.4 percent, and about 9 percent was wanted; the reported run is the third and last, plus the threshold script run 4 times. All seeds are fixed (dataset seed 2026, split seed 42, tree seed 0), so every re-run prints the same numbers.

**The data are invented.** Nile Valley Foods Ltd is fictional. `s03_measure.py` generates 3,000 fictional invoices (columns: invoice_ugx, years_as_customer, late_last_12m, days_since_last_order, pays_by_momo, credit_used, paid_late) and writes them to `demo_runs/s03/invoices.csv`. The late-payment rule in the generator is invented; the model learns it back, so the result shows how to read a result table and says nothing about real Ugandan shops.

**Split.** 2100 training invoices and 900 test invoices (stratified). In the test set 83 were paid late and 817 on time (late rate 9.2% overall).

## 1. Baselines (test set)

- Always say "on time": accuracy 90.8%, recall 0%, no flags.
- Rule "flag if paid late at least once in the last 12 months": flagged 445, caught 65, false alarms 380, missed 18; accuracy 55.8%, precision 14.6%, recall 78.3%.
- Logistic regression (scaled inputs), AUC on the test set 0.798; accuracy at a 0.50 threshold 91.1% on test and 90.9% on training data.

## 2. The same model at six thresholds (exact output of `s03_threshold.py 0.50 0.30 0.20 0.15 0.10 0.05`)

```
900 test invoices, 83 really late.  Always saying "on time" scores 90.8% accuracy.
threshold flagged caught false_alarms missed precision recall   F1  accuracy  cost_UGX
     0.50       9      6            3     77       67%     7%   13%     91.1%   23,280,000
     0.30      43     15           28     68       35%    18%   24%     89.3%   21,260,000
     0.20     102     35           67     48       34%    42%   38%     87.2%   16,440,000
     0.15     152     43          109     40       28%    52%   37%     83.4%   15,040,000
     0.10     254     54          200     29       21%    65%   32%     74.6%   13,780,000
     0.05     526     78          448      5       15%    94%   26%     49.7%   12,020,000
```

Costs are ASSUMED for the lesson: UGX 20,000 to chase a flagged invoice and UGX 300,000 for a missed late invoice. Never flagging costs UGX 24,900,000 (83 x 300,000). With `--miss 100000` the cheapest of 0.50, 0.20, 0.05 is 0.20 (UGX 6,840,000); with `--miss 600000` it is 0.05 (UGX 13,520,000).

## 3. A model that memorises (decision trees, same split)

- Unlimited depth: depth 21, 229 leaves, accuracy on training data 100.0%, on test data 85.2% (recall 26.5%, precision 23.4%).
- Depth 3: 8 leaves, training 91.1%, test 90.1% (recall 10.8%, precision 37.5%).

| Depth | Training accuracy | Test accuracy |
|---|---|---|
| 1 | 90.8% | 90.8% |
| 2 | 90.8% | 90.8% |
| 3 | 91.1% | 90.1% |
| 4 | 91.4% | 90.6% |
| 6 | 92.5% | 89.6% |
| 8 | 95.0% | 88.7% |
| 12 | 97.6% | 84.6% |
| 21 | 100.0% | 85.2% |

The unlimited tree scores below the always-on-time baseline on test data.

## 4. The twenty cases for the hands-on exercise

Drawn from the test set with seed 7: 6 really late and 14 on time. The draw seed is the first seed from 7 upward that gives the 2 x 2 table below at threshold 0.20 (chosen so that every box is used and precision differs from recall); the scores and outcomes are the model's real ones.

| Case | Invoice | Amount UGX | Score | Really late |
|---|---|---|---|---|
| 1 | INV0318 | 470,000 | 0.33 | on time |
| 2 | INV0168 | 744,000 | 0.47 | late |
| 3 | INV1940 | 822,000 | 0.10 | on time |
| 4 | INV1486 | 427,000 | 0.01 | on time |
| 5 | INV0216 | 463,000 | 0.07 | on time |
| 6 | INV1334 | 195,000 | 0.13 | on time |
| 7 | INV2427 | 774,000 | 0.17 | late |
| 8 | INV1848 | 824,000 | 0.06 | on time |
| 9 | INV1345 | 218,000 | 0.02 | on time |
| 10 | INV0761 | 216,000 | 0.08 | late |
| 11 | INV0002 | 524,000 | 0.08 | on time |
| 12 | INV2938 | 285,000 | 0.03 | on time |
| 13 | INV2286 | 464,000 | 0.11 | on time |
| 14 | INV1810 | 309,000 | 0.13 | on time |
| 15 | INV2788 | 889,000 | 0.09 | late |
| 16 | INV0512 | 4,262,000 | 0.73 | late |
| 17 | INV1030 | 224,000 | 0.03 | on time |
| 18 | INV1920 | 268,000 | 0.12 | on time |
| 19 | INV0655 | 697,000 | 0.53 | late |
| 20 | INV1629 | 391,000 | 0.32 | on time |

**Answer key (facilitator).** Flag at 0.20 or more: caught 3 (cases 2, 16, 19), false alarms 2 (cases 1, 20), missed 3 (cases 7, 10, 15), rightly cleared 12. Precision 3 / 5 = 60%, recall 3 / 6 = 50%.
At 0.50: flagged 2 (cases 16, 19), both late: precision 2 / 2 = 100%, recall 2 / 6 = 33%.
At 0.15: flagged 6 (cases 1, 2, 7, 16, 19, 20), caught 4 (2, 7, 16, 19), false alarms 2 (1, 20): precision 4 / 6 = 67%, recall 4 / 6 = 67%.

## Files
- `demo_runs/s03/s03_measure.py` (everything), `s03_threshold.py` (live threshold), `results.json` (all numbers the slides use), `invoices.csv` (the data), `output_s03_measure.txt`, `output_s03_threshold.txt`, `output_s03_threshold_miss100k.txt`, `output_s03_threshold_miss600k.txt` (exact printed output).
- Slides label these as "recorded run, 6 November 2026".
