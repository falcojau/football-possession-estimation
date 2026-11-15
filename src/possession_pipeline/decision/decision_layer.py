from possession_pipeline.game.game_state_machine import GameState


def combine_states(
    possession_state: str | None,
    game_state: GameState,
) -> str | None:

    if possession_state not in ("H", "A", None):
        raise ValueError(
            f"Invalid possession state: {possession_state}"
        )

    if not isinstance(game_state, GameState):
        raise ValueError(
            f"Invalid game state: {game_state}"
        )

    if game_state == GameState.STOPPED:
        return "D"

    if game_state == GameState.IN_PLAY:
        return possession_state

    return None