import numpy as np
from scipy.io.wavfile import write
import scipy.signal as sig
from librosa.core import istft
from librosa.core import stft
import os

RATE = 44100

def wavwrite(filepath, data, sr, norm=True, dtype='int16'):
    if norm:
        data /= np.max(np.abs(data))
    data = data * np.iinfo(dtype).max
    data = data.astype(dtype)
    write(filepath, sr, data)

def make_sinewave(f, t, sr):
    vals = np.array([2 * np.pi * x * f / sr for x in range(int(sr * t))])
    return np.sin(vals)

def encode(data_file):
    signal = make_sinewave(900, 5, RATE)
    spec = stft(signal, win_length=2048, hop_length=1024)

    with open(data_file) as dfile:
        d = dfile.read(1)
        i = 1
        spec[0][20] = np.float64(os.path.getsize(data_file))/2**16
        while d:
            h = int(d.encode("hex"), 16)
            spec[i][h] = np.abs(np.max(spec[i]))
            d = dfile.read(1)
            i += 1

    return istft(spec)


wavwrite('encode.wav', encode('test.txt'), RATE)
