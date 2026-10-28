"""Build the teaching edition into a STAGING folder. Nothing in the live edition changes.

  python3 build_edition.py STAGING_FOLDER

Sources, all under Authoring/:
  decks      Baseline/Final Decks                    (versioned builder output, hash-checked)
             + Edition/patch/slide_patch.json        (text and picture corrections)
             + Documents/lesson_notes.json           (speaker notes: read-aloud scripts)
             + Illustrations/                        (pictures and placement plan)
  documents  Baseline/Documents
             + Edition/patch/docx_patch.json         (paragraph text corrections)
  backup     Documents/make_presenter_backup.py      (Presenter Notes Backup.txt: sources and click counts)
  files      Edition/files/                          (practice files, teaching resources and other
                                                      hand-written files, in the edition's own layout)
Then run compare_edition.py STAGING and verify_edition.py before promoting.
"""
import sys, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTH = HERE.parent
sys.path.insert(0, str(HERE))
PY = sys.executable
BASE = AUTH / 'Baseline'

def check_baseline():
    """Refuse to build from a baseline that differs from its manifest."""
    import json, hashlib
    man = json.loads((BASE / 'Baseline Manifest.json').read_text(encoding='utf-8'))['files']
    bad = [k for k, h in man.items() if not (BASE / k).exists() or hashlib.sha256((BASE / k).read_bytes()).hexdigest() != h]
    extra = [str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and str(p.relative_to(BASE)) not in man and p.name not in ('Baseline Manifest.json', 'README.txt', '.DS_Store')]
    if bad or extra: sys.exit(f'Baseline does not match its manifest. Changed or missing: {bad[:5]}; unlisted: {extra[:5]}')

def run(*a):
    subprocess.run([PY, *map(str, a)], check=True)

def main(staging):
    check_baseline()
    st = Path(staging)
    if st.exists() and any(st.iterdir()): sys.exit(f'{st} is not empty. Use a new folder.')
    st.mkdir(parents=True, exist_ok=True)
    decks = st / '02 Class Slides'
    run(HERE / 'edition_patch.py', 'apply', BASE / 'Final Decks', HERE / 'patch', decks)
    run(AUTH / 'Documents/apply_lesson_notes.py', decks)
    run(AUTH / 'Illustrations/add_illustrations.py', decks)
    tmp = st / '_docs'
    run(HERE / 'docx_patch.py', 'apply', AUTH / 'Baseline/Documents', HERE / 'patch/docx_patch.json', tmp)
    run(AUTH / 'Documents/add_demonstration_instructions.py', tmp / 'Facilitator Guide.docx')
    for src, dst in (('Course Overview.docx', '01 Course Overview'), ('Learner Workbook.docx', '03 Learner Materials'),
                     ('Facilitator Guide.docx', '04 Facilitator Materials'), ('Law Firm Implementation Playbook.docx', '04 Facilitator Materials')):
        (st / dst).mkdir(parents=True, exist_ok=True); shutil.copy2(tmp / src, st / dst / src)
    shutil.rmtree(tmp)
    shutil.copytree(HERE / 'files', st, dirs_exist_ok=True)
    run(AUTH / 'Documents/make_demo_materials.py', st / '04 Facilitator Materials/Teaching Resources/Demo Materials', st)
    run(AUTH / 'Documents/make_presenter_backup.py', st / '04 Facilitator Materials/Teaching Resources/Presenter Notes Backup.txt')
    run(AUTH / 'Documents/make_playback_checklist.py', st / '04 Facilitator Materials/Teaching Resources/Playback and Rehearsal Checklist.txt')
    print('staging edition built in', st)

if __name__ == '__main__':
    main(sys.argv[1])
