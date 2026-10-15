/** Authorized 29 September reopening. Retries retain each activation deadline. */
function openCML3112QuizzesSept29(){
  var p=PropertiesService.getScriptProperties(),property='CML3112_QUIZZES_20260929';
  var cfg=JSON.parse(p.getProperty(property)||'{}');
  if(WINDOW_HOURS!==24){throw Error('Expected the 24-hour quiz policy');}
  var old=JSON.parse(p.getProperty(W3_LAUNCH_PROPERTY)||'null');
  if(old&&old.status!=='closed'){throw Error('Resolve the older Week 3 launch before reopening');}
  [3,4].forEach(function(w){
    var k='CML3112|'+w,links=loadLinks_(),L=links[k];
    if(!L){throw Error('Missing quiz '+k);}
    var f=FormApp.openById(L.formId),pub=publishForm_(f);
    if(pub!=='ok'&&pub!=='unsupported'){throw Error('Cannot publish '+k);}
    if(!cfg[k]){
      var now=Date.now();
      cfg[k]={openedAt:now,closeAt:now+86400000,previousOpenedAt:L.openedAt||null,previousCloseAt:L.closeAt||null};
      p.setProperty(property,JSON.stringify(cfg));
    }
    var r=cfg[k];
    if(Date.now()>=r.closeAt){throw Error('Window expired; a new opening requires lecturer authorization');}
    // Preserve the original sitting and all previous responses.
    if(!L.openedAt){L.openedAt=r.openedAt;}
    L.catchupOpenedAt=r.openedAt;L.closeAt=r.closeAt;links[k]=L;saveLinks_(links);
    var baseKey=property+'_DESCRIPTION_'+w,base=p.getProperty(baseKey);
    if(base===null){base=f.getDescription();p.setProperty(baseKey,base);}
    f.setDescription('Current deadline: '+Utilities.formatDate(new Date(r.closeAt),'Africa/Kampala','EEE d MMM yyyy HH:mm:ss')+' Kampala. This activation lasts 24 hours. Submit before the deadline.\n\n'+base);
    addPending_(L.formId,r.closeAt,k);
    if(!ensureCloseTrigger_()){throw Error('Automatic closing could not be scheduled');}
    var handler='closeCML3112QuizzesSept29';
    if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){
      ScriptApp.newTrigger(handler).timeBased().everyMinutes(5).create();
      ScriptApp.newTrigger(handler).timeBased().at(new Date(r.closeAt)).create();
    }
    f.setAcceptingResponses(true);
  });
  statusCML3112QuizzesSept29();
}
function closeCML3112QuizzesSept29(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('CML3112_QUIZZES_20260929')||'{}');
  var links=loadLinks_(),remaining=false;
  Object.keys(cfg).forEach(function(k){
    var r=cfg[k],L=links[k];
    if(Date.now()<r.closeAt){remaining=true;return;}
    // An explicitly authorized later window must not be closed by this handler.
    if(L&&Number(L.closeAt)===r.closeAt){closeQuiz(Number(k.split('|')[1]),'CML3112');}
  });
  if(!remaining){ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeCML3112QuizzesSept29';}).forEach(function(t){ScriptApp.deleteTrigger(t);});}
}
function statusCML3112QuizzesSept29(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('CML3112_QUIZZES_20260929')||'{}'),links=loadLinks_();
  [3,4].forEach(function(w){var k='CML3112|'+w,L=links[k],r=cfg[k];
    Logger.log('QUIZ_WINDOW '+JSON.stringify({key:k,formId:L.formId,openedAt:r?new Date(r.openedAt).toISOString():null,closeAt:L.closeAt?new Date(L.closeAt).toISOString():null,url:L.short||L.live,accepting:FormApp.openById(L.formId).isAcceptingResponses()}));
  });
  Logger.log('QUIZ_TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
