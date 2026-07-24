# Feasibility report

**A two-subject feasibility study of closed-loop LIFU–EEG on open hardware.**

> **Research use only.** This report describes a research feasibility study. It makes no
> clinical claims. It refers throughout to research **subjects**, **sonications**, and
> **research use**. It does not describe treatment, patients, or clinical efficacy.

---

## Summary

This study asked a single question: **can the OpenLIFU platform run a closed loop** —
acquire EEG in real time, compute a signal-derived state, and gate low-intensity focused
ultrasound on that state, within an explicit safety envelope? The answer is **yes**: a
working end-to-end closed-loop LIFU–EEG system was built on open hardware and run with
two subjects over a twelve-week internship.

This is a *feasibility* result, not an efficacy result. It demonstrates that the platform
and the surrounding open-source tooling (LSL, PsychoPy, the OpenLIFU stack) can be
assembled into a real-time closed loop that behaves within defined bounds.

---

## Method (as built)

- **Subjects:** two employee participants under a 2-subject research authorization.
- **Acquisition:** g.tec amplifier via the g.Pipe SDK, streamed over LSL.
- **Task:** PsychoPy 2-back working-memory task.
- **Signal:** theta-band power, converted online to a per-subject Z-score against a
  100 s resting baseline (see [`../calibration.md`](../calibration.md)).
- **Control law:** the six-condition trigger gate with a hard safety ceiling, cooldown,
  and per-session cap (see [`../protocol.md`](../protocol.md)).
- **Sonication:** issued through `openlifu-python`.
- **Logging:** all streams timestamped on the shared LSL clock for offline analysis.

---

## Findings

1. **The closed loop runs end to end.** Acquisition → artifact gating → theta Z-score →
   six-condition gate → sonication → logging operates in real time within a session.

2. **The safety envelope behaves as specified.** The safety ceiling, 10 s cooldown, and
   10-sonication session cap bound the system's behavior independently of the signal.
   Every sonication decision — permitted or refused — is logged with the full state of
   all six conditions.

3. **Trigger latency is dominated by the GUI path.** End-to-end trigger latency is
   ~170 ms in direct Python versus ~422 ms through the 3D Slicer GUI — a ~250 ms delta
   attributable to the Slicer–Python bridge rather than to the trigger logic. This is
   the study's most portable technical finding and is documented in
   [`../known-issues.md`](../known-issues.md) and
   [`../../notebooks/latency_analysis.ipynb`](../../notebooks/latency_analysis.ipynb).

---

## Limitations

- **n = 2.** This is a feasibility demonstration, not a study powered for any effect.
- **Manual targeting.** No MRI-guided targeting and no acoustic skull correction (see
  [`../known-issues.md`](../known-issues.md)).
- **Single amplifier.** Validated only with the g.tec amplifier; the acquisition
  abstraction is untested against a second device.
- **No raw data published.** No EEG from this study is included in this repository. Any
  future publication of a real trace is a separate, explicitly consented contribution.

---

## Reproducing without human data

The full pipeline — calibration, Z-score, trigger gate, logging — can be exercised
against the synthetic theta fixture with no human recordings:

```bash
python -m fixtures.synthetic_theta
python -m openlifu_closed_loop --source synthetic --dry-run
```

This is the recommended way to inspect the system's real-time behavior and the trigger
gate independently of any subject data.
