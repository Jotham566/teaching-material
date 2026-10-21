import fs from 'node:fs/promises';
import path from 'node:path';

const reasons={
 GRADED:'The complete source mark is retained until the identity issue is resolved.',
 IDENTITY_CONFLICT:'The account and registration histories still conflict. Compare the related identities before allocating the retained mark.',
 IDENTITY_MISSING:'The submission lacks an email or Student Registration Number.',
 IDENTITY_MISMATCH:'The notebook declares a different registration from the submission form.',
 WRITTEN_REVIEW:'The two grading passes disagree or raise a concern. Review the written evidence against the rubric.',
 WRITTEN_ERROR:'Written grading could not complete. See the processing detail.',
 TEXT_EXTRACTION_PENDING:'One or more attachments could not be read reliably.',
 README_OR_NOTEBOOK_MISSING:'A2 requires a notebook and a README. The expected pair was not found.',
 NOTEBOOK_MISSING_OR_AMBIGUOUS:'No single .ipynb notebook was found among the uploaded files.',
 EMPTY_NOTEBOOK:'The uploaded notebook is empty (zero bytes).',
 INVALID_NOTEBOOK:'The uploaded file is not a readable notebook.',
 TIMING_REVIEW:'The receipt is outside a verified submission window or its timing remains unresolved.',
 AWAITING_GRADING:'This receipt has not yet received a complete grade.',
 PARTIAL_CODE_ONLY:'The coding component is available; the written component is not yet final.'
};
async function optionalJson(file,fallback){try{return JSON.parse(await fs.readFile(file,'utf8'));}catch(e){if(e.code==='ENOENT')return fallback;throw e;}}
export async function reviewDetails(data,base){
 const grades=new Map((await optionalJson(path.join(base,'written_queue/combined_results.json'),[])).map(r=>[r.response_id,r]));
 const prepared=await optionalJson(path.join(base,'written_text/prepared.json'),{});
 const coding=new Map([
  ...await optionalJson(path.join(base,'notebook_grades/identity_checked_results.json'),[]),
  ...await optionalJson(path.join(base,'refresh_20261021/coding/results.json'),[])
 ].map(r=>[r.response_id,r]));
 const manifests=new Map();
 for(const name of new Set(data.current.map(r=>r.source))){
  if(path.basename(name)!==name)throw Error('Invalid source filename');
  manifests.set(name,await optionalJson(path.join(base,'reconciled',name),{}));
 }
 return data.current.filter(r=>r.status!=='GRADED').map(r=>{
  const g=grades.get(r.response_id)||{},meta=manifests.get(r.source)||{};
  const evaluations=g.evidence?.evaluations||[];
  const notes=[g.error,...(prepared[r.response_id]?.errors||[]).map(x=>x.error),
    ...evaluations.flatMap((e,i)=>(e.concerns||[]).map(c=>`Pass ${i+1}: ${typeof c==='string'?c:JSON.stringify(c)}`))].filter(Boolean);
  const scores=evaluations.map((e,i)=>`Pass ${i+1}: ${(e.criteria||[]).map(c=>`${c.id} ${c.awarded}`).join('; ')}`).join('\n');
  const relatedIds=[...new Set(data.attempts.filter(x=>x.cohort===r.cohort&&r.email&&x.email===r.email).map(x=>x.student_id))].filter(x=>x&&x!==r.student_id);
  const relatedEmails=[...new Set(data.attempts.filter(x=>x.cohort===r.cohort&&r.student_id&&x.student_id===r.student_id).map(x=>x.email))].filter(x=>x&&x!==r.email);
  const files=(r.file_ids||[]).map(id=>{
   if(!/^[A-Za-z0-9_-]+$/.test(id))throw Error('Invalid Drive file ID');
   const f=(meta.files||[]).find(x=>x.id===id);
   return {name:f?.original_name||id,url:`https://drive.google.com/file/d/${id}/view`};
  });
  const formId=meta.form_id||meta.quizzes?.[0]?.form_id;
  return {r,reason:[reasons[r.status]||r.status,r.source_status!==r.status?reasons[r.source_status]||r.source_status:''].filter(Boolean).join(' '),
   detail:notes.join('\n').slice(0,3000),scores,relatedIds:relatedIds.join('; '),relatedEmails:relatedEmails.join('; '),
   declared:g.record?.declared_sid||coding.get(r.response_id)?.record?.declared_sid||'',files,
   formUrl:formId&&/^[A-Za-z0-9_-]+$/.test(formId)?`https://docs.google.com/forms/d/${formId}/edit`:''};
 });
}
