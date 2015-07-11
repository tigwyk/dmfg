import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'sdfns90dfm8904kljklklas9089s90903kljklsaldlklasdklqwopeudabfjzsklacje89903oklsjdqpfskldfjwlaxcjvxlcvxcv'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CELERY_BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


class ProductionConfig(Config):
    DEBUG = False
    GOOGLE_LOGIN_CLIENT_ID = '540878604386-k4bjmu9ih3t8oih8ej7215lf9sbs5qcj.apps.googleusercontent.com'
    GOOGLE_LOGIN_CLIENT_SECRET = 'jsFoXb5KLYVQwrzxXcj09IDj'
    GOOGLE_LOGIN_REDIRECT_URI = 'http://sheltered-taiga-4486.herokuapp.com/oauth2callback'
    GOOGLE_LOGIN_CLIENT_SCOPES = 'https://www.googleapis.com/auth/plus.login'
    SERVER_NAME = 'sheltered-taiga-4486.herokuapp.com'
    CELERY_BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SERVER_NAME = 'git.leeingram.com'


class TestingConfig(Config):
    TESTING = True
