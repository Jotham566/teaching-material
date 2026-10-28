/* Local deterministic control simulator. No model, URA connection or external action. */
(function(root){
class Workflow {
 constructor(){this.approval=null;this.log=[];this.calls=0;this.limit=3;this.spent=0;this.budget=2.5;this.unitCost=1;this.completed=new Map();this.uncertain=null;}
 snapshot(v){return JSON.stringify({case:v.case,period:v.period,recipient:v.recipient,records:v.records,evidence:v.evidence});}
 prepare(v){
  if(v.case!=='M-01'||!/^\d{4}-\d{2}$/.test(v.period))return {state:'HELD',reason:'Check case and period.'};
  if(v.recipient!=='Internal partner')return {state:'HELD',reason:'Recipient is outside the allowed route.'};
  if(!v.evidence)return {state:'HELD',reason:'Required evidence has not been checked.'};
  if(!Array.isArray(v.records)||!v.records.length)return {state:'HELD',reason:'Source records missing.'};
  let seen=new Map(),net=0,duplicates=[];
  for(const r of v.records){
   if(!r.id||!['invoice','credit'].includes(r.kind)||!Number.isFinite(r.amount)||r.amount<0)return {state:'HELD',reason:'Invalid source row.'};
   if(r.period!==v.period)continue;
   const key=r.kind+':'+r.id;
   if(seen.has(key)){if(JSON.stringify(seen.get(key))!==JSON.stringify(r))return {state:'HELD',reason:'Conflicting duplicate needs review.'};duplicates.push(key);continue;}
   seen.set(key,r);net+=r.kind==='credit'?-r.amount:r.amount;
  }
  if(!seen.size)return {state:'HELD',reason:'No source records match the selected period.'};
  if(net<0)return {state:'HELD',reason:'Negative net needs review.'};
  return {state:'READY',net,duplicates,snapshot:this.snapshot(v)};
 }
 approve(v){const p=this.prepare(v);if(p.state!=='READY')return p;this.approval=p.snapshot;this.log.push('Approved exact local snapshot');return {...p,state:'APPROVED'};}
 decline(){this.approval=null;this.log.push('Reviewer declined');return {state:'STOPPED',reason:'Dependent action held.'};}
 run(v,timeout=false){
  const p=this.prepare(v);if(p.state!=='READY')return p;
  if(this.uncertain)return {state:'HELD',reason:'Inspect uncertain status before retry.'};
  if(this.approval!==p.snapshot)return {state:'HELD',reason:'No current approval for these fields.'};
  if(this.completed.has(p.snapshot))return {state:'DUPLICATE PREVENTED',ack:this.completed.get(p.snapshot)};
  if(this.calls>=this.limit)return {state:'HELD',reason:'Local call budget exhausted.'};
  if(this.spent+this.unitCost>this.budget)return {state:'HELD',reason:'Illustrative spend budget exhausted.'};
  this.calls++;this.spent+=this.unitCost;const ack='LOCAL-'+this.calls;this.completed.set(p.snapshot,ack);this.approval=null;
  this.log.push('Local mock '+ack+'; net '+p.net);
  if(timeout){this.uncertain=p.snapshot;return {state:'UNCERTAIN',reason:'Local mock ran but acknowledgement was withheld. Inspect status.'};}
  return {state:'MOCK ACKNOWLEDGED',ack,net:p.net};
 }
 inspect(){if(!this.uncertain)return {state:'STATUS CHECKED',reason:'No uncertain local action.'};const ack=this.completed.get(this.uncertain);this.uncertain=null;return {state:'STATUS CHECKED',ack,reason:'Local action already recorded; do not repeat.'};}
}
if(typeof module!=='undefined')module.exports={Workflow};root.Workflow=Workflow;
})(typeof globalThis!=='undefined'?globalThis:window);
