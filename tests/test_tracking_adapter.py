import math

import pytest

from possession_pipeline.tracking.tracking_adapter import (
    adapt_tracking_row,
)


def test_tracking_row():

    row = {
        "frame_id": 15000,
        "ball_x": 0.5,
        "ball_y": 0.4,
        "1_x": 0.48,
        "1_y": 0.42,
        "25_x": 0.7,
        "25_y": 0.6,
    }

    frame = adapt_tracking_row(row)

    assert frame.frame_id == 14999
    assert frame.ball_position == (0.5, 0.4)
    assert frame.home_players[1] == (0.48, 0.42)
    assert frame.away_players[25] == (0.7, 0.6)


def test_missing_ball():

    row = {
        "frame_id": 1,
        "ball_x": math.nan,
        "ball_y": math.nan,
    }

    frame = adapt_tracking_row(row)

    assert frame.frame_id == 0
    assert frame.ball_position is None


def test_missing_player():

    row = {
        "frame_id": 1,
        "ball_x": 0.5,
        "ball_y": 0.5,
        "1_x": math.nan,
        "1_y": math.nan,
    }

    frame = adapt_tracking_row(row)

    assert 1 not in frame.home_players

def test_invalid_frame_id():

    row = {
        "frame_id": 0,
        "ball_x": 0.5,
        "ball_y": 0.5,
    }

    with pytest.raises(ValueError):
        adapt_tracking_row(row)

from types import SimpleNamespace

from possession_pipeline.tracking.tracking_adapter import (
    adapt_kloppy_frame,
)


def test_native_adapter():

    record = SimpleNamespace(
        frame_id=10,
        ball_coordinates=SimpleNamespace(
            x=0.5,
            y=0.4,
        ),
        players_coordinates={
            "Track 1": SimpleNamespace(
                x=0.48,
                y=0.42,
            ),
            "Track 25": SimpleNamespace(
                x=0.7,
                y=0.6,
            ),
        },
    )

    frame = adapt_kloppy_frame(record)

    assert frame.frame_id == 9
    assert frame.ball_position == (0.5, 0.4)
    assert frame.home_players[1] == (0.48, 0.42)
    assert frame.away_players[25] == (0.7, 0.6)