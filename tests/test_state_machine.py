import pytest

from possession_pipeline.possession.state_machine import run_temporal_state_machine


def test_output_length():

    evidence = ["H", "H", "A", None, "A"]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert len(predictions) == len(evidence)


def test_valid_labels():

    evidence = ["H", "A", None, "H", "A"]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert set(predictions).issubset({"H", "A", None})


def test_missing_observations():

    evidence = ["H", "H", None, None, "H"]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert predictions == ["H", "H", "H", "H", "H"]


def test_short_opposite_evidence():

    evidence = ["H", "H", "A", "A", "H"]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert predictions == ["H", "H", "H", "H", "H"]


def test_confirmed_transition():

    evidence = ["H", "H", "A", "A", "A"]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert predictions == ["H", "H", "H", "H", "A"]

def test_no_look_ahead():

    prefix = ["H", "H", "A", "A"]

    future = ["A", "A", "H", "H"]

    predictions_prefix = run_temporal_state_machine(
        prefix,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    predictions_full = run_temporal_state_machine(
        prefix + future,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert predictions_prefix == predictions_full[:len(prefix)]

def test_missing_resets_candidate():

    evidence = [
        "H",
        "A",
        "A",
        None,
        "A",
    ]

    predictions = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert predictions == [
        "H",
        "H",
        "H",
        "H",
        "H",
    ]