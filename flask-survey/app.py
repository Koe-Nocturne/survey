from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


@app.route("/", methods=["GET"])
def initial_survey():
    '''Uploading the initial page'''
    return render_template("start.html",
                           title=satisfaction_survey.title,
                           mid_text=satisfaction_survey.instructions)

@app.route("/start", methods=["POST", "GET"])
def create_session():
    responses = session["responses"]
    return redirect("/questions")


@app.route("/questions/<int:qid>", methods=["GET"])
def route_questions(qid):
    sat_surv = satisfaction_survey
    if(len(session) != qid or qid > len(session)):
        flash("Accessing an invalid question, you have been redirected")
        return redirect(f"/questions/{len(session)}")
    return render_template("question.html",
        title=sat_surv.title,
        mid_text=sat_surv.questions[qid].question,
        selection=sat_surv.questions[qid].choices)


@app.route("/questions")
def questions_redirector(responses):
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/answer", methods=["POST"])
def get_answers(responses):
    choice = request.form["answer"]
    responses.append("choice")
    session["responses"] = responses

    return redirect(f"/questions")
       
@app.route("/thanks")
def thanks():
    return render_template("thanks.html")