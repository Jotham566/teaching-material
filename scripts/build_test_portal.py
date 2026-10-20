"""Bundle only student notebooks/data into the separate Apps Script portal."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'IUEA_Teaching_Plan'
packets={}
for exam in ['TEST1','TEST2']:
 for cohort in ['CML3111','CML3112','CML3113']:
  for variant in 'ABC':
   folder=base/'assessment_banks'/exam/cohort/variant
   nb=json.loads((folder/(exam+'_student.ipynb')).read_text())
   assert len(nb['cells'][-1]['outputs'])==0
   packets['|'.join([cohort,exam,variant])]={'notebook':json.dumps(nb,ensure_ascii=False),'csv':(folder/'engineering_data.csv').read_text(),'instructions':(folder/'ASSIGNMENT_INSTRUCTIONS.txt').read_text()}
out=base/'test_portal/Packets.gs'
out.write_text('// Generated from student files only. Never add answer keys.\nvar PORTAL_PACKETS = '+json.dumps(packets,ensure_ascii=False)+';\n')
print(out, out.stat().st_size)
