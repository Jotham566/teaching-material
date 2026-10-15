/** Lecturer-authorized 29 September: Week 3 has not yet been taught to Friday cohorts. */
function extendFridayA3ToOctober9(){
  var p=PropertiesService.getScriptProperties();
  ['CML3113','CML3111'].forEach(function(code){
    var key=code+'|W03',r=submissionState_()[key],hour=code==='CML3113'?'08':'11';
    var oldClose='2026-10-02T'+hour+':00:00+03:00',newClose='2026-10-09T'+hour+':00:00+03:00';
    if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r)){throw Error('Assignment not ready '+key);}
    if([Date.parse(oldClose),Date.parse(newClose)].indexOf(Date.parse(r.closeAt))<0){throw Error('Unexpected existing deadline '+key);}
    var backup='FRIDAY_A3_OCT9_PREVIOUS_'+code;
    if(p.getProperty(backup)===null){p.setProperty(backup,JSON.stringify({openAt:r.openAt,closeAt:r.closeAt}));}
    // Keep the original opening and previously accepted submissions.
    setSubmissionWindow(key,r.openAt,newClose);
    var sheet=submissionBook_().getSheetByName('Assignment links'),rows=sheet.getDataRange().getValues(),found=0;
    rows.forEach(function(v,i){if(v[0]===code&&v[1]==='A3'){sheet.getRange(i+1,5).setValue(newClose);found++;}});
    if(found!==1){throw Error('Expected one A3 index row '+key);}
    r=submissionState_()[key];var f=FormApp.openById(r.formId);
    if(!f.isAcceptingResponses()||Date.parse(r.closeAt)!==Date.parse(newClose)){throw Error('Extension verification failed '+key);}
    Logger.log('A3_EXTENDED '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,url:r.url,accepting:true}));
  });
  ensureSubmissionTrigger_();
  Logger.log('CLOSING_HANDLERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
