/** Install in the lecturer collection project only, after deploying timed portal/collector. */
function scheduleTakeHomeTest1October23(){
 var c=examConfig_(),book=SpreadsheetApp.openById(c.bookId),sheet=book.getSheetByName('Test windows');
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  sheet.getRange(1,5).setValue('duration_minutes');
  var schedule={
   'CML3111|TEST1':['2026-10-23T19:00:00+03:00','2026-10-29T23:59:00+03:00'],
   'CML3113|TEST1':['2026-10-23T19:00:00+03:00','2026-10-29T23:59:00+03:00'],
   'CML3112|TEST1':['2026-10-27T19:00:00+03:00','2026-11-02T23:59:00+03:00']
  };
  var rows=sheet.getDataRange().getValues();
  Object.keys(schedule).forEach(function(key){
   var index=rows.findIndex(function(r){return r[0]===key;});if(index<1)throw Error('Missing window '+key);
   sheet.getRange(index+1,2,1,4).setValues([[schedule[key][0],schedule[key][1],'YES',180]]);
  });
  PropertiesService.getScriptProperties().setProperty('IUEA_PORTAL_REQUIRED_V1','YES');
 }finally{lock.releaseLock();}
 syncColabExams();
 verifyTakeHomeTest1October23();
}
function verifyTakeHomeTest1October23(){
 var c=examConfig_();
 ['CML3111','CML3112','CML3113'].forEach(function(cohort){var key=cohort+'|TEST1',w=examWindow_(key,c);console.log(key+' '+JSON.stringify(w)+' accepting='+FormApp.openById(c.forms[key].formId).isAcceptingResponses());});
 console.log('Scheduler triggers: '+ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='syncColabExams';}).length);
}
