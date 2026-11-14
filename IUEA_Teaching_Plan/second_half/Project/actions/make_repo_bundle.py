"""Assemble the contents of the PRIVATE grading repository in a folder (nothing is created on GitHub, nothing is pushed).

    python3 actions/make_repo_bundle.py <empty folder>

The folder gets the same relative layout as this repository, so every path in the grader works unchanged:
  .github/workflows/grade-ml-project.yml      the workflow
  IUEA_Teaching_Plan/grader/                  only the modules the project grading imports, the sandbox worker and the Colab shim
  IUEA_Teaching_Plan/second_half/Build/ref/   the two NumPy reference helpers the project reference imports (read only)
  IUEA_Teaching_Plan/second_half/Project/     grader_spec (hidden checks and data, no proof parts), sandbox, actions, the issued notebooks
                                              (the copy check compares with them), the data file, and the two tools the grader imports
No student data is copied: no submissions, no class list, no results, no data/ folder except the public entry host.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
PLAN = PROJECT.parents[1]
ROOT = PLAN.parent
GRADER_MODULES = ['batch_grade.py', 'engineering_contracts.py', 'grader_fairness.py', 'isolated_grading.py', 'iuea_grader.py', 'registration.py',
                  'isolated_worker.py', 'colab_shim.py', 'ownwork_fairness.py', 'review_fairness.py']
REF = ['sk_tree_replica.py', 'week_reference_numpy.py']
PROJECT_DIRS = ['grader_spec', 'sandbox', 'actions', 'Notebooks', 'data_source']
PROJECT_TOOLS = ['pipeline_cells.py', 'project_content.py', 'export_for_gradebook.py']
SKIP = shutil.ignore_patterns('__pycache__', '*.pyc', 'proof_parts', 'e2e_results.txt', '.DS_Store')


def build(target):
    target = Path(target)
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f'{target} is not empty.')
    copy = lambda src, dst: (dst.parent.mkdir(parents=True, exist_ok=True), shutil.copy2(src, dst))
    for name in GRADER_MODULES:
        if (PLAN / 'grader' / name).exists():
            copy(PLAN / 'grader' / name, target / 'IUEA_Teaching_Plan/grader' / name)
    for name in REF:
        copy(PLAN / 'second_half/Build/ref' / name, target / 'IUEA_Teaching_Plan/second_half/Build/ref' / name)
    for d in PROJECT_DIRS:
        shutil.copytree(PROJECT / d, target / 'IUEA_Teaching_Plan/second_half/Project' / d, ignore=SKIP)
    for name in PROJECT_TOOLS:
        copy(PROJECT / 'tools' / name, target / 'IUEA_Teaching_Plan/second_half/Project/tools' / name)
    copy(ROOT / 'data/test_portal_config.json', target / 'data/test_portal_config.json')
    copy(HERE / 'workflow/grade-ml-project.yml', target / '.github/workflows/grade-ml-project.yml')
    (target / 'README.md').write_text('# IUEA ML project grading (private)\n\nInstant checks for the Engineering ML project, run by GitHub Actions. '
                                      'See IUEA_Teaching_Plan/second_half/Project/deploy/SETUP_GITHUB_ACTIONS.md in the teaching repository. '
                                      'This repository holds hidden checks and hidden data: keep it private and never add students as collaborators.\n')
    (target / '.gitignore').write_text('__pycache__/\n*.pyc\ngrading_output/\n')
    files = [p for p in target.rglob('*') if p.is_file()]
    print(f'{len(files)} files, {sum(p.stat().st_size for p in files) / 1e6:.1f} MB in {target}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    build(sys.argv[1])
