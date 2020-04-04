from flask import Flask
from flask_login import LoginManager
# from . import routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

"""
app_blueprint = routes.create_blueprint()
app.register_blueprint(app_blueprint)
"""

from app import routes, models
