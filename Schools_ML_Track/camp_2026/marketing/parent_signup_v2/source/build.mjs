import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(path.join(process.env.RUNTIME_NODE_MODULES,'package.json'));
const {Presentation,PresentationFile,FileBlob}=await import(require.resolve('@oai/artifact-tool'));
const SK='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations/26.1007.11041/skills/presentations';
const {finalizePresentation,applyPresentationChartFont}=await import(`${SK}/container_tools/artifact_tool_utils.mjs`);
const N='#002540',T='#007D9B',P='#6500BC',B='#007DDD',L='#E5F7FC',Y='#FFDA49',W='#FFFFFF';
const refs='UNESCO: https://www.unesco.org/en/articles/ai-competency-framework-students\nOECD: https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html\nNCDC: https://ele.ncdc.go.ug/course/section.php?id=9\nIcons: Font Awesome, https://fontawesome.com/license/free; Tabler, https://tabler.io/icons. Licenses included. Camp details supplied by Jotham Martin Wambi. No organisational endorsement implied.';
function tx(s,v,x,y,w,h,size=40,color=N,bold=false,font='Arial'){const a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=v;a.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none',wrap:'none',insets:{top:0,left:0,right:0,bottom:0},verticalAlignment:'top'};return a;}
function rect(s,x,y,w,h,c){s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:c,line:{fill:'none',width:0}});}
async function im(s,f,x,y,w,h){s.images.add({blob:await fs.readFile(`${root}/assets/${f}`),contentType:'image/png',position:{left:x,top:y,width:w,height:h},fit:'contain',alt:f});}
function base(p,i,label,dark=false){const s=p.slides.add();s.background.fill=dark?N:W;tx(s,'SCHOOL TRACK',64,55,670,45,29,dark?'#96DAE9':T,true);tx(s,`${i} / 7`,916,55,120,45,29,dark?'#96DAE9':T);tx(s,label,64,106,900,40,23,dark?'#96DAE9':T);tx(s,'HOLIDAY DATA & AI CAMP',64,1256,750,36,25,dark?W:N,true);tx(s,'DEC 2026',854,1256,190,36,25,dark?W:N,true);s.speakerNotes.textFrame.setText(refs);return s;}
function example(s,title,body,y=860){rect(s,0,y,1080,325,L);tx(s,title,64,y+35,952,54,33,T,true);tx(s,body,64,y+111,952,180,41,N);}
async function cta(s,subtitle){tx(s,'A holiday to build\nsomething useful.',64,204,952,210,78,W,true);tx(s,'For S.4, S.5 & S.6 students\nand school leavers',64,460,952,125,44,Y,true);tx(s,'Data Analysis & Machine Learning\nNo coding experience needed',64,631,952,116,38,W);tx(s,'8 weeks     Maximum 5 learners per group',64,790,952,49,32,'#BFEAF3');tx(s,'UGX 1,000,000 per learner',64,852,952,53,39,W,true);tx(s,'REGISTER FOR DECEMBER',64,978,728,48,34,Y,true);tx(s,'forms.gle/n8XLwbK1QxcUsRnx5',64,1040,728,45,31,W);tx(s,'Calls & WhatsApp: +256 750 990 718',64,1110,752,43,31,W);await im(s,'registration-qr.png',857,984,165,165);tx(s,subtitle,64,1180,952,33,22,'#BFEAF3');}
let p=Presentation.create({slideSize:{width:1080,height:1350}});
let s=base(p,1,'FOR PARENTS',true);
tx(s,'This holiday,',64,227,952,120,79,W,true);
tx(s,'your child could\nbuild their first\ndata project.',64,381,952,360,84,Y,true);
tx(s,'A guided start in Data Analysis\nand Machine Learning.',64,853,952,122,42,W);
tx(s,'For S.4, S.5 & S.6 students\nand school leavers',64,1042,952,108,38,'#BFEAF3',true);
s=base(p,2,'WHY START BEFORE UNIVERSITY?');
tx(s,'Give curiosity\na practical outlet.',64,212,952,212,76,N,true);
tx(s,'Help your learner practise skills\nthey can use across subjects.',64,481,952,115,40,T);
await im(s,'database-00769B.png',64,685,85,85);tx(s,'Work with real datasets',189,698,813,58,42,N,true);
await im(s,'chart-column-00769B.png',64,835,85,85);tx(s,'Explain what the numbers show',189,848,813,58,41,N,true);
await im(s,'brain-6500BC.png',64,985,85,85);tx(s,'Question AI-generated answers',189,998,813,58,41,N,true);
tx(s,'An opportunity to explore their interests early.',64,1164,952,47,30,T);
s=base(p,3,'A REAL PUBLIC DEMONSTRATION');
tx(s,'Can a computer\nidentify a flower?',64,197,952,193,73,N,true);
tx(s,'This example predicts the flower type\nusing measurements from the Iris dataset.',64,428,952,108,37,T);
await im(s,'iris-project-screenshot.png',48,602,984,410);
tx(s,'Dots: measured flowers. Colours: model predictions.',64,1052,952,43,30,N,true);
tx(s,'Published scikit-learn example using the UCI Iris dataset.\nExternal example; not camp learner work. Source link in caption.',64,1137,952,74,24,T);
s.speakerNotes.textFrame.setText(refs+'\nActual screenshot of https://scikit-learn.org/stable/_images/sphx_glr_plot_classification_001.png from https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html . Copyright scikit-learn developers, BSD-3-Clause. Screenshot unchanged apart from fitting to slide. Dataset: https://archive.ics.uci.edu/dataset/53/iris . This external example is illustrative and is not a promised exact camp project or learner work.');
s=base(p,4,'WHAT YOUR CHILD WILL BUILD');
await im(s,'folder-open-00769B.png',64,206,132,132);
tx(s,'A project to show.\nFindings to explain.',64,389,952,205,72,N,true);
tx(s,'DATA ANALYSIS',64,675,952,50,33,T,true);
tx(s,'Analyse a dataset, create clear charts\nand present a portfolio project.',64,744,952,118,40,N);
tx(s,'MACHINE LEARNING',64,930,952,50,33,P,true);
tx(s,'Build a prediction model, test it\nand explain where it makes mistakes.',64,1000,952,119,40,N);
s=base(p,5,'GUIDANCE YOU CAN ASK ABOUT');
tx(s,'A guided start.\nA small group.',64,200,952,206,75,N,true);
tx(s,'No coding experience needed.\nBegin with Python programming basics.',64,466,952,116,41,T);
tx(s,'Maximum 5 learners per group',64,637,952,64,46,N,true);
rect(s,0,771,1080,425,L);
tx(s,'YOUR TUTOR',64,804,952,43,28,T,true);
tx(s,'Jotham Martin Wambi',64,868,952,65,49,N,true);
tx(s,'Lecturer in AI & Machine Learning, IUEA\nData Scientist & ML/AI Engineer\nMaster’s, Yamaguchi University, Japan',64,963,952,173,35,N);
s=base(p,6,'PLAN THEIR DECEMBER LEARNING');
tx(s,'8 weeks of\npractical learning',64,215,952,207,75,N,true);
tx(s,'UGX 1,000,000',64,536,952,102,82,P,true);
tx(s,'per learner',64,653,952,62,43,N,true);
tx(s,'Same fee per learner for groups of 1–5.',64,749,952,55,33,T);
tx(s,'3 learning days each week',64,825,952,50,37,N,true);
tx(s,'2 in person at The National ICT Innovation Hub,\nNakawa. 1 online. Other days: project work.',64,891,952,105,32,N);
tx(s,'Bring a Windows or Mac laptop.',64,1030,952,49,35,T,true);
tx(s,'Start date and session times: to be confirmed.',64,1130,952,46,29,T);
s=base(p,7,'DECEMBER 2026 REGISTRATION',true);
tx(s,'Give your child\na place to begin.',64,199,952,212,80,W,true);
tx(s,'15 places',64,500,952,120,100,Y,true);
tx(s,'across the whole programme',64,648,952,60,39,W);
tx(s,'Register one or more learners\nthrough the parent/guardian option.',64,791,952,117,39,'#BFEAF3');
tx(s,'REGISTER YOUR CHILD',64,984,747,50,36,Y,true);
tx(s,'forms.gle/n8XLwbK1QxcUsRnx5',64,1051,747,49,31,W);
tx(s,'Calls & WhatsApp: +256 750 990 718',64,1113,752,48,31,W);
await im(s,'registration-qr.png',857,984,165,165);
tx(s,'Programme capacity: 15. Availability confirmed after enquiry.',64,1185,952,39,23,'#BFEAF3');
await finish(p,'Parent_Signup_Carousel','carousel',[]);
async function finish(p,name,dir,charts){const candidate=`${root}/.build/${name}.pptx`,final=`${root}/output/${name}_Editable.pptx`;await (await PresentationFile.exportPptx(p)).save(candidate);await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:'/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:`${SK}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${SK}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu','10287000,12858750','--validate-heading-fit'],explicitTotalSlideCount:p.slides.items.length,fontPolicy:{basis:'design',families:['Arial']},materializeLiteralChartWorkbooks:charts.length>0,requiredNativeChartOwnerSlides:charts,verifyArtifactToolImport:true,receiptPath:`${root}/.build/${name}-validation.json`});const finalP=await PresentationFile.importPptx(await FileBlob.load(final));for(let i=0;i<finalP.slides.items.length;i++){const png=await finalP.export({slide:finalP.slides.items[i],format:'png',scale:1});await fs.writeFile(`${root}/output/${dir}/${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await png.arrayBuffer()));}console.log(`Finished ${name}`);}
