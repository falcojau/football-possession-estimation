import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kloppy import metrica

import games


def main():

    paths = games.asset_paths(source="tactical")

    dataset = metrica.load_tracking_epts(
        meta_data=paths["atd_meta"],
        raw_data=paths["atd_raw"],
        limit=12000,
    )

    df = dataset.to_df()

    print("\nBALL STATE VALUES:")
    print(
        df["ball_state"].value_counts(
            dropna=False
        )
    )

    print("\nBALL OWNING TEAM VALUES:")
    print(
        df["ball_owning_team_id"].value_counts(
            dropna=False
        )
    )

    print("\nBALL STATE VS BALL VISIBILITY:")

    df["ball_visible"] = (
        df["ball_x"].notna()
        & df["ball_y"].notna()
    )

    print(
        df.groupby(
            ["ball_state", "ball_visible"],
            dropna=False,
        ).size()
    )


if __name__ == "__main__":
    main()