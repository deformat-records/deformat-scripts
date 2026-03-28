# Slicethon

Slices WAV files into evenly sized segments using ffmpeg.
This script was designed for quickly breaking samples into equal sections for chopping, resampling, drum slicing, or loading into trackers and firmware workflows.
It reads the exact file duration using `ffprobe`, calculates equal slice lengths, then exports each slice as an individual WAV file.

## How To Use

Requirements:
- ffmpeg installed and available in system PATH

Usage:
```bash
python slicethon.py input.wav slice_count
```

Example:
```bash
python slicethon.py amen.wav 16
```

Batch All WAV in a directory:
```bash
python slicethon.py * 16
```

This will process every `.wav` file in the current directory.

## Output

A folder is created automatically using the source filename:

```text
amen/
├── amen_0001.wav
├── amen_0002.wav
├── amen_0003.wav
├── amen_0004.wav
├── amen_0005.wav
└── ...
```

Each slice keeps:
- original sample format
- original extension
- sequential numbering with zero padding

## Features

- automatic duration detection using `ffprobe`
- equal slice math based on total duration
- zero-padded filenames (`0001`, `0002`, etc.)
- per-file output folders
- supports single-file or wildcard batch slicing

## Notes

Slice length is calculated as:

```python
duration / slice_count
```

This means all slices are mathematically equal, even if the source length is unusual.

## Typical Uses

- chopping breaks into equal divisions
- preparing samples for trackers
- generating firmware-ready sample banks
- quick modular resampling workflows

## Limits

Current script behavior:
- requires valid WAV input
- slice count must be an integer
- output overwrites existing files with same names (so be careful)

If the file does not exist, conversion stops immediately.