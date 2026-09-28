"""Canonical assessment IDs, weights, submission formats and deadlines.
Dates use Africa/Kampala (UTC+03:00). Existing Week 1 is preserved.
DA dates are deliberately unset until its actual start date is supplied.
"""
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=3))
COHORTS = {'CML3112': (1, 11), 'CML3113': (4, 8), 'CML3111': (4, 11)}
QUIZ_WEEKS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
CHALLENGE_WEEKS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
WEIGHTS = {'quizzes': 10, 'challenges': 10, 'data_project': 10, 'test1': 15,
           'test2': 20, 'ml_project': 25, 'demo': 10}
TITLES = ['Three problems one dataset', 'Proof of life', 'Engineering functions',
          'Reading report', 'Pandas investigation', 'Cleaning and quality',
          'Regression and baseline', 'Classification and cost', 'Validation and trust',
          'Features and ablation', 'Model recommendation']


def slot(code, week):
    weekday, hour = COHORTS[code]
    return datetime(2026, 9, 7, hour, tzinfo=TZ) + timedelta(days=weekday + 7*(week-1))


def records():
    rows = []
    for code in COHORTS:
        for index, week in enumerate(CHALLENGE_WEEKS, 1):
            rows.append(dict(key=f'{code}|W{week:02}', track='IUEA', cohort=code,
                id=f'W{week:02}', label=f'A{index}', week=week, title=TITLES[index-1],
                maximum=20, component='challenges', formats=(['ipynb'] if week in (3,4,5) else ['ipynb','md'] if week==2 else ['ipynb', 'pdf', 'docx', 'pptx']),
                opens_at=(slot(code,week)-timedelta(days=2) if week==5 and code!='CML3112' else slot(code, week)).isoformat(),
                closes_at=(slot(code, week)+timedelta(hours=3) if week==12 else slot(code, week+1)).isoformat(),
                delivery_note=('Recorded Week 5 session for Friday cohorts; use the published walkthrough and Week 6 consolidation.' if week==5 and code!='CML3112' else ''),
                preserve_existing=week==1, grading='notebook' if week in (3,4,5) else 'hybrid' if week==2 else 'rubric'))
        if code=='CML3112':
            # Five-minute opening buffer for the authorized 22 September class.
            next(r for r in rows if r['key']=='CML3112|W03')['opens_at']='2026-09-22T10:55:00+03:00'
            # Explicit instructor catch-up request; earned Week 1 marks stay protected.
            rows[-len(CHALLENGE_WEEKS)]['opens_at']='2026-09-15T03:31:20.401Z'
            rows[-len(CHALLENGE_WEEKS)]['closes_at']=slot(code,3).isoformat()
            rows[-len(CHALLENGE_WEEKS)]['delivery_note']='Week 1 catch-up collection authorized 15 September; deadline matches Week 2. Existing marks preserved; new written grading held pending validation.'
        if code=='CML3112':
            # Authorized 22 September technical-issue reopening; live 24-hour expiry.
            for r in rows:
                if r['key'] in ('CML3112|W01','CML3112|W02'):
                    r['closes_at']='2026-09-23T13:02:48.578Z'
        if code in ('CML3111','CML3113'):
            catchup_open={'CML3111':'2026-09-21T10:25:33.406Z','CML3113':'2026-09-21T10:25:40.556Z'}
            rows[-len(CHALLENGE_WEEKS)]['opens_at']=catchup_open[code]
            rows[-len(CHALLENGE_WEEKS)]['closes_at']=slot(code,3).isoformat()
            rows[-len(CHALLENGE_WEEKS)]['delivery_note']='Week 1 catch-up collection authorized 21 September; deadline matches Week 2. Existing marks preserved; new written grading held pending validation.'
        if code in ('CML3111','CML3113'):
            # Authorized 26 September A1/A2 catch-up; prior opening dates retained.
            for r in rows:
                if r['key'] in (code+'|W01',code+'|W02'):
                    r['closes_at']='2026-09-27T08:05:46.219Z'
        for aid, week, title, component, formats in [
            ('DA_PROJECT',8,'Data analysis project','data_project',['ipynb','pdf','docx']),
            ('TEST1',7,'Practical Test 1','test1',['ipynb']),
            ('TEST2',14,'Practical Test 2','test2',['ipynb']),
            ('ML_PROJECT',15,'Engineering ML project','ml_project',['ipynb','pdf','docx']),
            ('DEMO',15,'Presentation and individual reflection','demo',['pptx','pdf','docx'])]:
            close = slot(code,week)+(timedelta(hours=3) if aid in ('TEST1','TEST2','DEMO') else timedelta())
            rows.append(dict(key=f'{code}|{aid}', track='IUEA', cohort=code, id=aid,
                label=aid, week=week, title=title, maximum=100, component=component,
                formats=formats, opens_at=slot(code,week if aid.startswith('TEST') else max(2,week-3)).isoformat(),
                closes_at=close.isoformat(), preserve_existing=False, grading='rubric'))
    for session, weight, title in [(5,15,'SQL analysis'),(9,15,'Data cleaning'),(13,30,'Business investigation'),(15,40,'Dashboard and presentation')]:
        rows.append(dict(key=f'DA|S{session:02}',track='DA',cohort='DA',id=f'S{session:02}',label=f'S{session:02}',
            week=(session+2)//3,title=title,maximum=100,component='DA',weight=weight,
            formats=['sql'] if session==5 else ['pptx','pdf','docx'] if session==15 else ['ipynb','pdf','docx'],opens_at=None,closes_at=None,
            preserve_existing=False,grading='sql' if session==5 else 'rubric'))
    return rows


def grade_headers():
    return ['student_id','name','email','cohort'] + [f'Q{i}' for i in range(1,13)] + [f'W{w:02}' for w in CHALLENGE_WEEKS] + ['Data Analysis Project','Practical Test 1','Practical Test 2','ML Project','Demo','Final %','Band','Missing','Challenges done']


if __name__ == '__main__':
    import csv, json
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    (root/'data/assessments.json').write_text(json.dumps(records(),indent=2)+'\n')
    with (root/'IUEA_Teaching_Plan/grader/Grades_template.csv').open('w') as f:
        csv.writer(f).writerow(grade_headers())
