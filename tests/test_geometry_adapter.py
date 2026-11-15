import pytest

from possession_pipeline.game.geometry_adapter import (
    positions_to_candidates,
)

from possession_pipeline.game.game_state_machine import GameEvent

from possession_pipeline.pipeline.integration import (
    run_pipeline_with_geometry,
)


def test_geometry_adapter():

    positions = [
        (0.50, 0.50),
        (1.05, 0.50),
        (None, None),
    ]

    events = positions_to_candidates(positions)

    assert events == [
        None,
        GameEvent.STOPPAGE_CANDIDATE,
        None,
    ]


def test_geometry_pipeline_remains_unknown():

    evidence = ["H", "H", "A"]

    positions = [
        (0.50, 0.50),
        (1.05, 0.50),
        (0.50, 0.50),
    ]

    results = run_pipeline_with_geometry(
        evidence_sequence=evidence,
        ball_positions=positions,
        confirmation_frames=3,  # Synthetic test only
    )

    assert len(results) == 3

    assert all(
        result.game_state.value == "UNKNOWN"
        for result in results
    )

    assert all(
        result.final_prediction is None
        for result in results
    )


def test_geometry_pipeline_rejects_misalignment():

    evidence = ["H", "A"]

    positions = [(0.50, 0.50)]

    with pytest.raises(ValueError):
        run_pipeline_with_geometry(
            evidence_sequence=evidence,
            ball_positions=positions,
            confirmation_frames=3,
        )


def test_geometry_adapter_rejects_invalid_position():

    with pytest.raises(ValueError):
        positions_to_candidates([
            (0.50, 0.50),
            "invalid",
        ])