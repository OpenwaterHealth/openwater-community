# Protocol

This document describes the experimental protocol implemented by the pipeline: the
sonication parameters, the task design, and — most importantly — the six trigger
conditions that gate every sonication decision.

> **Research use only.** Nothing in this document describes a clinical procedure. All
> language here refers to research **subjects**, **sonications**, and **research use**.

---

## 1. Session structure

A session runs in three phases:

1. **Calibration (100 s).** The subject sits at rest while a baseline of theta-band
   power is collected. No sonications are permitted during calibration. See
   [`calibration.md`](calibration.md).
2. **Closed-loop task.** The subject performs a PsychoPy 2-back working-memory task
   (see [Task design](#3-task-design)). Real-time theta Z-scores are computed against
   the baseline, and sonications are gated on the six trigger conditions.
3. **Wind-down.** The task ends, logging is flushed, and the session summary is written.

---

## 2. Sonication parameters

Sonication is issued through `openlifu-python`. The specific transducer, focal
parameters, and acoustic output are set in the run configuration and must be reviewed
against the device's research-use operating envelope before any session with a subject.

> [!IMPORTANT]
> Acoustic output parameters are **configuration**, not constants baked into this
> repository. They are documented in the run config and reviewed per protocol. This
> repository does not assert any specific dose as validated.

Timing of *when* a sonication may occur is governed entirely by the trigger gate below.

---

## 3. Task design

A **2-back working-memory task** implemented in PsychoPy. Stimuli are presented in a
sequence; the subject responds when the current stimulus matches the one presented two
steps earlier. The task is the behavioral context in which theta dynamics are expected,
and its active/inactive state is one of the six trigger conditions (condition 2 — a
sonication is only permitted while the task is active).

Task events (stimulus onset, response, correctness) are timestamped onto the LSL clock
so they can be aligned with EEG and sonication events offline.

---

## 4. The six trigger conditions

This is the safety-critical surface of the system. A sonication is permitted only when
**all six** conditions are simultaneously true. Each condition is implemented as a
single, independently testable predicate in
[`src/openlifu_closed_loop/triggers/`](../src/openlifu_closed_loop/triggers), with one
test per condition.

| # | Condition | Predicate | Rationale |
|---|-----------|-----------|-----------|
| 1 | **Baseline buffer complete** | The 100 s calibration baseline has been fully collected | A Z-score is meaningless without a baseline. No sonication before calibration completes. |
| 2 | **Task active** | The 2-back task is currently running | Sonication is only meaningful in the behavioral context the study is about. |
| 3 | **Theta Z above trigger** | `theta_z > 1.5` | The event the loop is closing on: elevated theta relative to the subject's own baseline. |
| 4 | **Below safety ceiling** | `theta_z < 10` | A hard ceiling. A Z-score at or above 10 indicates an implausible/artefactual excursion; the gate refuses to sonicate rather than act on it. |
| 5 | **Cooldown elapsed** | `now - last_sonication >= 10 s` | Enforces a minimum spacing between sonications. |
| 6 | **Session cap not reached** | `sonication_count < 10` | A hard per-session ceiling on total sonications. |

### Design notes

- **Conditions 4, 5, and 6 are safety bounds**, not signal conditions. They exist to
  bound the system's behavior regardless of what the signal does: no acting on
  implausible excursions (4), no rapid repetition (5), no unbounded session totals (6).
- The gate is **conjunctive and fail-closed**: if any input is missing, stale, or
  out of range, the condition it feeds evaluates false and no sonication is permitted.
- Artifact gating (see [`architecture.md`](architecture.md)) runs *upstream* of the
  trigger gate. Contaminated samples are suppressed before they can influence the
  theta Z-score, so the trigger gate never sees them.

> If this work is ever cited in a research, IRB, or regulatory context, the `triggers/`
> module and this table are what should be read together. Keep them in sync: a change to
> a threshold here must correspond to a change in the module and its test.

---

## 5. Logging

Every sonication decision — permitted or refused — is logged with the state of all six
conditions at decision time, plus a timestamp on the LSL clock. This makes the gate's
behavior fully auditable offline and is the basis for the latency analysis in
[`../notebooks/latency_analysis.ipynb`](../notebooks/latency_analysis.ipynb).
