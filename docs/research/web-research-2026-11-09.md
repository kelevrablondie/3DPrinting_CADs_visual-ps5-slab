# Web research: measured PS5 Disc Edition data (2026-11-09)

Research report written by Claude's research mode from external sources, kept here as a side note next to
`reverse-engineering-2026-11-09.md`. It is reference material, not a measurement record: nothing here
overrides `CLAUDE.md` or `TODO.md`. Values are as reported by the cited sources (mostly tape measurements).

## Summary for the open TODO jobs

| Job | Result | Confidence |
|---|---|---|
| **1B** plate spacing | Every independent source puts the widest point with stock plates at **~103–104 mm** (Sony spec 104; a Japanese owner's tape measurement of a CFI-1100A01: ~103 mm). With Mike's 95 mm at the drive end, the widest point must be the fan end → **S ≈ 114 mm** (predicts 102 / 95). S ≈ 106 (94 / 87) would sit ~10 mm under every real reading | Moderate (tape only; nobody separates fan end vs drive end) |
| **1D** I/O across the thickness | **No dimensioned source exists.** Only the order is confirmed (bottom-up: power, HDMI, LAN, 2× USB-A, lock slot). Keep the photo/X-ray estimate from `reverse-engineering-2026-11-09.md`; verify on the console | Low–moderate |
| **1C** slide distance | **No measured value anywhere.** Circulating numbers ("lift ~3 mm", "1–2 cm") come from unsourced / AI-generated pages — discard | None |

## Gap 1: total width / plate spacing

**Sony's spec.** PlayStation Blog launch post (16 Sep 2020): "Approx. 390mm x 104mm x 260mm (width x height x
depth) (excludes largest projection, excludes Base)". Digital Edition: 390 × 92 × 260 mm, same qualifier.
Japanese CFI-1200A safety guide: 外形寸法（最大突起部除く） 約390 × 104 × 260 mm. The PS5 Ultimate FAQ
(9 Nov 2020) says "excluding the Base". Sony never defines "largest projection"; 最大突起部除く is standard
Japanese spec boilerplate (also used for the DualSense and Media Remote).

What the excluded projection is (inferred, not sourced):
- **Not the stand**: listed separately ("excludes Base"); the Taiwanese spec (via kocpc) reads
  不包括最大突出部位與底座 = "largest projection *and* base".
- **Almost certainly not the drive bulge**: Disc 104 vs Digital 92 mm differ by 12 mm, so 104 includes the
  drive side.
- **Probably not a big plate flare**: real readings of the widest point are at or just under 104 mm, so the
  excluded feature adds ≤ ~1 mm (feet, button caps, port lips — unsourced).
- ResetEra guesses ("white tips", "stand clamp") are speculation.

**Independent real-console measurements (all tape, none caliper):**

| Source | Console | Method | Reading | Notes |
|---|---|---|---|---|
| game8bit.com (31 Aug 2024) | CFI-1100A01 Disc | Tape, photographed, "longest part" (一番長い部分を測定) | Thickness ~10.3 cm (≈103 mm); 39 × 10 × 26 cm rounded; ~404 mm tall on stand; 4161 g | Best available; position along the length not stated, ±1 mm |
| couple-game.net (2023–24) | Old-model Disc | Tape, author warns ±0.5 cm | Lying flat on base: 11 cm incl. 0.6 cm base lift → body ≈104 mm. Standing on base: 15.5 × 40.4 × 26 cm. Base Ø155, 193 long incl. hook, 47 high | Standing-without-base figure just repeats Sony's spec |
| itomarublog.com | Disc, launch | Unstated | "幅9cm程" (≈90 mm) | Conflicts with everything else; probably a narrow point. Low reliability |
| Mike | Disc | Two books, tape | 95 mm at drive mid-height | Primary data, drive end |

**Conclusion:** use S ≈ 114 mm; design the fan end at 102–104 mm and the drive end at ~95 mm. Remaining
uncertainty 1–2 mm (102 vs 104), within tape error. One two-book reading at the very top of the fan end closes it.

**Checked, no usable width data:**
- Taiwan NCC certification photos (Sep 2020, CFI-1018B, fccid.io) — reported as "next to a ruler"; appearance
  PDF not retrievable, no readable scale in write-ups. Pre-launch but real hardware.
- Wall mounts: HIDEit (bracket 399 × 127 × 76.5 mm, uses the centre channel), Monoprice 47565 (tech drawing
  not retrievable; fits Disc/Digital/Pro), VIVO (bracket 15.7″ × 5.9″ × 3″) — bracket sizes, not console width.
- dbrand Darkplates: no drawings; skin 0.25 mm only.
- Aggregators (sizevista, oreateai, dimensions.com, comparesizes, Wikipedia) repeat Sony's spec; oreateai's
  "drive bulge adds 12–16 mm" and Alibaba's "390 × 260 × 202 mm" are unsourced / wrong.
- Cults3D "PS5 Console – Raw 3D Scan | OBJ & STL" (~US$5.61): listing couldn't be opened; scanner, revision and
  bounding box unknown. Worth buying only if the seller confirms a real assembled console scanned after Nov 2020.

## Gap 2: I/O positions across the thickness

No dimensioned source reachable:
- **iFixit device page diagrams (#diagram/24724, /24725)**: GygInfographics exploded views, drawn in Adobe
  Illustrator with isometric projection — illustrations, not scalable drawings. Teardown confirms rear: 2× USB-A
  3.0, LAN, HDMI 2.1, two-pin power; front: USB-A, USB-C, power and eject buttons.
- **Fasttech** (front frame CFI-11xx page blocked; related I/O Port Frame CFI-1015A/1115A/1215A, top frame, side
  covers, HDMI port listings): compatibility and price only ($28.99–39.99), no dimensions. Note: revision-specific
  I/O port frames exist, so port positions may differ by a millimetre or two between CFI-10xx/11xx/12xx (unconfirmed).
- **Port order** (Notebookcheck, Sep 2020), bottom-up when standing: power, HDMI 2.1, Ethernet, two USB-A,
  security lock slot at the top. Matches our X-ray order.

## Gap 3: side-plate slide distance

- iFixit Faceplates Replacement: "Lift up the corner… slide the faceplate towards the bottom." No distance.
  By-product: stand screw is **26.5 mm** long.
- Sony support: "slightly pulling up and to your right". Glistco: slide toward the bottom, away from the PS-logo
  corner; install by sliding toward the logo corner until it clicks.
- 4Gamer interview (16 Oct 2020) with Yasuhiro Ootori (SIE mechanical design): side panels are ABS, no screws,
  removed by releasing the clips and sliding (爪を外してスライド). No distance; confirms fan Ø120 × 45 mm.
- Discard: Alibaba buying guides ("lift ~3 mm", plate thickness "1.8" or "2.1–2.4 mm"), 9meters ("1–2 cm") —
  unsourced, contradictory.

## Recommendations from the report
1. Lock S ≈ 114 mm; fan end 102–104, drive end ~95. Confirm with one two-book (ideally caliper) reading at the
   very top of the fan end: 102–104 confirms, ~94 overturns.
2. Slide distance: masking tape across plate edge and core, one pencil line over both; lift the corner, slide
   until it just frees, measure the offset. 3× per side. While the plate is off, caliper the hook and slot lengths
   (matters more for a printed plate than the slide itself).
3. I/O: measure from each black rear-face edge to the HDMI and USB shell centres at three points along the length
   (square or caliper depth rod); print a thin rear-edge test coupon with the cut-outs before a full plate.
4. Optional: the Cults3D raw scan, only with seller confirmation (real, assembled, post-Nov-2020, scanner, revision).
5. Revision tolerance: give port cut-outs ~±1.5 mm clearance so one plate fits CFI-10xx/11xx/12xx.

## Caveats
- All independent widths are tape measurements (±1 to ±5 mm) and none separates fan end from drive end; the case
  for 114 rests on combining them with Mike's 95 mm reading.
- "Largest projection" is inferred, not defined by Sony.
- NCC ruler photos could not be checked for a readable scale.
- Render-based or pre-launch sources (2020 EvilBoris Sketchfab model, LetsGoDigital/Reddit size comparisons,
  A9VG leaked-plate paper-scale estimates) were excluded.

## Sources
- game8bit — https://game8bit.com/media/ps5-box-size/
- PlayStation Blog, PS5 Ultimate FAQ — https://blog.playstation.com/2020/11/09/ps5-the-ultimate-faq/
- Sony CFI-1200A safety guide (JP) — https://manuals.playstation.net/document/pdf/CFI-1200A_5.5_2.pdf
- PlayStation Blog, launch post — https://blog.playstation.com/2020/09/16/playstation-5-launches-in-november-starting-at-399-for-ps5-digital-edition-and-499-for-ps5-with-ultra-hd-blu-ray-disc-drive/
- TechRadar — https://www.techradar.com/news/new-ps5-images-offer-the-best-look-yet-at-the-consoles-size
- kocpc — https://www.kocpc.com.tw/archives/344898
- Gigazine — https://gigazine.net/gsc_news/en/20200920-ps5-photos-how-big/
- ResetEra p.2 — https://www.resetera.com/threads/official-ps5-images-with-measurements-from-fccid-io.290234/page-2
- ResetEra p.3 — https://www.resetera.com/threads/official-ps5-images-with-measurements-from-fccid-io.290234/page-3
- couple-game — https://couple-game.net/ps5-size/
- itomarublog — https://itomarublog.com/open-ps5/
- Tom's Guide — https://www.tomsguide.com/uk/news/ps5-photos-just-leaked-meet-the-biggest-console-ever
- HotHardware — https://hothardware.com/news/playstation-5-looks-massive-in-photo
- fccid.io NCC — https://fccid.io/NCC/CCAB20LP129AT2
- HIDEit — https://hideitmounts.com/products/hideit-ps5-sony-playstation-5-mount
- Firefold — https://www.firefold.com/products/hideit-ps5-sony-playstation-5-mount-pro-bundle
- Monoprice — https://www.monoprice.com/product?p_id=47565
- VIVO — https://vivo-us.com/products/mount-ps5b
- dbrand — https://dbrand.com/search/device/playstation-5-disc
- sizevista — https://sizevista.com/gaming-console-ps5-dimensions/
- Wikipedia — https://en.wikipedia.org/wiki/PlayStation_5
- dimensions.com — https://www.dimensions.com/element/playstation-5
- comparesizes — https://comparesizes.com/comparison/PS5-disc-vs-PS5-digital-vs-PS5-Slim-disc-vs-PS5-Slim-digital-size/1717973113309
- oreateai — https://learn.oreateai.com/learn/exact-dimensions-for-every-ps5-model-from-original-to-pro
- Alibaba guide — https://electronics.alibaba.com/buyingguides/ps5-dimensions-guide-slim-vs.-original-vs.-pro-size-comparison
- Cults3D tags — https://cults3d.com/en/tags/playstation-5 , https://cults3d.com/en/tags/ps5
- iFixit device page — https://www.ifixit.com/Device/PlayStation_5
- Dribbble (GygInfographics) — https://dribbble.com/shots/24857570-PS5-Exploded-View
- iFixit guide PDF — https://documents.cdn.ifixit.com/pdf/ifixit/guide_138280_en.pdf
- Fasttech — https://fasttechstore.com/playstation-5-1 , https://fasttechstore.com/playstation-5-1/p/playstation-5-io-port-frame-for-cfi-12xx , https://fasttechstore.com/playstation-5-1/p/playstation-5-io-port-frame
- XtremePS3 — https://www.xtremeps3.com/2020/09/17/what-ports-does-the-ps5-have/
- iFixit Faceplates Replacement — https://www.ifixit.com/Guide/PlayStation+5+Faceplates+Replacement/147825
- PlayStation support — https://www.playstation.com/en-us/support/hardware/replace-ps5-console-cover/
- Glistco — https://www.glistco.com/blogs/glistco-world/how-to-remove-and-install-ps5-plates
- 9meters — https://9meters.com/technology/consoles/how-to-remove-a-ps5-cover
- Notebookcheck (shell images) — https://www.notebookcheck.net/Leaked-PS5-shell-images-suggest-that-the-device-s-plates-are-removable-and-the-PlayStation-5-is-a-colossal-console.483270.0.html
- Notebookcheck (size comparison) — https://www.notebookcheck.net/PS5-size-comparison-PlayStation-5-towers-over-the-Xbox-Series-X-and-even-looks-down-on-the-king-sized-PS3.479012.0.html
