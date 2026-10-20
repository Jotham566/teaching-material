"""Corrections from the full-course review, preserving assessment interfaces."""
import copy,json,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
def text(title,body,notes):return dict(kind='explanation',title=title,body=body,notes=notes)
def code(title,src,notes):return dict(kind='code',title=title,code=src,practice_code=src,code_size=25,body='',caption='Run using this week’s supplied CSV.',explain=[],notes=notes)
def apply():
 p=ROOT/'data/iuea_deck_content.json';D=json.loads(p.read_text())
 if not any(d['cohort']=='CML3112' and d['week']==2 for d in D):
  d=copy.deepcopy(next(d for d in D if d['cohort']=='CML3111' and d['week']==2));d['cohort']='CML3112';d['filename']='CML3112_Week02_Design_Infrastructure.pptx'
  links=json.loads((ROOT/'data/submission_links.json').read_text());quizzes=json.loads((ROOT/'data/quiz_links.json').read_text())
  def stamp(value):return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(ZoneInfo('Africa/Kampala')).strftime('%d %b %Y, %H:%M Kampala')
  for s in d['slides']:
   for field in ('title','body','notes','caption','code','practice_code'):
    if field in s:s[field]=s[field].replace('CML3111','CML3112').replace('motor_test_bench.csv','site_inspection_log.csv').replace('current_a','crack_mm').replace('Communications, Electrical, Mechatronics and Robotics Engineering','Architecture and Civil Engineering')
   if s['title']=='The engineering context':s['body']='A team records measurements during a site inspection.\n\nA reading has a number and a unit, such as crack width in millimetres.\n\nToday’s goal is to run and save the notebook; specialist construction knowledge is not required.'
   if 'catch-up upload' in s['title']:s['body']='Submit A1 separately from the A2 notebook and README.\n\nRecorded deadline: '+stamp(links['CML3112|W01']['closeAt'])+'. Check the active form for an announced extension.\n\nEnter your own Student Registration Number.'
   if s['title']=='Proof of life submission':
    s['body']='Opens: '+stamp(links['CML3112|W02']['openAt'])+'\n\nRecorded deadline: '+stamp(links['CML3112|W02']['closeAt'])+'\n\nUse your full Student Registration Number. Check the active form for any announced extension.'
   if s.get('url'):
    if '/forms/' in s['url']:
     s['url']=quizzes['CML3112|1'] if 'Quiz 1' in s['title'] else quizzes['CML3112|2'] if 'quiz' in s['title'].lower() else links['CML3112|W01']['url'] if 'Week 1' in s['title'] else links['CML3112|W02']['url']
  D.append(d)
 for d in D:
  if d.get('full_course_review_revision'):continue
  if d['week']==2:
   i=next(i for i,s in enumerate(d['slides']) if s['title']=='Your cohort data')+1
   # The setup code is provided, rather than an unexplained new coding assignment.
   d['slides'].insert(i,text('The supplied CSV-reading cell','The main notebook already contains the CSV-reading code. Upload the four-row Week 2 CSV, then run the cell.\n\nimport loads Python’s CSV tools. open opens the named file; DictReader uses its header as field names. list collects the rows; len counts them.\n\nKeep the supplied code. Weeks 3–4 explain how to write these operations yourself.','The intended result is four data rows; the header is not counted. If the file is missing, use Colab’s Files panel to upload this week’s CSV. Do not substitute the larger Week 4 file that shares its filename. This is a setup check, not a requirement to invent file-reading code before learning it.'))
  if d['week']==5:
   new=[]
   for s in d['slides']:
    if s['title']=='Filtering rows with a mask':
     s=copy.deepcopy(s);s['title']='Ask a question about each energy reading';s['body']='raw["kwh"] selects the energy column. Comparing it with 5000 returns one True or False per row.\n\nTrue means the reading is greater than 5,000 kWh; False means it is not. Equality does not pass this strict threshold.';s['notes']='This is a practice question, not an engineering safety limit. Separate calculating the answers from selecting the rows. True and False are Boolean values, not the strings "True" and "False".'
    if s['title']=='Readings above the stated threshold':
     new.extend([code('Inspect the answers before selecting rows','energy_is_high = raw["kwh"] > 5000\nprint(raw["kwh"].head())\nprint(energy_is_high.head())','Match the row labels in the two outputs. The comparison answers the question for every row and leaves raw unchanged.'),text('Use the True answers to select rows','raw[energy_is_high] returns the rows whose answer is True. This selection is often called a Boolean mask.\n\n.sum() counts True answers because True counts as 1 and False as 0.','Quoted names inside brackets select a named column; a True/False Series inside brackets selects rows. The question and the table must refer to matching row labels.'),code('Keep and count the high-energy readings','high_energy_readings = raw[energy_is_high]\nprint(high_energy_readings.head())\nprint(int(energy_is_high.sum()))','This result table contains the selected rows. We only inspect it here; the original raw table remains unchanged. The count should equal the number of retained rows. The supplied threshold is strictly greater than 5000, so exactly 5000 is excluded.')]);continue
    new.append(s)
   d['slides']=new
  # Remove old slide-number cues after insertions; retain subject-specific explanation.
  for i,s in enumerate(d['slides'],1):
   s['sequence_number']=i
   s['notes']=re.sub(r'^CML\d+, Week \d+, slide \d+:.*\n\n','',s.get('notes',''))
   # Generic prose should not be changed into identifiers just because a sentence ends with a period.
   if not s.get('code') and d['week']>=8:
    for field in ('body','notes'):
     if field in s:
      s[field]=s[field].replace('supported mean_load_by_equipment_group','supported result').replace('successful mean_load_by_equipment_group','successful result').replace('stated mean_load_by_equipment_group','stated result')
  d['full_course_review_revision']='2026-10-20'
 p.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':apply()
