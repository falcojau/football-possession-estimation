from possession_pipeline.decision.final_decision import (
    make_final_decision,
)
from possession_pipeline.game.game_state_machine import (
    GameState,
)
from possession_pipeline.game.activity_inference import (
    ActivityStatus,
)
from possession_pipeline.game.stoppage_inference import (
    StoppageStatus,
)

def test_confirmed_stoppage_overrides_activity():

    result = make_final_decision(
        possession_estimate="H",
        game_state=GameState.STOPPED,
        activity_status=ActivityStatus.INFERRED_IN_PLAY,
    )

    assert result.final_prediction == "D"
    assert result.decision_source == "CONFIRMED_STOPPAGE"


def test_confirmed_in_play():

    result = make_final_decision(
        possession_estimate="A",
        game_state=GameState.IN_PLAY,
        activity_status=ActivityStatus.UNKNOWN,
    )

    assert result.final_prediction == "A"
    assert result.decision_source == "CONFIRMED_IN_PLAY"


def test_unknown_uses_inferred_activity():

    result = make_final_decision(
        possession_estimate="H",
        game_state=GameState.UNKNOWN,
        activity_status=ActivityStatus.INFERRED_IN_PLAY,
    )

    assert result.final_prediction == "H"
    assert result.decision_source == "INFERRED_ACTIVITY"


def test_possible_stoppage_is_conservative():

    result = make_final_decision(
        possession_estimate="H",
        game_state=GameState.POSSIBLE_STOPPAGE,
        activity_status=ActivityStatus.INFERRED_IN_PLAY,
    )

    assert result.final_prediction is None
    assert result.decision_source == "POSSIBLE_STOPPAGE"


def test_inferred_stoppage_returns_dead_ball():

    result = make_final_decision(
        possession_estimate=None,
        game_state=GameState.UNKNOWN,
        activity_status=ActivityStatus.UNKNOWN,
        stoppage_status=StoppageStatus.INFERRED_STOPPAGE,
    )

    assert result.final_prediction == "D"
    assert result.decision_source == "INFERRED_STOPPAGE"


def test_confirmed_in_play_overrides_inferred_stoppage():

    result = make_final_decision(
        possession_estimate="H",
        game_state=GameState.IN_PLAY,
        activity_status=ActivityStatus.UNKNOWN,
        stoppage_status=StoppageStatus.INFERRED_STOPPAGE,
    )

    assert result.final_prediction == "H"
    assert result.decision_source == "CONFIRMED_IN_PLAY"


def test_possible_stoppage_remains_conservative():

    result = make_final_decision(
        possession_estimate="A",
        game_state=GameState.POSSIBLE_STOPPAGE,
        activity_status=ActivityStatus.UNKNOWN,
        stoppage_status=StoppageStatus.INFERRED_STOPPAGE,
    )

    assert result.final_prediction is None
    assert result.decision_source == "POSSIBLE_STOPPAGE"