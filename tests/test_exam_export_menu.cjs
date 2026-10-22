const fs=require('fs'),vm=require('vm'),assert=require('assert');
let cells={},props={},exportCount=0,syncs=0,locked=false;
const sheet={getRange:r=>({getValue:()=>cells[r],setValue:v=>{cells[r]=v;},getValues:()=>[[cells.E1],[cells.E2]],activate:()=>{},setValues:v=>{if(r==='A1:B5'){cells.B1=v[0][1];cells.B5=v[4][1];}else{cells.E1=v[0][1];cells.E2=v[1][1];}}})};
const book={getSheetByName:()=>sheet,setActiveSheet:()=>{},toast:()=>{}};
const lock={tryLock:()=>{if(locked)return false;locked=true;return true;},releaseLock:()=>{locked=false;}};
const c={console,SpreadsheetApp:{openById:()=>book,getActiveSpreadsheet:()=>book,flush:()=>{}},PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>{props[k]=v;}})},LockService:{getScriptLock:()=>lock,getDocumentLock:()=>lock},Utilities:{getUuid:()=> 'unique'},examConfig_:()=>({bookId:'TESTBOOK'}),syncColabExamsUnlocked_:()=>{assert(locked);syncs++;},exportColabConfig_:()=>{assert(locked);exportCount++;return {url:'https://example.test/batch',notebooks:3,issues:1};}};
vm.createContext(c);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/exam_export_menu_listener.gs','utf8'),c);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_operations/test_export_menu.gs','utf8'),c);
c.requestTestExport();assert.equal(cells.E2,'PENDING');cells.E1='first';c.requestTestExport();assert.equal(cells.E1,'first');
locked=true;c.processTestExportRequest();assert.equal(cells.E2,'PENDING');assert.equal(exportCount,0);locked=false;
c.processTestExportRequest();assert.equal(exportCount,1);assert.equal(syncs,1);assert.equal(cells.B1,'COMPLETE');assert.equal(cells.E2,'ACCEPTED');assert.equal(cells.B5,'https://example.test/batch');assert(!locked);
cells.E2='PENDING';c.processTestExportRequest();assert.equal(exportCount,1); // replay safe
cells.B1='RUNNING';c.requestTestExport();assert.equal(cells.E1,'first');
props.TEST_EXPORT_STARTED=String(Date.now()-11*60000);c.processTestExportRequest();assert.equal(cells.B1,'STOPPED');
c.requestTestExport();c.exportColabConfig_=()=>{throw Error('Drive unavailable');};assert.throws(()=>c.processTestExportRequest(),/Drive unavailable/);assert.equal(cells.B1,'STOPPED');assert(!locked);
console.log('PASS: menu deduplication, lock contention, successful export, replay, timeout and recoverable failure');
// Existing export still includes both tests, keeps collection issues and excludes rehearsal.
const e={console};vm.createContext(e);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/exam_collection.gs','utf8'),e);
const row=(id,test,status)=>[id,'CML3111',test,'A','Synthetic','synthetic@example.test','SYNTHETIC','','','',status,'file','hash'];
let manifest;
e.SpreadsheetApp={openById:()=>({getUrl:()=> 'BOOK',getSheetByName:()=>({getDataRange:()=>({getValues:()=>[[],row('one','TEST1','COLLECTED'),row('two','TEST2','COLLECTED'),row('bad','TEST1','COLLECTION_ERROR'),row('qa','TEST1','REHEARSAL')]})})})};
e.DriveApp={getFileById:()=>({getBlob:()=>({setName:()=>({})})}),getFolderById:()=>({createFile:()=>({getId:()=> 'ZIP'})})};
e.Utilities={newBlob:s=>{manifest=JSON.parse(s);return {};},zip:()=>({}),formatDate:()=> 'date'};
const result=e.exportColabConfig_({bookId:'BOOK',folderId:'FOLDER'});assert.equal(result.notebooks,2);assert.equal(result.issues,1);assert.deepEqual(manifest.jobs.map(x=>x.assessment),['TEST1','TEST2']);assert.equal(manifest.collection_issues[0][0],'bad');
console.log('PASS: Test 1 and Test 2 included, rehearsal excluded, collection issues preserved');
