"""Thresholds, door line, and camera settings for the room monitor."""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent

# Camera
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Clear / Blurry. Laplacian variance at or below this is Blurry.
BLUR_THRESHOLD = 100.0
# Minimum seconds between saved blurry frames.
SNAPSHOT_COOLDOWN_SEC = 5.0
SNAPSHOT_DIR = PACKAGE_DIR / "snapshots"

# Motion / No motion. Mean absolute frame difference above this is Motion.
MOTION_THRESHOLD = 8.0

# Door line in normalized frame coordinates, (x, y) from top-left.
# Default is a vertical line across the middle of the view.
DOOR_LINE_START = (0.50, 0.15)
DOOR_LINE_END = (0.50, 0.90)
# Crossing onto the positive side of the line (left of the default line) is an Entry.
ENTRY_IS_POSITIVE = True

# People. Ultralytics ships ByteTrack as bytetrack.yaml.
YOLO_MODEL = "yolo11n-pose.pt" # optional model yolo26n-pose.pt
TRACKER = "bytetrack.yaml"
CONFIDENCE = 0.40
KEYPOINT_CONF = 0.30

# Seated vs. Standing/Moving.
# Thigh or full-leg vertical span divided by torso height. Smaller means folded, so Seated.
SEATED_THIGH_RATIO = 0.55
SEATED_LEG_RATIO = 1.15
# Fallback when hips and knees are missing: short boxes are treated as Seated.
SEATED_BOX_RATIO = 1.15
# Centroid speed in pixels per frame at or above this is Standing/Moving.
MOVING_SPEED_PX = 12.0

LOG_DIR = PACKAGE_DIR / "logs"
LOG_CSV = LOG_DIR / "events.csv"
WINDOW_NAME = "Room monitor"
