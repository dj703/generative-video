# generative-video

An informational video generator that uses the Wikipedia API, GPT, DALL-E, ElevenLabs text-to-speech, and ffmpeg to generate a video on a specified topic geared towards a specific audience.

## To run:
```
python -m venv venv      
. venv/bin/activate
pip install -r requirements.txt
flask run
```
You may will need to set the environment variable `OPENAI_API_KEY` to your key; the key in this repository has been disabled.

Video files are currently deposited in the `static` folder.



