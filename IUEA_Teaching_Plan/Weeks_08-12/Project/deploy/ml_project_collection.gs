/** Add this file to the lecturer-owned collector project (the one that holds exam_collection.gs), AFTER replacing exam_collection.gs with deploy/exam_collection.gs.
 * Creates the three ML_PROJECT Test windows rows with duration_minutes=180. Nothing is opened: every row is created with enabled NO and empty times.
 * The project has no Google Form: notebooks arrive through the submission web app (deploy/ml_project_pipeline.gs). Run installMlProjectCollection() once.
 */
var ML_PROJECT_MINUTES = 180;
function installMlProjectCollection(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_();
  if(!c.bookId)throw Error('Run installColabExamCollection first: the collector workbook does not exist yet.');
  var windows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows');
  if(!windows)throw Error('The Test windows sheet is missing.');
  var have=windows.getDataRange().getValues().map(function(r){return r[0];}),created=[];
  ['CML3111','CML3112','CML3113'].forEach(function(cohort){
   var key=cohort+'|ML_PROJECT';if(have.indexOf(key)>=0)return;
   windows.appendRow([key,'','','NO',ML_PROJECT_MINUTES]);created.push(key);
  });
  console.log('Test windows rows created: '+(created.join(', ')||'none (all three already existed)')+'. Every row is enabled NO. Nothing was opened.');
  console.log('Collector workbook id (BOOK_ID for the submission web app): '+c.bookId);
 }finally{lock.releaseLock();}
}
/** Read only. Logs the three ML_PROJECT Test windows rows so you can check the typed times and the duration. */
function showMlProjectWindows(){
 var c=examConfig_(),rows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows').getDataRange().getValues();
 rows.slice(1).filter(function(r){return /\|ML_PROJECT$/.test(r[0]);}).forEach(function(r){console.log(r[0]+' | opens '+r[1]+' | closes '+r[2]+' | enabled '+r[3]+' | minutes '+r[4]);});
}
/** Sets one project window. Run ONLY after you have confirmed the date with the students. confirm must be the word CONFIRMED.
 * The confirmed window (13 November 2026) is the same for all three courses:
 * setMlProjectWindow('CML3112','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED'), then CML3113 and CML3111, then run syncColabExams. */
function setMlProjectWindow(cohort,opensIso,closesIso,confirm){
 if(confirm!=='CONFIRMED')throw Error('Pass CONFIRMED as the fourth argument once the date is confirmed.');
 var key=String(cohort)+'|ML_PROJECT';
 if(!/^CML311[123]\|ML_PROJECT$/.test(key))throw Error('Use CML3111, CML3112 or CML3113.');
 if(!isFinite(Date.parse(opensIso))||!isFinite(Date.parse(closesIso))||Date.parse(closesIso)<=Date.parse(opensIso))throw Error('Use real dates with the Kampala offset, closing after opening.');
 if(Date.parse(closesIso)-Date.parse(opensIso)>72*3600000)throw Error('The window is more than 72 hours. The project window is 23 November 00:00 to 25 November 23:59.');
 if(Date.parse(closesIso)-Date.parse(opensIso)<ML_PROJECT_MINUTES*60000)throw Error('The window is shorter than 3 hours.');
 var c=examConfig_(),sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows'),rows=sheet.getDataRange().getValues();
 var at=rows.findIndex(function(r,i){return i>0&&r[0]===key;});
 if(at<0)throw Error('No Test windows row for '+key+'. Run installMlProjectCollection first.');
 sheet.getRange(at+1,1,1,5).setValues([[key,opensIso,closesIso,'YES',ML_PROJECT_MINUTES]]);
 console.log('Window set for '+key+': '+opensIso+' to '+closesIso+', '+ML_PROJECT_MINUTES+' minutes. Run syncColabExams to open the form.');
}
