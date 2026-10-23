"""Build only the coding-only Test 1; preserve Test 2 and collection settings."""
import csv,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';G=BASE/'grader'
sys.path.insert(0,str(G))
from engineering_contracts import DOMAINS,dataset
from test1_coding_contracts import VERSION,PARTS
from build_colab_exams import cell

TASKS=[
('EDA before cleaning', 'explore_data(input_records)', '''First read `engineering_data.csv` with pandas, using `file_path`, and store the table in `raw_data` (2 marks). The file is in the current folder, so its name is the relative file path.

Then use the original data, including its errors. Calculate and return:
- `preview`: the first five rows as a DataFrame (2 marks).
- `rows` and `columns`: the two dimensions (2 marks together).
- `missing`: missing-value count for each column as a Series (2 marks).
- `duplicates`: repeated record IDs after the first occurrence (2 marks).
The return dictionary is supplied. Replace each `None` with your calculation. Do not clean this table. The supplied run cell also calls `info()` to show data types and recorded counts, and `describe()` to show numeric summaries; these inspection commands carry no extra marks.''',
'''    raw_data = pd.DataFrame(input_records)
    return {"preview": None, "rows": None, "columns": None,
            "missing": None, "duplicates": None}''',
'print(explore_data(records))\nraw_data.info()\nprint(raw_data.describe())',15),
('Visualisation before cleaning', 'plot_observations(input_records, target_unit, chart_title)', '''Create one scatter chart from the original table: `load_pct` on the horizontal axis and `target` on the vertical axis. Keep repeated observations and invalid loads in this BEFORE chart. Matplotlib does not draw pairs with a missing coordinate; do not fill or clean the data for this chart.
Return the supplied `figure`. Plot the correct points (4 marks), add the supplied `chart_title` (2), label the horizontal axis with load and percent (2), and label the vertical axis with target and the supplied `target_unit` (2). Colour and styling are your choice.''',
'''    raw_data = pd.DataFrame(input_records)
    figure, axes = plt.subplots()
    # Add scatter points, title and axis labels here.
    return figure''',
'before_figure = plot_observations(records, TARGET_UNIT, "Before cleaning")\nplt.show()',15),
('Clean the data', 'clean_observations(input_records)', '''Work on a copy. Apply these rules IN ORDER:
1. Keep the first occurrence of each `record_id`.
2. Exclude rows with a missing `target` or `load_pct` outside 0–100 inclusive. Keep valid boundary values 0 and 100.
3. Calculate the median `ambient_c` from the retained rows, ignoring missing values. Fill only missing ambient temperatures with this median.
Return the cleaned DataFrame with the same five columns and original row order. Do not change equipment labels or known measurements. Index numbers do not matter. Do not remove rows merely because they have a high target.
The grader gives 4 marks for each correctly retained column (record IDs, equipment IDs, loads, temperatures and targets).''',
'''    raw_data = pd.DataFrame(input_records)
    # Apply the three cleaning rules, then return cleaned_data.
    raise NotImplementedError("Complete cleaning")''',
'cleaned_data = clean_observations(records)\nprint(cleaned_data.head())\nprint(cleaned_data.isna().sum())\ncleaned_records = records_from_table(cleaned_data)',25),
('Visualisation after cleaning', 'plot_cleaned(input_records, target_unit, chart_title)', '''The input now contains CLEANED observations. Make the same load/target scatter chart so it can be compared with the BEFORE chart. Use the supplied title and target unit. Return a Figure, not an image filename or text.
Correct cleaned points: 4 marks; title: 2; horizontal axis with percent: 2; vertical axis with target units: 2. You may reuse or call your Task 2 function. No written comparison is required.''',
'''    cleaned_data = pd.DataFrame(input_records)
    figure, axes = plt.subplots()
    # Add scatter points, title and axis labels here.
    return figure''',
'after_figure = plot_cleaned(cleaned_records, TARGET_UNIT, "After cleaning")\nplt.show()',10),
('Calculate statistics', 'calculate_statistics(input_records)', '''Use CLEANED data. Return the following six entries in the supplied dictionary (2.5 marks each):
- `mean`, `sum`, `median`, `count`, `std`: calculated from the `target` column.
- `mode`: ALL most frequent equipment IDs, as a list in alphabetical order, calculated from `equipment_id`.
Use pandas' sample standard deviation (`.std()`, default `ddof=1`). Do not round returned answers. The sum is a descriptive calculation across observations, not a total-energy measure or a safety conclusion.
**Reference provided for this test:** mean is the average; sum adds values; median is the middle value; count counts recorded values; standard deviation measures spread. `values.std()` returns sample standard deviation. Mode means most frequent: `labels.mode().tolist()` returns ALL tied modes as a list. For labels `A, A, B, B, C`, it returns `["A", "B"]`. You do not need to derive a statistical formula.''',
'''    cleaned_data = pd.DataFrame(input_records)
    return {"mean": None, "sum": None, "median": None,
            "count": None, "std": None, "mode": None}''',
'print(calculate_statistics(cleaned_records))',20),
('Group and aggregate', 'summarize_equipment(input_records)', '''Group CLEANED observations by `equipment_id`. Use `groupby` and `agg` to calculate the `mean`, `sum` and `count` of `target` for each equipment ID (5 marks per column).
Return a DataFrame whose index contains equipment IDs and whose columns are named `mean`, `sum`, `count`. Equipment order does not affect marks. Keep full numerical precision.
Reference: `table.groupby("group_column")["numeric_column"].agg(["mean", "sum", "count"])` applies several calculations to each group. Replace the placeholder column names with the required columns.''',
'''    cleaned_data = pd.DataFrame(input_records)
    # Return the grouped summary DataFrame.
    raise NotImplementedError("Complete grouping")''',
'print(summarize_equipment(cleaned_records))',15),
('A function with conditions', 'classify_load(load_pct)', '''Write a reusable function using `if`, `elif`, `else` and `return`. Its input is one valid numeric load percentage from the same dataset. Return exactly:
- `"low"` if load is below 40;
- `"medium"` if load is from 40 through 75 inclusive;
- `"high"` if load is above 75.
These are test categories, not engineering safety limits. Check both boundary values: 40 and 75 must return `"medium"`. Return the label rather than only printing it. The supplied run cell uses a load from your cleaned CSV.''',
'''    # Write the conditions and return one label.
    raise NotImplementedError("Complete load classification")''',
'first_load = cleaned_data["load_pct"].iloc[0]\nprint(first_load, classify_load(first_load))',15),
('A loop using the same data', 'count_load_bands(load_values)', '''Use a `for` loop to visit every load in the supplied list. Call `classify_load` for each load and increment the matching counter in the supplied dictionary. Return the dictionary after the loop. An empty list must return all three counts as zero.
The run cell gets this list from the CLEANED CSV. For `[20, 40, 75, 90]`, the result is `{"low": 1, "medium": 2, "high": 1}`. Do not type the final dataset counts by hand. If Task 7 is unfinished, you may put the same conditions inside this loop for partial credit.''',
'''    counts = {"low": 0, "medium": 0, "high": 0}
    # Loop over load_values and update counts.
    return counts''',
'load_values = cleaned_data["load_pct"].tolist()\nprint(count_load_bands(load_values))',20)
]

GUIDE_EXTRA='\n## Coding tasks and time plan\n10 minutes setup · 135 coding · 15 checking · 20 submitting.\n\nUse pandas, matplotlib and ordinary Python. Write only in the answer cells. Run the cells labelled “Run only”; do not edit them.\n\nKeep function names and return keys unchanged. The supplied first line turns input records into a DataFrame. Calculate from that input; the grader checks other values too. Later functions can earn marks even if cleaning is unfinished.\n'

def student_guide(course):
 return f"""# {course} Test 1 — Take-home practical
**Individual work · 100 marks · 3 hours from Start test**

1. Run **Check details and countdown**, then **Prepare CSV and libraries**.
2. In Task 1, write the pandas code to read the file into `raw_data`.
3. Complete Tasks 1–8 in order. Task 3 produces `cleaned_data`. Save regularly.
4. Run **Submit your test**, click the button, then open its form and press **Submit**. Wait for confirmation.

The timer includes setup, interruptions and submission. It stops at your personal deadline or the class cutoff, whichever comes first. To resume, use the same entry link, email and registration number; your timer does not restart.

No AI-generated answers or collaboration. If a support cell is changed or deleted, use **Edit → Undo**. If submission fails, contact your lecturer before the deadline.
"""+GUIDE_EXTRA

def build_test1():
 config=json.loads((ROOT/'data/colab_test_submission_config.json').read_text());helper=(BASE/'test_operations/colab_submit_cell.py').read_text()

 titles={task:entry[0] for (task,_),entry in zip(PARTS,TASKS)}
 for course,(domain,unit,*_) in DOMAINS.items():
  guide=student_guide(course)
  (BASE/'student_guides'/course/'TEST1.md').write_text(guide)
  for variant,seed in [('A',17),('B',29),('C',43)]:
   folder=BASE/'assessment_banks/TEST1'/course/variant
   rows=dataset(course,seed,dirty=True)
   with (folder/'engineering_data.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
   cells=[cell(guide),cell(f'FULL_NAME = ""\nEMAIL = ""\nSTUDENT_ID = ""\nCOHORT = "{course}"\nTEST_ID = "TEST1"\nVARIANT = "{variant}"\n',True),cell(f'''## Understand the supplied CSV
Each row is one synthetic observation of **{domain}**. This is a practice engineering dataset, not evidence for a real safety decision.

| Column | Meaning |
|---|---|
| record_id | Observation identifier, not time; a repeated ID is a duplicate |
| equipment_id | Equipment label; many observations can belong to the same equipment |
| load_pct | Load percentage; valid values are 0–100 inclusive |
| ambient_c | Ambient temperature, degrees Celsius |
| target | {domain}, in {unit} |

Blank cells become missing values in pandas. All tasks use this same CSV. Tasks 1–2 use RAW data; Task 3 cleans it; Tasks 4–8 use CLEANED data.

The supplied `records_from_table` helper converts a table into a list of row dictionaries. You do not need to write or change it. Each function's supplied first line converts those rows back into a DataFrame. This allows the grader to check different data without changing your code.'''),cell('import pandas as pd\nimport matplotlib.pyplot as plt\n\ndef records_from_table(table):\n    objects = table.astype(object)\n    return objects.where(table.notna(), None).to_dict("records")\n\nTARGET_UNIT = '+repr(unit)+'\nprint("Setup ready. Continue to Task 1.")\n',True)]
   cells[3]['metadata']={'cellView':'form','tags':['iuea-support']}
   cells[3]['source'].insert(0,'#@title Run only — prepare CSV and libraries\n')
   for i,((task,marks),(title,signature,prompt,starter,driver,minutes)) in enumerate(zip(PARTS,TASKS),1):
    cells.append(cell(f'## Task {i}: {title} — {marks} marks · about {minutes} minutes\n\n{prompt}'))
    if i==1:
     reading=cell('file_path = "engineering_data.csv"\n# Write your pandas CSV-reading statement below. Store the result in raw_data.\n\n',True)
     reading['metadata']['tags']=['iuea-read-csv'];cells.append(reading)
     cells.append(cell('#@title Run only — pass your raw_data to the tasks\nrecords = records_from_table(raw_data)\nprint(raw_data.head())\n',True))
     cells[-1]['metadata']={'cellView':'form','tags':['iuea-support']}
    cells += [cell('def '+signature+':\n'+starter+'\n',True),cell('#@title Run only — show Task '+str(i)+' results\n'+driver+'\n',True)]
    cells[-1]['metadata']={'cellView':'form','tags':['iuea-support']}

   cells += [cell('## Check and submit\nCheck that each task runs, both charts appear, and your answers use the supplied data. Save your notebook. No written report is required. Run the submission cell below, click **Submit test**, then open the generated form and press **Submit** before your deadline. The notebook button alone is not a completed submission.')]
   submit=cell('#@title Submit your test\n'+helper.replace('__EXAM_CONFIG__',repr(dict(lecturer_email=config['lecturer_email'],forms={course+'|TEST1':config['forms'][course+'|TEST1']}))),True)
   submit['metadata']={'tags':['iuea-submission','autograde-skip'],'cellView':'form'};cells.append(submit)
   nb=dict(cells=cells,metadata=dict(iuea_exam_version=VERSION,kernelspec=dict(display_name='Python 3',language='python',name='python3')),nbformat=4,nbformat_minor=5)
   (folder/'TEST1_student.ipynb').write_text(json.dumps(nb,indent=1,ensure_ascii=False)+'\n')
   for name in ['TASKS.md','ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt','STUDENT_HOW_TO.md']:(folder/name).write_text(guide)
   (folder/'TASKS.md').write_text(guide+'\n\n'+'\n\n'.join('## Task '+str(i)+': '+entry[0]+' — '+str(marks)+' marks\n\n'+entry[2] for i,((task,marks),entry) in enumerate(zip(PARTS,TASKS),1)))
   with zipfile.ZipFile(folder.parent.parent/f'{course}_TEST1_{variant}_student.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['TEST1_student.ipynb','engineering_data.csv','ASSIGNMENT_INSTRUCTIONS.txt']:z.write(folder/name,name)
 questions={f'q{i}':dict(marks=m,visible=False,prompt=t,answer_vars=[]) for i,(t,m) in enumerate(PARTS,1)}
 (G/'specs/spec_TEST1.py').write_text(f'ASSIGNMENT="TEST1"\nTITLE="Coding-only Test 1"\nVERSION={VERSION!r}\nDEFAULT_COHORT=""\nQUESTION_ORDER={list(questions)!r}\nQUESTIONS={questions!r}\n')
 (G/'specs/hidden/spec_TEST1_hidden.py').write_text('from test1_coding_contracts import assess\nQUESTIONS={\n'+',\n'.join(f'{q!r}: {{"check": lambda ns: assess(ns,{task!r})}}' for q,(task,_) in zip(questions,PARTS))+'\n}\n')
 rubric=dict(id='TEST1-'+VERSION,title='Coding-only Test 1',maximum=100,grading='deterministic',criteria=[dict(id=f'q{i}',title=titles[t],maximum=m,description=TASKS[i-1][2]) for i,(t,m) in enumerate(PARTS,1)])
 (G/'rubrics/TEST1.json').write_text(json.dumps(rubric,indent=2)+'\n')
 p=G/'rubrics/hybrid/TEST1.json';hybrid=json.loads(p.read_text());hybrid['id']='TEST1-'+VERSION;p.write_text(json.dumps(hybrid,indent=2)+'\n')
 p=BASE/'assessment_banks/assessment_components.json';components=json.loads(p.read_text());components['TEST1']=dict(maximum=100,deterministic_maximum=100,reasoning_maximum=0,version=VERSION,parts=PARTS);p.write_text(json.dumps(components,indent=2)+'\n')
 p=ROOT/'data/assessments.json';items=json.loads(p.read_text())
 for item in items:
  if item['id']=='TEST1' and item['cohort'] in DOMAINS:item.update(grading='notebook',formats=['ipynb'],assessment_version=VERSION)
 p.write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':build_test1()
