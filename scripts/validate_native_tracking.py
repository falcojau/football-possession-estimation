import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kloppy import metrica

import games

from possession_pipeline.tracking.tracking_adapter import (
    adapt_kloppy_frame,
)

from possession_pipeline.tracking.frame_validator import (
    validate_frame_sequence,
)


def main():

    paths = games.asset_paths(source="tactical")

    dataset = metrica.load_tracking_epts(
        meta_data=paths["atd_meta"],
        raw_data=paths["atd_raw"],
        limit=12000,
    )

    frames = (
        adapt_kloppy_frame(record)
        for record in dataset.records
    )

    total = validate_frame_sequence(frames)

    assert total == 12000

    print(f"Validated frames: {total}")
    print("Frame sequence is contiguous.")
    print("Native tracking validation passed.")


if __name__ == "__main__":
    main()