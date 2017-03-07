import numpy as np
import librosa
from librosa.core import istft
from librosa.core import stft
import os
import sys
from wavwrite import *

RATE = 44100
WINDOW_LENGTH = 2048
HOP_SIZE = 1024

def make_sinewave(f, t, sr):
    vals = np.array([2 * np.pi * x * f / sr for x in range(int(sr * t))])
    return np.sin(vals)

def add_start_stop(spectrogram):
    delimiter = np.zeros((64, spectrogram.shape[0]))
    for i in delimiter:
        i[500] = np.max(np.abs(spectrogram))

    flipped = np.concatenate((delimiter, np.flipud(np.rot90(spectrogram)), delimiter))
    return np.flipud(np.rot90(flipped))

def encode(data_file, output_file, key_file=None):
    reps = 1
    data_file_size = os.path.getsize(data_file)

    if key_file is not None:
        signal, sr = librosa.load(key_file, sr=RATE)
        spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)
    else:
        signal = make_sinewave(900, data_file_size*reps/25, RATE)
        spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)

    with open(data_file) as dfile:
        d = dfile.read(1)
        i = 0
        while d:
            h = int(d.encode("hex"), 16)
            for r in range(reps):
                if key_file is not None:
                    spec[h][i+r] = np.max(np.abs([spec[x][i+r] for x in range(spec.shape[0])])) + 200
                else:
                    spec[h][i+r] = np.max(np.abs([spec[x][i+r] for x in range(spec.shape[0])])) * 200
                spec[h-1][i+r] = 0
                spec[h+1][i+r] = 0
            d = dfile.read(1)
            i += reps

    spec = add_start_stop(spec)

    wavwrite(output_file, istft(spec, 1024, 2048), RATE)


def main():
    if len(sys.argv) == 4:
        return encode(sys.argv[1], sys.argv[2], sys.argv[3])

    return encode(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
