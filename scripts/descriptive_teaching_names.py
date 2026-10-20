"""Descriptive teaching names and prerequisite explanations, Weeks 8–15.
Preserves CSV columns, library keyword arguments and assessed interfaces.
"""
import ast,copy,json,re,sys
from pathlib import Path
import black
from pandas_explanations import OPS
ROOT=Path(__file__).resolve().parents[1]
NAMES={'raw':'raw_data','data':'modelling_data','train':'training_data','validation':'validation_data','test':'test_data','features':'feature_columns','model':'linear_model','predictions':'validation_predictions','baseline':'baseline_model','tree':'tree_model','results':'validation_results','residual':'prediction_errors','mae':'mean_absolute_error_value','rmse':'root_mean_squared_error','records':'equipment_records','table':'equipment_data','result':'mean_load_by_equipment_group','a':'actual_labels','pred':'predicted_labels','tp':'true_positive_count','fn':'false_negative_count','fp':'false_positive_count','tn':'true_negative_count','cost':'total_error_cost','indicators':'class_indicator_columns','actual':'actual_values','predicted':'predicted_values','training_median':'training_ambient_median','filled':'filled_validation_ambient','cv':'grouped_folds','scores':'negative_error_scores','fold_errors':'fold_absolute_errors','train_x':'training_features','valid_x':'validation_features','out':'extended_data','base_cols':'base_feature_columns','extra_cols':'extended_feature_columns','base':'base_pipeline','extra':'extended_pipeline','base_pred':'base_predictions','extra_pred':'extended_predictions','base_mae':'base_absolute_error','extra_mae':'extended_absolute_error','start':'prediction_start_time','latency_ms':'prediction_time_ms','candidates':'candidate_models','eligible':'eligible_models','ordered':'ranked_models','winner':'selected_model_name','filename':'practice_filename','source':'practice_data','mean_target':'training_target_mean','errors':'baseline_errors','linear':'linear_pipeline','linear_pred':'linear_predictions','tree_pred':'tree_predictions','readings':'reading_values'}
MEANINGS={
'raw_data':'original CSV table; keep it unchanged so the analysis can be checked',
'modelling_data':'copied observations after duplicate and validity checks',
'valid_row_mask':'True for rows with a recorded target and a load from 0 through 100',
'training_data':'rows used to learn model settings; only these rows may determine imputation values',
'validation_data':'separate rows used to compare models without fitting on them',
'test_data':'held-out rows kept aside until the final evaluation',
'feature_columns':'the list of input column names supplied to the model',
'linear_model':'the linear regression estimator or imputation-and-regression pipeline',
'validation_predictions':'one predicted target for each validation row, in the same order',
'baseline_model':'a simple reference predictor which always predicts the training target mean',
'tree_model':'the tree regression pipeline being compared on the same validation rows',
'validation_results':'actual and predicted targets paired with each record ID',
'prediction_errors':'actual targets minus predictions; signs indicate under- or over-prediction',
'mean_absolute_error_value':'average absolute prediction error, in the target unit',
'root_mean_squared_error':'square root of the mean squared prediction error, in the target unit',
'actual_labels':'the recorded class of each observation: 1 means positive and 0 means negative',
'predicted_labels':'the model’s 0/1 class decisions in matching row order',
'true_positive_count':'number of rows with actual 1 and predicted 1',
'false_negative_count':'number of missed positives: actual 1 but predicted 0',
'false_positive_count':'number of false alarms: actual 0 but predicted 1',
'true_negative_count':'number of rows with actual 0 and predicted 0',
'precision':'fraction of positive predictions that are correct',
'recall':'fraction of actual positives detected by the model',
'total_error_cost':'five penalty units per missed positive plus one per false alarm in this scenario',
'class_indicator_columns':'one integer 0/1 column for each predicted class',
'actual_values':'observed targets or labels in the order used for comparison',
'predicted_values':'predictions aligned with those actual values',
'training_ambient_median':'median ambient temperature calculated only from training rows',
'filled_validation_ambient':'validation ambient column with gaps filled using the training median',
'grouped_folds':'the split rule that keeps observations from one equipment group together',
'negative_error_scores':'negative mean absolute errors returned by scikit-learn’s scoring convention',
'fold_absolute_errors':'positive mean absolute error for each validation fold',
'training_features':'training table containing the engineered feature columns',
'validation_features':'validation table with the same feature calculations applied',
'extended_data':'a copy with additional derived columns; the input table is preserved',
'base_feature_columns':'input columns for the simpler comparison pipeline',
'extended_feature_columns':'base columns plus the interaction feature being tested',
'base_pipeline':'imputer and regression model using only the base columns',
'extended_pipeline':'a separate imputer and regression model using the extended columns',
'base_predictions':'validation predictions from the base pipeline',
'extended_predictions':'validation predictions from the extended pipeline',
'base_absolute_error':'validation mean absolute error for the base pipeline',
'extended_absolute_error':'validation mean absolute error for the extended pipeline',
'prediction_start_time':'timer reading immediately before predicting the batch',
'prediction_time_ms':'measured batch time in milliseconds divided by validation-row count',
'candidate_models':'table of model names, measured validation errors and prediction times',
'eligible_models':'candidates satisfying both stated limits',
'ranked_models':'eligible candidates sorted by error, time and name, in that order',
'selected_model_name':'name of the first eligible ranked model, or None if none qualify',
'practice_filename':'the exact name of the accompanying revision CSV',
'practice_data':'the small practice table read from that CSV',
'training_target_mean':'mean target calculated from training rows only',
'baseline_predictions':'the training mean repeated once per validation observation',
'baseline_errors':'observed validation targets minus baseline predictions',
'linear_pipeline':'median imputer followed by linear regression',
'linear_predictions':'validation predictions from the linear pipeline',
'tree_predictions':'validation predictions from the tree pipeline',
'reading_values':'the supplied readings represented as a pandas Series',
'equipment_records':'the input list of row dictionaries supplied to the function',
'equipment_data':'the same function input represented as a DataFrame',
'mean_load_by_equipment_group':'mean load for each equipment ID; returned as a dictionary'}
MORE={
'SimpleImputer':('Filling model inputs','SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.'),
'make_pipeline':('A sequence of model steps','make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.'),
'LinearRegression':('Creating linear regression','LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.'),
'fit':('Learning from training examples','model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.'),
'predict':('Predicting new targets','model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.'),
'DummyRegressor':('A training-mean baseline','DummyRegressor(strategy="mean") learns the mean training target during fit. It predicts that same value for every new row. Compare a more complex model against this simple baseline.'),
'DecisionTreeRegressor':('Creating a regression tree','DecisionTreeRegressor splits inputs into regions with different predicted values. max_depth limits the number of split levels. random_state fixes random choices so the example can be repeated.'),
'GroupKFold':('Keeping groups together','GroupKFold(n_splits=4) creates four train/validation splits. All rows of an equipment group stay on one side of each split. Four splits require at least four distinct training groups.'),
'cross_val_score':('Scoring repeated splits','cross_val_score fits a fresh model for each split and scores its held-out rows. groups identifies the equipment groups and cv supplies the split rule. neg_mean_absolute_error returns negative MAE; negate it to report positive errors.'),
'mean_absolute_error':('Comparing two prediction sets','mean_absolute_error(actual, predicted) averages the absolute differences of paired values. Lower is better. Both lists must have the same length and row order; the answer has the target’s unit.'),
'perf_counter':('Measuring elapsed time','perf_counter() reads a high-resolution clock in seconds. Subtract the earlier reading from the later one, then multiply by 1000 for milliseconds. One measured run is an illustration, not a reliable performance benchmark.'),
'loc':('Selecting labelled rows','table.loc[row_mask] selects rows whose mask is True. With column labels, .loc selects named columns too. .copy() makes a separate working table after selection.'),
'reset_index':('Aligning positions for subtraction','series.reset_index(drop=True) replaces old row labels with 0, 1, 2, and so on. drop=True discards the old labels. Apply it when pairing with a new prediction Series that has those positional labels.'),
'python_function':('Defining and calling a function','def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.'),
'python_slice':('Selecting a short preview','values[:5] selects positions 0 through 4, or fewer if the sequence is shorter. The stop position is excluded. This preview does not change the full array stored in the variable.'),
'python_repeat':('Repeating a baseline value','[training_target_mean] is a one-item list. Multiplying that list by the number of validation rows repeats its value once per row. This is list repetition, not multiplication of the mean itself.'),
'python_if':('Checking a condition before calculating','if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.'),
'python_power':('Squared error and square root','error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.'),
'python_basics':('Reading the code syntax','= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.'),
}
OPS.update(MORE)

def name_map(week):
 m=dict(NAMES);m['valid']='validation_data' if week==14 else 'valid_row_mask'
 if week==14:m['baseline']='baseline_predictions'
 return m

def rename_code(program,mapping,preserve_parameters=False):
 tree=ast.parse(program);protected=set()
 if preserve_parameters:
  protected={a.arg for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for a in n.args.args}
 starts=[];offset=0
 for line in program.splitlines(keepends=True):starts.append(offset);offset+=len(line)
 edits=[]
 for n in ast.walk(tree):
  name=n.id if isinstance(n,ast.Name) else n.arg if isinstance(n,ast.arg) else None
  if name in mapping and name not in protected:
   a=starts[n.lineno-1]+n.col_offset;b=a+len(name);edits.append((a,b,mapping[name]))
 for a,b,value in sorted(set(edits),reverse=True):program=program[:a]+value+program[b:]
 return program

def prose(text,mapping):
 # Replace identifiers in code fragments, without replacing normal English words.
 for old,new in mapping.items():
  text=re.sub(r'\b'+re.escape(old)+r'(?=\.[A-Za-z_]|\[)',new,text)
  text=text.replace('`'+old+'`','`'+new+'`')
  if old in ('tp','tn','fp','fn','train_x','valid_x','base_cols','extra_cols','base_pred','extra_pred','base_mae','extra_mae','linear_pred','tree_pred','cv'):
   text=re.sub(r'\b'+old+r'\b',new,text)
 return text

def operations(program):
 tree=ast.parse(program);found=['python_basics']
 for n in ast.walk(tree):
  key=None
  if isinstance(n,ast.Import):key='alias'
  elif isinstance(n,ast.Attribute):key=n.attr if n.attr in OPS else None
  elif isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in OPS:key=n.func.id
  elif isinstance(n,ast.Subscript):key='python_slice' if isinstance(n.slice,ast.Slice) else 'select'
  elif isinstance(n,ast.FunctionDef):key='python_function'
  elif isinstance(n,ast.If):key='python_if'
  elif isinstance(n,ast.BinOp):key='python_power' if isinstance(n.op,ast.Pow) else 'mask' if isinstance(n.op,ast.BitAnd) else 'python_repeat' if isinstance(n.op,ast.Mult) and isinstance(n.left,ast.List) else 'arithmetic'
  if key and key not in found:found.append(key)
 return found

def chunk_program(program):
 # Readable line length; split at complete top-level statements where possible.
 formatted=black.format_str(program,mode=black.Mode(line_length=66)).strip()
 tree=ast.parse(formatted);lines=formatted.splitlines();chunks=[];current=[]
 for node in tree.body:
  block=lines[node.lineno-1:node.end_lineno]
  if current and len(current)+len(block)>8:chunks.append('\n'.join(current));current=[]
  while len(block)>8:
   chunks.append('\n'.join(block[:8]));block=block[8:]
  current+=block
 if current:chunks.append('\n'.join(current))
 return formatted,chunks

def explain_statement(node):
 if isinstance(node,(ast.Import,ast.ImportFrom)):return 'Load the named tools. Importing a model class does not train a model.'
 if isinstance(node,ast.FunctionDef):return 'Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.'
 names=[n.id for t in (node.targets if isinstance(node,ast.Assign) else []) for n in ast.walk(t) if isinstance(n,ast.Name)]
 if names:
  return ' '.join(name+' stores '+MEANINGS.get(name,'the result of the displayed expression')+'.' for name in names)
 if isinstance(node,ast.If):return 'Check the condition first, then run only the matching branch. This avoids invalid division or selecting a row that does not exist.'
 if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):
  call=node.value
  if isinstance(call.func,ast.Name) and call.func.id=='print':return 'Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.'
  if isinstance(call.func,ast.Attribute) and call.func.attr in OPS:return OPS[call.func.attr][1]
 return 'Evaluate the displayed statement using the values produced by the preceding statements.'

def revise():
 p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text());manifest=[]
 for d in decks:
  if d['week']<8 or d.get('descriptive_names_revision')=='2026-10-20-v2':continue
  m=name_map(d['week']);old=copy.deepcopy(d['slides']);new=[];seen=set();skip=0
  for index,s in enumerate(old):
   if skip:skip-=1;continue
   if s.get('kind')=='contract':
    new.append(s);continue
   if not s.get('code'):
    for field in ('body','notes','caption','title'):
     if field in s:s[field]=prose(s[field],m)
    if 'concepts' in s:
     for concept in s['concepts']:concept['meaning']=prose(concept['meaning'],m)
    seen.update(s.get('introduced_operations',[]));new.append(s);continue
   full=s.get('practice_code') or s['code']
   # Existing continuation slides store the complete executable program on the first slide.
   if s.get('practice_code'):
    while index+skip+1<len(old) and old[index+skip+1].get('kind')=='code' and old[index+skip+1].get('practice_code')=='':skip+=1
   renamed=rename_code(full,m);formatted,chunks=chunk_program(renamed)
   required=operations(formatted);missing=[k for k in required if k not in seen]
   for j in range(0,len(missing),2):
    keys=missing[j:j+2];new.append({'kind':'explanation','title':' / '.join(OPS[k][0] for k in keys),'body':'\n\n'.join(OPS[k][1] for k in keys),'notes':'\n\n'.join(OPS[k][1] for k in keys)+'\nExplain these operations before running the following example.','introduced_operations':keys,'operation_prerequisite':True,'descriptive_names_revision':True})
   seen.update(required)
   assigned=[]
   for node in ast.walk(ast.parse(formatted)):
    if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Store) and node.id in MEANINGS and node.id not in assigned:assigned.append(node.id)
   # Put the meaning of the first new variables beside their first use in lecturer notes.
   walkthrough='\n\n'.join(ast.unparse(n)+'\n'+explain_statement(n) for n in ast.parse(formatted).body)
   meaning='\n'.join(n+': '+MEANINGS[n]+'.' for n in assigned)
   oldnote=s.get('notes','');reading=''
   if 'Reading the result\n' in oldnote:reading=oldnote.split('Reading the result\n',1)[1].split('Further explanation')[0]
   elif d['week']==14:reading=oldnote
   title=re.sub(r' \(\d+/\d+\)$','',s['title'])
   check=rename_code(s.get('revision_check',''),m) if s.get('revision_check') else ''
   for part,code in enumerate(chunks):
    item=copy.deepcopy(s);item.update(title=title+(f' ({part+1}/{len(chunks)})' if len(chunks)>1 else ''),code=code,practice_code=formatted if part==0 else '',code_size=25,explain=['\n'.join(meaning.splitlines()[:1]) or 'Use the named inputs in the displayed calculation.'],notes='Variable names\n'+meaning+'\n\nComplete example, step by step\n'+walkthrough+'\n\nReading the result\n'+prose(reading,m),explained_operations=required,descriptive_names_revision=True)
    if part:item['caption']='Continue the same example in the same code cell.'
    if s.get('revision_example'):
     # Revisions are executed from complete code in their matching notebook.
     item['revision_example']=part==len(chunks)-1
     item['revision_check']=check if part==len(chunks)-1 else ''
    new.append(item)
   manifest.append({'cohort':d['cohort'],'week':d['week'],'title':title,'operations':required,'variables':assigned})
  for i,s in enumerate(new,1):s['sequence_number']=i
  d['slides']=new;d['descriptive_names_revision']='2026-10-20-v2'
  (ROOT/'IUEA_Teaching_Plan/decks/lecturer_notes'/Path(d['filename']).with_suffix('.md')).write_text('# '+d['cohort']+' Week '+str(d['week'])+'\n\n'+'\n\n'.join(f"## Slide {i}: {s['title']}\n\n{s.get('notes','')}" for i,s in enumerate(new,1)))
 p.write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'data/descriptive_names_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':revise()
