import scipy.signal as sig
from librosa.core import stft
from librosa.core import load
import numpy as np

RATE = 44100

def decode(wavfile):
    signal, sr = load(wavfile, sr=RATE)
    spec = stft(signal, win_length=2048, hop_length=1024)
    message = ""

    for i in range(1, 844):
        message += str(chr(np.argmax(np.abs(spec[i]))))
    return message

print decode('encode.wav')
