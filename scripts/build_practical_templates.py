"""Build Weeks 3 and 5 handouts from the authoritative public task contracts."""
import json,shutil,sys
from pathlib import Path
from build_week2_kit import notebook
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';GRADER=BASE/'grader'
sys.path.insert(0,str(GRADER))
import iuea_grader as ig

for week in (3,5):
 aid=f'W{week:02}';specfile=GRADER/'specs'/f'spec_{aid}.py'
 spec=ig.load_spec(aid,str(specfile),include_hidden=False)
 for code in ('CML3111','CML3112','CML3113'):
  dest=BASE/'practicals'/aid/code;dest.mkdir(parents=True,exist_ok=True)
  if week==5:shutil.copy2(GRADER/'data/campus_energy.csv',dest/'campus_energy.csv')
  cells=[('markdown',f'# {aid}: {spec.TITLE}\n{code}. Complete each named output. Save as STUDENT_ID_{aid}.ipynb.'),
         ('code',f'STUDENT_ID="YOUR_ID"\nCOHORT="{code}"\n')]
  for qid,q in ig.resolve_questions(spec,code):
   cells.append(('markdown',f'## {qid}: {q["marks"]} marks\n{q.get("prompt","")}'))
   if week==3 and qid=='q5':
    cells.append(('markdown','You may compare these six readings directly; a loop is not required this week.'))
    cells.append(('code','READINGS = [98.5, 103.2, 99.0, 111.4, 94.8, 100.6]\n'))
   cells.append(('code','# Your answer here\n'))
  cells.append(('markdown','Restart and Run All, then save your named notebook. Your uploaded notebook is marked automatically after submission.'))
  (dest/(aid+'_student.ipynb')).write_text(json.dumps(notebook(cells),indent=2)+'\n')
  intro='Open the notebook in Colab. No grading scripts are needed. '
  if week==5:
   intro+='Upload campus_energy.csv too. This is a fictional 24-row teaching dataset, not measured campus consumption. Complete the six tasks for 20 marks. '
  else:intro+='Complete the five tasks for 20 marks. '
  (dest/'README.md').write_text(f'# {code} {aid}\n\n'+intro+'The notebook states every task and mark. Your uploaded notebook is marked automatically after submission. Restart and Run All, save STUDENT_ID_'+aid+'.ipynb, and upload it through your cohort assignment form.\n')

print('Built six practical templates; grading tools stay with the lecturer')
