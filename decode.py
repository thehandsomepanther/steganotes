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

    for i in range(3, 1000, 3):
        h = np.argmax(np.abs(spec[i]))

        while h > 256:
            spec[i][h] = 0
            h = np.argmax(np.abs(spec[i]))

        char = str(chr(h))
        message += char
    return message

print decode('encode.wav')
