import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import Counter

ball_states = Counter()
ball_owning_teams = Counter()

from kloppy import metrica

import games

import csv

from pathlib import Path

from possession_pipeline.game.activity_inference import (
    ActivityEvidence,
    infer_activity,
)
from possession_pipeline.game.game_state_machine import GameState
from possession_pipeline.decision.final_decision import make_final_decision

from possession_pipeline.tracking.tracking_adapter import (
    adapt_kloppy_frame,
)
from possession_pipeline.features.geometry_features import (
    extract_geometry_features,
)
from possession_pipeline.evidence.evidence_generator import (
    generate_evidence,
)
from possession_pipeline.possession.state_machine import (
    TemporalStateMachine,
)
from possession_pipeline.game.smart_tagging_adapter import (
    extract_restart_candidates,
)
from possession_pipeline.game.restart_index import RestartIndex
from starter.load_smart_tagging import load
from possession_pipeline.game.stoppage_inference import (
    StoppageEvidence,
    infer_stoppage,
)


def main():
    
    paths = games.asset_paths(source="tactical")

    dataset = metrica.load_tracking_epts(
        meta_data=paths["atd_meta"],
        raw_data=paths["atd_raw"],
        limit=None,
    )

    events = load()

    candidates = extract_restart_candidates(events)

    restart_index = RestartIndex(candidates)

    print("Restart candidates:", len(candidates))
    print("Merged intervals:", len(restart_index.intervals))

    # La posesión no expira en el pipeline (max_missing_frames=None).
    machine = TemporalStateMachine(
        confirmation_frames=3,
    )

    evidence_counts = Counter()
    prediction_counts = Counter()
    final_counts = Counter()
    decision_sources = Counter()

    processed = 0

    output_path = Path(
        "evaluation/results/experimental_stoppage_submission.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["frame", "label"])

        for record in dataset.records:

            ball_state = getattr(record, "ball_state", None)
            owning_team = getattr(record, "ball_owning_team_id", None)

            ball_states[str(ball_state)] += 1
            ball_owning_teams[str(owning_team)] += 1

            frame = adapt_kloppy_frame(record)

            features = extract_geometry_features(frame)

            evidence = generate_evidence(features)

            possession_estimate = machine.update(evidence)

            activity_evidence = ActivityEvidence(
                ball_visible=frame.ball_position is not None,
                possession_evidence=evidence,
            )

            activity_status = infer_activity(activity_evidence)

            stoppage_evidence = StoppageEvidence(
                restart_candidate_present=restart_index.contains(frame.frame_id),
                ball_visible=frame.ball_position is not None,
                possession_evidence=evidence,
            )

            stoppage_status = infer_stoppage(stoppage_evidence)

            # No inventamos eventos confirmados, solo usamos los que nos da el dataset.
            game_state = GameState.UNKNOWN

            decision = make_final_decision(
                possession_estimate=possession_estimate,
                game_state=game_state,
                activity_status=activity_status,
                stoppage_status=stoppage_status,
            )

            final_prediction = decision.final_prediction

            writer.writerow([
                frame.frame_id,
                final_prediction if final_prediction is not None else "X",
            ])

            evidence_counts[evidence or "None"] += 1
            prediction_counts[possession_estimate or "None"] += 1
            final_counts[final_prediction or "X"] += 1
            decision_sources[decision.decision_source] += 1

            processed += 1
            if processed % 25000 == 0:
                print(f"Processed {processed} frames...")

    assert sum(evidence_counts.values()) == processed
    assert sum(prediction_counts.values()) == processed
    assert sum(final_counts.values()) == processed

    print(f"\nPROCESSED FRAMES: {processed}")

    print("\nEVIDENCE")
    print(dict(evidence_counts))

    print("\nPOSSESSION ESTIMATES")
    print(dict(prediction_counts))

    print("\nFINAL PREDICTIONS")
    print(dict(final_counts))

    print("\nDECISION SOURCES")
    print(dict(decision_sources))

    print("\nBALL STATES")
    print(dict(ball_states))

    print("\nBALL OWNING TEAMS")
    print(dict(ball_owning_teams))

    print("\nCSV GENERATED")
    print(output_path)


if __name__ == "__main__":
    main()
