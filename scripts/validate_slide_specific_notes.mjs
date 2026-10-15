import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const runtime='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=runtime;
const {PresentationFile,FileBlob}=createRequire(`${runtime}/package.json`)('@oai/artifact-tool');
const skill='/Users/jothamwambi/.codex/plugins/cache/openai-primary-runtime/presentations/26.927.11222/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(`${skill}/container_tools/artifact_tool_utils.mjs`));
const base=path.resolve('review/2026-09-29/slide-specific-notes');
const rows=JSON.parse(await fs.readFile(`${base}/staged.json`,'utf8'));
await fs.mkdir(`${base}/validated`,{recursive:true});
for(const row of rows){
 const name=path.basename(row.path),work=`${base}/validation/${name.slice(0,-5)}`;
 await fs.mkdir(work,{recursive:true});
 const finalPath=`${base}/validated/${name}`;
 if(await fs.stat(finalPath).catch(()=>null)){
  const digest=createHash('sha256').update(await fs.readFile(finalPath)).digest('hex');
  if(digest===row.sha256){console.log('Validated earlier '+name);continue;}
  await fs.rename(finalPath,finalPath+'.previous');
  await fs.rename(`${work}/validation.json`,`${work}/validation.previous.json`);
 }
 await finalizePresentation({workspaceDir:process.cwd(),candidatePath:`${base}/candidates/${name}`,finalPath,
  explicitTotalSlideCount:row.slides,pythonExecutable:'/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
  integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,
  layoutArgs:[],verifyArtifactToolImport:true,receiptPath:`${work}/validation.json`});
 console.log('VALID '+name);
}
// Notes-only changes preserve every visual byte. Render representative originals
// and outputs to verify the note transplant did not affect their appearance.
for(const [name,nums] of [['CML3111_Week02_Engineering.pptx',[7,18]],['CML3112_Week03_Design_Infrastructure.pptx',[12,53]],['CML3112_Week11_Design_Infrastructure.pptx',[14]]]){
 for(const edition of ['originals','validated']){
  const p=await PresentationFile.importPptx(await FileBlob.load(`${base}/${edition}/${name}`));
  for(const n of nums){const png=await p.export({slide:p.slides.items[n-1],format:'png',scale:1});await fs.writeFile(`${base}/validation/${name.slice(0,-5)}/${edition}-${n}.png`,new Uint8Array(await png.arrayBuffer()));}
 }
}
