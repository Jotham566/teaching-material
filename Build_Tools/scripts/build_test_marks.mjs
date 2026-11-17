/** Private lecturer workbook, built from the trusted batch ledger. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const runtime=path.join(process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook,SpreadsheetFile}=createRequire(path.join(runtime,'package.json'))('@oai/artifact-tool');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: build_test_marks.mjs workbook_data.json output.xlsx');
const data=JSON.parse(await fs.readFile(input,'utf8'));
const wb=Workbook.create();
const headers=['Full name','Student Registration Number','Google email','Programme','Test','Variant','Status','Mark /100','Maximum','Semester points','Submitted (Kampala)','Response ID'];
const safe=x=>typeof x==='string'&&/^[=+@-]/.test(x)?"'"+x:x;
const vals=r=>[r.full_name,r.student_registration_number,r.email,r.cohort,r.assessment,r.variant,r.status,r.score??null,r.maximum??100,null,new Date(new Date(r.submitted_at).getTime()+3*3600000),r.response_id].map(safe);
for(const [name,rows] of [['Current marks',data.current],['All attempts',data.attempts]]){
 const s=wb.worksheets.add(name);s.showGridLines=false;
 s.getRange('A2').values=[[name==='Current marks'?'IUEA test marks':'Submission audit']];
 s.getRange('A3').values=[['Test 1: 15 semester points. Test 2: 20. Blank marks are pending, not zero.']];
 s.getRange('A4').values=[['Attendees come from submissions. Absence cannot be established without an enrolled roster.']];
 s.getRange('A6:L6').values=[headers];
 const end=Math.max(7,6+rows.length);
 s.getRange('A2:L'+end).format.font={name:'Arial',size:11,color:'#1C3144'};
 s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#1C3144'};
 if(rows.length)s.getRange('A7:L'+end).values=rows.map(vals);
 for(let i=0;i<rows.length;i++){const r=i+7;s.getRange('J'+r).formulas=[[`=IF(AND(G${r}="GRADED",ISNUMBER(H${r})),H${r}/I${r}*IF(E${r}="TEST1",15,20),"")`]];}
 s.getRange('A6:L6').format={fill:'#1C3144',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:36,horizontalAlignment:'center',verticalAlignment:'center'};
 s.getRange('A7:L'+end).format.rowHeight=26;
 s.getRange('A6:L'+end).format.columnWidth=18;
 s.getRange('A6:C'+end).format.columnWidth=30;
 s.getRange('G6:G'+end).format.columnWidth=26;
 s.getRange('K6:K'+end).format.columnWidth=24;
 s.getRange('L6:L'+end).format.columnWidth=28;
 s.getRange('H7:J'+end).setNumberFormat('0.00');
 s.getRange('K7:K'+end).setNumberFormat('dd mmm yyyy hh:mm:ss');
 s.getRange('G7:G'+end).conditionalFormats.add('containsText',{text:'CONFLICT',format:{fill:'#FCE4D6',font:{bold:true,color:'#9C0006'}}});
 s.tables.add('A6:L'+end,true,name==='Current marks'?'CurrentMarks':'AllAttempts');
 s.freezePanes.freezeRows(6);s.freezePanes.freezeColumns(2);
}
const issues=wb.worksheets.add('Collection issues');issues.showGridLines=false;
issues.getRange('A2').values=[['Submission collection issues']];
issues.getRange('A4').values=[['Resolve these before releasing marks. They have no final score.']];
issues.getRange('A6:F6').values=[['Programme','Test','Full name','Registration Number','Status','Reason']];
const problemRows=data.collection_issues||[];
if(problemRows.length)issues.getRange('A7:F'+(6+problemRows.length)).values=problemRows.map(r=>[r[1],r[2],r[4],r[6],r[10],r[14]].map(safe));
else issues.getRange('A7').values=[['No collection issues in this batch.']];
issues.getRange('A2:F'+Math.max(7,6+problemRows.length)).format.font={name:'Arial',size:11};
issues.getRange('A2').format.font={name:'Arial',size:16,bold:true};
issues.getRange('A6:F6').format={fill:'#1C3144',font:{name:'Arial',size:11,color:'#FFFFFF',bold:true},rowHeight:30};
issues.getRange('A6:E'+Math.max(7,6+problemRows.length)).format.columnWidth=26;
issues.getRange('F6:F'+Math.max(7,6+problemRows.length)).format.columnWidth=90;
wb.recalculate();
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20}});
await fs.mkdir(path.dirname(output),{recursive:true});
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
if(process.env.IUEA_WORKBOOK_QA==='1'){
 for(const name of ['Current marks','All attempts','Collection issues']){
  const blob=await wb.render({sheetName:name,range:name==='Collection issues'?'A1:F10':'A1:K12',scale:1});
  await fs.writeFile(path.join(path.dirname(output),name.replaceAll(' ','_')+'.png'),new Uint8Array(await blob.arrayBuffer()));
 }
 console.log(scan.ndjson);
 console.log((await wb.inspect({kind:'table',range:'Current marks!G6:K12',include:'values,formulas',tableMaxRows:7,tableMaxCols:5})).ndjson);
}
console.log('Saved marks workbook.');
