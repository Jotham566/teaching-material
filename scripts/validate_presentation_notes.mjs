import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
process.env.RUNTIME_NODE_MODULES='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const require=createRequire('/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {PresentationFile,FileBlob}=require('@oai/artifact-tool');
const skill='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.61513/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(`${skill}/container_tools/artifact_tool_utils.mjs`));
const base=path.resolve('review/2026-09-21/presentation-notes');
const plan=JSON.parse(await fs.readFile(`${base}/installation.json`,'utf8'));
const notes=JSON.parse(await fs.readFile(`${base}/notes-plan.json`,'utf8'));
await fs.mkdir(`${base}/validated`,{recursive:true});let report=[];
const prior=JSON.parse(await fs.readFile(`${base}/validation-progress.json`,'utf8').catch(()=> '[]'));
const {createHash}=await import('node:crypto');
for(const d of plan){
 const name=path.basename(d.path),work=`${base}/validation/${name.slice(0,-5)}`;await fs.mkdir(work,{recursive:true});
 const old=prior.find(x=>x.path===d.path);const receipt=await fs.readFile(`${work}/validation.json`,'utf8').then(JSON.parse).catch(()=>null);
 const digest=createHash('sha256').update(await fs.readFile(d.path)).digest('hex');
 if(old && receipt?.finalSha256===digest && !old.fit_flags.length){report.push(old);await fs.writeFile(`${base}/validation-progress.json`,JSON.stringify(report,null,2));console.log(name+' unchanged, verified receipt');continue;}
 const candidate=`${work}/candidate.pptx`;await fs.copyFile(d.path,candidate);
 await fs.rm(`${base}/validated/${name}`,{force:true});
 await fs.rm(`${work}/validation.json`,{force:true});
 await finalizePresentation({workspaceDir:process.cwd(),candidatePath:candidate,finalPath:`${base}/validated/${name}`,explicitTotalSlideCount:d.slides,pythonExecutable:'/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:[],verifyArtifactToolImport:true,receiptPath:`${work}/validation.json`});
 const p=await PresentationFile.importPptx(await FileBlob.load(`${base}/validated/${name}`));
 if(p.slides.items.length!==d.slides)throw Error('Slide count '+name);
 const expected=notes.find(x=>x.path===d.path);
 const inspected=(await p.inspect({kind:'notes',maxChars:1000000})).ndjson.split('\n').filter(Boolean).map(x=>JSON.parse(x)).filter(x=>x.kind==='notes');
 if(inspected.length!==d.slides || inspected.some(x=>!x.text.includes('TEACHING PURPOSE')))throw Error('Missing imported notes '+name);
 const changed=d.visible_edits.map(x=>x.slide);let flags=[];
 for(const num of changed){
  const slide=p.slides.items[num-1];const png=await p.export({slide,format:'png',scale:1});await fs.writeFile(`${work}/after-${num}.png`,new Uint8Array(await png.arrayBuffer()));
  const layout=JSON.parse(await (await slide.export({format:'layout'})).text());
  await fs.writeFile(`${work}/after-${num}.layout.json`,JSON.stringify(layout));
  for(const el of layout.elements){if(!el.text||!el.textLayout)continue;const sizes=(el.paragraphs||[]).map(x=>x.resolvedTextStyle?.fontSize).filter(Boolean);const font=sizes.length?Math.max(...sizes):(el.resolvedFontSize||0);const lines=el.textLayout.lineCount||1;if(font*lines*1.1>el.bbox[3]+3)flags.push({slide:num,text:el.text,font,lines,height:el.bbox[3]});}
 }
 if(changed.length){const old=await PresentationFile.importPptx(await FileBlob.load(`${base}/originals/${name}`));for(const num of changed){const png=await old.export({slide:old.slides.items[num-1],format:'png',scale:1});await fs.writeFile(`${work}/before-${num}.png`,new Uint8Array(await png.arrayBuffer()));}}
 report.push({path:d.path,imported_notes:d.slides,changed_rendered:changed,fit_flags:flags});await fs.writeFile(`${base}/validation-progress.json`,JSON.stringify(report,null,2));console.log(name+' OK; '+flags.length+' fit flags');
}
