/** Week 4 taught on 6 October. Preserve the original A4 opening and prior submissions. */
function prepareCML3112A4October6(){
 var key='CML3112|W04',s=submissionState_(),r=s[key],end='2026-10-13T11:00:00+03:00';
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r)){throw Error('A4 release checks failed');}
 setSubmissionWindow(key,r.openAt,end);
 var sh=submissionBook_().getSheetByName('Assignment links');
 sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3112'&&v[1]==='A4'){sh.getRange(i+1,5).setValue(end);}});
 ensureSubmissionTrigger_();
 var handler='closeCML3112A4October13';
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){ScriptApp.newTrigger(handler).timeBased().at(new Date(end)).create();}
 r=submissionState_()[key];
 Logger.log('A4_UPDATED '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,accepting:FormApp.openById(r.formId).isAcceptingResponses(),url:r.url}));
}
function closeCML3112A4October13(){
 var r=submissionState_()['CML3112|W04'],end=Date.parse('2026-10-13T11:00:00+03:00');
 if(Date.now()>=end&&Date.parse(r.closeAt)===end){FormApp.openById(r.formId).setAcceptingResponses(false);}
}
function auditIUEAAssignmentsOctober6(){
 var s=submissionState_();
 Object.keys(s).filter(function(k){return /^CML311[123]\|/.test(k);}).sort().forEach(function(k){
  var r=s[k];try {var f=FormApp.openById(r.formId);Logger.log('ASSIGNMENT '+JSON.stringify({key:k,accepting:f.isAcceptingResponses(),openAt:r.openAt,closeAt:r.closeAt,url:r.url}));}
  catch(e){Logger.log('AUDIT_ERROR '+k+' '+e.message);}
 });
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}

/** Lecturer confirmed moving A5 one week later on 6 October. */
function moveCML3112A5OneWeekOctober6(){
 var key='CML3112|W05',start='2026-10-13T11:00:00+03:00',end='2026-10-20T11:00:00+03:00';
 var r=submissionState_()[key];
 if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(key,r)){throw Error('A5 release checks failed');}
 var sh=submissionBook_().getSheetByName('Assignment links'),rows=sh.getDataRange().getValues();
 if(rows.filter(function(v){return v[0]==='CML3112'&&v[1]==='A5';}).length!==1){throw Error('Expected one A5 row');}
 setSubmissionWindow(key,start,end);
 rows.forEach(function(v,i){if(v[0]==='CML3112'&&v[1]==='A5'){sh.getRange(i+1,4,1,2).setValues([[start,end]]);}});
 r=submissionState_()[key];
 var f=FormApp.openById(r.formId);
 f.setAcceptingResponses(Date.now()>=Date.parse(start)&&Date.now()<Date.parse(end));
 ensureSubmissionTrigger_();
 [['openCML3112A5October13',start],['closeCML3112A5October20',end]].forEach(function(pair){
  if(Date.parse(pair[1])>Date.now()&&!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===pair[0];})){
   ScriptApp.newTrigger(pair[0]).timeBased().at(new Date(pair[1])).create();
  }
 });
 Logger.log('A5_MOVED '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,accepting:f.isAcceptingResponses(),url:r.url}));
 Logger.log('TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function openCML3112A5October13(){syncSubmissions();}
function closeCML3112A5October20(){
 var r=submissionState_()['CML3112|W05'],end=Date.parse('2026-10-20T11:00:00+03:00');
 if(Date.now()>=end&&Date.parse(r.closeAt)===end){FormApp.openById(r.formId).setAcceptingResponses(false);}
}
