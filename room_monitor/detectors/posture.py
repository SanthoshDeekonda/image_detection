"""Seated vs. Standing/Moving from pose keypoints and track speed."""

from .. import config
from .people import Person

LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6
LEFT_HIP = 11
RIGHT_HIP = 12
LEFT_KNEE = 13
RIGHT_KNEE = 14
LEFT_ANKLE = 15
RIGHT_ANKLE = 16


def _point(person: Person, index: int):
    if person.keypoint_conf[index] < config.KEYPOINT_CONF:
        return None
    x, y = person.keypoints[index]
    return float(x), float(y)


def _mid(left, right):
    if left and right:
        return ((left[0] + right[0]) / 2.0, (left[1] + right[1]) / 2.0)
    return left or right


class PostureClassifier:
    def __init__(self) -> None:
        self._previous: dict[int, tuple[float, float]] = {}

    def classify(self, people: list[Person]) -> dict[int, str]:
        labels: dict[int, str] = {}
        current: dict[int, tuple[float, float]] = {}

        for person in people:
            centroid = person.centroid
            current[person.track_id] = centroid
            previous = self._previous.get(person.track_id)
            speed = 0.0
            if previous is not None:
                speed = ((centroid[0] - previous[0]) ** 2 + (centroid[1] - previous[1]) ** 2) ** 0.5
            labels[person.track_id] = _label(person, speed)

        self._previous = current
        return labels


def _label(person: Person, speed: float) -> str:
    if _is_seated(person) and speed < config.MOVING_SPEED_PX:
        return "Seated"
    return "Standing/Moving"


def _is_seated(person: Person) -> bool:
    shoulder = _mid(_point(person, LEFT_SHOULDER), _point(person, RIGHT_SHOULDER))
    hip = _mid(_point(person, LEFT_HIP), _point(person, RIGHT_HIP))
    knee = _mid(_point(person, LEFT_KNEE), _point(person, RIGHT_KNEE))
    ankle = _mid(_point(person, LEFT_ANKLE), _point(person, RIGHT_ANKLE))

    if shoulder and hip and knee:
        torso = abs(hip[1] - shoulder[1]) + 1e-6
        if abs(knee[1] - hip[1]) / torso < config.SEATED_THIGH_RATIO:
            return True
        if ankle is not None and abs(ankle[1] - hip[1]) / torso < config.SEATED_LEG_RATIO:
            return True
        return False

    x1, y1, x2, y2 = person.bbox
    return (y2 - y1) / max(x2 - x1, 1) < config.SEATED_BOX_RATIO
