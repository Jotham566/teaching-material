/** Install in the QUIZ project. Share scheduling metadata with the private exporter. */
function publishCAQuizWindows(){
 var book=SpreadsheetApp.openById('1FxAVXwSvLEd7TEd3pJ2E0_ka7Mp6ZM6pW1yNsXKWdm4');
 var sheet=book.getSheetByName('CA Quiz windows')||book.insertSheet('CA Quiz windows');
 sheet.getRange('E1').setValue('SYNCING');
 var links=loadLinks_(),now=new Date().toISOString(),rows=[['key','window_json','verified_at']];
 Object.keys(links).filter(function(k){return /^CML311[123]\|[1-5]$/.test(k);}).sort().forEach(function(k){var r=links[k];rows.push([k,JSON.stringify({openedAt:r.openedAt,closeAt:r.closeAt,formId:r.formId}),now]);});
 if(rows.length!==16)throw Error('Expected 15 quiz windows');
 sheet.getRange(1,1,rows.length,3).setValues(rows);sheet.getRange('E1').setValue('OK');
 Logger.log('Published 15 quiz windows for private CA exports; no responses or marks changed.');
}
function installCAQuizWindowMirror(){
 publishCAQuizWindows();
 if(!ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='publishCAQuizWindows';}))ScriptApp.newTrigger('publishCAQuizWindows').timeBased().everyMinutes(15).create();
}
