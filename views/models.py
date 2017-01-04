from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todos = db.relationship('Users', backref=db.backref('todos', lazy='dynamic'))
    created_time = db.Column(db.DateTime, default=datetime.now())
    updated_time = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, content, owner_id, todos, updated_time=datetime.now(), is_done=False, is_deleted=False):
        self.content = content
        self.owner_id = owner_id
        self.updated_time = updated_time
        self.todos = todos
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
    password_hash = db.Column(db.String(128), nullable=False)
    permission = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, permission=False):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.permission = permission

    @property
    def password(self):
        raise AttributeError('Password is a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{self.username}, {self.permission}'.format(self=self)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
