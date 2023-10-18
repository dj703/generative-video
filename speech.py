from elevenlabs import clone, generate, play, set_api_key
from elevenlabs.api import History
import requests

set_api_key("594c070f41584bfe35263d1c3fcd9a97")

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "<xi-api-key>"
}

data = {
  "text": "Hey there, kiddos! Today, we're going to talk about a pretty cool place called the MIT Media Lab.",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('speech-output/output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

