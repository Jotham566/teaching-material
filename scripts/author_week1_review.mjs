import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire('/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {Presentation,PresentationFile}=require('@oai/artifact-tool');
const dir='review/2026-10-20/full-course-review';
await fs.mkdir(dir+'/authored',{recursive:true});
for(const d of JSON.parse(await fs.readFile(dir+'/week1-review-plan.json','utf8'))){
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 for(const s of d.slides)p.slides.add().speakerNotes.textFrame.setText(s.notes);
 await(await PresentationFile.exportPptx(p)).save(dir+'/authored/'+d.filename);
}
