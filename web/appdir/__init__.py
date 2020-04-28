from flask import Flask
from appdir.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)

from appdir import routes, models

