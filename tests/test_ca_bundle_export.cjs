const fs=require('fs'),vm=require('vm'),assert=require('assert');
const c={};vm.createContext(c);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/assessment_operations/export_continuous_assessment.gs','utf8'),c);
const cutoff=Date.parse('2026-10-21T10:00:00Z');
const values=[['Timestamp','Email Address','Score','Student Registration Number'],[new Date(cutoff-1000),' Demo@example.test ',0,'SYNTHETIC'],[new Date(cutoff+1000),'late@example.test',5,'LATER']];
const result=c.caRecordedRows_(values,cutoff),key=Math.floor((cutoff-1000)/1000)+'|demo@example.test';
assert.equal(Object.keys(result).length,1);assert.equal(result[key][0].score,0);assert.equal(result[key][0].fields['Student Registration Number'],'SYNTHETIC');
assert.throws(()=>c.caRecordedRows_([['Wrong header']],cutoff),/missing/);
const duplicate=c.caRecordedRows_([...values,values[1]],cutoff);assert.equal(duplicate[key].length,2);
// Select the sheet by its actual linked form, never by a sheet-number guess.
const wrong={getFormUrl:()=>null},correct={getFormUrl:()=> 'https://docs.google.com/forms/d/FORM/viewform'};
c.SpreadsheetApp={openById:()=>({getSheets:()=>[wrong,correct]})};
const f={getDestinationId:()=> 'BOOK',getPublishedUrl:()=> 'https://docs.google.com/forms/d/e/PUBLIC/viewform',getId:()=> 'FORM'};
assert.equal(c.caScoreSheet_(f),correct);
console.log('PASS: recorded zero marks, cutoff, duplicate detection and form-linked sheet selection');
// Existing saved Forms scores are a fallback for old receipts absent from Sheets.
let exported;
const item={getType:()=> 'MULTIPLE_CHOICE',asMultipleChoiceItem:()=>({getPoints:()=>5})};
let savedScore=0;
const response={getTimestamp:()=>new Date(cutoff-1000),getRespondentEmail:()=> 'legacy@example.test',getId:()=> 'SYNTHETIC-RECEIPT',getItemResponses:()=>[],getGradableItemResponses:()=>[{getItem:()=>item,getScore:()=>savedScore}]};
c.PropertiesService={getScriptProperties:()=>({getProperty:k=>k==='CA_EXPORT_CUTOFF'?String(cutoff):'0',setProperty:()=>{}})};
c.caFolder_=()=>({});c.caJson_=(_folder,_name,value)=>{exported=value;};c.Logger={log:()=>{}};
c.QUIZ_IDENTITY_FORMS=Object.fromEntries(['CML3111','CML3112','CML3113'].flatMap(code=>[1,2,3,4,5].map(w=>[code+'|'+w,'FORM'])));
c.FormApp={openById:()=>({getResponses:()=>[response],getId:()=> 'FORM',getItems:()=>[]})};
c.caScoreSheet_=()=>({getDataRange:()=>({getValues:()=>[['Timestamp','Email Address','Score']]}),getParent:()=>({getId:()=> 'BOOK'}),getSheetId:()=>1});
c.exportCAQuizzes();assert.equal(exported.quizzes[0].records[0].answers[0].score,0);
assert.equal(exported.warnings[0].issue,'RECORDED_FORM_SCORE_FALLBACK');
savedScore=null;c.exportCAQuizzes();assert.equal(exported.quizzes[0].records[0].answers[0].score,null);
assert(exported.warnings.some(x=>x.issue==='QUIZ_SCORE_PENDING'));
console.log('PASS: legacy recorded Forms zero preserved; missing scores stay pending');
// Large assignments resume inside the collection instead of restarting all files.
const props={CA_EXPORT_CURSOR:'0',CA_EXPORT_CUTOFF:String(cutoff)},stored=new Map();
function iterator(rows){let i=0;return {hasNext:()=>i<rows.length,next:()=>rows[i++]};}
const folder={getFilesByName:name=>iterator(stored.has(name)?[{getBlob:()=>({getDataAsString:()=>JSON.stringify(stored.get(name))}),setTrashed:()=>stored.delete(name)}]:[])};
c.PropertiesService={getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>{props[k]=v;}})};
c.caFolder_=()=>folder;c.caHash_=()=> 'synthetic-hash';c.caJson_=(_folder,name,data)=>stored.set(name,JSON.parse(JSON.stringify(data)));c.caPut_=()=>{};
c.Utilities={zip:()=>({})};
c.submissionState_=()=>Object.fromEntries(['CML3111','CML3112','CML3113'].flatMap(code=>[1,2,3,4,5].map(w=>[code+'|W0'+w,{formId:'FORM'}])));
const fileIds=Array.from({length:81},(_,i)=>'file'+i);
c.submissionBook_=()=>({getSheetByName:()=>({getDataRange:()=>({getValues:()=>[['assessment_key','submitted_at','file_ids','response_id','student_id','status'],['CML3111|W01',new Date(cutoff-1000),JSON.stringify(fileIds),'SYNTHETIC-RECEIPT','SYNTHETIC','ON_TIME']]})})});
c.FormApp={openById:()=>({getResponses:()=>[response]})};
c.DriveApp={getFileById:()=>({getName:()=> 'work.pdf',getBlob:()=>({setName:()=>({getBytes:()=>[1,2,3]})})})};
c.exportCAAssignments();assert.equal(props.CA_EXPORT_CURSOR,'0');assert.equal(stored.get('CML3111_W01_checkpoint.json').meta.files.length,80);
c.exportCAAssignments();assert.equal(props.CA_EXPORT_CURSOR,'1');assert.equal(stored.get('CML3111_W01_manifest.json').files.length,81);assert(!stored.has('CML3111_W01_checkpoint.json'));
console.log('PASS: large assignment checkpoint resumes without duplicating attachments');
// The currently executing one-shot trigger is still listed when a lock fails.
// Always enqueue another retry; testing for an existing trigger can strand it.
let retries=0;c.LockService={getScriptLock:()=>({tryLock:()=>false})};
c.ScriptApp={getProjectTriggers:()=>[{getHandlerFunction:()=> 'exportCANext'}],newTrigger:()=>({timeBased:()=>({after:()=>({create:()=>{retries++;}})})})};
c.exportCANext();assert.equal(retries,1);console.log('PASS: lock contention schedules a fresh retry');
