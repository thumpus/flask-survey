from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
responses = []
survey = satisfaction_survey
survey_finished = False

@app.route('/')
def show_home():
    """show the homepage for the survey"""
    return render_template('home.html', title = survey.title, instructions = survey.instructions)

@app.route('/questions/<int:question_id>', methods = ["GET", "POST"])
def show_next_question(question_id):
    """handle post request of previous question's answer if applicable, show next question"""
    if request.method == "POST":
        responses.append(request.form["option"])
    if survey_finished == True:
        return """
            <h1>Thank you!</h1>
            <p>You have answered all the questions. You may now close this page.</p>
             """
    elif question_id > (len(survey.questions) - 1) or question_id != len(responses):
        flash("Invalid question ID. Redirecting to next question.")
        return redirect(f"/questions/{len(responses)}")
    else:    
        question = survey.questions[question_id]
        return render_template("question.html", question_text = question.question, question_id = question_id, choices = question.choices)
    

@app.route(f'/questions/{len(survey.questions)}', methods = ["GET", "POST"])
def show_thanks():
    """accept the last answer and show a thank you page once all questions have been answered"""
    if request.method == "POST":
        responses.append(request.form["option"])
    print(responses)
    survey_finished = True
    print(survey_finished)
    return """
    <h1>Thank you!</h1>
    <p>You have answered all the questions. You may now close this page.</p>
    """

