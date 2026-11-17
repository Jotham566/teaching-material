"""Prerequisite-led teaching revision. Preserve issued assessment interfaces.

Apply after the legacy sequence and reviewed-notes overlay. The exported JSON
is the reproducible source for the PPTX and matching practice notebooks.
"""
import copy, re

def prose(title,*body,notes=''):
 return dict(title=title,kind='explanation',body='\n\n'.join(body),notes=notes)
def code(title,program,caption,explain=()):
 return dict(title=title,kind='code',body='',code=program,practice_code=program,caption=caption,explain=list(explain),notes=caption+'\n\n'+program)
def table(title,rows,caption):
 return dict(title=title,kind='table',body='',table=rows,caption=caption,notes=caption)

COLLECTIONS=[
 prose('One value and a collection of values','A variable can refer to one value: reading = 98. A collection stores several related values under one name.','Python has several collection types. Choose one according to how you need to find, change or organise its contents.'),
 table('Lists dictionaries tuples and sets', [['Type','Example','Choose it for'],['list','[98, 105, 92]','Values in a changeable order'],['dict','{"reading": 98}','Values found by named keys'],['tuple','(2, 3)','Positions you will not reassign'],['set','{"A", "B"}','Distinct items and membership']], 'List and tuple positions start at zero. Dictionaries use keys. Sets have no positional index.'),
 prose('A list stores values in positions','readings = [98, 105, 92] creates a list. Square brackets enclose the items; commas separate them.','An index is an item’s position. Python starts counting at zero: readings[0] is 98, readings[1] is 105, readings[2] is 92.','Three items have positions 0, 1 and 2. readings[3] raises IndexError because there is no fourth item.'),
 code('Creating and reading a list','readings = [98, 105, 92]\nprint(readings)\nprint(readings[0])\nprint(len(readings))','Output: [98, 105, 92], then 98, then 3.', ['[ ] creates a list or selects a position.','len counts the items; it is a built-in function.']),
 prose('Choosing the right collection','A dictionary connects a key to a value: {"reading": 98}. The colon connects them; record["reading"] finds the value by its key.','A tuple such as (2, 3) stores ordered items whose positions cannot be reassigned. A set such as {"A", "B"} stores distinct items without positions.','We use a list for today’s readings because their order matters. Week 4 develops dictionary, tuple and set operations before we use them with records.'),
 prose('A method belongs to a value','A function is called by name: len(readings). A method is called through a value with a dot: readings.index(105).','index searches a list for a value and returns its first position. Here readings.index(105) returns 1. A missing value raises ValueError.','The parentheses contain inputs to the operation. The square brackets in readings[1] select an item; they do a different job.')]

W4_COLLECTIONS=[
 prose('A dictionary is a record with named fields','record = {"unit": "A", "reading": 4} stores two key–value pairs. Keys name fields; values hold the information.','Braces enclose the dictionary. A colon separates each key from its value and a comma separates pairs. Each key is unique.','record["reading"] returns 4. Unlike a list position, "reading" names the field we want.'),
 code('Reading and updating a dictionary','record = {"unit": "A", "reading": 4}\nprint(record["reading"])\nrecord["reading"] = 6\nprint(record["reading"])\nprint(record.get("missing", 0))','Output: 4, then 6, then 0. get uses the fallback only when that key is absent.', ['["reading"] selects a key, not a position.','Assigning through the key updates its value.']),
 prose('Tuples and unpacking','A tuple stores items in order. point = (2, 3) stores two coordinates; point[0] is 2. You cannot reassign point[0].','x, y = point gives the first item to x and the second to y. This is unpacking; the number of names must match the number of items.','A tuple prevents replacing its positions. It does not freeze the contents of a mutable object stored inside it.'),
 code('Unpacking a pair','point = (2, 3)\nx, y = point\nprint(x)\nprint(y)','Output: 2, then 3.', ['Two names receive the two items in order.']),
 prose('A set remembers distinct items','A set is useful when the question is “Have we seen this ID?” It keeps one instance of each distinct item.','seen = set() creates an empty set. seen.add("A") adds an item. "A" in seen asks whether it is present.','Do not use a set when position or repeated readings matter. Sets cannot be indexed. {} creates an empty dictionary, not an empty set.'),
 code('Set membership and repeated IDs','seen = set()\nseen.add("A")\nseen.add("A")\nprint(len(seen))\nprint("A" in seen)\nprint("B" in seen)','Output: 1, True, False. Adding the same ID twice keeps one distinct ID.', ['in returns True or False.','A set answers membership questions.']),
 table('How the four collections differ',[['Collection','Find an item by','Repeats / changes'],['list','Position: values[0]','Repeats allowed; items change'],['dict','Key: record["reading"]','Keys unique; values change'],['tuple','Position: point[0]','Repeats allowed; positions fixed'],['set','Membership: "A" in seen','Distinct items; add or remove']], 'Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.')]

CONTEXT={3:'Use one engineering calculation to connect numbers, named inputs, decisions and returned answers. Then store several readings in a list to compare their errors.',4:'Sensor readings arrive as records in a CSV file. We first learn the Python collections and loops needed to read those records and summarise them.',5:'The supplied campus_energy.csv records campus electricity use. We practise pandas on four invented rows first, then inspect the supplied file and its units.',6:'A repeated record or a missing measurement can change a summary. We keep the original records, apply the stated cleaning rules and explain each change before plotting.',8:'A regression model predicts a numerical engineering target from measurements available beforehand. The small invented data explain the code; they do not establish real-world accuracy.',9:'A warning system predicts a category. We compare each prediction with its recorded answer, then count false alarms and missed warnings using an explicit cost rule.',10:'We want evidence about new equipment or future observations. The way we separate data must match that use before any model or preprocessing learns from it.',11:'A calculated input may help a model. We compare the original and extended inputs on the same observations, then decide whether the evidence supports the extra feature.',12:'The lowest prediction error may come from a model that is too slow for the stated task. We apply the published constraints before ranking eligible models.',13:'A project is ready for handover when its files and written instructions reproduce its results in a fresh session. Today we check that evidence ourselves.'}
RECAP={3:'From slides 1–12: values have types, variables name values, = assigns, and print displays a result. float("3.5") converts text to a number. We now use those ideas in calculations and functions.',4:'Week 3 introduced values, function inputs and results, conditions and list positions. Now we repeat a calculation across records, then organise those records by keys.',5:'Week 4 used lists, dictionaries, loops and CSV rows. pandas keeps these same records in a labelled table and provides operations that work across its columns.',6:'Week 5 selected and summarised columns. Before trusting those summaries, inspect missing values, repeated observations and measurement units.',8:'Weeks 3–6 supplied Python, tables, cleaning and charts. We now use paired inputs and known answers to fit a prediction rule.',9:'Week 8 predicted a number. This week predicts a category and counts the different kinds of correct and incorrect result.',10:'We have compared predictions with known answers. Now we control which observations may influence training, choices and the final evaluation.',11:'We already keep evaluation data separate. Now we change one input representation while keeping the comparison protocol fixed.',12:'We already calculate validation errors. Now we combine those errors with a practical constraint and an explicit tie-break rule.',13:'The models and charts already exist. The remaining task is to make the evidence understandable and runnable from the supplied files.'}
TOPICS={3:'Functions and their inputs',4:'Lists loops and records',5:'pandas tables and summaries',6:'Cleaning decisions and charts',7:'Practical Test 1 preparation',8:'Regression models and errors',9:'Classification outcomes',10:'Validation and leakage',11:'Feature comparisons',12:'Model selection',13:'Project handover',14:'Practical Test 2 preparation',15:'Project presentation'}

def revise(deck):
 if deck['week']<3:return deck
 d=copy.deepcopy(deck);w=d['week'];cohort=d['cohort'];old=d['slides'];new=[];videos=[]
 skip={'What the activity shows'}
 if w==3:skip|={'A calculation has inputs and an answer','A reusable calculation','A change to predict','The practice result','Following a function call','Reading a short list','Quantities and units'}
 if w==4:skip|={'Dictionary','Read dictionary operations','Dictionary lookups and list slices','A dictionary gives each value a key','Three ways to collect values'}
 if w==5:skip|={'A DataFrame is a labelled table','Selection and grouping answer different questions'}
 if w==6:skip|={'Copying records and recognising repeats'}
 if w==9:skip|={'Two fractions ask different questions','Probability and a warning decision'}
 if w==10:skip|={'A training-only fill value'}
 for i,s0 in enumerate(old):
  s=copy.deepcopy(s0);title=s['title'];s['_original_slide']=i+1
  if title in skip or s.get('kind')=='activity':continue
  if title=='Short explainer and discussion':
   s['title']='Optional revision video';s['body']='For revision after class.\n\n'+s['body'];videos.append(s);continue
  if title=='After the video':continue # listening question stays with the link
  if w==3 and i==12:
   new.append(prose('Week 3 continuation',RECAP[3],'Next: arithmetic, decisions, functions, then lists and the A3 brief.',notes='For CML3112 resume here after teaching original slides 1–12. Briefly show the output from the previous example: 7.0 and <class \'float\'>. No need to reteach all twelve slides.'))
  if title=='The engineering context' and w!=3:s['body']=CONTEXT[w];s['kind']='explanation';s['title']='Why this week’s tools are needed'
  if title=='Recall and a first attempt' and w!=3:
   s['title']='Connection to the previous lesson';s['body']=RECAP.get(w,s['body']);s['kind']='explanation'
  if title=='Words we will use' and not(w==3 and i<12):s['title']=' and '.join(c['term'] for c in s.get('concepts',[])) or TOPICS[w]
  if title=='Your turn':
   answer=next((x.get('body','') for x in old[i+1:i+3] if x['title']=='Practice discussion'),'')
   s['title']='Revision example and answer';s['kind']='explanation'
   s['body']='Example: '+s['body']+'\n\nAnswer: '+answer
   if w==13:s['body']='Check: restart the notebook runtime and follow your README exactly, without using remembered variables.\n\nIf Step 2 names data.csv but the file is readings.csv, correct the filename in the instructions. Run again from the beginning and record the successful result.'
  if title=='Practice discussion':continue
  if w==3 and title=='Selecting a largest error without loops':
   new+=copy.deepcopy(COLLECTIONS)
   s['body']='An error is measured − expected. Its sign shows the direction. abs gives its magnitude: abs(-8) is 8.\n\nmax finds the largest supplied value: max(2, 5, 8) is 8. Compare magnitudes when the task asks for the largest error by size.\n\nKeep the original signed error as well, because the magnitude alone loses direction.'
  if w==3 and title=='Worked example':
   s['title']='Defining and calling double_value';s['code']='def double_value(x):\n    return x * 2\n\nanswer = double_value(4)\nprint(answer)';s['practice_code']=s['code'];s['caption']='Output: 8. Calling passes 4 to x; return sends 8 back; print displays it.'
  if w==3 and s.get('code')=='print(double_value(4))':continue
  if w==3 and title=='Worked example continued':
   if s.get('code','').startswith('def safe_share'):
    new.append(prose('An input check before division','Division by zero raises ZeroDivisionError. We choose to return None when people is zero, so there is no calculated share.','The check belongs inside the function, before the division. return ends that call immediately. A valid input follows the later return line.'))
    s['title']='A function with a zero-input check';s['code']+='\n\nprint(safe_share(12, 3))';s['practice_code']=s['code'];s['caption']='Output: 4.0. safe_share(12, 0) returns None before any division.'
   elif s.get('code')=='print(safe_share(12, 3))':continue
  if w==3 and title=='Expected output':continue
  if w==3 and title=='Read the quantities before the formulas':
   s['body']='Mass measures matter in kilograms (kg). Weight is a force in newtons (N): mass × gravitational acceleration. The assignment uses g = 9.81 m/s².\n\nPower is energy transferred per second, in watts (W). Efficiency in percent = 100 × useful output power / input power.\n\nA named constant stores a value kept fixed in the calculation. Uppercase names such as G are a convention, not a Python restriction.'
  if w==3 and title=='Units branches and error messages':
   s['title']='Unit conversions for the assignment';s['body']='Millimetres become metres by dividing by 1000: 200 mm is 0.2 m.\n\nPercent becomes a fraction by dividing by 100: 75% is 0.75.\n\nOnly for rotational-speed questions: rpm means revolutions per minute. One revolution is 2π radians and one minute is 60 seconds, so multiply rpm by 2π/60.'
  if w==3 and title=='Units branches and error messages continued':
   if 'FIRST' in s.get('body',''):
    s['title']='More than two branches';s['body']='if tests the first condition. elif means “otherwise, if” and tests another condition only if the earlier one was false. else handles the remaining case.\n\nPython runs only the first matching branch. Put a narrower condition before a broader one that would also match. A colon and indentation mark each body.'
    new.append(s)
    new.append(code('Tracing an if elif else chain','level = 7\nif level >= 10:\n    print("high")\nelif level >= 5:\n    print("medium")\nelse:\n    print("low")','Output: medium. The first condition is false; the second is true.',['elif is checked only after the earlier condition fails.']))
    continue
   else:continue
  if w==4 and title=='A position and a key find different things':
   new+=copy.deepcopy(W4_COLLECTIONS)
   new.append(prose('Dictionary items and two loop names','record.items() provides each key with its value as a pair. The loop unpacks each pair into the names key and value.','for key, value in record.items(): repeats the indented body for each field. Use .items() when both the label and its value are needed.'))
   new.append(code('Looping through named fields','record = {"unit": "A", "reading": 6}\nfor key, value in record.items():\n    print(key, value)','Output: unit A, then reading 6. The dictionary preserves insertion order.',['.items() supplies pairs.','key and value are names chosen for this loop.']))
  if w==4 and title=='A record and a growing list':new.append(prose('A list of dictionaries','A record holds named fields for one observation. A list of records holds several observations in order.','records[0] selects the first dictionary. records[0]["reading"] then selects that dictionary’s reading field.','for row in records takes one dictionary at a time. row["reading"] retrieves that observation’s field; float converts numeric text when needed.'))
  if w==4 and title=='Expected output':
   new.append(s)
   new.append(code('Built-in summaries of a list','readings = [2, 4, 6]\nprint(sum(readings))\nprint(len(readings))\nprint(min(readings))\nprint(max(readings))','Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.', ['These functions are built into Python.','min and max require a nonempty list here.']))
   continue
  if w==5 and title=='A chained expression is several small steps':
   # Present the simple total before the illustration of the longer chain.
   continue
  if w==5 and title=='Unique labels and the largest group':
   new.append(prose('Reading a chain one operation at a time','df.groupby("building") groups rows by their building labels. ["kwh"] selects the energy values within each group. .sum() totals them.','Store this result in totals. totals.idxmax() returns the label with the largest total. These are consecutive operations on the result of the previous step.'))
  if w==6 and title=='A chart with labelled axes':s['body']='matplotlib is a plotting library. plt is the short name we give its pyplot module.\n\nfig, ax = plt.subplots() returns two objects: fig is the whole figure; ax is its plotting area. scatter places the paired measurements as points.\n\nax.set_xlabel(...) labels the horizontal axis. set_ylabel labels the vertical axis. Keep fig when the task asks you to return a Figure object.'
  if w==8 and title=='Worked example':new.append(prose('Where the modelling tools come from','scikit-learn is an installed machine-learning library. Its Python import name is sklearn. linear_model is the part containing LinearRegression.','from sklearn.linear_model import LinearRegression makes that model class available. LinearRegression() creates an individual model object.','In Colab this library is normally available. If an import fails, use the course setup instructions and retry the import before running model code.'))
  if w==8 and title=='Rows and arrays before model code':
   new.append(prose('A matrix is a rectangular table of numbers','A matrix has rows and columns. For modelling, one row is one observation and each column is one input feature.','[[1, 20], [2, 22]] has two rows and two columns. The outer list contains rows; each inner list contains that row’s features.','X is a conventional name for this input table. y holds one known target per row. These names have no special power in Python.'))
  if w==9 and title=='Counting arbitrary paired observations':s['body']+='\n\ntp = tn = fp = fn = 0 sets all four counters to zero. tp += 1 is shorthand for tp = tp + 1.'
  if w==10 and title=='Cross-validation':new.append(prose('Parameters hyperparameters and a fold','A parameter is learned during fitting, such as a line’s slope. A hyperparameter is a setting chosen around fitting, such as a tree’s max_depth.','A fold is one part of the development data used for a validation turn. Refit the entire preprocessing and model on the other parts for that turn.','Compare candidate settings using validation evidence. Keep the final test outside that selection process.'))
  if w==12 and title=='Worked example (1/2)':new.append(prose('Candidate records and eligibility','A candidate is one model under consideration. Its dictionary records a name, a validation error and measured run time.','An eligible candidate meets every published constraint. Build a list of eligible records first. If the list is empty, use the task’s specified no-candidate result.'))
  if w==13 and s.get('concepts'):
   for c in s['concepts']:
    if c['term']=='Peer review':c.update(term='Independent run check',meaning='Restart the session and follow your written instructions without relying on earlier variables. Record the first failure and its repair.')
   if 'Peer review' in s['title']:s['title']='Run checks and contribution evidence'
  if w in (7,14):
   s['body']=s.get('body','').replace('both required test files','the complete test notebook').replace('both required file types','the complete notebook').replace('both required files','the complete notebook')
  # Every slide should support independent revision and preserve current assessment rules.
  for key in ('body','caption','check'):
   if isinstance(s.get(key),str):
    s[key]=s[key].replace('using peer feedback', 'using a fresh run').replace('Read the code together. Predict the result before running.','Read top to bottom. Run the complete example in the matching practice notebook.').replace('Ask a partner to follow your README without verbal help.','Follow your README yourself in a fresh session.')
  new.append(s)
 # Place prerequisite explanations next to their first use, not late in revision.
 if w==3:
  block=[x for x in new if x['title'] in ('More than two branches','Tracing an if elif else chain')]
  new=[x for x in new if x not in block]
  pos=next(i for i,x in enumerate(new) if x['title']=='Function')
  new[pos:pos]=block
  for x in new:
   if x['title']=='Arithmetic that needs care':
    x['body']='Parentheses run first: (2 + 4) / 2 is 3.0. Without them, division runs before addition: 2 + 4 / 2 is 4.0.\n\n/ gives a quotient. // rounds that quotient down: 7 // 2 is 3 and -7 // 2 is -4.\n\nMany decimal fractions are approximate in a computer. A tolerance is an allowed difference, for example 0.01 m when checking two calculated lengths.'
   if x['title']=='Comparison and logic':x['caption']='> means greater than; < means less than; <= means at most. = assigns, while == compares. True and False are Boolean values.'
 if w==9:
  names=('Probability and a decision threshold','A category decision can use a probability')
  block=[x for x in new if x['title'] in names];new=[x for x in new if x not in block]
  pos=next(i for i,x in enumerate(new) if x['title']=='Threshold and cost');new[pos:pos]=block
  for x in new:
   if x['title']=='A category can become indicator columns':x['caption']='An encoder converts category labels to numeric columns. Fit it on training data. Each indicator is 1 when that category applies, otherwise 0.'
 # Videos are optional revision, after all taught material and submission directions.
 new+=videos
 from iuea_explicit_foundations import expand
 new=expand(new,w,cohort)
 for i,s in enumerate(new):
  s['sequence_number']=i+1
  title=s['title']
  captions={
   'Inputs, instructions and a returned result':'The illustration uses slab_volume: length × width × thickness. The next function uses the same input/body/return pattern.',
   'A loop changes the running total':'This illustration uses six separate readings. Next we trace the smaller list [2, 4, 6] using the same running-total rule.',
   'A labelled table in Python':'The illustration uses machinery records. The same row, column and index structure applies to our building-energy table.',
   'A comparison creates a Boolean mask':'The illustration filters torque readings. Our next example applies the same True/False selection to kWh values.',
   'A working copy preserves the original':'In this separate four-record example, remove one repeated C record and fill B with (20 + 24) / 2 = 22.',
   'Choosing a chart for the question':'This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.',
  }
  if title in captions:s['caption']=captions[title]
  if title.startswith('Worked example'):
   s['title']=TOPICS[w]+' in Python'+(' '+title[len('Worked example'):].strip() if title!='Worked example' else '')
  if title=='Expected output':s['title']=TOPICS[w]+' results'
  if title=='Before you leave':s['title']='Revision and submission checklist'
  prior=new[i-1]['title'] if i else 'the preceding week'
  following=new[i+1]['title'] if i+1<len(new) else 'independent revision and the issued task'
  evidence=s.get('caption') or s.get('body') or '\n'.join(c['term']+': '+c['meaning'] for c in s.get('concepts',[]))
  original=s.get('notes','')
  # Old keyword-matched explanations sometimes described another topic. Keep only
  # a specific lecturer cue and references, not old connect/next/check blocks.
  cue=re.search(r'LECTURER CUE\n(.*?)(?=\n\n[A-Z][A-Z ]+\n|$)',original,re.S)
  cue=cue.group(1).strip() if cue else ''
  cue='\n'.join(line for line in cue.splitlines() if not re.search(r'partner|ask pairs|exchange your|form groups|make.*cards|swap roles',line,re.I))
  detail=[]
  if s.get('body'):detail.append(s['body'])
  for c in s.get('concepts',[]):detail.append(c['term']+': '+c['meaning'])
  if s.get('table'):
   detail+=[' | '.join(str(v) for v in row) for row in s['table']]
  if s.get('code'):detail.append('Read the code in this order:\n'+s['code'])
  detail+=s.get('explain',[])
  if s.get('caption'):detail.append(s['caption'])
  if s.get('expected_stdout'):detail.append('Expected printed output:\n'+s['expected_stdout'].rstrip())
  if s.get('foundation_expansion'):detail.append(original)
  explanation='\n\n'.join(detail) or evidence
  references='\n'.join(line for line in original.splitlines() if line.startswith(('https://','Source:','Reference:')))
  s['notes']=f"PURPOSE\n{s['title']}\n\nCONNECT\nPrevious slide: {prior}.\n\nEXPLAIN\n{explanation}\n\nLECTURER CUE\n{cue or 'Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.'}\n\nTEACHING MODE\nDemonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.\n\nNEXT\n{following}.\n\nREFERENCES\n{references}"
  s.pop('_original_slide',None)
 d['slides']=new
 return d
