function scheduleFridayOctober16Assignments(){
 var specs=fridayAssignmentSpecs_(),state=submissionState_();
 specs.forEach(function(s){var r=state[s[0]];if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(s[0],r))throw Error('Not ready '+s[0]);});
 var names=['openFridayAssignment3113','openFridayAssignment3111','closeFridayAssignment3113','closeFridayAssignment3111'];
 ScriptApp.getProjectTriggers().forEach(function(t){if(names.indexOf(t.getHandlerFunction())>=0)ScriptApp.deleteTrigger(t);});
 specs.forEach(function(s){
  setSubmissionWindow(s[0],s[1],s[2]);
  var r=submissionState_()[s[0]],f=FormApp.openById(r.formId);f.setAcceptingResponses(Date.now()>=Date.parse(s[1])&&Date.now()<Date.parse(s[2]));
  var sh=submissionBook_().getSheetByName('Assignment links');sh.getDataRange().getValues().forEach(function(v,i){if(v[0]===s[0].split('|')[0]&&v[1]===s[3])sh.getRange(i+1,4,1,2).setValues([[s[1],s[2]]]);});
  ScriptApp.newTrigger(s[4]).timeBased().at(new Date(s[1])).create();ScriptApp.newTrigger(s[5]).timeBased().at(new Date(s[2])).create();
  Logger.log(s[0]+' | opens '+r.openAt+' | due '+r.closeAt+' | accepting: '+f.isAcceptingResponses()+' | uploadReady: '+r.uploadReady+' | '+r.url);
 });
 ensureSubmissionTrigger_();Logger.log('VERIFIED triggers: '+ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();}).join(', '));
}
function fridayAssignmentSpecs_(){return [['CML3113|W05','2026-10-16T08:00:00+03:00','2026-10-23T08:00:00+03:00','A5','openFridayAssignment3113','closeFridayAssignment3113'],['CML3111|W06','2026-10-16T11:00:00+03:00','2026-10-23T11:00:00+03:00','A6','openFridayAssignment3111','closeFridayAssignment3111']];}
function fridayAssignmentRun_(index){var s=fridayAssignmentSpecs_()[index],r=submissionState_()[s[0]];if(r.openAt!==s[1]||r.closeAt!==s[2])return;var now=Date.now();if(now<Date.parse(s[1]))return;FormApp.openById(r.formId).setAcceptingResponses(r.uploadReady===true&&submissionAssessmentReleased_(s[0],r)&&now<Date.parse(s[2]));}
function openFridayAssignment3113(){fridayAssignmentRun_(0);}
function openFridayAssignment3111(){fridayAssignmentRun_(1);}
function closeFridayAssignment3113(){fridayAssignmentRun_(0);}
function closeFridayAssignment3111(){fridayAssignmentRun_(1);}
