---
name: part-models
description: Source geometry (3D STEP models, PCB footprints, mechanical drawings) for pre-existing / off-the-shelf (COTS) components — the parts you buy, not the parts you design. Runs a trust-and-automatability-tiered source waterfall (manufacturer STEP, DigiKey API, LCSC/EasyEDA, SnapEDA, Ultra Librarian, McMaster-Carr, TraceParts), records provenance + license in a component ledger, and verifies each model against a datasheet dimension before the design leans on it. Use whenever the design needs the shape/footprint/envelope of a bought component: "find a CAD model for this connector", "get the STEP for this dev board", "do we have geometry for the battery holder", "footprint for MPN X", "recreate this part's dimensions". Complements the `datasheets` skill (which extracts electrical specs) — this one owns geometry. For electrical specs use `datasheets`; for part search/pricing use `digikey`/`bom`.
---

# part-models — geometry for off-the-shelf components

The design depends on the shape of parts you didn't design: connectors, dev boards,
battery holders, buttons, standoffs, sensors on a carrier. Before you can place them
in CAD or lay out around them, you need their geometry — a 3D STEP model, a PCB
footprint, or at minimum enough dimensions to recreate the envelope.

This skill exists so the agent never re-derives *where to look* or *how much to trust
what it finds*. It runs a fixed waterfall, stamps provenance, and verifies before use.

**Scope:** pre-existing / COTS parts only — things that exist in the world and can be
bought. Net-new parts you design (enclosure, brackets) are `cad/` parametric source,
not this skill. See CLAUDE.md → Layout: fetched models live in `models/`, our source
lives in `cad/`.

## The three ways to get geometry (in effort order)

For every COTS component, get its geometry from exactly one of:

1. **Detailed specs** — datasheet mechanical drawing with enough dimensions to model
   the envelope. Handled with the `datasheets` skill; recreate as parametric `cad/`.
2. **An existing CAD model** — download a vendor/community STEP or footprint. This
   skill's main job. Still needs a verify step (below) — a found model is not trusted
   until one dimension is checked.
3. **Human measurement** — caliper the real part. **Last resort**, only when 1 and 2
   are exhausted or a fit-critical dimension can't be trusted from a found model.
   Don't send the human to the calipers before the waterfall is dry (CLAUDE.md rule:
   "don't ask the human for anything derivable from files").

## Source waterfall

Tiered by **(can the agent do it end-to-end?) × (is the license clean to commit?)**.
Walk top-down; stop at the first source that yields a usable, verifiable model.

### Tier A — agent does search → download → verify autonomously

| Source | Good for | Notes |
|--------|----------|-------|
| **Manufacturer product page** | Anything with a vendor STEP | Most authoritative. Vendor's own license — usually fine to commit. Try first. |
| **DigiKey API** (`digikey` skill) | Electronic components | Already wired (`.env` creds). Returns datasheet + media/model links for many MPNs. |
| **LCSC / EasyEDA** | JLC assembly parts | Authoritative for the exact `Cxxxxx` parts JLCPCB will place. Natural when targeting JLCPCB. |
| **KiCad libraries / `packages3D`** | Common passives, standard footprints | Already local; check before fetching anything. |

### Tier B — agent finds the exact part + verifies; human does the login-gated download

These are excellent libraries but **wall the actual download behind a login or an
approved API key**, and some carry redistribution-restricted licenses. The agent's job
here is to find the *exact* part page, hand the human the URL and what to grab, then
ingest and verify what comes back.

| Source | Good for | Gate & license caveat |
|--------|----------|-----------------------|
| **SnapEDA / SnapMagic Search** | Symbols, footprints, 3D STEP for electronics | Download needs account. License **CC BY-SA 4.0 + Design Exception**: fine in a manufactured design, but sharing CAD files publicly (e.g. committing to a public repo) triggers attribution *and* a redistribution restriction — see "Committing models" below. Promotes to Tier A if `SNAPEDA_API_KEY` is set in `.env` (free tier, request at snapeda.com/get-api). |
| **Ultra Librarian** | Symbols, footprints, 3D STEP (16M+ parts) | Registration required to download. License is friendlier — content "may be distributed without restriction" incl. open-source. |
| **McMaster-Carr** | Standard mechanical hardware (fasteners, standoffs, bearings) | Gold-standard STEP for standard parts. Download via their part page. |
| **TraceParts / 3D ContentCentral** | Manufacturer-certified mechanical CAD | Registration; per-manufacturer terms. |
| **GrabCAD / Printables / Thingiverse** | Community models when nothing else exists | **Untrusted provenance** — treat as listing-tier. Only use with a verify against a datasheet dimension, never for a fit-critical feature on trust alone. |

If a Tier-B source is the only hit, produce a one-line fetch instruction:
> Download `<MPN>` STEP from `<exact part URL>` → drop in `models/incoming/`. I'll verify it.

## Verify — the agent owns this regardless of source

A downloaded model is **not** trusted until checked. Before any design leans on it:

- Open the model (or its bounding box) and compare **≥1 fit-critical dimension** to the
  datasheet mechanical drawing (or one caliper value if no drawing). Overall length,
  connector pitch, mounting-hole spacing, and mating-face height are the usual ones.
- If it disagrees with the datasheet, the model is wrong — fix or discard it. A wrong
  model that looks right is worse than no model (it fails silently at fit-check).
- Community-tier models (GrabCAD etc.) that will carry a fit-critical feature need that
  feature's dimension verified specifically, not just a spot-check elsewhere.

This is the geometry analog of CLAUDE.md's "render and look every iteration" — a STEP
that imports without error is not a STEP with the right dimensions.

## The component ledger — `models/ledger.md`

One row per COTS component. This is the artifact that makes Phase 1's exit gate
("every dimension the design depends on exists, with provenance stated") mechanically
checkable — no ledger row, no ground truth.

| Field | Meaning |
|-------|---------|
| `MPN` | Manufacturer part number (the identity). |
| `source` | Which waterfall source the geometry came from. |
| `tier` | Trust tier: `caliper` > `vendor-CAD` > `datasheet` > `community/listing`. |
| `file` | Path in `models/` (or `— (measured, see cad/)` if recreated from dims). |
| `critical dims` | The dimensions the design actually depends on. |
| `verified` | ✓ + which dimension was checked against what, or ✗ (blocks use). |
| `license` | e.g. `vendor`, `CC BY-SA (restricted redistribution)`, `UL-free`, `McMaster`. |

Keep the trust hierarchy consistent with ROADMAP Phase 1: `caliper > vendor CAD >
datasheet > listing`. A found model's tier is capped by its source — a GrabCAD model is
`community` even after a spot-check; verifying promotes *confidence*, not *provenance*.

## Committing models — license gate

fablab commits artifacts. Before committing a fetched model, check its license:

- **Clean to commit** (manufacturer, McMaster, Ultra Librarian, KiCad libs): put the
  file in `models/` and commit it.
- **Redistribution-restricted** (SnapEDA / CC BY-SA-ShareAlike, or anything unclear):
  put the file in **`models/restricted/`** (gitignored) and commit only its
  `ledger.md` row (MPN + source URL + provenance), so a teammate re-fetches from
  source. When in doubt, restricted first (CLAUDE.md secrets rule generalizes here).

Human-fetched Tier-B downloads land in **`models/incoming/`** (gitignored) for the
agent to verify, then move to `models/` or `models/restricted/` per license.

## Workflow

1. **Identify** the COTS part (MPN, or class + key constraints if no MPN yet).
2. **Check local first** — `models/`, KiCad `packages3D`, existing `datasheets/`.
3. **Walk the waterfall** top-down; stop at first usable hit.
4. **Verify** ≥1 fit-critical dimension against the datasheet.
5. **Record** a `models/ledger.md` row (provenance, tier, license, verified).
6. **Commit or gitignore** per the license gate.
7. Only if the waterfall is dry / trust insufficient → **spec a measurement** for the
   human (exact dimension, why it's needed, what tolerance).
