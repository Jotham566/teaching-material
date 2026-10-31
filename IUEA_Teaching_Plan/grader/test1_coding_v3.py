"""Independent checks for the coding-only take-home Test 1."""
import math
from engineering_contracts import dataset, clean, DOMAINS, unit_matches

VERSION = '2026.10-test1-coding-v3'
PARTS = [('eda',10),('before',10),('cleaning',20),('after',10),
         ('statistics',15),('grouping',15),('conditions',10),('loops',10)]
FUNCTIONS = dict(eda='explore_data', before='plot_observations', cleaning='clean_observations',
                 after='plot_cleaned', statistics='calculate_statistics', grouping='summarize_equipment',
                 conditions='classify_load', loops='count_load_bands')

def equal(actual, expected):
    import pandas as pd
    try:
        if isinstance(expected,pd.DataFrame):
            if not isinstance(actual,pd.DataFrame): return False
            pd.testing.assert_frame_equal(actual.reset_index(drop=True),expected.reset_index(drop=True),check_dtype=False,check_exact=False,rtol=1e-6,atol=1e-6)
            return True
        if isinstance(expected,pd.Series):
            if not isinstance(actual,pd.Series): return False
            pd.testing.assert_series_equal(actual,expected,check_dtype=False,check_names=False,check_exact=False,rtol=1e-6,atol=1e-6)
            return True
        if isinstance(expected,dict):
            return isinstance(actual,dict) and actual.keys()==expected.keys() and all(equal(actual[k],v) for k,v in expected.items())
        if isinstance(expected,list):
            return isinstance(actual,list) and len(actual)==len(expected) and all(equal(a,b) for a,b in zip(actual,expected))
        if isinstance(expected,(int,float)) or hasattr(expected,'item'):
            return not isinstance(actual,bool) and math.isclose(float(actual),float(expected),rel_tol=1e-6,abs_tol=1e-6)
        # A Series or array answer gives an element-wise result, which is a wrong answer, not a crash.
        return bool(actual==expected)
    except (AssertionError,ValueError,TypeError,KeyError): return False

def assess(ns, task):
    import pandas as pd
    fn=ns.get(FUNCTIONS[task]); passed=[]
    # Keep already-issued notebooks with the former raw_table name gradable.
    submitted_raw_data = ns.get('raw_data', ns.get('raw_table'))
    read_ok = task=='eda' and equal(submitted_raw_data, ns.get('_IUEA_ASSIGNED_DATA')) and isinstance(submitted_raw_data, pd.DataFrame)
    if not callable(fn): return False,'Complete '+FUNCTIONS[task]+'.', .2 if read_ok else 0
    if task in ('conditions','loops') and not ns.has_syntax(FUNCTIONS[task], 'If' if task=='conditions' else 'For'):
        return False, 'Use the requested if/elif/else or for-loop inside this function.', 0
    course=ns.get('COHORT')
    if course not in DOMAINS: return False,'Invalid course.',0
    for seed in (71,113):
        raw=dataset(course,seed,36,dirty=True)
        # Test boundary loads, duplicate handling, and a mode that is not simply all IDs.
        raw[0]['load_pct']=0;raw[1]['load_pct']=100
        raw[-1]=dict(raw[0]);raw[5]['equipment_id']='E1'
        fixed=clean(raw);table=pd.DataFrame(raw);cleaned=pd.DataFrame(fixed)
        if task=='conditions':
            for load,label in [(0,'low'),(39.99,'low'),(40,'medium'),(75,'medium'),(75.01,'high'),(100,'high')]:
                try: passed.append(fn(load)==label)
                except Exception: passed.append(False)
            continue
        if task=='loops':
            for values in ([],[0,40,75,100],cleaned['load_pct'].tolist()):
                expected={k:0 for k in ('low','medium','high')}
                for value in values: expected['low' if value<40 else 'medium' if value<=75 else 'high']+=1
                try: passed.append(equal(fn(values),expected))
                except Exception: passed.append(False)
            continue
        sizes={'eda':4,'before':5,'cleaning':5,'after':5,'statistics':6,'grouping':3}
        try:
            if task in ('before','after'):
                from isolated_grading import PlotEvidence
                data=raw if task=='before' else fixed
                output=fn(data,DOMAINS[course][1],'Before cleaning' if task=='before' else 'After cleaning')
                if not isinstance(output,PlotEvidence) or len(output.get('plot_axes',[]))!=1:
                    passed.extend([False]*5);continue
                ax=output['plot_axes'][0]
                expected=[[r['load_pct'],r['target']] for r in data if r['target'] is not None]
                # Matplotlib represents missing pairs as NaN. Ignore only non-finite pairs.
                scatter=[]
                for collection in ax['scatter']:
                    scatter.extend([p for p in collection if all(v is not None and math.isfinite(v) for v in p)])
                # Point order and chart wording/style are not assessed.
                correct_points=equal(sorted(scatter),sorted(expected))
                passed.extend([correct_points,correct_points,bool(ax['title'].strip()),
                               bool(ax['xlabel'].strip()) and ('%' in ax['xlabel'] or 'percent' in ax['xlabel'].lower()),
                               unit_matches(ax['ylabel'],DOMAINS[course][1],label=True)])
                continue
            output=fn(raw if task in ('eda','cleaning') else fixed)
            if task=='eda':
                expected={'preview':table.head(),'rows':len(table),'columns':len(table.columns),
                          'missing':table.isna().sum(),'duplicates':table.duplicated('record_id').sum()}
                passed.extend([isinstance(output,dict) and equal(output.get('preview'),expected['preview']),
                               isinstance(output,dict) and equal(output.get('rows'),expected['rows']) and equal(output.get('columns'),expected['columns']),
                               isinstance(output,dict) and equal(output.get('missing'),expected['missing']),
                               isinstance(output,dict) and equal(output.get('duplicates'),expected['duplicates'])])
            elif task=='cleaning':
                # Credit correctly retained IDs, then each measurement/category column independently.
                for column in table.columns:
                    passed.append(isinstance(output,pd.DataFrame) and column in output and
                                  equal(output[column].reset_index(drop=True),cleaned[column].reset_index(drop=True)))
            elif task=='statistics':
                target=cleaned['target']
                expected={k:getattr(target,k)() for k in ('mean','sum','median','count','std')}
                expected['mode']=cleaned['equipment_id'].mode().tolist()
                passed.extend(isinstance(output,dict) and equal(output.get(k),v) for k,v in expected.items())
            elif task=='grouping':
                expected=cleaned.groupby('equipment_id')['target'].agg(['mean','sum','count'])
                for column in expected:
                    passed.append(isinstance(output,pd.DataFrame) and column in output and
                                  equal(output[column].sort_index(),expected[column]))
        except Exception:
            passed.extend([False]*sizes[task])
    fraction=sum(bool(x) for x in passed)/len(passed)
    if task=='eda':
        fraction=.2*bool(read_ok)+.8*fraction
    return fraction==1,f'{sum(bool(x) for x in passed)}/{len(passed)} function checks passed.' + (f' CSV reading: {bool(read_ok)}.' if task=='eda' else ''),fraction


def hidden_spec_source():
    """Generate the matching trusted dispatch, even after restoring an older snapshot."""
    return 'from test1_coding_contracts import assess\nQUESTIONS={\n' + ',\n'.join(
        f'{("q"+str(i))!r}: {{"check": lambda ns: assess(ns,{task!r})}}'
        for i,(task,_) in enumerate(PARTS,1)) + '\n}\n'
