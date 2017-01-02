from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

main = Blueprint('main', __name__, template_folder='templates')
db = SQLAlchemy()
from . import tdl_server
