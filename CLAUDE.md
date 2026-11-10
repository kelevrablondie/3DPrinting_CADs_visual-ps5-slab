# PS5 "Slab" – custom side plates for an original PS5 Disc Edition

Owner: Mike. Personal, non-commercial project. Read this file fully before touching anything.

**Work in progress: read `HANDOFF.md` next. A redesign is mid-discussion and a question is waiting for Mike.**

## Goal
Replace Sony's curved side plates with **flat, level, minimalist plates** (Xbox One S–like slab),
console used **horizontally only**. The black core stays visible as the centre band (front/rear I/O,
disc drive, light bars are NOT covered). Style: minimalism, subtle touches, PS1 / 30th-Anniversary grey.

## Decisions made (by Mike) – do not reopen without asking
| Topic | Decision |
|---|---|
| Orientation | Horizontal only, **disc-side plate down**, level on its feet. Chosen for the APU's liquid metal: either flat side keeps gravity square to the die, and disc-down should leave the die facing up (inferred from iFixit's teardown order, not confirmed) |
| Plate depth / seam | **255 mm deep, 2 tiles split near z≈158** (tiles ~160 + 224 mm). Seam is now **diagonal + stepped** (BoxPlates-style, self-aligning, stiffer), not a straight cut; it must still clear every clip strip. Shape not designed yet |
| Edges (revisited) | Slanted reveal kept (cardboard mock-up skipped) |
| Grille / vents (2026-11-02) | **6 mm hex honeycomb, 1.2 mm webs (~69 % open) everywhere**: Ø110 fan grilles, face lips at the fan end, back lips end to end, both end walls. Replaces the 3.4 mm round holes |
| Shape | Flat plates, minimal overhang, hide the stock curvature |
| Front / rear | Open – plates never cover I/O, disc slot or rear exhaust |
| Short ends | **Direction: option D** (2026-11-02) — no separate mesh panels; the plates' own end walls carry vent slots that wrap the corners from the fan grille (BoxPlates idea, adapted for FDM). Our own pattern, not Devyn's line pattern. Wall shape/slot details still to brainstorm, see `HANDOFF.md`. Semi-open walls in `slab.py` are rejected |
| Edges | Straight edges. Gaps as invisible as possible → skirt edges are straight but follow the core twist (4 mm reveal) |
| Drive (2026-11-02) | Drive sits **behind the level south face lip**, like the stock faceplate; the disc slot (copied from the stock disc-plate scan, see `HANDOFF.md`) now sits **inside the black stripe**, in a **black filler** at the front drive end that also guides the disc back to the drive entry (y≈111). Filler printed with the south face lip via the AMS (fallback: welded) (2026-11-10). Replaces the old notch, the swoop idea and the slot hole in the lip |
| Fan | 120 mm double-sided intake (Sony teardown + iFixit photo confirm openings both sides) → grille on **both** plates |
| Accent | Four-colour decorative inserts (red/yellow/green/blue), no lighting. No Sony logo/trademark |
| Colour | Plates PS1-style grey (#c6c4be); core is the console's own black |
| Mounting | **Slide-in, replaceable clip strips** (2026-11-02, BoxPlates-style) that slot into channels on the plate inner wall/floor; no glue. Replaces glued shelves + 0.8 mm pockets. Clip strips come out **by hand** (Mike, 2026-11-10). Proposal awaiting Mike's review (`HANDOFF.md`, Clip strips): dovetail channel, solid end stop on the removal-pull side, thumb latch at the open end. Shelves v2 hook geometry is the starting point |
| Assembly | Weld tiles on the bench (only solvent step, never near the console) → slide clip strips in → fit to console |
| Feet | TPU, ~12 mm, on the bottom plate (bottom fan grille must breathe) |
| Wrap / lips (2026-11-02) | Plates wrap the core with **level lips and a constant black stripe** on face, back and both ends (devynPC 1:05 sketch; `docs/mockups/wrap_views.png`). Lips sit in front of the core face, so they are **separate lip strips welded to the plate edge**; the plate tiles stay 255 deep for the 256 bed. Face lips vented at the fan end; back lips vented end to end (honeycomb, see Grille), no notches or holes anywhere (Mike, 2026-11-10: "no breakup lines"). Stripe x −25.5…+22.2 (~48 mm; `wrap.py` `STRIPE`): the disc-side edge sits at the disc slot's outer edge, so rear plug heads clear it and the slot lies inside the stripe. Lips: north 39.5, south ~32 |
| North top (2026-11-02) | Single grey, engraved 0.4 mm only (no colour inlay, keeps PS1 calm). The tile seam is a **faceted panel line**: z 164 behind y −70, a 45° jog, then z 158. One path clears every clip of **both** plates by ≥3 mm, and it continues as the split groove on the face lips (158) and back lips (164). The fan grille stays honeycomb inside a **chamfered square panel line** (124 mm, 14 mm chamfers), so it doesn't read as a round fan. Markings in Hack mono: `[MONOLITH] U-05` at the front corner of the drive end, `INTAKE` plus 8 ticks by the panel. Style cue: the Xbox One X Cyberpunk 2077 controller's split line and bracketed text, with no CDPR or Microsoft art copied |
| Lip strip length | Face and back strips (381 mm) don't fit the bed, so they split at the seam z. End strips (261 mm) fit diagonally at ~25° |
| Removal / sleeve (2026-11-10) | Disassembly **as close to OEM as possible, sturdy, no glue**: lift the corner, slide, off. The end lips would block the slide (the plates slide in opposite directions), so both plates **overhang both ends by the slide distance + 0.5 mm** (a sleeve; the black end faces sit recessed in a grey frame). Needs TODO Job 1C; placeholder 25 mm. Not built yet |
| Accent placement | Colour inserts on the **north face lip** (seen from the working orientation), not on the plate top |

## Printing constraints
- Printer: Mike plans to buy a Bambu **X2D Combo** (256 × 256 × 260 mm, heated chamber up to 65 °C; 235.5 mm wide when using both nozzles). Print the 255 mm tile side along Y: about 0.5 mm spare per side, so no brim on those edges.
- Plate outline 384 × 255 mm (grows with end walls) → **2 tiles**; the stepped seam is not designed yet. A 2×2 split can't avoid shelves: the flat `bottom` shelf spans almost the full depth.
- Materials: plates + shelves **ASA/ABS** (solvent-weldable, heat), feet TPU. No PLA.
- Shelves print **upright as installed** (layers along the hook shafts); brim on the tall ones.
- Print tiles face-down on textured PEI for a uniform outer finish.

## Data provenance & trust (important)
Not in the public repo, local only and gitignored: `sources/ps5-cover-standard-edition/`, `sources/obj-visual-model/`, `sources/max-visual-model/`, `style_reference_render_*`, `devynpc_clip_shelves_photo.webp`. History was purged with git-filter-repo on 2026-11-02. Backup: `../ps5-slab-backup-20261102-2025/`.
| Source | Use | Trust |
|---|---|---|
| `sources/rhys34512-printables-973426/` – Rhys34512, Printables #973426, **CC BY-NC 4.0** | Clip geometry, inner surfaces, glue planes | **Fit-critical basis.** Hobbyist scan-derived, author printed & installed. Unverified by us → print `deliverables/coupon_*.stl` first |
| `sources/ps5-cover-standard-edition/` – MakerWorld #2863474 per the STL headers; creator and licence unconfirmed | Same scan, decimated (median dev. 0.13 mm). The full "cd" disc panel was a byte-identical duplicate of `disk-panel.stl` (17-byte header diff) → omitted | Duplicate, cross-check only |
| `sources/obj-visual-model/PS5.obj` (units ×200 = mm) | Proportions / visual only | **Not dimensional** (core depth 242 vs real 255) |
| `sources/max-visual-model/ps5v2disk.max` | Nothing – created 13 Jun 2020 (2 days after reveal, before launch) = built from renders | Not usable |
| X-ray (`reference-images/xray_*`, Creative Electron / iFixit) | Fan position; scale checked (outline 553 px = 390 mm ⇒ fan blades 170 px = 120 mm ✓) | ±5 mm |
| Mike's tape measurements (below) | Core envelope, reveal, overhang | ±1–2 mm. iPhone Measure-app numbers in photos: ±1 cm, sanity only |

### Mike's measurements (tape / books method)
- Core length ~380 mm. Core depth 255 mm (middle), 240 mm (top/fan end).
- Core **front** face width: 40 mm bottom (73 mm incl. drive), 55 mm middle (at front USB-A), 75 mm top.
- Core **rear** face width: 80 mm bottom, 71 near HDMI, 60 near first USB, 55 middle, 45 top.
- Stock console width with plates, books at drive mid-height: 95 mm.
  ⇒ glue-plane spacing = 95 + 18.2 (flat plate flare offset at that height) + 0.5 (disc) ≈ **114 mm**;
  predicts ~102 mm at top end vs Sony spec 104 → consistent within 2 mm.
- Fan: at the top end, ~13 cm from rear (photo) / 132 mm from rear, 76 mm from top (X-ray).
- Lying on a table, book on top: 96 mm disc bump up, 95 mm disc bump down. **Spacing unresolved:** the scan says the console tilts ~2.5° lying down, so these imply ~106 mm if the book found the true top, but 114 mm fits the 95 mm drive-end reading and Sony's 104 mm. TODO.md Job 1B settles it (S=114 predicts 102 fan end / 95 drive end; S=106 predicts 94 / 87).
  **2026-11-09: S=114 adopted as working value** (`docs/research/`): Sony 104, game8bit tape ~103 (CFI-1100A01), and the
  95 drive-end reading all fit 114; 106 would sit ~10 mm under every real reading. Job 1B now only asks for the fan-end
  reading as a confirmation (102–104 confirms, ~94 overturns). If wrong, the error is cosmetic (stripe ~8 mm narrower).
- Rear port positions along z (X-ray, ±4 mm, from the drive end): power 30–44, HDMI 71–85, LAN 106–123, USB 131–145 and 155–169.
  Front: USB-C 166–176, USB-A 183–197. Openings sit inside the stripe, ~2 mm from its disc-side edge; plug heads
  overlap −17.8 by ~1–3 mm (photo estimate, ±3–4 mm), hence the stripe edge at −25.5. Plan for ±1.5 mm port variation between CFI-10xx/11xx/12xx.
- Plate slide distance: not derivable from any source (no published value). Deferred until the clip strips need it.

## Coordinate frames
**Scan-local** (per panel, origin = panel bbox min): X across the panel, Y depth (0 = rear, +Y front),
Z height (0 = bottom end). Flat panel: console at −X, outboard +X. Disc panel: console at +X, outboard −X.
Scan glue planes (= stock plate outermost point; shelf back faces): flat x = 374.74, disc x = 184.35.

**Console frame (standing)** used by `cad/slab.py`: X width (**+X flat side, −X disc side**), Y depth (+Y front),
Z height (0 = core bottom end). Glue planes: flat +59.2, disc −54.8 (114 apart). Core centre x = +2.2.
Transforms scan → console:
- flat: x' = x − 374.74 + 59.2, y' = y − 231.12 − 130.75, z' = z − 196.34 − 4
- disc: x' = x − 184.35 − 54.8, y' = y − 126.61 − 130.75, z' = z − 196.16 − 4
Horizontal model = standing model rotated `Rot(0, −90, 0)` (disc side down).

## Key geometry (current values in `cad/slab.py`)
- Plate outline L 384 × D 255, corner R 10, floor 2.5, skirt wall 2.5. Total width 119 mm (+12 mm feet), pending Job 1B.
- Skirt edges: straight lines from (face width/2 + 4 mm) at z=0 to the same at z=380, front and rear separately;
  Disc-side front skirt removed over z 0…143 (drive notch).
- End walls (rejected concept, remove with the redesign): straight edges `END_FLAT`, `END_DISC` from `analysis/end_edges.py`; `cad/check_end_walls.py` checks core clearance over a 25 mm slide.
- Grille: hex 3.4 mm holes, 5 mm pitch, R 55 around (y 3, z 305), holes skipped within 2.5 mm of shelf pockets.
- Clip shelves v2 (`deliverables/ps5_clip_shelves_v2.zip`, also `analysis/shelf_*.stl`): 5 flat + 4 disc, 18 hooks
  (flat 11, disc 7), glue faces +0.8 mm for the pockets. Clip table: `analysis/clip_map.png`; groups: `tools/shelf_groups.json`.

## Files
```
sources/            original inputs (see trust table) + reference-images/
analysis/           scan analysis scripts and outputs (heightmaps *.npz, clip/edge/section plots, shelves, core proxy)
  hmap.py           panel heightmaps -> {flat,disk}_hmap.npz          clips.py  clip detection
  section*.py       clip cross-sections                                edges.py  stock edge-wrap depth
  shelves.py        clip-shelf generator (run via tools/run_shelves.sh)
  coupon.py         fit-test coupons                                   frame.py  (rejected) adapter-frame concept
  core_proxy*.py    core stand-in = space between plate inner surfaces ∩ measured face-width loft (+ drive box)
cad/
  wrap.py           ★ current PRE-ALPHA draft: wrap-around plates, lip strips, honeycomb, disc slot (model: wrap_horizontal, ~50 s cold)
  slab.py           earlier skirt concept; wrap.py imports its constants and internals()
  concepts.py, concept_d.py, concept_e.py   earlier rejected concepts (A/B/C, enclosed D, open E)
  mesh2step.py      STL -> sewn STEP so meshes can be placed in cadgen models (read_step)
  pockets.json, grille.json                 generated by tools/make_pockets_grille.py
  core/             STEP/STL proxies (core_final, drive_proxy, shelves in console frame)
  renders/          latest renders (hero_front/rear, ortho_front_rear, inside)
deliverables/       shelves v2 zip, fit-test coupons, adapter concept (rejected)
tools/              requirements.txt, shelf_groups.json, run_shelves.sh, make_pockets_grille.py, place_shelves.py
```

## Environment
- CAD: **text-to-cad** plugin + `cadgen` 0.8.4 (build123d / OCCT).
  `claude plugin marketplace add earthtojake/text-to-cad#latest && claude plugin install text-to-cad@earthtojake`
  Needs `uv`. One-time: `uvx --no-config --managed-python --python 3.13 --from cadgen==0.8.4 cadgen doctor`.
  Run models with `cadgen +0.8.4 run cad/slab.py`; snapshots `cadgen +0.8.4 snapshot <id> out.png --display shaded`.
  Headless Linux needs Xvfb (`Xvfb :99 & export DISPLAY=:99`); a desktop session doesn't.
  Telemetry was turned off: `uvx ... cadgen telemetry off`.
- Analysis Python: `pip install -r tools/requirements.txt` (system Python, not cadgen's).
- Rebuild order: `analysis/hmap.py` → `tools/run_shelves.sh` → `analysis/core_proxy.py` + `core_proxy2.py`
  → `tools/make_pockets_grille.py` → `tools/place_shelves.py` → `cad/mesh2step.py` (core_final, drive_proxy, shelves)
  → `cad/slab.py`. A full slab build takes ~100 s.
- Gotchas: build123d `Plane.YZ/XZ * Polygon` extrusions came out zero-volume here → use
  `Face(Wire.make_polygon([...]))` + `extrude(dir=...)` (as in slab.py). cadgen `read_mesh` can't place meshes
  → convert with mesh2step.py.

## Open items (next session)
1. **Mike: TODO.md Job 1B** (fan end only) confirms the glue-plane spacing of 114. Job 1D (one HDMI reading) checks
   that rear plug heads clear the stripe edge at −25.5. If the spacing changes, update P_FLAT/P_DISC in `cad/slab.py`, `analysis/core_proxy.py`, `analysis/core_proxy2.py` and `tools/place_shelves.py`, then rebuild.
2. Printable set, after item 1 and the end-wall design: slide-in clip channels, stepped seam near z≈158, inserts (0.6 mm, 14 × 2.5), TPU feet, export STL/3MF/STEP.
3. Grille still has small bites where it meets the shelf pads. Accept them or move the pads.
4. Skirt tab: `plate()` now gives one solid per plate and no separate tab was found; confirm by eye, then close.
5. **Before any full print:** print `deliverables/coupon_F11_small_corner.stl` and `coupon_F5_large_spring.stl`
   and test-lock them on the console.
6. Core proxy is approximate (scan envelope ∩ tape loft) – fine for reveals, not for fit. Skirt clearance at D 255 is ≥2.7 mm on the proxy only.

## Working style (Mike)
Direct, structured, numbered frameworks; challenge bad logic; no fluff or motivational language.
Hold file generation until Mike says **GO** when he asks for that.
