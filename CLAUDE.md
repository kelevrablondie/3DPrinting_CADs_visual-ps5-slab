# PS5 "Slab" – custom side plates for an original PS5 Disc Edition

Owner: Mike. Personal, non-commercial project. Read this file fully before touching anything.

## Goal
Replace Sony's curved side plates with **flat, level, minimalist plates** (Xbox One S–like slab),
console used **horizontally only**. The black core stays visible as the centre band (front/rear I/O,
disc drive, light bars are NOT covered). Style: minimalism, subtle touches, PS1 / 30th-Anniversary grey.

## Decisions made (by Mike) – do not reopen without asking
| Topic | Decision |
|---|---|
| Orientation | Horizontal only. Current model: disc-side plate down (flip still open, see Open items) |
| Shape | Flat plates, minimal overhang, hide the stock curvature |
| Front / rear | Open – plates never cover I/O, disc slot or rear exhaust |
| Edges | Straight edges. Gaps as invisible as possible → skirt edges are straight but follow the core twist (4 mm reveal) |
| Drive | **Notch** in disc-side skirt so the drive face is framed, no gap |
| Fan | 120 mm double-sided intake (Sony teardown + iFixit photo confirm openings both sides) → grille on **both** plates |
| Accent | Four-colour decorative inserts (red/yellow/green/blue), no lighting. No Sony logo/trademark |
| Colour | Plates PS1-style grey (#c6c4be); core is the console's own black |
| Mounting | Separate **clip shelves** glued into the plates (devynPC-style), registered by **0.8 mm alignment pockets** in the floor |
| Glue procedure | Weld tiles → dry-fit shelves on console, lower plate, confirm every shelf drops into its pocket → remove → glue on bench (no glue near the console) |
| Feet | TPU, ~12 mm, on the bottom plate (bottom fan grille must breathe) |

## Printing constraints
- Printer: friend's Bambu **P2S** (AMS) now, possibly own Bambu X-series later. Plan for **256 × 256 × 256 mm**.
- Plate outline 384 × 258 mm → **2×2 tiles** with dovetails; seams must avoid clip shelves
  (in scan-local coords: vertical seam ~Y 110, horizontal seam ~Z 160 or 211 — re-check in console frame).
- Materials: plates + shelves **ASA/ABS** (solvent-weldable, heat), feet TPU. No PLA.
- Shelves print **upright as installed** (layers along the hook shafts); brim on the tall ones.
- Print tiles face-down on textured PEI for a uniform outer finish.

## Data provenance & trust (important)
| Source | Use | Trust |
|---|---|---|
| `sources/rhys34512-printables-973426/` – Rhys34512, Printables #973426, **CC BY-NC 4.0** | Clip geometry, inner surfaces, glue planes | **Fit-critical basis.** Hobbyist scan-derived, author printed & installed. Unverified by us → print `deliverables/coupon_*.stl` first |
| `sources/ps5-cover-standard-edition/` | Same scan, decimated (median dev. 0.13 mm). The full "cd" disc panel was a byte-identical duplicate of `disk-panel.stl` (17-byte header diff) → omitted | Duplicate, cross-check only |
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
- Plate outline L 384 × D 258, corner R 10, floor 2.5, skirt wall 2.5. Total width 119 mm (+12 mm feet).
- Skirt edges: straight lines from (face width/2 + 4 mm) at z=0 to the same at z=380, front and rear separately;
  no skirt across the short ends (core fills them). Disc-side front skirt removed over z 0…143 (drive notch).
- Grille: hex 3.2 mm holes, 5 mm pitch, R 60 around (y 3, z 305), holes skipped within 2.5 mm of shelf pockets.
- Clip shelves v1 (`deliverables/ps5_clip_shelves_v1.zip`, also `analysis/shelf_*.stl`): 4 per side, 18 hooks
  (flat 11, disc 7). Clip table: `analysis/clip_map.png`; groups: `tools/shelf_groups.json`.

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
  slab.py           ★ current parametric model (models: slab_horizontal, slab_standing)
  concepts.py, concept_d.py, concept_e.py   earlier rejected concepts (A/B/C, enclosed D, open E)
  mesh2step.py      STL -> sewn STEP so meshes can be placed in cadgen models (read_step)
  pockets.json, grille.json                 generated by tools/make_pockets_grille.py
  core/             STEP/STL proxies (core_final, drive_proxy, shelves in console frame)
  renders/          latest renders (hero_front/rear, ortho_front_rear, inside)
deliverables/       shelves v1 zip, fit-test coupons, adapter concept (rejected)
tools/              requirements.txt, shelf_groups.json, run_shelves.sh, make_pockets_grille.py, place_shelves.py
```

## Environment
- CAD: **text-to-cad** plugin + `cadgen` 0.8.2 (build123d / OCCT).
  `claude plugin marketplace add earthtojake/text-to-cad#latest && claude plugin install text-to-cad@earthtojake`
  Needs `uv`. One-time: `uvx --no-config --managed-python --python 3.13 --from cadgen==0.8.2 cadgen doctor`.
  Run models with `cadgen +0.8.2 run cad/slab.py`; snapshots `cadgen +0.8.2 snapshot <id> out.png --display shaded`.
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
1. Mike to decide: keep **diagonal straight reveal** (current) vs edges parallel to outline with larger gaps.
2. Grille vs shelf pads overlap (≈5 mm at F3 pads): shrink grille to Ø110 (recommended) **or** move pads.
3. Disc side down (current) vs flat side down.
4. Shelves **v2: +0.8 mm** on glue face to compensate the alignment pocket depth.
5. Remove leftover small skirt tab at one corner of the top plate.
6. Printable set: 2×2 tile split + dovetails (≤256 mm), inserts (0.6 mm, 14 × 2.5), TPU feet, export STL/3MF/STEP.
7. **Before any full print:** print `deliverables/coupon_F11_small_corner.stl` and `coupon_F5_large_spring.stl`
   and test-lock them on the console.
8. Core proxy is approximate (scan envelope ∩ tape loft) – fine for reveals, not for fit.

## Working style (Mike)
Direct, structured, numbered frameworks; challenge bad logic; no fluff or motivational language.
Hold file generation until Mike says **GO** when he asks for that.
