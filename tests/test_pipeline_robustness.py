import pytest

from possession_pipeline.pipeline.integration import (
    run_pipeline_with_events,
)

from possession_pipeline.game.game_state_machine import (
    GameEvent,
    GameState,
)

from possession_pipeline.contracts.data_contracts import FrameResult


def test_long_missing_evidence():

    evidence = [
        "H",
        None,
        None,
        None,
        None,
        None,
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
        None,
        None,
        None,
    ]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,
    )

    assert len(results) == 6

    assert [r.possession_estimate for r in results] == [
        "H", "H", "H", "H", "H", "H"
    ]

    assert [r.final_prediction for r in results] == [
        "H", "H", "H", "H", "H", "H"
    ]


def test_state_transitions():

    evidence = [
        "H", "H", "H",
        "A", "A", "A",
        "A", "A",
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
        None,
        None,
        None,
        GameEvent.STOPPAGE_CONFIRMED,
        GameEvent.RESTART_CONFIRMED,
    ]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,
    )

    assert [r.possession_estimate for r in results] == [
        "H", "H", "H",
        "H", "H", "A",
        "A", "A",
    ]

    assert [r.final_prediction for r in results] == [
        "H", "H", "H",
        "H", "H", "A",
        "D", "A",
    ]


def test_invalid_evidence():

    evidence = [
        "H",
        "Barcelona",
        "A",
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
    ]

    with pytest.raises(ValueError):
        run_pipeline_with_events(
            evidence_sequence=evidence,
            game_events=events,
            confirmation_frames=3,
        )


def test_no_look_ahead():

    evidence_short = [
        "H", "H", "A"
    ]

    events_short = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
    ]

    evidence_long = [
        "H", "H", "A",
        "A", "A", "H",
    ]

    events_long = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
        None,
        None,
        GameEvent.STOPPAGE_CONFIRMED,
    ]

    short_results = run_pipeline_with_events(
        evidence_sequence=evidence_short,
        game_events=events_short,
        confirmation_frames=3,
    )

    long_results = run_pipeline_with_events(
        evidence_sequence=evidence_long,
        game_events=events_long,
        confirmation_frames=3,
    )

    assert [
        r.final_prediction for r in short_results
    ] == [
        r.final_prediction for r in long_results[:3]
    ]


def test_output_consistency():

    evidence = [
        "H", None, "A", "A", "A"
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
        None,
        None,
    ]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,
    )

    assert len(results) == len(evidence)

    assert [r.frame_id for r in results] == list(
        range(len(evidence))
    )

    assert all(
        isinstance(result, FrameResult)
        for result in results
    )

    assert all(
        result.possession_estimate in ("H", "A", None)
        for result in results
    )

    assert all(
        result.final_prediction in ("H", "A", "D", None)
        for result in results
    )

    assert all(
        isinstance(result.game_state, GameState)
        for result in results
    )


def test_empty_sequence():

    results = run_pipeline_with_events(
        evidence_sequence=[],
        game_events=[],
        confirmation_frames=3,
    )

    assert results == []


def test_candidate_reset_after_missing():

    evidence = [
        "H",
        "A",
        "A",
        None,
        "A",
        "A",
        "A",
    ]

    events = [
        GameEvent.RESTART_CONFIRMED,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,
    )

    assert [r.possession_estimate for r in results] == [
        "H",
        "H",
        "H",
        "H",
        "H",
        "H",
        "A",
    ]


def test_unknown_remains_unknown():

    evidence = ["H", "H", "A", "A"]

    events = [None, None, None, None]

    results = run_pipeline_with_events(
        evidence_sequence=evidence,
        game_events=events,
        confirmation_frames=3,
    )

    assert all(
        r.game_state == GameState.UNKNOWN
        for r in results
    )

    assert all(
        r.final_prediction is None
        for r in results
    )