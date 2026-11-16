"""Build the deployment bundle that lets the Test 1 machinery run the project sitting: python3 tools/build_deploy_bundle.py

Writes Project/deploy/ (the live files in test_portal/ and grader/ are NOT touched; every output is a patched COPY, each patch asserts its match count):
  Portal.gs                  test_portal/Portal.gs with the ML_PROJECT key, the project packets and the project instructions
  PacketsMLProject.gs        the 3 course notebooks for the 9 packet keys (3 courses x allocation labels A, B, C, which the portal still draws;
                             every label gets the same notebook) and the data block once. No keys, no solutions, no separate CSV.
  Index.html                 test_portal/Index.html with the project heading, the window and project wording (no CSV download for the project)
  gateway/page.mjs           the same page for the Cloudflare gateway (generated exactly as scripts/build_test_gateway.py does)
  gateway/worker.mjs         test_portal/gateway/worker.mjs accepting the ML_PROJECT key
  exam_collection.gs         grader/exam_collection.gs with the ML_PROJECT key in authoriseFreshTestAttempt and the project wording on the form
  test_monitor.gs            grader/test_monitor.gs with ML_PROJECT in the monitor
  ml_project_collection.gs   NEW: installMlProjectCollection() creates the three forms and the Test windows rows (duration 180)
  Test_windows_rows.csv      the three Test windows rows for the confirmed window (23 to 25 November 2026), ready to type; enabled NO
Run build_project_notebooks.py first. For the release run it with --require-forms (after the forms exist), then this script again.
The gateway reads at most 4 MiB from Apps Script; the issued notebook is about 0.5 MB, so it fits.
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import project_content as PC  # noqa: E402
import project_contracts as K  # noqa: E402
import project_numpy_reference as P  # noqa: E402

PLAN = PC.PLAN
DEPLOY = PC.PROJECT / 'deploy'
ROOT = PLAN.parent
KEY_OLD = r'/^(CML3111|CML3112|CML3113)\|TEST[12]$/'
KEY_NEW = r'/^(CML3111|CML3112|CML3113)\|(TEST[12]|ML_PROJECT)$/'


def sub(text, old, new, count=1):
    if text.count(old) == 0 and new in text:      # already patched (setup_pipeline.sh copies the patched gateway back): leave it
        return text
    assert text.count(old) == count, f'expected {count} match(es), found {text.count(old)}: {old[:80]!r}'
    return text.replace(old, new)


def instructions_js():
    """The first cell of every issued project and rehearsal notebook, as the portal inserts it: the notebook's own intro (one text, so the
    two never disagree) with the student's deadline under the heading."""
    import build_project_notebooks as BN
    texts = {f'{c}|{t}': BN.intro_cell(c, 'rehearsal' if t == 'ML_REHEARSAL' else 'student', True, deadline_slot=True)
             for c in PC.CODES for t in ('ML_PROJECT', 'ML_REHEARSAL')}
    return ('var PORTAL_ML_INSTRUCTIONS = ' + json.dumps(texts, ensure_ascii=False, indent=1) + ';\n'
            'function portalMlInstructions_(course,deadline,test){\n test=test||\'ML_PROJECT\';\n'
            " return PORTAL_ML_INSTRUCTIONS[course+'|'+test].replace('__DEADLINE__',test==='ML_REHEARSAL'?'**Practice deadline (nothing is locked): '+deadline+'.**':'**Your submission deadline: '+deadline+'.**');\n}\n")

PORTAL_PIPELINE_JS = r'''
// ---------------------------------------------------------------- ML project pipeline (13 November 2026)
// The class list: a sheet "Class list" in the same workbook, columns cohort | registration | full_name (paste it from the gradebook roster).
// No token (collection design of 14 November 2026): the issued notebook is a Drive file shared with the student's Google account as an
// editor; the collector stops editing and collects it at the deadline. The allocation code links the automatic backups to the attempt.
var PORTAL_REG_FORMAT=/^\d{2}\/[A-Z0-9]{1,8}(\/[A-Z0-9]{1,8}){1,3}(-[A-Z0-9]{1,4})?$/;
function portalRegNormal_(value){return String(value||'').toUpperCase().replace(/\s+/g,'');}
// No mixing of programmes (lecturer, 15 November 2026). Each course belongs to set programmes, read from the class list of 14 November 2026.
// The programme code is the last part of the registration number, before any -S/-J (24/351/BSCE-S -> BSCE).
var PORTAL_DEMO_REGISTRATIONS=['26/SMOKE/001/TEST','26/DEMO/001/LECTURER'];
var PORTAL_PROGRAMMES={BSEE:'CML3111',BSMRE:'CML3111',BSCE:'CML3112',BARC:'CML3112',BSME:'CML3113',BSPE:'CML3113',BPE:'CML3113'};
function portalProgramme_(reg){var parts=String(reg).split('/');return parts[parts.length-1].replace(/-.*$/,'');}
// Open entry (lecturer, 14 November 2026): nobody is refused for not being on the class list. The registration must match a sensible
// pattern (Test 1 normalisation: upper case, spaces removed). On the list: the student confirms the name. Not on the list: the student types
// the full name, starts normally and is graded like anyone else; the collector flags NOT_ON_LIST (information only).
function portalClassEntry_(book,key,registration,typedName){
 var reg=portalRegNormal_(registration),course=String(key).split('|')[0];
 if(!reg)throw Error('Enter your registration number.');
 if(!PORTAL_REG_FORMAT.test(reg))throw Error('Enter your registration number as it is on your student card, for example 24/351/BSCE-S.');
 // The rehearsal is the lecturer's, run live in the revision class (lecturer, 16 November 2026): only the demo numbers open it, in any course.
 // The demo numbers never open the real project.
 var demo=PORTAL_DEMO_REGISTRATIONS.indexOf(reg)>=0;
 if(String(key).split('|')[1]==='ML_REHEARSAL'){
  if(!demo)throw Error('This registration number cannot open the rehearsal: your lecturer runs it in class. Your project opens on Monday 23 November 2026.');
  return {registration:reg,name:'Lecturer demo',course:course,onList:true};
 }
 if(demo)throw Error('This registration number is for practice only. Enter your own registration number.');
 var sheet=book.getSheetByName('Class list');
 var rows=sheet?sheet.getDataRange().getValues().slice(1).filter(function(r){return portalRegNormal_(r[1])===reg;}):[];
 var here=rows.filter(function(r){return String(r[0]).trim().toUpperCase()===course;})[0];
 if(here)return {registration:String(here[1]).trim(),name:String(here[2]).trim(),course:course,onList:true};
 // 1. On another course's class list: refused. 2. Not on any list: the programme code must belong to the chosen course; an unknown code is
 // refused so the lecturer can add the student to the right list. The page shows these messages and offers the right course.
 if(rows.length)throw Error('This registration number is on the '+String(rows[0][0]).trim().toUpperCase()+' class list, not '+course+'. Choose '+String(rows[0][0]).trim().toUpperCase()+' as your course.');
 var programme=portalProgramme_(reg),owner=PORTAL_PROGRAMMES[programme];
 if(!owner)throw Error('This registration number ('+programme+') does not match any of the three courses. Message your lecturer on the class channel to be added to the right class list.');
 if(owner!==course)throw Error('This registration number is for '+programme+', which takes '+owner+', not '+course+'. Choose '+owner+' as your course.');
 var name=String(typedName||'').trim();
 if(typedName!==undefined&&(name.length<3||name.length>160||/[\x00-\x1f\x7f]/.test(name)||name==='(class list)'))throw Error('Enter your full name: your registration number is not on the class list.');
 return {registration:String(registration).trim().toUpperCase(),name:name,course:course,onList:false};
}
// The identity goes into the ONE supplied cell (the setup cell): the line _IUEA_IDENTITY = {...} is replaced. The countdown and the backup read it.
function portalMlFill_(nb,record,email,deadline,parts){
 var cell=nb.cells[1],src=Array.isArray(cell.source)?cell.source.join(''):cell.source;
 if(src.indexOf('# IUEA-SETUP-CELL')<0)throw Error('Files are unavailable. Tell the lecturer.');
 var ident={name:String(record[6]||''),registration:String(record[1]),email:email,course:parts[0],test:parts[1],allocation:String(record[3]),deadline:deadline};
 cell.source=src.replace(/^_IUEA_IDENTITY = .*$/m,function(){return '_IUEA_IDENTITY = '+JSON.stringify(ident);});
 cell.metadata=cell.metadata||{};cell.metadata.cellView='form';
 // The deadline in plain text at the top, visible before anything runs (lecturer, 16 November 2026).
 var intro=nb.cells[0],text=Array.isArray(intro.source)?intro.source.join(''):intro.source,when=Utilities.formatDate(new Date(deadline),'Africa/Kampala','EEEE d MMMM yyyy, HH:mm');
 intro.source=text.replace(/\n/,'\n**'+(parts[1]==='ML_REHEARSAL'?'Practice deadline (nothing is locked)':'Your deadline')+': '+when+' Kampala time.**\n');
}
function portalNameHint_(name){
 var words=String(name||'').trim().split(/\s+/).filter(String);
 return words.length?words[0]+(words.length>1?' '+words.slice(1).map(function(w){return w.charAt(0).toUpperCase()+'.';}).join(' '):''):'';
}
/** Called by the entry page while the student types (through the gateway). Read only. */
function portalCheckRegistration(input){
 input=input||{};var key=String(input.test||'');
 if(!/^(CML3111|CML3112|CML3113)\|ML_(PROJECT|REHEARSAL)$/.test(key))throw Error('Use your lecturer’s test link.');
 var entry=portalClassEntry_(SpreadsheetApp.openById(PORTAL_BOOK_ID),key,input.registration);
 return {registration:entry.registration,nameHint:entry.onList?portalNameHint_(entry.name):'',onList:entry.onList,course:entry.course};
}
// The countdown for the ML project and its rehearsal: Ctrl+S reminders 30 and 10 minutes before the deadline. Information only:
// at the deadline the collector stops editing on the server (the rehearsal is never stopped).
function portalMlCountdownCode_(deadline,test){
 var rehearsal=test==='ML_REHEARSAL';
 var html='<div style="border:2px solid #126573;padding:14px;font:18px Arial"><strong>'+(rehearsal?'Rehearsal countdown (practice only)':'Project countdown')+'</strong><p class="iuea-clock"></p><p class="iuea-reminder" style="font-weight:bold;color:#9f251e"></p>'+
  '<p>Deadline: __LOCAL_DEADLINE__ (Kampala time). There is no Submit button: your notebook saves itself and is collected at your deadline. Press Ctrl+S now and then.'+(rehearsal?' In the rehearsal your editing is never stopped.':' At the deadline your editing stops.')+' This clock uses your device time; the server decides.</p></div>'+
  '<script>(function(){const box=document.currentScript.previousElementSibling;const end=Date.parse("__DEADLINE__");function tick(){const left=Math.max(0,end-Date.now());const n=Math.ceil(left/1000);'+
  'box.querySelector(".iuea-clock").textContent=left?Math.floor(n/3600)+"h "+Math.floor(n%3600/60)+"m "+n%60+"s left":"Time has ended. Your work has been collected.";'+
  'const r=box.querySelector(".iuea-reminder");r.textContent=left>0&&left<=10*60000?"10 minutes or less left: press Ctrl+S now.":(left>0&&left<=30*60000?"30 minutes or less left: press Ctrl+S now.":"");}'+
  'tick();const t=setInterval(function(){if(!box.isConnected){clearInterval(t);return;}tick();},1000);})();</script>';
 return "\n# This display is a reminder. The lecturer's server keeps your deadline.\nfrom IPython.display import HTML as _TimerHTML, display as _timer_display\n_timer_display(_TimerHTML("+JSON.stringify(html.replace(/__DEADLINE__/g,deadline).replace('__LOCAL_DEADLINE__',Utilities.formatDate(new Date(deadline),'Africa/Kampala','d MMM yyyy HH:mm:ss')))+"))\n";
}
'''

GATEWAY_ROUTES = r''' // ML project collection (14 November 2026): the class-list check while typing, the silent backups from Colab, and the entry page's
 // Check my work, I have finished and status. The allocation code (issued once, unguessable) identifies the attempt; no token.
 if(['/api/check','/api/backup','/api/mywork','/api/finish','/api/status','/api/fixemail'].includes(url.pathname)){
  if(request.method!=='POST')return json({ok:false,error:'Use POST.'},405);
  if(!(request.headers.get('Content-Type')||'').startsWith('application/json'))return json({ok:false,error:'Invalid request.'},415);
  // Backups come from Colab's Python, which sends no Origin. Everything else comes from the entry page itself (same origin only).
  if(url.pathname!=='/api/backup'&&request.headers.get('Origin')!==url.origin)return json({ok:false,error:'Open your lecturer’s test page and try again.'},403);
  let body;
  try{body=JSON.parse(await limitedText(request,url.pathname==='/api/backup'?12*1024*1024:4096));}catch{return json({ok:false,error:'The request is too large or not readable.'},400);}
  const attempt=typeof body.attempt==='string'&&/^T-[A-Za-z0-9-]{8,64}$/.test(body.attempt)?body.attempt:'';
  let target,payload;
  if(url.pathname==='/api/check'){
   if(!projectKeyPattern.test(String(body.test||''))||typeof body.registration!=='string'||!body.registration.trim()||body.registration.length>40||/[\x00-\x1f\x7f]/.test(body.registration))return json({ok:false,error:'Enter your registration number.'},400);
   if(!env.PORTAL_GATEWAY_KEY||env.PORTAL_GATEWAY_KEY.length<32)return json({ok:false,error:'Portal connection unavailable. Tell your lecturer.'},503);
   target=env.APPS_SCRIPT_URL;payload={secret:env.PORTAL_GATEWAY_KEY,action:'check',input:{test:body.test,registration:body.registration.trim()}};
  }else{
   if(!env.COLLECTOR_GATEWAY_KEY||env.COLLECTOR_GATEWAY_KEY.length<32||!env.COLLECTOR_URL)return json({ok:false,error:'The collection service is unavailable. Tell your lecturer.'},503);
   if(!attempt)return json({ok:false,error:'Open your project from the entry page first.'},400);
   const action={'/api/backup':'backup','/api/mywork':'checkwork','/api/finish':'finish','/api/status':'status','/api/fixemail':'fixemail'}[url.pathname];
   if(action==='fixemail'&&!(typeof body.new_email==='string'&&body.new_email.length<=254&&/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.new_email.trim())))return json({ok:false,error:'Enter the Google email you are signed into in Colab.'},400);
   if(action==='backup'&&(typeof body.notebook!=='string'||typeof body.href!=='string'||body.href.length>500))return json({ok:false,error:'Invalid backup.'},400);
   payload={secret:env.COLLECTOR_GATEWAY_KEY,action,attempt};
   if(action==='backup'){payload.notebook=body.notebook;payload.href=body.href;}
   if(action==='fixemail')payload.new_email=body.new_email.trim();
   target=env.COLLECTOR_URL;
  }
  try{
   const backend=new URL(target);
   if(backend.origin!=='https://script.google.com'||!/^\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(backend.pathname)||backend.search)throw Error();
   const response=await upstream(backend.href,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),redirect:'follow',signal:AbortSignal.timeout(28000)});
   if(!response.ok)throw Error();
   const data=JSON.parse(await limitedText(response,64*1024));
   if(data.ok===true&&data.result&&typeof data.result==='object')return json({ok:true,result:data.result});
   if(data.ok===false&&typeof data.error==='string')return json({ok:false,error:data.error,result:data.result&&typeof data.result==='object'?data.result:undefined},409);
   throw Error();
  }catch{return json({ok:false,error:'The connection could not complete. Try again in a minute. If it continues, tell your lecturer.'},502);}
 }
'''


def patch_portal():
    s = (PLAN / 'test_portal/Portal.gs').read_text()
    KEYS = r'(TEST1|ML_PROJECT|ML_REHEARSAL)'
    # The live portal (4 November 2026) accepts TEST1 only. Add the project and its rehearsal to both gates.
    s = sub(s, r"if(!/^(CML3111|CML3112|CML3113)\|TEST1$/.test(key))return HtmlService.createHtmlOutput('Use the Test 1 link supplied by your lecturer.');",
            r"if(!/^(CML3111|CML3112|CML3113)\|" + KEYS + r"$/.test(key))return HtmlService.createHtmlOutput('Use the test link or QR code supplied by your lecturer.');")
    s = sub(s, r"if(!/^(CML3111|CML3112|CML3113)\|TEST1$/.test(key))throw Error('Use the Test 1 link supplied by your lecturer.');",
            r"if(!/^(CML3111|CML3112|CML3113)\|" + KEYS + r"$/.test(key))throw Error('Use your lecturer’s test link.');"
            # the class list decides the name and the registration (as typed, checked against the list)
            r"if(/\|ML_(PROJECT|REHEARSAL)$/.test(key)){var classEntry=portalClassEntry_(SpreadsheetApp.openById(PORTAL_BOOK_ID),key,input.registration,String(input.name||''));input={test:key,name:classEntry.name,email:input.email,registration:classEntry.registration};}")
    s = sub(s, "var packet=PORTAL_PACKETS[key+'|'+record[4]];if(!packet)", "var packet=PORTAL_PACKETS[key+'|'+record[4]]||(typeof PORTAL_PACKETS_ML!=='undefined'?PORTAL_PACKETS_ML[key+'|'+record[4]]:undefined);if(!packet)")
    s = sub(s, "var nb=JSON.parse(packet.notebook),parts=key.split('|');",
            "var nb=JSON.parse(packet.notebook),parts=key.split('|');if(packet.data){var si=/^ML_/.test(parts[1])?1:3,packed=Array.isArray(nb.cells[si].source)?nb.cells[si].source.join(''):nb.cells[si].source;nb.cells[si].source=packed.replace('__IUEA_PACKED_DATA__',packet.data);}")
    # the project has ONE supplied cell (the setup cell, position 1): none of the Test 1 cell edits apply to it
    s = sub(s, " nb.cells[1].source='# Do not edit this cell: identifies your attempt", " if(!/^ML_/.test(parts[1]))nb.cells[1].source='# Do not edit this cell: identifies your attempt")
    s = sub(s, "finalCell.source='# Do not edit this cell: links your saved answers", "if(!/^ML_/.test(parts[1]))finalCell.source='# Do not edit this cell: links your saved answers")
    s = sub(s, "  nb.metadata.iuea_started_at=record[7];nb.metadata.iuea_deadline=deadline;\n", "  nb.metadata.iuea_started_at=record[7];nb.metadata.iuea_deadline=deadline;\n  if(/^ML_/.test(parts[1])){portalMlFill_(nb,record,email,deadline,parts);}else{\n")
    s = sub(s, "  setup.metadata=setup.metadata||{};setup.metadata.cellView='form';\n", "  setup.metadata=setup.metadata||{};setup.metadata.cellView='form';\n  }\n")
    s = sub(s, "  nb.cells[0].source=instructions;\n", "  if(/^ML_/.test(parts[1])){instructions=portalMlInstructions_(parts[0],w.label,parts[1]);}else nb.cells[0].source=instructions;\n")
    s = sub(s, "+portalCountdownCode_(deadline);", "+(/^ML_/.test(parts[1])?portalMlCountdownCode_(deadline,parts[1]):portalCountdownCode_(deadline));")
    # the rehearsal is never closed by the personal deadline (practice only)
    s = sub(s, "if(Date.now()>Math.min(Date.parse(record[8]),Date.parse(w.close)))throw Error(", "if(!/\\|ML_REHEARSAL$/.test(key)&&Date.now()>Math.min(Date.parse(record[8]),Date.parse(w.close)))throw Error(")
    s = sub(s, "if(Date.now()>Date.parse(deadline))throw Error(", "if(!/\\|ML_REHEARSAL$/.test(key)&&Date.now()>Date.parse(deadline))throw Error(")
    # the Drive copy is named by registration and allocation; the entry page receives the allocation code (for Check my work and I have finished)
    s = sub(s, "record[0].replace('|','_')+'_student.ipynb'", "(/\\|ML_/.test(record[0])?record[0].replace('|','_')+'_'+String(record[1]).replace(/[^A-Za-z0-9]+/g,'-')+'_'+record[3]+'.ipynb':record[0].replace('|','_')+'_student.ipynb')")
    s = sub(s, "return {resumed:resumed,", "return {attempt:/\\|ML_/.test(key)?record[3]:'',resumed:resumed,")
    s = sub(s, "var t=HtmlService.createTemplateFromFile('Index');", "var t=HtmlService.createTemplateFromFile(/\\|ML_/.test(key)?'ProjectIndex':'Index');")
    s = sub(s, "  portalAssertNotSubmitted_(book,key,email,normalized);", "  if(!/\\|ML_/.test(key))portalAssertNotSubmitted_(book,key,email,normalized);   // the project collects at the deadline; returning resumes the same file")
    s = s.rstrip('\n') + '\n\n' + instructions_js() + PORTAL_PIPELINE_JS
    (DEPLOY / 'Portal.gs').write_text(s)


def patch_index():
    s = (PLAN / 'test_portal/Index.html').read_text()
    s = sub(s, "document.getElementById('heading').textContent=testKey.replace('|TEST',' — Test ');",
            "document.getElementById('heading').textContent=testKey.replace('|ML_PROJECT',': Engineering ML project (online, 3 hours)').replace('|TEST',' — Test ');")
    windows = ',\n'.join(f" '{c}|ML_PROJECT':'{PC.WINDOW['opens']} to {PC.WINDOW['closes']}; start by 20:59 on 25 November for the full 3 hours'" for c in PC.CODES)
    s = sub(s, "'CML3112|TEST1':'27 October 2026, 7:00 PM – 2 November 2026, 11:59 PM'\n};", "'CML3112|TEST1':'27 October 2026, 7:00 PM – 2 November 2026, 11:59 PM',\n" + windows + "\n};")
    s = sub(s, "Keep the requested answer names unchanged. Only Task 7 of Test 1 requires a function.</li>", 'Keep the requested answer names unchanged.<span id="test1Only"> Only Task 7 of Test 1 requires a function.</span></li>')
    s = sub(s, "document.getElementById('dataStep').textContent='Run Check details and countdown near the top (if present), then Prepare CSV and libraries. This creates engineering_data.csv automatically. For Test 1, write your own pandas code to read it into raw_data in Task 1. Rerun the countdown and setup after a runtime reset. The countdown does not pause or extend your deadline; older copies without it can use the timer on this page.';",
            "document.getElementById('dataStep').textContent=testKey.endsWith('|ML_PROJECT')?'Run Check details and countdown near the top, then Prepare the data and the libraries. The data file is stored inside that cell and is written out for you: no upload or download is needed. Rerun both after a runtime reset. The countdown does not pause or extend your deadline.':'Run Check details and countdown near the top (if present), then Prepare CSV and libraries. This creates engineering_data.csv automatically. For Test 1, write your own pandas code to read it into raw_data in Task 1. Rerun the countdown and setup after a runtime reset. The countdown does not pause or extend your deadline; older copies without it can use the timer on this page.';")
    s = sub(s, "if(windows[testKey]){document.getElementById('takehome').hidden=false;",
            "if(testKey.endsWith('|ML_PROJECT')){document.getElementById('test1Only').hidden=true;document.getElementById('csv').hidden=true;document.querySelector('.brand').textContent='IUEA • ENGINEERING ML PROJECT';}\nif(windows[testKey]){document.getElementById('takehome').hidden=false;")
    (DEPLOY / 'Index.html').write_text(s)
    # the Cloudflare gateway page: the same transformation as scripts/build_test_gateway.py
    page = s.replace('<base target="_top">', '')
    page = sub(page, '<?!= JSON.stringify(testKey) ?>', '__TEST_KEY_JSON__')
    gateway_src = (ROOT / 'scripts/build_test_gateway.py').read_text()
    marker = "page=page.replace(\"let objectUrls=[];\",'''"
    start = gateway_src.index(marker)
    end = gateway_src.index("(portal/'gateway/page.mjs')")
    transform = gateway_src[start:end]
    scope = {'page': page}
    exec(transform, scope)       # the identical replacements, then the assertion that no Google RPC call is left
    (DEPLOY / 'gateway').mkdir(exist_ok=True)
    (DEPLOY / 'gateway/page.mjs').write_text('// Generated by tools/build_deploy_bundle.py from deploy/Index.html (same transformation as scripts/build_test_gateway.py).\nexport default ' +
                                             json.dumps(scope['page'], ensure_ascii=False) + ';\n')
    w = (PLAN / 'test_portal/gateway/worker.mjs').read_text()
    w = sub(w, r'const keyPattern=/^CML311[123]\|TEST1$/;', r'const keyPattern=/^CML311[123]\|(TEST1|ML_PROJECT|ML_REHEARSAL)$/;')
    w = sub(w, "import page from './page.mjs';", "import page from './page.mjs';\nimport projectPage from './project_page.mjs';\nconst projectKeyPattern=/^CML311[123]\\|ML_(PROJECT|REHEARSAL)$/;")
    w = sub(w, "page.replace('__TEST_KEY_JSON__',JSON.stringify(key))", "(projectKeyPattern.test(key)?projectPage:page).replace('__TEST_KEY_JSON__',JSON.stringify(key))")
    w = sub(w, " if(url.pathname!=='/api/files')return json({ok:false,error:'Page not found.'},404);", GATEWAY_ROUTES.rstrip('\n') + "\n if(url.pathname!=='/api/files')return json({ok:false,error:'Page not found.'},404);")
    template = (HERE / 'project_index.template.html').read_text().replace('__WINDOW__', f"{PC.WINDOW['opens']} to {PC.WINDOW['closes']}").replace('__LAST_START__', PC.WINDOW['last_full_start'])
    (DEPLOY / 'ProjectIndex.html').write_text(template.replace('__TEST_KEY_JSON__', '<?!= JSON.stringify(testKey) ?>'))
    (DEPLOY / 'gateway/project_page.mjs').write_text('// Generated by tools/build_deploy_bundle.py from tools/project_index.template.html.\nexport default ' +
                                                     json.dumps(template.replace('<base target="_top">', ''), ensure_ascii=False) + ';\n')
    (DEPLOY / 'gateway/worker.mjs').write_text(w)
    g = (PLAN / 'test_portal/Gateway.gs').read_text()
    g = sub(g, "reply={ok:true,result:requestTestFiles(request.input)};", "reply={ok:true,result:request.action==='check'?portalCheckRegistration(request.input):requestTestFiles(request.input)};")
    g = sub(g, "var safe=/^(This test |Enter |Use your lecturer|These details |This Google email |The page is busy|Files are unavailable)/.test(message);",
            "var safe=/^(This test |This registration |You are listed in |Enter |Use your lecturer|These details |This Google email |The page is busy|Files are unavailable)/.test(message);")
    (DEPLOY / 'Gateway.gs').write_text(g)


def patch_collector():
    s = (PLAN / 'grader/exam_collection.gs').read_text()
    s = sub(s, r"if(!/^CML311[123]\|TEST[12]$/.test(key))throw Error('Use an assessment key such as CML3111|TEST1.');",
            r"if(!/^CML311[123]\|(TEST[12]|ML_PROJECT)$/.test(key))throw Error('Use an assessment key such as CML3111|TEST1 or CML3112|ML_PROJECT.');")
    s = sub(s, "text+='\\n\\nTAKE-HOME TEST: '+w.minutes", "text+='\\n\\n'+(/ML_PROJECT/.test(form.getTitle())?'TIMED ONLINE PROJECT':'TAKE-HOME TEST')+': '+w.minutes")
    (DEPLOY / 'exam_collection.gs').write_text(s)
    m = (PLAN / 'grader/test_monitor.gs').read_text()
    m = sub(m, r"if(!/^CML311[123]\|TEST[12]$/.test(a[0])", r"if(!/^CML311[123]\|(TEST[12]|ML_PROJECT)$/.test(a[0])")
    m = sub(m, "['TEST1','TEST2'].forEach(function(test){", "['TEST1','TEST2','ML_PROJECT'].forEach(function(test){")
    (DEPLOY / 'test_monitor.gs').write_text(m)


NEW_COLLECTION = r'''/** Add this file to the lecturer-owned collector project (the one that holds exam_collection.gs), AFTER replacing exam_collection.gs with deploy/exam_collection.gs.
 * Creates the three ML_PROJECT Test windows rows with duration_minutes=180. Nothing is opened: every row is created with enabled NO and empty times.
 * The project has no Google Form: notebooks arrive through the submission web app (deploy/ml_project_pipeline.gs). Run installMlProjectCollection() once.
 */
var ML_PROJECT_MINUTES = 180;
function installMlProjectCollection(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_();
  if(!c.bookId)throw Error('Run installColabExamCollection first: the collector workbook does not exist yet.');
  var windows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows');
  if(!windows)throw Error('The Test windows sheet is missing.');
  var have=windows.getDataRange().getValues().map(function(r){return r[0];}),created=[];
  ['CML3111','CML3112','CML3113'].forEach(function(cohort){
   var key=cohort+'|ML_PROJECT';if(have.indexOf(key)>=0)return;
   windows.appendRow([key,'','','NO',ML_PROJECT_MINUTES]);created.push(key);
  });
  console.log('Test windows rows created: '+(created.join(', ')||'none (all three already existed)')+'. Every row is enabled NO. Nothing was opened.');
  console.log('Collector workbook id (BOOK_ID for the submission web app): '+c.bookId);
 }finally{lock.releaseLock();}
}
/** Read only. Logs the three ML_PROJECT Test windows rows so you can check the typed times and the duration. */
function showMlProjectWindows(){
 var c=examConfig_(),rows=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows').getDataRange().getValues();
 rows.slice(1).filter(function(r){return /\|ML_PROJECT$/.test(r[0]);}).forEach(function(r){console.log(r[0]+' | opens '+r[1]+' | closes '+r[2]+' | enabled '+r[3]+' | minutes '+r[4]);});
}
/** Sets one project window. Run ONLY after you have confirmed the date with the students. confirm must be the word CONFIRMED.
 * The confirmed window (13 November 2026) is the same for all three courses:
 * setMlProjectWindow('CML3112','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED'), then CML3113 and CML3111, then run syncColabExams. */
function setMlProjectWindow(cohort,opensIso,closesIso,confirm){
 if(confirm!=='CONFIRMED')throw Error('Pass CONFIRMED as the fourth argument once the date is confirmed.');
 var key=String(cohort)+'|ML_PROJECT';
 if(!/^CML311[123]\|ML_PROJECT$/.test(key))throw Error('Use CML3111, CML3112 or CML3113.');
 if(!isFinite(Date.parse(opensIso))||!isFinite(Date.parse(closesIso))||Date.parse(closesIso)<=Date.parse(opensIso))throw Error('Use real dates with the Kampala offset, closing after opening.');
 if(Date.parse(closesIso)-Date.parse(opensIso)>72*3600000)throw Error('The window is more than 72 hours. The project window is 23 November 00:00 to 25 November 23:59.');
 if(Date.parse(closesIso)-Date.parse(opensIso)<ML_PROJECT_MINUTES*60000)throw Error('The window is shorter than 3 hours.');
 var c=examConfig_(),sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows'),rows=sheet.getDataRange().getValues();
 var at=rows.findIndex(function(r,i){return i>0&&r[0]===key;});
 if(at<0)throw Error('No Test windows row for '+key+'. Run installMlProjectCollection first.');
 sheet.getRange(at+1,1,1,5).setValues([[key,opensIso,closesIso,'YES',ML_PROJECT_MINUTES]]);
 console.log('Window set for '+key+': '+opensIso+' to '+closesIso+', '+ML_PROJECT_MINUTES+' minutes. Run syncColabExams to open the form.');
}
'''


REHEARSAL_OPENS = {'CML3112': '2026-11-17T08:00:00+03:00', 'CML3113': '2026-11-20T08:00:00+03:00', 'CML3111': '2026-11-20T08:00:00+03:00'}
REHEARSAL_CLOSES = '2026-11-22T23:59:00+03:00'


def build_packets():
    """One notebook per course and per kind (the project, ML_PROJECT, and its rehearsal, ML_REHEARSAL) for the three allocation labels A, B
    and C. The data block of the setup cell is stored once and put back by the portal, so the file stays small."""
    sources = {'ML_PROJECT': 'Notebooks/{code}/ML_PROJECT_student.ipynb', 'ML_REHEARSAL': 'Rehearsal/{code}/ML_PROJECT_rehearsal.ipynb'}
    packed = PC.packed_data()
    lines = ['// Generated from student files only (tools/build_deploy_bundle.py). Never add answer keys.',
             '// The data block of the setup cell is stored once (ML_PROJECT_DATA); the portal puts it back into cell 3 of the issued notebook.',
             'var ML_PROJECT_DATA = ' + json.dumps(packed) + ';', 'var ML_PROJECT_NOTEBOOKS = {};', 'var PORTAL_PACKETS_ML = {};']
    packets = {}
    for test, pattern in sources.items():
        for code in PC.CODES:
            nb = json.loads((PC.PROJECT / pattern.format(code=code)).read_text())
            assert '# IUEA-SETUP-CELL' in ''.join(nb['cells'][1]['source']), 'cell 1 must be the one supplied setup cell (the portal edits it by position)'
            assert sum('# IUEA-SETUP-CELL' in ''.join(c['source']) for c in nb['cells']) == 1, 'exactly one supplied cell'
            assert not any('iuea-submission' in c.get('metadata', {}).get('tags', []) for c in nb['cells']), 'no Submit cell any more'
            cell1 = ''.join(nb['cells'][1]['source'])
            assert cell1.count(packed) == 1, 'the setup cell must hold the data block once'
            light = json.loads(json.dumps(nb))
            light['cells'][1]['source'] = cell1.replace(packed, '__IUEA_PACKED_DATA__')
            lines.append(f'ML_PROJECT_NOTEBOOKS[{json.dumps(code + "|" + test)}] = ' + json.dumps(json.dumps(light, ensure_ascii=False), ensure_ascii=False) + ';')
            if test == 'ML_PROJECT':
                instructions = (f'{code} ML_PROJECT: Engineering ML project, 3 hours from Start. The window {PC.WINDOW_TEXT}.\n'
                                'Individual work. No AI. Run the countdown and setup cells, do Tasks 1 to 7, Restart session and run all, press Ctrl+S. '
                                'No Submit button: your work is collected at your deadline.\n')
            else:
                instructions = (f'{code} ML_REHEARSAL: unmarked rehearsal of the Engineering ML project. Same steps: Start, work in the notebook that opens, '
                                'then Check my work and I have finished on the entry page. Nothing is locked or marked.\n')
            for v in ('A', 'B', 'C'):
                key = f'{code}|{test}|{v}'
                lines.append(f'PORTAL_PACKETS_ML[{json.dumps(key)}] = {{notebook: ML_PROJECT_NOTEBOOKS[{json.dumps(code + "|" + test)}], data: ML_PROJECT_DATA, csv: "", instructions: {json.dumps(instructions)}}};')
                packets[key] = instructions
    (DEPLOY / 'PacketsMLProject.gs').write_text('\n'.join(lines) + '\n')
    return packets


def links_and_qr():
    """The three entry links (same Cloudflare host as Tests 1 and 2) and their QR codes, built exactly as scripts/configure_test_portal.py builds them."""
    from urllib.parse import urlencode
    sys.path.insert(0, str(ROOT / 'scripts'))
    import qrgen
    config = json.loads((ROOT / 'data/test_portal_config.json').read_text())
    public = config['public_url'].rstrip('/') + '/'
    qrdir = DEPLOY / 'qr'
    qrdir.mkdir(exist_ok=True)
    lines = ['# ML_PROJECT entry links (the same host as Practical Test 1)', '',
             f'Share these with the rehearsal (after Class 3) and again before the window. The window {PC.WINDOW_TEXT}, the same for all three courses. The page releases nothing before the Test windows row is enabled and open.', '',
             '| Course | Window | Entry link |', '|---|---|---|']
    for c in PC.CODES:
        url = public + '?' + urlencode({'test': c + '|ML_PROJECT'})
        qrgen.png(url, qrdir / f'{c}_ML_PROJECT.png', ec='M', module_px=12, quiet=4)
        lines.append(f'| {c} | {PC.WINDOW["opens"]} to {PC.WINDOW["closes"]} | [{url}]({url}) |')
    lines += ['', '## Rehearsal links (unmarked, never locked)', '', '| Course | Rehearsal entry link |', '|---|---|']
    for c in PC.CODES:
        url = public + '?' + urlencode({'test': c + '|ML_REHEARSAL'})
        lines.append(f'| {c} | [{url}]({url}) |')
    (DEPLOY / 'ML_PROJECT_ENTRY_LINKS.md').write_text('\n'.join(lines) + '\n')


def main():
    DEPLOY.mkdir(exist_ok=True)
    patch_portal()
    patch_index()
    patch_collector()
    (DEPLOY / 'ml_project_collection.gs').write_text(NEW_COLLECTION)
    packets = build_packets()
    with (DEPLOY / 'Test_windows_rows.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['assessment_key', 'opens_at', 'closes_at', 'enabled', 'duration_minutes', 'note'])
        for c in PC.CODES:
            w.writerow([f'{c}|ML_PROJECT', PC.WINDOW['iso_open'], PC.WINDOW['iso_close'], 'NO', PC.MINUTES, 'window confirmed 13 November 2026; set enabled to YES before 23 November 00:00'])
        for c in PC.CODES:
            w.writerow([f'{c}|ML_REHEARSAL', REHEARSAL_OPENS[c], REHEARSAL_CLOSES, 'NO', PC.MINUTES, 'rehearsal: never locked, never marked; set enabled to YES on the revision class day'])
    links_and_qr()
    print('deploy bundle written to', DEPLOY, '-', len(packets), 'packets')


if __name__ == '__main__':
    main()
