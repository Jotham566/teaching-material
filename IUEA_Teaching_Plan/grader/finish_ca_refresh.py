"""Finish the prepared 21 October refresh after the current written queue exits."""
import collections,json,os,shutil,subprocess,time
from pathlib import Path
import continuous_assessment as ca
import grade_ca_batch,grade_ca_written,prepare_ca_written
from calibration_record import model_for_report
from run_ca_written_queue import merged_results,unload,NODE,ROOT

PRIVATE=ROOT/'IUEA_Teaching_Plan/assessment_operations/private'

def main():
 p=PRIVATE;status=p/'refresh_status.json';new=p/'reconciled_20261021'
 def stage(value,**details):
  status.write_text(json.dumps(dict(stage=value,pid=os.getpid(),**details),indent=2))
 try:
  stage('WAITING_FOR_WRITTEN_QUEUE')
  while True:
   state=json.loads((p/'written_queue/queue_status.json').read_text())
   if state['state']=='COMPLETE':break
   if state['state']=='STOPPED':raise RuntimeError('Original written queue stopped; refresh not started.')
   try:os.kill(state['pid'],0)
   except ProcessLookupError:raise RuntimeError('Original written process exited without completion.')
   time.sleep(10)
  stage('GRADING_NEW_AND_RECOVERED_NOTEBOOKS')
  subprocess.run(['docker','desktop','start'],check=True,timeout=120)
  for attempt in range(30):
   if subprocess.run(['docker','info'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
   time.sleep(2)
  else:raise RuntimeError('Docker did not become ready')
  retry=p/'retry_input_20261021.json';out=p/'refresh_20261021';out.mkdir(exist_ok=True)
  grade_ca_batch.run(new,retry,out/'coding')
  # The existing checker already calculated these marks; only punctuation differs.
  import sys
  sys.path.insert(0,str(ROOT/'scripts'))
  from reconcile_ca_notebook_identity import reconcile
  coding=out/'coding/results.json';coding.write_text(json.dumps(reconcile(json.loads(coding.read_text())),indent=2))
  prepare_ca_written.prepare(new,retry,out/'text')
  subprocess.run(['docker','desktop','stop','--timeout','30'],check=True,timeout=60)
  stage('GRADING_RECOVERED_WRITTEN_FILES')
  for assessment,report in [('W01',p/'W01_calibration_isolated.json'),('W02',ROOT/'review/2026-09-14/rework/local_calibration_v10.json')]:
   grade_ca_written.run(new,retry,coding,report,assessment,out/assessment,out/'text/prepared.json')
   unload(model_for_report(report))
  stage('UPDATING_WORKBOOK')
  combined=p/'written_queue/combined_results.json'
  results=merged_results([combined,coding,out/'W01/results.json',out/'W02/results.json'])
  result_file=out/'combined_results.json';result_file.write_text(json.dumps(results,indent=2))
  ledger=ca.build(new,result_file,json.loads((new/'timing.json').read_text()))
  # Preserve the previous source snapshot before switching the workbook's sources.
  backup=p/'reconciled_20261020'
  if backup.exists():raise RuntimeError('Source backup already exists; inspect before repeating this refresh.')
  (p/'reconciled').rename(backup);shutil.copytree(new,p/'reconciled')
  combined.write_text(json.dumps(results,indent=2))
  prepared=json.loads((p/'written_text/prepared.json').read_text());prepared.update(json.loads((out/'text/prepared.json').read_text()))
  (p/'written_text/prepared.json').write_text(json.dumps(prepared,indent=2))
  ledger_file=p/'ledger.json';ledger_file.write_text(json.dumps(ledger,indent=2))
  temporary=p/'IUEA_Continuous_Assessment.refresh.xlsx'
  subprocess.run([str(NODE),str(ROOT/'scripts/build_continuous_assessment.mjs'),str(ledger_file),str(temporary)],check=True,
                 env=dict(os.environ,IUEA_WORKBOOK_QA='1'))
  os.replace(temporary,p/'IUEA_Continuous_Assessment.xlsx')
  stage('COMPLETE',current_statuses=dict(collections.Counter(r['status'] for r in ledger['current'])))
 except BaseException as exc:
  stage('STOPPED',error=str(exc));raise

if __name__=='__main__':main()
