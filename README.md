# bumble

A compact, feature-rich 59-key Alice-style unibody split keyboard with a
wireless brain and a color screen at its heart.

Built from the [fablab](https://github.com/dskarbrevik/fablab) template — this
project doubles as its first real test run. (Formerly `wing60`; renamed at LOG 8.)

## What it is

Classic Alice-family geometry (±12° wedges, plate-verified spacing — see
LOG 5/6/9 for the measurement work), kept lean:

- **No macro column** — no extra left-wing keys.
- **Quiet bottom row** — two mods on each bottom corner (Ctrl Cmd … Alt Fn) and
  just the two spacebars in the middle; no thumb-cluster extras.
- **No mirrored B** — the classic Alice duplicate B was dropped (LOG 17) to
  open the center void for the screen; left B carries the key.

| Row | Keys | Count |
|---|---|---|
| Number | `` ` `` 1–0 - = Backspace | 14 |
| Top | Tab Q–P [ ] \ | 14 |
| Home | Caps A–' Enter | 13 |
| Bottom alpha | Shift Z–B N–/ Shift | 12 |
| Modifier | Ctrl Cmd **Space \| Space** Alt Fn | 6 |

No F-row, no arrows, no nav cluster — those live on a layer.

## Feature goals

- **Wireless**: Bluetooth, and/or 2.4 GHz via a dongle. Battery + charging on
  board. (Candidate: nRF52840 + ZMK — architecture decision pending in Phase 1.)
- **Center color screen**: a quality color display in the middle of the board
  (the ~51 mm-wide void between the spacebars) showing a cute gif/image, typing
  stats, and live modifier presses. Note the known tension: ZMK's display story
  is monochrome-first; color + animation may need a custom display module or a
  co-processor. To be resolved before the schematic.
- **Soldered switches** — no hotswap sockets.
- **Two PCB variants**: MX (19.05 mm) and Kailh Choc (18 × 17 mm), shared
  schematic.

## Status

Phase 0 (Define) — layout converging (`design/renders/layout_iter8` = first
60-key bumble). See `ROADMAP.md` for the live plan and `LOG.md` for history.

Repo shape: `design/` holds whole-device intent (key layout, concept renders),
`components/` has one subdir per actual part we build (plate, pcb, case,
firmware), `parts/bom.json` is the versioned buy list, and `bundle.json` logs
which component + BOM versions form each release.

## Toolset

Run `make setup` after cloning — it verifies/installs everything below and skips
what's already present.

- **[build123d](https://github.com/gumyr/build123d)** — parametric CAD in Python
- **trimesh / pyvista** — mesh interference checks and render generation
- **[Zener](https://github.com/diodeinc/pcb)** — declarative schematics (`.zen`)
- **KiCad 9+** — PCB layout, DRC, gerber export
- **[FreeRouting](https://github.com/freerouting/freerouting)** — autorouting
- **DigiKey API** — part search, pricing/stock, datasheets (`cp .env.example .env` and fill in)

Bundled agent skills in `.claude/skills/` (`kicad`, `bom`, `digikey`, `jlcpcb`,
`datasheets`) are from [kicad-happy](https://github.com/aklofas/kicad-happy) v1.3.1
by Andrew Klofas, MIT-licensed (`.claude/skills/LICENSE-kicad-happy`). `part-models`
is fablab-native.
