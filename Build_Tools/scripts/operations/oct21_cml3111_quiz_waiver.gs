/** Close Quiz 6 without changing responses or awarded scores. */
function applyCML3111Quiz6WaiverOct21(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var links=loadLinks_(),key='CML3111|6',r=links[key];if(!r)throw Error('Missing '+key);
  var f=FormApp.openById(r.formId);
  function canonical(v){if(v instanceof Date)return v.toISOString();if(Array.isArray(v))return v.map(canonical);if(v&&typeof v==='object'){var o={};Object.keys(v).sort().forEach(function(k){o[k]=canonical(v[k]);});return o;}return v;}
  function hash(v){return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,JSON.stringify(canonical(v))));}
  function responses(){return f.getResponses().map(function(x){return [x.getId(),x.getTimestamp().toISOString(),x.getGradableItemResponses().map(function(a){return [a.getItem().getId(),a.getResponse(),a.getScore()];})];});}
  var destination=f.getDestinationId(),book=destination?SpreadsheetApp.openById(destination):null;
  function sheets(){return book?book.getSheets().map(function(s){return [s.getName(),hash(s.getDataRange().getValues())];}):[];}
  var before=responses(),marks=sheets(),others=JSON.parse(JSON.stringify(links));delete others[key];
  var p=PropertiesService.getScriptProperties();if(!p.getProperty('CML3111_Q6_BEFORE_WAIVER_OCT21'))p.setProperty('CML3111_Q6_BEFORE_WAIVER_OCT21',JSON.stringify({state:r,title:f.getTitle(),description:f.getDescription()}));
  r.waived=true;r.openedAt=null;r.closeAt=null;
  f.setAcceptingResponses(false);
  if(f.getTitle().indexOf('NOT ASSIGNED')<0)f.setTitle(f.getTitle()+' — NOT ASSIGNED');
  f.setDescription('CML3111 Quiz 6 is waived. No submission required. Existing responses and scores are retained but excluded from coursework totals.');
  try{f.setCustomClosedFormMessage('CML3111 Quiz 6 is waived. No submission required. Earlier responses remain on record.');}catch(e){Logger.log('Custom closed notice unavailable; title and description identify waiver.');}
  removePending_(r.formId);saveLinks_(links);
  var found=folder_().getFilesByName(LINKS_SHEET_NAME);
  if(found.hasNext()){var sh=SpreadsheetApp.open(found.next()).getSheets()[0];sh.getDataRange().getValues().forEach(function(v,i){if(v[0]==='CML3111'&&Number(v[1])===6){sh.getRange(i+1,4).setValue('NOT ASSIGNED');sh.getRange(i+1,1,1,9).setNote('Quiz 6 waived. Preserve responses and raw scores; exclude from totals and missing-work flags.');}});}
  var after=responses(),now=loadLinks_();delete now[key];
  Logger.log(JSON.stringify({responsesPreserved:hash(before)===hash(after),sheetsPreserved:hash(marks)===hash(sheets()),otherSchedulesPreserved:hash(others)===hash(now)}));
  if(hash(before)!==hash(after)||hash(marks)!==hash(sheets())||hash(others)!==hash(now))throw Error('Preservation verification failed');
  Logger.log(JSON.stringify({key:key,waived:true,accepting:f.isAcceptingResponses(),openedAt:null,closeAt:null,responsesBefore:before.length,responsesAfter:after.length,responsesAndScoresPreserved:true,recordedSheetsPreserved:true,otherSchedulesPreserved:true,pendingCloseRemoved:!loadPending_()[r.formId],url:r.short||r.live}));
 }finally{lock.releaseLock();}
}
