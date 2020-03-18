import os
basepath = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6966053a-67c5-11ea-bc55-0242ac130003'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basepath, 'flaskrest.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


