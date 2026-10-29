# Submission helper only. This cell is excluded from marking.
# Run this cell, then click Submit test. Never share credentials or tokens.
import copy as _copy
import hashlib as _hashlib
import io as _io
import json as _json
import urllib.parse as _urlparse
import uuid as _uuid
import datetime as _datetime
import time as _time
import threading as _threading
import ipywidgets as _widgets
from IPython.display import display as _display, HTML as _HTML, clear_output as _clear_output

_EXAM_CONFIG = __EXAM_CONFIG__
_EXPIRED_MESSAGE = 'Time has ended. Submission is closed. Do not use an old form link. Contact your lecturer if you need help.'

class _IUEAAccountMismatch(RuntimeError):
    def __init__(self, active_email, allocated_email, snapshot_owner=''):
        self.active_email = active_email or 'could not be verified'
        self.allocated_email = allocated_email or 'could not be verified'
        self.snapshot_owner = snapshot_owner

def _show_account_warning(error):
    import html as _html
    active = _html.escape(error.active_email)
    allocated = _html.escape(error.allocated_email)
    owner = ''
    if error.snapshot_owner:
        owner = '<p><strong>Snapshot owner:</strong> '+_html.escape(error.snapshot_owner)+'</p>'
    _display(_HTML(
        '<div role="alert" style="border:4px solid #b3261e;background:#fff0ee;'
        'padding:18px;margin:12px 0;color:#7a1712;font-size:17px">'
        '<p style="font-size:21px;font-weight:bold;margin-top:0">'
        'ACCOUNT MISMATCH — submission link withheld</p>'
        '<p><strong>Currently active Colab account:</strong> '+active+'</p>'
        '<p><strong>Account allocated to this test:</strong> '+allocated+'</p>'
        +owner+
        '<p>Switch to the allocated Google account inside Colab, then rerun this '
        'submission cell. Do not submit while these accounts differ.</p></div>'
    ))

def _submission_expired():
    _deadline = globals().get('_IUEA_DEADLINE', '')
    if not _deadline:
        if globals().get('_IUEA_ALLOCATION') and TEST_ID == 'TEST1':
            raise RuntimeError('The saved deadline is missing. Reopen your issued notebook through the test entry page; do not start another attempt.')
        return False
    return _time.time() >= _datetime.datetime.fromisoformat(_deadline.replace('Z', '+00:00')).timestamp()

def _check_submission_time():
    if _submission_expired():
        raise RuntimeError(_EXPIRED_MESSAGE)

# Check before requesting Google access or creating any snapshot.
_check_submission_time()
# Authenticate while running the cell so Colab can display its account dialog.
from google.colab import auth as _colab_auth
print('Double-check your full name, Student ID/ Registration Number, and email before submitting.')
print('Name:', FULL_NAME, '| Student ID/ Registration Number:', STUDENT_ID, '| Email:', EMAIL)
print('Prepare submission: authorize your own Google account if asked.')
_colab_auth.authenticate_user()

_button = _widgets.Button(description="Submit test", button_style="success", icon="check")
_submission_output = _widgets.Output()

def _prepare_test_submission(_):
    _button.disabled = True
    with _submission_output:
        _clear_output()
        try:
            _check_submission_time()
            for _label,_value in [('Full name',FULL_NAME),('Student ID/ Registration Number',STUDENT_ID),('Email',EMAIL)]:
                if not isinstance(_value,str) or not _value.strip():
                    raise ValueError('Complete '+_label+' in the identity cell and run that cell first.')
            _key = COHORT+'|'+TEST_ID
            _form = _EXAM_CONFIG['forms'][_key]
            if VARIANT not in ('A','B','C'):raise ValueError('Keep your assigned variant A, B or C.')
            from google.colab import auth as _auth, _message
            import google.auth as _google_auth
            from googleapiclient.discovery import build as _build
            from googleapiclient.http import MediaIoBaseUpload as _MediaUpload
            print('Preparing your notebook snapshot. Use the same Google account in the final form.')
            import logging as _logging
            _logging.getLogger('google_auth_httplib2').addFilter(lambda r: not r.getMessage().startswith('httplib2 transport does not support per-request timeout'))
            _credentials,_project = _google_auth.default()
            _drive = _build('drive','v3',credentials=_credentials,cache_discovery=False)
            _reply = _message.blocking_request('get_ipynb',timeout_sec=60)
            _notebook = _copy.deepcopy(_reply['ipynb'])
            _metadata = _notebook.get('metadata',{})
            _allocated_email = str(
                _metadata.get('iuea_allocated_email')
                or globals().get('_IUEA_ALLOCATED_EMAIL')
                or EMAIL
            ).strip().lower()
            _metadata_code = str(_metadata.get('iuea_allocation_code') or '')
            _runtime_code = str(globals().get('_IUEA_ALLOCATION') or '')
            if not _allocated_email:
                raise ValueError('The issued notebook has no allocated Google account. Return to the test entry page and contact your lecturer.')
            if _metadata_code and _runtime_code and _metadata_code != _runtime_code:
                raise ValueError('This notebook allocation does not match the running identity cell. Reopen your issued notebook from the test entry page.')
            _active_email = str(
                (_drive.about().get(fields='user(emailAddress)').execute()
                 .get('user',{}).get('emailAddress',''))
            ).strip().lower()
            if not _active_email or _active_email != _allocated_email:
                raise _IUEAAccountMismatch(_active_email, _allocated_email)
            if str(EMAIL).strip().lower() != _allocated_email:
                raise ValueError('The notebook identity email does not match the allocation. Reopen your issued notebook from the test entry page.')
            # Remove outputs from the submission helper, which contain temporary links.
            for _cell in _notebook['cells']:
                if 'iuea-submission' in _cell.get('metadata',{}).get('tags',[]):
                    _cell['outputs']=[];_cell['execution_count']=None
            _payload = _json.dumps(_notebook,ensure_ascii=False).encode('utf-8')
            if len(_payload)>10*1024*1024:raise ValueError('Notebook exceeds 10 MB. Clear large outputs, then try again.')
            _sha = _hashlib.sha256(_payload).hexdigest()
            _name = COHORT+'_'+TEST_ID+'_submission_'+_uuid.uuid4().hex[:12]+'.ipynb'
            _check_submission_time()
            _created = _drive.files().create(body={'name':_name,'mimeType':'application/x-ipynb+json'},media_body=_MediaUpload(_io.BytesIO(_payload),mimetype='application/x-ipynb+json',resumable=False),fields='id').execute()
            _snapshot = _drive.files().get(
                fileId=_created['id'],fields='id,owners(emailAddress)'
            ).execute()
            _owners = _snapshot.get('owners',[])
            _snapshot_owner = str(
                _owners[0].get('emailAddress','') if _owners else ''
            ).strip().lower()
            if not _snapshot_owner or _snapshot_owner != _allocated_email:
                raise _IUEAAccountMismatch(
                    _active_email,_allocated_email,
                    _snapshot_owner or 'could not be verified'
                )
            _drive.permissions().create(fileId=_created['id'],body={'type':'user','role':'reader','emailAddress':_EXAM_CONFIG['lecturer_email']},sendNotificationEmail=False).execute()
            _values={'Full name':FULL_NAME.strip(),'Student Registration Number':STUDENT_ID.strip(),'Variant':globals().get('_IUEA_ALLOCATION', VARIANT),'Snapshot file ID':_created['id'],'Snapshot SHA-256':_sha}
            _parts = _urlparse.urlsplit(_form['prefill'])
            _query = _urlparse.parse_qsl(_parts.query,keep_blank_values=True)
            _replace={'PLACEHOLDER_'+str(_form['items'][k]):str(v) for k,v in _values.items()}
            _query=[(k,_replace.get(v,v)) for k,v in _query]
            # Select the student's account when several Google accounts are signed in.
            _query=[(k,v) for k,v in _query if k.lower() != 'authuser']
            _query.append(('authuser', EMAIL.strip().lower()))
            _link = _urlparse.urlunsplit((_parts.scheme,_parts.netloc,_parts.path,_urlparse.urlencode(_query),_parts.fragment))
            import html as _html
            _check_submission_time()
            _display(_HTML('<a target="_blank" rel="noopener" href="'+_html.escape(_link,quote=True)+'" style="font-size:18px">Finish submission: open the form and press Submit</a>'))
            print('Snapshot prepared. You have NOT submitted yet. Open the link above, confirm your details, tick the email confirmation box and press Submit before the deadline. Keep the confirmation page. Do not edit the snapshot file in Drive.')
        except _IUEAAccountMismatch as _error:
            _show_account_warning(_error)
            print('No submission link was created. Switch to the allocated account and rerun this cell.')
        except Exception as _error:
            print('Submission was not completed:',str(_error)[:300])
            print(_EXPIRED_MESSAGE if _submission_expired() else 'If time remains, retry or contact your lecturer before the deadline. Do not assume your work was submitted.')
        finally:
            _button.disabled = _submission_expired()

_button.on_click(_prepare_test_submission)
_display(_button,_submission_output)

# Disable the displayed button when the fixed deadline arrives, even without a click.
if globals().get('_submission_expiry_timer'):
    _submission_expiry_timer.cancel()
if globals().get('_IUEA_DEADLINE'):
    def _close_submission_button():
        _button.disabled = True
        _button.description = 'Time has ended'
        with _submission_output:
            _clear_output()
            print(_EXPIRED_MESSAGE)
    _seconds_left = max(0, _datetime.datetime.fromisoformat(_IUEA_DEADLINE.replace('Z', '+00:00')).timestamp() - _time.time())
    _submission_expiry_timer = _threading.Timer(_seconds_left, _close_submission_button)
    _submission_expiry_timer.daemon = True
    _submission_expiry_timer.start()
