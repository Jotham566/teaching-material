"""A calibration is usable only after its entire declared case set finishes."""
import hashlib,json
from pathlib import Path

def source_hash(contents):
 """Match artifact_grade.packet_hash for an ordered list of file contents."""
 return hashlib.sha256(json.dumps([hashlib.sha256(c.encode()).hexdigest() for c in contents]).encode()).hexdigest()

def authored_cases(assessment):
 """Bind release to today's authored cases, including their exact inputs."""
 if assessment=='W02':
  from calibrate_local_grader import CASES
  return {name:dict(expected_range=[lo,hi],source_sha256=source_hash([
   readme,json.dumps({'cells':[{'cell_type':'markdown','source':['My explanation: '+explanation]}]})]))
   for name,explanation,readme,lo,hi in CASES}
 path=Path(__file__).parent/'calibration_cases'/f'{assessment}.json'
 if not path.is_file():
  if assessment in {'TEST1','TEST2','DA_PROJECT','ML_PROJECT','DEMO','S13','S15'}:
   raise ValueError('No authored known-answer case set exists for this complete assessment')
  return None
 cases=json.loads(path.read_text())
 if len({c['case'] for c in cases})!=len(cases):raise ValueError('Duplicate authored calibration case')
 return {c['case']:dict(expected_range=c['expected_range'],source_sha256=source_hash([c['text']])) for c in cases}

def validate_current_cases(rows,assessment):
 expected=authored_cases(assessment)
 if expected is None:return
 if len(rows)!=len(expected) or {r['case'] for r in rows}!=set(expected):
  raise ValueError('Calibration does not cover the current authored case set')
 for row in rows:
  case=expected[row['case']];result=row['result'];score=result.get('score');lo,hi=case['expected_range']
  if row.get('expected_range')!=case['expected_range'] or result.get('source_sha256')!=case['source_sha256']:
   raise ValueError('Calibration inputs or expected marks differ from current authored cases')
  if isinstance(score,bool) or not isinstance(score,(int,float)) or not lo<=score<=hi:
   raise ValueError('Calibration score falls outside its authored expected range')

def complete(path,expected_cases):
 path=Path(path);rows=json.loads(path.read_text());names=[r['case'] for r in rows]
 if len(expected_cases)<5 or len(set(expected_cases))!=len(expected_cases) or set(names)!=set(expected_cases) or len(names)!=len(expected_cases):raise ValueError('Calibration case set is incomplete')
 record=dict(completed=True,case_count=len(rows),report_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 path.with_suffix(path.suffix+'.complete.json').write_text(json.dumps(record,indent=2))

def require_complete(path):
 path=Path(path);marker=path.with_suffix(path.suffix+'.complete.json')
 if not marker.is_file():raise ValueError('Calibration run has not completed')
 record=json.loads(marker.read_text());rows=json.loads(path.read_text())
 if record.get('completed') is not True or record.get('case_count')!=len(rows) or record.get('report_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('Calibration completion record is stale')


def model_for_report(path):
 """Use the model recorded by a complete passing report; full validation follows."""
 require_complete(path)
 rows=json.loads(Path(path).read_text())
 if len(rows)<5 or any(r.get('passed') is not True for r in rows):raise ValueError('A passing calibration is required to select its local model')
 names={r.get('result',{}).get('model') for r in rows}
 if len(names)!=1:raise ValueError('Calibration records different models')
 model=next(iter(names))
 if not isinstance(model,str) or not model.strip() or 'cloud' in model.lower():raise ValueError('Calibration must name one local model')
 return model


def profile_for_report(path):
 """Resolve only a supported, consistent profile from completed calibration."""
 require_complete(path)
 rows=json.loads(Path(path).read_text())
 if len(rows)<5 or any(r.get('passed') is not True for r in rows):raise ValueError('A passing calibration is required to select its profile')
 profiles={r.get('result',{}).get('evaluation_profile','standard') for r in rows}
 if len(profiles)!=1 or not profiles.issubset({'standard','reasoned'}):raise ValueError('Calibration must name one supported grading profile')
 return next(iter(profiles))
