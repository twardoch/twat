#!/usr/bin/env -S uv run
# /// script
# dependencies = ["prefect", "pydantic"]
# ///
from functools import cached_property
from pathlib import Path

from prefect import flow, task
from pydantic import BaseModel, computed_field


# Define your expensive operations as Prefect tasks.
@task(retries=2)
def extract_audio_task(video_path: Path, audio_path: Path) -> None:
    """Extract audio from video, simulating a long-running process."""

    # Simulate fetching video metadata as JSON
    import json
    import time
    from random import randint

    time.sleep(2)  # Simulate API call

    metadata = {
        "duration": randint(60, 3600),
        "codec": "aac",
        "bitrate": f"{randint(128, 320)}kbps",
        "channels": 2,
        "sample_rate": 44100,
    }

    metadata["duration"] // 10
    for _i in range(10):
        time.sleep(0.5)  # Simulate processing time

    # Save simulated audio and metadata
    audio_path.write_text(json.dumps(metadata))


@task(retries=2)
def generate_transcript_task(audio_path: Path) -> str:
    """Generate transcript from audio, simulating API calls and processing."""

    import json
    import time
    from random import choice, randint

    # Simulate loading audio metadata
    metadata = json.loads(audio_path.read_text())

    time.sleep(1.5)

    # Simulate processing chunks with progress
    duration = metadata["duration"]
    chunk_size = 30  # Process in 30-second chunks
    chunks = duration // chunk_size

    words = [
        "hello",
        "world",
        "this",
        "is",
        "a",
        "test",
        "video",
        "with",
        "some",
        "random",
        "words",
        "being",
        "processed",
    ]

    transcript_parts = []
    for _i in range(chunks):
        time.sleep(0.3)  # Simulate API call and processing
        # Generate some random text
        chunk_text = " ".join(choice(words) for _ in range(randint(5, 15)))
        transcript_parts.append(chunk_text)

    return " ".join(transcript_parts)


@flow
def process_video_flow(video_path: Path) -> (Path, str):
    audio = video_path.with_suffix(".mp3")
    # Only extract audio if the file does not exist.
    if not audio.exists():
        extract_audio_task(video_path, audio)
    transcript = generate_transcript_task(audio)
    return audio, transcript


class VideoTranscript(BaseModel):
    video_path: Path

    @computed_field
    @cached_property
    def audio_path(self) -> Path:
        # Trigger the Prefect flow to process the video.
        audio, _ = process_video_flow(self.video_path)
        return audio

    @computed_field
    @cached_property
    def text_transcript(self) -> str:
        # Ensure audio extraction happens first.
        _, transcript = process_video_flow(self.video_path)
        return transcript


# Usage Example:
if __name__ == "__main__":
    # Assume "video.mp4" exists; audio and transcript will be generated on demand.
    vt = VideoTranscript(video_path=Path("video.mp4"))
