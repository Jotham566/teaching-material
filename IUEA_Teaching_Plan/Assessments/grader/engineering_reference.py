"""Lecturer-only reference implementation; NEVER include in student packages."""
import math,statistics

def clean_records(records):
    seen=set();out=[]
    for row in records:
        if row['record_id'] in seen:continue
        seen.add(row['record_id'])
        if row['target'] is None or not 0<=row['load_pct']<=100:continue
        out.append(dict(row))
    median=statistics.median(r['ambient_c'] for r in out if r['ambient_c'] is not None)
    for r in out:
        if r['ambient_c'] is None:r['ambient_c']=median
    return out

def summarize_records(rows):
    values=[r['target'] for r in rows]
    return dict(count=len(rows),mean=sum(values)/len(values),minimum=min(values),maximum=max(values),group_means={g:sum(r['target'] for r in rows if r['equipment_id']==g)/sum(r['equipment_id']==g for r in rows) for g in sorted({r['equipment_id'] for r in rows})})

def predict_regression(training_records,feature_records):
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    x=[[r['load_pct'],r['ambient_c']] for r in training_records];y=[r['target'] for r in training_records]
    test=[[r['load_pct'],r['ambient_c']] for r in feature_records]
    result={'baseline':[sum(y)/len(y)]*len(test)}
    for name,model in [('linear',LinearRegression()),('tree',DecisionTreeRegressor(max_depth=4,random_state=17))]:
        pipeline=make_pipeline(SimpleImputer(strategy='median'),model);pipeline.fit(x,y);result[name]=pipeline.predict(test).tolist()
    return result

def classification_metrics(actual,predicted):
    tp=tn=fp=fn=0
    for a,p in zip(actual,predicted):
        if a==1 and p==1:tp+=1
        elif a==0 and p==0:tn+=1
        elif a==0 and p==1:fp+=1
        else:fn+=1
    return dict(tp=tp,tn=tn,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0,recall=tp/(tp+fn) if tp+fn else 0,cost=5*fn+fp)

def group_split(records):
    return {name:[r['record_id'] for r in records if r['equipment_id'] in groups] for name,groups in [('train',['E1','E2','E3','E4']),('validation',['E5']),('test',['E6'])]}

def make_features(records):
    return [[r['load_pct'],r['ambient_c'],r['load_pct']/100,r['load_pct']*r['ambient_c']] for r in records]

def ablation_metrics(training_records,validation_records):
    from sklearn.linear_model import LinearRegression
    errors=[]
    for extended in (False,True):
        def features(rows):
            return [[r['load_pct'],r['ambient_c']]+([r['load_pct']*r['ambient_c']] if extended else []) for r in rows]
        model=LinearRegression().fit(features(training_records),[r['target'] for r in training_records])
        predicted=model.predict(features(validation_records))
        errors.append(sum(abs(r['target']-p) for r,p in zip(validation_records,predicted))/len(predicted))
    return dict(base_mae=errors[0],extended_mae=errors[1],improvement=errors[0]-errors[1])

def select_model(candidates,max_mae,max_ms):
    eligible=[r for r in candidates if r['validation_mae']<=max_mae and r['latency_ms']<=max_ms]
    return min(eligible,key=lambda r:(r['validation_mae'],r['latency_ms'],r['name']))['name'] if eligible else None

def regression_errors(actual,predicted):
    differences=[a-p for a,p in zip(actual,predicted)]
    return dict(mae=sum(abs(d) for d in differences)/len(differences),rmse=math.sqrt(sum(d*d for d in differences)/len(differences)))


def build_charts(rows):
    import matplotlib.pyplot as plt
    unit={'CML3111':'deg C','CML3112':'kW','CML3113':'kWh/t'}[COHORT]
    figures=[]
    fig,ax=plt.subplots();ax.scatter([r['load_pct'] for r in rows],[r['target'] for r in rows]);ax.set(title='How does demand vary with load?',xlabel='Load (%)',ylabel='Target ('+unit+')');figures.append(fig)
    means=summarize_records(rows)['group_means']
    fig,ax=plt.subplots();ax.bar(list(means),list(means.values()));ax.set(title='Which equipment has higher mean demand?',xlabel='Equipment',ylabel='Mean target ('+unit+')');figures.append(fig)
    fig,ax=plt.subplots();ax.hist([r['target'] for r in rows],bins=10);ax.set(title='What range of demand was observed?',xlabel='Target ('+unit+')',ylabel='Observation count');figures.append(fig)
    fig,ax=plt.subplots();ax.plot([r['record_id'] for r in rows],[r['target'] for r in rows]);ax.set(title='How does demand vary across record order?',xlabel='Record ID (not a time axis)',ylabel='Target ('+unit+')');figures.append(fig)
    return figures


def five_findings(rows):
    values=summarize_records(rows);values['group_gap']=max(values['group_means'].values())-min(values['group_means'].values());del values['group_means']
    unit={'CML3111':'deg C','CML3112':'kW','CML3113':'kWh/t'}[COHORT]
    return {k:dict(value=v,unit='observations' if k=='count' else unit) for k,v in values.items()}


def audit_cleaning(raw_records, cleaned_records):
    return dict(raw_count=len(raw_records),cleaned_count=len(cleaned_records),
                duplicate_ids=len(cleaned_records)-len({r['record_id'] for r in cleaned_records}),
                missing_targets=sum(r['target'] is None for r in cleaned_records),
                invalid_loads=sum(not 0<=r['load_pct']<=100 for r in cleaned_records))
