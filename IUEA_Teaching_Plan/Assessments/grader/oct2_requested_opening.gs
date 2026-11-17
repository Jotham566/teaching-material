/** Requested 2 October: CML3113 A2/A3 and CML3111 A4. */
function openRequestedAssignmentsOctober2(){
 var p=PropertiesService.getScriptProperties(),prop='REQUESTED_OPENING_20261002',s=submissionState_();
 var expected={'CML3113|W03':'2026-10-09T08:00:00+03:00','CML3111|W04':'2026-10-09T11:00:00+03:00'};
 var keys=['CML3113|W02','CML3113|W03','CML3111|W04'];
 keys.forEach(function(k){var r=s[k];if(!r||!r.ready||!r.uploadReady||!submissionAssessmentReleased_(k,r)){throw Error('Not ready '+k);}if(expected[k]&&Date.parse(r.closeAt)!==Date.parse(expected[k])){throw Error('Unexpected deadline '+k);}});
 var cfg=JSON.parse(p.getProperty(prop)||'null');
 if(!cfg){cfg={start:Date.now(),previous:{}};cfg.end=cfg.start+86400000;keys.forEach(function(k){cfg.previous[k]={openAt:s[k].openAt,closeAt:s[k].closeAt};});p.setProperty(prop,JSON.stringify(cfg));}
 if(Date.now()>=cfg.end){throw Error('Reopening expired');}
 var sheet=submissionBook_().getSheetByName('Assignment links'),rows=sheet.getDataRange().getValues();
 keys.forEach(function(k){var r=s[k],end=k==='CML3113|W02'?new Date(cfg.end).toISOString():r.closeAt;
 var start=Date.parse(r.openAt)>cfg.start?new Date(cfg.start).toISOString():r.openAt;
 setSubmissionWindow(k,start,end);
 var parts=k.split('|'),label='A'+Number(parts[1].slice(1)),found=0;
 rows.forEach(function(v,i){if(v[0]===parts[0]&&v[1]===label){sheet.getRange(i+1,4,1,2).setValues([[start,end]]);found++;}});
 if(found!==1){throw Error('Index row missing '+k);}
 r=submissionState_()[k];if(!FormApp.openById(r.formId).isAcceptingResponses()){throw Error('Still closed '+k);}
 Logger.log('ASSIGNMENT_OPEN '+JSON.stringify({key:k,openAt:r.openAt,closeAt:r.closeAt,url:r.url,accepting:true}));
 });
 ensureSubmissionTrigger_();var h='closeCML3113A2October3';
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()===h;})){ScriptApp.newTrigger(h).timeBased().at(new Date(cfg.end)).create();}
 Logger.log('CLOSING_TRIGGERS '+JSON.stringify(ScriptApp.getProjectTriggers().map(function(t){return t.getHandlerFunction();})));
}
function closeCML3113A2October3(){
 var cfg=JSON.parse(PropertiesService.getScriptProperties().getProperty('REQUESTED_OPENING_20261002')||'null');
 if(!cfg||Date.now()<cfg.end){return;}
 var r=submissionState_()['CML3113|W02'];if(Date.parse(r.closeAt)===cfg.end){FormApp.openById(r.formId).setAcceptingResponses(false);}
}
