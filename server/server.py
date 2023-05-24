# Documentation https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/
from flask import Flask
from flask_marshmallow import Marshmallow

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

# Init Flask-Login
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Init Flask, DB, migrations and encryption
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()

def create_server():
    server = Flask(__name__)
    server.secret_key = "!EdH&Nv15Jx%I1m1PGCCu8@03waFObL$"
    server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    login_manager.init_app(server)
    db.init_app(server)
    migrate.init_app(server, db)
    bcrypt.init_app(server)
    return server