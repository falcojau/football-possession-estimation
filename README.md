# Football Possession Estimation

End-to-end football possession estimation system using player and ball tracking data, geometric analysis, and temporal state machines. 
The pipeline processes over 199,000 frames, combining rule-based inference and explainable decision logic to estimate possession and potential game stoppages.

## Acknowledgements

This project builds on the **More than a Hack 2027** challenge organised by
[Metrica Sports](https://metrica-sports.com), FC Barcelona and Mobile World Capital Barcelona.
The original starter kit is available at
<https://github.com/metrica-sports/more-than-a-hack-2027>, copyright © Metrica Sports, and is
used under the MIT licence reproduced in [LICENSE](LICENSE).

**The match data is not included and not covered by this repository's licence.** Videos, tracking,
Smart Tagging and homography are licensed separately for the competition only. This repository
also does not include the competition documentation, the scorer, the public ground truth, the
baselines or any submission. To run the code you need to enrol in the challenge and download the
data yourself.

## What comes from where

| Path | Origin |
| --- | --- |
| `games.py` | Original starter kit (Metrica Sports), unmodified. Per-game constants and data paths. |
| `starter/load_smart_tagging.py` | Original starter kit (Metrica Sports), unmodified. Smart Tagging XML loader. |
| `LICENSE` | Original Metrica Sports MIT licence, kept as is. |
| `src/possession_pipeline/` | Independently developed: tracking adapter, geometry features, evidence generation, temporal state machine, game-state / activity / stoppage inference, restart index, decision layer, exporter. |
| `tests/`, `scripts/`, `exploration/` | Independently developed. |
| `TECHNICAL_DOCUMENTATION.md` | Independently developed: methodology, policies and limitations. |

The two original files reference `DATA.md`, which is [DATA.md](DATA.md) in this repository. The original `LICENSE` also mentions `RULES.md`, which belongs to the original competition repository.
The original competition documents (`RULES.md`, `FAQ.md`, `CHALLENGE.md`, `EVALUATION.md`, `SUBMISSION.md`, `OVERVIEW.md`) are not republished here; they are available in the official Metrica Sports repository: <https://github.com/metrica-sports/more-than-a-hack-2027>.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
```

`exploration/inspect_tracking.py` is optional and needs `pip install -r requirements-exploration.txt`
(adds scikit-learn). It also reads the public 5-minute ground truth from the original repository,
which is not republished here, so it only runs if you place that file locally.

The tests use synthetic data and do not need the match data.

## Running on the real data

Place the match assets in `data/` (or set `MTAH_DATA_DIR`), as described in [DATA.md](DATA.md). Then, from the repository root:

```bash
python scripts/run_real_inference.py
```

It creates `evaluation/results/` if needed and writes a `frame,label` CSV there; the folder is git-ignored. Generated
submissions are never committed, since a full-match label file is a derivative of the restricted data.

## Method and limitations

See [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md). In short: the possession evidence is a
geometric proximity heuristic, not verified possession, and the Smart Tagging restart intervals are
fixed-length windows, not observed stoppage lengths.

## Licence and copyright

MIT, see [LICENSE](LICENSE), kept exactly as in the original starter kit. It covers the code only,
never the match data.

- Starter-kit components (`games.py`, `starter/load_smart_tagging.py`): Copyright (c) 2026-2027 Metrica Sports.
- Independently developed code and documentation (`src/`, `tests/`, `scripts/`, `exploration/`,
  `TECHNICAL_DOCUMENTATION.md`): Copyright (c) 2026 Jaume Falcó, released under the same MIT terms.
