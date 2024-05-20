from elevenlabs import clone, generate, play, set_api_key, save
from elevenlabs.api import History
import requests
import os

root = os.path.dirname(__file__)

# can also do this via API/Python POST requests but that didn't work

set_api_key("594c070f41584bfe35263d1c3fcd9a97")

words = """

        """
filename = ""

def generate_audio(words, filename):
    audio = generate(
        text=words,
        voice="Sarah",
        model='eleven_monolingual_v1'
    )
    #play(audio)
    save(
        audio=audio,
        filename=os.path.join(root, "speech-output/" + filename + ".mp3")
    )

if words and filename:
    generate_audio(words,filename)

