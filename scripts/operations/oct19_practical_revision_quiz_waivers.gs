/** Close only the waived quizzes; never delete responses or raw scores. */
function waiveQuiz6ForPracticalRevision(){
 var links=loadLinks_(),control=JSON.stringify(links['CML3111|6']);
 ['CML3112','CML3113'].forEach(function(code){
  var key=code+'|6',r=links[key];if(!r)throw Error('Missing '+key);
  var f=FormApp.openById(r.formId),before=f.getResponses().length;
   if(f.getTitle().indexOf('NOT ASSIGNED')<0)f.setTitle(f.getTitle()+' — NOT ASSIGNED');
  if(!r.waiverOriginal)r.waiverOriginal={openedAt:r.openedAt,closeAt:r.closeAt,description:f.getDescription()};
  r.waived=true;r.openedAt=null;r.closeAt=null;
  if(f.isAcceptingResponses())f.setAcceptingResponses(false);
  try{f.setCustomClosedFormMessage(code+' Quiz 6 is waived. No submission required. Use the class for practical revision.');}catch(e){Logger.log('Closed notice unavailable: '+e.message);}
  f.setDescription(code+' Quiz 6 — NOT ASSIGNED\nPractical revision replaces this quiz. No mark is required. Existing responses are preserved.');
  removePending_(r.formId);
  if(f.getResponses().length!==before)throw Error('Response count changed');
  Logger.log(JSON.stringify({key:key,waived:true,accepting:f.isAcceptingResponses(),responsesPreserved:before,url:r.short||r.live}));
 });
 saveLinks_(links);
 if(JSON.stringify(loadLinks_()['CML3111|6'])!==control)throw Error('CML3111 changed');
 var found=folder_().getFilesByName(LINKS_SHEET_NAME);
 if(found.hasNext()){var sh=SpreadsheetApp.open(found.next()).getSheets()[0];sh.getDataRange().getValues().forEach(function(v,i){if(['CML3112','CML3113'].indexOf(v[0])>=0&&Number(v[1])===6){sh.getRange(i+1,4).setValue('NOT ASSIGNED');sh.getRange(i+1,1,1,9).setNote('Quiz 6 waived for practical revision. Exclude from grades; preserve responses.');}});}
 Logger.log('CML3111 unchanged. Both Quiz 6 forms closed and pending closure entries removed.');
 Logger.log('Triggers: '+ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}).join(', '));
}
