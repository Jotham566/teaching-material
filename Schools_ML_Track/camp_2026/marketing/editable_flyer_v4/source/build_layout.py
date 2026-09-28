from pathlib import Path
import json,copy,shutil
r=Path(__file__).resolve().parent.parent
v2=json.loads((r.parent/'editable_flyer_v2/source/layout.json').read_text())['elements']
v3=json.loads((r.parent/'editable_flyer_v3/source/layout.json').read_text())['elements']
E=[]
def img(n,f,x,y,w,h):E.append(dict(kind='image',name=n,file='assets/'+f,x=x,y=y,w=w,h=h))
def box(n,x,y,w,h,c,rad=0):E.append(dict(kind='rect',name=n,x=x,y=y,w=w,h=h,color=c,r=rad))
img('Classroom background','classroom-background.png',0,0,1024,1536)
img('Desk and books footer','desk-footer.png',0,1420,1024,356)
img('Actual photographic portrait, background masked only','actual-portrait-cutout.png',376,0,574,709)
img('Original-style hero accents','hero-brushes.png',0,0,1024,618)
img('Original-style footer accents','footer-brushes.png',0,1420,1024,356)
for e in v2:
 if e['name']=='Central white sheet':break
 if e['name'] in ['Photographic backdrop','Decorative brush accents']:continue
 E.append(copy.deepcopy(e))
box('Central white sheet',18,618,989,810,'#FFFFFF',18)
box('Data Analysis panel',31,629,475,512,'#E6F6FE',15)
box('Machine Learning panel',519,629,475,512,'#F2E7FD',15)
for name in ['chart-simple','network','Data Analysis title','ML title']:
 E.append(copy.deepcopy(next(e for e in v2 if e['name']==name)))
for side,n,value,x in [('DA','DA description','Turn real data into\nuseful insights',166),('ML','ML description','Teach computers to find patterns\n& make predictions',655)]:
 e=copy.deepcopy(next(e for e in v3 if e['name']==n));e.update(value=value,x=x,y=691,w=335,h=62,size=22,font='Arial Narrow');E.append(e)
for e in v3:
 if e['kind']=='image' and ' logo ' in e['name']:
  e=copy.deepcopy(e);e['y']=776;E.append(e)
 if ' label ' in e['name']:
  e=copy.deepcopy(e);e['y']=829;E.append(e)
box('DA rule',51,867,435,1,'#B1DAED');box('ML rule',540,867,435,1,'#D7BCEB')
for e in v3:
 if ' learning ' in e['name']:
  e=copy.deepcopy(e);i=int(e['name'].split()[-1])-1;e.update(y=880+29*i,h=30);E.append(e)
for e in v3:
 if 'outcome strip' in e['name'] or e['name'] in ['DA Build','DA project examples','ML Build','ML project examples']:
  e=copy.deepcopy(e);e['y']+=13;E.append(e)
start=False
for e in v2:
 if e['name']=='calendar-days':start=True
 if start:
  e=copy.deepcopy(e);e['y']+=240;E.append(e)
# Copy any reused v2 raster icons absent from the preceding edition.
for e in E:
 if e['kind']=='image' and not (r/e['file']).exists():shutil.copy2(r.parent/'editable_flyer_v2'/e['file'],r/e['file'])
(r/'source/layout.json').write_text(json.dumps(dict(width=1024,height=1776,elements=E),indent=2))
print('Restored design assembled, 1024 x 1776')
