from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
login = LoginManager(app)
login.login_view = 'login'
migrate = Migrate(app, db)

# import routes for triumph-webapp and triumphapi for api's
from triumph import models, routes
