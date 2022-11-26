from flask import Flask

app = Flask(__name__)

from shortner import routes
