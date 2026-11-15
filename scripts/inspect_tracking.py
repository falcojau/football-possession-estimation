import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kloppy import metrica  # noqa: E402

import games  # noqa: E402

from possession_pipeline.features.geometry_features import (
    extract_geometry_features,
)
from possession_pipeline.tracking.tracking_adapter import (  # noqa: E402
    adapt_tracking_row,
)


paths = games.asset_paths(source="tactical")

dataset = metrica.load_tracking_epts(
    meta_data=paths["atd_meta"],
    raw_data=paths["atd_raw"],
    limit=12000,
)

frame_df = dataset.to_df()

print("Columns:")
print(frame_df.columns.tolist()[:20])

print("\nFirst frames:")

visible_frames = 0

for _, row in frame_df.iterrows():

    frame = adapt_tracking_row(row)

    if frame.ball_position is None:
        continue

    features = extract_geometry_features(frame)

    print(
        f"Frame {frame.frame_id} | "
        f"d_H: {features.d_H:.2f} | "
        f"d_A: {features.d_A:.2f} | "
        f"Margin: {features.distance_margin:.2f}"
    )

    visible_frames += 1

    if visible_frames == 5:
        break