"""Annotate the iFixit / Creative Electron X-ray with rear and front I/O positions.

Output: sources/reference-images/xray_ports_overlay.png (CC BY-NC-SA 3.0, derivative of the X-ray).
Positions are read by eye from the X-ray in original pixels; see docs/research/reverse-engineering-2026-11-09.md.
Scale: 0.705 mm/px (outline 553 px = 390 mm; cross-checked by the 120 mm fan = 170 px).
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources/reference-images/xray_creative_electron_ifixit.jpg"
OUT = ROOT / "sources/reference-images/xray_ports_overlay.png"

S = 390 / 553          # mm per px
DRIVE_END = 572        # px, right edge of the console outline (drive end)
REAR_Y, FRONT_Y = 52, 392
REAR = [(510, 530, "Power"), (451, 471, "HDMI"), (398, 421, "LAN"), (367, 386, "USB 2"), (333, 352, "USB 1")]
FRONT = [(292, 312, "USB-A"), (323, 336, "USB-C"), (348, 550, "Disc drive")]


def mm_from_drive_end(x0, x1):
    return (DRIVE_END - x1) * S, (DRIVE_END - x0) * S


def main():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    big = im.resize((w * 2, h * 2), Image.LANCZOS)
    d = ImageDraw.Draw(big)

    def mark(x0, x1, y, label, col, above):
        a, b = mm_from_drive_end(x0, x1)
        d.rectangle([x0 * 2, (y - 6) * 2, x1 * 2, (y + 6) * 2], outline=col, width=3)
        d.text((x0 * 2, (y - 26) * 2 if above else (y + 10) * 2), f"{label}\n{a:.0f}-{b:.0f}", fill=col)

    for x0, x1, label in REAR:
        mark(x0, x1, REAR_Y, label, (220, 30, 30), False)
    for x0, x1, label in FRONT:
        mark(x0, x1, FRONT_Y, label, (20, 90, 200), True)
    d.text((20, 20), "REAR edge (top) - mm from DRIVE END (right), +-4 mm. "
                     "X-ray: Creative Electron / iFixit, CC BY-NC-SA 3.0", fill=(0, 0, 0))
    d.text((20, h * 2 - 40), "FRONT edge (bottom). Scale 0.705 mm/px from fan diameter 120 mm and length 390 mm",
           fill=(0, 0, 0))
    big.save(OUT)
    for x0, x1, label in REAR + FRONT:
        a, b = mm_from_drive_end(x0, x1)
        print(f"{label:10s} {a:5.0f} - {b:5.0f} mm from drive end")


if __name__ == "__main__":
    main()
