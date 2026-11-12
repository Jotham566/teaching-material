#!/bin/bash
# One command: pull the latest Mac-mini snapshot from the private grading repo, rebuild the final-marks workbook and put it on the Desktop.
#   bash IUEA_Teaching_Plan/grader/refresh_final_marks.sh            (add --no-pull to skip the git pull)
# Optional: put approved regrade marks in ~/Desktop/IUEA_Regrade/approved_overrides.csv and they are applied automatically.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PRIV="$HOME/Projects/IUEA-Grading-Private"
SNAP="$PRIV/snapshot/IUEA_Teaching_Plan"
OUT="$HOME/Desktop/IUEA_Semester1_Final_Marks.xlsx"
OV="$HOME/Desktop/IUEA_Regrade/approved_overrides.csv"
PY="$REPO/.iuea-grader-env/bin/python"
if [ "${1:-}" != "--no-pull" ]; then git -C "$PRIV" pull --ff-only; fi
git -C "$PRIV" log -1 --format='Private snapshot: %h %ad %s' --date=short
ARGS=(--ledger "$SNAP/assessment_operations/private/ledger.json" --tests "$SNAP/test_operations/grading_output/current_marks.csv")
if [ -f "$OV" ]; then ARGS+=(--overrides "$OV"); echo "Applying approved regrade marks from $OV"; fi
TD="$HOME/Desktop/IUEA_Regrade/Test1_rerun_proposals.csv"
if [ -f "$TD" ]; then ARGS+=(--test-detail "$TD"); fi
ARGS+=(--notebook-grades "$SNAP/assessment_operations/private/notebook_grades")
CD="$HOME/Desktop/IUEA_Regrade/A2-A5_rerun_proposals.csv"
if [ -f "$CD" ]; then ARGS+=(--coding-detail "$CD"); fi
ARGS+=(--quiz-dir "$SNAP/assessment_operations/private/reconciled")
AL="$HOME/Desktop/IUEA_Regrade/identity_aliases.csv"
if [ -f "$AL" ]; then ARGS+=(--aliases "$AL"); fi
ARGS+=(--test-issues "$SNAP/test_operations/grading_output/collection_issues.json")
TMP="$(mktemp -d)"
"$PY" "$REPO/IUEA_Teaching_Plan/grader/final_marks_export.py" "${ARGS[@]}" --out "$TMP/marks.xlsx"
# recalculate through LibreOffice so every viewer shows the totals
soffice -env:UserInstallation="file://$TMP/lo" --headless --convert-to xlsx --outdir "$TMP/out" "$TMP/marks.xlsx" >/dev/null 2>&1 && cp "$TMP/out/marks.xlsx" "$OUT" || cp "$TMP/marks.xlsx" "$OUT"
echo "Written: $OUT"
