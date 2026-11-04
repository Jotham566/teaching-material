import datetime as dt, json, sys
sys.path.insert(0,'/sessions/focused-youthful-einstein/mnt/IUEA-Teaching-Resources/Schools_ML_Track/camp_2026/build')
from lessons import ml
HOL={dt.date(2026,12,25):'Christmas Day',dt.date(2026,12,26):'Boxing Day',dt.date(2027,1,1):"New Year's Day",dt.date(2027,1,26):'NRM Liberation Day'}
start=dt.date(2026,12,3)
core=[]; d=start
while len(core)<24:
    if d.weekday() in (1,3,5) and d not in HOL: core.append(d)
    d+=dt.timedelta(1)
labs={}
for l in ml.LABS:
    n=int(l['after'][2:]); d=core[n-1]+dt.timedelta(1)
    while d.weekday()!=4: d+=dt.timedelta(1)
    while d in HOL or d.weekday()>4: d+=dt.timedelta(1)
    labs[l['after']]=d
rows=[]
for i,(d,l) in enumerate(zip(core,ml.ML),1): rows.append((d,'core',f'ML{i:02d}',l['title']))
for l in ml.LABS: rows.append((labs[l['after']],'lab',{'ML03':'F01','ML06':'F02','ML09':'F03','ML12':'F04'}[l['after']],l['title']))
rows.sort()
for r in rows: print(r[0],r[0].strftime('%a'),r[2],r[3][:50])
# holiday-affected classes
for h in HOL: print(h,h.strftime('%a'))
json.dump([[r[0].isoformat(),r[1],r[2],r[3]] for r in rows],open('rows.json','w'))
