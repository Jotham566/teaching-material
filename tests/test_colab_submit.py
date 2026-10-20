import hashlib,json,sys,types,unittest,urllib.parse
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class Button:
 def __init__(self,**kwargs):self.disabled=False
 def on_click(self,f):self.callback=f
class Output:
 def __enter__(self):pass
 def __exit__(self,*args):pass
class Call:
 def __init__(self,value):self.value=value
 def execute(self):return self.value
class SubmitTests(unittest.TestCase):
 def helper(self,missing=False):
  captured={};shown=[]
  class Drive:
   def files(self):return self
   def permissions(self):return self
   def create(self,**kwargs):
    if 'fileId' in kwargs:captured['permission']=kwargs;return Call({})
    captured['bytes']=kwargs['media_body'];return Call({'id':'snapshot-id'})
  drive=Drive();google=types.ModuleType('google');auth=types.ModuleType('google.auth');auth.default=lambda:('fake',None);google.auth=auth
  colab=types.ModuleType('google.colab');colab.auth=types.SimpleNamespace(authenticate_user=lambda:None)
  nb={'nbformat':4,'cells':[{'cell_type':'code','source':'x=1','metadata':{}},{'cell_type':'code','source':'helper','metadata':{'tags':['iuea-submission']},'outputs':[{'secret':'temporary link'}],'execution_count':2}]}
  colab._message=types.SimpleNamespace(blocking_request=lambda *a,**k:{'ipynb':nb})
  api=types.ModuleType('googleapiclient');discovery=types.ModuleType('googleapiclient.discovery');discovery.build=lambda *a,**k:drive
  http=types.ModuleType('googleapiclient.http');http.MediaIoBaseUpload=lambda stream,**k:stream.read()
  ip=types.ModuleType('IPython');display=types.ModuleType('IPython.display');display.display=lambda *x:shown.extend(x);display.HTML=lambda x:x;display.clear_output=lambda:None
  widget=types.ModuleType('ipywidgets');widget.Button=Button;widget.Output=Output
  modules={'google':google,'google.auth':auth,'google.colab':colab,'googleapiclient':api,'googleapiclient.discovery':discovery,'googleapiclient.http':http,'IPython':ip,'IPython.display':display,'ipywidgets':widget}
  config={'lecturer_email':'lecturer@example.com','forms':{'CML3111|TEST1':{'prefill':'https://docs.google.com/forms/test?entry.1=PLACEHOLDER_10&entry.2=PLACEHOLDER_20&entry.3=PLACEHOLDER_30','items':{'Full name':40,'Variant':50,'Student Registration Number':10,'Snapshot file ID':20,'Snapshot SHA-256':30}}}}
  ns=dict(FULL_NAME='' if missing else 'Synthetic',STUDENT_ID='DEMO / & example',COHORT='CML3111',TEST_ID='TEST1',VARIANT='A')
  with patch.dict(sys.modules,modules):
   exec((ROOT/'IUEA_Teaching_Plan/test_operations/colab_submit_cell.py').read_text().replace('__EXAM_CONFIG__',repr(config)),ns)
   ns['_button'].callback(None)
  return ns,captured,shown
 def test_snapshot_and_prefill(self):
  ns,captured,shown=self.helper();payload=json.loads(captured['bytes']);self.assertEqual(payload['cells'][-1]['outputs'],[])
  self.assertFalse(captured['permission']['sendNotificationEmail']);self.assertEqual(captured['permission']['body']['role'],'reader')
  link=next(x for x in shown if isinstance(x,str));self.assertIn('DEMO+%2F+%26+example',link);self.assertIn(hashlib.sha256(captured['bytes']).hexdigest(),link);self.assertFalse(ns['_button'].disabled)
 def test_missing_identity_does_not_upload(self):
  ns,captured,shown=self.helper(True);self.assertEqual(captured,{});self.assertFalse(ns['_button'].disabled)
if __name__=='__main__':unittest.main()
