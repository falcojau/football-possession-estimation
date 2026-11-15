import pytest

from possession_pipeline.decision.decision_layer import combine_states
from possession_pipeline.game.game_state_machine import GameState


@pytest.mark.parametrize(
    "possession, game_state, expected",
    [
        ("H", GameState.IN_PLAY, "H"),
        ("A", GameState.IN_PLAY, "A"),
        ("H", GameState.STOPPED, "D"),
        ("A", GameState.STOPPED, "D"),
        (None, GameState.STOPPED, "D"),
        ("H", GameState.UNKNOWN, None),
        ("A", GameState.UNKNOWN, None),
        ("H", GameState.POSSIBLE_STOPPAGE, None),
        ("A", GameState.POSSIBLE_STOPPAGE, None),
        (None, GameState.IN_PLAY, None),
    ],
)
def test_combine_states(
    possession,
    game_state,
    expected,
):
    assert combine_states(
        possession,
        game_state,
    ) == expected


def test_invalid_possession():

    with pytest.raises(ValueError):
        combine_states(
            "X",
            GameState.IN_PLAY,
        )


def test_invalid_game_state():

    with pytest.raises(ValueError):
        combine_states(
            "H",
            "STOPPED",
        )