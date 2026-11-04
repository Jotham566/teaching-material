/** Add this file to the lecturer-owned collector project (the one that holds exam_collection.gs), AFTER replacing exam_collection.gs with deploy/exam_collection.gs.
 * Creates the three ML_PROJECT submission forms exactly as installColabExamCollection created the Test 1 and Test 2 forms, and the three Test windows rows
 * with duration_minutes=180. Nothing is opened: every row is created with enabled NO and empty times. Run installMlProjectCollection() once.
 */
var ML_PROJECT_MINUTES = 180;
function installMlProjectCollection(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_();
  if(!c.bookId||!c.folderId)throw Error('Run installColabExamCollection first: the collector workbook does not exist yet.');
  c.forms=c.forms||{};
  var book=SpreadsheetApp.openById(c.bookId);
  var windows=book.getSheetByName('Test windows');
  if(!windows)throw Error('The Test windows sheet is missing.');
  var created=[];
  ['CML3111','CML3112','CML3113'].forEach(function(cohort){
   var key=cohort+'|ML_PROJECT';
   if(c.forms[key])return;
   var form=FormApp.create(cohort+' ML_PROJECT — Colab test submission');
   form.setDescription('Use the Submit test button at the end of your issued Colab notebook. It prepares the fields below. Sign in with the same Google account used in Colab. Submit before your personal deadline. Your exact notebook snapshot is copied to the lecturer’s private folder. No download or file upload is required.');
   form.setCollectEmail(true).setLimitOneResponsePerUser(true).setAllowResponseEdits(false);
   var names=['Full name','Student Registration Number','Variant','Snapshot file ID','Snapshot SHA-256'];var items={};
   names.forEach(function(name){var item=form.addTextItem().setTitle(name).setRequired(true);if(name==='Student Registration Number')item.clearValidation().setHelpText('Enter your own registration number exactly as on your university record. Any format is accepted.');items[name]=item.getId();});
   form.setConfirmationMessage('Your response has been recorded. The lecturer’s system will verify and collect the notebook snapshot. Keep your snapshot in Drive until grades are released. If the button or form reported an error, tell the lecturer immediately. Grades are calculated after the sitting. One submission is allowed per Google account and per Student Registration Number. Responses cannot be edited. Contact your lecturer if a correction is needed.');
   form.setDestination(FormApp.DestinationType.SPREADSHEET,c.bookId);
   if(typeof form.setPublished==='function')form.setPublished(true);
   form.setAcceptingResponses(false);
   var prefill=form.createResponse();form.getItems(FormApp.ItemType.TEXT).forEach(function(item){prefill.withItemResponse(item.asTextItem().createResponse('PLACEHOLDER_'+item.getId()));});
   c.forms[key]={formId:form.getId(),url:form.getPublishedUrl(),prefill:prefill.toPrefilledUrl(),items:items};examSave_(c);
   windows.appendRow([key,'','','NO',ML_PROJECT_MINUTES]);
   ScriptApp.newTrigger('collectColabExamResponse').forForm(form).onFormSubmit().create();
   created.push(key);
  });
  console.log('Created forms: '+(created.join(', ')||'none (all three already existed)')+'. Every Test windows row is enabled NO. Nothing was opened.');
  console.log('PUBLIC_NOTEBOOK_CONFIG '+JSON.stringify({lecturer_email:EXAM_OWNER,forms:c.forms}));
 }finally{lock.releaseLock();}
}
/** Read only. Logs the three ML_PROJECT Test windows rows so you can check the typed times and the duration. */
function showMlProjectWindows(){
 var c=examConfig_(),rows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows').getDataRange().getValues();
 rows.slice(1).filter(function(r){return /\|ML_PROJECT$/.test(r[0]);}).forEach(function(r){console.log(r[0]+' | opens '+r[1]+' | closes '+r[2]+' | enabled '+r[3]+' | minutes '+r[4]);});
}
/** Sets one project window. Run ONLY after you have confirmed the date with the students. confirm must be the word CONFIRMED.
 * Example: setMlProjectWindow('CML3112','2026-12-01T11:00:00+03:00','2026-12-01T14:00:00+03:00','CONFIRMED'). Then run syncColabExams. */
function setMlProjectWindow(cohort,opensIso,closesIso,confirm){
 if(confirm!=='CONFIRMED')throw Error('Pass CONFIRMED as the fourth argument once the date is confirmed.');
 var key=String(cohort)+'|ML_PROJECT';
 if(!/^CML311[123]\|ML_PROJECT$/.test(key))throw Error('Use CML3111, CML3112 or CML3113.');
 if(!isFinite(Date.parse(opensIso))||!isFinite(Date.parse(closesIso))||Date.parse(closesIso)<=Date.parse(opensIso))throw Error('Use real dates with the Kampala offset, closing after opening.');
 if(Date.parse(closesIso)-Date.parse(opensIso)>ML_PROJECT_MINUTES*60000+15*60000)throw Error('The window is more than 3 hours 15 minutes. The sitting window should be the class slot.');
 var c=examConfig_(),sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows'),rows=sheet.getDataRange().getValues();
 var at=rows.findIndex(function(r,i){return i>0&&r[0]===key;});
 if(at<0)throw Error('No Test windows row for '+key+'. Run installMlProjectCollection first.');
 sheet.getRange(at+1,1,1,5).setValues([[key,opensIso,closesIso,'YES',ML_PROJECT_MINUTES]]);
 console.log('Window set for '+key+': '+opensIso+' to '+closesIso+', '+ML_PROJECT_MINUTES+' minutes. Run syncColabExams to open the form.');
}
