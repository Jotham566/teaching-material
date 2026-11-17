/** Collect missing A1 for the remaining Week 2 cohorts; grading stays held. */
function enableRemainingWeek1Uploads() {
  ['CML3111','CML3113'].forEach(function(cohort) {
    var state=submissionState_(),key=cohort+'|W01',a=state[key],w2=state[cohort+'|W02'];
    if(!a||!a.uploadReady||!w2||!isFinite(Date.parse(w2.closeAt))||Date.now()>=Date.parse(w2.closeAt)){
      throw Error('Check the published Week 2 deadline before opening '+key);
    }
    a.collectionOnly=true;
    a.collectionEvidence='Instructor request 21 September 2026: collect missed A1 during Week 2 with the Week 2 upload deadline; preserve marks and keep new written grading held.';
    saveSubmissionState_(state,key);
    var begin=a.openAt||new Date().toISOString();
    setSubmissionWindow(key,begin,w2.closeAt);
    var form=FormApp.openById(a.formId);
    form.setDescription('Week 1 catch-up A1 — Three problems one dataset. Submit this separately from A2. Deadline: '+Utilities.formatDate(new Date(w2.closeAt),'Africa/Kampala','yyyy-MM-dd HH:mm')+' (Kampala UTC+03:00).\n\nDescribe three engineering problems. For each, state the quantity/category of interest, possible inputs, target where appropriate, data source, limitation and why machine learning is or is not suitable. Choose one problem/dataset and justify it.\n\nUpload one complete report as DOCX or selectable-text PDF, or PPTX with narration notes or notebook evidence. Enter your own Student Registration Number exactly as on your university record. The field is required and accepts any format. Use your registered account. Keep the confirmation.\n\nCriteria: Problem framing 6; data and feasibility 8; judgement 6. Existing earned marks remain protected. New written-work results remain pending automated-grading validation.');
    configureSubmissionIdentity_(submissionTextItem_(form,'student_id',false),cohort);
    var book=submissionBook_(),links=book.getSheetByName('Assignment links');
    links.getDataRange().getValues().forEach(function(row,i){if(row[0]===cohort&&row[1]==='A1'){links.getRange(i+1,4,1,2).setValues([[begin,w2.closeAt]]);}});
    var release=book.getSheetByName('Assessment release');
    if(release){release.getDataRange().getValues().forEach(function(row,i){if(row[0]===key){release.getRange(i+1,2,1,3).setValues([['COLLECTION ONLY — GRADING HELD',a.collectionEvidence,form.isAcceptingResponses()]]);}});}
    Logger.log('A1_CATCHUP '+JSON.stringify({key:key,openAt:begin,closeAt:w2.closeAt,url:form.getPublishedUrl(),accepting:form.isAcceptingResponses()}));
  });
  ensureSubmissionTrigger_();
}
