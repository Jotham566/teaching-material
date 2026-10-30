/** Read-only lecturer summary for Test 1 (and Test 2 via summariseTest2). Writes nothing.
 *  Uses testMonitorRows_ from Test_Monitor.js, so the numbers match the Test Monitor tab.
 *  Run summariseTest1() in the collector project and read the log. */
function summariseTest1() { summariseTest_('TEST1'); }
function summariseTest2() { summariseTest_('TEST2'); }

function summariseTest_(test) {
  var c = examConfig_();
  if (!c.bookId) { throw Error('Test collection workbook is not configured.'); }
  var book = SpreadsheetApp.openById(c.bookId);
  var read = function (name) { var s = book.getSheetByName(name); return s ? s.getDataRange().getValues() : []; };
  var rows = testMonitorRows_(read('Test allocations'), read('Collection'), read('Test windows'), Date.now());
  var total = { submitted: 0, timedOut: 0, errors: 0, inProgress: 0, notStarted: 0, other: 0 };
  Logger.log('=== ' + test + ' summary at ' + Utilities.formatDate(new Date(), 'Africa/Kampala', 'EEE d MMM HH:mm') + ' Kampala ===');
  ['CML3111', 'CML3112', 'CML3113'].forEach(function (course) {
    var set = rows.filter(function (r) { return r.key === course + '|' + test; });
    var by = function (fn) { return set.filter(fn); };
    var submitted = by(function (r) { return r.status === 'Submitted'; });
    var timedOut = by(function (r) { return r.status === 'Time expired without accepted submission'; });
    var errors = by(function (r) { return r.status === 'Submission needs attention'; });
    var inProgress = by(function (r) { return r.status === 'In progress'; });
    var notStarted = by(function (r) { return r.status === 'Not started'; });
    var other = set.length - submitted.length - timedOut.length - errors.length - inProgress.length - notStarted.length;
    Logger.log(course + ': ' + set.length + ' students | VALID SUBMISSIONS ' + submitted.length + ' | TIMED OUT (3h elapsed, nothing accepted) ' + timedOut.length
      + ' | SUBMISSION ERRORS ' + errors.length + ' | IN PROGRESS ' + inProgress.length + ' | RESET, NOT STARTED ' + notStarted.length + (other ? ' | OTHER ' + other : ''));
    var codes = {};
    errors.forEach(function (r) { var k = String(r.detail).split(':')[0] || 'UNKNOWN'; codes[k] = (codes[k] || 0) + 1; });
    Object.keys(codes).forEach(function (k) { Logger.log('    error type ' + k + ': ' + codes[k]); });
    timedOut.concat(errors).forEach(function (r) { Logger.log('    ' + r.status.slice(0, 10) + ' | ' + r.reg + ' | ' + r.email + ' | ' + String(r.detail).slice(0, 110)); });
    total.submitted += submitted.length; total.timedOut += timedOut.length; total.errors += errors.length;
    total.inProgress += inProgress.length; total.notStarted += notStarted.length; total.other += other;
  });
  Logger.log('ALL GROUPS: valid ' + total.submitted + ' | timed out ' + total.timedOut + ' | errors ' + total.errors + ' | in progress ' + total.inProgress + ' | reset, not started ' + total.notStarted);
}
