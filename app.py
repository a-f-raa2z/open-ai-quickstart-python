import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    global diary
    if request.method == "POST":
        diary = request.form["diary"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(diary),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = diary + " : "+str(request.args.get("result"))
    return render_template("index.html", result=result)


def generate_prompt(diary):
    return """The following is a list of diaries and the tags that they are associated with
Diary: I love zoo!
Tags: Mood_Positive
Diary: Sadd
Tags: Mood_Negative
Diary: Milk tea is good
Tags: Food_beverage
Diary: Zeyu ate basque cake
Tags: Food_Dessert
Diary:I watched Addams today.
Tags: Activity_Movie
Diary:I went to westfield.
Tags: Activity_Shopping
Diary:I am visiting New Yorkk .
Tags: Activity_Travel
Diary: We had good brunch in the city.
Tags: Food_Meal
Diary: {}
Tags: 
""".format(
        diary.capitalize()
    )
