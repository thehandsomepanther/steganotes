import scipy.signal as sig
import librosa
from librosa.core import stft
from librosa.core import load
import numpy as np

RATE = 44100

def decode(wavfile):
    signal, sr = librosa.load(wavfile, sr=44100)
    spec = stft(signal, 2048, 1024)
    message = ""

    for i in range(1, 1000):
        h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        while h > 256:
            spec[h][i] = 0
            h = np.argmax(np.abs([spec[x][i] for x in range(spec.shape[0])]))

        char = str(chr(h))
        message += char
    return message

print decode('encode.wav')
