"""Run the documented classroom demonstrations. Outputs go outside the course by default.
No installation, account creation, publication, external action or real client data is performed.
"""
import argparse,csv,datetime,json,os,shutil,subprocess,sys,re,hashlib
from pathlib import Path
from decimal import Decimal
P=Path(__file__).resolve().parent
R=P.parents[1]
TR=R/'04 Facilitator Materials/Teaching Resources'
BUNDLED=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies'
PY=BUNDLED/'python/bin/python3'
EMB=Path.home()/'.cache/klai-course/embedding-venv/bin/python'
NODE=BUNDLED/'node/bin/node'
D=P/'02 Data and Retrieval';T=P/'04 Automation and Tax'
ACTIONS={
'preflight':'Check files and the teaching Mac runtimes without calling any account.',
's02_vectors':'Run the real embedding self-test and save its measured vectors/similarities.',
's05_ocr':'Read the three existing images with local Apple Vision OCR; originals remain untouched.',
's06_baseline':'Reproduce the historical lexical fixture result, including its expected failures.',
's06_reviewed':'Run all 19 repaired retrieval checks with cached models.',
's06_query':'Retrieve the selected current agreement and its amendment context.',
's06_missing':'Request an unavailable agreement; no substitute source should be returned.',
's09_host':'Run seven scripted host-enforcement tests; no model call.',
's09_protocol':'Run three scripted malformed/ungrounded-reply tests; no model call.',
's09_agent':'Make a real read-only model-selected lookup using the existing Claude CLI account.',
's09_injection':'Run the same model-selected task with the fictional injected note.',
's09_unknown':'Ask the model for unavailable CONTRACT-99; do not substitute CONTRACT-01.',
's09_onecall':'Give the model a one-lookup budget; a refusal is not guaranteed to be exercised.',
's10_reconcile':'Independently calculate the small and larger fictional reconciliations.',
's10_controls':'Exercise local approval, stale approval, decline, recipient, retry and budget controls.',
's11_ocr_ladder':'Read 12 prepared images for three selected passages with Apple Vision; historical Tesseract output is separate.',
's12_costs':'Independently calculate the fictional main and stress cost scenarios.'}
def rows(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def child(cmd,out,name,cwd=None,timeout=180):
    proc=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,cwd=cwd,timeout=timeout)
    (out/(name+'.txt')).write_text(proc.stdout+proc.stderr,encoding='utf8')
    print(proc.stdout,end='');print(proc.stderr,end='',file=sys.stderr)
    return proc

def reconcile():
    inv=rows(T/'Invoice Import.csv');unique={}
    for r in inv:
        k=r['invoice_id']
        if k in unique and unique[k]!=r:raise ValueError('Conflicting invoice requires review')
        unique[k]=r
    imported=sum(int(r['amount_ugx']) for r in inv);gross=sum(int(r['amount_ugx']) for r in unique.values());credits=sum(int(r['amount_ugx']) for r in rows(T/'Credit Notes.csv'));receipts=sum(int(r['amount_ugx']) for r in rows(T/'Receipts.csv') if r['period']=='2026-09')
    small=dict(imported=imported,duplicate_difference=imported-gross,unique_invoices=gross,credits=credits,net=gross-credits,receipts=receipts,teaching_outstanding=gross-credits-receipts)
    allrows=rows(T/'Ledger Challenge.csv');iv=[r for r in allrows if r['kind']=='invoice' and r['period']=='2026-09'];u={};dups=[]
    for r in iv:
        k=r['record_id']
        if k in u:
            if u[k]!=r:raise ValueError('Conflicting challenge invoice requires review')
            dups.append(k)
        u[k]=r
    g=sum(int(r['amount_ugx']) for r in u.values());cr=sum(int(r['amount_ugx']) for r in allrows if r['kind']=='credit' and r['period']=='2026-09');rc=sum(int(r['amount_ugx']) for r in allrows if r['kind']=='receipt' and r['period']=='2026-09')
    large=dict(imported=sum(int(r['amount_ugx']) for r in iv),unique_invoices=g,duplicate_ids=dups,credits=cr,net=g-cr,september_receipts=rc,teaching_outstanding=g-cr-rc,missing_unique_invoice_support=sum(not r['support_reference'].strip() for r in u.values()))
    assert small['net']==98000000 and small['teaching_outstanding']==18000000
    assert large['net']==58650000 and large['teaching_outstanding']==28650000
    return dict(kind='deterministic classroom calculation, not an AI output or tax assessment',small=small,larger=large)

def costs():
    d={r['item']:Decimal(r['assumed_value']) for r in rows(P/'05 Firm Adoption/Cost and Effort Example.csv')}
    calc=lambda m:d['tasks_per_month']*m*d['reviewer_hourly_cost']/60
    manual=calc(d['manual_minutes_per_task']);main=calc(d['assisted_minutes_per_task']);stress=calc(d['stress_assisted_minutes']);tool=d['subscription']+d['usage']+d['maintenance'];benefit=manual-main-tool
    values=dict(manual_monthly_UGX=manual,main_monthly_review_UGX=main,stress_monthly_review_UGX=stress,tool_monthly_UGX=tool,main_effect_UGX=benefit,stress_effect_UGX=manual-stress-tool,illustrative_setup_payback_months=d['setup']/benefit,input_output_tokens_USD_per_task=d['input_tokens_per_task']/1000000*d['input_rate']+d['output_tokens_per_task']/1000000*d['output_rate'])
    assert benefit==160000 and values['stress_effect_UGX']==-360000
    return dict(kind='fictional planning arithmetic, not vendor pricing or guaranteed savings',values={k:format(v.quantize(Decimal('0.000001')), 'f').rstrip('0').rstrip('.') for k,v in values.items()})

def native_ocr(demo,out):
    swift=shutil.which('swift')
    if not swift:raise SystemExit('Swift runtime is missing. Use the named saved OCR route in the Guide; do not call it a live extraction.')
    images=[D/n for n in ['Original Source.png','Synthetic Scan.png','Degraded Scan - moderate.png']] if demo=='s05_ocr' else sorted((D/'OCR Experiment/images').glob('p*_*.png'))
    if demo=='s11_ocr_ladder' and len(images)!=12:raise ValueError('Expected 12 prepared images for passages 1, 2 and 6')
    result=child([swift,'-suppress-warnings',P/'facilitator_ocr.swift',*images],out,'Apple Vision Raw',timeout=240)
    if result.returncode:return result.returncode
    raw=json.loads(result.stdout)
    if any(x['error'] is not None for x in raw['images']):raise ValueError('An OCR image failed; inspect the raw record and use the saved route.')
    for item in raw['images']:
        f=Path(item['file']);(out/(f.stem+'.txt')).write_text(item['text']+'\n')
        item['source_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'Apple Vision OCR.json').write_text(json.dumps(raw,indent=2)+'\n')
    if demo=='s11_ocr_ladder':
        blocks=[b.strip().replace('\n',' ') for b in (D/'OCR Experiment/passages.txt').read_text().split('\n\n') if b.strip()]
        def words(t):return re.findall(r"[A-Za-z0-9’'\-\.]+",t.lower())
        def edit(a,b):
            previous=list(range(len(b)+1))
            for i,x in enumerate(a,1):
                current=[i]
                for j,y in enumerate(b,1):current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(x!=y)))
                previous=current
            return previous[-1]
        neg=re.compile(r'\b(not|no|never|neither|nor|without|except|unless|cannot|shall not|may not)\b',re.I);rows_=[]
        for item in raw['images']:
            name=Path(item['file']).stem;passage=int(name[1:3]);condition=name[4:];ref=blocks[passage-1];negs=[m.group(0).lower() for m in neg.finditer(ref)];kept=sum(bool(re.search(r'\b'+re.escape(n)+r'\b',item['text'],re.I)) for n in negs);errors=edit(words(ref),words(item['text']))
            rows_.append(dict(passage=passage,condition=condition,word_accuracy=round(max(0,1-errors/max(1,len(words(ref)))),3),negations_in_source=len(negs),negations_kept=kept,ocr_text=item['text']))
        with (out/'Quality Results.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows_[0]));w.writeheader();w.writerows(rows_)
        summary=['ACTUAL APPLE VISION RUN | '+raw['configuration'],'Uses 12 prepared images: three selected passages under four conditions. Historical Tesseract results cover twelve passages; do not rank engines across different samples.']
        for condition in sorted({x['condition'] for x in rows_}):
            rs=[x for x in rows_ if x['condition']==condition];summary.append(f"{condition}: mean word accuracy {sum(x['word_accuracy'] for x in rs)/len(rs):.1%}; negations kept {sum(x['negations_kept'] for x in rs)} of {sum(x['negations_in_source'] for x in rs)}")
        text='\n'.join(summary)+'\n';(out/'OCR Quality Summary.txt').write_text(text);print(text)
    return 0

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('demo',choices=ACTIONS,nargs='?',default='preflight');p.add_argument('--list',action='store_true');p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.list:
        for k,v in ACTIONS.items():print(k+' : '+v)
        return 0
    out=a.output_dir or Path.home()/'Downloads/KLAi Demo Runs'/datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')/a.demo
    out.mkdir(parents=True,exist_ok=True);print('DEMO:',a.demo,'\nOUTPUT:',out,'\n'+ACTIONS[a.demo],flush=True)
    metadata=dict(demo=a.demo,date=datetime.datetime.now().astimezone().isoformat(),description=ACTIONS[a.demo],output_directory=str(out));(out/'Run Record.json').write_text(json.dumps(metadata,indent=2)+'\n')
    if a.demo=='preflight':
        checks={'bundled Python':str(PY) if PY.exists() else 'MISSING','embedding Python':str(EMB) if EMB.exists() else 'MISSING','Node':str(NODE) if NODE.exists() else 'MISSING','Apple Vision Swift runner':shutil.which('swift') or 'MISSING','Claude CLI':shutil.which('claude') or 'MISSING','guide':str(R/'04 Facilitator Materials/Facilitator Guide.docx'),'prompt folder':str(TR/'Demo Materials')}
        print(json.dumps(checks,indent=2));(out/'Preflight.json').write_text(json.dumps(checks,indent=2));return 0
    if a.demo in ('s10_reconcile','s12_costs'):
        result=reconcile() if a.demo=='s10_reconcile' else costs();text=json.dumps(result,indent=2);print(text);(out/'Result.json').write_text(text+'\n');return 0
    if a.demo in ('s05_ocr','s11_ocr_ladder'):
        return native_ocr(a.demo,out)
    if a.demo=='s10_controls':
        code=r'''const {Workflow}=require(process.argv[1]);let checks=[];function test(name,got,want){checks.push({name,got,want,pass:got===want})}function input(){return {case:'M-01',period:'2026-09',recipient:'Internal partner',evidence:true,records:[{kind:'invoice',id:'A',period:'2026-09',amount:100}]}}let w=new Workflow(),v=input();test('missing evidence',w.prepare({...v,evidence:false}).state,'HELD');test('prepare',w.prepare(v).state,'READY');test('approve',w.approve(v).state,'APPROVED');let changed={...v,records:[{...v.records[0],amount:101}]};test('stale approval',w.run(changed).state,'HELD');w.approve(v);w.decline();test('decline stops action',w.run(v).state,'HELD');test('recipient held',w.prepare({...v,recipient:'New external recipient'}).state,'HELD');w=new Workflow();w.approve(v);test('withheld acknowledgement',w.run(v,true).state,'UNCERTAIN');test('blind retry held',w.run(v).state,'HELD');test('status checked',w.inspect().state,'STATUS CHECKED');w.approve(v);test('same snapshot not repeated',w.run(v).state,'DUPLICATE PREVENTED');w=new Workflow();for(let i=1;i<=2;i++){v={...input(),records:[{...input().records[0],amount:100+i}]};w.approve(v);w.run(v)}v={...input(),records:[{...input().records[0],amount:103}]};w.approve(v);test('spend budget',w.run(v).reason,'Illustrative spend budget exhausted.');w=new Workflow();w.limit=0;w.approve(input());test('call budget',w.run(input()).reason,'Local call budget exhausted.');console.log(JSON.stringify({kind:'scripted local engine tests, no model or external action',checks},null,2));if(checks.some(x=>!x.pass))process.exit(1);'''
        return child([NODE,'-e',code,T/'workflow_engine.js'],out,a.demo).returncode
    if not PY.exists():raise SystemExit('Bundled Python missing. See the guide setup and use the saved route for class.')
    if a.demo in ('s02_vectors','s06_reviewed','s06_query','s06_missing'):
        if not EMB.exists():raise SystemExit('Embedding environment missing; use the saved route and complete setup before class.')
        if a.demo=='s02_vectors':cmd=[EMB,D/'embedding_selftest.py','--save',out/'Embedding Selftest.txt']
        elif a.demo=='s06_reviewed':cmd=[EMB,D/'test_reviewed_retrieval.py','--output',out/'Retrieval Tests.json']
        else:cmd=[EMB,D/'reviewed_retrieval.py','Is consent required?', '--source-id','UNAVAILABLE-ID' if a.demo=='s06_missing' else 'CONTRACT-01','--offline']
        return child(cmd,out,a.demo,cwd=D).returncode
    if a.demo=='s06_baseline':
        r=child([PY,D/'run_retrieval_tests.py','--method','lexical'],out,a.demo,cwd=D)
        # This is intentionally the preserved failing baseline, not the repaired route.
        return 0 if 'K3 FAIL' in r.stdout and 'K8 FAIL' in r.stdout else 1
    if a.demo=='s09_host':return child([PY,T/'host_control_tests.py',D],out,a.demo).returncode
    if a.demo=='s09_protocol':return child([PY,T/'test_agent_protocol.py'],out,a.demo).returncode
    cli=shutil.which('claude')
    if not cli:raise SystemExit('Claude CLI missing. Use the saved model-selected trace; host tests still run without an account.')
    extra=[]
    if a.demo=='s09_injection':extra=['--injection']
    elif a.demo=='s09_onecall':extra=['--max-calls','1']
    elif a.demo=='s09_unknown':extra=['--task','Review CONTRACT-99 in M-01. Do not substitute CONTRACT-01. If the source is unavailable, ask for it.']
    return child([PY,T/'read_only_agent.py',D,'--cli',cli,'--output',out/'Agent Trace.json']+extra,out,a.demo,timeout=300).returncode
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,subprocess.TimeoutExpired) as e:print('STOP:',e,file=sys.stderr);raise SystemExit(1)
