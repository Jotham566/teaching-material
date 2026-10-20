"""Private equivalent pandas solutions for regression testing, never student ZIPs.
The independent engineering_reference and hidden expectations remain unchanged.
"""
import pandas as pd


def records_from_table(table):
    return table.astype(object).where(table.notna(), None).to_dict('records')


def clean_records(records):
    table = pd.DataFrame(records).drop_duplicates('record_id').copy()
    table = table[table['target'].notna() & table['load_pct'].between(0, 100)].copy()
    table['ambient_c'] = table['ambient_c'].fillna(table['ambient_c'].median())
    return records_from_table(table)


def summarize_records(clean_records):
    table = pd.DataFrame(clean_records)
    target = table['target']
    return dict(count=len(table), mean=float(target.mean()), minimum=float(target.min()),
                maximum=float(target.max()), group_means=table.groupby('equipment_id')['target'].mean().to_dict())


def audit_cleaning(raw_records, cleaned_records):
    table = pd.DataFrame(cleaned_records, columns=['record_id','equipment_id','load_pct','ambient_c','target'])
    return dict(raw_count=len(raw_records), cleaned_count=len(table),
                duplicate_ids=int(table.duplicated('record_id').sum()),
                missing_targets=int(table['target'].isna().sum()),
                invalid_loads=int((~table['load_pct'].between(0,100)).sum()))


def group_split(records):
    table = pd.DataFrame(records)
    return {name:table.loc[table['equipment_id'].isin(groups),'record_id'].tolist()
            for name,groups in [('train',['E1','E2','E3','E4']),('validation',['E5']),('test',['E6'])]}


def predict_regression(training_records, feature_records):
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    training = pd.DataFrame(training_records)
    new = pd.DataFrame(feature_records)
    columns = ['load_pct','ambient_c']
    result = {'baseline':[float(training['target'].mean())]*len(new)}
    for name,model in [('linear',LinearRegression()),('tree',DecisionTreeRegressor(max_depth=4,random_state=17))]:
        pipeline = make_pipeline(SimpleImputer(strategy='median'),model)
        pipeline.fit(training[columns],training['target'])
        result[name] = pipeline.predict(new[columns]).tolist()
    return result


def regression_errors(actual, predicted):
    table = pd.DataFrame({'actual':actual,'predicted':predicted})
    errors = table['actual']-table['predicted']
    return dict(mae=float(errors.abs().mean()), rmse=float((errors**2).mean()**0.5))


def classification_metrics(actual, predicted):
    table = pd.DataFrame({'actual':actual,'predicted':predicted})
    a,p = table['actual'],table['predicted']
    tp=int(((a==1)&(p==1)).sum());tn=int(((a==0)&(p==0)).sum())
    fp=int(((a==0)&(p==1)).sum());fn=int(((a==1)&(p==0)).sum())
    return dict(tp=tp,tn=tn,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0,
                recall=tp/(tp+fn) if tp+fn else 0,cost=5*fn+fp)


def make_features(feature_records):
    table=pd.DataFrame(feature_records).copy()
    table['load_fraction']=table['load_pct']/100
    table['interaction']=table['load_pct']*table['ambient_c']
    return table[['load_pct','ambient_c','load_fraction','interaction']].to_numpy().tolist()


def ablation_metrics(training_records,validation_records):
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    train=pd.DataFrame(training_records).copy();valid=pd.DataFrame(validation_records).copy()
    for table in (train,valid):table['interaction']=table['load_pct']*table['ambient_c']
    errors=[]
    for columns in (['load_pct','ambient_c'],['load_pct','ambient_c','interaction']):
        model=LinearRegression().fit(train[columns],train['target'])
        errors.append(float(mean_absolute_error(valid['target'],model.predict(valid[columns]))))
    return dict(base_mae=errors[0],extended_mae=errors[1],improvement=errors[0]-errors[1])


def select_model(candidates,max_mae,max_ms):
    table=pd.DataFrame(candidates,columns=['name','validation_mae','latency_ms'])
    eligible=table[(table['validation_mae']<=max_mae)&(table['latency_ms']<=max_ms)]
    ranked=eligible.sort_values(['validation_mae','latency_ms','name'])
    return None if ranked.empty else ranked.iloc[0]['name']


def build_charts(clean_records):
    import matplotlib.pyplot as plt
    table=pd.DataFrame(clean_records)
    unit={'CML3111':'deg C','CML3112':'kW','CML3113':'kWh/t'}[COHORT]
    figures=[]
    fig,ax=plt.subplots();table.plot.scatter(x='load_pct',y='target',ax=ax)
    ax.set(title='Target versus load',xlabel='Load (%)',ylabel='Target ('+unit+')');figures.append(fig)
    means=table.groupby('equipment_id',sort=True)['target'].mean()
    fig,ax=plt.subplots();means.plot.bar(ax=ax)
    ax.set(title='Mean target by equipment',xlabel='Equipment',ylabel='Mean target ('+unit+')');figures.append(fig)
    fig,ax=plt.subplots();table['target'].plot.hist(bins=10,ax=ax)
    ax.set(title='Target distribution',xlabel='Target ('+unit+')',ylabel='Observation count');figures.append(fig)
    fig,ax=plt.subplots();ax.plot(table['record_id'],table['target'])
    ax.set(title='Target in record order',xlabel='Record ID (not time)',ylabel='Target ('+unit+')');figures.append(fig)
    return figures


def five_findings(clean_records):
    values=summarize_records(clean_records)
    groups=pd.Series(values.pop('group_means'))
    values['group_gap']=float(groups.max()-groups.min())
    unit={'CML3111':'deg C','CML3112':'kW','CML3113':'kWh/t'}[COHORT]
    return {k:dict(value=v,unit='observations' if k=='count' else unit) for k,v in values.items()}
