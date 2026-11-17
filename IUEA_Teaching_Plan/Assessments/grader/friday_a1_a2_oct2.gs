/** Lecturer-authorized catch-up: CML3111/CML3113 A1 and A2, until 2 October 10:59 Kampala. */
function openFridayA1A2UntilOctober2() {
  var end='2026-10-02T10:59:00+03:00';
  if(Date.now()>=Date.parse(end)){throw Error('This catch-up window has expired.');}
  var keys=['CML3111|W01','CML3111|W02','CML3113|W01','CML3113|W02'];
  var state=submissionState_(),props=PropertiesService.getScriptProperties();
  var sheet=submissionBook_().getSheetByName('Assignment links'),rows=sheet.getDataRange().getValues();
  keys.forEach(function(key){
    var r=state[key],parts=key.split('|'),label=parts[1]==='W01'?'A1':'A2';
    if(!r||!r.ready||!r.uploadReady||!(submissionAssessmentReleased_(key,r)||submissionCatchupCollectionAllowed_(key,r))){throw Error('Not ready '+key);}
    if(rows.filter(function(v){return v[0]===parts[0]&&v[1]===label;}).length!==1){throw Error('Expected one index row '+key);}
    if(!props.getProperty('FRIDAY_OCT2_PREVIOUS_'+key)){props.setProperty('FRIDAY_OCT2_PREVIOUS_'+key,JSON.stringify({openAt:r.openAt,closeAt:r.closeAt}));}
  });
  // Retire the earlier timer for these same four forms, if it remains installed.
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeFridayCatchupSept26';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
  keys.forEach(function(key){
    var r=state[key],parts=key.split('|'),label=parts[1]==='W01'?'A1':'A2';
    // Preserve original opening times and earlier submissions.
    setSubmissionWindow(key,r.openAt,end);
    rows.forEach(function(v,i){if(v[0]===parts[0]&&v[1]===label){sheet.getRange(i+1,5).setValue(end);}});
    r=submissionState_()[key];
    if(Date.parse(r.closeAt)!==Date.parse(end)||!FormApp.openById(r.formId).isAcceptingResponses()){throw Error('Opening verification failed '+key);}
    Logger.log('OPEN_UNTIL_FRIDAY '+JSON.stringify({key:key,openAt:r.openAt,closeAt:r.closeAt,url:r.url,accepting:true}));
  });
  ensureSubmissionTrigger_();
  var handler='closeFridayA1A2October2';
  if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===handler;})){
    ScriptApp.newTrigger(handler).timeBased().at(new Date(end)).create();
    ScriptApp.newTrigger(handler).timeBased().everyMinutes(1).create();
  }
  Logger.log('CLOSING_TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function closeFridayA1A2October2(){
  var end=Date.parse('2026-10-02T10:59:00+03:00');
  if(Date.now()<end){return;}
  var state=submissionState_();
  ['CML3111|W01','CML3111|W02','CML3113|W01','CML3113|W02'].forEach(function(key){
    var r=state[key];
    // A later lecturer-authorized extension takes precedence over this timer.
    if(r&&Date.parse(r.closeAt)===end){FormApp.openById(r.formId).setAcceptingResponses(false);}
  });
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='closeFridayA1A2October2';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
}
