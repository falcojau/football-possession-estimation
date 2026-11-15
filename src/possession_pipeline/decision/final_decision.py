from possession_pipeline.game.game_state_machine import (
    GameState,
)
from possession_pipeline.game.activity_inference import (
    ActivityStatus,
)
from possession_pipeline.decision.activity_decision import (
    ActivityDecision,
    combine_activity_and_possession,
)
from possession_pipeline.game.stoppage_inference import (
    StoppageStatus,
)


def make_final_decision(
    possession_estimate: str | None,
    game_state: GameState,
    activity_status: ActivityStatus,
    stoppage_status: StoppageStatus = StoppageStatus.UNKNOWN
) -> ActivityDecision:

    if possession_estimate not in ("H", "A", None):
        raise ValueError("Invalid possession estimate")

    if not isinstance(game_state, GameState):
        raise ValueError("Invalid game state")

    if not isinstance(activity_status, ActivityStatus):
        raise ValueError("Invalid activity status")

    if not isinstance(stoppage_status, StoppageStatus):
        raise ValueError("Invalid stoppage status")

    if game_state == GameState.STOPPED:
        return ActivityDecision(
            final_prediction="D",
            decision_source="CONFIRMED_STOPPAGE",
        )

    if game_state == GameState.IN_PLAY:
        return ActivityDecision(
            final_prediction=possession_estimate,
            decision_source="CONFIRMED_IN_PLAY",
        )

    if game_state == GameState.POSSIBLE_STOPPAGE:
        return ActivityDecision(
            final_prediction=None,
            decision_source="POSSIBLE_STOPPAGE",
        )

    if stoppage_status == StoppageStatus.INFERRED_STOPPAGE:
        return ActivityDecision(
            final_prediction="D",
            decision_source="INFERRED_STOPPAGE",
        )

    return combine_activity_and_possession(
        possession_estimate=possession_estimate,
        activity_status=activity_status,
    )