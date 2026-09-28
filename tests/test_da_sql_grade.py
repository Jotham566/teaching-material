import sqlite3,sys,unittest,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'IUEA_Teaching_Plan/grader'))
from da_sql_grade import query,score_rows,REFERENCE,grade_manifest
class SQLChecks(unittest.TestCase):
 def setUp(self):self.db=ROOT/'DataAnalysis_Track/data/riverside.db'
 def test_correct_and_wrong_values(self):
  rows=query(self.db,REFERENCE)
  self.assertEqual(score_rows(rows,rows)['score'],100)
  wrong=[tuple(r[:3])+tuple(0 for _ in range(3)) for r in rows]
  self.assertLess(score_rows(wrong,rows)['score'],100)
 def test_multiple_return_events_do_not_duplicate_gross(self):
  with tempfile.TemporaryDirectory() as folder:
   database=Path(folder)/'fixture.db'
   with sqlite3.connect(database) as c:
    c.executescript("""CREATE TABLE orders(order_id,rep_id,order_date,status);
CREATE TABLE order_items(line_no,order_id,quantity,unit_price_ugx,discount);
CREATE TABLE returns(line_no,quantity_returned);
CREATE TABLE reps(rep_id,region,rep_name);
INSERT INTO orders VALUES(1,1,'2025-01-01','Delivered');
INSERT INTO order_items VALUES(1,1,10,100,0);
INSERT INTO returns VALUES(1,2),(1,3);
INSERT INTO reps VALUES(1,'Central','Example');""")
   self.assertEqual(query(database,REFERENCE),[['Central','Example','2025-01',1000.0,500.0,500.0]])
 def test_write_denied(self):
  with self.assertRaises(sqlite3.Error):query(self.db,'DELETE FROM orders')
 def test_attach_denied(self):
  with self.assertRaises(sqlite3.Error):query(self.db,"ATTACH DATABASE ':memory:' AS extra")
 def test_recursive_timeout(self):
  with self.assertRaises(sqlite3.Error):query(self.db,'WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n',seconds=.05)
 def test_large_result_is_bounded(self):
  sql="WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n WHERE x<100) SELECT printf('%050000d',x) AS region, 'Rep' AS rep_name, '2025-01' AS month, 1 AS gross_ugx, 0 AS returned_ugx, 1 AS net_ugx FROM n"
  with self.assertRaisesRegex(ValueError,'2 MiB'):query(self.db,sql)
 def test_duplicate_keys_fail(self):
  rows=query(self.db,REFERENCE)
  with self.assertRaises(ValueError):score_rows(rows+rows[:1],rows)

class SQLPacketChecks(unittest.TestCase):
 def test_incomplete_packet_does_not_block_valid_report(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder);good=p/'report.sql';good.write_text(REFERENCE)
   rows=[dict(student_id='S10001',file=str(good)),dict(student_id='S10002',file=str(p/'wrong.pdf'))]
   result=grade_manifest(rows,ROOT/'DataAnalysis_Track/data/riverside.db')
   self.assertEqual(result[0]['score'],100)
   self.assertEqual(result[1]['status'],'EXCEPTION');self.assertIsNone(result[1]['score'])
 def test_missing_and_ambiguous_files_remain_pending(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)
   rows=[dict(student_id='S10001',file=str(p/'missing.sql')),
         dict(student_id='S10002',file=str(p/'one.sql'),response_id='same'),
         dict(student_id='S10002',file=str(p/'two.sql'),response_id='same')]
   result=grade_manifest(rows,ROOT/'DataAnalysis_Track/data/riverside.db')
   self.assertTrue(all(r['status']=='EXCEPTION' and r['score'] is None for r in result))
