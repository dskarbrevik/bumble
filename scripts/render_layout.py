"""Render components/layout/layout.py to components/layout/renders/layout_iter{N}.png.

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
sys.path.insert(0, str(ROOT / "components" / "layout"))
import layout  # noqa: E402

KEY_FACE, MOD_FACE, SPACE_FACE = "#f2f2f0", "#dddddb", "#cdd6e0"
EDGE, LEGEND, BG = "#8a8a88", "#3a3a38", "#fafaf8"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", type=int, required=True, help="LOG entry number N")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

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

    ax.set_title(f"bumble — iter {args.iter} — {len(keys)} keys — "
                 f"Alice geometry, split extra {layout.SPLIT_EXTRA:g}u",
                 fontsize=11, color=LEGEND)
    ax.autoscale()
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.axis("off")

    out = (Path(args.out) if args.out
           else ROOT / "components" / "layout" / "renders" / f"layout_iter{args.iter}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=BG)
    print(f"wrote {out} ({len(keys)} keys)")

    old = sorted(out.parent.glob("layout_iter*.png"), key=lambda p: p.stat().st_mtime)
    for p in old[:-10]:
        p.unlink()
        print(f"gc: removed {p.name}")


if __name__ == "__main__":
    main()
