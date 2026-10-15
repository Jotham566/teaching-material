import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {Presentation,PresentationFile,FileBlob}=require('@oai/artifact-tool');
const base=path.resolve('review/2026-09-29/slide-specific-notes');
const plans=JSON.parse(await fs.readFile(`${base}/notes-plan.json`,'utf8'));
await fs.mkdir(`${base}/authored`,{recursive:true});
// Notes carriers author native notes without reflowing the original artwork.
for(const d of plans){
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 for(const s of d.slides){if(!s.notes)throw Error('Missing notes');p.slides.add().speakerNotes.textFrame.setText(s.notes);}
 await(await PresentationFile.exportPptx(p)).save(`${base}/authored/${path.basename(d.path)}`);
 console.log(path.basename(d.path));
}
