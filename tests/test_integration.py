import pytest

from possession_pipeline.pipeline.integration import run_pipeline
from possession_pipeline.game.game_state_machine import GameState
from possession_pipeline.pipeline.integration import (
    run_pipeline_with_events,
)

from possession_pipeline.game.game_state_machine import GameEvent


def test_pipeline_integration():

    evidence = [
        "H",
        "H",
        None,
        "A",
        "A",
        "A",
    ]

    game_states = [
        GameState.IN_PLAY,
        GameState.IN_PLAY,
        GameState.UNKNOWN,
        GameState.IN_PLAY,
        GameState.IN_PLAY,
        GameState.IN_PLAY,
    ]

    results = run_pipeline(
        evidence_sequence=evidence,
        game_states=game_states,
        confirmation_frames=3,  # Synthetic test only
    )

    assert len(results) == 6

    assert [r.frame_id for r in results] == list(range(6))

    assert [r.possession_estimate for r in results] == [
        "H",
        "H",
        "H",
        "H",
        "H",
        "A",
    ]

    assert [r.final_prediction for r in results] == [
        "H",
        "H",
        None,
        "H",
        "H",
        "A",
    ]

def test_pipeline_rejects_misaligned_inputs():

    evidence = ["H", "A", "H"]

    game_states = [
        GameState.IN_PLAY,
        GameState.IN_PLAY,
    ]

    with pytest.raises(ValueError):
        run_pipeline(
            evidence_sequence=evidence,
            game_states=game_states,
            confirmation_frames=3,
        )

def test_pipeline_with_game_events():

    evidence = [
        "H",
        "H",
        "H",
        None,
        "A",
        "A",
        "A",
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        GameEvent.STOPPAGE_CANDIDATE,
        GameEvent.STOPPAGE_CONFIRMED,
        None,
        GameEvent.RESTART_CONFIRMED,
        None,
    ]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,  # Synthetic test only
    )

    assert len(results) == 7

    assert [r.game_state for r in results] == [
        GameState.IN_PLAY,
        GameState.IN_PLAY,
        GameState.POSSIBLE_STOPPAGE,
        GameState.STOPPED,
        GameState.STOPPED,
        GameState.IN_PLAY,
        GameState.IN_PLAY,
    ]

    assert [r.possession_estimate for r in results] == [
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "A",
    ]

    assert [r.final_prediction for r in results] == [
        "H",
        "H",
        None,
        "D",
        "D",
        "H",
        "A",
    ]

def test_pipeline_with_events_rejects_misalignment():

    evidence = ["H", "A", "H"]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
    ]

    with pytest.raises(ValueError):
        run_pipeline_with_events(
            evidence_sequence=evidence,
            game_events=events,
            confirmation_frames=3,
        )

def test_pipeline_with_events_rejects_invalid_event():

    evidence = ["H", "H"]

    events = [
        GameEvent.RESTART_CONFIRMED,
        "INVALID_EVENT",
    ]

    with pytest.raises(ValueError):
        run_pipeline_with_events(
            evidence_sequence=evidence,
            game_events=events,
            confirmation_frames=3,
        )