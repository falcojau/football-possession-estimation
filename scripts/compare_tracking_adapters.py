import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kloppy import metrica

import games

from possession_pipeline.tracking.tracking_adapter import (
    adapt_tracking_row,
    adapt_kloppy_frame,
)

def main():

    paths = games.asset_paths(source="tactical")

    dataset = metrica.load_tracking_epts(
        meta_data=paths["atd_meta"],
        raw_data=paths["atd_raw"],
        limit=4210,
    )

    df = dataset.to_df()

    checked = 0
    visible = 0

    for record, (_, row) in zip(
        dataset.records,
        df.iterrows(),
    ):

        native = adapt_kloppy_frame(record)

        dataframe = adapt_tracking_row(row)

        assert native == dataframe

        checked += 1

        if native.ball_position is not None:
            visible += 1

    print(f"Frames compared: {checked}")
    print(f"Frames with visible ball: {visible}")
    print("Native adapter matches DataFrame adapter.")

if __name__ == "__main__":
    main()