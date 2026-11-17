"""Checks for ordinary notebook answers; retain compatibility with issued v3 tests."""
import ast
import math
from engineering_contracts import DOMAINS, clean, dataset, unit_matches
from test1_coding_v3 import equal, assess as assess_v3
VERSION='2026.10-test1-notebook-v4'
PARTS=[('eda',20),('before',10),('cleaning',20),('after',10),('statistics',15),('grouping',10),('function',5),('loops',10)]

def source_tree(ns):
    nodes=[]
    for source in getattr(ns,'notebook_sources',[]):
        try:nodes.extend(ast.parse(source).body)
        except SyntaxError:pass
    return ast.Module(body=nodes,type_ignores=[])

def method_used(ns, obj, method):
    return any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and
               isinstance(n.func.value,ast.Name) and n.func.value.id==obj and n.func.attr==method
               for n in ast.walk(source_tree(ns)))

def plot_checks(output,table,unit):
    from isolated_grading import PlotEvidence
    if not isinstance(output,PlotEvidence) or len(output.get('plot_axes',[]))!=1:return [False]*5
    ax=output['plot_axes'][0];points=[]
    for collection in ax['scatter']:
        points.extend(p for p in collection if all(v is not None and math.isfinite(v) for v in p))
    expected=table[['load_pct','target']].dropna().values.tolist()
    correct=equal(sorted(points),sorted(expected))
    return [correct,correct,bool(ax['title'].strip()),
            bool(ax['xlabel'].strip()) and ('%' in ax['xlabel'] or 'percent' in ax['xlabel'].lower()),
            unit_matches(ax['ylabel'],unit,label=True)]

def assess(ns,task):
    import pandas as pd
    if ns.get('_IUEA_NOTEBOOK_VERSION')=='2026.10-test1-coding-v3':
        return assess_v3(ns,'conditions' if task=='function' else task)
    raw=ns.get('_IUEA_ASSIGNED_DATA');course=ns.get('COHORT')
    if not isinstance(raw,pd.DataFrame) or course not in DOMAINS:return False,'Assigned dataset unavailable.',0
    records=raw.astype(object).where(raw.notna(),None).to_dict('records')
    fixed=pd.DataFrame(clean(records))
    def get(name):
        try:return ns.get(name)
        except Exception:return None
    checks=[];weights=[]
    if task=='eda':
        invalid=raw[raw['target'].isna() | (raw['load_pct']<0) | (raw['load_pct']>100)]
        expected=[('raw_data',raw,2),('first_rows',raw.head(),1),('last_rows',raw.tail(),1),
                  ('data_shape',list(raw.shape),1),('row_count',len(raw),1),
                  ('target_dtype',str(raw['target'].dtype),2),('numeric_summary',raw.describe(),2),
                  ('missing_counts',raw.isna().sum(),2),('duplicate_count',raw.duplicated('record_id').sum(),2),
                  ('invalid_records',invalid,4)]
        for name,value,weight in expected:checks.append(equal(get(name),value));weights.append(weight)
        checks.append(method_used(ns,'raw_data','info'));weights.append(2)
    elif task in ('before','after'):
        checks=plot_checks(get('before_figure' if task=='before' else 'after_figure'),raw if task=='before' else fixed,DOMAINS[course][1])
    elif task=='cleaning':
        result=get('cleaned_data')
        checks=[isinstance(result,pd.DataFrame) and col in result and equal(result[col].reset_index(drop=True),fixed[col].reset_index(drop=True)) for col in raw.columns]
    elif task=='statistics':
        checks=[equal(get('target_'+name),getattr(fixed['target'],name)()) for name in ('mean','sum','median','count','std')]
        modes=get('equipment_modes')
        if isinstance(modes,pd.Series):modes=modes.tolist()
        checks.append(equal(modes,fixed['equipment_id'].mode().tolist()))
    elif task=='grouping':
        result=get('equipment_summary');expected=fixed.groupby('equipment_id')['target'].agg(['mean','count'])
        checks=[isinstance(result,pd.DataFrame) and col in result and equal(result[col].sort_index(),expected[col]) for col in expected]
    elif task=='function':
        for seed in (71,113):
            rows=clean(dataset(course,seed,36,dirty=True));table=pd.DataFrame(rows)
            for column in ('target','load_pct'):
                try:result=ns.call_with_dataframe('calculate_column_statistics',rows,column)
                except Exception:result=None
                checks.extend(isinstance(result,dict) and equal(result.get(name),getattr(table[column],name)()) for name in ('mean','sum','median'))
    elif task=='loops':
        expected={name:0 for name in ('low','medium','high')}
        for value in fixed['load_pct']:expected['low' if value<40 else 'medium' if value<=75 else 'high']+=1
        result=get('load_band_counts')
        checks=[isinstance(result,dict) and equal(result.get(k),v) for k,v in expected.items()];weights=[2,2,2]
        loops=[n for n in source_tree(ns).body if isinstance(n,ast.For)]
        # Require the requested control flow to actually update the named answer.
        def updates(n):return any(isinstance(x,(ast.Assign,ast.AugAssign)) and any(isinstance(y,ast.Name) and y.id=='load_band_counts' for y in ast.walk(x)) for x in ast.walk(n))
        loops=[n for n in loops if updates(n)]
        checks.extend([bool(loops),any(isinstance(n,ast.If) and n.orelse for loop in loops for n in ast.walk(loop))]);weights.extend([2,2])
    weights=weights or [1]*len(checks)
    fraction=sum(w for check,w in zip(checks,weights) if check)/sum(weights)
    return fraction==1,f'{sum(bool(c) for c in checks)}/{len(checks)} checks passed.',fraction

def hidden_spec_source():
    return 'from test1_coding_contracts import assess\nQUESTIONS={\n'+',\n'.join(f'{("q"+str(i))!r}: {{"check": lambda ns: assess(ns,{task!r})}}' for i,(task,_) in enumerate(PARTS,1))+'\n}\n'
