"""Deterministic fictional logs with the patterns described in Week 4.
All thresholds are teaching assumptions, not professional acceptance rules.
"""
import csv,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'IUEA_Teaching_Plan/practicals/W04'
from build_week2_kit import notebook

def task_explanations(column, group, threshold):
 return {
  'valid_count': f'Store an integer count of rows whose {column} field is nonblank. Skip blank readings before numeric conversion.',
  'mean_reading': f'Store the arithmetic mean of the nonblank {column} values as a number. Add the valid readings and divide by their count. Keep full precision.',
  'above_limit': f'Store an integer count of valid {column} readings strictly greater than {threshold}. A reading equal to the threshold is not counted.',
  'group_means': f'Store a dictionary whose keys are the {group} labels and whose values are the mean valid {column} readings within each group. Divide each group total by its own valid count. Keep full precision.'}


def main():
 for code in ('CML3112','CML3113','CML3111'):
  rng=random.Random(404);rows=[]
  for i in range(300):
   if code=='CML3112':
    inspector='I'+str(i%4+1);structure='B'+str((i//4)%12+1)
    crack=round(.12+.02*((i//4)%12)+rng.uniform(-.04,.04),3)
    row=dict(structure_id=structure,span_m=12+((i//4)%12),inspection_date=f'2026-03-{i%28+1:02}',crack_width_mm=crack,defect_rating=min(5,1+int(crack/.12)+(inspector=='I4')),inspector_id=inspector)
    filename,column,group,threshold='site_inspection_log.csv','crack_width_mm','structure_id',.30
   elif code=='CML3113':
    shift='night' if i%2 else 'day';bit='B'+str((i//2)%3+1)
    rate=round(11+rng.uniform(-1,1)-(4 if shift=='night' and bit=='B3' else 0),2)
    row=dict(hole_id='H'+str(i%15+1),depth_m=80+i%80,rate_of_penetration=rate,bit_type=bit,operator_id='O'+str(i%5+1),downtime_min=i%25,downtime_reason=['service','power','change'][i%3],shift=shift)
    filename,column,group,threshold='drill_shift_log.csv','rate_of_penetration','bit_type',8.0
   else:
    motor='M'+str(i%8+1);voltage=200 if (i//8)%2 else 230
    temp=round(85+rng.uniform(-4,4)+(55 if motor=='M3' and voltage==200 else 0),2)
    row=dict(motor_id=motor,supply_v=voltage,current_a=round(5+rng.random(),2),rpm=1400+i%80,winding_temp_c=temp,vibration_rms=round(.5+rng.random(),3),pass_fail='pass' if voltage==230 else 'check',test_date=f'2026-03-{i%28+1:02}',ambient_temp_c=25)
    filename,column,group,threshold='motor_test_bench.csv','winding_temp_c','motor_id',130.0
   if i in (17,89,201):row[column]=''
   rows.append(row)
  dest=OUT/code;dest.mkdir(parents=True,exist_ok=True)
  with (dest/filename).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  valid=[r for r in rows if r[column]!=''];values=[r[column] for r in valid]
  groups={g:sum(r[column] for r in valid if r[group]==g)/sum(r[group]==g for r in valid) for g in {r[group] for r in valid}}
  expected={'valid_count':len(valid),'mean_reading':sum(values)/len(values),'above_limit':sum(v>threshold for v in values),'group_means':groups}
  (dest/'README.md').write_text(f'# Week 4 {code}\n\nFictional teaching data. {len(rows)} records. Three blank {column} values must be skipped in numerical summaries. Threshold {threshold} is a teaching assumption.\n\nCompute valid_count, mean_reading, above_limit (strictly greater than {threshold}) and group_means keyed by {group}. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.\n')
  cells=[('markdown',f'# Week 4 reading report\nRead README.md. Keep units in your explanation.\n'),('code',f'STUDENT_ID="YOUR_ID"\nCOHORT="{code}"\nimport csv\nwith open("{filename}",newline="") as f:\n    rows=list(csv.DictReader(f))\n')]
  for var in expected:cells += [('markdown',f'## {var} (5 marks)\n{task_explanations(column,group,threshold)[var]}\n'),('code','# Your calculation here\n')]
  (dest/'W04_student.ipynb').write_text(json.dumps(notebook(cells),indent=2))
  (ROOT/'IUEA_Teaching_Plan/grader/specs/hidden'/f'W04_{code}_expected.json').write_text(json.dumps(expected,indent=2))

if __name__=='__main__':main()
