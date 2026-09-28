/** Rebuild editable PPTX and PNG from layout.json using the installed Codex runtime. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
const modules=process.env.RUNTIME_NODE_MODULES;
if(!modules)throw new Error('Set RUNTIME_NODE_MODULES to the Codex runtime node_modules folder.');
const require=createRequire(path.join(modules,'package.json'));
const {Presentation,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(await fs.readFile(`${root}/source/layout.json`,'utf8'));
const p=Presentation.create({slideSize:{width:data.width,height:data.height}}),s=p.slides.add();s.background.fill='#FFFFFF';
for(const e of data.elements){
 const position={left:e.x,top:e.y,width:e.w,height:e.h,rotation:e.rot??0};
 if(e.kind==='image'){s.images.add({blob:await fs.readFile(path.join(root,e.file)),contentType:'image/png',position,fit:'contain',alt:e.name});continue;}
 const sh=s.shapes.add({name:e.name,geometry:e.kind==='rect'?(e.r?'roundRect':'rect'):'textbox',position,fill:e.kind==='rect'?e.color:'none',borderRadius:e.r??0,line:{fill:'none',width:0}});
 if(e.kind==='text'){sh.text=e.value;sh.text.style={typeface:e.font??'Arial',fontSize:e.size,bold:e.bold,color:e.color,autoFit:'none',wrap:'none',alignment:e.align??'left',verticalAlignment:'top',insets:{top:0,left:0,right:0,bottom:0}};}
}
s.speakerNotes.textFrame.setText(await fs.readFile(`${root}/source/SOURCES.md`,'utf8'));
const basename=process.argv[2]??'School_Track_Flyer_updated';if(!/^[\w-]+$/.test(basename))throw new Error('Use a plain filename without an extension.');
await (await PresentationFile.exportPptx(p)).save(`${root}/output/${basename}.pptx`);
const png=await p.export({slide:s,format:'png',scale:2});await fs.writeFile(`${root}/output/${basename}.png`,new Uint8Array(await png.arrayBuffer()));console.log(`Exported ${basename}.pptx and .png. Inspect both after editing.`);
