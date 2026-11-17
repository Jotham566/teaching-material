"""Run in the pinned teaching Docker image; emit trusted reference predictions."""
import argparse,json,sys
sys.path.insert(0,'/ref')
from engineering_contracts import dataset,DOMAINS
from engineering_reference import predict_regression,ablation_metrics
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--task",choices=["regression","ablation"],default="regression")
args=parser.parse_args()
out={}
for cohort in DOMAINS:
 for seed in (71,113):
  training=dataset(cohort,seed,90);held=dataset(cohort,seed+300,18)
  features=[{k:v for k,v in r.items() if k!='target'} for r in held]
  out[cohort+'|'+str(seed)]=(predict_regression(training,features) if args.task=='regression' else ablation_metrics(training,held))
print(json.dumps(out,sort_keys=True))
