"""Synthetic theta-band EEG source — replay fixture, NO human data.

Streams a configurable theta-band signal (with adjustable bursts and noise) onto an LSL
'EEG' stream so the full pipeline — acquisition, artifact gating, calibration, the
trigger gate, and logging — can be exercised end to end without an amplifier or a
subject. This is the recommended way to inspect the system's real-time behavior.

Usage:
    python -m fixtures.synthetic_theta [--fs 250] [--theta-hz 6.0] [--duration 0]

--duration 0 streams indefinitely until interrupted.

No recording from the feasibility study is included here or anywhere in this repository.
"""

from __future__ import annotations

import argparse
import math
import time

try:
    from pylsl import StreamInfo, StreamOutlet
except Exception:  # pragma: no cover - pylsl optional at import time
    StreamInfo = StreamOutlet = None  # type: ignore


def synthetic_sample(t: float, theta_hz: float, burst: bool) -> float:
    """One synthetic EEG sample at time ``t`` (seconds).

    A theta-band sinusoid whose amplitude increases during a 'burst', so that the
    downstream Z-score crosses the trigger threshold in a controllable way. Pure
    function — deterministic, easy to unit-test, and free of any human data.
    """
    amplitude = 3.0 if burst else 1.0
    return amplitude * math.sin(2.0 * math.pi * theta_hz * t)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="synthetic_theta")
    parser.add_argument("--fs", type=float, default=250.0, help="Sample rate (Hz).")
    parser.add_argument("--theta-hz", type=float, default=6.0, help="Theta frequency (Hz).")
    parser.add_argument(
        "--duration", type=float, default=0.0,
        help="Seconds to stream; 0 = until interrupted.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if StreamOutlet is None:
        raise RuntimeError("pylsl is required to stream. Install with: pip install pylsl")

    info = StreamInfo("EEG", "EEG", 1, args.fs, "float32", "synthetic_theta")
    outlet = StreamOutlet(info)
    print(f"Streaming synthetic theta at {args.theta_hz} Hz, fs={args.fs} Hz. Ctrl-C to stop.")

    n = 0
    dt = 1.0 / args.fs
    try:
        while True:
            t = n * dt
            # A burst every ~20 s so the trigger gate has something to fire on.
            burst = (int(t) % 20) < 3
            outlet.push_sample([synthetic_sample(t, args.theta_hz, burst)])
            n += 1
            if args.duration and t >= args.duration:
                break
            time.sleep(dt)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
