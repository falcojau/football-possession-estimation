from possession_pipeline.features.geometry_features import (
    GeometryFeatures,
)

from possession_pipeline.evidence.evidence_generator import (
    generate_evidence,
)


def test_home_evidence():

    features = GeometryFeatures(
        frame_id=0,
        d_H=1.0,
        d_A=4.0,
        distance_margin=3.0,
    )

    assert generate_evidence(features) == "H"


def test_away_evidence():

    features = GeometryFeatures(
        frame_id=0,
        d_H=5.0,
        d_A=2.0,
        distance_margin=-3.0,
    )

    assert generate_evidence(features) == "A"


def test_equal_distance():

    features = GeometryFeatures(
        frame_id=0,
        d_H=2.0,
        d_A=2.0,
        distance_margin=0.0,
    )

    assert generate_evidence(features) is None


def test_missing_distance():

    features = GeometryFeatures(
        frame_id=0,
        d_H=None,
        d_A=3.0,
        distance_margin=None,
    )

    assert generate_evidence(features) is None