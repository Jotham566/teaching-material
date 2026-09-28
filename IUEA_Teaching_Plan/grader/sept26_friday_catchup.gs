/** Authorized A1/A2 reopening for Friday cohorts; repeat runs retain the original expiry. */
function reopenFridayAssignmentsSept26(){
 var p=PropertiesService.getScriptProperties(),prop='FRIDAY_CATCHUP_20260926',cfg=JSON.parse(p.getProperty(prop)||'null');
 if(!cfg){cfg={start:Date.now(),previous:{}};cfg.end=cfg.start+86400000;p.setProperty(prop,JSON.stringify(cfg));}
 if(Date.now()>=cfg.end){throw Error('Catch-up window expired.');}
 ['CML3111|W01','CML3111|W02','CML3113|W01','CML3113|W02'].forEach(function(k){
  var r=submissionState_()[k];
  if(!r||!r.ready||!r.uploadReady||!(submissionAssessmentReleased_(k,r)||submissionCatchupCollectionAllowed_(k,r))){throw Error('Not ready for collection '+k);}
  if(!cfg.previous[k]){cfg.previous[k]={openAt:r.openAt,closeAt:r.closeAt};p.setProperty(prop,JSON.stringify(cfg));}
  setSubmissionWindow(k,cfg.previous[k].openAt,new Date(cfg.end).toISOString());
  var rows=submissionBook_().getSheetByName('Assignment links'),v=rows.getDataRange().getValues(),parts=k.split('|');
  v.forEach(function(row,i){if(row[0]===parts[0]&&row[1]===(parts[1]==='W01'?'A1':'A2')){rows.getRange(i+1,5).setValue(new Date(cfg.end).toISOString());}});
  var f=FormApp.openById(r.formId);if(!f.isAcceptingResponses()){throw Error('Still closed '+k);}
  Logger.log('REOPENED '+JSON.stringify({key:k,url:r.url,accepting:true,catchupStart:new Date(cfg.start).toISOString(),closeAt:new Date(cfg.end).toISOString()}));
 });
 ensureSubmissionTrigger_();
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeFridayCatchupSept26';})){
  ScriptApp.newTrigger('closeFridayCatchupSept26').timeBased().at(new Date(cfg.end)).create();
  ScriptApp.newTrigger('closeFridayCatchupSept26').timeBased().everyMinutes(1).create();
 }
}
function closeFridayCatchupSept26(){
 var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('FRIDAY_CATCHUP_20260926')||'null');
 if(!cfg||Date.now()<cfg.end){return;}
 var s=submissionState_();['CML3111|W01','CML3111|W02','CML3113|W01','CML3113|W02'].forEach(function(k){FormApp.openById(s[k].formId).setAcceptingResponses(false);});
 ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeFridayCatchupSept26';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
}
function auditAssignmentAutomationSept26(){
 var s=submissionState_();
 ['CML3111|W01','CML3111|W02','CML3113|W01','CML3113|W02','CML3111|W03','CML3113|W03','CML3112|W03'].forEach(function(k){var r=s[k];Logger.log('ASSIGNMENT_AUTOMATION '+JSON.stringify({key:k,openAt:r.openAt,closeAt:r.closeAt,ready:r.ready,uploadReady:r.uploadReady,allowed:submissionAssessmentReleased_(k,r)||submissionCatchupCollectionAllowed_(k,r),accepting:FormApp.openById(r.formId).isAcceptingResponses(),lastSuccess:r.lastSuccess,error:r.error||null}));});
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
