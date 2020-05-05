import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess'
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.environ['HOME'], '.tdl/tdl.db')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
