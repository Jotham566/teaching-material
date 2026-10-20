function extendCML3112A5ToFridayOctober23(){
 var key='CML3112|W05',end='2026-10-23T23:59:00+03:00',r=submissionState_()[key];
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r))throw Error('A5 not ready');
 if(Date.now()>=Date.parse(end))throw Error('Extension deadline has passed');
 var start=r.openAt,previous=r.closeAt;
 setSubmissionWindow(key,start,end);
 var sh=submissionBook_().getSheetByName('Assignment links'),matches=0;
 sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3112'&&v[1]==='A5'){sh.getRange(i+1,4,1,2).setValues([[start,end]]);matches++;}});
 if(matches!==1)throw Error('Expected one A5 links row, found '+matches);
 var form=FormApp.openById(r.formId);form.setAcceptingResponses(Date.now()>=Date.parse(start));ensureSubmissionTrigger_();
 ScriptApp.getProjectTriggers().forEach(function(t){if(['closeA5EveningOctober20','closeCML3112A5FridayOctober23'].indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 ScriptApp.newTrigger('closeCML3112A5FridayOctober23').timeBased().at(new Date(end)).create();
 var saved=submissionState_()[key];
 if(saved.closeAt!==end||saved.openAt!==start)throw Error('Saved schedule mismatch');
 Logger.log(JSON.stringify({key:key,previousDeadline:previous,openAt:saved.openAt,closeAt:saved.closeAt,accepting:form.isAcceptingResponses(),url:saved.url}));
 Logger.log('Verified deadline: Friday 23 October 2026, 11:59 PM Kampala. Assignment links row updated. Automatic closure scheduled.');
}
function closeCML3112A5FridayOctober23(){var r=submissionState_()['CML3112|W05'];if(r.closeAt==='2026-10-23T23:59:00+03:00'&&Date.now()>=Date.parse(r.closeAt))FormApp.openById(r.formId).setAcceptingResponses(false);}
