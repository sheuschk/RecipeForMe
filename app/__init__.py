from flask import Flask
# from . import routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""
app_blueprint = routes.create_blueprint()
app.register_blueprint(app_blueprint)
"""

from app import routes, models
