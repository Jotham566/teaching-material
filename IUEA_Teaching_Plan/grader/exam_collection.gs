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
   form.setCollectEmail(true).setLimitOneResponsePerUser(true).setAllowResponseEdits(false);
   var names=['Full name','Student Registration Number','Variant','Snapshot file ID','Snapshot SHA-256'];var items={};
   names.forEach(function(name){var item=form.addTextItem().setTitle(name).setRequired(true);if(name==='Student Registration Number')item.clearValidation().setHelpText('Enter your own registration number exactly as on your university record. Any format is accepted.');items[name]=item.getId();});
   form.setConfirmationMessage('Your response has been recorded. The lecturer’s system will verify and collect the notebook snapshot. Keep your snapshot in Drive until grades are released. If the button or form reported an error, tell the invigilator immediately. Grades are calculated after the test. One submission is allowed per Google account and per Student Registration Number for this test. Review your work before submitting; responses cannot be edited. Contact your lecturer if a correction is needed.');
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
 return r?{open:String(r[1]),close:String(r[2]),enabled:String(r[3]).toUpperCase()==='YES',minutes:Number(r[4])||0}:{open:'',close:'',enabled:false};
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
   if(w.minutes){
    if(!allocation.started||!allocation.deadline||!isFinite(Date.parse(allocation.started))||!isFinite(Date.parse(allocation.deadline)))throw Error('No saved test timer. Start through the test entry page.');
    row[8]=allocation.started;row[9]=new Date(Math.min(Date.parse(allocation.deadline),Date.parse(w.close))).toISOString();
    if(Date.parse(stamp)<Date.parse(row[8])||Date.parse(stamp)>Date.parse(row[9])){row[10]='OUTSIDE_PERSONAL_WINDOW';row[14]='Submitted outside the saved three-hour test window.';sheet.appendRow(row.map(examText_));return;}
   }
   if(!/^[a-zA-Z0-9_-]{10,200}$/.test(row[13])||!/^[a-f0-9]{64}$/.test(row[12]))throw Error('Invalid snapshot reference');
   var file=DriveApp.getFileById(row[13]);
   var ownerEmail=String(file.getOwner().getEmail()||'');
   if(ownerEmail.toLowerCase()!==email.toLowerCase())throw Error('Snapshot owned by '+(ownerEmail||'unknown')+' but submitted by '+(email||'unknown')+'. Open the form and snapshot in the authorized Google account.');
   if(file.getSize()>10*1024*1024)throw Error('Notebook exceeds 10 MB');
   var blob=file.getBlob(),bytes=blob.getBytes();
   var hash=Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,bytes).map(function(b){return ('0'+((b+256)%256).toString(16)).slice(-2);}).join('');
   if(hash!==row[12])throw Error('Snapshot changed after preparation. Contact your lecturer; do not submit using another account.');
   var nb=JSON.parse(blob.getDataAsString());if(nb.nbformat!==4||!Array.isArray(nb.cells))throw Error('Snapshot is not a notebook');
   if(allocation.code&&(!nb.metadata||nb.metadata.iuea_allocation_code!==allocation.code))throw Error('Notebook does not match your issued test files. Return to the test entry page.');
   // This runs under the collector/export lock: only one accepted receipt per identity.
   var accepted=sheet.getLastRow()>1?sheet.getRange(2,1,sheet.getLastRow()-1,15).getValues():[];
   var duplicate=accepted.find(function(r){return r[1]===parts[0]&&r[2]===parts[1]&&r[10]==='COLLECTED'&&
    (String(r[5]).trim().toLowerCase()===email.trim().toLowerCase()||examRegistrationKey_(r[6])===examRegistrationKey_(row[6]));});
   if(duplicate){row[10]='DUPLICATE_SUBMISSION';row[14]='Already accepted receipt '+duplicate[0]+'. One submission per Google email and Student Registration Number per test. Contact your lecturer for any correction.';sheet.appendRow(row.map(examText_));return;}
   // Copy the bytes just verified, not the mutable source file a second time.
   var copy=DriveApp.getFolderById(c.folderId).createFile(Utilities.newBlob(bytes,'application/x-ipynb+json',response.getId()+'.ipynb'));
   row[11]=copy.getId();row[10]='COLLECTED';
  }
 }catch(e){row[10]='COLLECTION_ERROR';row[14]=String(e);}
 sheet.appendRow(row.map(examText_));
}
function collectColabExamResponse(e){var lock=LockService.getScriptLock();lock.waitLock(30000);try{var c=examConfig_();var key=Object.keys(c.forms).filter(function(k){return c.forms[k].formId===e.source.getId();})[0];if(!key)throw Error('Unknown test form');examCollect_(e.response,key,c);}finally{lock.releaseLock();}}
function examRegistrationKey_(value){return String(value||'').trim().toUpperCase().replace(/\s+/g,'');}
function examFormInstructions_(form,w){
 if(!form.hasLimitOneResponsePerUser())form.setLimitOneResponsePerUser(true);
 if(form.canEditResponse())form.setAllowResponseEdits(false);
 var text="Submit this form only through the link generated by the Submit test button in your own Colab notebook.\n\nGoogle may select the wrong account when multiple accounts are signed in. Before pressing Submit, check the Google account email shown in the banner at the top of this form. It must be the same account allocated on the test entry page and used to create your Colab snapshot. If it is different, use Switch account and select the allocated account; do not submit from another account.\n\n1. Check the Google email shown above. It must be the account you entered on the test entry page and used in Colab. Use Switch account if needed.\n2. Check your full name and Student Registration Number. Leave the prefilled test allocation code, snapshot ID and hash unchanged.\n3. Tick the email confirmation box and press Submit before your deadline. Wait for the confirmation page.\n\nNo manual notebook download or upload is required. Keep your saved snapshot unchanged in Drive until marks are released. The notebook button alone does not submit this form. If something fails, contact your lecturer immediately, before your deadline. Grades are calculated after the test. One submission is allowed per Google account and per Student Registration Number for this test. Review your work before submitting; responses cannot be edited. Contact your lecturer if a correction is needed.";
 if(isFinite(Date.parse(w.open))&&isFinite(Date.parse(w.close))){
  text+='\n\nOpens: '+Utilities.formatDate(new Date(w.open),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala. Closes: '+Utilities.formatDate(new Date(w.close),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala.';
 }
 if(w.minutes)text+='\n\nTAKE-HOME TEST: '+w.minutes+' minutes from Start test. Your personal deadline may be earlier than the class closing time above. Complete this form before your personal deadline shown on the entry page. A form confirmation does not override the deadline: late responses are retained for review but are not graded.';
 if(form.getDescription()!==text)form.setDescription(text);
 form.getItems(FormApp.ItemType.TEXT).forEach(function(item){var i=item.asTextItem();if(/^Snapshot /.test(i.getTitle())&&i.getHelpText()!=='Automatically filled by the notebook button. Do not change this value.')i.setHelpText('Automatically filled by the notebook button. Do not change this value.');});
}
function syncColabExams(){
 var lock=LockService.getScriptLock();if(!lock.tryLock(1000))return false;
 try{return syncColabExamsUnlocked_();}finally{lock.releaseLock();}
}
// Caller holds the assignment project's script lock.
function syncColabExamsUnlocked_(){
  var c=examConfig_(),ledger=SpreadsheetApp.openById(c.bookId).getSheetByName('Collection'),known={};
  if(ledger.getLastRow()>1)ledger.getRange(2,1,ledger.getLastRow()-1,1).getValues().forEach(function(r){known[r[0]]=true;});
  Object.keys(c.forms||{}).forEach(function(key){
   var f=FormApp.openById(c.forms[key].formId),w=examWindow_(key,c),now=Date.now();examFormInstructions_(f,w);
   var shouldOpen=w.enabled&&now>=Date.parse(w.open)&&now<=Date.parse(w.close);
   if(f.isAcceptingResponses()!==shouldOpen)f.setAcceptingResponses(shouldOpen);
   f.getResponses().forEach(function(r){if(!known[r.getId()]){examCollect_(r,key,c);known[r.getId()]=true;}});
  });return true;
}
function exportCollectedColabTests(){
 if(!syncColabExams())throw Error('Collection is currently running. Wait a moment and run export again.');exportColabConfig_(examConfig_());
}
function exportColabConfig_(c){
 var book=SpreadsheetApp.openById(c.bookId),rows=book.getSheetByName('Collection').getDataRange().getValues().slice(1),jobs=[],blobs=[],issues=[];
 rows.forEach(function(r){if(r[10]==='REHEARSAL')return;if(r[10]!=='COLLECTED'){issues.push(r);return;}var file=DriveApp.getFileById(r[11]);var name=r[0]+'.ipynb';blobs.push(file.getBlob().setName(name));jobs.push({response_id:r[0],cohort:r[1],assessment:r[2],variant:r[3],full_name:r[4],email:r[5],email_verified:true,student_registration_number:r[6],submitted_at:r[7],opens_at:r[8],closes_at:r[9],notebook_sha256:r[12],file:name});});
 blobs.push(Utilities.newBlob(JSON.stringify({schema:1,exported_at:new Date().toISOString(),jobs:jobs,collection_issues:issues,entry_identity_evidence:examEntryIdentity_(book)},null,2),'application/json','manifest.json'));
 var zip=DriveApp.getFolderById(c.folderId).createFile(Utilities.zip(blobs,'IUEA-test-batch-'+Utilities.formatDate(new Date(),'Africa/Kampala','yyyyMMdd-HHmmss')+'.zip'));
 console.log('DOWNLOAD BATCH: https://drive.google.com/file/d/'+zip.getId()+'/view');console.log(jobs.length+' collected notebooks; '+issues.length+' collection issues. Workbook: '+book.getUrl());
 return {url:'https://drive.google.com/file/d/'+zip.getId()+'/view',notebooks:jobs.length,issues:issues.length};
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
 if(!sheet)throw Error('Test allocation does not match: no issued allocation was found. Get your test files from the lecturer’s test entry link first.');
 var rows=sheet.getDataRange().getValues().slice(1),r=rows.filter(function(x){return x[0]===key&&x[3]===code;})[0];
 if(!r)throw Error('Test allocation does not match: allocation code is not issued for '+key+'. Use the notebook issued for this test.');
 var allocatedRegistration=String(r[1]||'').toUpperCase(),submittedRegistration=String(reg||'').trim().toUpperCase();
 var allocatedEmail=String(r[2]||'').toLowerCase(),submittedEmail=String(email||'').toLowerCase();
 if(allocatedRegistration!==submittedRegistration)throw Error('Test allocation does not match: allocation is for registration number '+(allocatedRegistration||'unknown')+' but the form reports '+(submittedRegistration||'unknown')+'. Use the details in your issued notebook.');
 if(allocatedEmail!==submittedEmail)throw Error('Test allocation email mismatch: allocated to '+(allocatedEmail||'unknown')+' but the form was submitted by '+(submittedEmail||'unknown')+'. Open the form using the authorized Google account.');
 if(!/^[ABC]$/.test(r[4]))throw Error('Test allocation does not match: assigned variant is invalid. Contact your lecturer.');
 return {variant:r[4],code:code,started:r[7]||'',deadline:r[8]||'',entry_name:r[6]||''};
}
function enableTestPortalCollection(){
 var c=examConfig_();
 Object.keys(c.forms).forEach(function(key){var f=FormApp.openById(c.forms[key].formId);f.getItems(FormApp.ItemType.TEXT).forEach(function(item){var t=item.asTextItem();if(t.getTitle()==='Variant'||t.getTitle()==='Test allocation code')t.setTitle('Test allocation code').setHelpText('Automatically filled by your issued notebook. Do not change this code.');});});
 PropertiesService.getScriptProperties().setProperty('IUEA_PORTAL_REQUIRED_V1','YES');
 console.log('Test forms now require a matching private portal allocation. Existing collected attempts remain unchanged.');
}

/*
 * Lecturer-only recovery for a genuine technical failure.
 *
 * Keep these functions in the private collector/gradebook Apps Script project.
 * They must never be copied to Portal.gs or a public web-app project.  A retry
 * does not delete the original form receipt, snapshot or Collection row: it
 * marks any accepted receipt as superseded, revokes the old allocation code,
 * clears the timer/notebook reference, and records the authorisation.  The
 * student must then return to the normal entry page with the same details.
 */
var EXAM_RETRY_HEADERS=['authorised_at','assessment_key','registration_normalized','old_email','new_email','old_allocation_code','new_allocation_code','reason','authorised_by','form_responses_removed'];
function examRetrySheet_(book){return examSheet_(book,'Test Retry Authorisations',EXAM_RETRY_HEADERS);}
function examRetryEmail_(email){
 email=String(email||'').trim().toLowerCase();
 if(email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))throw Error('Enter a valid replacement Google email, or leave it blank to keep the existing email.');
 return email;
}
function authoriseFreshTestAttempt(key,registration,reason,replacementEmail){
 key=String(key||'').trim();
 if(!/^CML311[123]\|TEST[12]$/.test(key))throw Error('Use an assessment key such as CML3111|TEST1.');
 var reg=examRegistrationKey_(registration),why=String(reason||'').trim();
 if(!reg)throw Error('Enter a Student ID/ Registration Number.');
 if(why.length<8)throw Error('Record a short reason for the technical retry (at least 8 characters).');
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_(),book=SpreadsheetApp.openById(c.bookId),allocations=book.getSheetByName('Test allocations');
  if(!allocations)throw Error('No Test allocations sheet exists yet.');
  var rows=allocations.getDataRange().getValues(),matches=[];
  rows.slice(1).forEach(function(row,index){if(row[0]===key&&examRegistrationKey_(row[1])===reg)matches.push({row:row,index:index+2});});
  if(matches.length!==1)throw Error(matches.length?'More than one allocation matches this registration number. Resolve the duplicate first.':'No issued allocation matches this registration number for '+key+'.');
  var match=matches[0],old=match.row,oldCode=String(old[3]||''),oldEmail=String(old[2]||'').trim().toLowerCase(),newEmail=examRetryEmail_(replacementEmail)||oldEmail;
  if(!newEmail)throw Error('The allocation has no Google email. Supply the replacement email before authorising a retry.');
  var form=c.forms&&c.forms[key];if(!form||!form.formId)throw Error('No submission form is configured for '+key+'.');
  var collection=book.getSheetByName('Collection'),receiptRows=collection&&collection.getLastRow()>1?collection.getRange(2,1,collection.getLastRow()-1,15).getValues():[];
  // Remove only this identity's prior form responses so Google Forms' one-response
  // setting cannot block the approved retry. Collection rows remain as audit data.
  var responseIds=[];receiptRows.forEach(function(r){
   if(r[1]+'|'+r[2]===key&&examRegistrationKey_(r[6])===reg&&r[0])responseIds.push(String(r[0]));
  });
  var liveForm=FormApp.openById(form.formId),removed=0;
  responseIds.forEach(function(id){try{liveForm.deleteResponse(id);removed++;}catch(e){throw Error('Could not clear the earlier form response '+id+'. No retry was authorised: '+String(e));}});
  // Preserve the old receipt/snapshot; it cannot be exported as the active attempt.
  if(collection&&receiptRows.length)receiptRows.forEach(function(r,index){
   if(r[1]+'|'+r[2]===key&&examRegistrationKey_(r[6])===reg&&r[10]==='COLLECTED'){
    collection.getRange(index+2,11).setValue('SUPERSEDED_FOR_RETRY');
    collection.getRange(index+2,15).setValue('Superseded by authorised technical retry at '+new Date().toISOString()+'. Reason: '+why);
   }
  });
  var newCode='T-'+Utilities.getUuid(),resetAt=new Date().toISOString();
  // Same variant, new allocation code. Clearing start/deadline/notebook makes the
  // portal issue one fresh timer and a fresh private notebook on the next visit.
  old[2]=newEmail;old[3]=newCode;old[5]=resetAt;old[7]='';old[8]='';old[9]='';old[11]='DIRECT';
  allocations.getRange(match.index,1,1,old.length).setValues([old]);
  var actor='';try{actor=Session.getActiveUser().getEmail()||'';}catch(ignore){}
  examRetrySheet_(book).appendRow([resetAt,key,reg,oldEmail,newEmail,oldCode,newCode,why,actor,removed]);
  SpreadsheetApp.flush();
  console.log('RETRY AUTHORISED '+JSON.stringify({key:key,registration:reg,email:newEmail,allocation:newCode,removed_form_responses:removed}));
  return {assessment:key,registration:reg,email:newEmail,new_allocation_code:newCode,form_responses_removed:removed};
 }finally{lock.releaseLock();}
}
// Convenience wrapper: provide only the registration number when it belongs to
// exactly one currently open test. If it is ambiguous, use authoriseFreshTestAttempt.
function authoriseFreshTestAttemptForRegistration(registration,reason,replacementEmail){
 var reg=examRegistrationKey_(registration),c=examConfig_(),book=SpreadsheetApp.openById(c.bookId),sheet=book.getSheetByName('Test allocations');
 if(!reg||!sheet)throw Error('Enter a registration number that has an issued test allocation.');
 var now=Date.now(),keys={};sheet.getDataRange().getValues().slice(1).forEach(function(r){
  if(examRegistrationKey_(r[1])!==reg)return;
  var w=examWindow_(r[0],c);if(w.enabled&&now>=Date.parse(w.open)&&now<=Date.parse(w.close))keys[r[0]]=true;
 });
 var choices=Object.keys(keys);
 if(choices.length!==1)throw Error(choices.length?'More than one open test matches this registration number. Use authoriseFreshTestAttempt with the assessment key.':'No single open test matches this registration number. Use authoriseFreshTestAttempt with the assessment key.');
 return authoriseFreshTestAttempt(choices[0],registration,reason,replacementEmail);
}
// Run this from the private Apps Script editor. It asks only for the student ID
// and reason, selects the single currently-open test, and logs the audit result.
function promptAuthoriseFreshTestAttempt(){
 var registration=Browser.inputBox('Authorise a fresh test attempt','Student ID / Registration Number:',Browser.Buttons.OK_CANCEL);
 if(registration==='cancel')return;
 var reason=Browser.inputBox('Authorise a fresh test attempt','Reason for this technical retry (recorded in the audit log):',Browser.Buttons.OK_CANCEL);
 if(reason==='cancel')return;
 var result=authoriseFreshTestAttemptForRegistration(registration,reason,'');
 Browser.msgBox('Fresh attempt authorised for '+result.registration+'. The student should return to the entry page with the same Google email.');
}

// Keep the synthetic portal verification attempt in the audit, outside student batches.
function archivePortalRehearsal(){
 var s=SpreadsheetApp.openById(examConfig_().bookId).getSheetByName('Collection');
 var rows=s.getDataRange().getValues();
 rows.forEach(function(r,i){if(r[0]==='2_ABaOnucErCJWtrUJ5QIk9pt_P22bRhZm6nqe2Li0vTcYyr5VIZ1viWAb6n2zcNRcqPdXOIk'&&r[4]==='QA Portal Rehearsal'){s.getRange(i+1,11).setValue('REHEARSAL');s.getRange(i+1,15).setValue('Synthetic portal verification only. Excluded from student batches.');console.log('Synthetic rehearsal retained in audit and excluded from student batches.');}});
}

// Names/emails entered at entry are self-declared until matched to a collected verified account.
function examEntryIdentity_(book){
 var sheet=book.getSheetByName('Test allocations');if(!sheet)return [];
 return sheet.getDataRange().getValues().slice(1).map(function(r){return {assessment_key:r[0],student_registration_number:r[1],email:r[2],allocation_code:r[3],full_name:r[6]||'',started_at:r[7]||'',personal_deadline:r[8]||'',email_verified:false};});
}

/** Apply the policy without deleting or altering existing responses or marks. */
function enforceSingleTestSubmission(){
 var c=examConfig_();
 Object.keys(c.forms).forEach(function(key){var f=FormApp.openById(c.forms[key].formId);examFormInstructions_(f,examWindow_(key,c));console.log(key+' one_response='+f.hasLimitOneResponsePerUser()+' edits='+f.canEditResponse());});
}
