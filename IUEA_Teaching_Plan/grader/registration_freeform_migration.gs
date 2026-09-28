/** Run in Assignment Controls. Changes existing IUEA identity items in place.
 * Does not change deadlines, response data, upload items or release settings.
 * Re-running resumes after the last successful form.
 */
function makeIueaRegistrationRequiredFreeform() {
  var lock=LockService.getScriptLock();lock.waitLock(30000);
  try {
    var state=submissionState_(),start=Date.now(),changed=0;
    var keys=Object.keys(state).filter(function(key){return /^CML311[123]\|/.test(key);});
    keys.sort();
    for(var i=0;i<keys.length;i++) {
      var key=keys[i],entry=state[key];
      if(entry.registrationFreeformV1){continue;}
      if(Date.now()-start>240000){break;}
      var form=FormApp.openById(entry.formId);
      var items=form.getItems(FormApp.ItemType.TEXT).filter(function(item){return submissionFieldKey_(item.getTitle())==='student_id';});
      if(items.length!==1){throw new Error('Expected exactly one existing registration field: '+key);}
      var item=items[0].asTextItem(),identity=item.getId();
      configureSubmissionIdentity_(item,key.split('|')[0]);
      item.setTitle('Student Registration Number');
      if(!item.isRequired()||item.getId()!==identity){throw new Error('Identity field verification failed: '+key);}
      entry.registrationFreeformV1=true;
      saveSubmissionState_(state,key);
      changed++;
      Logger.log(key+': required freeform registration saved; existing field '+identity+' preserved.');
    }
    var remaining=keys.filter(function(key){return !state[key].registrationFreeformV1;}).length;
    Logger.log(JSON.stringify({iueaForms:keys.length,updatedThisRun:changed,remaining:remaining,policy:'Required text; no pattern validation'}));
  } finally {lock.releaseLock();}
}
