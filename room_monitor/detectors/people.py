"""People tracking with YOLO11n-pose and ByteTrack."""

from dataclasses import dataclass

import numpy as np
from ultralytics import YOLO

from .. import config


@dataclass
class Person:
    track_id: int
    bbox: tuple[int, int, int, int]
    keypoints: np.ndarray
    keypoint_conf: np.ndarray

    @property
    def centroid(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


class PeopleDetector:
    def __init__(self) -> None:
        self.model = YOLO(config.YOLO_MODEL)

    def detect(self, frame) -> list[Person]:
        results = self.model.track(
            frame,
            persist=True,
            tracker=config.TRACKER,
            conf=config.CONFIDENCE,
            classes=[0],
            verbose=False,
        )
        if not results:
            return []

        result = results[0]
        boxes = result.boxes
        keypoints = result.keypoints
        if boxes is None or keypoints is None or boxes.id is None:
            return []

        ids = boxes.id.cpu().numpy().astype(int)
        xyxy = boxes.xyxy.cpu().numpy()
        points = keypoints.xy.cpu().numpy()
        if keypoints.conf is None:
            conf = np.ones(points.shape[:2], dtype=np.float32)
        else:
            conf = keypoints.conf.cpu().numpy()

        people: list[Person] = []
        for index, track_id in enumerate(ids):
            x1, y1, x2, y2 = xyxy[index]
            people.append(
                Person(
                    track_id=int(track_id),
                    bbox=(int(x1), int(y1), int(x2), int(y2)),
                    keypoints=points[index],
                    keypoint_conf=conf[index],
                )
            )
        return people
