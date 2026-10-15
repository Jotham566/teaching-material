# CML3112 A8 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate building cooling load; target unit: **kW**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `classification_metrics(actual, predicted)` — 9 marks

- For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.
- Return a dictionary with tp, tn, fp, fn, precision, recall and cost. 1 means warning and 0 means no warning; actual is the true label and predicted is the model label.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

**Supplied scenario (use for the written questions):**

There are 100 validation observations: 10 actual warnings and 90 non-warnings. Model A has TP=9, FN=1, FP=3, TN=87; B has TP=10, FN=0, FP=6, TN=84. A missed warning costs 5 teaching cost units and a false alarm costs 1. Choose A or B and justify the trade-off. These are assumed costs, not approved operating limits.

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **3 marks:** Calculate the total assumed cost for A and for B using 5 × FN + FP.

2. **2 marks:** Compare missed warnings and false alarms. Explain why accuracy alone may be misleading.

3. **2 marks:** Choose a model using the assumed total cost and justify your choice.

4. **2 marks:** What costs or real warning data need checking before deployment?

5. **2 marks:** Which labels and calculation rules must be saved so someone can reproduce your result?


## Submit

ONE completed assignment notebook (.ipynb).
