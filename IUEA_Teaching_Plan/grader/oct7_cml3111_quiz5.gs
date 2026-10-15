/** Fixed 24-hour Week 5 window, authorised for 7 October at actual activation, 08:41:19 Kampala. */
function scheduleCML3111Quiz5October7(){
 var start=Date.parse('2026-10-07T08:41:19+03:00'),end=start+86400000;
 if(Date.now()>=end){throw Error('Requested window expired');}
 var links=loadLinks_(),r=links['CML3111|5'];if(!r){throw Error('Quiz not found');}
 var f=FormApp.openById(r.formId);var pub=publishForm_(f);if(pub!=='ok'&&pub!=='unsupported'){throw Error(pub);}
 if(Date.now()<start){
  f.setAcceptingResponses(false);
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='activateCML3111Quiz5October7';})){
   ScriptApp.newTrigger('activateCML3111Quiz5October7').timeBased().at(new Date(start)).create();
  }
 }else{activateCML3111Quiz5October7();}
 ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeCML3111Quiz5October8';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeCML3111Quiz5October8';})){
  ScriptApp.newTrigger('closeCML3111Quiz5October8').timeBased().at(new Date(end)).create();
 }
 Logger.log('QUIZ5_SCHEDULED '+JSON.stringify({key:'CML3111|5',openAt:new Date(start).toISOString(),closeAt:new Date(end).toISOString(),accepting:f.isAcceptingResponses(),url:r.short||r.live}));
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function activateCML3111Quiz5October7(){
 var start=Date.parse('2026-10-07T08:41:19+03:00'),end=start+86400000;
 if(Date.now()<start||Date.now()>=end){return;}
 var links=loadLinks_(),r=links['CML3111|5'];
 FormApp.openById(r.formId).setAcceptingResponses(true);
 r.openedAt=start;r.closeAt=end;links['CML3111|5']=r;saveLinks_(links);
 addPending_(r.formId,end,'CML3111|5');if(!ensureCloseTrigger_()){throw Error('Close timer not installed');}
 Logger.log('QUIZ5_OPEN '+JSON.stringify(r));
}
function closeCML3111Quiz5October8(){
 var r=loadLinks_()['CML3111|5'],end=Date.parse('2026-10-08T08:41:19+03:00');
 if(Date.now()>=end&&r.closeAt===end){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();}
}
