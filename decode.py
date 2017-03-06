import librosa
from librosa.core import stft
from librosa.core import load
import numpy as np
import sys

RATE = 44100
WINDOW_LENGTH = 2048
HOP_SIZE = 1024

def decode(wavfile):
    signal, sr = librosa.load(wavfile, sr=RATE)
    spec = stft(signal, WINDOW_LENGTH, HOP_SIZE)
    message = ""

    for i in range(1, spec.shape[1]):
        h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        while h > 256:
            spec[h][i] = 0
            h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        char = str(chr(h))
        message += char
    return message

def main():
    print decode(sys.argv[1])

if __name__ == "__main__":
    main()
