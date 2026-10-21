#!/bin/zsh
set -eu
cd "$(dirname "$0")/../.."
private="IUEA_Teaching_Plan/assessment_operations/private"
if [[ -d "$private/reconciled_20261020" ]]; then
  print "This snapshot has been refreshed. The old queue inputs must not replace the newer results."
  print "Check refresh_status.json and the updated workbook. Use the documented refresh process for new submissions."
  exit 0
fi
if pgrep -f '[f]inish_ca_refresh.py' >/dev/null; then
  print "The snapshot refresh is already running. Do not start a second grading queue."
  exit 1
fi
if pgrep -f '[r]un_ca_written_queue.py' >/dev/null; then
  print "Written grading is already running. Do not start a second copy."
  exit 1
fi
print "Resume grading the downloaded snapshot. This does not fetch new submissions."
print "Keep this Mac powered. Close memory-heavy applications first."
print "Progress: $private/written_queue/queue_status.json"
caffeinate -i .iuea-grader-env/bin/python \
  IUEA_Teaching_Plan/grader/run_ca_written_queue.py \
  --source "$private/reconciled" \
  --ledger "$private/grading_input.json" \
  --coding "$private/notebook_grades/identity_checked_results.json" \
  --prepared "$private/written_text/prepared.json" \
  --w1-calibration "$private/W01_calibration_isolated.json" \
  --w2-calibration review/2026-09-14/rework/local_calibration_v10.json \
  --out "$private/written_queue" \
  >> "$private/written_queue.log" 2>&1
print "Queue finished. Check pending statuses in the private workbook."
