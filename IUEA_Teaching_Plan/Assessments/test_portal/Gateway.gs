/** Server-to-server entry only. Keep PORTAL_GATEWAY_KEY in Script Properties. */
function doPost(e) {
 var reply;
 try {
  var raw=e&&e.postData&&e.postData.contents;
  if(!raw||raw.length>8192)throw Error('Invalid request.');
  var request=JSON.parse(raw);
  var expected=PropertiesService.getScriptProperties().getProperty('PORTAL_GATEWAY_KEY');
  if(!expected||expected.length<32||request.secret!==expected)return gatewayJson_({ok:false,error:'Portal connection unavailable. Tell your lecturer.'});
  // Reuse the same window checks, stable allocation and student packets.
  reply={ok:true,result:requestTestFiles(request.input)};
 } catch(error) {
  var message=String(error.message||'');
  var safe=/^(This test |Enter |Use your lecturer|These details |This Google email |The page is busy|Files are unavailable)/.test(message);
  reply={ok:false,error:safe?message:'Could not prepare files. Tell your lecturer.'};
 }
 return gatewayJson_(reply);
}
function gatewayJson_(value) {
 return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}
