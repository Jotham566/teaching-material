import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {handle} from '../IUEA_Teaching_Plan/test_portal/gateway/worker.mjs';
const secret='synthetic-test-secret-not-for-production-12345';
let mode='open',counter=0,rows=[['key','reg','email','code','variant','created']];
const keys=['CML3111','CML3112','CML3113'].flatMap(c=>['TEST1','TEST2'].map(t=>c+'|'+t));
const ctx={Date,Math,JSON,Error,PropertiesService:{getScriptProperties:()=>({getProperty:()=>secret})},
 SpreadsheetApp:{openById:()=>({getSheetByName:n=>n==='Test windows'?{getDataRange:()=>({getValues:()=>[['key','open','close','enabled'],...keys.map(k=>[k,new Date(Date.now()+(mode==='future'?60000:-60000)).toISOString(),new Date(Date.now()+(mode==='expired'?-1000:120000)).toISOString(),mode==='disabled'?'NO':'YES'])]})}:{getDataRange:()=>({getValues:()=>rows}),getLastRow:()=>rows.length,getRange:()=>({setRichTextValues:r=>rows.push(...r)})}}),newRichTextValue:()=>({setText(s){this.s=s;return this},build(){return this.s}})},
 LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock:()=>{}})},Utilities:{getUuid:()=>`synthetic-${++counter}`,formatDate:d=>d.toISOString()},
 ContentService:{MimeType:{JSON:'application/json'},createTextOutput:text=>({text,setMimeType(){return this}})}};
vm.createContext(ctx);
for(const file of ['Portal.gs','Packets.gs','Gateway.gs'])vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/test_portal/'+file,'utf8'),ctx);
const env={PORTAL_GATEWAY_KEY:secret,APPS_SCRIPT_URL:'https://script.google.com/macros/s/TEST_DEPLOYMENT/exec'};
let calls=0;
const upstream=async(url,options)=>{
 calls++;assert.equal(url,env.APPS_SCRIPT_URL);assert.equal(options.redirect,'follow');assert.equal(options.headers.Cookie,undefined);assert.equal(options.headers.Authorization,undefined);
 return new Response(ctx.doPost({postData:{contents:options.body}}).text,{headers:{'Content-Type':'application/json'}});
};
const request=input=>new Request('https://test.example/api/files',{method:'POST',headers:{Origin:'https://test.example','Content-Type':'application/json',Cookie:'Google-account=must-not-forward'},body:JSON.stringify(input)});
const learner=test=>({test,name:'Synthetic learner',email:'demo@example.com',registration:'DEMO / freeform'});
for(const key of keys){
 const page=await handle(new Request('https://test.example/?test='+encodeURIComponent(key)),env,upstream);const html=await page.text();
 assert.equal(page.status,200);assert(html.includes(JSON.stringify(key)));assert(!html.includes('google.script.run'));assert(!html.includes(secret));assert(!html.includes('/macros/'));assert(html.includes("fetch('/api/files'"));
 const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(script);
 // All browser input goes through the worker and authenticated backend adapter.
 mode='open';let payloads=[];
 for(let i=0;i<3;i++){
  const input={...learner(key),email:`demo${i}@example.com`,registration:`DEMO / ${i}`};
  const response=await handle(request(input),env,upstream);assert.equal(response.status,200);assert.equal(response.headers.get('Cache-Control'),'no-store, private');
  const result=(await response.json()).result;payloads.push(result);
  assert(result.csv.startsWith('record_id'));assert.equal(result.csvName,'engineering_data.csv');assert.equal(result.notebookName,key.split('|')[1]+'_student.ipynb');
  const nb=JSON.parse(result.notebook);assert(nb.cells[1].source.includes(input.email));assert(nb.metadata.iuea_allocation_code);
  const repeat=(await (await handle(request(input),env,upstream)).json()).result;assert.equal(result.notebook,repeat.notebook);
 }
 assert.equal(new Set(payloads.map(p=>JSON.parse(p.notebook).metadata.iuea_allocation_code)).size,3);
 const before=rows.length;
 for(const state of ['future','expired','disabled']){mode=state;const result=await handle(request(learner(key)),env,upstream);assert.equal(result.status,409);const body=await result.json();assert.equal(body.ok,false);assert.equal(body.result,undefined);assert.match(body.error,/opens|closed|not open/);}
 assert.equal(rows.length,before);
}
assert.equal(rows.length,19);
let before=calls;
assert.equal((await handle(request(learner(keys[0])),{},upstream)).status,503);
assert.equal((await handle(new Request('https://test.example/api/files',{method:'POST',headers:{Origin:'https://other.example','Content-Type':'application/json'},body:'{}'}),env,upstream)).status,403);
assert.equal((await handle(request({...learner(keys[0]),registration:''}),env,upstream)).status,400);
assert.equal((await handle(request({...learner(keys[0]),name:'x'.repeat(9000)}),env,upstream)).status,400);
assert.equal(calls,before);
const denied=JSON.parse(ctx.doPost({postData:{contents:JSON.stringify({secret:'wrong',input:learner(keys[0])})}}).text);assert.equal(denied.ok,false);
const network=await handle(request(learner(keys[0])),env,async()=>{throw Error('private upstream error')});assert.equal(network.status,502);assert(!(await network.text()).includes('private upstream'));
const googleError=await handle(request(learner(keys[0])),env,async()=>new Response('<html>Google error</html>'));assert.equal(googleError.status,502);
console.log('PASS: all 6 routes, all 18 allocations, stable repeated downloads, all 6 early/expired/disabled windows, no browser Google RPC, no cookie forwarding, no caching, malformed requests, secret failures and upstream errors.');
