"""Explain operations before code and attach slide-specific walkthroughs.

Rebuild order: prepare_beginner_ppt_content.py, verify_csv_examples.py,
build_beginner_pathway.py, then build/publish the validated PPTX edition.
Execution verification supplies actual outputs for every code continuation.
"""
import ast,json,re
from pathlib import Path
from pandas_continuity import p
ROOT=Path(__file__).resolve().parents[1]
# Each entry is visible to students before its first executable use in a deck.
OPS={
'alias':('Import and short names','import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.'),
'read_csv':('Reading a CSV','pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.'),
'head':('A preview of rows','table.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.'),
'shape':('Counting dimensions','table.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.'),
'dtypes':('Column data types','table.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.'),
'select':('Selecting columns','table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.'),
'mask':('Selecting rows with a mask','A column comparison produces one True or False per row. table[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.'),
'assign':('Adding or replacing a column','table["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.'),
'arithmetic':('Column arithmetic','Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.'),
'chain':('Reading chained operations','Read a chain from left to right. In table["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.'),
'mean':('Mean of recorded values','series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.'),
'sum':('Adding values and counting True','series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. table.isna().sum() therefore counts missing cells separately for each column.'),
'groupby':('Grouping rows','table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.'),
'nunique':('Counting distinct labels','series.nunique() counts different recorded values, ignoring missing values by default. It counts categories rather than rows.'),
'idxmax':('Label of the largest value','series.idxmax() returns the label attached to the largest value. It does not return that value. If several entries tie, it returns the first such label.'),
'copy':('A separate working table','table.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.'),
'isna':('Finding missing cells','isna() returns True for missing entries such as NaN and None. It returns False for a recorded zero. A DataFrame gives a mask for every cell; a Series gives one mask value per row.'),
'notna':('Finding recorded cells','notna() returns True where a value is present. Use it to retain observations with a recorded target before modelling.'),
'duplicated':('Marking repeated observations','table.duplicated("record_id") marks later rows with an already-seen record_id. The first occurrence is False. Repeated equipment IDs alone do not mean duplicate observations.'),
'drop_duplicates':('Keeping the first observation','table.drop_duplicates("record_id") returns rows with the first occurrence of each ID, preserving their order. It does not overwrite the source unless you assign the result.'),
'between':('An inclusive range','series.between(0, 100) is True for values from 0 through 100, including both limits. The resulting mask helps select valid rows.'),
'median':('Middle recorded value','series.median() sorts known values conceptually and returns the middle one. With an even count, it averages the two middle values. Missing entries do not enter the calculation.'),
'fillna':('Replacing missing entries','series.fillna(value) returns a column whose missing entries contain value. Recorded values stay unchanged. Assign the returned column to retain the fill.'),
 'to_numeric':('Converting numeric text','pd.to_numeric(column, errors="coerce") converts numeric values or text. Unparseable text becomes missing. Compare original and converted values so existing gaps are not counted as conversion failures.'),
'agg':('Several summaries at once','series.agg(["mean", "min", "max"]) applies those three named calculations and returns a labelled Series of results. min and max give the lowest and highest recorded values.'),
'round':('Rounded display','series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.'),
'scatter':('Scatter plot from columns','table.plot.scatter(x="load_pct", y="target", ax=ax) plots one point per row using those two columns. ax selects the plotting area. Rows with missing plot coordinates cannot form complete points.'),
'bar':('A bar for each labelled value','series.plot.bar(ax=ax) draws a bar for each Series label. When the Series contains group means, bar heights represent those means.'),
'hist':('Histogram intervals','series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.'),
'DataFrame':('A table from Python values','pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.'),
'Series':('A labelled column','pd.Series(values) creates a one-dimensional labelled sequence. With an array of fold errors, the default labels are 0, 1, 2 and so on.'),
 'to_dict':('Returning a dictionary','series.to_dict() maps Series labels to values. table.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.'),
'isin':('Membership in a group list','series.isin(["E1", "E2"]) returns True for entries matching either listed label. table[that_mask] keeps all observations belonging to those groups.'),
 'tolist':('Returning plain values','series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and predictions.'),
'abs':('Magnitude of each error','series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.'),
'get_dummies':('Category indicator columns','pd.get_dummies(column, prefix="class", dtype=int) creates a 0/1 column per category. prefix names the columns, such as class_0 and class_1. dtype=int displays integers.'),
 'std':('Spread of fold errors','series.std(ddof=0) measures how far values spread around their mean. ddof=0 divides squared deviations by the number of values. This describes these folds, not a confidence interval.'),
'sort_values':('Sorting by several columns','table.sort_values(["validation_mae", "latency_ms", "name"]) sorts ascending by error first. Equal errors use latency, then alphabetical name as tie-breaks.'),
'empty':('Checking for no rows','table.empty is True when the filtered table has no entries. Check it before attempting to select a first row. empty is a property, without parentheses.'),
'iloc':('Selecting by row position','table.iloc[0] selects the first row by its position, not its label. ["name"] then selects that row’s name field. An empty table has no row at position zero.')}

def operations(program):
 tree=ast.parse(program);found=[]
 def add(k):
  if k not in found:found.append(k)
 for n in ast.walk(tree):
  if isinstance(n,ast.Import) and any(a.name=='pandas' for a in n.names):add('alias')
  if isinstance(n,ast.Attribute):
   if n.attr in OPS:add(n.attr)
   elif n.attr not in {'plot','fit','predict','subplots','set_xlabel','set_ylabel','set_title','show'}:
    raise ValueError('Operation needs a prerequisite explanation: '+n.attr)
  if isinstance(n,ast.Subscript):
   add('select')
   if isinstance(n.slice,(ast.Name,ast.Compare,ast.BoolOp,ast.BinOp,ast.Call)):add('mask')
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) for t in n.targets):add('assign')
  if isinstance(n,ast.BinOp) and not isinstance(n.op,ast.BitAnd):add('arithmetic')
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='round':add('round')
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,(ast.Call,ast.Subscript)):add('chain')
 return found

# Context attached to named intermediate results rather than generic lecturer cues.
ASSIGN={
'raw':'Read the supplied file into raw. Its rows remain the untouched source for this lesson.',
'mask':'Compare each kwh reading with 5000. Store the resulting True/False decisions without changing the readings.',
 'totals':'Group all source rows by building and add each group’s recorded energy.',
'priced':'Select positive energy readings and copy them before calculating a unit rate.',
'duplicates':'Mark every repeated record_id after its first appearance. This mask identifies observations, not equipment groups.',
'clean':'Apply this cleaning step to the current working table. Deduplicate first, filter invalid rows next, then fill missing ambient values.',
'known':'Mark rows whose target is recorded. A missing target cannot serve as an observed training answer.',
'in_range':'Mark loads in the inclusive 0–100 range.',
'fill':'Calculate the median only after the earlier cleaning steps. Its unit is degrees Celsius.',
'numbers':'Attempt conversion of ambient_c. Invalid numeric text becomes missing because errors="coerce".',
'failed':'Mark entries that were originally present but became missing during conversion. Exclude pre-existing gaps from this failure count.',
'means':'Calculate the mean target separately for each equipment ID from the cleaned rows.',
'records':'Convert the source table to row dictionaries for the function call. This step changes the representation, not the measured values.',
 'table':'Build a DataFrame from the function’s input records. A different caller can supply different observations.',
'result':'Group the function’s rows by equipment and calculate each mean load.',
'data':'Apply the displayed preparation step while retaining the observation identifiers and source ordering.',
'valid':'Require a recorded target and a load between 0 and 100. Both masks must be True.',
 'train':'Keep equipment E1–E4 together in the training partition.',
 'validation':'Keep equipment E5 in validation. Its targets evaluate predictions and never fit the model.',
 'test':'Reserve equipment E6 for the final test. Do not inspect its target scores while choosing a model.',
 'features':'Store the input column names in the order used for fitting and prediction.',
 'model':'Create a pipeline containing a training-median imputer and a linear regression model. It has not learned from observations until fit is called.',
 'predictions':'Predict the validation rows using the fitted training pipeline. The returned array follows validation row order.',
 'baseline':'Create the comparator that predicts the training target mean for every observation.',
 'tree':'Create a median-imputation pipeline with a depth-four tree and fixed random seed.',
 'results':'Copy each validation record_id and target so the predictions can be traced to their source observation.',
 'residual':'Subtract each prediction from its paired actual target. Negative residuals mean an overprediction.',
 'mae':'Take each residual’s absolute value, then average. This is a typical error magnitude in the target unit.',
 'rmse':'Square the residuals, average, then take the square root. Large errors receive more weight than in MAE.',
 'a':'Select the actual reference labels. A value of 1 identifies a true warning case.',
 'pred':'Select the predicted labels from the same rows and in the same order.',
 'tp':'Count rows where actual=1 and predicted=1: correctly raised warnings.',
 'fn':'Count rows where actual=1 and predicted=0: missed warnings.',
 'fp':'Count rows where actual=0 and predicted=1: false alarms.',
 'tn':'Count rows where actual=0 and predicted=0: correctly silent cases.',
 'precision':'Start at zero, or inside the guarded branch divide true positives by all predicted positives.',
 'recall':'Start at zero, or inside the guarded branch divide true positives by all actual positives.',
 'cost':'Multiply missed warnings by five and add false alarms under the stated teaching cost rule.',
 'indicators':'Create one 0/1 column per predicted category. These are a representation example, not new model input features.',
 'actual':'Convert actual labels to a plain list for the published function interface.',
 'predicted':'Convert predicted labels to a plain list in the same row order.',
 'training_median':'Calculate the ambient median from training rows only.',
 'filled':'Fill validation gaps with the training median. A validation value never contributes to that median.',
 'cv':'Create four validation folds that keep equipment groups together.',
 'scores':'Run the model pipeline separately in each training fold. The scorer returns negative MAE, so a larger score means a smaller error.',
 'fold_errors':'Negate the scores to obtain positive errors, then place them in a pandas Series.',
 'out':'Copy the function input so derived columns do not alter its source.',
 'train_x':'Apply the feature function to the training rows.',
 'valid_x':'Apply the identical feature function to validation rows.',
 'base_cols':'Name the two original features: load and ambient temperature.',
 'extra_cols':'Append the interaction column name to the base feature list.',
 'base':'Create a fresh median-imputation and linear regression pipeline for the base features.',
 'extra':'Create a separate pipeline for the extended feature set.',
 'base_pred':'Predict the same validation observations using the base model.',
 'extra_pred':'Predict those validation observations using the extended model.',
 'base_mae':'Compare base predictions with their actual validation targets using MAE.',
 'extra_mae':'Compare extended predictions with the same targets using MAE.',
 'start':'Read the clock immediately before the timed prediction call.',
 'latency_ms':'Subtract the start time, convert seconds to milliseconds and divide by the number of validation observations. This is a batch average per observation.',
 'candidates':'Create a candidate table from the model name, calculated validation MAE and measured latency. The evidence comes from the supplied CSV and this computer.',
 'eligible':'Keep only candidates meeting both inclusive practice limits. The limits are stated requirements, not measured observations.',
 'ordered':'Rank eligible candidates by error, then latency, then name.',
 'winner':'Return None for no eligible rows, otherwise take the first sorted row’s name.'}

PRINT={
'raw.head()':'The first five observations and their column headings. Read one whole row aloud before discussing a column.',
'raw.shape':'The pair is row count followed by column count.',
'raw.dtypes':'Read each heading beside its stored type. float64 can include missing numerical entries.',
'raw.isna().sum()':'Each number counts missing cells in that named column, not rows with any missing cell.',
'clean.isna().sum()':'Check which gaps remain after cleaning. Zero means no missing cells in that column.',
'raw[duplicates].head()':'These are the later copies marked as duplicates, not all rows from repeated equipment.',
'raw[failed].head()':'An empty table means this supplied column had no conversion failures.',
 'len(raw)':'Read original row count, cleaned row count, then ambient fill in degrees Celsius.',
 'len(train)':'The three numbers are training, validation and final-test row counts, in that order.',
 'tp':'Read counts as true positives, false negatives, false positives, then true negatives.',
 'tp + fn + fp + tn':'The sum of the four categories should equal the number of CSV rows.',
 'len(actual)':'The two counts should match because the columns describe paired outcomes.',
 'winner':'Read the chosen name, or None if the measured candidate fails a requirement.',
 'candidates':'Read model name, validation MAE and measured milliseconds per observation. Timing will vary between runs.',
 'base_mae - extra_mae':'A positive number favours the extra feature. A negative number means its validation MAE increased.',
 'round(base_mae - extra_mae, 4)':'A positive number favours the extra feature. A negative number means its validation MAE increased.'}

def statement_note(n):
 src=ast.unparse(n)
 if isinstance(n,(ast.Import,ast.ImportFrom)):
  return 'Load '+', '.join(a.name for a in n.names)+(' from '+n.module if isinstance(n,ast.ImportFrom) else '')+'. An import makes these names available; it does not run the analysis.'
 if isinstance(n,ast.FunctionDef):return 'Define '+n.name+' with the displayed input. Its indented body runs only when the function is called.'
 if isinstance(n,ast.Assign):
  target=n.targets[0]
  if isinstance(target,ast.Name) and target.id in ('clean','data'):
   if 'drop_duplicates' in src:return 'Keep the first row for each record_id, preserving source order, then copy the retained rows into '+target.id+'. Later copies cannot replace an invalid first occurrence.'
   if 'known & in_range' in src:return 'Keep only rows whose known-target and valid-load masks are both True. Copy the selected rows back into clean.'
   if 'data[valid]' in src:return 'Keep only rows marked True by valid, then copy them back into data. The raw source remains unchanged.'
  if isinstance(target,ast.Subscript):
   key=ast.unparse(target.slice)
   meanings={'rate_ugx_per_kwh':'Divide each recorded cost by its paired positive energy reading. The new column has units UGX/kWh.','ambient_c':'Replace only missing ambient values with the calculated fill. Other readings remain unchanged.','predicted':'Attach predictions to the validation rows in their original order.','load_fraction':'Divide percentage load by 100 to express it as a fraction.','load_ambient':'Multiply paired load and ambient values. This derived interaction has combined units.'}
   return meanings.get(key.strip("'\""),'Assign the calculated values to '+ast.unparse(target)+'.')
  if isinstance(target,ast.Tuple):return 'Create a new Figure and Axes. The first name stores the whole figure and the second stores its plotting area.'
  name=ast.unparse(target)
  if name not in ASSIGN:raise ValueError('Missing assignment explanation: '+name)
  return ASSIGN[name]
 if isinstance(n,ast.Return):return 'Return '+ast.unparse(n.value)+' to the caller. return supplies the function result; print would only display it.'
 if isinstance(n,ast.If):return 'Check '+ast.unparse(n.test)+'. Execute the indented branch only if this is True. This prevents an invalid division or access to a missing row.'
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
  call=n.value;f=ast.unparse(call.func)
  if f=='print':
   key=ast.unparse(call.args[0]) if call.args else ''
   return 'Display '+', '.join(ast.unparse(a) for a in call.args)+'. '+PRINT.get(key,'Read these values alongside their source column labels. The display does not change the calculation or source data.')
  if f=='baseline.fit':return 'Calculate and store the mean of the supplied training targets. This DummyRegressor has no imputer and does not learn a feature-dependent relationship.'
  if f.endswith('.fit'):return 'Fit '+f.rsplit('.',1)[0]+' using the specified training features and targets. Its imputer learns only from those training features.'
  if f.endswith('.predict'):return 'Run prediction with the already fitted model. This call is timed but does not refit the model.'
  if '.plot.scatter' in f:return 'Plot each retained load and target pair. One point represents one observation.'
  if '.plot.bar' in f:return 'Draw one bar per equipment group using the calculated mean target.'
  if '.plot.hist' in f:return 'Count retained target values in ten intervals and draw those counts.'
  if '.set_' in f:return 'Label this plotting axis or title with '+ast.unparse(call.args[0])+'. Include the quantity and unit so the chart can be interpreted.'
  if f=='plt.show':return 'Display the completed figures. The figure objects still exist for later use.'
 raise ValueError('Missing statement explanation: '+src)

def walkthrough(program,start,end):
 tree=ast.parse(program);items=[]
 for n in sorted((n for n in ast.walk(tree) if isinstance(n,ast.stmt)),key=lambda n:(n.lineno,n.col_offset)):
  if n.lineno<=end and (n.end_lineno>=start):
   if isinstance(n,(ast.FunctionDef,ast.If)) and n.lineno<start:continue
   snippet=program.splitlines()[n.lineno-1].strip()
   items.append(f'Line {n.lineno}: {snippet}\n{statement_note(n)}')
 return '\n\n'.join(items)

INTERPRET={
'Loading the supplied observations':'The preview establishes the file schema. The row/column pair describes the full file, while head shows only five rows. Explain that NaN means a missing entry, not a measured zero.',
'Energy values and their mean':'The displayed mean covers the entire kwh column, not just the five previewed readings. Its unit is kWh per recorded meter-month.',
'Readings above the stated threshold':'The final count covers all readings above 5,000 kWh. The displayed subset is only the first five matches.',
'Building totals from campus_energy.csv':'The labelled totals add energy over the recorded months. The distinct-label count is the number of buildings, and the final name identifies the largest total.',
'Rates from recorded cost and energy':'For any displayed row, divide cost_ugx by kwh to reproduce the rate. Compare rates only where energy is positive.',
'Inspecting gaps and repeated IDs':'The first output counts gaps per column. The next number counts later duplicate record IDs. The final table locates those duplicate rows for inspection.',
'Cleaning the supplied observations':'Read the first three values as original row count, retained row count and the ambient fill in degrees Celsius. The final counts check remaining gaps after the ordered cleaning steps.',
'Conversion check on the supplied ambient column':'A zero count and empty table are a valid result: no recorded value failed conversion. They do not mean the original column had no missing entries.',
'Summaries of the cleaned CSV':'The first output gives overall mean, minimum and maximum target. The second gives a mean for each equipment group. Group means need not average to the overall mean unless group sizes are equal.',
'Load and target in the supplied CSV':'Read x as percentage load and y as the cohort target. Describe the observed association. This scatter alone does not prove that changing load causes the target change.',
'Equipment means and target distribution':'The first figure compares group means in the target unit. The histogram counts observations in target intervals. These answer different questions.',
'A function called with the supplied records':'Each dictionary key is an equipment ID and its value is mean load_pct. This example summarises raw records, including any invalid raw loads. It demonstrates a function boundary, not the cleaned-data summary required elsewhere.',
'Pandas rehearsal using the supplied CSV':'The first number is the raw overall target mean. The labelled values are raw equipment means. pandas skips missing targets; this rehearsal does not perform the Week 6 cleaning policy.',
'Preparing the supplied modelling rows':'Read the three counts in training, validation, test order. Check that each equipment ID belongs to one partition only. The sum equals the retained modelling-row count.',
'Training and predicting on the supplied data':'Each printed value predicts the target for the corresponding first validation row. Compare with those rows’ actual targets, keeping their order. A plausible-looking prediction is not evidence of low error.',
'Baseline and tree on the same CSV rows':'The first list repeats the training target mean. The second contains tree predictions for the same validation rows. Compare errors on those same rows rather than choosing whichever list looks more varied.',
'Errors from the supplied validation observations':'Use record_id to locate a source row. Subtract predicted from target to reproduce its residual. The final pair is MAE followed by RMSE, in the cohort target unit.',
'Confusion counts from classification_case.csv':'For the supplied six pairs, the counts are TP=3, FN=1, FP=1 and TN=1. Their sum is six, matching the file. Locate each missed warning and false alarm in the original rows.',
'Metrics from the supplied outcomes':'Precision is 3/(3+1)=0.75 and recall is 3/(3+1)=0.75. Cost is 5×1+1=6. The cost units are hypothetical penalties, not currency or physical units.',
'Indicators from the supplied class labels':'A row with predicted=0 has class_0=1 and class_1=0. A predicted=1 row reverses those indicators. The final two counts confirm that actual and predicted lists are paired.',
'Training median from the actual ambient readings':'The first value is the training ambient median. The next is the number of validation gaps. If that count is zero, fillna leaves the validation readings unchanged.',
'Fold errors calculated from the supplied training rows':'Read the list as four fold MAEs, then the mean MAE and the population standard deviation of those fold errors. Variation across folds describes this evaluation; it is not a confidence interval.',
'Features from the supplied load and ambient columns':'Check a displayed load fraction by dividing its percentage by 100. Check load_ambient by multiplying the source load and ambient temperature for that same record. Missing inputs propagate until the fitted imputer handles them.',
'Paired ablation using the supplied CSV':'Read the first pair as base MAE then extended MAE. The final number is base minus extended. Here the sign determines whether adding the interaction helped on these validation observations. Do not claim improvement if the result is negative.',
'A measured candidate from the supplied validation data':'The row combines the actual validation MAE with a measured batch-average prediction time per observation. Timings vary by machine and run, so do not expect an exact match to the saved value.',
'Selection from the measured candidate table':'The name means the measured candidate passed both limits. None means no eligible row remained. With one candidate this tests eligibility, not superiority to other algorithms.'}

def revise(decks):
 for d in decks:
  if d['week']<5 or not d.get('csv_examples_revision') or d.get('pandas_explanations_revision'):continue
  seen=set();new=[];program='';base='';part=0
  for s in d['slides']:
   if s['kind']=='code':
    if s.get('practice_code'):
     program=s['practice_code'];base=re.sub(r' \(\d+/\d+\)$','',s['title']);part=0
     missing=[k for k in operations(program) if k not in seen]
     for j in range(0,len(missing),3):
      keys=missing[j:j+3]
      intro=p('Operations for the next example',*[OPS[k][0]+': '+OPS[k][1] for k in keys],note='\n\n'.join(OPS[k][0]+'\n'+OPS[k][1] for k in keys))
      intro['introduced_operations']=keys;intro['operation_prerequisite']=True;new.append(intro)
     seen.update(missing)
    else:part+=1
    original=s['notes'].split('\n\nOutput from the supplied CSV')[0]
    output=s['notes'].split('\n\nOutput from the supplied CSV (this cohort):\n',1)
    # Continuation slides receive the same verified output and their own code steps.
    result=next((x.get('notes','').split('\n\nOutput from the supplied CSV (this cohort):\n',1)[1] for x in d['slides'] if x.get('practice_code')==program and '\n\nOutput from the supplied CSV (this cohort):\n' in x.get('notes','')),'Run the example to display the current result.')
    unit={'CML3111':'motor winding temperature in degrees Celsius','CML3112':'building cooling load in kW','CML3113':'crusher energy demand in kWh/t'}[d['cohort']]
    s['notes']='Code walkthrough\n'+walkthrough(program,part*8+1,part*8+len(s['code'].splitlines()))+'\n\nReading the result\n'+INTERPRET[base]+('\nThis cohort’s engineering target is '+unit+'.' if d['week']>=6 and d['week']!=9 else '')+'\n\nOutput from the supplied CSV (this cohort):\n'+result+'\n\nFurther explanation\n'+re.sub(r'^CML311\d, Week \d+, slide \d+:.*?\n\n','',original,flags=re.S)
    s['explained_operations']=operations(program);s['walkthrough_revision']=True
   new.append(s)
  for i,s in enumerate(new,1):
   s['sequence_number']=i
   s['notes']=re.sub(r'^CML311\d, Week \d+, slide \d+:.*?\n\n','',s.get('notes',''),flags=re.S)
   s['notes']=f'{d["cohort"]}, Week {d["week"]}, slide {i}: {s["title"]}\n\n'+s['notes']
  d['slides']=new;d['pandas_explanations_revision']='2026-10-15'
 return decks
if __name__=='__main__':
 path=ROOT/'data/iuea_deck_content.json';path.write_text(json.dumps(revise(json.loads(path.read_text())),indent=2)+'\n')
