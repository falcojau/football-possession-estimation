from possession_pipeline.observation.observation_tracker import track_observations

def test_observation_status():

    evidence = ["H", "H", None, None, "A"]

    predictions = ["H", "H", "H", "H", "H"]

    results = track_observations(
        evidence,
        predictions,
    )

    assert results[0]["observation_status"] == "VISIBLE"

    assert results[2]["observation_status"] == "MISSING"

    assert results[3]["last_known_state"] == "H"

    assert results[4]["observation_status"] == "VISIBLE"


def test_mismatched_lengths():

    evidence = ["H", "A", None]
    predictions = ["H", "H"]

    try:
        track_observations(evidence, predictions)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")