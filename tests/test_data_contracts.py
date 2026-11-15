import pytest

from dataclasses import FrozenInstanceError

from possession_pipeline.contracts.data_contracts import FrameResult
from possession_pipeline.game.game_state_machine import GameState


def make_valid_frame():
    return FrameResult(
        frame_id=0,
        possession_estimate="H",
        observation_status="VISIBLE",
        game_state=GameState.IN_PLAY,
        final_prediction="H",
    )


def test_valid_frame():
    result = make_valid_frame()

    assert result.frame_id == 0
    assert result.possession_estimate == "H"
    assert result.final_prediction == "H"


def test_negative_frame_id():
    with pytest.raises(ValueError):
        FrameResult(
            frame_id=-1,
            possession_estimate="H",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="H",
        )


def test_invalid_possession():
    with pytest.raises(ValueError):
        FrameResult(
            frame_id=0,
            possession_estimate="Barcelona",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="H",
        )


def test_invalid_observation_status():
    with pytest.raises(ValueError):
        FrameResult(
            frame_id=0,
            possession_estimate="H",
            observation_status="UNKNOWN",
            game_state=GameState.IN_PLAY,
            final_prediction="H",
        )


def test_invalid_game_state():
    with pytest.raises(ValueError):
        FrameResult(
            frame_id=0,
            possession_estimate="H",
            observation_status="VISIBLE",
            game_state="IN_PLAY",
            final_prediction="H",
        )


def test_invalid_final_prediction():
    with pytest.raises(ValueError):
        FrameResult(
            frame_id=0,
            possession_estimate="H",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="Barcelona",
        )


def test_frame_is_immutable():
    result = make_valid_frame()

    with pytest.raises(FrozenInstanceError):
        result.final_prediction = "A"


def test_unknown_game_state_with_possession():
    result = FrameResult(
        frame_id=0,
        possession_estimate="A",
        observation_status="MISSING",
        game_state=GameState.UNKNOWN,
        final_prediction=None,
    )

    assert result.possession_estimate == "A"
    assert result.game_state == GameState.UNKNOWN
    assert result.final_prediction is None