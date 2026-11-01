"""Record lecturer-verified identity decisions in the private identity policy.

  confirm_identity.py alias CML3113 '24/925/BSPE-S' '24/925/BSPE-J'   # a mistyped registration
  confirm_identity.py release RESPONSE_ID                             # accept a held notebook receipt

The policy file is private and survives regrades. Rerun reconcile-identities afterwards.
"""
import json
import sys
from pathlib import Path
from reconcile_registrations import canonical

POLICY=Path(__file__).resolve().parents[1]/'assessment_operations/private/identity_policy.json'


def load():return json.loads(POLICY.read_text()) if POLICY.is_file() else {}


def save(policy):
    POLICY.parent.mkdir(parents=True,exist_ok=True)
    POLICY.write_text(json.dumps(policy,indent=2,ensure_ascii=False)+'\n')


def alias(course,wrong,right):
    policy=load();target=canonical(right)
    if not target or target==canonical(wrong):raise SystemExit('Nothing to change')
    policy.setdefault('approved_aliases',{}).setdefault(course,{})[canonical(wrong)]=target
    save(policy);print(f'{course}: {canonical(wrong)} -> {target}')


def release(response_id):
    policy=load();ids=policy.setdefault('confirmed_responses',[])
    if response_id not in ids:ids.append(response_id)
    save(policy);print('Confirmed receipt',response_id[-12:])


if __name__=='__main__':
    a=sys.argv[1:]
    if len(a)==4 and a[0]=='alias':alias(*a[1:])
    elif len(a)==2 and a[0]=='release':release(a[1])
    else:raise SystemExit(__doc__)
