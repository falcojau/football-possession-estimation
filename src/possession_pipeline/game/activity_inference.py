from dataclasses import dataclass
from enum import Enum


class ActivityStatus(Enum):
    INFERRED_IN_PLAY = "INFERRED_IN_PLAY"  # Nuestro algoritmo considera probable que el juego esté activo
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ActivityEvidence:
    ball_visible: bool
    possession_evidence: str | None


def infer_activity(
    evidence: ActivityEvidence,
) -> ActivityStatus:

    if evidence.possession_evidence not in ("H", "A", None):
        raise ValueError("Invalid possession evidence")

    if (
        evidence.ball_visible
        and evidence.possession_evidence in ("H", "A")
    ):
        return ActivityStatus.INFERRED_IN_PLAY

    return ActivityStatus.UNKNOWN