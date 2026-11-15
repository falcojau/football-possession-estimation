from bisect import bisect_right

from possession_pipeline.game.smart_tagging_adapter import (
    RestartCandidate,
)


class RestartIndex:

    def __init__(self, candidates: list[RestartCandidate]):

        intervals = sorted(
            (candidate.start_frame, candidate.end_frame)
            for candidate in candidates
        )

        merged = []

        for start, end in intervals:

            if start > end:
                raise ValueError(
                    "Interval start cannot exceed interval end"
                )

            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(
                    merged[-1][1],
                    end,
                )

        self.intervals = [
            (start, end)
            for start, end in merged
        ]

        self.starts = [
            start
            for start, _ in self.intervals
        ]

    def contains(self, frame_id: int) -> bool:

        index = bisect_right(self.starts, frame_id) - 1

        if index < 0:
            return False

        start, end = self.intervals[index]

        return start <= frame_id <= end