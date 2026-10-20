/** Editable PPTX teaching edition, built with the bundled Artifact Tool runtime. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const runtime=process.env.RUNTIME_NODE_MODULES || '/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=runtime;
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(runtime,'@oai/artifact-tool/dist/artifact_tool.mjs')).href).catch(async()=>{
 const {createRequire}=await import('node:module');return createRequire(path.join(runtime,'package.json'))('@oai/artifact-tool');
});
const skillRoot='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations';
const skillVersion=(await fs.readdir(skillRoot)).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})).at(-1);
const skill=path.join(skillRoot,skillVersion,'skills/presentations');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const review=path.join(root,'review/2026-09-15/ppt-revision');
const decks=JSON.parse(await fs.readFile(path.join(root,'data/iuea_deck_content.json'),'utf8'));
const selected=process.argv.slice(2);const edition=process.env.PPT_EDITION||('build-'+Date.now());
const ink='#1C3144',orange='#E4572E',muted='#6B7A8A',teal='#2E7D6F';
function panel(slide,left,top,width,height,fill){return slide.shapes.add({geometry:'rect',position:{left,top,width,height},fill,line:{fill:'none',width:0}});}
function textbox(slide,text,left,top,width,height,size=30,font='Calibri',color=ink,bold=false){
 const box=slide.shapes.add({geometry:'textbox',position:{left,top,width,height},fill:'none',line:{fill:'none',width:0}});
 box.text=text;box.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none'};return box;
}
for(const deck of decks){
 if(selected.length && !selected.includes(deck.cohort+'-W'+String(deck.week).padStart(2,'0')))continue;
 const dest=path.join(review,'final',edition,deck.filename);await fs.mkdir(path.dirname(dest),{recursive:true});
 if(await fs.stat(dest).catch(()=>null)){console.log('EXISTS '+deck.filename);continue;}
 const build=path.join(review,'build',edition,deck.filename.replace('.pptx',''));await fs.mkdir(build,{recursive:true});
 const presentation=Presentation.create({slideSize:{width:1279.968,height:720}});let tableOwners=[];let idx=0;
 for(const s of deck.slides){
  idx++;const slide=presentation.slides.add();
  const k=s.kind||'explanation';
  const paragraphs=(s.body||'').split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean);
  const dark=['question','exit'].includes(k);
  slide.background.fill=dark?ink:'#FFFFFF';
  async function illustration(file,pos){const bytes=await fs.readFile(path.join(root,file));slide.images.add({blob:new Uint8Array(bytes),contentType:'image/png',alt:s.title,fit:'contain',position:pos});}
  function header(label){
   if(!dark)panel(slide,0,0,1279.968,146,ink);
   textbox(slide,label,62,19,1160,30,20,'Calibri',orange,true);
   textbox(slide,s.title,62,55,1160,85,s.title.length>50?36:42,'Calibri','#FFFFFF',true);
  }
  function rowList(items,left=78,top=185,width=1120,height=445,color=ink){
   const step=height/items.length;
   items.forEach((p,i)=>{
    textbox(slide,String(i+1).padStart(2,'0'),left,top+i*step,65,60,34,'Calibri',orange,true);
    const size=p.length>200?27:30;
    textbox(slide,p,left+83,top+i*step,width-90,step-8,size,'Calibri',color);
   });
  }
  function bodyText(text,left,top,width,height,size=31,color=ink,bold=false){return textbox(slide,text,left,top,width,height,size,'Calibri',color,bold);}
  if(k==='cover'){
   await illustration(s.image,{left:0,top:0,width:1279.968,height:720});
   panel(slide,0,0,565,720,ink);
   textbox(slide,deck.cohort+'   WEEK '+deck.week,58,72,500,45,26,'Calibri',orange,true);
   textbox(slide,s.title,58,170,485,245,51,'Calibri','#FFFFFF',true);
   textbox(slide,s.body,58,425,485,115,28,'Calibri','#D8E3EC');
   textbox(slide,s.subtitle.split('\n').slice(1).join('\n'),58,574,490,91,23,'Calibri','#D8E3EC');
  }else if(k==='figure'||k==='scene'){
   // Enlarged illustrations have a compact header so their labels survive projection.
   panel(slide,0,0,1279.968,100,ink);
   textbox(slide,s.title,50,20,1180,68,s.title.length>65?34:39,'Calibri','#FFFFFF',true);
   await illustration(s.image,{left:35,top:111,width:1210,height:485});
   panel(slide,0,610,1279.968,62,'#E5F1EE');
   textbox(slide,s.caption,58,618,1160,50,24,'Calibri',teal,true);
  }else if(k==='code'){
   header('WORKED EXAMPLE');
   const maxLen=Math.max(...s.code.split('\n').map(x=>x.length));
   const split=maxLen<=44;
   const width=split?766:1135;
   const size=Math.min(29,s.code_size||29,(width-75)/(Math.max(maxLen,1)*0.62));
   if(size<22)throw Error('Code line too long '+deck.filename+' '+idx+' '+maxLen);
   panel(slide,55,178,width,358,ink);
   const codebox=textbox(slide,s.code,72,196,width-32,330,size,'Courier New','#F4F7FA');
   for(const token of ['def','return','for','if','else','elif','import','from','None','True','False']){
    try{codebox.text.get(token).color='#FFB080';}catch{}
   }
   const cues=s.explain||[];
   if(split){
    textbox(slide,'HOW TO READ IT',850,180,360,36,20,'Calibri',teal,true);
    cues.forEach((t,i)=>bodyText(t,850,232+i*112,350,99,24));
   }else{
    // Long code stays at a readable size. Its explanation continues in Presenter View.
    bodyText(cues[0]||'Read each input before running.',72,552,1120,50,25,teal,true);
   }
   textbox(slide,s.caption,72,612,1120,50,24,'Calibri',muted);
  }else if(k==='table'){
   header('READ THE EXAMPLE');
   tableOwners.push(idx);const values=s.table;
   const h=values.length<=3?240:350;
   const table=slide.tables.add({rows:values.length,columns:values[0].length,left:62,top:182,width:1156,height:h,values});
   const size=Math.max(...values.flat().map(x=>String(x).length))>38?23:27;
   for(let r=0;r<values.length;r++)for(let c=0;c<values[r].length;c++){
    const cell=table.getCell(r,c);cell.fill=r===0?teal:r%2?'#EEF3F6':'#FFFFFF';
    cell.text.style={typeface:'Calibri',fontSize:size,color:r===0?'#FFFFFF':ink,bold:r===0};
   }
   textbox(slide,s.caption,72,h+215,1120,118,27,'Calibri',ink);
  }else if(k==='concepts'){
   header('PLAIN-LANGUAGE MEANINGS');
   s.concepts.forEach((c,i)=>{
    const single=s.concepts.length===1;
    const left=62+i*590;
    panel(slide,left,180,single?1156:560,440,i?'#E5F1EE':'#EEF3F6');
    textbox(slide,c.term,left+25,205,single?1096:507,94,single?42:35,'Calibri',i?teal:orange,true);
    textbox(slide,c.meaning,left+25,322,single?1096:507,270,single?34:28,'Calibri',ink);
   });
  }else if(k==='activity'){
   header('TRY IT TOGETHER   '+s.duration.toUpperCase());
   rowList(paragraphs,65,190,1140,420);
   panel(slide,0,621,1279.968,49,'#E5F1EE');
   bodyText('Follow the worked example and explain the result.',65,628,1135,38,24,teal,true);
  }else if(k==='question'||k==='exit'){
   header(k==='exit'?'INDIVIDUAL EXIT CHECK':'PREDICT BEFORE RUNNING');
   bodyText(k==='exit'?'EXPLAIN IT':'YOUR TURN',65,170,300,52,26,orange,true);
   const size=(s.body||'').length>290?31:38;
   bodyText(s.body,65,241,1135,325,size,'#FFFFFF');
   bodyText(k==='exit'?'Point to your evidence. Save your work.':'Read the question, then follow the lecturer’s worked explanation.',65,608,1135,57,24,'#BBCDD9');
  }else if(k==='debrief'||k==='output'){
   header(k==='output'?'CHECK THE OUTPUT':'DISCUSS THE REASONING');
   panel(slide,62,184,1156,370,'#E5F1EE');
   const size=(s.body||'').length<140?42:32;
   textbox(slide,s.body,95,213,1085,320,size,k==='output'?'Courier New':'Calibri',teal,k!=='output');
   bodyText('Which step produced this result? What changes if one input changes?',72,586,1120,65,27,ink);
  }else if(k==='goals'){
   header('TODAY’S DESTINATION');
   panel(slide,62,182,550,440,'#EEF3F6');
   bodyText('WHAT WE WILL DO',87,210,498,40,22,orange,true);
   bodyText(s.body,87,272,498,310,30);
   bodyText('HOW YOU WILL SHOW IT',652,210,540,40,22,teal,true);
   bodyText(s.check,652,272,535,310,30);
  }else if(k==='link'||k==='test_entry'){
   const quiz=/quiz/i.test(s.title);const video=s.label.includes('video');
   header(k==='test_entry'?'TEST ACCESS':quiz?'QUIZ ACCESS':video?'WATCH, THEN EXPLAIN':'ASSIGNMENT SUBMISSION');
   const qr=s.qr&&await fs.readFile(path.join(root,s.qr)).catch(()=>null);
   rowList(paragraphs,62,181,qr?840:1150,335);
   if(qr){
    slide.images.add({blob:new Uint8Array(qr),contentType:'image/png',alt:(k==='test_entry'?'Test entry QR code for ':'Quiz QR code for ')+deck.cohort+' week '+deck.week,fit:'contain',position:{left:959,top:220,width:230,height:230}});
    bodyText(k==='test_entry'?'TEST FILES':'24 HOURS',970,462,230,40,28,orange,true);
   }
   panel(slide,62,540,1156,69,'#E5F1EE');
   const link=textbox(slide,s.label,84,553,1110,48,30,'Calibri',teal,true);link.text.get(s.label).link={uri:s.url,isExternal:true};
   if(k==='test_entry'){
    textbox(slide,'Direct URL (click or copy into your laptop browser):',72,617,1120,26,17,'Calibri',muted);
    const direct=textbox(slide,s.url,72,646,1140,34,14,'Calibri',teal);
    direct.text.get(s.url).link={uri:s.url,isExternal:true};
   }else textbox(slide,s.url,72,627,1120,32,17,'Calibri',muted);
  }else if(k==='contract'){
   header('YOUR REQUIRED TASK');
   panel(slide,62,184,1156,406,'#EEF3F6');
   bodyText(s.body,88,212,1100,356,(s.body||'').length>340?29:32);
   panel(slide,62,612,1156,53,'#E5F1EE');
   bodyText('Keep the exact names and outputs. Check types, units and the issued brief.',78,620,1124,39,24,teal,true);
  }else if(s.operation_prerequisite && paragraphs.length===1){
   header('ONE IDEA AT A TIME');
   panel(slide,62,184,1156,438,'#EEF3F6');
   bodyText(s.body,100,235,1075,330,34);
  }else if(k==='steps'){
   header('WHAT TO DO');
   rowList(paragraphs,62,187,1150,449);
  }else{
   header(k==='context'?'THE ENGINEERING QUESTION':'ONE IDEA AT A TIME');
   if(paragraphs.length>=3){rowList(paragraphs,62,187,1150,450);}
   else if(paragraphs.length===2){
    panel(slide,62,184,557,438,'#EEF3F6');panel(slide,651,184,567,438,'#E5F1EE');
    bodyText(paragraphs[0],89,222,499,366,31);bodyText(paragraphs[1],678,222,509,366,31);
   }else{
    const bits=(s.body||'').split(/(?<=[.!?])\s+(?=[A-Z])/);
    if(bits.length>1){
     panel(slide,62,184,470,441,teal);
     bodyText(bits[0],91,223,410,359,bits[0].length>180?30:36,'#FFFFFF',true);
     bodyText(bits.slice(1).join('\n\n'),581,210,620,407,30);
    }else{
     panel(slide,62,184,1156,438,'#EEF3F6');
     bodyText(s.body,96,234,1085,325,(s.body||'').length>230?32:40,ink,true);
    }
   }
  }
  if(k!=='cover')textbox(slide,deck.cohort+'   Week '+deck.week+'   '+idx,62,685,1135,23,16,'Calibri',dark?'#BBCDD9':muted);
  slide.speakerNotes.textFrame.setText(s.notes||'');
 }
 const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(presentation)).save(candidate);
 await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:dest,
 pythonExecutable:'/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12191695,6858000','--validate-bullet-geometry','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],
 requiredNativeTableOwnerSlides:tableOwners,fontPolicy:{basis:'design',families:['Cambria','Calibri','Courier New']},verifyArtifactToolImport:true,
 receiptPath:path.join(build,'validation.json')});
 // Render the exported file, not just the in-memory authoring model.
 const imported=await PresentationFile.importPptx(await FileBlob.load(dest));
 const render=path.join(build,'render');await fs.mkdir(render,{recursive:true});
 for(let i=0;i<imported.slides.items.length;i++){
  const png=await imported.export({slide:imported.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(render,`slide-${String(i+1).padStart(3,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 }
 console.log('BUILT '+deck.filename+' '+idx+' slides');
}
