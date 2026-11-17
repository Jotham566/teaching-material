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
async function build(square){const H=square?1080:1350;const p=Presentation.create({slideSize:{width:1080,height:H}});const s=p.slides.add();s.background.fill=C.paper;
 tx(s,'KLAi',56,34,148,66,48,C.navy,true);tx(s,'KAMPALA AI',205,51,300,34,23,C.teal,true);tx(s,'DECEMBER 2026',728,48,310,38,28,C.navy,true);
 const hy=square?115:125,hs=square?86:108,step=square?88:115;
 tx(s,'What will',56,hy,970,step+12,hs,C.navy,true);tx(s,'you build',56,hy+step,970,step+12,hs,C.navy,true);tx(s,'this holiday?',56,hy+step*2,970,step+12,hs,C.teal,true);
 const camp=square?408:529;
 tx(s,'HOLIDAY DATA & AI CAMP',56,camp,980,56,square?39:42,C.navy,true);
 tx(s,'For students and school leavers',56,camp+63,968,45,square?29:32,C.navy);
 const oy=square?549:675;
 await im(s,'chart-column-00769B.png',56,oy+4,67,67);
 tx(s,'A data project',146,oy,405,46,33,C.teal,true);tx(s,'Explore real data.\nCreate charts that explain it.',146,oy+51,410,82,27,C.navy);
 await im(s,'brain-6500BC.png',575,oy+4,67,67);
 tx(s,'A prediction model',666,oy,366,45,32,C.purple,true);tx(s,'Train a model.\nTest its predictions.',666,oy+51,366,82,27,C.navy);
 const my=square?706:844;
 tx(s,'8 weeks',56,my,230,55,39,C.navy,true);tx(s,'Max. 5 learners\nper group',292,my+1,360,83,29,C.navy,true);
 tx(s,'15 places',752,my-1,280,58,43,C.purple,true);tx(s,'across the programme',752,my+58,282,35,22,C.navy);
 const fy=square?796:961;
 tx(s,'UGX 1,000,000 per learner',56,fy,968,48,square?32:36,C.navy,true);
 tx(s,'No coding experience needed. Bring a Windows or Mac laptop.',56,fy+55,970,42,square?25:27,C.navy);
 if(!square){tx(s,'The National ICT Innovation Hub, Nakawa + online',56,1070,970,43,27,C.teal,true);}
 const foot=square?902:1134;band(s,foot,H-foot);
 tx(s,'Register your interest',56,foot+23,748,48,square?35:38,C.yellow,true);
 tx(s,'forms.gle/n8XLwbK1QxcUsRnx5',56,foot+83,753,42,32,C.white,true);
 tx(s,'Calls & WhatsApp: +256 750 990 718',56,foot+139,753,38,28,C.white);
 await im(s,'registration-qr.png',844,foot+16,square?150:164,square?150:164);
 s.speakerNotes.textFrame.setText('Camp details supplied by Jotham Martin Wambi. Programme capacity is 15 total places; this is not a claim about remaining availability. Start date remains to be confirmed. In-person sessions at The National ICT Innovation Hub, Nakawa; two in person and one online per week. Registration is a request for a place. Icons sourced previously from Font Awesome Free: https://fontawesome.com/license/free (license included). Registration QR points to https://forms.gle/n8XLwbK1QxcUsRnx5 . KLAi brand is editable text, not a reconstructed logo.');
 const stem=square?'Camp_Project_Square':'Camp_Project_Portrait';
 const candidatePath=`${root}/.build/${stem}.pptx`,finalPath=`${root}/output/${stem}_Editable.pptx`;
 await (await PresentationFile.exportPptx(p)).save(candidatePath);
 await finalizePresentation({workspaceDir:root,candidatePath,finalPath,pythonExecutable:`${runtime}/python/bin/python3`,integrityValidatorPath:`${SK}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${SK}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu',`${1080*9525},${H*9525}`,'--validate-heading-fit'],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:`${root}/.build/${stem}.validation.json`});
 const out=await PresentationFile.importPptx(await FileBlob.load(finalPath));const png=await out.export({slide:out.slides.items[0],format:'png',scale:2});await fs.writeFile(`${root}/output/${stem}.png`,new Uint8Array(await png.arrayBuffer()));console.log(stem+' complete');
}
await build(false);await build(true);
