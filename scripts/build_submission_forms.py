"""Embed the canonical registry in the assignment submission Apps Script."""
import json
from pathlib import Path
from assessment_registry import records
root=Path(__file__).resolve().parents[1]
p=root/'IUEA_Teaching_Plan/grader/submission_forms.gs'
s=p.read_text()
a=s.index('var ASSESSMENTS = '); b=s.index('\n',a)
# The entire generated declaration is one line; briefs can contain semicolons.
assessments=records()
for row in assessments:
    rubric=root/'IUEA_Teaching_Plan/grader/rubrics'/(row['id']+'.json')
    if row['grading']=='notebook':
        practical=root/'IUEA_Teaching_Plan/practicals'/row['id']/row['cohort']/'README.md'
        row['brief']=practical.read_text() if practical.exists() else 'Use the issued cohort notebook; all checks total 20 marks.'
    elif row['grading']=='sql':row['brief']='Submit one .sql file for the 2025 delivered revenue report, net of returns. Columns in order: region, rep_name, month, gross_ugx, returned_ugx, net_ugx. One row per rep/month. Marks: correct row keys 25, gross amounts 25, returned amounts 25, net amounts 25. Amount tolerance: 1 UGX. All checks run locally against the supplied Riverside database.'
    elif row['id']=='W02':row['brief']=(root/'IUEA_Teaching_Plan/setup/A2_assignment_brief.md').read_text()
    elif row['id'] in ('W06','W08','W09','W10','W11','W12','S09'):
        r=json.loads((root/'IUEA_Teaching_Plan/grader/rubrics/hybrid'/(row['id']+'.json')).read_text())
        package=('DA_S09_student.zip' if row['id']=='S09' else row['cohort']+'_'+row['id']+'_student.zip')
        row['brief']='Use the lecturer-issued '+package+'. Read TASKS.md and complete its required function interfaces using the supplied data.\n\n'
        row['brief']+='Mark split: '+str(r['deterministic_maximum'])+' executed checks + '+str(r['maximum'])+' written evidence = '+str(r['assessment_maximum'])+'.\n'
        row['brief']+='Written criteria: '+', '.join(c['title']+' ('+str(c['maximum'])+')' for c in r['criteria'])+'.\n\n'
        row['brief']+=('Submit one complete notebook AND one accessible DOCX or selectable-text PDF cleaning log together. Use your learner ID.' if row['id']=='S09' else 'Submit exactly one complete notebook. Set STUDENT_ID to your full Student Registration Number, including slashes, and COHORT to '+row['cohort']+'. Write your own explanation in the cell headed My written evidence. Extra project exercises are formative and add no weekly marks.')
        row['brief']+='\n\nUse your registered Google account. Keep a local copy and the confirmation. Any replacement response must contain the complete required packet; the latest on-time response replaces the earlier submission. Opening and expiry follow the published Kampala window. If dates are not yet published, this form remains closed.'
    elif rubric.exists():
        r=json.loads(rubric.read_text());row['brief']='Assessment criteria:\n'+'\n'.join(f"{c['title']} ({c['maximum']:g} marks): {c['description']}" for c in r['criteria'])
    guidebase=root/('DataAnalysis_Track' if row['cohort']=='DA' else 'IUEA_Teaching_Plan')
    guide=guidebase/'student_guides'/row['cohort']/(row['id']+'.md')
    if guide.exists():
        # Workflow is the student-facing source; rubrics remain authoritative separately.
        row['brief']=guide.read_text()
    else:raise FileNotFoundError(guide)


s=s[:a]+'var ASSESSMENTS = '+json.dumps(assessments,ensure_ascii=False,separators=(',',':'))+';'+s[b:]
p.write_text(s)
