import math

# Evalúa geometría

def detect_out_of_bounds_candidate(
    ball_x: float | None,
    ball_y: float | None,
) -> bool:

    if ball_x is None or ball_y is None:
        return False

    if math.isnan(ball_x) or math.isnan(ball_y):
        return False

    return (
        ball_x < 0
        or ball_x > 1
        or ball_y < 0
        or ball_y > 1
    )


