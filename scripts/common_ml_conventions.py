"""Retain conventional ML matrix names, with explicit beginner definitions."""
import copy,json,re,ast
from pathlib import Path
from descriptive_teaching_names import chunk_program,rename_code
ROOT=Path(__file__).resolve().parents[1]
def apply():
 p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text())
 for d in decks:
  if d['week']<8 or d.get('common_ml_names'):continue
  seen_input=False;old=d['slides'];new=[];skip=0
  for i,s in enumerate(old):
   if skip:skip-=1;continue
   for k in ('body','notes','caption'):
    if k in s:s[k]=s[k].replace('mean_absolute_error_value','mae').replace('root_mean_squared_error','rmse')
   if not s.get('code'):new.append(s);continue
   program=s.get('practice_code') or s['code']
   if s.get('practice_code'):
    while i+skip+1<len(old) and old[i+skip+1].get('kind')=='code' and old[i+skip+1].get('practice_code')=='':skip+=1
   program=rename_code(program,{'mean_absolute_error_value':'mae','root_mean_squared_error':'rmse'})
   # Work on the AST string to match formatted multiline calls safely.
   tree=ast.parse(program);lines=program.splitlines();prefix=[]
   for node in ast.walk(tree):
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='fit' and len(node.args)>=2:
     x,y=node.args[:2]
     if isinstance(x,ast.Subscript) and isinstance(x.value,ast.Name) and x.value.id=='training_data':
      valid=copy.deepcopy(x);valid.value.id='validation_data'
      if not seen_input:
       prefix=['X_train = '+ast.unparse(x),'y_train = '+ast.unparse(y),'X_valid = '+ast.unparse(valid),'y_valid = validation_data["target"]']
       seen_input=True
      node.args[0]=ast.Name(id='X_train',ctx=ast.Load());node.args[1]=ast.Name(id='y_train',ctx=ast.Load())
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='predict' and node.args:
     x=node.args[0]
     if isinstance(x,ast.Subscript) and isinstance(x.value,ast.Name) and x.value.id=='validation_data':node.args[0]=ast.Name(id='X_valid',ctx=ast.Load())
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='cross_val_score':
     node.args[1]=ast.Name(id='X_train',ctx=ast.Load());node.args[2]=ast.Name(id='y_train',ctx=ast.Load())
   # In Test 2 revision the one-feature example is followed by two-feature pipelines.
   if d['week']==14 and s['title']=='The model tools':
    program=ast.unparse(tree)+'\nX_train = training_data[feature_columns]\nX_valid = validation_data[feature_columns]'
   else:program='\n'.join(prefix)+ ('\n' if prefix else '')+ast.unparse(tree)
   if prefix:
    new.append({'kind':'explanation','title':'Standard names for model inputs','body':'X_train: training input columns. y_train: the matching observed targets.\n\nX_valid: validation input columns. y_valid: their observed targets, kept for evaluation.\n\nCapital X usually means a two-dimensional table; lowercase y usually means one target per row.','notes':'These are common machine-learning conventions. Some tutorials write train_x and train_y instead. The names are chosen by the programmer, not special Python keywords. Keep training_data as the full table; selecting X_train must exclude target. Rows in X and y must stay paired. fit uses training pairs; predict receives only X_valid. Compare predictions with y_valid afterwards.','introduced_operations':['ml_matrix_names'],'operation_prerequisite':True})
   formatted,chunks=chunk_program(program)
   for j,part in enumerate(chunks):
    t=copy.deepcopy(s);title=re.sub(r' \(\d+/\d+\)$','',s['title']);t['title']=title+(f' ({j+1}/{len(chunks)})' if len(chunks)>1 else '')
    t.update(code=part,practice_code=formatted if j==0 else '',code_size=25)
    # Replace previous complete-code walkthrough, retaining the meaning/result explanations.
    note=t.get('notes','');note=note.split('Complete example, step by step')[0]+'Complete example\n'+formatted+'\n\n'+('Model inputs: X_train and X_valid select input columns only; y_train and y_valid contain targets in the same row order.\n' if seen_input else '')+'\n'+(note.split('Reading the result\n',1)[1] if 'Reading the result\n' in note else '')
    t['notes']=note
    if s.get('revision_example') or s.get('revision_check'):
     t['revision_example']=True;t['revision_check']=rename_code(s.get('revision_check',''),{'mean_absolute_error_value':'mae','root_mean_squared_error':'rmse'}) if j==len(chunks)-1 else ''
    new.append(t)
  d['slides']=new;d['common_ml_names']=True
  for i,s in enumerate(new,1):s['sequence_number']=i
 p.write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':apply()
