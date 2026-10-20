#!/bin/zsh
set -e
teaching_root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$teaching_root"
/usr/bin/caffeinate -i "$teaching_root/.iuea-grader-env/bin/python" "$teaching_root/IUEA_Teaching_Plan/grader/grade_test_batch.py"
read '?Press Return to close this window.'
