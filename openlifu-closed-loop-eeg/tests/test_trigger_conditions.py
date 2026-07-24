"""One test per trigger condition — the safety-critical surface.

If you change a threshold or condition in ``triggers/conditions.py``, update the matching
test here and the table in ``docs/protocol.md``. The three must stay in sync.
"""

from openlifu_closed_loop.triggers.conditions import (
    LoopState,
    may_sonicate,
    blocking_conditions,
)


def _ready_state(**overrides) -> LoopState:
    """A state in which all six conditions pass; override one field to break one."""
    base = dict(
        baseline_seconds_collected=100.0,
        task_active=True,
        theta_z=2.0,                       # > 1.5 and < 10
        seconds_since_last_sonication=15.0,
        sonication_count=0,
    )
    base.update(overrides)
    return LoopState(**base)


def test_all_conditions_met_permits_sonication():
    assert may_sonicate(_ready_state())
    assert blocking_conditions(_ready_state()) == []


def test_condition_1_baseline_incomplete_blocks():
    state = _ready_state(baseline_seconds_collected=99.0)
    assert not may_sonicate(state)
    assert "baseline_complete" in blocking_conditions(state)


def test_condition_2_task_inactive_blocks():
    state = _ready_state(task_active=False)
    assert not may_sonicate(state)
    assert "task_active" in blocking_conditions(state)


def test_condition_3_theta_below_trigger_blocks():
    state = _ready_state(theta_z=1.4)
    assert not may_sonicate(state)
    assert "theta_above_trigger" in blocking_conditions(state)


def test_condition_4_theta_at_or_above_ceiling_blocks():
    state = _ready_state(theta_z=10.0)
    assert not may_sonicate(state)
    assert "below_safety_ceiling" in blocking_conditions(state)


def test_condition_5_cooldown_not_elapsed_blocks():
    state = _ready_state(seconds_since_last_sonication=9.9)
    assert not may_sonicate(state)
    assert "cooldown_elapsed" in blocking_conditions(state)


def test_condition_6_session_cap_reached_blocks():
    state = _ready_state(sonication_count=10)
    assert not may_sonicate(state)
    assert "under_session_cap" in blocking_conditions(state)
