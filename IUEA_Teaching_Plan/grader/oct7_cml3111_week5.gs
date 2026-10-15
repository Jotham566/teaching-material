/** Compensation class 7 October 08:30–11:30 Kampala; existing A5 deadline retained. */
function openCML3111A5October7(){
 var key='CML3111|W05',r=submissionState_()[key],start='2026-10-07T08:30:00+03:00';
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r)){throw Error('A5 release checks failed');}
 setSubmissionWindow(key,start,r.closeAt);
 var sh=submissionBook_().getSheetByName('Assignment links');
 sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3111'&&v[1]==='A5'){sh.getRange(i+1,4).setValue(start);}});
 ensureSubmissionTrigger_();r=submissionState_()[key];
 var f=FormApp.openById(r.formId);if(!f.isAcceptingResponses()){throw Error('A5 did not open');}
 Logger.log('A5_OPEN '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,url:r.url,accepting:f.isAcceptingResponses()}));
}
