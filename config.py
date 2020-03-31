import platform
import os


class Config(object):

    SECRET_KEY = "".join(tuple(platform.uname()._asdict().values()) +
                         platform.python_build())

    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(BASEDIR, 'wg_app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

