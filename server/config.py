import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
