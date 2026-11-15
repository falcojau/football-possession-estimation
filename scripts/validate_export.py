from pathlib import Path

from possession_pipeline.contracts.data_contracts import FrameResult
from possession_pipeline.game.game_state_machine import GameState

from possession_pipeline.export.submission_exporter import (
    export_submission,
    EXPECTED_FRAMES,
)


def main():

    results = []

    for frame_id in range(EXPECTED_FRAMES):

        result = FrameResult(
            frame_id=frame_id,
            possession_estimate=None,
            observation_status="MISSING",
            game_state=GameState.UNKNOWN,
            final_prediction=None,
        )

        results.append(result)

    output_path = Path("outputs/synthetic_validation.csv")

    export_submission(
        results=results,
        output_path=output_path,
    )

    print(f"Generated: {output_path}")
    print(f"Frames: {len(results)}")


if __name__ == "__main__":
    main()