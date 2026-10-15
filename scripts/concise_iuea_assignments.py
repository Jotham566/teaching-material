"""Student instructions only: preserve executable cells, assessment contracts and marks."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'IUEA_Teaching_Plan'
sys.path.insert(0,str(BASE/'grader'))
from engineering_contracts import TASKS, DOMAINS
COMPONENTS=json.loads((BASE/'assessment_banks/assessment_components.json').read_text())
MARKER='<!-- assignment-workflow -->'
DETAIL='<!-- student-task-detail -->'
WRITTEN={
'W06':[
('duplicates','Why should a repeated record_id be kept only once? Explain the effect on counting observations.'),
('invalid','Why exclude a missing target or an invalid load rather than inventing or clipping a value?'),
('impute','Why use the median for missing ambient temperature, and why keep the raw data?'),
('limitations','Explain one meaningful limitation of the data or cleaning decisions.'),
('use','What use is justified by these teaching data? What would be needed before real deployment?')],
'W08':[
('choice','Which candidate would you recommend for further evaluation, using the supplied MAE comparison? Explain why.'),
('limits','What can these synthetic validation results tell you—and what can they not establish about real equipment?'),
('data','Name the input file, cohort identifier and target unit someone needs to reproduce the work.'),
('protocol','Describe the run order, group split and preprocessing rules needed to reproduce a fair comparison.')],
'W09':[
('costs','Calculate the total assumed cost for A and for B using 5 × FN + FP.'),
('tradeoff','Compare missed warnings and false alarms. Explain why accuracy alone may be misleading.'),
('choice','Choose a model using the assumed total cost and justify your choice.'),
('deployment','What costs or real warning data need checking before deployment?'),
('reproduce','Which labels and calculation rules must be saved so someone can reproduce your result?')],
'W10':[
('groups','Why must all observations from the same equipment ID stay in one partition?'),
('fit','Which data may fit preprocessing? How will E6 be protected during fitting and model selection?'),
('scope','What claim is supported by this synthetic evaluation? Explain its limits for real deployment.'),
('shift','How could unseen equipment or a hotter environment cause the model to fail?')],
'W11':[
('dictionary','Define each base feature and the interaction, with units. State when each becomes available.'),
('control','What must stay unchanged to isolate the effect of adding the interaction?'),
('ablation','Calculate and interpret the change in MAE in the supplied comparison.'),
('decision','Would you retain the interaction for this comparison? Justify your decision.'),
('limit','What does this one validation result fail to establish about other datasets or conditions?')],
'W12':[
('choice','Apply both limits and the tie-breaking rule. Choose a candidate and justify its eligibility and ranking.'),
('protocol','What must be identical for the candidates to be compared fairly?'),
('explanation','Explain the difference between a local explanation of one prediction and global feature importance.'),
('assumption','State the latency-budget and latency-measurement assumptions behind your decision.'),
('failure','Describe one realistic way the selected model could fail after deployment.'),
('change','What latency budget would make the tree eligible, and how would that change your choice?')],
}

def deadline(row,links):
    value=links.get(row['key'],{}).get('closeAt') or row.get('closes_at')
    if not value:return 'Wait for the lecturer to announce the deadline.'
    date=datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=3)))
    return date.strftime('%d %B %Y, %H:%M')+' Kampala. The live form shows any later change.'

def notebook_name(row):
    return 'proof_of_life.ipynb' if row['id']=='W02' else row['id']+'_student.ipynb'

def upload_list(row):
    aid=row['id']
    if aid=='W01':return 'ONE report: DOCX or selectable-text PDF is recommended. Existing PPTX-with-notes and written-notebook routes remain accepted.'
    if aid=='W02':return 'TWO files together: your completed notebook (.ipynb) AND your own README.md.'
    if aid in ('DA_PROJECT','ML_PROJECT'):return 'TWO files together: your completed notebook (.ipynb) AND one complete report (DOCX or selectable-text PDF).'
    if aid=='DEMO':return 'TWO files together: your presentation (.pptx, with narration notes) AND one DOCX/PDF containing your written defence, reflection and AI-use declaration.'
    return 'ONE completed assignment notebook (.ipynb).'

def help_line(aid):
    if aid in ('TEST1','TEST2'):return 'This is an offline test. Ask the invigilator for file or computer help; do not sign in online.'
    return 'Need help opening, saving or uploading? Use STUDENT_HOW_TO.md only for the step you are stuck on. It is a reference, not extra homework.'

def instructions(row,folder,links):
    aid,code=row['id'],row['cohort']
    lines=[f"# {code} {row['label']} — {row['title']}",f"**Submit:** {upload_list(row)}",f"**Deadline:** {deadline(row,links)}",'## 1. Start']
    if aid=='W01':
        lines+=['Open a blank Word or Google Docs document. No Python, Colab or GitHub is needed. Add your name, Student Registration Number and cohort.',
        '## 2. Complete four sections',
        '1. **Problem 1:** describe an engineering decision, its inputs and intended result, a possible data source and a limitation. Explain whether machine learning would help.\n2. **Problem 2:** answer the same points for a different problem.\n3. **Problem 3:** answer the same points for a third problem.\n4. **My selected problem and dataset:** choose one and justify why the proposed data could answer its question.',
        'Inputs are information used to make a prediction; the target is the result to predict. Propose the study—you are not asked to train a model.',
        '**Marks (20):** problem framing 6; data and feasibility 8; judgement 6.']
    elif aid=='W02':
        csv=next(folder.glob('*.csv')).name
        lines += [f'Open **proof_of_life.ipynb** in Colab. Upload **{csv}** to its Files sidebar. Use the Week 2 file with four data rows.',
        '## 2. Complete these steps',
        f'1. Enter your own Student Registration Number in STUDENT_ID; keep COHORT="{code}".\n2. Complete and run the main notebook. Write your execution-order explanation after **My explanation:**.\n3. Restart and run all cells. Check proof_sum = 4, readings = 17 and rows contains the four CSV records.\n4. Save your notebook and the CSV in your own private GitHub repository. Write your own README.md: programme, file list and how to run the notebook.',
        '**Marks (20):** identity 2; proof_sum 4; readings 4; CSV records 4; explanation 3; README 3.',
        '**Practice only:** repair notebooks 01–04 and hello_engineering.py. Do not upload them. The supplied instruction README is not your own README.']
    elif aid=='DEMO':
        lines+=['Use your completed project and repository. Open a blank PowerPoint presentation and a Word/Google Docs document.',
        '## 2. Prepare the evidence',
        '1. **Slides + narration notes (35 marks):** explain the engineering question, method, results and limitations.\n2. **Written defence (40):** answer the two prompts issued by the lecturer, citing your own cells/results.\n3. **Reflection (20):** write 500 words about progress since Week 1, remaining difficulties and two Semester 2 goals.\n4. **AI-use declaration (5):** describe assistance, or state none. Put items 2–4 in one document.',
        'Add the repository URL and team ID where applicable. Live discussion is practice; submit the written evidence for grading.']
    else:
        inputs=sorted(p.name for p in folder.iterdir() if p.suffix=='.csv')
        lines += [f'Open **{notebook_name(row)}**.'+(' Keep these supporting files beside it: '+', '.join(inputs)+'.' if inputs else '')]
        if aid not in ('TEST1','TEST2'):lines+=['In Colab: File → Open notebook → Upload. Add any supplied CSV files through the Files sidebar. Save your own copy in Drive.']
        if aid in ('W03','W05'):
            lines += ['No grading scripts are needed. Complete every task; your uploaded notebook is marked automatically after submission.']
        lines+=['## 2. Work down the notebook',
        f'1. Set STUDENT_ID to your own Student Registration Number, keeping quotes and slashes. Keep COHORT="{code}".\n2. Answer each numbered task immediately below its prompt. Keep the required names exactly as shown.']
        if aid in ('W03','W04','W05'):
            lines+=['3. Complete every task. The marks beside the tasks total **20**. No separate report or written-evidence section is required.']
            lines+=['The Repository URL field is optional for this assignment; a GitHub repository is not required.']
            if aid=='W03':lines+=['Five tasks: weight, signed percent error, your cohort formula, efficiency and the largest error. Formulas and units are beside each question. A loop is not required.']
            if aid=='W04':lines+=['Four outputs, 5 marks each: valid_count, mean_reading, above_limit and group_means. Use Week 4’s **300-row CSV**, not the four-row Week 2 file. Skip blank readings. A4 is a Python notebook task, despite the title “Reading report”.']
            if aid=='W05':lines+=['Six tasks: load the data, count meters, calculate cost_per_kwh, filter high_use, calculate the mean and find peak_building. Create cost_per_kwh before filtering.']
        elif aid in ('DA_PROJECT','ML_PROJECT'):
            lines+=['3. Use the **Report checklist** in the notebook to write one report. Include all listed evidence, captions, repository URL and run instructions. A repository link alone is not the report.']
            if aid=='ML_PROJECT':lines+=['Include the two-page engineering brief, contribution log and AI-use declaration.']
        else:
            lines+=['3. Answer the **Written questions** in the notebook’s **My written evidence** cell. Use your own words. The prompts show the marks.']
            if aid in WRITTEN and aid!='W06':lines+=['The written questions use the supplied scenario. Label these as supplied results, not measurements you computed.']
            if aid in ('TEST1','TEST2'):lines+=['Follow the invigilator’s timing. Type Part B under a Part B subheading in My written evidence, without running code during Part B.']
        lines+=['## 3. Check and save','Restart and run all cells from the top. Fix errors, then download/save the completed notebook. For the filename only, replace slashes in your registration number with underscores and add _'+aid+'.ipynb.']
    lines+=['## 4. Hand in' if aid not in ('W01','W02','DEMO') else '## 3. Hand in']
    if aid in ('TEST1','TEST2'):
        lines+=['Give the saved notebook to the invigilator through the prescribed offline collection process. Stop editing when collected. Any later Google upload only transfers that collected file.']
    else:
        lines+=['Open your cohort’s form below. Enter your Student Registration Number. Choose **Add file → Upload**, attach the required file(s), then press **Submit**. Keep the confirmation.',
        'For individual work, leave Team ID blank. Each file must be at most 10 MB. A replacement before the deadline must contain the complete file set again.',
        '**Do not submit:** the ZIP, guided_practice.ipynb, raw CSVs or helper scripts.']
        if aid=='W02':lines+=['Paste your repository URL in the form as well; the URL does not replace the two files.']
    if links.get(row['key'],{}).get('url'):lines+=['**Submission link:** '+links[row['key']]['url']]
    lines+=['## Help only if needed',help_line(aid)]
    if aid in ('DA_PROJECT','ML_PROJECT','TEST1','TEST2','DEMO'):lines+=['Preparation only until the lecturer releases this assessment. This guide does not open its form.']
    return '\n\n'.join(lines)+'\n'

def written_questions(aid):
    rubric=json.loads((BASE/'grader/rubrics/hybrid'/f'{aid}.json').read_text())
    if aid in WRITTEN:
        lookup={c['id']:c for c in rubric['criteria']}
        prompts=[f'{i}. **{lookup[key]["maximum"]:g} '+('mark' if lookup[key]['maximum']==1 else 'marks')+f':** {q}' for i,(key,q) in enumerate(WRITTEN[aid],1)]
    else:
        prompts=[]
        for i,c in enumerate(rubric['criteria'],1):
            text=c['description'].split(' Assess the written justification')[0]
            # Keep existing evidence criteria while removing assessor-directed boilerplate.
            prompts.append(f'{i}. **{c["title"]} ({c["maximum"]:g} written marks):** '+text)
    lead='## Report checklist' if aid in ('DA_PROJECT','ML_PROJECT') else '## Written questions'
    parts=[DETAIL,lead]
    if rubric.get('scenario'):parts+=['**Supplied scenario (use for the written questions):**\n\n'+rubric['scenario']]
    if aid in ('DA_PROJECT','ML_PROJECT'):parts+=['Put the complete written evidence in your report, with relevant notebook results and chart captions.']
    else:parts+=['Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.']
    parts+=prompts
    if aid=='TEST2':parts+=['**Data-preparation marking rule:** the required leakage-safe group split must pass for written data-preparation marks. Other criteria are marked separately.']
    if aid in ('TEST1','TEST2'):
        parts+=['### Part B — invigilator-controlled timing','15 minutes setup; 120 minutes practical; 25 minutes typed offline reasoning with no code execution; 20 minutes collection. No internet, messaging or AI.','Under a Part B subheading answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required?']
    return '\n\n'.join(parts)+'\n'

def function_prompt(task,marks):
    signature,contract=TASKS[task]
    if task=='charts4':contract=TASKS['charts'][1]+' Return all four figures as a list of actual matplotlib Figure objects.'
    # Same contracts, broken into one instruction per bullet.
    pieces=re.split(r'(?<=[.;]) (?=[A-Z])',contract)
    pieces={
      'clean':[
        'Return a list of copied records, keeping their original order. Do not change the raw input.',
        'Keep only the first occurrence of each record_id.',
        'Drop a record if target is missing or load_pct is outside 0–100 inclusive.',
        'Using the remaining records, find the median of the non-missing ambient_c values. Use it to fill missing ambient_c.',
        'Make no other changes.'],
      'audit':[
        'Return integer counts describing the two lists you receive; do not change either list.',
        'raw_count: number of records in raw_records. cleaned_count: number in cleaned_records.',
        'duplicate_ids: number of cleaned records beyond the first occurrence of each record_id.',
        'missing_targets: number of cleaned records with target=None.',
        'invalid_loads: number of cleaned records with load_pct outside 0–100 inclusive.',
        'Count any defects still present in the supplied cleaned_records; do not assume they are all zero.'],
      'regression':[
        'Use load_pct and ambient_c as the two input features. Feature records do not contain target.',
        'Fit preprocessing on training_records only.',
        'Fit a baseline that predicts the mean training target.',
        'Fit linear regression and a decision tree with max_depth=4 and random_state=17.',
        'Predict for feature_records using all three models.'],
    }.get(task,pieces)
    extra={
      'summary':'Return a dictionary with exactly count, mean, minimum, maximum and group_means. group_means is a dictionary from equipment ID to its mean target.',
      'audit':'Return a dictionary with exactly raw_count, cleaned_count, duplicate_ids, missing_targets and invalid_loads.',
      'errors':'Return a dictionary with mae and rmse. MAE is the mean absolute error; RMSE is the square root of the mean squared error. Match actual and predicted by position.',
      'regression':'Return a dictionary with baseline, linear and tree; each value is a prediction list in feature_records order.',
      'split':'Return a dictionary with train, validation and test. Each value is a list of record_id values.',
      'classification':'Return a dictionary with tp, tn, fp, fn, precision, recall and cost. 1 means warning and 0 means no warning; actual is the true label and predicted is the model label.',
    }.get(task)
    return f'### `{signature}` — {marks:g} marks\n\n'+'\n'.join('- '+x for x in pieces)+ ('\n- '+extra if extra else '')+'\n\nWrite your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.\n'

def early_prompts(code):
    q3={
    'CML3112':'Write slab_mass(area_m2, thickness_m). Return the slab mass in kg. Volume = area × thickness; mass = volume × 2400 kg/m³. Both lengths are already in metres; area is in m².',
    'CML3111':'Write power_loss(current, resistance). Return power lost in watts. Use current² × resistance; current is in amperes and resistance in ohms.',
    'CML3113':'Write mud_pressure(depth_m, density). Return pressure in kPa. Pressure in Pa = density × 9.81 × depth_m; divide by 1000 for kPa. Depth is in metres and density in kg/m³.'}[code]
    return [
    '## q1: 3 marks\nA 40 kg motor sits on a bench. Set weight_n to its weight in newtons. Weight = mass × gravitational acceleration; use 9.81 m/s² for the acceleration.',
    '## q2: 4 marks\nWrite percent_error(measured, expected). Return the signed percentage: 100 × (measured − expected) / expected. The reference expected value is nonzero. Keep the sign: a negative result means the measurement is below the reference. Return a number, not text with a % symbol.',
    '## q3: 3 marks\n'+q3,
    '## q4: 5 marks\nWrite efficiency(out_w, in_w). If input power in_w is zero or negative, return None. Otherwise return 100 × out_w / in_w. Both powers are in watts. Return a number, not text with a % symbol.',
    '## q5: 5 marks\nUse the six READINGS already supplied and a nominal (reference) value of 100.\n\n1. Use your percent_error function for each reading.\n2. Compare the sizes of the errors, ignoring their signs for this comparison.\n3. Set worst_reading to the original reading with the largest error size.\n4. Set worst_error to that reading’s signed percent error, keeping its original sign.\n\nYou may compare the six readings directly. A loop is not required.'
    ]

def apply_to_folder(row,folder,guide):
    """Idempotent markdown-only notebook changes; never reset work or outputs."""
    aid=row['id'];code=row['cohort']
    if not folder.exists():return
    for name in ('ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt'):(folder/name).write_text(guide)
    (folder/'STUDENT_HOW_TO.md').write_text((BASE/'setup/STUDENT_HOW_TO.md').read_text())
    notebooks=[folder/notebook_name(row)]
    for path in notebooks:
        if not path.exists():continue
        nb=json.loads(path.read_text());nb['cells']=[c for c in nb['cells'] if MARKER not in ''.join(c.get('source',[])) and DETAIL not in ''.join(c.get('source',[]))]
        def cell(text):return dict(cell_type='markdown',metadata={},source=text.splitlines(True))
        # One working place: the short brief is in the notebook, not another required file.
        nb['cells'].insert(1,cell(MARKER+'\n'+guide))
        if aid in ('W03','W04','W05'):
            nb['cells'][0]=cell(f'# {code} {row["label"]} — {row["title"]}\nComplete the tasks below in this notebook. The short instructions follow.\n')
        if aid=='W03':
            prompts=early_prompts(code)
            for c in nb['cells']:
                text=''.join(c.get('source',[]));m=re.match(r'## q([1-5]):',text)
                if c['cell_type']=='markdown' and m:c['source']=(prompts[int(m[1])-1]+'\n').splitlines(True)
        if aid in COMPONENTS:
            parts=COMPONENTS[aid]['criterion_allocation']
            for c in nb['cells']:
                if c['cell_type']!='markdown':continue
                text=''.join(c['source'])
                for part in parts:
                    sig=TASKS[part['task']][0]
                    if text.startswith(sig+' —') or text.startswith('### `'+sig+'`'):
                        c['source']=function_prompt(part['task'],part['marks']).splitlines(True)
            evidence=next(i for i,c in enumerate(nb['cells']) if ''.join(c.get('source',[])).startswith('## My written evidence'))
            domain,unit,*_=DOMAINS[code]
            context=f'{DETAIL}\n## Your data\n\nInvestigate {domain}; target unit: **{unit}**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.\n\nA record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.\n'
            nb['cells'].insert(2,cell(context));evidence+=1
            nb['cells'].insert(evidence,cell(written_questions(aid)))
            # TASKS.md is an alternative view of the exact prompts, not extra work.
            tasks=[f'# {code} {row["label"]} — task reference','These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.',context.replace(DETAIL+'\n','')]
            tasks += [function_prompt(x['task'],x['marks']) for x in parts]
            tasks += [written_questions(aid).replace(DETAIL+'\n',''),'## Submit',upload_list(row)]
            (folder/'TASKS.md').write_text('\n\n'.join(tasks)+'\n')
        path.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
    if aid in ('W03','W04','W05'):
        (folder/'README.md').write_text(f'# {code} {row["label"]} — {row["title"]}\n\nOpen **{notebook_name(row)}**. Its opening instructions and task cells contain all required work.\n\nSubmit {upload_list(row)}\n\nASSIGNMENT_INSTRUCTIONS.txt is a separate copy of the notebook instructions. STUDENT_HOW_TO.md is optional setup/file help. guided_practice.ipynb is ungraded practice.\n')
    elif aid=='W02':
        (folder/'README.md').write_text(f'# {code} A2 package guide\n\nOpen **proof_of_life.ipynb** first. Its opening instructions contain the task, exact files and marks.\n\nThis supplied README is a package guide, not the README you submit. Write your own README in your repository as the notebook requests.\n\nRepairs 01–04 and hello_engineering.py are practice only. STUDENT_HOW_TO.md is help when needed; ASSIGNMENT_INSTRUCTIONS.txt repeats the notebook instructions.\n')

def form_brief(row,folder):
    aid=row['id']
    lines=[f'{row["cohort"]} {row["label"]} — {row["title"]}', 'WHAT TO UPLOAD',upload_list(row),'WHERE TO DO THE WORK']
    if aid=='W01':lines+=['Your report needs four sections: Problem 1, Problem 2, Problem 3, and My selected problem and dataset. For each problem explain the decision, possible inputs/target, data source, limitation and whether ML helps. Justify your selection. No coding or GitHub is required.']
    elif aid=='DEMO':lines+=['Use the issued presentation/defence prompts. Put narration in slide notes. The document must include both defence answers, the 500-word reflection and AI-use declaration.']
    else:lines+=['Open '+notebook_name(row)+'. Read its short opening instructions and complete each task in order. The marks are beside the tasks.']
    if aid=='W02':lines+=['Write your own README.md with your programme, file list and run instructions. Paste your private repository URL below. The repair notebooks and hello_engineering.py are practice only.']
    if aid=='W04':lines+=['A4 “Reading report” is a Python notebook task, not a Word report. Use the Week 4 CSV (300 rows).']
    if aid in ('W03','W04','W05'):lines+=['No separate report or written-evidence section is required.']
    elif aid in WRITTEN:lines+=['Include answers to the written questions in the notebook cell headed My written evidence.']
    if aid in ('TEST1','TEST2'):lines+=['Upload only the file collected by the invigilator. Offline collection is authoritative; do not edit it afterwards.']
    lines+=['BEFORE SUBMITTING','Save/download the completed file(s). For notebooks, restart and run all cells first. Enter your own Student Registration Number exactly as on your university record. Leave Team ID blank for individual work.','Choose Add file > Upload, wait for the filenames, then press Submit. Keep the confirmation. Maximum 10 MB per file. A replacement before the deadline must contain the whole file set.','Do not upload the ZIP, guided_practice.ipynb, CSV data or helper scripts.','NEED HELP?','Use STUDENT_HOW_TO.md from your package for opening, saving or uploading. If access fails, keep your work and contact the lecturer.']
    return '\n\n'.join(lines)
