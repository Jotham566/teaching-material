/** Instructor-authorized upload catch-up, preserving earlier submission timestamps and grades. */
function reopenTechnicalCatchupAssignmentsSept22(){
  var p=PropertiesService.getScriptProperties(),key='TECH_CATCHUP_20260922_ASSIGNMENTS';
  var cfg=JSON.parse(p.getProperty(key)||'null');
  if(!cfg){cfg={openedAt:Date.now(),previous:{}};cfg.closeAt=cfg.openedAt+86400000;p.setProperty(key,JSON.stringify(cfg));}
  if(Date.now()>=cfg.closeAt){throw Error('Catch-up expired; new authorization required.');}
  ['W01','W02'].forEach(function(id){
    var k='CML3112|'+id,r=submissionState_()[k];
    if(!r||!r.ready||!r.uploadReady){throw Error('Upload not ready '+k);}
    if(!submissionAssessmentReleased_(k,r)&&!submissionCatchupCollectionAllowed_(k,r)){throw Error('Collection not released '+k);}
    if(!cfg.previous[k]){cfg.previous[k]={openAt:r.openAt,closeAt:r.closeAt};p.setProperty(key,JSON.stringify(cfg));}
    // Keep the original start so earlier valid submissions are not relabelled EARLY.
    setSubmissionWindow(k,cfg.previous[k].openAt,new Date(cfg.closeAt).toISOString());
    var sheet=submissionBook_().getSheetByName('Assignment links'),rows=sheet.getDataRange().getValues();
    rows.forEach(function(v,i){if(v[0]==='CML3112'&&v[1]===(id==='W01'?'A1':'A2')){sheet.getRange(i+1,5).setValue(new Date(cfg.closeAt).toISOString());}});
    r=submissionState_()[k];var f=FormApp.openById(r.formId);
    if(!f.isAcceptingResponses()){throw Error('Form did not reopen '+k);}
    Logger.log('CATCHUP_ASSIGNMENT '+JSON.stringify({key:k,accepting:true,catchupOpenedAt:new Date(cfg.openedAt).toISOString(),openAt:r.openAt,closeAt:r.closeAt,url:r.url}));
  });
  // Match the separately verified quiz window so catch-up scores are not discarded as late.
  var imports=JSON.parse(p.getProperty('QUIZ_IMPORT_SOURCES')||'{}');
  if(!p.getProperty('TECH_CATCHUP_20260922_IMPORTS_BEFORE')){p.setProperty('TECH_CATCHUP_20260922_IMPORTS_BEFORE',JSON.stringify(imports));}
  imports['CML3112|1']={formId:'1ASfefZ-HIFo22Jfq18wHv6Ua2Q311EpGmlBlZS4Gtf8',closeAt:'2026-09-23T13:01:20.264Z'};
  imports['CML3112|2']={formId:'1c_B10_ZKfYw7lVnRt7vsNfzV_mFfQ3jX9w7uvKyS3to',closeAt:'2026-09-23T13:01:20.264Z'};
  p.setProperty('QUIZ_IMPORT_SOURCES',JSON.stringify(imports));
  var oldCatchup=JSON.parse(p.getProperty('CML3112_W01_CATCHUP')||'null');
  if(oldCatchup){oldCatchup.closeAt=imports['CML3112|1'].closeAt;p.setProperty('CML3112_W01_CATCHUP',JSON.stringify(oldCatchup));}
  Logger.log('CATCHUP_IMPORTS '+JSON.stringify({'CML3112|1':imports['CML3112|1'],'CML3112|2':imports['CML3112|2']}));
  ensureSubmissionTrigger_();
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeTechnicalCatchupAssignmentsSept22';})){
    ScriptApp.newTrigger('closeTechnicalCatchupAssignmentsSept22').timeBased().at(new Date(cfg.closeAt)).create();
    ScriptApp.newTrigger('closeTechnicalCatchupAssignmentsSept22').timeBased().everyMinutes(1).create();
  }
}
function closeTechnicalCatchupAssignmentsSept22(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('TECH_CATCHUP_20260922_ASSIGNMENTS')||'null');
  if(!cfg||Date.now()<cfg.closeAt){return;}
  var state=submissionState_();
  ['W01','W02'].forEach(function(id){FormApp.openById(state['CML3112|'+id].formId).setAcceptingResponses(false);});
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeTechnicalCatchupAssignmentsSept22';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
}
