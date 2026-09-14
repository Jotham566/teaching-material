# -*- coding: utf-8 -*-
"""Generate the projected quiz countdown.

WHY NOT A TIMER INSIDE THE FORM
Google Forms has no countdown and no auto-submit, in 2026 as before. Every
add-on that adds one works by hosting your form on the add-on's own site,
which would break the forms.gle links the QR codes point at, put a graded
assessment behind a third party, and meter it: a hundred students times
twelve sittings is well past any free tier.

A projected clock is also the better match for how this quiz actually runs.
The class starts together on your word, so one clock everybody can see is
the honest model. Per-student timers would only matter for an asynchronous
quiz, and this one is not.

This clock counts the five minutes students are given, which is when the
quiz is meant to be taken. The form itself stays open for 48 hours after
that, so a failed network in Room 106 does not cost anybody a mark. Both
numbers are stated on the form.

Single file, no network, no fonts to load. Opens in any browser, works
offline, and is big enough to read from the back of a lecture hall.
"""
import io
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

OUT = _ROOT + "/IUEA_Teaching_Plan/quiz_timer.html"

# The five minutes students are given, and what this clock counts. The form
# then stays open for WINDOW_HOURS (48) so a failed network does not cost a
# mark. Keep in step with QUIZ_MIN in build_quiz_forms_gs.py and
# QUIZ_MIN_ON_CLOCK in the Apps Script.
WINDOW_MIN = 5

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IUEA quiz timer</title>
<style>
  :root { color-scheme: light }
  * { box-sizing: border-box; margin: 0; padding: 0 }
  body {
    background: #1C3144; color: #F4F7FA; height: 100vh;
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; overflow: hidden;
    font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-user-select: none; user-select: none;
  }
  #kicker {
    letter-spacing: .18em; text-transform: uppercase;
    font-size: clamp(12px, 1.6vw, 22px); font-weight: 700;
    color: #E4572E; margin-bottom: 1vh;
  }
  #clock {
    font-variant-numeric: tabular-nums; font-weight: 700;
    font-size: min(38vw, 62vh); line-height: .95;
    letter-spacing: -.02em; transition: color .3s;
  }
  #msg {
    font-size: clamp(14px, 2.2vw, 34px); color: #B8C9D8;
    margin-top: 1vh; text-align: center; padding: 0 4vw;
  }
  #controls { margin-top: 4vh; display: flex; gap: 1.2vw; flex-wrap: wrap;
              justify-content: center }
  button {
    font: inherit; font-size: clamp(12px, 1.3vw, 19px); font-weight: 600;
    padding: .7em 1.4em; border-radius: .4em; border: 2px solid #46617A;
    background: transparent; color: #C9D8E4; cursor: pointer;
  }
  button:hover { background: #24405A; color: #fff }
  button.go { background: #E4572E; border-color: #E4572E; color: #fff }
  button.go:hover { background: #F26A42 }
  #hint { position: fixed; bottom: 2vh; font-size: clamp(11px,1.1vw,16px);
          color: #6C8298 }
  .warn { color: #FFC24A !important }
  .over { color: #FF6B57 !important }
  #clock.done { animation: flash 1s steps(2) infinite }
  @keyframes flash { 50% { opacity: .28 } }
</style>
</head>
<body>
  <div id="kicker">End-of-session quiz</div>
  <div id="clock">__MMSS__</div>
  <div id="msg">Press <b>Space</b> or Start when the class has scanned.</div>
  <div id="controls">
    <button class="go" id="startBtn">Start</button>
    <button id="resetBtn">Reset</button>
    <button data-min="5">5 min</button>
    <button data-min="6">6 min</button>
    <button data-min="10">10 min</button>
    <button id="fsBtn">Full screen</button>
  </div>
  <div id="hint">Space start or pause &nbsp;·&nbsp; R reset &nbsp;·&nbsp;
    F full screen &nbsp;·&nbsp; the form stays open 48 hours after this,
    for a failed network rather than for extra thinking time</div>

<script>
(function () {
  var WINDOW_MIN = __WINDOW__;
  var total = WINDOW_MIN * 60;
  var left = total;
  var running = false;
  var endAt = null;
  var tick = null;

  var clock = document.getElementById('clock');
  var msg = document.getElementById('msg');
  var startBtn = document.getElementById('startBtn');

  function fmt(s) {
    if (s < 0) s = 0;
    var m = Math.floor(s / 60), r = s % 60;
    return m + ':' + (r < 10 ? '0' : '') + r;
  }

  function beep(freq, ms) {
    try {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return;
      var ctx = new C();
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = 'sine'; o.frequency.value = freq;
      g.gain.value = 0.16;
      o.connect(g); g.connect(ctx.destination);
      o.start();
      setTimeout(function () { o.stop(); ctx.close(); }, ms);
    } catch (e) { /* a silent room is not a failure */ }
  }

  var beeped = {};
  function paint() {
    clock.textContent = fmt(left);
    clock.className = '';
    if (left <= 0) {
      clock.className = 'over done';
      msg.innerHTML = '<b>Time. Phones down.</b> If something went wrong ' +
        'for you, the form is open for 48 hours.';
      if (!beeped.end) { beeped.end = 1; beep(880, 400);
        setTimeout(function(){ beep(660, 500); }, 450); }
      return;
    }
    if (left <= 30) {
      clock.className = 'over';
      msg.innerHTML = '<b>Thirty seconds.</b> Submit now.';
      if (!beeped.s30) { beeped.s30 = 1; beep(760, 180); }
    } else if (left <= 120) {
      clock.className = 'warn';
      msg.innerHTML = '<b>Two minutes left.</b> If you are unsure, ' +
        'answer anyway: a blank scores the same as a wrong one.';
      if (!beeped.m2) { beeped.m2 = 1; beep(620, 160); }
    } else if (running) {
      msg.innerHTML = 'Five questions. One attempt. Your best ten of ' +
        'twelve quizzes count.';
    }
  }

  function loop() {
    left = Math.round((endAt - Date.now()) / 1000);
    if (left <= 0) { left = 0; running = false;
      clearInterval(tick); startBtn.textContent = 'Start'; }
    paint();
  }

  function start() {
    if (running) {                      // pause
      running = false; clearInterval(tick);
      startBtn.textContent = 'Resume';
      msg.innerHTML = 'Paused.';
      return;
    }
    // wall-clock based, so a busy laptop cannot make the clock drift
    endAt = Date.now() + left * 1000;
    running = true;
    startBtn.textContent = 'Pause';
    beep(520, 120);
    paint();
    tick = setInterval(loop, 250);
  }

  function reset(mins) {
    running = false; clearInterval(tick);
    beeped = {};
    if (mins) { WINDOW_MIN = mins; }
    total = WINDOW_MIN * 60;
    left = total;
    startBtn.textContent = 'Start';
    msg.innerHTML = 'Press <b>Space</b> or Start when the class has scanned.';
    paint();
  }

  startBtn.addEventListener('click', start);
  document.getElementById('resetBtn').addEventListener('click',
    function () { reset(); });
  document.getElementById('fsBtn').addEventListener('click', function () {
    if (document.fullscreenElement) { document.exitFullscreen(); }
    else { document.documentElement.requestFullscreen(); }
  });
  Array.prototype.forEach.call(
    document.querySelectorAll('button[data-min]'), function (b) {
      b.addEventListener('click', function () {
        reset(Number(b.getAttribute('data-min')));
      });
    });

  document.addEventListener('keydown', function (e) {
    if (e.code === 'Space') { e.preventDefault(); start(); }
    else if (e.key === 'r' || e.key === 'R') { reset(); }
    else if (e.key === 'f' || e.key === 'F') {
      document.getElementById('fsBtn').click();
    }
  });

  paint();
}());
</script>
</body>
</html>
"""


def main():
    mm = WINDOW_MIN
    html = (HTML
            .replace("__WINDOW__", str(WINDOW_MIN))
            .replace("__MMSS__", "%d:00" % mm))
    # A malformed colour fails silently in CSS: the browser drops the
    # declaration and you find out on the projector. Check the colours in
    # declaration VALUES only, since "#kicker" and the like are selectors.
    import re
    style = html.split("<style>", 1)[1].split("</style>", 1)[0]
    for decl in re.findall(r":[^;{}]+", style):
        for c in re.findall(r"#[0-9A-Za-z]+", decl):
            body = c[1:]
            assert (len(body) in (3, 6, 8)
                    and re.fullmatch(r"[0-9A-Fa-f]+", body)), \
                f"not a valid CSS colour in a declaration: {c}"
    assert "__WINDOW__" not in html and "__MMSS__" not in html, \
        "a placeholder was left unreplaced"
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("saved", OUT)
    print("  clock: %d minutes (keep in step with QUIZ_MIN_ON_CLOCK in "
          "create_quiz_forms.gs)" % WINDOW_MIN)
    print("  size: %.0f KB, no network, opens offline" % (len(html) / 1024))


if __name__ == "__main__":
    main()
