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
# 1. Replace None with pd.read_csv(...) using file_path inside the parentheses.
raw_data = None

# 2. Methods use (); attributes such as shape and dtype do not.
first_rows = None          # First five rows: use the head method on raw_data.
last_rows = None           # Last five rows: use the tail method.
data_shape = None          # Store (rows, columns) using the shape attribute.
row_count = None           # Count rows with len(...).
target_dtype = None        # Select the target column first, then use its dtype.

# 3. Add the info() call here. It displays information; do not assign its result.

numeric_summary = None    # Use describe() on the whole raw_data table.
# 4. isna() and isnull() both mark missing cells True; sum() counts them.
missing_counts = None     # Use either missing-value method, then .sum().
# Repeated equipment IDs are normal. Look for repeated record_id values.
duplicate_count = None    # duplicated("record_id") marks repeats; sum counts them.

# 5. Find bad rows without changing raw_data.
# Build three conditions: missing target, load below 0, load above 100.
# Combine with | (OR), putting each comparison in parentheses.
# Select rows with raw_data[condition] or raw_data.loc[condition].
invalid_records = None

# 6. Run this cell and inspect your results. None means an answer is unfinished.
print(first_rows)
print(last_rows)
print(data_shape, row_count, target_dtype)
print(numeric_summary)
print(missing_counts)
print("Repeated record IDs:", duplicate_count)
print(invalid_records)''', '',25),
('Visualisation before cleaning', '', """Using `raw_data`, create a scatter chart of `load_pct` (horizontal) against `target` (vertical). Do not clean or fill values first.
Use `figure, axes = plt.subplots()`, then either `axes.scatter(...)` or `raw_data.plot.scatter(x=..., y=..., ax=axes)`.
Add a title, horizontal label including %, and vertical label including the target unit shown above. Keep `before_figure = figure`: it saves this chart for marking.
Marks: correct points 4; title 2; horizontal label 2; vertical label and unit 2.""",
'''figure, axes = plt.subplots()
# 1. Add raw_data.plot.scatter(x=..., y=..., ax=axes).
# Replace ... with quoted column names: horizontal load_pct, vertical target.
# Alternatively use axes.scatter with those two selected columns.

# 2. Add axes.set_title(...), axes.set_xlabel(...), axes.set_ylabel(...).
# Labels are text in quotes. Include % for load and the target unit from Your CSV.

before_figure = figure  # Do not edit: keeps the before-cleaning chart for marking.
plt.show()
# Check: one chart, two labelled axes, and the raw observations still included.
''', '',15),
('Clean the data', '', """Start with a copy of `raw_data`; call it `cleaned_data`. Apply these rules in order:
1. Keep the first row for each `record_id`.
2. Remove rows with missing `target` or `load_pct` outside 0–100. Keep 0 and 100.
3. Find the median `ambient_c` in the retained rows. Fill only missing temperatures with this median.
Keep the same five columns and row order. Do not alter known values or equipment labels. Display the cleaned table and check for missing values, duplicates and invalid loads again.
Marks: 4 for each correctly cleaned column. Index numbers do not matter.""",
'''# Work in this order. Write your code under each step.
# 1. Make a separate copy with .copy(); name it cleaned_data.

# 2. Use drop_duplicates on record_id; save the result back to cleaned_data.
# Default keep="first" keeps the first occurrence. Check len(cleaned_data).

# 3. Use dropna(subset=[...]) for missing target values only.
# Do not drop rows just because ambient_c is missing; you will fill those later.

# 4. Use the load_pct column's between(0, 100) to identify valid loads.
# Select those rows with cleaned_data[condition] or .loc[condition], then .copy().
# Save the selected table back to cleaned_data. Both endpoints are valid.

# 5. Calculate the ambient_c median from the retained rows.
# Fill only that column's gaps with fillna(the_median_you_calculated).
# Assign the filled column back to cleaned_data["ambient_c"].

# 6. Check the result: display cleaned_data, its length, missing counts,
# duplicate record_id count, and whether all loads are between 0 and 100.
# Use .isna().sum() or .isnull().sum(); use .between(0, 100).all() for loads.
# Expect no duplicate IDs, no missing values, and all loads valid.
''', '',25),
('Visualisation after cleaning', '', """Repeat Task 2 using `cleaned_data`. Use a new figure with the same two columns and units, and a title such as “After cleaning”. Keep `after_figure = figure`: it saves this chart for marking.
Marks: correct cleaned points 4; title 2; horizontal label 2; vertical label and unit 2. No written comparison is required.""",
'''figure, axes = plt.subplots()
# Repeat your Task 2 plotting steps, now using cleaned_data instead of raw_data.
# Use load_pct horizontally and target vertically. Plot on this new axes.
# Change the title to describe the cleaned data; keep the same axis units.


after_figure = figure  # Do not edit: keeps the after-cleaning chart for marking.
plt.show()
# Check that the chart uses only the rows retained in Task 3.
''', '',10),
('Calculate statistics', '', """Using `cleaned_data`, calculate `target_mean`, `target_sum`, `target_median`, `target_count` and `target_std` from `target`.
Also calculate and display `equipment_modes`: all most frequent `equipment_id` values using `.mode()`. Each of these six answers earns 2.5 marks.
Use pandas' `.std()` with its default sample standard deviation. Do not round answers. Mode means most frequent; `.mode()` returns every tied mode. These are descriptive calculations, not safety conclusions.""",
'''# Select cleaned_data["target"], then apply the method for each calculation.
# Pattern: table["column"].method(). Keep full precision; do not round.
target_mean = None       # Average: mean().
target_sum = None        # Add values: sum().
target_median = None     # Middle value: median().
target_count = None      # Number of non-missing values: count().
target_std = None        # Spread: std(), with pandas' default settings.
# For this answer select equipment_id, not target. Keep ALL tied modes.
equipment_modes = None  # Most frequent labels: mode(). Keep its Series or a list.

print("Mean:", target_mean)
print("Sum:", target_sum)
print("Median:", target_median)
print("Count:", target_count)
print("Standard deviation:", target_std)
print("Equipment modes:", equipment_modes)
''', '',15),
('Group and aggregate', '', """Group `cleaned_data` by `equipment_id`. Use `groupby` and `agg` to calculate the mean and count of `target` for each equipment. Store the DataFrame as `equipment_summary` and display it.
Its index must contain equipment IDs and its two columns must be named `mean` and `count`. Keep full precision. Group order does not affect marks (5 marks per column).""",
'''# You may write this in three steps, as in revision:
# 1. Group cleaned_data by equipment_id with groupby(...).
# 2. Select target from those groups.
# 3. Apply agg([...]) with the strings "mean" and "count".
equipment_summary = None
print(equipment_summary)
# Check: one row per equipment; columns named mean and count.
''' , '',10),
('Reuse your statistics in one function', 'calculate_column_statistics(table, column_name)', """Turn three calculations from Task 5 into a reusable function. The supplied inputs are a DataFrame (`table`) and a column name (`column_name`).
Return a dictionary with keys `mean`, `sum`, `median`, calculated from `table[column_name]`. Replace the three `None` values. Use the inputs rather than a fixed column or the global `cleaned_data`.
Then call your function for `cleaned_data` and `"target"`, and again for `"load_pct"`. Display both results. The grader tests the function with other numeric values (5 marks).""",
'''def calculate_column_statistics(table, column_name):  # Do not edit: defines the function inputs used for marking.
    # Repeat Task 5's mean, sum and median calculations on table[column_name].
    # Use these inputs, not the global cleaned_data or a fixed column name.
    # Keep the three quoted keys; replace each None with a calculation.
    return {"mean": None, "sum": None, "median": None}

# Call the function twice: use cleaned_data with "target", then with "load_pct".
# Pattern: result = function_name(table, "column"); then print(result).
# The target results should match your Task 5 mean, sum and median.''', '',15),
('Conditions and a loop', '', """Use a `for` loop over `cleaned_data["load_pct"]`. Inside it, use `if`, `elif`, `else` to count loads in these categories:
- `low`: below 40;
- `medium`: 40 to 75 inclusive;
- `high`: above 75.
Update the supplied `load_band_counts` dictionary and display it after the loop. Do not type the final counts by hand. For loads `[20, 40, 75, 90]`, the counts would be `{"low": 1, "medium": 2, "high": 1}`.
These are test categories, not safety limits. Correct counts: 6 marks; a loop: 2; conditions inside that loop: 2. No second function is required.""",
'''load_band_counts = {"low": 0, "medium": 0, "high": 0}
# Loop over cleaned_data["load_pct"] using a descriptive name such as load_value.
# Inside the loop: if below 40, elif at most 75, else above 75.
# Add one to the matching counter: load_band_counts["low"] += 1 in the low branch.
# Use the medium and high keys in their respective branches.
# Indent conditions inside the loop, and increments inside their conditions.
# Write your loop here:

print(load_band_counts)  # Keep outside the loop to show the final counts once.
# Check: the three counts should add up to len(cleaned_data).''', '',20)
]

GUIDE_EXTRA='\n## Coding tasks and time plan\n10 minutes setup · 135 coding · 15 checking · 20 submitting.\n\nUse pandas, matplotlib and ordinary Python. Work from top to bottom in the answer cells. Replace `None` with your calculation; it means “not completed yet”. Follow the comments, run each cell and check its output. You may add code cells, but keep the requested result names. Only Task 7 requires a function.\n\nCells labelled **Do not edit this cell** are supplied setup or submission tools: run them, but do not change or delete them. In answer cells, keep lines marked **Do not edit** unchanged.\n'

def student_guide(course):
 return f"""# {course} Test 1 — Take-home practical
**Individual work · 100 marks · 3 hours from Start test**

## Start here
**You can submit only once.** Before submitting, double-check your work, full name, Student ID/ Registration Number and Google email. You cannot edit or replace a submitted response; contact your lecturer if a correction is needed.

Use this private notebook directly; you do not need another copy. Click **Connect** at the top right if shown. Press the triangle beside a code cell to run it.

1. **Run, do not edit:** **Check details and countdown**. **Double-check your full name, Student ID/ Registration Number, and email.** Use the same Google email in Colab and the submission form. If any detail is wrong, contact your lecturer before continuing; do not create another identity.
2. **Run, do not edit:** **Prepare CSV and libraries**. It creates your assigned CSV automatically; you do not need to upload a file.
3. **Write your code:** start in the answer cell immediately below Task 1. Read the CSV with pandas using `file_path`.
4. Complete Tasks 1–8 in order. Keep `raw_data` unchanged; Task 3 produces `cleaned_data`. Save regularly.
5. Leave **at least 20 minutes to submit**. Follow the **Save and submit** checklist at the end. Submission is finished only when the Google Form confirms that your response has been recorded.

The timer includes setup, interruptions and submission. A sleeping or disconnected browser may show an outdated countdown: rerun the countdown cell when you return. The server deadline still applies. It ends at your personal deadline or the class cutoff, whichever comes first. Resume with the same entry link, email and registration number; the timer does not restart.

## Test rules
**Permitted resources:** Your lecture slides, revision guide, cheatsheet and personal course notes. Use your assigned CSV and write the code yourself.

**No AI or outside help:** Do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your test answers. Do not obtain answers from another person, collaborate, or copy someone else’s work.

**Understanding check:** You may be asked to explain your submitted code or make a small change without AI or another person’s help.

**Declaration:** By submitting, I confirm that I completed this test myself without AI assistance or another person’s help, using only the permitted resources. I can explain and modify the code I submitted. If you change a support cell, use **Edit → Undo**. If submission fails, contact your lecturer before the deadline.
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
Each row is a synthetic observation of **{domain}**. One DataFrame is the whole table; selecting one column gives a Series.

| Column | Meaning |
|---|---|
| record_id | Observation ID; repeated IDs are duplicates, not time points |
| equipment_id | Equipment label; one piece of equipment can have several observations |
| load_pct | Load percentage; valid range 0–100 inclusive |
| ambient_c | Ambient temperature in degrees Celsius |
| target | {domain}, measured in {unit} |

If your revision example used `reading`, `machine`, `load`, `ambient`, their matching test columns are `record_id`, `equipment_id`, `load_pct`, `ambient_c`. `target` keeps the same name. The revision names `source_data` or `raw_table` mean the original table; here call it `raw_data`. Use this test's column names and data, not the practice CSV or its numerical answers.

Blank cells become missing values. Tasks 1–2 use `raw_data`; Task 3 creates `cleaned_data`; Tasks 4–8 use it. Use only this assigned CSV.'''),cell('#@title Prepare CSV and libraries — Do not edit this cell\n# Do not edit this cell: loads the two libraries for your answers.\nimport pandas as pd\nimport matplotlib.pyplot as plt\nTARGET_UNIT = '+repr(unit)+'  # Do not edit: supplies the target measurement unit.\nprint("Setup ready. Continue to Task 1.")\n',True)]
   cells[3]['metadata']={'cellView':'form','tags':['iuea-support']}
   for i,((task,marks),(title,signature,prompt,starter,driver,minutes)) in enumerate(zip(PARTS,TASKS),1):
    cells.append(cell(f'## Task {i}: {title} — {marks} marks · about {minutes} minutes\n\n{prompt}'))
    answer=cell(starter+'\n',True)
    answer['metadata']['tags']=['iuea-answer-'+task]
    if i==1:answer['metadata']['tags'].append('iuea-read-csv')
    cells.append(answer)

   cells += [cell("""## Need help with a technical problem?
| What you see | What to do |
|---|---|
| Disconnected runtime | Click **Connect**. If variables are gone, rerun **Prepare CSV and libraries**, then your answer cells in order from Task 1. Restarting clears variables; it does not reset the timer. |
| `NameError` | Check the variable spelling and run the earlier cell that creates it. Editing a cell does not run it. |
| `KeyError` | Check the exact column spelling in `raw_data.columns`. |
| `FileNotFoundError` | Rerun **Prepare CSV and libraries** and check that `file_path` names `engineering_data.csv`. |
| Authorization or submission stalls | Select the same Google account used at entry. Allow the requested access to save your snapshot and share it privately with your lecturer. If it still fails, record the error and contact your lecturer before the deadline. |
| Tab closed or laptop restarted | Reopen the test entry link with the same email and registration number, then resume your notebook. Only saved changes can be recovered. Rerun the countdown cell. |

Fix the first error before later cells. Do not delete or edit supplied support cells. If you accidentally change one, use **Edit → Undo**.

## Save and submit — allow at least 20 minutes
**One submission only per Google account and per Student ID/ Registration Number for this test.** Check your work and details before pressing Submit in the Google Form. After submitting, contact your lecturer for any correction; do not use another account.

**Declaration:** By submitting, I confirm that I completed this test myself without AI assistance or another person’s help, using only the permitted resources. I can explain and modify the code I submitted.

1. Check your code cells and charts. Submit your work even if some tasks are unfinished. No written report is required.
2. Choose **File → Save**. Double-check your **full name, Student ID/ Registration Number and Google email**.
3. **Run, do not edit:** the **Submit your test** cell below. Click **Submit test** and wait for its form link. If no new tab opens, click the displayed link.
4. In the Google Form, check the signed-in email, name and registration number again. Keep the prefilled snapshot and allocation details unchanged. Complete the required confirmation and press **Submit** before your deadline.
5. Wait for **Your response has been recorded**. Keep your saved snapshot unchanged until marks are released.

**A saved notebook, a snapshot, or an open form is not a completed submission. You must submit the Google Form.** The confirmation acknowledges receipt only. The server rejects late receipts from grading, even if an old form was left open. When time ends, the notebook submission button closes. Contact your lecturer if you need help.
""")]
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
