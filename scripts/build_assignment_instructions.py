"""Build student workflow instructions without changing questions or grading code."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'IUEA_Teaching_Plan'
DA = ROOT/'DataAnalysis_Track'
ROWS = json.loads((ROOT/'data/assessments.json').read_text())
LINKS = json.loads((ROOT/'data/submission_links.json').read_text())
MARKER = '<!-- assignment-workflow -->'

NOTEBOOK_STEPS = """1. Read the task text above each answer cell before editing. Complete the supplied notebook rather than starting an unrelated notebook.
2. Replace YOUR_ID in STUDENT_ID with your own identity, keeping the quotes. Check COHORT. Keep every required variable/function name unchanged.
3. Write code in the answer cells. A function must return the requested result; printing a result alone does not return it. Follow the specified input types, output types, units and missing-value rules.
4. Run cells from top to bottom. A blank answer can fail a visible check or raise NotImplementedError until you complete it. Read the first error and fix its cause. Never change helper files or tests to force a pass.
5. Where present, double-click the text cell headed My written evidence and write your own explanations, keeping that heading. Read every written criterion; copied task instructions or code comments do not replace your reasoning.
6. Restart the session and Run all. Upload missing input files again if the temporary runtime has lost them. Inspect the results, download the finished .ipynb and reopen it to check that you saved the final version.
"""

REPORT_STEPS = """Create a blank document in Word or Google Docs. Put your identity, cohort and assessment title at the top. Use the headings requested below, explain your decisions in your own words, and give units beside numerical results. In Google Docs choose File > Download > Microsoft Word (.docx) or PDF Document (.pdf). In Word use Save As for DOCX or Export for PDF. Reopen the downloaded file; check that text can be selected and charts have readable captions. A scan, photo or image-only PDF is not a readable report for automated assessment.
"""

def bank(row):
    aid,code=row['id'],row['cohort']
    if code=='DA':return DA/'assessment_banks'/aid
    if aid=='W02':return BASE/'setup'/code
    if aid in ('W03','W04','W05'):return BASE/'practicals'/aid/code
    return BASE/'assessment_banks'/aid/code/'A'

def instructions(row):
    aid,code=row['id'],row['cohort'];folder=bank(row)
    identity='DA learner ID from your roster' if code=='DA' else 'Student Registration Number exactly as on your university record'
    t=f"# {code} {row['label']} — {row['title']}\n\n## Start here\n\n"
    if aid in ('TEST1','TEST2'):
        t+='Use only the variant issued by the invigilator on the prepared lab computer. No internet, account sign-in, messaging or AI during the test. Read TASKS.md for the timed practical and typed Part B.\n\n'
    else:
        t+=f"Use your own {identity}. Sign in to upload with the Google account registered with the lecturer. If you need account or file help, read STUDENT_HOW_TO.md supplied with the student materials. A repository is a folder of saved project files; an upload form is where you hand in assessed work. Saving to a repository does not submit an assignment.\n\n"
    if aid=='W01':
        t+='No coding or GitHub account is needed for A1. Use the report route below.\n\n## Do the work\n\n'+REPORT_STEPS+'\n'
        t+='1. Add headings Problem 1, Problem 2, Problem 3 and My selected problem and dataset.\n2. For each problem describe a specific engineering decision, the quantity or category involved, and why ML is or is not suitable.\n3. Name plausible features (input information), a target where appropriate (the result to predict), a data source and a limitation.\n4. Choose one problem/dataset and explain why its evidence could answer the question. Do not claim a model was trained when you only proposed a study.\n\n## Check and submit\n\nCheck all three problems and your justified selection are present. Marks: problem framing 6, data and feasibility 8, judgement 6. Submit ONE complete report, preferably DOCX or selectable-text PDF. PPTX with full narration notes or a notebook containing the written report is also accepted. Do not upload several versions.\n\n'
    elif aid=='W02':
        csv=next(folder.glob('*.csv')).name
        t+=f"Before class, complete sections 1–2 of STUDENT_HOW_TO.md: Google and GitHub sign-in, download and extract the cohort ZIP. In class, follow sections 3–8.\n\n## Do the work\n\n1. Open proof_of_life.ipynb in Colab using File > Open notebook > Upload, and save your own copy in Drive. Upload {csv} through the Files sidebar. This Week 2 CSV has four data rows.\n2. Enter your Student Registration Number in STUDENT_ID, keeping quotes and slashes. Keep COHORT=\"{code}\". Run the cells as taught, repeat the increment cell and write your own explanation after the existing My explanation: prefix in its text cell; keep that prefix.\n3. Open repairs 01–04 when the lecturer directs you; return to proof_of_life.ipynb afterwards. The repairs and hello_engineering.py are practice, not uploads.\n4. Restart the session and Run all. Check proof_sum is 4, readings is 17 and rows holds the four supplied CSV records. Download the completed notebook as your own registration number with slashes replaced by underscores, followed by _W02.ipynb.\n5. On GitHub create a private repository with Add README enabled. Use Add file > Upload files to upload the downloaded notebook and {csv}; Commit changes to save them.\n6. Edit the repository README.md. In your own words include your programme, exact file list and step-by-step run instructions. Commit the edit and download the raw README.md file. See sections 6–7 of STUDENT_HOW_TO.md for each click. Do not submit the instruction README from the ZIP.\n\n## Check and submit\n\nUpload exactly TWO files together: your completed renamed notebook and your own README.md. Paste the repository URL into the form. The CSV stays in your repository/runtime; do not upload it to the form. A URL alone is not the submission. Check both filenames, click Submit and keep confirmation.\n\nMarks out of 20: notebook identity 2, proof_sum 4, fresh-run readings 4, correct CSV records 4, your execution-order explanation 3, your README 3.\n\nA1, Quiz 1, A2 and Quiz 2 are four separate tasks. Each quiz closes 24 hours after its own lecturer activation; assignment deadlines are separate. See WEEK1_CATCHUP.txt.\n\n"
    elif aid=='S05':
        t+='## Do the work\n\n1. Install DB Browser for SQLite from https://sqlitebrowser.org/dl/ using the Windows or macOS installer for your computer, or use the prepared lab installation. It is a desktop application, not a website account; no database account is needed.\n2. Copy the supplied riverside.db into your session folder, open DB Browser, choose Open Database and select that copy. Choose Execute SQL. Follow the SQL lab examples before building the assessed query.\n3. Build the 2025 Delivered report, net of returns, with one row per rep/month. Return columns in this order: region, rep_name, month, gross_ugx, returned_ugx, net_ugx. Use rep region, retain walk-in orders and combine multiple return events before joining.\n4. Run your query using the Execute button. Check there are no duplicate rep/month keys, all months are in 2025, and net equals gross minus returns. Add a SQL comment identifying a rep to discuss and why; the discussion is formative.\n5. Save the SQL text from the Execute SQL editor as your learner ID followed by _S05.sql. If using a text editor, save plain text with a .sql extension, not .sql.txt. Reopen the file and execute it against the issued database.\n\n## Check and submit\n\nSubmit exactly ONE .sql file containing the final report query, optionally with comments beginning --. Do not submit the database, CSV result, screenshot or the entire lab exercise. Marks: row keys 25, gross 25, returns 25, net 25; amount tolerance is 1 UGX after rounding.\n\n'
    elif aid in ('DEMO','S15'):
        t+='## Do the work\n\n'
        if aid=='DEMO':
            t+='1. In PowerPoint choose Blank Presentation, or open https://slides.google.com and choose Blank. Use readable slide text to explain your engineering question, method, results and limitations. Add your full spoken explanation in the Notes area beneath each slide.\n2. In a separate Word/Google Docs document, include your two individual written-defence answers, referring to specific cells/results in your own project. Use the two prompts issued by the lecturer; do not invent replacement questions.\n3. Add a 500-word individual reflection: what changed since Week 1, what remains difficult and two concrete Semester 2 goals. Add your complete AI-use declaration, including none if none was used.\n4. Save slides as PPTX (Google Slides: File > Download > Microsoft PowerPoint). Save the written defence/reflection/declaration as DOCX or selectable-text PDF. Reopen both; check narration is still in slide notes.\n\n## Check and submit\n\nSubmit the presentation PPTX and one document containing your individual defence, reflection and AI-use declaration together. Include the repository URL and team ID where applicable. The marks assess submitted evidence: presentation 35, individual defence 40, reflection 20, declaration 5.\n\n'
        else:
            t+='1. Use the Power BI lab walkthrough before this capstone. Windows: obtain Power BI Desktop from https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop. Mac: use the lecturer-provisioned browser workspace, already tested with your authorised teaching account, or a prepared Windows lab computer. A personal Gmail account is not a substitute for workspace access. Do not buy a licence or start a trial to unblock class.\n2. Load the five CSV tables into ONE model, set types, build the relationships, date table and three measures in lab_powerbi.md. Reconcile the totals before designing visuals. Save your .pbix locally or save the browser report in the designated workspace.\n3. Create the required one-page dashboard, capture readable visuals with visible filters, and write the question, numerical answer, supporting evidence and what would change your recommendation.\n4. Build a short PowerPoint presentation for the five-minute explanation. Put your narration in slide notes. Include the model/relationship evidence, measure formulas as text, dashboard evidence and recommendation.\n5. Complete all five S15CHECK lines from NUMERICAL_EVIDENCE.md using values read from your own model. Include them as plain text in slide notes or a DOCX/PDF appendix; screenshots alone cannot supply those values.\n\n## Check and submit\n\nUpload PPTX with narration notes and, if the written evidence is separate, its DOCX or selectable-text PDF. Include all requested numerical evidence in that upload set. Keep the PBIX or authorised report link as supporting project material and give the link in your evidence document. The upload form does not accept PBIX or ZIP. Check the five filter contexts and the distinction between delivered revenue before returns and net revenue.\n\n'
    else:
        notebooks=sorted(p.name for p in folder.glob('*.ipynb'))
        inputs=sorted(p.name for p in folder.iterdir() if p.suffix in ('.csv','.py','.db')) if folder.exists() else []
        t+='Open '+', '.join(notebooks)+' as the assignment notebook. '
        t+=('Keep these input/helper files in its runtime folder: '+', '.join(inputs)+'. ' if inputs else '')
        if aid not in ('TEST1','TEST2'):
            t+='In Colab use File > Open notebook > Upload for .ipynb; use the Files sidebar Upload button for data and .py helpers. Save your own notebook copy in Drive. '
        t+='Keep the issued raw files unchanged.\n\n## Do the work\n\n'+NOTEBOOK_STEPS+'\n'
        if aid in ('W03','W04','W05'):
            t+='Read README.md and each notebook question in order. The mark allocations in the notebook sum to 20. '
            if aid=='W04':t+='Use this week’s 300-row dataset, not Week 2’s four-row file with a similar name. Skip blank readings before converting to numbers. '
            if aid=='W05':t+='Create cost_per_kwh before selecting high_use so that the new column is included. '
            t+='\n\n'
        elif aid=='S09':
            t+='Read TASKS.md in full. Work in this order: inspect the raw inputs, normalise orders, clean line items, generate the report, reconcile the clean-table SQL and pandas results, then explain the raw currency-rounding difference. Write a separate cleaning log of at most 900 words covering the ten published written criteria.\n\n'+REPORT_STEPS+'\n'
        elif aid=='S13':
            t+='Choose one sector from TASKS.md. Read the matching snapshot README for provenance and units. Calculate its five named findings, create a captioned chart for each, then write your question, findings, limitations and recommendation in one report. Preserve the required FINDINGS keys and units.\n\n'+REPORT_STEPS+'\n'
        elif aid in ('DA_PROJECT','ML_PROJECT'):
            t+='Read TASKS.md and complete ALL its rubric criteria as well as the named functions. '
            if aid=='DA_PROJECT':t+='Frame the question, profile data, justify cleaning, make at least four labelled charts, interpret the findings and record each member’s contribution. '
            else:t+='Frame the prediction problem, document data and features, separate the equipment groups, compare the baseline and two fitted models, report validation evidence and limitations, and write the two-page engineering brief. '
            t+='Write your report in DOCX or selectable-text PDF. Include contribution and AI-use declarations where required, a repository URL and run instructions. Keep README, requirements.txt and source data in the repository; put concise relevant run/evidence text in the uploaded report too, because a link alone cannot be graded.\n\n'+REPORT_STEPS+'\n'
        elif aid in ('TEST1','TEST2'):
            t+='Read the assigned variant’s TASKS.md. Save the practical notebook before Part B. Type the Part B answers under a Part B subheading in the existing text cell beginning ## My written evidence; keep that exact heading. Do not execute code during that period. Include all required written evidence and chart captions in that notebook. Save again and hand it to the invigilator using the prescribed offline collection process.\n\n'
        else:
            t+='Read TASKS.md for the exact function contracts and marking criteria. Complete the functions first, then interpret the supplied scenario in My written evidence. Distinguish supplied comparison numbers from results you computed. Extra project exercises are practice and add no weekly marks.\n\n'
        t+='## Check and submit\n\n'
        if aid in ('DA_PROJECT','ML_PROJECT','S09','S13'):
            t+='Submit ONE completed notebook AND ONE complete DOCX or selectable-text PDF report together. Keep all required written sections in that report. '
        else:t+='Submit exactly ONE completed .ipynb notebook containing code, outputs and the required written evidence. '
        t+=f'Use your own identity in the filename, with slashes changed to underscores for IUEA, followed by _{aid}.ipynb. Do not submit the literal name STUDENT_ID. '
        if aid in ('TEST1','TEST2'):t+='The invigilator’s offline collection is authoritative; a later upload only transports that collected work. Do not keep editing after collection.\n\n'
        else:t+='Do not upload guided_practice.ipynb, helper files, the ZIP or raw data unless the brief specifically requests them.\n\n'
    if aid not in ('TEST1','TEST2'):
        t+='## How to hand in\n\nOpen the correct cohort/assessment form below and read its current deadline. Fill the required identity fields; leave Team ID blank for individual work. Choose Add file > Upload and select the complete required file set. Wait for the filenames to appear, then click Submit. Keep the confirmation page and local copies. Each file must be at most 10 MB. If replacing work before the deadline, send the complete set again; the latest on-time response replaces the earlier response. If the form is closed or upload fails, keep your files and contact the lecturer; do not use a different assignment form.\n\n'
    entry=LINKS.get(row['key'],{})
    if entry.get('url'):t+='Student submission link: '+entry['url']+'\n\n'
    if row.get('closes_at'):t+='Published closing time (UTC+03:00 is Kampala): '+row['closes_at']+'. Read the live form for any announced revision.\n\n'
    else:t+='Dates are not yet scheduled. Wait for the lecturer’s release and announced opening/deadline.\n\n'
    if aid in ('DA_PROJECT','ML_PROJECT','TEST1','TEST2','DEMO','S09','S13','S15'):
        t+='Preparation guidance only until the lecturer releases this assessment after its grading checks. These instructions do not open a form or release an unvalidated assessment.\n'
    return t

def main():
    index=['# Assignment instructions index','', 'Read the matching guide before starting. The lecturer releases assignments on their published schedule.','']
    for row in ROWS:
        guide=instructions(row);base=DA if row['cohort']=='DA' else BASE
        path=base/'student_guides'/row['cohort']/(row['id']+'.md');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(guide)
        relative=path.relative_to(ROOT).as_posix()
        link=('../'+relative) if base==DA else path.relative_to(BASE).as_posix()
        index.append(f"- [{row['key']}]({link})")
        folder=bank(row)
        if folder.exists():
            targets=sorted(folder.parent.glob('*/TASKS.md')) if row['id'] in ('TEST1','TEST2') else [folder/'TASKS.md']
            for target in targets:
                dest=target.parent
                if not dest.exists():continue
                (dest/'ASSIGNMENT_INSTRUCTIONS.md').write_text(guide)
                (dest/'ASSIGNMENT_INSTRUCTIONS.txt').write_text(guide)
                helpfile=(DA/'STUDENT_HOW_TO.md') if base==DA else (BASE/'setup/STUDENT_HOW_TO.md')
                (dest/'STUDENT_HOW_TO.md').write_text(helpfile.read_text())
                for npath in dest.glob('*.ipynb'):
                    if row['id']=='W02' and npath.name!='proof_of_life.ipynb':continue
                    nb=json.loads(npath.read_text());nb['cells']=[c for c in nb['cells'] if MARKER not in ''.join(c.get('source',[]))]
                    nb['cells'].insert(1,dict(cell_type='markdown',metadata={},source=(MARKER+'\n## Before you begin\nOpen ASSIGNMENT_INSTRUCTIONS.txt from your extracted folder for the starting files, steps, checks and exact upload list. Read STUDENT_HOW_TO.md in a text editor for account creation and Colab/download help. '+('This test is offline: use only the invigilator’s instructions; do not sign in to online accounts.' if row['id'] in ('TEST1','TEST2') else 'Keep the required names below unchanged. Write your own answers; guided_practice.ipynb is not a graded upload.')+'\n').splitlines(True)))
                    npath.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
    (BASE/'Assignment_Instructions_Index.md').write_text('\n'.join(index)+'\n')
    print('Built instructions for',len(ROWS),'assessments; code cells and marking contracts preserved.')

if __name__=='__main__':main()
