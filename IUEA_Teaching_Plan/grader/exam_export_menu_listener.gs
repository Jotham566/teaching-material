/** Install in the existing assignment project with exam_collection.gs.
 * Uses the existing collection/export format for Test 1 and Test 2, all cohorts.
 */
function testExportSheet_(){
 var b=SpreadsheetApp.openById(examConfig_().bookId);
 return b.getSheetByName('Test Export')||b.insertSheet('Test Export');
}
function testExportProgress_(sheet,state,result){
 result=result||{};
 sheet.getRange('A1:B5').setValues([['Practical test export',state],['Notebooks',result.notebooks==null?'':result.notebooks],['Collection issues',result.issues==null?'':result.issues],['Updated',new Date().toISOString()],['Download / detail',result.url||result.detail||'Collecting submissions and preparing the ZIP.']]);
}
function installTestExportMenuListener(){
 var s=testExportSheet_();if(!s.getRange('A1').getValue())testExportProgress_(s,'READY',{detail:'Choose Export Test ZIP > Export latest submissions.'});
 var triggers=ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='processTestExportRequest';});
 if(!triggers.length)ScriptApp.newTrigger('processTestExportRequest').timeBased().everyMinutes(1).create();
 triggers.slice(1).forEach(function(t){ScriptApp.deleteTrigger(t);});
 console.log('Test export menu listener installed. Existing test windows are unchanged.');
}
function processTestExportRequest(){
 var s=testExportSheet_(),p=PropertiesService.getScriptProperties();
 // A terminated Apps Script invocation cannot run longer than this interval.
 // Surface a timeout for an explicit retry instead of leaving RUNNING forever.
 if(s.getRange('B1').getValue()==='RUNNING'&&Date.now()-Number(p.getProperty('TEST_EXPORT_STARTED'))>10*60000){
  testExportProgress_(s,'STOPPED',{detail:'Export timed out. Choose Export latest submissions to retry. Original submissions are preserved.'});
  s.getRange('E2').setValue('ERROR: timeout');return;
 }
 if(s.getRange('E2').getValue()!=='PENDING')return;
 var lock=LockService.getScriptLock();if(!lock.tryLock(1000))return;
 try{
  var rows=s.getRange('E1:E2').getValues(),request=String(rows[0][0]);
  if(!request||rows[1][0]!=='PENDING')return;
  var previous=JSON.parse(p.getProperty('TEST_EXPORT_COMPLETED')||'null');
  if(previous&&previous.request===request){testExportProgress_(s,'COMPLETE',previous.result);s.getRange('E2').setValue('ACCEPTED');return;}
  p.setProperty('TEST_EXPORT_STARTED',String(Date.now()));
  testExportProgress_(s,'RUNNING');SpreadsheetApp.flush();
  // Same lock as live collection prevents simultaneous copying of a receipt.
  syncColabExamsUnlocked_();
  var result=exportColabConfig_(examConfig_());
  p.setProperty('TEST_EXPORT_COMPLETED',JSON.stringify({request:request,result:result}));
  testExportProgress_(s,'COMPLETE',result);s.getRange('E2').setValue('ACCEPTED');
 }catch(e){testExportProgress_(s,'STOPPED',{detail:String(e)});s.getRange('E2').setValue('ERROR: '+String(e));throw e;}
 finally{lock.releaseLock();}
}
