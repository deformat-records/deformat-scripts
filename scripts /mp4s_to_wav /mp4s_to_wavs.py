# mp4s_to_wavs.py
# Realy basic, but has saved me A LOT of time in an editor.

import sys
import subprocess
from pathlib import Path


def convert_mp4_to_wav(folder):
    folder = Path(folder)

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    mp4_files = list(folder.glob("*.mp4"))

    if not mp4_files:
        print("No MP4 files.")
        return

    for mp4 in mp4_files:
        wav = mp4.with_suffix(".wav")

        print(f"Converting: {mp4.name} -> {wav.name}")

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(mp4),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "2",
            str(wav)
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed: {mp4.name}")

    print("Done!")

# because I always forget.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mp4s_to_wavs.py <folder>")
        sys.exit(1)

    convert_mp4_to_wav(sys.argv[1])