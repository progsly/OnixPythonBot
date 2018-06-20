# This bot use Machine Learning and TensorFlow framework to recognize objects on the photos.

## Run bot
Copy **config.default.py** to **config.py**

Fill the parameters in config.py.

"TOKEN": "bot token "

"HOST": "server url - mybot.example.com"


Run commands: 
 
1. `docker build -t OnixPythonBot .`
2. `docker run -p 8000:8000 OnixPythonBot`