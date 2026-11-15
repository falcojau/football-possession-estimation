from possession_pipeline.game.smart_tagging_adapter import (
    extract_restart_candidates,
)

from possession_pipeline.game.game_state_machine import (
    GameState,
)

from possession_pipeline.decision.decision_layer import (
    combine_states,
)


def test_restart_candidate_does_not_confirm_game_state():

    events = [
        {
            "code": "SET PIECES",
            "start_frame": 100,
            "end_frame": 200,
            "tags": {
                "Type": "Corner Kick",
                "Team": "Barcelona",
            },
        }
    ]

    candidates = extract_restart_candidates(events)

    assert len(candidates) == 1

    # A candidate alone does not justify changing UNKNOWN.
    game_state = GameState.UNKNOWN

    final_prediction = combine_states(
        possession_state="H",
        game_state=game_state,
    )

    assert final_prediction is None