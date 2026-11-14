#!/usr/bin/env bash
# Set up (or update) the ML project collection and instant marking, almost hands-free. Safe to run again: every step checks first.
#
#   bash IUEA_Teaching_Plan/second_half/Project/deploy/setup_pipeline.sh --dry-run     shows every step, changes nothing, calls no service
#   bash IUEA_Teaching_Plan/second_half/Project/deploy/setup_pipeline.sh               does it (needs the lecturer's yes)
#
# Uses the tools already signed in on this Mac: gh (account Jotham566), clasp 3.4.1 (~/.clasprc.json) and wrangler (npx --yes wrangler,
# config IUEA_Teaching_Plan/test_portal/gateway/wrangler.jsonc). The only manual steps: paste the GitHub token once (a link opens the form
# already filled in) and approve the Google consent screen once.
# Secrets are made here and kept in ~/.iuea_pipeline_secrets (outside the repository, mode 600). They are never printed.
set -euo pipefail

DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$(dirname "$HERE")"; PLAN="$(cd "$PROJECT/../.." && pwd)"; ROOT="$(dirname "$PLAN")"
GATEWAY="$PLAN/test_portal/gateway"
PY="${PY:-$ROOT/.iuea-grader-env/bin/python}"
OWNER="${GH_OWNER:-Jotham566}"; REPO="$OWNER/iuea-ml-grading"
SECRETS="${IUEA_SECRETS:-$HOME/.iuea_pipeline_secrets}"; STATE="$HOME/.iuea_pipeline_state"; WORK="$HOME/.iuea_pipeline_work"
COLLECTOR_TITLE="IUEA ML Project Submissions"; PORTAL_TITLE="IUEA Student Test Entry"
SMOKE_REG="26/SMOKE/001/TEST"          # a made-up registration, added to the Class list for the smoke test only
DONE=()

say()  { printf '\n== %s\n' "$*"; }
step() { if (( DRY )); then printf '   [dry run] would: %s\n' "$*"; else printf '   %s\n' "$*"; fi; }
run()  { if (( DRY )); then printf '   [dry run] would run: %s\n' "$*"; else "$@"; fi; }
note() { DONE+=("$*"); }
get()  { [[ -f "$1" ]] && grep -E "^$2=" "$1" | tail -1 | cut -d= -f2- || true; }
put()  { local f="$1" k="$2" v="$3"; (( DRY )) && return 0; touch "$f"; chmod 600 "$f"; grep -vE "^$k=" "$f" > "$f.tmp" || true; printf '%s=%s\n' "$k" "$v" >> "$f.tmp"; mv "$f.tmp" "$f"; chmod 600 "$f"; }
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing tool: $1. $2"; exit 1; }; }

say "0. Checks on this Mac (nothing is changed)"
need gh "Install GitHub CLI and run gh auth login."; need npx "Install Node."; need clasp "npm install -g @google/clasp@3.4.1"; need openssl ""; need rsync ""; need curl ""
[[ -x "$PY" ]] || { echo "No grader Python at $PY (set PY=...)"; exit 1; }
[[ -f "$HOME/.clasprc.json" ]] || { echo "clasp is not signed in: run clasp login"; exit 1; }
[[ -f "$GATEWAY/wrangler.jsonc" ]] || { echo "No wrangler config at $GATEWAY/wrangler.jsonc"; exit 1; }
BOOK_ID="$(grep -oE "PORTAL_BOOK_ID = '[^']+'" "$HERE/Portal.gs" | cut -d"'" -f2)"
PORTAL_EXEC="$("$PY" -c "import json;print(json.load(open('$ROOT/data/test_portal_config.json'))['deployment_url'])")"
PORTAL_DEPLOYMENT="$(echo "$PORTAL_EXEC" | sed -E 's#.*/macros/s/([^/]+)/exec#\1#')"
PUBLIC="$("$PY" -c "import json;print(json.load(open('$ROOT/data/test_portal_config.json'))['public_url'].rstrip('/'))")"
echo "   tools found; workbook ${BOOK_ID:0:6}...; portal deployment ${PORTAL_DEPLOYMENT:0:10}...; gateway $PUBLIC"
if (( ! DRY )); then gh auth status >/dev/null 2>&1 || { echo "gh is not signed in: gh auth login"; exit 1; }; fi

say "1. Secrets (kept in $SECRETS, mode 600, outside the repository)"
for k in GATEWAY_KEY ACTIONS_SECRET BOOTSTRAP_KEY; do
  if [[ -n "$(get "$SECRETS" $k)" ]]; then echo "   $k: already made"; else step "make $k (openssl rand -hex 32)"; put "$SECRETS" $k "$(openssl rand -hex 32)"; fi
done
note "secrets in $SECRETS"

say "2. Build the files (local)"
run "$PY" "$PROJECT/tools/build_grader_spec.py"
run "$PY" "$PROJECT/tools/build_project_notebooks.py"
run "$PY" "$PROJECT/tools/build_deploy_bundle.py"
BUNDLE="$(mktemp -d)/bundle"; "$PY" "$PROJECT/actions/make_repo_bundle.py" "$BUNDLE" | sed 's/^/   /'

say "3. The private grading repository $REPO"
if (( DRY )); then step "create $REPO as PRIVATE if it does not exist (gh repo create $REPO --private)"
elif gh repo view "$REPO" >/dev/null 2>&1; then echo "   exists"
else gh repo create "$REPO" --private --description "IUEA ML project grading (private: hidden checks)" >/dev/null; echo "   created (private)"; fi
step "copy the bundle into $WORK/grading-repo, commit only if something changed, push to main"
if (( ! DRY )); then
  mkdir -p "$WORK"; [[ -d "$WORK/grading-repo/.git" ]] || git clone -q "https://github.com/$REPO.git" "$WORK/grading-repo" 2>/dev/null || { mkdir -p "$WORK/grading-repo"; git -C "$WORK/grading-repo" init -q -b main; git -C "$WORK/grading-repo" remote add origin "https://github.com/$REPO.git"; }
  rsync -a --delete --exclude .git "$BUNDLE/" "$WORK/grading-repo/"
  git -C "$WORK/grading-repo" add -A
  if ! git -C "$WORK/grading-repo" diff --cached --quiet; then git -C "$WORK/grading-repo" commit -q -m "Grading bundle $(date +%Y-%m-%d)"; git -C "$WORK/grading-repo" push -q -u origin HEAD:main; echo "   pushed"; else echo "   no change"; fi
fi
note "private repository $REPO with the grader, hidden data, sandbox and workflow"

say "4. The dispatch token (the one paste)"
if [[ -n "$(get "$SECRETS" GITHUB_TOKEN)" ]]; then echo "   already saved"
else
  URL="https://github.com/settings/personal-access-tokens/new?name=IUEA+ML+dispatch&description=Collector+sends+repository_dispatch+to+iuea-ml-grading&target_name=$OWNER&expires_in=60&contents=write"
  echo "   gh cannot create a fine-grained token. Open this link (the form is filled in), choose Repository access: Only select repositories,"
  echo "   pick iuea-ml-grading, check that Contents is Read and write, press Generate token, copy it:"
  echo "   $URL"
  if (( DRY )); then step "wait for the token to be pasted (input hidden) and save it as GITHUB_TOKEN"
  else
    (open "$URL" >/dev/null 2>&1 || true); read -rsp "   Paste the token and press Enter: " TOKEN; echo
    [[ "$TOKEN" =~ ^github_pat_[A-Za-z0-9_]{40,}$ ]] || { echo "   That does not look like a fine-grained token (github_pat_...)."; exit 1; }
    put "$SECRETS" GITHUB_TOKEN "$TOKEN"; unset TOKEN
  fi
fi

say "5. The collector web app ($COLLECTOR_TITLE)"
CDIR="$WORK/collector"; CID="$(get "$STATE" COLLECTOR_SCRIPT_ID)"; CDEP="$(get "$STATE" COLLECTOR_DEPLOYMENT)"
if (( DRY )); then step "find '$COLLECTOR_TITLE' with clasp list-scripts --noShorten, or clasp create-script --type standalone --title '$COLLECTOR_TITLE' --rootDir $CDIR"
elif [[ -z "$CID" ]]; then
  CID="$(clasp list-scripts --noShorten 2>/dev/null | grep -F "$COLLECTOR_TITLE" | grep -oE '[A-Za-z0-9_-]{40,}' | head -1 || true)"
  mkdir -p "$CDIR"
  if [[ -n "$CID" ]]; then (cd "$CDIR" && clasp clone-script "$CID" --rootDir . >/dev/null); else (cd "$CDIR" && clasp create-script --type standalone --title "$COLLECTOR_TITLE" --rootDir . >/dev/null); CID="$("$PY" -c "import json;print(json.load(open('$CDIR/.clasp.json'))['scriptId'])")"; fi
  put "$STATE" COLLECTOR_SCRIPT_ID "$CID"
fi
step "write the code and the manifest (Drive advanced service v3, web app as the lecturer, Anyone) and a one-time _bootstrap.gs (the SHA-256 of the bootstrap key only)"
if (( ! DRY )); then
  [[ -f "$CDIR/.clasp.json" ]] || (mkdir -p "$CDIR" && cd "$CDIR" && clasp clone-script "$CID" --rootDir . >/dev/null)
  find "$CDIR" -maxdepth 1 \( -name '*.js' -o -name '*.gs' -o -name '*.html' \) -delete
  cp "$HERE/ml_project_pipeline.gs" "$CDIR/ml_project_pipeline.gs"; cp "$HERE/clasp/collector.appsscript.json" "$CDIR/appsscript.json"
  HASH="$(printf '%s' "$(get "$SECRETS" BOOTSTRAP_KEY)" | openssl dgst -sha256 | awk '{print $NF}')"
  printf "var MLP_BOOTSTRAP_HASH = '%s';  // one-time, removed again by setup_pipeline.sh\n" "$HASH" > "$CDIR/_bootstrap.gs"
  (cd "$CDIR" && clasp push --force >/dev/null)
  if [[ -n "$CDEP" ]]; then (cd "$CDIR" && clasp create-deployment -i "$CDEP" -d "setup $(date +%F)" >/dev/null)
  else CDEP="$(cd "$CDIR" && clasp create-deployment -d "setup $(date +%F)" | grep -oE 'AKfy[A-Za-z0-9_-]+' | head -1)"; put "$STATE" COLLECTOR_DEPLOYMENT "$CDEP"; fi
fi
COLLECTOR_URL="https://script.google.com/macros/s/${CDEP:-<new deployment id>}/exec"
step "deployment kept the same /exec URL on every later run: $COLLECTOR_URL"
say "6. Google consent (the one approval)"
echo "   Open the collector in the editor, choose authorizeMlProject, press Run, and approve the consent screen with your Google account."
echo "   https://script.google.com/d/${CID:-<script id>}/edit"
if (( ! DRY )); then (open "https://script.google.com/d/$CID/edit" >/dev/null 2>&1 || true); read -rp "   Press Enter when it says Approved: " _; fi
step "bootstrap: POST the properties once over HTTPS (BOOK_ID, FOLDER_ID made if missing, GATEWAY_KEY, ACTIONS_SECRET, GITHUB_REPO, GITHUB_TOKEN), install the sheets, the windows rows (enabled NO) and the every-minute deadline trigger, add the smoke-test row"
if (( ! DRY )); then
  BODY="$("$PY" - "$SECRETS" "$BOOK_ID" "$REPO" "$SMOKE_REG" <<'PYEOF'
import json, sys
s = dict(l.rstrip('\n').split('=', 1) for l in open(sys.argv[1]) if '=' in l)
print(json.dumps(dict(action='bootstrap', key=s['BOOTSTRAP_KEY'], smoke_registration=sys.argv[4], properties=dict(BOOK_ID=sys.argv[2], GATEWAY_KEY=s['GATEWAY_KEY'],
      ACTIONS_SECRET=s['ACTIONS_SECRET'], GITHUB_REPO=sys.argv[3], GITHUB_TOKEN=s['GITHUB_TOKEN']))))
PYEOF
)"
  ANSWER="$(curl -sSL -X POST -H 'Content-Type: application/json' --data-binary @- "$COLLECTOR_URL" <<<"$BODY")"; unset BODY
  echo "$ANSWER" | "$PY" -c "import json,sys;a=json.load(sys.stdin);assert a.get('ok'),a;print('   properties set:',', '.join(a['result']['properties_set']));print('   ping:',a['result']['ping'])"
  rm -f "$CDIR/_bootstrap.gs"; (cd "$CDIR" && clasp push --force >/dev/null && clasp create-deployment -i "$CDEP" -d "bootstrap removed $(date +%F)" >/dev/null)
  echo "   the bootstrap file is removed again; the route now refuses"
fi
note "collector web app $COLLECTOR_URL with the deadline trigger"

say "7. GitHub repository secrets"
step "gh secret set COLLECTOR_SECRET and COLLECTOR_URL -R $REPO (values read from stdin, never on the command line)"
if (( ! DRY )); then get "$SECRETS" ACTIONS_SECRET | gh secret set COLLECTOR_SECRET -R "$REPO" >/dev/null; printf '%s' "$COLLECTOR_URL" | gh secret set COLLECTOR_URL -R "$REPO" >/dev/null; fi
note "repository secrets COLLECTOR_SECRET, COLLECTOR_URL"

say "8. The student portal ($PORTAL_TITLE)"
PDIR="$WORK/portal"; PID="$(get "$STATE" PORTAL_SCRIPT_ID)"
if (( DRY )); then step "find '$PORTAL_TITLE' with clasp list-scripts (or ask once for its script id), clone it into $PDIR (keeps every file it has, such as the Test 1 packets)"
else
  if [[ -z "$PID" ]]; then
    PID="$(clasp list-scripts --noShorten 2>/dev/null | grep -F "$PORTAL_TITLE" | grep -oE '[A-Za-z0-9_-]{40,}' | head -1 || true)"
    [[ -n "$PID" ]] || read -rp "   Script id of '$PORTAL_TITLE' (Project settings, IDs): " PID
    put "$STATE" PORTAL_SCRIPT_ID "$PID"
  fi
  rm -rf "$PDIR"; mkdir -p "$PDIR"; (cd "$PDIR" && clasp clone-script "$PID" --rootDir . >/dev/null)
fi
step "replace Portal, Gateway, PacketsMLProject, Index and ProjectIndex with the deploy/ copies, push, and redeploy the SAME deployment ${PORTAL_DEPLOYMENT:0:10}... (the /exec URL does not change)"
if (( ! DRY )); then
  for f in Portal Gateway PacketsMLProject; do rm -f "$PDIR/$f.js" "$PDIR/$f.gs"; cp "$HERE/$f.gs" "$PDIR/$f.gs"; done
  cp "$HERE/Index.html" "$PDIR/Index.html"; cp "$HERE/ProjectIndex.html" "$PDIR/ProjectIndex.html"
  (cd "$PDIR" && clasp push --force >/dev/null && clasp create-deployment -i "$PORTAL_DEPLOYMENT" -d "ML project collection $(date +%F)" >/dev/null)
fi
note "portal pushed and redeployed at the same URL"

say "9. The Cloudflare gateway"
step "copy worker.mjs, page.mjs and project_page.mjs into $GATEWAY, set the Worker secrets COLLECTOR_GATEWAY_KEY and COLLECTOR_URL (stdin), npx --yes wrangler deploy"
if (( ! DRY )); then
  cp "$HERE/gateway/worker.mjs" "$HERE/gateway/page.mjs" "$HERE/gateway/project_page.mjs" "$GATEWAY/"
  (cd "$GATEWAY" && get "$SECRETS" GATEWAY_KEY | npx --yes wrangler secret put COLLECTOR_GATEWAY_KEY --config wrangler.jsonc >/dev/null \
    && printf '%s' "$COLLECTOR_URL" | npx --yes wrangler secret put COLLECTOR_URL --config wrangler.jsonc >/dev/null && npx --yes wrangler deploy --config wrangler.jsonc >/dev/null)
fi
note "gateway deployed with /api/check, /api/backup, /api/mywork, /api/finish, /api/status"

say "10. Smoke test against the live endpoints (made-up registration $SMOKE_REG; nothing is started)"
step "GET the rehearsal entry page; POST /api/check for $SMOKE_REG; ping the collector with the Actions secret; list the workflow"
if (( ! DRY )); then
  curl -sSf "$PUBLIC/?test=CML3112%7CML_REHEARSAL" -o /dev/null && echo "   entry page: OK"
  curl -sS -X POST -H 'Content-Type: application/json' -H "Origin: $PUBLIC" --data "{\"test\":\"CML3112|ML_REHEARSAL\",\"registration\":\"$SMOKE_REG\"}" "$PUBLIC/api/check" | grep -q '"ok":true' && echo "   class list check through the gateway: OK"
  "$PY" -c "import json,sys;print(json.dumps({'action':'ping','secret':sys.argv[1]}))" "$(get "$SECRETS" ACTIONS_SECRET)" | curl -sSL -X POST -H 'Content-Type: application/json' --data-binary @- "$COLLECTOR_URL" | grep -q '"sweep_triggers":1' && echo "   collector and deadline trigger: OK"
  gh workflow list -R "$REPO" | grep -q "Grade ML project submission" && echo "   workflow present: OK"
fi

say "11. Release build of the notebooks"
step "write tools/pipeline_ready.json, rebuild with --require-forms (no DRAFT banner), rebuild the bundle, push the portal packets again"
if (( ! DRY )); then
  printf '{"collector_deployed": "%s"}\n' "$(date +%F)" > "$PROJECT/tools/pipeline_ready.json"
  "$PY" "$PROJECT/tools/build_project_notebooks.py" --require-forms >/dev/null && "$PY" "$PROJECT/tools/build_deploy_bundle.py" >/dev/null
  rm -f "$PDIR/PacketsMLProject.js" "$PDIR/PacketsMLProject.gs"; cp "$HERE/PacketsMLProject.gs" "$PDIR/"
  (cd "$PDIR" && clasp push --force >/dev/null && clasp create-deployment -i "$PORTAL_DEPLOYMENT" -d "release notebooks $(date +%F)" >/dev/null)
fi

say "Summary"
if (( DRY )); then echo "   DRY RUN: nothing was created, changed or called. Run again without --dry-run when the lecturer has approved."; echo "   A real run would set up:"; else echo "   Set up:"; fi
for d in "${DONE[@]}"; do echo "   - $d"; done
echo "   Left for you: load the class list (loadClassListFromCsv in the collector editor), one Colab dry run with the rehearsal link,"
echo "   and on 22 November openMlProjectWindow('ALL','2026-11-23T00:00:00+03:00','2026-11-25T23:59:00+03:00','CONFIRMED')."
