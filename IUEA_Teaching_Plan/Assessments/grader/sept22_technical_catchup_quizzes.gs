/** Instructor-authorized technical-issue catch-up. Run once; retries do not extend it. */
function reopenTechnicalCatchupQuizzesSept22(){
  var p=PropertiesService.getScriptProperties(),key='TECH_CATCHUP_20260922_QUIZZES';
  var cfg=JSON.parse(p.getProperty(key)||'null');
  if(!cfg){cfg={openedAt:Date.now(),previous:{}};cfg.closeAt=cfg.openedAt+86400000;p.setProperty(key,JSON.stringify(cfg));}
  if(Date.now()>=cfg.closeAt){throw Error('Catch-up expired; new authorization required.');}
  if(WINDOW_HOURS!==24){throw Error('Expected 24-hour quiz policy');}
  [1,2].forEach(function(w){
    var links=loadLinks_(),k='CML3112|'+w,L=links[k];
    if(!L){throw Error('Missing '+k);}
    if(!cfg.previous[k]){cfg.previous[k]={openedAt:L.openedAt,closeAt:L.closeAt};p.setProperty(key,JSON.stringify(cfg));}
    var f=FormApp.openById(L.formId),pub=publishForm_(f);
    if(pub!=='ok'&&pub!=='unsupported'){throw Error('Publication failed '+k);}
    // Preserve the original sitting metadata; showScores still recognizes earlier attempts.
    L.closeAt=cfg.closeAt;L.catchupOpenedAt=cfg.openedAt;links[k]=L;saveLinks_(links);
    var desc=f.getDescription().replace(/Deadline: .*? Kampala\./g,'').replace(/Deadline: .*?\(Kampala UTC\+03:00\)\.?/g,'');
    f.setDescription('Technical-issue catch-up: submit before '+Utilities.formatDate(new Date(cfg.closeAt),'Africa/Kampala','EEE d MMM yyyy HH:mm:ss')+' Kampala (24-hour reopening).\n\n'+desc);
    addPending_(L.formId,cfg.closeAt,k);f.setAcceptingResponses(true);
    Logger.log('CATCHUP_QUIZ '+JSON.stringify({key:k,formId:L.formId,accepting:f.isAcceptingResponses(),openedAt:new Date(cfg.openedAt).toISOString(),closeAt:new Date(cfg.closeAt).toISOString(),url:L.short||L.live}));
  });
  ensureCloseTrigger_();
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeTechnicalCatchupQuizzesSept22';})){
    ScriptApp.newTrigger('closeTechnicalCatchupQuizzesSept22').timeBased().at(new Date(cfg.closeAt)).create();
    ScriptApp.newTrigger('closeTechnicalCatchupQuizzesSept22').timeBased().everyMinutes(1).create();
  }
}
function closeTechnicalCatchupQuizzesSept22(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('TECH_CATCHUP_20260922_QUIZZES')||'null');
  if(!cfg||Date.now()<cfg.closeAt){return;}
  [1,2].forEach(function(w){closeQuiz(w,'CML3112');});
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeTechnicalCatchupQuizzesSept22';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
}
