// A local stand-in for the online pieces, with NO network: the student portal (deploy/Portal.gs, Gateway.gs, PacketsMLProject.gs), the
// collector (deploy/ml_project_pipeline.gs) and the Cloudflare gateway (deploy/gateway/worker.mjs). The REAL files run here, unchanged, on
// in-memory fakes of Sheets, Drive (files, permissions, revisions with modifiedTime), Properties, triggers and UrlFetch. GitHub's
// repository_dispatch is recorded, not sent.
//
//   node local_stack.mjs <port>     the gateway is http://127.0.0.1:<port>/ and the collector web app is /collector
// Admin routes, for the tests only (they stand in for Colab, Drive and the time trigger):
//   POST /admin/setup {open, close, classList}      fresh workbook          POST /admin/clock {offset_ms}     move the clock
//   POST /admin/save {file, email, notebook}        a Colab autosave by that Google account (refused without edit rights)
//   POST /admin/copy {file, email}                  "Save a copy in Drive" by that account; returns the new file id
//   POST /admin/sweep                               the every-minute trigger      POST /admin/extend {who, minutes, reason}
//   POST /admin/release   POST /admin/classlist {csv, cohort}   GET /admin/state   GET /admin/export (the real exportMlProjectBatch)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const deploy = path.join(here, '..', 'deploy');
const port = Number(process.argv[2] || 8787);
const SECRETS = { portalGateway: crypto.randomBytes(24).toString('hex'), collectorGateway: crypto.randomBytes(24).toString('hex'),
  actions: process.env.COLLECTOR_SECRET || crypto.randomBytes(24).toString('hex') };
const PORTAL_URL = 'https://script.google.com/macros/s/LOCALPORTAL/exec', COLLECTOR_URL = 'https://script.google.com/macros/s/LOCALCOLLECTOR/exec';
let offset = 0;
class Clock extends Date { constructor(...a) { if (a.length) super(...a); else super(Date.now() + offset); } static now() { return Date.now() + offset; } }
const nowIso = () => new Clock().toISOString();

// ---------------------------------------------------------------- fakes shared by both Apps Script projects (one workbook, one Drive)
const signed = buf => [...buf].map(x => x > 127 ? x - 256 : x);
const unsigned = bytes => Buffer.from(bytes.map(x => (x + 256) % 256));
function blob(data, mime, name) {
  const buf = typeof data === 'string' ? Buffer.from(data, 'utf8') : Array.isArray(data) ? unsigned(data) : Buffer.from(data);
  return { buf, getBytes: () => signed(buf), getDataAsString: () => buf.toString('utf8'), setName(n) { this.name = n; return this; }, name, getName() { return this.name; } };
}
function makeSheet(rows) {
  const s = { rows,
    getDataRange: () => ({ getValues: () => s.rows.map(r => r.slice()) }), getLastRow: () => s.rows.length,
    appendRow: r => { s.rows.push(r.slice()); }, setFrozenRows() {}, clearContents: () => { s.rows.length = 0; },
    getRange: (r, c, h = 1, w = 1) => ({ getValues: () => s.rows.slice(r - 1, r - 1 + h).map(x => x.slice(c - 1, c - 1 + w)),
      setValues: v => v.forEach((row, i) => row.forEach((x, j) => { s.rows[r - 1 + i] ??= []; s.rows[r - 1 + i][c - 1 + j] = x; })),
      setRichTextValues(v) { this.setValues(v); }, setValue(v) { this.setValues([[v]]); }, setNumberFormat() {} }) };
  return s;
}
const sheets = {};
const book = { getSheetByName: n => sheets[n] || null, insertSheet: n => (sheets[n] = makeSheet([])), getUrl: () => 'local-book' };
const files = {}, dispatches = [], zips = [];
let fileCount = 0;
function newFile(b, owner) {
  const id = 'file' + String(++fileCount).padStart(10, '0');
  files[id] = { owner, perms: [], revisions: [{ id: 'r1', modifiedTime: nowIso(), text: b.getDataAsString() }], zip: b.zip || null };
  return fileApi(id);
}
function fileApi(id) {
  const f = files[id]; if (!f) throw Error('No file ' + id);
  const latest = () => f.revisions[f.revisions.length - 1];
  return { getId: () => id, getBlob: () => blob(latest().text), getLastUpdated: () => new Clock(latest().modifiedTime), getSize: () => Buffer.byteLength(latest().text),
    setContent: t => { f.revisions.push({ id: 'r' + (f.revisions.length + 1), modifiedTime: nowIso(), text: t }); } };
}
const DriveApp = { createFolder: () => ({ getId: () => 'folder' }), getFolderById: () => ({ createFile: b => newFile(b, 'lecturer') }), getFileById: id => fileApi(id) };
const Drive = {
  Permissions: { list: id => ({ permissions: files[id].perms.map((p, i) => ({ id: 'p' + i, emailAddress: p.email, role: p.role })) }),
    update: (res, id, pid) => { files[id].perms[Number(pid.slice(1))].role = res.role; },
    create: (res, id) => { files[id].perms.push({ email: res.emailAddress.toLowerCase(), role: res.role }); } },
  Revisions: { list: id => ({ revisions: files[id].revisions.map(r => ({ id: r.id, modifiedTime: r.modifiedTime })) }) } };
const Utilities = { getUuid: () => crypto.randomUUID(), newBlob: blob, sleep() {},
  formatDate: d => new Date(new Date(d).getTime() + 3 * 3600000).toISOString().replace('T', ' ').slice(0, 19),
  computeDigest: (_, bytes) => signed(crypto.createHash('sha256').update(unsigned(bytes)).digest()), DigestAlgorithm: { SHA_256: 'sha256' },
  computeHmacSha256Signature: (v, k) => signed(crypto.createHmac('sha256', k).update(v).digest()),
  base64EncodeWebSafe: b => unsigned(b).toString('base64').replace(/\+/g, '-').replace(/\//g, '_'),
  parseCsv: t => t.trim().split(/\r?\n/).map(l => l.split(',')),
  zip: (blobs, name) => { const z = blob('zip', 'application/zip', name); z.zip = blobs.map(b => ({ name: b.getName(), text: b.getDataAsString() })); zips.push(z.zip); return z; } };
const lock = { tryLock: () => true, waitLock() {}, releaseLock() {} };
const ContentService = { createTextOutput: t => ({ text: t, setMimeType() { return this; } }), MimeType: { JSON: 'json' } };
const triggers = [];
function project(fileNames, props) {
  const ctx = { Date: Clock, Math, JSON, console: { log() {} }, Object, Array, Error, Number, String, isFinite, parseInt, Boolean, RegExp, Set,
    SpreadsheetApp: { openById: () => book, newRichTextValue: () => ({ setText(v) { this.v = v; return this; }, build() { return this.v; } }) },
    LockService: { getScriptLock: () => lock },
    PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] ?? null, setProperty: (k, v) => { props[k] = String(v); }, deleteProperty: k => { delete props[k]; } }) },
    Utilities, DriveApp, Drive, ContentService, Session: { getEffectiveUser: () => ({ getEmail: () => 'lecturer@example.org' }) },
    ScriptApp: { getOAuthToken: () => 'local-only', getProjectTriggers: () => triggers.map(t => ({ getHandlerFunction: () => t })),
      newTrigger: fn => ({ timeBased: () => ({ everyMinutes: () => ({ create: () => triggers.push(fn) }) }) }) },
    UrlFetchApp: { fetch: (url, options = {}) => {
      if (url.startsWith('https://api.github.com/repos/')) { dispatches.push({ url, payload: JSON.parse(options.payload) }); return { getResponseCode: () => 204 }; }
      let m = /drive\/v3\/files\/([^/?]+)\/permissions/.exec(url);
      if (m) { const b = JSON.parse(options.payload); files[m[1]].perms.push({ email: b.emailAddress.toLowerCase(), role: b.role }); return { getResponseCode: () => 200 }; }
      m = /drive\/v3\/files\/([^/?]+)\/revisions\/([^/?]+)\?alt=media/.exec(url);
      if (m) { const r = files[m[1]].revisions.find(x => x.id === m[2]); return { getResponseCode: () => r ? 200 : 404, getContentText: () => r.text }; }
      if (/drive\/v3\/files\/[^/?]+$/.test(url)) return { getResponseCode: () => 200 };   // writersCanShare
      throw Error('no network in the local stack: ' + url);
    } },
    HtmlService: { createHtmlOutput: m => ({ m }), createTemplateFromFile: () => ({ evaluate: () => ({ setTitle() { return this; }, addMetaTag() { return this; } }) }) } };
  vm.createContext(ctx);
  for (const f of fileNames) vm.runInContext(fs.readFileSync(path.join(deploy, f), 'utf8'), ctx, { filename: f });
  return ctx;
}
const portalProps = { PORTAL_GATEWAY_KEY: SECRETS.portalGateway };
const collectorProps = { BOOK_ID: 'book', FOLDER_ID: 'folder', GATEWAY_KEY: SECRETS.collectorGateway, ACTIONS_SECRET: SECRETS.actions,
  GITHUB_REPO: 'Jotham566/iuea-ml-grading', GITHUB_TOKEN: 'never-a-real-token' };
const portal = project(['Portal.gs', 'Gateway.gs', 'PacketsMLProject.gs'], portalProps);
vm.runInContext('var PORTAL_PACKETS = {};', portal);
const collector = project(['ml_project_pipeline.gs'], collectorProps);
const { handle } = await import(path.join(deploy, 'gateway', 'worker.mjs'));
const env = { PORTAL_GATEWAY_KEY: SECRETS.portalGateway, APPS_SCRIPT_URL: PORTAL_URL, COLLECTOR_GATEWAY_KEY: SECRETS.collectorGateway, COLLECTOR_URL };
const upstream = async (url, init) => {
  const target = url === PORTAL_URL ? portal : url === COLLECTOR_URL ? collector : null;
  if (!target) throw Error('no network in the local stack: ' + url);
  return new Response(target.doPost({ postData: { contents: init.body } }).text, { status: 200, headers: { 'Content-Type': 'application/json' } });
};

function setup(body) {
  for (const k of Object.keys(sheets)) delete sheets[k];
  sheets['Test allocations'] = makeSheet([['assessment_key', 'registration_normalized', 'email', 'allocation_code', 'variant', 'created_at', 'full_name', 'started_at', 'personal_deadline', 'notebook_id', 'window_opens_at', 'working_mode']]);
  sheets['Test windows'] = makeSheet([['assessment_key', 'opens_at', 'closes_at', 'enabled', 'duration_minutes']].concat(
    ['CML3111', 'CML3112', 'CML3113'].flatMap(c => [[c + '|ML_PROJECT', body.open, body.close, 'YES', 180], [c + '|ML_REHEARSAL', body.open, body.close, 'YES', 180]])));
  sheets['Class list'] = makeSheet([['cohort', 'registration', 'full_name']].concat(body.classList));
  vm.runInContext('installMlProjectPipeline()', collector);
  return { ok: true, triggers: triggers.length };
}
const read = req => new Promise(ok => { const parts = []; req.on('data', c => parts.push(c)); req.on('end', () => ok(Buffer.concat(parts).toString())); });
const send = (res, status, value) => { res.writeHead(status, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(value)); };
const run = (ctx, code) => vm.runInContext(code, ctx);

http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://127.0.0.1:${port}`);
    if (url.pathname === '/collector') return send(res, 200, JSON.parse(collector.doPost({ postData: { contents: await read(req) } }).text));
    if (url.pathname.startsWith('/admin/')) {
      const body = req.method === 'POST' ? JSON.parse((await read(req)) || '{}') : {};
      switch (url.pathname) {
        case '/admin/setup': return send(res, 200, setup(body));
        case '/admin/clock': offset = Number(body.offset_ms) || 0; return send(res, 200, { ok: true, now: nowIso() });
        case '/admin/save': {
          const f = files[body.file], who = String(body.email).toLowerCase();
          const can = f && (f.owner === who || f.perms.some(p => p.email === who && p.role === 'writer'));
          if (!can) return send(res, 403, { ok: false, error: 'Colab: you do not have permission to save this notebook' });
          f.revisions.push({ id: 'r' + (f.revisions.length + 1), modifiedTime: nowIso(), text: body.notebook });
          return send(res, 200, { ok: true, revisions: f.revisions.length });
        }
        case '/admin/copy': {
          const f = files[body.file], who = String(body.email).toLowerCase();
          if (!f || !(f.perms.some(p => p.email === who) || f.owner === who)) return send(res, 403, { ok: false });
          const copy = newFile(blob(f.revisions.at(-1).text), who);
          return send(res, 200, { ok: true, file: copy.getId() });
        }
        case '/admin/sweep': return send(res, 200, { ok: true, collected: run(collector, 'mlpSweep()') });
        case '/admin/extend': collector.__x = body; return send(res, 200, { ok: true, changed: run(collector, 'extendMlProject(__x.who, __x.minutes, __x.reason)') });
        case '/admin/fresh': collector.__f = body; return send(res, 200, { ok: true, changed: run(collector, 'freshMlProjectAttempt(__f.registration, __f.reason, __f.email)') });
        case '/admin/release': run(collector, 'releaseMlProjectMarks("RELEASE")'); return send(res, 200, { ok: true });
        case '/admin/classlist': {
          const id = newFile(blob(body.csv), 'lecturer').getId(); collector.__c = { id, cohort: body.cohort || '' };
          run(collector, 'loadClassListFromCsv(__c.id, __c.cohort)'); return send(res, 200, { ok: true, rows: sheets['Class list'].rows });
        }
        case '/admin/state': return send(res, 200, { dispatches, triggers, collection: sheets['Collection']?.rows || [], checks: sheets['Instant checks']?.rows || [],
          states: sheets['Attempt state']?.rows || [], allocations: sheets['Test allocations']?.rows || [], extensions: sheets['Extensions']?.rows || [],
          windows: sheets['Test windows']?.rows || [], perms: Object.fromEntries(Object.entries(files).map(([k, f]) => [k, f.perms])) });
        case '/admin/export': run(collector, 'exportMlProjectBatch()'); return send(res, 200, { ok: true, files: zips.at(-1) });
        default: return send(res, 404, { ok: false });
      }
    }
    // everything else is the gateway, exactly as Cloudflare would run it
    const body = req.method === 'POST' ? await read(req) : undefined;
    const answer = await handle(new Request(url, { method: req.method, headers: req.headers, body }), env, upstream);
    res.writeHead(answer.status, Object.fromEntries(answer.headers));
    res.end(Buffer.from(await answer.arrayBuffer()));
  } catch (error) { send(res, 500, { ok: false, error: String(error && error.stack || error).slice(0, 1200) }); }
}).listen(port, '127.0.0.1', () => console.log('LOCAL STACK READY ' + port));
