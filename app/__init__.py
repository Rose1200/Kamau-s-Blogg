from flask import Flask
from .config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
from .model import User

# Initializing application
def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    return app
    