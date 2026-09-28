from schools_camp_content import ROOT,ML,DA,ROADMAP
from schools_camp_delivery import OBJECTIVES,build_delivery_plan
from pathlib import Path
import csv,json,random,sqlite3,shutil,zipfile

def write(path,text):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
def cell(kind,text):
 d={'cell_type':kind,'metadata':{},'source':text.splitlines(keepends=True)}
 if kind=='code':d.update(execution_count=None,outputs=[])
 return d

def build():
 data=ROOT/'data';data.mkdir(parents=True,exist_ok=True)
 rng=random.Random(19)
 products=[('Book','Stationery',3000),('Pen','Stationery',1000),('Juice','Refreshment',2000)]
 rows=[]
 for i in range(60):
  item,category,price=products[i%3]
  rows.append(dict(sale_id=i+1,date=f'2026-12-{1+i//3:02}',item=item,units=rng.randint(1,8),unit_price_ugx=price))
 def savecsv(name,values):
  with (data/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
 savecsv('camp_shop.csv',rows)
 homes=[]
 for i in range(120):
  area=rng.randint(20,180);rooms=rng.randint(1,5)
  homes.append(dict(home_id=i+1,area_m2=area,rooms=rooms,rent_ugx=100000+area*3000+rooms*20000+rng.randint(-25000,25000)))
 savecsv('synthetic_homes.csv',homes)
 conn=sqlite3.connect(data/'camp_shop.sqlite')
 conn.executescript('DROP TABLE IF EXISTS sales; DROP TABLE IF EXISTS products; CREATE TABLE sales(sale_id INTEGER PRIMARY KEY,date TEXT,item TEXT,units INTEGER,unit_price_ugx INTEGER); CREATE TABLE products(item TEXT PRIMARY KEY,category TEXT);')
 conn.executemany('INSERT INTO sales VALUES(?,?,?,?,?)',[tuple(r.values()) for r in rows]);conn.executemany('INSERT INTO products VALUES(?,?)',[(p[0],p[1]) for p in products]);conn.commit()
 ref={'row_count':len(rows),'units_ge_5':sum(r['units']>=5 for r in rows),'total_units':sum(r['units'] for r in rows),'revenue_ugx':sum(r['units']*r['unit_price_ugx'] for r in rows),'by_item':list(conn.execute('SELECT item,SUM(units),SUM(units*unit_price_ugx),COUNT(*) FROM sales GROUP BY item ORDER BY item')),'by_category':list(conn.execute('SELECT p.category,SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products p ON s.item=p.item GROUP BY p.category ORDER BY p.category'))}
 conn.close();write(ROOT/'instructor_materials'/'reference_values.json',json.dumps(ref,indent=2)+'\n')
 write(data/'DATA_DICTIONARY.md','''# Supplied teaching data

Both CSV files are generated synthetic examples, not observations of actual shops or housing. The generator uses a fixed seed for reproducible checking. They contain no learner records. No claim about real demand, prices or rents can be inferred from them.

## camp_shop.csv and camp_shop.sqlite

60 sales records across 20 illustrative December dates. `sale_id`: unique record identifier. `date`: YYYY-MM-DD date string. `item`: Book, Pen or Juice. `units`: whole items sold. `unit_price_ugx`: UGX per item. Revenue is units multiplied by unit price. Costs are absent, so profit cannot be calculated. The SQLite products table has one unique item key and its category. A matching item connects sales to products. No intentionally missing values or duplicate IDs in this clean file; cleaning mistakes are introduced separately in the worked lessons.

## synthetic_homes.csv

120 invented independent home records. `home_id`: identifier, exclude from model inputs. `area_m2`: floor area in square metres. `rooms`: whole-number room count. `rent_ugx`: invented monthly rent in UGX. Features: area_m2 and rooms. Target: rent_ugx. The generation formula deliberately creates an easy learnable relationship; performance is a workflow exercise, not validation of a market model. Use a held-out test and report this limitation.

## Iris

ML classification uses `sklearn.datasets.load_iris`, bundled with scikit-learn after installation. Inputs are four flower measurements in centimetres; target is a species category encoded as 0, 1 or 2. Display `data.feature_names` and `data.target_names` in class to connect codes with names. This is a historical teaching dataset, not student data. Source documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
''')
 syllabus=['# Holiday Data and AI Camp curriculum\n','Eight weeks, three core classes per week, 24 core sessions per chosen track. ML also includes four foundation labs on a fourth day in weeks 1–4; see FOUNDATION_LABS.md for the required sequence. Audience: S.4–S.6 students and vacists. No programming, spreadsheet or statistics experience assumed.\n','The proposed session length is three hours, including a 15-minute break. Four proposed two-hour foundation labs bring ML to 80 scheduled hours including breaks; DA has 72. Confirm durations before advertising hour totals. A December 2026 start normally runs into January 2027; map 24 core class dates plus four ML lab dates around holidays before taking payment.\n']
 for code,name,lessons in [('ML','Machine Learning',ML),('DA','Data Analysis',DA)]:
  sd=ROOT/'student_materials'/code;td=ROOT/'instructor_materials'/code;sd.mkdir(parents=True,exist_ok=True);td.mkdir(parents=True,exist_ok=True)
  for filename in ['camp_shop.csv','synthetic_homes.csv','camp_shop.sqlite','DATA_DICTIONARY.md']:
   if code=='DA' and filename=='synthetic_homes.csv':continue
   if code=='ML' and filename=='camp_shop.sqlite':continue
   shutil.copy2(data/filename,sd/filename)
  syllabus += [f'\n## {name}\n']
  for i,l in enumerate(lessons,1):
   ident=f'{code}{i:02}';week=(i-1)//3+1
   prerequisite='START_HERE.md; no subject knowledge assumed' if i==1 else f'{code}{i-1:02} {lessons[i-2]["title"]}'
   lang={'python':'python','sql':'sql'}.get(l['mode'],'text')
   worked='```'+lang+'\n'+l['demo']+'\n```' if l['mode'] in ('python','sql') else l['demo']
   packet=f'''# {ident} {l['title']}

Week {week} | Session {i} of 24 | {name}

## Before this lesson

Complete {prerequisite}. If you cannot explain the previous example, use its repair cue with the instructor before moving on.

## Learning objective

By the end of this class: {OBJECTIVES[code][i-1]}

## Understand the idea

{l['explain']}

## Follow the worked example

1. Read the example before running or typing it. Say what you expect to happen.
2. The instructor demonstrates it, explaining each new term. Follow one step at a time.
3. Compare your output with the expected result below. If it differs, use the repair cue.

{worked}

Expected result: {l['expected']}

## Your turn

{l['task']}

Save your work using the session code {ident}. Keep the original worked example and put your own attempt below it or in a separate sheet/file. Add two sentences: what I changed and how I checked it. Follow AI_USE_POLICY.md: weeks 1–6 permit no AI-generated solutions for core exercises, labs or assessments. Weeks 7–8 allow only limited supervised demonstrations and critique after an independent attempt; core exercises remain unaided. Final assessment must be demonstrated and explained without AI assistance.

## When something goes wrong

{l['repair']}

## Practise between classes

Spend 20 to 30 minutes repeating the worked example without copying, then change one input and predict the new result. Stop after 30 minutes if stuck, save the error or a screenshot, and bring the question to the next class. On project weeks use the same time to complete the stated milestone. Plan two 45 to 60 minute practice blocks on non-class days; leave time for rest and school work.

## Check before leaving

Show your saved file, explain one new term, and point to the evidence that your answer works. Use the submission instructions in START_HERE.md for any assessed work. A file saved on your laptop has not automatically been submitted.
'''
   write(sd/f'{ident}.md',packet)
   teacher=f'''# {ident} Instructor guide

Read the matching student sheet first. Prerequisite: {prerequisite}.

Learning objective: {OBJECTIVES[code][i-1]}

## Explain and demonstrate

Use the student definition, then type or perform the worked example slowly. Ask learners to predict the result before you run it. Explain punctuation and units aloud. Do not add a new library or formula unless its purpose and inputs are demonstrated. Ask each of the five students to change one value and explain what changed.

Correct worked result: {l['expected']}

Specific repair cue: {l['repair']}

## Independent task reference

{l['answer']}

## Questions to ask

- What information goes in and what should come out of this particular example?
- Which result would convince you the task is correct?
- What does the example not tell us?

Use the task reference to evaluate their reasoning. If a learner cannot explain the basic operation, repeat the tiny example with different values before assigning the main task. For students who finish early, ask for an edge case or a limitation; do not introduce next week's syntax to the whole group.

## Evidence and feedback

Record complete, needs repair or absent for each learner. Give one concrete repair action. During a five-student class allocate a short individual check to every learner, not only volunteers. Keep instructor answers private. For SQL and numerical work use reference_values.json and the reference scripts. Short explanations and live demonstrations still require instructor judgement; do not describe them as fully auto-graded.

## Suggested three hour pacing

15 minutes retrieval and setup; 20 minutes first explanation; 25 minutes guided attempt; 20 minutes individual variation; 15 minutes away from screens; 20 minutes second demonstration or repair; 40 minutes independent task; 15 minutes feedback and saving; 10 minutes exit check. Total 180 minutes. If an idea takes longer, reduce the optional variation rather than skipping the explanation. Sessions 12 and 18 use most practice time for the checkpoint; sessions 19 to 24 use it for project mentoring and rehearsal.
'''
   write(td/f'{ident}_guide.md',teacher)
   if code in ('ML','DA'):
    cells=[cell('markdown',packet.split('## Follow the worked example')[0])]
    cells += [cell('markdown','## Worked example\nPredict the output, then run the following cell.'),cell('code',l['demo'])] if l['mode']=='python' else [cell('markdown','## Worked task\n'+l['demo'])]
    cells += [cell('markdown','Expected result: '+l['expected']+'\n\n## Your task\n'+l['task']+'\n\nRepair cue: '+l['repair']),cell('code','# Write your own code here.\n') if l['mode']=='python' else cell('markdown','Write your project evidence here.'),cell('markdown','## My explanation\nWhat I changed:\n\nHow I checked it:\n\nOne question or limitation:')]
    nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}},'nbformat':4,'nbformat_minor':5}
    # Stable cell IDs keep current notebook readers from requiring repair.
    for j,c in enumerate(cells):c['id']=f'{ident.lower()}-{j}'
    write(sd/f'{ident}.ipynb',json.dumps(nb,indent=2)+'\n')
   if l['mode']=='sql':write(sd/f'{ident}_example.sql','-- Worked example; your independent task belongs in a separate SQL file.\n'+l['demo']+'\n')
   syllabus += [f'### Week {week} session {i} {l["title"]}\n',l['explain']+'\n',f'Practice and evidence: {l["task"]}\n']
 write(ROOT/'teaching'/'CURRICULUM.md','\n'.join(syllabus))
 write(ROOT/'instructor_materials'/'reference_queries.sql','''-- Run against camp_shop.sqlite; instructor reference, not student assessment work.
SELECT COUNT(*) AS records,SUM(units) AS units,SUM(units*unit_price_ugx) AS revenue_ugx FROM sales;
SELECT item,SUM(units),SUM(units*unit_price_ugx),COUNT(*) FROM sales GROUP BY item ORDER BY item;
SELECT p.category,SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products p ON s.item=p.item GROUP BY p.category ORDER BY p.category;
SELECT COUNT(*) FROM sales WHERE units>=5;
''')
 write(ROOT/'instructor_materials'/'ml18_reference.py','''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
X,y=load_iris(return_X_y=True)
X_dev,X_test,y_dev,y_test=train_test_split(X,y,test_size=.2,random_state=7,stratify=y)
X_train,X_val,y_train,y_val=train_test_split(X_dev,y_dev,test_size=.25,random_state=7,stratify=y_dev)
assert (len(X_train),len(X_val),len(X_test))==(90,30,30)
baseline=DummyClassifier(strategy="most_frequent").fit(X_train,y_train)
print("Validation baseline",accuracy_score(y_val,baseline.predict(X_val)))
models=[DecisionTreeClassifier(max_depth=d,random_state=7).fit(X_train,y_train) for d in [1,3]]
scores=[accuracy_score(y_val,m.predict(X_val)) for m in models]
chosen=max(range(len(models)),key=lambda i:scores[i])
print("Validation scores",scores,"Chosen depth",[1,3][chosen])
print("Final test accuracy",accuracy_score(y_test,models[chosen].predict(X_test)))
print(confusion_matrix(y_test,models[chosen].predict(X_test)))
''')
 if __name__=='__main__':print('Built 48 lesson sheets, 48 instructor guides, 48 core notebooks and five SQL examples.')
if __name__=='__main__':
 build()
 from build_schools_camp_foundations import build as build_foundations
 build_foundations()
 build_delivery_plan()
