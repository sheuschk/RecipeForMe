import platform
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or "".join(tuple(platform.uname()._asdict().values()) +
                         platform.python_build())

    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    DATABASE_URL = 'postgres:nothing'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(BASEDIR, 'RecipeForMe.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    TESTING = os.environ.get('TESTING')

    posts = os.environ.get('POSTS_PER_PAGE')
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE')) if posts else 10

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
