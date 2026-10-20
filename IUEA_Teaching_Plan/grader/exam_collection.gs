/** Colab test snapshots. Add to the existing lecturer-owned assignment project.
 * No web app, public folder, AI service or paid cloud runtime is required.
 * Source hashes bind the form timestamp to exact notebook bytes.
 */
var EXAM_CONFIG='IUEA_COLAB_EXAMS_V1';
var EXAM_OWNER='wirmbeesubs@gmail.com';
var EXAM_COLUMNS=['response_id','cohort','assessment','variant','full_name','email','student_registration_number','submitted_at','opens_at','closes_at','status','snapshot_id','notebook_sha256','source_id','detail'];
function examConfig_(){return JSON.parse(PropertiesService.getScriptProperties().getProperty(EXAM_CONFIG)||'{}');}
function examSave_(c){PropertiesService.getScriptProperties().setProperty(EXAM_CONFIG,JSON.stringify(c));}
function examText_(s){s=String(s==null?'':s);return /^[=+@-]/.test(s)?"'"+s:s;}
function examSheet_(book,name,headers){var s=book.getSheetByName(name)||book.insertSheet(name);if(!s.getLastRow()){s.appendRow(headers);s.setFrozenRows(1);s.getRange(1,1,1,headers.length).setBackground('#1C3144').setFontColor('#FFFFFF').setFontWeight('bold');}return s;}
function installColabExamCollection(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_();
  if(!c.folderId)c.folderId=DriveApp.createFolder('IUEA private test snapshots').getId();
  if(!c.bookId)c.bookId=SpreadsheetApp.create('IUEA Test submissions and marks').getId();
  c.forms=c.forms||{};examSave_(c);
  var book=SpreadsheetApp.openById(c.bookId);
  examSheet_(book,'Collection',EXAM_COLUMNS);
  var windows=examSheet_(book,'Test windows',['assessment_key','opens_at','closes_at','enabled']);
  windows.getRange('B:C').setNumberFormat('@');
  ['CML3111','CML3112','CML3113'].forEach(function(cohort){['TEST1','TEST2'].forEach(function(exam){
   var key=cohort+'|'+exam;
   if(c.forms[key])return;
   var form=FormApp.create(cohort+' '+exam+' — Colab test submission');
   form.setDescription('Use the Submit test button at the end of your issued Colab notebook. It prepares the fields below. Sign in with the same Google account used in Colab. Submit before the lecturer’s deadline. Your exact notebook snapshot is copied to the lecturer’s private folder. No download or file upload is required.');
   form.setCollectEmail(true).setLimitOneResponsePerUser(false).setAllowResponseEdits(false);
   var names=['Full name','Student Registration Number','Variant','Snapshot file ID','Snapshot SHA-256'];var items={};
   names.forEach(function(name){var item=form.addTextItem().setTitle(name).setRequired(true);if(name==='Student Registration Number')item.clearValidation().setHelpText('Enter your own registration number exactly as on your university record. Any format is accepted.');items[name]=item.getId();});
   form.setConfirmationMessage('Your response has been recorded. The lecturer’s system will verify and collect the notebook snapshot. Keep your snapshot in Drive until grades are released. If the button or form reported an error, tell the invigilator immediately. Grades are calculated after the test.');
   form.setDestination(FormApp.DestinationType.SPREADSHEET,c.bookId);
   if(typeof form.setPublished==='function')form.setPublished(true);
   form.setAcceptingResponses(false);
   var prefill=form.createResponse();form.getItems(FormApp.ItemType.TEXT).forEach(function(item){prefill.withItemResponse(item.asTextItem().createResponse('PLACEHOLDER_'+item.getId()));});
   c.forms[key]={formId:form.getId(),url:form.getPublishedUrl(),prefill:prefill.toPrefilledUrl(),items:items};examSave_(c);
   windows.appendRow([key,'','','NO']);
   ScriptApp.newTrigger('collectColabExamResponse').forForm(form).onFormSubmit().create();
  });});
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='syncColabExams';}))ScriptApp.newTrigger('syncColabExams').timeBased().everyMinutes(5).create();
  console.log('Installed. Forms remain closed until their Test windows row is enabled. Workbook: '+book.getUrl());
  console.log('PUBLIC_NOTEBOOK_CONFIG '+JSON.stringify({lecturer_email:EXAM_OWNER,forms:c.forms}));
 }finally{lock.releaseLock();}
}
function examWindow_(key,c){
 var rows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows').getDataRange().getValues();
 var r=rows.slice(1).filter(function(x){return x[0]===key;})[0];
 return r?{open:String(r[1]),close:String(r[2]),enabled:String(r[3]).toUpperCase()==='YES'}:{open:'',close:'',enabled:false};
}
function examCollect_(response,key,c){
 var sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Collection');
 if(sheet.getLastRow()>1&&sheet.getRange(2,1,sheet.getLastRow()-1,1).getValues().some(function(r){return r[0]===response.getId();}))return;
 var values={};response.getItemResponses().forEach(function(ir){values[ir.getItem().getTitle()]=String(ir.getResponse()).trim();});
 var w=examWindow_(key,c),stamp=response.getTimestamp().toISOString(),parts=key.split('|'),email=response.getRespondentEmail()||'';
 var row=[response.getId(),parts[0],parts[1],values['Test allocation code']||values['Variant']||'',values['Full name']||'',email,values['Student Registration Number']||'',stamp,w.open,w.close,'PENDING','',values['Snapshot SHA-256']||'',values['Snapshot file ID']||'',''];
 try{
  if(!w.enabled||!isFinite(Date.parse(w.open))||!isFinite(Date.parse(w.close))||Date.parse(stamp)<Date.parse(w.open)||Date.parse(stamp)>Date.parse(w.close)){row[10]='OUTSIDE_WINDOW';}
  else{
   if(!email||!row[4]||!row[6])throw Error('Missing student details');
   var allocation=examAllocation_(row[3],key,row[6],email,c);row[3]=allocation.variant;
   if(!/^[a-zA-Z0-9_-]{10,200}$/.test(row[13])||!/^[a-f0-9]{64}$/.test(row[12]))throw Error('Invalid snapshot reference');
   var file=DriveApp.getFileById(row[13]);
   if(file.getOwner().getEmail().toLowerCase()!==email.toLowerCase())throw Error('The form account must own the snapshot. Use the same account in Colab and the form.');
   if(file.getSize()>10*1024*1024)throw Error('Notebook exceeds 10 MB');
   var blob=file.getBlob(),bytes=blob.getBytes();
   var hash=Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,bytes).map(function(b){return ('0'+((b+256)%256).toString(16)).slice(-2);}).join('');
   if(hash!==row[12])throw Error('Snapshot changed after preparation. Use the notebook button again and submit a new response before the deadline.');
   var nb=JSON.parse(blob.getDataAsString());if(nb.nbformat!==4||!Array.isArray(nb.cells))throw Error('Snapshot is not a notebook');
   if(allocation.code&&(!nb.metadata||nb.metadata.iuea_allocation_code!==allocation.code))throw Error('Notebook does not match your issued test files. Return to the test entry page.');
   // Copy the bytes just verified, not the mutable source file a second time.
   var copy=DriveApp.getFolderById(c.folderId).createFile(Utilities.newBlob(bytes,'application/x-ipynb+json',response.getId()+'.ipynb'));
   row[11]=copy.getId();row[10]='COLLECTED';
  }
 }catch(e){row[10]='COLLECTION_ERROR';row[14]=String(e);}
 sheet.appendRow(row.map(examText_));
}
function collectColabExamResponse(e){var lock=LockService.getScriptLock();lock.waitLock(30000);try{var c=examConfig_();var key=Object.keys(c.forms).filter(function(k){return c.forms[k].formId===e.source.getId();})[0];if(!key)throw Error('Unknown test form');examCollect_(e.response,key,c);}finally{lock.releaseLock();}}
function examFormInstructions_(form,w){
 var text='Use the Submit test button at the end of your issued Colab notebook. It prepares the fields below. Sign in with the same Google account used in Colab. Tick the email confirmation box, check your details and press Submit. Leave the automatically filled snapshot fields unchanged. No manual notebook download or file upload is required. Grades are calculated after the test.';
 if(isFinite(Date.parse(w.open))&&isFinite(Date.parse(w.close))){
  text+='\n\nOpens: '+Utilities.formatDate(new Date(w.open),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala. Closes: '+Utilities.formatDate(new Date(w.close),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala.';
 }
 if(form.getDescription()!==text)form.setDescription(text);
 form.getItems(FormApp.ItemType.TEXT).forEach(function(item){var i=item.asTextItem();if(/^Snapshot /.test(i.getTitle())&&i.getHelpText()!=='Automatically filled by the notebook button. Do not change this value.')i.setHelpText('Automatically filled by the notebook button. Do not change this value.');});
}
function syncColabExams(){
 var lock=LockService.getScriptLock();if(!lock.tryLock(1000))return false;
 try{
  var c=examConfig_(),ledger=SpreadsheetApp.openById(c.bookId).getSheetByName('Collection'),known={};
  if(ledger.getLastRow()>1)ledger.getRange(2,1,ledger.getLastRow()-1,1).getValues().forEach(function(r){known[r[0]]=true;});
  Object.keys(c.forms||{}).forEach(function(key){
   var f=FormApp.openById(c.forms[key].formId),w=examWindow_(key,c),now=Date.now();examFormInstructions_(f,w);
   var shouldOpen=w.enabled&&now>=Date.parse(w.open)&&now<=Date.parse(w.close);
   if(f.isAcceptingResponses()!==shouldOpen)f.setAcceptingResponses(shouldOpen);
   f.getResponses().forEach(function(r){if(!known[r.getId()]){examCollect_(r,key,c);known[r.getId()]=true;}});
  });return true;
 }finally{lock.releaseLock();}
}
function exportCollectedColabTests(){
 if(!syncColabExams())throw Error('Collection is currently running. Wait a moment and run export again.');exportColabConfig_(examConfig_());
}
function exportColabConfig_(c){
 var book=SpreadsheetApp.openById(c.bookId),rows=book.getSheetByName('Collection').getDataRange().getValues().slice(1),jobs=[],blobs=[],issues=[];
 rows.forEach(function(r){if(r[10]==='REHEARSAL')return;if(r[10]!=='COLLECTED'){issues.push(r);return;}var file=DriveApp.getFileById(r[11]);var name=r[0]+'.ipynb';blobs.push(file.getBlob().setName(name));jobs.push({response_id:r[0],cohort:r[1],assessment:r[2],variant:r[3],full_name:r[4],email:r[5],email_verified:true,student_registration_number:r[6],submitted_at:r[7],opens_at:r[8],closes_at:r[9],notebook_sha256:r[12],file:name});});
 blobs.push(Utilities.newBlob(JSON.stringify({schema:1,exported_at:new Date().toISOString(),jobs:jobs,collection_issues:issues},null,2),'application/json','manifest.json'));
 var zip=DriveApp.getFolderById(c.folderId).createFile(Utilities.zip(blobs,'IUEA-test-batch-'+Utilities.formatDate(new Date(),'Africa/Kampala','yyyyMMdd-HHmmss')+'.zip'));
 console.log('DOWNLOAD BATCH: https://drive.google.com/file/d/'+zip.getId()+'/view');console.log(jobs.length+' collected notebooks; '+issues.length+' collection issues. Workbook: '+book.getUrl());
}

// Separate rehearsal form, workbook and snapshot folder; never mixed with student marks.
function prepareColabRehearsal(){
 var saved=PropertiesService.getScriptProperties().getProperty('IUEA_COLAB_QA_V1');
 var c=saved?JSON.parse(saved):null;
 if(!c){
  var source=examConfig_().forms['CML3111|TEST1'];
  var copy=DriveApp.getFileById(source.formId).makeCopy('REHEARSAL ONLY — Colab submission test');
  var f=FormApp.openById(copy.getId());
  var b=SpreadsheetApp.create('IUEA REHEARSAL ONLY — test collection');
  f.setDestination(FormApp.DestinationType.SPREADSHEET,b.getId());
  var items={},prefill=f.createResponse();
  f.getItems(FormApp.ItemType.TEXT).forEach(function(i){items[i.getTitle()]=i.getId();prefill.withItemResponse(i.asTextItem().createResponse('PLACEHOLDER_'+i.getId()));});
  c={bookId:b.getId(),folderId:DriveApp.createFolder('IUEA REHEARSAL snapshots').getId(),forms:{}};
  c.forms['CML3111|TEST1']={formId:f.getId(),url:f.getPublishedUrl(),prefill:prefill.toPrefilledUrl(),items:items};
  examSheet_(b,'Collection',EXAM_COLUMNS);
  examSheet_(b,'Test windows',['assessment_key','opens_at','closes_at','enabled']);
  // Rehearsal collection runs at export; reserve trigger quota for real tests.
  PropertiesService.getScriptProperties().setProperty('IUEA_COLAB_QA_V1',JSON.stringify(c));
 }
 var sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows');
 sheet.getRange('B:C').setNumberFormat('@');
 sheet.getRange(2,1,1,4).setValues([['CML3111|TEST1',new Date(Date.now()-60000).toISOString(),new Date(Date.now()+7200000).toISOString(),'YES']]);
 var form=FormApp.openById(c.forms['CML3111|TEST1'].formId);if(typeof form.setPublished==='function')form.setPublished(true);form.setAcceptingResponses(true);
 console.log('QA_CONFIG '+JSON.stringify({lecturer_email:EXAM_OWNER,forms:c.forms}));
 console.log('QA_WORKBOOK https://docs.google.com/spreadsheets/d/'+c.bookId+'/edit');
}
function collectQAColabExamResponse(e){var c=JSON.parse(PropertiesService.getScriptProperties().getProperty('IUEA_COLAB_QA_V1'));var lock=LockService.getScriptLock();lock.waitLock(30000);try{examCollect_(e.response,'CML3111|TEST1',c);}finally{lock.releaseLock();}}
function exportQAColabTests(){var c=JSON.parse(PropertiesService.getScriptProperties().getProperty('IUEA_COLAB_QA_V1'));FormApp.openById(c.forms['CML3111|TEST1'].formId).getResponses().forEach(function(r){examCollect_(r,'CML3111|TEST1',c);});exportColabConfig_(c);}
function closeColabRehearsal(){var c=JSON.parse(PropertiesService.getScriptProperties().getProperty('IUEA_COLAB_QA_V1'));FormApp.openById(c.forms['CML3111|TEST1'].formId).setAcceptingResponses(false);}
function verifyColabExamCollection(){
 var c=examConfig_(),triggers=ScriptApp.getProjectTriggers();
 console.log('SCHEDULER '+triggers.filter(function(t){return t.getHandlerFunction()==='syncColabExams';}).length);
 Object.keys(c.forms).forEach(function(key){var id=c.forms[key].formId;var count=triggers.filter(function(t){return t.getHandlerFunction()==='collectColabExamResponse'&&t.getTriggerSourceId()===id;}).length;console.log(key+' submission trigger='+count+' accepting='+FormApp.openById(id).isAcceptingResponses());});
}

function examAllocation_(code,key,reg,email,c){
 var required=PropertiesService.getScriptProperties().getProperty('IUEA_PORTAL_REQUIRED_V1')==='YES';
 if(/^[ABC]$/.test(code)&&!required)return {variant:code,code:''};
 var sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test allocations');
 if(!sheet)throw Error('Get your test files from the lecturer’s test entry link first.');
 var rows=sheet.getDataRange().getValues().slice(1),r=rows.filter(function(x){return x[0]===key&&x[3]===code;})[0];
 if(!r||String(r[1])!==String(reg).trim().toUpperCase()||String(r[2]).toLowerCase()!==email.toLowerCase()||!/^[ABC]$/.test(r[4]))throw Error('Test allocation does not match your registration number and Google email. Use your issued notebook and the same account.');
 return {variant:r[4],code:code};
}
function enableTestPortalCollection(){
 var c=examConfig_();
 Object.keys(c.forms).forEach(function(key){var f=FormApp.openById(c.forms[key].formId);f.getItems(FormApp.ItemType.TEXT).forEach(function(item){var t=item.asTextItem();if(t.getTitle()==='Variant'||t.getTitle()==='Test allocation code')t.setTitle('Test allocation code').setHelpText('Automatically filled by your issued notebook. Do not change this code.');});});
 PropertiesService.getScriptProperties().setProperty('IUEA_PORTAL_REQUIRED_V1','YES');
 console.log('Test forms now require a matching private portal allocation. Existing collected attempts remain unchanged.');
}

// Keep the synthetic portal verification attempt in the audit, outside student batches.
function archivePortalRehearsal(){
 var s=SpreadsheetApp.openById(examConfig_().bookId).getSheetByName('Collection');
 var rows=s.getDataRange().getValues();
 rows.forEach(function(r,i){if(r[0]==='2_ABaOnucErCJWtrUJ5QIk9pt_P22bRhZm6nqe2Li0vTcYyr5VIZ1viWAb6n2zcNRcqPdXOIk'&&r[4]==='QA Portal Rehearsal'){s.getRange(i+1,11).setValue('REHEARSAL');s.getRange(i+1,15).setValue('Synthetic portal verification only. Excluded from student batches.');console.log('Synthetic rehearsal retained in audit and excluded from student batches.');}});
}
