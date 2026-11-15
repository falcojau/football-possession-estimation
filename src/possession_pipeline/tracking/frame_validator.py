def validate_frame_sequence(frames, expected_start=0):
    """
    Validate that frame IDs are contiguous and ordered.
    Returns the number of validated frames.
    """

    expected_frame = expected_start
    count = 0

    for frame in frames:

        if frame.frame_id != expected_frame:
            raise ValueError(
                f"Expected frame {expected_frame}, "
                f"received {frame.frame_id}"
            )

        expected_frame += 1
        count += 1

    return count