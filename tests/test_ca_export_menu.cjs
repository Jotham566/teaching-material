const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source='IUEA_Teaching_Plan/assessment_operations/';
let cells={},props={},queued=0,started=0,released=0;
const sheet={getRange:r=>({getValue:()=>cells[r],setValue:v=>{cells[r]=v;},getValues:()=>[[cells.E1],[cells.E2]],setValues:v=>{cells.E1=v[0][1];cells.E2=v[1][1];},activate:()=>{}})};
const book={getSheetByName:()=>sheet,setActiveSheet:()=>{},toast:()=>{}};
const lock={tryLock:()=>true,releaseLock:()=>released++};
const c={SpreadsheetApp:{getActiveSpreadsheet:()=>book,flush:()=>{}},LockService:{getDocumentLock:()=>lock,getScriptLock:()=>lock},Utilities:{getUuid:()=> 'request-new'},submissionBook_:()=>book,PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>{props[k]=v;}})},ScriptApp:{getProjectTriggers:()=>[],newTrigger:()=>({timeBased:()=>({after:()=>({create:()=>queued++})})})}};
vm.createContext(c);vm.runInContext(fs.readFileSync(source+'export_continuous_assessment.gs','utf8'),c);vm.runInContext(fs.readFileSync(source+'ca_export_menu.gs','utf8'),c);
c.startCAExport=id=>{started++;props.CA_EXPORT_REQUEST_ID=id;props.CA_EXPORT_STATE='RUNNING';};
cells={B1:'COMPLETE'};c.requestGradingZip();assert.equal(cells.E2,'PENDING');
cells.E1='first';c.requestGradingZip();assert.equal(cells.E1,'first'); // double click keeps request
c.processCAExportRequest();assert.equal(started,1);assert.equal(queued,1);assert.equal(cells.E2,'ACCEPTED');
c.processCAExportRequest();assert.equal(started,1);assert.equal(queued,1);
props.CA_EXPORT_STATE='COMPLETE';cells.E2='PENDING';c.processCAExportRequest();assert.equal(started,1);assert.equal(queued,1); // replay after completion
cells.B1='RUNNING';cells.E1='existing';cells.E2='ACCEPTED';c.requestGradingZip();assert.equal(cells.E1,'existing');
cells.B1='STOPPED';props.CA_EXPORT_STATE='STOPPED';c.requestGradingZip();c.processCAExportRequest();assert.equal(started,1);assert.equal(queued,2);
cells.E2='PENDING';c.LockService.getScriptLock=()=>({tryLock:()=>false});c.processCAExportRequest();assert.equal(cells.E2,'PENDING');
c.LockService.getScriptLock=()=>lock;cells.E1='fresh';props.CA_EXPORT_STATE='COMPLETE';c.startCAExport=()=>{throw Error('Mirror is stale');};assert.throws(()=>c.processCAExportRequest(),/stale/);assert.match(cells.E2,/ERROR:.*stale/);assert(released>0);
console.log('PASS: menu queues once; running export retained; stopped export resumed; completed request replay safe; lock retry and errors preserved');
