
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import cv2 
from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent
MODEL_NAME = "yolo11n.pt"

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


def process_video(
    video_path: Path,
    output_dir: Path,
    save_video: bool = False,
) -> dict:
    video_path = Path(video_path)
    output_dir = Path(output_dir)

    if not video_path.is_file():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    annotated_path = output_dir / "annotated.mp4"
    results_path = output_dir / "results.json"

    # Remove outdated outputs before processing.
    results_path.unlink(missing_ok=True)
    annotated_path.unlink(missing_ok=True)

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    writer = None

    try:
        fps = capture.get(cv2.CAP_PROP_FPS)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if fps <= 0 or width <= 0 or height <= 0:
            raise RuntimeError("Invalid video metadata")

        if save_video:
            writer = cv2.VideoWriter(
                str(annotated_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (width, height),
            )

            if not writer.isOpened():
                raise RuntimeError(
                    "Cannot create annotated video"
                )

        # New model instance resets tracking between videos.
        model = YOLO(MODEL_NAME)

        processed_frames = 0
        max_visible = 0
        total_visible = 0

        # Overall tracking statistics.
        seen_tracks = {}
        class_counts = Counter()

        # Per-second statistics.
        interval_data = defaultdict(
            lambda: {
                "frames": 0,
                "total_visible": 0,
                "max_visible": 0,
                "track_ids": set(),
            }
        )

        while True:
            success, frame = capture.read()

            if not success:
                break

            frame_index = processed_frames
            processed_frames += 1

            result = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=list(VEHICLE_CLASSES.keys()),
                conf=0.25,
                verbose=False,
            )[0]

            boxes = result.boxes
            visible = len(boxes) if boxes is not None else 0

            max_visible = max(max_visible, visible)
            total_visible += visible

            second = int(frame_index / fps)
            interval = interval_data[second]

            interval["frames"] += 1
            interval["total_visible"] += visible
            interval["max_visible"] = max(
                interval["max_visible"], visible
            )

            if boxes is not None and boxes.id is not None:
                track_ids = boxes.id.int().cpu().tolist()
                class_ids = boxes.cls.int().cpu().tolist()

                for track_id, class_id in zip(
                    track_ids, class_ids
                ):
                    interval["track_ids"].add(track_id)

                    if track_id not in seen_tracks:
                        vehicle_type = VEHICLE_CLASSES[class_id]
                        seen_tracks[track_id] = vehicle_type
                        class_counts[vehicle_type] += 1

            if writer is not None:
                annotated = result.plot()

                cv2.putText(
                    annotated,
                    f"Visible: {visible} | Tracks: {len(seen_tracks)}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                writer.write(annotated)

            if processed_frames % 100 == 0:
                print(
                    f"{video_path.name}: "
                    f"{processed_frames} frames processed"
                )

        if processed_frames == 0:
            raise RuntimeError("Video contains no readable frames")

        intervals = []

        for second, values in sorted(interval_data.items()):
            intervals.append({
                "start_second": second,
                "end_second": min(
                    second + 1,
                    round(processed_frames / fps, 3),
                ),
                "average_visible": round(
                    values["total_visible"] / values["frames"],
                    2,
                ),
                "max_visible": values["max_visible"],
                "unique_track_ids": len(values["track_ids"]),
            })

        report = {
            "video_id": video_path.stem,
            "source_file": video_path.name,
            "source_type": "recorded_video",
            "recorded_at": None,
            "processed_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "road_segment_id": None,
            "model": MODEL_NAME,
            "tracker": "bytetrack",
            "fps": round(fps, 3),
            "resolution": {
                "width": width,
                "height": height,
            },
            "duration_seconds": round(
                processed_frames / fps, 2
            ),
            "processed_frames": processed_frames,
            "statistics": {
                "max_visible_vehicles": max_visible,
                "average_visible_vehicles": round(
                    total_visible / processed_frames, 2
                ),
                "unique_track_ids": len(seen_tracks),
                "track_counts_by_class": {
                    name: class_counts[name]
                    for name in VEHICLE_CLASSES.values()
                },
            },
            "intervals": intervals,
            "count_method": "unique_tracker_ids",
            "count_is_estimate": True,
            "annotated_video": (
                annotated_path.name if save_video else None
            ),
            "processing_status": "completed",
        }

    finally:
        capture.release()

        if writer is not None:
            writer.release()

    with results_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return report
