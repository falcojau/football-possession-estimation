import csv

from pathlib import Path
from collections.abc import Sequence

from possession_pipeline.contracts.data_contracts import FrameResult

VALID_LABELS = {"H", "A", "D", "X"}

EXPECTED_FRAMES = 199_319     # El número de frames es correcto.


def export_label(prediction: str | None) -> str:

    if prediction is None:
        return "X"

    if prediction not in {"H", "A", "D"}:
        raise ValueError(
            f"Invalid prediction: {prediction}"
        )

    return prediction


def export_submission(
    results: Sequence[FrameResult],      # Todos los elementos son FrameResult.
    output_path: str | Path,
    expected_frames: int = EXPECTED_FRAMES,
) -> Path:

    if len(results) != expected_frames:
        raise ValueError(
            f"Expected {expected_frames} frames, "
            f"received {len(results)}"
        )

    output_path = Path(output_path)

    # Validate before writing anything.
    rows = []

    for expected_frame, result in enumerate(results):

        if not isinstance(result, FrameResult):
            raise TypeError(
                f"Expected FrameResult at index {expected_frame}"
            )

        if result.frame_id != expected_frame:
            raise ValueError(
                f"Frame mismatch: expected {expected_frame}, "
                f"received {result.frame_id}"
            )

        label = export_label(result.final_prediction)

        rows.append((result.frame_id, label))

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["frame", "label"])

        writer.writerows(rows)

    return output_path