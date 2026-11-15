from possession_pipeline.possession.state_machine import (
    TemporalStateMachine,
    run_temporal_state_machine,
)


def test_incremental_matches_batch():

    evidence = ["H", "H", "A", "A", "A", None, "H", "H", "H"]

    batch = run_temporal_state_machine(
        evidence,
        confirmation_frames=3,
    )

    machine = TemporalStateMachine(confirmation_frames=3)

    incremental = [
        machine.update(item)
        for item in evidence
    ]

    assert incremental == batch


def test_state_preserved_between_chunks():

    machine = TemporalStateMachine(confirmation_frames=3)

    chunk_1 = ["H", "H", "A"]
    chunk_2 = ["A", "A"]

    result_1 = [machine.update(item) for item in chunk_1]
    result_2 = [machine.update(item) for item in chunk_2]

    assert result_1 + result_2 == [
        "H", "H", "H", "H", "A"
    ]


def test_missing_resets_candidate_not_current_state():

    machine = TemporalStateMachine(confirmation_frames=3)

    evidence = ["H", "A", "A", None, "A"]

    results = [machine.update(item) for item in evidence]

    assert results == ["H", "H", "H", "H", "H"]


def test_invalid_evidence():

    machine = TemporalStateMachine(confirmation_frames=3)

    try:
        machine.update("D")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")