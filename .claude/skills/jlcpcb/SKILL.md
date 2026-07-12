---
name: jlcpcb
description: JLCPCB PCB fabrication and assembly — BOM/CPL generation, basic vs extended parts, assembly constraints, design rules, ordering workflow. Use with KiCad for JLCPCB manufacturing. Use this skill when the user mentions JLCPCB, wants to order PCBs or assembled boards, needs prototype bare PCBs and stencils, wants to know JLCPCB design rules and capabilities, or is asking about PCB manufacturing costs or turnaround times. For gerber/CPL export, stencil ordering, and BOM management, see the `bom` skill.
---

# JLCPCB — PCB Fabrication & Assembly

JLCPCB is a PCB fabrication and assembly service based in Shenzhen, China. It is a sister company to LCSC Electronics (common ownership) — they share the same parts library.

**Typical usage**: Order bare prototype PCBs + framed stencil from JLCPCB during prototyping (parts sourced separately from DigiKey/Mouser, hand-assembled in lab). For production runs (100s qty), order fully assembled boards from JLCPCB using LCSC parts. PCBWay is an alternative assembler. For component searching, see the `lcsc` skill. For BOM management, gerber/CPL export, and stencil ordering, see the `bom` skill.

## Related Skills

| Skill | Purpose |
|-------|---------|
| `kicad` | Read/analyze KiCad project files, DFM scoring against JLCPCB capabilities |
| `bom` | BOM management, gerber/CPL export, stencil ordering |
| `digikey` | Search DigiKey (prototype sourcing, primary — also preferred for datasheet downloads via API) |
| `mouser` | Search Mouser (prototype sourcing, secondary) |
| `lcsc` | Search LCSC (production sourcing — JLCPCB uses LCSC parts library) |
| `pcbway` | Alternative PCB fabrication & assembly |
| `emc` | EMC pre-compliance risk analysis — run before fab to catch EMC issues |
| `spice` | SPICE simulation — verify analog subcircuits before committing to fab |

## Assembly Parts Library

### Part Categories

| Category | Description | Assembly Fee |
|----------|-------------|--------------|
| **Basic** | ~698 common parts (resistors, caps, diodes, etc.) pre-loaded on pick-and-place machines | No extra fee |
| **Preferred Extended** | Frequently used extended parts | No feeder loading fee (Economic assembly) |
| **Extended** | 300k+ less common parts loaded on demand | $3 per unique extended part |

### LCSC Part Numbers

Every assembly component is identified by an **LCSC Part Number** (`Cxxxxx`, e.g., `C14663`). This is the definitive identifier for BOM matching. See the `lcsc` skill for searching parts.

### Parts Search (JLCPCB-Specific)

- Parts library: `https://jlcpcb.com/parts/componentSearch?searchTxt=<query>`
- Basic parts only: `https://jlcpcb.com/parts/basic_parts`

## BOM Format for Assembly

JLCPCB accepts CSV, XLS, or XLSX BOMs with these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Comment` / `Value` | Yes | Component value (e.g., 100nF, 10k) |
| `Designator` | Yes | Reference designators, comma-separated (e.g., C1,C2,C5) |
| `Footprint` | Yes | Package/footprint name |
| `LCSC Part #` | Recommended | LCSC part number (Cxxxxx) — guarantees exact match |

The column header for LCSC numbers must be exactly **"LCSC Part #"** or **"LCSC Part Number"** — typos cause upload failures.

### KiCad BOM Export for JLCPCB

1. In KiCad schematic editor, add an `LCSC` field to each symbol with the LCSC part number
2. Export BOM as CSV with columns: Reference, Value, Footprint, LCSC
3. Rename columns to match JLCPCB's expected format:
   - `Reference` -> `Designator`
   - `Value` -> `Comment`
   - `Footprint` -> `Footprint`
   - `LCSC` -> `LCSC Part #`

For gerber export settings, CPL format, and stencil ordering, see the `bom` skill.

## JLCPCB Official API (Approval Required)

Apply at `https://api.jlcpcb.com`. Access is gated — requires review based on order history and business profile.

Available APIs (once approved):
- **Components API** — real-time pricing, inventory, component specs
- **PCB API** — upload gerbers, get quotes, place orders, track status
- **Stencil API** — stencil quoting and ordering
- **3D Printing API** — SLA/MJF/SLM/FDM ordering

## PCB Design Rules (JLCPCB Capabilities)

### Standard PCB (1-2 layers)

| Parameter | Minimum |
|-----------|---------|
| Trace width | 0.127mm (5mil) |
| Trace spacing | 0.127mm (5mil) |
| Via diameter | 0.45mm |
| Via drill | 0.2mm |
| Annular ring | 0.125mm |
| Min hole size | 0.2mm |
| Board thickness | 0.4-2.4mm (default 1.6mm) |
| Min board size | 6x6mm |
| Max board size | 500x400mm (2-layer) |

### Multi-layer (4+ layers)

| Parameter | Minimum |
|-----------|---------|
| Trace width | 0.09mm (3.5mil) |
| Trace spacing | 0.09mm (3.5mil) |
| Via diameter | 0.25mm |
| Via drill | 0.15mm |
| Board thickness | 0.6-2.4mm |

### Seed the project's DRC from these rules BEFORE routing — don't wait for the fab gate

The tables above are only useful if KiCad's *live DRC* enforces them. KiCad checks a
board against the rules configured **in the project** — if the project keeps default
rules, live DRC passes "0 errors" while real JLCPCB violations (sub-min trace/space,
thin annular rings, undersized drills, edge clearance) accumulate silently, then all
surface at once during the final fab audit. That is a wiring failure, not a design
failure. Fix it by making the fab's constraints the project's DRC rules from the start
of layout.

**At the start of the routing sub-phase (ROADMAP Phase 3), seed the project once:**

1. Set board-setup constraints (Board Setup → Constraints / Pre-defined Sizes) to the
   min trace width, clearance, via, drill, and annular ring for the chosen tier
   (2-layer standard vs 4-layer advanced above). These live in the `.kicad_pro`.
2. Emit a `pcb/jlcpcb.kicad_dru` for constraints KiCad's board setup can't express
   (e.g. edge/hole clearances, courtyard rules) and import it via Board Editor → Board
   Setup → Design Rules → Custom Rules / Import. A `.kicad_dru` is plain S-expression
   text — write it directly. Example (2-layer standard):

   ```
   (version 1)
   (rule "min_trace_width"
     (constraint track_width (min 0.127mm)))
   (rule "min_clearance"
     (constraint clearance (min 0.127mm)))
   (rule "min_via"
     (constraint via_diameter (min 0.45mm))
     (constraint hole_size (min 0.2mm)))
   (rule "min_annular_ring"
     (constraint annular_width (min 0.125mm)))
   (rule "edge_clearance"
     (constraint edge_clearance (min 0.3mm)))
   ```

3. Commit the `.kicad_dru` with the board. Now every routing iteration's "DRC 0 errors"
   gate (Phase 3c) **is** the DFM check — objective violations are caught the moment
   they're introduced, one iteration at a time.

**Run the DFM scoring pass every iteration too, not just at the gate.** The `kicad`
skill's `analyze_pcb.py` scores against JLCPCB tiers and catches things live DRC won't
(tombstoning risk, thermal-pad via adequacy, placement density). Run it each routing
iteration; the Phase 4 audit then only *confirms* a clean board instead of *discovering*
a backlog of objective issues. See CLAUDE.md → Lessons: objective checks belong in the
loop, not the audit.

### Importing an existing DRU

If you already have a JLCPCB `.kicad_dru`, import it in Board Editor → Board Setup →
Design Rules → Import Settings.

## Assembly Constraints

### Economic vs Standard Assembly

| Feature | Economic | Standard |
|---------|----------|----------|
| Sides | Top only | Top + Bottom |
| Component types | SMD only | SMD + through-hole |
| Min component size | 0201 | 01005 |
| Fine-pitch BGA/QFP | Down to 0.5mm pitch | Down to 0.4mm pitch |
| Turnaround | ~3-5 days | ~3-5 days |
| Extended part fee | $3 per unique part | $3 per unique part |

### General Constraints

- **Minimum order**: 5 PCBs for assembly
- **Unique parts limit**: No hard limit, but each extended part adds $3
- **Basic parts**: No extra fee, pre-loaded on machines

## Rotation Offsets

JLCPCB's pick-and-place uses different rotation conventions than KiCad for some footprints. Common offsets:

| Footprint Family | Typical Offset |
|-----------------|----------------|
| SOT-23, SOT-23-5, SOT-23-6 | +180° |
| SOT-223 | +180° |
| SOIC-8, SOIC-16 | +90° or +270° |
| QFN (all sizes) | +90° |
| SMA/SMB/SMC diodes | +180° |
| USB-C connectors | Varies — check datasheet |

To fix rotation issues:
1. Add rotation corrections directly in the CPL file before uploading (adjust the Rotation column)
2. For custom footprints, verify pin 1 orientation matches JLCPCB expectations
3. JLCPCB's review step catches major errors, but subtle 180° rotations on symmetric parts (caps, resistors) may slip through
4. After first assembly order, note any rotation corrections needed and apply them to future CPL exports

## Ordering Workflow

### Prototype Order (Bare PCB + Stencil)

1. **Export gerbers** from KiCad (see `bom` skill for export settings)
2. Upload gerbers to `https://cart.jlcpcb.com/quote` — configure layers, thickness, color, qty
3. Add a **framed stencil** to the cart (uses paste layers from your gerbers)
4. Order — PCBs and stencil typically arrive in ~1 week

### Production Order (Assembled Boards)

1. **Export gerbers** from KiCad (see `bom` skill for export settings)
2. **Export BOM** as CSV with LCSC part numbers (format above)
3. **Export CPL** (placement file) as CSV (see `bom` skill for format)
4. Upload gerbers to `https://cart.jlcpcb.com/quote` — configure layers, thickness, color, qty
5. Enable "PCB Assembly", select Economic or Standard
6. Upload BOM and CPL files
7. Review part matching — fix any unmatched parts by searching LCSC numbers
8. Confirm and order

## Tips

- **Prefer Basic parts** — no extra fee, always in stock, faster assembly
- **Check stock before ordering** — extended parts can go out of stock; use the `lcsc` skill to search
- **Panel by JLCPCB** — for small boards, let JLCPCB panelize (cheaper) vs custom panels
- **Lead-free solder** — default is leaded (HASL); select lead-free HASL or ENIG if needed
- **Impedance control** — available for multi-layer boards, specify stackup in order notes
- **Castellated holes** — supported, enable in order options
- **V-cuts and mouse bites** — supported for panel separation
- **Silkscreen minimum** — 0.8mm height, 0.15mm line width for readable text
- **Edge clearance** — keep copper >=0.3mm from board edge (0.5mm recommended)
