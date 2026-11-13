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
    assert text.count(old) == count, f'expected {count} match(es), found {text.count(old)}: {old[:80]!r}'
    return text.replace(old, new)


def instructions_js():
    """The project's student instructions as the portal inserts them (cell 0 of every issued notebook)."""
    text = f'''# __COURSE__ Engineering ML project: online, 3 hours

Individual work • Part A 30 marks and Part B 15 marks (45 marks, scaled to 40 percent of the course) • Up to three hours from **Start test**.

__DEADLINE__
The timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the window's close ({PC.WINDOW['closes']} Kampala time). Colab may still allow editing afterwards, but late work is not accepted for grading.

## 1. Work in your private notebook
Click **Open my test in Colab** on the entry page and use the same Google account throughout. This is your own private, editable notebook: work in it directly. Click **Connect** if shown. To resume after a closed tab or a shutdown, reopen the entry link with the same email and registration number and click Resume my test in Colab. Save regularly with **File, then Save**: only saved work can be recovered.

## 2. Load the data
Check the identity cell near the top. Tell your lecturer at once on the class channel if the details are wrong; do not change the supplied course, test or allocation settings. Run the first code cell using the triangle beside it to check your details and display the countdown. Then run **Prepare the data and the libraries**. The steel plant data file is stored inside that cell and is written out for you: no upload or download is needed. After a runtime reset, rerun these two cells before your work.

Data: {P.CITATION}

## 3. Complete the tasks
Work from top to bottom. Tasks 1 to 7 are coded functions and results (Task 6 uses the supplied model-choice rule); Task 8 is the Part B memo form (a dictionary called `MEMO`). Keep supplied function names, variable names and required output formats unchanged. {PC.OWN_CELLS} The self-check cells are not marked. Everything is marked automatically by the lecturer's computer, on other rows you cannot see. Use the time plan in the notebook and leave at least 20 minutes to submit.

## 4. Submit: allow at least 20 minutes
1. Choose **Runtime, then Restart session and run all**. Every cell must run without an error. Save.
2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.
3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.
4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student ID/ Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.
5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.

**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. One submission only per Google account and Student ID/ Registration Number. You cannot edit or replace a submitted response; contact your lecturer for any correction.

## If something fails
Report it at once on the class channel, with a screenshot. The lecturer answers on the channel {PC.SUPPORT_HOURS.split(' (')[0]}. The lecturer can authorise one fresh attempt; it still ends at the window's close. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun the setup cells; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.

**Permitted resources:** Your lecture slides, your lab notebooks from Classes 1 to 3, the revision guide, cheatsheet and personal course notes. Write the code yourself.

**No AI or outside help:** Do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not obtain answers from another person, collaborate, or copy someone else's work.

**Understanding check:** After the window, any student may be asked, in an online call, to explain their submitted code or make a small change, without AI or another person's help. The copy checks and the identity checks run on every notebook.

**Declaration:** By submitting, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and modify the code I submitted.
'''
    return ('function portalMlInstructions_(course,deadline){\n return ' + json.dumps(text, ensure_ascii=False) +
            ".replace('__COURSE__',course).replace('__DEADLINE__','**Your submission deadline: '+deadline+'.**');\n}\n")


def patch_portal():
    s = (PLAN / 'test_portal/Portal.gs').read_text()
    # The live portal (4 November 2026) accepts TEST1 only and answers TEST2 with a withdrawal message. Add ML_PROJECT to both TEST1 gates.
    s = sub(s, r"if(!/^(CML3111|CML3112|CML3113)\|TEST1$/.test(key))return HtmlService.createHtmlOutput('Use the Test 1 link supplied by your lecturer.');",
            r"if(!/^(CML3111|CML3112|CML3113)\|(TEST1|ML_PROJECT)$/.test(key))return HtmlService.createHtmlOutput('Use the test link or QR code supplied by your lecturer.');")
    s = sub(s, r"if(!/^(CML3111|CML3112|CML3113)\|TEST1$/.test(key))throw Error('Use the Test 1 link supplied by your lecturer.');",
            r"if(!/^(CML3111|CML3112|CML3113)\|(TEST1|ML_PROJECT)$/.test(key))throw Error('Use your lecturer’s test link.');")
    s = sub(s, "var packet=PORTAL_PACKETS[key+'|'+record[4]];if(!packet)", "var packet=PORTAL_PACKETS[key+'|'+record[4]]||(typeof PORTAL_PACKETS_ML!=='undefined'?PORTAL_PACKETS_ML[key+'|'+record[4]]:undefined);if(!packet)")
    s = sub(s, "var nb=JSON.parse(packet.notebook),parts=key.split('|');",
            "var nb=JSON.parse(packet.notebook),parts=key.split('|');if(packet.data){var packed=Array.isArray(nb.cells[3].source)?nb.cells[3].source.join(''):nb.cells[3].source;nb.cells[3].source=packed.replace('__IUEA_PACKED_DATA__',packet.data);}")
    s = sub(s, "  nb.cells[0].source=instructions;\n", "  if(parts[1]==='ML_PROJECT'){instructions=portalMlInstructions_(parts[0],w.label);}\n  nb.cells[0].source=instructions;\n")
    s = s.rstrip('\n') + '\n\n' + instructions_js()
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
    w = sub(w, r'const keyPattern=/^CML311[123]\|TEST1$/;', r'const keyPattern=/^CML311[123]\|(TEST1|ML_PROJECT)$/;')
    (DEPLOY / 'gateway/worker.mjs').write_text(w)


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
 * Creates the three ML_PROJECT submission forms exactly as installColabExamCollection created the Test 1 and Test 2 forms, and the three Test windows rows
 * with duration_minutes=180. Nothing is opened: every row is created with enabled NO and empty times. Run installMlProjectCollection() once.
 */
var ML_PROJECT_MINUTES = 180;
function installMlProjectCollection(){
 var lock=LockService.getScriptLock();lock.waitLock(30000);
 try{
  var c=examConfig_();
  if(!c.bookId||!c.folderId)throw Error('Run installColabExamCollection first: the collector workbook does not exist yet.');
  c.forms=c.forms||{};
  var book=SpreadsheetApp.openById(c.bookId);
  var windows=book.getSheetByName('Test windows');
  if(!windows)throw Error('The Test windows sheet is missing.');
  var created=[];
  ['CML3111','CML3112','CML3113'].forEach(function(cohort){
   var key=cohort+'|ML_PROJECT';
   if(c.forms[key])return;
   var form=FormApp.create(cohort+' ML_PROJECT — Colab test submission');
   form.setDescription('Use the Submit test button at the end of your issued Colab notebook. It prepares the fields below. Sign in with the same Google account used in Colab. Submit before your personal deadline. Your exact notebook snapshot is copied to the lecturer’s private folder. No download or file upload is required.');
   form.setCollectEmail(true).setLimitOneResponsePerUser(true).setAllowResponseEdits(false);
   var names=['Full name','Student Registration Number','Variant','Snapshot file ID','Snapshot SHA-256'];var items={};
   names.forEach(function(name){var item=form.addTextItem().setTitle(name).setRequired(true);if(name==='Student Registration Number')item.clearValidation().setHelpText('Enter your own registration number exactly as on your university record. Any format is accepted.');items[name]=item.getId();});
   form.setConfirmationMessage('Your response has been recorded. The lecturer’s system will verify and collect the notebook snapshot. Keep your snapshot in Drive until grades are released. If the button or form reported an error, tell the lecturer immediately. Grades are calculated after the sitting. One submission is allowed per Google account and per Student Registration Number. Responses cannot be edited. Contact your lecturer if a correction is needed.');
   form.setDestination(FormApp.DestinationType.SPREADSHEET,c.bookId);
   if(typeof form.setPublished==='function')form.setPublished(true);
   form.setAcceptingResponses(false);
   var prefill=form.createResponse();form.getItems(FormApp.ItemType.TEXT).forEach(function(item){prefill.withItemResponse(item.asTextItem().createResponse('PLACEHOLDER_'+item.getId()));});
   c.forms[key]={formId:form.getId(),url:form.getPublishedUrl(),prefill:prefill.toPrefilledUrl(),items:items};examSave_(c);
   windows.appendRow([key,'','','NO',ML_PROJECT_MINUTES]);
   ScriptApp.newTrigger('collectColabExamResponse').forForm(form).onFormSubmit().create();
   created.push(key);
  });
  console.log('Created forms: '+(created.join(', ')||'none (all three already existed)')+'. Every Test windows row is enabled NO. Nothing was opened.');
  console.log('PUBLIC_NOTEBOOK_CONFIG '+JSON.stringify({lecturer_email:EXAM_OWNER,forms:c.forms}));
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


def build_packets():
    """One notebook per course (the memo lists are lettered per course) for the three allocation labels A, B and C. The data block of the
    setup cell is stored once and put back by the portal, so the file stays small. The data is inside the notebook: the packet CSV is empty."""
    notebooks = {}
    for code in PC.CODES:
        nb = json.loads((PC.PROJECT / 'Notebooks' / code / 'ML_PROJECT_student.ipynb').read_text())
        assert len(nb['cells'][-1]['outputs']) == 0 and 'iuea-submission' in nb['cells'][-1]['metadata']['tags'], 'the last cell must be the empty submit cell'
        assert ''.join(nb['cells'][1]['source']).startswith('FULL_NAME') and '# IUEA-SETUP-CELL' in ''.join(nb['cells'][3]['source']), 'cells 1 and 3 must be the identity and setup cells (the portal edits them by position)'
        notebooks[code] = nb
    packed = PC.packed_data()
    lines = ['// Generated from student files only (tools/build_deploy_bundle.py). Never add answer keys.',
             '// The data block of the setup cell is stored once (ML_PROJECT_DATA); the portal puts it back into cell 3 of the issued notebook.',
             'var ML_PROJECT_DATA = ' + json.dumps(packed) + ';', 'var ML_PROJECT_NOTEBOOKS = {};', 'var PORTAL_PACKETS_ML = {};']
    for code, nb in notebooks.items():
        cell3 = ''.join(nb['cells'][3]['source'])
        assert cell3.count(packed) == 1, 'the setup cell must hold the data block once'
        light = json.loads(json.dumps(nb))
        light['cells'][3]['source'] = cell3.replace(packed, '__IUEA_PACKED_DATA__')
        lines.append(f'ML_PROJECT_NOTEBOOKS[{json.dumps(code)}] = ' + json.dumps(json.dumps(light, ensure_ascii=False), ensure_ascii=False) + ';')
    packets = {}
    for code in PC.CODES:
        instructions = (f'{code} ML_PROJECT: Engineering ML project, online, 3 hours from Start test. The window {PC.WINDOW_TEXT}.\n'
                        'Open your private notebook in Colab from the entry page. Individual work, no AI or outside help. '
                        'Run the countdown cell and the setup cell, complete Tasks 1 to 8, Restart session and run all, then run the Submit test cell and press Submit on the form before your personal deadline.\n')
        for v in ('A', 'B', 'C'):
            key = f'{code}|ML_PROJECT|{v}'
            lines.append(f'PORTAL_PACKETS_ML[{json.dumps(key)}] = {{notebook: ML_PROJECT_NOTEBOOKS[{json.dumps(code)}], data: ML_PROJECT_DATA, csv: "", instructions: {json.dumps(instructions)}}};')
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
    links_and_qr()
    print('deploy bundle written to', DEPLOY, '-', len(packets), 'packets')


if __name__ == '__main__':
    main()
