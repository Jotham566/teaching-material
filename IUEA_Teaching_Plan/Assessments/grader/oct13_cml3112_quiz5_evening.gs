function scheduleQuiz5EveningOctober13(){
 var start=Date.parse('2026-10-13T18:00:00+03:00'),end=start+86400000,r=loadLinks_()['CML3112|5'];
 if(Date.now()>=end)throw Error('Window expired');
 var f=FormApp.openById(r.formId),pub=publishForm_(f);if(pub!=='ok'&&pub!=='unsupported')throw Error(pub);
 if(Date.now()<start){f.setAcceptingResponses(false);}else{openQuiz5EveningOctober13();}
 var names=['openQuiz5EveningOctober13','closeQuiz5EveningOctober14'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 [[names[0],start],[names[1],end]].forEach(function(v){if(v[1]>Date.now())ScriptApp.newTrigger(v[0]).timeBased().at(new Date(v[1])).create();});
 Logger.log(JSON.stringify({key:'CML3112|5',openAt:new Date(start).toISOString(),closeAt:new Date(end).toISOString(),accepting:f.isAcceptingResponses(),url:r.short||r.live}));
 Logger.log(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}));
}
function openQuiz5EveningOctober13(){
 var start=Date.parse('2026-10-13T18:00:00+03:00'),end=start+86400000;if(Date.now()<start||Date.now()>=end)return;
 var links=loadLinks_(),r=links['CML3112|5'];FormApp.openById(r.formId).setAcceptingResponses(true);r.openedAt=start;r.closeAt=end;saveLinks_(links);addPending_(r.formId,end,'CML3112|5');if(!ensureCloseTrigger_())throw Error('Close timer failed');
}
function closeQuiz5EveningOctober14(){var r=loadLinks_()['CML3112|5'],end=Date.parse('2026-10-14T18:00:00+03:00');if(Date.now()>=end&&r.closeAt===end){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();}}
