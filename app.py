from flask import Flask, render_template
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
        question = Question(datetime.utcnow().__str__(), form.title.data, form.text.data)
        
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




if __name__ == '__main__':
    app.run()


