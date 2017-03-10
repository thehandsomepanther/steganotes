import pyaudio
import wave
import sys
import select
import tty
import termios
from decode import *

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = .5
WAVE_OUTPUT_FILENAME = "output.wav"

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    print("* recording, press ESC to stop")
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':
                print("* done recording")
                stream.stop_stream()
                stream.close()
                p.terminate()
                break

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
print decode(WAVE_OUTPUT_FILENAME)
