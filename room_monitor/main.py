"""Webcam loop: detect, combine state, draw, and log."""

# `python room_monitor/main.py` has no package context. Put the image_detection
# root on the path and mark this file as part of room_monitor so the relative
# imports below resolve. `python -m room_monitor.main` already has that context.
if __name__ == "__main__" and __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "room_monitor"

import time
from datetime import datetime

import cv2

from . import config
from .detectors.doorway import DoorwayTracker
from .detectors.motion import MotionDetector
from .detectors.people import PeopleDetector
from .detectors.posture import PostureClassifier
from .detectors.quality import assess_quality, save_blurry_frame
from .event_log import EventLog
from .overlay import draw
from .state import build_state


def main() -> None:
    capture = cv2.VideoCapture(config.CAMERA_INDEX)
    if not capture.isOpened():
        raise SystemExit(f"Could not open camera {config.CAMERA_INDEX}")

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    motion = MotionDetector()
    people = PeopleDetector()
    doorway = DoorwayTracker()
    posture = PostureClassifier()
    log = EventLog()
    last_snapshot = 0.0

    while True:
        ok, frame = capture.read()
        if not ok:
            break

        now = datetime.now()
        quality, blur_score = assess_quality(frame)
        if quality == "Blurry" and time.monotonic() - last_snapshot >= config.SNAPSHOT_COOLDOWN_SEC:
            path = save_blurry_frame(frame, now)
            print(f"saved blurry frame {path}")
            last_snapshot = time.monotonic()

        motion_label, motion_score = motion.assess(frame)
        detected = people.detect(frame)
        events = doorway.update(detected, frame.shape)
        postures = posture.classify(detected)
        state = build_state(
            quality,
            blur_score,
            motion_label,
            motion_score,
            detected,
            postures,
            events,
            now,
        )
        log.record(state)
        draw(frame, state)
        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
