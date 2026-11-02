# Handoff: where the last session stopped (2026-11-02)

Read `CLAUDE.md` first, then this. Delete this file once the redesign below is settled and its decisions are in `CLAUDE.md`.

## State right now
Still mid-design on the plate edges, west/east ends and disc access. **Nothing is approved to build yet**: Mike must approve a written description first. Branch `handoff-end-panels` was merged into `main` and deleted.

## Decided 2026-11-02 (recorded in `CLAUDE.md`)
1. **Ends: option D.** Mike likes the BoxPlates look: no separate mesh panels; vent slots in the plates' own end walls, wrapping the corners from the fan grille. Merge his ideas with our design for **FDM / DIY**, not injection moulding: our own pattern (not his line pattern), printable without supports in the face-down tile orientation, ASA wall thickness.
2. **Clips: slide-in, replaceable strips** in channels on the plate, no glue. Replaces glued shelves + 0.8 mm pockets.
3. **Seam: diagonal + stepped**, near z≈158, must clear the clip strips.
4. Heat test: optional, "nice to test afterwards".
5. Duplicate `Ps5 *.stl` downloads deleted (all six matched tracked files byte-for-byte past the header).

## Next questions for Mike (one at a time, brainstorming skill)
1. End wall height/profile: level edge vs following the slanted skirt, and whether the slots run the full end or only near the fan (west).
2. Slot style for FDM: e.g. hex holes continuing the grille vs our own slot pattern.
3. Disc access "swoop" (item 4 below) still unresolved.
4. Clip-strip retention: friction fit, snap detent, or a screw/stop at the channel end.

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
3. Use cadgen as `cadgen +0.8.4`, the installed version.

## Side items
- Job 1B is still unmeasured and could change plate spacing by up to 8 mm.
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

## Video reference 2: devynPC "I fixed the PS5 Pro" (reviewed 2026-11-02)
Devyn Johnston, https://youtu.be/yilU2dU2YgA (4:50, 20 Jan 2025). This is the first prototype, made before BoxPlates. The console is a **PS5 Pro** (four plates, two per side), so again nothing is fit-verified for our Disc Edition. **No dimensions, materials or print settings are given.** Times are caption times; frame-only observations are approximate.

1. **Alignment is the main risk (2:49–3:07):** getting each plate's tilt and angle right "took the most trial and error". **1–2 mm off** and the plates collide, clips miss, or the plate visibly isn't level. That supports Job 1B, the coupons, and a cheap partial test print before a full plate.
2. **Check level with a spirit level (~3:20, frame):** he put a spirit level on the printed top plate. Add a spirit-level check to our test fit.
3. **Clips rebuilt as clean CAD (~2:40–2:50, frames):** he aligned the scanned clips, then modelled clean solid clips (ribbed hooks) on top of them instead of using the scan mesh. Our shelves come from scan meshes (`analysis/shelves.py`). When we design the slide-in strips, rebuild the hooks as parametric solids from our clip cross-sections (`analysis/section*.py`).
4. **The first prototype had fixed clips; BoxPlates has slide-in strips.** That's an inference that he moved away from fixed clips, but the video doesn't give a reason.
5. **Vents only where the stock plates left openings (3:24–3:34):** fan grille plus holes on the front and sides. The CAD frames (~3:40) show the hole pattern continuing over the plate's end wall and lip, which is option D. His pattern is an Xbox One S style grid of round holes with a chamfered look, taken from Microsoft's design, so again don't copy it. Our hex grille is our own.
6. **Front lip lowered to hide the curve (0:57–1:03):** the plate lip comes down over the core's curve, leaving the glossy middle strip and its ports open. That matches our "hide" language and the level face and back edges in "What Mike asked for", item 6.
7. **Plate as a shallow tray (~3:30, frame):** a section view shows a floor with low walls and a step partway along. That may be an early version of the stepped seam, but it can't be confirmed from the frame.
