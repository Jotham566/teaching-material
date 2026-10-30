"""Trusted numerical contracts for later engineering work.

These assess declared outputs on unseen inputs, not claims in a report.
The notebook is executed only by isolated_grading, never imported here.
"""
import math,random,statistics,json,copy,re,unicodedata
from pathlib import Path

DOMAINS={
 'CML3112':('building cooling load','kW',0.45,0.8,58),
 'CML3113':('crusher energy demand','kWh/t',0.12,0.2,16),
 'CML3111':('motor winding temperature','deg C',0.7,1.1,95),
}

def dataset(cohort,seed=17,n=90,dirty=False):
    _,_,a,b,_=DOMAINS[cohort];rng=random.Random(seed);rows=[]
    for i in range(n):
        load=round(rng.uniform(20,95),2);ambient=round(rng.uniform(18,35),2)
        rows.append(dict(record_id=i+1,equipment_id='E'+str(i%6+1),load_pct=load,ambient_c=ambient,
                         target=round(a*load+b*ambient+rng.gauss(0,.7),3)))
    if dirty:
        rows[3]['target']=None;rows[8]['load_pct']=-5;rows[13]['ambient_c']=None
        rows.append(dict(rows[0]))
    return rows

def clean(rows):
    seen=set();kept=[]
    for r in rows:
        if r['record_id'] in seen:continue
        seen.add(r['record_id'])
        if r['target'] is None or not 0<=r['load_pct']<=100:continue
        kept.append(dict(r))
    median=statistics.median(r['ambient_c'] for r in kept if r['ambient_c'] is not None)
    for r in kept:
        if r['ambient_c'] is None:r['ambient_c']=median
    return kept

def summary(rows):
    targets=[r['target'] for r in rows]
    return dict(count=len(rows),mean=statistics.mean(targets),minimum=min(targets),maximum=max(targets),
                group_means={g:statistics.mean(r['target'] for r in rows if r['equipment_id']==g) for g in sorted({r['equipment_id'] for r in rows})})

def metrics(actual,predicted):
    tp=sum(a==1 and p==1 for a,p in zip(actual,predicted));tn=sum(a==0 and p==0 for a,p in zip(actual,predicted))
    fp=sum(a==0 and p==1 for a,p in zip(actual,predicted));fn=sum(a==1 and p==0 for a,p in zip(actual,predicted))
    return dict(tp=tp,tn=tn,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0,recall=tp/(tp+fn) if tp+fn else 0,cost=5*fn+fp)

def same(a,b):
    if isinstance(b,dict):return isinstance(a,dict) and a.keys()==b.keys() and all(same(a[k],v) for k,v in b.items())
    if isinstance(b,list):return isinstance(a,(list,tuple)) and len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    if isinstance(b,(int,float)):return not isinstance(a,bool) and isinstance(a,(int,float)) and math.isfinite(a) and math.isclose(a,b,rel_tol=1e-6,abs_tol=1e-6)
    return a==b

# Accept equivalent written units without changing numerical or dimensional checks.
_UNIT_PATTERNS = {
 'deg C': r'(?:°\s*c|deg(?:ree)?s?\.?\s*c(?:elsius)?|celsius)',
 'kW': r'kw',
 'kWh/t': r'kwh\s*/\s*t',
 'observations': r'observations',
}
def unit_matches(actual, expected, label=False):
    if not isinstance(actual, str): return False
    text = unicodedata.normalize('NFKC', actual).strip().lower()
    pattern = _UNIT_PATTERNS.get(expected)
    if pattern is None: return text == expected.lower()
    if label:
        return re.search(r'(?<![\w/])' + pattern + r'(?![\w/])', text) is not None
    return re.fullmatch(pattern, text) is not None

def measurement_same(actual, expected):
    return (isinstance(actual, dict) and actual.keys() == expected.keys()
            and same(actual['value'], expected['value'])
            and unit_matches(actual['unit'], expected['unit']))

TASKS={
 'audit':('audit_cleaning(raw_records, cleaned_records)','Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive. Report the actual supplied data, which may still contain defects. Do not change either input. All five values are integer counts.'),
 'clean':('clean_records(records)','Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values. Preserve raw input. No other changes.'),
 'summary':('summarize_records(clean_records)','Return count, mean, minimum, maximum of target and group_means by equipment_id. Retain full precision.'),
 'regression':('predict_regression(training_records, feature_records)','Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.'),
 'classification':('classification_metrics(actual, predicted)','For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.'),
 'split':('group_split(records)','Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test. Return train, validation and test lists of record_id in input order. Do not use target values to choose membership.'),
 'features':('make_features(feature_records)','Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c]. Use inputs available at prediction time only.'),
 'ablation':('ablation_metrics(training_records, validation_records)','Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c. Evaluate both on the same validation records. Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding. Inputs are complete; never fit on validation targets.'),
 'selection':('select_model(candidates, max_mae, max_ms)','Candidates have name, validation_mae and latency_ms. Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically. Return the selected name or None. Never use test scores for selection.'),
 'charts':('build_charts(clean_records)','Return at least three actual matplotlib Figure objects: scatter load_pct vs target; bar of mean target by equipment_id in alphabetical order; target histogram with ten equal bins from minimum to maximum. Add chart titles and axis labels, including target units. A fourth figure, when required, plots record_id vs target in input order.'),
 'charts4':('build_charts(clean_records)','Return all four figures described by the charts contract, including record_id vs target. These must be actual matplotlib Figure objects, not metadata dictionaries.'),
 'findings':('five_findings(clean_records)','Return a dict with count, mean, minimum, maximum and group_gap (highest minus lowest equipment mean). Each value is a dict with value and unit; count uses observations and other values use the cohort target unit. These numerical findings are checked independently of the narrative.'),
 'groupcv':('group_cv_mae(records)','The records are clean and have targets. Using whole equipment groups, hold out each of E1, E2, E3, E4 and E5 in turn (E6 is never used). For each fold fit sklearn LinearRegression on load_pct and ambient_c using the other four groups, and compute the MAE on the held-out group. Return folds (the five MAEs in the order E1 to E5), mean (their average) and spread (their sample standard deviation, ddof=1). Do not round.'),
 'ridgeknn':('ridge_and_knn(training_records, validation_records)','Records are complete and the validation records are held out. Fit on the training records only. Ridge: a pipeline of PolynomialFeatures(3, include_bias=False), StandardScaler() and Ridge(alpha=1.0) on load_pct alone. Nearest neighbours: StandardScaler fitted on the training load_pct and ambient_c, then KNeighborsRegressor(n_neighbors=3). Return ridge_mae and knn_mae, each model\'s MAE on the validation records without rounding, and better, which is the text "ridge" or "knn" for the smaller MAE.'),
 'errors':('regression_errors(actual, predicted)','Return mae and rmse, calculated over the same paired observations, with full precision.'),
}

def check(ns,task):
    cohort=ns.get('COHORT','');fn=ns.get(TASKS[task][0].split('(')[0])
    if cohort not in DOMAINS:return False,'Set your assigned COHORT.'
    if not callable(fn):return False,'Implement '+TASKS[task][0]+'.'
    try:
        for seed in (71,113):
            rows=dataset(cohort,seed,n=36,dirty=True);fixed=clean(rows)
            if task=='clean':ok=same(fn(rows),fixed)
            elif task=='summary':ok=same(fn(fixed),summary(fixed))
            elif task=='audit':
                candidates=[copy.deepcopy(fixed),copy.deepcopy(fixed)+[dict(fixed[0])],copy.deepcopy(fixed)]
                candidates[-1][0]['target']=None;candidates[-1][1]['load_pct']=-1
                ok=True
                for candidate in candidates:
                    expected=dict(raw_count=len(rows),cleaned_count=len(candidate),duplicate_ids=len(candidate)-len({r['record_id'] for r in candidate}),missing_targets=sum(r['target'] is None for r in candidate),invalid_loads=sum(not 0<=r['load_pct']<=100 for r in candidate))
                    if not same(fn(rows,candidate),expected):ok=False;break
            elif task=='classification':
                a=[0,1,1,0,1,0,1,1] if seed==71 else [0,0,0]
                p=[1,1,0,0,1,0,0,1] if seed==71 else [0,0,0]
                ok=same(fn(a,p),metrics(a,p))
            elif task=='split':
                expected={k:[r['record_id'] for r in fixed if r['equipment_id'] in groups] for k,groups in [('train',['E1','E2','E3','E4']),('validation',['E5']),('test',['E6'])]}
                ok=same(fn(fixed),expected)
            elif task=='features':
                x=[{k:v for k,v in r.items() if k!='target'} for r in fixed]
                ok=same(fn(x),[[r['load_pct'],r['ambient_c'],r['load_pct']/100,r['load_pct']*r['ambient_c']] for r in x])
            elif task=='ablation':
                training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
                expected=json.loads((Path(__file__).parent/'specs/hidden/ablation_reference_values.json').read_text())[cohort+'|'+str(seed)]
                ok=same(fn(training,held),expected)
            elif task=='selection':
                candidates=[dict(name='linear',validation_mae=2,latency_ms=3),dict(name='tree',validation_mae=1,latency_ms=30),dict(name='baseline',validation_mae=2,latency_ms=1)]
                limit=10 if seed==71 else 0
                ok=fn(candidates,2,limit)==('baseline' if seed==71 else None)
            elif task in ('charts','charts4'):
                out=fn(fixed);count=4 if task=='charts4' else 3
                from isolated_grading import PlotEvidence
                ok=isinstance(out,list) and len(out)>=count and all(isinstance(f,PlotEvidence) for f in out[:count])
                if ok:
                    axes=[f.get('plot_axes',[]) for f in out[:count]]
                    ok=all(len(a)==1 for a in axes)
                if ok:
                    axes=[a[0] for a in axes];unit=DOMAINS[cohort][1]
                    ok=all(a['title'].strip() and a['xlabel'].strip() and a['ylabel'].strip() for a in axes)
                    ok=ok and all(unit_matches(a['xlabel']+' '+a['ylabel'], unit, label=True) for a in axes)
                    expected=[[r['load_pct'],r['target']] for r in fixed]
                    ok=ok and any(same(points,expected) for points in axes[0]['scatter'])
                    groups=summary(fixed)['group_means'];bars=axes[1]['bars']
                    ok=ok and same([b['height'] for b in bars],list(groups.values())) and axes[1]['xticklabels']==list(groups)
                    import numpy as np
                    heights,edges=np.histogram([r['target'] for r in fixed],bins=10)
                    bars=axes[2]['bars']
                    ok=ok and same([b['height'] for b in bars],heights.tolist()) and same([b['x'] for b in bars],edges[:-1].tolist())
                    if count==4:
                        ok=ok and any(same(line['x'],[r['record_id'] for r in fixed]) and same(line['y'],[r['target'] for r in fixed]) for line in axes[3]['lines'])
            elif task=='findings':
                values=summary(fixed);values['group_gap']=max(values['group_means'].values())-min(values['group_means'].values());del values['group_means']
                expected={k:dict(value=v,unit='observations' if k=='count' else DOMAINS[cohort][1]) for k,v in values.items()}
                actual=fn(fixed)
                ok=isinstance(actual,dict) and actual.keys()==expected.keys() and all(measurement_same(actual[k],v) for k,v in expected.items())
            elif task=='errors':
                a=[1,3,7];p=[2,3,5] if seed==71 else [1,3,7]
                expected=dict(mae=sum(abs(x-y) for x,y in zip(a,p))/3,rmse=math.sqrt(sum((x-y)**2 for x,y in zip(a,p))/3))
                ok=same(fn(a,p),expected)
            else:
                # Compare predictions with a reference built in the pinned
                # runtime, including the published tree parameters.
                training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
                features=[{k:v for k,v in r.items() if k!='target'} for r in held]
                expected=json.loads((Path(__file__).parent/'specs/hidden/regression_reference_values.json').read_text())[cohort+'|'+str(seed)]
                ok=same(fn(training,features),expected)
            if not ok:return False,'Check '+TASKS[task][0]+' against its published input/output and boundary rules. Tested on unseen records.'
        return True,''
    except Exception as exc:return False,'Your '+TASKS[task][0]+' failed: '+str(exc)[:180]
