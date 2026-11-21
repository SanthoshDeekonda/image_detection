"""Console and CSV logging for room-state changes and door crossings."""

import csv
from pathlib import Path

from . import config
from .state import RoomState

COLUMNS = (
    "timestamp",
    "quality",
    "blur_score",
    "motion",
    "motion_score",
    "people_count",
    "postures",
    "door_events",
)


class EventLog:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or config.LOG_CSV
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._last_signature = None
        if not self.path.exists():
            with self.path.open("w", newline="") as handle:
                csv.writer(handle).writerow(COLUMNS)

    def record(self, state: RoomState) -> None:
        signature = state.signature()
        if signature == self._last_signature:
            return
        self._last_signature = signature
        row = _row(state)
        print(" | ".join(str(value) for value in row))
        with self.path.open("a", newline="") as handle:
            csv.writer(handle).writerow(row)


def _row(state: RoomState) -> list:
    postures = "; ".join(f"#{person.track_id} {person.posture}" for person in state.people)
    events = "; ".join(f"{event.kind} #{event.track_id}" for event in state.door_events)
    return [
        state.timestamp.isoformat(timespec="seconds"),
        state.quality,
        f"{state.blur_score:.1f}",
        state.motion,
        f"{state.motion_score:.2f}",
        state.people_count,
        postures,
        events,
    ]
