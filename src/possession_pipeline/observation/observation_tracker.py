def track_observations(
    evidence_sequence: list[str | None],
    predictions: list[str | None],
) -> list[dict]:

    if len(evidence_sequence) != len(predictions):
        raise ValueError(
            "Evidence and predictions must have the same length"
        )

    results = []

    for frame, (evidence, prediction) in enumerate(
        zip(evidence_sequence, predictions)
    ):

        observation_status = (
            "MISSING" if evidence is None else "VISIBLE"
        )

        results.append({
            "frame": frame,
            "last_known_state": prediction,
            "observation_status": observation_status,
        })

    return results