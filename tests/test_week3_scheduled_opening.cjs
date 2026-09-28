const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const target=Date.parse('2026-09-22T10:55:00+03:00');let now=target-60000,opens=0,closes=0,accepting=false,props={},triggers=[];
const L={formId:'1IJ9gMwpUg8Il9nqP3OPMDDTw7zFkV655RmWqw9TgsmY',short:'quiz-link'};
class Clock extends Date {static now(){return now;}}
const c={Date:Clock,WINDOW_HOURS:24,Logger:{log(){}},PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>{props[k]=v;}})},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock(){}})},loadLinks_:()=>({'CML3112|3':L}),FormApp:{openById:()=>({isAcceptingResponses:()=>accepting})},openQuizFor:()=>{opens++;accepting=true;L.openedAt=now;L.closeAt=now+86400000;},closeQuiz:()=>{closes++;accepting=false;},ScriptApp:{getProjectTriggers:()=>triggers,deleteTrigger:t=>{triggers=triggers.filter(x=>x!==t);},newTrigger:handler=>{const b={timeBased:()=>b,everyMinutes:()=>b,at:()=>b,create:()=>{triggers.push({getHandlerFunction:()=>handler});}};return b;}}};
vm.createContext(c);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/week3_scheduled_opening.gs','utf8'),c);
c.schedule_W3_CML3112_Sept22();assert.equal(opens,0);assert.equal(triggers.length,2);
now=target;c.maintainScheduled_W3_CML3112();assert.equal(opens,1);assert.equal(L.closeAt-L.openedAt,86400000);
const deadline=L.closeAt;now+=300000;c.schedule_W3_CML3112_Sept22();assert.equal(opens,1);assert.equal(L.closeAt,deadline);
now=deadline-1;c.maintainScheduled_W3_CML3112();assert.equal(closes,0);
now=deadline;c.maintainScheduled_W3_CML3112();assert.equal(closes,1);assert.equal(triggers.length,0);
c.maintainScheduled_W3_CML3112();assert.equal(opens,1);assert.equal(closes,1);
console.log('PASS: no early opening, scheduled activation, 24-hour deadline, retry without extension, no early close, cleanup and no reopening');
