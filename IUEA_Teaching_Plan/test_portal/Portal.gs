/** Deploy in a SEPARATE Apps Script project, executing as the lecturer.
 * Only requestTestFiles is callable from the student page. Administrative
 * collector functions must never be placed in this public web-app project.
 */
var PORTAL_BOOK_ID = '1BveqLGvv-6C-00TMbUF0qti6VoEnAcRX9K1s9eja8uM';
var PORTAL_ALLOCATION_HEADERS = ['assessment_key','registration_normalized','email','allocation_code','variant','created_at','full_name','started_at','personal_deadline','notebook_id','window_opens_at'];
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
function requestTestFiles(input) {
 input=input||{};var key=String(input.test||'');
 if(!/^(CML3111|CML3112|CML3113)\|TEST[12]$/.test(key))throw Error('Use your lecturer’s test link.');
 var name=portalIdentity_(input.name,'full name',160),email=portalIdentity_(input.email,'Google-account email',254).toLowerCase(),reg=portalIdentity_(input.registration,'Student Registration Number',160);
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))throw Error('Enter the email of the Google account you will use in Colab and the submission form.');
 var normalized=reg.toUpperCase(),book=SpreadsheetApp.openById(PORTAL_BOOK_ID),w=portalWindow_(book,key);
 var lock=LockService.getScriptLock();if(!lock.tryLock(15000))throw Error('The page is busy. Wait a few seconds and try again.');
 var record;
 try {
  var sheet=book.getSheetByName('Test allocations');
  if(!sheet){sheet=book.insertSheet('Test allocations');sheet.appendRow(PORTAL_ALLOCATION_HEADERS);sheet.setFrozenRows(1);}
  if(w.minutes)sheet.getRange(1,1,1,PORTAL_ALLOCATION_HEADERS.length).setValues([PORTAL_ALLOCATION_HEADERS]);
  var rows=sheet.getDataRange().getValues().slice(1);
  record=rows.filter(function(r){return r[0]===key&&r[1]===normalized;})[0];
  if(record&&record[2]!==email)throw Error('These details do not match the earlier allocation. Use the same Google email and registration number, or ask your lecturer for help.');
  if(!record&&rows.some(function(r){return r[0]===key&&r[2]===email&&r[1]!==normalized;}))throw Error('This Google email already has an allocation. Use the same registration number, or ask your lecturer for help.');
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
   if(!isFinite(Date.parse(record[7]))||!isFinite(Date.parse(record[8])))throw Error('This test timer needs lecturer review.');
   if(Date.now()>Math.min(Date.parse(record[8]),Date.parse(w.close)))throw Error('This test has reached your personal deadline. Your timer cannot restart. Contact your lecturer.');
   sheet.getRange(rowNumber,1,1,PORTAL_ALLOCATION_HEADERS.length).setRichTextValues([record.map(function(v){return SpreadsheetApp.newRichTextValue().setText(String(v||'')).build();})]);
   record._row=rowNumber;
  }
 } finally {lock.releaseLock();}
 // Recheck the deadline after waiting for the allocation lock.
 w=portalWindow_(book,key);
 var packet=PORTAL_PACKETS[key+'|'+record[4]];if(!packet)throw Error('Files are unavailable. Tell the lecturer.');
 var nb=JSON.parse(packet.notebook),parts=key.split('|');
 if(w.minutes){name=record[6];reg=record[1];}
 nb.cells[1].source='FULL_NAME = '+JSON.stringify(name)+'\nEMAIL = '+JSON.stringify(email)+'\nSTUDENT_ID = '+JSON.stringify(reg)+'  # Your Student Registration Number\nCOHORT = '+JSON.stringify(parts[0])+'\nTEST_ID = '+JSON.stringify(parts[1])+'\n';
 var finalCell=nb.cells[nb.cells.length-1];finalCell.source='_IUEA_ALLOCATION = '+JSON.stringify(record[3])+'\nVARIANT = '+JSON.stringify(record[4])+'  # Internal file allocation; leave unchanged.\n'+(Array.isArray(finalCell.source)?finalCell.source.join(''):finalCell.source);
 nb.metadata.iuea_allocation_code=record[3];
 var instructions=packet.instructions,colabUrl='';
 if(w.minutes){
  var deadline=new Date(Math.min(Date.parse(record[8]),Date.parse(w.close))).toISOString();
  w.label=Utilities.formatDate(new Date(deadline),'Africa/Kampala','d MMM yyyy HH:mm:ss')+' Kampala time';
  instructions=portalTimedInstructions_(parts[0],w.label);
  nb.cells[0].source=instructions;
  nb.cells.forEach(function(cell){var text=Array.isArray(cell.source)?cell.source.join(''):cell.source;if(typeof text==='string'&&text.indexOf('invigilator')>=0)cell.source=text.replace(/invigilator/g,'lecturer');});
  nb.metadata.iuea_started_at=record[7];nb.metadata.iuea_deadline=deadline;
  // The data is part of this student's packet. Running setup restores the exact CSV, including after reconnecting.
  var setup=nb.cells[3],original=Array.isArray(setup.source)?setup.source.join(''):setup.source;
  setup.source='# Run this supplied setup cell. It loads your assigned CSV automatically.\nfrom pathlib import Path as _IueaPath\n_IueaPath("engineering_data.csv").write_text('+JSON.stringify(packet.csv)+', encoding="utf-8")\n'+original;
  setup.metadata=setup.metadata||{};setup.metadata.cellView='form';
  setup.source='#@title Load the supplied CSV and Python libraries\n'+setup.source;
  colabUrl=portalColabFile_(book,record,nb);
  portalWindow_(book,key);
  if(Date.now()>Date.parse(deadline))throw Error('This test has reached your personal deadline. Contact your lecturer.');
 }
 return {colabUrl:colabUrl,startedAt:record[7]||'',personalDeadline:w.minutes?deadline:'',serverNow:new Date().toISOString(),course:parts[0],test:parts[1],deadline:w.label,notebook:JSON.stringify(nb,null,1),notebookName:parts[1]+'_student.ipynb',csv:packet.csv,csvName:'engineering_data.csv',instructions:instructions};
}

function portalTimedInstructions_(course,deadline){
 return '# '+course+' TEST1 — Take-home practical test\n\nIndividual work • 100 marks • Three hours from Start test.\n\n**Your submission deadline: '+deadline+'.** Refreshing, changing devices or reopening Colab does not restart or pause the timer. The class closing time is the final cutoff.\n\n1. Open your issued notebook in Colab. Sign in with the Google email you entered. Choose File → Save a copy in Drive and work in that copy.\n2. Run the identity cell. Run **Load the supplied CSV and Python libraries**. It creates engineering_data.csv for you: no manual CSV upload is needed. Run it again after a runtime reset.\n3. Read each question and complete the supplied functions using pandas. Put your interpretation choices in DECISIONS. Leave supplied function names and identity details unchanged.\n4. Allow at least 20 minutes for checking and submission. Save and run your completed cells. Submit even if some tasks are unfinished.\n5. Run the final submission cell and click Submit test. Authorize your own Google account. Open the generated form, confirm the same account, check your details and press Submit BEFORE your personal deadline. The notebook button alone does not submit.\n\nThe timer includes setup, internet interruptions and submission. Colab may still let you edit after time expires, but late submissions are not accepted for grading. Contact your lecturer immediately about a technical problem.\n\nNo AI-generated solutions, collaboration, messaging or copied answers. Keep your snapshot unchanged until marks are released. A replacement must be submitted within the same personal deadline. No separate CSV, PDF or ZIP submission is needed.\n';
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
  var response=UrlFetchApp.fetch('https://www.googleapis.com/drive/v3/files/'+file.getId()+'/permissions?sendNotificationEmail=false',{method:'post',contentType:'application/json',headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},payload:JSON.stringify({type:'user',role:'reader',emailAddress:record[2]}),muteHttpExceptions:true});
  if(response.getResponseCode()!==200)throw Error('Files are unavailable in Colab. Contact your lecturer; your timer has started.');
  sheet.getRange(record._row,10).setValue(file.getId());
  return 'https://colab.research.google.com/drive/'+file.getId();
 }finally{lock.releaseLock();}
}
