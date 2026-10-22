"""Read-only calibration check. No inference, student files or marks are changed."""
import hashlib
import json
from pathlib import Path
import artifact_grade
from calibration_record import model_for_report, profile_for_report

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORTS = {
    'A1': (ROOT/'IUEA_Teaching_Plan/assessment_operations/private/W01_calibration_isolated.json', HERE/'rubrics/W01.json'),
    'A2': (ROOT/'review/2026-09-14/rework/local_calibration_v10.json', HERE/'rubrics/W02.json'),
}


def differences(saved, actual, rubric, model):
    expected = hashlib.sha256(json.dumps(rubric, sort_keys=True).encode()).hexdigest()
    checks = [('Model name', saved.get('model'), model),
              ('Model digest', saved.get('model_identity', {}).get('digest'), actual.get('digest')),
              ('Ollama version', saved.get('model_identity', {}).get('ollama_version'), actual.get('ollama_version')),
              ('Rubric digest', saved.get('rubric_sha256'), expected)]
    return [(label, old, new) for label, old, new in checks if old != new]


def main():
    failed = False
    for label, (report, rubric_path) in REPORTS.items():
        print('\n'+label+' written grading')
        try:
            model = model_for_report(report)
            backend = artifact_grade
            if profile_for_report(report) == 'reasoned':
                from reasoned_artifact_grade import load_backend
                backend = load_backend()
            rubric = json.loads(rubric_path.read_text())
            identity = backend.local_model_identity(model)
            rows = json.loads(report.read_text())
            print('Model: '+model)
            print('Installed Ollama: '+identity['ollama_version'])
            for field, saved, current in differences(rows[0]['result'], identity, rubric, model):
                print(f'MISMATCH {field}: saved={saved}; installed/current={current}')
            backend.validate_calibration(report, rubric, identity, model)
            print('PASS: complete calibration matches this setup.')
        except Exception as exc:
            failed = True
            print('BLOCKED: '+str(exc))
    print('\nRead-only check finished. No model inference or student grading was performed.')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
