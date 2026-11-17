/** @OnlyCurrentDoc
 * Bound to the private test collection workbook. No Drive permissions required.
 */
function onOpen(){
 SpreadsheetApp.getUi().createMenu('Export Test ZIP')
  .addItem('Export latest submissions','requestTestExport')
  .addItem('View progress / download','showTestExport')
  .addToUi();
}
function showTestExport(){
 var b=SpreadsheetApp.getActiveSpreadsheet(),s=b.getSheetByName('Test Export');
 if(!s)throw Error('Test export listener has not been installed.');
 b.setActiveSheet(s);s.getRange('A1').activate();
}
function requestTestExport(){
 var lock=LockService.getDocumentLock();if(!lock.tryLock(5000))throw Error('Another request is being saved. Try again shortly.');
 try{
  var b=SpreadsheetApp.getActiveSpreadsheet(),s=b.getSheetByName('Test Export');
  if(!s)throw Error('Test export listener has not been installed.');
  if(s.getRange('E2').getValue()==='PENDING'||s.getRange('B1').getValue()==='RUNNING'){
   b.toast('An export is already queued or running. Check Test Export for progress.','Export Test ZIP',8);
  }else{
   s.getRange('D1:E3').setValues([['Export request',Utilities.getUuid()],['Request status','PENDING'],['Requested at',new Date().toISOString()]]);
   SpreadsheetApp.flush();b.toast('Request queued. Google normally starts within a minute. Wait for COMPLETE before downloading.','Export Test ZIP',10);
  }
  showTestExport();
 }finally{lock.releaseLock();}
}
