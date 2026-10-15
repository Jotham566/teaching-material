/** Description-only refresh. Load IUEA_CONCISE_BRIEFS from the generated payload.
 * Does not change windows, questions, required fields, responses or grades.
 */
function refreshConciseAssignmentInstructionsSept29(){
  var lock=LockService.getScriptLock();lock.waitLock(30000);
  try{
    var props=PropertiesService.getScriptProperties(),state=submissionState_();
    var version='IUEA_CONCISE_INSTRUCTIONS_20260929',done=JSON.parse(props.getProperty(version)||'[]');
    var keys=Object.keys(IUEA_CONCISE_BRIEFS),changed=0;
    for(var i=0;i<keys.length;i++){
      var key=keys[i];if(done.indexOf(key)>=0){continue;}
      var r=state[key],brief=IUEA_CONCISE_BRIEFS[key];
      if(!r||!r.formId){throw Error('Missing existing form '+key);}
      var form=FormApp.openById(r.formId),accepting=form.isAcceptingResponses();
      var ids=form.getItems().map(function(item){return item.getId();}).join(',');
      var snapshot=JSON.stringify(r),backup=version+'_BEFORE_'+key;
      if(props.getProperty(backup)===null){props.setProperty(backup,form.getDescription());}
      var deadline=r.closeAt?Utilities.formatDate(new Date(r.closeAt),'Africa/Kampala','yyyy-MM-dd HH:mm'):'Not scheduled yet';
      var description='Maximum '+brief.maximum+' marks. Deadline: '+deadline+' (Kampala UTC+03:00).\n\n'+brief.brief;
      form.setDescription(description);
      if(form.getDescription()!==description||form.isAcceptingResponses()!==accepting||form.getItems().map(function(item){return item.getId();}).join(',')!==ids||JSON.stringify(submissionState_()[key])!==snapshot){throw Error('Verification failed '+key);}
      done.push(key);props.setProperty(version,JSON.stringify(done));changed++;
      Logger.log('CONCISE_UPDATED '+key+' accepting='+accepting+' window_and_fields_preserved=true');
      if(changed>=12){break;}
    }
    Logger.log('CONCISE_PROGRESS '+done.length+'/'+keys.length);
  }finally{lock.releaseLock();}
}

/** Clarify the existing optional field; do not add or require a repository. */
function clarifyEarlyAssignmentRepositoryFieldSept29(){
  var state=submissionState_();
  ['CML3111','CML3112','CML3113'].forEach(function(code){
    ['W03','W04','W05'].forEach(function(id){
      var key=code+'|'+id,form=FormApp.openById(state[key].formId);
      var items=form.getItems(FormApp.ItemType.TEXT).filter(function(item){return item.getTitle()==='Repository URL';});
      if(items.length!==1||items[0].asTextItem().isRequired()){throw Error('Inspect repository field '+key);}
      items[0].asTextItem().setHelpText('Optional for this assignment. You do not need a GitHub repository or a URL to submit this notebook.');
      Logger.log('OPTIONAL_REPOSITORY_CLARIFIED '+key);
    });
  });
}
