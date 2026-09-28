"""Trusted numerical evidence for S13; no student code executes here.

The five questions retain a sector choice and check reported findings against
an attributed, immutable snapshot. These 40 component marks do not authorize
a final grade: interpretation, charts and release calibration remain separate.
"""
import csv,hashlib,io,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SNAPSHOTS=ROOT/'DataAnalysis_Track/data/sector_snapshots'
SOURCES={'bank':('bank-full.csv',';'),'machine':('ai4i2020.csv',','),'development':('uganda_gdp_2000_2023.csv',',')}
QUESTIONS={
 'bank':[
  ('subscription_rate','percent','What percentage of all campaign records have y=yes?'),
  ('housing_rate_gap','percentage points','What is the subscription-rate difference: housing=yes minus housing=no? Each rate uses its own housing group denominator.'),
  ('previous_success_rate','percent','Among records with poutcome=success, what percentage have y=yes?'),
  ('subscribed_campaign_median','contacts','What is the median campaign contact count among records with y=yes?'),
  ('subscribed_age_gap','years','What is mean age among y=yes minus mean age among y=no?')],
 'machine':[
  ('failure_rate','percent','What percentage of all observations have Machine failure=1?'),
  ('type_rate_gap','percentage points','What is the failure-rate difference: Type H minus Type L, each with its own type denominator?'),
  ('torque_gap','Nm','What is mean Torque [Nm] among failed observations minus the mean among non-failed observations?'),
  ('no_failure_accuracy','percent','What percentage of all observations would an always-no-failure rule classify correctly?'),
  ('failed_tool_wear_median','minutes','What is median Tool wear [min] among observations with Machine failure=1?')],
 'development':[
  ('latest_gdp','current USD','What is Uganda GDP in current US dollars in 2023?'),
  ('window_change','percent','What is the percentage change in nominal current-USD GDP from 2000 to 2023, using 2000 as denominator?'),
  ('change_2020','percent','What is the percentage change from 2019 to 2020, using 2019 as denominator?'),
  ('median_annual_change','percent','What is the median of the 23 consecutive-year percentage changes during 2000–2023?'),
  ('largest_increase_year','year','Which ending year has the largest consecutive-year percentage increase in current-USD GDP? Break an exact tie by earliest ending year.')]
}

def load_rows(sector):
 name,delimiter=SOURCES[sector]
 manifest=json.loads((SNAPSHOTS/'manifest.json').read_text())
 entry=next(r for r in manifest['files'] if r['file']==name)
 raw=(SNAPSHOTS/name).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=entry['sha256'] or len(raw)!=entry['bytes']:raise ValueError('Reference snapshot changed; stop and version the assessment')
 return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')),delimiter=delimiter))

def reference(sector,rows):
 """Compute the five specified findings, with explicit group populations."""
 if sector=='bank':
  yes=[r for r in rows if r['y']=='yes'];no=[r for r in rows if r['y']=='no']
  def rate(group):return 100*sum(r['y']=='yes' for r in group)/len(group)
  values=[rate(rows),rate([r for r in rows if r['housing']=='yes'])-rate([r for r in rows if r['housing']=='no']),rate([r for r in rows if r['poutcome']=='success']),statistics.median(float(r['campaign']) for r in yes),statistics.mean(float(r['age']) for r in yes)-statistics.mean(float(r['age']) for r in no)]
 elif sector=='machine':
  failed=[r for r in rows if int(r['Machine failure'])==1];ok=[r for r in rows if int(r['Machine failure'])==0]
  def rate(group):return 100*sum(int(r['Machine failure'])==1 for r in group)/len(group)
  values=[rate(rows),rate([r for r in rows if r['Type']=='H'])-rate([r for r in rows if r['Type']=='L']),statistics.mean(float(r['Torque [Nm]']) for r in failed)-statistics.mean(float(r['Torque [Nm]']) for r in ok),100*len(ok)/len(rows),statistics.median(float(r['Tool wear [min]']) for r in failed)]
 elif sector=='development':
  if len(rows)!=24 or {int(r['year']) for r in rows}!=set(range(2000,2024)):raise ValueError('Expected one record for each year 2000–2023')
  values_by_year={int(r['year']):float(r['gdp_current_usd']) for r in rows}
  if any(not math.isfinite(v) or v<=0 for v in values_by_year.values()):raise ValueError('GDP comparison requires positive non-missing observations; do not impute')
  changes={year:100*(values_by_year[year]/values_by_year[year-1]-1) for year in range(2001,2024)}
  values=[values_by_year[2023],100*(values_by_year[2023]/values_by_year[2000]-1),changes[2020],statistics.median(changes.values()),min(changes,key=lambda year:(-changes[year],year))]
 else:raise ValueError('Unknown sector')
 return {q[0]:dict(value=value,unit=q[1]) for q,value in zip(QUESTIONS[sector],values)}

def check(ns,index):
 sector=ns.get('SECTOR');findings=ns.get('FINDINGS')
 if sector not in SOURCES:return False,'Set SECTOR to bank, machine or development.'
 if not isinstance(findings,dict):return False,'Provide the FINDINGS dictionary with the published question IDs.'
 qid,unit,_=QUESTIONS[sector][index];item=findings.get(qid)
 if not isinstance(item,dict) or set(item)!={'value','unit'}:return False,'Supply value and unit for '+qid+'.'
 value=item['value']
 if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value):return False,'Use a finite numeric value, not a string or boolean.'
 if item['unit']!=unit:return False,'Use the published unit for '+qid+'.'
 expected=reference(sector,load_rows(sector))[qid]['value']
 tolerance=1 if unit=='current USD' else 0 if unit=='year' else .011
 if abs(value-expected)>tolerance:return False,'Check the published population, denominator, direction and rounding for '+qid+'.'
 return True,'Numerical finding matches the fixed sector snapshot; interpretation is assessed separately.'
