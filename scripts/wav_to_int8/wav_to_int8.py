# wav_to_int8.py
#
# WAV 2 int8 converts a directory of wav files to raw and then int8.h for use with the GMO
# I really only used num2words to keep the aesthetic of the original moffenzeef code
# So this library is not important.
#
# by John Merrik for Deformat
# For more useful audio scripts (mostly python):
# https://github.com/deformat-records/deformat-scripts
# no attribution required, just leave this crap up here

import os
import subprocess
import array
import textwrap
import random
import argparse
import wave
from pathlib import Path
from num2words import num2words

SAMPLE_RATE = 16384
MAX_SECONDS = 8
MAX_FILES = 64  # This can probably be changed, honestly not sure of the limit.
MEMORY_LIMIT = 131072

NORMALIZE = True
HIGHPASS = 20

OUTPUT_DIR = Path("samples")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir", help="Input directory containing source audio files"
    )
    parser.add_argument("--normalize", action="store_true")
    return parser.parse_args()

def get_duration(file):
    result = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file),
        ]
    )
    return float(result.decode().strip())

def get_num_samples(wav_file):
    """added for calculation of the longest sampledata for MAX_NUM_CELLS in Arduino code"""
    with wave.open(str(wav_file), 'rb') as wf:
        return wf.getnframes()

def convert_audio(infile, outfile, target_duration, normalize=False):
    """DOWNGRADE the audio as needed"""

    filters = []

    if HIGHPASS:
        filters.append(f"highpass=f={HIGHPASS}")

    if normalize:
        filters.append("loudnorm")

    filters.append(f"apad=whole_dur={target_duration}")

    filter_chain = ",".join(filters)

    subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-nostats",
            "-y",
            "-i",
            str(infile),
            "-af",
            filter_chain,
            "-ac",
            "1",
            "-ar",
            str(SAMPLE_RATE),
            "-f",
            "u8",
            "-acodec",
            "pcm_s8",
            str(outfile),
        ],
        check=True,
    )
    
# taken and adapted from:
# https://github.com/sensorium/Mozzi/blob/master/extras/python/char2mozzi.py
def char2mozzi(infile, outfile, tablename, samplerate):
    with open(os.path.expanduser(infile), "rb") as fin:
        print("opened " + infile)
        valuesfromfile = array.array("b")
        valuesfromfile.fromfile(fin, os.path.getsize(infile))

    values = valuesfromfile.tolist()

    with open(os.path.expanduser(outfile), "w") as fout:
        fout.write(f"#ifndef {tablename}_H_\n")
        fout.write(f"#define {tablename}_H_\n\n")
        fout.write("#include <Arduino.h>\n")
        fout.write('#include "mozzi_pgmspace.h"\n\n')
        fout.write(f"#define {tablename}_NUM_CELLS {len(values)}\n")
        fout.write(f"#define {tablename}_SAMPLERATE {samplerate}\n\n")

        outstring = f"CONSTTABLE_STORAGE(int8_t) {tablename}_DATA [] = {{"

        for i in range(len(values)):
            if (
                i < len(values) - 2
                and values[i] == values[i + 1] == values[i + 2] == 33
            ):
                values[i + 2] = random.choice([32, 34])

            outstring += f"{values[i]}, "

        outstring += "};"
        fout.write(textwrap.fill(outstring, 80))
        fout.write(f"\n\n#endif /* {tablename}_H_ */\n")

    print("wrote " + outfile)

def main():
    args = parse_args()

    input_dir = Path(args.input_dir)
    normalize = args.normalize
    file_stem = input_dir.name

    wav_dir = OUTPUT_DIR / "Wav"
    raw_dir = OUTPUT_DIR / "Raw"
    header_dir = OUTPUT_DIR / "Wavetables"

    for d in [wav_dir, raw_dir, header_dir]:
        d.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.wav"))

    if not files:
        raise Exception("No input files found.")

    if len(files) > MAX_FILES:
        raise Exception(f"Maximum {MAX_FILES} files supported.")

    # get durations of all WAVs
    durations = [get_duration(f) for f in files]
    longest = max(durations)

    if longest > MAX_SECONDS:
        raise Exception(f"Maximum sample length is {MAX_SECONDS} seconds.")

    # final number of cells after padding
    MAX_NUM_CELLS = int(SAMPLE_RATE * longest)

    if longest > MAX_SECONDS:
        raise Exception(f"Maximum sample length is {MAX_SECONDS} seconds.")

    total_bytes = longest * SAMPLE_RATE * len(files)

    if total_bytes > MEMORY_LIMIT:
        raise Exception(f"OVER MEMORY LIMIT OF {MEMORY_LIMIT}")

    includes = []

    # get max num here, and sort
    includes.append(f'#define MAX_NUM_CELLS {MAX_NUM_CELLS} // if using multiple banks, replace with longest')
    includes.append(f'Sample<MAX_NUM_CELLS, AUDIO_RATE> aSample(ANY_SAMPLE_DATA); // replace with any sample data')
    
    for i, file in enumerate(files, start=1):
        word = num2words(i).replace("-", "").replace(" ", "")
        stem = f"{file_stem}{word}"

        wav_out = wav_dir / f"{stem}.wav"
        raw_out = raw_dir / f"{stem}.raw"
        header_out = header_dir / f"{stem}_int8.h"

        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-nostats",
                "-y",
                "-i",
                str(file),
                str(wav_out),
            ],
            check=True,
        )

        convert_audio(wav_out, raw_out, longest, normalize)

        tablename = stem.upper()

        char2mozzi(str(raw_out), str(header_out), tablename, SAMPLE_RATE)

        includes.append(f'#include "Wavetables/{stem}_int8.h"')

    with open(OUTPUT_DIR / "includes.txt", "w") as f:
        f.write("\n".join(includes))

    print("Done.")


if __name__ == "__main__":
    main()