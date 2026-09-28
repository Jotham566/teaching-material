/** Authorized CML3112 Week 3 launch: 22 September 2026, before 11 AM Kampala.
 * Append to the QUIZ controller. Does not reopen Week 1/2 or reset attempts.
 */
var W3_LAUNCH_PROPERTY='CML3112_W3_LAUNCH_20260922';
var W3_LAUNCH_HANDLER='maintainScheduled_W3_CML3112';
function schedule_W3_CML3112_Sept22(){
  var target=Date.parse('2026-09-22T10:55:00+03:00');
  if(Date.now()>=target+24*3600000){throw Error('Launch window has passed; do not reopen automatically.');}
  var links=loadLinks_(),L=links['CML3112|3'];
  if(!L||L.formId!=='1IJ9gMwpUg8Il9nqP3OPMDDTw7zFkV655RmWqw9TgsmY'){throw Error('Unexpected Quiz 3 form');}
  if(WINDOW_HOURS!==24){throw Error('Expected 24-hour policy');}
  var p=PropertiesService.getScriptProperties(),raw=p.getProperty(W3_LAUNCH_PROPERTY);
  if(!raw){p.setProperty(W3_LAUNCH_PROPERTY,JSON.stringify({target:target,status:'scheduled'}));}
  armScheduled_W3_CML3112_();
  maintainScheduled_W3_CML3112();
  statusScheduled_W3_CML3112();
}
function armScheduled_W3_CML3112_(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty(W3_LAUNCH_PROPERTY)||'null');
  ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()===W3_LAUNCH_HANDLER;}).forEach(function(t){ScriptApp.deleteTrigger(t);});
  if(!cfg||cfg.status==='closed'){return;}
  // Polling is a retry path if the one-off timer is delayed or a transient call fails.
  ScriptApp.newTrigger(W3_LAUNCH_HANDLER).timeBased().everyMinutes(5).create();
  var at=cfg.status==='open'?cfg.closeAt:cfg.target;
  if(at>Date.now()){ScriptApp.newTrigger(W3_LAUNCH_HANDLER).timeBased().at(new Date(at)).create();}
}
function maintainScheduled_W3_CML3112(){
  var lock=LockService.getScriptLock();if(!lock.tryLock(1000)){return;}
  try{
    var p=PropertiesService.getScriptProperties(),cfg=JSON.parse(p.getProperty(W3_LAUNCH_PROPERTY)||'null');
    if(!cfg||cfg.status==='closed'||Date.now()<cfg.target){return;}
    var L=loadLinks_()['CML3112|3'];
    if(cfg.status==='scheduled'){
      if(Date.now()>=cfg.target+24*3600000){cfg.status='closed';cfg.reason='missed launch window';p.setProperty(W3_LAUNCH_PROPERTY,JSON.stringify(cfg));armScheduled_W3_CML3112_();throw Error('Launch window passed without activation');}
      // Recover a previous successful open without extending its deadline.
      if(!L.openedAt){openQuizFor(3,'CML3112');L=loadLinks_()['CML3112|3'];}
      if(!L.openedAt||Number(L.closeAt)!==Number(L.openedAt)+24*3600000){throw Error('Quiz did not record a 24-hour activation');}
      if(!FormApp.openById(L.formId).isAcceptingResponses()&&Date.now()<L.closeAt){throw Error('Quiz is unexpectedly closed; preserve its original activation for investigation');}
      cfg.status='open';cfg.openedAt=Number(L.openedAt);cfg.closeAt=Number(L.closeAt);p.setProperty(W3_LAUNCH_PROPERTY,JSON.stringify(cfg));armScheduled_W3_CML3112_();
      Logger.log('W3_OPEN '+JSON.stringify(cfg));
    }
    if(cfg.status==='open'&&Date.now()>=cfg.closeAt){closeQuiz(3,'CML3112');cfg.status='closed';p.setProperty(W3_LAUNCH_PROPERTY,JSON.stringify(cfg));armScheduled_W3_CML3112_();Logger.log('W3_CLOSED '+JSON.stringify(cfg));}
  }finally{lock.releaseLock();}
}
function statusScheduled_W3_CML3112(){
  var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty(W3_LAUNCH_PROPERTY)||'null'),L=loadLinks_()['CML3112|3'];
  Logger.log('W3_SCHEDULE '+JSON.stringify({configuration:cfg,accepting:FormApp.openById(L.formId).isAcceptingResponses(),url:L.short||L.live,handlers:ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})}));
}
