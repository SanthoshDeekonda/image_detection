"""Clear / Blurry frame quality from Laplacian variance."""

from datetime import datetime
from pathlib import Path

import cv2

from .. import config


def assess_quality(frame) -> tuple[str, float]:
    """Return ("Clear" or "Blurry", variance score)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    label = "Blurry" if score <= config.BLUR_THRESHOLD else "Clear"
    return label, score


def save_blurry_frame(frame, when: datetime | None = None) -> Path:
    """Write a blurry frame under snapshots/ and return the path."""
    when = when or datetime.now()
    config.SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = config.SNAPSHOT_DIR / f"blur_{when.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    cv2.imwrite(str(path), frame)
    return path
