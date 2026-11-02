# Handoff: where the last session stopped (2026-11-02)

Read `CLAUDE.md` first, then this. Delete this file once the redesign below is settled and its decisions are in `CLAUDE.md`.

## State right now
We are mid-design on the plate edges, west/east ends and disc access. **Nothing is approved to build yet**: Mike must approve the full description first. Everything from this session is uncommitted in the working tree on `main`.

## The question waiting for Mike
Which shape is closest to what he pictured for the west and east mesh panels, and what would he change?

See `docs/mockups/end_panel_options.png`, true scale; the three top drawings are the options, the two bottom ones are the face and back.
- **A, wedge fillers:** plates stay 384 mm. Mesh only fills the big wedge at each end. The core's end stays visible.
- **B, one full slant:** one mesh face per end, north edge to south edge. North plate 434 mm, south plate 390 mm.
- **C, two slants, pinched waist:** two mesh faces per end meeting near the core. Both plates 424 mm.

Mike clicked C, C, B, A in the browser, then asked to save without replying. **Treat that as browsing, not a choice, and ask again.** A, B and C are Claude's readings of "slanted"; none may match what he pictured.

## What Mike asked for (his words, in order)
1. On the end walls added this session: "not what I had in mind". The sides should be "more consistant with the 'hide' language".
2. "additional pannels, that are slants to the new actual side plates and they are meshed, to prevent blocked airflow".
3. The slants should be "visualy level and not repeat the curve of the core".
4. Disc access: "an integrated cutout" in the actual panel, "almost like the original plate does this... the pannel basically swoops in, having a litlle edge lip". Reference: `sources/reference-images/style_reference_render_10.webp`.
5. Compass directions, console horizontal and facing you, disc drive at the bottom right: upper panel **north**, under panel **south**, mesh panels **west and east** ("where the vertical stand and empty space was on the original").
6. "level edges on the x axis throughout the 'face' of the console and it's back. where it blocks airflow, insert the vents."

## Claude's mapping and findings (not yet confirmed by Mike)
- North = flat plate, south = disc plate, west = fan end (z≈380), east = drive end (z≈0).
- Level edge position is limited by the core's widest point plus the 4 mm reveal, using `slab.py`'s tape values:
  - Face: north x=43.7, south x=-39.3, so 15.5 mm deep.
  - Back: north x=46.2, south x=-41.8, so 13 mm deep.
- These edges are shallower than today's slanted skirts in most places and never deeper, leaving up to 21.5 mm open. So vents on the face and back may not be needed, though airflow is untested. The core's curve stays visible in that open band.
- The drive reaches x≈-50.8, past the level edge, so the swoop must drop to near the south plate over z≈0–165. It is only a rough sketch in the mockup. The drive area isn't clearly visible in render 10, so check the stock plate scan too.
- Plates of 424–434 mm should still fit in two tiles on the 256 mm bed, but this is not checked against the shelves or seam.
- Separate mesh panels need their own mounting. Not discussed yet.

## Conflicts to clear with Mike when the design is written up
These `CLAUDE.md` decisions change if this goes ahead: "Edges" (slanted reveal, core-following skirts) and "Drive" (notch).

## Rejected but still in the code
The semi-open walls are still in `cad/slab.py` (`END_FLAT`, `END_DISC`, `end_wall_cut`, the wall zone in `plate()`), with `analysis/end_edges.py`, `cad/check_end_walls.py` and `cad/renders/ends_*.png`. Mike rejected the concept. Remove them when the new design is built. The model builds as it stands, so nothing is broken in the meantime.

## How to resume
1. The process in use is the `superpowers:brainstorming` skill. Mike accepted its browser mockups. The questions continue one at a time, and a written description needs his approval before any build.
2. The old mockup server dies with the session. To reopen it, run the skill's `scripts/start-server.sh --project-dir <scratchpad> --open`, then copy `docs/mockups/end_panels_screen.html` into the new `screen_dir`. To change the drawings, edit and run `python3 -I docs/mockups/end_panels_mockup.py <out.html>`.
3. Use cadgen as `cadgen +0.8.4`, the installed version. `CLAUDE.md` still says 0.8.2.

## Side items, unchanged
- Job 1B is still unmeasured and could change plate spacing by up to 8 mm.
- `sources/ps5-cover-standard-edition/` has six untracked STLs Mike downloaded (`Ps5 *.stl`), about 84 MB: five duplicate tracked files and one is the omitted 82 MB panel. Don't run `git add -A` until they're dealt with. Claude recommended deleting them; Mike hasn't answered.
- That model's creator and licence are still unconfirmed, because Cloudflare blocked curl and Mike saved the files rather than the page.

## Video reference: devynPC "BoxPlates" (reviewed 2026-11-02)
Devyn Johnston, "I fixed the PS5 and now YOU can too", https://youtu.be/dNhaeyO8Zh0 (6:03, 31 May 2025). Same maker as the "devynPC-style" shelves. Commercial, injection-moulded flat plates. **No dimensions given.** His prototype was for a PS5 **Pro Digital**, so nothing is fit-verified for our original Disc Edition. Borrow ideas only; his line-pattern look is his design, so don't copy it. Times are transcript times; frame-only observations are approximate.

1. **Seam (open item 2):** his printed prototype is two shells joined by a **diagonal, stepped seam**, not a straight cut, and has hook pads on the floor. It's an option for our z≈158 seam: stiffer and self-aligning.
2. **Clips (4:21–5:01):** separate **slide-in, replaceable** clip strips in PETG (thick walls, dense infill, internal supports) slot into a channel on the plate's inner wall. Ours are glued. Slide-in would remove the glue-and-align step and allow a reprint of one broken clip. This doesn't reopen the "Mounting" decision; ask Mike before changing it.
3. **Airflow (3:01–3:42):** fine parallel slots over the fan carry on down the front lip, **wrap the corners** and run along the sides. This is a possible 4th answer to the west/east end question above: slots cut through the plate's own end walls instead of separate mesh panels, so no extra mounting is needed.
4. **Stock plates block the side intake (3:16–3:30)** and route air round the top and front. Sony's plastic rails round the fan keep the plate off it, so leave clearance over those rails. This supports grilles on both plates.
5. **Thermals (3:44–4:19):** 2 h God of War Ragnarök with stock plates vs 2 h with BoxPlates on a PS5 Pro, filmed with FLIR: same at the centre, cooler overall and at the rear vent. Not rigorous; weak evidence that open sides are safe.
6. **Disc models (2:35–2:39)** need a new bottom plate with a hidden disc slot, which relates to Mike's "swoop" disc access. Not shown in detail.
7. **Geometry (1:47–2:10):** he used a 3D scan, then removed the tilt and straightened the angles; "way more iterations than I expected". Expect several test prints (see Job 1B and the coupons).
