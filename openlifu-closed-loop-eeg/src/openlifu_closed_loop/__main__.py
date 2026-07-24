"""Entry point for the closed-loop pipeline.

Usage:
    python -m openlifu_closed_loop --source {synthetic,gpipe} [--dry-run]

--dry-run exercises the full trigger gate and logging path but issues NO sonications.

This is scaffolding for the reference implementation. The wiring of acquisition →
artifact gating → triggers → lifu → logging is filled in when the original developer's
pipeline is migrated in (see the repository README and docs/architecture.md). The
safety-critical trigger gate itself is implemented in ``triggers/conditions.py``.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openlifu_closed_loop")
    parser.add_argument(
        "--source",
        choices=["synthetic", "gpipe"],
        default="synthetic",
        help="EEG source: 'synthetic' fixture (no human data) or the g.Pipe adapter.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the full decision/logging path without issuing sonications.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    raise NotImplementedError(
        "Pipeline wiring is scaffolding pending migration of the developer's code. "
        f"Parsed args: source={args.source!r}, dry_run={args.dry_run}. "
        "The trigger gate is implemented and tested in triggers/conditions.py."
    )


if __name__ == "__main__":
    main()
