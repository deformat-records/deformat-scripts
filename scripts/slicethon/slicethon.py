# slicethon.py
# slice wav files into even numbers of slices.
#
# by John Merrik for Deformat
# For more useful audio scripts (mostly python):
# https://github.com/deformat-records/deformat-scripts
# no attribution required, just leave this crap up here

import subprocess
import sys
from pathlib import Path

def get_duration(input_file):
    """Return audio duration in seconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file,
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def slice_audio(input_file, slice_count):
    """Slice the audio file into X number of slices"""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"File not found: {input_file}")
        sys.exit(1)

    # Create output folder with same name as file
    output_folder = input_path.with_suffix("")  # remove extension
    output_folder.mkdir(exist_ok=True)

    duration = get_duration(str(input_path))
    slice_len = duration / slice_count

    print(f"Total duration: {duration:.3f}s")
    print(f"Each slice: {slice_len:.3f}s")
    print(f"Output folder: {output_folder}")

    for i in range(slice_count):
        start = slice_len * i

        output_file = (
            output_folder /
            f"{input_path.stem}_{i+1:04d}{input_path.suffix}"
        )

        print(f"→ Writing slice {i+1}/{slice_count}: {output_file.name}")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", str(input_path),
                "-ss", str(start),
                "-t", str(slice_len),
                str(output_file)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

    print("Sliced!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python slicethon.py input.wav slice_count")
        sys.exit(1)

    input_file = sys.argv[1]
    slice_count = int(sys.argv[2])
     
    if (input_file == "*"):
        folder = Path(".\\")
        for wav in folder.glob("*.wav"):
            slice_audio(wav, slice_count)
    else:
        slice_audio(input_file, slice_count)