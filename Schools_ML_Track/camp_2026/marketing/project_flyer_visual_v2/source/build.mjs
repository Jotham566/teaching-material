import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies';
process.env.RUNTIME_NODE_MODULES=path.join(runtime,'node/node_modules');
const require=createRequire(path.join(runtime,'node/node_modules/package.json'));
const {Presentation,PresentationFile,FileBlob}=await import(require.resolve('@oai/artifact-tool'));
const SK='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations/26.1013.11914/skills/presentations';
const {finalizePresentation}=await import(`${SK}/container_tools/artifact_tool_utils.mjs`);
const C={navy:'#002540',teal:'#007D9B',purple:'#6500BC',paper:'#FAF8F1',yellow:'#FFDB55',white:'#FFFFFF'};
function tx(s,v,x,y,w,h,size=32,color=C.navy,bold=false){const a=s.shapes.add({name:v.split('\n')[0],geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=v;a.text.style={typeface:'Arial',fontSize:size,bold,color,autoFit:'none',wrap:'none',insets:{top:0,left:0,right:0,bottom:0},verticalAlignment:'top'};return a;}
async function im(s,f,x,y,w,h){s.images.add({blob:await fs.readFile(`${root}/assets/${f}`),contentType:'image/png',position:{left:x,top:y,width:w,height:h},fit:'contain',alt:f==='registration-qr.png'?'Scan to open the camp registration form':f.includes('brain')?'Machine learning':'Data analysis'});}
function band(s,y,h){s.shapes.add({name:'Registration footer background',geometry:'rect',position:{left:0,top:y,width:1080,height:h},fill:C.navy,line:{fill:'none',width:0}});}
async function build(square){
 const H=square?1080:1350;
 const p=Presentation.create({slideSize:{width:1080,height:H}}),s=p.slides.add();s.background.fill=C.paper;
 const heroEnd=square?470:610;
 band(s,0,heroEnd);
 tx(s,'KLAi',56,24,148,64,47,C.white,true);
 tx(s,'KAMPALA AI',205,43,300,34,23,C.yellow,true);
 tx(s,'DECEMBER 2026',728,38,310,38,27,C.white,true);
 const photoTop=square?94:110;
 s.images.add({blob:await fs.readFile(`${root}/assets/students-learning-kampus-pexels.jpg`),contentType:'image/jpeg',position:{left:520,top:photoTop,width:560,height:heroEnd-photoTop},fit:'cover',alt:'Illustrative stock photograph of two students working together at a laptop, with a tutor'});
 const hy=square?121:162,step=square?77:86,hs=square?68:74;
 tx(s,'What will',48,hy,475,96,hs,C.white,true);
 tx(s,'you build',48,hy+step,475,96,hs,C.white,true);
 tx(s,'this holiday?',48,hy+2*step,475,96,hs,C.yellow,true);
 tx(s,'No coding experience needed',48,square?371:464,460,42,square?25:27,C.white,true);
 const logoY=square?417:533,logoS=square?38:48;
 s.shapes.add({name:'Light background for library logos',geometry:'rect',position:{left:48,top:logoY-8,width:275,height:logoS+16},fill:C.paper,line:{fill:'none',width:0}});
 for(const [f,x] of [['python-original.png',64],['pandas-original.png',143],['scikitlearn-original.png',221]]) await im(s,f,x,logoY,logoS,logoS);
 tx(s,'Illustrative photo: Kampus Production / Pexels',527,heroEnd+7,535,23,16,'#566775');
 const camp=square?515:665;
 tx(s,'HOLIDAY DATA & AI CAMP',48,camp,980,56,square?40:45,C.navy,true);
 tx(s,'For students and school leavers',48,camp+59,984,45,square?29:32,C.navy);
 const oy=square?646:804;
 await im(s,'chart-column-00769B.png',48,oy+4,60,60);
 tx(s,'A data project',130,oy,420,45,square?30:32,C.teal,true);
 tx(s,'Explore real data.\nCreate charts that explain it.',130,oy+49,428,80,square?25:27,C.navy);
 await im(s,'brain-6500BC.png',568,oy+4,60,60);
 tx(s,'A prediction model',649,oy,390,45,square?30:32,C.purple,true);
 tx(s,'Train a model.\nTest its predictions.',649,oy+49,390,80,square?25:27,C.navy);
 const my=square?788:967;
 tx(s,'8 weeks',48,my,230,52,square?34:39,C.navy,true);
 tx(s,'Max. 5 learners per group',265,my+7,460,42,square?26:28,C.navy,true);
 tx(s,'15 places',786,my-3,260,58,square?39:43,C.purple,true);
 tx(s,'across the programme',786,my+47,270,30,20,C.navy);
 const fee=square?837:1045;
 tx(s,'UGX 1,000,000 per learner',48,fee,975,48,square?31:36,C.navy,true);
 if(square){tx(s,'Nakawa + online. Windows or Mac laptop required.',48,fee+47,975,35,24,C.teal,true);}
 else{tx(s,'Windows or Mac laptop required',48,1098,975,39,27,C.navy);tx(s,'The National ICT Innovation Hub, Nakawa + online',48,1138,975,37,27,C.teal,true);}
 const foot=square?929:1188;band(s,foot,H-foot);
 tx(s,'Register your interest',48,foot+15,745,46,square?32:35,C.yellow,true);
 tx(s,'forms.gle/n8XLwbK1QxcUsRnx5',48,foot+65,760,43,square?29:31,C.white,true);
 tx(s,'Calls & WhatsApp: +256 750 990 718',48,foot+115,760,38,square?26:28,C.white);
 await im(s,'registration-qr.png',858,foot+14,square?125:135,square?125:135);
 s.speakerNotes.textFrame.setText('Camp details supplied by Jotham Martin Wambi. Programme capacity is 15 total places, not remaining availability. Start date to be confirmed. Two in-person sessions at The National ICT Innovation Hub, Nakawa, and one online session per week. Registration is a request for a place. Photo: Kampus Production, https://www.pexels.com/photo/attentive-young-black-groupmates-using-laptop-while-preparing-for-exams-with-anonymous-teacher-5940713/ . Pexels license https://www.pexels.com/license/ . Photo is illustrative stock photography, not a picture of KLAi learners or coaches; no endorsement implied. Icons: Font Awesome Free https://fontawesome.com/license/free . Library logos: Devicon https://devicon.dev/ . QR: https://forms.gle/n8XLwbK1QxcUsRnx5');
 const stem=square?'Camp_Visual_Square_Final':'Camp_Visual_Portrait_Final';
 const candidatePath=`${root}/.build/${stem}.pptx`,finalPath=`${root}/output/${stem}_Editable.pptx`;
 await (await PresentationFile.exportPptx(p)).save(candidatePath);
 await finalizePresentation({workspaceDir:root,candidatePath,finalPath,pythonExecutable:`${runtime}/python/bin/python3`,integrityValidatorPath:`${SK}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${SK}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu',`${1080*9525},${H*9525}`,'--validate-heading-fit'],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:`${root}/.build/${stem}.validation.json`});
 const out=await PresentationFile.importPptx(await FileBlob.load(finalPath));
 const png=await out.export({slide:out.slides.items[0],format:'png',scale:2});
 await fs.writeFile(`${root}/output/${stem}.png`,new Uint8Array(await png.arrayBuffer()));console.log(stem+' complete');
}
await build(false);await build(true);
