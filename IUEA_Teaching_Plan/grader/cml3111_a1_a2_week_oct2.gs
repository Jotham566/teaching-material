/** Lecturer requested one further week for CML3111 A1/A2 on 2 October 2026. */
function reopenCML3111A1A2ForWeekOctober2(){
 var p=PropertiesService.getScriptProperties(),prop='CML3111_A1_A2_WEEK_20261002';
 var keys=['CML3111|W01','CML3111|W02'],state=submissionState_();
 var sheet=submissionBook_().getSheetByName('Assignment links'),rows=sheet.getDataRange().getValues();
 keys.forEach(function(k){var r=state[k],label='A'+Number(k.split('|')[1].slice(1));
  if(!r||!r.ready||!r.uploadReady||!(submissionAssessmentReleased_(k,r)||submissionCatchupCollectionAllowed_(k,r))){throw Error('Not ready '+k);}
  if(rows.filter(function(v){return v[0]==='CML3111'&&v[1]===label;}).length!==1){throw Error('Expected one link row '+k);}
 });
 var cfg=JSON.parse(p.getProperty(prop)||'null');
 if(!cfg){cfg={start:Date.now(),previous:{}};cfg.end=cfg.start+7*86400000;keys.forEach(function(k){cfg.previous[k]={openAt:state[k].openAt,closeAt:state[k].closeAt};});p.setProperty(prop,JSON.stringify(cfg));}
 if(Date.now()>=cfg.end){throw Error('Authorized week has expired.');}
 keys.forEach(function(k){var r=state[k],end=new Date(cfg.end).toISOString(),label='A'+Number(k.split('|')[1].slice(1));
  setSubmissionWindow(k,r.openAt,end);
  rows.forEach(function(v,i){if(v[0]==='CML3111'&&v[1]===label){sheet.getRange(i+1,5).setValue(end);}});
  r=submissionState_()[k];if(Date.parse(r.closeAt)!==cfg.end||!FormApp.openById(r.formId).isAcceptingResponses()){throw Error('Opening verification failed '+k);}
  Logger.log('WEEK_REOPENED '+JSON.stringify({key:k,openAt:r.openAt,reopenedAt:new Date(cfg.start).toISOString(),closeAt:r.closeAt,url:r.url,accepting:true}));
 });
 ensureSubmissionTrigger_();var handler='closeCML3111A1A2WeekOctober2';
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){ScriptApp.newTrigger(handler).timeBased().at(new Date(cfg.end)).create();}
 Logger.log('CLOSING_TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function closeCML3111A1A2WeekOctober2(){
 var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('CML3111_A1_A2_WEEK_20261002')||'null');
 if(!cfg||Date.now()<cfg.end){return;}
 var s=submissionState_();['CML3111|W01','CML3111|W02'].forEach(function(k){var r=s[k];if(Date.parse(r.closeAt)===cfg.end){FormApp.openById(r.formId).setAcceptingResponses(false);}});
}
