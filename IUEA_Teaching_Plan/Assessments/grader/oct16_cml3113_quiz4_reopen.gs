function reopenCML3113Quiz4October16(){
  var links=loadLinks_(),key='CML3113|4',r=links[key];
  if(!r||!r.formId)throw Error('Missing Quiz 4');
  var f=FormApp.openById(r.formId),pub=publishForm_(f);
  if(pub!=='ok'&&pub!=='unsupported')throw Error(pub);
  var names=['openQuiz4CML3113MiddayOctober15','closeQuiz4CML3113MiddayOctober16','closeCML3113Quiz4ReopenedOctober16'];
  ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
  f.setAcceptingResponses(true);
  var start=Date.now(),end=start+86400000;
  r.openedAt=start;r.closeAt=end;saveLinks_(links);
  addPending_(r.formId,end,key);
  ScriptApp.newTrigger('closeCML3113Quiz4ReopenedOctober16').timeBased().at(new Date(end)).create();
  if(!ensureCloseTrigger_())throw Error('Fallback close timer failed');
  Logger.log(JSON.stringify({key:key,accepting:f.isAcceptingResponses(),openedAt:new Date(start).toISOString(),closeAt:new Date(end).toISOString(),opensKampala:Utilities.formatDate(new Date(start),'Africa/Kampala','yyyy-MM-dd HH:mm:ss'),closesKampala:Utilities.formatDate(new Date(end),'Africa/Kampala','yyyy-MM-dd HH:mm:ss'),url:r.short||r.live}));
  Logger.log('Closing timer: '+ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeCML3113Quiz4ReopenedOctober16';}));
}
function closeCML3113Quiz4ReopenedOctober16(){
  var r=loadLinks_()['CML3113|4'];
  if(Date.now()>=r.closeAt){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);ensureCloseTrigger_();}
}
