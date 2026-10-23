"""Build the approved fully automatic Colab tests; no answer keys in student files."""
import csv,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';G=BASE/'grader'
sys.path.insert(0,str(G))
from engineering_contracts import DOMAINS,TASKS,dataset
from colab_exam_contracts import PARTS,VERSION
SCENARIOS={
'TEST1':[
('D1','A repeated record_id comes from uploading the same observation twice. Why keep only the first?','A: To make every equipment mean equal. | B: To avoid counting one observation twice. | C: To remove all observations for that equipment.'),
('D2','A row has no target value. Why exclude it from this target analysis?','A: A blank target always means zero. | B: It proves the equipment failed. | C: The measured result is unavailable; inventing it would distort the analysis.'),
('D3','The load/target scatter rises from left to right. What does this establish?','A: An association in these observations, not proof that load causes the target. | B: Load alone causes every change. | C: The equipment is unsafe.'),
('D4','The median ambient temperature is used for missing entries. Which limitation remains?','A: All missing values are now known measurements. | B: Filled values are estimates and can change the results. | C: The original data no longer need to be kept.'),
('D5','Equipment E2 has the largest mean target in these synthetic records. What is justified?','A: Replace E2 immediately. | B: E2 must always have the largest target in the real world. | C: Report the observed difference; investigate representative measured data before acting.'),
('D6','The chart x-axis is record_id. Can it be described as a time trend?','A: No; a record identifier is not a timestamp. | B: Yes; each ID represents one hour. | C: Yes; IDs prove observations are equally spaced in time.')],
'TEST2':[
('D1','Why keep all records for an equipment ID in one partition?','A: To make all partition sizes equal. | B: To select equipment using target values. | C: To avoid evaluating on equipment already represented during fitting.'),
('D2','Which records may determine the median used to fill missing model inputs?','A: Training records only; reuse those medians for validation and test. | B: All records before splitting. | C: Test records because they are the newest.'),
('D3','Supplied validation MAE: baseline 4.0, linear 1.2, tree 1.8 target units. Select by smallest validation MAE.','A: Baseline. | B: Linear. | C: Tree.'),
('D4','When may E6 test targets be used?','A: While choosing the model with the smallest error. | B: To fit the imputer. | C: Once for final evaluation after model selection is fixed.'),
('D5','A few predictions have very large errors. Why can RMSE exceed MAE?','A: Squaring errors gives larger errors more influence. | B: RMSE is a percentage. | C: MAE ignores every large error.'),
('D6','A model performs well on this synthetic dataset. What is the next justified step?','A: Deploy it as a safety system immediately. | B: Evaluate representative measured data and operating conditions before considering deployment. | C: Claim it works on every engineering system.')]
}

def cell(text,code=False):
    d=dict(cell_type='code' if code else 'markdown',metadata={},source=text.splitlines(True))
    if code:d.update(execution_count=None,outputs=[])
    return d

TEST1_GUIDANCE = "# {course} TEST1 — Take-home practical test\n\nIndividual work • 100 marks • Up to three hours from **Start test**.\n\n{deadline}\nThe timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the class closing time. Colab may still allow editing afterwards, but late work is not accepted for grading.\n\n## 1. Open your own working copy\nOn the entry page, enter your full name, Google account email and Student Registration Number. Use that same Google account throughout. Click **Open my test in Colab**, then **File → Save a copy in Drive**. Work in this saved copy, not the read-only original. Click **Connect** if shown. To resume your work, reopen your saved copy from Google Drive; opening the original again does not recover your answers.\n\n## 2. Load the data\nCheck the identity cell near the top. Tell your lecturer immediately if the details are wrong; do not change the supplied course, test or allocation settings. Run the identity cell using the triangle beside it. Then run **Load the supplied CSV and Python libraries**. In the issued notebook this creates `engineering_data.csv` automatically; no separate CSV upload is needed. Wait for the preview and row count. After a runtime reset, rerun these setup cells before your work. If using a backup notebook without an embedded CSV setup cell, upload your assigned `engineering_data.csv` through Colab's folder icon first.\n\n## 3. Complete the questions\nWork from top to bottom. Read each question, write your code in its code cell and run it. Keep supplied function names and required output formats unchanged. Use pandas as instructed. Complete the eight coding tasks using pandas, matplotlib and ordinary Python. There are no interpretation choices or written report. Save regularly using **File → Save**.\n\n## 4. Submit — allow at least 20 minutes\n1. Run your completed cells, check the results and save. Submit your completed work even if some questions are unfinished.\n2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.\n3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.\n4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.\n5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.\n\n**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. Marks are calculated after the test. If you replace your submission, submit a complete new snapshot and its form before the same deadline.\n\n## If something fails\nRecord the error and contact your lecturer immediately, before the deadline. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun setup; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.\n\nNo AI-generated solutions, collaboration, messaging or copied answers.\n"

def brief(cohort,exam,url=''):
    if exam == 'TEST1':
        from build_test1_coding import student_guide
        return student_guide(cohort)
    return f'''# {cohort} {exam} — Colab practical test

**Submit one notebook snapshot:** your completed `{exam}_student.ipynb`. Total: **100 marks**. Individual work.

1. Open your lecturer’s test entry link or scan its QR code. Enter your full name, Google email and Student Registration Number. Download the notebook and CSV shown on your page. On your laptop, open Colab → **File → Open notebook → Upload** and select the notebook. Save your own copy in Drive.
2. In Colab's **Files** sidebar, upload your downloaded `engineering_data.csv`. Do not rename it. Enter your name, email and Student Registration Number in the identity cell. Keep the supplied course, test and internal allocation settings unchanged.
3. Work from top to bottom. Write each function beneath its question. Use pandas. The notebook explains the columns, return formats and marks. Answer the six interpretation questions by putting A, B or C in `DECISIONS`.
4. Restart the session and run all cells. If Colab asks for the CSV again, upload the same file. Fix errors and save. Run the final submission cell.
5. Click **Submit test** at the bottom of the notebook. Authorize your own Google account if asked. The button saves a snapshot and prepares a form link. Open that link using the same account, check your details, tick the email confirmation box and press **Submit** on the form. Keep the confirmation. The notebook button alone is not a completed submission. No manual download or file upload is needed. Keep the snapshot in Drive until grades are released.

**Timing:** 15 minutes setup, 120 minutes coding, 25 minutes interpretation and checking, 20 minutes final save and submission (180 minutes total). The invigilator announces the exact start and deadline. Report connection problems immediately.

**Rules:** Colab and the submission form are permitted. No AI-generated solutions, messaging, collaboration or copied answers. Follow the invigilator's rules for other resources. The lecturer's isolated grader reruns your code on unseen data; stored outputs and claimed marks are not trusted. Partial credit is available for independent checked outputs. An error in one task does not automatically zero the entire test.

**Do not submit:** ZIP, CSV, PDF, screenshots or grading scripts. No separate written report. A replacement before the deadline must contain the complete notebook. The latest on-time submission is reviewed for marking; earlier attempts remain in the audit log. If that attempt has a technical or identity problem, its mark stays pending until resolved.

**Submission:** use the generated link from the notebook’s Submit test button. A general form link will not contain your prepared snapshot.
'''

def build():
    config=json.loads((ROOT/'data/colab_test_submission_config.json').read_text())
    links=config['forms']
    helper=(BASE/'test_operations/colab_submit_cell.py').read_text()
    components=json.loads((BASE/'assessment_banks/assessment_components.json').read_text())
    for exam,parts in PARTS.items():
        if exam == 'TEST1':
            continue  # Coding-only Test 1 is generated independently below.
        titles={'clean':'Cleaning','summary':'Summary statistics','charts':'Three labelled charts','findings':'Five numerical findings','split':'Equipment-group split','regression':'Baseline, linear and tree predictions','errors':'MAE and RMSE','decisions':'Structured interpretation'}
        rubric=dict(id=exam+'-'+VERSION,title='Practical '+exam,maximum=100,grading='deterministic',criteria=[dict(id=f'q{i}',title=titles[t],maximum=m,description=('Six scenario choices in DECISIONS; 5 marks for each correct choice.' if t=='decisions' else TASKS[t][1])) for i,(t,m) in enumerate(parts,1)])
        (G/'rubrics'/f'{exam}.json').write_text(json.dumps(rubric,indent=2)+'\n')
        (G/'rubrics/hybrid'/f'{exam}.json').write_text(json.dumps(dict(id=exam+'-'+VERSION,title='No AI grading component',maximum=0,assessment_maximum=100,deterministic_maximum=100,criteria=[],note='This test is marked entirely by the deterministic Colab exam grader.'),indent=2)+'\n')
        questions={f'q{i}':dict(marks=m,visible=False,prompt=t,answer_vars=[]) for i,(t,m) in enumerate(parts,1)}
        (G/'specs'/f'spec_{exam}.py').write_text(f'ASSIGNMENT={exam!r}\nTITLE={exam!r}\nVERSION={VERSION!r}\nDEFAULT_COHORT=""\nQUESTION_ORDER={list(questions)!r}\nQUESTIONS={questions!r}\n')
        checks={f'q{i}':t for i,(t,m) in enumerate(parts,1)}
        (G/'specs/hidden'/f'spec_{exam}_hidden.py').write_text('from colab_exam_contracts import assess\nQUESTIONS={\n'+',\n'.join(f'{q!r}: {{"check": lambda ns: assess(ns,{exam!r},{t!r})}}' for q,t in checks.items())+'\n}\n')
        components[exam]=dict(maximum=100,deterministic_maximum=100,reasoning_maximum=0,version=VERSION,parts=parts)
        for cohort,(domain,unit,*_) in DOMAINS.items():
            url=links.get(cohort+'|'+exam,{}).get('url','')
            guide=brief(cohort,exam,url)
            (BASE/'student_guides'/cohort/(exam+'.md')).write_text(guide)
            for variant,seed in [('A',17),('B',29),('C',43)]:
                folder=BASE/'assessment_banks'/exam/cohort/variant;folder.mkdir(parents=True,exist_ok=True)
                rows=dataset(cohort,seed,dirty=True)
                with (folder/'engineering_data.csv').open('w') as f:
                    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
                cells=[cell(guide),cell(f'FULL_NAME = ""\nEMAIL = ""\nSTUDENT_ID = ""  # Your Student Registration Number exactly as on your university record\nCOHORT = "{cohort}"\nTEST_ID = "{exam}"\nVARIANT = "{variant}"\n',True),
                    cell(f'## Understand the data\nEach row is one synthetic observation of {domain}. `record_id` identifies a record; it is not time. `equipment_id` identifies equipment and repeats across observations. `load_pct` is load in percent (valid range 0–100 inclusive). `ambient_c` is ambient temperature in degrees Celsius. `target` is {domain}, measured in **{unit}**. Blank CSV values become missing values. These data are for teaching, not operational decisions.\n\nA DataFrame is a table. The supplied helper converts it to a list of dictionaries: one dictionary per row, column names as keys, with missing values represented by `None`. Your functions accept these lists and return the stated structures. Keep function names, argument order and dictionary keys exactly as printed. Keep full numerical precision.'),
                    cell('import pandas as pd\nimport matplotlib.pyplot as plt\n\ndef records_from_table(table):\n    objects = table.astype(object)\n    return objects.where(table.notna(), None).to_dict("records")\n\nraw_table = pd.read_csv("engineering_data.csv")\nrecords = records_from_table(raw_table)\nprint(raw_table.head())\nprint("Rows:", len(raw_table))\n',True)]
                if exam=='TEST2':
                    cells += [cell('## Supplied preparation — not graded\nKeep the first copy of each record ID, exclude rows without a target and rows outside the valid load range. These are fixed row rules, not learned model parameters. **Do not fill missing ambient temperatures here.** Your model function must learn its median only from training records using `SimpleImputer(strategy="median")`, followed by the model in a scikit-learn pipeline. Features are `load_pct` then `ambient_c`, in that order. The target must not be a feature.'),cell('eligible = raw_table.drop_duplicates("record_id").copy()\neligible = eligible[eligible["target"].notna() & eligible["load_pct"].between(0, 100)].copy()\nrecords = records_from_table(eligible)\n',True)]
                for i,(task,marks) in enumerate(parts,1):
                    if task=='decisions':continue
                    signature,prompt=TASKS[task]
                    if task=='regression':prompt+=' Use SimpleImputer(strategy="median") fitted on training records only, separately in each model pipeline. The baseline is the mean training target. Preserve feature order: load_pct, ambient_c.'
                    if task=='charts':prompt+=' Only the first three charts are required for this test. Return them in the stated order.'
                    cells += [cell(f'## Task {i}: {task.title()} — {marks} marks\n`{signature}`\n\n{prompt}\n\nFor calculations, start with `table = pd.DataFrame(...)`, replacing `...` with the input argument. Calculate from the input passed to your function, not from the global CSV variable. Hidden checks use different numbers with the same columns and rules.'),cell(f'def {signature}:\n    # Replace this placeholder with your solution.\n    raise NotImplementedError("Complete this task")\n',True)]
                cells += [cell('## Structured interpretation — 30 marks\nChoose exactly one option per question. Each is worth 5 marks. These questions use the stated scenarios; do not replace their supplied values with your CSV results.\n\n'+'\n\n'.join(f'**{k}. {q}**\n\n{o}' for k,q,o in SCENARIOS[exam])),cell('DECISIONS = {"D1": "", "D2": "", "D3": "", "D4": "", "D5": "", "D6": ""}\n',True)]
                driver='cleaned = clean_records(records)\nprint(summarize_records(cleaned))\nfigures = build_charts(cleaned)\nplt.show()\nprint(five_findings(cleaned))\n' if exam=='TEST1' else 'partitions = group_split(records)\ntraining = [r for r in records if r["record_id"] in partitions["train"]]\nvalidation = [r for r in records if r["record_id"] in partitions["validation"]]\nfeatures = [{k: v for k, v in r.items() if k != "target"} for r in validation]\npredictions = predict_regression(training, features)\nactual = [r["target"] for r in validation]\nfor name, predicted in predictions.items():\n    print(name, regression_errors(actual, predicted))\n# E6 is reserved for final evaluation; do not use it to select a model.\n'
                cells += [cell('## Run your functions on the supplied CSV\nRun this supplied cell after implementing the tasks. It calls your functions in the required order and displays their results. This is a check of your work, not an extra task or additional marks. If a function is unfinished, return to that task. Function checks are independent: an unfinished earlier function does not prevent the grader checking later functions on its own inputs.'),cell(driver,True)]
                cells.append(cell('## Submit your test\nRun the cell below and click **Submit test**. Open the generated form link, check your details and press **Submit** there. Use your own Google account in both Colab and the form. Wait for the form confirmation. If anything fails, contact your lecturer before your personal deadline (or the announced deadline for an invigilated test). Do not edit the saved snapshot.'))
                submit=cell(helper.replace('__EXAM_CONFIG__',repr(dict(lecturer_email=config['lecturer_email'],forms={cohort+'|'+exam:links[cohort+'|'+exam]}))),True)
                submit['metadata']['tags']=['iuea-submission','autograde-skip']
                submit['metadata']['cellView']='form'
                submit['source'].insert(0, '#@title Submit your test\n')
                cells.append(submit)
                nb=dict(cells=cells,metadata=dict(iuea_exam_version=VERSION,kernelspec=dict(display_name='Python 3',language='python',name='python3')),nbformat=4,nbformat_minor=5)
                (folder/(exam+'_student.ipynb')).write_text(json.dumps(nb,indent=1,ensure_ascii=False)+'\n')
                for name in ['TASKS.md','ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt','STUDENT_HOW_TO.md']:(folder/name).write_text(guide)
                # These are invigilator-issued, variant-specific packets; no grader or solutions.
                package=BASE/'assessment_banks'/exam/f'{cohort}_{exam}_{variant}_student.zip'
                with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
                    for name in [exam+'_student.ipynb','engineering_data.csv','ASSIGNMENT_INSTRUCTIONS.txt']:z.write(folder/name,name)
    (BASE/'assessment_banks/assessment_components.json').write_text(json.dumps(components,indent=2)+'\n')
    path=ROOT/'data/assessments.json';rows=json.loads(path.read_text())
    for r in rows:
        if r['id'] == 'TEST2' and r['cohort'] in DOMAINS:r.update(grading='notebook',formats=['ipynb'],assessment_version=VERSION)
    path.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    from build_test1_coding import build_test1
    build_test1()

if __name__=='__main__':build()
