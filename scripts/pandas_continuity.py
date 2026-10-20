"""Pandas-first continuation. Preserve issued contracts and all existing URLs.
Applied after the foundations and notes overlays so rebuilds cannot restore
manual CSV/list workflows after Week 5. All examples are teaching data.
"""
from copy import deepcopy
import re
SOURCE='https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html'

def p(title,*body,note):
 return dict(kind='explanation',title=title,body='\n\n'.join(body),notes=note+'\n\nReference: '+SOURCE,pandas_revision=True)
def t(title,rows,caption,note):
 return dict(kind='table',title=title,body='',table=rows,caption=caption,notes=note,pandas_revision=True)
def c(title,program,caption,note):
 lines=program.strip().splitlines();result=[]
 for start in range(0,len(lines),8):
  part=start//8+1;total=(len(lines)+7)//8
  result.append(dict(kind='code',title=title+(f' ({part}/{total})' if total>1 else ''),body='',code='\n'.join(lines[start:start+8]),practice_code=program.strip() if start==0 else '',caption=caption if start==0 else 'Continue the same cell with the indentation shown.',explain=[(note.split('. ')[0]+'.')[:130]],notes=note+'\n\nComplete worked example:\n'+program.strip(),pandas_revision=True))
 return result

def picture(old,title,caption=None):
 s=deepcopy(next(s for s in old if s['title']==title))
 if caption:s['caption']=caption
 return s

def bridge():
 return [p('Pandas inside the assignment functions','The published function names and outputs stay the same. Inside a function, pd.DataFrame(records) gives the input records column names.','Calculate with pandas. Convert back only when returning the type requested by the task. This keeps existing submissions compatible.',note='A function interface is the agreed input and output format, not a ban on pandas. The grader calls the function on unseen records. Explain that a DataFrame returned where a list is required is still a contract error.'),
 p('Returning the requested Python type','table.to_dict("records") returns a list containing one dictionary per row. summary.to_dict() returns a dictionary from labels to values.','table.to_numpy().tolist() returns rows of values in the selected column order. series.tolist() returns a column as a list.','Use int(...) for counts and float(...) for numerical summaries when constructing a returned dictionary.',note='Point out the difference between a list of row dictionaries and a list of lists. The words records and list describe output formats. Conversion belongs at the function boundary, not after every calculation.'),
 *c('A table inside a function','''import pandas as pd
def totals(records):
    table = pd.DataFrame(records)
    result = table.groupby("site")["hours"].sum()
    return result.to_dict()
example = [{"site": "A", "hours": 2},
           {"site": "A", "hours": 3}]
print(totals(example))''','Output: {"A": 5}. This is a practice example.', 'The caller supplies records. The function builds a table, groups its hours, and returns a dictionary. No CSV file is opened inside this function: the caller already supplied the data. Do not copy this site/hours schema into an engineering_data task.')]

def week6(old,cohort):
 out=[p('From Week 5 tables to Week 6 cleaning','Week 5 loaded a CSV into a DataFrame and selected columns and rows. We use the same tools today.','We will keep the raw table, examine missing and repeated observations, justify each change, then summarise and plot.',note='Recall df["kwh"] and df[mask]. Today changes the data-quality question, not the basic data structure. CSV is still the file format; pandas is the library reading it.'),
 p('The issued table and its measurements','engineering_data.csv contains record_id, equipment_id, load_pct, ambient_c and target. One row is one observation.','record_id identifies the observation. equipment_id identifies its source and can repeat legitimately. load_pct is a percentage; ambient_c is degrees Celsius.',note='The target differs by cohort: CML3111 motor winding temperature (deg C), CML3112 building cooling load (kW), CML3113 crusher energy demand (kWh/t). All are synthetic records. Show these headers before asking learners to select a field.'),
 p('Loading the supplied CSV','Extract the student ZIP. In Colab, upload engineering_data.csv using the Files panel. Keep it beside the notebook locally.','pd.read_csv reads a CSV into a DataFrame. head() previews rows, shape gives dimensions and dtypes shows how columns were interpreted.',note='If the file is missing, check the Files panel and exact spelling. Uploading the notebook does not upload its CSV. Do not switch to the csv module as a workaround.'),
 *c('Inspect the issued table','''import pandas as pd
raw_table = pd.read_csv("engineering_data.csv")
print(raw_table.head())
print(raw_table.shape)
print(raw_table.dtypes)''','The target column uses your programme’s stated unit.','Explain raw_table as the name of the untouched input. Printed dimensions vary by issued variant; do not hardcode them. Numeric blanks normally appear as NaN after reading. The following tiny table is separate from the assignment data.'),
 p('A small table we can check by hand','Our practice table records room temperatures in degrees Celsius. It contains one repeated observation, one missing reading and one unusual reading.','We will use it to understand the operations before applying the assignment’s own rules.',note='Do not imply this is the assignment answer. The assignment has additional load and target rules and a different schema.'),
 *c('Create the practice table','''practice = pd.DataFrame({
    "record_id": [1, 1, 2, 3, 4],
    "room": ["A", "A", "A", "B", "B"],
    "temperature_c": [20, 20, None, 24, 80]
})
print(practice)''','Five rows; record 1 appears twice.','Each dictionary key becomes a column. Lists supply values in row order. pandas represents the missing numerical value as NaN. 80 may be suspicious, but a large value alone is not permission to delete it.'),
 p('Missing is different from zero','Zero is a recorded number. None, NaN and pd.NA can represent missing information in different Python or pandas structures.','Use series.isna() and series.notna() to detect missing entries in pandas. Do not use value is None as a general DataFrame missing-value test.',note='A numeric Series containing None commonly stores NaN instead. isna recognises pandas missing markers. For [0, None, 4], only the middle entry is missing. Count it without discarding zero.'),
 *c('Find and count missing values','''gaps = practice["temperature_c"].isna()
print(gaps.tolist())
print(int(gaps.sum()))
print(practice[gaps])''','Output: [False, False, True, False, False]; count 1.','isna returns one Boolean per row. Summing Booleans counts True values. practice[gaps] selects exactly the missing row. Explain int as conversion to a Python integer.'),
 picture(old,'A working copy preserves the original','Keep the original table. Apply a stated rule to a separate working copy.'),
 p('A working copy and duplicate observations','clean = practice.copy() creates a working table. Keep practice unchanged so the effect of cleaning can be checked.','duplicated(subset="record_id", keep="first") marks later occurrences of an observation ID. drop_duplicates removes those occurrences.','Repeated room or equipment names are expected. They do not identify duplicate observations.',note='The first and second rows share record_id=1, so only the second is a duplicate. The A label on record 2 is legitimate. Explain subset as the column(s) used to decide sameness and keep="first" as the retention rule.'),
 *c('Keep the first copy of each observation','''duplicate = practice.duplicated("record_id")
print(duplicate.tolist())
clean = practice.drop_duplicates("record_id").copy()
print(clean["record_id"].tolist())''','Remaining observation IDs: [1, 2, 3, 4].','drop_duplicates defaults to keeping the first occurrence. Original row order is retained. copy gives a clear independent working table. The original practice still has five rows.'),
 p('Median filling adds an estimate','Sort the retained known values: 20, 24, 80. The middle value is 24. pandas median() ignores missing values.','fillna(24) fills only missing entries. A measured zero or the unusual 80 stays unchanged.','The filled value is an estimate, not a recovered measurement. A column with no known values needs an explicit policy.',note='For an even count, average the two middle numbers. Example: 20,22,24,80 gives 23. Do not silently substitute zero if all readings are missing. Our practice and issued grading data have known ambient values after cleaning.'),
 *c('Fill only the missing temperature','''fill = clean["temperature_c"].median()
clean["estimated"] = clean["temperature_c"].isna()
clean["temperature_c"] = clean["temperature_c"].fillna(fill)
print(fill)
print(clean["temperature_c"].tolist())
print(len(practice), len(clean))''','Fill: 24.0. Values: [20.0, 24.0, 24.0, 80.0].','The estimated column is useful in this practice audit. The assignment says make no other changes, so do not add that column to its returned records. Assigning the filled column avoids chained or inplace assignments.'),
 p('Filtering and missing targets','A mask is one True/False decision per row. notna() keeps known measurements; between(low, high) includes both limits by default.','Use & to combine pandas masks and parentheses around comparisons. ~ reverses True and False in a mask. Python and does not combine entire Series.','For A6, remove duplicate IDs first. Then exclude missing targets and loads outside 0–100. Calculate the ambient median only from the rows that remain.',note='Order matters: if the first record with an ID is invalid, a later duplicate must not replace it. Explain that the known-target mask and valid-load mask must both be True. This is the issued policy, not a universal cleaning rule.'),
 *c('A filter with two conditions','''measured = practice["temperature_c"].notna()
moderate = practice["temperature_c"].between(15, 30)
selected = practice[measured & moderate]
print(selected["record_id"].tolist())''','Output: [1, 1, 3]. This filter does not remove duplicates.','The practice filter demonstrates combining conditions only. It is not authority to delete unusual temperatures from the assignment. Repeated IDs remain because this cell filters the original practice table.'),
 p('Numeric text and failed conversion','pd.Series([...]) builds one labelled column from a list of values.','pd.to_numeric converts numeric text into numbers. Its default is to raise an error for text such as "24 C".','errors="coerce" replaces unconvertible entries with a missing value. Count and inspect these failures before using a mean.','A sentinel such as -999 or zero counts as a real number unless the data documentation says it represents missing information.',note='The error identifies a value and position to inspect. Coercion does not repair the value or justify discarding its row. Zero can be valid. Only replace a sentinel when the source documentation supports that interpretation.'),
 *c('Inspect values that failed conversion','''text = pd.Series(["20", "24 C", "26"])
numbers = pd.to_numeric(text, errors="coerce")
failed = text.notna() & numbers.isna()
print(text[failed].tolist())
print(int(failed.sum()))''','Failed value: ["24 C"]. Count: 1.','A Series is a labelled column. Compare original non-missing values with converted missing values to distinguish parsing failures from pre-existing gaps. The unit string must be interpreted before repair.'),
 p('Summaries and an audit','mean(), min() and max() summarise a numerical column. groupby collects rows with the same label before a calculation.','An audit counts what is actually present. It must still detect a duplicate, missing target or invalid load if the supposed cleaned data contain one.',note='Do not return zero for every audit defect just because clean_records is supposed to remove them. The grader deliberately supplies imperfect cleaned data to check that audit_cleaning inspects its input.'),
 *c('Summarise the cleaned practice table','''values = clean["temperature_c"]
print(float(values.mean()))
print(float(values.min()), float(values.max()))
means = clean.groupby("room")["temperature_c"].mean()
print(means.to_dict())''','Mean: 37.0. Range: 20.0–80.0. A: 22.0; B: 52.0.','A has observations 20 and 24; B has 24 and 80. The large B mean motivates investigation, not a causal claim. The estimated reading affects the result.'),
 picture(old,'Choosing a chart for the question'),
 p('Charts from DataFrame columns','A scatter plot pairs two numerical measurements. A histogram counts observations in value ranges. A bar chart can compare group means.','matplotlib supplies figures and axes. An axis label states the quantity and unit. plot methods draw on the axes supplied through ax=.',note='Explain fig as the whole image and ax as the plotting area. Use data columns directly instead of rebuilding them with loops. A pooled histogram cannot answer whether two group means differ.'),
 *c('Draw and label the practice charts','''import matplotlib.pyplot as plt
fig, ax = plt.subplots()
clean.plot.scatter(x="record_id", y="temperature_c", ax=ax)
ax.set_xlabel("Observation ID (not time)")
ax.set_ylabel("Temperature (degrees C)")
ax.set_title("Practice observations after cleaning")
plt.show()''','The horizontal axis is observation ID, not elapsed time.','The project scatter instead uses load_pct and target with the cohort unit. Do not infer a time trend from record order. The following bar and histogram answer different questions.'),
 *c('Group comparison and distribution','''fig, ax = plt.subplots()
means.plot.bar(ax=ax)
ax.set_ylabel("Mean temperature (degrees C)")
ax.set_title("Practice room means")
fig2, ax2 = plt.subplots()
clean["temperature_c"].plot.hist(bins=3, ax=ax2)
ax2.set_xlabel("Temperature (degrees C)")
ax2.set_ylabel("Observation count")
ax2.set_title("Practice temperature distribution")
plt.show()''','Bar: group means. Histogram: counts in value intervals.','bins chooses how many intervals to use. The project has a specific ten-bin rule; three is only this small demonstration. Actual Figure objects must be returned by the assessment function, not screenshots or dictionaries.')]
 out+=bridge()
 out+=[p('Missing values at the submission boundary','The issued records use None for missing numeric fields. A DataFrame may represent the same gaps as NaN.','The supplied loader and records_from_table helper handle that conversion. Use them as provided; do your analysis with pandas.','The assignment still needs your cleaning, summary and audit functions. The loader is not a solution.',note='The helper uses an object-typed copy before replacing missing markers, otherwise a float column would convert None back to NaN. Return copied records in original order and preserve raw input. Model teaching later uses training-only imputation rather than cleaning a full modelling dataset before splitting.')]
 return out

def week8(old,cohort):
 out=[p('Tables become model inputs','Continue with pandas tables. X contains the selected feature columns; y contains the target column in matching row order.','A feature is available when making a prediction. The target is the value we want the model to predict.',note='X is a DataFrame, y is a Series. Double brackets select several columns as a table; single brackets select one column. A model never receives a new observation’s true target at prediction time.'),
 p('Training validation and final test','Training observations fit the model. Validation observations help choose the model. The final test estimates performance after choices are fixed.','If the intended use is new equipment, keep all observations of one equipment ID in one partition.',note='Demonstrate partition roles before fit. Week 10 develops grouping. The tiny independent tables below illustrate API behaviour only and do not establish reliable performance.'),
 t('Four invented training observations',[['Input','Target'],['1','12'],['2','14'],['3','16'],['4','18']], 'The pattern is target = 10 + 2 × input.', 'Work out 15 at input 2.5 by hand. Explain that the real model estimates its relationship from examples rather than receiving this equation.'),
 picture(old,'Fitting a line to observations'),
 p('Column selection and shape','train[["input"]] keeps a table, even with one column. train["target"] gives a labelled column.','shape reports dimensions: X.shape is (4, 1), meaning four observations and one feature. y.shape is (4,), meaning four target values.','Choose X and y from the same rows. Filtering one without the other can mispair values or raise a length error.',note='A tuple describes dimensions. A model’s two-dimensional feature input differs from a one-dimensional target. Use named columns again when predicting to preserve order and meaning.'),
 *c('Create named training and prediction tables','''import pandas as pd
train = pd.DataFrame({"input": [1, 2, 3, 4],
                      "target": [12, 14, 16, 18]})
features = ["input"]
X = train[features]
y = train["target"]
new = pd.DataFrame({"input": [2.5, 5.0]})
print(X.shape, y.shape)''','Shapes: (4, 1) and (4,).','features is a list of column names, not the numerical data. train[features] selects those columns in that order. Lists still have a legitimate role as configuration; the actual observations remain a DataFrame.'),
 p('A model object learns a rule','Import LinearRegression from sklearn.linear_model. LinearRegression() creates an unfitted model object.','fit(X, y) learns its parameters from training data. predict(new[features]) returns predictions without fitting again.','tolist() converts a prediction array into the Python list required by the assignment.',note='Explain module, class, object and method. Instantiation and training are different steps. Printing a prediction is useful for inspection, but the assessed function must return it.'),
 *c('Fit and predict with named columns','''from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(new[features])
print(predictions.round(2).tolist())''','Predictions: [15.0, 20.0].','round(2) is only for display. Keep full precision in returned answers. If feature labels or their order change, fix the input selection rather than suppressing warnings.'),
 p('A baseline makes a simple comparison','A training-mean baseline predicts the training target mean for every new row. DummyRegressor(strategy="mean") implements it.','Compare models on the same held-out observations. A learned model must earn its complexity by improving useful evidence.',note='The four targets average 15. Both new rows get 15 from the baseline. The line also predicts 15 at 2.5, so this one point does not establish superiority.'),
 *c('Run the mean baseline','''from sklearn.dummy import DummyRegressor
baseline = DummyRegressor(strategy="mean")
baseline.fit(X, y)
print(baseline.predict(new[features]).tolist())''','Baseline predictions: [15.0, 15.0].','strategy is a named option. The mean comes from training targets only. Validation and final-test targets never determine it.'),
 p('A regression tree predicts from regions','A regression tree asks threshold questions about feature values. At a leaf it predicts from the training targets that reached that region.','max_depth limits how many levels the tree can grow. random_state fixes the randomness used by this example.',note='A tree need not extrapolate a straight-line trend. These models answer the same prediction task using different rules. The assignment fixes max_depth=4 and random_state=17 for reproducible grading.'),
 *c('Fit the required small tree','''from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor(max_depth=4, random_state=17)
tree.fit(X, y)
print(tree.predict(new[features]).tolist())''','The tree predicts training-region values, not an extended line.','With these inputs the predictions are 14 and 18. The 2.5 observation falls on the left side of a 2.5 threshold. Discuss why unseen input 5 need not produce 20.'),
 p('Missing features and a pipeline','loc[row_label, column_label] selects a table cell by its labels. Assigning None marks our practice cell as missing.','SimpleImputer(strategy="median") learns one fill value per feature from training observations.','make_pipeline(imputer, model) links preprocessing and modelling. fit learns both from training data; predict reuses the fitted steps.','Never calculate fill values from validation or test rows. Never fill a missing target and pretend it was measured.',note='A pipeline is a sequence of operations. It prevents accidentally refitting the imputer at prediction time. All-missing feature columns require a separate explicit policy; this example has known training values.'),
 *c('Fit preprocessing only on training data','''from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
train_missing = train.copy()
train_missing.loc[1, "input"] = None
pipeline = make_pipeline(SimpleImputer(strategy="median"),
                         LinearRegression())
pipeline.fit(train_missing[features], y)
print(pipeline.predict(new[features]).round(2).tolist())''','Training fills come from train_missing, never from new.','loc[row_label, column_label] selects a cell by labels; explain this syntax before running. The missing training input is filled using median 3. This changes the learned line, so do not expect the earlier predictions.'),
 p('Prediction errors use matching rows','A residual is actual minus predicted. MAE is the mean absolute error. RMSE is the square root of the mean squared error.','Both use the target unit. Squaring makes RMSE more sensitive to large errors. Neither is a guaranteed error bound for every future prediction.',note='For actual 10 and 20 versus predictions 12 and 16, residuals are -2 and 4. MAE is 3; RMSE is sqrt(10), about 3.1623. A plot of residual against actual shares actual in both axes; a pattern alone needs further checks.'),
 *c('Calculate two error measures with pandas','''errors = pd.DataFrame({"actual": [10, 20],
                       "predicted": [12, 16]})
residual = errors["actual"] - errors["predicted"]
mae = residual.abs().mean()
rmse = (residual ** 2).mean() ** 0.5
print(float(mae), float(rmse))''','MAE = 3.0; RMSE ≈ 3.1623.','abs takes the magnitude. **2 squares each error and **0.5 takes the square root after averaging. Independent Series align on row labels; constructing the paired table together prevents accidental mismatch in this example.'),
 p('Training scores are not test evidence','A regression model’s score(X, y) usually reports R²: performance relative to predicting the evaluation target mean. It is not classification accuracy.','Scoring the training rows describes training fit. Use unseen evaluation rows to assess generalisation.',note='R² can be negative. A high training score alone does not show that new equipment will be predicted well. Keep the mean baseline comparison and the target-unit errors visible.')]
 return out+bridge()

def week9(old,cohort):
 out=[p('A table of actual and predicted labels','For this lesson, 1 means a warning is needed and 0 means no warning is needed. Each row pairs one actual label with one prediction.','Continue using pandas to inspect and count those paired outcomes.',note='Actual is the reference answer; predicted is the model decision. The word positive means the designated class, not a desirable outcome.'),picture(old,'Every paired result belongs in one cell'),
 t('Four outcomes',[['Actual','Predicted','Name'],['1','1','True positive'],['0','0','True negative'],['0','1','False positive'],['1','0','False negative']], 'A false negative misses a real warning.', 'A false positive raises an unnecessary warning. Each observation belongs to exactly one category.'),
 p('Counting conditions with pandas','== compares values. & means both conditions must hold for each row. Put each comparison in parentheses.','A Boolean mask contains True and False values. sum() counts True entries; int(...) returns a Python integer.',note='Do not use Python and between Series. Confirm the row pair belongs to the selected category before summing it.'),
 *c('Count the four outcomes','''import pandas as pd
results = pd.DataFrame({"actual": [1, 1, 0, 0],
                        "predicted": [1, 0, 1, 0]})
a = results["actual"]
pred = results["predicted"]
tp = int(((a == 1) & (pred == 1)).sum())
fn = int(((a == 1) & (pred == 0)).sum())
fp = int(((a == 0) & (pred == 1)).sum())
tn = int(((a == 0) & (pred == 0)).sum())
print(tp, fn, fp, tn)''','Output: 1 1 1 1.','Explain each mask against the four-row table. This counts observations rather than calculating a mean of labels. Rows must stay paired and equal in number.'),
 p('Precision recall and a zero denominator','Precision = TP / (TP + FP): of the warnings raised, how many were correct?','Recall = TP / (TP + FN): of the real warnings, how many were detected?','If a denominator is zero, this assignment returns 0 for that measure. State the convention rather than divide by zero.',note='The worked table gives precision=0.5 and recall=0.5. Neither measure alone shows every error. A system that predicts only the majority class can have high accuracy while missing all rare failures.'),
 *c('Calculate rates and the stated cost','''precision = 0.0
if tp + fp > 0:
    precision = tp / (tp + fp)
recall = 0.0
if tp + fn > 0:
    recall = tp / (tp + fn)
cost = 5 * fn + fp
print(precision, recall, cost)''','Output: 0.5 0.5 6.','The cost rule assigns five units to a missed warning and one to a false alarm. It is a teaching assumption, not an approved engineering safety limit.'),
 p('A probability becomes a decision','A model can return a probability for class 1. A threshold converts it into a yes/no decision.','Using >= includes an observation exactly on the threshold. Lowering the threshold raises more warnings, which can improve recall and also increase false alarms.',note='Probability and class are different outputs. Explain .astype(int) before running: it converts False to 0 and True to 1. Threshold selection belongs on validation data, not repeated final-test tuning.'),
 *c('Apply a threshold to probabilities','''probability = pd.Series([0.1, 0.4, 0.8])
labels = (probability >= 0.5).astype(int)
more_warnings = (probability >= 0.3).astype(int)
print(labels.tolist())
print(more_warnings.tolist())''','At 0.5: [0, 0, 1]. At 0.3: [0, 1, 1].','The probabilities did not change; the operating decision did. Actual labels are needed before counting new false alarms or recall.'),
 p('Categories and multiple classes','Category names may need numeric indicator columns before modelling. pd.get_dummies creates one indicator column per category.','A binary metric assumes two classes. If the actual labels contain three classes, use a stated multiclass metric policy rather than hiding or deleting the third class.',note='Explain one-hot encoding without claiming a numeric order between category names. Fit any learned encoder on training data and preserve its columns. The assignment remains binary labels 0 and 1.'),
 *c('Inspect an indicator table','''kind = pd.Series(["pump", "motor", "pump"])
indicators = pd.get_dummies(kind, dtype=int)
print(indicators)''','Each row has 1 in its category column and 0 elsewhere.','This table is an illustration. For a model, use a fitted encoder within the preprocessing pipeline to handle consistent columns and unseen categories.'),
 p('Read the issued classification CSV','classification_case.csv contains actual and predicted labels. Read it with pd.read_csv, inspect its columns, then pass the two columns as lists to your function.','Your function must also work on unseen paired labels with the same published binary rules.',note='The supplied classification file is separate from engineering_data.csv. Do not load the generic engineering table when this task asks for actual and predicted.'),
 *c('Load the issued paired outcomes','''case = pd.read_csv("classification_case.csv")
print(case.head())
actual = case["actual"].tolist()
predicted = case["predicted"].tolist()
print(len(actual), len(predicted))''','Both lists must have the same length.','This cell loads the task data; it does not implement classification_metrics. Learners write their function using the demonstrated masks and return the specified dictionary.')]
 return out+bridge()

def week10(old,cohort):
 return [p('Three partitions with different jobs','Training fits the model and its preprocessing. Validation guides choices. The final test measures the fixed choice once.','Keep the same pandas column names and order in every partition.',note='Evaluation data may be inspected for schema, but their targets must not train the model or determine preprocessing values.'),picture(old,'Three sets have different jobs'),
 p('Repeated equipment stays together','equipment_id identifies the source of observations. For evaluation on unseen equipment, an ID must not appear in both training and evaluation.','isin(["A", "B"]) creates a row mask for membership in the named groups. loc[mask, columns] selects rows and columns by labels.',note='A random split of individual rows can leak equipment-specific patterns. The assignment gives fixed E1–E4, E5, E6 partitions, not the A/B/C practice labels.'),
 *c('Split a teaching table by equipment','''import pandas as pd
data = pd.DataFrame({"record_id": [1, 2, 3, 4],
                     "equipment_id": ["A", "A", "B", "C"],
                     "input": [20, 22, 24, 30]})
train = data[data["equipment_id"].isin(["A"])].copy()
validation = data[data["equipment_id"].isin(["B"])].copy()
test = data[data["equipment_id"].isin(["C"])].copy()
print(train["record_id"].tolist())''','Training IDs: [1, 2]; validation: [3]; test: [4].','copy makes partition ownership explicit. Each group stays together. Four invented rows teach the split operation but are insufficient for a trustworthy real-world evaluation.'),
 p('Learn the fill from training only','Find the median of training values. Use that same number to fill gaps in validation and test values.','A pipeline fits the imputer and model together on training data. Calling predict reuses the fitted preprocessing.',note='Even preprocessing without target labels can leak information about evaluation distributions. Do not fit_transform on the complete file before splitting.'),
 *c('Reuse the training median','''training_values = pd.Series([20, 22, 24])
validation_values = pd.Series([None, 40])
training_median = training_values.median()
filled = validation_values.fillna(training_median)
print(float(training_median), filled.tolist())''','Output: 22.0 [22.0, 40.0].','The validation value 40 does not contribute to the median. The full model should use the Week 8 pipeline for this operation.'),
 p('Leakage can hide inside preprocessing','Scaling learns location and spread from data. Fit scalers only on training rows, just like imputers.','A model-only pipeline cannot repair earlier full-file imputation. Include the required preprocessing steps inside the fitted pipeline.',note='Some algorithms react to feature scale; trees generally do not need standard scaling for split order. Use StandardScaler in a pipeline when appropriate, and do not introduce it as a compulsory extra step for every model.'),
 p('Training fit and generalisation','Overfitting means the model follows training-specific patterns that do not transfer well. Underfitting means it misses useful relationships even in training.','A large gap between strong training performance and weaker held-out performance is a warning to investigate.',note='Do not treat any numeric gap as proof of one cause. Different data distributions or leakage can also affect scores. Keep units, sample counts and split policy beside metrics.'),picture(old,'Each fold takes a turn at validation'),
 p('Cross-validation repeats the evaluation','Each fold takes a turn as validation while the others supply training data. Group-aware folds keep equipment together.','Report the mean and variation, not just the best fold. std(ddof=0) describes their spread using the population standard deviation.',note='Folds are evaluation partitions, not new independent datasets. Refit preprocessing within each training fold. An unusually poor fold may indicate a difficult equipment group or distribution shift.'),
 *c('Summarise several validation errors','''fold_errors = pd.Series([2.0, 3.0, 4.0])
print(float(fold_errors.mean()))
print(float(fold_errors.std(ddof=0)))''','Mean error: 3.0; population standard deviation ≈ 0.8165.','ddof is the correction used in the denominator. Here ddof=0 describes these three reported fold results as a complete set. A different convention must be labelled.'),
 p('The issued split and modelling functions','group_split returns record IDs for E1–E4 training, E5 validation and E6 test, preserving input order.','predict_regression keeps the Week 8 interface and training-only pipeline. Do not combine the partitions before fitting.',note='Use pandas filtering and the record_id Series, then .tolist() at the return boundary. The two functions have different responsibilities: splitting identifies membership; prediction trains only on the supplied training records.')]+bridge()

def week11(old,cohort):
 return [p('Features are named columns','A derived feature calculates new information from inputs already available at prediction time. A ratio divides; an interaction multiplies.','Use the same formula, column names and order for training and evaluation tables.',note='A feature using the future target leaks the answer. A physical motivation is useful but must still be checked under the same evaluation protocol.'),picture(old,'A physical relationship can form a feature'),
 p('Assigning a derived column','table["new_name"] = expression creates or replaces a column. pandas applies column arithmetic row by row.','copy() protects the source table. Select the final columns explicitly before fitting or returning a feature matrix.',note='This avoids building feature rows with append loops. Naming intermediate columns makes the units and formulas inspectable.'),
 *c('Build derived columns in pandas','''import pandas as pd
raw = pd.DataFrame({"load_pct": [40, 60],
                    "ambient_c": [25, 30]})
features = raw.copy()
features["load_fraction"] = features["load_pct"] / 100
features["interaction"] = features["load_pct"] * features["ambient_c"]
print(features)''','Fractions: 0.4, 0.6. Interactions: 1000, 1800.','The interaction inherits combined units; it is not a new directly measured physical quantity. The assignment orders load_pct, ambient_c, load_fraction, interaction.'),
 p('Ablation tests one change','Compare a baseline feature set with an extended feature set on the same validation rows. Keep the model and fitting procedure the same.','Improvement = baseline MAE minus extended MAE. A positive result means lower error for the extended version.',note='Do not compare different splits or training observations. The issued ablation task uses complete inputs and only adds load_pct*ambient_c, not the fraction column.'),
 p('The two-model practice experiment','Our invented table has a, b and target columns. A helper creates the a_times_b interaction on a copy.','LinearRegression fits each feature set. mean_absolute_error compares predictions with the same validation targets.',note='A helper function is reusable preparation, not a fitted preprocessing estimator. Its deterministic multiplication formula is identical for both partitions. This tiny experiment teaches the comparison procedure rather than establishing engineering benefit.'),
 *c('Prepare training and validation tables','''train = pd.DataFrame({"a": [1, 2, 3, 4, 5],
                      "b": [2, 3, 2, 4, 3],
                      "target": [3, 5, 5, 8, 8]})
valid = pd.DataFrame({"a": [2, 3], "b": [2, 3],
                      "target": [4, 6]})
def add_interaction(table):
    out = table.copy()
    out["a_times_b"] = out["a"] * out["b"]
    return out
train_x = add_interaction(train)
valid_x = add_interaction(valid)''','The same helper calculates both interaction columns.','The target remains in these tables for convenience but is never selected as a predictor. Read the feature-name lists in the next cell before fitting.'),
 *c('Compare models on the same validation rows','''from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
base_cols = ["a", "b"]
extended_cols = ["a", "b", "a_times_b"]
base = LinearRegression().fit(train_x[base_cols], train["target"])
extra = LinearRegression().fit(train_x[extended_cols], train["target"])
base_pred = base.predict(valid_x[base_cols])
extra_pred = extra.predict(valid_x[extended_cols])
base_mae = mean_absolute_error(valid["target"], base_pred)
extra_mae = mean_absolute_error(valid["target"], extra_pred)
print(float(base_mae - extra_mae))''','Both errors use the same two validation targets.','In these additive practice data both fits can be essentially exact; tiny floating differences are not evidence of useful improvement. Round only displayed values, never submitted metrics.'),
 p('Scaling and encoding have distinct purposes','Scaling changes numerical units of comparison. Encoding turns category labels into model inputs. Fit learned transformations on training data.','An ordinary decision tree generally preserves its splits under a positive linear rescaling of a feature. A scaler need not improve its score.',note='Do not add transformations just because they exist. State which algorithm and data property motivates each step. A category code must not imply an unsupported ranking.'),
 p('The two assignment outputs differ','make_features returns rows ordered as load_pct, ambient_c, load_fraction, interaction. Select those four columns, then use to_numpy().tolist().','ablation_metrics compares only the base two columns with the base two plus interaction. Return base_mae, extended_mae and their difference.',note='Keep the distinction explicit: the feature-building task asks for four columns, while the experimental comparison specifies three in the extended model. Both contracts are unchanged.')]+bridge()

def week12(old,cohort):
 return [p('Compare models in a table','Each candidate has a name, validation error and prediction latency. Latency means the time needed to produce a prediction.','First decide which candidates meet every constraint. Rank only the eligible candidates.',note='The final test is not a model-selection table. Validation errors must use comparable observations and units. Latency figures need a stated measurement environment.'),t('Two invented candidates',[['Name','MAE','Latency (ms)'],['simple','3','2'],['complex','1','20']], 'Requirements: MAE at most 3 and latency at most 10 ms.', 'Only simple meets both limits. A lower error does not excuse a failed latency requirement.'),
 p('An inclusive filter combines both limits','<= includes equality with the limit. & requires both masks to be True.','The result may contain no candidates. eligible.empty tells us whether the filtered table has no rows.',note='Test an exactly-at-limit row. Explain that no eligible candidate is a valid outcome, not permission to relax the requirements silently.'),
 *c('Filter candidate rows','''import pandas as pd
candidates = pd.DataFrame({"name": ["simple", "complex"],
                           "validation_mae": [3.0, 1.0],
                           "latency_ms": [2, 20]})
error_ok = candidates["validation_mae"] <= 3
speed_ok = candidates["latency_ms"] <= 10
eligible = candidates[error_ok & speed_ok]
print(eligible["name"].tolist())''','Output: ["simple"].','The masks have one result per candidate. Adding a fast candidate with error above 3 must not make it eligible.'),
 p('Ranking and tie-breaks','sort_values(["validation_mae", "latency_ms", "name"]) sorts by error first, latency second and name third. Ascending is the default.','iloc[0] selects the first row by position after sorting. Use it only after checking that the table is not empty.',note='Unlike loc, iloc uses integer positions. The name tie-break is alphabetical. Show two equal-error rows before asking learners to implement the policy.'),
 *c('Choose only from eligible candidates','''ordered = eligible.sort_values(
    ["validation_mae", "latency_ms", "name"])
if ordered.empty:
    winner = None
else:
    winner = ordered.iloc[0]["name"]
print(winner)''','Winner: simple. No eligible rows would return None.','Sorting a copy of the candidate table leaves original inputs unchanged. The assessed function returns the name, not the whole row or the smallest metric.'),
 p('A recommendation needs limits and evidence','State the selected model, validation error, latency and requirements. Explain when the recommendation would change.','A local explanation describes one prediction. It does not establish causation or guarantee safe performance elsewhere.',note='A conditional engineering recommendation recognises uncertainty and deployment constraints. An impressive training score or feature-importance chart alone is insufficient.'),
 p('Hyperparameters and fair comparison','A hyperparameter is a setting chosen before fitting, such as maximum tree depth. Training learns model parameters from the data.','Tune settings using validation or cross-validation. Keep the final test reserved for the fixed choice.',note='A trial that sees final-test performance and then chooses a model has used that test for selection. Explain why repeated trial-and-error can overfit validation too.'),
 p('Returning the model-selection result','select_model accepts candidate dictionaries. Convert them to a DataFrame, apply both limits, sort and return the chosen name or None.','regression_errors keeps the Week 8 MAE/RMSE contract, full precision and paired-observation requirement.',note='Empty input must not fail because column names are missing; construct a DataFrame with the expected columns or handle the empty case before selecting columns. No final-test scores are used.')]+bridge()

BUILDERS={6:week6,8:week8,9:week9,10:week10,11:week11,12:week12}
def revise_decks(decks):
 for d in decks:
  w=d['week'];cohort=d['cohort']
  if w<6:continue
  old=d['slides']
  if w in BUILDERS:
   end=next(i for i,s in enumerate(old) if s['title']=='Your issued task')
   retained=deepcopy(old[end:])
   for s in retained:
    if s['title']=='Revision and submission checklist':
     s['body']='Explain each cleaning or modelling decision using your pandas table and its outputs.\n\nKeep raw data unchanged. Restart and run all cells before submitting the required assignment notebook.'
   d['slides']=[deepcopy(old[0]),p('Today’s learning','Use pandas tables for this week’s data work. Explain the decisions and check the outputs.','Complete the issued function interfaces and written evidence using the demonstrated workflow.',note='Core practice precedes the assessment brief. Give the class one consistent data-handling approach: pandas for tables, scikit-learn for models, matplotlib for figures.')]+BUILDERS[w](old,cohort)+retained
  else:
   # Assessment and presentation weeks keep their existing procedures.
   new=[p('The continuing pandas workflow','Load CSV files with pd.read_csv. Keep raw data unchanged and use named columns throughout the investigation.','Use pandas for cleaning, summaries and model inputs. Return the published Python types at assessment function boundaries.',note='This is revision, not a new test requirement. Lists can name columns or hold returned predictions, but students do not need to rebuild table operations with manual CSV loops. Existing function signatures, marks and allowed-resource rules stay unchanged.')]
   if w in (7,14):
    old=[s for s in old if s['title']!='Practice before test day']
    new+=c('Pandas rehearsal before test day','''import pandas as pd
practice = pd.DataFrame({"group": ["A", "A", "B"],
                         "reading": [3, 5, 7]})
print(float(practice["reading"].mean()))
print(practice.groupby("group")["reading"].mean().to_dict())''','Overall mean: 5.0. Group means: A=4.0, B=7.0.','This rehearsal happens before the timed test. Check the local environment can import pandas without internet. Use only the released permitted resources during the assessment itself.')
   if w==13:
    old=[s for s in old if s['title'] not in ('Project handover in Python','Project handover results')]
    new+=[p('Relative data paths and saved outputs','pd.read_csv("data/raw/engineering_data.csv") reads a file relative to the notebook’s working folder. State that folder in the README.','clean.to_csv("cleaned_data.csv", index=False) exports a table without adding pandas row labels as a new column.',note='Explain data/raw as folders inside the project. A path starting with a private machine username will fail elsewhere. Keep raw data separate and never overwrite it with cleaned data.')]
   d['slides']=deepcopy(old[:3])+new+deepcopy(old[3:])
  for i,s in enumerate(d['slides'],1):
   s['sequence_number']=i
   # Remove stale old-number headings/transitions from retained notes.
   n=s.get('notes','')
   n=re.sub(r'CML311\d, Week \d+, slide \d+\s*','',n)
   n=re.sub(r'\n\nContinue to\n.*','',n,flags=re.S)
   n=re.sub(r'\n\nNEXT\n.*?(?=\n\n[A-Z]|$)','',n,flags=re.S)
   s['notes']=f'{cohort}, Week {w}, slide {i}: {s["title"]}\n\n'+n
  d['pandas_revision']='2026-10-15'
 return decks

if __name__=='__main__':
 import json
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]
 path=root/'data/iuea_deck_content.json'
 decks=json.loads(path.read_text())
 # Running directly is only for a source that has not yet received this overlay.
 if any(d.get('pandas_revision') for d in decks):raise SystemExit('Already revised; regenerate with prepare_beginner_ppt_content.py.')
 path.write_text(json.dumps(revise_decks(decks),indent=2)+'\n')
