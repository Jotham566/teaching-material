const fs=require('fs'),vm=require('vm'),assert=require('assert');
const c={};vm.createContext(c);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/gradebook.gs','utf8'),c);
for(const cohort of ['CML3111','CML3112','CML3113']){
 const row={cohort,quizzes:Array(12).fill(5),challenges:Array(11).fill(20),dataProject:100,test1:100,test2:100,mlProject:100,demo:100};
 row.quizzes[5]='';row.challenges[5]='';const before=JSON.stringify(row);const r=c.computeFinal_(row);assert.equal(r.final,100);assert.equal(r.missing.length,0);assert.equal(JSON.stringify(row),before);
 row.quizzes[5]=5;row.challenges[5]=20;assert.equal(c.computeFinal_(row).final,100);
 const only={cohort,quizzes:['','','','','',5],challenges:['','','','','',20]};assert.equal(c.computeFinal_(only).final,0);
 assert.match(c.progressSummary_(row),/best 9/);assert.match(c.progressSummary_(row),/best 7/);
 assert.match(c.progressSummary_(only),/not assigned/);
}
assert.equal(c.computeFinal_({cohort:'CML3111',quizzes:['','','','','',5],challenges:['','','','','',20]}).final,0);
console.log('PASS: waived marks excluded, full marks reachable, raw records immutable, all three programmes covered');
const q={};vm.createContext(q);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/create_quiz_forms.gs','utf8'),q);
for(const cohort of ['CML3111','CML3112','CML3113'])assert.throws(()=>q.openQuizFor(6,cohort),/waived/);
const a={};vm.createContext(a);vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/grader/submission_forms.gs','utf8'),a);
for(const cohort of ['CML3111','CML3112','CML3113']){
 assert.throws(()=>a.setSubmissionWindow(cohort+'|W06','2026-10-20T08:00:00+03:00','2026-10-27T08:00:00+03:00'),/waived/);
 assert.equal(a.submissionAssessmentReleased_(cohort+'|W06',{assessmentReleased:true,releaseEvidence:'Previously validated assessment release.'}),false);
}
console.log('PASS: waived forms cannot be reactivated by the ordinary opening/scheduling helpers');
// The old date-specific trigger must not bypass the waiver at its opening time.
const schedule={Date:class extends Date{static now(){return Date.parse('2026-10-16T08:30:00Z');}},loadLinks_:()=>({'CML3111|6':{formId:'preserved-form',waived:true}}),FormApp:{openById(){throw Error('Waived form must not be opened');}}};
vm.createContext(schedule);vm.runInContext(fs.readFileSync('scripts/operations/oct16_friday_quizzes_waiver_guard.gs','utf8'),schedule);schedule.openFridayQuiz3111();
console.log('PASS: date-specific Friday opener respects CML3111 waiver');
