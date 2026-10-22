"""Grade a lecturer-exported test ZIP. Original snapshots and attempts are retained."""
import argparse,hashlib,json,os,shlex,subprocess,tempfile,zipfile
import contextlib
from pathlib import Path
from exam_intake import connect,process,export
from isolated_grading import preflight
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DEFAULT_OUT=ROOT/'IUEA_Teaching_Plan/test_operations/grading_output'

def grade_batch(archive,out):
    preflight()
    out=Path(out);out.mkdir(parents=True,exist_ok=True);os.chmod(out,0o700)
    with zipfile.ZipFile(archive) as z:
        if len(z.namelist())!=len(set(z.namelist())):raise ValueError('Duplicate archive paths')
        if sum(i.file_size for i in z.infolist())>500*1024*1024:raise ValueError('Batch exceeds 500 MB')
        manifest=json.loads(z.read('manifest.json'))
        if manifest.get('schema')!=1:raise ValueError('Unknown batch format')
        ids=[j['response_id'] for j in manifest['jobs']]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate response IDs')
        with connect(out/'ledger.sqlite3') as db:
            for index,job in enumerate(manifest['jobs'],1):
                try:
                    filename=job['file']
                    if Path(filename).name!=filename or not filename.endswith('.ipynb'):raise ValueError('Unsafe notebook filename')
                    info=z.getinfo(filename)
                    if info.file_size>10*1024*1024:raise ValueError('Notebook exceeds 10 MB')
                    content=z.read(filename)
                    if hashlib.sha256(content).hexdigest()!=job['notebook_sha256']:raise ValueError('Snapshot checksum mismatch')
                    # Store originals under content hashes, not user-provided paths.
                    originals=out/'originals';originals.mkdir(exist_ok=True)
                    path=originals/(job['notebook_sha256']+'.ipynb');path.write_bytes(content)
                    result=process(job,path,db)
                    print(f'{index}/{len(ids)}: {job["cohort"]} {job["assessment"]}: {result["status"]}',flush=True)
                except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
                    row=['']*15
                    for col,key in [(0,'response_id'),(1,'cohort'),(2,'assessment'),(4,'full_name'),(6,'student_registration_number')]:row[col]=job.get(key,'')
                    row[10]='BATCH_ERROR';row[14]=str(error)
                    manifest.setdefault('collection_issues',[]).append(row)
                    print(f'{index}/{len(ids)}: BATCH_ERROR: {error}',flush=True)
            export(db,out)
    # Preserve collection errors as visible exceptions rather than silently dropping students.
    (out/'collection_issues.json').write_text(json.dumps(manifest.get('collection_issues',[]),indent=2)+'\n')
    data=json.loads((out/'workbook_data.json').read_text());data['collection_issues']=manifest.get('collection_issues',[])
    (out/'workbook_data.json').write_text(json.dumps(data,indent=2)+'\n')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('batch',nargs='?');p.add_argument('--out',type=Path,default=DEFAULT_OUT);p.add_argument('--no-workbook',action='store_true');p.add_argument('--ca-private',type=Path,help='Cumulative private directory for a custom test output directory');a=p.parse_args()
    if not a.batch:
        entered=input('Drag the downloaded IUEA-test-batch ZIP into this window, then press Return:\n').strip()
        paths=shlex.split(entered)
        if len(paths)!=1:raise ValueError('Choose exactly one exported batch ZIP')
        a.batch=paths[0]
    from integrate_test_marks import integrate_locked
    import refresh_ca
    # Custom/rehearsal output must never silently update production marks.
    ca_private = a.ca_private or (refresh_ca.PRIVATE if a.out.resolve()==DEFAULT_OUT.resolve() else None)
    if a.no_workbook: ca_private = None
    guard = refresh_ca.exclusive(ca_private) if ca_private else contextlib.nullcontext()
    with guard:
        out=grade_batch(Path(a.batch).expanduser(),a.out)
        if not a.no_workbook:
            node=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
            subprocess.run([str(node),str(ROOT/'scripts/build_test_marks.mjs'),str(out/'workbook_data.json'),str(out/'Test_Marks.xlsx')],check=True)
        if ca_private:
            try:
                integrate_locked(out/'workbook_data.json', ca_private)
            except Exception:
                print('Test results are saved, but the cumulative update did not finish. Fix the reported issue and repeat the same command; saved test attempts are reused.', flush=True)
                raise
        else:
            print('Custom output / no-workbook mode: cumulative workbook not updated.')
    print('Finished. Results:',out)
    if not a.no_workbook:
        subprocess.run(['open',str(out/'Test_Marks.xlsx')],check=False)
        if ca_private: subprocess.run(['open',str(ca_private/refresh_ca.BOOK)],check=False)
if __name__=='__main__':main()
