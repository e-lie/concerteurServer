from app import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date())
    title = db.Column(db.Unicode(300))
    text = db.Column(db.Unicode(1000))
    current = db.Column(db.Boolean())

    messages = db.relationship('Message', backref='question')


    def __init__(self, date, text, title, current):
        self.date = date
        self.text = text
        self.title = title
        self.current = current

    def __repr__(self):
        return '<Question {}: {}>'.format(self.id, self.text)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    numHash = db.Column(db.String(100))
    messages = db.relationship('Message', backref='user')

    def __init__(self, numHash, message):
        self.numHash = numHash
        self.messages = [message]

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.numHash)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Unicode(1000))
    audio = db.Column(db.String(500))

    def __init__(self, date, text, question_id):
        self.date = date
        self.text = text
        self.question_id = question_id

    def __repr__(self):
        return '<Message {}: {}>'.format(self.id, self.text)
