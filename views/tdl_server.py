# coding=utf-8
from flask import render_template, session, redirect, request, flash, url_for, abort
from . import main, db
from models import Users, ToDoList
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LoginForm, AddUserForm, ToDoForm


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


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
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('登录失败')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('main.index'))


@main.route('/addtodo', methods=['POST', 'GET'])
@login_required
def add_todo():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDoList(content=form.todo_content.data,
                        owner_id=current_user.id)
        db.session.add(todo)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('addtodo.html', form=form)


@main.route('/adduser', methods=['POST', 'GET'])
@login_required
def add_user():
    if not current_user.is_administrator:
        abort(403)
    form = AddUserForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     password=form.password.data,
                     is_administrator=form.is_administrator.data)
        db.session.add(user)
        flash('添加成功')
        return redirect(request.args.get('next') or url_for('main.login'))
    return render_template('adduser.html', form=form)
