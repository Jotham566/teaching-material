"""Grade eligible packets, isolate incomplete submissions, and prepare imports."""
import argparse,csv,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from urllib.parse import quote
HERE=Path(__file__).resolve().parent
SUPPORTED=('W02','W03','W04','W05','W06','W08','W09','W10','W11','W12','TEST1','TEST2','DA_PROJECT','ML_PROJECT','S09')
RESULT_FIELDS=['student_id','status','score','maximum']

def packet_plan(groups,assessment):
    valid={};invalid={}
    for sid,rows in groups.items():
        notebooks=[r for r in rows if Path(r['file']).suffix.lower()=='.ipynb']
        reports=[r for r in rows if Path(r['file']).suffix.lower() in ('.pdf','.docx')]
        if any(not Path(r['file']).is_file() for r in rows):invalid[sid]='A prepared attachment is missing; restore the original download.'
        elif len(notebooks)!=1:invalid[sid]='Submit exactly one notebook in the complete packet.'
        elif assessment=='W02' and not any(Path(r['file']).suffix.lower()=='.md' for r in rows):invalid[sid]='Include the README with the notebook in one complete response.'
        elif assessment=='S09' and len(reports)!=1:invalid[sid]='Include exactly one accessible PDF or DOCX cleaning log.'
        else:valid[sid]=rows
    return valid,invalid

def write_csv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('assessment','cohort','prepared','out'):p.add_argument('--'+k,required=True)
    p.add_argument('--calibration',help='Required for local reasoning marks')
    p.add_argument('--data-dir');p.add_argument('--variant',choices=['A','B','C'],default='A');p.add_argument('--model',help='Defaults to the model in the passing calibration report');a=p.parse_args()
    if a.assessment not in SUPPORTED:raise ValueError('No checked contract for assessment')
    if (a.assessment=='S09')!=(a.cohort=='DA'):raise ValueError('S09 belongs to the independent DA track; IUEA assessments use their engineering cohort')
    deterministic_only=a.assessment in ('W03','W04','W05')
    prepared=Path(a.prepared).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    rubric_path=HERE/'rubrics'/('W02.json' if a.assessment=='W02' else 'hybrid/'+a.assessment+'.json')
    from artifact_grade import validate_calibration,local_model_identity,group_manifest
    from registration import filename_id
    rubric=None;maximum=20;artifact_script=HERE/'artifact_grade.py'
    if not deterministic_only:
        if not a.calibration:raise ValueError('A passing current calibration report is required for reasoning marks')
        from calibration_record import model_for_report,profile_for_report
        if not a.model:a.model=model_for_report(a.calibration)
        rubric=json.loads(rubric_path.read_text());maximum=rubric.get('assessment_maximum',20 if a.assessment=='W02' else rubric['maximum'])
        if profile_for_report(a.calibration)=='reasoned':
            from reasoned_artifact_grade import load_backend
            validate_calibration=load_backend().validate_calibration
            artifact_script=HERE/'reasoned_artifact_grade.py'
        validate_calibration(a.calibration,rubric,local_model_identity(a.model),a.model)
    with (prepared/'manifest.csv').open() as f:groups=group_manifest(list(csv.DictReader(f)))
    if not groups:raise ValueError('No eligible submissions in manifest')
    valid,invalid=packet_plan(groups,a.assessment)
    if a.assessment=='S09':default_data=HERE.parents[1]/'DataAnalysis_Track/assessment_banks/S09'
    elif a.assessment=='W02':default_data=HERE.parent/'setup'/a.cohort
    elif deterministic_only:default_data=HERE.parent/'practicals'/a.assessment/a.cohort
    else:default_data=HERE.parent/'assessment_banks'/a.assessment/a.cohort/a.variant
    data=Path(a.data_dir).resolve() if a.data_dir else default_data
    if not data.is_dir():raise ValueError('No dataset for this cohort and variant')
    final_rows=[]
    if valid:
        with tempfile.TemporaryDirectory() as staging:
            for sid,rows in valid.items():
                notebook=next(Path(r['file']) for r in rows if Path(r['file']).suffix.lower()=='.ipynb')
                shutil.copyfile(notebook,Path(staging)/(filename_id(sid)+'_'+a.assessment+'.ipynb'))
            subprocess.run([sys.executable,str(HERE/'batch_grade.py'),'--assignment',a.assessment,'--cohort',a.cohort,'--notebooks',staging,'--out',str(out/'deterministic'),'--jobs','1','--data-dir',str(data)],check=True)
        if deterministic_only:
            with (out/'deterministic/results.csv').open() as f:
                final_rows=[dict(student_id=r['student_id'],status=r['status'],score=r['notebook_total'],maximum=r['max_total']) for r in csv.DictReader(f)]
        else:
            reasoning_rows=[r for rows in valid.values() for r in rows if a.assessment!='S09' or Path(r['file']).suffix.lower() in ('.pdf','.docx')]
            reasoning_manifest=out/'reasoning_manifest.csv';write_csv(reasoning_manifest,reasoning_rows,list(reasoning_rows[0]))
            subprocess.run([sys.executable,str(artifact_script),'--submissions',str(reasoning_manifest),'--rubric',str(rubric_path),'--calibration-report',a.calibration,'--deterministic-results',str(out/'deterministic/results.csv'),'--out',str(out/'combined'),'--model',a.model],check=True)
            with (out/'combined/results.csv').open() as f:final_rows=list(csv.DictReader(f))
    for sid,reason in invalid.items():
        result=dict(status='EXCEPTION',score=None,maximum=maximum,error=reason)
        final_rows.append(dict(student_id=sid,status='EXCEPTION',score='',maximum=maximum))
        if deterministic_only:
            folder=out/'deterministic/feedback';folder.mkdir(parents=True,exist_ok=True)
            (folder/(quote(sid,safe='')+'.txt')).write_text('Result pending; no final mark.\n'+reason+'\n')
        else:
            folder=out/'combined';folder.mkdir(parents=True,exist_ok=True)
            (folder/(quote(sid,safe='')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    if {r['student_id'] for r in final_rows}!=set(groups) or len(final_rows)!=len(groups):raise ValueError('Grading output does not match the prepared packet identities')
    write_csv(out/'results.csv',final_rows,RESULT_FIELDS)
    if not deterministic_only:
        write_csv(out/'combined/results.csv',final_rows,RESULT_FIELDS)
        subprocess.run([sys.executable,str(HERE/'export_feedback.py'),'--results',str(out/'combined'),'--rubric',str(rubric_path),'--out',str(out/'feedback')],check=True)
    subprocess.run([sys.executable,str(HERE/'prepare_grade_import.py'),str(out/'results.csv'),'--out',str(out/'import')],check=True)
    print(len(valid),'complete packets processed;',len(invalid),'incomplete packets remain pending')
if __name__=='__main__':main()
