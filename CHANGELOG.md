# Changelog

Progress on the PS5 "Slab" side plates, newest first. Dates are when the work landed. The design is **pre-alpha**:
nothing here has been printed or test-fitted yet. See `README.md` for the project and `TODO.md` for what's next.

## 2026-11-10 (b): Clip strips, square face, fit tests
### Added
- **Slide-in clip strips** (`cad/wrap.py`, `clip_strip`): each hook shelf becomes a strip that slides along dovetail
  rails on the plate floor, with a solid end stop on the side that takes the pull when the plate slides off and a latch
  ledge at the open end. Hooks stay in their scanned positions. No glue.
- `cad/check_clip_strips.py`: checks that every strip clears its plate when installed, that the end stop blocks it and
  that the latch ledge catches it.
- **Fit tests to print first** (`deliverables/fit_tests/`, Bambu Studio–ready `.3mf`): two hook coupons, plus one clip
  strip with a matching plate offcut, built from the live model by `cad/fit_tests.py`. Print order in `TODO.md`.
- This changelog.
- Docs brought in line with the build: `HANDOFF.md` rewritten for the current state, 2D face mockup (`wrap_views.png`) redrawn with the 40 mm face stripe and the slot through the lip.
### Changed
- The south face lip now covers the core out to its narrowest face edge. The face shows one continuous 40 mm black
  band with no filler seam, the disc slot is cut through the lip, and a hidden guide is printed as one with the lip.
  The face corners are squared over the end lips.
### Removed
- Declined designs moved to `archive/`: concepts A–E, the semi-open end walls, the adapter frame, and the glued clip
  shelves (replaced by the clip strips).
### Known gaps
- Hooks are still the scanned meshes, not parametric solids. The latch's flex arm is not modelled.
- One end stop sits ~2 mm from the tile seam (target ≥3 mm). The floor grille doesn't yet account for the rails.

## 2026-11-10 (a): Notchless stripe and sleeve
- Disc-side stripe edge moved to −25.5 so rear plugs clear it without notches. Disc slot in a black filler (superseded the same day).
- Decided: plates overhang both ends as a sleeve, so they can slide off like the stock plates (not built yet).
- Exploded-view sketches of the clip-strip proposal (`docs/mockups/explode/`).

## 2026-11-09: Research
- Reverse-engineering notes and an X-ray overlay for I/O positions.
- Web research on PS5 width, I/O and slide distance. Plate spacing of 114 mm adopted as the working value.

## 2026-11-02: Wrap-around design
- Direction set: flat, level plates that wrap the core with level lips and a constant black stripe (BoxPlates-inspired, our own pattern).
- 6 mm hex honeycomb for every vent. Drive sits behind the south face lip, and the disc slot is taken from the stock plate scan.
- Pre-alpha 3D draft (`cad/wrap.py`). North top engraved with a faceted seam line, a chamfered fan panel and `[MONOLITH] U-05` markings.
- 255 mm plate depth in two tiles, separate lip strips, plain-language `TODO.md` measuring jobs.
- Licence changed to CC BY-NC 4.0. Scan source and iFixit images credited; unlicensed references kept local only.
