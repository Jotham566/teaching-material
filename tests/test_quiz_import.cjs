const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs','utf8');
function run({email='learner@example.test',rosterEmail='learner@example.test',existing='',week=2,score=1,late=false,identityScore=null,questions=5}={}){
 const writes=[];const ctx={console};vm.createContext(ctx);vm.runInContext(source,ctx);
 const mc=()=>({getType:()=> 'MULTIPLE_CHOICE',asMultipleChoiceItem:()=>({getPoints:()=>1})});
 const response={getTimestamp:()=>new Date(late?'2026-09-18T00:00:00Z':'2026-09-16T00:00:00Z'),getRespondentEmail:()=>email,
 getItemResponses:()=>[{getItem:()=>({getTitle:()=> 'Student Registration Number'}),getResponse:()=> '99/TEST/000/DEMO-X'}],
 getGradableItemResponses:()=>[{getItem:()=>({getType:()=> 'TEXT'}),getScore:()=>identityScore},...Array.from({length:questions},()=>({getItem:mc,getScore:()=>score}))]};
 ctx.PropertiesService={getScriptProperties:()=>({getProperty:()=>JSON.stringify({['CML3112|'+week]:{formId:'quiz',closeAt:'2026-09-17T00:00:00Z'}})})};
 ctx.FormApp={ItemType:{MULTIPLE_CHOICE:'MULTIPLE_CHOICE'},openById:()=>({getResponses:()=>[response]})};
 ctx.readGradesSheet_=()=>({headers:['Student Registration Number','cohort','email','Q'+week],rows:[['99/TEST/000/DEMO-X','CML3112',rosterEmail,existing]],sheet:{getRange:(...args)=>({setValues:values=>writes.push({args,values})})}});
 try{ctx.importQuizScores();return {writes};}catch(error){return {writes,error};}
}
let result=run();assert(!result.error);assert.equal(result.writes[0].values[0][0],5);
for(const options of [{email:''},{rosterEmail:''},{email:'other@example.test'},{score:null},{score:2},{questions:4},{week:1,existing:4}]){
 result=run(options);assert(result.error,JSON.stringify(options));assert.equal(result.writes.length,0);
}
result=run({late:true,email:'other@example.test',existing:3});assert(!result.error);assert.equal(result.writes[0].values[0][0],3);
result=run({week:1,existing:5});assert(!result.error);assert.equal(result.writes[0].values[0][0],5);
console.log('Quiz import: registration aliases, zero-point identity, verified email, late exclusion, mark bounds and Week 1 protection passed');
