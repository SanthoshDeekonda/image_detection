"""Combine detector outputs into one room state."""

from dataclasses import dataclass, field
from datetime import datetime

from .detectors.doorway import DoorEvent
from .detectors.people import Person


@dataclass
class PersonState:
    track_id: int
    posture: str
    bbox: tuple[int, int, int, int]


@dataclass
class RoomState:
    timestamp: datetime
    quality: str
    blur_score: float
    motion: str
    motion_score: float
    people: list[PersonState] = field(default_factory=list)
    door_events: list[DoorEvent] = field(default_factory=list)

    @property
    def people_count(self) -> int:
        return len(self.people)

    def signature(self) -> tuple:
        """Identity of the state, ignoring timestamps and raw scores."""
        people = tuple((person.track_id, person.posture) for person in self.people)
        events = tuple((event.track_id, event.kind) for event in self.door_events)
        return (self.quality, self.motion, people, events)


def build_state(
    quality: str,
    blur_score: float,
    motion: str,
    motion_score: float,
    people: list[Person],
    postures: dict[int, str],
    door_events: list[DoorEvent],
    when: datetime | None = None,
) -> RoomState:
    views = [
        PersonState(
            track_id=person.track_id,
            posture=postures.get(person.track_id, "Standing/Moving"),
            bbox=person.bbox,
        )
        for person in people
    ]
    views.sort(key=lambda person: person.track_id)
    return RoomState(
        timestamp=when or datetime.now(),
        quality=quality,
        blur_score=blur_score,
        motion=motion,
        motion_score=motion_score,
        people=views,
        door_events=door_events,
    )
