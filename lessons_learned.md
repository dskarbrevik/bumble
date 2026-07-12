# Lessons learned — bumble

Process lessons for the fablab template, discovered on this project. Not the
same as CLAUDE.md's Lessons section (technical truths about *this device*) —
entries here are about *how the agent+human workflow should run*, and are
reviewed at each release for upstreaming into fablab's `lessons_learned.md`.

Entry format: one `##` heading per lesson — what to do, why, and the concrete
moment on this project that taught it.

---

## Reference design files first, renders second

Concept-first request ("compact alice style split keyboard") went through four
render iterations of a wrong mental model ("normal keyboard bent in the middle")
before we anchored on real design files. The Arisu KiCad PCB gave the true
4-zone geometry, exact ±12° rotations, and the pivot; a Yeti plate DXF then
confirmed the model on a second board and handed us fab specs (cutout sizes,
stab spacing, fillet radii) for free. Product photos and flattened layout data
(QMK JSON strips rotations) were useful hints but not ground truth — only
manufacturing files are. Next project: before iterating on look-and-feel, spend
the first iteration hunting DXF/STEP/kicad_pcb references for the device family
and parsing them for anchor dimensions.

*Taught by: LOG 4→6 (2026-07-10 → 2026-07-12).*
