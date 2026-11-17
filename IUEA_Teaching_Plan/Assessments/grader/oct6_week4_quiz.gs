/** Fixed 24-hour Week 4 window, authorised for 6 October at 11:00 Kampala. */
function scheduleCML3112Quiz4October6(){
 var start=Date.parse('2026-10-06T11:00:00+03:00'),end=start+86400000;
 if(Date.now()>=end){throw Error('Requested window expired');}
 var links=loadLinks_(),r=links['CML3112|4'];if(!r){throw Error('Quiz not found');}
 var f=FormApp.openById(r.formId);var pub=publishForm_(f);if(pub!=='ok'&&pub!=='unsupported'){throw Error(pub);}
 if(Date.now()<start){
  f.setAcceptingResponses(false);
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='activateCML3112Quiz4October6';})){
   ScriptApp.newTrigger('activateCML3112Quiz4October6').timeBased().at(new Date(start)).create();
  }
 }else{activateCML3112Quiz4October6();}
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeCML3112Quiz4October7';})){
  ScriptApp.newTrigger('closeCML3112Quiz4October7').timeBased().at(new Date(end)).create();
 }
 Logger.log('QUIZ4_SCHEDULED '+JSON.stringify({key:'CML3112|4',openAt:new Date(start).toISOString(),closeAt:new Date(end).toISOString(),accepting:f.isAcceptingResponses(),url:r.short||r.live}));
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function activateCML3112Quiz4October6(){
 var start=Date.parse('2026-10-06T11:00:00+03:00'),end=start+86400000;
 if(Date.now()<start||Date.now()>=end){return;}
 var links=loadLinks_(),r=links['CML3112|4'];
 FormApp.openById(r.formId).setAcceptingResponses(true);
 r.openedAt=start;r.closeAt=end;links['CML3112|4']=r;saveLinks_(links);
 addPending_(r.formId,end,'CML3112|4');if(!ensureCloseTrigger_()){throw Error('Close timer not installed');}
 Logger.log('QUIZ4_OPEN '+JSON.stringify(r));
}
function closeCML3112Quiz4October7(){
 var r=loadLinks_()['CML3112|4'],end=Date.parse('2026-10-07T11:00:00+03:00');
 if(Date.now()>=end&&r.closeAt===end){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();}
}
function auditIUEAQuizzesOctober6(){
 var links=loadLinks_();
 Object.keys(links).filter(function(k){return /^CML311[123]\|/.test(k);}).sort().forEach(function(k){
  var r=links[k];try {Logger.log('QUIZ '+JSON.stringify({key:k,accepting:FormApp.openById(r.formId).isAcceptingResponses(),openedAt:r.openedAt,closeAt:r.closeAt,url:r.short||r.live}));}
  catch(e){Logger.log('AUDIT_ERROR '+k+' '+e.message);}
 });
 closeStatus();
}
