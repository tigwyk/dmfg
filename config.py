import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['PYTHON_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CELERY_BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


class ProductionConfig(Config):
    DEBUG = False
    GOOGLE_LOGIN_CLIENT_ID = os.environ['GOOGLE_LOGIN_CLIENT_ID']
    GOOGLE_LOGIN_CLIENT_SECRET = os.environ['GOOGLE_LOGIN_CLIENT_SECRET']
    GOOGLE_LOGIN_REDIRECT_URI =  os.environ['GOOGLE_LOGIN_REDIRECT_URI']
    GOOGLE_LOGIN_CLIENT_SCOPES =  os.environ['GOOGLE_LOGIN_CLIENT_SCOPES']
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
