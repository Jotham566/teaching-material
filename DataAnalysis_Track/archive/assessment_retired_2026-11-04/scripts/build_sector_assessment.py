"""Publish S13 numeric questions without exposing private reference values."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from sector_findings import QUESTIONS
out=ROOT/'DataAnalysis_Track/assessment_banks/S13';out.mkdir(parents=True,exist_ok=True)
questions={f'q{i+1}':dict(marks=8,visible=False,prompt='Verify numerical evidence for finding '+str(i+1)+' in the chosen sector.',answer_vars=['SECTOR','FINDINGS']) for i in range(5)}
(G/'specs/spec_S13.py').write_text("ASSIGNMENT='S13'\nTITLE='Sector investigation: numerical component only'\nDEFAULT_COHORT='DA'\nQUESTION_ORDER="+repr(list(questions))+"\nQUESTIONS="+repr(questions)+'\n')
(G/'specs/hidden/spec_S13_hidden.py').write_text('from sector_findings import check\nQUESTIONS={'+','.join(repr(f'q{i+1}')+': {"check": lambda ns: check(ns,'+str(i)+')}' for i in range(5))+'}\n')
parts=['# S13 — sector investigation: numerical evidence','**DRAFT: component validation only. This is not a released assignment or a final-grade specification.** The assessment remains 30% of the independent track and 100 marks: Question 20, Analysis 40, Judgement 25, Communication 15. The checks below supply the Analysis component. The remaining 60 marks require calibrated reasoning and chart evidence before release.',
'Choose bank, machine or development. Use the matching fixed file in ../../data/sector_snapshots and read its README for provenance, units and limits. Compute the five findings below in your notebook; show the analysis and a relevant chart with a caption for each. Present the five numbered findings, limitations and recommendation in a concise accessible report. Marks concern the findings, not coding style. Do not replace missing values silently or infer causation from these comparisons.',
'Keep STUDENT_ID as your DA roster ID and COHORT="DA". Set SECTOR to your choice. Save a FINDINGS dictionary keyed by the question IDs; each item contains a numeric value and the exact published unit. Example structure (not an answer): `FINDINGS={"subscription_rate":{"value":0.0,"unit":"percent"}, ...}`. Prefer full precision; values rounded to two decimals are accepted. GDP accepts 1 USD rounding difference; the ending year must be exact. Each finding is worth 8 numerical marks. Fractions are not percentages, and a percentage-point difference is not a relative percentage change.']
for sector,items in QUESTIONS.items():
 parts+=['## '+sector]
 for i,(qid,unit,question) in enumerate(items,1):parts+=[f'{i}. `{qid}` — {question} Unit: `{unit}`.']
parts+=['## Submission and limits','Submit one notebook and one accessible PDF/DOCX report together. The numerical component checks values against the chosen snapshot; it cannot establish whether a recommendation is justified or a chart communicates well. Its 40-mark output must not be imported as a final 100-mark assessment. The S13 form stays closed until the full rubric and packet workflow pass release checks and actual dates are supplied.']
(out/'TASKS.md').write_text('\n\n'.join(parts)+'\n')
cell={'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':'STUDENT_ID="YOUR_DA_ID"\nCOHORT="DA"\nSECTOR="bank"  # or machine / development\nFINDINGS={}  # Populate from your analysis, using TASKS.md question IDs.\n'}
(out/'S13_student.ipynb').write_text(json.dumps(dict(cells=[cell],metadata={},nbformat=4,nbformat_minor=5),indent=2)+'\n')
print('Built draft S13 numerical component: 5 findings x 8 marks; full release remains blocked')
