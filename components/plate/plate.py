"""bumble switch plate — parametric, driven by design/layout.py placed().

Outline: convex hull of each half's key corners, offset outward by the plate
margin, unioned (the halves' offset hulls overlap at the apex), filleted.
One square cutout per switch, rotated with its zone. Exports STL + PNG render.

Usage: uv run python components/plate/plate.py --iter N
Outputs: components/plate/plate_iter{N}.stl,
         components/plate/renders/plate_iter{N}.png (gitignored scratch)
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "design"))
import layout  # noqa: E402

from build123d import Polygon, extrude, fillet, offset, export_stl, Kind  # noqa: E402

U = layout.UNIT_MM


def hull(points):
    """Monotone-chain convex hull, returns CCW points."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (
                (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1])
                - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0])
            ) <= 0:
                out.pop()
            out.append(p)
        return out

    lower, upper = half(pts), half(reversed(pts))
    return lower[:-1] + upper[:-1]


def poly_mm(pts_u):
    """u -> mm, flip y so the STL isn't mirrored (layout y is down)."""
    return Polygon(*[(x * U, -y * U) for x, y in pts_u], align=None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", type=int, required=True)
    args = ap.parse_args()

    keys = layout.placed()
    left = [p for k in keys if k["zone"] in ("LO", "LI") for p in k["corners"]]
    right = [p for k in keys if k["zone"] in ("RI", "RO") for p in k["corners"]]

    # center bridge: spans the apex + spacebar gap (placeholder screen bay)
    bridge = [p for k in keys if k["legend"] in ("5", "6", "7", "8", "")
              for p in k["corners"]]

    outline = None
    for pts in (hull(left), hull(right), hull(bridge)):
        face = offset(poly_mm(pts), layout.PLATE_MARGIN_MM, kind=Kind.ARC)
        outline = face if outline is None else outline + face

    try:
        outline = fillet(outline.vertices(), layout.PLATE_CORNER_R_MM)
    except Exception as e:
        print(f"fillet skipped: {e}")

    holes = None
    c = layout.CUTOUT_MM / 2 / U  # half cutout in u
    for k in keys:
        cx, cy = k["center"]
        ang, piv = k["angle"], k["pivot"]
        base = [(cx + dx, cy + dy) for dx, dy in
                ((-c, -c), (c, -c), (c, c), (-c, c))]
        # corners are in final coords already; rotate the square about its own
        # center by the zone angle to match switch orientation
        import math
        r = math.radians(ang)
        pts = [(cx + (x - cx) * math.cos(r) - (y - cy) * math.sin(r),
                cy + (x - cx) * math.sin(r) + (y - cy) * math.cos(r))
               for x, y in base]
        h = poly_mm(pts)
        holes = h if holes is None else holes + h

    plate = extrude(outline - holes, amount=layout.PLATE_THICK_MM)

    bb = plate.bounding_box()
    n = len(keys)
    print(f"{n} cutouts; plate {bb.size.X:.1f} x {bb.size.Y:.1f} mm, "
          f"{layout.PLATE_THICK_MM} mm thick")

    stl = HERE / f"plate_iter{args.iter}.stl"
    export_stl(plate, str(stl))
    print(f"wrote {stl}")

    import pyvista as pv
    mesh = pv.read(str(stl))
    pl = pv.Plotter(shape=(2, 1), off_screen=True, window_size=(1700, 1500))
    pl.set_background("#fafaf8")
    pl.subplot(0, 0)
    pl.add_mesh(mesh, color="#b9c2cc", show_edges=False)
    pl.add_text(f"bumble plate — iter {args.iter} — {n} keys — "
                f"{bb.size.X:.0f} x {bb.size.Y:.0f} mm", font_size=11, color="#3a3a38")
    pl.view_xy()
    pl.enable_parallel_projection()
    pl.subplot(1, 0)
    pl.add_mesh(mesh, color="#b9c2cc", show_edges=False)
    pl.view_isometric()
    out = HERE / "renders" / f"plate_iter{args.iter}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    pl.screenshot(str(out))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
