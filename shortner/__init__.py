from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url.db'
db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actual_url = db.Column(db.String(120), index=True, unique=True)
    short_url = db.Column(db.String(60), index=True, unique=True)

    def __repr__(self):
        return f"URL : {self.actual_url}, Short: {self.short_url}"

from shortner import routes
