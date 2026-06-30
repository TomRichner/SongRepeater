# SongRepeater

Builds a "study loop" MP3 from a song: it plays the first *N* minutes of the
input, then *N* minutes of silence, and repeats that pattern several times.

By default it produces `[2 min audio][2 min silence] × 5` — a 20-minute file.

## Setup

Requires Python 3.12. Dependencies (`soundfile`, `numpy`) are installed into a
local virtual environment — no `ffmpeg` or other system packages needed.

Create the virtual environment and install the dependencies with `pip`:

```bash
python3.12 -m venv .venv
.venv/bin/pip install soundfile numpy
```

## Usage

```bash
.venv/bin/python song_repeater.py beethoven.mp3
```

This writes `beethoven_loop.mp3` next to the input.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `<input>_loop.mp3` | Output MP3 path |
| `--segment` | `120` | Seconds of audio per repeat |
| `--silence` | `120` | Seconds of silence per repeat |
| `--repeats` | `5` | Number of repeats |

### Examples

```bash
# Default: 2 min audio + 2 min silence, x5 (20 min total)
.venv/bin/python song_repeater.py beethoven.mp3

# Custom output name
.venv/bin/python song_repeater.py beethoven.mp3 -o study_loop.mp3

# 90 s of audio, 30 s of silence, repeated 8 times
.venv/bin/python song_repeater.py beethoven.mp3 --segment 90 --silence 30 --repeats 8
```

## How it works

The output pattern is `[audio][silence]` repeated `--repeats` times, ending on
silence:

```
audio | silence | audio | silence | ... (repeats times)
```

The same first `--segment` seconds of the song are used for every repeat. If the
song is shorter than `--segment`, the whole song is used. The output keeps the
input's sample rate and channel count.
