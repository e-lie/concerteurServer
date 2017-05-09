import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 't_ifJk2jhR,jl$0'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    QUESTION_ARCHIVE_DIR = 'question_archives'
    MP3_DIR = './app/main/static/mp3'
    MESSAGES_ARCHIVE_FILENAME = 'messages.txt'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
