import librosa
from librosa.core import istft
from librosa.core import stft
from librosa.core import load
import numpy as np
import sys
from wavwrite import *

RATE = 44100
WINDOW_LENGTH = 2048
HOP_SIZE = 1024

def decode(wavfile, key_file=None):
    signal, sr = librosa.load(wavfile, sr=RATE)
    spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)
    message = ""

    if key_file is not None:
        key_signal, sr = librosa.load(key_file, sr=RATE)
        signal = np.pad(signal, (0, key_signal.shape[0] - signal.shape[0]), 'edge')
        spec = np.subtract(stft(key_signal, WINDOW_LENGTH, HOP_SIZE), spec)
        wavwrite('minus.wav', istft(spec, 1024, 2048), RATE)

    i, decode = 0, False
    while i < spec.shape[1]:
        h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))
        if h == 500:
            decode = True
            i=i+1
            continue

        if decode:
            while h > 255:
                spec[h][i] = 0
                h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))
            char = str(chr(h))
            message += char

        i = i+1

    return message

def main():
    if len(sys.argv) == 3:
        print decode(sys.argv[1], sys.argv[2])
    else:
        print decode(sys.argv[1])

if __name__ == "__main__":
    main()
