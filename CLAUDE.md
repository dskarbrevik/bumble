# bumble — agent guide

## Every session

Read `ROADMAP.md` first. Find the `[IN PROGRESS]` phase; work only that. Then read the
top entries of `LOG.md` to see where the last session left off. Phase-specific rules
live in the roadmap at each phase — this file holds only what applies always.

Every iteration ends with a `LOG.md` entry (schema in its header). Work that isn't
logged didn't happen — the next session can't see it.

## Always-on rules

- **Never overwrite a design artifact — always add** (naming in Versioning below).
- **Don't ask the human for anything derivable from files.** Source models,
  datasheets, and captures on disk are the agent's job to extract from. The human's
  hands are for what only hands can do.
- **Secrets:** personal captures and credentials go in `secrets/`, which is
  gitignored. When in doubt, gitignore first, ask second.
- **When docs and reality disagree, fix the doc in the same edit as the work.** Stale
  comments and stale checkboxes poison future sessions.

## Layout

Every artifact type has a home — never park files at repo root.

```
design/      design-intent definitions (key layout, geometry params) consumed by scripts/
firmware/    source, one dir per program
cad/         parametric CAD source for parts WE design; outputs per Versioning below
models/      fetched geometry for BOUGHT (COTS) parts + models/ledger.md (provenance);
             license-restricted files gitignored, ledger row still committed (part-models skill)
pcb/         schematic + layout; fab exports in pcb/fab/
bom/         one BOM per confirmed board revision
datasheets/  component PDFs
scripts/     repeatable tools — delete one-shots when done, or label [SUPERSEDED]
renders/     generated views (gitignored; renders/confirmed/ is committed)
releases/    complete build packages (see Releases)
secrets/     personal captures & credentials (gitignored)
```

Create directories on first use; don't pre-create empty ones.

## Versioning

One scheme for every artifact type — no ad-hoc suffixes or pet names.

- **Scratch:** `{artifact}_iter{N}`, where N is the LOG entry number. Gitignored.
  Garbage-collect: when creating a new iter file, delete all but the latest 10 for
  that artifact.
- **Confirmed:** `{artifact}_v{MAJ}.{MIN}.{PATCH}` in that type's `confirmed/` dir,
  committed. Patch = tweak, minor = design change, major = architecture change.
- **Exception — files whose names are load-bearing:** don't rename; mark revisions
  with a git tag plus a committed snapshot render. Two kinds in this toolchain:
  - **KiCad projects** — `.kicad_pro/.sch/.pcb` must share a basename and
    cross-reference it internally.
  - **Zener `.zen` schematics** — modules are loaded by path (`Module(".../X.zen")`)
    and the top-level file is the entry point named in `pcb.toml`; renaming breaks
    every importer and the manifest.
  The schematic and the layout are **one board** — tag them together as a single board
  revision `pcb-v{X.Y.Z}` (a net change reopens routing, so their versions must never
  diverge). Iterate `.zen` and KiCad files in place; the tag + snapshot render is the
  revision record.

## Releases

A release is the complete package needed to build the device at a point in time:
`releases/v{X.Y.Z}/` containing `manifest.md` (pinned versions of every artifact —
CAD, PCB tag, BOM, firmware commit), `assembly.md`, and the fab-ready exports.
Mirror it as a GitHub release: tag `device-v{X.Y.Z}`, exports attached as assets.

The agent never cuts a release on its own — it **proposes** one whenever a buildable
snapshot exists that money or physical work is about to be spent against: a fab order
is about to be placed, or the binding acceptance test just passed.

## Lessons

Process lessons that fablab itself should learn (workflow, not device-specific)
go in `lessons_learned.md` instead — reviewed at each release for upstreaming
into the template.

Load-bearing truths about this project — the kind that silently break builds or burn
hours when forgotten. When a failure's root cause is thematic (it would recur), add
one line here in the same session it's diagnosed. Not a changelog; incidental bugs
don't belong.

- Scalar metrics lie: a falling error count is not progress — render the artifact and
  look at it, every iteration.
- Editing a generator ≠ editing the artifact: after changing source, regenerate and
  verify the output actually changed.
- Objective checks belong in the loop, not the audit. Any machine-checkable rule (fab
  DFM/DRC, print min-wall) must be seeded into the iteration gate from the start, so
  the final audit only *confirms*. If the audit *discovers* an objective violation,
  the check was missing upstream — add it to the loop, don't just fix the instance.
- A found CAD model is not trusted geometry: a STEP that imports clean can still have
  the wrong dimensions. Verify every sourced COTS model against one datasheet
  dimension before the design leans on it (part-models skill).
