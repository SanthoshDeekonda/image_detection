"""Motion / No motion from the mean absolute difference between frames."""

import cv2

from .. import config


class MotionDetector:
    def __init__(self) -> None:
        self._previous = None

    def assess(self, frame) -> tuple[str, float]:
        """Return ("Motion" or "No motion", mean absolute difference)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if self._previous is None or self._previous.shape != gray.shape:
            self._previous = gray
            return "No motion", 0.0

        delta = cv2.absdiff(self._previous, gray)
        score = float(delta.mean())
        self._previous = gray
        label = "Motion" if score >= config.MOTION_THRESHOLD else "No motion"
        return label, score
