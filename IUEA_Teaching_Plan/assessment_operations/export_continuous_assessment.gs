/** Private, read-only source exports. Does not change forms, windows or marks.
 * Install in the assignment project. Run exportCAAssignments repeatedly until done.
 * A new export run can be started with startCAExport; prior exports remain intact.
 */
function startCAExport() {
  var p=PropertiesService.getScriptProperties();
  var f=DriveApp.createFolder('Private CA export '+new Date().toISOString());
  p.setProperty('CA_EXPORT_FOLDER',f.getId());p.setProperty('CA_EXPORT_CURSOR','0');p.setProperty('CA_QUIZ_CURSOR','0');
  Logger.log(f.getUrl());
}
function exportCAAssignments() {
  var started=Date.now();
  var p=PropertiesService.getScriptProperties();if(!p.getProperty('CA_EXPORT_FOLDER'))startCAExport();
  var folder=DriveApp.getFolderById(p.getProperty('CA_EXPORT_FOLDER'));
  var state=submissionState_(),keys=Object.keys(state).filter(function(k){return /^CML311[123]\|W0[1-5]$/.test(k);}).sort();
  var cursor=Number(p.getProperty('CA_EXPORT_CURSOR')||0);
  if(cursor>=keys.length){Logger.log('COMPLETE '+folder.getUrl());return;}
  var key=keys[cursor],a=state[key],form=FormApp.openById(a.formId);
  var records=[],fileIds={},audit=submissionBook_().getSheetByName('Submission audit').getDataRange().getValues(),headers=audit.shift();
  audit.forEach(function(values){
    var r={};headers.forEach(function(h,i){r[h]=values[i];});
    if(r.assessment_key!==key)return;
    var files=JSON.parse(r.file_ids||'[]');
    records.push({response_id:r.response_id,assessment_key:key,email:r.email,submitted_at:new Date(r.submitted_at).toISOString(),fields:{'Student Registration Number':r.student_id},file_ids:files});
    files.forEach(function(id){fileIds[id]=true;});
  });
  if(form.getResponses().length!==records.length)throw Error('AUDIT_RECEIPT_COUNT_MISMATCH '+key);
  var meta={exported_at:new Date().toISOString(),key:key,window:{open:a.openAt,close:a.closeAt},form_id:a.formId,records:records,files:[],errors:[]};
  var blobs=[],bytes=0,part=0;
  function flush(){if(blobs.length){folder.createFile(Utilities.zip(blobs,key.replace('|','_')+'_files_'+(++part)+'.zip'));blobs=[];bytes=0;}}
  Object.keys(fileIds).forEach(function(id){
    try {
      if(Date.now()-started>250000)throw Error('EXPORT_TIME_LIMIT');
      var f=DriveApp.getFileById(id),name=f.getName(),ext=(name.match(/\.[A-Za-z0-9]+$/)||['.bin'])[0].toLowerCase();
      var b=f.getBlob().setName(id+ext),size=b.getBytes().length;
      if(bytes+size>15000000)flush();blobs.push(b);bytes+=size;
      meta.files.push({id:id,original_name:name,export_name:id+ext,size:size,sha256:Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,b.getBytes()).map(function(v){return ('0'+((v+256)%256).toString(16)).slice(-2);}).join('')});
    }catch(e){meta.errors.push({file_id:id,error:String(e)});}
  });flush();
  folder.createFile(key.replace('|','_')+'_manifest.json',JSON.stringify(meta),MimeType.PLAIN_TEXT);
  p.setProperty('CA_EXPORT_CURSOR',String(cursor+1));
  Logger.log(JSON.stringify({key:key,responses:records.length,files:meta.files.length,errors:meta.errors.length,completed:cursor+1,total:keys.length,folder:folder.getUrl()}));
}

/** One quiz per run, checkpointed to avoid the Apps Script execution limit. */
function exportCAQuizzes() {
  var p=PropertiesService.getScriptProperties();
  if(!p.getProperty('CA_EXPORT_FOLDER'))startCAExport();
  var folder=DriveApp.getFolderById(p.getProperty('CA_EXPORT_FOLDER'));
  var keys=Object.keys(QUIZ_IDENTITY_FORMS).filter(function(k){return /^CML311[123]\|[1-5]$/.test(k);}).sort();
  var cursor=Number(p.getProperty('CA_QUIZ_CURSOR')||0);
  if(cursor>=keys.length){Logger.log('QUIZZES COMPLETE '+folder.getUrl());return;}
  var key=keys[cursor],form=FormApp.openById(QUIZ_IDENTITY_FORMS[key]),items=[],titles={};
  form.getItems().forEach(function(item){
    titles[item.getId()]=item.getTitle();
    if(String(item.getType())==='MULTIPLE_CHOICE'){
      var q=item.asMultipleChoiceItem();
      items.push({id:item.getId(),title:item.getTitle(),points:q.getPoints(),correct:q.getChoices().filter(function(c){return c.isCorrectAnswer();}).map(function(c){return c.getValue();})});
    }
  });
  var records=form.getResponses().map(function(r){
    var scores={};
    // Recorded totals are joined from the private response Sheets export.
    // Per-item score RPCs for every receipt can exceed the execution limit.
    return {response_id:r.getId(),email:r.getRespondentEmail(),submitted_at:r.getTimestamp().toISOString(),answers:r.getItemResponses().map(function(ir){var id=ir.getItem().getId();return {id:id,title:titles[id],answer:ir.getResponse(),score:scores[id]===undefined?null:scores[id]};})};
  });
  folder.createFile(key.replace('|','_Q')+'_quiz.json',JSON.stringify({exported_at:new Date().toISOString(),quizzes:[{key:key,form_id:form.getId(),items:items,records:records}]}),MimeType.PLAIN_TEXT);
  p.setProperty('CA_QUIZ_CURSOR',String(cursor+1));
  Logger.log(JSON.stringify({key:key,responses:records.length,completed:cursor+1,total:keys.length,folder:folder.getUrl()}));
}

/** Checkpoint each collection; remove only this export's temporary trigger. */
function exportCANext(){
  var lock=LockService.getScriptLock();
  if(!lock.tryLock(1000)){
    ScriptApp.newTrigger('exportCANext').timeBased().after(60000).create();
    Logger.log('Another script holds the lock; export retry scheduled.');
    return;
  }
  try{
    ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='exportCANext';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
    var p=PropertiesService.getScriptProperties();
    var started=Date.now();
    if(Number(p.getProperty('CA_QUIZ_CURSOR')||0)<15)exportCAQuizzes();
    while(Number(p.getProperty('CA_QUIZ_CURSOR')||0)>=15&&Date.now()-started<30000&&Number(p.getProperty('CA_EXPORT_CURSOR')||0)<15)exportCAAssignments();
    if(Number(p.getProperty('CA_QUIZ_CURSOR')||0)<15||Number(p.getProperty('CA_EXPORT_CURSOR')||0)<15)
      ScriptApp.newTrigger('exportCANext').timeBased().after(1000).create();
    else Logger.log('ALL EXPORTS COMPLETE');
  }finally{lock.releaseLock();}
}
function inspectCAExportProgress(){
  var p=PropertiesService.getScriptProperties();
  Logger.log(JSON.stringify({quizzes:p.getProperty('CA_QUIZ_CURSOR'),assignments:p.getProperty('CA_EXPORT_CURSOR'),folder:'https://drive.google.com/drive/folders/'+p.getProperty('CA_EXPORT_FOLDER')}));
}
/** Read only the known scheduling backups; never dump all script properties. */
function inspectCAWindowHistory(){
  var p=PropertiesService.getScriptProperties();
  ['FRIDAY_CATCHUP_20260926','FRIDAY_OCT2_PREVIOUS_CML3113|W01','FRIDAY_OCT2_PREVIOUS_CML3113|W02','CML3113_A1_WEEK_20261002','REQUESTED_OPENING_20261002','FRIDAY_A3_OCT9_PREVIOUS_CML3113'].forEach(function(k){Logger.log(k+' '+p.getProperty(k));});
}
