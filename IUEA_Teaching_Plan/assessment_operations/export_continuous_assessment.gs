/** ONE private ZIP: original files, recorded Sheet scores, audit and deadlines.
 * Run exportCAGradingZip once. Inspect progress for the download link.
 * No source form, response, mark, sharing permission or deadline is changed.
 */
function caHash_(bytes){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,bytes).map(function(v){return ('0'+((v+256)%256).toString(16)).slice(-2);}).join('');}
function caFolder_(){return DriveApp.getFolderById(PropertiesService.getScriptProperties().getProperty('CA_EXPORT_FOLDER'));}
function caPut_(folder,blob){
 // Replace only this run's generated export file, never an original submission.
 var old=folder.getFilesByName(blob.getName());while(old.hasNext())old.next().setTrashed(true);
 return folder.createFile(blob);
}
function caJson_(folder,name,data){return caPut_(folder,Utilities.newBlob(JSON.stringify(data),MimeType.PLAIN_TEXT,name));}
function caCutoff_(){return Number(PropertiesService.getScriptProperties().getProperty('CA_EXPORT_CUTOFF'));}
function caProgress_(state,message){
 var p=PropertiesService.getScriptProperties();p.setProperty('CA_EXPORT_STATE',state);
 var book=submissionBook_(),s=book.getSheetByName('CA Export')||book.insertSheet('CA Export');
 s.getRange(1,1,5,2).setValues([['CA grading export',state],['Assignments',Number(p.getProperty('CA_EXPORT_CURSOR')||0)+'/15'],['Quizzes',Number(p.getProperty('CA_QUIZ_CURSOR')||0)+'/15'],['Updated',new Date().toISOString()],['Download / detail',message||'Run inspectCAExportProgress for the latest status.']]);
}
function startCAExport(){
 var p=PropertiesService.getScriptProperties();
 if(p.getProperty('CA_EXPORT_STATE')==='RUNNING')throw Error('An export is running. Use inspectCAExportProgress; do not start another.');
 var sheet=submissionBook_().getSheetByName('CA Quiz windows');if(!sheet)throw Error('Quiz timing mirror is not configured.');
 if(sheet.getRange('E1').getValue()!=='OK')throw Error('Quiz timing mirror is incomplete. Run publishCAQuizWindows.');
 var rows=sheet.getDataRange().getValues(),deadlines={};
 rows.slice(1).forEach(function(r){if(/^CML311[123]\|[1-5]$/.test(r[0])){if(Date.now()-Date.parse(r[2])>30*60000)throw Error('Quiz timing mirror is stale; run publishCAQuizWindows in the quiz project.');deadlines[r[0]]=JSON.parse(r[1]);}});
 if(Object.keys(deadlines).length!==15)throw Error('Incomplete quiz timing mirror');
 var cutoff=Date.now(),folder=DriveApp.createFolder('Private CA grading '+new Date(cutoff).toISOString());
 p.setProperties({CA_EXPORT_FOLDER:folder.getId(),CA_EXPORT_CURSOR:'0',CA_QUIZ_CURSOR:'0',CA_EXPORT_CUTOFF:String(cutoff),CA_EXPORT_STATE:'RUNNING',CA_EXPORT_ZIP:''},false);
 caJson_(folder,'quiz_deadlines.json',deadlines);caProgress_('RUNNING','Preparing one private ZIP. Submissions after '+new Date(cutoff).toISOString()+' will be in the next batch.');
}
function exportCAGradingZip(){
 var p=PropertiesService.getScriptProperties();
 if(['RUNNING','STOPPED'].indexOf(p.getProperty('CA_EXPORT_STATE'))<0)startCAExport();
 exportCANext();
}
function exportCAAssignments(){
 var p=PropertiesService.getScriptProperties(),folder=caFolder_(),started=Date.now(),cutoff=caCutoff_();
 var state=submissionState_(),keys=Object.keys(state).filter(function(k){return /^CML311[123]\|W0[1-5]$/.test(k);}).sort(),cursor=Number(p.getProperty('CA_EXPORT_CURSOR')||0);
 if(cursor>=15)return;if(keys.length!==15)throw Error('Expected 15 assignment forms');
 var key=keys[cursor],a=state[key],checkpointName=key.replace('|','_')+'_checkpoint.json',saved=folder.getFilesByName(checkpointName),checkpoint;
 if(saved.hasNext())checkpoint=JSON.parse(saved.next().getBlob().getDataAsString());
 else{
  var form=FormApp.openById(a.formId),records=[],fileIds={};
  var audit=submissionBook_().getSheetByName('Submission audit').getDataRange().getValues(),headers=audit.shift();
  audit.forEach(function(v){var r={};headers.forEach(function(h,i){r[h]=v[i];});if(r.assessment_key!==key||new Date(r.submitted_at).getTime()>cutoff)return;
   var ids=JSON.parse(r.file_ids||'[]');records.push({response_id:r.response_id,assessment_key:key,email:r.email||'',submitted_at:new Date(r.submitted_at).toISOString(),fields:{'Student Registration Number':r.student_id},file_ids:ids,timing_status:r.status});ids.forEach(function(id){fileIds[id]=true;});});
  var ids=form.getResponses().filter(function(r){return r.getTimestamp().getTime()<=cutoff;}).map(function(r){return r.getId();}).sort();
  if(JSON.stringify(ids)!==JSON.stringify(records.map(function(r){return r.response_id;}).sort()))throw Error('Assignment audit is not synced for '+key+'. Run syncSubmissions, then resume this export.');
  checkpoint={meta:{exported_at:new Date().toISOString(),cutoff:new Date(cutoff).toISOString(),key:key,window:{open:a.openAt,close:a.closeAt},form_id:a.formId,records:records,files:[],errors:[]},fileIds:Object.keys(fileIds),part:0};
  caJson_(folder,checkpointName,checkpoint);
 }
 var meta=checkpoint.meta,blobs=[],bytes=0,copied=0;
 function flush(){if(blobs.length){caPut_(folder,Utilities.zip(blobs,key.replace('|','_')+'_files_'+(++checkpoint.part)+'.zip'));blobs=[];bytes=0;}}
 while(meta.files.length<checkpoint.fileIds.length&&copied<80&&Date.now()-started<200000){
  var id=checkpoint.fileIds[meta.files.length],f=DriveApp.getFileById(id),name=f.getName(),ext=(name.match(/\.[A-Za-z0-9]+$/)||['.bin'])[0].toLowerCase(),blob=f.getBlob().setName(id+ext),content=blob.getBytes();
  if(bytes+content.length>15000000)flush();blobs.push(blob);bytes+=content.length;
  meta.files.push({id:id,original_name:name,export_name:id+ext,size:content.length,sha256:caHash_(content)});copied++;
 }
 flush();caJson_(folder,checkpointName,checkpoint);
 if(meta.files.length<checkpoint.fileIds.length){Logger.log(key+': '+meta.files.length+'/'+checkpoint.fileIds.length+' files checkpointed.');return;}
 caJson_(folder,key.replace('|','_')+'_manifest.json',meta);
 var temporary=folder.getFilesByName(checkpointName);while(temporary.hasNext())temporary.next().setTrashed(true);
 p.setProperty('CA_EXPORT_CURSOR',String(cursor+1));Logger.log(key+': '+meta.records.length+' receipts, '+meta.files.length+' files copied.');
}

function caScoreSheet_(form){
 var id=form.getDestinationId();if(!id)throw Error('Quiz has no response spreadsheet');
 var sheets=SpreadsheetApp.openById(id).getSheets(),url=form.getPublishedUrl().split('?')[0];
 for(var i=0;i<sheets.length;i++){
  var u=sheets[i].getFormUrl();if(!u)continue;
  if(u.split('?')[0]===url||u.indexOf('/'+form.getId()+'/')>=0||FormApp.openByUrl(u).getId()===form.getId())return sheets[i];
 }
 throw Error('Cannot identify the quiz response sheet by its linked form');
}
function caRecordedRows_(values,cutoff){
 var heads=values[0],ts=heads.indexOf('Timestamp'),email=heads.indexOf('Email Address'),score=heads.indexOf('Score');
 if(ts<0||email<0||score<0)throw Error('Quiz sheet is missing Timestamp, Email Address or Score');
 var rows={};values.slice(1).forEach(function(v){if(!v[ts])return;var time=new Date(v[ts]).getTime();if(time>cutoff)return;
  var key=Math.floor(time/1000)+'|'+String(v[email]).trim().toLowerCase();if(!rows[key])rows[key]=[];
  var fields={};heads.forEach(function(h,i){if(/registration|student number|student id/i.test(h))fields[h]=v[i];});
  rows[key].push({score:v[score],fields:fields});});return rows;
}
function exportCAQuizzes(){
 var p=PropertiesService.getScriptProperties(),folder=caFolder_(),cutoff=caCutoff_(),keys=Object.keys(QUIZ_IDENTITY_FORMS).filter(function(k){return /^CML311[123]\|[1-5]$/.test(k);}).sort(),cursor=Number(p.getProperty('CA_QUIZ_CURSOR')||0);
 if(cursor>=15)return;if(keys.length!==15)throw Error('Expected 15 quiz forms');
 var key=keys[cursor],form=FormApp.openById(QUIZ_IDENTITY_FORMS[key]),sheet=caScoreSheet_(form),values=sheet.getDataRange().getValues(),recorded=caRecordedRows_(values,cutoff),warnings=[];
 var titles={};form.getItems().forEach(function(item){titles[item.getId()]=item.getTitle();});
 var records=form.getResponses().filter(function(r){return r.getTimestamp().getTime()<=cutoff;}).map(function(r){
  var email=r.getRespondentEmail()||'',match=recorded[Math.floor(r.getTimestamp().getTime()/1000)+'|'+email.trim().toLowerCase()]||[];
  if(match.length!==1){
   // A few legacy receipts have no unique Sheet row. Read their saved Forms
   // scores; never recalculate from a changed answer key or invent a zero.
   var total=0,maximum=0,complete=true;
   r.getGradableItemResponses().forEach(function(ir){var item=ir.getItem();if(String(item.getType())!=='MULTIPLE_CHOICE')return;var points=item.asMultipleChoiceItem().getPoints();if(!points)return;maximum+=points;var value=ir.getScore();if(typeof value!=='number'||value<0||value>points)complete=false;else total+=value;});
   match=[{fields:{},score:complete&&maximum===5?total:null}];
   warnings.push({response_id:r.getId(),issue:'RECORDED_FORM_SCORE_FALLBACK'});
  }
  var answers=r.getItemResponses().map(function(ir){var id=ir.getItem().getId();return {id:id,title:titles[id],answer:ir.getResponse(),score:null};}),entry=match[0];
  function registration(fields){var found='';Object.keys(fields).some(function(h){if(/registration|student number|student id/i.test(h)&&String(fields[h]||'').trim()){found=String(fields[h]).replace(/\s/g,'').toUpperCase();return true;}return false;});return found;}
  var fields={};answers.forEach(function(a){fields[a.title]=a.answer;});var entered=registration(fields),inSheet=registration(entry.fields);
  if(entered&&inSheet&&entered!==inSheet)throw Error('Quiz registration differs between Form and Sheet; review '+key);
  if(!entered&&inSheet)answers.push({id:'sheet-identity',title:'Student Registration Number',answer:inSheet,score:null});
  var score=entry.score;if(score==='')score=null;
  if(score!==null&&(typeof score!=='number'||score<0||score>5))throw Error('Invalid recorded quiz score for '+key);
  if(score===null)warnings.push({response_id:r.getId(),issue:'QUIZ_SCORE_PENDING'});
  answers.push({id:'recorded-total',title:'Recorded Forms total',answer:'',score:score});
  return {response_id:r.getId(),email:email,submitted_at:r.getTimestamp().toISOString(),answers:answers};
 });
 caJson_(folder,key.replace('|','_Q')+'_quiz.json',{exported_at:new Date().toISOString(),cutoff:new Date(cutoff).toISOString(),source_kind:'recorded_sheet_scores_with_form_receipts',spreadsheet_id:sheet.getParent().getId(),sheet_id:sheet.getSheetId(),warnings:warnings,quizzes:[{key:key,form_id:form.getId(),items:[{id:'recorded-total',points:5}],records:records}]});
 p.setProperty('CA_QUIZ_CURSOR',String(cursor+1));Logger.log(key+': '+records.length+' recorded scores copied.');
}
function finishCAGradingZip_(){
 var p=PropertiesService.getScriptProperties(),folder=caFolder_(),files=folder.getFiles(),blobs=[],entries=[];
 while(files.hasNext()){var f=files.next(),name=f.getName();if(name==='ca_bundle.json'||name.indexOf('IUEA_CA_')===0)continue;
  if(!/^(quiz_deadlines\.json|CML311[123]_(W0[1-5]_(manifest\.json|files_\d+\.zip)|Q[1-5]_quiz\.json))$/.test(name))throw Error('Unexpected export file '+name);
  var blob=f.getBlob().setName(name),bytes=blob.getBytes();blobs.push(blob);entries.push({name:name,sha256:caHash_(bytes),bytes:bytes.length});
 }
 if(entries.filter(function(x){return /_manifest\.json$/.test(x.name);}).length!==15||entries.filter(function(x){return /_quiz\.json$/.test(x.name);}).length!==15)throw Error('Incomplete export: no ZIP released');
 var metadata={format:'IUEA_CA_BUNDLE',version:1,complete:true,cutoff:new Date(caCutoff_()).toISOString(),exported_at:new Date().toISOString(),files:entries};
 blobs.push(Utilities.newBlob(JSON.stringify(metadata),MimeType.PLAIN_TEXT,'ca_bundle.json'));
 var name='IUEA_CA_'+Utilities.formatDate(new Date(caCutoff_()),'Africa/Kampala','yyyyMMdd_HHmmss')+'.zip',zip=caPut_(folder,Utilities.zip(blobs,name));
 p.setProperty('CA_EXPORT_ZIP',zip.getId());caProgress_('COMPLETE',zip.getUrl());Logger.log('DOWNLOAD ONE ZIP: '+zip.getUrl());
}
function exportCANext(){
 var lock=LockService.getScriptLock();if(!lock.tryLock(1000)){
  Logger.log('Another operation holds the lock; a retry is scheduled.');
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='exportCANext';}))ScriptApp.newTrigger('exportCANext').timeBased().after(60000).create();
  return;
 }
 try{
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='exportCANext';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
  var p=PropertiesService.getScriptProperties();if(p.getProperty('CA_EXPORT_STATE')==='COMPLETE')return;caProgress_('RUNNING');
  var started=Date.now();
  while(Date.now()-started<30000){
   if(Number(p.getProperty('CA_QUIZ_CURSOR'))<15)exportCAQuizzes();
   else if(Number(p.getProperty('CA_EXPORT_CURSOR'))<15)exportCAAssignments();
   else {finishCAGradingZip_();return;}
  }
  caProgress_('RUNNING');ScriptApp.newTrigger('exportCANext').timeBased().after(1000).create();
 }catch(e){caProgress_('STOPPED',String(e));throw e;}finally{lock.releaseLock();}
}
function inspectCAExportProgress(){
 var p=PropertiesService.getScriptProperties();Logger.log(JSON.stringify({state:p.getProperty('CA_EXPORT_STATE'),assignments:p.getProperty('CA_EXPORT_CURSOR'),quizzes:p.getProperty('CA_QUIZ_CURSOR'),download:p.getProperty('CA_EXPORT_ZIP')?'https://drive.google.com/file/d/'+p.getProperty('CA_EXPORT_ZIP')+'/view':null}));
}
