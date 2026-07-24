"""The six trigger conditions that gate every sonication.

This is the safety-critical surface of the system. A sonication is permitted only when
ALL six conditions are simultaneously true. Each condition is a single, independently
testable predicate, and each has one test in ``tests/test_trigger_conditions.py``.

The condition table here is kept in sync with ``docs/protocol.md``. A change to a
threshold in one place must be reflected in the other and in the tests.

The gate is conjunctive and fail-closed: any missing or out-of-range input makes the
condition it feeds evaluate False, so no sonication is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Thresholds (mirror docs/protocol.md) ---
THETA_TRIGGER_Z = 1.5      # condition 3: theta Z above which a sonication may be triggered
THETA_CEILING_Z = 10.0     # condition 4: hard safety ceiling; at/above this we refuse
COOLDOWN_SECONDS = 10.0    # condition 5: minimum spacing between sonications
SESSION_CAP = 10           # condition 6: maximum sonications per session
BASELINE_SECONDS = 100.0   # condition 1: required calibration baseline length


@dataclass(frozen=True)
class LoopState:
    """A snapshot of everything the trigger gate needs to make one decision."""

    baseline_seconds_collected: float
    task_active: bool
    theta_z: float
    seconds_since_last_sonication: float
    sonication_count: int


# --- The six conditions (see docs/protocol.md) ---

def baseline_complete(state: LoopState) -> bool:
    """Condition 1: the 100 s calibration baseline has been fully collected."""
    return state.baseline_seconds_collected >= BASELINE_SECONDS


def task_active(state: LoopState) -> bool:
    """Condition 2: the subject is engaged in the 2-back task."""
    return bool(state.task_active)


def theta_above_trigger(state: LoopState) -> bool:
    """Condition 3: real-time theta Z-score exceeds the trigger threshold (1.5)."""
    return state.theta_z > THETA_TRIGGER_Z


def below_safety_ceiling(state: LoopState) -> bool:
    """Condition 4: theta Z-score is below the hard safety ceiling (10).

    A Z at or above the ceiling is treated as an implausible / artefactual excursion,
    and the gate refuses to sonicate rather than acting on it.
    """
    return state.theta_z < THETA_CEILING_Z


def cooldown_elapsed(state: LoopState) -> bool:
    """Condition 5: at least 10 s have passed since the previous sonication."""
    return state.seconds_since_last_sonication >= COOLDOWN_SECONDS


def under_session_cap(state: LoopState) -> bool:
    """Condition 6: fewer than 10 sonications have been delivered this session."""
    return state.sonication_count < SESSION_CAP


# Ordered so a caller can report exactly which condition(s) blocked a decision.
CONDITIONS = (
    ("baseline_complete", baseline_complete),
    ("task_active", task_active),
    ("theta_above_trigger", theta_above_trigger),
    ("below_safety_ceiling", below_safety_ceiling),
    ("cooldown_elapsed", cooldown_elapsed),
    ("under_session_cap", under_session_cap),
)


def may_sonicate(state: LoopState) -> bool:
    """Return True only if all six trigger conditions hold. Fail-closed."""
    return all(predicate(state) for _name, predicate in CONDITIONS)


def blocking_conditions(state: LoopState) -> list[str]:
    """Return the names of the conditions currently blocking a sonication.

    An empty list means a sonication is permitted. Used for auditable logging of every
    decision, permitted or refused (see docs/protocol.md, section 5).
    """
    return [name for name, predicate in CONDITIONS if not predicate(state)]
