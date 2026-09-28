"""Reviewed teaching order shared by editable slides and guided notebooks.

Every inherited slide must be explicitly placed or explicitly replaced. New
material explains a prerequisite before its first worked use. The plan uses
stable title/occurrence keys, so additions cannot silently bypass the review.
"""
from pathlib import Path
from collections import Counter
import ast, copy, json, re
from beginner_experiential import explain_code
from beginner_pathway import COHORTS
PLAN=json.loads(Path(__file__).with_name('beginner_sequence_plan.json').read_text())
AUDIT=[]

def prose(title,*paragraphs,kind='explanation'):
 return dict(title=title,body='\n\n'.join(paragraphs),kind=kind,notes='Explain this before the next worked example. Point to each named part, then ask learners to describe it in their own words.')
def terms(title,*pairs):
 return dict(title=title,body='',kind='concepts',concepts=[dict(term=a,meaning=b) for a,b in pairs],notes='Give the everyday meaning first. Read each symbol aloud before asking students to use it.')
def code(title,program,caption):
 return dict(title=title,body='',kind='code',code=program,practice_code=program,caption=caption,explain=explain_code(program),notes=caption+'\n\nComplete practice code:\n'+program)

def additions(week,cohort,old):
 vocabulary={c['term']:c['meaning'] for s in old for c in s.get('concepts',[])}
 def t(title,*names):return terms(title,*[(n,vocabulary[n]) for n in names])
 a={
 'numbers':[terms('Start with numbers and values',('Number','A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.'),('Value and unit','A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.'))],
 'variables':[terms('Give a value a name',('Variable','A variable is a name referring to a value. In readings = 12, readings is the name and 12 is its initial number.'),('Assignment','Read = as “assign”, not “is equal to”. Python calculates the right side first, then gives that value to the name on the left. A later assignment replaces its previous value.'))],
 'open_notebook':[prose('Open the main notebook together','Download the ZIP for your course code. Extract it into one folder; leave the supplied files together.','Open Google Colab. Choose Open notebook → Upload and select proof_of_life.ipynb.','Wait for the notebook page. Find one text block and one code block before clicking Run.',kind='steps')],
 'save_notebook':[prose('Save a copy you can find again','In Colab choose File → Download → Download .ipynb. Find the downloaded notebook on your computer.','Use File → Open notebook → Upload to reopen that file. Check your changes are present.','Restart the session, upload the supplied CSV again if needed, and Run all. Save the notebook again after this check.',kind='steps')],
 'repair_words':[terms('The words in the repair exercises',('Module and version','A module is a collection of Python tools. import asks for it. A version identifies a software release; different releases can behave differently.'),('Path and working folder','A path tells Python where a file is. A bare filename is looked up in the current working folder. The runtime Files panel shows uploaded files.'))],
 'github':[prose('Record a change in your repository','Sign into GitHub. Create a repository: the project folder with recorded history. Use an appropriate private setting for personal work.','Choose Add file → Upload files. Add the notebook, supplied CSV and README.md. A README is a text file containing your run instructions.','Write a short message describing the change and choose Commit changes. A commit records this version of the files.','Open the file list to confirm the files arrived. Copy the repository page URL for the assignment form.',kind='steps')],
 'calls':[terms('Read a function call before using it',('A built-in function','Python already provides tools such as print, type and float. A function call asks a named tool to do its work: print(3) displays 3.'),('Parentheses, quotes and comments','Parentheses hold the inputs to a call. Quotes make text: "3.5" is text; float("3.5") converts it to a number. # starts a comment that Python does not run.'))],
 'signed_error':[prose('Keep the reading beside its signed error','These paired lists use the same positions: the first error belongs to the first reading. The sign tells the direction; abs gives only the size.','index(value) finds the first position containing that value. Use that position in the original lists. An exact tie selects the first here; follow the issued task’s rule.'),code('Find a position, then recover the original values','readings = [98, 105, 92]\nerrors = [-2, 5, -8]\nsizes = [abs(errors[0]), abs(errors[1]), abs(errors[2])]\nposition = sizes.index(max(sizes))\nprint(readings[position], errors[position])','Expected: 92 -8. The largest size is 8; the signed error is -8.')],
 'units':[prose('Read the quantities before the formulas','Mass measures matter in kg. Weight is a force in newtons (N): mass × gravitational acceleration. Here g = 9.81 m/s².','Power is a rate of energy transfer, measured in watts (W). Efficiency compares useful output power with input power.','rpm means revolutions per minute. One revolution is 2π radians; one minute is 60 seconds. π is approximately 3.14159.','A named constant is a value kept fixed for a calculation. Uppercase names such as PI are a convention; Python does not prevent changing them.')],
 'list_methods':[terms('Read list operations',('append and len','readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.'),('Slice','readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.'))],
 'dict_methods':[terms('Read dictionary operations',('Key and lookup','A key is the name used to find a value. record["reading"] looks up that key. record.get("missing", 0) returns 0 if the key is absent.'),('items and paired names','record.items() supplies key/value pairs. for key, value in ... puts each pair into two names, then runs the indented block once for that pair.'))],
 'group_means':[prose('A group mean needs its own count','The preceding loop calculated a total for each group. Count records in those same groups, then divide each group total by its own count.','items() supplies the group name and its total together. We use small invented records, not the assignment’s answers.'),code('From group totals to group means','counts = {}\nfor row in records:\n    group = row["group"]\n    counts[group] = counts.get(group, 0) + 1\nmeans = {}\nfor group, total in totals.items():\n    means[group] = total / counts[group]\nprint(means)','Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.')],
 'invalid_text':[prose('When numeric text cannot be converted','float("bad") raises ValueError: the text does not represent a number. An exception interrupts ordinary execution.','try contains the operation that might fail. except ValueError runs only for that named failure. Indentation shows the two blocks.'),code('Catch one expected conversion failure','text = "bad"\ntry:\n    reading = float(text)\nexcept ValueError:\n    reading = None\nprint(reading)','Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.')],
 'create_table':[code('Build the table before asking questions','import pandas as pd\ndf = pd.DataFrame({"building": ["A", "A", "B", "B"],\n                   "kwh": [2, 4, 5, 7]})\nprint(df)','Each dictionary key becomes a column name. Equal-length lists supply its rows.')],
 'select_column':[code('Select a column and calculate its mean','print(df["kwh"])\nprint(df["kwh"].mean())','The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.')],
 'filter_table':[code('Keep rows where the comparison is true','mask = df["kwh"] > 4\nprint(mask)\nprint(df[mask])','The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.')],
 'group_table':[code('Calculate one total for each building','print(df.groupby("building")["kwh"].sum())','Expected: A totals 6 kWh; B totals 12 kWh.')],
 'derived_column':[prose('Create a column from two existing columns','A new column can store a calculation for every row. Division pairs the values in matching rows.','For this invented table all energy values are positive. UGX is Uganda shillings. Cost divided by energy has units UGX/kWh.'),code('An energy rate is cost divided by energy','df["cost_ugx"] = [1000, 2400, 3500, 5600]\ndf["rate_ugx_per_kwh"] = df["cost_ugx"] / df["kwh"]\nprint(df["rate_ugx_per_kwh"])','Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.')],
 'copy_set':[terms('Copy a record and remember an ID',('dict(row)','For our flat records, dict(row) makes a separate dictionary with the same fields. Changing a number in the copy leaves the original record unchanged.'),('set, in, add and continue','set() starts an empty collection of unique items. in checks membership; add remembers an item. continue skips the rest of the current loop pass.'))],
 'chart_kinds':[terms('Choose a chart after naming the question',('Scatter and bar','A scatter plot places one point for each paired measurement. A bar chart compares values across named groups. Label both axes and their units.'),('Histogram and bins','A histogram counts observations in numerical intervals called bins. The horizontal axis is the measurement; the vertical axis is a count. Bin edges affect its appearance.'))],
 'line_errors':[prose('A fitted line is a numerical rule','For these invented observations, target = 2 × input + 10 matches all four points. 2 is the slope; 10 is the intercept, the value at input zero.','A prediction error is the difference between a prediction and the measured answer. A vertical gap in the picture shows that error.','Fitting chooses the slope and intercept to minimise summed squared errors. Squaring means multiplying an error by itself; a small training error still needs an unseen-data check.')],
 'nested_arrays':[terms('Rows and arrays before model code',('Nested lists','[[1], [2], [3]] has three inner lists: three rows with one feature each. [12, 14, 16] has one target per row in the same order.'),('NumPy and array','NumPy is a numerical library; np is its short imported name. np.array(...) builds an array. shape reports its dimensions. np.nan represents a missing numerical value.'))],
 'objects':[terms('A model object keeps learned information',('Object and method','LinearRegression() creates a model object. A method is an operation on that object. model.fit(...) stores learned information; model.predict(...) uses it.'),('Options','An argument such as strategy="mean" names an option. A random seed fixes the starting state of random choices; it does not prove that a model is accurate.'))],
 'pipeline':[terms('Reuse the same preparation on new inputs',('Imputer','An imputer fills missing feature values using a stated rule. Fit learns the replacement from training observations only. Prediction reuses that stored replacement.'),('Pipeline','A pipeline connects preprocessing and a model. make_pipeline creates that connection. Its fit learns both stages on training data; predict applies them to new features.'))],
 'pairs_sqrt':[terms('The operations in the error calculation',('zip and paired names','zip(actual, predicted) pairs values at matching positions. for truth, guess in ... assigns each pair to two names. Here both lists must have the same nonzero length.'),('Square and square root','difference ** 2 squares an error. sqrt reverses a square for nonnegative numbers: sqrt(9) is 3. from math import sqrt makes this tool available.'))],
 'r_squared':[prose('R² compares against a mean prediction','R² compares squared errors with predicting the mean of the evaluated targets. It is a score, not “percentage accuracy”.','1 means perfect predictions on those observations. 0 matches that mean-prediction reference; a negative score can be worse.','Use the same evaluation observations and report the specified error metric with its units. Constant targets need special handling; this score alone does not prove usefulness.')],
 'cost_rule':[prose('State the cost rule before calculating','A cost rule assigns a penalty to each kind of mistake. In this teaching example, a missed warning costs 5 units and a false alarm costs 1 unit.','Total cost = 5 × FN + FP. One missed warning and one false alarm therefore cost 6 units.','These are invented teaching penalties. Use the published assignment cost rule and explain whose consequences it represents.')],
 'probability':[terms('Probability and a decision threshold',('Probability','A probability is between 0 and 1. Multiply by 100 for percent: 0.7 is 70%. A model’s probability is an estimate that needs checking.'),('Threshold','A threshold turns a score into a decision. For a rule score >= 0.5, a score of 0.7 gives class 1. Use validation data to choose the threshold.'))],
 'encoding':[terms('Represent a category with indicators',('Category','A category is a label such as steel or timber. Its name does not imply a numerical size or rank.'),('One-hot indicator','Create a column for each category. Its entry is 1 when the row has that category and 0 otherwise. Learn the allowed categories from training data.'))],
 'accuracy':[prose('Accuracy can hide missed warnings','Accuracy = number of correct labels / number of labels. It counts correct warnings and correct non-warnings together.','If 90 of 100 cases need no warning, predicting no warning every time gives 90% accuracy. It detects none of the 10 real warnings: recall is 0.','Always inspect the actual/predicted counts and relevant costs before calling a classifier useful.')],
 'split_tools':[terms('Choose a split that matches future use',('Equipment or time','For unseen equipment, keep each equipment ID together. For future-time prediction, train on earlier observations and evaluate on later ones.'),('Scaler and split tool','A scaler learns how to rescale features; fit it on training data. GroupShuffleSplit is a library tool for group separation. Our assignment instead uses its fixed published equipment lists.'))],
 'electric_units':[prose('Read the physical example across programmes','Current I is the flow of electric charge, measured in amperes (A). Resistance R opposes that flow, measured in ohms.','Power P is energy transferred per second, measured in watts (W). Resistive heating follows P = I²R in this example.','I² means I × I. With I = 2 A and R = 3 ohms, P = 2 × 2 × 3 = 12 W. This relationship motivates a feature; evaluation still tests whether it helps.')],
 'experiment_syntax':[prose('Read the two-model experiment','Each row contains a pair of inputs. for a, b in rows assigns the first entry to a and the second to b, then repeats the block.','with_interaction returns a new table containing a, b and a × b. Both models keep the same training and validation rows.','fit returns the fitted model object, so creating and fitting can appear in one expression. round(value, 6) rounds a displayed number to six decimal places.')],
 'path_syntax':[terms('Read the path example',('Path and cwd','Path is a tool imported from Python’s pathlib module. Path.cwd() returns the folder where Python is currently running.'),('name','The .name property gives the last folder component as text. It depends on your runtime. A different folder name is expected on another computer.'))],
 'handover_words':[terms('Tell another person what the project needs',('requirements.txt and versions','This text file lists required Python packages and their versions. Record the versions used in the working environment; test them with the supplied run instructions.'),('Data source, permission and seed','Name the data source and any licence or permission for reuse. Record random seeds used in modelling. A seed supports repeatability; it does not repair data leakage.'))],
 'presentation_words':[terms('A presentation connects a claim to evidence',('Finding and limitation','A finding states what the evidence shows. A limitation states where that evidence is incomplete or may not apply. Point to the relevant chart, metric or record.'),('Defence and reflection','A defence explains why you made a choice. A reflection explains what you learned and would improve. Describe your own contribution with specific evidence.'))]
 }
 a['programme_quantities']=[terms('Read the quantities in your programme example', *{
 'CML3111':[('Voltage and current','Voltage describes electrical potential difference in volts (V). Current is the rate of charge flow in amperes (A). This example uses direct current (DC).'),('Power','Power is energy transferred each second, measured in watts (W). For this DC example, power = voltage × current. Resistive heating later uses current squared × resistance.')],
 'CML3112':[('Length, width and area','Length and width are distances in metres (m). A rectangle’s area is length × width, measured in square metres (m²).'),('Thickness and density','Thickness is the third distance. Area × thickness gives volume in m³. Density is mass per volume, in kg/m³; volume × density gives mass in kg.')],
 'CML3113':[('Volume, time and flow','Volume is how much space fluid occupies, here in litres. Time is measured in seconds. Flow is volume divided by time, in litres per second.'),('Density and pressure','Density is mass per volume in kg/m³. Pressure is force per area, measured in pascals (Pa). 1000 Pa = 1 kPa. Fluid density and depth determine the hydrostatic contribution.')]
 }[cohort])]
 a['blank_filter']=[prose('Skip a blank before converting text','An empty text field is "". The comparison != means “not equal to”. Only convert a value after the blank check passes.','In this example, values records valid numbers only. Its length is the valid count; the group summaries must use the same valid-record policy.'),code('Collect only the recorded numbers','text_values = ["2.5", "", "3.5"]\nvalues = []\nfor text in text_values:\n    if text != "":\n        values.append(float(text))\nprint(len(values), values)','Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.')]
 mappings={2:{'runtime':['Runtime'],'repository':['Repository and commit']},3:{'operators':['Operator'],'function':['Function'],'indentation':['Indentation and return'],'condition':['Condition']},4:{'list':['List and index'],'loop':['Loop and iteration'],'accumulator':['Accumulator'],'dictionary':['Dictionary'],'csv':['CSV and header'],'imports':['with and import']},5:{'mask':['Mask and filter'],'groupby':['groupby and aggregation']},6:{'audit':['Audit'],'axes':['Chart axes']},8:{'model_baseline':['Baseline'],'linear_tree':['Linear model and tree'],'fit_predict':['fit and predict'],'metrics':['MAE and RMSE']},9:{'class_tp':['Class and positive label','TP and TN'],'fp_fn':['FP and FN'],'precision_recall':['Precision','Recall'],'threshold_cost':['Threshold and cost']},10:{'preprocessing':['Preprocessing and pipeline'],'cross_validation':['Cross-validation']}}
 for key,names in mappings.get(week,{}).items():a[key]=[t(' / '.join(names),*names)]
 if week==4:
  filename=COHORTS[cohort]['file']
  a['read_csv']=[prose('Read the supplied CSV in four steps','Place '+filename+' beside the notebook, or upload it in Colab’s Files panel.','import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.','list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.'),code('Open a real CSV and inspect its first row',f'import csv\nwith open("{filename}", newline="") as source:\n    rows = list(csv.DictReader(source))\nprint(rows[0])\nprint(len(rows))','Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.')]
 if week==5:
  a['pandas_csv']=[prose('Load the assignment table before analysing it','Upload campus_energy.csv to the current runtime first. read_csv reads it into a new DataFrame.','head() displays the first five rows; shape gives row and column counts; dtypes shows column data types.','We call this issued_table to keep it separate from the invented four-row df used above.'),code('Inspect the supplied energy file','issued_table = pd.read_csv("campus_energy.csv")\nprint(issued_table.head())\nprint(issued_table.shape)\nprint(issued_table.dtypes)','Check column names, data types and units before attempting the six issued tasks.')]
 return a


def split_program(program,limit=9):
 """Prefer complete top-level statements; retain indentation for long blocks."""
 lines=program.splitlines()
 try:
  ends={n.end_lineno for n in ast.parse(program).body}
 except SyntaxError:
  ends=set()
 chunks=[];start=0
 while start<len(lines):
  stop=min(start+limit,len(lines))
  if stop<len(lines):
   candidates=[n for n in ends if start<n<=stop]
   if candidates:stop=max(candidates)
  chunk='\n'.join(lines[start:stop]).strip('\n')
  if chunk:chunks.append(chunk)
  start=stop
 return chunks

def sequence(slides,week,cohort):
 original=copy.deepcopy(slides);counts=Counter();lookup={}
 for s in original:
  counts[s['title']]+=1;lookup[s['title']+' #'+str(counts[s['title']])]=s
 spec=copy.deepcopy(PLAN[str(week)])
 if week==5 and cohort!='CML3112':spec['order'].insert(-1,'Week 5 support #1')
 keys=[k for k in spec['order'] if not k.startswith('@')]+spec['replaced']
 assert len(keys)==len(set(keys)) and set(keys)==set(lookup),(week,'Unreviewed or repeated slide',set(lookup)-set(keys),set(keys)-set(lookup))
 extra=additions(week,cohort,original);ordered=[]
 for key in spec['order']:
  batch=copy.deepcopy(extra[key[1:]]) if key.startswith('@') else [lookup[key]]
  for s in batch:s['sequence_source']=key
  ordered.extend(batch)
 # Corrections found during the slide-by-slide prerequisite review.
 for s in ordered:
  title=s['title']
  if week==2 and title.startswith('Preparing for the assignment'):s['body']=s['body'].replace('Model repair 01, guide 02–03 and trace 04.','Watch repair 01, work through 02–03 together, then trace 04.')
  if week==4 and title=='Your cohort data':
   fields={'CML3111':'winding_temp_c (degrees C); group by motor_id','CML3112':'crack_width_mm (millimetres); group by structure_id','CML3113':'rate_of_penetration (m/hour); group by bit_type'}
   s['body']=COHORTS[cohort]['file']+'\n\nSummarise '+fields[cohort]+'.\n\nRead the issued task’s blank-value and threshold rules before calculating.'
  if week==5 and title=='Rows columns and units':s['body'] += '\n\nA data type (dtype) describes the kind of values in a column, such as whole numbers, decimals or text.'
  if week==6 and title=='Filling a gap adds an estimate':s['body'] += '\n\nIn Python, value is None tests for a missing marker. is not None tests that it is not that marker.'
  if week==2 and title=='Recall and a first attempt':s['body']='Think of an everyday measurement, such as a desk length. What number and unit would you write down? We will explain the computer terms before using them.'
  if week==4 and title=='Recall and a first attempt':s['body']='Last week we gave values names and called functions. Explain what print(2 + 4) displays, then change one number.'
  if week==4 and title.startswith('Preparing for the assignment'):
   s['body']=s['body'].replace('count, mean, maximum and threshold','valid_count, mean_reading, above_limit and group_means')
  if week==10 and title=='What standard deviation tells us':
   s['body']='Scores 3, 4 and 5 have mean 4. Their deviations are -1, 0 and 1.\n\nFor these three fold scores, population SD = sqrt((1 + 0 + 1) / 3), about 0.82.\n\nSD describes spread around the mean in the score’s units. The next illustration uses this same population convention; it is not a confidence interval.'
   s['notes']='Square each deviation, average all three, then take the square root. Here we describe the full displayed set. A sample SD would instead divide by n - 1; do not mix conventions.'
  if week==12 and title=='Worked example':
   s['code']=s['code'].replace('print([item["name"] for item in eligible])','names = []\nfor item in eligible:\n    names.append(item["name"])\nprint(names)');s['practice_code']=s['code']
  if week==14:
   s['body']=re.sub(r'Confirm[^.]*calibrat[^.]*\.', 'Follow the test instructions issued by your lecturer.',s.get('body',''),flags=re.I)
  if week==15:
   s['body']=s.get('body','').replace('Live questioning and peer comments support learning; they are not a new manual marking workload.','Submit your own written defence and reflection as instructed.')
  if s.get('kind')=='code' and 'practice_code' not in s:s['practice_code']=s['code']
 if week==2:
  root=Path(__file__).resolve().parents[1]
  links=json.loads((root/'data/submission_links.json').read_text());quizzes=json.loads((root/'data/quiz_links.json').read_text())
  entry=links[cohort+'|W01']
  from datetime import datetime,timezone,timedelta
  close=entry.get('closeAt') or links[cohort+'|W02']['closeAt']
  deadline=datetime.fromisoformat(close.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=3))).strftime('%d %b %Y, %H:%M Kampala')
  catchup=[prose('Week 2 includes your Week 1 catch-up','Complete A1, the Week 1 three-problems assignment, and submit it using the A1 link.','Take Quiz 1 when your lecturer activates it. It is separate from the A1 upload.','Also complete today’s A2 notebook and README, and take Quiz 2 when activated. These are four separate tasks.',kind='steps')]
  ordered[2:2]=catchup
  detail=[prose('A1 — what to write and submit','Describe three engineering problems. For each, state what you would measure or classify and whether machine learning is suitable.','List possible inputs, the target where appropriate, a data source and one limitation for each problem. Choose one problem and dataset and justify your choice.','Write one complete report in DOCX or selectable-text PDF. PPTX with narration notes or notebook evidence is also accepted. Upload through the A1 form; keep its confirmation.',kind='steps'),dict(title='Week 1 Assignment A1 catch-up upload',kind='link',body='Submit A1 separately from the A2 notebook and README.\n\nDeadline: '+deadline+'.\n\nEnter your own Student Registration Number; the required field accepts any format.',url=entry['url'],label='Open Week 1 A1 assignment form',notes='Week 1 collection is permitted; existing marks remain protected and new written grading remains held until validated.'),dict(title='Week 1 Quiz 1 catch-up',kind='link',body='Quiz 1 is required catch-up work, separate from A1.\n\nComplete it individually after lecturer activation.\n\nIt closes 24 hours after activation, not at the assignment deadline.\n\nPress Submit and keep your confirmation.',url=quizzes[cohort+'|1'],label='Open Week 1 Quiz 1',notes='In Quiz Controls run open_W1_'+cohort+' when ready to give the full 24-hour window. Announce the exact logged deadline. Opening this link does not activate the quiz.')]
  for slide in catchup+detail:slide['sequence_source']='@week1_catchup'
  pos=next(i for i,x in enumerate(ordered) if x['title']=='Week 2 assignment')
  ordered[pos:pos]=detail
 # Reassemble prior page-sized fragments, then paginate at statement boundaries.
 result=[];i=0
 while i<len(ordered):
  s=ordered[i];i+=1
  if s.get('kind')!='code':result.append(s);continue
  program=s.get('practice_code','')
  if not program:raise AssertionError(('orphan continuation',week,s['title']))
  while i<len(ordered) and ordered[i].get('kind')=='code' and ordered[i].get('practice_code')=='':i+=1
  chunks=split_program(program);base=re.sub(r' \(\d+/\d+\)$','',s['title'])
  for j,chunk in enumerate(chunks):
   part=copy.deepcopy(s);part.update(title=base+(f' ({j+1}/{len(chunks)})' if len(chunks)>1 else ''),code=chunk,practice_code=program if j==0 else '',explain=explain_code(chunk))
   if j:part['caption']='Continue the SAME cell; keep indentation. Run after all parts are entered.'
   result.append(part)
 for n,s in enumerate(result,1):
  s['notes']=s.get('notes','')+'\n\nSequence: explain → read example → predict → run → change one input. Use the guided notebook in this same order. Pause if a prerequisite is unclear.'
  s['sequence_number']=n
 slides[:]=result
 AUDIT.append(dict(cohort=cohort,week=week,reviewed_original_slides=len(original),final_slides=len(result),placed_sources=[s['sequence_source'] for s in result],replaced=spec['replaced']))
