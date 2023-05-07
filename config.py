"""Configration for application"""

from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_DEBUG")
    FLASK_APP = "app.py"

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = True

class DbConfig:

    """Configration for database"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///url.db"
    SQLALCHEMY_BINDS = {
    "key": "sqlite:///key.db"
    }
