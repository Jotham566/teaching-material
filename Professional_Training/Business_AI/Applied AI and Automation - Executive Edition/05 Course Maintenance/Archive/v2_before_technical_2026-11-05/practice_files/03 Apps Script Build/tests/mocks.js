'use strict';
// Hand-written mocks of the Google services used by the .gs files.
// They keep everything in memory and record every call, so tests can check what happened.
// No network is used anywhere.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

/** Reads a small CSV file into a 2D array. Numbers become numbers, as Google Sheets would give them. */
function readCsvValues(file) {
  const text = fs.readFileSync(file, 'utf8').replace(/\r/g, '').trim();
  const lines = text.split('\n');
  const parse = (line) => {
    const cells = [];
    let cur = '';
    let quoted = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') { quoted = !quoted; }
      else if (ch === ',' && !quoted) { cells.push(cur); cur = ''; }
      else { cur += ch; }
    }
    cells.push(cur);
    return cells;
  };
  const rows = lines.map(parse);
  return rows.map((row, r) => row.map((cell) => {
    if (r === 0) return cell;
    if (cell !== '' && /^-?\d+(\.\d+)?$/.test(cell) && !/^0\d/.test(cell)) return Number(cell);
    return cell;
  }));
}

/** Builds a fresh set of mocks and returns { mocks, state }. */
function createMocks() {
  const state = {
    sheets: {},          // name -> { name, data }
    drafts: [],          // GmailApp.createDraft calls
    sentEmails: [],      // GmailApp.sendEmail calls (must stay empty)
    fetchCalls: [],      // UrlFetchApp.fetch calls
    fetchResponder: null,
    properties: {},      // Script Properties
    triggers: [],        // live triggers
    deletedTriggers: 0,
    logLines: [],        // Logger.log lines
    userEmail: 'owner@example.com',
    timeZone: 'Africa/Kampala'
  };

  function makeSheet(name, data) {
    const sheet = { name: name, data: data ? data.map((r) => r.slice()) : [] };
    sheet.getName = () => sheet.name;
    sheet.getLastRow = () => sheet.data.length;
    sheet.getDataRange = () => ({
      getValues: () => {
        const width = sheet.data.reduce((m, r) => Math.max(m, r.length), 0);
        return sheet.data.map((r) => {
          const copy = r.slice();
          while (copy.length < width) copy.push('');
          return copy;
        });
      }
    });
    sheet.clear = () => { sheet.data = []; return sheet; };
    sheet.appendRow = (row) => { sheet.data.push(row.slice()); return sheet; };
    sheet.getRange = (r, c, nr, nc) => ({
      setValues: (values) => {
        for (let i = 0; i < nr; i++) {
          while (sheet.data.length < r - 1 + i + 1) sheet.data.push([]);
          for (let j = 0; j < nc; j++) sheet.data[r - 1 + i][c - 1 + j] = values[i][j];
        }
      }
    });
    state.sheets[name] = sheet;
    return sheet;
  }

  const spreadsheet = {
    getSheetByName: (name) => state.sheets[name] || null,
    insertSheet: (name) => makeSheet(name, []),
    getSpreadsheetTimeZone: () => state.timeZone
  };

  const SpreadsheetApp = { getActiveSpreadsheet: () => spreadsheet };

  const GmailApp = {
    createDraft: (to, subject, body) => { state.drafts.push({ to, subject, body }); return {}; },
    sendEmail: (to, subject, body) => { state.sentEmails.push({ to, subject, body }); }
  };

  const UrlFetchApp = {
    fetch: (url, params) => {
      state.fetchCalls.push({ url, params });
      if (state.fetchResponder) return state.fetchResponder(url, params);
      throw new Error('No fetch responder set in this test: a network call was attempted.');
    }
  };

  const PropertiesService = {
    getScriptProperties: () => ({
      getProperty: (k) => (Object.prototype.hasOwnProperty.call(state.properties, k) ? state.properties[k] : null),
      setProperty: (k, v) => { state.properties[k] = v; }
    })
  };

  const Logger = { log: (text) => { state.logLines.push(String(text)); } };

  const ScriptApp = {
    WeekDay: { MONDAY: 'MONDAY', TUESDAY: 'TUESDAY', FRIDAY: 'FRIDAY' },
    getProjectTriggers: () => state.triggers.slice(),
    deleteTrigger: (t) => {
      const i = state.triggers.indexOf(t);
      if (i >= 0) { state.triggers.splice(i, 1); state.deletedTriggers++; }
    },
    newTrigger: (handler) => {
      const spec = { handler: handler, kind: null, weekday: null, hour: null };
      const builder = {
        timeBased: () => { spec.kind = 'time'; return builder; },
        onWeekDay: (d) => { spec.weekday = d; return builder; },
        atHour: (h) => { spec.hour = h; return builder; },
        create: () => {
          const trigger = { getHandlerFunction: () => spec.handler, spec: spec };
          state.triggers.push(trigger);
          return trigger;
        }
      };
      return builder;
    }
  };

  const pad = (n) => String(n).padStart(2, '0');
  const Utilities = {
    // Formats in UTC only. Enough for the 'yyyy-MM-dd' pattern used by the scripts.
    formatDate: (date, tz, pattern) => {
      if (pattern !== 'yyyy-MM-dd') throw new Error('mock supports only yyyy-MM-dd');
      return date.getUTCFullYear() + '-' + pad(date.getUTCMonth() + 1) + '-' + pad(date.getUTCDate());
    }
  };

  const Session = {
    getScriptTimeZone: () => state.timeZone,
    getEffectiveUser: () => ({ getEmail: () => state.userEmail })
  };

  return {
    state,
    makeSheet,
    mocks: { SpreadsheetApp, GmailApp, UrlFetchApp, PropertiesService, Logger, ScriptApp, Utilities, Session }
  };
}

/** Builds a vm context with the mocks and the three .gs files loaded, as Apps Script would load them in one project. */
function loadProject(rootDir) {
  const env = createMocks();
  const context = vm.createContext(Object.assign({}, env.mocks, { console: console }));
  ['ai_helper.gs', 'weekly_digest.gs', 'invoice_check.gs'].forEach((file) => {
    const code = fs.readFileSync(path.join(rootDir, file), 'utf8');
    vm.runInContext(code, context, { filename: file });
  });
  env.context = context;
  /** Runs a small piece of code inside the project, for example "DIGEST_DRY_RUN = false". */
  env.run = (code) => vm.runInContext(code, context);
  /** Puts a fixture CSV into a sheet with this name. */
  env.loadSheet = (name, csvFile) => env.makeSheet(name, readCsvValues(csvFile));
  /** Gives a fake successful Gemini reply. */
  env.fakeGeminiOk = (text) => {
    env.state.fetchResponder = () => ({
      getResponseCode: () => 200,
      getContentText: () => JSON.stringify({ candidates: [{ content: { parts: [{ text: text }] } }] })
    });
  };
  return env;
}

module.exports = { loadProject, readCsvValues };
