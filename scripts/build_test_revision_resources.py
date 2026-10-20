"""Build advance practice CSVs and student-only sharing bundles for six test decks."""
import csv,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'IUEA_Teaching_Plan/test_revision'
def build_data():
 for cohort in ('CML3111','CML3112','CML3113'):
  for exam in (1,2):
   folder=BASE/cohort/f'Test{exam}';folder.mkdir(parents=True,exist_ok=True)
   name=f'{cohort}_Test{exam}_practice.csv'
   rows=[[1,'M1',20,10,20],[2,'M1',40,20,''],[3,'M2',60,30,30],[4,'M2',80,40,40]]
   if exam==1:rows += [[1,'M1',20,10,20],[5,'M2',50,'',90],[6,'M2',120,90,100]]
   with (folder/name).open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['reading','machine','load','target','ambient']);w.writerows(rows)
   (folder/'START_HERE.txt').write_text(f'''{cohort} — Test {exam} revision (Week {7 if exam==1 else 14})

1. Open the accompanying PDF and start at slide 1.
2. Open colab.research.google.com. Sign in and choose New notebook.
3. Rename the notebook Test revision. Click Connect.
4. Click the folder icon on the left, then Upload. Select {name}.
5. Add code cells and run the worked examples in slide order.
6. Try each practice question before reading the answer slide.
7. Save your notebook in Drive. No practice submission is required.

Keep the CSV filename unchanged. Upload it again if the Colab session resets.
The slides explain the columns, cleaning rules and expected outputs.
All data are invented for learning. These are not the assessment files.
On test day, use the different notebook and engineering_data.csv issued by the timed portal.
''')
 # These cohorts use the advance material for their ungraded revision class.
 for cohort in ('CML3112','CML3113'):
  p=BASE/cohort/'Test1/START_HERE.txt'
  p.write_text('A6 and Quiz 6 are waived. Use these files for ungraded practical revision. No practice submission is required.\n\n'+p.read_text())

def package():
 decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
 for d in decks:
  if d['week'] not in (7,14):continue
  exam=1 if d['week']==7 else 2;folder=BASE/d['cohort']/f'Test{exam}'
  deck=folder/Path(d['filename']).with_suffix('.pdf')
  if not deck.exists():raise FileNotFoundError('Run scripts/export_test_revision_pdfs.mjs first: '+str(deck))
  with zipfile.ZipFile(folder/f"{d['cohort']}_Test{exam}_revision.zip",'w',zipfile.ZIP_DEFLATED) as z:
   for p in [deck,folder/f"{d['cohort']}_Test{exam}_practice.csv",folder/'START_HERE.txt']:z.write(p,p.name)
if __name__=='__main__':
 import sys
 build_data()
 if '--package' in sys.argv:package()
