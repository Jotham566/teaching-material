// Description-only update. Never rebuild forms, change windows or touch responses.
function refreshAssignmentInstructions() {
  var lock=LockService.getScriptLock();lock.waitLock(30000);
  try {
    var state=submissionState_(),props=PropertiesService.getScriptProperties();
    var version='ASSIGNMENT_INSTRUCTIONS_20260921',done=JSON.parse(props.getProperty(version)||'[]');
    var changed=0;
    for(var i=0;i<ASSESSMENTS.length;i++) {
      var a=ASSESSMENTS[i];if(done.indexOf(a.key)>=0){continue;}
      var record=state[a.key];if(!record||!record.formId){throw Error('Missing existing form '+a.key);}
      var form=FormApp.openById(record.formId),accepting=form.isAcceptingResponses();
      var itemIds=form.getItems().map(function(item){return item.getId();}).join(',');
      var deadline=record.closeAt?Utilities.formatDate(new Date(record.closeAt),'Africa/Kampala','yyyy-MM-dd HH:mm'):'Not scheduled yet';
      var brief=a.brief.replace(/Published closing time[^\n]*\n/g,'');
      form.setDescription('Maximum '+a.maximum+' marks. Deadline: '+deadline+' (Kampala UTC+03:00).\n'+
        'Follow the exact file list below. Latest complete on-time submission is marked.\n\n'+brief);
      if(form.isAcceptingResponses()!==accepting||form.getItems().map(function(item){return item.getId();}).join(',')!==itemIds){throw Error('Form settings changed unexpectedly '+a.key);}
      if(form.getDescription().indexOf('## Start here')<0){throw Error('Description verification failed '+a.key);}
      done.push(a.key);props.setProperty(version,JSON.stringify(done));changed++;
      Logger.log('INSTRUCTIONS_UPDATED '+a.key+' accepting='+accepting+' fields_preserved=true');
      if(changed>=18){break;}
    }
    Logger.log('INSTRUCTIONS_PROGRESS '+done.length+'/'+ASSESSMENTS.length);
  } finally {lock.releaseLock();}
}

function refreshAssignmentEvidenceLabels() {
  var props=PropertiesService.getScriptProperties(),key='ASSIGNMENT_INSTRUCTIONS_20260921';
  var done=JSON.parse(props.getProperty(key)||'[]');
  props.setProperty(key,JSON.stringify(done.filter(function(k){return !/\|(W02|TEST1|TEST2)$/.test(k);})));
  refreshAssignmentInstructions();
}
