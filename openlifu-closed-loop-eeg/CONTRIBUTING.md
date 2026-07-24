# Contributing

Thanks for your interest in contributing to `openlifu-closed-loop-eeg`.

This repository is an Openwater open-source project. Organization-wide contribution
guidance, the Code of Conduct, and the Contributor License Agreement (CLA) process live
in the Openwater org `.github` repository and apply here. This file covers what is
specific to this repository.

## Before you start

- **Good entry points** are in [`docs/known-issues.md`](docs/known-issues.md) and the
  repository's issues. Hardware-adapter contributions (a non-g.tec acquisition adapter)
  and the video-marker synchronization feature are especially welcome.
- **Design-dependent items** are labeled `needs-design`. Please wait for scope to be
  ruled on before investing significant effort in those — comment on the issue first.

## Contributor License Agreement

Contributions are accepted under the project's CLA. CLA Assistant is configured on the
org, so signing is a one-time, in-PR step. External contributions will be gated on it.

## Development

```bash
pip install -e ".[dev]"
pytest                      # runs the test suite, including one test per trigger condition
python -m fixtures.synthetic_theta            # synthetic EEG source, no human data
python -m openlifu_closed_loop --source synthetic --dry-run
```

## The safety-critical module

The six trigger conditions live in
[`src/openlifu_closed_loop/triggers/`](src/openlifu_closed_loop/triggers) with **one
test per condition.** If you change a threshold or a condition:

1. Update the predicate in `triggers/`.
2. Update its test.
3. Update the condition table in [`docs/protocol.md`](docs/protocol.md).

These three must stay in sync. PRs that change trigger behavior without updating the
protocol doc and tests will be asked to do so.

## Language discipline

This is a pre-clearance, research-use project. Public-facing text — code comments,
docs, commit messages, issues — uses **subject**, **sonication**, and **research use**.
Do not introduce clinical framing (e.g. "patient", "treatment", "clinical potential").
See the disclaimer in the [README](README.md).

## Data

Do not commit raw EEG, subject-derived data, or the proprietary g.Pipe SDK (or any SDK
binaries) to this repository. See [`.gitignore`](.gitignore).
