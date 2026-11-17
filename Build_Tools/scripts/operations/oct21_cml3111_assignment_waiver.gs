/** Authorised CML3111-only extension. Never edit responses or marks. */
function applyCML3111A6WaiverOct21(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var state=submissionState_(),key='CML3111|W06',r=state[key];if(!r)throw Error('Missing '+key);
  var book=submissionBook_(),f=FormApp.openById(r.formId);
  function canonical(v){if(v instanceof Date)return v.toISOString();if(Array.isArray(v))return v.map(canonical);if(v&&typeof v==='object'){var o={};Object.keys(v).sort().forEach(function(k){o[k]=canonical(v[k]);});return o;}return v;}
  function hash(v){return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,JSON.stringify(canonical(v))));}
  function responses(){return f.getResponses().map(function(x){return [x.getId(),x.getTimestamp().toISOString(),x.getItemResponses().map(function(a){return [a.getItem().getId(),a.getResponse()];})];});}
  function sheets(){return book.getSheets().filter(function(s){return ['Assignment links','Assessment waivers'].indexOf(s.getName())<0;}).map(function(s){return [s.getName(),hash(s.getDataRange().getValues())];});}
  var before=responses(),marks=sheets(),others=JSON.parse(JSON.stringify(state));delete others[key];
  var original={state:r,title:f.getTitle(),description:f.getDescription(),accepting:f.isAcceptingResponses()};
  var p=PropertiesService.getScriptProperties();if(!p.getProperty('CML3111_A6_BEFORE_WAIVER_OCT21'))p.setProperty('CML3111_A6_BEFORE_WAIVER_OCT21',JSON.stringify(original));
  r.waived=true;r.assessmentReleased=false;r.openAt=null;r.closeAt=null;
  r.waiverReason='A6 waived for practical revision. Retain submissions and raw marks; exclude from totals and missing-work flags.';
  saveSubmissionState_(state,key);
  f.setAcceptingResponses(false);
  if(f.getTitle().indexOf('NOT ASSIGNED')<0)f.setTitle(f.getTitle()+' — NOT ASSIGNED');
  f.setDescription('CML3111 A6 is waived. No submission is required. Existing submissions and recorded marks are retained, but do not count towards coursework totals.');
  try{f.setCustomClosedFormMessage('CML3111 A6 is waived. No submission required. Your earlier work remains on record.');}catch(e){Logger.log('Custom closed notice unavailable; title and description identify waiver.');}
  var links=book.getSheetByName('Assignment links');
  links.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3111'&&v[1]==='A6'){links.getRange(i+1,4,1,2).setValues([['NOT ASSIGNED','NOT ASSIGNED']]);links.getRange(i+1,1,1,links.getLastColumn()).setNote(r.waiverReason);}});
  var policy=book.getSheetByName('Assessment waivers')||book.insertSheet('Assessment waivers');
  if(!policy.getLastRow())policy.appendRow(['cohort','assessment','status','reason','quiz_best','assignment_best','recorded_at']);
  var rows=policy.getDataRange().getValues();['A6','Quiz 6'].forEach(function(a){if(!rows.some(function(v){return v[0]==='CML3111'&&v[1]===a;}))policy.appendRow(['CML3111',a,'NOT_ASSIGNED','Exclude from totals/missing flags; preserve source work',9,7,new Date().toISOString()]);});
  var after=responses(),now=submissionState_();delete now[key];
  Logger.log(JSON.stringify({responsesPreserved:hash(before)===hash(after),sheetsPreserved:hash(marks)===hash(sheets()),otherSchedulesPreserved:hash(others)===hash(now)}));
  if(hash(before)!==hash(after)||hash(marks)!==hash(sheets())||hash(others)!==hash(now))throw Error('Preservation verification failed; inspect before further changes.');
  var blocked=!submissionAssessmentReleased_(key,{assessmentReleased:true,releaseEvidence:'Previously validated'});if(!blocked)throw Error('Release guard failed');
  Logger.log(JSON.stringify({key:key,waived:true,accepting:f.isAcceptingResponses(),openAt:null,closeAt:null,responsesBefore:before.length,responsesAfter:after.length,responseContentPreserved:true,recordedSheetsPreserved:true,otherSchedulesPreserved:true,openingBlocked:true,url:r.url}));
 }finally{lock.releaseLock();}
}
