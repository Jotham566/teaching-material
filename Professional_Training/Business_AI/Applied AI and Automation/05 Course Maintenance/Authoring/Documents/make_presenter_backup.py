"""Write Presenter Notes Backup.txt: the material kept out of the read-aloud notes.

  python3 make_presenter_backup.py OUTPUT_FILE

Per slide that has sources or click builds: the title, the number of clicks and the source links.
Reads course.json (titles) and lesson_notes_sources.json (sources, click counts).
"""
import sys, json, re
from pathlib import Path
here = Path(__file__).resolve().parent
course = json.loads((here / 'course.json').read_text(encoding='utf-8'))
over = json.loads((here.parent / 'Edition/expected_changes.json').read_text(encoding='utf-8'))['title_overrides']
extra = json.loads((here / 'lesson_notes_sources.json').read_text(encoding='utf-8'))
out = ["PRESENTER NOTES BACKUP",
       "",
       "The speaker notes in the decks are a script to read aloud. This file holds what the script leaves out: the source links behind a slide and the click count of each animated slide.",
       "",
       "Reading an animated slide. The first paragraph of its note is read before any click. Each of the next paragraphs is read as the matching click reveals its part. Paragraphs after those continue once the last part is on screen. Play the slide in Slide Show mode; editing view shows the finished diagram.",
       ""]
for sess in course:
    n = sess['session']; rows = []
    for i, s in enumerate(sess['slides'], 1):
        e = extra[f'{n}/{i}']
        m = re.search(r'(\d+) native click', e['playback'] or '')
        if not e['sources'] and not m: continue
        line = f"Slide {i}: {over.get(f'{n}/{i}', s['title'])}"
        if m: line += f"  [{m.group(1)} clicks]"
        rows.append(line)
        if e['sources']: rows.append("  " + e['sources'].replace('Sources: ', 'Sources: ', 1))
    out += [f"SESSION {n}: {sess['title']}", *rows, ""]
Path(sys.argv[1]).write_text("\n".join(out), encoding='utf-8')
print('written', sys.argv[1])
