/** Instructor requested one hour from activation on 7 October. Idempotent retries. */
function reopenCML3112Quiz3OneHourOctober7(){
 var p=PropertiesService.getScriptProperties(),key='CML3112|3',prop='CML3112_Q3_HOUR_20261007';
 var links=loadLinks_(),r=links[key];if(!r){throw Error('Quiz not found');}
 var f=FormApp.openById(r.formId),pub=publishForm_(f);
 if(pub!=='ok'&&pub!=='unsupported'){throw Error(pub);}
 var cfg=JSON.parse(p.getProperty(prop)||'null');
 if(!cfg){cfg={start:Date.now()};cfg.end=cfg.start+3600000;p.setProperty(prop,JSON.stringify(cfg));}
 if(Date.now()>=cfg.end){throw Error('Authorized hour expired');}
 f.setAcceptingResponses(true);
 r.openedAt=cfg.start;r.closeAt=cfg.end;links[key]=r;saveLinks_(links);
 addPending_(r.formId,cfg.end,key);if(!ensureCloseTrigger_()){throw Error('Close timer failed');}
 var handler='closeCML3112Quiz3HourOctober7';
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){
  ScriptApp.newTrigger(handler).timeBased().at(new Date(cfg.end)).create();
 }
 Logger.log('QUIZ3_ONE_HOUR '+JSON.stringify({key:key,openedAt:new Date(cfg.start).toISOString(),closeAt:new Date(cfg.end).toISOString(),accepting:f.isAcceptingResponses(),url:r.short||r.live}));
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function closeCML3112Quiz3HourOctober7(){
 var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('CML3112_Q3_HOUR_20261007')||'null');
 if(!cfg||Date.now()<cfg.end){return;}
 var r=loadLinks_()['CML3112|3'];if(r.closeAt===cfg.end){
  FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();
 }
}
