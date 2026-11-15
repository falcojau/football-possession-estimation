from dataclasses import dataclass

from possession_pipeline.game.activity_inference import (
    ActivityStatus,
)


@dataclass(frozen=True)
class ActivityDecision:
    final_prediction: str | None
    decision_source: str


def combine_activity_and_possession(
    possession_estimate: str | None,
    activity_status: ActivityStatus,
) -> ActivityDecision:

    if possession_estimate not in ("H", "A", None):
        raise ValueError("Invalid possession estimate")

    if not isinstance(activity_status, ActivityStatus):
        raise ValueError("Invalid activity status")

    if activity_status == ActivityStatus.INFERRED_IN_PLAY:
        return ActivityDecision(
            final_prediction=possession_estimate,
            decision_source="INFERRED_ACTIVITY",
        )

    return ActivityDecision(
        final_prediction=None,
        decision_source="UNKNOWN_ACTIVITY",
    )