from pathlib import Path
import json,copy
r=Path(__file__).resolve().parent.parent
old=json.loads((r.parent/'editable_flyer_v4/source/layout.json').read_text())
E=[]
N='#002342';B='#00769B';P='#6500BC'
def box(n,x,y,w,h,c,rad=0):E.append(dict(kind='rect',name=n,x=x,y=y,w=w,h=h,color=c,r=rad))
def img(n,f,x,y,w,h):E.append(dict(kind='image',name=n,file='assets/'+f,x=x,y=y,w=w,h=h))
def tx(n,v,x,y,w,h,z,c=N,b=False,font='Arial',align='left'):E.append(dict(kind='text',name=n,value=v,x=x,y=y,w=w,h=h,size=z,color=c,bold=b,font=font,rot=0,align=align))
remove={'Actual photographic portrait, background masked only','Top right slogan','Tutor information panel','Tutor name','Tutor role','Tutor profession','Tutor institution','Tutor masters','Tutor doctorate','linkedin','Tutor LinkedIn','Original-style hero accents'}
for e in old['elements']:
 if e['name'] in remove:continue
 e=copy.deepcopy(e)
 if e['name']=='Classroom background':e.update(file='assets/classroom-hero.png',h=618)
 # Insert the outcomes band before the retained benefits, booking and footer.
 if e['y']>=1150:e['y']+=200
 if e['name']=='Central white sheet':e['h']+=200
 if ' learning ' in e['name']:
  e['x']+=29;e['w']-=29
  x=e['x']-28;c='00769B' if e['name'].startswith('DA') else '6500BC'
  img('Skill tick '+e['name'],'circle-check-'+c+'.png',x,e['y']+5,17,17)
 E.append(e)
E.insert(next(i for i,e in enumerate(E) if e['name']=='Intake'),dict(kind='image',name='Left hero brush accents',file='assets/left-hero-brushes.png',x=0,y=0,w=560,h=618))
# Preserve the full original photograph, with exact source aspect ratio and no overlap.
img('Original JPEG portrait — unchanged','actual-portrait.jpeg',610,24,390,390*2292/1856)
box('Tutor card',610,514,390,97,N,12)
tx('Tutor name','Jotham Martin Wambi',625,524,365,31,24,'#FFFFFF',True)
tx('Tutor profession','Main Tutor · Data Scientist & ML/AI Engineer',625,561,366,23,16,'#FFFFFF',False,'Arial Narrow')
tx('Tutor institution','Lecturer, AI & Machine Learning, IUEA',625,586,365,22,15,'#FFFFFF')
# A spacious shared outcome band, with one icon per distinct benefit.
tx('Outcomes heading','By the end of the camp, learners will have:',48,1162,935,39,27,N,True)
cols=[(61,'folder-open-00769B.png','Built a practical\nportfolio project',B),(302,'database-00769B.png','Analysed\nreal datasets',B),(543,'chart-column-00769B.png','Created data\nvisualisations',B),(784,'brain-6500BC.png','Built a\nprediction model',P)]
for i,(x,f,v,c) in enumerate(cols):
 img('Outcome icon '+str(i+1),f,x+70,1215,51,47)
 tx('Outcome '+str(i+1),v,x,1276,190,60,22,c,True,'Arial Narrow','center')
 if i==3:tx('ML outcome qualifier','Machine Learning track',x-6,1334,204,23,16,P,False,'Arial Narrow','center')
box('Outcomes divider',49,1364,927,1,'#CFDEE8')
(r/'source/layout.json').write_text(json.dumps(dict(width=1024,height=1976,elements=E),indent=2))
print('Layout includes unchanged full original photo, ten skill ticks and four outcomes')
