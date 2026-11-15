import pandas as pd

original = pd.read_csv(
    "evaluation/results/final_submission.csv"
)

experimental = pd.read_csv(
    "evaluation/results/experimental_stoppage_submission.csv"
)

assert len(original) == len(experimental) == 199319

assert original["frame"].equals(experimental["frame"])

valid_labels = {"H", "A", "D", "X"}

assert set(original["label"]).issubset(valid_labels)
assert set(experimental["label"]).issubset(valid_labels)

changes = original[
    original["label"] != experimental["label"]
].copy()

changes["new_label"] = experimental.loc[
    changes.index, "label"
]

print("\nCHANGED PREDICTIONS")
print(
    changes.groupby(["label", "new_label"]).size()
)

assert (
    (changes["label"] == "X")
    & (changes["new_label"] == "D")
).all()

print("\nINTEGRITY CHECK PASSED")