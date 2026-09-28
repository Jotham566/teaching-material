# Editable School Track flyer

## Files

- `output/School_Track_Flyer.pptx`: one portrait PowerPoint slide. All 41 text objects are native editable text; backgrounds, portrait, QR and icons are separate objects. Open in PowerPoint or import into another presentation editor. Import fidelity may vary.
- `output/School_Track_Flyer.svg`: standalone layered vector file with editable text and embedded images, for tools such as Inkscape or Illustrator. The font is Arial. Icons are replaceable images; original vector icons are in `assets/`.
- `output/School_Track_Flyer.png`: 2160 × 3240 pixels for WhatsApp and digital sharing.
- `output/School_Track_Flyer.pdf`: A4 portrait PDF with selectable vector text and clickable contact links. The original 2:3 composition is centred with white side margins. No bleed or crop marks are included.
- `source/layout.json`: named objects, copy, colours, coordinates and links.
- `source/export_powerpoint.mjs` and `source/export_print.py`: rebuild scripts.
- `source/SOURCES.md`: credits, provenance and content decisions.

## Easiest editing workflow

1. Duplicate the PowerPoint master and open the duplicate in PowerPoint.
2. Click text to edit it. Use the Selection Pane to find named objects such as “Intake”, “Group fee”, “Private fee terms” and “WhatsApp number”.
3. To replace the portrait, use Change Picture and keep its proportions. Keep the QR square and preserve its white border. If the phone number changes, update both the displayed number and QR/link destination.
4. Keep Arial to minimise font substitutions. The master is 11.25 × 16.875 inches (2:3 portrait). Avoid changing the slide ratio.
5. Export fresh PNG/PDF files after every edit. Existing exports do not update themselves. The supplied SVG and JSON are independent copies; changes in PowerPoint do not propagate into them.

## Source-based rebuilding

Edit `source/layout.json` if you want to regenerate multiple formats together. Use a Node runtime with `@oai/artifact-tool`, set `RUNTIME_NODE_MODULES` to its node_modules folder, and run `node source/export_powerpoint.mjs School_Track_Flyer_v2`. This writes a new PPTX and PNG. Use the Codex presentation finalizer for publication validation.

Run `python3 source/export_print.py` with ReportLab installed to regenerate the supplied PDF/SVG names. The print exporter currently uses Arial files in macOS `/System/Library/Fonts/Supplemental`; adjust that path on other systems. The scripts use existing assets and require no new internet downloads. Review all generated formats after changes.

## Improvements in this edition

The headline, student audience and booking information now have a clear reading order. The two tracks use consistent colours, with plain-language outcomes and tools. Repeated slogans and decorative book imagery have been removed to create room for essential information. Fees are paired with group-size conditions. The original portrait and QR remain intact. The laptop requirement is visible.

## Details to settle for the next revision

The supplied image says UGX 1,000,000 covers groups of one to four. Earlier programme notes say one or two, with a separate quote for three/four. This edition follows the image; confirm the intended wording. Add exact start/end dates, venue or online delivery, and session times once decided. These will make it easier for parents to judge whether the programme fits their plans. The QR invites an enquiry; it does not automatically secure a place.

A practical next campaign asset would be a short social post for each track, linking to this full flyer. Keep this full-information version for enquiries and parent sharing.
