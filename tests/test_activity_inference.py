import pytest

from possession_pipeline.game.activity_inference import (
    ActivityEvidence,
    ActivityStatus,
    infer_activity,
)


def test_visible_ball_with_possession_evidence():

    evidence = ActivityEvidence(
        ball_visible=True,
        possession_evidence="H",
    )

    assert infer_activity(evidence) == ActivityStatus.INFERRED_IN_PLAY


def test_missing_ball():

    evidence = ActivityEvidence(
        ball_visible=False,
        possession_evidence=None,
    )

    assert infer_activity(evidence) == ActivityStatus.UNKNOWN


def test_visible_ball_without_possession_evidence():

    evidence = ActivityEvidence(
        ball_visible=True,
        possession_evidence=None,
    )

    assert infer_activity(evidence) == ActivityStatus.UNKNOWN


def test_invalid_possession_evidence():

    evidence = ActivityEvidence(
        ball_visible=True,
        possession_evidence="D",
    )

    with pytest.raises(ValueError):
        infer_activity(evidence)