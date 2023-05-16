"""Creating app and database object"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import app config
from config import DbConfig, Config

db = SQLAlchemy()


def init_app():
    """Initialize the applications"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    app.config.from_object(DbConfig)

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

        return app
