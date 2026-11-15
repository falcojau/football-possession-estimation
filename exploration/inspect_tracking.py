import os
import sys

import pandas as pd
from kloppy import metrica

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from games import asset_paths  # noqa: E402

PITCH_WIDTH_M = 105.3
PITCH_HEIGHT_M = 68.0


def distance_to_ball(x_player, y_player, x_ball, y_ball):
    """Distance in meters between a 
    player and the ball, correcting for the non-square pitch."""
    dx = (x_player - x_ball) * PITCH_WIDTH_M
    dy = (y_player - y_ball) * PITCH_HEIGHT_M
    return (dx**2 + dy**2) ** 0.5


def nearest_to_ball(slots, frame):
    """Among the given slots visible in frame, return (slot, distance) of the closest to the ball."""

    x_ball = frame["ball_x"]
    y_ball = frame["ball_y"]

    if pd.isna(x_ball) or pd.isna(y_ball):
        return None, None

    nearest_slot = None
    nearest_distance = None
    for slot in slots:
        x = frame[f"{slot}_x"]
        y = frame[f"{slot}_y"]

        if pd.isna(x) or pd.isna(y):
            continue

        distance = distance_to_ball(x, y, x_ball, y_ball)
        if nearest_distance is None or distance < nearest_distance:
            nearest_slot = slot
            nearest_distance = distance

    return nearest_slot, nearest_distance


def build_distance_features(df):
    rows = []

    for _, frame in df.iterrows():
        frame_id = int(frame["frame_id"])

        _, d_h = nearest_to_ball(
            barcelona_slots,
            frame,
        )

        _, d_a = nearest_to_ball(
            athletic_slots,
            frame,
        )

        # No ball observation -> no distance evidence
        if d_h is None or d_a is None:
            rows.append({
                "frame_id": frame_id,
                "d_H": None,
                "d_A": None,
                "distance_margin": None,
                "min_distance": None,
            })
            continue

        rows.append({
            "frame_id": frame_id,
            "d_H": d_h,
            "d_A": d_a,
            "distance_margin": d_a - d_h,
            "min_distance": min(d_h, d_a),
        })

    return pd.DataFrame(rows)

def build_ball_movement_features(df):
    features = df[
        ["frame_id", "ball_x", "ball_y"]
    ].copy()

    # Movement between consecutive frames in metres
    dx = features["ball_x"].diff() * PITCH_WIDTH_M
    dy = features["ball_y"].diff() * PITCH_HEIGHT_M

    distance = (dx**2 + dy**2) ** 0.5

    # 25 FPS -> metres/frame * 25 = metres/second
    features["ball_speed"] = distance * 25

    # Change in speed between consecutive frames.
    # m/s per frame -> *25 = m/s²
    features["ball_acceleration"] = (
        features["ball_speed"].diff() * 25
    )

    return features[
        [
            "frame_id",
            "ball_speed",
            "ball_acceleration",
        ]
    ]


paths = asset_paths()

dataset = metrica.load_tracking_epts(
    meta_data=paths["atd_meta"],
    raw_data=paths["atd_raw"],
)

df = dataset.to_df()

print("\nTEAMS")
for team in dataset.metadata.teams:
    print(team)

print("\nPLAYERS")
barcelona_slots = []
athletic_slots = []
for team in dataset.metadata.teams:
    for player in team.players:
        slot = player.player_id

        if str(team) == "Barcelona":
            barcelona_slots.append(slot)
        elif str(team) == "Atletic Club":
            athletic_slots.append(slot)

print("Barcelona:", barcelona_slots)
print("Athletic:", athletic_slots)

def add_control_evidence(features):
    features = features.copy()

    features["proximity_evidence"] = (
        features["distance_margin"]
    )

    return features

def add_evidence_team(features):
    features = features.copy()

    features["evidence_team"] = None

    features.loc[
        features["proximity_evidence"] > 0,
        "evidence_team"
    ] = "H"

    features.loc[
        features["proximity_evidence"] < 0,
        "evidence_team"
    ] = "A"

    return features

def add_distance_dynamics(features):
    features = features.copy()

    features["d_H_change"] = features["d_H"].diff()
    features["d_A_change"] = features["d_A"].diff()
    features["min_distance_change"] = (
        features["min_distance"].diff()
    )

    return features

first_half_df = df[
    (df["frame_id"] >= 11185)
    & (df["frame_id"] <= 90651)
].copy()

distance_features = build_distance_features(first_half_df)
ball_features = build_ball_movement_features(first_half_df)

features = distance_features.merge(
    ball_features,
    on="frame_id",
    how="left",
)

features = add_distance_dynamics(features)
features = add_control_evidence(features)
features = add_evidence_team(features)

print("\nFEATURES (first half)")
print("Shape:", features.shape)
print(
    "Frame range:",
    features["frame_id"].min(),
    "->",
    features["frame_id"].max(),
)
print("Unique frames:", features["frame_id"].nunique())
print("Expected:", len(first_half_df))
print()
print(features.columns.tolist())


gt_path = "evaluation/gt/BAR-ATH_possession_gt_public.csv"

gt = pd.read_csv(gt_path)
print("Shape:", gt.shape)
print()
print("Columns:", gt.columns.tolist())
print()
print(gt.head(10))
print()
print(gt.tail(10))
print()
print("Index:", gt.index.min(), "->", gt.index.max())

gt_graded = gt[
    gt["label"].isin(["H", "A", "D"])
].copy()

gt_graded["previous_label"] = gt_graded["label"].shift(1)

gt_transitions = gt_graded[
    gt_graded["label"] != gt_graded["previous_label"]
].copy()

# La primera fila graded no cuenta como transición
gt_transitions = gt_transitions.iloc[1:]

print(
    gt_transitions[
        ["frame", "previous_label", "label"]
    ].to_string(index=False)
)

print()
print("GT transitions:", len(gt_transitions))


print("\nNon-null values per column:")
print(gt.notna().sum())

print("\nUnique values:")
for col in gt.columns:
    print(col, gt[col].dropna().unique()[:20])

ha_transitions = gt_transitions[
    gt_transitions["previous_label"].isin(["H", "A"])
    & gt_transitions["label"].isin(["H", "A"])
].copy()

# Convertimos GT/video frame 0-based
# a tracking frame_id 1-based
ha_transitions["tracking_frame_id"] = (
    ha_transitions["frame"] + 1
)

print(
    ha_transitions[
        [
            "frame",
            "tracking_frame_id",
            "previous_label",
            "label",
        ]
    ].to_string(index=False)
)

print()
print(
    "H/A transitions:",
    len(ha_transitions)
)

gt_ha = ha_transitions.copy()

gt_ha["gt_tracking_frame"] = (
    gt_ha["frame"] + 1
)

gt_ha["direction"] = (
    gt_ha["previous_label"]
    + "→"
    + gt_ha["label"]
)

print("TEMPORAL STATE MACHINE v4")

def temporal_state_machine_v4(
    features,
    confirmation_frames=10,
    max_min_ball_speed=5,
    max_min_distance=None,
):

    current_state = None
    candidate_state = None
    candidate_count = 0

    candidate_min_ball_speed = float("inf")
    candidate_min_distance = float("inf")

    predictions = []

    for _, row in features.iterrows():

        evidence = row["evidence_team"]
        ball_speed = row["ball_speed"]
        min_distance = row["min_distance"]

        if evidence not in ["H", "A"]:
            predictions.append(current_state)
            continue

        if current_state is None:

            current_state = evidence
            candidate_state = None
            candidate_count = 0
            candidate_min_ball_speed = float("inf")
            candidate_min_distance = float("inf")

        elif evidence == current_state:

            candidate_state = None
            candidate_count = 0
            candidate_min_ball_speed = float("inf")
            candidate_min_distance = float("inf")

        else:

            if candidate_state != evidence:

                candidate_state = evidence
                candidate_count = 1
                candidate_min_ball_speed = float("inf")
                candidate_min_distance = float("inf")

            else:
                candidate_count += 1

            if pd.notna(ball_speed):
                candidate_min_ball_speed = min(
                    candidate_min_ball_speed,
                    ball_speed,
                )

            if pd.notna(min_distance):
                candidate_min_distance = min(
                    candidate_min_distance,
                    min_distance,
                )

            temporal_ok = (
                candidate_count >= confirmation_frames
            )

            speed_ok = (
                max_min_ball_speed is None
                or candidate_min_ball_speed <= max_min_ball_speed
            )

            distance_ok = (
                max_min_distance is None
                or candidate_min_distance <= max_min_distance
            )

            if temporal_ok and speed_ok and distance_ok:

                current_state = candidate_state

                candidate_state = None
                candidate_count = 0
                candidate_min_ball_speed = float("inf")
                candidate_min_distance = float("inf")

        predictions.append(current_state)

    return predictions

results_v3 = []

for distance_threshold in [None, 1, 2, 3]:

    test = features.copy()

    test["prediction"] = temporal_state_machine_v4(
        test,
        confirmation_frames=10,
        max_min_ball_speed=5,
        max_min_distance=distance_threshold,
    )

    evaluated = gt[
        gt["label"].isin(["H", "A"])
    ].copy()

    evaluated["frame_id"] = evaluated["frame"] + 1

    evaluated = evaluated.merge(
        test[["frame_id", "prediction"]],
        on="frame_id",
        how="left",
    )

    accuracy = (
        evaluated["prediction"]
        == evaluated["label"]
    ).mean() * 100

    transitions = (
        evaluated["prediction"]
        != evaluated["prediction"].shift()
    ).sum()

    results_v3.append({
        "distance_threshold": (
            "None"
            if distance_threshold is None
            else distance_threshold
        ),
        "accuracy": accuracy,
        "predicted_transitions": transitions,
    })


results_v3 = pd.DataFrame(results_v3)

print(
    results_v3.round(2).to_string(index=False)
)

def evaluate_transition_latency_v3(
    features,
    gt_ha,
    confirmation_frames=10,
    speed_threshold=5,
    distance_threshold=1,
    search_window=50,
):

    test = features.copy()

    test["prediction"] = temporal_state_machine_v4(
        test,
        confirmation_frames=confirmation_frames,
        max_min_ball_speed=speed_threshold,
        max_min_distance=distance_threshold,
    )

    test["previous_prediction"] = test["prediction"].shift(1)

    predicted_transitions = test[
        test["prediction"].isin(["H", "A"])
        & test["previous_prediction"].isin(["H", "A"])
        & (test["prediction"] != test["previous_prediction"])
    ].copy()

    predicted_transitions["direction"] = (
        predicted_transitions["previous_prediction"]
        + "→"
        + predicted_transitions["prediction"]
    )

    rows = []

    for _, gt_row in gt_ha.iterrows():

        gt_frame = int(gt_row["gt_tracking_frame"])
        direction = gt_row["direction"]

        candidates = predicted_transitions[
            (predicted_transitions["direction"] == direction)
            & predicted_transitions["frame_id"].between(
                gt_frame - search_window,
                gt_frame + search_window,
            )
        ].copy()

        if candidates.empty:
            rows.append({
                "gt_frame": gt_frame,
                "direction": direction,
                "predicted_frame": None,
                "latency_frames": None,
            })
            continue

        candidates["abs_distance"] = (
            candidates["frame_id"] - gt_frame
        ).abs()

        best = candidates.sort_values(
            "abs_distance"
        ).iloc[0]

        predicted_frame = int(best["frame_id"])

        rows.append({
            "gt_frame": gt_frame,
            "direction": direction,
            "predicted_frame": predicted_frame,
            "latency_frames": predicted_frame - gt_frame,
        })

    return pd.DataFrame(rows)

latency_v3 = evaluate_transition_latency_v3(
    features,
    gt_ha,
)

detected = latency_v3[
    latency_v3["latency_frames"].notna()
]

print(latency_v3.to_string(index=False))

print(
    "\nDetected:",
    len(detected),
    "/",
    len(latency_v3),
)

print(
    "Mean abs latency:",
    round(detected["latency_frames"].abs().mean(), 2),
    "frames",
)

print(
    "Median latency:",
    round(detected["latency_frames"].median(), 2),
    "frames",
)

state_machine = features.copy()

state_machine["prediction"] = temporal_state_machine_v4(
    state_machine,
    confirmation_frames=10,
    max_min_ball_speed=5,
)

print(
    state_machine["prediction"]
    .value_counts(dropna=False)
)

print(
    "Frames:",
    len(state_machine)
)

print(
    "Transitions:",
    (
        state_machine["prediction"]
        != state_machine["prediction"].shift()
    ).sum()
)

eval_ha = gt[
    gt["label"].isin(["H", "A"])
].copy()

eval_ha["frame_id"] = eval_ha["frame"] + 1

eval_ha = eval_ha.merge(
    state_machine[
        ["frame_id", "prediction"]
    ],
    on="frame_id",
    how="left",
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,   
)

eval_valid = eval_ha.dropna(subset=["prediction"])

print(
    f"Evaluated {len(eval_valid)}/{len(eval_ha)} graded H/A frames "
    f"({len(eval_ha) - len(eval_valid)} with no prediction yet)"
)

y_true = eval_valid["label"]
y_pred = eval_valid["prediction"]

print("H/A EVALUATION")
print("=" * 50)

print(
    "Accuracy:",
    round(
        accuracy_score(y_true, y_pred),
        4,
    )
)

precision, recall, f1, support = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=["H", "A"],
        zero_division=0,
    )
)

for team, p, r, f, s in zip(
    ["H", "A"],
    precision,
    recall,
    f1,
    support,
):
    print(
        f"{team}: "
        f"precision={p:.3f} "
        f"recall={r:.3f} "
        f"F1={f:.3f} "
        f"support={s}"
    )

print(
    "\nMacro F1:",
    round(f1.mean(), 4)
)

print(
    "\nConfusion matrix:"
)

print(
    confusion_matrix(
        y_true,
        y_pred,
        labels=["H", "A"],
    )
)

test_features = pd.DataFrame({
    "evidence_team": [
        "H",
        "H",
        "H",
        None,
        None,
        None,
        "H",
        "H",
    ],
    "ball_speed": [0] * 8,
    "min_distance": [0] * 8,
})

predictions = temporal_state_machine_v4(
    test_features,
    confirmation_frames=10,
)

print("Test predictions with insufficient confirmation frames:")
print(predictions)