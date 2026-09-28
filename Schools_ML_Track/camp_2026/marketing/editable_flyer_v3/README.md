# Updated School Track flyer

This revision uses the organiser's **actual, unmodified JPEG portrait**, expands both learning tracks in plain language, and separates the project outcomes with blue and purple strips. The repeated slogans, books-and-mug scene and longer tutor biography were removed to make room. The library logos, fees, contacts and functional QR remain.

## Deliverables

- `output/School_Track_Updated.pptx`: editable PowerPoint master. Text and panels are native editable objects. The original portrait, logos and QR are individually replaceable image objects.
- `output/School_Track_Updated.png`: 2048 × 3072 image for sharing.
- `output/School_Track_Updated.pdf`: A4 PDF with selectable text, embedded fonts and contact links. White side margins preserve the 2:3 composition; no print bleed.
- `output/School_Track_Updated.svg`: layered editable SVG with embedded image assets.

The portrait in `assets/actual-portrait.jpeg` is a byte-for-byte copy of the supplied `Jotham Martin Wambi Pic.jpeg`. It has not been generated, retouched or background-removed. The original grey photographic background is preserved. No generated photographic backdrop is used in this revision.

## Editing

Duplicate the PowerPoint before editing. Select text directly, or use the Selection Pane to locate named items such as “DA learning 1”, “ML Build”, “Private fee condition” and “Phone”. Replace pictures using Change Picture. Keep the QR square with its white border. If changing the number, update the QR and contact links too.

This version uses Arial, Arial Black and Arial Narrow. The handwritten font used by the previous edition is not required. Export new sharing/print files after editing. Changes in PowerPoint do not update the separate SVG or source JSON automatically.

For source edits, change `source/layout.json` and run `source/export_powerpoint.mjs` with RUNTIME_NODE_MODULES pointing to the installed Codex runtime package directory. Run `source/export_print.py` with ReportLab for PDF/SVG. The print script uses macOS font paths. `source/build_layout.py` rebuilds the JSON from the authored copy; running it replaces manual JSON edits. Inspect every export after changes.

## Content and sources

The latest user request supplies the learning topics and project examples, including dashboards and recommendations. Examples describe possible projects, not a promise that every learner completes every example. Prices and group-size conditions retain the supplied reference's wording. Exact venue and dates are still not supplied. The QR opens https://wa.me/256750990718.

Logos and supporting icons retain the internet sources from the preceding version; original SVGs, source URLs and licenses are included in `assets/`. See `source/SOURCES.md`.
