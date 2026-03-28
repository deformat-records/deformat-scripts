# Deformat Helper Scripts

A collection of scripts and small tools to assist in various audio applications.
This repo hosts a selection of scripts (mainly python) to aid in other Deformat projects, or audio applications in general.

I will do my best to update every script here, particularly those that are designed to work with another specific project.
Additionally, I will attempt to make their usage as clear as possible.

Some of these were written in a hurry, some way in the past, so consistency is not exactly there.
Because of that, I will do my best to document them here.

## List of scripts and what they do:

Here I will do my best to overview each script.
I will also include a README.md for each individual script to help clarify usage, and all else related to it.

| Script | Purpose | Related Project |
|--------|---------|-----------------|
| [wav_to_int8.py](scripts/wav_to_int8/) | Convert wav files to firmware headers | [project-omg](https://github.com/deformat-records/project-omg) |
| [mp4s_to_wav.py](scripts/mp4s_to_wav/) | Batch wav audio from mp4 video files | General Use |
---
### WAV to _int8.h

Converts a directory of audio samples into Mozzi-compatible _int8.h header files for embedded firmware use.

Designed for [Moffenzeef GMO](https://github.com/moffenzeefmodular/GMO) / [project-omg](https://github.com/deformat-records/project-omg), this script uses FFmpeg to normalize audio and adapts [char2mozzi.py](https://github.com/sensorium/Mozzi/blob/master/extras/python/char2mozzi.py) logic to generate firmware-ready wavetable headers.

Features:
- mono conversion
- 8-bit signed PCM output
- automatic sample padding (ensures all the same length)
- memory limit checking
- generated include list

Usage:
```bash
python wav_to_int8.py <input_directory>
```

[wav_to_int8.py documentation](scripts/wav_to_int8/README.md)

### MP4 to WAV

Extracts audio from all MP4 files in a directory and converts them to WAV format using ffmpeg.

Features:
- batch conversion of all `.mp4` files
- 44.1 kHz output
- stereo WAV export
- preserves original filenames

Usage:
```bash
python mp4s_to_wavs.py <input_directory>
```

[mp4s_to_wav.py documentation](scripts/mp4s_to_wav/README.md)

---

## Notes

This repository will continue to expand as older utilities are cleaned up and documented.
Some scripts are tightly connected to specific Deformat projects, while others may be generally useful for audio workflows.
As many of these were (originally) written for personal use, they may be hard to follow, poorly documented, or contain "borrowed" code.

I will do my best to document, and attribte as I add them to the repo