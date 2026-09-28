"""Bounded SQL execution inside the no-network teaching container."""
import json,sqlite3,sys,time
from contextlib import closing
COLUMNS=['region','rep_name','month','gross_ugx','returned_ugx','net_ugx']

def evaluate(sql,seconds):
    if len(sql)>100000:raise ValueError('SQL exceeds 100,000 characters')
    deadline=time.monotonic()+seconds
    with closing(sqlite3.connect('file:/inputs.sqlite?mode=ro&immutable=1',uri=True)) as db:
        db.enable_load_extension(False)
        allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION,sqlite3.SQLITE_RECURSIVE}
        def authorize(action,arg1,arg2,*rest):
            if action not in allowed:return sqlite3.SQLITE_DENY
            if action==sqlite3.SQLITE_FUNCTION and str(arg2).lower() in ('load_extension','readfile','writefile'):return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        db.set_authorizer(authorize);db.set_progress_handler(lambda:int(time.monotonic()>deadline),1000)
        db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH,1024*1024)
        cursor=db.execute(sql)
        if [d[0].lower() for d in cursor.description or []]!=COLUMNS:raise ValueError('Output columns must be '+', '.join(COLUMNS))
        rows=[];size=0
        for row in cursor:
            if len(rows)>=10000:raise ValueError('Result exceeds 10,000 rows')
            size+=len(json.dumps(row,ensure_ascii=False).encode())
            if size>2*1024*1024:raise ValueError('SQL result exceeds 2 MiB')
            rows.append(row)
        return rows

if __name__=='__main__':
    try:
        request=json.loads(sys.stdin.read(700000));rows=evaluate(request['sql'],float(request['seconds']))
        print(json.dumps(dict(rows=rows),ensure_ascii=False))
    except Exception as exc:
        print(json.dumps(dict(error=str(exc)[:400],kind='sqlite' if isinstance(exc,sqlite3.Error) else 'validation')))
