import pytest

from possession_pipeline.game.dead_ball_detector import detect_out_of_bounds_candidate


@pytest.mark.parametrize(
    "ball_x, ball_y, expected",
    [
        (0.5, 0.5, False),
        (0.0, 0.5, False),
        (1.0, 0.5, False),
        (1.05, 0.5, True),
        (-0.05, 0.5, True),
        (0.5, 1.10, True),
        (0.5, -0.10, True),
        (None, 0.5, False),
        (float("nan"), 0.5, False),
    ],
)
def test_out_of_bounds_candidate(
    ball_x,
    ball_y,
    expected,
):
    result = detect_out_of_bounds_candidate(
        ball_x,
        ball_y,
    )

    assert result == expected