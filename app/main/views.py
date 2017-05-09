from flask import current_app, render_template, request, url_for, jsonify
from .. import db, bootstrap
from ..models import Question, User, Message
from .forms import AddQuestionForm, AddMessageForm
from ..acapelaVaas import get_acapela_sound
from . import main

from datetime import datetime
from parse import parse
import os


@main.route('/')
def concerteur_home():
    print(main.template_folder)
    return render_template('home.html')
    #return "caca"

@main.route('/add-question', methods=['GET', 'POST'])
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

        question.archive_name = '{}_{}_{}'.format(question.id, question.title.replace(' ','_'), question.time_created.isoformat())
        #create archive directory
        
        dirpath = '{}/{}'.format(current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        db.session.commit()

    return render_template('add_question.html', form=form )

    
@main.route('/messages')
def messages():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('messages.html', questions=questions)
    
@main.route('/trash')
def trash():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('trash.html', questions=questions)


#TODO add authentification for security
@main.route('/add-message', methods=['GET', 'POST'])
def add_sms():

    form = AddMessageForm()
    if request.method == 'GET':
        return render_template('add_message.html', form=form)

    else:
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
            mp3_name = message.id.__str__() + '_' + message.time_created.isoformat() + '_' + user.numHash.__str__() + '.mp3'
            mp3_path = current_app.config['MP3_DIR'] + '/' + mp3_name
            mp3_archive_path = '{}/{}/{}'.format( current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name, mp3_name)
            messages_archive_file = '{}/{}/{}'.format( current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name, current_app.config['MESSAGES_ARCHIVE_FILENAME'])

            message.audio_path = mp3_name

            #create the file at that path
            mp3_sound = get_acapela_sound(message=message.text)
            with open(mp3_path, 'wb') as mp3:
                mp3.write(mp3_sound)
            with open(mp3_archive_path, 'wb') as archive_mp3:
                archive_mp3.write(mp3_sound)

            with open(messages_archive_file, 'a') as messages_file:
                messages_file.write('{}\n\n{}\n------\n'.format(message.audio_path, message.text))


            db.session.add(message)
            db.session.commit()
            
            #return "<h1>{}: {}</h1>".format(hashNum, request.form['text'])
            return render_template('add_message.html', form=form)

        else:
            erreur = "Erreur : pas de question disponible pour ajouter des messages"
            print( erreur )
            return erreur




@main.route('/del-message/<message_num>', methods=['GET'])
def del_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    message.trashed = True
    db.session.add(message)
    db.session.commit()
    return 'Message {} mis à la poubelle. <br> <a href="/messages">retour</a>'.format(message_num)

@main.route('/get-sound-list', methods=['POST'])
def get_sound_list():
    
    filename = request.form['lastFilename']
    if filename:
        message_id = parse("{}_{}_{}",filename)[0]
    else:
        message_id = 1

    print(message_id)

    if int(message_id) < 0:
        message_id = 1

    max_id = int(db.session.query(Message.id).order_by(Message.id.desc()).first()[0])

    if int(message_id) > max_id:
        message_id = 1
        filename = "{}_mfoaiezjfamozife_moiefamoiezjf".format(max_id)

    question_id = db.session.query(Message.question_id).filter(Message.id == str(message_id)).first()[0]
    current_question = db.session.query(Question).filter(Question.current==True).first()

    if question_id < current_question.id:
        new_question = True
        filename_list = [message.audio_path for message in current_question.messages]
    else:
        new_question = False
        filename_tuples = db.session.query(Message.audio_path).filter(Message.id > message_id).all()
        filename_list = [tupl[0] for tupl in filename_tuples]

    
    if filename_list:
        data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename_list[-1]}
    else:
        data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename}
        print(jsonify(data))
    return jsonify(data)

@main.route('/get-sound', methods=['POST'])
def get_sound():
    filename = request.form['soundname']
    mp3Url = 'mp3' + '/' + filename
    return app.send_static_file(mp3Url)

