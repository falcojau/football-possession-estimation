import math

from dataclasses import dataclass

from possession_pipeline.tracking.tracking_adapter import (
    TrackingFrame,
)


PITCH_LENGTH = 105
PITCH_WIDTH = 68


@dataclass(frozen=True)
class GeometryFeatures:
    frame_id: int
    d_H: float | None
    d_A: float | None
    distance_margin: float | None


def distance_in_metres(
    point_a: tuple[float, float],
    point_b: tuple[float, float],
) -> float:

    dx = (point_a[0] - point_b[0]) * PITCH_LENGTH
    dy = (point_a[1] - point_b[1]) * PITCH_WIDTH

    return math.hypot(dx, dy)


def nearest_player_distance(
    ball_position: tuple[float, float],
    players: dict[int, tuple[float, float]],
) -> float | None:

    if not players:
        return None

    return min(
        distance_in_metres(ball_position, position)
        for position in players.values()
    )


def extract_geometry_features(
    frame: TrackingFrame,
) -> GeometryFeatures:

    if frame.ball_position is None:
        return GeometryFeatures(
            frame_id=frame.frame_id,
            d_H=None,
            d_A=None,
            distance_margin=None,
        )

    d_H = nearest_player_distance(
        frame.ball_position,
        frame.home_players,
    )

    d_A = nearest_player_distance(
        frame.ball_position,
        frame.away_players,
    )

    distance_margin = (
        d_A - d_H
        if d_H is not None and d_A is not None
        else None
    )

    return GeometryFeatures(
        frame_id=frame.frame_id,
        d_H=d_H,
        d_A=d_A,
        distance_margin=distance_margin,
    )