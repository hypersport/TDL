# coding=utf-8
from flask import render_template, session, redirect, request, flash, url_for
from . import main, db
from models import Users, ToDoList
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LoginForm, AddUserForm


@main.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')


@main.route('/api')
def api():
    return render_template('api.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登陆成功')
            return redirect(url_for('main.index'))
        flash('登录失败')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('main.login'))


@main.route('/addtask')
@login_required
def add_task():
    pass


@main.route('/adduser', methods=['POST', 'GET'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     password=form.password.data)
        db.session.add(user)
        flash('添加成功')
        return redirect(url_for('main.login'))
    return render_template('adduser.html', form=form)
