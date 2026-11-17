import assert from 'node:assert/strict';
import {isWaived} from '../scripts/ca_assessment_policy.mjs';
for(const week of [6,7,14,15]){
 assert.equal(isWaived(`Q${week}`),true);
 assert.equal(isWaived(`W${String(week).padStart(2,'0')}`),true);
}
for(const id of ['Q1','W01','Q8','W08','Q13','TEST1','TEST2','DA_PROJECT','ML_PROJECT','DEMO'])
 assert.equal(isWaived(id),false);
console.log('PASS: weekly waivers preserve major assessment and other-week eligibility');
