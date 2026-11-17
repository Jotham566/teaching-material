"""Release existing checked marks for punctuation-only notebook ID differences."""
import argparse,json,re
from pathlib import Path

def reconcile(rows):
 compact=lambda value:re.sub(r'[^A-Z0-9]','',str(value or '').upper())
 for row in rows:
  if row['status']!='IDENTITY_MISMATCH':continue
  record=row.get('record',{});declared=compact(record.get('declared_sid'))
  if not declared or declared!=compact(row['student_id']):continue
  questions=record.get('questions',{})
  expected=14 if row['assessment']=='W02' else 20
  if not questions or any(q.get('err') for q in questions.values()):continue
  if sum(q.get('marks',0) for q in questions.values())!=expected:continue
  if any(not 0<=q.get('awarded',-1)<=q['marks'] for q in questions.values()):continue
  score=sum(q['awarded'] for q in questions.values())
  row.update(code_score=score,code_maximum=expected,
             score=None if expected==14 else score,
             status='PARTIAL_CODE_ONLY' if expected==14 else 'GRADED',
             identity_evidence='Notebook and receipt differ only in punctuation/spacing/case. Original grader record retained.')
 return rows

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 Path(a.out).write_text(json.dumps(reconcile(json.loads(Path(a.input).read_text())),indent=2))
