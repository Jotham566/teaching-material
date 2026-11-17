function correctCML3113A4Wednesday(){
 var key='CML3113|W04',r=submissionState_()[key],end='2026-10-21T17:59:00+03:00';
 if(!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r))throw Error('A4 not ready');
 Logger.log('Previous deadline: '+r.closeAt);
 setSubmissionWindow(key,r.openAt,end);
 var sh=submissionBook_().getSheetByName('Assignment links');sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3113'&&v[1]==='A4')sh.getRange(i+1,5).setValue(end);});
 FormApp.openById(r.formId).setAcceptingResponses(Date.now()<Date.parse(end));ensureSubmissionTrigger_();
 ScriptApp.getProjectTriggers().forEach(function(t){if(t.getHandlerFunction()==='closeCML3113A4Wednesday')ScriptApp.deleteTrigger(t);});
 ScriptApp.newTrigger('closeCML3113A4Wednesday').timeBased().at(new Date(end)).create();
 Logger.log(JSON.stringify({key:key,accepting:FormApp.openById(r.formId).isAcceptingResponses(),closeAt:submissionState_()[key].closeAt,url:r.url,closeTimer:ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='closeCML3113A4Wednesday';})}));
}
function closeCML3113A4Wednesday(){var r=submissionState_()['CML3113|W04'];if(r.closeAt==='2026-10-21T17:59:00+03:00'&&Date.now()>=Date.parse(r.closeAt))FormApp.openById(r.formId).setAcceptingResponses(false);}
