## how to get started

install portaudio

```
brew install portaudio
```

use `virtualenv` to make a new environment and install python dependencies
```
mkvirtualenv steganotes
pip install -r requirements.txt
```

recommended: install avconv to make converting to wav easier
```
brew install libav
```

then run `avconv -i <from-file> <to-file>` to convert
