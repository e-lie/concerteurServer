from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import Required
from acapelaVaas import getAcapelaSound
from datetime import datetime


import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Question, User, Message

bootstrap = Bootstrap(app)

class AddQuestionForm(Form):
    title = StringField('Titre de la question', validators=[Required()])
    text = TextAreaField('Texte de la question', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/')
def concerteur_home():
    return render_template('home.html')

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    question = None
    form = AddQuestionForm()
    if form.validate_on_submit():
        #change preceding current question 
        currQuestion = db.session.query(Question).filter(Question.current==True).first()
        if currQuestion:
            currQuestion.current = False
            db.session.add(currQuestion)
        
        question = Question(date=datetime.utcnow().__str__(), title=form.title.data, text=form.text.data, current=True)

        form.title.data = ''
        form.text.data = ''

        db.session.add(question)
        db.session.commit()

        #return redirect(url_for('questions'))

    return render_template('add_question.html', form=form )

@app.route('/questions')
def questions():
    questions = db.session.query(Question).order_by(Question.date).all()
    return render_template('questions.html', questions=questions)

@app.route('/addsms', methods=['POST'])
def addsms():
    question = db.session.query(Question).filter(Question.current==True).first()

    if question:
        hashNum = hash(request.form['num'])
        message = Message(date=datetime.utcnow(), text=request.form['text'], question_id=question.id)
        user = db.session.query(User).filter(User.numHash==hashNum).first()
        if not user:
            user = User(hashNum, message)
            db.session.add(user)

        db.session.add(message)

        db.session.commit()
        return "<h1>{}: {}</h1>".format(hashNum, request.form['text'])
    else:
        print('pas de question disponible', file='./concerteur.err')
        #return "Error adding message : no available question"




if __name__ == '__main__':
    app.run()


