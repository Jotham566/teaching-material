"""Add ungraded data-loading scaffolds, without changing answer cells/contracts."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan'
MARK='PANDAS_WORKFLOW_20261015'
GUIDE='''## Working with pandas

Use pandas for table operations from Week 6 onward. Keep every published function name, input and return type. Inside a function, use `pd.DataFrame(records)` to work with named columns. Convert only the returned result to the required list or dictionary. Existing correct solutions using Python loops remain accepted; you do not need to redo submitted work.

The first notebook cells load the supplied data and provide `records_from_table`. That helper converts pandas missing values back to Python None when the published record interface needs it. It does not clean your data or answer the tasks. Do not edit raw files or calculate answers from hardcoded totals.

Work in this order: inspect the table; implement one required function; call it using the loaded data; inspect its output; complete your written evidence; restart and run all; submit only the required files. Keep `STUDENT_ID` as the notebook variable name and enter your own Student Registration Number as its value.
'''
LOADER='''import pandas as pd

def records_from_table(table):
    """Adapt pandas missing markers to the issued record interface."""
    objects = table.astype(object)
    return objects.where(table.notna(), None).to_dict("records")

raw_table = pd.read_csv("engineering_data.csv")
records = records_from_table(raw_table)
print(raw_table.head())
print(raw_table.shape)
'''
CLASSIFICATION='''import pandas as pd
case = pd.read_csv("classification_case.csv")
actual = case["actual"].tolist()
predicted = case["predicted"].tolist()
print(case.head())
'''
def revise():
 count=0
 for aid in ('W06','W08','W09','W10','W11','W12','DA_PROJECT','ML_PROJECT'):
  for folder in (BASE/'assessment_banks'/aid).glob('CML*/*'):
   if not folder.is_dir():continue
   for path in folder.glob('*_student.ipynb'):
    nb=json.loads(path.read_text());nb['cells']=[c for c in nb['cells'] if c.get('metadata',{}).get('pandas_support')!=MARK]
    cells=[dict(cell_type='markdown',metadata={'pandas_support':MARK},source=(GUIDE if aid!='W09' else GUIDE.replace('The first notebook cells load the supplied data and provide `records_from_table`. That helper converts pandas missing values back to Python None when the published record interface needs it. It does not clean your data or answer the tasks.', 'The supplied loading cell reads classification_case.csv with pandas and creates the actual and predicted lists. It does not calculate the assessed metrics.')).splitlines(True)),dict(cell_type='code',metadata={'pandas_support':MARK},execution_count=None,outputs=[],source=(CLASSIFICATION if aid=='W09' else LOADER).splitlines(True))]
    # Before the first question but after identity, preserving all answer cells.
    pos=next((i+1 for i,c in enumerate(nb['cells']) if c['cell_type']=='code' and 'STUDENT_ID' in ''.join(c['source'])),1)
    nb['cells'][pos:pos]=cells
    path.write_text(json.dumps(nb,indent=2)+'\n');count+=1
   for name in ('TASKS.md','ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt'):
    path=folder/name
    if not path.exists():continue
    s=path.read_text();s=s.split('\n<!-- '+MARK+' -->')[0].rstrip()
    path.write_text(s+'\n\n<!-- '+MARK+' -->\n## Pandas workflow\n\nRun the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.\n')
 print('Added pandas scaffolding to',count,'assessment notebooks')
if __name__=='__main__':revise()
