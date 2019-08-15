from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"

debug = DebugToolbarExtension(app)

responses = []
question_number = 0


@app.route("/", methods=["GET"])
def initial_survey():
    '''Uploading the initial page'''

    return render_template("start.html",
                           title=satisfaction_survey.title,
                           mid_text=satisfaction_survey.instructions)


@app.route("/question/<question_number>", methods=["POST"])
def route_questions(question_number):
    if (question_number == len(satisfaction_survey.questions)):
        return redirect("/thanks")
    else:
        if(question_number > 0):
            responses.append(request.form[''])
        question_number += 1
        return render_template("question.html",
                           title=satisfaction_survey.title,
                           mid_text=satisfaction_survey.question[question_number].question,
                           selection=satisfaction_survey.question[question_number].choices)
