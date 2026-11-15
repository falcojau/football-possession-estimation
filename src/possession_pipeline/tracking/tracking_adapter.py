import math

from dataclasses import dataclass

from collections.abc import Mapping

@dataclass(frozen=True)
class TrackingFrame:
    frame_id: int
    ball_position: tuple[float, float] | None   # Contiene coordenadas normalizadas
    home_players: dict[int, tuple[float, float]]
    away_players: dict[int, tuple[float, float]]

def valid_coordinate(value) -> bool:
    if isinstance(value, bool):
        return False
    
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    
    return math.isfinite(number)

def extract_position(
    row: Mapping,
    x_column: str,
    y_column: str,
) -> tuple[float, float] | None:

    x = row.get(x_column)

    y = row.get(y_column)

    if not valid_coordinate(x) or not valid_coordinate(y):
        return None
    
    return float(x), float(y)

def adapt_tracking_row(row: Mapping) -> TrackingFrame:
    
    atd_frame_id = int(row["frame_id"])

    if atd_frame_id < 1:
        raise ValueError("ATD frame_id must start at 1")
    frame_id = atd_frame_id - 1

    ball_position = extract_position(
        row,
        "ball_x",
        "ball_y",
    )

    home_players = {}

    away_players = {}

    for player_id in range(1, 47):
        position = extract_position(
            row,
            f"{player_id}_x",
            f"{player_id}_y",
        )

        if position is None:
            continue
        if player_id <= 24:
            home_players[player_id] = position
        else:
            away_players[player_id] = position

    return TrackingFrame(
        frame_id=frame_id,
        ball_position=ball_position,
        home_players=home_players,
        away_players=away_players,
    )

def adapt_kloppy_frame(record) -> TrackingFrame:

    atd_frame_id = int(record.frame_id)

    if atd_frame_id < 1:
        raise ValueError("ATD frame_id must start at 1")

    frame_id = atd_frame_id - 1

    ball = record.ball_coordinates

    if (
        ball is not None
        and valid_coordinate(ball.x)
        and valid_coordinate(ball.y)
    ):
        ball_position = (float(ball.x), float(ball.y))
    else:
        ball_position = None

    home_players = {}
    away_players = {}

    for player, coordinates in record.players_coordinates.items():

        if coordinates is None:
            continue

        if not (
            valid_coordinate(coordinates.x)
            and valid_coordinate(coordinates.y)
        ):
            continue

        player_id = int(str(player).replace("Track ", ""))

        position = (
            float(coordinates.x),
            float(coordinates.y),
        )

        if 1 <= player_id <= 24:
            home_players[player_id] = position

        elif 25 <= player_id <= 46:
            away_players[player_id] = position

    return TrackingFrame(
        frame_id=frame_id,
        ball_position=ball_position,
        home_players=home_players,
        away_players=away_players,
    )