import os
import blurbs
import dalle
import datetime
import openai
import requests
import speech
import video
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()
# root = os.path.dirname(__file__)
root = "/home/dj703/generative-video/"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        sentences = []
        i=0
        while (len(sentences) <= 1 or len(sentences) >= 8) and i < 5:
            asker = request.form["who"]
            topic = request.form["topic"]
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-")
            filename = timestamp + topic.replace(' ', '_') + '-' + asker.replace(' ', '_')
            content = generate_prompt(topic,asker)
            response = client.chat.completions.create(    # sends API request
                model="gpt-3.5-turbo", #-instruct
                messages=[{"role": "user", "content": content[1]}],
                temperature=0.7,
                max_tokens = 512
            )
            text = str(response.choices[0].message.content)
            if not content[0]:  # didn't find the topic
                return redirect(url_for("index", result=text))
            sentences = text.split("|")

            print("Run ", str(i), ", length ", len(sentences))
            print(sentences)
            i+=1
        if len(sentences) == 1: # testing out format with period not |. Known glitches: period in name
                sentences = text.split('.')
        sentences = [s for s in sentences if s != ""]

        with open(os.path.join(root, 'speech-output/transcripts.txt'), 'a') as f: #write text into transcript
            f.write('\n' + filename + '\n')
            f.write(text + '\n\n')
        with open(os.path.join(root, 'clip-output/' + filename + '.txt'), 'w') as f: #write list of filenames
            for i in range(len(sentences)):
                f.write("file \'" + filename + '_' + str(i) + ".mp4\'\n")
            f.write("file \'" + "blank5.mp4\'\n")

        for i in range(len(sentences)):
            print(i)
            print(sentences[i])
            clipname = filename + '_' + str(i)
            dalle.generate_image(topic, sentences[i], clipname)
            speech.generate_audio(sentences[i], clipname)
            video.create_clip(clipname)
        video_url = video.concat_clips(filename)
        # video_url = "../static/20231127-165806-Europa-astronomer_working_on_the_Giant_Magellan_Telescope.mp4"
        return redirect(url_for("index", result=text.replace('|',''), video_url=video_url)) #, vid="/static/" + filename + ".mp4"

    result = request.args.get("result")
    video_url = request.args.get("video_url")
    print(result)
    print("video url: ")
    print(video_url)
    return_val = render_template("index.html", result=result, video_url=video_url) #, vid=vid
    print("every reload runs through here")
    return return_val


def generate_prompt(topic,asker):
    article = get_intro_wikipedia_article(topic)
    # article = get_wikipedia_article(topic)
    if not article:
        return (False, """You have been asked to give information on {}, but you were unable to find an article about it.
                  Ask them to try a different topic or reword the topic.""".format(topic))

    return (True, """You are an educational yet funny Gen Z YouTuber who uses a lot of sarcasm and throws shade.
    You direct your speech towards your viewers, who are {}.
    Generate a speech for a short video about {} using less than 100 words. You must format using the character | between each and every sentence.
    Everything you talk about in your script comes from the following text only, but don't talk about your sources and don't explicitly mention anything from the prompt before this.
    Text:
    ###
    {}
    ###
    Follow this format as explicitly as possible. You must use this format with the vertical bar character. Desired format:
    This is the first sentence! | This is the second sentence. | This is the third sentence
     """.format(
        asker, article, topic.capitalize() # puts the inputted name of animal into prompt
    )) # return with a specific structure, seen: ____ character talking: ____

def generate_blurb(topic, asker):
    blurb = None
    if topic == "Latent Lab":
        blurb = blurbs.latent_blurb
    elif topic == "NewsDive" or topic == "Newsdive":
        blurb = blurbs.newsdive_blurb
    elif topic == "Neural Notes":
        blurb = blurbs.neural_notes_blurb
    else:
        blurb = blurbs.wildfire_blurb
    #
    return """You are a research assistant at the MIT Media Lab introducing your project, but don't mention yourself.
    You tailor your explanation towards your audience, who are {}, and inject a little bit of humor and personality into your explanation.
    You get all your information from the following article only, but don't talk about your sources:
    {}
     Generate a speech about {} using less than 100 words.
     """.format(
        asker, blurb, topic.capitalize() # puts the inputted name of animal into prompt
    )

def get_wikipedia_article(title):
    # Wikipedia API endpoint
    url = "https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'explaintext': True, #pretty print otherwise it's HTML
        'titles': title
    }

    try:
        # Make a request to the Wikipedia API
        response = requests.get(url, params=params)
        response_data = response.json()

        # Extract the article content
        page = next(iter(response_data['query']['pages'].values()))
        if 'extract' in page:
            article_content = page['extract']
            return article_content
        else:
            return "Article not found."

    except requests.exceptions.RequestException as e:
        print("Error:", e)


def get_intro_wikipedia_article(title): # TO LOWERCASE
    # Wikipedia API endpoint
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + title

    try:
        # Make a request to the Wikipedia API
        response = requests.get(url)
        response_data = response.json()

        # Extract the introductory section
        if 'extract' in response_data:
            intro_content = response_data['extract']
            return intro_content
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error:", e)


