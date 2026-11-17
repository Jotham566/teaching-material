"""Apply published execution gates to reasoning marks before combining totals."""
import math

def combine(result,rubric,deterministic,deterministic_maximum,assessment_maximum):
    numerical=float(deterministic['notebook_total']);maximum=float(deterministic['max_total'])
    if maximum!=deterministic_maximum or not math.isfinite(numerical) or not 0<=numerical<=maximum or deterministic['status'] not in ('OK','ERRORS'):
        raise ValueError('Invalid deterministic component')
    result=dict(result,deterministic=deterministic,maximum=assessment_maximum)
    if result['score'] is None:return result
    reason=float(result['score']);adjustments=[]
    for parent,gate in rubric.get('execution_gates',{}).items():
        ids={c['id'] for c in rubric['criteria'] if c.get('parent_criterion',c['id'])==parent}
        if not ids:raise ValueError('Execution gate names an unknown reasoning criterion')
        actual=float(deterministic[gate['field']]);required=float(gate['equals'])
        if not math.isfinite(actual) or not math.isfinite(required):raise ValueError('Invalid execution gate evidence')
        if actual==required:continue
        evaluations=result.get('evaluations',[])
        if len(evaluations)!=2:raise ValueError('Execution gate requires both criterion-level evaluations')
        removed=sum(sum(c['awarded'] for c in e['criteria'] if c['id'] in ids) for e in evaluations)/2
        reason-=removed
        adjustments.append(dict(parent_criterion=parent,removed=removed,reason=gate['reason'],field=gate['field'],observed=actual,required=required))
    if not -0.001<=reason<=rubric['maximum']:raise ValueError('Invalid reasoning total after execution gates')
    result['reasoning_score_before_gates']=result['score'];result['execution_gate_adjustments']=adjustments
    result['score']=round(numerical+max(0,reason),2)
    return result
