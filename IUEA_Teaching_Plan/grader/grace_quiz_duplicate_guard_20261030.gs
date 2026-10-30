/**
 * One-off 30 Oct 2026: registration reminder + duplicate guard for quizzes 1-5 (CML3111/2/3).
 * Forms already allow one response per Google account. This also stops a second response with the
 * same registration number from another account: the earliest response is kept, and any later
 * one submitted during the grace period is deleted (logged first). Older data is never touched.
 * Run installGraceQuizGuard_20261030 once.
 */
var GRACE_GUARD_FROM_ = Date.parse('2026-10-30T17:40:00+03:00');
var GRACE_GUARD_END_ = Date.parse('2026-11-03T06:00:00+03:00');
var GRACE_QUIZ_REMINDER_ = '\u26A0 CHECK YOUR REGISTRATION NUMBER before you submit: it must match your student card exactly, or your mark cannot reach your record.\n'
  + 'ALREADY TAKEN THIS QUIZ? Do NOT submit again. A second response with the same registration number is deleted; your first one stands.\n\n';

function graceQuizItems_(form) {
  return form.getItems(FormApp.ItemType.TEXT).filter(function (it) { return /registration|student (number|id)/i.test(it.getTitle()); });
}

function installGraceQuizGuard_20261030() {
  var links = loadLinks_(), n = 0;
  ['CML3111', 'CML3112', 'CML3113'].forEach(function (c) {
    [1, 2, 3, 4, 5].forEach(function (w) {
      var L = links[c + '|' + w]; if (!L) { throw Error('Missing ' + c + '|' + w); }
      var f = FormApp.openById(L.formId);
      var desc = f.getDescription().replace(/\u26A0 CHECK YOUR REGISTRATION NUMBER[\s\S]*?your first one stands\.\n\n/, '');
      var m = desc.match(/^GRACE PERIOD:.*\n\n/);
      f.setDescription(m ? m[0] + GRACE_QUIZ_REMINDER_ + desc.slice(m[0].length) : GRACE_QUIZ_REMINDER_ + desc);
      graceQuizItems_(f).forEach(function (it) {
        var t = it.asTextItem(), h = t.getHelpText().replace(/ \u26A0 Double-check.*$/, '');
        t.setHelpText(h + ' \u26A0 Double-check this number before submitting.');
      });
      n++;
    });
  });
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'guardGraceQuizDuplicates_20261030') { ScriptApp.deleteTrigger(t); } });
  Logger.log('Project triggers before install: ' + ScriptApp.getProjectTriggers().length + ' (limit 20)');
  ScriptApp.newTrigger('guardGraceQuizDuplicates_20261030').timeBased().everyMinutes(5).create();
  Logger.log('Reminder added to ' + n + ' quiz forms; duplicate guard runs every 5 minutes.');
  guardGraceQuizDuplicates_20261030();
}

function guardGraceQuizDuplicates_20261030() {
  if (Date.now() > GRACE_GUARD_END_) {
    ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'guardGraceQuizDuplicates_20261030') { ScriptApp.deleteTrigger(t); } });
    return;
  }
  var links = loadLinks_();
  ['CML3111', 'CML3112', 'CML3113'].forEach(function (c) {
    [1, 2, 3, 4, 5].forEach(function (w) {
      var L = links[c + '|' + w]; if (!L) { return; }
      var f = FormApp.openById(L.formId), items = graceQuizItems_(f);
      if (!items.length) { return; }
      var first = {};
      f.getResponses().forEach(function (r) {
        var ir = r.getResponseForItem(items[0]); if (!ir) { return; }
        var reg = String(ir.getResponse()).replace(/\s+/g, '').toUpperCase(); if (!reg) { return; }
        if (!first[reg]) { first[reg] = r; return; }
        if (r.getTimestamp().getTime() < GRACE_GUARD_FROM_) { return; }
        Logger.log('DUPLICATE REMOVED ' + c + '|Q' + w + ' reg=' + reg + ' by=' + r.getRespondentEmail() + ' at=' + r.getTimestamp().toISOString() + ' score=' + r.getGradableResponses().length + ' kept=' + first[reg].getRespondentEmail());
        f.deleteResponse(r.getId());
      });
    });
  });
}
