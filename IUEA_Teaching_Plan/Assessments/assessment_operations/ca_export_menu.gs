/** @OnlyCurrentDoc
 * Bind this small script to the assignment collection spreadsheet.
 * The existing lecturer-owned exporter processes requests; no Drive access here.
 */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Export Grading ZIP')
    .addItem('Start / resume export', 'requestGradingZip')
    .addItem('View progress / download', 'showGradingZipProgress')
    .addToUi();
}
function showGradingZipProgress() {
  var book = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = book.getSheetByName('CA Export');
  if (!sheet) throw Error('CA Export is not configured.');
  book.setActiveSheet(sheet);
  sheet.getRange('A1').activate();
}
function requestGradingZip() {
  var lock = LockService.getDocumentLock();
  if (!lock.tryLock(5000)) throw Error('Another export request is being saved. Try again shortly.');
  try {
    var book = SpreadsheetApp.getActiveSpreadsheet(), sheet = book.getSheetByName('CA Export');
    if (!sheet) throw Error('CA Export is not configured.');
    var requestStatus = String(sheet.getRange('E2').getValue());
    if (sheet.getRange('B1').getValue() === 'RUNNING') {
      book.toast('An export is already running. Check its progress below.', 'Export Grading ZIP', 8);
    } else if (requestStatus === 'PENDING') {
      book.toast('Your request is already queued. Google will start it shortly.', 'Export Grading ZIP', 8);
    } else {
      sheet.getRange('D1:E3').setValues([
        ['Export request', Utilities.getUuid()],
        ['Request status', 'PENDING'],
        ['Requested at', new Date().toISOString()]
      ]);
      SpreadsheetApp.flush();
      book.toast('Export queued. Check CA Export for progress and the download link. Allow about a minute to start.', 'Export Grading ZIP', 10);
    }
    showGradingZipProgress();
  } finally { lock.releaseLock(); }
}
