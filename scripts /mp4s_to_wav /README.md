# MP4s to WAV

Extracts audio from all `.mp4` files in a directory and converts them to `.wav` files using ffmpeg

This script is useful for quickly pulling audio from recorded jams, phone captures, or video exports for later editing, sampling, or tracker preparation.
Really any directory of videos you have that you want to extract the audio from.

Each `.mp4` file is converted to a `.wav` file with the same base filename.

Features:
- batch conversion of all `.mp4` files
- 44.1 kHz output
- stereo WAV export
- preserves original filenames

## How To Use

Requirements:
- ffmpeg installed and available in system PATH

Usage:
```bash
python mp4s_to_wavs.py <input_directory>
```
