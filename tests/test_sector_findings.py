import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import sector_findings as sf
class NS:
 def __init__(self,sector,findings):self.values={'SECTOR':sector,'FINDINGS':findings}
 def get(self,name):return self.values.get(name)
class SectorFindings(unittest.TestCase):
 def test_bank_denominators_and_direction(self):
  rows=[dict(y=y,housing=h,poutcome=p,campaign=c,age=a) for y,h,p,c,a in [('yes','yes','success',2,30),('no','yes','failure',4,50),('no','yes','success',3,40),('yes','no','success',4,50)]]
  r=sf.reference('bank',rows)
  self.assertEqual(r['subscription_rate']['value'],50)
  self.assertAlmostEqual(r['housing_rate_gap']['value'],-200/3)
  self.assertAlmostEqual(r['previous_success_rate']['value'],200/3)
  self.assertEqual(r['subscribed_campaign_median']['value'],3)
  self.assertEqual(r['subscribed_age_gap']['value'],-5)
 def test_machine_units_and_class_imbalance(self):
  rows=[{'Machine failure':f,'Type':t,'Torque [Nm]':q,'Tool wear [min]':w} for f,t,q,w in [(1,'H',50,100),(0,'H',20,20),(0,'L',30,30),(0,'L',40,40)]]
  r=sf.reference('machine',rows)
  self.assertEqual([r[q[0]]['value'] for q in sf.QUESTIONS['machine']],[25,50,20,75,100])
 def test_development_missing_zero_and_tie(self):
  rows=[dict(year=y,gdp_current_usd=2**(y-2000)) for y in range(2000,2024)]
  r=sf.reference('development',rows)
  self.assertEqual(r['median_annual_change']['value'],100)
  self.assertEqual(r['largest_increase_year']['value'],2001)
  rows[0]['gdp_current_usd']=''
  with self.assertRaises(ValueError):sf.reference('development',rows)
  rows[0]['gdp_current_usd']=0
  with self.assertRaises(ValueError):sf.reference('development',rows)
 def test_all_snapshots_and_invalid_claims(self):
  for sector in sf.SOURCES:
   expected=sf.reference(sector,sf.load_rows(sector));ns=NS(sector,expected)
   for i in range(5):self.assertTrue(sf.check(ns,i)[0],(sector,i))
   first=sf.QUESTIONS[sector][0][0]
   for wrong in [True,float('nan'),float('inf'),'10']:
    bad=json.loads(json.dumps(expected));bad[first]['value']=wrong
    self.assertFalse(sf.check(NS(sector,bad),0)[0])
   bad=json.loads(json.dumps(expected));bad[first]['unit']='wrong'
   self.assertFalse(sf.check(NS(sector,bad),0)[0])
   bad=json.loads(json.dumps(expected));bad[first]['value']+=20
   self.assertFalse(sf.check(NS(sector,bad),0)[0])
 def test_all_sector_packets_in_isolation(self):
  from batch_grade import grade_one
  for sector in sf.SOURCES:
   findings=sf.reference(sector,sf.load_rows(sector))
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'S10001_S13.ipynb';p.write_text(json.dumps({'cells':[{'cell_type':'code','source':'STUDENT_ID="S10001"\nCOHORT="DA"\nSECTOR='+repr(sector)+'\nFINDINGS='+repr(findings)}]}))
    result=grade_one(str(p),str(G/'specs/spec_S13.py'),str(G/'specs/hidden/spec_S13_hidden.py'),'S13','DA',None,10,40,None)
    self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),40,result)
 def test_component_cannot_be_imported_as_final(self):
  from da_gradebook import combine
  with self.assertRaises(ValueError):combine([dict(student_id='S10001',cohort='DA')],{'S13':[dict(student_id='S10001',status='AUTO_SCORED',score=40,maximum=40)]})
if __name__=='__main__':unittest.main()
