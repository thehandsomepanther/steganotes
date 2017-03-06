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

    for i in range(1, spec.shape[1]):
        h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        while h > 256:
            spec[h][i] = 0
            h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        char = str(chr(h))
        message += char

    return message

def main():
    if len(sys.argv) == 3:
        print decode(sys.argv[1], sys.argv[2])
    else:
        print decode(sys.argv[1])

if __name__ == "__main__":
    main()
