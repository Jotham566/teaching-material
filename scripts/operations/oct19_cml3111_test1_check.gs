// User-requested submission check. Re-running does not extend the same window.
function openCML3111Test1SubmissionCheckOct19(){
 var c=examConfig_(),key='CML3111|TEST1',props=PropertiesService.getScriptProperties();
 var prop='CML3111_TEST1_CHECK_20261019',saved=props.getProperty(prop),w;
 if(saved){w=JSON.parse(saved);}else{var now=new Date();w={open:now.toISOString(),close:new Date(now.getTime()+3600000).toISOString()};}
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
