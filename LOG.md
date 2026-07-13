# Log — bumble (formerly wing60; renamed at entry 8)

Append-only iteration log, newest entry first. One entry per iteration (one gated
change), numbered N, N+1, … Never edit a prior entry — a reversed decision gets a new
entry noting the reversal. If this file grows unwieldy, split into an index here +
per-entry files in `records/` (keep this header).

Entry schema — omit empty fields, keep entries short:

```
## N — YYYY-MM-DD — short title
**Phase:** 3b
**Did:** the one change made
**Observed:** what renders/measurements actually showed
**Issues:** anything wrong or suspicious
**Decision:** continue / revert / escalate — and why
**Open:** questions for the human
```

---

## 18 — 2026-07-13 — round screen baked in; case v1 (high-profile pebble, 6° wedge)
**Phase:** 0
**Did:** Human picked the round display + case with matching design language +
a few degrees of tilt; AskUser answers: 6° tilt, flush deck (profile question
unanswered -> went with recommended high-profile pebble). Baked into
design/layout.py: SCREEN spec block + screen_center() + footprint_hulls()
(hull logic moved from plate.py so plate and case share one outline source).
First split bake at 0.85u collided in the case: a flush ring needs deck
material for the module POCKET (37.5 carrier + walls), not just glass —
re-solved min split for ring outer 40.6mm at 0.8mm cap clearance ->
SPLIT_EXTRA 1.09u, cy 4.125u; plate now passes the module fully (38.5 hole).
New components/case/case.py: solid look-and-feel shell — pebble outline
(wall +3), per-half key wells, screen ring guarded from well cuts, module
pocket w/ 0.8 lip, 6° wedge, flat desk cut, deck 14mm front / 28 back.
Two silent-boolean bugs found (extrude ignores face Location; y-flipped faces
extrude -Z) -> dir=(0,0,1) everywhere + volume assert; lesson in CLAUDE.md.
**Observed:** case_iter18: wells read clean, ring sits between halves like a
crown, bulging slightly into each well — looks deliberate. Deck-edge fillets
fail (sharp rims) — cosmetic pass later. Footprint 362 x 134mm.
**Decision:** continue; case v1 to human for direction sign-off.
**Open:** case profile confirm (high-profile assumed); USB port position;
interior (cavity/ledge/bosses) once PCB exists; deck fillet fix.

## 17 — 2026-07-12 — right B removed (59 keys); ghost centering bug fixed; round screen leads
**Phase:** 0
**Did:** Human: drop the mirrored right B. layout.py now 59 keys (docstring
keeps the 1.48u-apex provenance note); README table/count, ROADMAP acceptance
test, BOM v0.1.2 (switches/diodes 59), repo description updated. Fixed a ghost
placement bug the human spotted in the iter-15/16 mockups: screens were
centered between the SPACEBARS, which sits ~0.5u left of the board's optical
centerline (the 6|7 apex gap) — that's why ghosts overlapped keys. Re-solved
min split on the true centerline with the B gone: the void at the old B row
opens 11mm -> 32mm, and the winners flip — round GC9A01 glass-only needs
+0.85u split (+16mm board) while the 1.69" rect needs MORE than before
(+1.24u) because it now binds on the surviving left B. Rendered corrected
mockups (screenfit_round_iter17, screenfit_169_iter17) + layout/plate iter17
(59 cutouts, 335.6 x 125.7 mm unchanged).
**Observed:** the circle nestles into the V riding the apex line — reads like
a watch face, angle-neutral against both ±12° wedges; the rect is clean but
reads as a phone slotted into the keyboard.
**Decision:** recommend round GC9A01, glass-only through a circular plate
aperture; escalate aesthetic call to human.
**Open:** confirm round vs rect (or ask for a rotated-rect mockup); carrier-
under-plate clearance vs switch bodies to verify in CAD once picked.
**Phase:** 0
**Did:** Human leans pure-widen and asked (a) is the 1.69" the lochord-dev
screen, (b) e-ink/low-power options, (c) big LiPo under the PCB. (a) Yes —
lochord-dev's hardware_data/st7789_display.yaml has CALIPER-VERIFIED dims of a
module the human owns: same 1.69" 240x280 panel (active 27.97x32.63, glass
30x37.5) on a generic 31x48 carrier, 8-pin header, 90 mA max draw — reusable
ground truth for Phase 1. Rendered its pure-widen fit (needs 1.171u vs
Waveshare carrier's 1.114u; taller carrier crowds the B keys more). Built
screensweep_iter16 comparison sheet of all pure-widen options. (b) ZMK
low-power displays are monochrome-only in practice (Sharp memory LCD =
nice!view, e-ink = Corne-ish Zen); color+animation requires a backlit TFT —
it's a pick-2 triangle: color/animation, low power, ZMK-off-the-shelf.
(c) Big LiPo under PCB is the right mitigation: huge unibody footprint fits
2000-5000 mAh easily; screen at 90 mA full-on = 22-55 h continuous on those
packs, weeks with timeout/dimming; note stock module chargers (~100 mA) are
too slow for big packs — our custom PCB should carry a 500 mA+ charger IC
(Phase 3 schematic item).
**Decision:** continue; screen pick still with human (pure-widen lineup
delivered).
**Open:** which panel/carrier; confirm big-LiPo + charger-IC direction.
**Phase:** 0
**Did:** Human decided wireless = BLE-only first take (dongle maybe later).
Researched color displays + ZMK feasibility (research agents blocked by session
limit; done inline). Firmware: prospector and YADS (zmk-dongle-screen) both
drive ST7789 SPI in full color from nRF52840 under ZMK/LVGL — the "ZMK is
monochrome-only" fear is dead; open risk shifts to battery draw of backlight
on a keyboard-mounted screen (mitigations: idle timeout, dimming, ambient
sensor). Parts shortlist (Waveshare modules): 1.69" 240x280 ST7789V2
31.5x39.0mm; 1.47" 172x320 22.0x38.5mm; 1.28" round GC9A01 37.5x40.4mm;
2.0" 320x240 58x35mm. Added --screen/--split-extra ghost options to
render_layout.py; measured the real center void (~11mm between Bs, ~30-38mm
between spacebars — the old ~51mm guess was wrong); computed min SPLIT_EXTRA
per candidate and rendered 5 mockups (screenfit_*_iter15).
**Observed:** pure-widen placements need 0.60-1.46u extra split (board grows
11-28mm) and push the screen up into the narrow wedge; a "+0.25u split + ~14mm
center chin" variant keeps the board compact and seats the 1.69" between the
spacebars — visually the strongest.
**Decision:** recommend 1.69" ST7789V2 + chin strategy; escalate to human.
**Open:** pick screen + placement (pure-widen vs chin); OK to carry backlight
battery risk to Phase 3 power budget?
**Phase:** 0
**Did:** Human: only actual components deserve a `components/` subdir; keep a
top-level `design/` for whole-device intent and idea iteration. Moved
components/layout/ back to design/ (layout.py + design/renders/ for layout and
concept renders); components/ now holds only real parts (plate today; pcb,
case, firmware on first use). CLAUDE.md Layout gains the second axis —
component vs concept; README/ROADMAP paths and both scripts updated; LOG-13
lesson amended with the refinement.
**Observed:** layout_iter14 + plate_iter14 regenerate identically (60 keys,
335.6 x 125.7 mm) — pure restructure, no geometry change.
**Decision:** continue.

## 13 — 2026-07-12 — rescaffold: components/ + parts/bom.json + bundle.json
**Phase:** 0
**Did:** Human: regroup the repo by what's being built, not by artifact type.
`design/` + `cad/` + `renders/` dissolved into `components/{layout,plate}/`
(pcb, case, firmware join on first use), each component owning its source,
scratch outputs, and renders/. New `parts/bom.json` (versioned; schema in
parts/README.md) seeded with 7 candidate line items = the buy list; new root
`bundle.json` = append-only log pairing component versions + BOM version per
release (replaces the planned releases/ manifest.md). CLAUDE.md Layout/Releases,
README, ROADMAP, .gitignore (`**/renders/*`), and both script paths updated;
lesson recorded for fablab upstreaming.
**Observed:** layout_iter13 + plate_iter13 regenerate identically (60 keys,
335.6 x 125.7 mm) — pure restructure, no geometry change.
**Decision:** continue.

## 12 — 2026-07-12 — fresh git history
**Phase:** 0
**Did:** Human: restart the repo without the accumulated history. Old repo
renamed bumble-tmp (then deleted); this tree re-committed as the first commit
of a new dskarbrevik/bumble. Note: pre-reset commit hashes referenced in older
LOG entries (e.g. the retired transcription script at 78a5da9) no longer
resolve — that history is intentionally gone.
**Decision:** continue.

## 11 — 2026-07-12 — de-brand: geometry table folded into layout.py, reference name removed
**Phase:** 0
**Did:** Human: the reference DXF has served its purpose — keep the Alice
spacing/sizing, drop the donor board's name from live artifacts. Folded the
KEYS table into design/layout.py (single design-definition file; deleted
design/yeti_ref.py), reworded README/ROADMAP/render titles to "Alice-family
geometry, plate-verified"; deleted the leftover comparison render. LOG and
lessons_learned keep the historical references (append-only). The human's
iCloud DXF copy is theirs to delete; repo never contained it.
**Observed:** layout_iter11 + plate_iter11 regenerate identically (60 keys,
335.6 x 125.7 mm) — pure refactor, no geometry change.
**Decision:** continue.

## 10 — 2026-07-12 — retire the transcription script; yeti_ref.py is source of truth
**Phase:** 0
**Did:** Human: the DXF->layout conversion is one-shot, so per the template rule
deleted scripts/yeti_to_layout.py (recoverable at commit 78a5da9). design/
yeti_ref.py header updated: now the hand-editable source of truth for key
placement; provenance and the carried Yeti nudges documented there.
**Decision:** continue.

## 9 — 2026-07-12 — Yeti-transcribed geometry: overlaps fixed, halves level
**Phase:** 0
**Did:** Human caught two iter-8 defects: cap overlaps at the wedge boundaries
(W/2, [/=, //') and the right half sitting visibly lower. Root causes: (1) our
right wedge rotated 6 columns where the Yeti rotates only 4 (P [ ; / . belong
to the straight zone), (2) the right pivot was mirrored about the board center
instead of the apex, dropping the right wedge ~4mm. Fix: stop re-deriving —
transcribe. New `scripts/yeti_to_layout.py` reads the Yeti plate DXF and emits
`design/yeti_ref.py` (committed): exact Yeti positions/angles for all kept keys
incl. its hand nudges (raised 2/-/P, ~4.1mm/row outer shear, 1.5mm spacebar-row
drop, +2mm right-wedge raise — all Yeti-native), minus macro column and thumb
extras, plus our bottom row (corner mod pairs aligned to the Shift blocks,
2.25|2.75 spacebars at Yeti space positions). layout.py is now a thin reader;
remaining knob: SPLIT_EXTRA (widens apex for the screen; 0 = Yeti-native 1.48u).
plate.py gained a center bridge hull (5/6/7/8 + spacebars) — placeholder screen
bay; also fixes the apex pinch the wider gap caused.
**Observed:** layout_iter9/plate_iter9: all boundary cap gaps >= 0 (tightest
2-3 at 0.05mm = Yeti's own tuck); apex 6->7 = 1.482u (Yeti 1.482); 7 sits 2.0mm
above 6 (Yeti-native). Plate 335.6 x 125.7mm, 60 cutouts, continuous apex.
**Decision:** continue — this is now faithfully the Yeti's geometry.
**Open:** iter8 open items (screen part, BLE-only vs dongle); SPLIT_EXTRA once
the screen is chosen; keep or restyle the bridge bay when the case is designed.

## 8 — 2026-07-12 — bumble: rename + 60-key layout (Yeti-compact) + feature goals
**Phase:** 0
**Did:** Human set the goal: "Yeti but more compact and feature-rich" — project
renamed wing60 -> bumble (GitHub repo renamed, local dir moved, refs updated;
older LOG entries keep the old name per append-only). Layout: added the mirrored
B to the right wedge (("B", 6.25, RI)) and widened SPLIT_GAP 0.45 -> 0.65u so the
apex 6->7 spacing lands at the Yeti's 1.48u, which is what makes room for the B
pair. Bottom row confirmed as-is (corner mods + two spacebars only; no macro
column, no thumb extras). README/ROADMAP now carry the feature goals: wireless
(BT and/or 2.4G dongle; nRF52840+ZMK candidate) and a center color screen
(gif/typing stats/mods) in the spacebar gap.
**Observed:** 60 keys exactly (name problem solved by the mirrored B). Apex 6->7
= 1.479u; B-to-B edge gap 11.4mm; spacebar-to-spacebar void 51.2mm wide — the
natural screen bay. Plate 340.5 x 124.0 mm, 60 cutouts (layout_iter8, plate_iter8).
**Issues:** ZMK color-display support is the weak link for the screen feature —
flagged in ROADMAP as an architecture decision blocking Phase 3.
**Decision:** continue — awaiting human sign-off on iter8 as the bumble baseline.
**Open:** Yeti-style outer shear + 1.5mm thumb-row drop (silhouette, next iter?);
screen part selection drives the final gap; BLE-only vs dongle-also.

## 7 — 2026-07-12 — lessons_learned.md + bend-angle sweep for the split-angle decision
**Phase:** 0
**Did:** Added `lessons_learned.md` (process lessons for upstreaming into fablab at
release; first entry: hunt reference design files before iterating renders) — same
scaffold added to the fablab repo itself; CLAUDE.md Lessons section now points to
it. Rendered `renders/bend_sweep_iter7.png`: 8/10/12deg at same scale with measured
plate size and apex distance, to ground the angle discussion with the human.
**Observed:** Size cost of the bend is trivial: ~330x119mm at 8deg -> 337x124 at
12deg (+7mm wide, +5mm tall). Apex 6->7 stays ~1.3u throughout (engine holds
clearance). The look difference is mostly wedge drama, not footprint.
**Decision:** escalate — human picks bend angle and stagger philosophy (Alice
row-stagger vs arc/columnar) before iter 8 touches layout.py.
**Open:** bend 8/10/12; row-stagger (Alice) vs columnar/arc — note keycap reality:
ANSI stagger + 2.25|2.75 spaces = standard Alice keycap kits fit; columnar would
be a different device family entirely. Plus LOG 6 knobs (mirrored B, outer shear,
thumb-row drop).

## 6 — 2026-07-12 — Yeti plate DXF analysis: model confirmed; mirrored B = 60th-key candidate
**Phase:** 0
**Did:** Human supplied the Axolstudio Yeti plate DXF (iCloud Drive, `Yeti_Plate.dxf`
— file is stored rotated 180deg). Parsed all cutouts + outline with ezdxf; identified
every key via QMK axolstudio/yeti + an alpha-block affine fit (residual 0.003mm —
the plate is exactly parametric).
**Observed:** Confirms the 4-zone model on a second production board: every cutout
at 0/+12/-12deg; wedge = 3456/WERT/SDFG/XCVB with standard ANSI staggers — same
boundary as Arisu and wing60 (Q8's W-straight look is the outlier). Diffs vs Arisu:
pivot (3.07, 0.81)u vs (3.35, 1.33); apex 6->7 = 1.48u vs 1.27 (wing60 iter5 ~1.45);
outer zones sheared outward ~4.1mm/row (smooth slanted edge; QMK-flattened x is a
lie there) instead of min-clearance rigid blocks, with small hand-tuned nudges
(keys next to the wedge raised 2.14mm); thumb row dropped an extra 1.5mm; right
half has a TGR-style mirrored B; 3-key macro column on the left wing; spacebars
2u | 2.75u with Fn tight against the left space. Plate fab specs harvested: 14.0mm
square cutouts (rotated ones too), stab holes 7mm wide at 23.88mm spacing + 1mm
notches, outline corners r6, feature fillets r1-r2. Render:
`renders/yeti_vs_wing60_iter6.png` (Yeti fully legended over our iter5, same scale).
**Decision:** continue — bend 12 and the zone boundary are now two-board-confirmed.
Propose mirrored B as the 60th key: it resolves 59-vs-60 AND the board name, and
it's the classic Alice touch.
**Open:** adopt mirrored B? outer-zone shear (Yeti) vs rigid blocks (Arisu/ours)?
thumb-row +1.5mm drop? spaces 2u|2.75u (Yeti) vs 2.25|2.75 (ours)? macro column
(would make 63 keys — probably not for a compact board)?

## 5 — 2026-07-10 — REAL Alice geometry: four zones, not two bent halves
**Phase:** 0
**Did:** LOG 4's model was wrong (human caught it): an Alice is NOT two rigid
rotated halves. Analyzed a Keychron Q8 product photo + the open-source Arisu
PCB (FateNozomi/arisu-pcb, switch coords in arisu.kicad_pcb). Ground truth:
every Arisu switch is at 0deg, +12deg, or -12deg — outer columns dead straight,
only the inner wedge rotates; outer zones also slide outward per row to clear
the wedge (flared silhouette). Solved the rotation pivot from switch coords:
(3.35u, 1.33u) from the half's top-left, verified exact against their B key.
Rewrote design/layout.py as a 4-zone geometry engine (LO/LI/RI/RO + placed()),
rewrote render_layout.py and cad/plate.py against it, deleted the superseded
render_variants.py. SPLIT_GAP 0.45u (Arisu apex: 6->7 centers 1.27u apart).
**Observed:** layout_iter5 + compare_iter5 (Q8 photo over our render): zone
structure, staircase boundaries, flare, and V apex all match. Plate 337x124mm;
offset-hull outline reads like the Q8 case. Plate fillet fails on offset-arc
vertices (harmless — offset already rounds convex corners).
**Decision:** continue — this is the real Alice bone structure.
**Open:** bend 12 (Arisu) vs ~10 (Q8 looks shallower); Q8 keeps W+S straight
(boundary one column further out on rows 1-2) — taste knob; left space 2.25u
leaves a void after Cmd; spacebar sizes; 59 vs 60 still undecided.

## 4 — 2026-07-10 — Alice-family research + variant comparison sheet
**Phase:** 0
**Did:** Human: current design reads as "a normal keyboard bent in the middle" —
researched real Alice-family geometry. Sources: QMK keyboard.json for tgr/alice,
sneakbox/aliceclone, projectkb/alice, xelus/valor (exact key sets; QMK flattens
rotation), mkbguide.com Alice guide (angles). Findings: TGR Alice ≈ ±8°
(AVA 6°, Neo Ergo 7°); 3-key macro column fills the left wing; optional
mirrored B on right half; bottom row is a thumb cluster (1.5u mods inboard of
swept corners, mods hug spaces, spaces nose into the split, 1.25u key BETWEEN
the spacebars); Arisu = no dup B, arrows, num-row alignment. Also: right Alt
moved against Fn in design/layout.py per human. Built
scripts/render_variants.py → renders/variants_iter4.png: TGR reference (from
real data), wing60 current, variant A (Alice thumbs, swept corners, ±8°,
home-row aligned), variant B (A + center Fn2 between spaces = 60 keys).
**Observed:** The Alice look comes mostly from the bottom row treatment, not
the alpha block — variants A/B read distinctly more Alice than the bent-60%.
**Decision:** escalate — human picks a direction from the sheet.
**Open:** A vs B (B restores 60 keys); mirrored B on right half?; angle 8 vs 10;
macro column (would add 2-3 keys, widens left wing)?

## 3 — 2026-07-10 — V-flip, new bottom row, first plate STL
**Phase:** 0
**Did:** Flipped split rotation to V (human: iter 2 read as an A). Bottom row set
to Ctrl, Cmd, Space | Space, Alt, Fn per human — **that is 6 keys, so the board
is now 59 keys, not 60** (flagged; name says 60). Added `cad/plate.py`
(build123d): MX plate from design/layout.py — rotated half outlines + center
bridge, 14 mm cutouts, 1.5 mm thick, 3 mm corner fillets → `plate_iter3.stl` +
pyvista render. Layout iter 3 re-rendered.
**Observed:** Plate 335 × 135 mm, 59 cutouts. Verified V orientation numerically
(` above 6, Bksp above 7 in STL frame) — not mirrored. Bottom-center slit is the
0.25u center-gap wedge the bridge leaves open; reads as an Arisu-style notch.
**Decision:** continue — plate STL is now the primary look-and-feel artifact.
**Open:** keep or close the bottom-center notch; 59 vs 60 keys; stabilizer
cutouts (2u+ keys) not yet modeled — needed before this plate is real.

## 2 — 2026-07-10 — layout render pipeline + first Alice render
**Phase:** 0
**Did:** Built the look-and-feel loop: `design/layout.py` (60-key definition,
split angle/gap params) + `scripts/render_layout.py` (matplotlib render with
auto-spacing between rotated halves, iter GC) → `renders/layout_iter2.png`.
Added matplotlib to the env. Recorded decisions: soldered, two PCB variants
(MX + Choc), 2.75u right Shift, 2-piece split space. Phase 2 marked SKIPPED
(human opted out of pre-fab derisking); binding acceptance test drafted as
post-assembly only.
**Observed:** Render shows the Alice wing correctly — halves ±10°, wedge gap
opening at top center, 60 keys, outer edges aligned. Bottom-row legends
(Ctrl/Alt | Alt/Fn/Menu) are placeholders per human.
**Decision:** continue — iterate the render with human feedback.
**Open:** split angle taste (8–12°?); center gap width; whether bottom row gaps
should close up; MCU choice can wait until layout converges.

## 1 — 2026-07-10 — repo created from fablab template
**Phase:** 0
**Did:** Created wing60 from the fablab template (first real use of the template).
Ran `make setup` (all green except Java — needed for FreeRouting, install before
Phase 3c). Replaced `{{device-name}}` placeholders; wrote device intent in README:
60-key Alice-style unibody split — 61-key ANSI 60% base − Win − right Ctrl + split
spacebar (2 pieces).
**Observed:** Template clone, setup, and skill autoload all worked; `.env` created
from example.
**Decision:** continue — kickoff (roadmap customization) is the next step.
**Open:** Binding acceptance test wording; envelope constraints (rotation angle,
board outline); MCU + switch choice (MX vs Choc, hotswap?); exact bottom-row/mod
arrangement; fill DigiKey credentials in `.env`.
