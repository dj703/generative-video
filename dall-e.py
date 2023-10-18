import os
import requests

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Image.create(
  prompt="a sunset in Taipei",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

print(image_url)
