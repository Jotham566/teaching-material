/** Create a separate lecturer decision sheet; never modifies the grading ledger. */
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {reviewDetails} from './ca_review_details.mjs';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: build_identity_review.mjs ledger.json NEW-review.xlsx');
try {await fs.access(output);throw Error('Review file already exists. Choose a new filename to preserve lecturer decisions.');} catch(e){if(e.code!=='ENOENT')throw e;}
const source=await fs.readFile(input),data=JSON.parse(source),base=path.dirname(input);
const evidence=JSON.parse(await fs.readFile(path.join(base,'identity_evidence.json'),'utf8'));
const details=new Map((await reviewDetails(data,base)).map(x=>[x.r.response_id,x]));
const uniq=xs=>[...new Set(xs.filter(Boolean))].sort();
const registrationFirst=data.identity_allocation_policy==='registration_first_notebook_precedence';
// Components group related evidence for review, not people for automatic merging.
// Blank identifiers never join unrelated receipts; course groups remain separate.
const parent=new Map();
function root(x){if(!parent.has(x))parent.set(x,x);if(parent.get(x)!==x)parent.set(x,root(parent.get(x)));return parent.get(x);}
function keys(r){return [r.email&&`${r.cohort}|email|${r.email.toLowerCase().trim()}`,r.student_id&&`${r.cohort}|reg|${r.student_id}`].filter(Boolean);}
function receiptRoot(r){const k=keys(r);return root(k[0]||`${r.cohort}|receipt|${r.response_id}`);}
for(const r of data.attempts){const k=keys(r);for(const v of k)parent.set(root(v),root(k[0]));}
const held=data.current.filter(r=>r.status.startsWith('IDENTITY_'));
const groups=new Map();for(const r of held){const key=receiptRoot(r);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);}
const cases=[],rows=[],links=[],coverage=[];
for(const [key,pending] of [...groups].sort((a,b)=>a[0].localeCompare(b[0]))){
 const records=data.attempts.filter(r=>receiptRoot(r)===key);
 const ids=uniq(records.map(r=>r.student_id)),emails=uniq(records.map(r=>r.email));
 const ev=records.flatMap(r=>evidence[r.response_id]||[]);
 const names=uniq([...records.map(r=>r.full_name),...ev.map(e=>e.name)]);
 const declared=uniq([...ev.flatMap(e=>(e.registrations||[]).map(x=>x.registration)),...pending.map(r=>details.get(r.response_id)?.declared)]);
 const caseId=pending[0].cohort+'-'+crypto.createHash('sha256').update(uniq(records.map(r=>r.response_id)).join('|')).digest('hex').slice(0,8);
 const questions=[];
 if(ids.length>1)questions.push('Which registration is correct on the university record: '+ids.join(' or ')+'? Confirm every digit and the programme suffix.');
 if(emails.length>1&&!registrationFirst)questions.push('Do all listed email accounts belong to the same student? If not, map each account/receipt to its owner.');
 if(pending.some(r=>r.status==='IDENTITY_MISMATCH'))questions.push(registrationFirst?'Notebook precedence is configured, but a trusted complete result could not be released. Inspect the notebook registration and original file; confirm the target and flag any unreadable/wrong upload.':'The form and notebook disagree. Confirm the author and correct registration for each flagged receipt; identify any wrong upload.');
 if(pending.some(r=>r.status==='IDENTITY_MISSING'))questions.push(registrationFirst?'Supply the missing Student Registration Number for each flagged receipt.':'Supply the missing registration/email for each flagged receipt.');
 if(!registrationFirst)questions.push(names.length?'Confirm the full name against the submitted work and university record.':'No name was recovered. Ask the student to confirm their full name and registration.');
 else questions.push('Confirm the registration for the flagged receipts only. Shared email/name does not require merging distinct registrations. Names are optional and do not block marks.');
 const first=rows.length+7;
 for(const r of records){
  const es=evidence[r.response_id]||[], files=uniq([...(r.file_ids||[]),...es.map(e=>e.file_id)]);
  for(const fileId of files.length?files:['']){
   const f=es.filter(e=>e.file_id===fileId), url=fileId?`https://drive.google.com/file/d/${fileId}/view`:'';
   if(fileId&&!/^[A-Za-z0-9_-]+$/.test(fileId))throw Error('Invalid file ID');
   const isHeld=pending.some(x=>x.response_id===r.response_id);
   rows.push([caseId,r.assessment,r.email,r.submitted_student_id||r.student_id,uniq(f.map(e=>e.name)).join('\n'),uniq(f.map(e=>e.quote)).join('\n'),uniq(f.flatMap(e=>(e.registrations||[]).map(x=>x.registration+': '+x.quote))).join('\n'),details.get(r.response_id)?.declared||'',url?'Open submission':'No attachment (quiz or missing file)',isHeld?r.status:'Related receipt: '+r.status,r.source_score??(r.status==='GRADED'?r.score:null),r.response_id,uniq(f.map(e=>e.error)).join('\n'),'','','','']);
   if(url)links.push([`I${rows.length+6}`,url]);
  }
 }
 cases.push([caseId,pending[0].cohort,names.join('\n')||'Name not recovered',ids.join('\n')||'Missing',emails.join('\n')||'Missing',questions.join('\n'),`Submission evidence rows ${first}–${rows.length+6}`,pending.length,'Unreviewed','','','','',declared.join('\n')]);
 coverage.push(...pending.map(r=>r.response_id));
}
if(coverage.length!==held.length||new Set(coverage).size!==held.length)throw Error('Held receipt coverage is not one-to-one');
const runtime=process.env.IUEA_ARTIFACT_NODE_MODULES||path.join(process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook,SpreadsheetFile}=createRequire(path.join(runtime,'package.json'))('@oai/artifact-tool');
const wb=Workbook.create();
function sheet(name,headers,values,widths){const s=wb.worksheets.add(name),end=values.length+6,last=String.fromCharCode(64+headers.length);s.showGridLines=false;s.getRange('A2').values=[[name]];s.getRange(`A6:${last}6`).values=[headers];if(values.length)s.getRange(`A7:${last}${end}`).values=values.map(r=>r.map(v=>typeof v==='string'&&/^[=+@-]/.test(v)?"'"+v:v));s.getRange(`A1:${last}${end}`).format.font={name:'Arial',size:11};s.getRange('A2').format.font={name:'Arial',size:16,bold:true};s.getRange(`A6:${last}6`).format={fill:'#17365D',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:48};s.getRange(`A7:${last}${end}`).format.wrapText=true;s.getRange(`A7:${last}${end}`).format.verticalAlignment='top';widths.forEach((w,i)=>s.getRange(`${String.fromCharCode(65+i)}6:${String.fromCharCode(65+i)}${end}`).format.columnWidth=w);s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(2);if(values.length)s.tables.add(`A6:${last}${end}`,true,name.replaceAll(' ','')+'Table');values.forEach((r,i)=>{const lines=Math.max(...r.map((v,j)=>String(v??'').split('\n').reduce((sum,line)=>sum+Math.max(1,Math.ceil(line.length/(widths[j]-2))),0)));s.getRange(`A${i+7}:${last}${i+7}`).format.rowHeight=Math.min(409,Math.max(55,lines*15+8));});return s;}
const s=sheet('Cases',['Case ID','Class','Names found (unconfirmed)','Registration candidates',registrationFirst?'Submission accounts':'Accounts to confirm','Exactly what to confirm','Where to find evidence','Held current records','Your decision','Confirmed full name','Confirmed Registration Number','Confirmed email(s)','Your explanation / evidence','Registrations quoted in files'],cases,[27,14,29,29,34,65,32,15,24,29,30,34,50,30]);
s.getRange('A3').values=[[`${cases.length} cases covering ${held.length} current records held for identity review. Source ledger: ${data.updated_at}.`]];
s.getRange('A4').values=[['1. Read the case. 2. Filter Submission evidence by Case ID and open files. 3. Fill yellow cells. Keep uncertain cases open.']];
s.getRange('A5').values=[[registrationFirst?'Confirm the registration in K and explain in M, or use yellow receipt-level fields. Names/email are optional. Return the saved file; marks do not change automatically.':'Same student: complete J–M. Different students: fill the yellow receipt-level fields on Submission evidence. Return the saved file; marks do not change automatically.']];
if(cases.length){s.getRange(`I7:M${cases.length+6}`).format.fill='#FFF2CC';s.getRange(`I7:I${cases.length+6}`).dataValidation={rule:{type:'list',values:['Unreviewed','Same student confirmed','Different students','Still uncertain']}};}
const e=sheet('Submission evidence',['Case ID','Assessment','Submitting email','Registration entered','Name in file','Exact name quotation','Registration quotation','Notebook registration','Submission link','Record status','Retained source mark','Response ID','File-reading issue','Confirmed author name','Confirmed registration','Confirmed account owner/email','Receipt decision / reason'],rows,[27,14,34,29,28,45,50,29,24,32,18,40,38,28,29,34,45]);
e.getRange('A3').values=[['Filter Case ID to see each account’s evidence. Related receipts provide context and are not all held marks.']];
e.getRange('A4').values=[['File names/quotes are evidence, not verified identity. Missing attachments are shown explicitly; quiz receipts usually have no files.']];
e.getRange('A5').values=[['For different students or wrong uploads, fill yellow columns for the affected Response IDs. Do not choose a registration from course-group patterns alone.']];
if(rows.length)e.getRange(`N7:Q${rows.length+6}`).format.fill='#FFF2CC';
wb.recalculate();
await fs.mkdir(path.dirname(output),{recursive:true});
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
const linkFile=output+'.links.json';await fs.writeFile(linkFile,JSON.stringify(links));
execFileSync(process.env.IUEA_PYTHON||'python3',[fileURLToPath(new URL('./attach_xlsx_hyperlinks.py',import.meta.url)),output,'xl/worksheets/sheet2.xml',linkFile],{timeout:120000,stdio:['ignore','pipe','pipe']});await fs.unlink(linkFile);
execFileSync(process.env.IUEA_PYTHON||'python3',[fileURLToPath(new URL('./validate_xlsx_table_headers.py',import.meta.url)),output],{timeout:120000,stdio:['ignore','pipe','pipe']});
for(const [sheetName,range] of [['Cases','A6:F9'],['Submission evidence','E6:I9']]){const image=await wb.render({sheetName,range,scale:1});await fs.writeFile(output+'.'+sheetName.replaceAll(' ','_')+'.png',new Uint8Array(await image.arrayBuffer()));}
const report={cases:cases.length,heldRecords:held.length,evidenceRows:rows.length,links:links.length,sourceSha256:crypto.createHash('sha256').update(source).digest('hex'),coveredResponseIds:coverage};
await fs.writeFile(output+'.audit.json',JSON.stringify(report,null,2));
if(!(await fs.readFile(input)).equals(source))throw Error('Source changed during review generation');
console.log(JSON.stringify({...report,coveredResponseIds:undefined}));
