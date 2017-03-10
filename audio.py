import pyaudio
import pygame
import sys
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "captured_output.wav"


def play_audio(wav_file):
    print '* * playing audio...'
    wf = wave.open(wav_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
    print '* * done.'

def listen_for_audio():
    # https://github.com/jeysonmc/python-google-speech-scripts/blob/master/stt_google.py
    p = pyaudio.PyAudio()
    pygame.init()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "* * listening for audio..."

    frames = []
    recording = True

    while recording:
        data = stream.read(CHUNK)
        frames.append (data)

        # if space bar is pressed to stop recording
        if pygame.event.peek():
            print "* * audio capture terminated..."
            stream.stop_stream()
            stream.close()
            p.terminate()
            recording = False

    print "* * writing captured audio to wav file"
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME
