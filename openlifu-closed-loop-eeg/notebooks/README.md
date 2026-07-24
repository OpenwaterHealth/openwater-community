# Notebooks

Analysis notebooks for the study.

## `latency_analysis.ipynb`

Measures and compares end-to-end trigger latency across execution paths, and documents
the **~250 ms delta between the direct-Python path (~170 ms) and the 3D Slicer GUI path
(~422 ms)** described in [`../docs/known-issues.md`](../docs/known-issues.md) and the
[feasibility report](../docs/results/feasibility-report.md).

The measurement is derived from the timestamped decision logs (see
[`../docs/architecture.md`](../docs/architecture.md)) and uses no human-subject data.

> The notebook itself is migrated in with the original developer's analysis code.
> This README documents its purpose so the finding is discoverable in the meantime.
