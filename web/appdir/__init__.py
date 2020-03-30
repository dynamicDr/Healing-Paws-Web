from flask import Flask
from appdir.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from appdir import routes

