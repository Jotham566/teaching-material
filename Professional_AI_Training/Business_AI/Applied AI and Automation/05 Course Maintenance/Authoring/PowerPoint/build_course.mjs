import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
const HERE=path.dirname(fileURLToPath(import.meta.url));
const AUTHOR=path.resolve(HERE,'..'),COURSE=path.resolve(HERE,'../../..');
const BUILD=path.join(AUTHOR,'.build/legal_tax_rebuild');
const SKILL='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11618/skills/presentations';
const MOD='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const PY='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
process.env.RUNTIME_NODE_MODULES=MOD;
const {Presentation,PresentationFile}=createRequire(path.join(MOD,'package.json'))('@oai/artifact-tool');
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')));
const DATA=JSON.parse(await fs.readFile(path.join(AUTHOR,'Documents/course.json'),'utf8'));
const C={ink:'#1C3144',teal:'#246E63',orange:'#C94E29',paper:'#F1F5F6',pale:'#E9F3F0',line:'#C9D5DA',muted:'#536474',white:'#FFFFFF'};
const FONT='Calibri';let serial=0;
const reveal=(n,name)=>`reveal-${String(n).padStart(2,'0')}-${name}`;
function text(s,t,x,y,w,h,size=30,bold=false,color=C.ink,name=''){
 let o=s.shapes.add({geometry:'textbox',name:name||`text-${++serial}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});o.text=t;o.text.style={typeface:FONT,fontSize:size,bold,color,autoFit:'none'};return o;
}
function shape(s,x,y,w,h,fill=C.paper,name='',geometry='rect',stroke=C.line){return s.shapes.add({geometry,name:name||`shape-${++serial}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:1.2}});}
function link(s,a,b,stage=0,fromSide='right',toSide='left',width=2.5){
 return s.shapes.connect(a,b,{kind:'straight',fromSide,toSide,name:stage?reveal(stage,'connection'):`link-${++serial}`,line:{fill:C.teal,width},tail:{type:'arrow',width:'med',length:'med'}});
}
function footer(s,d,n){text(s,`KLAi   Session ${String(d.session).padStart(2,'0')}   ${n}${d.slides[n-1].optional?'   OPTIONAL EXPLORATION':''}`,62,686,1120,22,16,false,C.muted);}
function header(s,x,d,n){text(s,`APPLIED AI AND AUTOMATION   ${String(d.session).padStart(2,'0')}`,62,26,1156,26,18,true,C.teal);text(s,x.title,62,69,1156,104,x.title.length>58?40:44,true);footer(s,d,n);}
function caption(s,t){text(s,t,65,614,1150,62,23,false,C.muted);}
function paragraphs(s,arr,{y=204,size=32,height=390}={}){
 const step=height/arr.length;
 arr.forEach((t,i)=>{text(s,String(i+1).padStart(2,'0'),65,y+i*step,50,45,26,true,C.orange);text(s,t,135,y+i*step,1070,step-12,size,false);});
}
function compare(s,a,b){
 [a,b].forEach(([label,body],i)=>{let x=65+i*595;text(s,label,x,210,550,70,28,true,i?C.teal:C.orange);text(s,body,x,302,550,288,33);});
}
function nativeTable(s,headers,rows,{x=65,y=203,w=1150,h=393,size=25,widths}={}){
 const t=s.tables.add({rows:rows.length+1,columns:headers.length,left:x,top:y,width:w,height:h,values:[headers,...rows],...(widths?{columnWidths:widths}:{})});t.borders.assign({style:'solid',fill:C.line,width:1});
 for(let i=0;i<rows.length+1;i++)for(let j=0;j<headers.length;j++){let c=t.getCell(i,j);c.fill=i===0?C.teal:(i%2?C.paper:C.white);c.text.style={typeface:FONT,fontSize:size,bold:i===0,color:i===0?C.white:C.ink};}return t;
}
function flow(s,steps,{y=290}={}){
 const gap=35,w=(1150-(steps.length-1)*gap)/steps.length,nodes=[];
 steps.forEach(([a,b],i)=>{let x=65+i*(w+gap);let o=shape(s,x,y,w,212,i===steps.length-1?C.pale:C.paper,reveal(i+1,'stage'));text(s,String(i+1).padStart(2,'0'),x,y-46,w,35,27,true,C.orange,reveal(i+1,'number'));text(s,a,x+16,y+16,w-32,76,steps.length>3?29:32,true,C.teal,reveal(i+1,'label'));text(s,b,x+16,y+111,w-32,85,26,false,C.ink,reveal(i+1,'detail'));nodes.push(o);});
 for(let i=0;i<nodes.length-1;i++){let c=link(s,nodes[i],nodes[i+1]);c.name=reveal(i+2,'arrow');}
}
const clause='The customer must give prior written consent to a change of control of the provider. Consent is not required for a reorganisation within a wholly owned group if the provider remains responsible for its obligations.';
const assets={};for(const k of ['document_layout','copilot_activity','contract_page','contract_scan']){const b=await fs.readFile(path.join(AUTHOR,'Reference Assets',k+'.png'));assets[k]=b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength);}
function image(s,key,alt,x=65,y=201,w=1150,h=394,crop){return s.images.add({blob:assets[key],contentType:'image/png',alt,fit:'contain',...(crop?{crop}:{}),position:{left:x,top:y,width:w,height:h}});}
function diagram(s,x,d){
 switch(x.kind){
 case 'matter':
  text(s,'Kampala Legal and Tax acts for the customer.',65,210,1140,70,35,true,C.ink);
  shape(s,65,335,510,185,C.pale);text(s,'Victoria Services Ltd',85,353,470,65,32,true,C.teal);text(s,'Customer and client',85,437,470,60,30);
  shape(s,705,335,510,185,C.paper);text(s,'Equator Systems Ltd',725,353,470,65,32,true,C.teal);text(s,'Service provider',725,437,470,60,30);
  text(s,'Contract',585,392,120,50,20,true,C.orange);caption(s,'Equator proposes a reorganisation. Ownership and continued responsibility are unconfirmed.');break;
 case 'definition':
  text(s,x.body[0],65,203,1150,237,36,true);text(s,x.title==='AI systems'?'THE FIELD':'IN OUR MATTER',65,470,1150,32,22,true,C.teal);text(s,x.body[1],65,521,1150,88,30);break;
 case 'fieldmap':{
  let a=shape(s,65,210,670,372,C.paper,reveal(1,'AI'));text(s,'Artificial intelligence',88,230,620,46,32,true,C.ink,reveal(1,'AI-label'));
  shape(s,109,294,585,256,C.pale,reveal(2,'ML'));text(s,'Machine learning',133,311,535,44,31,true,C.teal,reveal(2,'ML-label'));
  shape(s,162,391,475,127,C.white,reveal(3,'DL'));text(s,'Deep learning',184,414,430,80,30,true,C.teal,reveal(3,'DL-label'));
  text(s,'Generative AI',790,213,420,52,32,true,C.orange,reveal(4,'gen'));text(s,'A content-generation capability, often using deep learning.',790,289,420,135,29,false,C.ink,reveal(4,'gen-detail'));
  text(s,'Data science overlaps these fields and includes work without ML.',790,462,420,138,28,false,C.ink,reveal(5,'DS'));caption(s,'Natural language processing (NLP) studies computational processing of human language.');break;}
 case 'bridge':
  text(s,d.session===1?'YOUR CURRENT WORK':`RECALL SESSION ${d.session-1}`,65,210,1140,36,24,true,C.orange);
  text(s,x.body[0],65,262,1140,104,33,true,C.ink);
  text(s,'TODAY’S QUESTION',65,405,1140,36,24,true,C.teal);
  text(s,x.body[1],65,458,1140,121,34,true,C.ink);
  caption(s,'Result: '+d.result);break;
 case 'modelstages':
  text(s,'TRAINING: PARAMETERS CAN CHANGE',65,195,845,38,24,true,C.teal);
  text(s,'USE',953,195,260,38,24,true,C.orange);
  flow(s,x.steps);caption(s,'One common route. Providers vary. Inference does not itself run a training update.');break;
 case 'promptloop':
  flow(s,x.steps);caption(s,'Variant A: an unrelated buyer acquires control through a share sale. Apply the current clause.');break;
 case 'approvalgate':{
  let a=shape(s,65,257,265,158,C.paper,reveal(1,'draft'));text(s,'Draft and evidence',82,273,231,73,29,true,C.teal,reveal(1,'draft-label'));text(s,'Exact version',82,361,231,43,27,false,C.ink,reveal(1,'draft-detail'));
  let b=shape(s,430,257,320,158,C.pale,reveal(2,'review'));text(s,'Reviewer decision',448,273,284,73,29,true,C.teal,reveal(2,'review-label'));text(s,'Check and decide',448,361,284,43,27,false,C.ink,reveal(2,'review-detail'));
  let c=shape(s,850,257,365,158,C.paper,reveal(3,'continue'));text(s,'Continue',868,273,329,65,30,true,C.teal,reveal(3,'continue-label'));text(s,x.action_label,868,348,329,63,27,false,C.ink,reveal(3,'continue-detail'));
  let e=shape(s,430,491,320,100,C.paper,reveal(4,'hold'));text(s,'Hold or revise',448,510,284,61,30,true,C.orange,reveal(4,'hold-label'));
  for(const [from,to,st,side1,side2] of [[a,b,2,'right','left'],[b,c,3,'right','left'],[b,e,4,'bottom','top']]){let l=link(s,from,to,0,side1,side2);l.name=reveal(st,'decision-route');}
  text(s,'Approve',758,215,150,40,23,true,C.teal,reveal(3,'approve'));text(s,'Decline / evidence missing',768,478,440,66,25,true,C.orange,reveal(4,'decline'));caption(s,'Approval applies to the reviewed version. A changed field requires a new decision.');break;}
 case 'learningloop':
  flow(s,x.steps);caption(s,'Repeat with examples. Evaluate on relevant unseen data rather than training fit alone.');break;
 case 'labelled':
  nativeTable(s,['Input document','Target label'],[['Service terms and signature','Service agreement'],['Employment terms','Employment agreement'],['Invoice number and amount','Invoice']],{h:300});text(s,'These illustrative rows do not train or validate a classifier.',65,548,1150,66,29,true,C.orange);break;
 case 'network':{
  const cols=[125,445,765,1110],ys=[[310,430],[270,370,470],[270,370,470],[365]],nodes=[];
  cols.forEach((v,i)=>{nodes[i]=ys[i].map((yy,j)=>shape(s,v,yy,40,40,i===3?C.orange:C.pale,reveal(i+1,'unit-'+j),'ellipse',C.teal));text(s,['Inputs','Layer 1','Layer 2','Output'][i],i===0?65:i===1?375:i===2?695:1025,184,220,65,29,true,C.teal,reveal(i+1,'label'));});
  for(let i=0;i<3;i++)for(let a of nodes[i])for(let b of nodes[i+1]){let l=link(s,a,b);l.line={fill:'#7FA69F',width:1.8};l.name=reveal(i+2,'weight');}
  text(s,'Document features',65,540,280,50,25,true,C.ink,reveal(1,'input-example'));text(s,'Learned combinations',420,540,540,50,25,true,C.teal,reveal(3,'representation-example'));text(s,'Type score',1010,540,205,50,25,true,C.ink,reveal(4,'output-example'));
  caption(s,'Illustrative classifier: document features → learned layers → a category score. Not a biological brain.');break;}
 case 'tokens':
  nativeTable(s,['Schematic token','Illustrative ID','Representation'],[['The','103','A learned numerical vector'],['provider','285','A learned numerical vector'],['remains','914','A learned numerical vector'],['responsible','602','A learned numerical vector']],{h:350});caption(s,'Token boundaries and identifiers are illustrative. Numeric ID proximity does not measure meaning.');break;
 case 'embeddingmap':{
  const pts=[['Query: restructuring consent',220,300,1],['Clause 3: group exception',310,385,2],['Support access clause',430,475,2],['Invoice payment term',835,310,3],['Photograph consent',795,495,3]];
  const axisH=shape(s,110,571,1020,2,C.line,'axis-h','rect','none');shape(s,110,217,2,355,C.line,'axis-v','rect','none');
  pts.forEach(([label,px,py,g])=>{shape(s,px,py,18,18,g===1?C.orange:C.teal,reveal(g,label),'ellipse','none');text(s,label,px+26,py-13,365,76,25,true,g===1?C.orange:C.teal,reveal(g,label+'-text'));});
  caption(s,'Invented 2D projection of many-dimensional representations. Inspect candidates; distance is not legal meaning.');break;}
 case 'context':compare(s,x.left,x.right);caption(s,'Contextual representations depend on surrounding language.');break;
 case 'attention':{
  text(s,'The provider remains responsible for its obligations.',65,194,1140,58,34,true);
  const targets=[['provider',90,270,4],['responsible',470,270,2.5],['other context',850,270,1.2]],nodes=[];
  targets.forEach(([label,px,py,width],i)=>{nodes[i]=shape(s,px,py,300,85,C.paper,reveal(1,'context-'+i));text(s,label,px+15,py+20,270,50,30,true,C.teal,reveal(1,'context-label-'+i));});
  let query=shape(s,475,491,300,85,C.pale,reveal(2,'current-word'));text(s,'its',490,510,270,50,32,true,C.orange,reveal(2,'current-label'));
  targets.forEach((v,i)=>{let l=link(s,nodes[i],query,0,'bottom','top',v[3]);l.name=reveal(3,'weight-'+i);});
  text(s,'Input-dependent weighting combines these representations.',65,579,1140,34,25,true,C.ink,reveal(3,'operation'));
  caption(s,'Invented links for teaching. Actual attention depends on the input, layer and head; this is not a reasoning trace.');break;}
 case 'nexttoken':{
  text(s,'Prefix: “The provider remains …”',65,200,1140,60,36,true);
  [['responsible',.70],['liable',.20],['available',.10]].forEach(([word,v],i)=>{let yy=305+i*95;text(s,word,65,yy,300,60,31,true,C.teal,reveal(i+1,'candidate'));shape(s,390,yy,Math.round(v*850),48,i===0?C.teal:C.orange,reveal(i+1,'probability'));text(s,`${Math.round(v*100)}%`,1030,yy,180,55,31,true,C.ink,reveal(i+1,'score'));});
  caption(s,'Invented next-token probabilities sum to 100%. They are not probabilities that a legal claim is true.');break;}
 case 'generationloop':{
  const stages=[['Current prefix','The provider remains'],['Next-token scores','Choose “responsible”'],['New prefix','The provider remains responsible']];flow(s,stages,{y:270});
  text(s,'Repeat using the updated prefix → next token → updated prefix',65,537,1140,65,30,true,C.teal,reveal(4,'repeat'));caption(s,'Autoregressive generation builds a sequence. Evidence must still be supplied and checked.');break;}
 case 'contextwindow':{
  shape(s,65,244,1150,170,C.paper,reveal(1,'window'));text(s,'ACTIVE CONTEXT FOR THIS REQUEST',85,260,1100,45,25,true,C.teal,reveal(1,'window-label'));
  [['Instructions',85,190],['Evidence',295,350],['Conversation',665,300],['Output',985,210]].forEach(([t,px,w],i)=>{shape(s,px,329,w,60,i===1?C.pale:C.white,reveal(2,'segment'));text(s,t,px+8,340,w-16,45,23,true,C.ink,reveal(2,'segment-label'));});
  text(s,'Application files and earlier material can sit outside this window.',65,478,1140,85,33,true,C.orange,reveal(3,'outside'));caption(s,'Conceptual allocation, not measured token sizes. Product rules determine selection, summarisation and limits.');break;}
 case 'scancompare':
  image(s,'contract_scan','Synthetic degraded page made from the fictional clause',65,225,530,350);
  text(s,'EXTRACT AND VERIFY',680,210,530,45,25,true,C.teal);text(s,'Searchable text is useful only if the rule, negation, exception and condition survive.',680,283,530,170,33);
  text(s,'Compare the observed OCR with the original page.',680,495,530,85,30,true,C.orange);caption(s,'Synthetic scan of an authored source. A saved OCR run is separate from the deliberately damaged extract.');break;
 case 'ragarchitecture':{
  text(s,'PREPARE THE COLLECTION',65,193,1140,40,25,true,C.teal);
  const row1=[['Documents','Current and permitted'],['Chunks','Text + provenance'],['Embedding model','Numerical vectors'],['Index','Vectors + metadata']],n1=[];
  row1.forEach(([a,b],i)=>{let px=65+i*296;n1[i]=shape(s,px,247,260,140,C.paper,reveal(i+1,'prepare'));text(s,a,px+12,258,236,62,25,true,C.teal,reveal(i+1,'prepare-label'));text(s,b,px+12,326,236,55,22,false,C.ink,reveal(i+1,'prepare-detail'));if(i){let l=link(s,n1[i-1],n1[i]);l.name=reveal(i+1,'prepare-arrow');}});
  text(s,'ANSWER A QUESTION',65,407,1140,40,25,true,C.orange,reveal(5,'query-heading'));
  const row2=[['Query embedding','Represent the question'],['Retrieve + filter','Current allowed passages'],['Language model','Question + evidence'],['Answer + sources','Review against original']],n2=[];
  row2.forEach(([a,b],i)=>{let px=65+i*296;n2[i]=shape(s,px,464,260,140,C.pale,reveal(5+i,'answer'));text(s,a,px+12,476,236,62,25,true,C.teal,reveal(5+i,'answer-label'));text(s,b,px+12,544,236,55,22,false,C.ink,reveal(5+i,'answer-detail'));if(i){let l=link(s,n2[i-1],n2[i]);l.name=reveal(5+i,'answer-arrow');}});
  caption(s,'Embedding and answer generation have different roles. Retrieval can also use keywords or a hybrid method.');break;}
 case 'inventory':
  [['Paper','Files and scans'],['Digital files','Agreements and email'],['Systems','DMS and accounting']].forEach(([a,b],i)=>{let px=65+i*400;shape(s,px,300,350,220,C.paper);text(s,a,px+18,320,314,66,34,true,C.teal);text(s,b,px+18,419,314,85,30);});caption(s,'These are source categories, not sequential stages. Inventory each source before choosing a preparation route.');break;
 case 'retrievalphases':
  text(s,'SOURCE PREPARATION',65,200,550,44,25,true,C.teal);text(s,'QUESTION-TIME USE',660,200,550,44,25,true,C.orange);flow(s,x.steps);caption(s,'Prepare and index sources first. Each question retrieves evidence and generates a checked answer.');break;
 case 'jsonclause':
  text(s,'SOURCE',65,205,480,35,23,true,C.teal);text(s,'CONTRACT-01 v2\nClause 3\n'+clause,65,263,500,320,29);
  text(s,'STRUCTURED RECORD',665,205,540,35,23,true,C.teal);text(s,'{\n  "document_id": "CONTRACT-01",\n  "version": "v2",\n  "clause": "3",\n  "text": "Exact source passage",\n  "source_location": "clause 3"\n}',665,263,545,300,27);caption(s,'JSON stores named fields: document_id is a key; CONTRACT-01 is its value. Text is abbreviated here.');break;
 case 'akn':
  text(s,'<section eId="sec_3">\n  <heading>Change of control</heading>\n  <content>\n    <p>Clause text with its qualification</p>\n  </content>\n</section>',65,235,1150,275,32);caption(s,'Illustrative structural fragment. It is not a complete, schema-validated Akoma Ntoso document.');break;
 case 'chunks':
  text(s,'BAD SPLIT',65,207,1120,32,23,true,C.orange,reveal(1,'bad-label'));text(s,'Chunk A: Prior consent is required.\nChunk B: The group-reorganisation exception appears alone.',65,255,1120,145,33,false,C.ink,reveal(1,'bad'));
  text(s,'CONTEXT PRESERVED',65,430,1120,33,23,true,C.teal,reveal(2,'good-label'));text(s,'Keep the rule, exception and responsibility condition together, with source identity and location.',65,480,1120,111,33,true,C.teal,reveal(2,'good'));caption(s,'A chunking strategy needs tests based on the questions and relationships it must preserve.');break;
 case 'retrievaltrace':
  nativeTable(s,['Candidate','Status','Use'],[['Draft v1','Superseded','Historical context only'],['Executed v2','Current and permitted','Support current answer'],['OTHER-02','Restricted unrelated matter','Exclude']],{h:325});caption(s,'Prepared retrieval trace. This table is not evidence of a live search run.');break;
 case 'trace':{
  let a=shape(s,65,215,530,345,C.paper,reveal(1,'claim'));text(s,'FINDING',86,233,480,34,23,true,C.teal,reveal(1,'label'));text(s,'The group exception may apply. Confirm ownership and continued provider responsibility.',86,294,480,225,33,true,C.ink,reveal(1,'claim-text'));
  let b=shape(s,685,215,530,345,C.pale,reveal(2,'source'));text(s,'CONTRACT-01 v2, CLAUSE 3',706,233,480,44,23,true,C.teal,reveal(2,'source-label'));text(s,clause,706,294,480,245,29,false,C.ink,reveal(2,'source-text'));let l=link(s,a,b);l.name=reveal(2,'source-link');caption(s,'The clause establishes wording. Transaction facts require their own evidence.');break;}
 case 'evidence':
  nativeTable(s,x.headers||['Claim','Source and location','Status'],x.rows||[['Rule with exception','CONTRACT-01 v2, clause 3','Text checked'],['Wholly owned group','Client ownership evidence','Not supplied'],['Legal proposition','Current authority and passage','Verify separately']],{h:340});caption(s,'The judgment’s printed page 3 supports the appeal-scope proposition. Current applicability needs further checks.');break;
 case 'entities':
  text(s,'Victoria Services Ltd engages Equator Systems Ltd\nunder an agreement effective 15 August 2026.',65,221,1140,130,39,true);
  nativeTable(s,['Entity span','Category'],[['Victoria Services Ltd','Organisation'],['Equator Systems Ltd','Organisation'],['15 August 2026','Date']],{y:401,h:185,size:25});caption(s,'Recognition identifies spans. Roles, relationships and obligations require further analysis.');break;
 case 'clauseparts':
  const pp=[['RULE','Prior written consent for change of control.'],['EXCEPTION','Wholly owned group reorganisation.'],['CONDITION','Provider remains responsible for its obligations.']];
  pp.forEach(([a,b],i)=>{text(s,a,65,215+i*126,310,60,25,true,i===0?C.orange:C.teal,reveal(i+1,'part-label'));text(s,b,385,215+i*126,825,93,34,false,C.ink,reveal(i+1,'part-text'));});caption(s,'Teaching decomposition. Consult the complete clause before interpreting its effect.');break;
 case 'reviewtable':
  nativeTable(s,['Source','Finding','Next step'],[['Clause 3','Exception with conditions','Confirm ownership and responsibility'],['Clause 2','Prior approval for support access','Check named people and approval'],['Clause 4','Fee schedule absent','Obtain the signed schedule']],{h:350});caption(s,'Fictional teaching review. Partner approval determines the use of the finding.');break;
 case 'tooljson':
  text(s,'REQUEST',65,210,520,45,26,true,C.teal);text(s,'{\n  "tool": "lookup_contract",\n  "contract_id": "CONTRACT-01",\n  "version": "v2"\n}',65,280,520,265,30);
  text(s,'RETURNED EVIDENCE',680,210,530,45,26,true,C.teal);text(s,'Clause text\nVersion and status\nSource location\nOr a controlled error',680,280,530,265,33);caption(s,'Illustrative request. Syntax, permissions and factual support need separate checks.');break;
 case 'agentloop':{
  const coords=[[65,220],[705,220],[705,430],[65,430]],steps=[['Model chooses','Permitted next operation'],['Execution checks','Authority and arguments'],['Tool returns','Evidence or error'],['Model continues','Answer, ask or stop']],nodes=[];
  steps.forEach(([a,b],i)=>{let [px,py]=coords[i];nodes[i]=shape(s,px,py,510,135,C.paper,reveal(i+1,'stage'));text(s,a,px+18,py+14,474,52,30,true,C.teal,reveal(i+1,'label'));text(s,b,px+18,py+76,474,46,27,false,C.ink,reveal(i+1,'detail'));});
  [['right','left'],['bottom','top'],['left','right'],['top','bottom']].forEach(([a,b],i)=>{let l=link(s,nodes[i],nodes[(i+1)%4],0,a,b);l.name=reveal(i===3?4:i+2,'loop-arrow');});caption(s,'Stop on denied access, missing evidence or limits. Human approval gates consequential actions.');break;}
 case 'reconciliation':
  flow(s,[['Raw import','125 million'],['Remove duplicate','125 − 25 = 100'],['Apply credit','100 − 2 = 98'],['Match ledger','98 million']]);caption(s,'UGX million. Source identity and adjustments explain the difference; this computes no tax liability.');break;
 case 'waterfall':{
  const ch=s.charts.add('bar',{position:{left:75,top:205,width:1125,height:285},categories:['Raw import','Less duplicate','Less credit','Net sales'],series:[{name:'Invisible base',values:[0,100,98,0],fill:'none'},{name:'Total',values:[125,0,0,98],fill:C.teal},{name:'Deduction',values:[0,25,2,0],fill:C.orange}],barOptions:{direction:'column',grouping:'stacked',gapWidth:125},hasLegend:false,chartFill:C.white,chartLine:{fill:'none',width:0},plotAreaFill:C.white,xAxis:{textStyle:{fontSize:21,fill:C.ink},tickLabelPosition:'low'},yAxis:{minimumScale:0,maximumScale:140,textStyle:{fontSize:18,fill:C.muted},majorGridlines:{fill:C.line,width:1}},dataLabels:{showValue:false}});applyPresentationChartFont(ch,{fontFamily:FONT});
  text(s,'125 − 25 = 100; 100 − 2 = 98',65,492,1140,48,31,true,C.teal);
  shape(s,65,554,Math.round(1150*80/98),43,C.teal);shape(s,65+Math.round(1150*80/98),554,Math.round(1150*18/98),43,C.orange);
  text(s,'80 received',85,557,600,37,25,true,C.white);text(s,'18 outstanding',1000,558,205,37,23,true,C.white);
  caption(s,'UGX million. The 98 net sales split into 80 received and 18 outstanding under the stated timing assumptions.');return 'chart';}
 case 'financechart':{
  const c=s.charts.add('bar',{position:{left:90,top:205,width:1100,height:365},categories:['Raw import','Unique invoices','Net sales','Receipts'],series:[{name:'UGX million',values:[125,100,98,80],fill:C.teal}],barOptions:{direction:'column',grouping:'clustered',gapWidth:100},hasLegend:false,chartFill:C.white,chartLine:{fill:'none',width:0},plotAreaFill:C.white,xAxis:{textStyle:{fontSize:23,fill:C.ink},tickLabelPosition:'low'},yAxis:{textStyle:{fontSize:20,fill:C.muted},majorGridlines:{fill:C.line,width:1}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:27,bold:true,fill:C.ink}}});applyPresentationChartFont(c,{fontFamily:FONT});caption(s,'UGX million. Fictional teaching values with different definitions; differences require reconciliation.');return 'chart';}
 case 'taxexceptions':
  nativeTable(s,['Issue','Evidence','Status'],[['Duplicate INV-003','Same invoice repeated in import','Corrected import'],['Credit note: 2 million','CN-001 against INV-003','Reconciled'],['Missing identifier','INV-002 evidence field blank','Request support']],{h:350});caption(s,'Corrected data issues remain distinct from open professional tax questions.');break;
 case 'access':
  flow(s,[['User','M-01 team'],['Permission','M-01 allowed'],['Evidence','CONTRACT-01'],['Answer','Permitted sources only']]);caption(s,'OTHER-02 remains restricted. Source and derived access need maintenance and tests.');break;
 case 'riskcycle':{
  shape(s,65,210,1150,84,C.pale,reveal(1,'govern'));text(s,'GOVERN: responsibilities, policies and continuing oversight',83,228,1110,53,31,true,C.teal,reveal(1,'govern-label'));
  [['Map','Use, context and effects'],['Measure','Evidence about risks'],['Manage','Treatment and monitoring']].forEach(([a,b],i)=>{let px=65+i*400;shape(s,px,375,350,170,C.paper,reveal(2,'function-'+i));text(s,a,px+18,393,314,50,32,true,C.teal,reveal(2,'label-'+i));text(s,b,px+18,462,314,70,28,false,C.ink,reveal(2,'detail-'+i));});
  caption(s,'Govern applies throughout. Map, Measure and Manage interact and repeat as the system changes.');break;}
 case 'processcompare':{
  const current=[['Search','Find source'],['Read','Interpret'],['Draft','Prepare'],['Partner','Review']],assisted=[['Retrieve','Permitted sources'],['AI draft','Cited finding'],['Reviewer','Check and decide'],['Record','Approved result']];
  [current,assisted].forEach((steps,row)=>{let yy=258+row*227;text(s,row?'ASSISTED PROCESS':'CURRENT PROCESS',65,yy-52,1150,38,25,true,row?C.teal:C.orange,reveal(row+1,'route'));let nodes=[];
   steps.forEach(([a,b],i)=>{let px=65+i*296;nodes[i]=shape(s,px,yy,262,123,row?C.pale:C.paper,reveal(row+1,'stage-'+i));text(s,a,px+14,yy+10,234,45,28,true,C.teal,reveal(row+1,'label-'+i));text(s,b,px+14,yy+65,234,50,25,false,C.ink,reveal(row+1,'detail-'+i));});
   for(let i=0;i<3;i++){let ln=link(s,nodes[i],nodes[i+1]);ln.name=reveal(row+1,'arrow-'+i);}
  });caption(s,'The assisted design changes preparation. Qualified review and accountable use remain explicit.');break;}
 case 'journey':
  flow(s,[['Understand','Task and model'],['Prepare','Information and search'],['Apply','Legal and tax work'],['Lead','Govern and evaluate']]);caption(s,'The same fictional matter connects technical understanding with organisational decisions.');break;
 default:throw Error('Unsupported diagram '+x.kind);
 }
 return null;
}
const tableKinds=new Set(['labelled','tokens','entities','retrievaltrace','evidence','reviewtable','taxexceptions']);
async function build(d){
 const dir=path.join(BUILD,'Slides',String(d.session).padStart(2,'0'));await fs.mkdir(dir,{recursive:true});
 for(const f of await fs.readdir(dir)){const m=f.match(/^slide-(\d+)\.png$/);if(m&&Number(m[1])>d.slides.length)await fs.unlink(path.join(dir,f));}
 const finalDir=path.join(BUILD,'Final Decks');await fs.mkdir(finalDir,{recursive:true});
 const oldReceipt=path.join(dir,'validation.json');
 try{await fs.access(oldReceipt);await fs.rename(oldReceipt,path.join(dir,'validation-'+Date.now()+'.json'));}catch(e){if(e.code!=='ENOENT')throw e;}
 const name=`${String(d.session).padStart(2,'0')} - ${d.title}.pptx`,out=path.join(finalDir,name);
 try{await fs.access(out);const prior=path.join(BUILD,'Prior Exports');await fs.mkdir(prior,{recursive:true});await fs.rename(out,path.join(prior,Date.now()+'-'+name));}catch(e){if(e.code!=='ENOENT')throw e;}
 const p=Presentation.create({slideSize:{width:1280,height:720}}),tables=[],charts=[];
 for(let i=0;i<d.slides.length;i++){
  const x=d.slides[i],s=p.slides.add();s.background.fill=C.white;
  if(x.kind==='cover'){
   s.background.fill=C.ink;text(s,`SESSION ${String(d.session).padStart(2,'0')}`,65,62,1100,45,26,true,'#F3A087');
   text(s,d.title,65,176,1115,200,d.title.length>40?56:64,true,C.white);
   text(s,d.aim,65,430,1090,120,32,false,'#DCE8E6');
   text(s,'Jotham Martin Wambi   KLAi Professional Learning',65,631,1120,42,24,false,'#DCE8E6');
  }else{
   header(s,x,d,i+1);
   if(x.kind==='table'){nativeTable(s,x.headers,x.rows);tables.push(i+1);if(x.caption)caption(s,x.caption);}
   else if(x.kind==='compare'){compare(s,x.left,x.right);if(x.caption)caption(s,x.caption);}
   else if(x.kind==='flow'){flow(s,x.steps);}
   else if(x.kind==='screenshot'){
    if(x.asset==='document_layout'){
     image(s,x.asset,x.caption,65,207,660,388);
     text(s,'Characters and words',780,218,420,65,30,true,C.teal);text(s,'OCR recovers readable text.',780,294,420,90,30);
     text(s,'Layout and relationships',780,421,420,65,30,true,C.teal);text(s,'Headings, tables and reading order preserve context.',780,497,420,110,29);
    }else if(x.asset==='contract_page'){
     image(s,x.asset,x.caption,65,210,680,370);
     text(s,'DAMAGED EXTRACT',790,215,420,45,24,true,C.orange);text(s,'Consent is required for a reorganisation within a wholly owned group.',790,291,420,220,33);text(s,'Which wording disappeared?',790,532,420,65,28,true,C.teal);
    }else{image(s,x.asset,x.caption);}
    caption(s,x.caption);
   }
   else if(['text','agenda','clause','failure','leadership','product','prompt','authority','workshop','debrief','decision','close','riskregister','incident','injection'].includes(x.kind)){
    paragraphs(s,x.body,{size:x.kind==='close'?34:31,height:x.body.length===1?360:400});
    if(['workshop','decision'].includes(x.kind))caption(s,x.kind==='workshop'?'We complete this together during class.':'Record the decision and the evidence still needed.');
   }else{let k=diagram(s,x,d);if(k==='chart')charts.push(i+1);if(tableKinds.has(x.kind))tables.push(i+1);}
  }
  let note=x.note;
  const stages=[...new Set(s.shapes.items.map(z=>z.name?.match(/^reveal-(\d+)-/)?.[1]).filter(Boolean))].sort();
  note+='\n\nPlayback: '+(stages.length?`${stages.length} native click reveals. Advance each stage and ask about the relationship it adds.`:'Static slide. Discuss the complete visual; no click build is attached.');
  if(x.kind==='screenshot')note+='\nImage attribution: '+x.caption+'\n'+x.refs.join('\n');
  s.speakerNotes.text=note;
 }
 // Render each authored slide; final import and layout checks inspect the saved package.
 for(let i=0;i<p.slides.items.length;i++){let b=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(dir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));}
 const raw=path.join(dir,'draft.pptx'),candidate=path.join(dir,'animated.pptx'),lesson=path.join(dir,'lesson.json');
 await(await PresentationFile.exportPptx(p)).save(raw);await fs.writeFile(lesson,JSON.stringify(d));
 execFileSync(PY,[path.join(HERE,'add_animations.py'),raw,candidate,lesson]);
 const result=await finalizePresentation({workspaceDir:AUTHOR,candidatePath:candidate,finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),explicitTotalSlideCount:d.slides.length,requiredNativeTableOwnerSlides:tables,requiredNativeChartOwnerSlides:charts,fontPolicy:{basis:'design',families:[FONT]},materializeLiteralChartWorkbooks:charts.length>0,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tables.flatMap(n=>['--require-native-table-slide',String(n)])],verifyArtifactToolImport:true,receiptPath:path.join(dir,'validation.json')});
 console.log(JSON.stringify({session:d.session,slides:d.slides.length,file:out,findings:result.presentationLayout?.findingCount,warnings:result.presentationLayout?.warnings}));
}
const chosen=process.argv.slice(2).map(Number);for(const d of DATA)if(!chosen.length||chosen.includes(d.session))await build(d);
