
/** Change duration and descriptions without editing questions or responses. */
function apply24HourQuizPolicy(){
  if(WINDOW_HOURS!==24){throw Error('Expected 24-hour configuration');}
  var links=loadLinks_(),pending=loadPending_(),checked=0,active=[];
  Object.keys(links).forEach(function(key){
    var L=links[key],f=FormApp.openById(L.formId),before=f.getResponses().length;
    var description=f.getDescription().replace(/48(?=[ -]hour)/g,'24');
    if(description!==f.getDescription()){f.setDescription(description);}
    if(pending[L.formId]){
      if(!L.openedAt){throw Error('Missing original activation '+key);}
      L.closeAt=Number(L.openedAt)+24*3600000;
      pending[L.formId].closeAt=L.closeAt;
      active.push({key:key,openedAt:L.openedAt,closeAt:L.closeAt});
    }
    if(f.getResponses().length!==before){throw Error('Response count changed during update '+key);}
    checked++;
  });
  saveLinks_(links);savePending_(pending);autoCloseQuiz();
  Logger.log('QUIZ_24_HOUR_POLICY '+JSON.stringify({hours:WINDOW_HOURS,forms:checked,active:active,pending:loadPending_()}));
}
