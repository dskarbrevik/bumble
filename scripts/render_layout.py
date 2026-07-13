"""Render design/layout.py to design/renders/layout_iter{N}.png.

Usage: uv run python scripts/render_layout.py --iter N
Keeps only the latest 10 iter renders (CLAUDE.md versioning rule).
"""

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "design"))
import layout  # noqa: E402

KEY_FACE, MOD_FACE, SPACE_FACE = "#f2f2f0", "#dddddb", "#cdd6e0"
EDGE, LEGEND, BG = "#8a8a88", "#3a3a38", "#fafaf8"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", type=int, required=True, help="LOG entry number N")
    ap.add_argument("--out", default=None)
    ap.add_argument("--split-extra", type=float, default=None,
                    help="override layout.SPLIT_EXTRA (u) for this render")
    ap.add_argument("--screen", default=None,
                    help="ghost a screen module: 'W_MM,H_MM,label' (module outline)")
    ap.add_argument("--screen-active", default=None,
                    help="active area 'W_MM,H_MM' or 'round,DIA_MM' inside the module")
    ap.add_argument("--screen-bottom-mm", type=float, default=None,
                    help="module bottom edge y in mm (default: 2mm above plate edge)")
    args = ap.parse_args()

    if args.split_extra is not None:
        layout.SPLIT_EXTRA = args.split_extra
    keys = layout.placed()
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    inset = layout.KEY_INSET
    for k in keys:
        face = (SPACE_FACE if k["legend"] == "" else
                MOD_FACE if len(k["legend"]) > 1 else KEY_FACE)
        p = FancyBboxPatch((k["x"] + inset, k["y"] + inset),
                           k["w"] - 2 * inset, 1 - 2 * inset,
                           boxstyle="round,pad=0,rounding_size=0.12",
                           facecolor=face, edgecolor=EDGE, linewidth=1.0)
        p.set_transform(Affine2D().rotate_deg_around(*k["pivot"], k["angle"])
                        + ax.transData)
        ax.add_patch(p)
        if k["legend"]:
            ax.text(*k["center"], k["legend"], ha="center", va="center",
                    fontsize=11 if len(k["legend"]) == 1 else 8,
                    color=LEGEND, rotation=-k["angle"])

    title_extra = ""
    if args.screen:
        w_mm, h_mm, label = args.screen.split(",", 2)
        w, h = float(w_mm) / layout.UNIT_MM, float(h_mm) / layout.UNIT_MM
        # centered on the board's optical centerline — the apex gap between 6
        # and 7 (NOT the spacebar gap, which sits left of it); bottom near the
        # plate edge
        k6 = next(k for k in keys if k["legend"] == "6")
        k7 = next(k for k in keys if k["legend"] == "7")
        xc = (max(x for x, _ in k6["corners"]) +
              min(x for x, _ in k7["corners"])) / 2
        plate_bot = max(y for k in keys for _, y in k["corners"]) \
            + layout.PLATE_MARGIN_MM / layout.UNIT_MM
        bot = (args.screen_bottom_mm / layout.UNIT_MM if args.screen_bottom_mm
               else plate_bot - 2 / layout.UNIT_MM)
        ax.add_patch(plt.Rectangle((xc - w / 2, bot - h), w, h, fill=False,
                                   edgecolor="#c0392b", linewidth=1.4,
                                   linestyle="--"))
        if args.screen_active:
            a = args.screen_active.split(",")
            if a[0] == "round":
                d = float(a[1]) / layout.UNIT_MM
                ax.add_patch(plt.Circle((xc, bot - h / 2), d / 2, fill=True,
                                        facecolor="#2c3e50", alpha=0.25,
                                        edgecolor="#c0392b", linewidth=0.8))
            else:
                aw, ah = float(a[0]) / layout.UNIT_MM, float(a[1]) / layout.UNIT_MM
                ax.add_patch(plt.Rectangle((xc - aw / 2, bot - h / 2 - ah / 2),
                                           aw, ah, fill=True,
                                           facecolor="#2c3e50", alpha=0.25,
                                           edgecolor="#c0392b", linewidth=0.8))
        ax.text(xc, bot - h - 0.12, label, ha="center", va="bottom",
                fontsize=8, color="#c0392b")
        title_extra = f" — screen {w_mm}x{h_mm}mm"
        if bot > plate_bot:
            title_extra += f" (chin +{(bot - plate_bot) * layout.UNIT_MM:.0f}mm)"

    ax.set_title(f"bumble — iter {args.iter} — {len(keys)} keys — "
                 f"Alice geometry, split extra {layout.SPLIT_EXTRA:g}u{title_extra}",
                 fontsize=11, color=LEGEND)
    ax.autoscale()
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.axis("off")

    out = (Path(args.out) if args.out
           else ROOT / "design" / "renders" / f"layout_iter{args.iter}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=BG)
    print(f"wrote {out} ({len(keys)} keys)")

    old = sorted(out.parent.glob("layout_iter*.png"), key=lambda p: p.stat().st_mtime)
    for p in old[:-10]:
        p.unlink()
        print(f"gc: removed {p.name}")


if __name__ == "__main__":
    main()
