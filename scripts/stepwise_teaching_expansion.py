"""Stepwise teaching examples and a complete Week 6 EDA/cleaning workflow."""
import ast,copy,json,re
from pathlib import Path
from descriptive_teaching_names import chunk_program,operations,OPS,MEANINGS
ROOT=Path(__file__).resolve().parents[1]
def idea(title,body,notes=None):return dict(kind='explanation',title=title,body=body,notes=notes or body)
def example(title,program,notes):return dict(kind='code',title=title,body='',code=program,practice_code=program,code_size=25,caption='Run after the preceding example using the supplied CSV.',explain=[notes.split('\n')[0]],notes=notes)
CLEAN='''modelling_data = raw_data.drop_duplicates("record_id").copy()
target_is_recorded = modelling_data["target"].notna()
load_is_valid = modelling_data["load_pct"].between(0, 100)
rows_to_keep = target_is_recorded & load_is_valid
print(target_is_recorded.head())
print(load_is_valid.head())
modelling_data = modelling_data[rows_to_keep].copy()
print(len(raw_data), len(modelling_data))
is_training_equipment = modelling_data["equipment_id"].isin(["E1", "E2", "E3", "E4"])
is_validation_equipment = modelling_data["equipment_id"].isin(["E5"])
is_test_equipment = modelling_data["equipment_id"].isin(["E6"])
training_data = modelling_data[is_training_equipment].copy()
validation_data = modelling_data[is_validation_equipment].copy()
test_data = modelling_data[is_test_equipment].copy()
feature_columns = ["load_pct", "ambient_c"]
print(len(training_data), len(validation_data), len(test_data))'''
DETAIL={
'modelling_data':('Prepare valid observations','First keep the first record ID. Then ask two questions for each remaining row: is the target recorded, and is load between 0 and 100? Only a row passing both checks stays. Missing inputs are handled later using training data only.'),
'is_training_equipment':('Choose groups before choosing rows','isin(list_of_labels) answers True when a row’s equipment ID appears in the list. Here E1–E4 supply training rows, E5 validation rows and E6 test rows. The groups stay separate so one equipment group cannot appear on both sides.'),
'X_train':('Separate inputs from answers','X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.'),
'linear_model':('Create, then train, then predict','Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.'),
'baseline_model':('Start with a simple reference','A training-mean baseline predicts the same value for every validation row. fit calculates that value from y_train. Compare its error with the more complex model on the same validation rows.'),
'tree_model':('Compare a second kind of model','A regression tree learns splits in the input columns. max_depth limits its split levels. The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.'),
'validation_results':('Line up observations and predictions','Copy record IDs and observed targets from validation rows. Add predictions in that same order. Each row now pairs one observation with its own predicted value.'),
'prediction_errors':('Measure how far predictions missed','Subtract predicted from observed values. Positive errors mean underprediction; negative errors mean overprediction. abs removes signs for MAE. Squaring before averaging and taking a square root gives RMSE.'),
'grouped_folds':('Repeat evaluation without mixing groups','Four folds means four held-out group turns. In each turn, learn a fresh pipeline on the other training groups and score the held-out group. This uses training_data only; validation and test tables stay outside this calculation.'),
'negative_error_scores':('Read the scoring convention','scikit-learn uses larger scores as better. neg_mean_absolute_error therefore returns negative errors. Negate the returned scores to recover ordinary positive MAE; lower MAE is better.'),
'fold_absolute_errors':('Report typical error and variation','Each value is the MAE of one held-out fold. mean gives average error. std(ddof=0) describes spread across these four errors; it is not a confidence interval. A large spread suggests performance depends on the held-out equipment.'),
'base_feature_columns':('Change one feature set at a time','The base inputs are load and ambient temperature. The extended inputs also include their product. Train separate pipelines on the same rows and compare on the same validation rows. This isolates the effect of adding the feature.'),
'base_pipeline':('Fit both alternatives fairly','Each pipeline learns its own training medians and regression settings. The base model sees only base columns; the extended model sees the additional feature. Neither uses validation targets while learning.'),
'base_predictions':('Compare errors on the same rows','Predict both alternatives on matching validation rows. mean_absolute_error compares each prediction with its observed target. Base MAE minus extended MAE is positive when the extra feature helped on this validation set.'),
'prediction_start_time':('Time prediction, not training','perf_counter reads seconds from a high-resolution clock. Read it immediately before and after predict. Convert elapsed seconds to milliseconds and divide by row count. One timing is illustrative: repeated measurements are needed for a reliable speed claim.'),
'eligible_models':('Apply both model-selection rules','A candidate must satisfy both the error limit and the time limit. Compare each column with its limit first, then combine the True/False answers with &. Filtering can return no rows.'),
'ranked_models':('Choose only if an eligible model exists','sort_values orders by error, then time, then name. empty answers whether no rows remain. Check it before iloc[0], which requests the first row by position. Return None when no candidate qualifies.'),
'actual_labels':('Keep observations and decisions paired','actual contains the recorded class; predicted contains the model’s decision for the same row. Here 1 means positive and 0 negative. These are already-issued decisions; this exercise does not train a classifier.'),
'actual_is_positive':('Turn each class label into a question','actual == 1 asks whether the real class is positive; predicted == 1 asks whether the model predicted positive. Each comparison returns one True/False answer per row. Equality uses ==; assignment uses =.'),
'is_true_positive':('Count one outcome at a time','A true positive has actual 1 AND predicted 1. Combine the two answer columns with &, then sum the True entries. The other three outcomes use their own pairs of actual and predicted labels.'),
'precision':('Precision: how trustworthy are positive predictions?','The denominator is all predicted positives: true positives plus false positives. Divide correct positive predictions by that total. Check the denominator before dividing; this teaching example uses 0 when it is zero.'),
'recall':('Recall: how many real positives were found?','The denominator is all actual positives: true positives plus false negatives. Divide detected positives by that total. Precision and recall answer different questions even when they happen to have the same value.'),
'baseline_errors':('Compare the baseline with observed targets','Pair each baseline prediction with its validation target. reset_index(drop=True) makes their row labels match by position before subtraction. The training mean must come from training rows only.'),
}
MEANINGS.update(target_is_recorded='one True/False answer per row: whether target is present',load_is_valid='one True/False answer per row: whether load is within the stated limits',rows_to_keep='True only where both row checks pass')
def split_groups(program,title):
 tree=ast.parse(program);nodes=tree.body
 # Start a new teaching step at a change in purpose, never inside a function or if block.
 boundaries={'modelling_data','is_training_equipment','training_data','X_train','linear_model','baseline_model','tree_model','validation_results','prediction_errors','training_ambient_median','grouped_folds','negative_error_scores','fold_absolute_errors','base_feature_columns','base_pipeline','base_predictions','extended_predictions','prediction_start_time','candidate_models','eligible_models','ranked_models','actual_labels','actual_is_positive','is_true_positive','false_negative_count','precision','recall','total_error_cost','baseline_errors'}
 groups=[];current=[];seen=set()
 for n in nodes:
  target=n.targets[0].id if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) else ''
  if target in boundaries and target not in seen and current and not all(isinstance(x,(ast.Import,ast.ImportFrom)) for x in current):groups.append(current);current=[]
  current.append(n);seen.add(target)
 if current:groups.append(current)
 return groups

def apply():
 p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text());template=copy.deepcopy(next(d for d in decks if d['cohort']=='CML3113' and d['week']==6))
 for d in decks:
  if d.get('stepwise_pipeline_revision'):continue
  if d['week']==6:
   # Keep cohort-specific assessment endings; share the beginner cleaning walkthrough.
   old=d['slides'];core=[]
   for s in template['slides']:
    if s['title']=='Ungraded cleaning practice':break
    s=copy.deepcopy(s);s['notes']=s['notes'].split('\n\nVerified output')[0]
    core.append(s)
   core[0]=copy.deepcopy(old[0])
   if d['cohort']=='CML3111':
    core[1]=idea('Today: inspect, clean, check and plot','First inspect the original CSV. Then apply the cleaning rules, check the result, and explain the cleaned charts.\n\nThis walkthrough supports the existing Week 6 assignment and quiz. Their requirements are unchanged.')
    start=next(i for i,s in enumerate(old) if s['title'] in ('Your issued assignment','Your issued task','Ungraded cleaning practice'))
    tail=old[start:]
   else:
    tail=copy.deepcopy(template['slides'][len(core):])
    core[1]['body']=core[1]['body'].replace('CML3113',d['cohort'])
   unit={'CML3111':'°C','CML3112':'kW','CML3113':'kWh/t'}[d['cohort']]
   quantity={'CML3111':'motor temperature','CML3112':'power demand','CML3113':'crusher energy'}[d['cohort']]
   for s in core:
    for key in ('body','notes','caption','code','practice_code','title'):
     if isinstance(s.get(key),str):s[key]=s[key].replace('crusher energy',quantity).replace('Crusher energy',quantity.capitalize()).replace('kWh/t',unit)
    # Data-derived values are checked and described again by the verifier.
    if d['cohort']!='CML3113':s['notes']=re.sub(r'14\.001|26\.07','the value printed below',s['notes'])
   d['slides']=core+tail
   # EDA before changing any data: structure, summaries, group coverage, raw distribution.
   idx=next(i for i,s in enumerate(d['slides']) if s['title']=='Loading the supplied observations')+1
   eda=[idea('EDA: understand the original observations','EDA means exploratory data analysis: inspect what the columns mean, their types, missing values, ranges and patterns before choosing cleaning actions.\n\nrecord_id identifies an observation; equipment_id identifies its source. load_pct is %, ambient_c is °C, and target is '+quantity+' ('+unit+').','An ID is a label, not a measurement to average. The CSV is synthetic teaching data. Its patterns do not establish real engineering operating limits. Week 5 introduced EDA; here we repeat it as the first stage of a complete workflow.'),idea('Check types and recorded values','table.info() prints column types and non-missing counts. Call it directly; do not wrap it in print.\n\ntable[numeric_columns].describe() summarises selected numeric measurements: count, mean, standard deviation, minimum, quartiles and maximum.','count excludes missing cells. Quartiles split sorted values into four parts: 50% is the median, 25% and 75% bound the middle half. Standard deviation describes spread. Inspect measurements, not record IDs. A minimum below zero in load_pct flags a value to investigate.'),example('Inspect structure and numerical ranges','raw_data.info()\nnumeric_columns = ["load_pct", "ambient_c", "target"]\nprint(raw_data[numeric_columns].describe())','Compare count with the original row count. Read min and max before deciding whether a value violates the stated rule.'),idea('Check which equipment is represented','value_counts() counts rows for each label. dropna=False also shows missing labels.\n\nCounts can reveal missing groups or unequal coverage. Repeated equipment IDs are expected; repeated record IDs need separate inspection.'),example('Count observations per equipment','equipment_counts = raw_data["equipment_id"].value_counts(\n    dropna=False)\nprint(equipment_counts)','These are observation counts, not counts of distinct machines. The later duplicate row is still present in this raw-data summary.'),idea('Preview the raw distribution','A histogram groups numeric values into intervals and counts observations in each interval. bins=10 requests ten intervals.\n\nplt.subplots() gives a figure and its axes. ax selects where the chart is drawn. Missing numeric values are omitted from the plot.','Read the horizontal axis as the target measurement and the vertical axis as observation count. This is an uncleaned preview. An extreme value is a reason to investigate, not automatic permission to delete it.'),example('Plot the target before cleaning','import matplotlib.pyplot as plt\nraw_figure, raw_axes = plt.subplots()\nraw_data["target"].plot.hist(bins=10, ax=raw_axes)\nraw_axes.set_xlabel("'+quantity+' ('+unit+')")\nraw_axes.set_ylabel("Observation count")\nraw_axes.set_title("Before cleaning")\nplt.show()','The chart includes all recorded targets, including observations that may later be removed. Compare with the cleaned distribution at the end; do not infer causation from shape.')]
   d['slides'][idx:idx]=eda
   idx=next(i for i,s in enumerate(d['slides']) if s['title']=='Fill missing ambient temperatures')+1
   d['slides'][idx:idx]=[idea('Validate the result before interpreting charts','Count original and retained rows. Check duplicate record IDs, missing values and valid loads again.\n\n.all() answers True only when every row passes the condition. A check confirms what the data contain; a table named cleaned_data is not automatically correct.'),example('Check the cleaned table','print("Rows before:", len(raw_data))\nprint("Rows after:", len(cleaned_data))\nprint("Duplicate IDs:", cleaned_data.duplicated("record_id").sum())\nprint(cleaned_data.isna().sum())\nprint("Loads valid:", cleaned_data["load_pct"].between(0, 100).all())','Expect 91 original rows, 88 retained rows, zero duplicate IDs, zero remaining missing cells, and True for the load check. Missing temperatures are estimates; the unchanged raw table retains the original gaps.')]
  elif d['week']>=8:
   old=d['slides'];new=[];skip=0
   for i,s in enumerate(old):
    if skip:skip-=1;continue
    if not s.get('code'):
     s=copy.deepcopy(s)
     # Undo identifier substitutions in ordinary sentence-ending words.
     if d['week'] in (13,15):
      for field in ('body','notes','caption','title'):
       if field in s:
        for a,b in [('mean_load_by_equipment_group','result'),('modelling_data','data'),('reading_values','readings')]:s[field]=s[field].replace(a,b)
     new.append(s);continue
    program=s.get('practice_code') or s['code']
    if s.get('practice_code'):
     while i+skip+1<len(old) and old[i+skip+1].get('kind')=='code' and old[i+skip+1].get('practice_code')=='':skip+=1
    title=re.sub(r' \(\d+/\d+\)$','',s['title'])
    if title=='Preparing the supplied modelling rows':program=CLEAN
    if 'Confusion counts' in title:
     program='''actual_labels = raw_data["actual"]
predicted_labels = raw_data["predicted"]
actual_is_positive = actual_labels == 1
prediction_is_positive = predicted_labels == 1
actual_is_negative = actual_labels == 0
prediction_is_negative = predicted_labels == 0
print(actual_is_positive.head())
print(prediction_is_positive.head())
is_true_positive = actual_is_positive & prediction_is_positive
true_positive_count = int(is_true_positive.sum())
print("True positives:", true_positive_count)
false_negative_count = int((actual_is_positive & prediction_is_negative).sum())
false_positive_count = int((actual_is_negative & prediction_is_positive).sum())
true_negative_count = int((actual_is_negative & prediction_is_negative).sum())
print(false_negative_count, false_positive_count, true_negative_count)
print(true_positive_count + false_negative_count + false_positive_count + true_negative_count, len(raw_data))'''
    if title=='Selection from the measured candidate table':program=program.replace('eligible_models = candidate_models[\n    (candidate_models["validation_mae"] <= 10)\n    & (candidate_models["latency_ms"] <= 10)\n]','error_is_acceptable = candidate_models["validation_mae"] <= 10\ntime_is_acceptable = candidate_models["latency_ms"] <= 10\nmodel_is_eligible = error_is_acceptable & time_is_acceptable\neligible_models = candidate_models[model_is_eligible]')
    groups=split_groups(program,title)
    for gnum,group in enumerate(groups,1):
     source='\n'.join(ast.unparse(n) for n in group);fmt,chunks=chunk_program(source)
     names=[n.targets[0].id for n in group if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)]
     key=next((n for n in names if n in DETAIL),None)
     if key:
      heading,body=DETAIL[key];new.append(idea(heading,body))
     elif len(groups)>1:
      heading=title+' — step '+str(gnum)
      descriptions=[n+': '+MEANINGS[n]+'.' for n in names if n in MEANINGS]
      if descriptions:new.append(idea(heading,'\n\n'.join(descriptions[:2])))
     for j,chunk in enumerate(chunks):
      t=copy.deepcopy(s);t['title']=title+(f' — step {gnum}' if len(groups)>1 else '')+(f' ({j+1}/{len(chunks)})' if len(chunks)>1 else '')
      t.update(code=chunk,practice_code=fmt if j==0 else '',code_size=25,caption='Continue in the same code cell.' if j<len(chunks)-1 else 'Compare the printed result with the explanation in the notebook.',notes=(DETAIL[key][1]+'\n\n' if key else '')+s.get('notes',''))
      t['revision_check']='';t['stepwise_example']=True
      if d['week']==14:t['revision_example']=True
      new.append(t)
   d['slides']=new
  else:continue
  d['stepwise_pipeline_revision']='2026-10-20'
  for i,s in enumerate(d['slides'],1):s['sequence_number']=i
 p.write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n')
 print('Updated Week 6 and Weeks 8–15 for all cohorts.')
if __name__=='__main__':apply()
