import {isWaived} from './ca_assessment_policy.mjs';
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
const reviewReasons={
 NO_NOTEBOOK_CODE_ZERO:'No notebook was uploaded, so code is scored 0/14. Confirm the written part from the report.',
 NO_README_NOTEBOOK_TEXT_USED:'No README was uploaded; the written part was read from the notebook\'s own explanation cells. Confirm it.'
};
// Plain-language next step, derived from what was actually uploaded.
function nextStep(r,names,notes,g){
 const ext=[...new Set(names.map(n=>(n.match(/\.([A-Za-z0-9]+)\s*$/)||[,'no extension'])[1].toLowerCase()))].join(', ');
 if(g.review_reason&&reviewReasons[g.review_reason])return reviewReasons[g.review_reason];
 if(r.status==='NOTEBOOK_MISSING_OR_AMBIGUOUS'){
  const nb=names.filter(n=>/\.ipynb\s*$/i.test(n));
  return nb.length>1?`${nb.length} different notebooks were uploaded and none is clearly the submission. Open each and mark the right one.`
   :`No notebook (.ipynb) was uploaded; files are: ${ext}. Open the file(s) and mark manually.`;
 }
 if(r.status==='TEXT_EXTRACTION_PENDING'){
  const text=notes.join(' ');
  if(/image-only/i.test(text))return 'Scanned/image-only document with no selectable text. Read it and mark manually.';
  if(/Unsupported format/i.test(text))return `Unsupported upload (${ext}), e.g. a ZIP or repository export. Open it and mark manually.`;
  if(/could not be rendered/i.test(text))return 'The document would not open reliably. Open it in Drive and mark manually.';
  if(/exceeds supported text length/i.test(text))return 'Document too long for automatic reading. Mark manually.';
 }
 if(r.status==='IDENTITY_MISMATCH')return 'The notebook\'s student ID differs from the form entry and cannot be matched to this account. Confirm which registration is correct.';
 if(r.status==='IDENTITY_CONFLICT'||r.status==='IDENTITY_MISSING')return 'The registration entered is not a valid registration number and the account has no other registration to confirm it. Find the student\'s registration.';
 return '';
}
// Which kind of manual work this row needs, so the lecturer can batch it.
function category(status){
 if(/^IDENTITY_/.test(status))return '1. Identity';
 if(status==='TEXT_EXTRACTION_PENDING')return '2. Unreadable file';
 if(['NOTEBOOK_MISSING_OR_AMBIGUOUS','EMPTY_NOTEBOOK','INVALID_NOTEBOOK','README_OR_NOTEBOOK_MISSING'].includes(status))return '3. Notebook problem';
 if(['WRITTEN_REVIEW','WRITTEN_ERROR','PARTIAL_CODE_ONLY','CODING_PENDING','CODING_STALE'].includes(status))return '4. Written part to mark';
 return '5. Other';
}
function assessmentLabel(a){
 const w=/^W0([1-5])$/.exec(a);if(w)return `Assignment ${w[1]} (${a})`;
 const q=/^Q(\d+)$/.exec(a);if(q)return `Quiz ${q[1]} (${a})`;
 return a;
}
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
 const rows=data.current.filter(r=>r.status!=='GRADED'&&!isWaived(r.assessment)).map(r=>{
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
  const step=nextStep(r,files.map(f=>f.name),notes,g);
  return {r,category:category(r.status),label:assessmentLabel(r.assessment),reason:[reasons[r.status]||r.status,step,r.source_status!==r.status?reasons[r.source_status]||r.source_status:''].filter(Boolean).join(' '),
   detail:notes.join('\n').slice(0,3000),scores,relatedIds:relatedIds.join('; '),relatedEmails:relatedEmails.join('; '),
   declared:g.record?.declared_sid||coding.get(r.response_id)?.record?.declared_sid||'',files,
   formUrl:formId&&/^[A-Za-z0-9_-]+$/.test(formId)?`https://docs.google.com/forms/d/${formId}/edit#response=${encodeURIComponent(r.response_id)}`:''};
 });
 return rows.sort((a,b)=>a.category.localeCompare(b.category)||a.r.assessment.localeCompare(b.r.assessment)||a.r.cohort.localeCompare(b.r.cohort)||String(a.r.student_id).localeCompare(String(b.r.student_id)));
}
