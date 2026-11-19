
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from detect import BASE_DIR, process_video


VIDEOS_DIR = BASE_DIR / "videos"
OUTPUTS_DIR = BASE_DIR / "outputs"

SUPPORTED_FORMATS = {".mp4", ".avi", ".mov", ".mkv"}


def run_batch(
    save_video: str = "sample",
    sample_count: int = 2,
) -> dict:
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    videos = sorted(
        path for path in VIDEOS_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_FORMATS
    )

    if not videos:
        print(f"No videos found in: {VIDEOS_DIR}")
        return {}

    # Avoid collisions between files such as
    # traffic.mp4 and traffic.avi.
    output_names = [
        f"{video.stem}_{video.suffix[1:].lower()}"
        for video in videos
    ]

    if len(output_names) != len(set(output_names)):
        raise RuntimeError(
            "Duplicate video output names detected"
        )

    summary = {
        "batch_processed_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "total_videos": len(videos),
        "successful": 0,
        "failed": 0,
        "save_video_mode": save_video,
        "videos": [],
    }

    for index, video in enumerate(videos):
        print(
            f"\n[{index + 1}/{len(videos)}] "
            f"Processing {video.name}"
        )

        output_dir = OUTPUTS_DIR / output_names[index]

        should_save_video = (
            save_video == "all"
            or (
                save_video == "sample"
                and index < sample_count
            )
        )

        try:
            report = process_video(
                video_path=video,
                output_dir=output_dir,
                save_video=should_save_video,
            )

            summary["successful"] += 1

            summary["videos"].append({
                "video": video.name,
                "status": "completed",
                "output_folder": output_dir.name,
                "unique_track_ids": report[
                    "statistics"
                ]["unique_track_ids"],
                "max_visible_vehicles": report[
                    "statistics"
                ]["max_visible_vehicles"],
                "annotated_video": should_save_video,
            })

            print(f"Completed: {video.name}")

        except Exception as error:
            summary["failed"] += 1

            summary["videos"].append({
                "video": video.name,
                "status": "failed",
                "error": str(error),
            })

            print(f"Failed: {video.name} -> {error}")

    summary_path = OUTPUTS_DIR / "summary.json"

    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print("\nBatch processing completed")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Summary: {summary_path}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Smart Traffic batch video processing"
    )

    parser.add_argument(
        "--save-video",
        choices=["none", "sample", "all"],
        default="sample",
        help="Which annotated videos to save",
    )

    parser.add_argument(
        "--sample-count",
        type=int,
        default=2,
        help="Number of annotated videos in sample mode",
    )

    args = parser.parse_args()

    if args.sample_count < 0:
        parser.error("--sample-count must be >= 0")

    result = run_batch(
        save_video=args.save_video,
        sample_count=args.sample_count,
    )

    if result and result["failed"]:
        raise SystemExit(1)
