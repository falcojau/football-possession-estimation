# Data

This project uses the tracking and Smart Tagging data of the **More Than a Hack 2027** challenge,
provided by [Metrica Sports](https://metrica-sports.com): one full LaLiga match, FC Barcelona vs
Athletic Club (`BAR-ATH`).

## The data is not included

The datasets are **not part of this repository**. They are distributed by the organisers under
separate, competition-only terms that do not allow redistribution, and the MIT licence of this
repository does not cover them. The repository contains no video, tracking, Smart Tagging,
homography or ground-truth file.

## How to obtain it

Enrol in the challenge and download the data bundle through the official resources:
<https://github.com/metrica-sports/more-than-a-hack-2027>. Accepting the organisers' terms is
required. Do not share the files or commit them to any repository.

## Expected local layout

Unpack the bundle into `data/`, keeping the original file names. The folder is git-ignored.

```
data/
├── tactical/
│   ├── BAR-ATH_tactical.mp4
│   ├── BAR-ATH_tactical_atd.xml
│   ├── BAR-ATH_tactical_atd.txt
│   ├── BAR-ATH_tactical_homography.csv
│   └── BAR-ATH_tactical_smart_tagging.xml
└── broadcast/                      (optional, not used by the pipeline scripts)
    ├── BAR-ATH_broadcast.mp4
    ├── BAR-ATH_broadcast_atd.xml
    ├── BAR-ATH_broadcast_atd.txt
    └── BAR-ATH_broadcast_homography.csv
```

The pipeline reads the `tactical` source: tracking (`_atd.xml`, `_atd.txt`) and Smart Tagging
(`_smart_tagging.xml`).

## Resolving paths

`games.py` resolves every dataset path. By default it looks in `data/` at the repository root. To
use another location, set `MTAH_DATA_DIR`:

```bash
export MTAH_DATA_DIR=/path/to/data
```

```python
import games

paths = games.asset_paths()                    # tactical (default)
paths = games.asset_paths(source="broadcast")  # broadcast
```

If a file is missing, `games.require()` raises an error listing each expected path.
