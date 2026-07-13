"""bumble case — v1 look-and-feel shell, driven by design/layout.py.

High-profile "pebble": walls rise to the keycap skirt so switch bodies are
hidden; the top is one continuous deck with two key wells (one per half) and
the round screen set flush into the solid bridge between them. The whole body
is a 6-degree wedge (back high), flat on the desk.

v1 scope (LOG 18): OUTER FORM ONLY — a solid body with wells and screen
aperture. No interior cavity, plate ledge, bosses, or USB port yet; those
come once the PCB exists. Heights assume MX: cap skirt sits ~6.7 mm above
the plate, so a 6 mm deck hides switch bodies without touching caps.

Usage: uv run python components/case/case.py --iter N
Outputs: components/case/case_iter{N}.stl,
         components/case/renders/case_iter{N}.png (gitignored scratch)
"""

import argparse
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "design"))
import layout  # noqa: E402

from build123d import (Box, Circle, Kind, Polygon, Pos, Rot, extrude,  # noqa: E402
                       fillet, offset, export_stl)

U = layout.UNIT_MM

# case parameters (board frame: z up, plate top = z 0, y flipped from layout)
WALL_MM = 3.0            # outer skin beyond the plate outline
DECK_Z = 6.0             # deck top above plate top — just under the cap skirt
BODY_DEPTH = 40.0        # pre-tilt slab depth below plate (trimmed by desk cut)
WELL_CLEAR = 1.5         # key well clearance beyond cap edges
TILT_DEG = 6.0           # typing wedge, back edge high
FRONT_DECK_MM = 14.0     # deck-top height above desk at the front edge


def poly_mm(pts_u):
    return Polygon(*[(x * U, -y * U) for x, y in pts_u], align=None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", type=int, required=True)
    args = ap.parse_args()

    keys = layout.placed()
    hulls = layout.footprint_hulls(keys)

    # outer skin: plate outline + wall
    outline = None
    for pts in hulls:
        face = offset(poly_mm(pts), layout.PLATE_MARGIN_MM + WALL_MM,
                      kind=Kind.ARC)
        outline = face if outline is None else outline + face

    # NB: the y-flip in poly_mm reverses winding, so these faces' normals
    # point -Z and a bare extrude() goes DOWNWARD — always pass dir=(0,0,1),
    # and translate the SOLID after extruding (extrude ignores face Location).
    UP = (0, 0, 1)
    body = Pos(0, 0, -BODY_DEPTH) * extrude(outline,
                                            amount=DECK_Z + BODY_DEPTH, dir=UP)
    v0 = body.volume

    # key wells: one per half (hulls[0], hulls[1]); the bridge hull stays
    # solid. The screen's deck ring is protected from the well cuts — where
    # ring and well would overlap, the ring wins (SPLIT_EXTRA is solved so the
    # ring still clears the caps by 0.8mm).
    s = layout.SCREEN
    sx, sy = layout.screen_center(keys)
    ring_guard = Pos(sx * U, -sy * U, -3) * extrude(
        Circle(s["ring_outer_dia_mm"] / 2), amount=DECK_Z + 6, dir=UP)
    for pts in hulls[:2]:
        well = offset(poly_mm(pts), WELL_CLEAR, kind=Kind.ARC)
        cut = Pos(0, 0, -2) * extrude(well, amount=DECK_Z + 4, dir=UP)
        body -= (cut - ring_guard)

    # flush-deck screen: aperture through the ring, module pocket from below
    body -= Pos(sx * U, -sy * U, -2) * extrude(
        Circle(s["aperture_dia_mm"] / 2), amount=DECK_Z + 4, dir=UP)
    body -= Pos(sx * U, -sy * U, 0) * extrude(
        Circle(s["pocket_dia_mm"] / 2),
        amount=DECK_Z - 0.8, dir=UP)   # 0.8mm lip retains the module
    assert body.volume < v0 * 0.999, "well/aperture cuts removed no material"

    # soften the deck edges (outer rim, well rims, screen ring)
    try:
        top_edges = [e for e in body.edges()
                     if abs(e.center().Z - DECK_Z) < 0.01]
        body = fillet(top_edges, 0.8)
    except Exception as e:
        print(f"deck fillet skipped: {e}")

    # tilt and cut a flat desk plane so the front deck sits FRONT_DECK_MM high
    bb0 = body.bounding_box()
    t = math.radians(TILT_DEG)
    z_front_deck = bb0.min.Y * math.sin(t) + DECK_Z * math.cos(t)
    z_cut = z_front_deck - FRONT_DECK_MM
    body = Rot(TILT_DEG, 0, 0) * body
    bb1 = body.bounding_box()
    trim = Pos((bb1.min.X + bb1.max.X) / 2, (bb1.min.Y + bb1.max.Y) / 2,
               z_cut - 60) * Box(bb1.size.X + 20, bb1.size.Y + 20, 120)
    body -= trim
    body = Pos(0, 0, -z_cut) * body

    bb = body.bounding_box()
    z_back_deck = bb0.max.Y * math.sin(t) + DECK_Z * math.cos(t) - z_cut
    print(f"case {bb.size.X:.1f} x {bb.size.Y:.1f} mm footprint, "
          f"deck {FRONT_DECK_MM:.0f} mm front / {z_back_deck:.1f} mm back, "
          f"tilt {TILT_DEG:g} deg")

    stl = HERE / f"case_iter{args.iter}.stl"
    export_stl(body, str(stl))
    print(f"wrote {stl}")

    import pyvista as pv
    mesh = pv.read(str(stl))
    pl = pv.Plotter(shape=(3, 1), off_screen=True, window_size=(1700, 2100))
    pl.set_background("#fafaf8")
    pl.subplot(0, 0)
    pl.add_mesh(mesh, color="#d9c9a3", smooth_shading=True)
    pl.add_text(f"bumble case — iter {args.iter} — "
                f"{bb.size.X:.0f} x {bb.size.Y:.0f} mm — {TILT_DEG:g}° wedge",
                font_size=11, color="#3a3a38")
    pl.view_xy()
    pl.enable_parallel_projection()
    pl.enable_eye_dome_lighting()   # reveals wells/aperture in the flat top view
    cx = (bb.min.X + bb.max.X) / 2
    cy = (bb.min.Y + bb.max.Y) / 2
    pl.subplot(1, 0)
    pl.add_mesh(mesh, color="#d9c9a3", smooth_shading=True)
    pl.camera_position = [(cx + bb.size.X * 0.25, cy - bb.size.X * 1.05,
                           bb.size.X * 0.55),
                          (cx, cy, 0), (0, 0, 1)]
    pl.subplot(2, 0)
    pl.add_mesh(mesh, color="#d9c9a3", smooth_shading=True)
    pl.camera_position = [(cx + 1000, cy, 15), (cx, cy, 15), (0, 0, 1)]
    pl.enable_parallel_projection()
    pl.camera.parallel_scale = bb.size.Y * 0.75
    out = HERE / "renders" / f"case_iter{args.iter}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    pl.screenshot(str(out))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
