from possession_pipeline.features.geometry_features import (
    GeometryFeatures,
)


def generate_evidence(
    features: GeometryFeatures,
) -> str | None:

    if features.d_H is None or features.d_A is None:
        return None

    if features.d_H < features.d_A:
        return "H"

    if features.d_A < features.d_H:
        return "A"

    return None