from types import SimpleNamespace

import pytest

from possession_pipeline.tracking.frame_validator import (
    validate_frame_sequence,
)


def make_frames(ids):
    return [
        SimpleNamespace(frame_id=frame_id)
        for frame_id in ids
    ]


def test_contiguous_frames():

    frames = make_frames([0, 1, 2, 3, 4])

    assert validate_frame_sequence(frames) == 5


def test_missing_frame():

    frames = make_frames([0, 1, 3, 4])

    with pytest.raises(ValueError):
        validate_frame_sequence(frames)


def test_duplicate_frame():

    frames = make_frames([0, 1, 1, 2])

    with pytest.raises(ValueError):
        validate_frame_sequence(frames)


def test_custom_start():

    frames = make_frames([100, 101, 102])

    assert validate_frame_sequence(
        frames,
        expected_start=100,
    ) == 3