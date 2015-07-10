import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'sdfns90dfm8904kljklklas9089s90903kljklsaldlklasdklqwopeudaafjzsklacje89903oklsjdopfskldfjllaxcjvxlcvxcv'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = 'sheltered-taiga-4486.herokuapp.com'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SERVER_NAME = 'git.leeingram.com'


class TestingConfig(Config):
    TESTING = True
