"""Concrete, observable activities and layout semantics for novice PowerPoint lessons.
Public assessment contracts remain supplied by prepare_beginner_ppt_content.py.
"""
from beginner_pathway import WEEKS
import re
ASSET='figs/experiential/'
EXPLANATIONS={
7:[('Rehearse before test day','Use the separate practice notebook before the timed session.\n\nOpen the supplied data and run a familiar calculation.\n\nThe test packet and permitted resources are issued by the lecturer.'),('Save both required files','Save the notebook and the separate typed Part B document.\n\nLocate both files in the designated local folder.\n\nReopen them to check that your latest work was saved.'),('Follow the published test procedure','Read the briefing before starting assessed work.\n\nUse only the resources permitted for that part of the test.\n\nReport a technical failure to the invigilator immediately.')],
14:[('Preparation happens before the test','Practise the already taught error calculations and data-splitting rules.\n\nUse separate practice values.\n\nThe timed session follows the issued test instructions.'),('Rehearse the offline save procedure','Save your notebook on the prepared lab computer.\n\nSave the typed Part B evidence as a separate file.\n\nLocate and reopen both files without internet.'),('A result needs an explanation','Name the target and its unit or class.\n\nExplain which data fitted preprocessing and which data evaluated the model.\n\nA high score alone does not establish a useful engineering model.')],
15:[('A six-minute presentation','Minutes 1–2: explain the question and data.\n\nMinutes 3–4: show the method and one supported result.\n\nMinutes 5–6: explain limitations, contributions and a next step.'),('Make the evidence readable','Name the chart axes and their units.\n\nState the measured evaluation result and how you obtained it.\n\nPoint to the particular table, plot or calculation that supports your claim.'),('Explain the limits honestly','State what your investigation can support.\n\nIf an answer is unknown, say what evidence would resolve it.\n\nTeaching data alone do not establish readiness for real operation.')],
2:[('A notebook has two kinds of cell','A code cell contains Python instructions and a run button.\n\nA text cell contains an explanation. It does not run Python.\n\nThe output appears below the code cell that produced it.'),('Four symbols in our first program','= assigns the value on the right to the name on the left.\n\n+ adds numbers. print(...) displays a value.\n\n# starts a comment for the person reading the code.'),('The session remembers earlier values','The first cell assigns 12 to readings.\n\nThe next cell adds 5 to the value currently stored.\n\nRunning only the second cell again adds another 5.')],
3:[('A calculation has inputs and an answer','Inputs are the values supplied to a calculation.\n\nAn operation combines them, such as length multiplied by width.\n\nThe result needs a unit, such as square metres.'),('A reusable calculation','def begins a function definition. The name identifies the calculation.\n\nParameters are names for the inputs. A colon and indentation mark the body.\n\nreturn sends a result back when the function is called.'),('Following a function call','double_value(4) puts 4 into the parameter x.\n\nx * 2 calculates 8. return passes 8 back.\n\nprint displays that returned value. A guard can return early when an input is invalid.')],
4:[('A list position starts at zero','In [2, 4, 6], position 0 holds 2.\n\nPosition 1 holds 4. Position 2 holds 6.\n\nThere is no position 3 in this three-item list.'),('A mean uses a total and a count','Start the total at 0. Add 2, then 4, then 6.\n\nThe final total is 12. The count is 3.\n\n12 / 3 gives the mean 4. An empty list needs a separate rule.'),('A CSV row becomes a dictionary','The header gives field names, such as unit and reading.\n\ncsv.DictReader returns one dictionary for each data row.\n\nThe value "2.5" starts as text. float("2.5") makes the number 2.5.')],
5:[('A table keeps related observations together','Our four rows record building A twice and building B twice.\n\nEach row contains the building label and an energy reading.\n\nkWh is energy. kW is power. The units describe different quantities.'),('A DataFrame is a labelled table','pandas is a library: a collection of reusable Python tools.\n\npd is the short name used after import pandas as pd.\n\npd.DataFrame(...) builds a table. pd.read_csv(...) loads one from a CSV file.'),('Selection and grouping answer different questions','A comparison produces True or False for every row.\n\nFiltering keeps rows whose comparison is True.\n\nGrouping collects rows with the same label before calculating a total or mean.')],
6:[('Filling a gap adds an estimate','The valid readings, sorted, are 20, 22, 24 and 80.\n\nThe two middle values are 22 and 24. Their mean is 23.\n\nUsing 23 for a blank is a declared cleaning rule. It does not recover the lost measurement.'),('Every cleaning change needs a record','A duplicate record ID suggests a repeated observation.\n\nTwo different observations from the same equipment can both be valid.\n\nRecord the evidence, action, number of affected rows and limitation.'),('A scatter plot pairs two measurements','The horizontal axis gives the input value.\n\nThe vertical axis gives the corresponding reading.\n\nOne point represents one observation. A pattern alone does not prove causation.')],
8:[('What learning means in this example','Training supplies inputs and their known answers.\n\nThe model uses those examples to choose its internal numbers.\n\nPrediction applies the fitted model to inputs whose answer we want to estimate.'),('Rows must stay paired with their answers','Each inner list in X_train is one observation.\n\ny_train contains one target value for each row, in the same order.\n\nChanging the order of only one list attaches answers to the wrong observations.'),('Creating, fitting and predicting','LinearRegression() creates a model that has not learned yet.\n\nfit(X_train, y_train) learns from paired training examples.\n\npredict(new_inputs) returns estimates. The actual targets are absent from new_inputs.')],
9:[('Actual and predicted describe different things','Actual is the recorded reference answer.\n\nPredicted is the answer produced by our model.\n\nA correct prediction matches the reference. Class 1 means warning in this example.'),('Two fractions ask different questions','Precision divides correct warnings by all predicted warnings.\n\nRecall divides correct warnings by all actual warnings.\n\nIf the denominator is zero, apply the explicit convention in the issued brief.'),('A category decision can use a probability','A classifier may estimate the probability of class 1.\n\nA threshold converts that estimate into warning or no warning.\n\nLogistic regression is a classification model. Its probability estimates still need evaluation.')],
10:[('Repeated equipment needs group separation','Readings from the same equipment can share patterns.\n\nPutting that equipment in both training and validation can make evaluation too easy.\n\nFor a new-equipment question, keep every row for an equipment ID in one partition.'),('A learned cleaning value comes from training','The training readings are 20, 22 and 24. Their median is 22.\n\nA missing validation value receives the already learned 22.\n\nA new validation reading of 40 must not change the fitted median.'),('Leakage gives away information from the future','Suppose we predict a fault before an inspection.\n\nfinal_inspection_result exists only after the inspection.\n\nUsing it as an input would answer a different, easier question than the one we intended.')],
11:[('A percentage and its fraction','40% means 40 out of 100.\n\n40 / 100 gives 0.4.\n\nThis changes the representation. It adds no new observation.'),('A combined input needs a reason','An interaction multiplies two inputs.\n\nIt may help a simple model represent a joint pattern.\n\nAn interaction with degrees Celsius is an empirical feature, not automatically a physical law.'),('One change makes a comparison interpretable','Base MAE is 3.0. Extended MAE is 2.5.\n\nImprovement = base error minus extended error = 0.5.\n\nKeep the training rows, validation rows, model family and metric fixed.')],
12:[('Eligibility comes before ranking','First check every stated requirement for each candidate.\n\nReject a candidate that fails even one requirement.\n\nRank the eligible candidates using the published tie-break rule.'),('A tuple supplies an ordered ranking key','A tuple holds several values in order, such as (error, time, name).\n\nPython compares the first values. A tie moves the comparison to the second.\n\nIf those also tie, the third value decides.'),('A recommendation needs evidence','State the question and the chosen candidate.\n\nGive the evaluation result and the constraint it satisfies.\n\nState a limitation and the evidence that could change the recommendation.')],
13:[('Saved outputs can hide missing steps','A notebook can display an old answer after its inputs have changed.\n\nA fresh session begins without the old variables.\n\nRestarting and running all tests whether the stated order creates the result.'),('A path names where a file is found','A relative path is interpreted from the current working folder.\n\nPackage versions describe the software used to run the code.\n\nThe README must give both run instructions and data-access instructions.'),('Useful feedback identifies an exact repair','Vague feedback: "It does not work."\n\nUseful feedback: "Step 2 names data.csv, but the supplied file is readings.csv."\n\nThe repair is to make the instructions and actual filename agree.')],
}
ACTIVITIES={
2:('You are the notebook’s memory','Write 12 on paper. This is the current value.','Add 5 and replace the old number with the result.','Repeat only that addition once. What value remains?','22. Re-running the setup first would replace the value with 12 again.'),
3:('You are the function','One partner supplies the input 4.','The other follows the rule: multiply the input by 2.','Return the answer on paper, then repeat with input 7.','The returned answers are 8 and 14. The same instructions accept different inputs.'),
4:('You are the loop','Write the readings 2, 4 and 6 on separate scraps of paper.','Move through them once. Keep a running total and a count.','Add a fourth reading of 8. Predict the new mean before coding.','The new total is 20 and count is 4, so the mean is 5. Resetting the total inside the loop loses earlier additions.'),
5:('You are groupby','Make four cards: A:2, A:4, B:5, B:7. Values are kWh.','Put matching building labels together and add each pile.','Which pile has the greatest total? How many distinct buildings?','A totals 6 kWh. B totals 12 kWh. B is largest and there are 2 distinct buildings.'),
6:('You are the cleaning audit','Copy four records: A:20, B:blank, C:24, C:24.','Keep the original. In the copy, retain one C and fill the blank with the median of 20 and 24.','Write what changed and which value was estimated.','The working records are A:20, B:22, C:24. One duplicate was removed and one blank was filled. 22 is an estimate, not a recovered measurement.'),
7:('Before the timed test','Save a practice notebook in the designated local folder.','Save a separate typed practice explanation.','Close both files and locate them again without help.','Both files reopen. Rehearse using practice material before the assessed period, never during its working time.'),
8:('You are a prediction rule','Use the rule prediction = 10 + 2 × input.','For input 3, calculate the prediction before using Python.','The measured answer is 18. How large is the error?','Prediction is 16. The absolute error is 2 target units. A single result does not show that the model is useful in general.'),
9:('You are the confusion matrix','Make four paired cards: (actual 1, predicted 1), (1,0), (0,1), (0,0).','Place each into TP, FN, FP or TN. Read the actual label first.','Count the four cells. Then calculate precision and recall.','Each cell contains one card. Precision = 1 / 2 and recall = 1 / 2. The denominators count different sets of warnings.'),
10:('You are the data splitter','Write A1, A2, B1, B2, C1 and C2 on six cards. The letter identifies equipment.','Put equipment A in training, B in validation and C in final test.','Could A2 move to validation if the goal is new-equipment performance?','No. Keep A1 and A2 together for this question. This tiny activity illustrates separation, not sufficient evaluation sample size.'),
11:('You are the feature reviewer','Write base error 3.0 and extended error 2.5.','Calculate base minus extended, using the same target unit.','Change only extended error to 3.4. Does the conclusion stay the same?','Improvement changes from +0.5 to -0.4. The second comparison does not support retaining the feature.'),
12:('You are the model selector','Limits: error at most 3, time at most 10 ms. Candidates: A (3,2), B (1,20), C (3,1).','Cross out candidates that fail a limit.','Choose by lowest error, then lowest time among the remaining candidates.','B fails the time limit. A and C tie on error. C wins because 1 ms is lower than 2 ms.'),
13:('You are a new project user','Exchange your README and files with a partner.','The partner follows the instructions in a fresh session without verbal hints.','Record the first missing or ambiguous step, repair it and retry.','Success means the instructions produce the stated result. Record the observed issue rather than simply writing "works".'),
14:('Rehearsal before Practical Test 2','Calculate errors for actual [4,8] and predicted [5,6].','Save the notebook and a separate explanation of which data may fit preprocessing.','Locate both saved files in the required folder.','Absolute errors are 1 and 2, so MAE is 1.5. Fit preprocessing on training records. This rehearsal happens before test time.'),
15:('You are explaining to a colleague','State the project question in one everyday sentence.','Show one labelled result and say how you obtained it.','Name one limitation and one decision you personally contributed.','A strong explanation connects a claim to evidence and makes its limits clear. Avoid claiming deployment readiness from teaching data.')}
IMAGES={2:('measure_record_decide','Measurements become observations','Which object was measured? Which quantity was recorded?'),4:('list_dictionary','A position and a key find different things','Both examples return 4. Explain how each lookup finds it.'),6:('data_cleaning','A working copy preserves the original','Point to the estimated value and the removed repeat.'),9:('classification_cards','Every paired result belongs in one cell','Read actual first, then predicted. Explain the missed warning.'),10:('train_validate_test','Three sets have different jobs','Which set must stay sealed until choices are fixed?'),11:('feature_recipe','A physical relationship can form a feature','Explain each quantity and the unit of the result.'),13:('reproducible_handoff','Someone else needs to reproduce the result','Which instructions would a new user need?')}

# Additional gaps revealed by checking the first use of syntax in the actual examples.
PREREQUISITES={
3:[('Reading an error message',[['Message','Meaning','First check'],['NameError','A name is unavailable','Spelling and run order'],['TypeError','Wrong kind of value','Text versus number'],['SyntaxError','Python cannot parse a line','Quotes, brackets, colon'],['IndentationError','Block spacing is invalid','Consistent spaces']], 'The last line names the error. The indicated line shows where Python noticed it.'),('Comparison and logic',[['Symbol','Question','Example result'],['==','Are values equal?','3 == 3 is True'],['!=','Are values different?','3 != 4 is True'],['>=','At least the limit?','3 >= 3 is True'],['and','Are both conditions true?','True and False is False'],['or','Is either condition true?','True or False is True']], 'An assignment uses =. A comparison uses ==. Capitalise True, False and None.')],
4:[('A CSV file has a header and text values',[['CSV line','Dictionary meaning'],['unit,reading','Two field names'],['A,2.5','{"unit": "A", "reading": "2.5"}'],['B,','{"unit": "B", "reading": ""}']], 'An empty field is empty text. Check the task’s rule before converting it.')],
5:[('A chained expression is several small steps',[['Step','Expression','Result type'],['Group','df.groupby("building")','Grouped rows'],['Select','["kwh"]','One measurement per row'],['Add','.sum()','A total for each group'],['Find largest','.idxmax()','Label of a largest total']], 'Read the chain from left to right. State how a tie should be handled before relying on one label.')],
8:[('An object remembers its fitted state',[['Python expression','What it means'],['model = LinearRegression()','Create an unfitted model object'],['model.fit(X_train, y_train)','Learn from paired training data'],['model.predict(X_new)','Use that learned state'],['random_state=17','Name an option and set its value']], 'An object holds state and has methods. A method is a function used through that object.')],
9:[('Counting syntax in the example',[['Code','Equivalent idea'],['tp = tn = fp = fn = 0','Set each of four counts to zero'],['tp += 1','tp = tp + 1'],['zip(actual, predicted)','Pair items in the same positions'],['elif condition:','Try this branch if earlier ones failed']], 'Our paired lists must have matching lengths. zip alone stops at the shorter list.')],
12:[('Sorting with a named function',[['Expression','Meaning'],['key=rank','Use rank to build each comparison key'],['sorted(eligible, key=rank)','Return a newly ordered list'],['ordered[0]','Select its first item'],['len(ordered) == 0','Check for no eligible candidate']], 'Check for an empty list before accessing position zero.')]
}
PREREQUISITES[4].append(('Dictionary lookups and list slices',[
 ['Expression','Meaning'],
 ['readings[0]','The first list item'],
 ['readings[1:3]','Items at positions 1 and 2'],
 ['record.get("missing", 0)','Use 0 if that key is absent'],
 ['record.items()','Each key paired with its value']],
 'A default value is a stated rule. Choose it deliberately; zero is not automatically a suitable missing-data value.'))
PREREQUISITES[6]=[('Following a cleaning loop',[
 ['Expression','Meaning'],
 ['seen = set()','Start an empty collection of IDs'],
 ['record_id in seen','Has this ID already been recorded?'],
 ['continue','Skip the remaining lines for this item'],
 ['value is None','Check for Python’s no-value marker']],
 'An empty string "" and None are different values. Parse CSV fields according to the issued rule.')]
PREREQUISITES[8].append(('Reading NumPy results',[
 ['Expression','Meaning'],
 ['np.nan','A missing numeric value marker'],
 ['X.shape','The array dimensions: rows, columns'],
 ['predictions.round(2)','Round a new array to two decimal places'],
 ['predictions.tolist()','Convert the array into a Python list']],
 'Use rounded values only for a labelled display. Keep full precision when the assignment requires it.'))

def transform(slides,week,cohort):
    original=slides[:]; result=[]
    termtitles={' and '.join(t[0] for t in WEEKS[week]['terms'][i:i+2]) for i in range(0,len(WEEKS[week]['terms']),2)}
    explanations=iter(EXPLANATIONS.get(week,[])); usedterms=False
    for s in original:
        title=s['title']; base=title.removesuffix(' continued')
        if base in termtitles:
            if not usedterms:
                for i in range(0,len(WEEKS[week]['terms']),2):
                    terms=WEEKS[week]['terms'][i:i+2]
                    result.append(dict(title='Words we will use',kind='concepts',body='',concepts=[dict(term=a,meaning=b) for a,b in terms],notes='Explain each word with the nearby worked example. Ask learners to point to the corresponding value, line or table entry.'))
                usedterms=True
            continue
        if week in EXPLANATIONS and base in ('Understanding the example','Reading the instructions','Checking our reasoning','What happens next','Preparation and expectations'):
            if title.endswith(' continued'):continue
            item=next(explanations,None)
            if item:s.update(title=item[0],body=item[1])
        if title=='The engineering context':
            s['kind']='context';s['body']=s['body'].replace('Explain the quantities before using them.','A measurement includes a number and its unit.')
        if title=='Today’s learning':
            s['kind']='goals';s['body']='\n\n'.join(STUDENT_GOALS[week][:2]);s['check']=STUDENT_GOALS[week][2]
        if title=='Before you leave':
            s['kind']='exit';s['body']=STUDENT_GOALS[week][2]+'\n\nSave your work and check the required submission files.'
        if s.get('kind')=='cover':s['image']=ASSET+'engineering_studio.png'
        if s.get('kind')=='code':s['explain']=explain_code(s['code'])
        if week==3 and title=='Selecting a largest error without loops':
            result.append(dict(title='Reading a short list',kind='table',body='',table=[['Expression','Value','Why'],['errors = [-2, 5, -8]','Three signed errors','Brackets hold the list'],['errors[0]','-2','Positions start at zero'],['abs(errors[2])','8','abs gives the size'],['max(2, 5, 8)','8','max selects the largest']],caption='The bracketed number is a position. It is not the value stored there.',notes='Trace positions 0, 1 and 2. abs(-8) is 8. Use a new list for a prediction before running the example.'))
        result.append(s)
    # Insert vocabulary and visual intuition after recall. Practice is ungraded.
    intro=[]
    if week in IMAGES:
        name,title,prompt=IMAGES[week]
        intro.append(dict(title=title,body='',kind='scene',image=ASSET+name+'.png',caption=prompt,notes='Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration. '+('The working-copy rule is a toy activity, not the exact assessed cleaning policy.' if week==6 else '')+' Source: figs/experiential/ASSET_SOURCES.md.'))
    for title,rows,caption in PREREQUISITES.get(week,[]):intro.append(dict(title=title,body='',kind='table',table=rows,caption=caption,notes='Read one row at a time and use a changed value. This is a syntax reference for the worked examples.'))
    # Put syntax references immediately before the first worked code, after initial intuition.
    if intro:
        result[3:3]=[x for x in intro if x['kind']=='scene']
        pos=next((i for i,s in enumerate(result) if s.get('kind')=='code'),3)
        result[pos:pos]=[x for x in intro if x['kind']=='table']
    activity=ACTIVITIES[week]
    task=dict(title=activity[0],kind='activity',body='\n\n'.join(activity[1:4]),duration='5 minutes',notes='Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: '+activity[4])
    answer=dict(title='What the activity shows',kind='debrief',body=activity[4],notes='Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.')
    # Ordinary lessons: activity before independent practice. Exam decks: rehearsal before timetable.
    pos=next((i for i,s in enumerate(result) if s['title'] in ('Your turn','Test session','Preparation checkpoint')),len(result)-1)
    result[pos:pos]=[task,answer]
    for s in result:
        if not s.get('kind'):
            if re.match(r'(q\d:|\w+\()',s['title']):s['kind']='contract'
            elif s['title'] in ('Your turn','Recall and a first attempt','A change to predict','After the video'):s['kind']='question'
            elif s['title'] in ('Practice discussion','The practice result'):s['kind']='debrief'
            elif any(x in s['title'].lower() for x in ('assignment','evidence','submission','project','issued','test session','repair','files in')):s['kind']='steps'
            else:s['kind']='explanation'
        if s['kind'] in ('question','activity'):s['notes']+='\nWait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.'
    slides[:]=result


def explain_code(code):
    """Short syntax prompts selected only for constructs present in this displayed code."""
    cues=[]
    for_meaning=('for takes the next item. The indented block repeats.' if re.search(r'^\s*for .+:\s*$',code,re.M) else 'for visits each item inside this compact expression.')
    if_meaning=('if tests a condition. The chosen indented block runs.' if re.search(r'^\s*if .+:\s*$',code,re.M) else 'if tests which values to keep or which expression to use here.')
    checks=[
      ('import ', 'import loads a library. from selects a tool from it.'),
      ('def ', 'def names the function. Inputs go inside parentheses.'),
      ('for ', for_meaning),
      ('if ', if_meaning),
      ('return ', 'return sends the result back to the caller.'),
      ('.fit(', 'fit learns using the supplied training observations.'),
      ('.predict(', 'predict applies the fitted model to new inputs.'),
      ('float(', 'float converts numeric text into a decimal number.'),
      ('type(', 'type reports the kind of value: for example, float.'),
      ('zip(', 'zip pairs items at matching positions in these equal-length lists.'),
      ('print(', 'print displays a value below the cell.'),
      ('.append(', 'append adds one item to the end of a list.'),
      ('[', 'Square brackets create a list or select an item.'),
      ('{', 'Braces hold dictionary key: value pairs here.'),
      (' = ', '= assigns the value on the right to the name on the left.')]
    for token,meaning in checks:
        if token in code:cues.append(meaning)
    return cues[:3] or ['Read the inputs and identify the operation.','Predict the result before running this cell.']

STUDENT_GOALS={
2:('Run a code cell and find its output.','Restart, save and reopen your main notebook.','You can explain why running the same cell again may change its output.'),
3:('Read Python values and arithmetic symbols.','Define a function, call it and check its inputs.','You can explain each input, the returned answer and its engineering unit.'),
4:('Read lists and dictionary fields.','Trace a loop, read CSV rows and calculate summaries.','You can show how the total and count change for each record.'),
5:('Read a labelled table and select rows.','Calculate column summaries and grouped totals.','You can explain which observations a filter keeps and what a grouped total means.'),
6:('Recognise missing values and repeated records.','Make a working copy and record each cleaning action.','You can justify a change, show its effect and identify an estimated value.'),
7:('Rehearse saving and reopening the required files.','Check the published test rules before the session.','You can locate both your notebook and typed reasoning document without help.'),
8:('Identify prediction inputs and a measured target.','Fit a simple model and compare prediction errors.','You can calculate one error and explain why evaluation needs unseen observations.'),
9:('Distinguish an actual label from a predicted label.','Count prediction outcomes and explain their costs.','You can identify a false negative and explain precision and recall with counts.'),
10:('Keep related equipment records together.','Separate training, validation and final testing.','You can identify which records may influence preprocessing and model selection.'),
11:('Create a feature from available measurements.','Compare models with one controlled change.','You can state the new feature’s meaning and calculate an improvement correctly.'),
12:('Check model requirements before ranking candidates.','Apply the tie-break rule and explain the choice.','You can justify a valid candidate with evidence and a stated limitation.'),
13:('Run the project from a fresh session.','Repair unclear run instructions using peer feedback.','Another learner can follow your README and reproduce the stated result.'),
14:('Rehearse previously taught modelling decisions.','Practise saving both required test files offline.','You can explain training-only preprocessing and locate your saved evidence.'),
15:('Explain your question and one supported finding.','State a limitation and your individual contribution.','You can point to the evidence behind one decision you personally worked on.')}
