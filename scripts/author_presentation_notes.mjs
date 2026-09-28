// Artifact Tool authors speaker-note XML. Original deck artwork stays untouched.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {Presentation,PresentationFile}=require('@oai/artifact-tool');
const base='review/2026-09-21/presentation-notes';
const plan=JSON.parse(await fs.readFile(`${base}/notes-plan.json`,'utf8'));
await fs.mkdir(`${base}/authored`,{recursive:true});
const changed=process.argv.includes('--changed-only')?JSON.parse(await fs.readFile(`${base}/changed-note-decks.json`,'utf8')):null;
for(const d of plan){
 if(changed && !changed.includes(d.path))continue;
 if(process.argv.includes('--projects-only') && !/CML.*Week(08|15)/.test(d.path))continue;
 const dest=`${base}/authored/${path.basename(d.path)}`;
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 for(const s of d.slides){const slide=p.slides.add();slide.speakerNotes.textFrame.setText(s.notes);}
 await (await PresentationFile.exportPptx(p)).save(dest);
 console.log(path.basename(dest));
}
