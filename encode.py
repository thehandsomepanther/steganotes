import numpy as np
from scipy.io.wavfile import write
from librosa.core import istft
from librosa.core import stft
import os
import sys

RATE = 44100
WINDOW_LENGTH = 2048
HOP_SIZE = 1024

def wavwrite(filepath, data, sr, norm=True, dtype='int16'):
    if norm:
        data /= np.max(np.abs(data))
    data = data * np.iinfo(dtype).max
    data = data.astype(dtype)
    write(filepath, sr, data)

def make_sinewave(f, t, sr):
    vals = np.array([2 * np.pi * x * f / sr for x in range(int(sr * t))])
    return np.sin(vals)

def encode(data_file, output_file):
    reps = 1
    data_file_size = os.path.getsize(data_file)
    signal = make_sinewave(900, data_file_size*reps/25, RATE)
    spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)

    with open(data_file) as dfile:
        d = dfile.read(1)
        i = 0
        while d:
            h = int(d.encode("hex"), 16)
            for r in range(reps):
                spec[h-1][i+r] = 0
                spec[h][i+r] = np.max(np.abs([spec[x][i+r] for x in range(spec.shape[0])])) * 200
                spec[h+1][i+r] = 0
            d = dfile.read(1)
            i += reps

    wavwrite(output_file, istft(spec, 1024, 2048), RATE)

def main():
    encode(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
