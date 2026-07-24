"""Closed-loop LIFU–EEG reference implementation (research use only).

Modules:
    acquisition     — g.Pipe SDK adapter → LSL (abstracted for other amplifiers)
    artifact_gating — MAD gate over a 500-sample rolling buffer
    triggers        — the six-condition safety-critical gate
    task            — PsychoPy 2-back working-memory task
    lifu            — openlifu-python sonication interface
    logging         — timestamped event logging across all streams

See docs/architecture.md for how these connect over Lab Streaming Layer.
"""

__version__ = "0.1.0"
