/** Deploy in a SEPARATE Apps Script project, executing as the lecturer.
 * Only requestTestFiles is callable from the student page. Administrative
 * collector functions must never be placed in this public web-app project.
 */
var PORTAL_BOOK_ID = '1BveqLGvv-6C-00TMbUF0qti6VoEnAcRX9K1s9eja8uM';
var PORTAL_ALLOCATION_HEADERS = ['assessment_key','registration_normalized','email','allocation_code','variant','created_at','full_name','started_at','personal_deadline','notebook_id','window_opens_at','working_mode'];
function doGet(e) {
 var key=String((e&&e.parameter&&e.parameter.test)||'');
 if(!/^(CML3111|CML3112|CML3113)\|TEST[12]$/.test(key))return HtmlService.createHtmlOutput('Use the test link or QR code supplied by your lecturer.');
 var t=HtmlService.createTemplateFromFile('Index');t.testKey=key;
 return t.evaluate().setTitle(key.replace('|',' ')+' test files').addMetaTag('viewport','width=device-width, initial-scale=1');
}
function portalIdentity_(x,label,max) {
 x=String(x||'').trim();if(!x||x.length>max||/[\x00-\x1f\x7f]/.test(x))throw Error('Enter your '+label+'.');return x;
}
function portalWindow_(book,key) {
 var rows=book.getSheetByName('Test windows').getDataRange().getValues();
 var r=rows.slice(1).filter(function(r){return r[0]===key;})[0];var now=Date.now();
 if(!r||String(r[3]).toUpperCase()!=='YES'||!isFinite(Date.parse(r[1]))||!isFinite(Date.parse(r[2])))throw Error('This test is not open yet. Ask your lecturer for the start time.');
 if(now<Date.parse(r[1]))throw Error('This test opens on '+Utilities.formatDate(new Date(r[1]),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala time.');
 if(now>Date.parse(r[2]))throw Error('This test has closed. Tell your lecturer if you had a technical problem.');
 return {open:new Date(r[1]).toISOString(),close:new Date(r[2]).toISOString(),minutes:Number(r[4])||0,label:Utilities.formatDate(new Date(r[2]),'Africa/Kampala','d MMM yyyy HH:mm')+' Kampala time'};
}
function portalRegistrationKey_(value){return String(value||'').toUpperCase().replace(/\s+/g,'');}
// Read-only receipt check. Never modify an issued notebook, allocation or receipt.
function portalAssertNotSubmitted_(book,key,email,registration) {
 var sheet=book.getSheetByName('Collection');
 if(!sheet)throw Error('This test submission status is temporarily unavailable. Retry with the same details; your existing timer is unchanged.');
 var parts=key.split('|');
 var accepted=sheet.getDataRange().getValues().slice(1).some(function(r){
  return r[1]===parts[0]&&r[2]===parts[1]&&r[10]==='COLLECTED'&&
   (String(r[5]||'').trim().toLowerCase()===email||portalRegistrationKey_(r[6])===portalRegistrationKey_(registration));
 });
 if(accepted)throw Error('This test already has an accepted submission for these details. You cannot submit again or replace your work. Your original submission is retained. Contact your lecturer if a correction is needed.');
}
function requestTestFiles(input) {
 input=input||{};var key=String(input.test||'');
 if(!/^(CML3111|CML3112|CML3113)\|TEST[12]$/.test(key))throw Error('Use your lecturer’s test link.');
 var name=portalIdentity_(input.name,'full name',160),email=portalIdentity_(input.email,'Google-account email',254).toLowerCase(),reg=portalIdentity_(input.registration,'Student ID/ Registration Number',160);
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))throw Error('Enter the email of the Google account you will use in Colab and the submission form.');
 var normalized=reg.toUpperCase(),book=SpreadsheetApp.openById(PORTAL_BOOK_ID),w=portalWindow_(book,key);
 var lock=LockService.getScriptLock();if(!lock.tryLock(15000))throw Error('The page is busy. Wait a few seconds and try again.');
 var record,resumed=false;
 try {
  portalAssertNotSubmitted_(book,key,email,normalized);
  var sheet=book.getSheetByName('Test allocations');
  if(!sheet){sheet=book.insertSheet('Test allocations');sheet.appendRow(PORTAL_ALLOCATION_HEADERS);sheet.setFrozenRows(1);}
  if(w.minutes)sheet.getRange(1,1,1,PORTAL_ALLOCATION_HEADERS.length).setValues([PORTAL_ALLOCATION_HEADERS]);
  var rows=sheet.getDataRange().getValues().slice(1);
  var matching=rows.filter(function(r){return r[0]===key&&portalRegistrationKey_(r[1])===portalRegistrationKey_(normalized);});
  if(matching.length>1)throw Error('These details match more than one allocation. Ask your lecturer for help.');
  record=matching[0];resumed=!!(record&&record[7]);
  if(record&&record[2]!==email)throw Error('These details do not match the earlier allocation. Use the same Google email and registration number, or ask your lecturer for help.');
  if(!record&&rows.some(function(r){return r[0]===key&&r[2]===email&&portalRegistrationKey_(r[1])!==portalRegistrationKey_(normalized);}))throw Error('This Google email already has a test in progress or an earlier allocation. Enter the registration number used when you first started. Spaces and letter case do not matter. If its digits or programme letters differ, ask your lecturer to correct the original record; do not start with another email.');
  if(!record){
   var counts={A:0,B:0,C:0};rows.filter(function(r){return r[0]===key;}).forEach(function(r){if(r[4] in counts)counts[r[4]]++;});
   var lowest=Math.min(counts.A,counts.B,counts.C),choices=Object.keys(counts).filter(function(k){return counts[k]===lowest;});
   var variant=choices[Math.floor(Math.random()*choices.length)],token='T-'+Utilities.getUuid();
   record=[key,normalized,email,token,variant,new Date().toISOString()];
   // RichTextValue stores freeform registration text literally, including leading =.
   sheet.getRange(sheet.getLastRow()+1,1,1,6).setRichTextValues([record.map(function(v){return SpreadsheetApp.newRichTextValue().setText(String(v)).build();})]);
  }
  if(w.minutes){
   var rowNumber=rows.findIndex(function(r){return r[0]===key&&r[3]===record[3];})+2;
   if(rowNumber===1)rowNumber=sheet.getLastRow();
   // Older rehearsal allocations have no timer. Their first take-home start is recorded once.
   if(!record[7]){record[6]=name;record[7]=new Date().toISOString();record[8]=new Date(Math.min(Date.now()+w.minutes*60000,Date.parse(w.close))).toISOString();record[9]='';record[10]=w.open;}
   if(!record[9])record[11]='DIRECT';
   if(record[11]===undefined)record[11]='COPY';
   if(!isFinite(Date.parse(record[7]))||!isFinite(Date.parse(record[8])))throw Error('This test timer needs lecturer review.');
   if(Date.now()>Math.min(Date.parse(record[8]),Date.parse(w.close)))throw Error('This test has reached your personal deadline. Submission is closed and your timer cannot restart. Contact your lecturer if you experienced a technical problem.');
   sheet.getRange(rowNumber,1,1,PORTAL_ALLOCATION_HEADERS.length).setRichTextValues([record.map(function(v){return SpreadsheetApp.newRichTextValue().setText(String(v||'')).build();})]);
   record._row=rowNumber;
  }
 } finally {lock.releaseLock();}
 // Recheck the deadline after waiting for the allocation lock.
 w=portalWindow_(book,key);
 var packet=PORTAL_PACKETS[key+'|'+record[4]];if(!packet)throw Error('Files are unavailable. Tell the lecturer.');
 var nb=JSON.parse(packet.notebook),parts=key.split('|');
 if(w.minutes){name=record[6];reg=record[1];}
 nb.cells[1].source='# Do not edit this cell: identifies your attempt and preserves your timer.\nFULL_NAME = '+JSON.stringify(name)+'\nEMAIL = '+JSON.stringify(email)+'\n_IUEA_ALLOCATED_EMAIL = '+JSON.stringify(email)+'\nSTUDENT_ID = '+JSON.stringify(reg)+'  # Your Student ID/ Registration Number\nCOHORT = '+JSON.stringify(parts[0])+'\nTEST_ID = '+JSON.stringify(parts[1])+'\n';
 var finalCell=nb.cells[nb.cells.length-1];finalCell.source='# Do not edit this cell: links your saved answers to your test attempt.\n_IUEA_ALLOCATION = '+JSON.stringify(record[3])+'\nVARIANT = '+JSON.stringify(record[4])+'  # Internal file allocation; leave unchanged.\n'+(Array.isArray(finalCell.source)?finalCell.source.join(''):finalCell.source);
 nb.metadata.iuea_allocation_code=record[3];
 nb.metadata.iuea_allocated_email=email;
 var instructions=packet.instructions,colabUrl='';
 if(w.minutes){
  var deadline=new Date(Math.min(Date.parse(record[8]),Date.parse(w.close))).toISOString();
  w.label=Utilities.formatDate(new Date(deadline),'Africa/Kampala','d MMM yyyy HH:mm:ss')+' Kampala time';
  instructions=portalTimedInstructions_(parts[0],w.label);
  if(record[11]==='DIRECT')instructions=instructions.replace('then **File → Save a copy in Drive**. Work in this saved copy, not the read-only original.','and work in that private editable notebook. You do not need to make a copy.').replace('To resume your work, reopen your saved copy from Google Drive; opening the original again does not recover your answers.','To resume, reopen the entry link or QR code with the same email and registration number, then click Resume my test in Colab. This opens the same notebook and its saved answers. Save regularly; unsaved changes lost before a shutdown cannot be recovered by the portal.');
  var codingGuide=packet.instructions.indexOf('## Coding tasks and time plan');
  if(codingGuide>=0)instructions+='\n\n'+packet.instructions.slice(codingGuide);
  if(/^2026\.10-test1-(coding-v3|notebook-v4)$/.test(nb.metadata.iuea_exam_version)&&record[11]==='DIRECT'){
   instructions=packet.instructions.replace('**Individual work · 100 marks · 3 hours from Start test**','**Individual work · 100 marks · Deadline: '+w.label+'**');
  }
  nb.cells[0].source=instructions;
  nb.cells.forEach(function(cell){var text=Array.isArray(cell.source)?cell.source.join(''):cell.source;if(typeof text==='string'&&text.indexOf('invigilator')>=0)cell.source=text.replace(/invigilator/g,'lecturer');});
  nb.metadata.iuea_started_at=record[7];nb.metadata.iuea_deadline=deadline;
  nb.cells.forEach(function(cell){if((cell.metadata&&cell.metadata.tags||[]).indexOf('iuea-submission')>=0){var source=Array.isArray(cell.source)?cell.source.join(''):cell.source;cell.source=source.replace('\n','\n_IUEA_DEADLINE = '+JSON.stringify(deadline)+' # Do not edit: fixed submission deadline.\n');}});
  nb.cells[1].source='#@title Check details and countdown — Do not edit this cell\n'+nb.cells[1].source+'print("Name:", FULL_NAME)\nprint("Student ID/ Registration Number:", STUDENT_ID)\nprint("Email:", EMAIL)\n'+portalCountdownCode_(deadline);
  nb.cells[1].metadata=nb.cells[1].metadata||{};
  nb.cells[1].metadata.tags=['iuea-timer','autograde-skip'];
  nb.cells[1].metadata.cellView='form';
  // The data is part of this student's packet. Running setup restores the exact CSV, including after reconnecting.
  var setup=nb.cells[3],original=Array.isArray(setup.source)?setup.source.join(''):setup.source;
  setup.source='#@title Prepare CSV and libraries — Do not edit this cell\n# Do not edit this cell: restores your assigned CSV and loads the libraries.\nwith open("engineering_data.csv", "w", encoding="utf-8") as _csv_file:\n    _csv_file.write('+JSON.stringify(packet.csv)+')\n'+original;
  setup.metadata=setup.metadata||{};setup.metadata.cellView='form';

  colabUrl=portalColabFile_(book,record,nb);
  portalWindow_(book,key);
  if(Date.now()>Date.parse(deadline))throw Error('This test has reached your personal deadline. Contact your lecturer.');
 }
 return {resumed:resumed,workingMode:record[11]||'COPY',colabUrl:colabUrl,startedAt:record[7]||'',personalDeadline:w.minutes?deadline:'',serverNow:new Date().toISOString(),course:parts[0],test:parts[1],deadline:w.label,notebook:JSON.stringify(nb,null,1),notebookName:parts[1]+'_student.ipynb',csv:packet.csv,csvName:'engineering_data.csv',instructions:instructions};
}

function portalTimedInstructions_(course,deadline){
 return "# __COURSE__ TEST1 — Take-home practical test\n\nIndividual work • 100 marks • Up to three hours from **Start test**.\n\n__DEADLINE__\nThe timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the class closing time. Colab may still allow editing afterwards, but late work is not accepted for grading.\n\n## 1. Open your own working copy\nOn the entry page, enter your full name, Google account email and Student ID/ Registration Number. Use that same Google account throughout. Click **Open my test in Colab**, then **File → Save a copy in Drive**. Work in this saved copy, not the read-only original. Click **Connect** if shown. To resume your work, reopen your saved copy from Google Drive; opening the original again does not recover your answers.\n\n## 2. Load the data\nCheck the identity cell near the top. Tell your lecturer immediately if the details are wrong; do not change the supplied course, test or allocation settings. Run the first code cell using the triangle beside it to check your details and display the countdown. Rerun it if the countdown is not visible after reopening; it always uses the original deadline. Then run **Load the supplied CSV and Python libraries**. In the issued notebook this creates `engineering_data.csv` automatically; no separate CSV upload is needed. Wait for the preview and row count. After a runtime reset, rerun these setup cells before your work. If using a backup notebook without an embedded CSV setup cell, upload your assigned `engineering_data.csv` through Colab's folder icon first.\n\n## 3. Complete the questions\nWork from top to bottom. Read each question, write your code in its code cell and run it. Keep supplied function names and required output formats unchanged. Use pandas as instructed. Complete the eight coding tasks using pandas, matplotlib and ordinary Python. There are no multiple-choice answers or written report. Use the task time estimates and leave at least 20 minutes to submit. Save regularly using **File → Save**.\n\n## 4. Submit — allow at least 20 minutes\n1. Run your completed cells, check the results and save. Submit your completed work even if some questions are unfinished.\n2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.\n3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.\n4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student ID/ Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.\n5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.\n\n**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. Marks are calculated after the test. One submission only per Google account and Student ID/ Registration Number for this test. Double-check your work and identity details before submitting. You cannot edit or replace a submitted response; contact your lecturer for any correction.\n\n## If something fails\nRecord the error and contact your lecturer immediately, before the deadline. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun setup; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.\n\n**Permitted resources:** Your lecture slides, revision guide, cheatsheet and personal course notes. Use your assigned CSV and write the code yourself.\n\n**No AI or outside help:** Do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your test answers. Do not obtain answers from another person, collaborate, or copy someone else’s work.\n\n**Understanding check:** You may be asked to explain your submitted code or make a small change without AI or another person’s help.\n\n**Declaration:** By submitting, I confirm that I completed this test myself without AI assistance or another person’s help, using only the permitted resources. I can explain and modify the code I submitted.\n".replace('__COURSE__',course).replace('__DEADLINE__','**Your submission deadline: '+deadline+'.**');
}
function portalColabFile_(book,record,notebook){
 // Serialize creation so repeated clicks never generate a new timer or a second issued file.
 var lock=LockService.getScriptLock();if(!lock.tryLock(15000))throw Error('The page is busy. Retry with the same details. Your timer is already running.');
 try{
  var sheet=book.getSheetByName('Test allocations'),saved=sheet.getRange(record._row,1,1,PORTAL_ALLOCATION_HEADERS.length).getValues()[0];
  if(saved[3]!==record[3])throw Error('Files are unavailable. Contact your lecturer.');
  if(saved[9])return 'https://colab.research.google.com/drive/'+saved[9];
  var props=PropertiesService.getScriptProperties(),folderId=props.getProperty('PORTAL_NOTEBOOK_FOLDER');
  if(!folderId){folderId=DriveApp.createFolder('IUEA private issued test notebooks').getId();props.setProperty('PORTAL_NOTEBOOK_FOLDER',folderId);}
  var file=DriveApp.getFolderById(folderId).createFile(Utilities.newBlob(JSON.stringify(notebook,null,1),'application/vnd.google.colaboratory',record[0].replace('|','_')+'_student.ipynb'));
  var response=UrlFetchApp.fetch('https://www.googleapis.com/drive/v3/files/'+file.getId()+'/permissions?sendNotificationEmail=false',{method:'post',contentType:'application/json',headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},payload:JSON.stringify({type:'user',role:record[11]==='DIRECT'?'writer':'reader',emailAddress:record[2]}),muteHttpExceptions:true});
  if(response.getResponseCode()!==200)throw Error('Files are unavailable in Colab. Contact your lecturer; your timer has started.');
  var sharing=UrlFetchApp.fetch('https://www.googleapis.com/drive/v3/files/'+file.getId(),{method:'patch',contentType:'application/json',headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},payload:JSON.stringify({writersCanShare:false}),muteHttpExceptions:true});
  if(sharing.getResponseCode()!==200)throw Error('Files are unavailable. Contact your lecturer; your timer has started.');
  sheet.getRange(record._row,10).setValue(file.getId());
  return 'https://colab.research.google.com/drive/'+file.getId();
 }finally{lock.releaseLock();}
}

function portalCountdownCode_(deadline){return "\n# This display is a reminder. The lecturer's server enforces the original deadline.\nfrom IPython.display import HTML as _TimerHTML, display as _timer_display\n_timer_display(_TimerHTML(\"\"\"<div style=\"border:2px solid #126573;padding:14px;font:18px Arial\"><strong>Test countdown</strong><p class=\"iuea-clock\"></p><p class=\"iuea-reminder\"></p><p>Deadline: __LOCAL_DEADLINE__ (Kampala time). Save regularly and finish the submission form before time expires. This clock uses your device time; the entry page and server determine your deadline.</p></div><script>(function(){const box=document.currentScript.previousElementSibling;const end=Date.parse('__DEADLINE__');function tick(){const remaining=Math.max(0,end-Date.now());const n=Math.ceil(remaining/1000);box.querySelector('.iuea-clock').textContent=remaining?Math.floor(n/3600)+'h '+Math.floor(n%3600/60)+'m '+n%60+'s remaining':'Time has ended. Late submissions are not accepted.';const reminder=box.querySelector('.iuea-reminder');if(reminder)reminder.textContent=remaining>0&&remaining<=20*60000?'20 minutes or less remain: save and complete the submission form now.':'';}tick();const interval=setInterval(function(){if(!box.isConnected){clearInterval(interval);return;}tick();},1000);})();</script>\"\"\"))\n".replace(/__DEADLINE__/g,deadline).replace('__LOCAL_DEADLINE__',Utilities.formatDate(new Date(deadline),'Africa/Kampala','d MMM yyyy HH:mm:ss'));}
