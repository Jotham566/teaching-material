"""Complete explanatory context and revision checks after the stepwise rebuild."""
import json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts')
from stepwise_teaching_expansion import idea,example
p=Path('data/iuea_deck_content.json');ds=json.loads(p.read_text())
for d in ds:
 if not d.get('stepwise_pipeline_revision') or d.get('stepwise_refined'):continue
 if d['week']==6:
  unit={'CML3111':'°C','CML3112':'kW','CML3113':'kWh/t'}[d['cohort']]
  quantity={'CML3111':'motor temperature','CML3112':'power demand','CML3113':'crusher energy'}[d['cohort']]
  i=next(i for i,s in enumerate(d['slides']) if s['title']=='Plot the target before cleaning')+1
  d['slides'][i:i]=[idea('Inspect a relationship before cleaning','A scatter plot places one observation at its load and target coordinates. x and y name the two columns; ax selects the plotting area.\n\nLook for gaps, unusual points and possible trends. A visible association does not show that load caused the target to change.'),example('Plot raw load against the target','raw_scatter_figure, raw_scatter_axes = plt.subplots()\nraw_data.plot.scatter(x="load_pct", y="target", ax=raw_scatter_axes)\nraw_scatter_axes.set_xlabel("Load (%)")\nraw_scatter_axes.set_ylabel("'+quantity+' ('+unit+')")\nraw_scatter_axes.set_title("Before cleaning")\nplt.show()','A point at load -5 is visible because these are uncleaned rows. Missing target values cannot be plotted. Later compare the cleaned scatter plot after applying the stated rules.')]
 for i,s in enumerate(d['slides'],1):
  s['sequence_number']=i
  if s.get('code'):
   s['teaching_explanation']=s['notes'].split('\n\nStep-by-step explanation')[0].split('\n\nVerified')[0] if d['week']==6 else ''
   if d['week']>=6:
    # Use the immediately preceding idea when it introduces this code group.
    if i>=2 and d['slides'][i-2]['kind']=='explanation':s['teaching_explanation']=d['slides'][i-2].get('body','')
  if d['week']==6 and '26.07' in (s.get('explain') or [''])[0] and d['cohort']!='CML3113':s['explain']=['Calculate the median using the retained rows only.']
 if d['week']==14:
  groups={}
  for s in d['slides']:
   if s.get('practice_code'):
    base=re.sub(r' — step \d+$','',re.sub(r' \(\d+/\d+\)$','',s['title']))
    s['original_example_title']=base;groups[base]=s
  for s in groups.values():s['last_example_step']=True
 d['stepwise_refined']=True
p.write_text(json.dumps(ds,ensure_ascii=False,indent=2)+'\n')
