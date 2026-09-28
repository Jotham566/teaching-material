# School Track flyer — original-style reconstruction

This edition replaces the earlier simplified design with a much closer reconstruction of the supplied 1024 × 1536 flyer. The previous edition remains unchanged in `../editable_flyer/`.

## Start here

Open `output/School_Track_Flyer_Editable.pptx` to edit the flyer. The slide preserves the original 2:3 portrait ratio. Headlines, slogans, tutor biography, course labels, benefits, fees, contacts, book titles and mug lettering are native editable text. Panels and dividers are native shapes. Logos, QR, photo background and brush decorations are separate replaceable image objects.

The photographic backdrop and brush overlay are reconstructed raster artwork, not editable photographs of individual objects. This is a close visual reconstruction, not a pixel-identical conversion of the flattened original. Some supporting icons and typefaces differ slightly. The Python, pandas and scikit-learn logos are internet-sourced assets rather than generated lettering.

## Fonts

The design uses Arial, Arial Black, Arial Narrow and **Caveat** for handwritten text. Caveat has been installed in the current Mac user’s Fonts folder and is also included as `assets/Caveat.ttf`, with its open font license. On another computer, install that font before opening the PowerPoint or SVG to prevent substitutions. Close and reopen PowerPoint if it was running during font installation. The PDF embeds fonts, and the SVG embeds the Caveat font data, though some vector editors may still require local installation.

## Deliverables

- `output/School_Track_Flyer_Editable.pptx` — editable PowerPoint master.
- `output/School_Track_Original_Style.png` — 2048 × 3072 sharing image.
- `output/School_Track_Original_Style.pdf` — A4 portrait, selectable text, embedded fonts and contact links; narrow white side margins preserve the 2:3 artwork. No print bleed or crop marks.
- `output/School_Track_Original_Style.svg` — layered vector document with editable text and embedded image assets.
- `source/layout.json` — named elements, text, styling and coordinates.
- `source/export_powerpoint.mjs` and `source/export_print.py` — regeneration scripts.
- `assets/` — photographic plate, accents, working QR, technology logos, supporting icons, font and licenses.

## Editing

1. Save a new copy of the PowerPoint. Use its Selection Pane to select named elements such as “Tutor name”, “Small group price”, “Private condition” or “Intake”.
2. Edit the text directly. Replace image objects with Change Picture. The photo and decoration layers can be moved behind everything else if you need access to a text box.
3. Keep the QR square with its white border. If the contact number changes, replace the QR and update the number and linked contact destinations together.
4. Export a fresh PNG/PDF after every edit. Edits in PowerPoint do not update the separate SVG, JSON or existing exports automatically.
5. For source-based edits, edit `source/layout.json`, install the included Caveat font, set `RUNTIME_NODE_MODULES` to the Codex runtime package directory, and run `node source/export_powerpoint.mjs Flyer_next`. Run `python3 source/export_print.py` with ReportLab to regenerate the PDF/SVG. That script uses macOS Arial font paths. Review every output after changes.

## Fidelity and content

Restored the soft classroom scene, oversized portrait, multicolour headline, handwritten slogans, brush underlines, biography card, pastel course panels, technology-logo rows, benefits icons, dark fee and booking blocks, desk, books and mug.

The supplied reference’s wording and pricing take precedence for this reconstruction, including UGX 1,000,000 for 1–4 learners. Earlier programme notes differ on that group-size condition. Venue and exact dates are not invented. “Incoming PhD Student” relates to the organiser’s April 2027 intake clarification. The supplied functional QR replaces the visual reference’s code and opens an enquiry at https://wa.me/256750990718.

See `source/SOURCES.md` for credits and `source/IMAGE_PROMPTS.md` for the exact photographic/decoration reconstruction prompts.
