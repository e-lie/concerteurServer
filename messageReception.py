from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from acapelaVaas import getAcapelaSound
from datetime import datetime


import os

smsNum = 33637105067
smsText = "Ceci est un message de test"

hashNum = hash(smsNum)

from app import app, db

from models import Question, User, Message

question = db.session.query(Question).filter(Question.current==True).first()

if question:
    user = db.session.query(User).filter(User.numHash==hashNum).first()
    if not user:
        user = User(hashNum)
        db.session.add(user)

    message = Message(date=datetime.utcnow(), text=smsText, question_id=question.id,
                    user_id=user.id)
    db.session.add(message)

    db.session.commit()
else:
    print('pas de question disponible', file='./concerteur.err')
