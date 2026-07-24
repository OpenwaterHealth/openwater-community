# Known issues

This project ships as a **working, documented, imperfect reference implementation.** The
imperfections are listed here honestly and completely — a researcher is better served by
an accurate limitations list than by a polished artifact that hides its edges, and these
items are exactly what generate the first outside contributions.

Items below are mirrored as GitHub issues where an actionable unit of work exists. Labels
in parentheses indicate issue triage intent.

---

## Documented technical findings

### Slicer vs. direct-Python trigger latency (~250 ms delta)
The end-to-end trigger latency measured through the 3D Slicer GUI path is **~422 ms**,
versus **~170 ms** running the same logic directly in Python — a reproducible ~250 ms
delta attributable to the Slicer–Python bridge, not to the trigger logic itself.

- This is a real, reproducible measurement and arguably the most interesting technical
  output of the study.
- It is a **Slicer–Python-bridge** characteristic, not an Openwater defect. It is worth
  reporting to the Slicer community as a standalone technical observation, separate from
  this repository.
- See [`../notebooks/latency_analysis.ipynb`](../notebooks/latency_analysis.ipynb) for
  the measurement method.
- Tracked as: *investigation* (`needs-triage`, `area: slicer`, `help wanted`).

---

## Scope limitations (by design)

These are not bugs — they are things this feasibility implementation deliberately does
**not** do. Whether to add them is a design decision for the platform owners.

- **No MRI-guided targeting.** Transducer placement is manual/anatomical. Tracked as an
  *enhancement* (`needs-design`) — scope to be ruled on before it is labeled beginner-friendly.
- **No acoustic skull correction** in this pipeline. Tracked as an *enhancement*
  (`needs-design`).
- **Software guardrails against a mid-session shutdown.** Hardening the pipeline against
  an abrupt host/process shutdown mid-session is not yet implemented. Tracked as an
  *enhancement* (`help wanted`).

---

## Requested features

- **Non-g.tec amplifier adapter.** The acquisition layer is abstracted behind an
  interface (see [`architecture.md`](architecture.md)); an adapter for a second amplifier
  would prove the abstraction and broaden reuse. Tracked as a *feature* (`help wanted`).
- **Video-stream marker synchronization.** Synchronizing a video stream's markers with
  the LSL clock, to align behavioral video with EEG/sonication events. Tracked as a
  *feature* (`good first issue`).

---

## Bug list

> [!NOTE]
> **This section is authored by the original developer (Janet).** Her first-hand
> descriptions of the bugs she encountered are more accurate than any reconstruction,
> and authoring them gives her attributed issues on the org. Each entry here should be
> filed as its own GitHub issue (`bug`; several are likely `good first issue`).
>
> _Placeholder — to be filled in by Janet before the end of the internship. Do not
> reconstruct these from memory; they are intentionally left for her to write._

- [ ] _(bug 1 — title, repro, expected vs. actual)_
- [ ] _(bug 2 — …)_
- [ ] _(bug 3 — …)_

---

## A note on triage

Design-dependent items (`needs-design`) should **not** be labeled `good first issue`
until scope has been ruled on by the platform owners — otherwise a new contributor can
sink effort into a direction that has not been decided.
