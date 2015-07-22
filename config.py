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
    GOOGLE_LOGIN_CLIENT_ID = '532557088815-8ak75vub4oq6fd36q4198a9rce6eeeui.apps.googleusercontent.com'
    GOOGLE_LOGIN_CLIENT_SECRET = 'ha1NTfZ7fZYDculqzl2-gr37'
    GOOGLE_LOGIN_REDIRECT_URI = 'http://sheltered-taiga-4486.herokuapp.com/callback/google'
    GOOGLE_LOGIN_CLIENT_SCOPES = 'https://www.googleapis.com/auth/plus.login'
    SERVER_NAME = 'sheltered-taiga-4486.herokuapp.com'
    OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
    }    
#    CELERY_BROKER_URL = os.environ['REDIS_URL']
#    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SERVER_NAME = 'git.leeingram.com'


class TestingConfig(Config):
    TESTING = True
