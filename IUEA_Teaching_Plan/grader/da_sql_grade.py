"""Read-only, resource-bounded SQL grading for the DA Session 5 report."""
import argparse,csv,json,math,sqlite3,subprocess,uuid
from pathlib import Path
REFERENCE="""
WITH lines AS (
 SELECT o.rep_id,substr(o.order_date,1,7) AS month,oi.line_no,
 oi.quantity*oi.unit_price_ugx*(1-oi.discount) AS gross_ugx
 FROM order_items oi JOIN orders o ON o.order_id=oi.order_id
 WHERE o.status='Delivered' AND o.order_date>='2025-01-01' AND o.order_date<'2026-01-01'
), net AS (
 SELECT l.rep_id,l.month,SUM(l.gross_ugx) AS gross_ugx,
 SUM(COALESCE(rt.quantity_returned,0)*oi.unit_price_ugx*(1-oi.discount)) AS returned_ugx
 FROM lines l JOIN order_items oi ON oi.line_no=l.line_no
 LEFT JOIN (SELECT line_no,SUM(quantity_returned) AS quantity_returned
            FROM returns GROUP BY line_no) rt ON rt.line_no=l.line_no GROUP BY l.rep_id,l.month
)
SELECT r.region,r.rep_name,n.month,ROUND(n.gross_ugx) AS gross_ugx,
ROUND(n.returned_ugx) AS returned_ugx,ROUND(n.gross_ugx-n.returned_ugx) AS net_ugx
FROM net n JOIN reps r ON r.rep_id=n.rep_id
"""
COLUMNS=['region','rep_name','month','gross_ugx','returned_ugx','net_ugx']

def query(database,sql,seconds=3):
    if len(sql)>100000:raise ValueError('SQL exceeds 100,000 characters')
    database=Path(database).resolve()
    if not database.is_file():raise ValueError('Missing grading database')
    if not 0<seconds<=10:raise ValueError('Invalid SQL time limit')
    worker=Path(__file__).with_name('da_sql_worker.py')
    container_name='iuea-sql-'+uuid.uuid4().hex
    command=['docker','run','--rm','--name',container_name,'-i','--network=none','--read-only','--cap-drop=ALL',
             '--security-opt=no-new-privileges','--pids-limit=32','--memory=256m','--cpus=1',
             '--user=65534:65534','--tmpfs=/tmp:rw,noexec,nosuid,size=32m',
             '-v',str(database)+':/inputs.sqlite:ro','-v',str(worker)+':/worker.py:ro',
             'iuea-notebooks:2026.09','python','/worker.py']
    try:
        result=subprocess.run(command,input=json.dumps(dict(sql=sql,seconds=seconds)),capture_output=True,text=True,timeout=seconds+15)
    except subprocess.TimeoutExpired as exc:raise ValueError('SQL exceeded the isolated execution limit') from exc
    finally:
        subprocess.run(['docker','rm','-f',container_name],capture_output=True,timeout=10)
    if result.returncode:raise ValueError('Isolated SQL execution failed; check Docker or reduce query resource use')
    if len(result.stdout.encode())>3*1024*1024:raise ValueError('SQL output exceeds transport limit')
    response=json.loads(result.stdout)
    if 'error' in response:
        if response.get('kind')=='sqlite':raise sqlite3.Error(response['error'])
        raise ValueError(response['error'])
    return response['rows']

def score_rows(actual,expected):
    def keyed(rows):
        out={}
        for row in rows:
            key=tuple(row[:3])
            if key in out:raise ValueError('Duplicate rep/month key in output')
            out[key]=row[3:]
        return out
    got,want=keyed(actual),keyed(expected)
    denominator=max(len(want),len(got),1)
    common=got.keys()&want.keys()
    marks={'grain':25*len(common)/denominator}
    for i,name in enumerate(COLUMNS[3:]):
        correct=sum(isinstance(got[k][i],(int,float)) and math.isfinite(got[k][i]) and abs(got[k][i]-want[k][i])<=1 for k in common)
        marks[name]=25*correct/denominator
    return dict(score=round(sum(marks.values()),2),maximum=100,status='AUTO_SCORED',criteria=marks,
                feedback='Compare each rep/month and each amount; tolerance is 1 UGX after rounding. Extra or missing rows reduce credit.')

def grade_manifest(rows,database):
    from artifact_grade import group_manifest
    groups=group_manifest(rows)
    if not groups:raise ValueError('No eligible submissions in manifest')
    expected=query(database,REFERENCE);results=[]
    for sid,packet in groups.items():
        files=[Path(r['file']) for r in packet if Path(r['file']).suffix.lower()=='.sql']
        try:
            if len(files)!=1:raise ValueError('Submit exactly one SQL file in the complete response.')
            with files[0].open(encoding='utf-8') as source:sql=source.read(100001)
            result=score_rows(query(database,sql),expected)
        except (sqlite3.Error,ValueError,OSError) as exc:
            result=dict(status='EXCEPTION',score=None,maximum=100,error=str(exc))
        results.append(dict(student_id=sid,**result))
    return results

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--submissions',required=True,help='Prepared manifest CSV')
    ap.add_argument('--database',default=str(Path(__file__).resolve().parents[2]/'DataAnalysis_Track/data/riverside.db'))
    ap.add_argument('--out',required=True);args=ap.parse_args()
    with open(args.submissions) as source:rows=list(csv.DictReader(source))
    results=grade_manifest(rows,args.database);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/'feedback.json').write_text(json.dumps(results,indent=2))
    with (out/'results.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['student_id','status','score','maximum'],extrasaction='ignore');w.writeheader();w.writerows(results)
    print('Processed',len(results),'SQL reports')

if __name__=='__main__':main()
