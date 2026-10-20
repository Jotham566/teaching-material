"""Keep later weekly submission instructions tied to the issued task bank."""
import json
from datetime import datetime,timezone,timedelta
from pathlib import Path
from pptxkit import s_points,notes
ROOT=Path(__file__).resolve().parents[1]
WORK={
 'W06':'Cleaning, summary and audit functions; a defect register and quality statement in your written-evidence cell.',
 'W08':'Regression and error functions; interpret the supplied model comparison, its limits and reproducibility.',
 'W09':'Classification checks; interpret the supplied error-cost scenario and justify your decision.',
 'W10':'Group split and preprocessing checks; explain leakage controls and conditions of use.',
 'W11':'Feature and error checks; define the features and interpret the supplied controlled ablation.',
 'W12':'Model selection and error checks; explain the supplied decision constraints, assumptions and limitations.'}

def add_weekly_submission(prs,aid,code):
    if aid=="W06" and code in ("CML3112","CML3113"):
        slide=s_points(prs,"Practical revision — no submission",[("A6 and Quiz 6 are waived","Save your practice notebook in Drive. Use the Test 1 revision slides and matching practice CSV before the test.")],kicker="UNGRADED PRACTICE",numbered=True)
        notes(slide,"No A6 or Quiz 6 is assigned. Existing submissions are retained and excluded from coursework totals.")
        return slide
    rubric=json.loads((ROOT/'IUEA_Teaching_Plan/grader/rubrics/hybrid'/f'{aid}.json').read_text())
    link=json.loads((ROOT/'data/submission_links.json').read_text())[code+'|'+aid]
    close=datetime.fromisoformat(link['closeAt']).astimezone(timezone(timedelta(hours=3))).strftime('%a %d %b, %H:%M Kampala')
    label=f'Open the {code} {aid} submission form'
    slide=s_points(prs,f'{aid}: your graded weekly submission',[
        ('Use the issued cohort task bank',f'assessment_banks/{aid}/{code}/A/TASKS.md and its student notebook. Use the supplied data and interfaces. Broader project exercises support practice and project development.'),
        ('Complete both parts',WORK[aid]+f' {rubric["deterministic_maximum"]} executed marks + {rubric["maximum"]:g} written marks = 20.'),
        ('Identify and retain your work','Set STUDENT_ID to your full Student Registration Number. Write in the cell headed My written evidence. Keep a downloaded copy of the complete notebook.'),
        (label,f'Upload the notebook through this link. Deadline: {close}. The form opens only within its released submission window.')],kicker='ASSESSMENT BRIEF',numbered=True)
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text==label:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:run.hyperlink.address=link['url']
    notes(slide,'The issued bank defines this weekly submission. Keep broader project practice separate.\n\nTO TEACH: use the final minutes already allocated to assignment instructions; confirm the cohort link and deadline. Keep private marking guidance out of student materials.')
    return slide
