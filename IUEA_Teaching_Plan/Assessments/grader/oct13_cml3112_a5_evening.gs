function scheduleA5EveningOctober13(){
 var key='CML3112|W05',start='2026-10-13T18:00:00+03:00',end='2026-10-20T18:00:00+03:00',r=submissionState_()[key];
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r))throw Error('A5 not ready');
 setSubmissionWindow(key,start,end);
 var sh=submissionBook_().getSheetByName('Assignment links');sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3112'&&v[1]==='A5')sh.getRange(i+1,4,1,2).setValues([[start,end]]);});
 FormApp.openById(r.formId).setAcceptingResponses(Date.now()>=Date.parse(start)&&Date.now()<Date.parse(end));ensureSubmissionTrigger_();
 var names=['openA5EveningOctober13','closeA5EveningOctober20'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 [[names[0],start],[names[1],end]].forEach(function(v){if(Date.parse(v[1])>Date.now())ScriptApp.newTrigger(v[0]).timeBased().at(new Date(v[1])).create();});
 Logger.log(JSON.stringify({key:key,openAt:start,closeAt:end,accepting:FormApp.openById(r.formId).isAcceptingResponses(),url:r.url}));
 Logger.log(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}));
}
function openA5EveningOctober13(){syncSubmissions();}
function closeA5EveningOctober20(){var r=submissionState_()['CML3112|W05'];if(Date.now()>=Date.parse(r.closeAt)&&r.closeAt==='2026-10-20T18:00:00+03:00')FormApp.openById(r.formId).setAcceptingResponses(false);}
