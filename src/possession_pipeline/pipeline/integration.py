from collections.abc import Sequence

from possession_pipeline.contracts.data_contracts import FrameResult
from possession_pipeline.game.game_state_machine import GameState
from possession_pipeline.possession.state_machine import run_temporal_state_machine
from possession_pipeline.observation.observation_tracker import track_observations
from possession_pipeline.decision.decision_layer import combine_states
from possession_pipeline.game.game_state_machine import (
    GameEvent,
    game_state_machine,
)
from possession_pipeline.game.geometry_adapter import (
    positions_to_candidates,
)


def run_pipeline(
    evidence_sequence: Sequence[str | None],
    game_states: Sequence[GameState],
    confirmation_frames: int,
) -> list[FrameResult]: # Cada frame contiene la información correspondiente a un frame.

    if len(evidence_sequence) != len(game_states):
        raise ValueError(
            "Evidence and game states must have the same length"
        )

    predictions = run_temporal_state_machine(
        evidence_sequence,
        confirmation_frames=confirmation_frames,  # Example value, adjust as needed
        max_missing_frames=None,  # Possession does not expire in the pipeline
    )

    observations = track_observations(
        list(evidence_sequence),
        predictions,
    )

    if len(predictions) != len(evidence_sequence):
        raise ValueError("Invalid possession output length")

    if len(observations) != len(evidence_sequence):
        raise ValueError("Invalid observation output length")

    results = []

    for frame_id, (possession, observation, game_state) in enumerate(
        zip(predictions, observations, game_states)
    ):
        if not isinstance(game_state, GameState):
            raise ValueError(f"Invalid game state at frame {frame_id}")

        if observation["frame"] != frame_id:
            raise ValueError(
                f"Observation frame mismatch at frame {frame_id}"
            )

        if observation["last_known_state"] != possession:
            raise ValueError(
                f"Observation possession mismatch at frame {frame_id}"
            )

        final_prediction = combine_states(
            possession,
            game_state,
        )

        result = FrameResult(
            frame_id=frame_id,
            possession_estimate=possession,
            observation_status=observation["observation_status"],
            game_state=game_state,
            final_prediction=final_prediction,
        )

        results.append(result)

    return results


def run_pipeline_with_events(
    evidence_sequence: Sequence[str | None],
    game_events: Sequence[GameEvent | None],
    confirmation_frames: int,
) -> list[FrameResult]:

    if len(evidence_sequence) != len(game_events):
        raise ValueError(
            "Evidence and game events must have the same length"
        )

    events = list(game_events)

    # Validate event types before processing.
    for frame_id, event in enumerate(events):
        if event is not None and type(event) is not GameEvent:
            raise ValueError(
                f"Invalid game event at frame {frame_id}: {event!r}"
            )

    game_states = game_state_machine(events)

    if len(game_states) != len(evidence_sequence):
        raise ValueError("Invalid game state output length")

    return run_pipeline(
        evidence_sequence=evidence_sequence,
        game_states=game_states,
        confirmation_frames=confirmation_frames,
    )


def run_pipeline_with_geometry(
    evidence_sequence: Sequence[str | None],
    ball_positions: Sequence[tuple[float | None, float | None]],
    confirmation_frames: int,
) -> list[FrameResult]:

    if len(evidence_sequence) != len(ball_positions):
        raise ValueError(
            "Evidence and ball positions must have the same length"
        )

    game_events = positions_to_candidates(ball_positions)

    return run_pipeline_with_events(
        evidence_sequence=evidence_sequence,
        game_events=game_events,
        confirmation_frames=confirmation_frames,
    )