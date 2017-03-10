## how to get started

install portaudio

```
brew install portaudio
```

use `virtualenv` and `virtualenvwrapper` to make a new environment and install python dependencies
```
mkvirtualenv steganotes
pip install -r requirements.txt
```

to activate your virtual environment:
```
workon steganotes
```

recommended: install avconv to make converting to wav easier
```
brew install libav
```

then run `avconv -i <from-file> <to-file>` to convert
