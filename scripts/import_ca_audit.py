"""Read the private Sheets audit export. Does not infer scores or student names."""
import argparse,collections,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
import openpyxl
ap=argparse.ArgumentParser();ap.add_argument('xlsx');ap.add_argument('out');a=ap.parse_args()
w=openpyxl.load_workbook(a.xlsx,read_only=True,data_only=True);rows=list(w['Submission audit'].values);headers=rows[0];groups=collections.defaultdict(list)
for values in rows[1:]:
 r=dict(zip(headers,values));key=r.get('assessment_key','')
 if not key.startswith(('CML3111|','CML3112|','CML3113|')):continue
 if key.split('|')[1] not in ['W01','W02','W03','W04','W05']:continue
 groups[key].append(dict(response_id=r['response_id'],assessment_key=key,email=r['email'] or '',submitted_at=r['submitted_at'],fields={'Student Registration Number':r['student_id']},file_ids=json.loads(r['file_ids']),timing_status=r['status']))
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
for key,records in groups.items():
 d=dict(key=key,exported_at=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256(Path(a.xlsx).read_bytes()).hexdigest(),source_kind='audit_only',window={'open':'2026-01-01T00:00:00Z','close':'2027-01-01T00:00:00Z'},records=records,files=[],errors=['Attachment export not yet downloaded. Timing statuses are retained from the source audit.'])
 (out/(key.replace('|','_')+'_manifest.json')).write_text(json.dumps(d,indent=2))
print('Imported audit receipts:',sum(map(len,groups.values())))
