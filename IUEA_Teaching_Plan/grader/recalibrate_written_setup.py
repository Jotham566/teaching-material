"""Validate installed A1/A2 models before replacing calibration; never grade students."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import artifact_grade
from calibration_record import model_for_report, profile_for_report
from check_written_setup import REPORTS, HERE, ROOT
from local_ai_resources import ensure_docker_stopped
from refresh_ca import exclusive, PRIVATE
from run_ca_written_queue import unload


def activate(candidates, reports=REPORTS):
    """Validate every candidate before touching either active report."""
    for label, (target, rubric_path) in reports.items():
        candidate = candidates[label]
        model = model_for_report(candidate)
        if profile_for_report(candidate) != 'standard':
            raise ValueError('Expected standard calibration profile')
        artifact_grade.validate_calibration(candidate, json.loads(rubric_path.read_text()),
                                           artifact_grade.local_model_identity(model), model)
    # Retain original reports with the candidate evidence, outside active paths.
    backup = next(iter(candidates.values())).parent/'previous_reports'
    backup.mkdir(exist_ok=True)
    for label, (target, _) in reports.items():
        for suffix in ('', '.complete.json'):
            old = Path(str(target)+suffix)
            if old.exists(): shutil.copy2(old, backup/(label+'.json'+suffix))
    for label, (target, _) in reports.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        for suffix in ('', '.complete.json'):
            dest = Path(str(target)+suffix)
            temporary = dest.with_name(dest.name+'.new')
            shutil.copy2(Path(str(candidates[label])+suffix), temporary)
            temporary.replace(dest)


def main(a1_model='qwen3.5:4b', a2_model='qwen3:4b', trial=False):
    with exclusive(PRIVATE):
        # Both names must already be available; do not silently download a new model.
        models = {'A1': a1_model, 'A2': a2_model}
        for model in models.values(): artifact_grade.local_model_identity(model)
        ensure_docker_stopped()
        trials = PRIVATE/'model_trials'; trials.mkdir(parents=True, exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix='installed_setup_', dir=trials))
        candidates = {label: folder/(label+'.json') for label in models}
        print('Calibration evidence: '+str(folder), flush=True)
        for label, model in models.items():
            print('Checking '+label+' with '+model+' using synthetic known-answer cases...', flush=True)
            for resident in models.values(): unload(resident)
            if label == 'A1':
                command = [sys.executable, str(HERE/'calibrate_rubric.py'),
                           '--rubric', str(HERE/'rubrics/W01.json'),
                           '--cases', str(HERE/'calibration_cases/W01.json')]
            else:
                command = [sys.executable, str(HERE/'calibrate_local_grader.py')]
            try:
                subprocess.run(command+['--model',model,'--out',str(candidates[label])],check=True,cwd=ROOT)
            finally:
                unload(model)
        if trial:
            for label, (_, rubric_path) in REPORTS.items():
                model = model_for_report(candidates[label])
                artifact_grade.validate_calibration(candidates[label], json.loads(rubric_path.read_text()),
                                                   artifact_grade.local_model_identity(model), model)
            print('TRIAL PASS: '+', '.join(l+'='+m for l, m in models.items())+' passed calibration. Nothing was activated.')
            print('Evidence: '+str(folder))
            return
        activate(candidates)
        print('PASS: both calibrations activated. Original reports are backed up. No student marks changed.')
        print('Repeat your original grade-submissions command with the same ZIP to resume.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Calibrate installed models; --trial validates a candidate without activating it.')
    ap.add_argument('--a1-model', default='qwen3.5:4b'); ap.add_argument('--a2-model', default='qwen3:4b')
    ap.add_argument('--trial', action='store_true')
    args = ap.parse_args()
    try: main(args.a1_model, args.a2_model, args.trial)
    except Exception as exc:
        print('STOPPED: '+str(exc), file=sys.stderr)
        print('Do not bypass calibration. Keep the evidence and share the failed case/error for review. Student marks were not changed.', file=sys.stderr)
        raise SystemExit(1)
