"""Build the deployment bundle that lets the Test 1 machinery run the project sitting: python3 tools/build_deploy_bundle.py

Writes Project/deploy/ (the live files in test_portal/ and grader/ are NOT touched; every output is a patched COPY, each patch asserts its match count):
  Portal.gs                  test_portal/Portal.gs with the ML_PROJECT key, the project packets and the project instructions
  PacketsMLProject.gs        the 9 student packets (3 cohorts x variants A, B, C): notebook, CSV, instructions. No keys, no solutions.
  Index.html                 test_portal/Index.html with the project heading, sitting times and project wording
  gateway/page.mjs           the same page for the Cloudflare gateway (generated exactly as scripts/build_test_gateway.py does)
  gateway/worker.mjs         test_portal/gateway/worker.mjs accepting the ML_PROJECT key
  exam_collection.gs         grader/exam_collection.gs with the ML_PROJECT key in authoriseFreshTestAttempt and the project wording on the form
  test_monitor.gs            grader/test_monitor.gs with ML_PROJECT in the monitor
  ml_project_collection.gs   NEW: installMlProjectCollection() creates the three forms and the Test windows rows (duration 180)
  Test_windows_rows.csv      the three proposed Test windows rows, ready to type (all 'proposed, lecturer to confirm'; enabled NO)
Run build_project_notebooks.py first. For the release run it with --require-forms (after the forms exist), then this script again.
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
    text = '''# __COURSE__ Engineering ML project: supervised timed sitting

Individual work • Part A 30 marks and Part B 15 marks (45 marks, scaled to 40 percent of the course) • Up to three hours from **Start test**.

__DEADLINE__
The timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the class closing time. Colab may still allow editing afterwards, but late work is not accepted for grading.

## 1. Work in your private notebook
Click **Open my test in Colab** on the entry page and use the same Google account throughout. This is your own private, editable notebook: work in it directly. Click **Connect** if shown. To resume after a closed tab or a shutdown, reopen the entry link with the same email and registration number and click Resume my test in Colab. Save regularly with **File, then Save**: only saved work can be recovered.

## 2. Load the data
Check the identity cell near the top. Tell your lecturer immediately if the details are wrong; do not change the supplied course, test or allocation settings. Run the first code cell using the triangle beside it to check your details and display the countdown. Then run **Prepare the data and the libraries**. It creates `engineering_data.csv` for you: no upload is needed. After a runtime reset, rerun these two cells before your work.

## 3. Complete the tasks
Work from top to bottom. Tasks 1 to 8 are coded functions and results; Task 9 is the Part B memo form (a dictionary called `MEMO`). Keep supplied function names, variable names and required output formats unchanged. The self-check cells are not marked. Everything is marked automatically by the lecturer's computer, on other data you cannot see. Use the time plan in the notebook and leave at least 20 minutes to submit.

## 4. Submit: allow at least 20 minutes
1. Choose **Runtime, then Restart session and run all**. Every cell must run without an error. Save.
2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.
3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.
4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student ID/ Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.
5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.

**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. One submission only per Google account and Student ID/ Registration Number. You cannot edit or replace a submitted response; contact your lecturer for any correction.

## If something fails
Record the error and contact your lecturer immediately, before the deadline. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun the setup cells; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.

**Permitted resources:** Your lecture slides, your lab notebooks, the revision guide, cheatsheet and personal course notes. Write the code yourself.

**No AI or outside help:** Do not use Gemini, ChatGPT, Copilot or any other AI tool to generate, complete, rewrite, explain or debug your answers. Do not obtain answers from another person, collaborate, or copy someone else's work.

**Understanding check:** You may be asked to explain your submitted code or make a small change without AI or another person's help.

**Declaration:** By submitting, I confirm that I completed this project myself without AI assistance or another person's help, using only the permitted resources. I can explain and modify the code I submitted.
'''
    return ('function portalMlInstructions_(course,deadline){\n return ' + json.dumps(text, ensure_ascii=False) +
            ".replace('__COURSE__',course).replace('__DEADLINE__','**Your submission deadline: '+deadline+'.**');\n}\n")


def patch_portal():
    s = (PLAN / 'test_portal/Portal.gs').read_text()
    s = sub(s, KEY_OLD, KEY_NEW, 2)
    s = sub(s, "var packet=PORTAL_PACKETS[key+'|'+record[4]];if(!packet)", "var packet=PORTAL_PACKETS[key+'|'+record[4]]||(typeof PORTAL_PACKETS_ML!=='undefined'?PORTAL_PACKETS_ML[key+'|'+record[4]]:undefined);if(!packet)")
    s = sub(s, "  nb.cells[0].source=instructions;\n", "  if(parts[1]==='ML_PROJECT'){instructions=portalMlInstructions_(parts[0],w.label);}\n  nb.cells[0].source=instructions;\n")
    s = s.rstrip('\n') + '\n\n' + instructions_js()
    (DEPLOY / 'Portal.gs').write_text(s)


def patch_index():
    s = (PLAN / 'test_portal/Index.html').read_text()
    s = sub(s, "document.getElementById('heading').textContent=testKey.replace('|TEST',' — Test ');",
            "document.getElementById('heading').textContent=testKey.replace('|ML_PROJECT',' — Engineering ML project (3-hour sitting)').replace('|TEST',' — Test ');")
    windows = ',\n'.join(f" '{c}|ML_PROJECT':'{PC.SITTING[c]['day']}, {PC.SITTING[c]['start']} – {PC.SITTING[c]['end']} (Kampala time; {PC.PROPOSED})'" for c in PC.CODES)
    s = sub(s, "'CML3112|TEST1':'27 October 2026, 7:00 PM – 2 November 2026, 11:59 PM'\n};", "'CML3112|TEST1':'27 October 2026, 7:00 PM – 2 November 2026, 11:59 PM',\n" + windows + "\n};")
    s = sub(s, "Keep the requested answer names unchanged. Only Task 7 of Test 1 requires a function.</li>", 'Keep the requested answer names unchanged.<span id="test1Only"> Only Task 7 of Test 1 requires a function.</span></li>')
    s = sub(s, "document.getElementById('dataStep').textContent='Run Check details and countdown near the top (if present), then Prepare CSV and libraries. This creates engineering_data.csv automatically. For Test 1, write your own pandas code to read it into raw_data in Task 1. Rerun the countdown and setup after a runtime reset. The countdown does not pause or extend your deadline; older copies without it can use the timer on this page.';",
            "document.getElementById('dataStep').textContent=testKey.endsWith('|ML_PROJECT')?'Run Check details and countdown near the top, then Prepare the data and the libraries. This creates engineering_data.csv automatically: no upload is needed. Rerun both after a runtime reset. The countdown does not pause or extend your deadline.':'Run Check details and countdown near the top (if present), then Prepare CSV and libraries. This creates engineering_data.csv automatically. For Test 1, write your own pandas code to read it into raw_data in Task 1. Rerun the countdown and setup after a runtime reset. The countdown does not pause or extend your deadline; older copies without it can use the timer on this page.';")
    s = sub(s, "if(windows[testKey]){document.getElementById('takehome').hidden=false;",
            "if(testKey.endsWith('|ML_PROJECT')){document.getElementById('test1Only').hidden=true;document.querySelector('.brand').textContent='IUEA • ENGINEERING ML PROJECT';}\nif(windows[testKey]){document.getElementById('takehome').hidden=false;")
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
    w = sub(w, r'const keyPattern=/^CML311[123]\|TEST[12]$/;', r'const keyPattern=/^CML311[123]\|(TEST[12]|ML_PROJECT)$/;')
    (DEPLOY / 'gateway/worker.mjs').write_text(w)


def patch_collector():
    s = (PLAN / 'grader/exam_collection.gs').read_text()
    s = sub(s, r"if(!/^CML311[123]\|TEST[12]$/.test(key))throw Error('Use an assessment key such as CML3111|TEST1.');",
            r"if(!/^CML311[123]\|(TEST[12]|ML_PROJECT)$/.test(key))throw Error('Use an assessment key such as CML3111|TEST1 or CML3112|ML_PROJECT.');")
    s = sub(s, "text+='\\n\\nTAKE-HOME TEST: '+w.minutes", "text+='\\n\\n'+(/ML_PROJECT/.test(form.getTitle())?'TIMED PROJECT SITTING':'TAKE-HOME TEST')+': '+w.minutes")
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
 * Example: setMlProjectWindow('CML3112','2026-12-01T11:00:00+03:00','2026-12-01T14:00:00+03:00','CONFIRMED'). Then run syncColabExams. */
function setMlProjectWindow(cohort,opensIso,closesIso,confirm){
 if(confirm!=='CONFIRMED')throw Error('Pass CONFIRMED as the fourth argument once the date is confirmed.');
 var key=String(cohort)+'|ML_PROJECT';
 if(!/^CML311[123]\|ML_PROJECT$/.test(key))throw Error('Use CML3111, CML3112 or CML3113.');
 if(!isFinite(Date.parse(opensIso))||!isFinite(Date.parse(closesIso))||Date.parse(closesIso)<=Date.parse(opensIso))throw Error('Use real dates with the Kampala offset, closing after opening.');
 if(Date.parse(closesIso)-Date.parse(opensIso)>ML_PROJECT_MINUTES*60000+15*60000)throw Error('The window is more than 3 hours 15 minutes. The sitting window should be the class slot.');
 var c=examConfig_(),sheet=SpreadsheetApp.openById(c.bookId).getSheetByName('Test windows'),rows=sheet.getDataRange().getValues();
 var at=rows.findIndex(function(r,i){return i>0&&r[0]===key;});
 if(at<0)throw Error('No Test windows row for '+key+'. Run installMlProjectCollection first.');
 sheet.getRange(at+1,1,1,5).setValues([[key,opensIso,closesIso,'YES',ML_PROJECT_MINUTES]]);
 console.log('Window set for '+key+': '+opensIso+' to '+closesIso+', '+ML_PROJECT_MINUTES+' minutes. Run syncColabExams to open the form.');
}
'''


def build_packets():
    packets = {}
    for code in PC.CODES:
        for v in K.MARKED_VARIANTS:
            folder = PC.PROJECT / 'Notebooks' / code / v
            nb = json.loads((folder / 'ML_PROJECT_student.ipynb').read_text())
            assert len(nb['cells'][-1]['outputs']) == 0 and 'iuea-submission' in nb['cells'][-1]['metadata']['tags'], 'the last cell must be the empty submit cell'
            assert ''.join(nb['cells'][1]['source']).startswith('FULL_NAME') and '# IUEA-SETUP-CELL' in ''.join(nb['cells'][3]['source']), 'cells 1 and 3 must be the identity and setup cells (the portal edits them by position)'
            text = (folder / 'engineering_data.csv').read_text()
            instructions = (f'{code} ML_PROJECT: Engineering ML project, supervised timed sitting ({PC.SITTING_TEXT[code]}).\n'
                            'Open your private notebook in Colab from the entry page. Individual work, 3 hours from Start test, no AI or outside help. '
                            'Run the countdown cell and the setup cell, complete Tasks 1 to 9, Restart session and run all, then run the Submit test cell and press Submit on the form before your personal deadline.\n')
            packets[f'{code}|ML_PROJECT|{v}'] = {'notebook': json.dumps(nb, ensure_ascii=False), 'csv': text, 'instructions': instructions}
    (DEPLOY / 'PacketsMLProject.gs').write_text('// Generated from student files only (tools/build_deploy_bundle.py). Never add answer keys.\nvar PORTAL_PACKETS_ML = ' + json.dumps(packets, ensure_ascii=False) + ';\n')
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
    lines = ['# ML_PROJECT entry links (the same host as Tests 1 and 2)', '',
             'Share these in Class 4 for the rehearsal information and on the day of the sitting. The page releases nothing before the Test windows row is enabled and open.', '',
             '| Course | Sitting (proposed, lecturer to confirm) | Entry link |', '|---|---|---|']
    for c in PC.CODES:
        url = public + '?' + urlencode({'test': c + '|ML_PROJECT'})
        qrgen.png(url, qrdir / f'{c}_ML_PROJECT.png', ec='M', module_px=12, quiet=4)
        lines.append(f'| {c} | {PC.SITTING_TEXT[c]} | [{url}]({url}) |')
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
            s = PC.SITTING[c]
            w.writerow([f'{c}|ML_PROJECT', s['iso_start'], s['iso_end'], 'NO', PC.MINUTES, f'{PC.PROPOSED}; set enabled to YES only after confirming'])
    links_and_qr()
    print('deploy bundle written to', DEPLOY, '-', len(packets), 'packets')


if __name__ == '__main__':
    main()
