/** Lecturer-authorized A3 reopening; A4 retains its published 6 October deadline. */
function openCML3112AssignmentsSept29(){
  var p=PropertiesService.getScriptProperties(),property='CML3112_ASSIGNMENTS_20260929';
  var state=submissionState_();
  ['W03','W04'].forEach(function(id){var k='CML3112|'+id,r=state[k];
    if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(k,r)){throw Error('Assignment is not ready and released: '+k);}
  });
  var a4=state['CML3112|W04'];
  if(Date.parse(a4.closeAt)!==Date.parse('2026-10-06T11:00:00+03:00')){throw Error('A4 deadline changed; inspect before proceeding');}
  var cfg=JSON.parse(p.getProperty(property)||'null');
  if(!cfg){
    var now=Date.now();
    cfg={openedAt:now,closeAt:now+86400000,previousOpenAt:state['CML3112|W03'].openAt,previousCloseAt:state['CML3112|W03'].closeAt};
    p.setProperty(property,JSON.stringify(cfg));
  }
  if(Date.now()>=cfg.closeAt){throw Error('A3 reopening expired; new lecturer authorization required');}
  // Preserve original opening so earlier valid uploads remain on time.
  setSubmissionWindow('CML3112|W03',cfg.previousOpenAt,new Date(cfg.closeAt).toISOString());
  var index=submissionBook_().getSheetByName('Assignment links'),rows=index.getDataRange().getValues(),found=0;
  rows.forEach(function(row,i){if(row[0]==='CML3112'&&row[1]==='A3'){index.getRange(i+1,5).setValue(new Date(cfg.closeAt).toISOString());found++;}});
  if(found!==1){throw Error('Expected one A3 link-index row');}
  var imports=JSON.parse(p.getProperty('QUIZ_IMPORT_SOURCES')||'{}');
  if(!p.getProperty(property+'_IMPORTS_BEFORE')){p.setProperty(property+'_IMPORTS_BEFORE',JSON.stringify(imports));}
  imports['CML3112|3']={formId:'1IJ9gMwpUg8Il9nqP3OPMDDTw7zFkV655RmWqw9TgsmY',closeAt:'2026-09-30T08:25:30.231Z'};
  imports['CML3112|4']={formId:'1x4zrT_Uim46XqyDoDW8C2hJcJ5sCwVkD-WJ1H-m87bw',closeAt:'2026-09-30T08:25:33.796Z'};
  p.setProperty('QUIZ_IMPORT_SOURCES',JSON.stringify(imports));
  ensureSubmissionTrigger_();
  var handler='closeCML3112A3Sept29';
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){
    ScriptApp.newTrigger(handler).timeBased().at(new Date(cfg.closeAt)).create();
  }
  // A4 has already opened on schedule. Verify both forms, without resetting A4.
  state=submissionState_();
  ['W03','W04'].forEach(function(id){var k='CML3112|'+id,r=state[k];
    if(!FormApp.openById(r.formId).isAcceptingResponses()){throw Error('Form is still closed: '+k);}
    Logger.log('ASSIGNMENT_WINDOW '+JSON.stringify({key:k,formId:r.formId,openAt:r.openAt,closeAt:r.closeAt,url:r.url,accepting:true}));
  });
  Logger.log('QUIZ_IMPORT_WINDOWS '+JSON.stringify({'CML3112|3':imports['CML3112|3'],'CML3112|4':imports['CML3112|4']}));
  Logger.log('ASSIGNMENT_TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function closeCML3112A3Sept29(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('CML3112_ASSIGNMENTS_20260929')||'null');
  if(!cfg||Date.now()<cfg.closeAt){return;}
  var r=submissionState_()['CML3112|W03'];
  if(Date.parse(r.closeAt)===cfg.closeAt){FormApp.openById(r.formId).setAcceptingResponses(false);}
}
