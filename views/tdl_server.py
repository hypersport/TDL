from flask import render_template, redirect, request, flash, url_for, abort
from . import main, db
from .models import Users, ToDoList
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LoginForm, AddUserForm, ToDoForm, ResetInfoForm
from datetime import datetime


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
    search_tag = request.form.get('search_tag', '')
    todos = ToDoList.query.filter_by(
        owner_id=current_user.id, is_deleted=False).filter(ToDoList.content.like('%' + search_tag + '%')).all()
    return render_template('index.html', todos=todos, search_tag=search_tag)


@main.route('/api')
def api():
    return render_template('api.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    user = Users.query.filter_by(id=1).first()
    if not user:
        user = Users(username='admin', password='admin', is_administrator=True)
        db.session.add(user)
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data, is_deleted=False).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登录成功')
            return redirect(request.args.get('next', '/') if request.args.get('next') != '/logout' else '/')
        flash('登录失败')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('main.index'))


@main.route('/chinfo', methods=['POST', 'GET'])
@login_required
def ch_info():
    form = ResetInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = form.password.data
        flash('密码修改成功')
        return redirect(url_for('main.index'))
    return render_template('chinfo.html', form=form)


@main.route('/addoredit/<int:todo_id>', methods=['POST', 'GET'])
@login_required
def add_or_edit(todo_id):
    form = ToDoForm()
    is_edit = 0
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for('main.index'))
        if todo_id:
            todo = ToDoList.query.get_or_404(todo_id)
            todo.content = form.todo_content.data
            todo.updated_time = datetime.now()
        else:
            todo = ToDoList(content=form.todo_content.data,
                            owner_id=current_user.id)
            db.session.add(todo)
        return redirect(url_for('main.index'))
    if todo_id:
        todo = ToDoList.query.get_or_404(todo_id)
        form.todo_content.data = todo.content
        is_edit = 1
    return render_template('addoredit.html', form=form, is_edit=is_edit)


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
        return redirect(url_for('main.index'))
    return render_template('adduser.html', form=form)


@main.route('/users', methods=['POST', 'GET'])
@login_required
def all_users():
    if not current_user.is_administrator:
        abort(403)
    users = Users.query.all()
    return render_template('users.html', users=users)


@main.route('/deluser', methods=['POST', 'GET'])
@login_required
def del_user():
    user_id = request.args.get('user_id', 0)
    if not current_user.is_administrator or user_id == 1:
        abort(403)
    user = Users.query.get_or_404(user_id)
    user.is_deleted = False if user.is_deleted else True
    return ''


@main.route('/chperm', methods=['POST', 'GET'])
@login_required
def ch_perm():
    user_id = request.args.get('user_id', 0)
    if not current_user.is_administrator or user_id == 1:
        abort(403)
    user = Users.query.get_or_404(user_id)
    user.is_administrator = False if user.is_administrator else True
    return ''


@main.route('/chstatus', methods=['POST', 'GET'])
@login_required
def ch_status():
    todo_id = request.args.get('todo_id', 0)
    todo = ToDoList.query.get_or_404(todo_id)
    if todo.owner_id != current_user.id:
        abort(403)
    todo.is_done = False if todo.is_done else True
    todo.updated_time = datetime.now()
    return ''


@main.route('/deltodo', methods=['POST', 'GET'])
@login_required
def del_todo():
    todo_id = request.args.get('todo_id', 0)
    todo = ToDoList.query.get_or_404(todo_id)
    if todo.owner_id != current_user.id:
        abort(403)
    todo.is_deleted = True
    return ''
