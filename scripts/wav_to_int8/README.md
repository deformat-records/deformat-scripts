# WAV to _int8.h

Converts a directory of wav samples to _int8.h files, mainly to be used in firmware for the GMO.
This script was designed to assist the [project-omg](https://github.com/deformat-records/project-omg) repo.

It first converts the samples to the correct bitrate/channels/etc using ffmpeg
then converts them using [char2mozzi.py](https://github.com/sensorium/Mozzi/blob/master/extras/python/char2mozzi.py)

## How To Use

requirements:
```bash
pip install num2words
```

usage:
```bash
python wav_to_int8.py <input_directory>
```
outputs:

samples/
├── Wav/
├── Raw/
├── Wavetables/
└── includes.txt

Input files are automatically renamed using spelled-out numbers:
- kickone_int8.h
- kicktwo_int8.h 
- kickthree_int8.h

It will generate a text file which can be used in the header to include these all.
You will need to place the Wavetables directory in the same as your sketech.

## Limits

Current script limits:
- Maximum files: 64
- Maximum memory: 131072 bytes
- Maximum sample rate: 16384 Hz

Memory is calculated using:
```python
longest_sample_duration * sample_rate * file_count
```

If memory exceeds the limit, conversion stops.