import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import Counter, defaultdict

from possession_pipeline.game.smart_tagging_adapter import (
    extract_restart_candidates,
)
from starter.load_smart_tagging import load


def main():

    events = load()

    set_pieces = [
        event
        for event in events
        if (event["code"] or "").strip().upper()
        == "SET PIECES"
    ]

    print(f"\nTotal SET PIECES: {len(set_pieces)}")

    types = Counter(
        event["tags"].get("Type", "UNKNOWN")
        for event in set_pieces
    )

    print("\nSET PIECE TYPES:")

    for event_type, count in types.most_common():
        print(f"{event_type}: {count}")

    print("\nFIRST 10 SET PIECES:")

    for event in set_pieces[:10]:

        print(
            f"Frames {event['start_frame']}-"
            f"{event['end_frame']} | "
            f"Type: {event['tags'].get('Type')} | "
            f"Team: {event['tags'].get('Team')}"
        )

    durations_by_type = defaultdict(list)

    for event in events:

        if (event["code"] or "").strip().upper() != "SET PIECES":
            continue

        restart_type = event["tags"].get("Type", "UNKNOWN")

        duration = event["end_frame"] - event["start_frame"]

        durations_by_type[restart_type].append(duration)

    print("\nSET PIECE DURATIONS")

    print("-------------------")

    for restart_type, durations in durations_by_type.items():

        unique_durations = sorted(set(durations))

        print(
            f"{restart_type}: "
            f"count={len(durations)}, "
            f"unique_durations={unique_durations}"
        )

    candidates = extract_restart_candidates(events)

    sorted_candidates = sorted(
        candidates,
        key=lambda candidate: candidate.start_frame,
    )

    overlaps = []

    for previous, current in zip(
        sorted_candidates,
        sorted_candidates[1:],
    ):
        if current.start_frame <= previous.end_frame:
            overlaps.append((previous, current))

    print("\nOVERLAPPING INTERVALS")
    print("Total:", len(overlaps))

    for previous, current in overlaps[:5]:
        print(previous, current)


if __name__ == "__main__":
    main()