import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kloppy import metrica

import games

from possession_pipeline.tracking.tracking_adapter import (
    adapt_tracking_row,
)
from possession_pipeline.features.geometry_features import (
    extract_geometry_features,
)
from possession_pipeline.evidence.evidence_generator import (
    generate_evidence,
)
from possession_pipeline.possession.state_machine import (
    temporal_state_machine,
)


def main():

    paths = games.asset_paths(source="tactical")

    dataset = metrica.load_tracking_epts(
        meta_data=paths["atd_meta"],
        raw_data=paths["atd_raw"],
        limit=12000,
    )

    frame_df = dataset.to_df()

    evidence_sequence = []
    frame_ids = []

    for _, row in frame_df.iterrows():

        frame = adapt_tracking_row(row)

        features = extract_geometry_features(frame)

        evidence = generate_evidence(features)

        frame_ids.append(frame.frame_id)
        evidence_sequence.append(evidence)

    # Synthetic integration value only.
    # NOT a competition parameter.
    predictions = temporal_state_machine(
        evidence_sequence,
        confirmation_frames=3,
    )

    print("First 10 frames with available evidence:")

    count = 0

    for frame_id, evidence, prediction in zip(
        frame_ids,
        evidence_sequence,
        predictions,
    ):

        if evidence is None:
            continue

        print(
            f"Frame {frame_id} | "
            f"Evidence: {evidence} | "
            f"Possession Estimate: {prediction}"
        )

        count += 1

        if count == 10:
            break


if __name__ == "__main__":
    main()