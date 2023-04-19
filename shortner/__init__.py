"""Creating app and database object"""
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
# adding configuration for using a sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url.db"
# Another database for storing keys
app.config["SQLALCHEMY_BINDS"] = {"key": "sqlite:///key.db"}
db = SQLAlchemy(app)

secret = secrets.token_urlsafe(32)
app.secret_key = secret
