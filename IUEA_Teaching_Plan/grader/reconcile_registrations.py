"""Evidence-based registration reconciliation; programme context never proves ownership."""
import collections
import hashlib
import json
import re
from pathlib import Path
import continuous_assessment as ca

# Lecturer-confirmed course composition. A course can contain multiple programmes.
COURSE_PROGRAMMES = {
    'CML3111': {'BSEE': 'Electrical Engineering', 'BSMRE': 'Robotics and Mechatronics'},
    'CML3112': {'BARC': 'Architecture', 'BSCE': 'Civil Engineering'},
    'CML3113': {'BSPE': 'Petroleum Engineering', 'BSME': 'Mining Engineering'},
}


def supported_typo_kind(original, target, course):
    """Suggest only narrow edits; callers must separately prove account/file support."""
    raw=canonical(original);normalized=re.sub(r'^UG/(\d{2,4})/',r'\1/UG/',raw)
    normalized=re.sub(r'^(\d{2,4})/GU/',r'\1/UG/',normalized)
    normalized=re.sub(r'/(?:UG/){2,}','/UG/',normalized)
    if normalized!=raw and normalized==canonical(target):return 'Misplaced or repeated UG segment'
    pattern = r'(\d{1,4})/(?:(UG|IG)/)?(\d+)/([A-Z]+)-([A-Z])'
    a, b = re.fullmatch(pattern, canonical(original)), re.fullmatch(pattern, canonical(target))
    if not a or not b or b[4] not in COURSE_PROGRAMMES.get(course, {}):return ''
    if a[3] != b[3] or a[5] != b[5]:return ''  # Never change serial digits or suffix.
    if a.groups()[:3]==b.groups()[:3] and a[4] not in COURSE_PROGRAMMES.get(course,{}):
        left,right=a[4],b[4]
        edits=(one_missing_letter(left,right) or one_missing_letter(right,left)
               or len(left)==len(right) and (sum(x!=y for x,y in zip(left,right))==1
                   or any(left[:i]+left[i+1]+left[i]+left[i+2:]==right for i in range(len(left)-1))))
        if edits:return 'Programme spelling typo'
    if a.groups()[:3] == b.groups()[:3] and len(a[4]) == len(b[4])+1:
        if any(a[4][i] == a[4][i-1] and a[4][:i]+a[4][i+1:] == b[4] for i in range(1,len(a[4]))):
            return 'Repeated programme letter'
    if a[1] == b[1] and a[4] == b[4] and a[2] == 'IG' and b[2] == 'UG':return 'IG/UG entry typo'
    if a[2] == b[2] and a[4] == b[4] and len(a[1]) == 1 and len(b[1]) == 2 and a[1] in b[1]:
        return 'Incomplete year (same submission must declare target)'
    return ''


def obvious_text_variant(original, target):
    """Non-numeric repairs against an observed, unique account registration."""
    raw=canonical(original);target=canonical(target)
    if raw==target:return ''
    if raw==target.replace('/','L'):return 'L entered instead of slash'
    if target in raw and re.fullmatch(r'[A-Z -]+',raw.replace(target,'',1)):
        return 'Name attached to complete registration'
    if raw==target.rsplit('-',1)[0]:return 'Missing suffix'
    if raw==re.sub(r'/\d+/(?=[A-Z]+-[A-Z]$)','/',target):return 'Missing serial component'
    if re.sub('[/-]','',raw)==re.sub('[/-]','',target)[:-1]:return 'Missing final suffix letter'
    return ''


def canonical(value):
    original = ca.norm(value)
    clean = re.sub("['’‘`\"“”]", '', original)
    punct=re.fullmatch(r'(\d{2,4})[/_.\\-](?:(UG)[/_.\\-])?(\d+)[/_.\\-]([A-Z]{2,12})[-/=]([A-Z])',clean)
    if punct:return '/'.join(x for x in (punct[1],punct[2],punct[3]) if x)+'/'+punct[4]+'-'+punct[5]
    joined=re.fullmatch(r'(\d{2,4}/(?:UG/)?\d+/)([A-Z]+)([A-Z])',clean)
    if joined and joined[2] in {code for codes in COURSE_PROGRAMMES.values() for code in codes}:
        return joined[1]+joined[2]+'-'+joined[3]
    # Only recognized registration shapes. Preserve every letter and digit.
    match = re.fullmatch(r'(\d{2,4}/(?:UG/)?\d+/)([A-Z]{2,12})[-/=]([A-Z])', clean)
    return ''.join((match[1], match[2], '-', match[3])) if match else original


def one_missing_letter(short, long):
    return len(long) == len(short)+1 and any(
        long[i].isalpha() and long[:i]+long[i+1:] == short for i in range(len(long)))


def read(path, default):
    return json.loads(path.read_text()) if path.is_file() else default


def reconcile(ledger, evidence, source, separator_only=False):
    """Keep raw receipts; reallocate supported scores and reapply identity/timing gates."""
    from recover_student_names import name_key, valid_name, compatible_name_keys
    source = Path(source)
    policy=read(Path(__file__).with_name('identity_policy_defaults.json'),{})
    policy.update(read(source.parent/'identity_policy.json',{}))
    # A lecturer can install updated private confirmations without restoring marks.
    live_policy=Path(__file__).resolve().parents[1]/'assessment_operations/private/identity_policy.json'
    policy.update(read(live_policy,{}))
    authoritative=policy.get('registration_authoritative',False) and not separator_only
    approved=policy.get('approved_aliases',{}) if not separator_only else {}
    def resolved(course,value):
        value=canonical(value)
        return approved.get(course,{}).get(value,value)
    rows = ledger['attempts']
    prior = {r['response_id']: (r['student_id'], r['status'], r.get('score')) for r in rows}
    verified = {}; notes = {}
    for r in rows:
        meta = read(source/r.get('source','missing'), {})
        hashes = {f['id']:f['sha256'] for f in meta.get('files', [])}
        verified[r['response_id']] = [p for p in evidence.get(r['response_id'], [])
            if p.get('file_id') in r.get('file_ids',[]) and hashes.get(p.get('file_id')) == p.get('sha256')]
        # Remove only identity holds added by the cumulative builder.
        if r['status'] in ('IDENTITY_CONFLICT','IDENTITY_MISSING') and 'source_status' in r:
            r['score'] = r.get('source_score'); r['status'] = r['source_status']
        r['student_id'] = resolved(r['cohort'],r['student_id'])
        if r['student_id']!=canonical(prior[r['response_id']][0]):notes[r['response_id']]='Lecturer-confirmed registration correction; original entry retained.'
    groups = collections.defaultdict(list); owners = collections.defaultdict(set)
    for r in rows:
        if r['email'] and r['student_id']:
            groups[(r['cohort'],r['email'])].append(r)
            owners[(r['cohort'],r['student_id'])].add(r['email'])
    # Recover omitted/misplaced separators only against an already submitted,
    # unambiguous registration. Never split a run of digits by guessing.
    compact=lambda value: re.sub(r"[\s/_=\-'’‘`\"“”]",'',str(value).upper())
    structured=collections.defaultdict(set)
    target_assessments=collections.defaultdict(set)
    for r in rows:
        sid=r['student_id']
        if re.fullmatch(r'\d{2,4}/(?:UG/)?\d+/[A-Z]{2,12}-[A-Z]',sid):
            structured[(r['cohort'],compact(sid))].add(sid)
            target_assessments[(r['cohort'],sid)].add(r['assessment'])
    for (course,email), account in groups.items():
        submitted={r['student_id'] for r in account}
        for r in account:
            sid=r['student_id']; candidates=structured[(course,compact(sid))]
            if len(candidates)!=1:continue
            target=next(iter(candidates))
            if target==sid or target not in submitted:continue
            family=[x for x in rows if x['cohort']==course and compact(x['student_id'])==compact(sid)]
            names={name_key(x['full_name']) for x in family if valid_name(x.get('full_name',''))}
            names|={name_key(p['name']) for x in family for p in verified[x['response_id']] if valid_name(p.get('name',''))}
            if len(target_assessments[(course,target)])<2 or not compatible_name_keys(names):
                notes[r['response_id']]='REVIEW: separator-only candidate lacks repeated target receipts or has conflicting names: '+target
                continue
            r['student_id']=target
            notes[r['response_id']]='Separator-only correction: identical letters and digits in the same order; same account also submitted the unique structured registration, repeated across assessments. Original retained.'
    # Rebuild ownership after formatting corrections; account conflicts are
    # still checked below before any held score can enter totals.
    owners=collections.defaultdict(set)
    for r in rows:
        if r['email'] and r['student_id']:owners[(r['cohort'],r['student_id'])].add(r['email'])
    for (course,email), account in groups.items():
        ids = {r['student_id'] for r in account}
        names = {name_key(r['full_name']) for r in account if valid_name(r.get('full_name',''))}
        names |= {name_key(p['name']) for r in account for p in verified[r['response_id']] if valid_name(p.get('name',''))}
        for sid in sorted(ids):
            targets = [] if separator_only else [t for t in ids if one_missing_letter(sid,t)]
            candidates = []
            for target in targets:
                target_rows = [r for r in account if r['student_id']==target]
                declarations = {p['sha256'] for r in target_rows for p in verified[r['response_id']]
                    if valid_name(p.get('name','')) and canonical_registration_in_header(target,p.get('header',''))}
                if names and compatible_name_keys(names) and len(declarations)>=2 and owners[(course,target)]=={email} and owners[(course,sid)]=={email}:
                    candidates.append(target)
            for r in account:
                if r['student_id'] != sid:continue
                if len(candidates)==1:
                    r['student_id']=candidates[0]
                    notes[r['response_id']]='Missing letter: same account and consistent name; target declared in two independently hashed submission files; no competing account.'
                elif targets:
                    notes[r['response_id']]='REVIEW: possible missing letter; insufficient or conflicting evidence. Candidate(s): '+', '.join(targets)
    # Programme-aware candidates still require the same account, compatible
    # author evidence and repeated hash-bound declarations. No cohort majority rule.
    supported_aliases = {}
    if not separator_only:
        for (course,email), account in groups.items():
            ids={r['student_id'] for r in account}
            names={name_key(r['full_name']) for r in account if valid_name(r.get('full_name',''))}
            names|={name_key(p['name']) for r in account for p in verified[r['response_id']] if valid_name(p.get('name',''))}
            declarations={r['response_id']:{canonical(x.get('registration','')) for p in verified[r['response_id']] for x in p.get('registrations',[])} for r in account}
            variants=ids|set().union(*declarations.values())
            for variant in sorted(variants):
                candidates=[]
                for target in sorted(ids):
                    kind=supported_typo_kind(variant,target,course)
                    if authoritative and not kind:kind=obvious_text_variant(variant,target)
                    if not kind or (not authoritative and not compatible_name_keys(names)):continue
                    if not authoritative and (owners[(course,target)]!={email} or owners.get((course,variant),{email})!={email}):continue
                    proof=[(r,p) for r in account for p in verified[r['response_id']]
                           if {canonical(x.get('registration','')) for x in p.get('registrations',[])}=={target}]
                    distinct_files=len({p['sha256'] for r,p in proof})
                    target_assessments={r['assessment'] for r in account if r['student_id']==target}
                    strong=distinct_files>=2 and len({r['assessment'] for r,p in proof})>=2
                    valid_ids={sid for sid in ids if re.fullmatch(r'\d{2,4}/(?:UG/)?\d+/[A-Z]+-[A-Z]',sid) and sid.rsplit('/',1)[-1].split('-')[0] in COURSE_PROGRAMMES.get(course,{})}
                    if authoritative and not kind.startswith('Incomplete year'):
                        strong=strong or (len(target_assessments)>=2 and distinct_files>=1) or (len(target_assessments)>=2 and (valid_ids=={target} or kind=='Programme spelling typo'))
                        if kind=='L entered instead of slash' and valid_ids=={target}:strong=True
                    if not strong:continue
                    if kind=='Missing serial component':
                        named_files={p['sha256'] for r in account for p in verified[r['response_id']] if valid_name(p.get('name',''))}
                        if not names or not compatible_name_keys(names) or len(named_files)<2 or distinct_files<2 or valid_ids!={target}:continue
                    affected=[r for r in account if r['student_id']==variant]
                    if kind.startswith('Incomplete year'):
                        if not affected or any(declarations[r['response_id']]!={target} for r in affected):continue
                    elif not names and not authoritative:continue
                    candidates.append((target,kind))
                if len(candidates)!=1:continue
                target,kind=candidates[0]
                supported_aliases[(course,email,variant)]=target
                for r in account:
                    if r['student_id']==variant or variant in declarations[r['response_id']]:
                        if r['student_id']==variant:r['student_id']=target
                        notes[r['response_id']]=kind+': lecturer-confirmed programme; same account; target declared in distinct files across assessments; no conflicting names or competing account. Original retained.'
                        if authoritative:notes[r['response_id']]=kind+': unique supported target on the same account, repeated across assessments and/or declared in original files. Numeric identity retained; original entry preserved.'
            # A name mistakenly entered in the registration field is recoverable
            # only from an exact submitted/lecturer-confirmed name and one target.
            if authoritative:
                targets={r['student_id'] for r in account if re.fullmatch(r'\d{2,4}/(?:UG/)?\d+/[A-Z]+-[A-Z]',r['student_id']) and r['student_id'].rsplit('/',1)[-1].split('-')[0] in COURSE_PROGRAMMES.get(course,{})}
                if len(targets)==1:
                    target=next(iter(targets));known_names={re.sub('[^A-Z]','',policy.get('confirmed_names',{}).get(course,{}).get(target,'').upper())}
                    known_names|={re.sub('[^A-Z]','',p.get('name','').upper()) for r in account for p in verified[r['response_id']] if any(resolved(course,x.get('registration',''))==target for x in p.get('registrations',[]))}
                    for r in account:
                        sid=r['student_id']
                        if re.fullmatch('[A-Z]+',sid) and sid in known_names and len({x['assessment'] for x in account if x['student_id']==target})>=2:
                            r['student_id']=target;notes[r['response_id']]='Name entered as registration: exact name confirmed in submission/lecturer evidence; sole valid registration repeatedly used by this account.'
    ca.recover_quiz_ids(rows)
    # Reuse only complete, hash-bound deterministic results; never manufacture a written mark.
    indexed = {}
    for relative in ('notebook_grades/results.json','notebook_grades/identity_checked_results.json','written_queue/combined_results.json'):
        for grade in read(source.parent/relative, []):
            if grade.get('record'): indexed[grade['response_id']]=grade
    def verified_grade(r,g):
        meta=read(source/r.get('source','missing'),{})
        files=[f for f in meta.get('files',[]) if f['id'] in r.get('file_ids',[])]
        hashes={f['id']:f['sha256'] for f in files}
        return (bool(hashes) and set(hashes)==set(r.get('file_ids',[])) and g.get('source_hashes')==hashes
                and g.get('cohort')==r['cohort'] and g.get('assessment')==r['assessment']
                and ca.norm(g.get('student_id'))==ca.norm(r.get('submitted_student_id',r['student_id']))
                and all((source/'files'/f['export_name']).is_file() and hashlib.sha256((source/'files'/f['export_name']).read_bytes()).hexdigest()==f['sha256'] for f in files))
    if authoritative and policy.get('prefer_notebook'):
        for r in rows:
            g=indexed.get(r['response_id'],{});declared=resolved(r['cohort'],g.get('record',{}).get('declared_sid',''))
            declared=supported_aliases.get((r['cohort'],r['email'],declared),declared)
            # Unchanged template text such as YOUR/ID is not a registration.
            if re.fullmatch(r'\d{2,4}/(?:UG/)?\d+/[A-Z]{2,12}-[A-Z]',declared) and verified_grade(r,g):
                if declared!=r['student_id']:
                    r['student_id']=declared
                    notes[r['response_id']]='Lecturer policy: hash-verified notebook registration overrides form registration. Original form entry retained.'
    aliases=collections.defaultdict(set)
    for r in rows:
        aliases[(r['cohort'],r['email'],canonical(r.get('submitted_student_id',r['student_id'])))].add(r['student_id'])
    for key,target in supported_aliases.items():aliases[key].add(target)
    for r in rows:
        if r['status']!='IDENTITY_MISMATCH' or r['assessment'] not in ('W02','W03','W04','W05'):continue
        g=indexed.get(r['response_id'],{}); record=g.get('record',{})
        meta=read(source/r.get('source','missing'),{})
        hashes={f['id']:f['sha256'] for f in meta.get('files',[]) if f['id'] in r.get('file_ids',[])}
        if not hashes or set(hashes)!=set(r.get('file_ids',[])) or g.get('source_hashes')!=hashes:continue
        if g.get('cohort')!=r['cohort'] or g.get('assessment')!=r['assessment']:continue
        if ca.norm(g.get('student_id'))!=ca.norm(r.get('submitted_student_id',r['student_id'])):continue
        if any(not (source/'files'/f['export_name']).is_file() or hashlib.sha256((source/'files'/f['export_name']).read_bytes()).hexdigest()!=f['sha256'] for f in meta.get('files',[]) if f['id'] in hashes):continue
        declared=resolved(r['cohort'],record.get('declared_sid'))
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
    conflicts={key for key,names in by_id.items() if not compatible_name_keys(names)}
    # Multiple accounts may belong to one learner, but require each account's
    # own independently hashed submission to state the same name and registration.
    accounts=collections.defaultdict(set); declarations=collections.defaultdict(list)
    for r in rows:
        key=(r['cohort'],r['student_id']);accounts[key].add(r['email'])
        for p in verified[r['response_id']]:
            declared={canonical(x.get('registration','')) for x in p.get('registrations',[])}
            if valid_name(p.get('name','')) and declared=={r['student_id']}:
                declarations[(key,r['email'])].append(p)
    supported_accounts=set()
    for key, emails in accounts.items():
        if len(emails)<2 or '' in emails or key in conflicts:continue
        per_account=[declarations[(key,email)] for email in emails]
        if not all(per_account):continue
        all_evidence=[p for group in per_account for p in group]
        if len({name_key(p['name']) for p in all_evidence})!=1:continue
        if any(not {p['sha256'] for p in group}-{p['sha256'] for other in per_account if other is not group for p in other} for group in per_account):continue
        supported_accounts.add(key)
        for r in rows:
            if (r['cohort'],r['student_id'])==key:
                notes[r['response_id']]='Each account submitted distinct file evidence declaring the same full name and registration; no conflicting names.'
    if authoritative:
        # Account ownership and display-name uncertainty do not block marks.
        # Malformed/unknown programme identifiers still require an explicit target.
        conflicts=set()
        known_programmes={code for codes in COURSE_PROGRAMMES.values() for code in codes}
        previously_graded={(r['cohort'],resolved(r['cohort'],prior[r['response_id']][0])) for r in rows if prior[r['response_id']][1]=='GRADED'}
        for r in rows:
            sid=r['student_id'];m=re.fullmatch(r'\d{2,4}/(?:UG/)?\d+/([A-Z]+)-[A-Z]',sid)
            if sid and (not m or m[1] not in known_programmes) and (r['cohort'],sid) not in previously_graded:
                conflicts.add((r['cohort'],sid))
                notes[r['response_id']]='REVIEW: registration needs a confirmed target; no programme or suffix guessed.'
            elif sid:notes.setdefault(r['response_id'],'Lecturer policy: marks allocated by Student Registration Number across accounts; name uncertainty does not withhold marks.')
            name=policy.get('confirmed_names',{}).get(r['cohort'],{}).get(sid)
            if name:r['full_name']=name
    rebuilt=ca.finalize(rows,ledger.get('sources',[]),conflicts,supported_accounts,registration_authoritative=authoritative)
    ledger.update(rebuilt)
    if authoritative:ledger['identity_allocation_policy']='registration_first_notebook_precedence'
    audit=[]
    for r in rows:
        old_id, old_status, old_score=prior[r['response_id']]
        raw=r.get('submitted_student_id',old_id)
        reason=notes.get(r['response_id'],'')
        if (r['cohort'],r['student_id']) in conflicts:reason+=' Unresolved identity: lecturer review required.'
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
