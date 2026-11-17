# Student test entry gateway

Status: the Cloudflare Worker deployed on 19 October 2026 remains live at https://iuea-test-entry.jothammartin-wambi.workers.dev/. The existing Apps Script endpoint now serves deployment version 22 (published 29 October 2026), including allocated-email notebook metadata and the Colab account preflight. On 4 November, Test 2 was withdrawn and replaced by the Engineering ML final project. The current Worker source and portal accept Test 1 only and return HTTP 410 for Test 2, but these source changes have **not** been deployed; do not share the old Test 2 links.

Students open one ordinary HTTPS address from a QR or clickable link. The page sends requests only to `/api/files` on the same host. The Worker forwards the request to Apps Script from the server without forwarding browser cookies. Google account selection therefore does not run in the student's browser during file retrieval. Colab and final Google Forms submission still require the student's own Google account.

## What remains enforced

`Gateway.gs` calls the existing `requestTestFiles` function. It keeps the private workbook, exact test windows, freeform required Student Registration Number, stable allocation, and matching notebook/CSV. The response is never cached. No marks, private workbook contents or administrative actions are exposed. The gateway secret stays in Cloudflare Secrets and Apps Script Script Properties, never in the page, source repository or QR.

Students' submitted name, email and registration number, and the returned test packet, pass through Cloudflare to/from the lecturer's Apps Script. The Worker code does not persist or log them; platform processing is subject to Cloudflare's terms. Keep observability disabled for this deployment. Do not enable a paid plan or add billing resources for this workflow.

## Deployment checklist

1. Use the lecturer's Cloudflare account on Workers Free. Account creation and acceptance of terms are the lecturer's actions. Confirm approval for the stated data flow before publication.
2. Create a strong random gateway secret locally. Set the same value in Apps Script Script Properties as `PORTAL_GATEWAY_KEY` and Cloudflare Worker Secrets as `PORTAL_GATEWAY_KEY`. Never print it, put it in a URL, or commit it. Local `.dev.vars` files are ignored.
3. Add `Gateway.gs` to the separate **IUEA Student Test Entry** Apps Script project. Do not add it to the collector project. Publish a new version of the original deployment, keeping execution as the lecturer and access Anyone. Keep all real test windows unchanged.
4. From this folder deploy `worker.mjs` with the adjacent `wrangler.jsonc`, on Workers Free. Its server-side `APPS_SCRIPT_URL` must be the original Apps Script `/exec` URL. Use the assigned workers.dev address; no domain purchase is needed.
5. Test all three Test 1 routes in an ordinary browser with multiple Google accounts signed in. Verify Test 2 routes return HTTP 410. Verify early, expired and disabled requests return no notebook or CSV. Use a separately authorised rehearsal window for live successful downloads; do not extend real windows for testing.
6. Verify both download buttons and their contents, stable repeated allocations and the existing notebook-to-form submission flow. Confirm no identity data or download responses are cached.
7. Only after live verification, run `python3 scripts/configure_test_portal.py ORIGINAL_APPS_SCRIPT_URL --public-url VERIFIED_GATEWAY_URL` from the repository root. Rebuild the three active Test 1 decks with the existing generators and review their access slides. The final project has a separate `ML_PROJECT` deployment bundle. Republish the link index and guides together. QR and visible clickable URL must point to the same course/test page on the new host.

The old Apps Script links remain usable as a fallback but retain Google's account-routing limitation. Publishing a gateway does not update already-shared PowerPoint copies; distribute the updated decks/links.

## Local verification

From the repository root:

```
python3 scripts/build_test_gateway.py
node tests/test_test_gateway.mjs
node tests/test_test_portal.cjs
```

The gateway tests run its real handler through `Gateway.gs` and the real portal allocation code with an in-memory workbook. They cover three Test 1 pages, all nine active packets, Test 2 rejection, repeat allocations, opening/deadline/disabled checks, missing/wrong secrets, malformed requests, upstream failures and prevention of browser-cookie forwarding. They do not establish that an undeployed public URL works.

## Live verification — 19 October 2026

The six-route and 18-packet browser and local checks above were completed before Test 2 was withdrawn. The current source's three Test 1 routes and nine packets are covered by the gateway tests; those tests also verify HTTP 410 retirement for Test 2. A later authorised CML3111 Test 1 rehearsal completed both live Cloudflare downloads, Colab execution, form submission, verified collection and Docker batch grading at 100/100. See the current rehearsal record in ../README.md. Physical phone-camera scanning was not performed; QR payloads are decoded independently and their destination is checked.
