"""Private deterministic exam checks. Never distribute this module to learners."""
import math
import copy
from engineering_contracts import dataset, clean, summary, same, DOMAINS, check, measurement_same, metrics
import test2_numpy_reference as T2REF

VERSION = '2026.12-colab-v3-weeks8-13'
PARTS = {
 'TEST1': __import__('test1_coding_contracts').PARTS,
 # Test 2 covers Weeks 8 to 13: split and validation (10), regression (8), errors (8), classification and cost (9),
 # group cross-validation (10), features and ablation (11), model selection (12), ridge and nearest neighbours (13).
 'TEST2': [('split',10),('regression',15),('errors',5),('classification',10),('groupcv',10),('ablation',10),('selection',10),('ridgeknn',15),('decisions',15)],
}
def decision_keys():
    import json
    from pathlib import Path
    return json.loads((Path(__file__).parent/'specs/hidden/colab_decision_keys.json').read_text())

def result(passed):
    fraction=sum(bool(x) for x in passed)/len(passed)
    return all(passed), f'{sum(bool(x) for x in passed)}/{len(passed)} checks passed.', fraction

def assess(ns, exam, task):
    if task=='decisions':
        answers=ns.get('DECISIONS',{})
        return result([isinstance(answers,dict) and str(answers.get(k,'')).strip().upper()==v for k,v in decision_keys()[exam].items()])
    if task in ('clean','charts'):
        # Two independent unseen datasets; retain existing plot-authenticity checks.
        return check(ns,task)
    names={'summary':'summarize_records','findings':'five_findings','split':'group_split','regression':'predict_regression','errors':'regression_errors',
           'classification':'classification_metrics','ablation':'ablation_metrics','selection':'select_model','groupcv':'group_cv_mae','ridgeknn':'ridge_and_knn'}
    fn=ns.get(names[task]);passed=[]
    if not callable(fn):return False,'Implement '+names[task]+'.',0
    cohort=ns.get('COHORT')
    if cohort not in DOMAINS:return False,'Invalid cohort.',0
    for seed in (71,113):
        fixed=clean(dataset(cohort,seed,n=36,dirty=True))
        if task=='summary':
            expected=summary(fixed);args=(fixed,)
        elif task=='findings':
            expected=summary(fixed);groups=expected.pop('group_means');expected['group_gap']=max(groups.values())-min(groups.values())
            expected={k:dict(value=v,unit='observations' if k=='count' else DOMAINS[cohort][1]) for k,v in expected.items()};args=(fixed,)
        elif task=='split':
            expected={k:[r['record_id'] for r in fixed if r['equipment_id'] in groups] for k,groups in [('train',['E1','E2','E3','E4']),('validation',['E5']),('test',['E6'])]};args=(fixed,)
        elif task=='errors':
            a=[1,3,7];p=[2,3,5] if seed==71 else [1,3,7]
            expected=dict(mae=sum(abs(x-y) for x,y in zip(a,p))/3,rmse=math.sqrt(sum((x-y)**2 for x,y in zip(a,p))/3));args=(a,p)
        elif task=='classification':
            a=[0,1,1,0,1,0,1,1] if seed==71 else [0,0,0]; p=[1,1,0,0,1,0,0,1] if seed==71 else [0,0,0]
            expected=metrics(a,p);args=(a,p)
        elif task=='ablation':
            import json
            from pathlib import Path
            training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
            expected=json.loads((Path(__file__).parent/'specs/hidden/ablation_reference_values.json').read_text())[cohort+'|'+str(seed)]
            args=(training,held)
        elif task=='selection':
            candidates=[dict(name='linear',validation_mae=2,latency_ms=3),dict(name='tree',validation_mae=1,latency_ms=30),dict(name='baseline',validation_mae=2,latency_ms=1)]
            limit=10 if seed==71 else 0
            try:passed.append(fn(copy.deepcopy(candidates),2,limit)==('baseline' if seed==71 else None))
            except Exception:passed.append(False)
            continue
        elif task=='groupcv':
            rows=clean(dataset(cohort,seed,n=60));expected=T2REF.group_cv(rows);args=(copy.deepcopy(rows),)
        elif task=='ridgeknn':
            training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
            expected=T2REF.ridge_and_knn(training,held);args=(copy.deepcopy(training),copy.deepcopy(held))
        else:
            import json
            from pathlib import Path
            training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
            training[4]['ambient_c']=None;held[2]['ambient_c']=None
            features=[{k:v for k,v in r.items() if k!='target'} for r in held]
            expected=json.loads((Path(__file__).parent/'specs/hidden/colab_regression_values.json').read_text())[cohort+'|'+str(seed)]
            args=(training,features)
        try:
            actual=fn(*args)
            compare = measurement_same if task == 'findings' else same
            passed.extend(isinstance(actual,dict) and k in actual and compare(actual[k],v) for k,v in expected.items())
        except Exception:
            passed.extend(False for _ in expected)
    return result(passed)
