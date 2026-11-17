"""Optional local reasoning profile with its own calibration fingerprint.

Reuse the standard extraction, validation, caching and combination code in an
isolated module instance. Only local chat generation options and its deadline
change; the ordinary grading module and its passing calibrations stay intact.
"""
import hashlib,importlib.util,json,sys,urllib.request
from pathlib import Path

PREDICTION_LIMIT=4096
REQUEST_TIMEOUT=360
_BACKEND=None

class ReasonedHTTP:
    def __init__(self,transport):self.transport=transport
    def open(self,request,timeout=None):
        if isinstance(request,urllib.request.Request) and request.full_url=='http://127.0.0.1:11434/api/chat':
            body=json.loads(request.data)
            body['think']=True
            body.setdefault('options',{})['num_predict']=PREDICTION_LIMIT
            request=urllib.request.Request(request.full_url,data=json.dumps(body).encode(),headers=dict(request.header_items()),method=request.get_method())
            timeout=REQUEST_TIMEOUT
        return self.transport.open(request,timeout=timeout)

def load_backend():
    global _BACKEND
    if _BACKEND is not None:return _BACKEND
    path=Path(__file__).with_name('artifact_grade.py')
    spec=importlib.util.spec_from_file_location('iuea_reasoned_backend',path)
    backend=importlib.util.module_from_spec(spec);sys.modules[spec.name]=backend;spec.loader.exec_module(backend)
    original_fingerprint=backend.evaluator_fingerprint
    def profile_fingerprint(rubric=None):
        material=original_fingerprint(rubric).encode()+Path(__file__).read_bytes()
        return hashlib.sha256(material).hexdigest()
    backend.LOCAL_HTTP=ReasonedHTTP(backend.LOCAL_HTTP)
    backend.evaluator_fingerprint=profile_fingerprint
    _BACKEND=backend
    return backend

if __name__=='__main__':load_backend().main()
