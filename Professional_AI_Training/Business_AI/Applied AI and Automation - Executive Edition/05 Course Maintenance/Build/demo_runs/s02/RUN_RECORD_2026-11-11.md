# Session 2 re-run, 11 November 2026: five fold scores of one 5-fold split

What was run: `python learn_run.py` in this folder, after adding section C (five fold scores of ONE complete 5-fold split, which is repeat 1 of the
`RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0)` already used; nothing else changed).
Tools: Python 3.12.14, scikit-learn 1.9.1, numpy 2.2.6 (the 5 November record says numpy 2.5.4; every earlier line of output is identical apart from that version line).
Date: 11 November 2026, one run. Output: `run_output.txt` (new) and `results_s02.json` (new keys `claims_one_split`, `messages_one_split`).
Old records kept unchanged: `run_output_2026-11-05.txt`, `results_s02_2026-11-05.json`.

Result (240 fictional claims, folds of 48 claims; train on 192):
- Depth-3 tree, test folds: 44, 44, 45, 45, 45 right of 48 = 0.9167, 0.9167, 0.9375, 0.9375, 0.9375; mean 0.9292; worst 0.9167; best 0.9375. Training: 184 or 185 of 192 (0.958 to 0.964).
- Unlimited tree, test folds: 42, 42, 43, 44, 41 of 48 = 0.8750, 0.8750, 0.8958, 0.9167, 0.8542; mean 0.8833. Training: 192 of 192 (1.000) in every fold.
- 40 messages, depth-3 tree on words: 2, 3, 5, 6, 7 of 8 = 0.250, 0.375, 0.625, 0.750, 0.875; mean 0.575.
Checked: these equal the first five of the 100 cross-validation scores (cross_val_score) for the same models.

Also added in the same run (section C, end): k-nearest neighbours, k = 5, on all three claim features with MIN-MAX scaling first (the method taught by hand):
0.889 cross-validated (5 folds x 20 repeats). For comparison, recorded 5 November and unchanged: raw 0.690, standard scaling 0.904.
Feature ranges in the 240 claims: amount UGX 5,000 to 1,567,000 (5 to 1,567 in thousands); days to file 0 to 66.
(The 5 November slide said "amount runs to 2,500, days to 90"; that was wrong and is corrected on the slides.)
