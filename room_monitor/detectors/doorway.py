"""Entry / Exit when a tracked person crosses the door line."""

from dataclasses import dataclass

from .. import config
from .people import Person


@dataclass
class DoorEvent:
    track_id: int
    kind: str  # "Entry" or "Exit"


def _line_pixels(width: int, height: int) -> tuple[tuple[float, float], tuple[float, float]]:
    x1, y1 = config.DOOR_LINE_START
    x2, y2 = config.DOOR_LINE_END
    return (x1 * width, y1 * height), (x2 * width, y2 * height)


def _cross(a, b, p) -> float:
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def _segments_intersect(p1, p2, q1, q2) -> bool:
    def orient(a, b, c) -> float:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    o1 = orient(p1, p2, q1)
    o2 = orient(p1, p2, q2)
    o3 = orient(q1, q2, p1)
    o4 = orient(q1, q2, p2)
    return o1 * o2 < 0 and o3 * o4 < 0


class DoorwayTracker:
    def __init__(self) -> None:
        self._previous: dict[int, tuple[float, float]] = {}

    def update(self, people: list[Person], frame_shape) -> list[DoorEvent]:
        height, width = frame_shape[:2]
        start, end = _line_pixels(width, height)
        events: list[DoorEvent] = []
        current: dict[int, tuple[float, float]] = {}

        for person in people:
            centroid = person.centroid
            current[person.track_id] = centroid
            previous = self._previous.get(person.track_id)
            if previous is None or not _segments_intersect(previous, centroid, start, end):
                continue

            arrived_positive = _cross(start, end, centroid) > 0
            if arrived_positive == config.ENTRY_IS_POSITIVE:
                kind = "Entry"
            else:
                kind = "Exit"
            events.append(DoorEvent(track_id=person.track_id, kind=kind))

        self._previous = current
        return events
