# Sources and artwork handling

Portrait: the organiser's original `Jotham Martin Wambi Pic.jpeg`, included unchanged as `assets/actual-portrait.jpeg`. `assets/actual-portrait-cutout.png` uses the actual photographic subject with a foreground mask from Apple Vision. The face, clothing and pose were not regenerated or retouched. `source/mask_portrait.swift` records the masking operation. Colour decoding and transparency are part of normal raster compositing.

Design reference: organiser-supplied `Pasted 2026-09-28 at 10.39.12 AM.png`. The reconstructed classroom, desk, books, mug and brush artwork follows that reference. The background is reconstructed raster artwork, not the original editable design file. The classroom-only plate was prepared using built-in ImageGen, with the generated person removed; the original photographic cutout is a separate layer. See IMAGE_PROMPTS.md.

The original top composition, pastel course panels, dark fee/contact blocks and books-and-mug footer are retained. The middle panel is extended by 240 pixels; canvas 1024 × 1776. This creates space for the user's expanded learning lists and Build outcomes without compressing the original top and footer.

Learning copy and examples: organiser's preceding request. Pricing and contact wording follow the supplied reference. “Incoming PhD” refers to April 2027; OMU means Osaka Metropolitan University. No institutional sponsorship is implied. Exact venue and dates are not supplied. The working supplied QR opens https://wa.me/256750990718.

Internet logos/icons: Devicon (Python, pandas and scikit-learn), Font Awesome Free (supporting icons), Tabler (network), Carbon (prediction symbol in prior revision), Microsoft Fluent Emoji (chart in prior revision). Caveat font: Google Fonts. The original URLs and license notices remain in assets/internet-sources.json and the license files. Some earlier unused vector assets are retained for future edits.
