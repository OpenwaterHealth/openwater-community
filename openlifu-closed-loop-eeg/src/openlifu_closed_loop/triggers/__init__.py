"""The safety-critical trigger gate. See conditions.py and docs/protocol.md."""

from .conditions import (  # noqa: F401
    LoopState,
    may_sonicate,
    blocking_conditions,
    CONDITIONS,
    THETA_TRIGGER_Z,
    THETA_CEILING_Z,
    COOLDOWN_SECONDS,
    SESSION_CAP,
    BASELINE_SECONDS,
)
