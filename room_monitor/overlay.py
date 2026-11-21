"""Status panel and door line drawing."""

import cv2

from . import config
from .state import RoomState


def draw(frame, state: RoomState) -> None:
    _draw_door_line(frame)
    _draw_people(frame, state)
    _draw_panel(frame, state)


def _draw_door_line(frame) -> None:
    height, width = frame.shape[:2]
    x1, y1 = config.DOOR_LINE_START
    x2, y2 = config.DOOR_LINE_END
    start = (int(x1 * width), int(y1 * height))
    end = (int(x2 * width), int(y2 * height))
    cv2.line(frame, start, end, (0, 220, 255), 2)
    cv2.putText(
        frame,
        "door",
        (start[0] + 8, start[1] + 16),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 220, 255),
        1,
        cv2.LINE_AA,
    )


def _draw_people(frame, state: RoomState) -> None:
    for person in state.people:
        x1, y1, x2, y2 = person.bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 220, 80), 2)
        cv2.putText(
            frame,
            f"#{person.track_id} {person.posture}",
            (x1, max(16, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (80, 220, 80),
            1,
            cv2.LINE_AA,
        )


def _draw_panel(frame, state: RoomState) -> None:
    lines = [
        f"Quality: {state.quality} ({state.blur_score:.0f})",
        f"Motion: {state.motion} ({state.motion_score:.1f})",
        f"People: {state.people_count}",
    ]
    if state.people:
        posture_text = ", ".join(f"#{person.track_id} {person.posture}" for person in state.people)
        lines.append(f"Posture: {posture_text}")
    else:
        lines.append("Posture: —")

    if state.door_events:
        door_text = ", ".join(f"{event.kind} #{event.track_id}" for event in state.door_events)
    else:
        door_text = "—"
    lines.append(f"Door: {door_text}")

    width = max(len(line) for line in lines) * 11 + 16
    height = 22 * len(lines) + 12
    cv2.rectangle(frame, (8, 8), (8 + width, 8 + height), (20, 20, 20), -1)
    for index, line in enumerate(lines):
        cv2.putText(
            frame,
            line,
            (16, 28 + index * 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (240, 240, 240),
            1,
            cv2.LINE_AA,
        )
