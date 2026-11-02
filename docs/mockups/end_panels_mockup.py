"""Throwaway mockup: true-scale SVGs (mm) from slab.py's numbers. Usage: gen_ends.py <out.html>"""
import sys

PLATE, CORE, DRIVE, GAP, MESH, BG, INK = "#c6c4be", "#1d1d1f", "#dcdcd8", "#6b6b70", "#2f6fb0", "#f4f5f7", "#222"
PN, PS, FL = 59.2, -54.8, 2.5


def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {extra}/>'


def text(x, y, s, size=9, anchor="middle", fill=INK, weight="400"):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-family="sans-serif" font-weight="{weight}">{s}</text>'


def svg(vb, body):
    return f'<svg viewBox="{vb}" style="width:100%;height:auto;display:block;background:{BG};border-radius:6px">{body}</svg>'


def front():
    """looking at the face: west left, east right. sx = 380 - z, sy = -x"""
    sx = lambda z: 380 - z
    top = lambda z: 22.2 + 17.5 * z / 380
    bot = lambda z: -17.8 - 17.5 * z / 380
    b = poly([(sx(382), -PN + 0), (sx(-2), -PN), (sx(-2), 53), (sx(382), 53)], GAP)
    b += poly([(sx(z), -top(z)) for z in (0, 380)] + [(sx(z), -bot(z)) for z in (380, 0)], CORE)
    b += poly([(sx(135), 17), (sx(0), 17), (sx(0), 50.8), (sx(135), 50.8)], DRIVE, 'stroke="#999" stroke-width=".4"')
    b += poly([(sx(382), -61.7), (sx(-2), -61.7), (sx(-2), -43.7), (sx(382), -43.7)], PLATE, 'stroke="#888" stroke-width=".4"')
    a, c = sx(165), sx(140)
    b += (f'<path d="M{sx(382)},39.3 L{a},39.3 C{a + 14},39.3 {c - 6},52.5 {c + 8},52.5 L{sx(-2)},52.5 L{sx(-2)},57.3 L{sx(382)},57.3 Z" '
          f'fill="{PLATE}" stroke="#888" stroke-width=".4"/>')
    b += text(190, -67, "NORTH (flat plate)") + text(190, 69, "SOUTH (disc plate)")
    b += text(-8, 3, "W", 11, weight="700") + text(388, 3, "E", 11, weight="700")
    b += text(300, 36, "disc drive", 8) + text(120, -48, "level edge, 15.5 mm deep", 7.5)
    return svg("-20 -78 420 156", b)


def rear():
    """looking at the back: east left, west right. sx = z, sy = -x"""
    top = lambda z: 42.2 - 17.5 * z / 380
    bot = lambda z: -37.8 + 17.5 * z / 380
    b = poly([(-2, -PN), (382, -PN), (382, 41.8), (-2, 41.8)], GAP)
    b += poly([(z, -top(z)) for z in (0, 380)] + [(z, -bot(z)) for z in (380, 0)], CORE)
    b += poly([(-2, -61.7), (382, -61.7), (382, -46.2), (-2, -46.2)], PLATE, 'stroke="#888" stroke-width=".4"')
    b += poly([(-2, 41.8), (382, 41.8), (382, 57.3), (-2, 57.3)], PLATE, 'stroke="#888" stroke-width=".4"')
    b += text(190, -67, "NORTH") + text(190, 69, "SOUTH")
    b += text(-8, 3, "E", 11, weight="700") + text(388, 3, "W", 11, weight="700")
    b += text(330, -30, "up to 21.5 mm open", 7.5, fill="#fff") + text(190, 53, "level edge, 13 mm deep", 7.5)
    return svg("-20 -78 420 156", b)


def section(z_w, z_e_n, z_e_s, z_w_n, z_w_s, mesh, note):
    """cut through the middle, west left, east right. Plate spans are given as z limits."""
    sx = lambda z: 380 - z
    b = poly([(sx(0), -37.5), (sx(380), -54.5), (sx(380), 38.5), (sx(0), 50.5)], CORE)
    b += poly([(sx(z_w_n), -61.7), (sx(z_e_n), -61.7), (sx(z_e_n), -PN), (sx(z_w_n), -PN)], PLATE, 'stroke="#888" stroke-width=".4"')
    b += poly([(sx(z_w_s), 54.8), (sx(z_e_s), 54.8), (sx(z_e_s), 57.3), (sx(z_w_s), 57.3)], PLATE, 'stroke="#888" stroke-width=".4"')
    for pts in mesh:
        d = " ".join(f"{sx(z):.1f},{-x:.1f}" for z, x in pts)
        b += f'<polyline points="{d}" fill="none" stroke="{MESH}" stroke-width="2.4" stroke-dasharray="3 1.6"/>'
    b += text(-52, 3, "W", 11, weight="700") + text(432, 3, "E", 11, weight="700")
    b += text(190, 72, note, 9)
    return svg("-62 -76 504 158", b)


OPTS = [
    ("a", "A", "Wedge fillers", "Plates stay 384 mm long. Mesh only fills the big open wedge at each end, slanting in toward the core. The core's black end stays visible, so its twist still shows.",
     section(0, -2, -2, 382, 382, [[(-2, 59.2), (12, 41.5)], [(382, -54.8), (370, -42.5)]], "384 mm long, no growth")),
    ("b", "B", "One full slant", "One mesh face per end, running from north plate edge to south plate edge. The north plate is longer than the south, so the silhouette is a trapezoid. The core's end is hidden behind mesh.",
     section(0, -27, -5, 407, 385, [[(-27, 59.2), (-5, -54.8)], [(407, 59.2), (385, -54.8)]], "north plate 434 mm, south plate 390 mm")),
    ("c", "C", "Two slants, pinched waist", "Two mesh faces per end, angling in from both plates to meet near the core. Both plates are the same length and overhang the core, so the shape looks like a shadow line at each end.",
     section(0, -22, -22, 402, 402, [[(-22, 59.2), (-3, 2.2), (-22, -54.8)], [(402, 59.2), (383, 2.2), (402, -54.8)]], "both plates 424 mm long")),
]

html = f"""<h2>West and east panels: which shape did you picture?</h2>
<p class="subtitle">True scale, from the current model's numbers. Grey = plates, black = core, blue dashes = mesh. Click the closest one.</p>
<div class="options">
"""
for key, letter, title, desc, art in OPTS:
    html += f"""<div class="option" data-choice="{key}" onclick="toggleSelect(this)">
<div class="letter">{letter}</div>
<div class="content"><h3>{title}</h3><p>{desc}</p>{art}</div>
</div>
"""
html += f"""</div>
<div class="section" style="margin-top:28px">
<h3>Already decided from your message: level edges and the disc swoop</h3>
<p class="subtitle">These two don't change with A, B or C. Check that they match what you meant.</p>
<div class="split">
<div class="mockup"><div class="mockup-header">Face (you looking at it)</div><div class="mockup-body">{front()}</div></div>
<div class="mockup"><div class="mockup-header">Back</div><div class="mockup-body">{rear()}</div></div>
</div>
</div>
"""
open(sys.argv[1], "w").write(html)
