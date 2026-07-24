# Architecture

The pipeline is a set of loosely coupled modules connected over
[Lab Streaming Layer (LSL)](https://labstreaminglayer.readthedocs.io/). LSL gives every
module a shared clock and lets components be developed, tested, and replaced
independently.

---

## LSL topology

```
        ┌──────────────────────┐
        │  g.tec amplifier      │
        │  (or synthetic_theta) │
        └──────────┬───────────┘
                   │  raw EEG  (LSL stream: "EEG")
                   ▼
        ┌──────────────────────┐
        │  acquisition/        │  g.Pipe SDK adapter → LSL
        └──────────┬───────────┘
                   │  EEG samples
                   ▼
        ┌──────────────────────┐
        │  artifact_gating/    │  MAD gate, 500-sample rolling buffer
        └──────────┬───────────┘
                   │  clean samples + gate flag
                   ▼
        ┌──────────────────────┐        ┌────────────────────┐
        │  triggers/           │◀───────│  task/ (PsychoPy    │
        │  six-condition gate  │  task  │  2-back)  LSL       │
        │  + safety ceiling    │  state │  markers            │
        └──────────┬───────────┘        └────────────────────┘
                   │  "sonicate" decision
                   ▼
        ┌──────────────────────┐
        │  lifu/               │  openlifu-python interface
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  logging/            │  timestamped event log (all streams)
        └──────────────────────┘
```

Every stream carries LSL timestamps, so acquisition, task markers, trigger decisions,
and sonication events can all be aligned to a common clock offline.

---

## Module boundaries

### `acquisition/`
Adapts the **g.tec g.Pipe SDK** to an LSL EEG stream. The SDK is proprietary and
user-supplied (see [`hardware-setup.md`](hardware-setup.md)); it is *not* vendored.

**Design intent:** the acquisition layer is abstracted behind an interface. Anyone with
a different amplifier can implement that interface and swap in their own adapter without
touching the rest of the pipeline. That is what makes this a reusable reference
implementation rather than a one-lab artifact. See
[`known-issues.md`](known-issues.md) for the open "non-g.tec amplifier adapter" item.

### `artifact_gating/`
A **median-absolute-deviation (MAD)** gate over a **500-sample rolling buffer**. Samples
whose deviation from the rolling median exceeds the MAD threshold are flagged as
contaminated. The gate runs upstream of the trigger logic so that artefactual samples
never influence the theta Z-score or a sonication decision.

### `triggers/`
The safety-critical surface. Implements the **six-condition gate** and the **safety
ceiling** (theta Z = 10). One predicate per condition, one test per condition. See
[`protocol.md`](protocol.md) for the full table. This is deliberately the most legible
module in the repository.

### `task/`
The **PsychoPy 2-back** working-memory task. Publishes task-state and stimulus/response
markers onto LSL. The task's active state feeds trigger condition 2.

### `lifu/`
The interface to **`openlifu-python`**, which issues sonications. `openlifu-python` is
AGPL-licensed (see the [README](../README.md#dependencies-of-note) and
[`NOTICE`](../NOTICE)). In `--dry-run` mode this module logs the decision but issues no
sonication.

### `logging/`
Timestamped event logging across all streams: EEG gate flags, task markers, trigger
decisions (with the full six-condition state), and sonication events. This is the raw
material for offline latency and safety analysis.

---

## Data flow guarantees

- **Fail-closed.** If any upstream input is missing or stale, the trigger gate refuses
  to sonicate (see [`protocol.md`](protocol.md)).
- **Artefact suppression is upstream of decisions.** The trigger gate only ever sees
  samples that passed the MAD gate.
- **Everything is timestamped.** No decision is made without a corresponding logged
  record on the shared LSL clock.
