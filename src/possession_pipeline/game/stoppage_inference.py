from dataclasses import dataclass
from enum import Enum


class StoppageStatus(Enum):
    INFERRED_STOPPAGE = "INFERRED_STOPPAGE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class StoppageEvidence:
    restart_candidate_present: bool
    ball_visible: bool
    possession_evidence: str | None


def infer_stoppage(
    evidence: StoppageEvidence,
) -> StoppageStatus:

    if evidence.possession_evidence not in ("H", "A", None):
        raise ValueError("Invalid possession evidence")

    if (
        evidence.restart_candidate_present
        and not evidence.ball_visible
        and evidence.possession_evidence is None
    ):
        return StoppageStatus.INFERRED_STOPPAGE

    return StoppageStatus.UNKNOWN