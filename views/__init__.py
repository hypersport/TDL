from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_bootstrap import Bootstrap

main = Blueprint('main', __name__, template_folder='templates')
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
login_manager.login_message = '请登录账号'

from . import tdl_server
from . import tdl_client
