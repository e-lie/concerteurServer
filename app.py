from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import Required
from acapelaVaas import get_acapela_sound
from datetime import datetime
from parse import parse


import os

app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Question, User, Message

bootstrap = Bootstrap(app)

class AddQuestionForm(Form):
    title = StringField('Titre de la question', validators=[Required()])
    text = TextAreaField('Texte de la question', validators=[Required()])
    submit = SubmitField('Submit')

class AddMessageForm(Form):
    num = StringField('numéro de téléphone associé au message (33634354637 pour un portable)', validators=[Required()])
    text = TextAreaField('Texte du message', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
def concerteur_home():
    return render_template('home.html')

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    question = None
    form = AddQuestionForm()
    if form.validate_on_submit():
        #change current question to false before adding the new current question
        currQuestion = db.session.query(Question).filter(Question.current==True).first()
        if currQuestion:
            currQuestion.current = False
            db.session.add(currQuestion)
        
        question = Question(title=form.title.data, text=form.text.data, current=True)

        form.title.data = ''
        form.text.data = ''

        db.session.add(question)
        db.session.commit()

    return render_template('add_question.html', form=form )

@app.route('/questions')
def questions():
    questions = db.session.query(Question).order_by(Question.time_created).all()
    return render_template('questions.html', questions=questions)

    
@app.route('/messages')
def messages():
    messages = db.session.query(Message).order_by(Message.id).all()
    return render_template('messages.html', messages=messages)


#TODO add authentification for security
@app.route('/add-message', methods=['GET', 'POST'])
def add_sms():

    form = AddMessageForm()
    if request.method == 'GET':
        return render_template('add_message.html', form=form)

    elif form.validate_on_submit():
        question = db.session.query(Question).filter(Question.current==True).first()

        if question:
            #FIXME install hashlib and use sha1 for this hash
            hashNum = hash(request.form['num'])
            message = Message(text=request.form['text'], question_id=question.id)
            user = db.session.query(User).filter(User.numHash==hashNum).first()
            if not user:
                user = User(hashNum, message)
            else:
                user.messages.append(message)

            db.session.add(user)
            db.session.add(message)
            db.session.commit()
            
            #create a unique filename (id + timestamp + hash of the sender number)
            #to link the "message" entry to a mp3 file on the server
            mp3Name = message.id.__str__() + '_' + message.time_created.isoformat() + '_' + user.numHash.__str__() + '.mp3'
            mp3Url = url_for('static', filename='mp3') + '/' + mp3Name
            #create the file at that path
            with open('.'+mp3Url, 'wb') as f:
                mp3 = get_acapela_sound(message=message.text)
                f.write(mp3)

            message.audio_path = mp3Name
            db.session.add(message)
            db.session.commit()
            
            #return "<h1>{}: {}</h1>".format(hashNum, request.form['text'])
            return render_template('add_message.html', form=form)

        else:
            erreur = "Erreur : pas de question disponible pour ajouter des messages"
            print( erreur )
            return erreur


@app.route('/get-sound-list', methods=['POST'])
def get_sound_list():
    
    filename = request.form['lastFilename']
    if filename:
        messageId = parse("{}_{}_{}",filename)[0]
    else:
        messageId = 1

    newerSounds = db.session.query(Message.audio_path).filter(Message.id > messageId).all()
    mp3Names = []
    for sound in newerSounds:
        mp3Names.append(sound[0])
    if mp3Names:
        data = {'filenames':mp3Names, 'lastfilename':mp3Names[-1]}
    else:
        data = {'filenames':mp3Names, 'lastfilename':filename}
    return jsonify(data)

@app.route('/get-sound', methods=['POST'])
def get_sound():
    filename = request.form['soundname']
    mp3Url = 'mp3' + '/' + filename
    return app.send_static_file(mp3Url)
    
