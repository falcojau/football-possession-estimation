import pytest

from possession_pipeline.game.stoppage_inference import (
    StoppageEvidence,
    StoppageStatus,
    infer_stoppage,
)


def test_candidate_with_missing_ball():

    evidence = StoppageEvidence(
        restart_candidate_present=True,
        ball_visible=False,
        possession_evidence=None,
    )

    assert infer_stoppage(evidence) == StoppageStatus.INFERRED_STOPPAGE


def test_candidate_with_visible_ball():

    evidence = StoppageEvidence(
        restart_candidate_present=True,
        ball_visible=True,
        possession_evidence="H",
    )

    assert infer_stoppage(evidence) == StoppageStatus.UNKNOWN


def test_missing_ball_without_candidate():

    evidence = StoppageEvidence(
        restart_candidate_present=False,
        ball_visible=False,
        possession_evidence=None,
    )

    assert infer_stoppage(evidence) == StoppageStatus.UNKNOWN


def test_invalid_possession_evidence():

    evidence = StoppageEvidence(
        restart_candidate_present=True,
        ball_visible=False,
        possession_evidence="D",
    )

    with pytest.raises(ValueError):
        infer_stoppage(evidence)