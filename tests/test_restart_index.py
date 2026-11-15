from possession_pipeline.game.restart_index import RestartIndex
from possession_pipeline.game.smart_tagging_adapter import RestartCandidate


def test_frame_inside_interval():

    index = RestartIndex([
        RestartCandidate(
            start_frame=100,
            end_frame=200,
            restart_type="Corner Kick",
            team="H",
        )
    ])

    assert index.contains(150) is True


def test_frame_outside_interval():

    index = RestartIndex([
        RestartCandidate(
            start_frame=100,
            end_frame=200,
            restart_type="Corner Kick",
            team="H",
        )
    ])

    assert index.contains(250) is False


def test_frame_before_first_interval():

    index = RestartIndex([
        RestartCandidate(
            start_frame=100,
            end_frame=200,
            restart_type="Corner Kick",
            team="H",
        )
    ])

    assert index.contains(50) is False


def test_empty_candidates():
    index = RestartIndex([])
    assert index.contains(150) is False


def test_overlapping_intervals():

    index = RestartIndex([
        RestartCandidate(
            start_frame=100,
            end_frame=200,
            restart_type="Corner Kick",
            team="H",
        ),
        RestartCandidate(
            start_frame=150,
            end_frame=250,
            restart_type="Free Kick",
            team="A",
        ),
    ])

    assert index.contains(175) is True
    assert index.contains(225) is True
    assert index.contains(251) is False


def test_nested_intervals():

    index = RestartIndex([
        RestartCandidate(
            start_frame=100,
            end_frame=300,
            restart_type="Corner Kick",
            team="H",
        ),
        RestartCandidate(
            start_frame=150,
            end_frame=200,
            restart_type="Free Kick",
            team="A",
        ),
    ])

    assert index.contains(250) is True