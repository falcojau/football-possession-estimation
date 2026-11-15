from collections.abc import Sequence

from possession_pipeline.game.dead_ball_detector import (
    detect_out_of_bounds_candidate,
)

from possession_pipeline.game.game_state_machine import GameEvent

# Transforma candidatos en eventos

def positions_to_candidates(
    ball_positions: Sequence[tuple[float | None, float | None]],
) -> list[GameEvent | None]:

    events = []

    for position in ball_positions:

        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError(
                f"Invalid ball position: {position!r}"
            )

        ball_x, ball_y = position

        is_candidate = detect_out_of_bounds_candidate(
            ball_x,
            ball_y,
        )

        if is_candidate:
            events.append(GameEvent.STOPPAGE_CANDIDATE)
        else:
            events.append(None)

    return events