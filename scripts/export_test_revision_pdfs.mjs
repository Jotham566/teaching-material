/** Export canonical decks with the bundled office converter before packaging. */
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const soffice='/Users/jothamwambi/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/soffice';
const profile=await fs.mkdtemp(path.join(os.tmpdir(),'iuea-pdf-'));
const staging=path.join(root,'review/2026-10-19/revision-pdfs');
await fs.mkdir(staging,{recursive:true});
const decks=JSON.parse(await fs.readFile('data/iuea_deck_content.json','utf8')).filter(d=>[7,14].includes(d.week) && (!process.argv.includes("--test2-only") || d.week===14));
execFileSync(soffice,['-env:UserInstallation='+pathToFileURL(profile).href,'--headless','--convert-to','pdf','--outdir',staging,...decks.map(d=>path.join(root,'IUEA_Teaching_Plan/decks',d.filename))],{stdio:'inherit',timeout:240000});
for(const d of decks){
 const name=d.filename.replace(/\.pptx$/,'.pdf');
 const dir=path.join(root,'IUEA_Teaching_Plan/test_revision',d.cohort,d.week===7?'Test1':'Test2');
 await fs.copyFile(path.join(staging,name),path.join(dir,name));
 console.log(name+' exported');
}
