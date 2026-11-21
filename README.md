# Room monitor

Webcam loop that reports image quality, motion, people, doorway crossings, and posture.

## Layout

- `config.py` — thresholds, door line position, camera index
- `main.py` — webcam loop
- `state.py` — combines detector outputs into one state
- `overlay.py` — status panel and door line drawing
- `event_log.py` — console and CSV logging
- `detectors/quality.py` — Clear / Blurry
- `detectors/motion.py` — Motion / No motion
- `detectors/people.py` — YOLO11n-pose and ByteTrack
- `detectors/doorway.py` — Entry / Exit line crossing
- `detectors/posture.py` — Seated vs. Standing/Moving
- `logs/` — `events.csv`
- `snapshots/` — blurry frames

## Run

From the repository root (`image_detection`):

```bash
pip install -r room_monitor/requirements.txt
python -m room_monitor.main
```

`python room_monitor/main.py` works as well. Modules inside the package import each other with relative imports (`from .` and `from ..`), so they resolve against `room_monitor` rather than the current working directory.

Press `q` to quit. The first run downloads `yolo11n-pose.pt`.

Edit `room_monitor/config.py` to move the door line, change the camera index, or retune thresholds. With the default vertical line, crossing onto the left side is an Entry.
