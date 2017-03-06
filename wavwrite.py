import numpy as np
from scipy.io.wavfile import write

def wavwrite(filepath, data, sr, norm=True, dtype='int16'):
    if norm:
        data /= np.max(np.abs(data))
    data = data * np.iinfo(dtype).max
    data = data.astype(dtype)
    write(filepath, sr, data)

def main():
    wavwrite(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
