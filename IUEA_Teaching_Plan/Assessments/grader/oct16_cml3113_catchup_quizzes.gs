function openCML3113Catchup72Hours(){
 var links=loadLinks_(),before=JSON.stringify(links['CML3113|5']);
 [1,2,3,4].forEach(function(w){if(!links['CML3113|'+w])throw Error('Missing quiz '+w);});
 var props=PropertiesService.getScriptProperties(),start=Number(props.getProperty('OCT16_3113_CATCHUP_START'))||Date.now(),end=start+259200000;
 if(Date.now()>=end)throw Error('Window expired');props.setProperty('OCT16_3113_CATCHUP_START',String(start));
 var old=['openQuiz4CML3113MiddayOctober15','closeQuiz4CML3113MiddayOctober16','closeCML3113Quiz4ReopenedOctober16','closeCML3113Catchup72Hours'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(old.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 [1,2,3,4].forEach(function(w){var key='CML3113|'+w,r=links[key],f=FormApp.openById(r.formId),p=publishForm_(f);if(p!=='ok'&&p!=='unsupported')throw Error(p);r.openedAt=start;r.closeAt=end;addPending_(r.formId,end,key);f.setAcceptingResponses(true);Logger.log(key+' accepting='+f.isAcceptingResponses()+' '+(r.short||r.live));});
 saveLinks_(links);ScriptApp.newTrigger('closeCML3113Catchup72Hours').timeBased().at(new Date(end)).create();if(!ensureCloseTrigger_())throw Error('Close fallback failed');
 Logger.log('WINDOW '+new Date(start).toISOString()+' to '+new Date(end).toISOString());Logger.log('KAMPALA CLOSE '+Utilities.formatDate(new Date(end),'Africa/Kampala','yyyy-MM-dd HH:mm:ss'));
 Logger.log('Quiz5 unchanged='+ (JSON.stringify(loadLinks_()['CML3113|5'])===before));Logger.log('Close timer installed='+ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeCML3113Catchup72Hours';}));
}
function closeCML3113Catchup72Hours(){var end=Number(PropertiesService.getScriptProperties().getProperty('OCT16_3113_CATCHUP_START'))+259200000,links=loadLinks_();[1,2,3,4].forEach(function(w){var r=links['CML3113|'+w];if(r.closeAt===end&&Date.now()>=end){FormApp.openById(r.formId).setAcceptingResponses(false);removePending_(r.formId);}});ensureCloseTrigger_();}
