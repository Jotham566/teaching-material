/** Lecturer-authorized A6 waiver. Original responses and marks are retained. */
function waiveA6ForPracticalRevision(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var state=submissionState_(),control=JSON.stringify(state['CML3111|W06']),book=submissionBook_();
  var policy=book.getSheetByName('Assessment waivers')||book.insertSheet('Assessment waivers');
  if(policy.getLastRow()===0)policy.appendRow(['cohort','assessment','status','reason','quiz_best','assignment_best','recorded_at']);
  ['CML3112','CML3113'].forEach(function(code){
   var key=code+'|W06',r=state[key];if(!r)throw Error('Missing '+key);
   var f=FormApp.openById(r.formId),before=f.getResponses().length;
   if(f.getTitle().indexOf('NOT ASSIGNED')<0)f.setTitle(f.getTitle()+' — NOT ASSIGNED');
   if(!r.waiverOriginal)r.waiverOriginal={openAt:r.openAt,closeAt:r.closeAt,assessmentReleased:r.assessmentReleased,description:f.getDescription()};
   r.waived=true;r.assessmentReleased=false;r.waiverReason='Not assigned: practical revision instead of A6. No mark or submission required.';
   r.openAt=null;r.closeAt=null;saveSubmissionState_(state,key);
   if(f.isAcceptingResponses())f.setAcceptingResponses(false);
  try{f.setCustomClosedFormMessage(code+' A6 is waived. No submission required. Use the class for practical revision.');}catch(e){Logger.log('Closed notice unavailable: '+e.message);}
   f.setDescription(code+' A6 — NOT ASSIGNED\nPractical revision replaces this assessment. No submission or mark is required. Existing responses are preserved.');
   var sh=book.getSheetByName('Assignment links');sh.getDataRange().getValues().forEach(function(v,i){if(v[0]===code&&v[1]==='A6'){sh.getRange(i+1,4,1,2).setValues([['NOT ASSIGNED','NOT ASSIGNED']]);sh.getRange(i+1,1,1,sh.getLastColumn()).setNote(r.waiverReason);}});
   var vals=policy.getDataRange().getValues();['A6','Quiz 6'].forEach(function(a){if(!vals.some(function(v){return v[0]===code&&v[1]===a;}))policy.appendRow([code,a,'NOT ASSIGNED','Practical revision; exclude from totals and missing flags; retain original records',9,7,new Date().toISOString()]);});
   var after=f.getResponses().length;if(before!==after)throw Error('Response count changed');
   Logger.log(JSON.stringify({key:key,waived:true,accepting:f.isAcceptingResponses(),responsesPreserved:after,url:r.url}));
  });
  if(JSON.stringify(submissionState_()['CML3111|W06'])!==control)throw Error('CML3111 changed');
  Logger.log('CML3111 unchanged. Waiver policy recorded: '+book.getUrl());
  Logger.log('Workbook sheets: '+book.getSheets().map(function(s){return s.getName();}).join(', '));
 }finally{lock.releaseLock();}
}
