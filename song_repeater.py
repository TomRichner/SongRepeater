#!/usr/bin/env python3
"""Build a "study loop" MP3 from a song.

Plays the first N minutes of the input, then N minutes of silence, repeated
some number of times: [audio][silence] x repeats.

Example:
    python song_repeater.py beethoven.mp3
    python song_repeater.py beethoven.mp3 -o loop.mp3 --segment 120 --silence 120 --repeats 5
"""

import argparse
import os
import sys

import numpy as np
import soundfile as sf


def build_loop(input_path, output_path, segment_s, silence_s, repeats):
    info = sf.info(input_path)
    sr = info.samplerate
    channels = info.channels

    segment_frames = int(round(segment_s * sr))
    silence_frames = int(round(silence_s * sr))

    # Read only the first `segment_s` seconds. If the song is shorter, we get
    # whatever is available.
    audio, _ = sf.read(input_path, frames=segment_frames, dtype="float32",
                       always_2d=True)
    got_s = len(audio) / sr
    if len(audio) < segment_frames:
        print(f"Note: song is only {got_s:.1f}s long; using the whole thing "
              f"instead of the requested {segment_s:.0f}s.")

    silence = np.zeros((silence_frames, channels), dtype="float32")

    block = np.concatenate([audio, silence], axis=0)
    full = np.tile(block, (repeats, 1))

    sf.write(output_path, full, sr, format="MP3")

    total_s = len(full) / sr
    print(f"Wrote {output_path}")
    print(f"  pattern: {got_s:.0f}s audio + {silence_s:.0f}s silence, "
          f"x{repeats}")
    print(f"  total duration: {total_s/60:.1f} min  ({sr} Hz, {channels} ch)")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="input audio file (e.g. beethoven.mp3)")
    p.add_argument("-o", "--output",
                   help="output MP3 path (default: <input>_loop.mp3)")
    p.add_argument("--segment", type=float, default=120.0,
                   help="seconds of audio per repeat (default: 120)")
    p.add_argument("--silence", type=float, default=120.0,
                   help="seconds of silence per repeat (default: 120)")
    p.add_argument("--repeats", type=int, default=5,
                   help="number of repeats (default: 5)")
    args = p.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Input file not found: {args.input}")

    output = args.output
    if output is None:
        base, _ = os.path.splitext(args.input)
        output = base + "_loop.mp3"

    build_loop(args.input, output, args.segment, args.silence, args.repeats)


if __name__ == "__main__":
    main()
