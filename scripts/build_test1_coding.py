"""Build only the coding-only Test 1; preserve Test 2 and collection settings."""
import csv,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';G=BASE/'grader'
sys.path.insert(0,str(G))
from engineering_contracts import DOMAINS,dataset
from test1_coding_contracts import VERSION,PARTS
from build_colab_exams import cell

TASKS=[
('Read and inspect the raw data', '', """Read `engineering_data.csv` with pandas using `file_path`; name the DataFrame `raw_data`. Keep it unchanged throughout the test.
Complete the named answers below:
- `first_rows`: first 5 rows using `.head()`; `last_rows`: last 5 using `.tail()` (1 mark each).
- `data_shape`: `.shape`; `row_count`: `len(raw_data)` (1 mark each).
- `target_dtype`: the `target` column's `.dtype` (2). A column has `.dtype`; a whole DataFrame has `.dtypes`.
- Run `raw_data.info()` to display column types and non-missing counts (2). It prints a summary; do not assign its result.
- `numeric_summary`: `.describe()` for numeric columns (2).
- `missing_counts`: missing count for each column, using `.isna()` or `.isnull()` followed by `.sum()` (2).
- `duplicate_count`: number of repeated `record_id` values AFTER the first occurrence (2).
- `invalid_records`: rows where `target` is missing OR `load_pct` is below 0 OR above 100 (4). This is inspection only: do not remove these rows yet.
Reading the correct CSV into `raw_data` earns 2 marks. Display your answers to check them.""",
'''file_path = "engineering_data.csv"  # Do not edit: locates your assigned CSV.
# Read the file into raw_data, then replace None with each calculation.
first_rows = None
last_rows = None
data_shape = None
row_count = None
target_dtype = None
# Display the column information here.
numeric_summary = None
missing_counts = None
duplicate_count = None
invalid_records = None''', '',25),
('Visualisation before cleaning', '', """Using `raw_data`, create a scatter chart of `load_pct` (horizontal) against `target` (vertical). Do not clean or fill values first.
Use `figure, axes = plt.subplots()`, then either `axes.scatter(...)` or `raw_data.plot.scatter(x=..., y=..., ax=axes)`.
Add a title, horizontal label including %, and vertical label including the target unit shown above. Keep `before_figure = figure`: it saves this chart for marking.
Marks: correct points 4; title 2; horizontal label 2; vertical label and unit 2.""",
'''figure, axes = plt.subplots()
# Add your scatter plot, title and labels here.
before_figure = figure  # Do not edit: keeps the before-cleaning chart for marking.
plt.show()''', '',15),
('Clean the data', '', """Start with a copy of `raw_data`; call it `cleaned_data`. Apply these rules in order:
1. Keep the first row for each `record_id`.
2. Remove rows with missing `target` or `load_pct` outside 0–100. Keep 0 and 100.
3. Find the median `ambient_c` in the retained rows. Fill only missing temperatures with this median.
Keep the same five columns and row order. Do not alter known values or equipment labels. Display the cleaned table and check for missing values, duplicates and invalid loads again.
Marks: 4 for each correctly cleaned column. Index numbers do not matter.""",
'''# Copy raw_data into cleaned_data, then apply the three cleaning rules.
# Display and check cleaned_data when finished.''', '',25),
('Visualisation after cleaning', '', """Repeat Task 2 using `cleaned_data`. Use a new figure with the same two columns and units, and a title such as “After cleaning”. Keep `after_figure = figure`: it saves this chart for marking.
Marks: correct cleaned points 4; title 2; horizontal label 2; vertical label and unit 2. No written comparison is required.""",
'''figure, axes = plt.subplots()
# Add the cleaned-data scatter plot, title and labels here.
after_figure = figure  # Do not edit: keeps the after-cleaning chart for marking.
plt.show()''', '',10),
('Calculate statistics', '', """Using `cleaned_data`, calculate `target_mean`, `target_sum`, `target_median`, `target_count` and `target_std` from `target`.
Also calculate and display `equipment_modes`: all most frequent `equipment_id` values using `.mode()`. Each of these six answers earns 2.5 marks.
Use pandas' `.std()` with its default sample standard deviation. Do not round answers. Mode means most frequent; `.mode()` returns every tied mode. These are descriptive calculations, not safety conclusions.""",
'''target_mean = None
target_sum = None
target_median = None
target_count = None
target_std = None
equipment_modes = None''', '',15),
('Group and aggregate', '', """Group `cleaned_data` by `equipment_id`. Use `groupby` and `agg` to calculate the mean and count of `target` for each equipment. Store the DataFrame as `equipment_summary` and display it.
Its index must contain equipment IDs and its two columns must be named `mean` and `count`. Keep full precision. Group order does not affect marks (5 marks per column).""",
'''equipment_summary = None''', '',10),
('Reuse your statistics in one function', 'calculate_column_statistics(table, column_name)', """Turn three calculations from Task 5 into a reusable function. The supplied inputs are a DataFrame (`table`) and a column name (`column_name`).
Return a dictionary with keys `mean`, `sum`, `median`, calculated from `table[column_name]`. Replace the three `None` values. Use the inputs rather than a fixed column or the global `cleaned_data`.
Then call your function for `cleaned_data` and `"target"`, and again for `"load_pct"`. Display both results. The grader tests the function with other numeric values (5 marks).""",
'''def calculate_column_statistics(table, column_name):  # Do not edit: defines the function inputs used for marking.
    return {"mean": None, "sum": None, "median": None}

# Call your function for the two columns below.''', '',15),
('Conditions and a loop', '', """Use a `for` loop over `cleaned_data["load_pct"]`. Inside it, use `if`, `elif`, `else` to count loads in these categories:
- `low`: below 40;
- `medium`: 40 to 75 inclusive;
- `high`: above 75.
Update the supplied `load_band_counts` dictionary and display it after the loop. Do not type the final counts by hand. For loads `[20, 40, 75, 90]`, the counts would be `{"low": 1, "medium": 2, "high": 1}`.
These are test categories, not safety limits. Correct counts: 6 marks; a loop: 2; conditions inside that loop: 2. No second function is required.""",
'''load_band_counts = {"low": 0, "medium": 0, "high": 0}
# Write your loop and conditions, then display load_band_counts.''', '',20)
]

GUIDE_EXTRA='\n## Coding tasks and time plan\n10 minutes setup · 135 coding · 15 checking · 20 submitting.\n\nUse pandas, matplotlib and ordinary Python. Work from top to bottom in the answer cells. Keep the requested result names so your work can be marked. Only Task 7 requires a function.\n\nCells labelled **Do not edit this cell** are supplied setup or submission tools: run them, but do not change or delete them. In answer cells, keep lines marked **Do not edit** unchanged.\n'

def student_guide(course):
 return f"""# {course} Test 1 — Take-home practical
**Individual work · 100 marks · 3 hours from Start test**

1. Run **Check details and countdown**. **Double-check your full name, Student ID/ Registration Number, and email.** Use the same Google email in Colab and the submission form. If any detail is wrong, contact your lecturer before continuing; do not create another identity.
2. Run **Prepare CSV and libraries**, then write your own pandas CSV-reading code in Task 1.
3. Complete Tasks 1–8 in order. Keep `raw_data` unchanged; Task 3 produces `cleaned_data`. Save regularly.
4. Run **Submit your test**, click the button, open its form, **check your name, Student ID/ Registration Number, and email again**, then press **Submit**. Wait for confirmation.

The timer includes setup, interruptions and submission. It ends at your personal deadline or the class cutoff, whichever comes first. Resume with the same entry link, email and registration number; the timer does not restart.

No AI-generated answers or collaboration. If you change a support cell, use **Edit → Undo**. If submission fails, contact your lecturer before the deadline.
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
   identity=f'''# Check your full name, Student ID/ Registration Number, and email.
FULL_NAME = ""
EMAIL = ""
STUDENT_ID = ""
COHORT = "{course}"  # Do not edit: identifies your course for marking.
TEST_ID = "TEST1"  # Do not edit: identifies this assessment.
VARIANT = "{variant}"  # Do not edit: identifies your assigned dataset.
'''
   cells=[cell(guide),cell(identity,True),cell(f'''## Your CSV
Each row is a synthetic observation of **{domain}**.

| Column | Meaning |
|---|---|
| record_id | Observation ID; repeated IDs are duplicates, not time points |
| equipment_id | Equipment label; one piece of equipment can have several observations |
| load_pct | Load percentage; valid range 0–100 inclusive |
| ambient_c | Ambient temperature in degrees Celsius |
| target | {domain}, measured in {unit} |

Blank cells become missing values. Tasks 1–2 use `raw_data`; Task 3 creates `cleaned_data`; Tasks 4–8 use it. Use only this assigned CSV.'''),cell('#@title Prepare CSV and libraries — Do not edit this cell\n# Do not edit this cell: loads the two libraries for your answers.\nimport pandas as pd\nimport matplotlib.pyplot as plt\nTARGET_UNIT = '+repr(unit)+'  # Do not edit: supplies the target measurement unit.\nprint("Setup ready. Continue to Task 1.")\n',True)]
   cells[3]['metadata']={'cellView':'form','tags':['iuea-support']}
   for i,((task,marks),(title,signature,prompt,starter,driver,minutes)) in enumerate(zip(PARTS,TASKS),1):
    cells.append(cell(f'## Task {i}: {title} — {marks} marks · about {minutes} minutes\n\n{prompt}'))
    answer=cell(starter+'\n',True)
    answer['metadata']['tags']=['iuea-answer-'+task]
    if i==1:answer['metadata']['tags'].append('iuea-read-csv')
    cells.append(answer)

   cells += [cell('## Check and submit\nCheck that each task runs, both charts appear, and your answers use the supplied data. Save your notebook. No written report is required. Run the submission cell below, click **Submit test**, then open the generated form and press **Submit** before your deadline. The notebook button alone is not a completed submission.')]
   submit=cell('#@title Submit your test — Do not edit this cell\n# Do not edit this cell: saves your answers and prepares the submission form.\n'+helper.replace('__EXAM_CONFIG__',repr(dict(lecturer_email=config['lecturer_email'],forms={course+'|TEST1':config['forms'][course+'|TEST1']}))),True)
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
