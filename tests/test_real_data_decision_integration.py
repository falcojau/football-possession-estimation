from possession_pipeline.tracking.tracking_adapter import (
    TrackingFrame,
)

from possession_pipeline.features.geometry_features import (
    extract_geometry_features,
)

from possession_pipeline.evidence.evidence_generator import (
    generate_evidence,
)

from possession_pipeline.possession.state_machine import (
    run_temporal_state_machine,
)

from possession_pipeline.game.game_state_machine import (
    GameState,
)

from possession_pipeline.decision.decision_layer import (
    combine_states,
)


def test_unknown_game_state_does_not_confirm_possession():

    frames = [
        TrackingFrame(
            frame_id=i,
            ball_position=(0.5, 0.5),
            home_players={1: (0.51, 0.5)},
            away_players={25: (0.8, 0.5)},
        )
        for i in range(5)
    ]

    evidence_sequence = [
        generate_evidence(
            extract_geometry_features(frame)
        )
        for frame in frames
    ]

    possession_estimates = run_temporal_state_machine(
        evidence_sequence,
        confirmation_frames=3,
        max_missing_frames=2,
    )

    assert possession_estimates[-1] == "H"

    final_predictions = [
        combine_states(
            possession_state=estimate,
            game_state=GameState.UNKNOWN,
        )
        for estimate in possession_estimates
    ]

    assert all(
        prediction is None
        for prediction in final_predictions
    )

