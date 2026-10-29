/** Private lecturer dashboard. Reads source tabs; writes only Test Monitor.
 * Install in the lecturer-owned collector project, never the public portal.
 */
function testMonitorRows_(allocations,receipts,windows,now){
 var norm=function(x){return String(x||'').trim().toUpperCase().replace(/\s+/g,'');};
 var email=function(x){return String(x||'').trim().toLowerCase();};
 var stamp=function(x){var n=x instanceof Date?x.getTime():Date.parse(x);return isFinite(n)?n:null;};
 var windowMap={};windows.slice(1).forEach(function(w){windowMap[w[0]]=w;});
 var used={},rows=[];
 allocations.slice(1).forEach(function(a){
  if(!/^CML311[123]\|TEST[12]$/.test(a[0])||/^DEMO|^REHEARSAL/i.test(String(a[1])))return;
  var issued=stamp(a[5]);
  var matches=[];receipts.slice(1).forEach(function(r,i){
   if(r[10]==='REHEARSAL'||r[1]+'|'+r[2]!==a[0])return;
   // Match BOTH entry identifiers. Do not silently merge conflicting accounts.
   if(norm(r[6])===norm(a[1])&&email(r[5])===email(a[2])){matches.push(r);used[i]=true;}
  });
  var accepted=matches.filter(function(r){return r[10]==='COLLECTED';});
  // A lecturer reset issues a new allocation: failures and superseded receipts from
  // before it are history (kept in Collection), not the student's current status.
  var current=matches.filter(function(r){return r[10]!=='SUPERSEDED_FOR_RETRY'&&(issued===null||(stamp(r[7])||0)>=issued);});
  var latest=current.slice().sort(function(a,b){return (stamp(b[7])||0)-(stamp(a[7])||0);})[0];
  var w=windowMap[a[0]],start=stamp(a[7]),personal=stamp(a[8]),close=w?stamp(w[2]):null;
  var deadline=personal!==null&&close!==null?Math.min(personal,close):personal!==null?personal:close;
  var status,detail='';
  if(accepted.length){status='Submitted';if(matches.length>accepted.length)detail='Accepted submission retained; additional receipt needs review in Collection.';}
  else if(latest){status='Submission needs attention';detail=String(latest[10])+': '+String(latest[14]||'Check Collection.');}
  else if(w&&!start&&issued!==null&&String(w[3]).toUpperCase()==='YES'){status='Not started';detail='Issued or reset by the lecturer; the timer starts when the student opens the test.';}
  else if(!w||!start||!deadline){status='Timer needs attention';detail='Missing start time or deadline; inspect Test allocations and Test windows.';}
  else if(String(w[3]).toUpperCase()!=='YES'){status='Test disabled';}
  else if(now>deadline){status='Time expired without accepted submission';}
  else {status='In progress';}
  var submission=accepted[0]||latest;
  rows.push({key:a[0],name:String(a[6]||''),reg:String(a[1]||''),email:String(a[2]||''),start:start,deadline:deadline,status:status,remaining:status==='In progress'?Math.max(0,Math.ceil((deadline-now)/60000)):'',submitted:submission?stamp(submission[7]):null,detail:detail,allocation:String(a[3]||''),started:!!start});
 });
 receipts.slice(1).forEach(function(r,i){
  if(used[i]||r[10]==='REHEARSAL'||r[10]==='SUPERSEDED_FOR_RETRY'||!/^CML311[123]$/.test(r[1]))return;
  // A failed receipt (e.g. mistyped registration) is resolved once the same student was reissued an allocation later.
  if(r[10]!=='COLLECTED'&&allocations.slice(1).some(function(a){
   var issued=stamp(a[5]);
   return a[0]===r[1]+'|'+r[2]&&issued!==null&&issued>(stamp(r[7])||0)&&(norm(a[1])===norm(r[6])||email(a[2])===email(r[5]));
  }))return;
  rows.push({key:r[1]+'|'+r[2],name:String(r[4]||''),reg:String(r[6]||''),email:String(r[5]||''),start:null,deadline:null,status:'Submission needs attention',remaining:'',submitted:stamp(r[7]),detail:'No exact entry match. '+r[10]+': '+String(r[14]||'Check both identifiers in Collection and Test allocations.'),allocation:'',started:false});
 });
 return rows.sort(function(a,b){return a.key.localeCompare(b.key)||(a.start||0)-(b.start||0)||a.reg.localeCompare(b.reg);});
}
function refreshTestMonitor(){
 var lock=LockService.getScriptLock();if(!lock.tryLock(1000))return;
 try{
  var c=examConfig_();if(!c.bookId)throw Error('Test collection workbook is not configured.');
  var book=SpreadsheetApp.openById(c.bookId),read=function(name){var s=book.getSheetByName(name);return s?s.getDataRange().getValues():[];};
  var windows=read('Test windows'),now=Date.now(),rows=testMonitorRows_(read('Test allocations'),read('Collection'),windows,now);
  var s=book.getSheetByName('Test Monitor')||book.insertSheet('Test Monitor');
  var local=function(ms){return ms===null?'':Utilities.formatDate(new Date(ms),'Africa/Kampala','yyyy-MM-dd HH:mm:ss');};
  var grid=[['Test Monitor — Kampala time (UTC+3)'],['Updated: '+local(now)+' | Automatic refresh about every 5 minutes.'],['In progress = timer open, not proof the student is online. Submitted = accepted for grading, not a grade.'],['No roster: students who have never started cannot be listed. Unmatched receipts are shown separately for review.'],[],['Programme / test','Window status','Opens (Kampala)','Closes (Kampala)','Started attempts','In progress','Submitted','Expired','Needs attention','Unmatched receipts']];
  ['CML3111','CML3112','CML3113'].forEach(function(course){['TEST1','TEST2'].forEach(function(test){
   var key=course+'|'+test,w=windows.slice(1).filter(function(w){return w[0]===key;})[0],subset=rows.filter(function(r){return r.key===key;}),count=function(status){return subset.filter(function(r){return r.status===status;}).length;};
   var open=w?Date.parse(w[1]):NaN,close=w?Date.parse(w[2]):NaN;
   var state=!w||String(w[3]).toUpperCase()!=='YES'?'Disabled':!isFinite(open)||!isFinite(close)?'Schedule needs attention':now<open?'Scheduled':now>close?'Closed':'Open';
   grid.push([course+' '+test,state,isFinite(open)?local(open):'',isFinite(close)?local(close):'',subset.filter(function(r){return r.started;}).length,count('In progress'),count('Submitted'),count('Time expired without accepted submission'),subset.filter(function(r){return /attention|disabled/i.test(r.status);}).length,subset.filter(function(r){return !r.allocation;}).length]);
  });});
  grid.push([],['Student activity — use the filter on the header below. Read-only report; make corrections in the source tabs.']);
  var headerRow=grid.length+1;
  grid.push(['Programme / test','Full name','Student ID/ Registration Number','Google email','Started (Kampala)','Deadline (Kampala)','Status','Minutes left at refresh','Submitted (Kampala)','Details','Allocation reference']);
  rows.forEach(function(r){grid.push([r.key.replace('|',' '),r.name,r.reg,r.email,local(r.start),local(r.deadline),r.status,r.remaining,local(r.submitted),r.detail,r.allocation]);});
  var width=11;grid=grid.map(function(r){while(r.length<width)r.push('');return r.map(function(v){return typeof v==='string'&&/^[=+@-]/.test(v)?"'"+v:v;});});
  if(s.getMaxRows()<grid.length)s.insertRowsAfter(s.getMaxRows(),grid.length-s.getMaxRows());
  if(s.getMaxColumns()<width)s.insertColumnsAfter(s.getMaxColumns(),width-s.getMaxColumns());
  // Write data first; clear only obsolete report rows, never a source tab.
  var oldRows=s.getLastRow();s.getRange(1,1,grid.length,width).setValues(grid);
  if(oldRows>grid.length)s.getRange(grid.length+1,1,oldRows-grid.length,width).clearContent();
  s.getRange(1,1,grid.length,width).setFontFamily('Arial').setFontSize(11).setVerticalAlignment('top').setWrap(true).setBackground('#FFFFFF').setFontColor('#172C40');
  [1,6,headerRow].forEach(function(r){s.getRange(r,1,1,width).setBackground('#1C3144').setFontColor('#FFFFFF').setFontWeight('bold');});
  s.setFrozenRows(1);s.setFrozenColumns(0);s.setHiddenGridlines(true);
  [150,220,230,250,180,180,290,130,180,420,200].forEach(function(w,i){s.setColumnWidth(i+1,w);});
  [1,2,3,4,headerRow-1].forEach(function(r){s.getRange(r,1,1,width).mergeAcross();});
  s.setRowHeights(1,4,38);s.setRowHeight(headerRow,48);
  var filter=s.getFilter(),criteria={};if(filter){for(var col=1;col<=width;col++){var criterion=filter.getColumnFilterCriteria(col);if(criterion)criteria[col]=criterion;}filter.remove();}if(rows.length){var updatedFilter=s.getRange(headerRow,1,rows.length+1,width).createFilter();Object.keys(criteria).forEach(function(col){updatedFilter.setColumnFilterCriteria(Number(col),criteria[col]);});}
  rows.forEach(function(r,i){s.getRange(headerRow+i+1,7).setBackground(r.status==='Submitted'?'#DDF1E4':r.status==='In progress'?'#DBEEF8':'#FFF0CC');});
  SpreadsheetApp.flush();
  console.log('Test Monitor refreshed: '+rows.length+' rows. '+book.getUrl()+'#gid='+s.getSheetId());
 }finally{lock.releaseLock();}
}
function installTestMonitor(){
 refreshTestMonitor();
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='refreshTestMonitor';}))ScriptApp.newTrigger('refreshTestMonitor').timeBased().everyMinutes(5).create();
 console.log('Automatic Test Monitor refresh installed (5 minutes). Source records and schedules unchanged.');
}
