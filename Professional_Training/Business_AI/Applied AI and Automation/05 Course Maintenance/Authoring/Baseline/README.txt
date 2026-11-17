REBUILD BASELINE

Final Decks and Documents hold the builder's output that the patch layer in Edition/patch is applied to. Edition/build_edition.py reads these files, not the private .build folder, and refuses to run if any file differs from Baseline Manifest.json.

The builder that produced them (PowerPoint/build_course.mjs, Documents/build_course_documents.py) needs the author's Mac runtime and its text still describes an earlier agreement. So the baseline cannot be regenerated from maintained sources. It is kept in version control as binary files instead. Do not edit these files. To change course text, change the patch files, lesson_notes.json or Edition/files.

If the builder is ever rerun and its output adopted as a new baseline, regenerate the patch (Edition/edition_patch.py make and Edition/docx_patch.py make) against it, rebuild, compare with the live edition and update the manifest in the same change.
