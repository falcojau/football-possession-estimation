import pytest

from possession_pipeline.tracking.tracking_adapter import (
    TrackingFrame,
)

from possession_pipeline.features.geometry_features import (
    distance_in_metres,
    extract_geometry_features,
)


def test_distance_in_metres():

    distance = distance_in_metres(
        (0.0, 0.0),
        (1.0, 0.0),
    )

    assert distance == pytest.approx(105.0)


def test_home_player_closer():

    frame = TrackingFrame(
        frame_id=0,
        ball_position=(0.5, 0.5),
        home_players={
            1: (0.51, 0.5),
        },
        away_players={
            25: (0.7, 0.5),
        },
    )

    features = extract_geometry_features(frame)

    assert features.d_H < features.d_A
    assert features.distance_margin > 0


def test_missing_ball():

    frame = TrackingFrame(
        frame_id=0,
        ball_position=None,
        home_players={},
        away_players={},
    )

    features = extract_geometry_features(frame)

    assert features.d_H is None
    assert features.d_A is None
    assert features.distance_margin is None


def test_missing_away_players():

    frame = TrackingFrame(
        frame_id=0,
        ball_position=(0.5, 0.5),
        home_players={
            1: (0.51, 0.5),
        },
        away_players={},
    )

    features = extract_geometry_features(frame)

    assert features.d_H is not None
    assert features.d_A is None
    assert features.distance_margin is None