# Reverse-engineering the missing measurements (2026-11-09)

Side note, not a measurement record. It checks whether the gaps in `TODO.md` (Jobs 1B, 1C, 1D) can be closed
from files and images instead of the tape. Nothing here overrides `CLAUDE.md` or `TODO.md`; values marked ±
are estimates until Mike confirms them.

## 1. Files evaluated this round

None of these files is in the repo: third-party, licence unknown, kept local only (same rule as the
`.gitignore` list).

| File | What it is | Evidence | Verdict |
|---|---|---|---|
| `PlayStation5DiskEdition.STEP` / `.SLDPRT` | SolidWorks 2018 solid, exported **2020-06-14** (3 days after the reveal, 5 months before launch) | Height 440 mm (real 390), total width 136 mm (real 104), core depth 227 mm (tape 255), height/depth 1.76 vs real 1.48 | Built from reveal renders. Proportions are wrong, so it can't be rescaled. **Not usable** |
| `PlayStation-5.dwg` | AutoCAD 2022 (2022-03-14), 2D furniture block in **cm**: plan, front, side views + a DualSense | Console ~365–372 mm tall without stand (real 390). DualSense 138 × 40 mm (real 160 × 66). No rear view | Stylised, inconsistent scale. **Not usable** for ±mm, nothing on rear ports |
| `ps5-playstation-5…zip` ("Funny_print") | Resin miniature, Anycubic Photon Workshop export, 136 mm tall, assembled (core + 2 plates) | Scaled ×2.847 to the scan's plate height: plate depth 261.9 (scan 261.5), core length 380.7 (tape ~380). But the plate surfaces deviate up to **18 mm** from the scan: flat plate flares at both ends (real: top only), no drive bulge on the disc plate (real: bulge at z≈65). Single-height widths 108–110 mm vs Sony 104 | Bounding box fitted to the spec, shapes stylised. Its plate spacing **can't be trusted** |

Why more files don't help: all models found so far were built from renders, photos or the published spec, so
their errors are **systematic, not random**. Averaging them doesn't converge. Only the plate scan, the X-ray,
Sony's spec and Mike's tape carry real measurements.

Tools: DWG read with LibreDWG 0.13.3 (`dwg2dxf`) + ezdxf; STEP loaded with build123d (cadgen).

## 2. Findings

### Job 1D: port positions along the length (closed to ±4 mm)
From the iFixit / Creative Electron X-ray (`sources/reference-images/xray_ports_overlay.png`,
made by `tools/xray_ports_overlay.py`). Scale 0.705 mm/px: outline 553 px = 390 mm, cross-checked by the
120 mm fan = 170 px. **Orientation and scale check:** the disc drive shows along the front edge at
16–158 mm from the drive end, matching the disc slot from the plate scan (22.5–145 mm).

| Back (mm from drive end) | | Front (mm from drive end) | |
|---|---|---|---|
| Power | 30–44 | USB-C | 166–176 |
| HDMI | 71–85 | USB-A | 183–197 |
| LAN | 106–123 | | |
| USB 2 (nearer drive) | 131–145 | | |
| USB 1 (nearer fan) | 155–169 | | |

Order matches `measure_rear_face.jpg` (bottom-up: power, HDMI, LAN, USB, USB).
Caveat: the X-ray outline may be the 388 mm plates rather than the 380 mm core, a 2.5 % scale ambiguity (±4 mm at 160 mm).

### Job 1D: position across the thickness, back (estimate ±3–4 mm)
From `measure_rear_face.jpg`, scaled by the 80 mm bottom width. The five rear ports sit in one straight
column about **3–18 mm off the rear-face centre, toward the disc side** (assuming the face centre = core
centre x +2.2).
- **Port openings sit inside the 40 mm stripe** (stripe x −17.8 … +22.2), about 2 mm from its disc-side edge.
- **Plug heads overlap the stripe edge by ~1–3 mm** (HDMI head ~21 mm wide, LAN/USB ~16 mm), so the back lips
  need notches at the X-ray positions above, or a back stripe shifted 3–4 mm toward the disc side.

### Job 1D: black part at the back, drive end / fan end
Already measured 2026-11-02: **80 mm / 45 mm** (`CLAUDE.md`, rear face widths).

### Front buttons
Not visible in the X-ray. Mike's photos and the layout model put them in the centre column, inside the stripe.
No cut-outs expected (medium confidence).

### Job 1B: plate spacing 114 vs ~106 (strongly favours 114)
- S = 114 predicts ~102 mm at the fan end (widest single height), within 2 mm of **Sony's 104 mm**.
- S = 106 predicts ~94 mm, **10 mm under Sony's own figure**.
- 114 also fits the 95 mm drive-end book reading. The lying-down readings (96/95) only point to 106 if the
  book found the true top; the console tilts ~2.5° lying down.
- Remaining risk: the wording of Sony's spec ("excludes largest projection").
- Consequence if wrong: cosmetic only. The clips fix each plate's position, so a wrong S shifts where the lips end
  (stripe ~32 mm instead of 40, less plug clearance), not the fit.

### Job 1C: slide distance (not derivable)
The scanned hook lips engage ~2–4 mm beyond their shafts (large hooks), but the slide also depends on the
chassis slot length, which no source shows. Lower bound only.

## 3. What still needs the tape (≈2 minutes)
1. **Job 1B:** books ~1 cm from the fan end. Expect **~102 mm** (confirms 114).
2. **Job 1D:** at HDMI height, the distance from the HDMI port's edge to the edge of the black rear face on the
   disc side. Decides notches vs a shifted back stripe.
3. Job 1C only if the final clip design needs it.
