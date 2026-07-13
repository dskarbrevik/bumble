# Roadmap to v1 — bumble

The working contract between human and agent: phase plan, live status, task list.
There is no separate TODO file — the checkboxes here are it.

**Agent:** every session, find the `[IN PROGRESS]` phase and work only that. Update
checkboxes and status tags in the same edit as the work. If reality has drifted from
this file, fix the file first.

## Kickoff (do once, together — then delete this section)

- Replace `{{placeholders}}`; fill in each phase's tasks.
- Don't delete inapplicable phases/tasks — ~~strike through~~ with a one-line reason.
- Every exit gate must be numeric or binary. Subjective gates never trigger.
- Ownership: human owns what only hands can do (measure, print, wire, test); agent
  owns everything derivable from files.

## Status tags

`[NOT STARTED]` `[IN PROGRESS]` `[BLOCKED — reason]` `[COMPLETE — YYYY-MM-DD]` —
custom tags welcome. One phase `[IN PROGRESS]` at a time; Phase 1 may run in parallel.

---

## Phase 0: Define `[IN PROGRESS]`

What the device is, why, and what done means. Human decides; agent drafts and challenges.
**Exit:** README states functions and constraints; roadmap customized; binding
acceptance test written — one physical sentence checkable in under a minute.

- [x] Device intent and core functions in README — sharpened 2026-07-12: compact,
      feature-rich Alice; project renamed wing60 → bumble
- [ ] Envelope / form-factor constraints — converging: case v1 (LOG 18) fixes
      high-profile pebble, 6° wedge, flush round screen ring; footprint
      ~362 x 134 mm, deck 14 mm front / 28 mm back. Write down as constraints
      once human signs off the case direction
- [ ] Feature architecture decided (blocks Phase 3 schematic):
  - [x] Wireless: **BLE-only first take** (human, 2026-07-12); 2.4 GHz dongle can
    be a later firmware/accessory addition. Candidate MCU: nRF52840.
    Battery + charging + power switch still to spec in Phase 3.
  - [ ] Center color screen: researched 2026-07-12 (LOG 15). ZMK tension
    resolved in principle: prospector + YADS prove nRF52840 + ZMK/LVGL drives
    ST7789 SPI in full color today (as dongles; bumble is unibody so the
    screen rides the central — battery cost is the open question, mitigate
    with idle timeout/dimming). Fit mockups in design/renders/screenfit_*_iter15:
    front-runner 1.69" 240×280 ST7789V2 with +0.25u split and ~14 mm center
    chin. Awaiting human pick of candidate + placement strategy.
- [ ] Look-and-feel converged: human signs off on a layout render
      (`design/layout.py` → `scripts/render_layout.py` → `design/renders/`)
- [x] Binding acceptance test (draft, post-assembly only per human): plugged in over
      USB, each of the 59 keys registers its legend once in a key tester
- [x] Toolchain chosen: fablab defaults (build123d, Zener, KiCad, FreeRouting) —
      this project is the template's shakedown run

## Phase 1: Ground truth `[NOT STARTED]`

Physical facts only hands can produce. Agent specifies what to measure; human measures.
Rules: rate every dimension caliper > vendor CAD > datasheet > listing; ground-truth
assets are read-only; personal captures live in `secrets/`, never in git.

For every **pre-existing / off-the-shelf (COTS)** component the design depends on, get
its geometry via the `part-models` waterfall before asking the human to measure —
try (1) datasheet dims, (2) an existing CAD model, and only then (3) calipers. Verify
every found model against one fit-critical datasheet dimension; record it in
`models/ledger.md` (source, trust tier, license, verified). No ledger row = no ground
truth. Net-new parts (enclosure, brackets) are designed in `components/`, not sourced here.

**Exit:** every dimension/capture the design depends on exists, with provenance stated;
every COTS part has a verified `models/ledger.md` row.

- [ ] {{measurements}}
- [ ] {{captures / source models}}
- [ ] Every COTS component: geometry sourced + verified + ledgered (`part-models`)

## Phase 2: Prove the cheap things `[SKIPPED — human opted out of pre-fab derisking, 2026-07-10]`

De-risk on dev boards, breadboards, and modules before paying for anything custom.
If something genuinely can't be tested cheaply, strike it through with the reason.
**Exit:** riskiest subsystems demonstrated on real hardware; component survey and
draft BOM complete; no "will this part even work?" unknowns.

- ~~Hello-world firmware on target MCU~~ human decision: no pre-fab testing;
  keyboards are well-trodden design space, risk accepted
- ~~Riskiest subsystem proven in isolation~~ same
- [ ] Component survey + draft BOM in `parts/bom.json` (MPN, dims, stock,
      price) — kept: paper-only, no hardware to buy; folds into Phase 3
- ~~Buy-vs-build decided per subsystem~~ trivially decided: custom PCB ×2 (MX,
  Choc), COTS switches/caps/MCU

## Phase 3: Design loop `[NOT STARTED]`

Iterate schematic → placement → routing → mechanical in small gated slices. Agent
iterates; human reviews renders and prototype prints.
Rules: one change per iteration — render, look, measure, log, decide. Never trust a
scalar metric without looking at the render. A net change reopens placement; a
placement change reopens routing. For subjective geometry (ergonomics, looks),
checkpoint with the human after every change — don't run ahead.
**Objective checks run in the loop, not at the fab gate.** Before routing, seed the
project's DRC from the fab house's capabilities (`jlcpcb` skill emits `.kicad_dru` +
board-setup constraints) so live DRC *is* the DFM check, and run the DFM scoring pass
(`kicad` `analyze_pcb.py`) every iteration. The Phase 4 audit must only *confirm* — if
it *discovers* an objective tolerance/DFM issue, that check was missing from the loop.

**Sub-phase exits:**
- 3a Schematic: ERC clean; every net maps to a BOM part
- 3b Placement: no courtyard overlaps; fits envelope; routing channels ≥ min width
- 3c Routing: 0 unrouted nets; DRC (seeded with fab rules) 0 errors / 0 warnings + DFM scoring clean (or each violation waived with reason)
- 3d Mechanical: interference ≤ {{1 mm³}}; single printable body; meets print-process DFM (min wall / overhang / feature); print feedback incorporated

Two board variants — MX (19.05 mm) and Choc (18 × 17 mm) — share one schematic;
placement and routing are per-variant. Soldered switches, no hotswap.

- [ ] Seed project DRC from fab capabilities before routing (`jlcpcb` → `.kicad_dru`)
- [ ] {{tasks, per sub-phase, at kickoff}}

## Phase 4: Fab gate `[NOT STARTED]`

The last cheap moment — be paranoid once, on purpose. Agent prepares; human approves spend.
**Exit:** adversarial review done (zero findings = didn't look hard enough); exports
regenerated by script; revision tagged; order placed.

- [ ] Adversarial design review; findings dispositioned
- [ ] DFM check against fab house rules
- [ ] Gerbers / STLs / BOM exported by script, reproducibly
- [ ] Revision tagged in git + snapshot render committed
- [ ] Order placed; cost and ETA logged
- [ ] Release package proposed to human (CLAUDE.md → Releases)

## Phase 5: Assemble & validate `[NOT STARTED]`

Parts → device → verdict. Human assembles and tests; agent diagnoses and specs fixes.
**Exit:** binding acceptance test passes on the assembled device.

- [ ] Bring-up plan written before parts arrive
- [ ] Assembled; smoke test passed
- [ ] Firmware flashed on real hardware
- [ ] Enclosure fit-check with real parts
- [ ] Binding acceptance test: {{restate}} — pass/fail logged
- [ ] Failures: root cause logged; fix routed back to the phase that owns it
- [ ] On pass: release package proposed to human (CLAUDE.md → Releases)
