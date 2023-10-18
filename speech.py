from elevenlabs import clone, generate, play, set_api_key, save
from elevenlabs.api import History
import requests
# can also do this via API/Python POST requests but that didn't work 

set_api_key("594c070f41584bfe35263d1c3fcd9a97")

def generate_audio(words):
    audio = generate(
        text=words,
        voice="Bella",
        model='eleven_monolingual_v1'
    )
    play(audio)
    save(
        audio=audio,
        filename="speech-output/tests-again.mp3"
    )

