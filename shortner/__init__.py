"""Creating app and database object"""
from flask import Flask
from config import DbConfig, Config

app = Flask(__name__, instance_relative_config=False)
# App config
app.config.from_object(Config)
# Database config
app.config.from_object(DbConfig)
