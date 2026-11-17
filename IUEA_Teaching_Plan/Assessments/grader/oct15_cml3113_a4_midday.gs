function scheduleA4MiddayOctober15(){
 var key='CML3113|W04',start='2026-10-15T12:00:00+03:00',end='2026-10-22T12:00:00+03:00',r=submissionState_()[key];
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r))throw Error('A4 not ready');
 setSubmissionWindow(key,start,end);
 var sh=submissionBook_().getSheetByName('Assignment links');sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3113'&&v[1]==='A4')sh.getRange(i+1,4,1,2).setValues([[start,end]]);});
 FormApp.openById(r.formId).setAcceptingResponses(Date.now()>=Date.parse(start)&&Date.now()<Date.parse(end));ensureSubmissionTrigger_();
 var names=['openA4MiddayOctober15','closeA4MiddayOctober22'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 [[names[0],start],[names[1],end]].forEach(function(v){if(Date.parse(v[1])>Date.now())ScriptApp.newTrigger(v[0]).timeBased().at(new Date(v[1])).create();});
 Logger.log(JSON.stringify({key:key,openAt:start,closeAt:end,accepting:FormApp.openById(r.formId).isAcceptingResponses(),url:r.url}));
 Logger.log(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}));
}
function openA4MiddayOctober15(){syncSubmissions();}
function closeA4MiddayOctober22(){var r=submissionState_()['CML3113|W04'];if(Date.now()>=Date.parse(r.closeAt)&&r.closeAt==='2026-10-22T12:00:00+03:00')FormApp.openById(r.formId).setAcceptingResponses(false);}
