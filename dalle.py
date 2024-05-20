import os
import openai
import base64

client = openai.OpenAI()
root = "/home/dj703/generative-video/"

text = "mountains and sea of Taiwan, hyperrealistic photograph"

def generate_image(topic, text, filename):
  try:
    response = client.images.generate(
      model="dall-e-3",
      prompt=topic + ": " + text,
      size="1024x1024",
      quality="standard",
      n=1,
      response_format="b64_json",
    )
    img_data = bytes(response.data[0].b64_json, 'utf-8')
    with open(os.path.join(root, f"image-output/{filename}.png"), "wb") as fh:
      fh.write(base64.decodebytes(img_data))
  except Exception as err:
    print("ERROR: ", err)
    try:
      print("DALL-E returned exception to this prompt; trying with topic")
      response = client.images.generate(
        model="dall-e-3",
        prompt=topic,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",
      )
      img_data = bytes(response.data[0].b64_json, 'utf-8')
      with open(os.path.join(root, f"image-output/{filename}.png"), "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    except:
      print("DALL-E returned exception to the topic as well; using black square")
      os.system(f"cp {root}image-output/black_square.png {root}image-output/{filename}.png")




# response = client.images.generate(
#   model="dall-e-3",
#   prompt="mountains and sea of Taiwan, hyperrealistic photograph",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )

# image_url = response.data[0].url