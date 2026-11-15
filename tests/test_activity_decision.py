import pytest

from possession_pipeline.decision.activity_decision import (
    combine_activity_and_possession,
)
from possession_pipeline.game.activity_inference import (
    ActivityStatus,
)


def test_inferred_activity_with_home_possession():

    result = combine_activity_and_possession(
        possession_estimate="H",
        activity_status=ActivityStatus.INFERRED_IN_PLAY,
    )

    assert result.final_prediction == "H"
    assert result.decision_source == "INFERRED_ACTIVITY"


def test_inferred_activity_without_possession():

    result = combine_activity_and_possession(
        possession_estimate=None,
        activity_status=ActivityStatus.INFERRED_IN_PLAY,
    )

    assert result.final_prediction is None


def test_unknown_activity():

    result = combine_activity_and_possession(
        possession_estimate="A",
        activity_status=ActivityStatus.UNKNOWN,
    )

    assert result.final_prediction is None
    assert result.decision_source == "UNKNOWN_ACTIVITY"


def test_invalid_possession():

    with pytest.raises(ValueError):
        combine_activity_and_possession(
            possession_estimate="D",
            activity_status=ActivityStatus.INFERRED_IN_PLAY,
        )