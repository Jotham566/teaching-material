# Slides build

Decks are generated, one PPTX per session, lab and the extension (`camp_2026/slides/`). Edit the lessons or the
authored content below, then rebuild.

```
python Schools_ML_Track/camp_2026/build/slides/build_slides.py            # every deck
python Schools_ML_Track/camp_2026/build/slides/build_slides.py DA09 ML14  # chosen decks
python Schools_ML_Track/camp_2026/build/slides/lint_slides.py             # house-style lint of the authored content
```

| File | What it holds |
|---|---|
| brand.py | KLAi colours, fonts and slide geometry. |
| figkit.py | The drawing kit: Scene, pictograms (person, shop, bottle, bike...), tables, code panels, charts style. |
| slidekit.py | Text measurement with the real Lato files, code highlighting, panel builders. |
| build_slides.py | Builds each deck's slide list from the lesson plus the authored content, then calls render_deck.js. |
| render_deck.js | Draws a spec with pptxgenjs: KLAi light and dark layouts, title placeholders, notes. |
| notes_auto.py | Spoken-script notes for the automatic slides. |
| figs_common.py, figs_da.py, figs_ml.py | The authored illustrations. A figure is a function `fn(w, h, **params) -> Scene`. |
| concepts_da_1.py, concepts_da_2.py, concepts_ml_1.py, concepts_ml_2.py | The authored concept slides and speaker notes per session. |
| lint_slides.py | Style lint. |

Figures are cached in `camp_2026/figures/`. Fonts: install Lato from `camp_2026/brand/fonts/` on any laptop that opens the decks.
