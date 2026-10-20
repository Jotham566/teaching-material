const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),crypto=require('crypto');
const source=fs.readFileSync('IUEA_Teaching_Plan/grader/exam_collection.gs','utf8');
function run({stamp='2026-10-19T10:00:00Z',owner='student@example.com',hashBad=false,name='Synthetic',existing=[]}={}){
 const bytes=Buffer.from(JSON.stringify({nbformat:4,cells:[]}));let copies=0;const rows=[['headers'],...existing];
 const sheet={getLastRow:()=>rows.length,getRange:()=>({getValues:()=>rows.slice(1).map(r=>[r[0]])}),appendRow:r=>rows.push(r)};
 const windows={getDataRange:()=>({getValues:()=>[['key','open','close','enabled'],['CML3111|TEST1','2026-10-19T09:00:00Z','2026-10-19T12:00:00Z','YES']]})};
 const blob={getBytes:()=>bytes,getDataAsString:()=>bytes.toString()};
 const ctx={PropertiesService:{getScriptProperties:()=>({getProperty:()=>null})},SpreadsheetApp:{openById:()=>({getSheetByName:n=>n==='Collection'?sheet:windows})},DriveApp:{getFileById:()=>({getOwner:()=>({getEmail:()=>owner}),getSize:()=>bytes.length,getBlob:()=>blob}),getFolderById:()=>({createFile:()=>{copies++;return {getId:()=> 'immutable-copy'};}})},Utilities:{DigestAlgorithm:{SHA_256:'sha256'},computeDigest:(_,b)=>[...crypto.createHash('sha256').update(b).digest()],newBlob:b=>b},console};
 vm.createContext(ctx);vm.runInContext(source,ctx);
 const vals={'Full name':name,'Student Registration Number':'DEMO / free form','Variant':'A','Snapshot file ID':'abcdefghijklmno','Snapshot SHA-256':hashBad?'0'.repeat(64):crypto.createHash('sha256').update(bytes).digest('hex')};
 const response={getId:()=> 'receipt',getTimestamp:()=>new Date(stamp),getRespondentEmail:()=> 'student@example.com',getItemResponses:()=>Object.entries(vals).map(([k,v])=>({getItem:()=>({getTitle:()=>k}),getResponse:()=>v}))};
 ctx.examCollect_(response,'CML3111|TEST1',{bookId:'book',folderId:'folder'});return {row:rows.at(-1),rows,copies};
}
assert.equal(run().row[10],'COLLECTED');assert.equal(run().copies,1);
assert.equal(run({stamp:'2026-10-19T12:00:01Z'}).row[10],'OUTSIDE_WINDOW');
assert.equal(run({stamp:'2026-10-19T08:59:59Z'}).copies,0);
assert.equal(run({hashBad:true}).row[10],'COLLECTION_ERROR');
assert.equal(run({owner:'different@example.com'}).copies,0);
assert.equal(run({name:'=1+1'}).row[4],"'=1+1");
assert.equal(run({existing:[['receipt']]}).copies,0);
console.log('Collector checks passed: valid, late, early, changed snapshot, wrong owner, formula text, duplicate.');
