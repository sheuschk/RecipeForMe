from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
import os
from repo.base import AbstractRepository, ConnectionAPI
from repo import create_repository
from typing import Optional, cast


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


class RecipeForMe(Flask):

    def __init__(self, import_name: str):
        """Initialize the application object."""
        super().__init__(import_name)
        self._repository: Optional[AbstractRepository] = None

    def setup_repository(self) -> None:
        """ Setip repo is for using the repository pattern. It is just implemented, not in use"""
        self._repository = create_repository(self.config.get('DATABASE_URL', None))
        print(self._repository)
        # Setup another repository if the application gets tested

        def close_connection(_exc: BaseException = None):
            """Close the connection to the repository."""
            connection = g.pop('connection', None)
            if connection:
                connection.close()

        self.teardown_request(close_connection)

    def get_connection(self) -> ConnectionAPI:
        """Return an open connection, specific for this request. This function gets called in the business logic.
        with current_app.get_connection"""
        if 'connection' not in g:
            if self._repository is None:
                raise TypeError("Repository not set")
            g.connection = self._repository.create()
        return cast(ConnectionAPI, g.connection)

    def setup_config(self, config_class):
        self.config.from_object(config_class)

    def setup_mail(self):
        """Setup mail server connection"""
        if self.config['MAIL_SERVER']:
            auth = None
            if self.config['MAIL_USERNAME'] or self.config['MAIL_PASSWORD']:
                auth = (self.config['MAIL_USERNAME'], self.config['MAIL_PASSWORD'])
            secure = None
            if self.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(self.config['MAIL_SERVER'], self.config['MAIL_PORT']),
                fromaddr='no-reply@' + self.config['MAIL_SERVER'],
                toaddrs=self.config['ADMINS'], subject='WG APP Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            self.logger.addHandler(mail_handler)

    def setup_logging(self):
        """Setup the logging for the application"""
        if self.config['LOG_TO_STDOUT']:
            # log to stdout is for heroku deployment
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            self.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/RecipeForMe.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)

        self.logger.setLevel(logging.INFO)
        self.logger.info('WG APP startup')


def create_app(config_class=Config):
    """Create RecipeForMe"""
    app = RecipeForMe(__name__)
    app.setup_config(config_class)
    app.setup_repository()

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:
        app.setup_mail()
        app.setup_logging()

    return app


from app import models
