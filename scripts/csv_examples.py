"""Bind worked table examples to the CSV shipped with the cohort/week."""
from pathlib import Path
from copy import deepcopy
import json,re
from pandas_continuity import p,c
ROOT=Path(__file__).resolve().parents[1]

def code(title,src,note):
 return c(title,src,'Run this cell on the supplied CSV. Read the output below the cell.',note)

def opening(file='engineering_data.csv'):
 return [p('The supplied file','Extract this week’s student ZIP. Upload '+file+' into Colab using the Files panel, or keep it beside the notebook locally.','The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.',note='Uploading a notebook does not upload its data. Check the exact filename and column headings. Each cohort has its own data, so numerical results can differ.'),*code('Loading the supplied observations',f'import pandas as pd\nraw = pd.read_csv("{file}")\nprint(raw.head())\nprint(raw.shape)\nprint(raw.dtypes)','read_csv creates a DataFrame. head shows the first five rows. shape gives row and column counts. dtypes describes each column. raw remains unchanged throughout the lesson.')]

def bridge():
 return [p('Pandas inside the required function','The assignment caller supplies records. pd.DataFrame(records) gives those records named columns. Calculate with pandas, then return the published Python type.','to_dict("records") makes a list of row dictionaries. Series.tolist() makes a list of values. A grouped Series.to_dict() maps group labels to results.',note='Keep the original function names and return types. Do not read a fixed CSV inside the assessed function: hidden tests supply different records. The separate calling cell reads the CSV.'),*code('A function called with the supplied records','''def mean_load_by_equipment(records):
    table = pd.DataFrame(records)
    result = table.groupby("equipment_id")["load_pct"].mean()
    return result.to_dict()
records = raw.to_dict("records")
print(mean_load_by_equipment(records))''','groupby collects matching equipment labels. mean averages the recorded loads in each group. The function returns a dictionary. For assessed missing-value conversions use the supplied records_from_table helper.')]

def prep():
 return [p('Rows used for modelling','Keep the first occurrence of each record_id. Retain recorded targets and load_pct within 0–100. Then separate E1–E4 for training, E5 for validation and E6 for the final test.','Fill missing input values using training data only. Keep final-test targets out of model selection.',note='This follows the issued data rules. Filtering observed targets is different from estimating missing targets. Deduplicate before filtering, so an invalid first occurrence is not replaced by its later duplicate.'),*code('Preparing the supplied modelling rows','''data = raw.drop_duplicates("record_id").copy()
valid = data["target"].notna() & data["load_pct"].between(0, 100)
data = data[valid].copy()
train = data[data["equipment_id"].isin(["E1", "E2", "E3", "E4"])].copy()
validation = data[data["equipment_id"].isin(["E5"])].copy()
test = data[data["equipment_id"].isin(["E6"])].copy()
features = ["load_pct", "ambient_c"]
print(len(train), len(validation), len(test))''','duplicated IDs refer to observations, while equipment IDs repeat legitimately. isin tests membership in the supplied list. Each mask selects rows. copy gives each partition its own table. features names the two input columns.')]

def models():
 return [p('Training a model with missing inputs','train[features] selects the two input columns as a table. train["target"] selects the observed target as a Series.','SimpleImputer(strategy="median") learns input fill values from training rows. make_pipeline links that operation to LinearRegression. fit learns the steps and predict reuses them.',note='A model object exists before training. X is two-dimensional and y is one-dimensional. Select inputs in the same order during prediction. A validation target must never enter fit.'),*code('Training and predicting on the supplied data','''from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
model.fit(train[features], train["target"])
predictions = model.predict(validation[features])
print(predictions[:5].round(3).tolist())''','The printed list shows the first five validation predictions. [:5] selects up to five items. round changes display only. Keep full precision for grading. The pipeline fills any missing validation input with the training median.')]

def errors():
 return [p('Matching actual values and predictions','Every validation row has an actual target and its corresponding prediction. Subtract in the same order. abs() gives error magnitude.','MAE averages absolute errors. RMSE squares errors, averages them, then takes the square root. Both have the target’s unit.',note='RMSE reacts more strongly to large errors. Neither metric is a maximum guaranteed error. Pair by row order before calculation. R² is a separate regression measure and can be negative.'),*code('Errors from the supplied validation observations','''results = validation[["record_id", "target"]].copy()
results["predicted"] = predictions
residual = results["target"] - results["predicted"]
mae = residual.abs().mean()
rmse = (residual ** 2).mean() ** 0.5
print(results.head())
print(round(float(mae), 4), round(float(rmse), 4))''','Assignment answers retain full precision. The example rounds printed values to four decimal places. record_id lets the learner trace a prediction back to its CSV observation.')]

def teaching(w,old,cohort):
 unit={'CML3111':'degrees C','CML3112':'kW','CML3113':'kWh/t'}[cohort]
 pictures=lambda titles:[deepcopy(s) for s in old if s['title'] in titles]
 if w==6:
  return opening()+[p('Missing values and duplicate observations','isna() identifies missing cells. Zero is a recorded value. duplicated("record_id") marks later copies of an observation.','Repeated equipment_id values are expected. They identify the equipment that produced each observation.',note='Numeric blanks usually become NaN. Do not use value is None as the general pandas missing-value test. Count gaps and duplicated observation IDs directly from this week’s file.'),*code('Inspecting gaps and repeated IDs','''print(raw.isna().sum())
duplicates = raw.duplicated("record_id")
print(int(duplicates.sum()))
print(raw[duplicates].head())''','A mask has one True or False value per row. sum counts True values. raw[duplicates] displays the marked rows.')]+pictures(['A working copy preserves the original'])+[p('Cleaning order','Keep the first record_id occurrence. Next, retain rows with a known target and load_pct between 0 and 100 inclusive.','Calculate the ambient_c median from those retained rows. fillna replaces only missing ambient readings.',note='The median is the middle of sorted known values, or the average of the middle two. A later duplicate does not replace an invalid first occurrence. Keep raw unchanged. All-missing ambient data would need a stated fallback policy.'),*code('Cleaning the supplied observations','''clean = raw.drop_duplicates("record_id").copy()
known = clean["target"].notna()
in_range = clean["load_pct"].between(0, 100)
clean = clean[known & in_range].copy()
fill = clean["ambient_c"].median()
clean["ambient_c"] = clean["ambient_c"].fillna(fill)
print(len(raw), len(clean), round(float(fill), 3))
print(clean.isna().sum())''','& combines the two masks. Keep parentheses when combining comparisons directly. between includes both limits. The printed counts and median come from the actual file.'),p('Checking numeric conversion','pd.to_numeric converts values to numbers. errors="coerce" turns invalid numeric text into a missing value.','Compare before and after conversion. A file with no invalid text should report zero conversion failures.',note='Coercion does not repair a bad value. Inspect the original row before deciding what to do. Do not manufacture a failure in this week’s CSV.'),*code('Conversion check on the supplied ambient column','''numbers = pd.to_numeric(raw["ambient_c"], errors="coerce")
failed = raw["ambient_c"].notna() & numbers.isna()
print(int(failed.sum()))
print(raw[failed].head())''','This distinguishes failed conversions from missing cells already present in the file.'),p('Summaries and grouped results','mean, min and max summarise a numeric column. groupby collects records with the same equipment label before calculating.','The audit must inspect the supplied data for remaining defects, even when another function was meant to clean them.',note='A group mean describes observations in this file. It does not prove that equipment identity causes the difference.'),*code('Summaries of the cleaned CSV','''print(clean["target"].agg(["mean", "min", "max"]))
means = clean.groupby("equipment_id")["target"].mean()
print(means.round(3))''','agg applies each named summary. The target unit is '+unit+'.')]+pictures(['Choosing a chart for the question'])+[p('Charts and units','A scatter plot compares two numerical columns. A histogram counts observations in value intervals. A bar chart compares group summaries.','plt.subplots creates a Figure and plotting Axes. Use ax= to choose where pandas draws, then label each axis.',note='The scatter uses the supplied load_pct and target. Equipment grouping is categorical. Use ten histogram bins as required by the project.'),*code('Load and target in the supplied CSV',f'''import matplotlib.pyplot as plt
fig, ax = plt.subplots()
clean.plot.scatter(x="load_pct", y="target", ax=ax)
ax.set_xlabel("Load (%)")
ax.set_ylabel("Target ({unit})")
ax.set_title("Supplied observations after cleaning")
plt.show()''','Each point is one retained observation. Keep the raw CSV unchanged.'),*code('Equipment means and target distribution',f'''fig, ax = plt.subplots()
means.plot.bar(ax=ax)
ax.set_ylabel("Mean target ({unit})")
fig2, ax2 = plt.subplots()
clean["target"].plot.hist(bins=10, ax=ax2)
ax2.set_xlabel("Target ({unit})")
ax2.set_ylabel("Observation count")
plt.show()''','The bars show group means. The histogram shows counts, not means. Assessed chart functions return Figure objects.')]+bridge()
 if w==8:
  return opening()+prep()+pictures(['Fitting a line to observations'])+models()+[p('Baseline and tree comparisons','A mean baseline predicts the training target mean for every validation observation. A regression tree splits input space and predicts from training observations in each leaf.','Use the same training rows and validation rows for both. max_depth=4 limits tree depth and random_state=17 makes the example reproducible.',note='Both methods answer the same target question. The baseline provides a useful comparison. Tree predictions need not extrapolate a straight line.'),*code('Baseline and tree on the same CSV rows','''from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
baseline = DummyRegressor(strategy="mean")
baseline.fit(train[features], train["target"])
tree = make_pipeline(SimpleImputer(strategy="median"),
                     DecisionTreeRegressor(max_depth=4, random_state=17))
tree.fit(train[features], train["target"])
print(baseline.predict(validation[features])[:5].round(3).tolist())
print(tree.predict(validation[features])[:5].round(3).tolist())''','Compare the displayed predictions with the actual targets in the validation table. Training scores alone cannot establish performance on unseen equipment.')]+errors()+bridge()
 if w==9:
  return opening('classification_case.csv')+pictures(['Every paired result belongs in one cell'])+[p('Counting the supplied paired labels','actual holds the reference label. predicted holds the model decision. In this file, 1 means warning and 0 means no warning.','== compares values. & requires both conditions for each row. Parenthesise each comparison. sum counts the True results.',note='True positive: actual 1 and predicted 1. False negative: actual 1 and predicted 0. False positive: actual 0 and predicted 1. True negative: both 0. Keep the two columns paired.'),*code('Confusion counts from classification_case.csv','''a = raw["actual"]
pred = raw["predicted"]
tp = int(((a == 1) & (pred == 1)).sum())
fn = int(((a == 1) & (pred == 0)).sum())
fp = int(((a == 0) & (pred == 1)).sum())
tn = int(((a == 0) & (pred == 0)).sum())
print(tp, fn, fp, tn)
print(tp + fn + fp + tn, len(raw))''','The four counts must total the number of paired observations. This file contains binary labels.'),p('Precision recall and cost','Precision is TP divided by TP + FP. Recall is TP divided by TP + FN. The issued policy returns zero when a denominator is zero.','The teaching cost is five units per missed warning plus one per false alarm. Explain the assumption when interpreting the result.',note='Precision asks how many warnings were correct. Recall asks how many real warning cases were found. Neither alone shows all mistakes. The cost is not an approved safety limit.'),*code('Metrics from the supplied outcomes','''precision = 0.0
if tp + fp > 0:
    precision = tp / (tp + fp)
recall = 0.0
if tp + fn > 0:
    recall = tp / (tp + fn)
cost = 5 * fn + fp
print(round(precision, 4), round(recall, 4), cost)''','Round printed values only. The assessed function returns full-precision metrics in the required dictionary.'),p('Probabilities and thresholds','A probability is a model’s estimated chance of class 1. A threshold turns it into a class decision. Lowering the threshold generally raises more warnings.','classification_case.csv supplies decisions only. It has no probability column, so we cannot recompute threshold choices from this file.',note='A threshold at 0.5 labels probabilities at least 0.5 as positive. Do not treat existing 0/1 labels as original probability estimates. Threshold selection requires held-out probability predictions.'),p('Category indicators','get_dummies creates one indicator column per category. Each indicator is 1 for a matching row and 0 otherwise.','Here we can demonstrate indicators using the predicted class labels already present in the CSV.',note='This is a representation demonstration. Do not use predicted labels as model input features to predict those same labels. A multiclass metric needs a stated policy for every class.'),*code('Indicators from the supplied class labels','''indicators = pd.get_dummies(raw["predicted"], prefix="class", dtype=int)
print(indicators.head())
actual = raw["actual"].tolist()
predicted = raw["predicted"].tolist()
print(len(actual), len(predicted))''','dtype=int displays 0/1 indicators. tolist supplies the published classification_metrics input lists.')]
 if w==10:
  return opening()+pictures(['Three sets have different jobs'])+prep()+[p('Training-only filling','median ignores missing values. Calculate it from training input values and reuse it for validation gaps.','Do not calculate a new median from validation or test observations. A pipeline keeps this rule with the model.',note='Even preprocessing without target labels can leak information about evaluation distributions.'),*code('Training median from the actual ambient readings','''training_median = train["ambient_c"].median()
filled = validation["ambient_c"].fillna(training_median)
print(round(float(training_median), 3))
print(validation["ambient_c"].isna().sum())
print(filled.head())''','A zero missing count means this partition needs no fill. The code still uses the training-derived value if a gap exists.')]+models()+pictures(['Each fold takes a turn at validation'])+[p('Cross-validation within training data','GroupKFold keeps each equipment group within one fold. Each fold takes a turn as validation while the remaining folds train the pipeline.','cross_val_score reports one score per fold. neg_mean_absolute_error returns negative MAE, so negate the scores before reporting errors.',note='Use only the E1–E4 training partition here. E5 remains the separate validation partition and E6 the final test. The imputer is refitted within each training fold.'),*code('Fold errors calculated from the supplied training rows','''from sklearn.model_selection import GroupKFold, cross_val_score
cv = GroupKFold(n_splits=4)
scores = cross_val_score(model, train[features], train["target"],
                         groups=train["equipment_id"], cv=cv,
                         scoring="neg_mean_absolute_error")
fold_errors = pd.Series(-scores)
print(fold_errors.round(4).tolist())
print(round(float(fold_errors.mean()), 4))
print(round(float(fold_errors.std(ddof=0)), 4))''','std(ddof=0) describes the spread of these four fold errors. It is not a confidence interval. Compare folds rather than reporting only the best one.')]+bridge()
 if w==11:
  return opening()+prep()+pictures(['A physical relationship can form a feature'])+[p('Derived features from existing inputs','load_pct / 100 gives load_fraction. Multiplying load_pct by ambient_c gives the load_ambient interaction.','table["new_name"] = expression adds a column. Apply the same formulas to training and validation rows, without changing raw data.',note='An interaction has combined units. It is not a new measured physical quantity. Use information available at prediction time.'),*code('Features from the supplied load and ambient columns','''def add_features(table):
    out = table.copy()
    out["load_fraction"] = out["load_pct"] / 100
    out["load_ambient"] = out["load_pct"] * out["ambient_c"]
    return out
train_x = add_features(train)
valid_x = add_features(validation)
print(train_x[["load_pct", "load_fraction", "load_ambient"]].head())''','A missing ambient value produces a missing interaction. Fit the imputer on training features only.'),p('Ablation compares the same observations','Fit one linear model using load_pct and ambient_c. Fit a second using those columns plus load_ambient.','Compare both on the same validation targets. Improvement equals baseline MAE minus extended MAE.',note='A positive improvement means lower error for the extended model. The four-column make_features output also includes load_fraction, but the ablation comparison uses the three specified extended columns.'),*code('Paired ablation using the supplied CSV','''from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
base_cols = ["load_pct", "ambient_c"]
extra_cols = base_cols + ["load_ambient"]
base = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
extra = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
base.fit(train_x[base_cols], train["target"])
extra.fit(train_x[extra_cols], train["target"])
base_pred = base.predict(valid_x[base_cols])
base_mae = mean_absolute_error(validation["target"], base_pred)
extra_pred = extra.predict(valid_x[extra_cols])
extra_mae = mean_absolute_error(validation["target"], extra_pred)
print(round(base_mae, 4), round(extra_mae, 4))
print(round(base_mae - extra_mae, 4))''','The example reports the actual comparison even when the extra feature does not improve the score. Both models use identical training and evaluation rows. Keep full precision in returned metrics.')]+bridge()
 if w==12:
  return opening()+prep()+models()+errors()+[p('Candidate evidence and latency','The CSV supplies observations, not a table of model candidates or timings. Calculate validation MAE from its held-out observations.','Measure prediction time on this computer. Timing varies by machine and repeated run, so record the measurement conditions.',note='perf_counter reads a high-resolution clock. Elapsed seconds times 1000 gives milliseconds. This classroom timing is a demonstration, not a production benchmark.'),*code('A measured candidate from the supplied validation data','''from time import perf_counter
start = perf_counter()
model.predict(validation[features])
latency_ms = (perf_counter() - start) * 1000 / len(validation)
candidates = pd.DataFrame({"name": ["linear"],
    "validation_mae": [float(mae)], "latency_ms": [latency_ms]})
print(candidates)''','The timing is average milliseconds per observation in this batch. Repeat a benchmark under controlled conditions before making a deployment claim.'),p('Constraints and tie-breaks','For this classroom decision, use MAE at most 10 target units and mean latency at most 10 ms per observation. These are stated practice requirements.','Filter both limits inclusively. sort_values ranks eligible rows by validation_mae, then latency_ms, then name. empty detects no eligible rows.',note='These limits illustrate a decision rule, not an engineering safety standard. The assessment passes its own candidates and limits, which the function must use.'),*code('Selection from the measured candidate table','''eligible = candidates[(candidates["validation_mae"] <= 10) &
                      (candidates["latency_ms"] <= 10)]
ordered = eligible.sort_values(["validation_mae", "latency_ms", "name"])
if ordered.empty:
    winner = None
else:
    winner = ordered.iloc[0]["name"]
print(winner)''','iloc[0] selects the first row by position only after checking that it exists. A result of None is valid when no candidate meets both requirements.'),p('Interpreting the recommendation','State the data, split, metric, timing method and constraints. Report when the measured model fails a requirement.','Tune hyperparameters using validation or cross-validation. Preserve the final test until the choice is fixed.',note='One candidate demonstrates eligibility, not superiority over untested alternatives. A local explanation does not establish causation.')]+bridge()
 return []

def earlier(d):
 w=d['week'];old=d['slides']
 end=next(i for i,s in enumerate(old) if s['title'] in ('Your issued task','Your issued assignment'))
 if w==5:
  concepts=[p('DataFrame and column names','A DataFrame is a table with named columns. campus_energy.csv contains meter_id, building, block, month, kwh and cost_ugx.','One row records a meter reading for a month. kwh measures energy and cost_ugx gives the cost in Uganda shillings.',note='Explain each field before indexing. This file provides the observations for every calculation in the lesson.')]
  content=concepts+opening('campus_energy.csv')+[p('Selecting and summarising a column','raw["kwh"] selects the energy column as a Series. mean() averages its known values.','Square brackets select a named column. Parentheses call a method such as mean().',note='The mean describes readings in this supplied file, not a general expected monthly use.'),*code('Energy values and their mean','print(raw["kwh"].head())\nprint(round(float(raw["kwh"].mean()), 3))','head shows the first five readings. The mean uses the entire column.'),p('Filtering rows with a mask','A comparison on a column produces one True or False for every row. raw[mask] retains the True rows.','Here the example asks which readings exceed 5,000 kWh. This threshold is a question for practice.',note='Explain the comparison before running it. A high reading is not automatically an error.'),*code('Readings above the stated threshold','mask = raw["kwh"] > 5000\nprint(raw[mask].head())\nprint(int(mask.sum()))','The count covers the whole supplied file. The preview shows only the first five matching rows.'),p('Groups and labels','groupby("building") gathers rows with the same building label. Selecting kwh and calling sum adds their energy.','nunique counts distinct building labels. idxmax returns the label whose total is largest.',note='The maximum is a building label, not a row number. Group totals cover the months present in the CSV.'),*code('Building totals from campus_energy.csv','totals = raw.groupby("building")["kwh"].sum()\nprint(totals)\nprint(raw["building"].nunique())\nprint(totals.idxmax())','Trace one building back to its source rows. pandas performs the grouping and addition.'),p('A calculated energy rate','Cost divided by energy gives UGX per kWh. First check that the denominator is positive.','copy preserves raw. Assigning table["new_name"] adds a calculated column.',note='A zero denominator cannot define a unit rate. Filtering here is for this rate demonstration, not an instruction to delete the original observation.'),*code('Rates from recorded cost and energy','priced = raw[raw["kwh"] > 0].copy()\npriced["rate_ugx_per_kwh"] = priced["cost_ugx"] / priced["kwh"]\nprint(priced[["building", "kwh", "cost_ugx", "rate_ugx_per_kwh"]].head())','The two columns come from the same source row. Double brackets select a list of columns in the requested display order.')]
  return old[:2]+content+old[end:]
 # Fundamentals before file access remain small explicit syntax examples.
 start=next(i for i,s in enumerate(old) if s['title']=='Open a real CSV and inspect its first row')
 numeric,group={'CML3111':('winding_temp_c','motor_id'),'CML3112':('crack_width_mm','structure_id'),'CML3113':('rate_of_penetration','bit_type')}[d['cohort']]
 content=[old[start],p('Numbers read from CSV','DictReader reads each row as a dictionary. CSV field values start as text. float converts a recorded numeric field to a number.','Check for an empty string before converting a blank cell.',note='Use the real header shown in the previous example. The list rows already contains the supplied file records.'),*code('Recorded values from the supplied rows',f'values = []\nfor row in rows:\n    text = row["{numeric}"]\n    if text != "":\n        values.append(float(text))\nprint(len(values))\nprint(values[:5])','Each retained number comes directly from a CSV row. [:5] previews up to five entries.'),p('One summary for each group','Keep a totals dictionary and a counts dictionary. Initialise a new group before adding its first reading.','Add the recorded value and increment its count. Divide each total by its count to obtain the group mean.',note='Every retained row contributes once. Use the actual group and measurement names in this cohort’s CSV.'),*code('Grouped means from the supplied rows',f'totals = {{}}\ncounts = {{}}\nfor row in rows:\n    group = row["{group}"]\n    if row["{numeric}"] != "":\n        value = float(row["{numeric}"])\n        totals[group] = totals.get(group, 0) + value\n        counts[group] = counts.get(group, 0) + 1\nmeans = {{}}\nfor group in totals:\n    means[group] = totals[group] / counts[group]\nprint(means)','get(group, 0) returns the existing value or zero for a new group. The measurement and grouping labels match the supplied CSV.')]
 return old[:start]+content+old[end:]

def revise(decks):
 for d in decks:
  w=d['week'];old=d['slides']
  if d.get('csv_examples_revision'):continue
  if w in (4,5):
   d['slides']=earlier(d)
  elif w in (6,8,9,10,11,12):
   end=next(i for i,s in enumerate(old) if s['title']=='Your issued task')
   d['slides']=old[:2]+teaching(w,old,d['cohort'])+old[end:]
  elif w in (7,14):
   new=[]
   for s in old:
    if s['title']=='Pandas rehearsal before test day':
     new+=code('Pandas rehearsal using the supplied CSV','''import pandas as pd
raw = pd.read_csv("engineering_data.csv")
print(raw["target"].mean())
print(raw.groupby("equipment_id")["target"].mean())''','Use the previous teaching week’s engineering_data.csv for this pre-test rehearsal. This does not grant access to the test dataset before the assessment. During the test, follow its permitted-resource rules.')
    else:new.append(s)
   d['slides']=new
  else:continue
  for i,s in enumerate(d['slides'],1):
   s['sequence_number']=i
   s['notes']=re.sub(r'^CML311\d, Week \d+, slide \d+:.*?\n\n','',s.get('notes',''),flags=re.S)
   s['notes']=f'{d["cohort"]}, Week {w}, slide {i}: {s["title"]}\n\n'+s['notes']
  d['csv_examples_revision']='2026-10-15'
 return decks

if __name__=='__main__':
 path=ROOT/'data/iuea_deck_content.json'
 path.write_text(json.dumps(revise(json.loads(path.read_text())),indent=2)+'\n')
