import os
import requests
import json
import speech

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        asker = request.form["who"]
        topic = request.form["topic"]
        response = openai.Completion.create(    # sends API request
            model="gpt-3.5-turbo-instruct",
            prompt=generate_prompt(topic, asker),
            temperature=0.8,
            max_tokens = 512
        )
        text = response.choices[0].text
        speech.generate_audio(text)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return_val = render_template("index.html", result=result)
    return return_val


def generate_prompt(topic,asker):
    article = get_intro_wikipedia_article(topic)
    if not article: 
        return """You have been asked to give information on {}, but you were unable to find an article about it. 
                  Ask them to try a different topic or reword the topic.""".format(topic)

    return """You are an educational yet funny Gen Z YouTuber who uses a lot of sarcasm and throws shade, but don't mention these facts about you explicitly.
    You tailor your script towards your viewers, who are {}. The narrator is the only character in your script.
    You get all your information from the following article only, but don't talk about your sources:
    {}
     Generate a speech for a short video about {} using less than 100 words. 
     """.format(
        asker, article, topic.capitalize() # puts the inputted name of animal into prompt
    ) # return with a specific structure, seen: ____ character talking: ____

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


def get_intro_wikipedia_article(title):
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
        

