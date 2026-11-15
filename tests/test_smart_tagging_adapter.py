from possession_pipeline.game.smart_tagging_adapter import (
    extract_restart_candidates,
)


def test_extract_corner_kick():

    events = [
        {
            "code": "SET PIECES",
            "start_frame": 100,
            "end_frame": 200,
            "tags": {
                "Type": "Corner Kick",
                "Team": "Barcelona",
            },
        }
    ]

    candidates = extract_restart_candidates(events)

    assert len(candidates) == 1
    assert candidates[0].restart_type == "Corner Kick"
    assert candidates[0].team == "H"


def test_ignore_non_set_piece():

    events = [
        {
            "code": "BUILD UP",
            "start_frame": 100,
            "end_frame": 200,
            "tags": {
                "Team": "Barcelona",
            },
        }
    ]

    candidates = extract_restart_candidates(events)

    assert candidates == []


def test_unknown_team():

    events = [
        {
            "code": "SET PIECES",
            "start_frame": 100,
            "end_frame": 200,
            "tags": {
                "Type": "Kick Off (Start)",
                "Team": "N/A",
            },
        }
    ]

    candidates = extract_restart_candidates(events)

    assert candidates[0].team is None