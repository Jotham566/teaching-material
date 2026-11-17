# Terminology rule for every slide, note, notebook, sheet task and document

**Use the real industry term as the name. Explain it in simple words next to it. Never replace it with a friendlier invented name.**

Reason (lecturer, 4 Nov 2026): learners will meet these words in documentation, job interviews, Kaggle, textbooks and later courses. Session 2 slide 3 said "grain" for the meaning of one row. A learner who later hears "record", "observation", "instance" or "unit of observation" is lost, and one who is told "grain" by a data-warehouse colleague has no anchor. The slide therefore names the real words and then explains them.

Pattern on a slide: **Term (alias, alias): plain-words explanation, then an example from the Lakeside data.** Define the term where it first appears in the deck. After that use the term itself, not a paraphrase. Where the course anchors on Excel, the Excel word comes first and the industry term right after it on the same slide ("a row, called a record or an observation in data science").

Also see `TERMS_base.md` (machine learning terms already agreed for the IUEA second half). Those apply here unchanged. The table below adds the data science course vocabulary. Left column: what must disappear as a NAME. It may stay in a plain-words explanation.

## Data, tables and statistics (Sessions 1 to 4, 7 to 12)

| Do not use as a name | Use this term | Plain-words explanation to give once |
|---|---|---|
| grain (as the main word) | **record (also called an observation, an instance or a row)** and **granularity** (data warehouse people say "grain") | A record is one row: one thing the table describes, such as one till order. Granularity is the level of detail of the table: one row per order, per order line or per branch per week. Write it as one sentence: "Each record is one till order." |
| the meaning of one row | **unit of observation** (what one record stands for) | |
| variable type | **data type** (how the value is stored: integer, float, string, datetime) and **variable type** (how it is measured: numeric, categorical, ordinal, datetime, text) | Numeric can be discrete (counts) or continuous (money, weight). Categorical can be nominal (no order) or ordinal (ordered). |
| number, category, date or text (as the only names) | numeric, categorical, datetime, text (string) | |
| column (when you mean a measured thing) | **variable** (also feature or field; an attribute of each record) | In a spreadsheet it is a column. In statistics it is a variable. In machine learning it is a feature (input) or the target. |
| key that never repeats | **primary key**; **composite key** when two columns together are unique | |
| a column pointing to another table | **foreign key** | |
| how the tabs link | **relational model**; **one-to-many**, **many-to-one** and **many-to-many relationship** (cardinality) | |
| how the tabs link (drawing) | **entity relationship diagram (ERD)** | |
| blank, empty cell | **missing value** (NaN in pandas, NULL in SQL) | Say whether it means "unknown", "not applicable" or "a walk-in customer". |
| a blank that means something | **informative missingness** (add a missing-indicator flag) | |
| filling the blanks | **imputation** (mean, median or constant imputation) | |
| average | **mean** (arithmetic mean). Say **median** and **mode** each time. | |
| spread | **standard deviation** (sample standard deviation, ddof=1 in pandas), **variance**, **interquartile range (IQR)** | |
| the middle half | **interquartile range (IQR)**: Q3 minus Q1 | |
| odd value | **outlier** (the IQR rule or z-score rule) | |
| lopsided | **skewness** (right-skewed, long right tail) | |
| a few rows from the whole file | **sample**, drawn from a **population** | |
| the gap between a sample and the whole | **sampling error**; the spread of sample means is the **sampling distribution** and its standard deviation is the **standard error** | |
| the wobble | **sampling variability** and **standard error** | |
| a pile of random draws on a computer | **Monte Carlo simulation** (random sampling) | |
| a random draw | **random sample**; **sampling with replacement** or **without replacement** | |
| hidden third factor | **confounder** (confounding variable) | |
| two columns move together | **correlation** (Pearson correlation coefficient r); correlation is not **causation** | |
| rows chosen by something other than chance | **selection bias**; **survivorship bias** | |
| a test run on two groups | **A/B test** (controlled experiment: **treatment** group and **control** group) | |
| the lift | **lift** (treatment mean minus control mean), **uplift** | |
| range that catches the true value | **confidence interval (CI)**; "95 percent" is the **confidence level** | |
| redrawing your own data | **bootstrap** (resampling with replacement) | |
| nothing is going on | **null hypothesis (H0)** and **alternative hypothesis (H1)** | |
| the p-value chance | **p-value**; **significance level (alpha)**; **statistical significance** | |
| big enough to matter | **effect size** and **practical significance** | |
| fake alarms | **false positive (Type I error)** and **false negative (Type II error)**; many tests raise the **multiple comparisons problem** | |
| peeking and stopping early | **optional stopping** (a form of **p-hacking**) | |
| pivot table | **pivot table** (keep); in SQL and pandas it is **GROUP BY** / **groupby** with **aggregation** | |
| a total per group | **aggregation** (aggregate function: SUM, COUNT, AVG, MIN, MAX) | |
| lines on an order | **line items** (the order lines table) | |
| join that multiplies rows | **fan-out** (row multiplication from a one-to-many join) | |
| lookup that keeps one row per key | **many-to-one merge** (pandas `validate='m:1'`) | |
| merge types | **inner join, left join, right join, full outer join** | |
| the cleaning table | **data cleaning log** (an audit trail of each change with row counts) | |
| the gap in the cleaning check | **reconciliation difference** (never call it a residual: residual is a model word) | |
| a looking-over routine | **exploratory data analysis (EDA)** | |
| the rate | **rate** (events per 100 items) versus **count**; **ratio**; **percentage** | |
| repeating yearly pattern | **seasonality**; with **trend** and **noise** (the **decomposition** of a time series) | |

## Machine learning workflow, models and evaluation (Sessions 13 to 20)

| Do not use as a name | Use this term | Plain-words explanation to give once |
|---|---|---|
| predictor, outcome | **independent variable (predictor, feature)** and **dependent variable (response, target)** | Statistics says dependent and independent; machine learning says feature and target. Show both once, then pick the course word for the session and say so. |
| the line through the cloud | **linear regression model**; the **fitted line**; **scatter plot** for the cloud | |
| the misses | **residuals** (actual minus predicted); the **error** of a prediction | |
| smallest misses | **ordinary least squares (OLS)**: minimise the sum of squared residuals | |
| share explained | **R squared** (coefficient of determination); **adjusted R squared** | |
| slope | **coefficient** (slope for a numeric predictor) and **intercept** | |
| 0 and 1 column for a category | **indicator variable (dummy variable)**; **one-hot encoding** (drop one level to avoid the **dummy variable trap**, perfect multicollinearity) | |
| the cloud is even | **homoscedasticity**; **residual plot** | |
| a set of settings found | **parameters** (learned) and **hyperparameters** (chosen) | |
| rows to learn from; hidden rows | **training set**; **test set**; **validation set** (hold-out) | |
| score of a learner that learns nothing | **baseline model** (majority-class baseline, DummyClassifier) | |
| one answer much more common | **class imbalance** (the **accuracy paradox**) | |
| yes or no question | **binary classification** with a **positive class** and a **negative class** | |
| cut-off, line | **decision threshold** (classification threshold) | |
| catches and false alarms | **true positive, false positive, true negative, false negative**; the **confusion matrix** | |
| of those flagged, how many right | **precision**; **recall (sensitivity, true positive rate)**; **F1 score**; **accuracy** | |
| trade-off curve | **ROC curve** and **AUC**; **precision-recall curve** | |
| the S curve | **sigmoid (logistic) function**; **log-odds** | |
| model that peeks | **data leakage** (target leakage, train-test contamination) | |
| rule from questions | **decision tree** (**root node, internal node, leaf node, split**) | |
| many trees voting | **random forest** (**bagging**, bootstrap aggregation; an **ensemble**) | |
| each tree repairs the last | **gradient boosting** (each new tree fits the residual errors of the ensemble so far) | |
| a model memorised | **overfitting** and **underfitting**; the **bias-variance trade-off**; **generalisation** | |
| testing five times | **k-fold cross-validation**; **stratified k-fold** | |
| trying settings | **hyperparameter tuning** (**grid search**, random search) | |
| shuffle one column | **permutation importance** | |
| groups of customers | **clusters** from **k-means clustering**; for the business they are **customer segments** | |
| the bend in the chart | **elbow method** on the **inertia** (within-cluster sum of squares) | |
| mix many columns into two | **principal component analysis (PCA)**, a **dimensionality reduction** method; **principal components** | |
| rescale a column | **feature scaling**: **standardisation (z-score)** and **min-max scaling** | |
| squeeze the long tail | **log transform** | |
| odd row | **anomaly detection** (outlier detection; IsolationForest) | |
| customer summary of recency, frequency, spend | **RFM analysis** | |
| a single neuron | **perceptron / artificial neuron**: weighted sum plus **bias**, then an **activation function** (sigmoid, ReLU) | |
| layers | **input layer, hidden layers, output layer**; a **feedforward neural network** or **multilayer perceptron (MLP)** | |
| repeated small corrections | **training by gradient descent** with **backpropagation**; **loss function**, **learning rate**, **epoch**, **batch** | |
| a model someone else trained | **pretrained model**; **transfer learning**; **inference** | |
| split by date | **time-based split (temporal split)**; **walk-forward validation** | |
| copy last year | **seasonal naive forecast** (a **naive baseline**) | |
| earlier value as a column | **lag feature** | |
| how far ahead | **forecast horizon** | |

## Text, language models, delivery and governance (Sessions 21 to 24)

| Do not use as a name | Use this term | Plain-words explanation to give once |
|---|---|---|
| word counts | **bag of words** (count vectorizer); **TF-IDF** (term frequency, inverse document frequency) | |
| list of numbers for meaning | **embedding** (a **vector**); **cosine similarity**; **semantic search** | |
| mood of a message | **sentiment analysis** (text classification) | |
| pattern for text | **regular expression (regex)** | |
| clean the text | **text preprocessing**: lowercasing, **tokenisation**, removing **stop words** | |
| word or piece of word | **token**; the **context window** is how many tokens the model can read at once | |
| fluent but invented | **hallucination** | |
| piece of a document | **chunk** (**chunking**) | |
| find passages first, then answer | **retrieval-augmented generation (RAG)** | |
| test sheet for the search | **evaluation set** (a labelled test set); **precision at k** and **recall at k** | |
| record of what the assistant did | **audit log** (prompt log) | |
| instruction to the model | **prompt** (a **system prompt** sets rules; **zero-shot** and **few-shot** prompting) | |
| save the model to a file | **model serialisation (persistence)** with joblib or pickle | |
| put the app on the internet | **deploy** the app (**deployment**) | |
| same result every run | **reproducibility** (fix the random **seed**, record library **versions**, a **requirements file**) | |
| project folder with history | **Git repository**; **commit**, **branch**, **push**; hosted on **GitHub** | |
| one-page model note | **model card** | |
| inputs change over time | **data drift** (and **concept drift** when the relationship changes) | |
| a column that stands in for another | **proxy variable** | |
| a fairness check by group | **fairness audit** (compare error and approval rates across groups; **disparate impact**) | |
| data about a person | **personal data**; the person is the **data subject** (Uganda Data Protection and Privacy Act, 2019); the organisation deciding the use is the **data controller** | |
| mark scheme | **rubric** | |
| capstone summary | **executive summary** | |

## Python and SQL names

Keep the real syntax names exactly: DataFrame, Series, index, `read_csv`, `groupby`, `merge`, `pivot_table`, `value_counts`, `train_test_split`, `LogisticRegression`, `RandomForestClassifier`, `GradientBoostingClassifier`, `KMeans`, `PCA`, `Pipeline`, `cross_val_score`, `GridSearchCV`, `classification_report`, `roc_auc_score`, SQL `SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, JOIN ... ON, LEFT JOIN, CASE WHEN, NULL`. Variable names in notebooks use the conventions: `df`, `orders`, `X`, `y`, `X_train`, `X_test`, `y_train`, `y_test`, `y_pred`, `y_prob`, `model`, `baseline_model`, `cv_scores`, `results`. No cute names.

## Notes

- Where a term has a precise statistical meaning, define it once with the formula where one exists (mean, standard deviation, standard error, z-score, residual, R squared, precision, recall, F1, MAE) using the `formula` slide kind and name every symbol.
- The beginner must still understand every slide without the speaker notes. The plain-words explanation follows the term and stays.
- "Illustrative" or "hypothetical" labels for made-up numbers. Lakeside, Nile Microfinance, District Clinics are fictional and generated.
- Do not call a gap between two totals a "residual" unless it is a model residual.

## Added after Session 2 (4 Nov 2026)

| Term | Use |
|---|---|
| identifier | a variable that names a record (order_id). Never add it up. |
| orphan record | a foreign key value with no matching primary key in the other table |
| junction table (bridge table) | a table that links two many-to-many tables |
| crow's foot | the three-prong line end on an ERD that marks the many side |
| data type versus variable type | data type: how the cell stores the value (string, integer, float). Variable type: how the value is measured (numeric, categorical, datetime, text). |

Model session: `content/s02.py` and `kit/diagrams_ds_a.py` (figure kinds for records, keys, ERD and traces; reuse them, do not duplicate). Known kit limits: `x_card` overlaps labels when four fields wrap (use three short fields), `x_sheet` does not scale to height (use size 15) and highlights one cell only.

## Added after the review pass (4 Nov 2026)
instalment-to-income ratio (also payment-to-income ratio; the loans variable `instalment_to_income`), join log (audit trail of row counts around a join), proof table, statistical power (the chance a test detects a real effect of a stated size), sampling variability, reconciliation difference (control-total gap in cleaning; `answer_key.json` still calls it `residual_ugx`), decision threshold (never 'cut-off'), true positive rate (recall, sensitivity) and false positive rate for the ROC axes (never 'catch rate' or 'false-alarm rate').
