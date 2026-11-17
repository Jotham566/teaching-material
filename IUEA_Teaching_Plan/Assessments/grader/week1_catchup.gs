
/** One-off instructor-authorized CML3112 Week 1 catch-up, 15 September 2026. */
function enableWeek1CatchupCML3112(){
  var key='CML3112|W01',state=submissionState_(),entry=state[key],w2=state['CML3112|W02'];
  var end='2026-09-22T11:00:00+03:00';
  if(!entry||!entry.uploadReady||Date.parse(w2.closeAt)!==Date.parse(end)||Date.now()>=Date.parse(end)){throw Error('Catch-up readiness/deadline mismatch');}
  var props=PropertiesService.getScriptProperties(),saved=props.getProperty('CML3112_W01_CATCHUP');
  var cfg=saved?JSON.parse(saved):{openAt:new Date().toISOString(),closeAt:new Date(Date.now()+24*3600000).toISOString(),formId:QUIZ_IDENTITY_FORMS['CML3112|1']};
  var q=FormApp.openById(cfg.formId),f=FormApp.openById(entry.formId),qCount=q.getResponses().length,aCount=f.getResponses().length;
  if(q.getTitle().indexOf('CML3112')<0||!q.isQuiz()){throw Error('Wrong quiz');}
  var items=q.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
  if(items.length!==5||items.some(function(i){return i.asMultipleChoiceItem().getPoints()!==1;})){throw Error('Unexpected quiz scoring');}
  var beforeKey='CML3112_W01_CATCHUP_BEFORE';
  if(!props.getProperty(beforeKey)){props.setProperty(beforeKey,JSON.stringify({quizDescription:q.getDescription(),assignmentDescription:f.getDescription(),quizResponses:qCount,assignmentResponses:aCount}));}
  entry.collectionOnly=true;entry.collectionEvidence='Instructor request 15 September 2026: collect missed Week 1 work until Week 2 upload deadline; preserve existing marks; new written grading remains held pending calibration.';
  saveSubmissionState_(state,key);
  f.setDescription('Week 1 catch-up: upload the work assigned in Week 1. The upload was unavailable last week. Deadline: 2026-09-22 11:00 (Kampala UTC+03:00). Existing earned marks are preserved. New written-work results remain pending until automated grading is validated.\n\nSubmit your three engineering problems, possible data/features and a defensible choice of one problem/dataset. Upload accessible DOCX, selectable-text PDF, PPTX with narration notes, or notebook evidence. Use your own Student Registration Number and registered Google account. Submit a complete replacement packet if needed. Keep your receipt.');
  setSubmissionWindow(key,cfg.openAt,end);ensureSubmissionTrigger_();
  q.setDescription('Week 1 catch-up quiz — CML3112. Five questions, one point each; one attempt per registered Google account. Enter your own Student Registration Number. Submit within 24 hours of activation. Deadline: '+Utilities.formatDate(new Date(cfg.closeAt),'Africa/Kampala','EEE d MMM yyyy HH:mm:ss')+' Kampala. This quiz deadline is separate from the Week 1 assignment-upload deadline. Your score is available immediately.');
  props.setProperty('CML3112_W01_CATCHUP',JSON.stringify(cfg));
  var imports=JSON.parse(props.getProperty('QUIZ_IMPORT_SOURCES')||'{}');imports['CML3112|1']={formId:cfg.formId,closeAt:cfg.closeAt};props.setProperty('QUIZ_IMPORT_SOURCES',JSON.stringify(imports));
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='syncWeek1CatchupCML3112';})){ScriptApp.newTrigger('syncWeek1CatchupCML3112').timeBased().everyMinutes(5).create();}
  syncWeek1CatchupCML3112();
  if(q.getResponses().length!==qCount||f.getResponses().length!==aCount){throw Error('Response count changed during setup; inspect audit');}
  Logger.log('CATCHUP '+JSON.stringify({assignment:submissionState_()[key],quiz:cfg,quizAccepting:q.isAcceptingResponses(),assignmentAccepting:f.isAcceptingResponses(),quizResponses:qCount,assignmentResponses:aCount}));
}
function syncWeek1CatchupCML3112(){
  var raw=PropertiesService.getScriptProperties().getProperty('CML3112_W01_CATCHUP');if(!raw){return;}
  var cfg=JSON.parse(raw),now=Date.now(),q=FormApp.openById(cfg.formId);
  var accepting=now>=Date.parse(cfg.openAt)&&now<=Date.parse(cfg.closeAt);
  if(q.isAcceptingResponses()!==accepting){q.setAcceptingResponses(accepting);}
  if(now>Date.parse(cfg.closeAt)){
    ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='syncWeek1CatchupCML3112';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
  }
}

function updateWeek1CatchupIndexCML3112(){
  var entry=submissionState_()['CML3112|W01'],book=submissionBook_(),sh=book.getSheetByName('Assignment links');
  var rows=sh.getDataRange().getValues(),matches=[];
  rows.forEach(function(r,i){if(r[0]==='CML3112'&&r[1]==='A1'){matches.push(i+1);}});
  if(matches.length!==1){throw Error('Expected one Week 1 index row');}
  sh.getRange(matches[0],4,1,2).setValues([[entry.openAt,entry.closeAt]]);
  var release=book.getSheetByName('Assessment release');
  if(release){release.getDataRange().getValues().forEach(function(r,i){if(r[0]==='CML3112|W01'){release.getRange(i+1,2,1,3).setValues([['COLLECTION ONLY — GRADING HELD',entry.collectionEvidence,FormApp.openById(entry.formId).isAcceptingResponses()]]);}});}
  var form=FormApp.openById(entry.formId),description=form.getDescription();
  if(description.indexOf('Problem framing (6)')<0){form.setDescription(description+'\n\nAssessment criteria: Problem framing (6): three specific engineering problems, measurable quantities/categories and ML suitability. Data and feasibility (8): features, targets where appropriate, sources and limitations. Judgement (6): defend your choice of one problem/dataset.');}
  Logger.log('CATCHUP_INDEX_UPDATED '+JSON.stringify({openAt:entry.openAt,closeAt:entry.closeAt,links:book.getUrl(),triggers:ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})}));
}

function correctCatchupQuizTo24Hours(){
  var props=PropertiesService.getScriptProperties(),cfg=JSON.parse(props.getProperty('CML3112_W01_CATCHUP'));
  if(!cfg||!isFinite(Date.parse(cfg.openAt))){throw Error('Missing original activation');}
  var assignmentBefore=JSON.stringify(submissionState_()['CML3112|W01']);
  cfg.closeAt=new Date(Date.parse(cfg.openAt)+24*3600000).toISOString();
  var q=FormApp.openById(cfg.formId),before=q.getResponses().length;
  props.setProperty('CML3112_W01_CATCHUP',JSON.stringify(cfg));
  q.setDescription('Week 1 catch-up quiz — CML3112. Five questions, one point each; one attempt per registered Google account. Enter your own Student Registration Number. Submit within 24 hours of activation. Deadline: '+Utilities.formatDate(new Date(cfg.closeAt),'Africa/Kampala','EEE d MMM yyyy HH:mm:ss')+' Kampala. This quiz deadline is separate from the Week 1 assignment-upload deadline. Your score is available immediately.');
  var imports=JSON.parse(props.getProperty('QUIZ_IMPORT_SOURCES')||'{}');imports['CML3112|1']={formId:cfg.formId,closeAt:cfg.closeAt};props.setProperty('QUIZ_IMPORT_SOURCES',JSON.stringify(imports));
  syncWeek1CatchupCML3112();
  if(q.getResponses().length!==before||JSON.stringify(submissionState_()['CML3112|W01'])!==assignmentBefore){throw Error('Catch-up preservation check failed');}
  Logger.log('CATCHUP_24_HOURS '+JSON.stringify({quiz:cfg,responses:before,accepting:q.isAcceptingResponses(),assignmentDeadline:submissionState_()['CML3112|W01'].closeAt}));
}
