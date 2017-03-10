from optparse import OptionParser
import sys

from encode import encode
from decode import decode
from audio import *

def main():
    # input flags for this program
    parser = OptionParser()
    parser.add_option("-e", "--encode", dest="encode_file", help="text file to with message to encode and send")
    parser.add_option("-o", "--output", dest="output_file", help="output file with encoded audio")
    parser.add_option("-d", "--decode", dest="decode_file", help="wav file to decode")
    parser.add_option("-p", "--play", action="store_true", dest="play_audio", default=False, help="play audio after encoding text message")
    parser.add_option("-l", "--listen", action="store_true", dest="listen", default=False, help="listen for audio signal and decode")
    options, args = parser.parse_args()

    if options.encode_file:
        output_file = options.output_file if options.output_file else 'output.wav'
        encode(options.encode_file, output_file)
        if options.play_audio:
            play_audio(output_file)
    elif options.listen:
        captured_wav = listen_for_audio()
        decode(captured_wav)
    elif options.decode_file:
        decode(options.decode_file)
    else:
        parser.print_help()
    return

if __name__ == "__main__":
    main()
