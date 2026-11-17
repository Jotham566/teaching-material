function scheduleFridayOctober16Quizzes(){
 var specs=fridayQuizSpecs_();
 specs.forEach(function(s){var r=loadLinks_()[s[0]];if(!r||!r.formId)throw Error('Missing '+s[0]);});
 var names=['openFridayQuiz3113','openFridayQuiz3111','closeFridayQuiz3113','closeFridayQuiz3111','openQuiz5CML3113MiddayOctober15','closeQuiz5CML3113MiddayOctober16'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 specs.forEach(function(s){
  var r=loadLinks_()[s[0]], f=FormApp.openById(r.formId), pub=publishForm_(f);if(pub!=='ok'&&pub!=='unsupported')throw Error(pub);
  removePending_(r.formId); f.setAcceptingResponses(false);
  ScriptApp.newTrigger(s[2]).timeBased().at(new Date(s[1])).create();
  ScriptApp.newTrigger(s[3]).timeBased().at(new Date(Date.parse(s[1])+86400000)).create();
  Logger.log(s[0]+' | opens '+s[1]+' | closes '+new Date(Date.parse(s[1])+86400000).toISOString()+' | currently accepting: '+f.isAcceptingResponses()+' | '+(r.short||r.live));
 });
 if(!ensureCloseTrigger_())throw Error('Existing close timer failed');
 Logger.log('VERIFIED triggers: '+ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}).join(', '));
}
function fridayQuizSpecs_(){return [['CML3113|5','2026-10-16T08:00:00+03:00','openFridayQuiz3113','closeFridayQuiz3113'],['CML3111|6','2026-10-16T11:00:00+03:00','openFridayQuiz3111','closeFridayQuiz3111']];}
function fridayQuizRun_(index,closing){
 var s=fridayQuizSpecs_()[index],start=Date.parse(s[1]),end=start+86400000,links=loadLinks_(),r=links[s[0]],now=Date.now();
 if(closing){if(now>=end&&r.closeAt===end){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();}return;}
 if(r.waived||s[0]==='CML3111|6'||now<start||now>=end)return;
 FormApp.openById(r.formId).setAcceptingResponses(true);r.openedAt=start;r.closeAt=end;saveLinks_(links);addPending_(r.formId,end,s[0]);if(!ensureCloseTrigger_())throw Error('Close timer failed');
}
function openFridayQuiz3113(){fridayQuizRun_(0,false);}
function openFridayQuiz3111(){fridayQuizRun_(1,false);}
function closeFridayQuiz3113(){fridayQuizRun_(0,true);}
function closeFridayQuiz3111(){fridayQuizRun_(1,true);}