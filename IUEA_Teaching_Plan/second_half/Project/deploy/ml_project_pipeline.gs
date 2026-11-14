/** IUEA ML project collection: the collector web app (collection design of 14 November 2026, no Submit step).
 *
 * A separate Apps Script project ("IUEA ML Project Submissions"), web app executing as the lecturer, access Anyone. It only answers doPost
 * and runs the time trigger mlpSweep. It writes to the same workbook as the Test 1 collector and the portal (Test allocations, Test windows,
 * Collection), so the existing export, monitor and fresh-attempt functions keep working.
 *
 * How collection works
 *   Start      the portal copies the issued notebook into the lecturer's Drive folder, shares it with the student's Google account as an
 *              EDITOR and records the file id (Test allocations, column notebook_id). Colab autosaves to that file.
 *   Backups    every 5 minutes the setup cell's thread sends the notebook on screen (route backup). Each is timestamped here. The newest
 *              on-time backup and the newest late backup are kept (two files per student); a late one is never used.
 *   Deadline   mlpSweep (every minute) finds attempts past their deadline (start + 180 minutes, capped at the window close, plus any
 *              extension), turns the student's permission into read only, and collects the NEWER of: the last Drive revision of the issued
 *              file saved at or before the deadline (Drive's modifiedTime), and the last on-time backup. The source and its time go in the
 *              Collection row and on the spot-check list. Then repository_dispatch sends it to GitHub Actions for marking.
 *   Finish     "I have finished" on the entry page does the same at once.
 *   Check      "Check my work" takes the current saved file (or the newest backup if newer) and asks Actions for the structural checks only.
 *   Rehearsal  keys CML311x|ML_REHEARSAL: the same, except editing is never stopped and nothing is marked (checks only, always shown).
 *
 * Script Properties (set by deploy/setup_pipeline.sh through the one-time bootstrap; none is in this file):
 *   BOOK_ID, FOLDER_ID, GATEWAY_KEY (= the Worker's COLLECTOR_GATEWAY_KEY), ACTIONS_SECRET (= the GitHub secret COLLECTOR_SECRET),
 *   GITHUB_REPO (owner/name), GITHUB_TOKEN (fine-grained, that repository only, Contents: read and write), ML_PROJECT_RELEASED (YES = marks shown).
 * Needs the Drive advanced service (v3), enabled in appsscript.json.
 */
var MLP_COLUMNS = ['response_id','cohort','assessment','variant','full_name','email','student_registration_number','submitted_at','opens_at','closes_at','status','snapshot_id','notebook_sha256','source_id','detail'];
var MLP_CHECK_COLUMNS = ['submission_id','kind','attempt','received_at','dispatched_at','dispatch_status','checked_at','runs_from_top','first_failed_cell','failed_cells','functions_found','missing_functions','memo_found','part_a','part_b','total','grader','detail','content_file','issued_file'];
var MLP_STATE_COLUMNS = ['attempt','assessment_key','registration','state','collected_at','source','source_time','submission_id','other_file_seen','last_backup_at','ontime_file','ontime_at','late_file','late_at','backups'];
var MLP_EXT_COLUMNS = ['at','who','minutes','reason','attempts_changed','by'];
var MLP_MAX_BYTES = 12 * 1024 * 1024;
var MLP_CHECK_GAP_MS = 2 * 60000;
var MLP_KEY = /^CML311[123]\|ML_(PROJECT|REHEARSAL)$/;

function mlpProps_(){return PropertiesService.getScriptProperties();}
function mlpProp_(name,minimum){var v=mlpProps_().getProperty(name);if(!v||(minimum&&v.length<minimum))throw Error('SETUP:'+name);return v;}
function mlpJson_(value){return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);}
function mlpSame_(a,b){a=String(a||'');b=String(b||'');if(!a||a.length!==b.length)return false;var d=0;for(var i=0;i<a.length;i++)d|=a.charCodeAt(i)^b.charCodeAt(i);return d===0;}
function mlpText_(s){s=String(s==null?'':s);return /^[=+@-]/.test(s)?"'"+s:s;}
function mlpReg_(v){return String(v||'').toUpperCase().replace(/\s+/g,'');}
function mlpBook_(){return SpreadsheetApp.openById(mlpProp_('BOOK_ID'));}
function mlpKampala_(iso){return Utilities.formatDate(new Date(iso),'Africa/Kampala','d MMM yyyy HH:mm:ss');}
function mlpSheet_(book,name,headers){var s=book.getSheetByName(name)||book.insertSheet(name);if(!s.getLastRow()){s.appendRow(headers);s.setFrozenRows(1);}return s;}
function mlpSha_(bytes){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,bytes).map(function(b){return ('0'+((b+256)%256).toString(16)).slice(-2);}).join('');}
function mlpRehearsal_(key){return /\|ML_REHEARSAL$/.test(key);}

// ---------------------------------------------------------------- the web app
function doPost(e){
 var request;
 try{var raw=e&&e.postData&&e.postData.contents;if(!raw||raw.length>MLP_MAX_BYTES*1.2)return mlpJson_({ok:false,error:'The request is too large or empty.'});request=JSON.parse(raw);}
 catch(err){return mlpJson_({ok:false,error:'Invalid request.'});}
 try{
  var action=String(request.action||'');
  if(action==='bootstrap')return mlpJson_({ok:true,result:mlpBootstrap_(request)});
  if(['backup','checkwork','finish','status'].indexOf(action)>=0){
   if(!mlpSame_(request.secret,mlpProp_('GATEWAY_KEY',32)))return mlpJson_({ok:false,error:'The collection service is unavailable. Tell your lecturer.'});
   var fn={backup:mlpBackup_,checkwork:mlpCheckWork_,finish:mlpFinish_,status:mlpStatus_}[action];
   return mlpJson_({ok:true,result:fn(request)});
  }
  if(['fetch','result','ping'].indexOf(action)>=0){
   if(!mlpSame_(request.secret,mlpProp_('ACTIONS_SECRET',32)))return mlpJson_({ok:false,error:'forbidden'});
   return mlpJson_({ok:true,result:action==='fetch'?mlpFetch_(request):action==='result'?mlpResult_(request):mlpPing_()});
  }
  return mlpJson_({ok:false,error:'Unknown request.'});
 }catch(err){
  var m=String(err&&err.message||err);
  if(/^SETUP:/.test(m))return mlpJson_({ok:false,error:'The collection service is not set up yet. Tell your lecturer.'});
  return mlpJson_({ok:false,error:/^(This |Your |Open |The notebook|You |Wait |Nothing )/.test(m)?m:'The request could not be completed. Try again; if it keeps failing, tell your lecturer.'});
 }
}

// ---------------------------------------------------------------- allocations, windows, state
function mlpAllocations_(book){
 var sheet=book.getSheetByName('Test allocations');if(!sheet)return [];
 return sheet.getDataRange().getValues().slice(1).map(function(r,i){return {row:i+2,key:String(r[0]),registration:String(r[1]),email:String(r[2]).toLowerCase(),code:String(r[3]),variant:String(r[4]),
  name:String(r[6]||''),started:String(r[7]||''),deadline:String(r[8]||''),notebookId:String(r[9]||'')};}).filter(function(a){return MLP_KEY.test(a.key);});
}
function mlpAllocation_(book,code){
 if(!/^T-[A-Za-z0-9-]{8,64}$/.test(String(code||'')))throw Error('Open your project from the entry page first.');
 var a=mlpAllocations_(book).filter(function(x){return x.code===code;})[0];
 if(!a)throw Error('This attempt was not found. It may have been replaced by a fresh attempt: open your project from the entry page.');
 return a;
}
function mlpWindow_(book,key){
 var r=book.getSheetByName('Test windows').getDataRange().getValues().slice(1).filter(function(x){return x[0]===key;})[0];
 return r?{open:String(r[1]),close:String(r[2]),enabled:String(r[3]).toUpperCase()==='YES'}:{open:'',close:'',enabled:false};
}
function mlpDeadline_(book,a){
 var w=mlpWindow_(book,a.key),d=Date.parse(a.deadline),c=Date.parse(w.close);
 if(!isFinite(d))return null;
 return new Date(isFinite(c)?Math.min(d,c):d).toISOString();
}
function mlpState_(book,a){
 var sheet=mlpSheet_(book,'Attempt state',MLP_STATE_COLUMNS),rows=sheet.getDataRange().getValues();
 for(var i=1;i<rows.length;i++)if(rows[i][0]===a.code){var o={_row:i+1};MLP_STATE_COLUMNS.forEach(function(c,j){o[c]=rows[i][j];});return o;}
 var fresh={attempt:a.code,assessment_key:a.key,registration:a.registration,state:'OPEN',backups:0};
 sheet.appendRow(MLP_STATE_COLUMNS.map(function(c){return mlpText_(fresh[c]==null?'':fresh[c]);}));
 fresh._row=sheet.getLastRow();return fresh;
}
function mlpSaveState_(book,st){
 var sheet=mlpSheet_(book,'Attempt state',MLP_STATE_COLUMNS);
 sheet.getRange(st._row,1,1,MLP_STATE_COLUMNS.length).setValues([MLP_STATE_COLUMNS.map(function(c){return mlpText_(st[c]==null?'':st[c]);})]);
}
function mlpLock_(){var l=LockService.getScriptLock();if(!l.tryLock(25000))throw Error('Wait a few seconds and try again: the server is busy.');return l;}
function mlpFileIdFromHref_(href){var m=/\/drive\/([A-Za-z0-9_-]{10,})/.exec(String(href||''));return m?m[1]:'';}

// ---------------------------------------------------------------- the silent backups
function mlpBackup_(request){
 var book=mlpBook_(),lock=mlpLock_();
 try{
  var a=mlpAllocation_(book,request.attempt),st=mlpState_(book,a),now=new Date(),stamp=now.toISOString();
  var text=String(request.notebook||'');
  if(!text||text.length>MLP_MAX_BYTES)throw Error('The notebook is empty or too large for a backup.');
  var nb;try{nb=JSON.parse(text);}catch(err){throw Error('The notebook could not be read.');}
  if(nb.nbformat!==4||!Array.isArray(nb.cells))throw Error('The notebook could not be read.');
  var deadline=mlpDeadline_(book,a),rehearsal=mlpRehearsal_(a.key);
  var onTime=rehearsal||(st.state==='OPEN'&&deadline&&now.getTime()<=Date.parse(deadline));
  var openFile=mlpFileIdFromHref_(request.href),other=!openFile||openFile!==a.notebookId;
  var folder=DriveApp.getFolderById(mlpProp_('FOLDER_ID')),blob=Utilities.newBlob(text,'application/x-ipynb+json',a.code+(onTime?'_backup':'_late_backup')+'.ipynb');
  var slot=onTime?'ontime':'late';
  if(st[slot+'_file'])DriveApp.getFileById(st[slot+'_file']).setContent(text);else st[slot+'_file']=folder.createFile(blob).getId();
  st[slot+'_at']=stamp;st.last_backup_at=stamp;st.backups=Number(st.backups||0)+1;
  if(other)st.other_file_seen=(st.other_file_seen?st.other_file_seen+' ':'')+(openFile||'(not a Drive file)');
  if(String(st.other_file_seen).length>300)st.other_file_seen=String(st.other_file_seen).slice(-300);
  mlpSaveState_(book,st);
  return {received_at:mlpKampala_(stamp),on_time:!!onTime,other_file:other,closed:!onTime};
 }finally{lock.releaseLock();}
}

// ---------------------------------------------------------------- Drive: permissions and revisions
function mlpSetRole_(fileId,email,role){
 var list=Drive.Permissions.list(fileId,{fields:'permissions(id,emailAddress,role)',supportsAllDrives:true}).permissions||[];
 var p=list.filter(function(x){return String(x.emailAddress||'').toLowerCase()===email;})[0];
 if(p&&p.role!==role)Drive.Permissions.update({role:role},fileId,p.id,{supportsAllDrives:true});
 if(!p)Drive.Permissions.create({type:'user',role:role,emailAddress:email},fileId,{sendNotificationEmail:false,supportsAllDrives:true});
}
function mlpRevisionAt_(fileId,cutoffIso){
 var revs=(Drive.Revisions.list(fileId,{fields:'revisions(id,modifiedTime)',pageSize:1000}).revisions||[])
  .filter(function(r){return Date.parse(r.modifiedTime)<=Date.parse(cutoffIso);})
  .sort(function(x,y){return Date.parse(x.modifiedTime)-Date.parse(y.modifiedTime);});
 if(!revs.length)return null;
 var last=revs[revs.length-1];
 var response=UrlFetchApp.fetch('https://www.googleapis.com/drive/v3/files/'+fileId+'/revisions/'+last.id+'?alt=media',{headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},muteHttpExceptions:true});
 if(response.getResponseCode()!==200)throw Error('Could not read revision '+last.id+' ('+response.getResponseCode()+')');
 return {time:new Date(last.modifiedTime).toISOString(),text:response.getContentText(),id:last.id};
}

// ---------------------------------------------------------------- collection at the deadline, or on "I have finished"
function mlpCollect_(book,a,st,cutoffIso,reason){
 var rehearsal=mlpRehearsal_(a.key);
 if(!rehearsal&&a.notebookId)mlpSetRole_(a.notebookId,a.email,'reader');                // editing stops; the student can still read their work
 var rev=a.notebookId?mlpRevisionAt_(a.notebookId,cutoffIso):null;
 var backup=null;
 if(st.ontime_file&&st.ontime_at&&Date.parse(st.ontime_at)<=Date.parse(cutoffIso))backup={time:new Date(st.ontime_at).toISOString(),text:DriveApp.getFileById(st.ontime_file).getBlob().getDataAsString()};
 var pick=rev&&(!backup||Date.parse(rev.time)>=Date.parse(backup.time))?{source:'drive-revision',time:rev.time,text:rev.text}:backup?{source:'backup',time:backup.time,text:backup.text}:null;
 var parts=a.key.split('|'),id='S-'+Utilities.getUuid().replace(/-/g,'').slice(0,20);
 var collection=mlpSheet_(book,'Collection',MLP_COLUMNS);
 var detail='Collected ('+reason+') from the '+(pick?(pick.source==='backup'?'newest on-time backup':'issued Drive file')+' saved '+mlpKampala_(pick.time):'nothing')+
  (rev&&pick&&pick.source==='backup'?'; the Drive file was last saved '+mlpKampala_(rev.time):'')+(st.other_file_seen?'; backups came from another file: '+st.other_file_seen:'')+
  (st.late_at?'; a backup after the deadline was kept and not used ('+mlpKampala_(st.late_at)+')':'')+'.';
 if(!pick){
  collection.appendRow([id,parts[0],parts[1],a.variant,a.name,a.email,a.registration,new Date().toISOString(),a.started,cutoffIso,'COLLECTION_ERROR','','','',detail].map(mlpText_));
  st.state=rehearsal?'OPEN':'COLLECTED';st.collected_at=new Date().toISOString();mlpSaveState_(book,st);return null;
 }
 var bytes=Utilities.newBlob(pick.text).getBytes();
 var file=DriveApp.getFolderById(mlpProp_('FOLDER_ID')).createFile(Utilities.newBlob(bytes,'application/x-ipynb+json',id+'.ipynb'));
 if(!rehearsal)collection.appendRow([id,parts[0],parts[1],a.variant,a.name,a.email,a.registration,pick.time,a.started,cutoffIso,'COLLECTED',file.getId(),mlpSha_(bytes),pick.source,detail].map(mlpText_));
 mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).appendRow(mlpCheckRow_({submission_id:id,kind:rehearsal?'check':'grade',attempt:a.code,received_at:pick.time,dispatch_status:'QUEUED',
  content_file:file.getId(),issued_file:pick.source==='drive-revision'||!st.other_file_seen}));
 if(!rehearsal){st.state='COLLECTED';st.collected_at=new Date().toISOString();st.source=pick.source;st.source_time=pick.time;st.submission_id=id;}
 mlpSaveState_(book,st);
 mlpDispatch_(id,rehearsal?'check':'grade');
 return id;
}
/** The time trigger, every minute: collect every project attempt whose deadline has passed. */
function mlpSweep(){
 var book=mlpBook_(),lock=LockService.getScriptLock();if(!lock.tryLock(50000))return;
 var done=[];
 try{
  mlpAllocations_(book).forEach(function(a){
   if(mlpRehearsal_(a.key)||!a.started)return;
   var deadline=mlpDeadline_(book,a);if(!deadline||Date.now()<Date.parse(deadline))return;
   var st=mlpState_(book,a);if(st.state!=='OPEN')return;
   try{done.push(mlpCollect_(book,a,st,deadline,'deadline'));}catch(err){console.log('collect failed for '+a.code+': '+err);}
  });
 }finally{lock.releaseLock();}
 return done;
}
function mlpFinish_(request){
 var book=mlpBook_(),lock=mlpLock_();
 try{
  var a=mlpAllocation_(book,request.attempt),st=mlpState_(book,a);
  if(st.state==='COLLECTED')return mlpStatusOf_(book,a,st);
  var deadline=mlpDeadline_(book,a),now=new Date().toISOString();
  var cutoff=deadline&&Date.parse(deadline)<Date.parse(now)?deadline:now;
  mlpCollect_(book,a,st,cutoff,'I have finished');
  return mlpStatusOf_(book,a,mlpState_(book,a));
 }finally{lock.releaseLock();}
}

// ---------------------------------------------------------------- Check my work (structural checks only, never a mark)
function mlpCheckWork_(request){
 var book=mlpBook_(),lock=mlpLock_();
 try{
  var a=mlpAllocation_(book,request.attempt),st=mlpState_(book,a);
  var rows=mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).getDataRange().getValues().slice(1).filter(function(r){return r[2]===a.code&&r[1]==='check';});
  if(rows.length&&Date.now()-Date.parse(rows[rows.length-1][3])<MLP_CHECK_GAP_MS)throw Error('Wait two minutes between checks. The last result is shown below.');
  var saved=a.notebookId?DriveApp.getFileById(a.notebookId):null;
  var savedAt=saved?new Date(saved.getLastUpdated()).toISOString():'';
  var text,when,issued;
  if(st.ontime_file&&(!savedAt||Date.parse(st.ontime_at)>Date.parse(savedAt))){text=DriveApp.getFileById(st.ontime_file).getBlob().getDataAsString();when=new Date(st.ontime_at).toISOString();issued=!st.other_file_seen;}
  else if(saved){text=saved.getBlob().getDataAsString();when=savedAt;issued=true;}
  else throw Error('Nothing has been saved yet. Press Ctrl+S in Colab, wait a minute and try again.');
  var id='C-'+Utilities.getUuid().replace(/-/g,'').slice(0,20);
  var file=DriveApp.getFolderById(mlpProp_('FOLDER_ID')).createFile(Utilities.newBlob(text,'application/x-ipynb+json',id+'.ipynb'));
  mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).appendRow(mlpCheckRow_({submission_id:id,kind:'check',attempt:a.code,received_at:new Date().toISOString(),dispatch_status:'QUEUED',content_file:file.getId(),issued_file:issued}));
 }finally{lock.releaseLock();}
 mlpDispatch_(id,'check');
 return {check:id,checked_version:mlpKampala_(when),issued_file:issued,pending:true};
}

// ---------------------------------------------------------------- what the student sees
function mlpStatus_(request){var book=mlpBook_(),a=mlpAllocation_(book,request.attempt);return mlpStatusOf_(book,a,mlpState_(book,a));}
function mlpStatusOf_(book,a,st){
 var rows=mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).getDataRange().getValues().slice(1).filter(function(r){return r[2]===a.code;}).map(mlpCheckObj_);
 var deadline=mlpDeadline_(book,a),rehearsal=mlpRehearsal_(a.key);
 var latest=rows.filter(function(r){return r.checked_at;}).pop()||null,pending=rows.filter(function(r){return !r.checked_at;}).length>0;
 var out={course:a.key.split('|')[0],rehearsal:rehearsal,state:st.state==='COLLECTED'?'collected':'open',deadline:deadline?mlpKampala_(deadline):'',
  collected:st.state==='COLLECTED'?{source:st.source==='backup'?'the newest automatic backup':'your saved notebook',time:mlpKampala_(st.source_time)}:null,
  last_backup:st.last_backup_at?mlpKampala_(st.last_backup_at):'',checks:null,pending:pending,mark:null};
 if(latest)out.checks={runs_from_top:latest.runs_from_top===true||String(latest.runs_from_top)==='true'||String(latest.runs_from_top)==='TRUE',first_failed_cell:String(latest.first_failed_cell||''),
  missing_functions:String(latest.missing_functions||'').split(',').filter(String),memo_found:latest.memo_found===true||/^true$/i.test(String(latest.memo_found)),
  issued_file:latest.issued_file===true||/^true$/i.test(String(latest.issued_file)),checked:mlpKampala_(latest.checked_at)};
 var graded=rows.filter(function(r){return r.kind==='grade'&&r.checked_at&&r.submission_id===st.submission_id;})[0];
 if(!rehearsal&&graded&&mlpReleased_(book,a.key)&&graded.total!=='')out.mark='Part A '+graded.part_a+', Part B '+graded.part_b+', total '+graded.total+' (final after the lecturer\'s checks)';
 return out;
}
function mlpReleased_(book,key){
 if(mlpProps_().getProperty('ML_PROJECT_RELEASED')!=='YES')return false;
 var w=mlpWindow_(book,key);return isFinite(Date.parse(w.close))&&Date.now()>Date.parse(w.close);
}

// ---------------------------------------------------------------- GitHub Actions
function mlpCheckRow_(o){return MLP_CHECK_COLUMNS.map(function(c){return mlpText_(o[c]==null?'':o[c]);});}
function mlpCheckObj_(r){var o={};MLP_CHECK_COLUMNS.forEach(function(c,j){o[c]=r[j];});return o;}
function mlpSetCheck_(id,values){
 var sheet=mlpSheet_(mlpBook_(),'Instant checks',MLP_CHECK_COLUMNS),rows=sheet.getDataRange().getValues();
 for(var i=1;i<rows.length;i++)if(rows[i][0]===id){MLP_CHECK_COLUMNS.forEach(function(c,j){if(c in values)rows[i][j]=values[c];});sheet.getRange(i+1,1,1,MLP_CHECK_COLUMNS.length).setValues([rows[i].map(mlpText_)]);return;}
 throw Error('Unknown submission '+id);
}
function mlpDispatch_(id,mode){
 var status;
 try{
  var response=UrlFetchApp.fetch('https://api.github.com/repos/'+mlpProp_('GITHUB_REPO')+'/dispatches',{method:'post',contentType:'application/json',muteHttpExceptions:true,
   headers:{Authorization:'Bearer '+mlpProp_('GITHUB_TOKEN'),Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},
   payload:JSON.stringify({event_type:'grade-ml-project',client_payload:{submission_id:id,mode:mode}})});
  status=response.getResponseCode()===204?'DISPATCHED':'DISPATCH_FAILED '+response.getResponseCode();
 }catch(err){status='DISPATCH_FAILED '+String(err.message||err).slice(0,80);}
 mlpSetCheck_(id,{dispatched_at:new Date().toISOString(),dispatch_status:status});
 return status;
}
function mlpFetch_(request){
 var id=String(request.submission_id||''),book=mlpBook_();
 var row=mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).getDataRange().getValues().slice(1).map(mlpCheckObj_).filter(function(r){return r.submission_id===id;})[0];
 if(!row)throw Error('Unknown submission');
 var a=mlpAllocations_(book).filter(function(x){return x.code===row.attempt;})[0];
 return {submission_id:id,mode:row.kind,cohort:a.key.split('|')[0],registration:a.registration,notebook:DriveApp.getFileById(row.content_file).getBlob().getDataAsString(),
  issued_file:row.issued_file===true||/^true$/i.test(String(row.issued_file)),rehearsal:mlpRehearsal_(a.key)};
}
function mlpResult_(request){
 var r=request.report||{},id=String(request.submission_id||'');
 mlpSetCheck_(id,{checked_at:new Date().toISOString(),runs_from_top:!!r.runs_from_top,first_failed_cell:String(r.first_failed_cell||'').slice(0,200),failed_cells:String((r.failed_cells||[]).join('; ')).slice(0,500),
  functions_found:!(r.missing_functions||[]).length,missing_functions:(r.missing_functions||[]).join(','),memo_found:!!r.memo_found,
  part_a:r.part_a==null?'':r.part_a,part_b:r.part_b==null?'':r.part_b,total:r.total==null?'':r.total,grader:String(r.grader||'').slice(0,80),detail:String(r.detail||'').slice(0,300)});
 return {stored:id};
}
function mlpPing_(){
 var book=mlpBook_(),triggers=ScriptApp.getProjectTriggers().filter(function(t){return t.getHandlerFunction()==='mlpSweep';}).length;
 return {sheets:['Test allocations','Test windows','Collection','Instant checks','Attempt state','Class list'].filter(function(n){return !!book.getSheetByName(n);}),sweep_triggers:triggers,
  properties:['BOOK_ID','FOLDER_ID','GATEWAY_KEY','ACTIONS_SECRET','GITHUB_REPO','GITHUB_TOKEN'].filter(function(k){return !!mlpProps_().getProperty(k);})};
}

// ---------------------------------------------------------------- one-time bootstrap from deploy/setup_pipeline.sh
// setup_pipeline.sh pushes a file _bootstrap.gs that defines MLP_BOOTSTRAP_HASH (the SHA-256 of a one-time key, not a secret), calls this
// route once over HTTPS with the key and the properties, then pushes the project again without that file. Without the file this route refuses.
function mlpBootstrap_(request){
 if(typeof MLP_BOOTSTRAP_HASH==='undefined'||!/^[a-f0-9]{64}$/.test(MLP_BOOTSTRAP_HASH))throw Error('forbidden');
 if(!mlpSame_(mlpSha_(Utilities.newBlob(String(request.key||'')).getBytes()),MLP_BOOTSTRAP_HASH))throw Error('forbidden');
 var allowed=['BOOK_ID','FOLDER_ID','GATEWAY_KEY','ACTIONS_SECRET','GITHUB_REPO','GITHUB_TOKEN'],set=[];
 Object.keys(request.properties||{}).forEach(function(k){if(allowed.indexOf(k)>=0&&request.properties[k]){mlpProps_().setProperty(k,String(request.properties[k]));set.push(k);}});
 if(!mlpProps_().getProperty('FOLDER_ID'))mlpProps_().setProperty('FOLDER_ID',DriveApp.createFolder('IUEA ML project collection (private)').getId());
 installMlProjectPipeline(String(request.smoke_registration||''));
 return {properties_set:set,ping:mlpPing_()};
}

// ---------------------------------------------------------------- lecturer-only (run from the editor; not reachable from the web)
var MLP_REHEARSAL_ROWS = [['CML3112|ML_REHEARSAL','2026-11-17T08:00:00+03:00'],['CML3113|ML_REHEARSAL','2026-11-20T08:00:00+03:00'],['CML3111|ML_REHEARSAL','2026-11-20T08:00:00+03:00']];
/** Run once from the editor to approve the Google consent screen (setup_pipeline.sh asks you to). It only reads; it needs no property. */
function authorizeMlProject(){
 DriveApp.getRootFolder().getName();ScriptApp.getProjectTriggers();Drive.About.get({fields:'user'});
 try{UrlFetchApp.fetch('https://www.googleapis.com/discovery/v1/apis',{muteHttpExceptions:true});}catch(e){}
 try{SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('BOOK_ID')||'none');}catch(e){}
 console.log('Approved. Go back to the Terminal and press Enter.');
}
/** Sheets, the project and rehearsal windows (enabled NO) and the every-minute deadline trigger. Safe to run again. */
function installMlProjectPipeline(smokeRegistration){
 var book=mlpBook_();
 mlpSheet_(book,'Collection',MLP_COLUMNS);mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS);mlpSheet_(book,'Attempt state',MLP_STATE_COLUMNS);mlpSheet_(book,'Extensions',MLP_EXT_COLUMNS);
 mlpSheet_(book,'Class list',['cohort','registration','full_name']);
 var windows=book.getSheetByName('Test windows'),have=windows.getDataRange().getValues().map(function(r){return r[0];});
 ['CML3111','CML3112','CML3113'].forEach(function(c){if(have.indexOf(c+'|ML_PROJECT')<0)windows.appendRow([c+'|ML_PROJECT','','','NO',180]);});
 MLP_REHEARSAL_ROWS.forEach(function(r){if(have.indexOf(r[0])<0)windows.appendRow([r[0],r[1],'2026-11-22T23:59:00+03:00','NO',180]);});
 if(smokeRegistration){var cl=book.getSheetByName('Class list');if(!cl.getDataRange().getValues().some(function(x){return mlpReg_(x[1])===mlpReg_(smokeRegistration);}))cl.appendRow(['CML3112',smokeRegistration,'Setup Smoke Test']);}
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='mlpSweep';}))ScriptApp.newTrigger('mlpSweep').timeBased().everyMinutes(1).create();
 console.log(JSON.stringify(mlpPing_()));
}
/** Sets one window (or all three with 'ALL'). confirm must be CONFIRMED. Example, on 22 November:
 *  openMlProjectWindow('ALL','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED'). For the rehearsal pass 'ML_REHEARSAL' last. */
function openMlProjectWindow(course,opensIso,closesIso,confirm,test){
 if(confirm!=='CONFIRMED')throw Error('Pass CONFIRMED as the fourth argument.');
 test=test||'ML_PROJECT';if(!/^ML_(PROJECT|REHEARSAL)$/.test(test))throw Error('test is ML_PROJECT or ML_REHEARSAL.');
 if(!isFinite(Date.parse(opensIso))||!isFinite(Date.parse(closesIso))||Date.parse(closesIso)-Date.parse(opensIso)<180*60000)throw Error('Use real dates with the Kampala offset, at least 3 hours apart.');
 var ws=mlpBook_().getSheetByName('Test windows'),rows=ws.getDataRange().getValues(),n=0;
 rows.forEach(function(r,i){if(i&&String(r[0]).split('|')[1]===test&&(course==='ALL'||String(r[0]).split('|')[0]===course)){ws.getRange(i+1,2,1,4).setValues([[opensIso,closesIso,'YES',180]]);n++;}});
 console.log(n+' window rows set and enabled.');return n;
}
/** A fresh attempt after a reported technical failure, or after a wrong Google account (give the right email as replacementEmail).
 *  The old notebook becomes read only and the old allocation is withdrawn; the student opens the entry link again (still capped at the
 *  window close). Logged in Extensions. */
function freshMlProjectAttempt(registration,reason,replacementEmail){
 if(!String(reason||'').trim())throw Error('Write the reason (it is logged).');
 var book=mlpBook_(),alloc=book.getSheetByName('Test allocations'),n=0;
 mlpAllocations_(book).forEach(function(a){
  if(mlpRehearsal_(a.key)||mlpReg_(a.registration)!==mlpReg_(registration))return;
  if(a.notebookId)mlpSetRole_(a.notebookId,a.email,'reader');
  alloc.getRange(a.row,1,1,12).setValues([[a.key+'|WITHDRAWN',a.registration,a.email,a.code,a.variant,'',a.name,a.started,a.deadline,a.notebookId,'','WITHDRAWN']]);
  n++;
 });
 mlpSheet_(book,'Extensions',MLP_EXT_COLUMNS).appendRow([new Date().toISOString(),registration,0,'fresh attempt: '+reason+(replacementEmail?' (new email '+replacementEmail+')':''),n,Session.getEffectiveUser().getEmail()].map(mlpText_));
 console.log(n?'Done. Ask the student to open the entry link again'+(replacementEmail?' with '+replacementEmail:'')+'.':'No attempt found for '+registration+'.');
 return n;
}
/** One line for an extension. who: 'ALL' (every course), a course code ('CML3112') or one registration number. minutes > 0.
 *  For ALL or a course, the window close moves too. An attempt already collected is opened again (editing restored). Logged in Extensions. */
function extendMlProject(who,minutes,reason){
 minutes=Number(minutes);if(!(minutes>0&&minutes<=24*60))throw Error('Give the extra minutes, 1 to 1440.');
 if(!String(reason||'').trim())throw Error('Write the reason (it is logged).');
 var book=mlpBook_(),lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  who=String(who||'').trim();var course=/^CML311[123]$/.test(who)?who:'',all=who.toUpperCase()==='ALL';
  if(all||course){
   var ws=book.getSheetByName('Test windows'),rows=ws.getDataRange().getValues();
   rows.forEach(function(r,i){if(i&&/\|ML_PROJECT$/.test(r[0])&&(all||r[0]===course+'|ML_PROJECT')&&isFinite(Date.parse(r[2])))ws.getRange(i+1,3).setValue(new Date(Date.parse(r[2])+minutes*60000).toISOString());});
  }
  var alloc=book.getSheetByName('Test allocations'),changed=0;
  mlpAllocations_(book).forEach(function(a){
   if(mlpRehearsal_(a.key)||!a.started||!isFinite(Date.parse(a.deadline)))return;
   if(!(all||(course&&a.key===course+'|ML_PROJECT')||(!all&&!course&&mlpReg_(a.registration)===mlpReg_(who))))return;
   alloc.getRange(a.row,9).setValue(new Date(Date.parse(a.deadline)+minutes*60000).toISOString());changed++;
   var st=mlpState_(book,a);
   if(st.state==='COLLECTED'){
    var col=book.getSheetByName('Collection'),cr=col.getDataRange().getValues();
    cr.forEach(function(r,i){if(i&&r[0]===st.submission_id)col.getRange(i+1,11).setValue('SUPERSEDED');});
    st.state='OPEN';st.submission_id='';mlpSaveState_(book,st);
    if(a.notebookId)mlpSetRole_(a.notebookId,a.email,'writer');
   }
  });
  mlpSheet_(book,'Extensions',MLP_EXT_COLUMNS).appendRow([new Date().toISOString(),who,minutes,String(reason),changed,Session.getEffectiveUser().getEmail()].map(mlpText_));
  console.log(changed+' attempts extended by '+minutes+' minutes ('+who+').');
  return changed;
 }finally{lock.releaseLock();}
}
/** Fills the Class list sheet from a CSV exported from the gradebook and uploaded to Drive (file id). Columns found by name:
 *  registration (or student_id), full_name (or name), cohort (or course). The CSV stays in your Drive; nothing goes to the repository. */
function loadClassListFromCsv(fileId,defaultCohort){
 var rows=Utilities.parseCsv(DriveApp.getFileById(fileId).getBlob().getDataAsString());
 var head=rows[0].map(function(h){return String(h).trim().toLowerCase();});
 var col=function(names){for(var i=0;i<names.length;i++){var j=head.indexOf(names[i]);if(j>=0)return j;}return -1;};
 var r=col(['registration','student_id','registration number','student registration number']),n=col(['full_name','name','student name']),c=col(['cohort','course','class']);
 if(r<0||n<0)throw Error('The CSV needs a registration (or student_id) column and a full_name (or name) column.');
 if(c<0&&!/^CML311[123]$/.test(String(defaultCohort||'')))throw Error('The CSV has no cohort column: pass the course, for example loadClassListFromCsv(id, "CML3112").');
 var out=rows.slice(1).filter(function(x){return String(x[r]||'').trim();}).map(function(x){return [c>=0?String(x[c]).trim().toUpperCase():defaultCohort,String(x[r]).trim(),String(x[n]).trim()];});
 var sheet=mlpSheet_(mlpBook_(),'Class list',['cohort','registration','full_name']),keep=sheet.getDataRange().getValues().slice(1).filter(function(x){return out.every(function(o){return o[0]!==String(x[0]).toUpperCase();});});
 sheet.clearContents();sheet.appendRow(['cohort','registration','full_name']);
 keep.concat(out).forEach(function(x){sheet.appendRow(x.map(mlpText_));});
 console.log(out.length+' students loaded for '+Array.from(new Set(out.map(function(o){return o[0];}))).join(', ')+'; '+keep.length+' kept for other courses.');
}
/** Send every collected or checked notebook that has no result yet to GitHub Actions again. */
function redispatchMlProject(){
 var rows=mlpSheet_(mlpBook_(),'Instant checks',MLP_CHECK_COLUMNS).getDataRange().getValues().slice(1).map(mlpCheckObj_).filter(function(r){return !r.checked_at;});
 rows.forEach(function(r){console.log(r.submission_id+' '+mlpDispatch_(r.submission_id,r.kind));});
}
/** The single switch: marks become visible after the window has closed. Pass the word RELEASE. */
function releaseMlProjectMarks(confirm){if(confirm!=='RELEASE')throw Error('Run releaseMlProjectMarks("RELEASE").');mlpProps_().setProperty('ML_PROJECT_RELEASED','YES');console.log('Marks are shown after each window has closed.');}
function hideMlProjectMarks(){mlpProps_().deleteProperty('ML_PROJECT_RELEASED');}
/** The batch for the final run on the Mac (grade_project.py --zip), with the source of each notebook and the instant results. */
function exportMlProjectBatch(){
 var book=mlpBook_(),rows=book.getSheetByName('Collection').getDataRange().getValues().slice(1).filter(function(r){return r[2]==='ML_PROJECT';});
 var states={};mlpSheet_(book,'Attempt state',MLP_STATE_COLUMNS).getDataRange().getValues().slice(1).forEach(function(r){states[r[7]]=r;});
 var jobs=[],blobs=[],issues=[];
 rows.forEach(function(r){
  if(r[10]!=='COLLECTED'){issues.push(r);return;}
  blobs.push(DriveApp.getFileById(r[11]).getBlob().setName(r[0]+'.ipynb'));
  var st=states[r[0]]||[];
  jobs.push({response_id:r[0],cohort:r[1],assessment:r[2],variant:r[3],full_name:r[4],email:r[5],email_verified:true,student_registration_number:r[6],submitted_at:r[7],opens_at:r[8],closes_at:r[9],
   notebook_sha256:r[12],file:r[0]+'.ipynb',source:r[13],source_time:r[7],other_file:String(st[8]||''),late_backup_at:String(st[13]||'')});
 });
 var instant=mlpSheet_(book,'Instant checks',MLP_CHECK_COLUMNS).getDataRange().getValues().slice(1).map(mlpCheckObj_).filter(function(o){return o.kind==='grade';});
 blobs.push(Utilities.newBlob(JSON.stringify({schema:1,exported_at:new Date().toISOString(),jobs:jobs,collection_issues:issues,instant_results:instant},null,2),'application/json','manifest.json'));
 var zip=DriveApp.getFolderById(mlpProp_('FOLDER_ID')).createFile(Utilities.zip(blobs,'IUEA-ml-project-batch-'+Utilities.formatDate(new Date(),'Africa/Kampala','yyyyMMdd-HHmmss')+'.zip'));
 console.log('DOWNLOAD BATCH: https://drive.google.com/file/d/'+zip.getId()+'/view  ('+jobs.length+' notebooks, '+issues.length+' not collected)');
}
