// User-requested submission check. Re-running does not extend the same window.
function openCML3111Test1CloudflareCheckOct19(){
 var c=examConfig_(),key='CML3111|TEST1',props=PropertiesService.getScriptProperties();
 var prop='CML3111_TEST1_CLOUDFLARE_CHECK_20261019',saved=props.getProperty(prop),w;
 if(saved){w=JSON.parse(saved);}else{w={open:'2026-10-19T14:26:54.000Z',close:'2026-10-19T15:26:54.000Z'};}
 if(Date.now()>Date.parse(w.close))throw Error('This rehearsal opening has expired. Do not reopen without a new instruction.');
 var sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows');
 var rows=sheet.getDataRange().getValues(),idx=rows.findIndex(function(r){return r[0]===key;});
 if(idx<1)throw Error('Test window not found');
 console.log('PREVIOUS '+JSON.stringify(rows[idx]));
 sheet.getRange(idx+1,2,1,3).setNumberFormat('@').setValues([[w.open,w.close,'YES']]);
 props.setProperty(prop,JSON.stringify(w));
 var f=FormApp.openById(c.forms[key].formId);examFormInstructions_(f,{open:w.open,close:w.close,enabled:true});f.setAcceptingResponses(true);
 console.log('OPEN '+Utilities.formatDate(new Date(w.open),'Africa/Kampala','d MMM yyyy HH:mm:ss')+' CLOSE '+Utilities.formatDate(new Date(w.close),'Africa/Kampala','d MMM yyyy HH:mm:ss')+' accepting='+f.isAcceptingResponses());
 console.log(f.getPublishedUrl());
}

// Export only the explicitly labelled synthetic attempt; exclude it from real marks.
function exportCloudflareRehearsalOct19(){
 if(!syncColabExams())throw Error('Collection busy; retry shortly.');
 var c=examConfig_(),sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Collection'),rows=sheet.getDataRange().getValues();
 var matches=rows.map(function(r,i){return {r:r,i:i};}).filter(function(x){return x.r[1]==='CML3111'&&x.r[2]==='TEST1'&&x.r[4]==='REHEARSAL — Cloudflare submission check'&&x.r[5]==='jothammartin.wambi@gmail.com'&&x.r[6]==='DEMO / portal'&&Date.parse(x.r[7])>=Date.parse('2026-10-19T14:26:54Z');});
 if(matches.length!==1)throw Error('Expected exactly one Cloudflare rehearsal; found '+matches.length);
 var x=matches[0],r=x.r;
 if(r[10]!=='COLLECTED'&&r[10]!=='REHEARSAL')throw Error('Rehearsal collection status: '+r[10]+' '+r[14]);
 var name=r[0]+'.ipynb',job={response_id:r[0],cohort:r[1],assessment:r[2],variant:r[3],full_name:r[4],email:r[5],email_verified:true,student_registration_number:r[6],submitted_at:r[7],opens_at:r[8],closes_at:r[9],notebook_sha256:r[12],file:name};
 var blobs=[DriveApp.getFileById(r[11]).getBlob().setName(name),Utilities.newBlob(JSON.stringify({schema:1,exported_at:new Date().toISOString(),jobs:[job],collection_issues:[]},null,2),'application/json','manifest.json')];
 var zip=DriveApp.getFolderById(c.folderId).createFile(Utilities.zip(blobs,'Cloudflare-rehearsal-20261019.zip'));
 sheet.getRange(x.i+1,11).setValue('REHEARSAL');
 console.log('REHEARSAL collected; verified identity and snapshot; excluded from student exports.');
 console.log('DOWNLOAD https://drive.google.com/file/d/'+zip.getId()+'/view');
}
