"""Package ready practicals using an explicit allowlist; no lecturer keys."""
from pathlib import Path
import zipfile,json,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'IUEA_Teaching_Plan'
LINKS=json.loads((ROOT/'data/submission_links.json').read_text()) if (ROOT/'data/submission_links.json').exists() else {}
OUT=BASE/'student_packages';OUT.mkdir(exist_ok=True)
beginner_update='--beginner-update' in sys.argv
count=0
for code in ('CML3111','CML3112','CML3113'):
    for week in (2,3,4,5,6,8,9,10,11,12):
        if beginner_update and week==2 and code=='CML3112':continue
        source=BASE/'setup'/code if week==2 else BASE/'practicals'/f'W{week:02}'/code if week<=5 else BASE/'assessment_banks'/f'W{week:02}'/code/'A'
        if not source.exists():raise FileNotFoundError(source)
        files=[p for p in source.iterdir() if p.suffix in ('.ipynb','.csv','.md','.py')]
        files += [source/'ASSIGNMENT_INSTRUCTIONS.txt']
        if not any(p.name=='STUDENT_HOW_TO.md' for p in files):files += [BASE/'setup/STUDENT_HOW_TO.md']
        if week==2:files += [BASE/'setup/README.md',BASE/'setup/A2_assignment_brief.md',BASE/'setup/A1_assignment_brief.md',BASE/'IUEA_ML_Student_Setup_Guide.docx']
        with zipfile.ZipFile(OUT/f'{code}_W{week:02}_student.zip','w',zipfile.ZIP_DEFLATED) as z:
            lesson=BASE/'guided_practice'/code/f'W{week:02}'
            if lesson.exists():
                if (lesson/'guided_practice.ipynb').exists():z.write(lesson/'guided_practice.ipynb','guided_practice.ipynb')
                if week!=2:
                    notebooks=[p.name for p in files if p.suffix=='.ipynb']
                    z.writestr('00_START_HERE.txt',f'{code} WEEK {week}\n\nBefore class: extract this ZIP and keep the files together.\nIn class: follow the lecturer’s PowerPoint presentation.\nUse guided_practice.ipynb for the small worked examples; it is NOT a graded upload.\nThen open the ASSIGNMENT notebook: '+', '.join(notebooks)+'\nOpen ASSIGNMENT_INSTRUCTIONS.txt first, then read the task prompts and README/TASKS before writing your own answers.\nUpload any supplied CSV and helper .py files to the same Colab runtime when the assignment needs them.\nDo not edit the grader/helper files.\nSubmit only the files requested by the assignment brief, using SUBMIT_HERE.txt for the link and deadline.\nDo not submit guided_practice.ipynb or the ZIP.\nKeep a downloaded copy and the confirmation.\n')
            if week==2:
                start=(BASE/'setup/W02_START_HERE.txt').read_text().replace('YOUR_COHORT',code)
                start+='\nIN CLASS\nFollow the lecturer’s PowerPoint. Start with proof_of_life.ipynb and open the four repairs only when directed.\nAlso read WEEK1_CATCHUP.txt: A1 and Quiz 1 are required alongside A2 and Quiz 2.\n'
                z.writestr('00_START_HERE.txt',start)
                a1=LINKS[code+'|W01'];q=json.loads((ROOT/'data/quiz_links.json').read_text())
                z.writestr('WEEK1_CATCHUP.txt','FOUR TASKS DURING WEEK 2\n\n1. Week 1 A1: complete the three-problems report and submit it separately here: '+a1['url']+'\nDeadline: '+str(a1['closeAt'])+'\n\n2. Week 1 Quiz 1: '+q[code+'|1']+'\n\n3. Week 2 A2: submit your completed main notebook and your own README together. See SUBMIT_HERE.txt.\n\n4. Week 2 Quiz 2: '+q[code+'|2']+'\n\nEach quiz is open for 24 hours from its own lecturer activation. The lecturer will announce the exact closing time. Assignment deadlines and quiz deadlines are different.\n')
            used=set()
            if week!=2:
                z.writestr('READ_INSTRUCTIONS_FIRST.txt','Read ASSIGNMENT_INSTRUCTIONS.md for this assignment, then STUDENT_HOW_TO.md if you need account, Colab or submission help.\n')
            for p in files:
                name=p.name
                if name in used:name='course_'+name
                used.add(name);z.write(p,name)
            entry=LINKS.get(f'{code}|W{week:02}')
            if entry:
                z.writestr('SUBMIT_HERE.txt',f"{code} — Week {week} assignment submission\n\n{entry['url']}\n\nOpens: {entry['openAt']}\nCloses: {entry['closeAt']}\nTimes include the Uganda UTC+03:00 offset.\n\nEnter your own Student Registration Number exactly as on your university record in the form and notebook STUDENT_ID value. The assignment form accepts any registration-number format and the field remains required. In filenames only, replace slashes with underscores. Sign in with the Google account registered on your class roster. Upload the files required in the assignment brief. Keep your submission confirmation. If you resubmit before the deadline, include the complete set of files again; the latest on-time submission replaces the earlier packet.\n")
        count+=1
print(f'Built {count} student-only practical packages')
if beginner_update:sys.exit(0)
# Independent checkpoint: include only the issued dataset and blank notebook.
da=ROOT/'DataAnalysis_Track';daout=da/'student_packages';daout.mkdir(exist_ok=True)
s09files=['TASKS.md','ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt','S09_student.ipynb','customers.csv','customers_raw.csv','orders.csv','orders_raw.csv','order_items.csv','order_items_raw.csv','products.csv','reps.csv','returns.csv','riverside.db']
entry=LINKS['DA|S09']
with zipfile.ZipFile(daout/'DA_S09_student.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(da/'STUDENT_HOW_TO.md','STUDENT_HOW_TO.md')
    for name in s09files:z.write(da/'assessment_banks/S09'/name,name)
    z.writestr('SUBMIT_HERE.txt','Independent Data Analyst track — Session 9\n\n'+entry['url']+'\n\nDates are not yet scheduled. The form stays closed until the lecturer publishes the actual opening and deadline.\n\nSubmit one complete notebook and one accessible DOCX or selectable-text PDF cleaning log in the same response. Use your learner ID and registered Google account. A replacement response must include both files. Keep the confirmation and a local copy.\n')
print('Built independent S09 student package; date remains unset')
