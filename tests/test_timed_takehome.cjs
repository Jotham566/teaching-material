const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
let windowKey='CML3111|TEST1';
let now=Date.parse('2026-10-23T16:00:00Z'),end=Date.parse('2026-10-29T20:59:00Z'),rows=[['headers']],fileCount=0;
const RealDate=Date;class Clock extends Date {constructor(x){super(x===undefined?now:x)}static now(){return now;}}
const range=(row,col=1,height=1,width=1)=>({getValues:()=>rows.slice(row-1,row-1+height).map(r=>r.slice(col-1,col-1+width)),setValues(v){v.forEach((r,i)=>{rows[row-1+i]??=[];r.forEach((x,j)=>rows[row-1+i][col-1+j]=x);});},setRichTextValues(v){this.setValues(v)},setValue(v){this.setValues([[v]])}});
const sheet={getDataRange:()=>({getValues:()=>rows}),getLastRow:()=>rows.length,getRange:range};
const windowRows=()=>[['key','open','close','enabled','duration'],[windowKey,'2026-10-23T16:00:00Z',new Date(end).toISOString(),'YES',180]];
const book={getSheetByName:n=>n==='Test windows'?{getDataRange:()=>({getValues:windowRows})}:sheet};
let driveCalls=[];let props={};const ctx={Date:Clock,Math,JSON,console,SpreadsheetApp:{openById:()=>book,newRichTextValue:()=>({setText(v){this.v=v;return this},build(){return this.v}})},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock(){}})},PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>props[k]=v})},Utilities:{getUuid:()=> 'synthetic-code',formatDate:d=>d.toISOString(),newBlob:b=>b},ScriptApp:{getOAuthToken:()=> 'never-real'},UrlFetchApp:{fetch:(url,options)=>{driveCalls.push({url,options});return {getResponseCode:()=>200}}},DriveApp:{createFolder:()=>({getId:()=> 'private-folder'}),getFolderById:()=>({createFile:()=>{const id='file-'+(++fileCount);return {getId:()=>id};}})}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_portal/Portal.gs','utf8'),ctx);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_portal/Packets.gs','utf8'),ctx);
const input={test:'CML3111|TEST1',registration:'DEMO / Timed',email:'synthetic@example.com',name:'Synthetic learner'};
let result=ctx.requestTestFiles(input);assert.equal(result.personalDeadline,'2026-10-23T19:00:00.000Z');assert.equal(rows[1][6],input.name);assert(result.colabUrl.includes('/drive/file-1'));let nb=JSON.parse(result.notebook);assert(nb.cells[3].source.includes('_csv_file.write'));assert(nb.cells[0].source.includes('Take-home'));assert.equal(fileCount,1);if(process.env.IUEA_TEST_PACKET_OUT)fs.writeFileSync(process.env.IUEA_TEST_PACKET_OUT,JSON.stringify(nb));
assert(!result.colabUrl.includes('authuser='));assert.equal(result.workingMode,'DIRECT');assert.equal(result.resumed,false);assert(driveCalls.some(c=>JSON.parse(c.options.payload).role==='writer'));assert(driveCalls.some(c=>JSON.parse(c.options.payload).writersCanShare===false));assert(nb.cells[1].source.includes('Test countdown'));assert(nb.cells[1].source.includes(result.personalDeadline));
now+=3600000;let again=ctx.requestTestFiles(input);assert.equal(again.personalDeadline,result.personalDeadline);assert.equal(again.colabUrl,result.colabUrl);assert.equal(fileCount,1);assert.equal(again.resumed,true);
const spaced=ctx.requestTestFiles({...input,registration:'demo/timed'});assert.equal(spaced.colabUrl,result.colabUrl);assert.equal(spaced.personalDeadline,result.personalDeadline);assert.equal(rows.length,2);assert.throws(()=>ctx.requestTestFiles({...input,registration:'DEMO/OTHER'}),/already has/);assert.throws(()=>ctx.requestTestFiles({...input,email:'other@example.com'}),/do not match/);
now=Date.parse(result.personalDeadline)+1;assert.throws(()=>ctx.requestTestFiles(input),/personal deadline/);assert.equal(rows.length,2);
rows=[['headers']];now=end-60000;result=ctx.requestTestFiles(input);assert.equal(Date.parse(result.personalDeadline),end);
now=end+1;assert.throws(()=>ctx.requestTestFiles(input),/closed/);
// Historical allocation created during rehearsal gets a new saved timer only on first timed start.
rows=[['headers'],['CML3111|TEST1','DEMO / TIMED','synthetic@example.com','T-old','A','2026-10-19T00:00:00Z']];now=Date.parse('2026-10-23T16:00:00Z');result=ctx.requestTestFiles(input);assert.equal(result.startedAt,new Date(now).toISOString());assert.equal(rows[1][3],'T-old');
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/exam_collection.gs','utf8'),ctx);
let collected=[];const collection={getLastRow:()=>1,appendRow:r=>collected.push(r)};
const originalGet=book.getSheetByName;book.getSheetByName=n=>n==='Collection'?collection:originalGet(n);
const vals={'Full name':'Synthetic learner','Student Registration Number':'DEMO / TIMED','Test allocation code':'T-old'};
const response={getId:()=> 'late-synthetic',getTimestamp:()=>new Date(now+3*3600000+1),getRespondentEmail:()=>input.email,getItemResponses:()=>Object.entries(vals).map(([k,v])=>({getItem:()=>({getTitle:()=>k}),getResponse:()=>v}))};
ctx.examCollect_(response,input.test,{bookId:'book'});assert.equal(collected[0][10],'OUTSIDE_PERSONAL_WINDOW');assert.equal(collected[0][9],result.personalDeadline);
console.log('PASS timed test: stored identity, stable timer/file, refresh, strict expiry, global cutoff, historical allocation migration, collector rejection of late form.');
// On-time collection exports the personal deadline, independently of notebook metadata.
const crypto=require('crypto');const bytes=Buffer.from(JSON.stringify({nbformat:4,cells:[],metadata:{iuea_allocation_code:'T-old'}}));
vals['Snapshot file ID']='synthetic-snapshot-id';vals['Snapshot SHA-256']=crypto.createHash('sha256').update(bytes).digest('hex');
ctx.Utilities.DigestAlgorithm={SHA_256:'sha256'};ctx.Utilities.computeDigest=(_,b)=>[...crypto.createHash('sha256').update(b).digest()];
ctx.DriveApp.getFileById=()=>({getOwner:()=>({getEmail:()=>input.email}),getSize:()=>bytes.length,getBlob:()=>({getBytes:()=>bytes,getDataAsString:()=>bytes.toString()})});
response.getTimestamp=()=>new Date(now+60*1000);response.getId=()=> 'ontime-synthetic';ctx.examCollect_(response,input.test,{bookId:'book',folderId:'private-folder'});
assert.equal(collected.at(-1)[10],'COLLECTED');assert.equal(collected.at(-1)[8],result.startedAt);assert.equal(collected.at(-1)[9],result.personalDeadline);
response.getId=()=> 'missing-timer';rows[1][7]='';rows[1][8]='';ctx.examCollect_(response,input.test,{bookId:'book'});assert.equal(collected.at(-1)[10],'COLLECTION_ERROR');
console.log('PASS collector: on-time snapshot accepted with personal timestamps; missing timer fails closed.');

// Exercise every timed Test 1 cohort/variant, including the embedded CSV bytes.
book.getSheetByName=originalGet;
for(const cohort of ['CML3111','CML3112','CML3113'])for(const variant of ['A','B','C']){
 windowKey=cohort+'|TEST1';now=Date.parse('2026-10-23T16:00:00Z');
 rows=[['headers'],[windowKey,'DEMO / TIMED',input.email,'T-'+cohort+'-'+variant,variant,'2026-10-19T00:00:00Z']];
 const issued=ctx.requestTestFiles({...input,test:windowKey});const notebook=JSON.parse(issued.notebook);
 const packet=ctx.PORTAL_PACKETS[windowKey+'|'+variant];
 assert.equal(issued.csv,packet.csv);
 assert(notebook.cells[3].source.includes(JSON.stringify(packet.csv)));
 assert(notebook.cells[1].source.includes(cohort));
 assert.equal(notebook.metadata.iuea_allocation_code,rows[1][3]);
 assert(notebook.cells.at(-1).source.includes('_IUEA_DEADLINE = '+JSON.stringify(issued.personalDeadline)));
 assert(notebook.cells.at(-1).source.includes('_check_submission_time()'));
 assert.equal(issued.personalDeadline,'2026-10-23T19:00:00.000Z');
 const baseline=JSON.parse(packet.notebook);
 for(let i=4;i<notebook.cells.length-1;i++)if(baseline.cells[i].cell_type==='code')assert.deepEqual(notebook.cells[i].source,baseline.cells[i].source);
 const repeat=ctx.requestTestFiles({...input,test:windowKey});assert.equal(repeat.colabUrl,issued.colabUrl);assert.equal(repeat.personalDeadline,issued.personalDeadline);
}
console.log('PASS all nine timed Test 1 packets: correct cohort, allocation, unchanged task code, exact CSV, three-hour deadline and stable resume.');

// Existing reader originals must never be represented as saved student work.
rows[1][11]='COPY';const legacy=ctx.requestTestFiles({...input,test:windowKey});assert.equal(legacy.workingMode,'COPY');assert(legacy.instructions.includes('Save a copy'));assert.equal(legacy.colabUrl,ctx.requestTestFiles({...input,test:windowKey}).colabUrl);
console.log('PASS: formatting-only resume, conflicting identity rejection, private editable file, sharing restriction, notebook countdown and legacy copies.');
// Countdown is presentation only and cannot reset the deadline on rerun.
const timerSource=ctx.portalCountdownCode_('2026-10-23T19:00:00.000Z');
assert.match(timerSource,/Kampala time/);assert.ok(!timerSource.includes('__LOCAL_DEADLINE__'));
const timerScript=timerSource.match(/<script>([\s\S]*?)<\/script>/)[1];
let timerNow=Date.parse('2026-10-23T18:00:00Z'),timerTick;
class DisplayClock extends Date{static now(){return timerNow;}}
const timerText={},timerReminder={},timerBox={isConnected:true,querySelector:s=>s==='.iuea-clock'?timerText:timerReminder};
const timerContext={Date:DisplayClock,Math,document:{currentScript:{previousElementSibling:timerBox}},setInterval:f=>{timerTick=f;return 1},clearInterval(){}};
vm.runInNewContext(timerScript,timerContext);assert.equal(timerText.textContent,'1h 0m 0s remaining');
timerNow+=60000;timerTick();assert.equal(timerText.textContent,'0h 59m 0s remaining');
vm.runInNewContext(timerScript,timerContext);assert.equal(timerText.textContent,'0h 59m 0s remaining');
timerNow=Date.parse('2026-10-23T18:40:00Z');timerTick();assert.match(timerReminder.textContent,/complete the submission form/);
timerNow+=3600000;timerTick();assert.match(timerText.textContent,/Time has ended/);
console.log('PASS countdown ticking, rerun without reset and expiry.');
