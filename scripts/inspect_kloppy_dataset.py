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
        limit=10,
    )

    print("\nDATASET TYPE:")
    print(type(dataset))

    print("\nDATASET LENGTH:")
    print(len(dataset.records))

    print("\nFIRST RECORD TYPE:")
    first_record = dataset.records[0]
    print(type(first_record))

    print("\nFIRST RECORD ATTRIBUTES:")
    print([
        attribute
        for attribute in dir(first_record)
        if not attribute.startswith("_")
    ])

    print("\nDATASET METADATA:")
    print(type(dataset.metadata))

    print("\nPITCH DIMENSIONS:")
    print(dataset.metadata.pitch_dimensions)

    print("\nFIRST FRAME:")

    print("Frame ID:", first_record.frame_id)

    print("Ball Coordinates:")
    print(first_record.ball_coordinates)

    print("\nPlayers Coordinates:")
    print(type(first_record.players_coordinates))

    print("\nFirst 3 players:")

    for player, coordinates in list(
        first_record.players_coordinates.items()
    )[:3]:
        print(player, coordinates)

if __name__ == "__main__":
    main()