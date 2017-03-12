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
    max_val = np.max(np.abs(spectrogram))
    start = np.zeros((spectrogram.shape[0], 32))
    stop = np.zeros((spectrogram.shape[0], 32))

    start[500] = np.full((32), max_val)
    stop[550] = np.full((32), max_val)
    return np.concatenate((start, spectrogram, stop), axis=1)

def encode(data_file, output_file, key_file=None):
    print '* * encoding message in audio file...'
    data_file_size = os.path.getsize(data_file)

    if key_file is not None:
        signal, sr = librosa.load(key_file, sr=RATE)
        spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)
    else:
        signal = make_sinewave(900, data_file_size/20, RATE)
        spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)

    with open(data_file) as dfile:
        d = dfile.read(1)
        i = 0
        while d:
            h = int(d.encode("hex"), 16)
            if key_file is not None:
                spec[h][i] = np.max(np.abs([spec[x][i] for x in range(spec.shape[0])])) + 200
            else:
                spec[h][i] = np.max(np.abs([spec[x][i] for x in range(spec.shape[0])])) * 200
            spec[h-1][i] = 0
            spec[h+1][i] = 0
            d = dfile.read(1)
            i += 1

    spec = spec[:,:i]

    spec = add_start_stop(spec)

    wavwrite(output_file, istft(spec, 1024, 2048), RATE)


def main():
    if len(sys.argv) == 4:
        return encode(sys.argv[1], sys.argv[2], sys.argv[3])

    return encode(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
