import csv

import pytest

from possession_pipeline.export.submission_exporter import (
    export_label,
    export_submission,
)

from possession_pipeline.contracts.data_contracts import (
    FrameResult,
)

from possession_pipeline.game.game_state_machine import (
    GameState,
)


def test_export_label():

    assert export_label("H") == "H"
    assert export_label("A") == "A"
    assert export_label("D") == "D"
    assert export_label(None) == "X"

    with pytest.raises(ValueError):
        export_label("Barcelona")

def test_export_submission(tmp_path):

    results = [
        FrameResult(
            frame_id=0,
            possession_estimate="H",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="H",
        ),
        FrameResult(
            frame_id=1,
            possession_estimate="H",
            observation_status="MISSING",
            game_state=GameState.UNKNOWN,
            final_prediction=None,
        ),
        FrameResult(
            frame_id=2,
            possession_estimate="A",
            observation_status="VISIBLE",
            game_state=GameState.STOPPED,
            final_prediction="D",
        ),
    ]

    output = tmp_path / "synthetic_submission.csv"

    export_submission(
        results=results,
        output_path=output,
        expected_frames=3,
    )

    with output.open(
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(csv.reader(file))

    assert rows == [
        ["frame", "label"],
        ["0", "H"],
        ["1", "X"],
        ["2", "D"],
    ]

def test_export_rejects_wrong_length(tmp_path):

    output = tmp_path / "invalid.csv"

    with pytest.raises(ValueError):
        export_submission(
            results=[],
            output_path=output,
            expected_frames=3,
        )

    assert not output.exists()

def test_export_rejects_wrong_frame_order(tmp_path):

    results = [
        FrameResult(
            frame_id=0,
            possession_estimate="H",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="H",
        ),
        FrameResult(
            frame_id=2,
            possession_estimate="A",
            observation_status="VISIBLE",
            game_state=GameState.IN_PLAY,
            final_prediction="A",
        ),
    ]

    output = tmp_path / "invalid_order.csv"

    with pytest.raises(ValueError):
        export_submission(
            results=results,
            output_path=output,
            expected_frames=2,
        )

    assert not output.exists()

