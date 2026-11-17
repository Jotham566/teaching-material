/**
 * invoice_check.gs
 * KLAi | Applied AI and Automation | Session 8
 *
 * Checks a sheet of supplier invoices and writes every problem to a 'Flags' sheet.
 * Four checks, all plain arithmetic and comparison, no AI:
 *   WRONG_TOTAL  the total does not equal quantity x unit price (plus VAT)
 *   DUPLICATE    the invoice id appears twice, or the same invoice appears twice under two ids
 *   MISSING_PO   the purchase order number is blank
 *   ZERO_VAT     the VAT rate is 0 (it may be correct for exempt items, so a person decides)
 * One more flag, BAD_NUMBER, appears when a quantity, price, VAT or total cannot be read.
 *
 * Needs ai_helper.gs in the same project (run log and shared helpers).
 * The script never changes your invoice sheet. It only reads it.
 *
 * Expected columns (as in supplier_invoices.csv):
 * invoice_id, date, supplier, description, qty, unit_price_ugx, vat_pct, total_ugx, po_number
 */

// ---------------------------------------------------------------------------
// CHANGE THESE to match your own sheet
// ---------------------------------------------------------------------------
var INVOICE_SHEET_NAME = 'supplier_invoices';  // the name of the tab that holds your invoices

// The heading of each column in YOUR sheet (left side stays, change the text on the right).
var INVOICE_COLUMNS = {
  id: 'invoice_id',
  date: 'date',
  supplier: 'supplier',
  description: 'description',
  qty: 'qty',
  unit: 'unit_price_ugx',
  vat: 'vat_pct',
  total: 'total_ugx',
  po: 'po_number'
};

// true: the total on the invoice includes VAT (total = qty x price x (1 + VAT/100)).
// false: the total is before VAT. Check one real invoice and set this to match.
var TOTAL_INCLUDES_VAT = true;

// A total may differ from our calculation by this many UGX (rounding) before it is flagged.
var TOTAL_TOLERANCE_UGX = 1;

var FLAGS_SHEET_NAME = 'Flags';
var INVOICE_DRY_RUN = true;   // true: check and log only, write nothing to 'Flags'. Set false to write the flags.

// ---------------------------------------------------------------------------
// Checks (no Google services: easy to test)
// ---------------------------------------------------------------------------

/** Returns the total we expect for a row: qty x price, with VAT added if TOTAL_INCLUDES_VAT is true, rounded to a whole UGX. */
function expectedTotal(qty, unitPrice, vatPct) {
  var base = qty * unitPrice;
  if (TOTAL_INCLUDES_VAT) {
    base = base * (1 + vatPct / 100);
  }
  return Math.round(base);
}

/** Checks a list of invoice row objects and returns a list of flags {row, invoice_id, supplier, flag, detail}. Row 2 is the first invoice. */
function checkInvoices(rows) {
  var C = INVOICE_COLUMNS;
  var flags = [];
  var idSeen = {};       // invoice id -> sheet row where first seen
  var contentSeen = {};  // supplier|date|description|qty|price -> sheet row where first seen

  rows.forEach(function (row, index) {
    var sheetRow = index + 2;  // row 1 holds the headings
    var id = String(row[C.id] === undefined || row[C.id] === null ? '' : row[C.id]).trim();
    var supplier = String(row[C.supplier] === undefined ? '' : row[C.supplier]).trim();

    function addFlag(flag, detail) {
      flags.push({ row: sheetRow, invoice_id: id, supplier: supplier, flag: flag, detail: detail });
    }

    // Duplicate check (one DUPLICATE flag per row)
    var contentKey = [supplier, normaliseInvoiceDate(row[C.date]), String(row[C.description]).trim(), toNumber(row[C.qty]), toNumber(row[C.unit])].join('|');
    if (id !== '' && idSeen[id] !== undefined) {
      addFlag('DUPLICATE', 'Invoice id ' + id + ' was already used on row ' + idSeen[id] + '.');
    } else if (contentSeen[contentKey] !== undefined) {
      addFlag('DUPLICATE', 'Same supplier, date, description, quantity and price as row ' + contentSeen[contentKey] + '.');
    }
    if (id !== '' && idSeen[id] === undefined) { idSeen[id] = sheetRow; }
    if (contentSeen[contentKey] === undefined) { contentSeen[contentKey] = sheetRow; }

    // Missing PO
    var po = String(row[C.po] === undefined || row[C.po] === null ? '' : row[C.po]).trim();
    if (po === '') {
      addFlag('MISSING_PO', 'The purchase order number is blank.');
    }

    // Numbers
    var qty = toNumber(row[C.qty]);
    var unit = toNumber(row[C.unit]);
    var vat = toNumber(row[C.vat]);
    var total = toNumber(row[C.total]);
    var unreadable = [];
    if (isNaN(qty)) { unreadable.push('quantity'); }
    if (isNaN(unit)) { unreadable.push('unit price'); }
    if (isNaN(vat)) { unreadable.push('VAT'); }
    if (isNaN(total)) { unreadable.push('total'); }
    if (unreadable.length > 0) {
      addFlag('BAD_NUMBER', 'Could not read: ' + unreadable.join(', ') + '.');
      return;
    }

    // Zero VAT
    if (vat === 0) {
      addFlag('ZERO_VAT', 'VAT is 0. Confirm that the item is exempt.');
    }

    // Wrong total
    var expected = expectedTotal(qty, unit, vat);
    if (Math.abs(expected - total) > TOTAL_TOLERANCE_UGX) {
      addFlag('WRONG_TOTAL', 'Total is ' + formatNumber(total) + ' but quantity x price' +
        (TOTAL_INCLUDES_VAT ? ' plus VAT' : '') + ' is ' + formatNumber(expected) +
        ' (difference ' + formatNumber(total - expected) + ').');
    }
  });
  return flags;
}

/** Turns a date cell into yyyy-mm-dd text so that a date and the same date as text compare equal. */
function normaliseInvoiceDate(value) {
  if (Object.prototype.toString.call(value) === '[object Date]') {
    return Utilities.formatDate(value, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  }
  return String(value === undefined || value === null ? '' : value).trim().slice(0, 10);
}

/** Counts flags by type, for example {WRONG_TOTAL: 2, DUPLICATE: 1}. */
function countFlags(flags) {
  var counts = {};
  flags.forEach(function (f) { counts[f.flag] = (counts[f.flag] || 0) + 1; });
  return counts;
}

/** Writes a count like {WRONG_TOTAL: 2} as the text "WRONG_TOTAL 2, DUPLICATE 1" (or "none"). */
function describeCounts(counts) {
  var parts = Object.keys(counts).sort().map(function (k) { return k + ' ' + counts[k]; });
  return parts.length > 0 ? parts.join(', ') : 'none';
}

// ---------------------------------------------------------------------------
// The run (talks to Google services)
// ---------------------------------------------------------------------------

/** Main function: reads the invoice sheet, finds the flags, logs the run and (unless dry run) rewrites the 'Flags' sheet. */
function runInvoiceCheck() {
  var mode = INVOICE_DRY_RUN ? 'dry-run' : 'live';
  try {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = spreadsheet.getSheetByName(INVOICE_SHEET_NAME);
    if (!sheet) {
      throw new Error('There is no sheet named "' + INVOICE_SHEET_NAME + '". Check INVOICE_SHEET_NAME in invoice_check.gs.');
    }
    var rows = valuesToObjects(sheet.getDataRange().getValues());
    var flags = checkInvoices(rows);
    var summary = 'Invoices read: ' + rows.length + '. Flags: ' + flags.length + ' (' + describeCounts(countFlags(flags)) + ').';

    if (INVOICE_DRY_RUN) {
      flags.forEach(function (f) { Logger.log('Row ' + f.row + ' ' + f.invoice_id + ' ' + f.flag + ': ' + f.detail); });
      logRun('runInvoiceCheck', mode, summary + ' Nothing written to ' + FLAGS_SHEET_NAME + '.');
      return flags;
    }

    var flagsSheet = getOrCreateSheet(spreadsheet, FLAGS_SHEET_NAME);
    flagsSheet.clear();
    flagsSheet.appendRow(['row', 'invoice_id', 'supplier', 'flag', 'detail']);
    flags.forEach(function (f) {
      flagsSheet.appendRow([f.row, f.invoice_id, f.supplier, f.flag, f.detail]);
    });
    logRun('runInvoiceCheck', mode, summary + ' Written to ' + FLAGS_SHEET_NAME + '.');
    return flags;
  } catch (err) {
    logRun('runInvoiceCheck', 'error', err.message);
    throw err;
  }
}
