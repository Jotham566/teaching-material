"""Evidence-based registration reconciliation; never infer degree from course group."""
import collections
import hashlib
import json
import re
from pathlib import Path
import continuous_assessment as ca


def canonical(value):
    original = ca.norm(value)
    clean = re.sub("['’‘`\"“”]", '', original)
    # Only recognized registration shapes. Preserve every letter and digit.
    match = re.fullmatch(r'(\d{2,4}/(?:UG/)?\d+/)([A-Z]{2,12})[-/]([A-Z])', clean)
    return ''.join((match[1], match[2], '-', match[3])) if match else original


def one_missing_letter(short, long):
    return len(long) == len(short)+1 and any(
        long[i].isalpha() and long[:i]+long[i+1:] == short for i in range(len(long)))


def read(path, default):
    return json.loads(path.read_text()) if path.is_file() else default


def reconcile(ledger, evidence, source):
    """Keep raw receipts; reallocate supported scores and reapply identity/timing gates."""
    from recover_student_names import name_key, valid_name
    source = Path(source)
    rows = ledger['attempts']
    prior = {r['response_id']: (r['student_id'], r['status'], r.get('score')) for r in rows}
    verified = {}
    for r in rows:
        meta = read(source/r.get('source','missing'), {})
        hashes = {f['id']:f['sha256'] for f in meta.get('files', [])}
        verified[r['response_id']] = [p for p in evidence.get(r['response_id'], [])
            if p.get('file_id') in r.get('file_ids',[]) and hashes.get(p.get('file_id')) == p.get('sha256')]
        # Remove only identity holds added by the cumulative builder.
        if r['status'] in ('IDENTITY_CONFLICT','IDENTITY_MISSING') and 'source_status' in r:
            r['score'] = r.get('source_score'); r['status'] = r['source_status']
        r['student_id'] = canonical(r['student_id'])
    groups = collections.defaultdict(list); owners = collections.defaultdict(set)
    for r in rows:
        if r['email'] and r['student_id']:
            groups[(r['cohort'],r['email'])].append(r)
            owners[(r['cohort'],r['student_id'])].add(r['email'])
    notes = {}
    for (course,email), account in groups.items():
        ids = {r['student_id'] for r in account}
        names = {name_key(r['full_name']) for r in account if valid_name(r.get('full_name',''))}
        names |= {name_key(p['name']) for r in account for p in verified[r['response_id']] if valid_name(p.get('name',''))}
        for sid in sorted(ids):
            targets = [t for t in ids if one_missing_letter(sid,t)]
            candidates = []
            for target in targets:
                target_rows = [r for r in account if r['student_id']==target]
                declarations = {p['sha256'] for r in target_rows for p in verified[r['response_id']]
                    if valid_name(p.get('name','')) and canonical_registration_in_header(target,p.get('header',''))}
                if len(names)==1 and len(declarations)>=2 and owners[(course,target)]=={email} and owners[(course,sid)]=={email}:
                    candidates.append(target)
            for r in account:
                if r['student_id'] != sid:continue
                if len(candidates)==1:
                    r['student_id']=candidates[0]
                    notes[r['response_id']]='Missing letter: same account and consistent name; target declared in two independently hashed submission files; no competing account.'
                elif targets:
                    notes[r['response_id']]='REVIEW: possible missing letter; insufficient or conflicting evidence. Candidate(s): '+', '.join(targets)
    ca.recover_quiz_ids(rows)
    # Reuse only complete, hash-bound deterministic results; never manufacture a written mark.
    indexed = {}
    for relative in ('notebook_grades/results.json','notebook_grades/identity_checked_results.json','written_queue/combined_results.json'):
        for grade in read(source.parent/relative, []):
            if grade.get('record'): indexed[grade['response_id']]=grade
    aliases=collections.defaultdict(set)
    for r in rows:
        aliases[(r['cohort'],r['email'],canonical(r.get('submitted_student_id',r['student_id'])))].add(r['student_id'])
    for r in rows:
        if r['status']!='IDENTITY_MISMATCH' or r['assessment'] not in ('W02','W03','W04','W05'):continue
        g=indexed.get(r['response_id'],{}); record=g.get('record',{})
        meta=read(source/r.get('source','missing'),{})
        hashes={f['id']:f['sha256'] for f in meta.get('files',[]) if f['id'] in r.get('file_ids',[])}
        if not hashes or set(hashes)!=set(r.get('file_ids',[])) or g.get('source_hashes')!=hashes:continue
        if g.get('cohort')!=r['cohort'] or g.get('assessment')!=r['assessment']:continue
        if ca.norm(g.get('student_id'))!=ca.norm(r.get('submitted_student_id',r['student_id'])):continue
        if any(not (source/'files'/f['export_name']).is_file() or hashlib.sha256((source/'files'/f['export_name']).read_bytes()).hexdigest()!=f['sha256'] for f in meta.get('files',[]) if f['id'] in hashes):continue
        declared=canonical(record.get('declared_sid'))
        accepted=declared==r['student_id'] or aliases.get((r['cohort'],r['email'],declared))=={r['student_id']}
        if not declared or not accepted or record.get('cell_errors'):continue
        questions=record.get('questions',{}); maximum=14 if r['assessment']=='W02' else 20
        if not questions or any(q.get('err') for q in questions.values()):continue
        if any(type(q.get('marks')) not in (int,float) or type(q.get('awarded')) not in (int,float) or not 0<=q['awarded']<=q['marks'] for q in questions.values()):continue
        if sum(q['marks'] for q in questions.values())!=maximum:continue
        total=sum(q['awarded'] for q in questions.values())
        r.update(code_score=total,code_maximum=maximum,score=total if maximum==20 else None,
                 status='GRADED' if maximum==20 else 'PARTIAL_CODE_ONLY')
    # Even matching registrations must not conceal contradictory author names.
    by_id=collections.defaultdict(set)
    for r in rows:
        key=(r['cohort'],r['student_id'])
        if valid_name(r.get('full_name','')):by_id[key].add(name_key(r['full_name']))
        by_id[key].update(name_key(p['name']) for p in verified[r['response_id']] if valid_name(p.get('name','')))
    conflicts={key for key,names in by_id.items() if len(names)>1}
    rebuilt=ca.finalize(rows,ledger.get('sources',[]),conflicts)
    ledger.update(rebuilt)
    audit=[]
    for r in rows:
        old_id, old_status, old_score=prior[r['response_id']]
        raw=r.get('submitted_student_id',old_id)
        reason=notes.get(r['response_id'],'')
        if (r['cohort'],r['student_id']) in conflicts:reason+=' Conflicting names: lecturer review required.'
        changed=raw!=r['student_id']
        if changed or reason or old_status!=r['status']:
            r['identity_evidence']=reason or ('Formatting normalized; original preserved.' if canonical(raw)==r['student_id'] else r.get('identity_evidence','Supported registration correction.'))
            audit.append(dict(response_id=r['response_id'],cohort=r['cohort'],email=r['email'],
                original=raw,student_id=r['student_id'],previous_id=old_id,
                previous_status=old_status,status=r['status'],previous_score=old_score,score=r.get('score'),
                decision='REVIEW' if 'REVIEW' in reason or r['status'].startswith('IDENTITY_') else 'SUPPORTED',
                reason=reason or ('Formatting normalized without changing letters or digits.' if canonical(raw)==r['student_id'] else r.get('identity_evidence','Existing supported registration correction.'))))
    ledger['registration_reconciliation']=audit
    return ledger


def canonical_registration_in_header(target, header):
    return any(canonical(token.strip('.,;:()[]'))==target for token in header.upper().split())
