import pytest

from possession_pipeline.possession.state_machine import (
    TemporalStateMachine,
)


def test_expiration_after_missing_limit():

    machine = TemporalStateMachine(
        confirmation_frames=3,
        max_missing_frames=2,
    )

    evidence = ["H", None, None, None]

    results = [machine.update(item) for item in evidence]

    assert results == ["H", "H", "H", None]


def test_new_evidence_after_expiration():

    machine = TemporalStateMachine(
        confirmation_frames=3,
        max_missing_frames=2,
    )

    evidence = ["H", None, None, None, "A"]

    results = [machine.update(item) for item in evidence]

    assert results == ["H", "H", "H", None, "A"]


def test_default_behavior_unchanged():

    machine = TemporalStateMachine(
        confirmation_frames=3,
    )

    evidence = ["H", None, None, None, None]

    results = [machine.update(item) for item in evidence]

    assert results == ["H", "H", "H", "H", "H"]


def test_invalid_missing_limit():

    with pytest.raises(ValueError):
        TemporalStateMachine(
            confirmation_frames=3,
            max_missing_frames=-1,
        )