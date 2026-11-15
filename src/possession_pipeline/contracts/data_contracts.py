from dataclasses import dataclass
from typing import Literal

from possession_pipeline.game.game_state_machine import GameState


PossessionState = Literal["H", "A"]
PossessionEstimate = PossessionState | None

ObservationStatus = Literal["VISIBLE", "MISSING"]

FinalPrediction = Literal["H", "A", "D"] | None


@dataclass(frozen=True)
class FrameResult:
    frame_id: int
    possession_estimate: PossessionEstimate # Estimación de posesión: H/A/None
    observation_status: ObservationStatus   # Disponibilidad de observación: VISIBLE/MISSING
    game_state: GameState
    final_prediction: FinalPrediction  # Resultado de Decision Layer: H/A/D/None

    def __post_init__(self):
        if type(self.frame_id) is not int or self.frame_id < 0:
            raise ValueError("frame_id must be a non-negative integer")

        if self.possession_estimate not in ("H", "A", None):
            raise ValueError("Invalid possession_estimate")

        if self.observation_status not in ("VISIBLE", "MISSING"):
            raise ValueError("Invalid observation_status")

        if not isinstance(self.game_state, GameState):
            raise ValueError("Invalid game_state")

        if self.final_prediction not in ("H", "A", "D", None):
            raise ValueError("Invalid final_prediction")