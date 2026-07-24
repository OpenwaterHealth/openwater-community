# openlifu-closed-loop-eeg

A reference implementation of **closed-loop low-intensity focused ultrasound (LIFU)
driven by real-time EEG**, built on the [OpenLIFU](https://github.com/OpenwaterHealth)
platform and open hardware.

The system acquires EEG, computes a running theta-band Z-score against a per-subject
baseline, and gates LIFU sonication on a set of explicit, safety-bounded trigger
conditions while a subject performs a working-memory task. It is a *feasibility
demonstration* produced by a two-subject study — the answer to the recurring question,
*"can OpenLIFU do closed-loop?"*

> [!IMPORTANT]
> **Research use only.** This software and the OpenLIFU platform are intended
> exclusively for research use. They are not cleared or approved by the FDA for
> clinical use. The safety and effectiveness of the platform have not been
> established through the FDA's formal review process.

---

## What this is

A closed-loop pipeline that connects four moving parts over
[Lab Streaming Layer (LSL)](https://labstreaminglayer.readthedocs.io/):

1. **Acquisition** — EEG streamed from a g.tec amplifier through the g.Pipe SDK.
2. **Artifact gating** — a median-absolute-deviation (MAD) gate over a rolling
   sample buffer that suppresses sonication decisions on contaminated data.
3. **Trigger logic** — a six-condition gate (see below) that decides, sample by
   sample, whether a sonication is permitted.
4. **Sonication** — LIFU pulses issued through `openlifu-python`, while the subject
   runs a PsychoPy 2-back task.

Everything is logged with timestamps for offline latency and safety analysis.

The **safety-critical surface is one module**: [`triggers/`](src/openlifu_closed_loop/triggers).
All six gate conditions live there, with one test per condition. If this work is ever
read in a research, IRB, or regulatory context, that is the module to read first. It is
written to be legible on purpose — see [`docs/protocol.md`](docs/protocol.md).

### The six trigger conditions

A sonication is permitted only when **all** of the following hold:

| # | Condition | Meaning |
|---|-----------|---------|
| 1 | Baseline buffer complete | The 100 s calibration baseline has been collected |
| 2 | Task active | The subject is engaged in the 2-back task |
| 3 | Theta Z > 1.5 | Real-time theta power exceeds the trigger threshold |
| 4 | Below safety ceiling (Z < 10) | Theta Z-score is under the hard safety ceiling |
| 5 | Cooldown elapsed | At least 10 s since the previous sonication |
| 6 | Session cap not reached | Fewer than 10 sonications delivered this session |

See [`docs/protocol.md`](docs/protocol.md) for the full rationale behind each
threshold and [`docs/calibration.md`](docs/calibration.md) for how the baseline and
Z-score are computed.

---

## Run it without any human data

The pipeline is runnable end-to-end with **no human recordings**. A synthetic signal
generator ([`fixtures/synthetic_theta.py`](fixtures/synthetic_theta.py)) replays a
configurable theta-band signal onto an LSL stream, so you can exercise acquisition,
artifact gating, the trigger gate, and logging without an amplifier or a subject.

```bash
# 1. Install (see docs/hardware-setup.md for the proprietary g.Pipe SDK step)
pip install -e .

# 2. Start the synthetic EEG source
python -m fixtures.synthetic_theta

# 3. Run the closed-loop pipeline against it
python -m openlifu_closed_loop --source synthetic --dry-run
```

`--dry-run` exercises the full trigger gate and logging path but issues **no**
sonications. No raw EEG from the feasibility study is published in this repository;
see [Data & human subjects](#data--human-subjects).

---

## Documentation

| Document | What's in it |
|----------|--------------|
| [`docs/protocol.md`](docs/protocol.md) | Sonication params, task design, the six trigger conditions |
| [`docs/architecture.md`](docs/architecture.md) | LSL topology and module boundaries |
| [`docs/hardware-setup.md`](docs/hardware-setup.md) | Headset + LIFU co-placement, gel, cap, g.Pipe SDK install |
| [`docs/calibration.md`](docs/calibration.md) | 100 s baseline and Z-score computation |
| [`docs/known-issues.md`](docs/known-issues.md) | Honest, complete list of current limitations and bugs |
| [`docs/results/feasibility-report.md`](docs/results/feasibility-report.md) | Two-subject feasibility findings |

---

## Dependencies of note

**`openlifu-python` is AGPL-licensed; this repository is Apache 2.0.** Openwater holds
copyright on both, so licensing this extension repository Apache 2.0 is not a
contradiction. However, **downstream users who combine this code with `openlifu-python`
still inherit the core's AGPL obligations.** If you build on this pipeline, review the
AGPL terms of `openlifu-python` for your use. See [`NOTICE`](NOTICE).

**The g.Pipe SDK is proprietary and cannot be vendored or redistributed.** It is a
user-supplied dependency — you install it yourself following
[`docs/hardware-setup.md`](docs/hardware-setup.md). The acquisition layer is abstracted
behind an interface so a different amplifier can be supported by swapping in a new
adapter; contributions of adapters for other hardware are welcome.

---

## Data & human subjects

The feasibility study involved **two employee participants under a 2-subject research
authorization.** No raw EEG or any data derived from those recordings is published in
this repository. If a real trace is ever published, it will arrive as a separate,
explicitly consented contribution — not as part of this scaffold.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Open issues and hardware-adapter contributions
are especially welcome — the [`docs/known-issues.md`](docs/known-issues.md) list is a
good place to start.

## Citing this work

If you use this reference implementation, please cite it using the metadata in
[`CITATION.cff`](CITATION.cff).

## License

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
