from . import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config
from datetime import datetime

try:
    from colorama import Fore
except ImportError as e:
    class Fore(object):
        RED = ''
        GREEN = ''
        RESET = ''

engine = create_engine(config['default'].SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


class Client(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_id = 0
        self.dbs = Session()

    def check_user(self):
        admin = self.dbs.query(models.Users).filter_by(id=1).first()
        if not admin:
            admin = models.Users(username='admin', password='admin', is_administrator=True)
            self.dbs.add(admin)
            self.dbs.commit()
        user = self.dbs.query(models.Users).filter_by(username=self.username, is_deleted=False).first()
        if user and user.verify_password(self.password):
            self.user_id = user.id
            return True
        return False

    def ld(self):
        todos = self.dbs.query(models.ToDoList).filter_by(owner_id=self.user_id, is_deleted=0, is_done=1).all()
        return todos

    def lu(self):
        todos = self.dbs.query(models.ToDoList).filter_by(owner_id=self.user_id, is_deleted=False, is_done=False).all()
        return todos

    def ls(self):
        todos = self.dbs.query(models.ToDoList).filter_by(owner_id=self.user_id, is_deleted=False).all()
        return todos

    def la(self):
        todos = self.dbs.query(models.ToDoList).filter_by(owner_id=self.user_id).all()
        return todos

    def add(self, todo):
        todo = models.ToDoList(content=todo, owner_id=self.user_id, updated_time=datetime.now())
        self.dbs.add(todo)
        self.dbs.commit()

    def edit(self, num, todo_text):
        todo = self.dbs.query(models.ToDoList).filter_by(id=num, owner_id=self.user_id).first()
        if todo:
            todo.content = todo_text
            self.dbs.commit()
        else:
            print(Fore.RED + '无效的命令' + Fore.RESET)

    def done(self, num):
        todo = self.dbs.query(models.ToDoList).filter_by(id=num, owner_id=self.user_id).first()
        if todo:
            todo.is_done = True
            self.dbs.commit()
        else:
            print(Fore.RED + '无效的命令' + Fore.RESET)

    def undone(self, num):
        todo = self.dbs.query(models.ToDoList).filter_by(id=num, owner_id=self.user_id).first()
        if todo:
            todo.is_done = False
            self.dbs.commit()
        else:
            print(Fore.RED + '无效的命令' + Fore.RESET)

    def remove(self, num):
        todo = self.dbs.query(models.ToDoList).filter_by(id=num, owner_id=self.user_id).first()
        if todo:
            todo.is_deleted = True
            self.dbs.commit()
        else:
            print(Fore.RED + '无效的命令' + Fore.RESET)

    def search(self, search_tag):
        todos = self.dbs.query(models.ToDoList).filter_by(owner_id=self.user_id, is_deleted=0).filter(
            models.ToDoList.content.like('%' + search_tag + '%')).all()
        return todos

    def users(self):
        user = self.dbs.query(models.Users).get(self.user_id)
        if user.is_administrator:
            users = self.dbs.query(models.Users).all()
            return users
        else:
            print(Fore.RED + '无权限' + Fore.RESET)

    def add_user(self, username, password):
        user = self.dbs.query(models.Users).get(self.user_id)
        if user.is_administrator:
            add_user = self.dbs.query(models.Users).filter_by(username=username).first()
            if not add_user:
                add_user = models.Users(username=username, password=password)
                self.dbs.add(add_user)
                self.dbs.commit()
            else:
                print('用户名已存在')
        else:
            print(Fore.RED + '无权限' + Fore.RESET)

    def del_user(self, num):
        user = self.dbs.query(models.Users).get(self.user_id)
        if user.is_administrator:
            del_user = self.dbs.query(models.Users).filter_by(id=num, is_deleted=False).first()
            if del_user and del_user.id != 1:
                del_user.is_deleted = True
                self.dbs.commit()
            else:
                print(Fore.RED + '用户不存在或已删除' + Fore.RESET)
        else:
            print(Fore.RED + '无权限' + Fore.RESET)

    def ch_perm(self, num):
        user = self.dbs.query(models.Users).get(self.user_id)
        if user.is_administrator:
            ch_perm_user = self.dbs.query(models.Users).filter_by(id=num, is_deleted=False).first()
            if ch_perm_user and ch_perm_user.id != 1:
                ch_perm_user.is_administrator = False if ch_perm_user.is_administrator else True
                self.dbs.commit()
            else:
                print(Fore.RED + '用户不存在' + Fore.RESET)
        else:
            print(Fore.RED + '无权限' + Fore.RESET)
