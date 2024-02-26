from flask import Flask,request, render_template, redirect, flash, jsonify, url_for,session
from random import randint,choice,sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz



app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

responses = []

@app.route('/')
def survey_start():
    session[RESPONSES_KEY] = []  # Initialize responses in session
    return render_template('survey_start.html', survey=satisfaction_survey)

@app.route('/questions/<int:question_number>')
def show_question(question_number):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # Trying to access question page too soon
        return redirect('/')

    if (question_number == len(responses)):
        question = satisfaction_survey.questions[question_number]
        return render_template('questions.html', question_number=question_number, question=question)
    elif (question_number < len(responses)):
        flash("You've already answered this question. Here's the next one.")
        return redirect(url_for('show_question', question_number=len(responses)))
    else:
        flash("Please answer the questions in order.")
        return redirect(url_for('show_question', question_number=len(responses)))

@app.route('/answer', methods=["POST"])
def handle_answer():
    # Use the session to store responses
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect('/')

    selected_choice = request.form['answer']
    responses.append(selected_choice)
    session[RESPONSES_KEY] = responses  # Reassign the modified responses back to session
    session.modified = True  # Let Flask know the session has been modified

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(url_for('show_question', question_number=len(responses)))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')