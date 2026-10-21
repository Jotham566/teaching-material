/** Private cumulative workbook. Run after rebuilding the trusted CA ledger. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {isWaived} from './ca_assessment_policy.mjs';
import {reviewDetails} from './ca_review_details.mjs';
const runtime=process.env.IUEA_ARTIFACT_NODE_MODULES||path.join(process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook,SpreadsheetFile}=createRequire(path.join(runtime,'package.json'))('@oai/artifact-tool');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: build_continuous_assessment.mjs ledger.json marks.xlsx');
const data=JSON.parse(await fs.readFile(input,'utf8')),wb=Workbook.create();
const cohorts=['CML3111','CML3112','CML3113'];
const quiz=[1,2,3,4,5,6,8,9,10,11,12,13].map(w=>'Q'+w);
const assignments=[1,2,3,4,5,6,8,9,10,11,12].map(w=>'W'+String(w).padStart(2,'0'));
const projects=['DA_PROJECT','TEST1','TEST2','ML_PROJECT','DEMO'];
const safe=v=>typeof v==='string'&&/^[=+@-]/.test(v)?"'"+v:v;
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
for(const name of [...cohorts,'Review needed','Written rubrics','Current marks','All attempts','Rules'])wb.worksheets.add(name);
function table(sheet,headers,rows){const end=Math.max(7,6+rows.length),last=col(headers.length-1);sheet.showGridLines=false;sheet.getRange(`A6:${last}6`).values=[headers];if(rows.length)sheet.getRange(`A7:${last}${end}`).values=rows.map(r=>r.map(safe));sheet.getRange(`A2:${last}${end}`).format.font={name:'Arial',size:11};sheet.getRange(`A2`).format.font={name:'Arial',size:16,bold:true};sheet.getRange(`A6:${last}6`).format={fill:'#17365D',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:44,verticalAlignment:'center',horizontalAlignment:'center'};sheet.getRange(`A7:${last}${end}`).format.rowHeight=23;sheet.getRange(`A6:${last}${end}`).format.columnWidth=16;sheet.freezePanes.freezeRows(6);sheet.freezePanes.freezeColumns(2);if(rows.length)sheet.tables.add(`A6:${last}${end}`,true,sheet.name.replaceAll(' ','')+'Table');return end;}
const recordHeaders=['Programme','Registration Number','Email','Name','Assessment','Submitted (Kampala)','Status','Mark','Maximum','Timing','Response ID','Source mark','Source status','Registration as entered','Code component','Code maximum','Identity evidence'];
for(const [name,records] of [['Current marks',data.current],['All attempts',data.attempts]]){
 const s=wb.worksheets.getItem(name);s.getRange('A2').values=[[name]];s.getRange('A4').values=[['Source receipts are retained. Pending marks are blank, never zero.']];
 const rows=records.map(r=>[r.cohort,r.student_id,r.email,r.full_name,r.assessment,new Date(stamp(r.submitted_at)+10800000),r.status,r.status==='GRADED'?r.score:null,r.maximum,r.timing_status,r.response_id,r.source_score??null,r.source_status??r.status,r.submitted_student_id??r.student_id,r.code_score??null,r.code_maximum??null,r.identity_evidence??'As submitted; formatting normalized']);
 const end=table(s,recordHeaders,rows);s.getRange(`B6:D${end}`).format.columnWidth=28;s.getRange(`F6:G${end}`).format.columnWidth=25;s.getRange(`K6:K${end}`).format.columnWidth=30;s.getRange(`F7:F${end}`).setNumberFormat('dd mmm yyyy hh:mm');s.getRange(`H7:I${end}`).setNumberFormat('0.00');s.getRange(`G7:G${end}`).conditionalFormats.add('notContainsText',{text:'GRADED',format:{fill:'#FFF2CC'}});
}
function stamp(s){return new Date(s).getTime();}
const review=await reviewDetails(data,path.dirname(input));
const rs=wb.worksheets.getItem('Review needed');
rs.getRange('A2').values=[['Submitted work requiring review']];
rs.getRange('A4').values=[['Filter by issue or programme. File links use your existing Google access. Held marks are not yet allocated to totals.']];
rs.getRange('A5').values=[['This list refreshes with grading. Keep decisions against the Response ID separately; do not overwrite calculated marks.']];
const fileCount=Math.max(1,...review.map(x=>x.files.length));
const rh=['Programme','Registration Number','Name','Email','Assessment','Issue','What needs attention','Held source mark','Code component','Two grading passes','Processing detail','Other registrations on account','Other accounts on registration','Notebook registration','Response form','Response ID',...Array.from({length:fileCount},(_,i)=>`Uploaded file ${i+1}`)];
const rend=table(rs,rh,review.map(x=>[x.r.cohort,x.r.student_id,x.r.full_name||'Not collected',x.r.email,x.r.assessment,x.r.status,x.reason,x.r.source_score??null,x.r.code_score??null,x.scores,x.detail,x.relatedIds,x.relatedEmails,x.declared,'',x.r.response_id,...Array(fileCount).fill('')]));
rs.getRange(`B6:D${rend}`).format.columnWidth=28;rs.getRange(`F6:G${rend}`).format.columnWidth=44;rs.getRange(`J6:N${rend}`).format.columnWidth=38;rs.getRange(`P6:${col(rh.length-1)}${rend}`).format.columnWidth=35;rs.getRange(`A7:${col(rh.length-1)}${rend}`).format.wrapText=true;rs.getRange(`A7:${col(rh.length-1)}${rend}`).format.rowHeight=100;rs.getRange(`A7:${col(rh.length-1)}${rend}`).format.verticalAlignment='center';
const reviewLinks=[];
const link=(cell,url,label)=>{rs.getRange(cell).values=[[safe(label)]];rs.getRange(cell).format.font={name:'Arial',size:11,color:'#0563C1'};reviewLinks.push([cell,url]);};
review.forEach((x,i)=>{const row=i+7;if(x.formUrl)link(`O${row}`,x.formUrl,'Open response form');x.files.forEach((f,j)=>link(`${col(16+j)}${row}`,f.url,f.name));});
const rubricSheet=wb.worksheets.getItem('Written rubrics'),rubricRows=[];
for(const assessment of ['W01','W02']){const rubric=JSON.parse(await fs.readFile(new URL(`../IUEA_Teaching_Plan/grader/rubrics/${assessment}.json`,import.meta.url),'utf8'));for(const c of rubric.criteria)rubricRows.push([assessment,c.id,c.title,c.maximum,c.description]);}
rubricSheet.getRange('A2').values=[['Written assessment marking criteria']];rubricSheet.getRange('A4').values=[['A1: written total /20. A2: written total /6 plus coding component /14. Grader-pass scores are not approved marks.']];
const rubricEnd=table(rubricSheet,['Assessment','Criterion ID','Criterion','Maximum','Awarding guidance'],rubricRows);rubricSheet.getRange(`C6:C${rubricEnd}`).format.columnWidth=32;rubricSheet.getRange(`E6:E${rubricEnd}`).format.columnWidth=100;rubricSheet.getRange(`A7:E${rubricEnd}`).format.wrapText=true;rubricSheet.getRange(`A7:E${rubricEnd}`).format.rowHeight=68;rubricSheet.getRange(`A7:E${rubricEnd}`).format.verticalAlignment='center';
const index=new Map(data.current.map((r,i)=>[[r.cohort,r.student_id,r.assessment].join('|'),i+7]));
function best(range,n){return `IF(COUNT(${range})=0,"",(${Array.from({length:n},(_,i)=>`IF(COUNT(${range})>=${i+1},LARGE(${range},${i+1}),0)`).join('+')})` ;}
for(const cohort of cohorts){
 const s=wb.worksheets.getItem(cohort),students=data.students.filter(r=>r.cohort===cohort),waived=true;
 const headers=['Name','Registration Number','Email','Record status','Earned points /100','Quizzes /10','Assignments /10','Data project /10','Test 1 /15','Test 2 /20','ML project /25','Demo /10','Graded items','Submitted work pending',...quiz.map(q=>q+' /5'),...assignments.map(q=>'A'+Number(q.slice(1))+' /20'),...projects.map(p=>p+' /100')];
 const end=table(s,headers,students.map(r=>[r.full_name||'Name not collected',r.student_id,r.email,...Array(headers.length-3).fill(null)]));
 s.tabColor='#17365D';s.getRange('A2').values=[[cohort+' continuous assessment']];s.getRange('A3').values=[['Updated '+new Date(data.updated_at).toISOString().slice(0,16).replace('T',' ')+' UTC. Earned points are provisional, not a final semester grade.']];s.getRange('A4').values=[['Blank = not graded or not submitted. WAIVED = excluded. Raw quiz and assignment marks are to the right.']];s.getRange(`A6:C${end}`).format.columnWidth=29;s.getRange(`D6:D${end}`).format.columnWidth=26;s.getRange(`E7:AP${end}`).setNumberFormat('0.00');s.getRange(`M7:N${end}`).setNumberFormat('0');
 const matrices=[];
 for(let i=0;i<students.length;i++){
  const student=students[i],row=i+7,records=data.current.filter(r=>r.cohort===cohort&&r.student_id===student.student_id&&!isWaived(r.assessment)),pending=records.filter(r=>r.status!=='GRADED').length;
  const f=Array(headers.length).fill(null);f[3]=records.some(r=>r.status.startsWith('IDENTITY_'))?'="Verify identity"':`=IF(N${row}>0,"Submitted work pending","Current marks recorded")`;f[4]=`=IF(COUNT(F${row}:L${row})=0,"",SUM(F${row}:L${row}))`;
  f[5]=best(`O${row}:Z${row}`,waived?9:10)+`/(${waived?9:10}*5)*10)`;
  f[6]=best(`AA${row}:AK${row}`,waived?7:8)+`/(${waived?7:8}*20)*10)`;
  for(let j=0;j<5;j++)f[7+j]=`=IF(ISNUMBER(${col(37+j)}${row}),${col(37+j)}${row}/100*${[10,15,20,25,10][j]},"")`;
  f[12]=`=COUNT(O${row}:AP${row})`;s.getRange(`N${row}`).values=[[pending]];
  [...quiz,...assignments,...projects].forEach((a,j)=>{const c=14+j;if(waived&&(a==='Q6'||a==='W06')){s.getRange(`${col(c)}${row}`).values=[['WAIVED']];return;}const sourceRow=index.get([cohort,student.student_id,a].join('|'));if(sourceRow)f[c]=`=IF('Current marks'!G${sourceRow}="GRADED",'Current marks'!H${sourceRow},"")`;});
  // Write only calculated blocks so identity values and waived labels survive.
  s.getRange(`D${row}:M${row}`).formulas=[f.slice(3,13).map(x=>x&&x.startsWith('=')?x:x?'='+x:null)];
  for(let j=14;j<f.length;j++)if(f[j])s.getRange(`${col(j)}${row}`).formulas=[[f[j]]];
 }
 s.getRange(`D7:D${end}`).conditionalFormats.add('containsText',{text:'Pending',format:{fill:'#FFF2CC'}});
 s.getRange(`D7:D${end}`).conditionalFormats.add('containsText',{text:'Verify',format:{fill:'#FFF2CC'}});
}
const rules=wb.worksheets.getItem('Rules');rules.getRange('A2').values=[['Marking rules and source coverage']];
const ruleRows=[['Quizzes',10,'All programmes: best 9 of 11; exclude Q6. Each /5.'],['Assignments',10,'All programmes: best 7 of 10; exclude A6. Each /20.'],['Data analysis project',10,'Out of 100'],['Practical Test 1',15,'Out of 100'],['Practical Test 2',20,'Out of 100'],['ML project',25,'Out of 100'],['Demo / reflection',10,'Out of 100'],['Waivers',null,'A6 and Quiz 6 waived for all three programmes. No weekly quiz/assignment in test weeks 7/14 or final-project week 15; major assessments retain their weights.'],['Current selection',null,'Latest eligible receipt per programme, registration number and assessment.'],['Identity',null,'Same-account punctuation variants and strongly supported early digit typos are reconciled; unresolved conflicts remain held.'],['Names',null,'Blank names are filled from a later verified source, never guessed from email.'],['Totals',null,'Earned semester points so far. Missing and future assessments are not final zeros.'],['Grade bands',null,'No letter grades: Faculty grade bands have not been verified.'],['Source coverage',null,data.sources.length+' source files. See the local source manifest for receipt hashes.']];
const re=table(rules,['Component','Weight /100','Rule'],ruleRows);rules.getRange(`A6:A${re}`).format.columnWidth=28;rules.getRange(`C6:C${re}`).format.columnWidth=95;rules.getRange(`C7:C${re}`).format.wrapText=true;rules.getRange(`A7:C${re}`).format.rowHeight=36;
rules.getRange('A14:C14').format.rowHeight=66;
wb.recalculate();
const check=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:30}});
await fs.mkdir(path.dirname(output),{recursive:true});await fs.writeFile(path.join(path.dirname(output),'workbook_check.ndjson'),check.ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
// Preserve native clickable links without unsupported formula-cache errors.
execFileSync(process.env.IUEA_PYTHON||'python3',[fileURLToPath(new URL('./attach_xlsx_hyperlinks.py',import.meta.url)),output,'xl/worksheets/sheet4.xml'],{input:JSON.stringify(reviewLinks)});
if(process.env.IUEA_WORKBOOK_QA==='1')for(const name of [...cohorts,'Review needed','Written rubrics','Current marks','All attempts','Rules']){const b=await wb.render({sheetName:name,range:name==='Written rubrics'?'A6:E15':name==='Review needed'?'E10:K14':name==='Rules'?'A1:C15':cohorts.includes(name)?'D1:N12':'E1:J12',scale:1});await fs.writeFile(path.join(path.dirname(output),name.replaceAll(' ','_')+'_preview.png'),new Uint8Array(await b.arrayBuffer()));}
console.log('Saved private cumulative workbook.');
