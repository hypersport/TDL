from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, default=datetime.now())
    updated_time = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, content, owner_id, updated_time=datetime.now(), is_done=False, is_deleted=False):
        self.content = content
        self.owner_id = owner_id
        self.updated_time = updated_time
        self.is_done = is_done
        self.is_deleted = is_deleted

    def __repr__(self):
        return '{}, {}, {}, {}, {}, {}, {}'.format(
            self.id,
            self.content,
            self.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            self.updated_time.strftime('%Y-%m-%d %H:%M:%S'),
            self.is_done,
            self.is_deleted,
            self.owner_id
        )


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    added_time = db.Column(db.DateTime, default=datetime.now())
    password_hash = db.Column(db.String(128), nullable=False)
    is_administrator = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_administrator=False):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_administrator = is_administrator

    @property
    def password(self):
        raise AttributeError('Password is a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.username, self.added_time.strftime('%Y-%m-%d %H:%M:%S'),
                                       self.is_administrator)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
