/** Synthetic QA workspace: separate Forms, response book and script state. */
function qaScope_() {
  SUBMISSION_CONFIG='IUEA_SUBMISSIONS_QA_V1';
  SUBMISSION_RESPONSE_BOOK='IUEA_SUBMISSIONS_QA_BOOK';
  ASSESSMENTS=[{key:'QA|W02',track:'QA',cohort:'QA',id:'W02',label:'W02',title:'Synthetic submission test — not a student assessment',maximum:20,formats:['ipynb','md'],opens_at:null,closes_at:null,preserve_existing:true,brief:'Synthetic test only. Use registration number 99/TEST/000/DEMO-X and the two supplied test files. No marks enter a student gradebook.'}];
  ensureSubmissionTrigger_=function(){};
}
function createSubmissionQA(){qaScope_();buildSubmissionForms();Logger.log('QA audit '+submissionBook_().getUrl());}
function openSubmissionQA(){
  qaScope_();
  var start=new Date(),end=new Date(start.getTime()+10*60*1000);
  confirmSubmissionReadiness(['QA|W02']);
  setSubmissionWindow('QA|W02',start.toISOString(),end.toISOString());
  var existing=ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='syncSubmissionQA';});
  if(!existing.length){ScriptApp.newTrigger('syncSubmissionQA').timeBased().everyMinutes(1).create();}
  submissionStatus();
}
function syncSubmissionQA(){qaScope_();syncSubmissions();}
function statusSubmissionQA(){qaScope_();submissionStatus();Logger.log('QA audit '+submissionBook_().getUrl());}
function exportSubmissionQA(){qaScope_();syncSubmissions();exportSubmissionFiles('QA|W02');}
function closeSubmissionQA(){
  qaScope_();var state=submissionState_();
  if(state['QA|W02']&&!state['QA|W02'].closedScanned){setSubmissionWindow('QA|W02',state['QA|W02'].openAt||new Date(0).toISOString(),new Date().toISOString());syncSubmissions();}
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='syncSubmissionQA';}).forEach(function(t){ScriptApp.deleteTrigger(t);});
  submissionStatus();
}
function inspectSubmissionQAExport(){
  qaScope_();syncSubmissions();exportSubmissionFiles('QA|W02');
  var id=PropertiesService.getScriptProperties().getProperty('UPLOAD_EXPORT:QA|W02');
  var files=DriveApp.getFolderById(id).getFiles();
  while(files.hasNext()){
    var f=files.next(),encoded=Utilities.base64Encode(f.getBlob().getBytes());
    if(encoded.length>50000){throw new Error('QA fixture too large for diagnostic export');}
    for(var i=0;i<encoded.length;i+=5000){Logger.log('QA_FILE '+JSON.stringify({name:f.getName(),part:i/5000,data:encoded.slice(i,i+5000)}));}
  }
  submissionStatus();
}
