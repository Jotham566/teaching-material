const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
let clock=Date.now(),rows=[['assessment_key','registration_normalized','email','allocation_code','variant','created_at']],counter=0,enabled='YES';
const windows={getDataRange:()=>({getValues:()=>[['key','open','close','enabled'],...['CML3111','CML3112','CML3113'].flatMap(c=>['TEST1','TEST2'].map(t=>[c+'|'+t,new Date(clock-60000).toISOString(),new Date(clock+60000).toISOString(),enabled]))]})};
const alloc={getDataRange:()=>({getValues:()=>rows}),getLastRow:()=>rows.length,getRange:()=>({setRichTextValues:r=>rows.push(...r)}),appendRow:r=>rows.push(r),setFrozenRows:()=>{}};
const ctx={Date,Math,JSON,console,SpreadsheetApp:{openById:()=>({getSheetByName:n=>n==='Test windows'?windows:alloc}),newRichTextValue:()=>({setText(s){this.s=s;return this},build(){return this.s}})},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock:()=>{}})},Utilities:{getUuid:()=>`allocation-${++counter}`,formatDate:d=>d.toISOString()},PropertiesService:{getScriptProperties:()=>({getProperty:()=> 'YES'})}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_portal/Portal.gs','utf8'),ctx);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_portal/Packets.gs','utf8'),ctx);
const input={test:'CML3111|TEST1',name:'Synthetic Test',email:'synthetic@example.com',registration:'free / form'};
let result=ctx.requestTestFiles(input),nb=JSON.parse(result.notebook),token=nb.metadata.iuea_allocation_code;
assert.equal(rows.length,2);assert.equal(ctx.requestTestFiles(input).notebook,result.notebook);assert.equal(rows.length,2);
assert(!nb.cells[1].source.includes('VARIANT'));assert(nb.cells[1].source.includes('free / form'));assert(nb.cells.at(-1).source.includes(token));
assert.equal(nb.metadata.iuea_allocated_email,input.email);assert(nb.cells[1].source.includes('_IUEA_ALLOCATED_EMAIL = '+JSON.stringify(input.email)));
assert(!Object.keys(result).includes('variant'));assert(!result.instructions.includes('assigned A, B or C'));assert(result.csv.startsWith('record_id'));
assert.throws(()=>ctx.requestTestFiles({...input,email:'other@example.com'}),/do not match/);
assert.throws(()=>ctx.requestTestFiles({...input,registration:'other'}),/already has/);
for(let i=0;i<29;i++)ctx.requestTestFiles({...input,email:`student${i}@example.com`,registration:`synthetic ${i}`});
let counts={A:0,B:0,C:0};rows.slice(1).forEach(r=>counts[r[4]]++);assert.deepEqual(counts,{A:10,B:10,C:10});
ctx.requestTestFiles({...input,email:'formula@example.com',registration:'=FREEFORM'});assert.equal(rows.at(-1)[1],'=FREEFORM');
enabled='NO';assert.throws(()=>ctx.requestTestFiles(input),/not open/);enabled='YES';clock=Date.now()-120000;assert.throws(()=>ctx.requestTestFiles(input),/closed/);clock=Date.now()+120000;assert.throws(()=>ctx.requestTestFiles(input),/opens/);clock=Date.now();
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/exam_collection.gs','utf8'),ctx);
assert.equal(ctx.examAllocation_(token,input.test,input.registration,input.email,{bookId:'book'}).code,token);
assert.throws(()=>ctx.examAllocation_(token,input.test,'wrong',input.email,{bookId:'book'}),/does not match/);
assert.throws(()=>ctx.examAllocation_(token,input.test,input.registration,'other@example.com',{bookId:'book'}),/Test allocation email mismatch: allocated to synthetic@example\.com but the form was submitted by other@example\.com/);
assert.throws(()=>ctx.examAllocation_('A',input.test,input.registration,input.email,{bookId:'book'}),/does not match/);
assert.throws(()=>ctx.examAllocation_(token,'CML3112|TEST1',input.registration,input.email,{bookId:'book'}),/does not match/);
assert.equal(Object.keys(ctx.PORTAL_PACKETS).length,18);
for(const packet of Object.values(ctx.PORTAL_PACKETS)){
 const n=JSON.parse(packet.notebook),submitCell=n.cells.find(cell=>(cell.metadata.tags||[]).includes('iuea-submission')),submitSource=submitCell.source.join('');
 assert(n.cells.at(-1).source.join('').includes("globals().get('_IUEA_ALLOCATION', VARIANT)"));
 assert(submitSource.includes("_drive.about().get(fields='user(emailAddress)')"));
 assert(submitSource.includes("_drive.files().get("));assert(submitSource.includes("authuser"));
 assert(!packet.instructions.includes('assigned A, B or C'));
}
console.log('Portal checks passed: 18 packets, stable allocation, balanced random distribution, identity conflict, literal registration, closed/early/late windows, collector binding and legacy bypass rejection.');

// Opening a page or reusing an allocation must never bypass an unopened window.
const before=rows.length;
for(const course of ['CML3111','CML3112','CML3113'])for(const exam of ['TEST1','TEST2']){
 const learner={...input,test:course+'|'+exam};
 enabled='NO';assert.throws(()=>ctx.requestTestFiles(learner),/not open/);
 enabled='YES';clock=Date.now()+120000;assert.throws(()=>ctx.requestTestFiles(learner),/opens/);
 clock=Date.now()-120000;assert.throws(()=>ctx.requestTestFiles(learner),/closed/);
}
assert.equal(rows.length,before);
console.log('All six entry points reject disabled, future and expired windows without allocating or returning files.');

// Exercise the download payload for every course, test and allocated packet.
enabled='YES';clock=Date.now();
const checked=new Set();
for(const course of ['CML3111','CML3112','CML3113'])for(const exam of ['TEST1','TEST2']){
 const key=course+'|'+exam;
 for(let i=0;i<6;i++){
  const learner={test:key,name:'Download rehearsal',email:`download-${course}-${exam}-${i}@example.com`,registration:`DEMO-DOWNLOAD-${course}-${exam}-${i}`};
  const payload=ctx.requestTestFiles(learner),notebook=JSON.parse(payload.notebook);
  const allocation=rows.find(r=>r[3]===notebook.metadata.iuea_allocation_code);
  const packetKey=key+'|'+allocation[4];checked.add(packetKey);
  const base=`IUEA_Teaching_Plan/assessment_banks/${exam}/${course}/${allocation[4]}`;
  assert.equal(payload.csv,fs.readFileSync(base+'/engineering_data.csv','utf8').replace(/\r\n/g,'\n'));
  assert.equal(payload.instructions,fs.readFileSync(base+'/ASSIGNMENT_INSTRUCTIONS.txt','utf8'));
  assert.equal(payload.notebookName,exam+'_student.ipynb');assert.equal(payload.csvName,'engineering_data.csv');
  const original=JSON.parse(fs.readFileSync(base+'/'+exam+'_student.ipynb','utf8'));
  assert.equal(notebook.cells.length,original.cells.length);
  for(let j=0;j<original.cells.length;j++)if(j!==1&&j!==original.cells.length-1)assert.deepEqual(notebook.cells[j],original.cells[j]);
  assert(notebook.cells[1].source.includes(JSON.stringify(learner.email.toLowerCase())));
  assert.equal(notebook.metadata.iuea_allocated_email,learner.email.toLowerCase());
  assert(notebook.cells.at(-1).source.includes(allocation[3]));
 }
}
assert.equal(checked.size,18);
console.log('All 18 download payloads match the current notebook questions, CSV and instructions, with correct learner identity and allocation.');
