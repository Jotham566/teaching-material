/** Append to ASSIGNMENT controller. Preserve the existing A3 closing time. */
function prepare_W3_CML3112_Sept22(){
  var key='CML3112|W03',state=submissionState_(),r=state[key];
  if(!r||r.formId!=='1U_wdHF0yS0OhZ15BGfsKYvwbDYv3Tcn2t4xyUhujAkA'){throw Error('Unexpected A3 form');}
  if(Date.parse(r.closeAt)!==Date.parse('2026-09-29T11:00:00+03:00')){throw Error('A3 deadline changed; inspect before rescheduling');}
  setSubmissionWindow(key,'2026-09-22T10:55:00+03:00',r.closeAt);
  ensureSubmissionTrigger_();
  var rows=submissionBook_().getSheetByName('Assignment links'),values=rows.getDataRange().getValues(),found=0;
  values.forEach(function(v,i){if(v[0]==='CML3112'&&v[1]==='A3'){rows.getRange(i+1,4).setValue('2026-09-22T10:55:00+03:00');found++;}});
  if(found!==1){throw Error('Expected exactly one A3 link-index row');}
  r=submissionState_()[key];
  Logger.log('W3_ASSIGNMENT_SCHEDULE '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,url:r.url,uploadReady:r.uploadReady,accepting:FormApp.openById(r.formId).isAcceptingResponses(),handlers:ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})}));
}
