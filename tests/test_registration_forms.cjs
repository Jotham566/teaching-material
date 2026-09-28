const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={console,Logger:{log:()=>{}},LockService:{getScriptLock:()=>({waitLock:()=>{},releaseLock:()=>{}})}};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/submission_forms.gs','utf8'),ctx);
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/registration_freeform_migration.gs','utf8'),ctx);
const state={
 'CML3112|W02':{formId:'one',openAt:'2026-09-15',closeAt:'2026-09-22',assessmentReleased:true},
 'CML3113|W03':{formId:'two',openAt:null,closeAt:null,assessmentReleased:false},
 'DA|S05':{formId:'da',closeAt:null}
};
const original=JSON.parse(JSON.stringify(state));
const items={};
for(const [id,title] of [['one','Student Registration Number'],['two','student_id'],['da','Student ID']]){
 items[id]={title,required:false,validation:'old pattern',changes:0,
  getTitle(){return this.title;},asTextItem(){return this;},getId(){return id;},
  setRequired(v){this.required=v;return this;},isRequired(){return this.required;},
  setHelpText(v){this.help=v;return this;},setTitle(v){this.title=v;return this;},
  clearValidation(){this.validation=null;this.changes++;return this;}
 };
}
ctx.FormApp={ItemType:{TEXT:'TEXT'},openById:id=>({getItems:()=>[items[id]]})};
ctx.submissionState_=()=>state;ctx.saveSubmissionState_=()=>{};
ctx.makeIueaRegistrationRequiredFreeform();ctx.makeIueaRegistrationRequiredFreeform();
for(const key of ['CML3112|W02','CML3113|W03']){
 const row=state[key],item=items[row.formId];
 assert.equal(item.validation,null);assert.equal(item.required,true);assert.equal(item.changes,1);
 assert.equal(item.getId(),original[key].formId);
 for(const field of Object.keys(original[key]))assert.equal(row[field],original[key][field]);
}
assert.equal(items.da.validation,'old pattern');assert.equal(items.da.changes,0);
assert.deepStrictEqual(state['DA|S05'],original['DA|S05']);
console.log('IUEA migration removes the pattern, keeps required identity items, preserves windows/releases and resumes safely; DA untouched.');

assert.equal(ctx.sheetText_('=DEMO'), "'=DEMO");
assert.equal(ctx.sheetText_('99/0000/DEMO-X'), '99/0000/DEMO-X');
assert.ok(fs.readFileSync('IUEA_Teaching_Plan/grader/submission_forms.gs','utf8').includes('key,sheetText_(sid),r.getRespondentEmail()'));
