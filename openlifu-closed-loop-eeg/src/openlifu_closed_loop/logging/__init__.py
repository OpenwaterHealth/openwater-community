"""Timestamped event logging across all streams.

Logs EEG gate flags, task markers, trigger decisions (with the full six-condition state
via ``triggers.blocking_conditions``), and sonication events on the shared LSL clock.
This is the raw material for offline latency and safety analysis (see
notebooks/latency_analysis.ipynb).

Scaffolding: the concrete logger is migrated in with the developer's code.
"""
