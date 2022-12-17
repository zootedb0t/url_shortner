from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__, static_url_path="/static")
# adding configuration for using a sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url.db"
db = SQLAlchemy(app)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

from shortner import routes, model
