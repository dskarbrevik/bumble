# parts/ — the buy list

`bom.json` captures every part we **buy or source** to assemble the device —
as opposed to `components/`, which holds the things we **design and build**
(plate, pcb, case). One file, versioned by its `version` field; git history is
the change record, and `bundle.json` at repo root pins which BOM version ships
in each release bundle.

## bom.json schema

```
version    semver — patch: qty/price/source tweak; minor: part added/removed
           or swapped; major: architecture change (e.g. MCU family switch)
updated    YYYY-MM-DD of last edit
parts[]    one object per line item:
  id           stable slug, never reused (e.g. "switch-mx")
  name         human name
  category     switch | keycap | stab | electronic | fastener | misc
  qty          count needed for one device
  mpn          manufacturer part number (null until chosen)
  manufacturer null until chosen
  source       where to buy — URL or vendor name (null until chosen)
  price_usd    extended price for qty (null until quoted)
  status       candidate | confirmed | ordered | received
  used_by      component subdirs that consume it (["pcb"], ["plate"], …)
  notes        free text — constraints, alternates, open questions
```

Rules: a part reaches `confirmed` only with an MPN and a source; anything the
schematic references must exist here first (ROADMAP 3a exit gate).
