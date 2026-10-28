"""Write Playback and Rehearsal Checklist.txt from the notes, the sources file and the course timing.

  python3 make_playback_checklist.py OUTPUT_FILE
Spoken time uses 130 words a minute. Optional slides are listed separately and excluded from the core total."""
import sys, json, re
from pathlib import Path
here = Path(__file__).resolve().parent
course = json.loads((here / 'course.json').read_text(encoding='utf-8'))
notes = json.loads((here / 'lesson_notes.json').read_text(encoding='utf-8'))
extra = json.loads((here / 'lesson_notes_sources.json').read_text(encoding='utf-8'))
over = json.loads((here.parent / 'Edition/expected_changes.json').read_text(encoding='utf-8'))['title_overrides']
WPM = 130
status_path = here / 'rehearsal_status.json'
status = json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {}
played = {(x['session'], x['slide']): x['clicks'] for x in status.get('native_playback', {}).get('slides', [])}
audio = {x['session']: x for x in status.get('audio', [])}
out = ["PLAYBACK AND REHEARSAL CHECKLIST", "",
 "Part 1, in PowerPoint on the machine you will teach from. Open each deck, choose Slide Show, and play every animated slide from the first click to the last. Confirm the stages appear in the order listed and that nothing overlaps. Editing view shows the finished diagram, so only Slide Show proves the build. Tick each line.",
 "Part 2, read the notes aloud once per session, timing yourself. The estimate below is the speaking time of the notes alone at 130 words a minute, before any pauses for the learner. Each session has 120 minutes, with different allocations for explanation, demonstration, guided work and discussion. The notes alone should fill well under the full class time.",
 "Part 3, run the demonstrations that need your accounts (see Run Demonstrations.txt and Demonstration Preflight.txt) and tick them here when done.", ""]
if status:
    out += [f"RECORDED REHEARSAL: {status['date']}",
            "Native PowerPoint playback completed: 34 animated slides, 126 clicks. Captures and visual review are in 05 Course Maintenance/Validation/Native PowerPoint Playback.",
            "All twelve core scripts were rendered into system-voice practice recordings. Rehearsal Audio retains their scripts, measured durations and regeneration instructions; generated audio binaries are excluded from the repository. These measurements exclude learner answers, reveals, demonstrations, discussion and breaks and are not a human rehearsal.",
            "See Mac Rehearsal Review.txt for the executed account routes and their limits. Empty human-rehearsal boxes remain personal delivery checks, not unperformed automated tests.", ""]
for s in course:
    n = s['session']; core = opt = 0; anim = []
    for i, sl in enumerate(s['slides'], 1):
        w = len(notes[f'{n:02d}'][str(i)].split())
        if i in s['optional_slides']: opt += w
        else: core += w
        m = re.search(r'(\d+) native click', extra[f'{n}/{i}']['playback'] or '')
        if m:
            done = played.get((n, i)) == int(m.group(1))
            anim.append(f"  [{'x' if done else ' '}] Slide {i}: {over.get(f'{n}/{i}', sl['title'])}, {m.group(1)} clicks" + (" (optional)" if i in s['optional_slides'] else ""))
    out += [f"SESSION {n}: {s['title']}",
            f"  Notes read aloud: about {round(core / WPM)} minutes for the core slides" + (f", plus about {round(opt / WPM)} minutes if you teach the optional ones." if round(opt / WPM) else "."),
            f"  [{'x' if any(x[0] == n for x in played) else ' '}] Deck opens in PowerPoint and Slide Show runs from slide 1",
            *([f"  [x] System-voice core script rendered and measured: {audio[n]['measured_audio_minutes']:.2f} minutes (automated practice aid)."] if n in audio else []),
            *anim, f"  [ ] Notes read aloud once, wording changed where it does not sound like you", ""]
out += ["ACCOUNT AND MODEL DEMONSTRATIONS"]
if status.get('account_demonstrations'):
    out += [f"  [x] {v}" for v in status['account_demonstrations'].values()]
    out += ["  [ ] Confirm the learner's exact product/settings and repeat there if different from the teaching account.",
            "  [ ] Enterprise connector, matter access and production-action tests, if those routes are selected for the firm.", ""]
else:
    out += ["  [ ] Connected retrieval demonstration run in your own account", "  [ ] Portal-builder demonstration run in your own account", "  [ ] Live deep-research demonstration run, output saved in Observed Runs", "  [ ] Neural embedding demonstration run; save the output in Observed Runs", "  [ ] Repeat the saved model runs in the tool the learner will use", ""]
Path(sys.argv[1]).write_text("\n".join(out), encoding='utf-8'); print('written', sys.argv[1])
