"""Reviewed wording corrections, applied before the final lecturer-note overlay."""
import json
from pathlib import Path
EDITS=json.loads((Path(__file__).resolve().parents[1]/'data/iuea_plain_language_edits.json').read_text())
def correct_text(text):
 for old,new in sorted(EDITS.items(),key=lambda x:-len(x[0])):
  text=text.replace(old,new)
 return text
def apply_plain_language(value):
 if isinstance(value,str):return correct_text(value)
 if isinstance(value,list):return [apply_plain_language(x) for x in value]
 if isinstance(value,dict):return {k:v if k in ('code','practice_code','url','filename') else apply_plain_language(v) for k,v in value.items()}
 return value
