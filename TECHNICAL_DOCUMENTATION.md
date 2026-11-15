# Football Possession Estimation — Technical Documentation

**Project:** More Than a Hack 2027 · FC Barcelona vs Athletic Club  
**Status:** Phase 9.2 documentation · 15 November 2026  
**Scope:** Methodology, inference policies, reproducibility, limitations and submission integrity.

## 1. System overview

The system estimates football possession from Metrica tracking data (199,319 frames at 25 FPS), supplemented with Smart Tagging metadata. Its principal components are:

1. **Tracking adapter:** converts native Kloppy records into normalized `TrackingFrame` objects; aligns the tracking record ID to a zero-based submission frame ID.
2. **Geometry extractor:** computes nearest-player distances to the ball for home (`d_H`) and away (`d_A`) teams.
3. **Evidence generator:** returns `H`, `A`, or `None` from geometric proximity. Proximity is a heuristic, not verified possession.
4. **Temporal state machine:** maintains a possession estimate and uses hysteresis to prevent immediate H↔A changes after isolated contradictory observations.
5. **Activity inference:** treats visible-ball frames with valid H/A proximity evidence as *inferred* in-play activity.
6. **Stoppage inference:** treats missing-ball frames within a Smart Tagging restart-candidate interval, with no geometric possession evidence, as *inferred* stoppages.
7. **Final decision policy:** gives confirmed game states priority, then applies the inferred policies where the game state is unknown.
8. **Submission writer:** exports one `frame,label` record per frame; `None` becomes `X`.

## 2. Temporal configuration and rationale

`TemporalStateMachine(confirmation_frames=..., max_missing_frames=...)` is a stateful component:

- **`confirmation_frames`** requires a specified number of consecutive contrary H/A observations before switching an existing possession estimate. This implements hysteresis and limits reactions to isolated proximity changes. At 25 FPS, the nominal confirmation duration is `confirmation_frames / 25` seconds (e.g., 3 frames = 120 ms). This is a timing interpretation, **not** evidence that any specific value is optimal.
- **`max_missing_frames`** optionally clears a retained possession estimate after a run of missing evidence. `None` disables expiration, allowing the last estimate to persist indefinitely. This can create stale estimates during long missing-data intervals.
- When evidence is `None`, the pending switch candidate resets; the current estimate is retained unless expiration is enabled.
- The initial non-null observation establishes the initial estimate; hysteresis governs subsequent switches.

**Configuration used by `scripts/run_real_inference.py`:** `confirmation_frames=3` (a nominal 120 ms at 25 FPS) and `max_missing_frames=None` (the possession estimate never expires). These values are copied from the executed script. They were chosen as engineering defaults and are **not** presented as optimal: they were not tuned against match video or possession ground truth. Any change to them should be justified by a predeclared requirement (e.g., tolerable decision latency) and recorded together with the generated submission.

## 3. Game-state and decision semantics

The event-driven game-state machine supports `UNKNOWN`, `IN_PLAY`, `POSSIBLE_STOPPAGE`, and `STOPPED`. The experimental real-data inference used `GameState.UNKNOWN` because no reliable confirmed stoppage/restart event stream was established.

Final decision precedence:

| Condition | Exported label | Decision provenance |
| --- | --- | --- |
| Confirmed `STOPPED` | `D` | `CONFIRMED_STOPPAGE` |
| Confirmed `IN_PLAY` | H/A, or `X` if no estimate | `CONFIRMED_IN_PLAY` |
| `POSSIBLE_STOPPAGE` | `X` | `POSSIBLE_STOPPAGE` |
| Unknown game state + inferred stoppage | `D` | `INFERRED_STOPPAGE` |
| Unknown game state + inferred activity | H/A | `INFERRED_ACTIVITY` |
| Otherwise | `X` | `UNKNOWN_ACTIVITY` |

**Critical:** `INFERRED_IN_PLAY` is not equivalent to a confirmed restart. `INFERRED_STOPPAGE` is not equivalent to a confirmed referee stoppage. The exported CSV contains only labels, not provenance; the internal `decision_source` counters preserve that distinction for reporting.

## 4. Smart Tagging interpretation

The `SET PIECES` category yielded **59 restart candidates**: 26 throw-ins, 12 corner kicks, 10 goal kicks, 5 free kicks, 4 kick-offs after goals and 2 kick-offs at the start. The two kick-off types have 125-frame windows (5 s); the other four types have 875-frame windows (35 s). Nine overlapping pairs were identified in a consecutive-interval audit.

These fixed-duration windows are consistent with standardized event annotations, **not observed stoppage lengths**. They do not specify exact referee stoppage or restart frames. `RestartIndex` merges overlapping windows for efficient membership queries; merging does not turn them into confirmed stoppages. The index currently treats end boundaries as inclusive, a convention that remains unverified against source metadata. Frame-ID alignment between Smart Tagging and zero-based tracking must also be checked before asserting exact frame correspondence.

The experimental stoppage heuristic returns `INFERRED_STOPPAGE` only when **all three** hold:

- The frame falls within at least one restart-candidate window.
- Ball coordinates are unavailable.
- Geometric possession evidence is `None`.

This combination is a **weak heuristic**: ball absence can be caused by occlusion or tracking failure during live play. No validation of `D` accuracy has been established.

## 5. Results and integrity checks

Both runs processed **199,319 frames**. Full-match geometry evidence: `H=63,789`, `A=48,630`, `None=86,900`. Temporal estimates: `H=114,721`, `A=80,406`, `None=4,192`. These distributions are diagnostics, not accuracy scores.

| Export label | Original submission | Experimental stoppage submission |
| --- | ---: | ---: |
| `H` | 63,779 | 63,779 |
| `A` | 48,640 | 48,640 |
| `D` | 0 | 14,121 |
| `X` | 86,900 | 72,779 |
| **Total** | **199,319** | **199,319** |

Experimental decision sources: `INFERRED_ACTIVITY=112,419`, `INFERRED_STOPPAGE=14,121`, `UNKNOWN_ACTIVITY=72,779`. A direct comparison found exactly **14,121 changes, all `X → D`**, with no H/A changes; the integrity check passed. The original submission was reported as passing the official format validator; the experimental export was generated and structurally compared, but an independent official-validator pass for that experimental file was **not explicitly confirmed in the supplied results** and should be performed before submission.

**Interpretation:** the experimental file increases specific-label coverage, but there is no evidence here that it improves prediction accuracy, possession-spell F1, or dead-ball recall/precision.

## 6. Known limitations

- **`INFERRED_IN_PLAY`:** ball visibility and proximity to a team do not prove active play or true ball control. A visible ball near a player may occur during a stoppage.
- **`X`:** denotes insufficient evidence under the decision policy; it does not necessarily mean the ball is absent, the match is stopped, or possession is inherently unknowable. Conservative policy can yield many `X` frames even when the temporal estimator retains H/A.
- **`D`:** in the experimental output, all `D` labels come from `INFERRED_STOPPAGE`, **not confirmed stoppage events**. Broad event windows and missing-ball observations can generate false positives; stoppages outside annotated windows may be missed.
- **Source metadata:** `ball_state` and `ball_owning_team_id` were `None` for all 199,319 Kloppy records, so neither supplies direct ground-truth game state.
- **Temporal persistence:** without expiration, the last known H/A estimate can remain stale across long observation gaps; with expiration, coverage decreases. Neither policy has been demonstrated to be more accurate.
- **Annotation timing:** Smart Tagging interval boundaries, inclusivity, and frame alignment require explicit source-contract verification.
- **Evaluation:** successful processing, passing unit tests, and valid CSV format demonstrate engineering integrity, **not predictive quality**.

## 7. Compliance and reproducibility

The project must not tune thresholds against the competition possession ground truth or provided match video, manually create match labels from the video, or upload supplied match data to external AI services. Synthetic tests and engineering-based reasoning are permitted. Document each final parameter's engineering rationale independently of competition evaluation data.

Before final delivery:

1. Record the exact executed temporal parameters, source revision/commit, and input-to-frame alignment convention.
2. Run the official validator on the **experimental** CSV; confirm 199,319 consecutive frame IDs (`0`–`199318`) and only `H/A/D/X` labels.
3. Keep both outputs separately named and document which one is submitted.
4. Ensure the public repository excludes restricted tracking, event data, video, and any prohibited derived material.
5. Clearly label inferred states as heuristic and avoid claims of accuracy without permitted evaluation evidence.

**Bottom line:** the system is an end-to-end, reproducible-in-principle heuristic possession pipeline with explicit uncertainty and provenance. Its experimental dead-ball predictions remain unverified estimates, not confirmed match events.
