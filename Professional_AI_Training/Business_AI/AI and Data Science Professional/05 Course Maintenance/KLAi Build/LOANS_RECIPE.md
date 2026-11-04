# The loans recipe (Sessions 14 to 17, 20, 23, 24)

Single source of truth: `content/loans_canon.py` (numpy and pandas only; `from loans_canon import prepare, split, facts`). Every number below comes from its numpy replicas. Recompute on real scikit-learn before printing anything on a handout. Checks: `python3 -I ref/verify_loans_canon.py`. The canonical rows are also in `loans_canon_split.csv` (row, loan_id, train or test, position in the test set).

## 1. The code as the learner types it (real scikit-learn)

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix

loans = pd.read_csv("loans.csv")
bad_age = (loans.age < 18) | (loans.age > 100)                        # two impossible ages: 0 and 199
loans.loc[bad_age, "age"] = loans.loc[~bad_age, "age"].median()       # 36; keeps all 8,000 rows
loans["income_missing"] = loans.monthly_income_ugx.isna().astype(int)
loans["monthly_income_ugx"] = loans.monthly_income_ugx.fillna(loans.monthly_income_ugx.median())   # 642,600
# 1.15 = assumed total repayment (loan plus 15 percent interest and fees). It is an ILLUSTRATIVE assumption, not in the data.
loans["instalment_to_income"] = loans.loan_amount_ugx * 1.15 / loans.term_months / loans.monthly_income_ugx

FEATURES = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans",
            "previous_late_payments", "group_loan", "savings_balance_ugx", "has_mobile_money",
            "distance_to_branch_km", "instalment_to_income"]               # 12 numeric; no collection_calls, no district

y = loans.default
X12 = loans[FEATURES]                                                      # Sessions 14, 17 and the tree in 15
X27 = pd.concat([loans[FEATURES], pd.get_dummies(loans[["gender", "occupation", "loan_purpose"]], dtype=int)], axis=1)   # Sessions 15, 16, 20, 23, 24

X_train, X_test, y_train, y_test = train_test_split(X27, y, test_size=0.25, stratify=y, random_state=42)

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))   # C=1.0, L2 penalty: the defaults
model.fit(X_train, y_train)
p_test = model.predict_proba(X_test)[:, 1]
print(roc_auc_score(y_test, p_test))

# choose the decision threshold on the TRAINING loans, then use the test loans once
p_cv = cross_val_predict(model, X_train, y_train, cv=5, method="predict_proba")[:, 1]
# cost = 1,000,000 * missed defaults + 100,000 * false alarms (illustrative); the rule threshold is 100/1100 = 0.0909

# quick check that you got the same rows as this recipe
print(X_test.index[:10].tolist(), sum(X_test.index))     # [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150] 8081998
```

## 2. Rules

1. 8,000 rows everywhere. Nobody deletes rows. The two impossible ages become the median of the valid ages (36).
2. `train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)` everywhere. 6,000 train (753 defaults), 2,000 test (251 defaults), baseline accuracy 0.8745 (1,749 of 2,000). No `np.random.default_rng` split, no unstratified split.
3. 12 numeric columns (X12) or 12 plus 15 indicators (X27). A session says which one it uses. A deliberately small model (S23 app) says "simplified" on the slide.
4. The derived variable is called `instalment_to_income` (in words: instalment-to-income ratio). Never "burden", "repayment burden" or "instalment share". The 1.15 is stated as an illustrative assumption wherever the ratio is defined.
5. The word is "decision threshold". Not cutoff, cut-off, or cut off.
6. Thresholds and hyperparameters are chosen on the training rows by cross-validation (or the rule threshold 0.0909). The test loans are used once, at the end. Never search the threshold on the test loans.
7. Every logistic regression is `make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))`; say that C = 1.0 (L2 penalty) is the default and that it makes the coefficients depend on the scaling.
8. The median income is computed on all 8,000 loans before the split, on purpose (simple; the leak is tiny). Session 20 shows the leak-free Pipeline way.
9. Leakage demonstration: add `collection_calls` to the 12 numeric columns (AUC 0.996).
10. Cross-validation is `cv=5` (StratifiedKFold, no shuffle). On the 6,000 training rows each fold has 1,200 loans (150 or 151 defaults). On all 8,000 loans each fold has 1,600 (200 or 201). Say which.

## 3. Canonical numbers (from a numpy replica; recompute on real scikit-learn before printing anything on a handout)

| Quantity | Value |
|---|---|
| Rows, defaults, default rate | 8,000; 1,004; 12.55 % |
| Impossible ages / median of valid ages | 2 (0 and 199) / 36 |
| Blank income / median income | 379 / UGX 642,600 |
| Train / test | 6,000 / 2,000 |
| Defaults in train / test | 753 / 251 |
| Baseline accuracy (predict nobody defaults) | 0.8745 (1,749 of 2,000); recall 0 |
| Same code, unstratified split (contrast only) | test defaults 220, baseline 0.890 |
| Logistic regression test AUC, 12 numeric / 27 columns | 0.755 / 0.756 |
| Train AUC, 12 / 27 | 0.761 / 0.764 |
| 5-fold CV AUC on training rows, 12 / 27 (mean, sd) | 0.753, 0.011 / 0.748, 0.007 |
| 5-fold CV AUC on all 8,000, 12 / 27 (mean, sd) | 0.756, 0.027 / 0.757, 0.028 |
| Leaky model AUC (12 + collection_calls; 27 + collection_calls) | 0.996; 0.996 |
| Simplified 4-variable model AUC (income, loan, term, late payments) | 0.727 |

Confusion on the 2,000 test loans, 27-column logistic regression (flag when probability is at least the threshold):

| Threshold | Flagged | TP | FP | FN | TN | Precision | Recall | F1 | Accuracy | Cost (UGX M) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 67 | 51 | 16 | 200 | 1,733 | 0.761 | 0.203 | 0.321 | 0.892 | 201.6 |
| 0.3 | 141 | 74 | 67 | 177 | 1,682 | 0.525 | 0.295 | 0.378 | 0.878 | 183.7 |
| 0.2 | 278 | 108 | 170 | 143 | 1,579 | 0.388 | 0.430 | 0.408 | 0.844 | 160.0 |
| 0.15 | 437 | 138 | 299 | 113 | 1,450 | 0.316 | 0.550 | 0.401 | 0.794 | 142.9 |
| 0.1 | 794 | 175 | 619 | 76 | 1,130 | 0.220 | 0.697 | 0.335 | 0.653 | 137.9 |
| 0.0909 (rule) | 897 | 188 | 709 | 63 | 1,040 | 0.210 | 0.749 | 0.328 | 0.614 | 133.9 |

At 0.2 with the 12 numeric columns only: TP 101, FP 161, FN 150, TN 1,588 (AUC 0.755).

Costs (UGX, illustrative: 1,000,000 per missed default, 100,000 per false alarm): flag nobody 251.0 M; flag everybody 174.9 M; cheapest threshold looking at the test loans (do not teach) 0.08 at 133.1 M; threshold chosen by 5-fold CV on the training rows 0.10 (27 columns), test cost 137.9 M; rule 0.0909 test cost 133.9 M.

Depth-3 decision tree, 12 numeric columns, `random_state=42`: accuracy 0.8875, 41 caught, 15 false alarms, 210 missed, 1,734 correct repaid; precision 0.732, recall 0.163; root split instalment_to_income <= 0.75; test AUC 0.722; 8 leaves. Same tree on 27 columns: identical counts. Excel-style rule instalment_to_income > 0.6: 123 caught, 271 false alarms, 128 missed, accuracy 0.8005.

Coefficients, 27-column model, per one standard deviation, sign means direction: instalment_to_income +0.80, previous_late_payments +0.26, savings_balance_ugx -0.18, group_loan -0.16, distance_to_branch_km +0.13, occupation Boda rider +0.13, previous_loans -0.10, has_mobile_money -0.09, monthly_income_ugx -0.09, loan_amount_ugx +0.08, age -0.06, term_months -0.01, income_missing +0.01, gender about 0.00 (the two mirror columns). Intercept -2.23.

Gender audit (2,000 test loans, approve when predicted probability of default is below 0.20): women 1,181 loans, approval 86.5 %, default rate 11.9 %, recall 0.450; men 819 loans, approval 85.6 %, default rate 13.6 %, recall 0.405. Approval ratio 1.01 (disparate impact ratio 0.99, well above 0.8). With the 12 numeric columns (gender not an input): women 86.5 %, men 87.4 %.

## 4. What each session must change

- S14: keep its recipe; rename `burden` to `instalment_to_income`; state 1.15 as illustrative; use the numbers above (tree 41 caught, 15 false alarms, 210 missed, precision 0.73, recall 0.16, accuracy 0.8875); delete "my stand-in program"; promise cross-validation in Session 16 or 17 in place of the validation set; slide 23 says the median is computed before the split on purpose; rule threshold 0.0909 explained.
- S15: slides 4, 5, 9 to 25, 27, 30, 32 and notebook Steps 1 to 5 use the canonical recipe (8,000 rows, flag, stratified 6,000 / 2,000, 251 defaults, X27). Recompute the default-rate quintile figures, coefficient table, a new example loan from the new test set (N07896 may not be in it), tree figures, threshold table and cost table. Threshold chosen by cross-validation on the training rows or the rule 0.0909, not on the test loans. Add the regularisation sentence (C = 1.0).
- S16: same recipe; slide 7 "87.45 percent, 1,749 of 2,000, 251 defaults"; recompute slides 4 to 5, 8 to 17, 20 to 23, 25 to 29, 34; CV folds 1,600 loans (all 8,000) with 200 or 201 defaults, or 1,200 with 150 or 151 (training rows); add a "tune before you test" slide; leaky model 0.996; ROC axes in words; "decision threshold" everywhere.
- S17: remove "ages 18 to 80 ... drop"; use the canonical preparation and `stratify=y` (it becomes the default, drop the CHANGE that adds it); the 12 numeric columns stay and the text says test AUC (0.755) differs from Session 15 (0.756, 27 columns) only by those 15 columns; keep the median-before-split note; fix "our NumPy code" on the bagging slide; rename burden.
- S20: replace `train_test_split(test_size=0.25, random_state=42)` by the stratified canonical split on the canonical preparation; recompute the numpy references with `RandomState(42)` rather than `default_rng`; AUC differences from the slides of up to about 0.03 are expected (random weights); more than 0.05 means a different split or variable list.
- S23: fit on the 6,000 training rows only; compute and print the held-out AUC in the notebook so the model card is reproducible; audit by gender on the 2,000 test loans (numbers above, or recompute for the four-variable model); rule A uses `instalment_to_income` (with 1.15) or is renamed and says "without charges"; keep the four-variable model only with the word "simplified" on the slide (test AUC 0.727); "instalment share" becomes instalment_to_income.
- S24: recompute the evidence slide from the canonical split and one stated model and decision threshold; replace "Session 19 numbers" by "Sessions 15 and 16 numbers"; remove the `default_rng` split; footnote: "Same loans as Sessions 14 to 17. Your own numbers from Sessions 15 and 16 will differ a little because the model and the decision threshold differ."
- Data dictionary: replace "grain" by "each record is one loan (granularity: one row per loan)".

## 5. Known limits of the replicas

No scikit-learn exists in the build sandbox. The stratified split is a copy of the library algorithm run on numpy's own random generator and agrees with an independent replica made earlier, but has not been compared with a real library run. Real lbfgs stops at a looser tolerance than the exact optimum used here: a test with a numpy L-BFGS at scikit-learn's tolerance moved the AUC by 5e-6 and no confusion count. The tree is a port of the earlier line-by-line CART replica. Step 1 of any recompute: run the index check at the end of section 1. If it prints different rows, recompute every number.
