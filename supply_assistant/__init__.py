from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from supply_assistant.cfg import config

app = Flask(__name__)
app.secret_key = config["SITE"]["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = config["DATABASE"]["uri"]
app.config['UPLOAD_FOLDER'] = config["SITE"]["upload_folder"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.wsgi_app = DispatcherMiddleware(
    Response('Not Found', status=404),
    {config['SITE']['base_url']: app.wsgi_app}
)
from supply_assistant import models, routes
from supply_assistant.bot import Bot
from supply_assistant import database_shortcuts

db.create_all()

database_shortcuts.initialize(db.session)

bot = Bot(db.session)
